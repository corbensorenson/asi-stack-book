#!/usr/bin/env python3
"""Execute validation units from the declarative registry by tier."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation" / "registry.json"


def run(command: list[str]) -> None:
    print("+ " + " ".join(command), flush=True)
    completed = subprocess.run(command, cwd=ROOT)
    if completed.returncode:
        raise SystemExit(completed.returncode)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tier", choices=("pr", "deep", "release"), required=True)
    parser.add_argument("--list", action="store_true")
    args = parser.parse_args()
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    ranks = {tier: index for index, tier in enumerate(registry["tier_order"])}
    selected = [unit for unit in registry["units"] if ranks[unit["execution_tier"]] <= ranks[args.tier]]
    if args.list:
        for unit in selected:
            print(f"{unit['order']:03d} {unit['execution_tier']:7s} {unit['validation_class']:24s} {unit['script']} {' '.join(unit['args'])}")
        print(f"Selected {len(selected)} registry units for tier {args.tier}.")
        return
    run([sys.executable, str(ROOT / "scripts" / registry["base_gate"]["script"])])
    for unit in selected:
        run([sys.executable, str(ROOT / "scripts" / unit["script"]), *unit["args"]])
    print(f"Validation registry tier {args.tier} passed: base gate plus {len(selected)} units.")


if __name__ == "__main__":
    main()
