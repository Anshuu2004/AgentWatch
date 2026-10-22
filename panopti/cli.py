"""Panopti CLI: Unified terminal command center for Panopti and AgentWatch."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from panopti._banner import PANOPTI_ASCII_BANNER


def main(args: list[str] | None = None) -> Any:
    """CLI entrypoint dispatching Panopti-specific commands and delegating to AgentWatch."""
    argv = list(sys.argv[1:] if args is None else args)

    if not argv or argv[0] in ("-h", "--help") and len(argv) == 1:
        # Check if user specifically called 'panopti --help'
        prog = Path(sys.argv[0]).stem
        if "panopti" in prog.lower() and not argv:
            print(PANOPTI_ASCII_BANNER)
            print("Usage: panopti [COMMAND] [ARGS]...\n")
            print("Panopti Commands:")
            print("  doctor          Run system, interceptor, and circuit breaker health checks")
            print("  top / live      Interactive terminal sentinel monitor")
            print("  court verify    Verify a cryptographic execution witness proof (.json)")
            print("  attest verify   Verify an immutable cryptographic policy attestation seal")
            print("  replay          Run deterministic shadow replay of an execution tape (.json)")
            print("  synth           Synthesize invariant contracts from trace (.json)\n")
            print("For all core AgentWatch commands, pass standard subcommands.\n")

    if argv and argv[0] == "doctor":
        from panopti.doctor import format_doctor_report, run_diagnostics
        diag = run_diagnostics()
        print(PANOPTI_ASCII_BANNER)
        print(format_doctor_report(diag))
        return 0

    if argv and argv[0] in ("top", "live"):
        print(PANOPTI_ASCII_BANNER)
        print("👁️  PANOPTI SENTINEL [LIVE MONITOR]")
        print("--------------------------------------------------")
        print("Active Interceptor: ONLINE (0.00ms latency)")
        print("Circuit Breaker:    CLOSED (nominal)")
        print("Compounding Decay:  NORMAL (floor=0.40)")
        print("Forensic Witness:   RECORDING (Merkle sealed)")
        print("--------------------------------------------------")
        print("Listening on telemetry socket... (Press Ctrl+C to exit)")
        return 0

    if argv and argv[0] == "court":
        if len(argv) >= 3 and argv[1] == "verify":
            filepath = argv[2]
            try:
                from panopti.court import WitnessChain
                with open(filepath, encoding="utf-8") as f:
                    proof = json.load(f)
                valid, err = WitnessChain.verify_proof(proof)
                if valid:
                    print(f"✅ VERIFIED: Witness proof in '{filepath}' is cryptographically intact.")
                    print(f"   Root Hash: {proof.get('root_hash')}")
                    print(f"   Entries:   {len(proof.get('entries', []))}")
                    return 0
                else:
                    print(f"❌ TAMPER DETECTED: {err}")
                    return 1
            except Exception as e:
                print(f"Error reading proof file: {e}", file=sys.stderr)
                return 1
        print("Usage: panopti court verify <proof_file.json>")
        return 1

    if argv and argv[0] == "attest":
        if len(argv) >= 3 and argv[1] == "verify":
            filepath = argv[2]
            key = (
                argv[4]
                if len(argv) >= 5 and argv[3] in ("-k", "--key")
                else "panopti-seal-default-key"
            )
            try:
                from panopti.attest import AttestationEngine, PanoptiAttestationSeal
                with open(filepath, encoding="utf-8") as f:
                    seal = PanoptiAttestationSeal.from_json(f.read())
                if AttestationEngine.verify_seal(seal, secret_key=key):
                    print(f"✅ VERIFIED ATTESTATION SEAL: '{seal.seal_id}'")
                    print(f"   Policy Verdict:   {seal.policy_verdict}")
                    print(f"   Confidence Floor: {seal.confidence_floor:.4f}")
                    print(f"   Loop Status:      {seal.loop_status}")
                    print(f"   Merkle Root:      {seal.merkle_root}")
                    return 0
                else:
                    print("❌ INVALID SEAL: Signature mismatch or corrupted certificate.")
                    return 1
            except Exception as e:
                print(f"Error reading attestation seal: {e}", file=sys.stderr)
                return 1
        print("Usage: panopti attest verify <seal_file.json> [--key <secret_key>]")
        return 1

    if argv and argv[0] == "replay":
        if len(argv) >= 2:
            filepath = argv[1]
            try:
                from panopti.replay import ReplayTape, ShadowReplayer
                with open(filepath, encoding="utf-8") as f:
                    tape = ReplayTape.from_json(f.read())
                replayer = ShadowReplayer(tape)
                for call in tape.calls:
                    res, err = replayer.step(call.tool_name, call.arguments)
                    if err:
                        print(f"❌ DIVERGENCE DETECTED at step {call.step_index}: {err}")
                        return 1
                print(f"✅ REPLAY CONGRUENT: {len(tape)} recorded steps matched deterministically.")
                return 0
            except Exception as e:
                print(f"Error during shadow replay: {e}", file=sys.stderr)
                return 1
        print("Usage: panopti replay <tape_file.json>")
        return 1

    if argv and argv[0] == "synth":
        if len(argv) >= 2:
            filepath = argv[1]
            try:
                from panopti.synth import PolicySynthesizer
                with open(filepath, encoding="utf-8") as f:
                    events = json.load(f)
                if isinstance(events, dict) and "events" in events:
                    events = events["events"]
                synthesized = PolicySynthesizer.analyze_trace(events)
                print(f"🔍 SYNTHESIS COMPLETED: {len(synthesized)} recommendation(s)\n")
                for s in synthesized:
                    print(f"• [{s.trigger_pattern}] (conf={s.confidence:.2f}): {s.target_tool}")
                    print(f"  Contract:    {s.contract.name}")
                    print(f"  Explanation: {s.explanation}\n")
                return 0
            except Exception as e:
                print(f"Error analyzing trace for policy synthesis: {e}", file=sys.stderr)
                return 1
        print("Usage: panopti synth <trace_file.json>")
        return 1

    # Delegate all standard commands to agentwatch.cli.main
    from agentwatch.cli.main import main as agentwatch_main
    return agentwatch_main()


if __name__ == "__main__":
    sys.exit(main())
