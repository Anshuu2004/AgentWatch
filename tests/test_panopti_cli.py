"""Unit tests for the Panopti CLI command center."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from panopti.cli import main
from panopti.court import WitnessChain


def test_cli_doctor_command(capsys: pytest.CaptureFixture[str]) -> None:
    """panopti doctor prints diagnostic report and banner."""
    ret = main(["doctor"])
    assert ret == 0
    captured = capsys.readouterr().out
    assert "PANOPTI RUNTIME DOCTOR" in captured
    assert "Overall Status" in captured


def test_cli_live_command(capsys: pytest.CaptureFixture[str]) -> None:
    """panopti top / live prints sentinel monitor."""
    ret = main(["live"])
    assert ret == 0
    captured = capsys.readouterr().out
    assert "PANOPTI SENTINEL [LIVE MONITOR]" in captured


def test_cli_court_verify_valid(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """panopti court verify confirms valid cryptographic proof."""
    chain = WitnessChain("test-cli-court")
    chain.record("agent", "action_1", {"key": "val"})
    proof = chain.export_proof()

    proof_file = tmp_path / "test_proof.json"
    proof_file.write_text(json.dumps(proof), encoding="utf-8")

    ret = main(["court", "verify", str(proof_file)])
    assert ret == 0
    captured = capsys.readouterr().out
    assert "VERIFIED: Witness proof" in captured
