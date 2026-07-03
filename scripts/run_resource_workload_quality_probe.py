#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from statistics import median
from datetime import datetime, timezone
from pathlib import Path
import shlex
import subprocess
import sys
import time
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "experiments" / "resource_workload_quality_probe" / "results" / "2026-07-01-local.json"
PROBE_ID = "resource-workload-quality-probe-2026-07-01-local"
RESULT_COMMAND = "python3 scripts/run_resource_workload_quality_probe.py --write-result"
SCOPED_TASK = "resource-workflow-trace-integrity-review"
SAMPLE_COUNT = 5

ROUTES = [
    {
        "route_id": "route://baseline-full-resource-lane-replay",
        "role": "baseline",
        "command": "python3 scripts/validate_resource_live_probe.py",
        "required_output": "Resource live probe validation passed",
        "quality_scope": "Full Resource Economics local replay surface.",
    },
    {
        "route_id": "route://selected-scoped-workflow-trace-validator",
        "role": "selected",
        "command": "python3 scripts/validate_resource_workflow_trace.py",
        "required_output": "Resource workflow trace validation passed",
        "quality_scope": "Scoped Resource workflow trace fixture and Lean/Python alignment review.",
    },
    {
        "route_id": "route://negative-no-op-success-text",
        "role": "negative_control",
        "command": "/bin/echo skipped resource workflow trace validator",
        "required_output": "Resource workflow trace validation passed",
        "quality_scope": "Invalid shortcut that returns quickly without running the required validator.",
    },
]

TRACKED_ARTIFACTS = [
    "docs/resource_workflow_trace.md",
    "docs/resource_live_probe.md",
    "scripts/validate_resource_workflow_trace.py",
    "scripts/validate_resource_live_probe.py",
    "experiments/resource_workflow_trace/results/2026-07-01-local.json",
    "experiments/resource_live_probe/results/2026-07-01-local.json",
    "lean/AsiStackProofs/ResourceEconomics.lean",
]

NON_CLAIMS = [
    "This workload-quality probe does not promote any chapter core claim above argument.",
    "This workload-quality probe does not create a support-state transition.",
    "This workload-quality probe does not prove stable speedup, deployed scheduler behavior, TokenMana behavior, PlanForge behavior, model quality, economic outcomes, physical feasibility, simulator adequacy, or workload-quality improvement outside this local repository task.",
    "The selected route is scoped to Resource workflow trace review only and does not replace the full book gate, release gate, production scheduler logs, human-repair measurement, or external review.",
]

RESIDUALS = [
    "The selected scoped validator does not check unrelated Resource Economics artifacts that the baseline live probe checks.",
    "The elapsed-time comparison is a local five-sample median measurement and remains vulnerable to machine load, cache state, and process scheduling noise.",
    "The no-op negative control demonstrates that a fast successful process is not adequate unless it runs the required validator and produces the expected validation surface.",
]


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def command_argv(command: str) -> list[str]:
    parts = shlex.split(command)
    if parts and parts[0] == "python3":
        return [sys.executable, *parts[1:]]
    return parts


