#!/usr/bin/env python3
"""Validate the immutable P2-R3a capacity and Docker preflight receipt."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
ATTEMPT = (
    ROOT
    / "experiments/p2_governed_repository_admission/infrastructure_materialization/attempts"
    / "2026-07-26-r3a-001/result.json"
)
SCHEMA = ROOT / "schemas/p2_r3a_capacity_preflight.schema.json"
RESOURCE = ROOT / "evidence_quality/p2_resource_ceiling.json"
QUEUE = ROOT / "experiments/p2_governed_repository_admission/corpus/replacement_queue.json"
DOC = ROOT / "docs/p2_r3a_capacity_and_docker_preflight_2026_07_26.md"


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def failures(record: dict, *, inspect_files: bool = True) -> list[str]:
    out: list[str] = []
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    for error in Draft202012Validator(
        schema, format_checker=FormatChecker()
    ).iter_errors(record):
        out.append(f"schema:{'.'.join(map(str, error.path))}: {error.message}")

    host = record.get("host_capacity", {})
    docker = record.get("docker", {})
    decision = record.get("decision", {})
    expected_floor_pass = (
        host.get("available_bytes", -1) >= host.get("minimum_required_bytes", 10**30)
    )
    expected_docker_pass = docker.get("daemon_reachable") is True
    expected_entry = expected_floor_pass and expected_docker_pass
    checks = [
        (record.get("attempt_id") == "2026-07-26-r3a-001", "attempt identity drifted"),
        (host.get("floor_pass") == expected_floor_pass, "host floor decision is inconsistent"),
        (
            host.get("shortfall_bytes")
            == max(0, host.get("minimum_required_bytes", 0) - host.get("available_bytes", 0)),
            "host shortfall arithmetic is inconsistent",
        ),
        (
            decision.get("entry_gate_pass") == expected_entry,
            "combined entry decision is inconsistent",
        ),
        (
            docker.get("all_diagnostic_commands_exit_zero")
            == docker.get("daemon_reachable"),
            "Docker command and daemon states disagree",
        ),
        (
            docker.get("reclaimable_bytes_known") == docker.get("daemon_reachable"),
            "Docker reclaimable-byte knowledge is overstated",
        ),
        (
            decision.get("pool_materialization_started") is False,
            "pool materialization was claimed",
        ),
        (
            decision.get("protected_task_content_opened") is False,
            "protected task content was opened",
        ),
        (
            decision.get("candidate_outcome_opened") is False,
            "candidate outcome was opened",
        ),
        (record.get("negative_inference_level") == "N0", "negative inference exceeded N0"),
        (record.get("support_state_effect") == "none", "support state moved"),
        (record.get("release_effect") == "none", "release state moved"),
    ]
    out.extend(message for passed, message in checks if not passed)

    receipts = record.get("command_receipts", [])
    expected_commands = [
        ["df", "-k", str(ROOT)],
        ["docker", "version", "--format", "{{json .}}"],
        ["docker", "info", "--format", "{{json .}}"],
        ["docker", "system", "df", "--format", "{{json .}}"],
    ]
    if [row.get("argv") for row in receipts] != expected_commands:
        out.append("diagnostic command set or order drifted")
    for index, row in enumerate(receipts):
        if row.get("stdout_sha256") != sha256_bytes(row.get("stdout", "").encode()):
            out.append(f"command {index} stdout digest mismatch")
        if row.get("stderr_sha256") != sha256_bytes(row.get("stderr", "").encode()):
            out.append(f"command {index} stderr digest mismatch")

    if expected_entry:
        if decision.get("blockers"):
            out.append("passing entry receipt retained blockers")
    else:
        expected_blockers = []
        if not expected_floor_pass:
            expected_blockers.append("host_free_bytes_below_frozen_50_gib_floor")
        if not expected_docker_pass:
            expected_blockers.append("docker_daemon_unreachable")
        if decision.get("blockers") != expected_blockers:
            out.append("blocking causes do not match measured entry failures")

    if inspect_files:
        resource = json.loads(RESOURCE.read_text(encoding="utf-8"))
        queue = json.loads(QUEUE.read_text(encoding="utf-8"))
        inputs = record.get("inputs", {})
        if inputs.get("resource_ceiling_sha256") != sha256_bytes(RESOURCE.read_bytes()):
            out.append("resource ceiling digest drifted")
        if inputs.get("replacement_queue_sha256") != sha256_bytes(QUEUE.read_bytes()):
            out.append("replacement queue digest drifted")
        if inputs.get("frozen_candidate_count") != queue.get("candidate_count"):
            out.append("candidate count drifted")
        if host.get("minimum_required_bytes") != resource["task_acceptance_ceilings"][
            "minimum_host_free_bytes_before_task"
        ]:
            out.append("frozen host floor drifted")
        doc = DOC.read_text(encoding="utf-8")
        for phrase in [
            "No protected task content was opened",
            "N0 infrastructure disposition",
            "does not count as a candidate attempt",
            "non-Docker user data",
            "30-candidate",
        ]:
            if phrase not in doc:
                out.append(f"human receipt missing boundary: {phrase}")
    return out


def main() -> None:
    record = json.loads(ATTEMPT.read_text(encoding="utf-8"))
    out = failures(record)
    mutations: list[tuple[str, dict]] = []

    def add(label: str, edit) -> None:
        candidate = copy.deepcopy(record)
        edit(candidate)
        mutations.append((label, candidate))

    add("floor pass forged", lambda r: r["host_capacity"].__setitem__("floor_pass", True))
    add("shortfall forged", lambda r: r["host_capacity"].__setitem__("shortfall_bytes", 0))
    add("entry pass forged", lambda r: r["decision"].__setitem__("entry_gate_pass", True))
    add("materialization forged", lambda r: r["decision"].__setitem__("pool_materialization_started", True))
    add("content opened", lambda r: r["decision"].__setitem__("protected_task_content_opened", True))
    add("N-level inflated", lambda r: r.__setitem__("negative_inference_level", "N2"))
    add("support promoted", lambda r: r.__setitem__("support_state_effect", "promotion"))
    add("command output edited", lambda r: r["command_receipts"][0].__setitem__("stdout", "edited"))
    add("queue shrank", lambda r: r["inputs"].__setitem__("frozen_candidate_count", 29))
    add("Docker knowledge forged", lambda r: r["docker"].__setitem__("reclaimable_bytes_known", True))
    for label, candidate in mutations:
        if not failures(candidate, inspect_files=False):
            out.append(f"negative mutation accepted: {label}")
    if out:
        raise SystemExit("P2-R3a capacity preflight failed:\n - " + "\n - ".join(out))
    print(
        "P2-R3a capacity preflight passed: exact entry decision, 30-candidate "
        "custody, N0 boundary, and 10/10 mutations rejected."
    )


if __name__ == "__main__":
    main()
