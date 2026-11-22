#!/usr/bin/env python3
"""Replay one retained instrument audit from an extracted standalone kit."""

import argparse
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent


def verify_members():
    for row in (ROOT / "SHA256SUMS").read_text().splitlines():
        expected, name = row.split("  ", 1)
        path = ROOT / name
        if not path.resolve().is_relative_to(ROOT) or sha256(path.read_bytes()).hexdigest() != expected:
            raise SystemExit(f"Replay kit member changed: {name}")


def main():
    records = json.loads((ROOT / "replays.json").read_text())
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", choices=tuple(records))
    parser.add_argument("--vary", action="store_true", help="Run the documented follow-up or reanalysis")
    args = parser.parse_args()
    verify_members()
    run = records[args.run]
    if args.vary:
        if run.get("variation"):
            subprocess.run([sys.executable, run["variation"]], cwd=ROOT, check=True)
        else:
            result = json.loads((ROOT / run["result"]).read_bytes())
            if args.run == "receiver-availability":
                rows = {}
                for primary, secondary in (("fresh", "fresh"), ("stale", "fresh"), ("unavailable", "unavailable")):
                    cases = [pair for pair in result["pairs"]
                             if (pair["primary"], pair["secondary"]) == (primary, secondary)]
                    rows[f"{primary}/{secondary}"] = {
                        arm: sum(pair["arms"][arm]["verified_closure"] for pair in cases)
                        for arm in cases[0]["arms"]
                    }
                print(json.dumps(rows, indent=2))
            elif args.run == "git-retrospective":
                rows = [row for row in result["trials"] if row["path"] == "external_effect_compensation"]
                print(json.dumps({
                    row["route"]: {"restores_and_retains": row["compensation_verified"],
                                   "passes_main_ancestry_policy": row["compensation_verified"]
                                   and row["effect_is_ancestor_of_tip"]}
                    for row in rows
                }, indent=2))
            else:
                selected = ("proposals/descriptive", "expanded/descriptive", "expanded/neutral")
                print(json.dumps({key: result["summary"][key] for key in selected}, indent=2))
        return
    actual = subprocess.check_output([sys.executable, *run["python_args"]], cwd=ROOT)
    expected = (ROOT / run["result"]).read_bytes()
    digest = sha256(actual).hexdigest()
    if actual != expected or digest != run["result_sha256"]:
        raise SystemExit(f"{args.run} differed from its pinned result. Observed SHA-256 {digest}.")
    print(f"{args.run} reproduced its pinned result. SHA-256 {digest}.")


if __name__ == "__main__":
    main()
