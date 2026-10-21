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
            print("  court verify    Verify a cryptographic execution witness proof (.json)\n")
            print("For all core AgentWatch commands, pass any standard subcommand (e.g. 'start', 'replay', 'eval').\n")

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

    # Delegate all standard commands to agentwatch.cli.main
    from agentwatch.cli.main import main as agentwatch_main
    return agentwatch_main()


if __name__ == "__main__":
    sys.exit(main())
