"""AgentWatch Temporal Contract and Evidence Sufficiency Module (v3.1 EvidenceLab)."""

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
)

__all__ = [
    "ContractOperator",
    "ContractRule",
    "CoverageSnapshot",
    "EvidenceAssessment",
    "EvidenceContract",
    "EvidenceVerdict",
    "MissingFact",
    "MissingReason",
    "Recoverability",
    "evaluate_contract",
    "get_remedy_for_missing_fact",
]
