"""Panopti Guard: Modern decorator and pre-execution interceptor for AI agent tools."""

from __future__ import annotations

import functools
import inspect
import logging
from dataclasses import dataclass
from typing import Any, Callable, TypeVar

from agentwatch.circuit_breaker.loop_detector import AgentLoopError, LoopDetector
from agentwatch.core.safety import SafetyEngine
from agentwatch.core.schema import ToolCallData
from agentwatch.core.watcher import AgentWatchBlockedError, watch
from panopti.contracts import (
    Contract,
    ContractRegistry,
    ContractViolationError,
    Disallows,
    MaxFrequency,
    RequiresPrior,
)

logger = logging.getLogger("panopti.guard")

F = TypeVar("F", bound=Callable[..., Any])


@dataclass(frozen=True)
class GuardDecision:
    """Pre-execution assessment result for a proposed tool action."""

    allowed: bool
    blocked: bool
    risk_level: str
    risk_score: float
    reason: str | None
    reasons: list[str]


class PanoptiGuard:
    """Active runtime guardrail engine."""

    def __init__(self) -> None:
        self._safety_engine = SafetyEngine()
        self._loop_detector = LoopDetector(window_size=10, max_repeats=3, max_oscillations=2)
        self._contracts = ContractRegistry()

    def register_contract(self, contract: Contract) -> None:
        """Register a temporal or state invariant contract."""
        self._contracts.add(contract)

    def record_execution(
        self, tool_name: str, arguments: dict[str, Any] | None = None
    ) -> None:
        """Record successful tool execution in history for temporal contract tracking."""
        self._contracts.record_success(tool_name, arguments)

    def check(
        self, tool_name: str, arguments: dict[str, Any] | None = None
    ) -> GuardDecision:
        """Evaluate a tool invocation against safety policies, contracts, and loops before execution."""
        args = arguments or {}

        # 1. Loop and oscillation check
        loop_warning = self._loop_detector.record(tool_name, args)
        if loop_warning:
            return GuardDecision(
                allowed=False,
                blocked=True,
                risk_level="CRITICAL",
                risk_score=1.0,
                reason=loop_warning,
                reasons=[loop_warning],
            )

        # 2. Invariant contracts check
        contract_allowed, contract_violation = self._contracts.evaluate(tool_name, args)
        if not contract_allowed:
            return GuardDecision(
                allowed=False,
                blocked=True,
                risk_level="HIGH",
                risk_score=0.9,
                reason=contract_violation,
                reasons=[contract_violation or "Contract violation"],
            )

        # 3. Safety policy check
        raw_cmd = args.get("cmd") or args.get("command") or args.get("script") or None
        tool_data = ToolCallData(
            tool_name=tool_name,
            arguments=args,
            raw_command=str(raw_cmd) if raw_cmd else None,
        )
        safety_result = self._safety_engine.evaluate(tool_data)

        risk_val = (
            safety_result.risk_level.value
            if hasattr(safety_result.risk_level, "value")
            else str(safety_result.risk_level)
        ).upper()

        if safety_result.blocked:
            reason = (
                safety_result.reasons[0]
                if safety_result.reasons
                else "Action blocked by safety policy"
            )
            return GuardDecision(
                allowed=False,
                blocked=True,
                risk_level=risk_val,
                risk_score=safety_result.risk_score,
                reason=reason,
                reasons=safety_result.reasons,
            )

        return GuardDecision(
            allowed=True,
            blocked=False,
            risk_level=risk_val,
            risk_score=safety_result.risk_score,
            reason=None,
            reasons=[],
        )

    def tool(
        self,
        name: str | None = None,
        *,
        max_repeats: int = 3,
        requires_prior: str | None = None,
        max_frequency: tuple[int, int] | None = None,
        raise_on_block: bool = True,
    ) -> Callable[[F], F]:
        """Decorator shielding a tool function with pre-execution safety and invariant contracts."""

        def decorator(fn: F) -> F:
            tool_name = name or fn.__name__
            sig = inspect.signature(fn)

            if requires_prior:
                self.register_contract(RequiresPrior(tool_name, requires_prior))
            if max_frequency:
                max_invocations, window_steps = max_frequency
                self.register_contract(
                    MaxFrequency(tool_name, max_invocations=max_invocations, window_steps=window_steps)
                )

            @functools.wraps(fn)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                bound = sig.bind_partial(*args, **kwargs)
                bound.apply_defaults()
                arguments = bound.arguments

                decision = self.check(tool_name, arguments)
                if decision.blocked:
                    reason_lower = (decision.reason or "").lower()
                    if "loop detected" in reason_lower or "oscillation" in reason_lower:
                        if raise_on_block:
                            raise AgentLoopError(
                                decision.reason or "Loop detected",
                                pattern=tool_name,
                                occurrences=max_repeats,
                            )
                    if "contract violation" in reason_lower:
                        if raise_on_block:
                            raise ContractViolationError(
                                decision.reason or "Contract violation",
                                contract_name=tool_name,
                                tool_name=tool_name,
                            )
                    if raise_on_block:
                        raise AgentWatchBlockedError(
                            decision.reason or "Blocked by Panopti",
                            tool_name=tool_name,
                            reasons=decision.reasons,
                        )
                    return {"error": decision.reason, "blocked": True}

                result = fn(*args, **kwargs)
                self.record_execution(tool_name, arguments)
                return result

            return wrapper  # type: ignore[return-value]

        return decorator

    @staticmethod
    def watch(agent: Any) -> Any:
        """Attach universal passive/active instrumentation to any supported agent framework."""
        return watch(agent)


# Default singleton instance
guard = PanoptiGuard()
