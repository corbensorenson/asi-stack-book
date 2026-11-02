"""Select only a successful tested artifact whose commit is still main's head.

This read-only guard runs inside the serialized Pages job, before download and
again immediately before deployment. It does not authorize a release or build.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SHA = re.compile(r"^[0-9a-f]{40}$")


def decision(candidate: str, current: str) -> dict[str, str | bool]:
    if not SHA.fullmatch(candidate) or not SHA.fullmatch(current):
        raise ValueError("deployment selection requires exact lowercase commit identities")
    eligible = candidate == current
    return {"eligible": eligible, "candidate": candidate, "current_main": current,
            "reason": "current_main_head" if eligible else "superseded_by_main_head"}


def current_main() -> str:
    result = subprocess.run(
        ["git", "ls-remote", "--exit-code", "origin", "refs/heads/main"],
        cwd=ROOT, capture_output=True, text=True, timeout=30,
    )
    if result.returncode:
        raise ValueError("cannot read origin main; deployment selection fails closed")
    rows = [line.split() for line in result.stdout.splitlines() if line.strip()]
    if len(rows) != 1 or len(rows[0]) != 2 or rows[0][1] != "refs/heads/main":
        raise ValueError("origin main has an ambiguous or missing commit identity")
    return rows[0][0]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--github-output", type=Path)
    args = parser.parse_args()
    try:
        selected = decision(args.candidate, current_main())
    except (ValueError, subprocess.TimeoutExpired) as exc:
        raise SystemExit(str(exc)) from exc
    if args.github_output:
        with args.github_output.open("a", encoding="utf-8") as handle:
            handle.write(f"eligible={str(selected['eligible']).lower()}\n")
    print(json.dumps(selected, sort_keys=True))


if __name__ == "__main__":
    main()
