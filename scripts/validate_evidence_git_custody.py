#!/usr/bin/env python3
"""Require claim-bearing evidence and release records to be committed.

This gate is intentionally post-commit.  A campaign disposition does not become
durable evidence merely because a JSON file exists in a working directory.
"""

from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROTECTED_ROOTS = ("evidence_transitions", "evidence_quality", "release_records")


def dirty_rows(porcelain: str) -> list[str]:
    """Return non-empty porcelain rows; kept separate for rejecting controls."""
    return [row for row in porcelain.splitlines() if row.strip()]


def git_porcelain() -> str:
    completed = subprocess.run(
        [
            "git",
            "status",
            "--porcelain=v1",
            "--untracked-files=all",
            "--",
            *PROTECTED_ROOTS,
        ],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return completed.stdout


def main() -> None:
    rows = dirty_rows(git_porcelain())
    controls = {
        "modified": " M evidence_quality/example.json",
        "staged": "M  evidence_transitions/example.json",
        "untracked": "?? release_records/example.json",
    }
    missed = [label for label, fixture in controls.items() if not dirty_rows(fixture)]
    if missed:
        raise SystemExit("Evidence git-custody negative controls failed: " + ", ".join(missed))
    if rows:
        raise SystemExit(
            "Evidence git custody failed. Claim-bearing evidence does not count until committed:\n - "
            + "\n - ".join(rows)
        )
    print(
        "Evidence git custody passed: evidence_transitions, evidence_quality, and "
        "release_records are committed and clean; 3/3 porcelain controls reject."
    )


if __name__ == "__main__":
    main()
