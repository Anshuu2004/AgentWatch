"""Evaluator for Evidence Sufficiency and Temporal Contracts.

Executes open-world temporal verification over ComputationalEvents,
extracting minimal witnesses and identifying unobserved facts without false alarms.
"""

from __future__ import annotations

from collections.abc import Sequence

from agentwatch.contracts.remedies import get_remedy_for_missing_fact
from agentwatch.contracts.schema import (
    ContractOperator,
    CoverageSnapshot,
    EvidenceAssessment,
    EvidenceContract,
    EvidenceVerdict,
    MissingFact,
    MissingReason,
    Recoverability,
)
from agentwatch.events.model import ComputationalEvent


def evaluate_contract(
    events: Sequence[ComputationalEvent],
    contract: EvidenceContract,
    coverage: Sequence[CoverageSnapshot] = (),
) -> EvidenceAssessment:
    """Evaluate an EvidenceContract against an execution trace.

    ponytail: pure function, no database lookups or external network calls.
    Returns minimal witness observation IDs and exact missing telemetry gaps.
    """
    rule = contract.rule
    target_events = [e for e in events if e.operation == rule.target_operation]

    if not target_events:
        return EvidenceAssessment(
            contract_name=contract.name,
            verdict=EvidenceVerdict.SUPPORTED,
            summary=f"No target operations ('{rule.target_operation}') occurred; contract vacuously satisfied.",
            assumptions=("Vacuous satisfaction over empty target set",),
        )

    # Index coverage by authoritative operations
    authoritative_sensors = {
        sensor.sensor_id: sensor
        for sensor in coverage
        if sensor.active
        and sensor.dropped_count == 0
        and rule.required_operation in sensor.authoritative_for
    }

    # Extract max clock uncertainty across sensors and events
    max_clock_uncertainty_ms = max(
        [s.clock_uncertainty_ms for s in coverage]
        + [e.time.uncertainty_ms or 0.0 for e in events]
        + [0.0]
    )

    all_support_obs: list[str] = []
    all_refute_obs: list[str] = []
    missing_facts: list[MissingFact] = []
    remedies: list[str] = []

    for target in target_events:
        # Resolve join key value (e.g. transaction_id)
        target_attrs = target.attributes
        join_key = rule.join_on[0] if rule.join_on else None
        join_val = target_attrs.get(join_key) if join_key else None

        # Find matching candidate required events
        candidates = [
            e
            for e in events
            if e.operation == rule.required_operation
            and (join_key is None or e.attributes.get(join_key) == join_val)
        ]

        if not candidates:
            # Open-world determination: was absence authoritatively captured?
            if authoritative_sensors and contract.require_authoritative_log_for_refutation:
                sensor_names = ", ".join(authoritative_sensors.keys())
                all_refute_obs.extend(target.derived_from)
                return EvidenceAssessment(
                    contract_name=contract.name,
                    verdict=EvidenceVerdict.REFUTED,
                    summary=(
                        f"Refuted: target '{rule.target_operation}' executed without required '{rule.required_operation}'. "
                        f"Authoritative sensors ({sensor_names}) attest complete coverage with zero dropped events."
                    ),
                    refute_obs_ids=tuple(dict.fromkeys(all_refute_obs)),
                    assumptions=(
                        f"Authoritative log completeness for '{rule.required_operation}' attested by {sensor_names}",
                    ),
                )
            else:
                # Missing telemetry: inconclusive, NOT a false alarm
                fact = MissingFact(
                    field_name=join_key or "event_id",
                    reason=MissingReason.SENSOR_DISABLED
                    if not coverage
                    else MissingReason.FIELD_ABSENT,
                    required_for=rule.required_operation,
                    candidate_sensors=(f"{rule.required_operation}_sensor",),
                    recoverability=Recoverability.INSTRUMENTABLE,
                )
                missing_facts.append(fact)
                remedies.append(get_remedy_for_missing_fact(fact))
                return EvidenceAssessment(
                    contract_name=contract.name,
                    verdict=EvidenceVerdict.INCONCLUSIVE,
                    summary=(
                        f"Inconclusive: target '{rule.target_operation}' was observed, but required '{rule.required_operation}' "
                        f"cannot be proven or refuted because no authoritative sensor attests its absence."
                    ),
                    missing_facts=tuple(missing_facts),
                    remedies=tuple(remedies),
                    assumptions=(
                        "Open-world assumption: absence of evidence is not evidence of absence",
                    ),
                )

        # Candidate found - verify temporal contract
        for req in candidates:
            req_time = req.time.start
            target_time = target.time.start

            if req_time is None or target_time is None:
                fact = MissingFact(
                    field_name="timestamp",
                    reason=MissingReason.FIELD_ABSENT,
                    required_for=rule.required_operation,
                    recoverability=Recoverability.INSTRUMENTABLE,
                )
                missing_facts.append(fact)
                remedies.append(get_remedy_for_missing_fact(fact))
                return EvidenceAssessment(
                    contract_name=contract.name,
                    verdict=EvidenceVerdict.INCONCLUSIVE,
                    summary="Inconclusive: one or more events lack valid start timestamps.",
                    missing_facts=tuple(missing_facts),
                    remedies=tuple(remedies),
                )

            # Check clock ambiguity
            diff_ms = abs((target_time - req_time).total_seconds() * 1000.0)
            has_causal_link = any(
                p.value in [sid[1] for sid in req.source_ids] for p in target.parents
            )

            if (
                max_clock_uncertainty_ms > 0
                and diff_ms <= max_clock_uncertainty_ms
                and not has_causal_link
            ):
                return EvidenceAssessment(
                    contract_name=contract.name,
                    verdict=EvidenceVerdict.CONFLICTING_EVIDENCE,
                    summary=(
                        f"Conflicting evidence: time difference ({diff_ms:.1f}ms) between events is within clock "
                        f"uncertainty threshold ({max_clock_uncertainty_ms:.1f}ms) with no explicit parent span link."
                    ),
                    support_obs_ids=tuple(dict.fromkeys(target.derived_from + req.derived_from)),
                    assumptions=(
                        f"Clock uncertainty of {max_clock_uncertainty_ms}ms prevents definitive ordering",
                    ),
                )

            if rule.operator == ContractOperator.PRECEDING_EVENT:
                delta_sec = (target_time - req_time).total_seconds()
                if delta_sec < 0:
                    # Occurred after target!
                    all_refute_obs.extend(target.derived_from + req.derived_from)
                    return EvidenceAssessment(
                        contract_name=contract.name,
                        verdict=EvidenceVerdict.REFUTED,
                        summary=f"Refuted: '{rule.required_operation}' occurred after '{rule.target_operation}' (delta: {delta_sec:.2f}s).",
                        refute_obs_ids=tuple(dict.fromkeys(all_refute_obs)),
                    )
                if delta_sec > rule.max_window_seconds:
                    all_refute_obs.extend(target.derived_from + req.derived_from)
                    return EvidenceAssessment(
                        contract_name=contract.name,
                        verdict=EvidenceVerdict.REFUTED,
                        summary=(
                            f"Refuted: '{rule.required_operation}' preceded target but exceeded max allowed window "
                            f"({delta_sec:.1f}s > {rule.max_window_seconds:.1f}s)."
                        ),
                        refute_obs_ids=tuple(dict.fromkeys(all_refute_obs)),
                    )

                # Preceding event satisfied!
                all_support_obs.extend(target.derived_from + req.derived_from)

            elif rule.operator == ContractOperator.EVENTUALLY_WITHIN:
                delta_sec = (req_time - target_time).total_seconds()
                if delta_sec < 0:
                    all_refute_obs.extend(target.derived_from + req.derived_from)
                    return EvidenceAssessment(
                        contract_name=contract.name,
                        verdict=EvidenceVerdict.REFUTED,
                        summary=f"Refuted: '{rule.required_operation}' occurred before target when expected after.",
                        refute_obs_ids=tuple(dict.fromkeys(all_refute_obs)),
                    )
                if delta_sec > rule.max_window_seconds:
                    all_refute_obs.extend(target.derived_from + req.derived_from)
                    return EvidenceAssessment(
                        contract_name=contract.name,
                        verdict=EvidenceVerdict.REFUTED,
                        summary=f"Refuted: '{rule.required_operation}' exceeded max follow-up window ({delta_sec:.1f}s).",
                        refute_obs_ids=tuple(dict.fromkeys(all_refute_obs)),
                    )

                all_support_obs.extend(target.derived_from + req.derived_from)

    return EvidenceAssessment(
        contract_name=contract.name,
        verdict=EvidenceVerdict.SUPPORTED,
        summary=f"Supported: all target operations satisfy contract '{contract.name}' with verified witnesses.",
        support_obs_ids=tuple(dict.fromkeys(all_support_obs)),
        assumptions=("Temporal constraints verified over observable execution witness",),
    )
