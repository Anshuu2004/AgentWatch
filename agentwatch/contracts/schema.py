"""Schema for Evidence Sufficiency and Temporal Contract Verification (v3.1 EvidenceLab).

Defines typed contracts, 4-valued epistemic verdicts, missingness reasons,
and coverage profiles for open-world trace verification.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any


class EvidenceVerdict(StrEnum):
    """Four-valued epistemic verdict for open-world trace verification.

    Distinguishes observed facts from observational absence.
    """

    SUPPORTED = "supported"
    REFUTED = "refuted"
    INCONCLUSIVE = "inconclusive"
    CONFLICTING_EVIDENCE = "conflicting_evidence"


class ContractOperator(StrEnum):
    """Temporal contract operators supported in v3.1."""

    PRECEDING_EVENT = "preceding_event"
    EVENTUALLY_WITHIN = "eventually_within"


class MissingReason(StrEnum):
    """Taxonomy of why an expected fact was not observed."""

    SENSOR_DISABLED = "SENSOR_DISABLED"
    FIELD_ABSENT = "FIELD_ABSENT"
    SPAN_ORPHAN = "SPAN_ORPHAN"
    SEQUENCE_GAP = "SEQUENCE_GAP"
    CLOCK_AMBIGUITY = "CLOCK_AMBIGUITY"
    REDACTED = "REDACTED"
    SAMPLED_OUT = "SAMPLED_OUT"
    UNOBSERVABLE = "UNOBSERVABLE"


class Recoverability(StrEnum):
    """Whether a missing fact can be captured by adding instrumentation."""

    INSTRUMENTABLE = "INSTRUMENTABLE"
    MAYBE = "MAYBE"
    FUNDAMENTAL_LIMIT = "FUNDAMENTAL_LIMIT"


@dataclass(frozen=True, slots=True)
class MissingFact:
    """A specific piece of uncaptured telemetry required to resolve an ambiguity."""

    field_name: str
    reason: MissingReason
    required_for: str
    candidate_sensors: tuple[str, ...] = ()
    recoverability: Recoverability = Recoverability.INSTRUMENTABLE

    def to_dict(self) -> dict[str, Any]:
        return {
            "field": self.field_name,
            "reason": self.reason.value,
            "required_for": self.required_for,
            "candidate_sensors": list(self.candidate_sensors),
            "recoverability": self.recoverability.value,
        }


@dataclass(frozen=True, slots=True)
class ContractRule:
    """The temporal and correlation rule to verify."""

    operator: ContractOperator
    target_operation: str
    required_operation: str
    max_window_seconds: float = 600.0
    join_on: tuple[str, ...] = ("transaction_id",)


@dataclass(frozen=True, slots=True)
class EvidenceContract:
    """A versioned declarative contract governing expected agent behavior."""

    name: str
    version: str
    rule: ContractRule
    description: str = ""
    require_authoritative_log_for_refutation: bool = True


@dataclass(frozen=True, slots=True)
class CoverageSnapshot:
    """Attestation of sensor presence, authority, and completeness for an execution scope."""

    sensor_id: str
    authoritative_for: tuple[str, ...] = ()
    active: bool = True
    dropped_count: int = 0
    clock_uncertainty_ms: float = 0.0


@dataclass(frozen=True, slots=True)
class EvidenceAssessment:
    """Result of evaluating a contract over an execution trace.

    Carries minimal supporting or refuting witness IDs and missing facts.
    """

    contract_name: str
    verdict: EvidenceVerdict
    summary: str
    support_obs_ids: tuple[str, ...] = ()
    refute_obs_ids: tuple[str, ...] = ()
    missing_facts: tuple[MissingFact, ...] = ()
    remedies: tuple[str, ...] = ()
    assumptions: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "contract": self.contract_name,
            "verdict": self.verdict.value,
            "summary": self.summary,
            "support_obs_ids": list(self.support_obs_ids),
            "refute_obs_ids": list(self.refute_obs_ids),
            "missing_facts": [f.to_dict() for f in self.missing_facts],
            "remedies": list(self.remedies),
            "assumptions": list(self.assumptions),
        }
