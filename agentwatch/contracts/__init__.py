"""AgentWatch Temporal Contract and Evidence Sufficiency Module (v3.1 EvidenceLab)."""

from agentwatch.contracts.coverage import (
    CoverageProfileRegistry,
    SequenceContinuityTracker,
    build_coverage_profile,
    parse_event_sequence,
)
from agentwatch.contracts.evaluator import evaluate_contract
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
    "ContractOperator",
    "ContractRule",
    "CoverageProfileRegistry",
    "CoverageSnapshot",
    "EvidenceAssessment",
    "EvidenceContract",
    "EvidenceVerdict",
    "MissingFact",
    "MissingReason",
    "Recoverability",
    "SequenceContinuityTracker",
    "SequenceGap",
    "build_coverage_profile",
    "evaluate_contract",
    "get_remedy_for_missing_fact",
    "parse_event_sequence",
]
