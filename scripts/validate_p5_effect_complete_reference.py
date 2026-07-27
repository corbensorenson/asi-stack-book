#!/usr/bin/env python3
"""Independently replay and validate the P5 local reference slice."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "experiments/effect_complete_reference/results/2026-07-27-local.json"
SCHEMA = ROOT / "schemas/effect_complete_reference_result.schema.json"
RUNNER = ROOT / "scripts/run_p5_effect_complete_reference.py"
REPORT = ROOT / "docs/p5_effect_complete_reference_report.md"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    failures: list[str] = []
    with tempfile.TemporaryDirectory(prefix="asi-p5-validation-") as directory:
        replay = Path(directory) / "result.json"
        completed = subprocess.run(
            [sys.executable, str(RUNNER), "--output", str(replay)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            timeout=90,
        )
        if completed.returncode:
            failures.append(f"runner failed: {completed.stderr or completed.stdout}")
        elif load(replay) != load(RESULT):
            failures.append("tracked result differs from independent fresh replay")
    result = load(RESULT)
    schema_errors = sorted(
        Draft202012Validator(load(SCHEMA)).iter_errors(result),
        key=lambda error: list(error.path),
    )
    failures.extend(f"schema: {error.message}" for error in schema_errors)
    ids = [receipt["case_id"] for receipt in result.get("receipts", [])]
    if len(ids) != len(set(ids)) or set(ids) != {
        "nominal-observe-exact-rollback",
        "concurrent-idempotent-effect",
        "revocation-defeats-stale-cache",
        "crash-after-effect-before-receipt",
        "irreversible-effect-compensation",
        "prospective-full-state-checkpoint",
        "descendant-aware-deletion",
        "scope-escape-rejected",
    }:
        failures.append("case denominator or identity drifted")
    if not all(receipt.get("passed") is True for receipt in result.get("receipts", [])):
        failures.append("one or more cases did not pass")
    if result.get("support_state_effect") != "none" or result.get("release_effect") != "none":
        failures.append("local reference slice laundered support or release state")
    report = REPORT.read_text(encoding="utf-8")
    for phrase in (
        "real subprocesses",
        "not a deployed AI service",
        "causal influence reduction",
        "P5 remains in progress",
    ):
        if phrase not in report:
            failures.append(f"report boundary missing: {phrase}")
    if failures:
        raise SystemExit(
            "P5 effect-complete reference validation failed:\n - "
            + "\n - ".join(failures)
        )
    print(
        "P5 effect-complete reference validation passed: fresh deterministic replay, "
        "8/8 bounded local cases, exact claim-axis separation, no support/release effect."
    )


if __name__ == "__main__":
    main()