def run_route_sample(route: dict[str, str]) -> dict[str, Any]:
    started = time.perf_counter()
    result = subprocess.run(
        command_argv(route["command"]),
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    elapsed_ms = round((time.perf_counter() - started) * 1000, 3)
    combined_output = result.stdout + result.stderr
    output_excerpt = [line for line in combined_output.strip().splitlines() if line][:6]
    quality_pass = result.returncode == 0 and route["required_output"] in combined_output
    return {
        "exit_code": result.returncode,
        "elapsed_ms": elapsed_ms,
        "output_sha256": sha256_text(combined_output),
        "output_excerpt": output_excerpt,
        "quality_pass": quality_pass,
    }


def run_route(route: dict[str, str]) -> dict[str, Any]:
    samples = [run_route_sample(route) for _ in range(SAMPLE_COUNT)]
    elapsed_values = [float(sample["elapsed_ms"]) for sample in samples]
    output_hashes = [str(sample["output_sha256"]) for sample in samples]
    exit_codes = [int(sample["exit_code"]) for sample in samples]
    quality_passes = [bool(sample["quality_pass"]) for sample in samples]
    quality_pass = all(quality_passes)
    return {
        "route_id": route["route_id"],
        "role": route["role"],
        "command": route["command"],
        "required_output": route["required_output"],
        "quality_scope": route["quality_scope"],
        "sample_count": SAMPLE_COUNT,
        "sample_elapsed_ms": elapsed_values,
        "elapsed_ms": round(float(median(elapsed_values)), 3),
        "elapsed_ms_min": round(min(elapsed_values), 3),
        "elapsed_ms_max": round(max(elapsed_values), 3),
        "exit_code": 0 if all(code == 0 for code in exit_codes) else next(code for code in exit_codes if code != 0),
        "exit_codes": exit_codes,
        "output_sha256": output_hashes[0],
        "output_sha256es": output_hashes,
        "output_excerpt": samples[0]["output_excerpt"],
        "quality_pass": quality_pass,
        "sample_quality_passes": quality_passes,
        "eligible": quality_pass,
    }


def artifact_stat(relative: str) -> dict[str, Any]:
    path = ROOT / relative
    raw = path.read_bytes()
    text = raw.decode("utf-8", errors="ignore")
    return {
        "path": relative,
        "bytes": len(raw),
        "lines": text.count("\n") + (0 if text.endswith("\n") or not text else 1),
        "sha256": sha256_bytes(raw),
    }


def build_record() -> dict[str, Any]:
    route_records = [run_route(route) for route in ROUTES]
    baseline = next(route for route in route_records if route["role"] == "baseline")
    selected = next(route for route in route_records if route["role"] == "selected")
    negative = next(route for route in route_records if route["role"] == "negative_control")
    selected_is_cheaper = selected["elapsed_ms"] < baseline["elapsed_ms"]
    negative_is_cheaper = negative["elapsed_ms"] < selected["elapsed_ms"]
    observed_reduction = round(
        (1 - (selected["elapsed_ms"] / baseline["elapsed_ms"])) * 100,
        3,
    ) if baseline["elapsed_ms"] > 0 else 0.0
    accepted = (
        baseline["quality_pass"]
        and selected["quality_pass"]
        and not negative["quality_pass"]
        and selected_is_cheaper
    )
    return {
        "probe_id": PROBE_ID,
        "record_kind": "resource_workload_quality_probe",
        "recorded_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "command": RESULT_COMMAND,
        "scoped_task": SCOPED_TASK,
        "local_only": True,
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
        "pass": accepted,
        "selected_route_id": selected["route_id"],
        "baseline_route_id": baseline["route_id"],
        "negative_control_route_id": negative["route_id"],
        "observed_selected_vs_baseline_elapsed_reduction_percent": observed_reduction,
        "selected_is_cheaper_than_baseline": selected_is_cheaper,
        "negative_control_is_cheaper_than_selected": negative_is_cheaper,
        "negative_control_rejected": not negative["quality_pass"],
        "summary": "Local Resource Economics workload-quality probe selected a scoped workflow-trace validator over the broader Resource live probe baseline using five-sample median elapsed time while rejecting a cheaper no-op success-text route.",
        "routes": route_records,
        "residuals": RESIDUALS,
        "non_claims": NON_CLAIMS,
        "artifact_refs": [*TRACKED_ARTIFACTS, str(RESULT.relative_to(ROOT))],
        "tracked_artifacts": [artifact_stat(path) for path in TRACKED_ARTIFACTS],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Resource Economics workload-quality probe.")
    parser.add_argument("--write-result", action="store_true", help=f"write {RESULT.relative_to(ROOT)}")
    args = parser.parse_args()

    record = build_record()
    text = json.dumps(record, indent=2, sort_keys=True) + "\n"
    if args.write_result:
        RESULT.parent.mkdir(parents=True, exist_ok=True)
        RESULT.write_text(text, encoding="utf-8")
        print(f"Wrote {RESULT.relative_to(ROOT)}")
    else:
        print(text, end="")
    if not record["pass"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
