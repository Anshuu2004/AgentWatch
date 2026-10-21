"""Unit tests for Panopti Invariant Contracts."""

from __future__ import annotations

import pytest

from panopti import (
    ContractViolationError,
    Disallows,
    MaxFrequency,
    PanoptiGuard,
    RequiresPrior,
)


def test_requires_prior_contract_blocks_when_missing() -> None:
    """Target tool cannot execute if required prerequisite was never called."""
    g = PanoptiGuard()
    g.register_contract(RequiresPrior(target_tool="deploy", required_prior="run_tests"))

    decision = g.check("deploy", {"target": "prod"})
    assert decision.blocked is True
    assert "requires prior successful execution" in (decision.reason or "")


def test_requires_prior_contract_allows_after_prerequisite() -> None:
    """Target tool executes normally once prerequisite is recorded."""
    g = PanoptiGuard()
    g.register_contract(RequiresPrior(target_tool="deploy", required_prior="run_tests"))

    g.record_execution("run_tests", {"suite": "unit"})
    decision = g.check("deploy", {"target": "prod"})
    assert decision.allowed is True
    assert decision.blocked is False


def test_requires_prior_within_steps_expiry() -> None:
    """Prerequisite expires if too many intervening steps occur."""
    g = PanoptiGuard()
    g.register_contract(RequiresPrior(target_tool="commit", required_prior="lint", within_steps=2))

    g.record_execution("lint")
    g.record_execution("step_a")
    g.record_execution("step_b")
    g.record_execution("step_c")  # 3 steps since lint

    decision = g.check("commit")
    assert decision.blocked is True
    assert "within the last 2 steps" in (decision.reason or "")


def test_disallows_contract() -> None:
    """Tool registered with Disallows is unconditionally prevented."""
    g = PanoptiGuard()
    g.register_contract(Disallows("eval", reason="Eval is deprecated"))

    decision = g.check("eval")
    assert decision.blocked is True
    assert "Eval is deprecated" in (decision.reason or "")


def test_max_frequency_contract() -> None:
    """Tool invocation exceeding sliding window frequency is blocked."""
    g = PanoptiGuard()
    g.register_contract(MaxFrequency("query_api", max_invocations=2, window_steps=5))

    g.record_execution("query_api")
    g.record_execution("query_api")

    decision = g.check("query_api")
    assert decision.blocked is True
    assert "exceeded maximum frequency" in (decision.reason or "")


def test_tool_decorator_with_contract_enforcement() -> None:
    """@guard.tool enforces inline requires_prior contract and raises ContractViolationError."""
    g = PanoptiGuard()

    @g.tool(requires_prior="login")
    def transfer_funds(account: str, amount: float) -> str:
        return f"transferred {amount} to {account}"

    with pytest.raises(ContractViolationError) as exc_info:
        transfer_funds("acc_123", 500.0)

    assert "requires prior successful execution of 'login'" in str(exc_info.value)
