"""Unit tests for Panopti Cryptographic Policy Attestation Seals."""

from __future__ import annotations

from panopti.attest import AttestationEngine, PanoptiAttestationSeal


def test_attestation_seal_generation_and_verification() -> None:
    merkle_root = "abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890"
    seal = AttestationEngine.create_seal(
        merkle_root=merkle_root,
        tool_count=5,
        confidence_floor=0.88,
        is_compliant=True,
        loop_detected=False,
        secret_key="my-audit-secret",
    )

    assert seal.seal_id.startswith("seal_")
    assert seal.policy_verdict == "COMPLIANT"
    assert seal.loop_status == "CLEAN"
    assert seal.tool_count == 5
    assert seal.confidence_floor == 0.88

    # Verify signature
    assert AttestationEngine.verify_seal(seal, secret_key="my-audit-secret") is True


def test_attestation_seal_tamper_detection() -> None:
    seal = AttestationEngine.create_seal(
        merkle_root="root_hash_value",
        tool_count=3,
        secret_key="secret-key",
    )

    # Tampered verdict
    tampered_verdict = PanoptiAttestationSeal(
        seal_id=seal.seal_id,
        merkle_root=seal.merkle_root,
        policy_verdict="VIOLATION",  # Tampered!
        confidence_floor=seal.confidence_floor,
        loop_status=seal.loop_status,
        tool_count=seal.tool_count,
        timestamp_iso=seal.timestamp_iso,
        signature=seal.signature,
    )
    assert AttestationEngine.verify_seal(tampered_verdict, secret_key="secret-key") is False

    # Tampered secret key
    assert AttestationEngine.verify_seal(seal, secret_key="wrong-secret-key") is False


def test_attestation_seal_json_roundtrip() -> None:
    seal = AttestationEngine.create_seal(
        merkle_root="0000aaaa1111bbbb",
        tool_count=10,
        confidence_floor=0.92,
        is_compliant=True,
        loop_detected=False,
    )

    json_str = seal.to_json()
    restored = PanoptiAttestationSeal.from_json(json_str)

    assert restored.seal_id == seal.seal_id
    assert restored.merkle_root == seal.merkle_root
    assert restored.signature == seal.signature
    assert AttestationEngine.verify_seal(restored) is True
