"""AgentWatch Temporal Contract and Evidence Sufficiency Module (v3.1 EvidenceLab)."""

from agentwatch.contracts.coverage import (
    CoverageProfileRegistry,
    SequenceContinuityTracker,
    build_coverage_profile,
    parse_event_sequence,
)
from agentwatch.contracts.evaluator import evaluate_contract
from agentwatch.contracts.order import (
    CausalCycleError,
    CausalRelation,
    EventTimeWatermarkBuffer,
    HappensBeforeGraph,
    IngestionResult,
    IngestionStatus,
    IntervalPrecedence,
    TimestampInterval,
)
from agentwatch.contracts.remedies import get_remedy_for_missing_fact
from agentwatch.contracts.schema import (
    ContractOperator,
    ContractRule,
    CoverageSnapshot,
    EvidenceAssessment,
    EvidenceContract,
    EvidenceVerdict,
    MissingFact,
    MissingReason,
    Recoverability,
    SequenceGap,
)

__all__ = [
    "CausalCycleError",
    "CausalRelation",
    "ContractOperator",
    "ContractRule",
    "CoverageProfileRegistry",
    "CoverageSnapshot",
    "EventTimeWatermarkBuffer",
    "EvidenceAssessment",
    "EvidenceContract",
    "EvidenceVerdict",
    "HappensBeforeGraph",
    "IngestionResult",
    "IngestionStatus",
    "IntervalPrecedence",
    "MissingFact",
    "MissingReason",
    "Recoverability",
    "SequenceContinuityTracker",
    "SequenceGap",
    "TimestampInterval",
    "build_coverage_profile",
    "evaluate_contract",
    "get_remedy_for_missing_fact",
    "parse_event_sequence",
]
