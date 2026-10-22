"""Panopti Autonomous Policy Synthesizer.

Analyzes execution traces to automatically synthesize formal invariant contracts
(MaxFrequency, Disallows, RequiresPrior) to prevent future runaway loops or thrashing.
Pure standard library (Ponytail: Ultra).
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any

from panopti.contracts import (
    Contract,
    Disallows,
    MaxFrequency,
)


@dataclass(slots=True)
class SynthesizedInvariant:
    """A formal invariant contract synthesized from an observed execution anomaly."""

    trigger_pattern: str
    target_tool: str
    confidence: float
    contract: Contract
    explanation: str


class PolicySynthesizer:
    """Analyzes agent trace history to synthesize self-healing invariant contracts."""

    @classmethod
    def analyze_trace(
        cls,
        events: list[dict[str, Any]],
    ) -> list[SynthesizedInvariant]:
        """Inspect trace events and synthesize invariant contracts.

        Args:
            events: List of event dicts containing at least 'tool_name' and optionally
                    'error', 'arguments', and 'success'.
        """
        synthesized: list[SynthesizedInvariant] = []
        if not events:
            return synthesized

        tool_sequence = [e.get("tool_name", "") for e in events if e.get("tool_name")]

        # 1. Detect repetitive tool hammering
        for tool, count in Counter(tool_sequence).items():
            if count >= 3:
                # Find maximum frequency within any 5-step window
                max_window_count = 0
                for i in range(len(tool_sequence)):
                    window = tool_sequence[i : i + 5]
                    max_window_count = max(max_window_count, window.count(tool))

                if max_window_count >= 3:
                    synthesized.append(
                        SynthesizedInvariant(
                            trigger_pattern="REPETITIVE_HAMMERING",
                            target_tool=tool,
                            confidence=0.95,
                            contract=MaxFrequency(
                                target_tool=tool,
                                max_invocations=2,
                                window_steps=5,
                                custom_message=(
                                    f"Synthesized constraint: tool '{tool}' exceeded frequency "
                                    f"ceiling (observed {max_window_count} calls in 5-step window)"
                                ),
                            ),
                            explanation=(
                                f"Observed {max_window_count} calls to '{tool}' within 5 steps; "
                                f"synthesized MaxFrequency(2, window=5) to clamp execution rate."
                            ),
                        )
                    )

        # 2. Detect 2-step oscillation (A -> B -> A -> B)
        if len(tool_sequence) >= 4:
            for i in range(len(tool_sequence) - 3):
                t1, t2, t3, t4 = (
                    tool_sequence[i],
                    tool_sequence[i + 1],
                    tool_sequence[i + 2],
                    tool_sequence[i + 3],
                )
                if t1 == t3 and t2 == t4 and t1 != t2:
                    synthesized.append(
                        SynthesizedInvariant(
                            trigger_pattern="OSCILLATION_TRAP",
                            target_tool=t1,
                            confidence=0.90,
                            contract=MaxFrequency(
                                target_tool=t1,
                                max_invocations=1,
                                window_steps=3,
                                custom_message=(
                                    f"Synthesized constraint: oscillation trap detected between "
                                    f"'{t1}' and '{t2}'"
                                ),
                            ),
                            explanation=(
                                f"Detected alternating execution pattern ({t1} -> {t2} -> {t1}); "
                                f"synthesized rate clamp on '{t1}' to break cycle."
                            ),
                        )
                    )
                    break

        # 3. Detect consecutive failing tool calls
        consecutive_failures: dict[str, int] = {}
        for event in events:
            tool = event.get("tool_name", "")
            if not tool:
                continue
            is_failure = bool(event.get("error")) or not event.get("success", True)
            if is_failure:
                consecutive_failures[tool] = consecutive_failures.get(tool, 0) + 1
                if consecutive_failures[tool] >= 2:
                    synthesized.append(
                        SynthesizedInvariant(
                            trigger_pattern="REPEATED_TOOL_FAILURE",
                            target_tool=tool,
                            confidence=0.98,
                            contract=Disallows(
                                target_tool=tool,
                                reason=(
                                    f"Automated policy shutdown: tool '{tool}' failed repeatedly "
                                    f"({consecutive_failures[tool]} consecutive errors)"
                                ),
                            ),
                            explanation=(
                                f"Tool '{tool}' produced consecutive errors; "
                                f"synthesized Disallows contract to prevent fault cascade."
                            ),
                        )
                    )
                    consecutive_failures[tool] = 0
            else:
                consecutive_failures[tool] = 0

        return synthesized
