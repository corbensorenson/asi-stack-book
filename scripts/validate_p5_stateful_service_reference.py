#!/usr/bin/env python3
"""Freshly replay and validate the P5 stateful-service reference slice."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "experiments/effect_complete_service/results/2026-07-27-local.json"
SCHEMA = ROOT / "schemas/effect_complete_service_result.schema.json"
RUNNER = ROOT / "scripts/run_p5_stateful_service_reference.py"
REPORT = ROOT / "docs/p5_stateful_service_reference_report.md"
EXPECTED_CASE_IDS = {
    "actual-learning-state-mutation",
    "artifact-only-rollback-rejected",
    "crash-restart-full-state-recovery",
    "partition-outbox-exactly-once",
    "revoked-credential-effect-rejected",
    "weight-and-environment-custody-tamper-rejected",
    "independent-observation-and-source-attestation",
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    failures: list[str] = []
    result = load(RESULT)
    commit = result.get("custody", {}).get("attested_source_commit")
    with tempfile.TemporaryDirectory(prefix="asi-p5-stateful-validation-") as directory:
        replay = Path(directory) / "result.json"
        completed = subprocess.run(
            [
                sys.executable,
                str(RUNNER),
                "--attested-source-commit",
                str(commit),
                "--output",
                str(replay),
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            timeout=90,
        )
        if completed.returncode:
            failures.append(
                f"runner failed: {completed.stderr or completed.stdout}"
            )
        elif load(replay) != result:
            failures.append("tracked result differs from a fresh deterministic replay")

    failures.extend(
        f"schema: {error.message}"
        for error in sorted(
            Draft202012Validator(load(SCHEMA)).iter_errors(result),
            key=lambda error: list(error.path),
        )
    )
    ids = [receipt.get("case_id") for receipt in result.get("receipts", [])]
    if set(ids) != EXPECTED_CASE_IDS or len(ids) != len(set(ids)):
        failures.append("case denominator or identity drifted")
    if not all(
        receipt.get("passed") is True for receipt in result.get("receipts", [])
    ):
        failures.append("one or more cases did not pass")
    if result.get("learning_state", {}).get("loss_after", float("inf")) >= result.get(
        "learning_state", {}
    ).get("loss_before", float("-inf")):
        failures.append("authored learning positive control no longer improves")
    rollback = result.get("rollback", {})
    if not rollback.get("artifact_only_control_rejected"):
        failures.append("weights-only rollback negative control did not reject")
    if not rollback.get("byte_exact_restore"):
        failures.append("full-state crash recovery is not byte exact")
    external = result.get("external_effect", {})
    if external.get("accepted_effect_count") != 1:
        failures.append("external effect denominator is not exactly one")
    if external.get("open_unowned_effects") != 0:
        failures.append("an external effect lost residual ownership")
    custody = result.get("custody", {})
    if custody.get("attestation_scope") != (
        "local_source_and_runtime_identity_not_deployment"
    ):
        failures.append("local custody was laundered into deployment attestation")
    if result.get("support_state_effect") != "none":
        failures.append("stateful service slice laundered chapter support")
    if result.get("release_effect") != "none":
        failures.append("stateful service slice laundered release authority")

    report = REPORT.read_text(encoding="utf-8")
    for phrase in (
        "actual model and Adam learning state",
        "weights-only rollback",
        "localhost partition",
        "not a production deployment",
        "P5 remains in progress",
    ):
        if phrase not in report:
            failures.append(f"report boundary missing: {phrase}")

    if failures:
        raise SystemExit(
            "P5 stateful service validation failed:\n - "
            + "\n - ".join(failures)
        )
    print(
        "P5 stateful service validation passed: fresh 7/7 replay, actual "
        "learning-state mutation, full-state crash recovery, partition/outbox, "
        "external observation, custody tamper controls, and no support/release effect."
    )


if __name__ == "__main__":
    main()
