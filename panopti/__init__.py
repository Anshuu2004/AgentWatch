"""Panopti: The All-Seeing Pre-Execution Guardrail & Forensic Engine for Autonomous AI.

Panopti is the successor to AgentWatch, providing pre-execution contract verification,
causal confidence decay tracking, and deterministic forensic shadow replay for agent swarms.
"""

from __future__ import annotations

from agentwatch._version import __version__

try:
    from agentwatch.circuit_breaker import (
        AgentLoopException,
        CircuitBreaker,
        CircuitState,
        CircuitThresholds,
        LoopDetector,
        TripReason,
    )
    from agentwatch.core.watcher import (
        AgentWatchBlockedError,
        GenericAdapter,
        detect_framework,
        detect_framework_label,
        watch,
    )

    PanoptiBlockedError = AgentWatchBlockedError
    guard = watch
except ImportError:  # pragma: no cover
    # Dependencies not fully installed in current environment
    watch = None  # type: ignore[assignment]
    guard = None  # type: ignore[assignment]
    detect_framework = None  # type: ignore[assignment]
    detect_framework_label = None  # type: ignore[assignment]
    GenericAdapter = None  # type: ignore[assignment]
    AgentWatchBlockedError = Exception  # type: ignore[assignment,misc]
    PanoptiBlockedError = AgentWatchBlockedError
    CircuitBreaker = None  # type: ignore[assignment]
    CircuitState = None  # type: ignore[assignment]
    CircuitThresholds = None  # type: ignore[assignment]
    TripReason = None  # type: ignore[assignment]
    LoopDetector = None  # type: ignore[assignment]
    AgentLoopException = Exception  # type: ignore[assignment,misc]

__all__ = [
    "__version__",
    "guard",
    "watch",
    "detect_framework",
    "detect_framework_label",
    "GenericAdapter",
    "PanoptiBlockedError",
    "AgentWatchBlockedError",
    "CircuitBreaker",
    "CircuitState",
    "CircuitThresholds",
    "TripReason",
    "LoopDetector",
    "AgentLoopException",
]
