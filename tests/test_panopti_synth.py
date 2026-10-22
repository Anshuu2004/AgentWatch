"""Unit tests for Panopti Autonomous Policy Synthesizer."""

from __future__ import annotations

from panopti.contracts import ExecutionEvent
from panopti.synth import PolicySynthesizer


def test_synth_detects_repetitive_tool_hammering() -> None:
    events = [
        {"tool_name": "fetch_api", "arguments": {"q": "1"}, "success": True},
        {"tool_name": "fetch_api", "arguments": {"q": "2"}, "success": True},
        {"tool_name": "fetch_api", "arguments": {"q": "3"}, "success": True},
    ]
    remedies = PolicySynthesizer.analyze_trace(events)
    assert len(remedies) == 1
    assert remedies[0].trigger_pattern == "REPETITIVE_HAMMERING"
    assert remedies[0].target_tool == "fetch_api"

    # Evaluate the synthesized contract against a history of 2 prior calls
    contract = remedies[0].contract
    history = [
        ExecutionEvent(step=0, tool_name="fetch_api", arguments={}),
        ExecutionEvent(step=1, tool_name="fetch_api", arguments={}),
    ]
    # 3rd invocation must be blocked by the synthesized contract
    allowed, err = contract.evaluate("fetch_api", {}, history)
    assert allowed is False
    assert "exceeded frequency ceiling" in (err or "")


def test_synth_detects_oscillation_trap() -> None:
    events = [
        {"tool_name": "state_a"},
        {"tool_name": "state_b"},
        {"tool_name": "state_a"},
        {"tool_name": "state_b"},
    ]
    remedies = PolicySynthesizer.analyze_trace(events)
    assert len(remedies) >= 1
    patterns = [r.trigger_pattern for r in remedies]
    assert "OSCILLATION_TRAP" in patterns


def test_synth_detects_repeated_consecutive_failures() -> None:
    events = [
        {"tool_name": "unstable_endpoint", "error": "500 Internal Error"},
        {"tool_name": "unstable_endpoint", "error": "503 Service Unavailable"},
    ]
    remedies = PolicySynthesizer.analyze_trace(events)
    assert len(remedies) == 1
    assert remedies[0].trigger_pattern == "REPEATED_TOOL_FAILURE"
    assert remedies[0].target_tool == "unstable_endpoint"

    contract = remedies[0].contract
    allowed, err = contract.evaluate("unstable_endpoint", {}, [])
    assert allowed is False
    assert "failed repeatedly" in (err or "")
