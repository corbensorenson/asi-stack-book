#!/usr/bin/env python3
"""Validate the frozen repair and, when present, its non-evidentiary result."""

from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "experiments/post_v2_3_evidence_protocol_renewal"
PREREG = BASE / "preflight/preregistration.json"
TASKS = BASE / "preflight/tasks.json"
RESULT = BASE / "preflight/attempt_1_result.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def errors_for(result: dict | None) -> list[str]:
    errors: list[str] = []
    prereg = json.loads(PREREG.read_text())
    tasks = json.loads(TASKS.read_text())
    historical = prereg.get("historical_failure_binding", {})
    if historical.get("raw_output_count") != 36 or len(historical.get("no_change_transitions", [])) != 2:
        errors.append("historical failure binding drifted")
    if tasks.get("task_count") != 4 or tasks.get("split") != "sacrificial_non_evidentiary_excluded_from_all_flagship_splits":
        errors.append("sacrificial task split drifted")
    if prereg.get("support_state_effect") != "none" or prereg.get("evidentiary_role") != "none_sacrificial_protocol_only":
        errors.append("preflight launders evidence or support")
    if result is None:
        return errors
    if result.get("preregistration_sha256") != sha(PREREG) or result.get("task_manifest_sha256") != sha(TASKS):
        errors.append("preflight result lost frozen input binding")
    rows = result.get("records", [])
    summary = result.get("summary", {})
    if len(rows) != 4 or summary.get("tasks") != 4:
        errors.append("preflight denominator drifted")
    if summary.get("terminal_states_captured") != 4 or summary.get("cost_latency_records") != 4:
        errors.append("terminal or cost/latency capture incomplete")
    if any(len(row.get("planned_arm_capture", {})) != 4 or not all(row["planned_arm_capture"].values()) for row in rows):
        errors.append("planned arm capture incomplete")
    for row in rows:
        for kind in ("reasoning", "final"):
            artifact = ROOT / row.get(kind, {}).get("path", "")
            if not artifact.is_file() or sha(artifact) != row[kind].get("sha256"):
                errors.append(f"{row.get('task_id')} {kind} artifact binding failed")
        spec = ROOT / row.get("evaluator", {}).get("spec_path", "")
        raw = ROOT / row.get("final", {}).get("path", "")
        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts/post_v2_3_renewal_evaluator.py"), "--spec", str(spec), "--raw", str(raw)],
            capture_output=True,
            text=True,
        )
        if proc.returncode or json.loads(proc.stdout) != row.get("evaluator", {}).get("outcome"):
            errors.append(f"{row.get('task_id')} evaluator replay drifted")
    passed = (
        summary.get("parseable_final_outputs") == 4
        and summary.get("evaluator_subprocess_successes") == 4
        and summary.get("all_four_arms_captured") == 4
    )
    expected_state = "passed_non_evidentiary_preflight" if passed else "failed_non_evidentiary_preflight"
    if result.get("state") != expected_state or result.get("flagship_eligibility") is not passed:
        errors.append("preflight state does not follow frozen pass rule")
    if result.get("support_state_effect") != "none":
        errors.append("preflight result changes support state")
    return errors


def main() -> None:
    result = json.loads(RESULT.read_text()) if RESULT.exists() else None
    errors = errors_for(result)
    if result is not None:
        for label, mutate in [
            ("denominator", lambda x: x["summary"].__setitem__("tasks", 3)),
            ("parseability", lambda x: x["summary"].__setitem__("parseable_final_outputs", 3)),
            ("arm erasure", lambda x: x["records"][0]["planned_arm_capture"].__setitem__("matched_baseline_admission", False)),
            ("input drift", lambda x: x.__setitem__("preregistration_sha256", "0" * 64)),
            ("support laundering", lambda x: x.__setitem__("support_state_effect", "promoted")),
        ]:
            candidate = copy.deepcopy(result)
            mutate(candidate)
            if not errors_for(candidate):
                errors.append(f"negative mutation accepted: {label}")
    if errors:
        raise SystemExit("Protocol preflight validation failed:\n - " + "\n - ".join(sorted(set(errors))))
    if result is None:
        print("Protocol preflight setup passed: frozen before outputs, 4 sacrificial tasks, 36 historical outputs and two no-change transitions preserved.")
    else:
        print(f"Protocol preflight validation passed: {result['state']}, {result['summary']['parseable_final_outputs']}/4 parseable finals, all four arms captured, and 5 rejecting controls.")


if __name__ == "__main__":
    main()
