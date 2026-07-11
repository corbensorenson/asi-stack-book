#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
from pathlib import Path

from build_canonical_public_status import ROOT, load_json, validate_against_schema


RECORD = ROOT / "experiments/post_v2_evidence_program/preregistration.json"
SCHEMA = ROOT / "schemas/post_v2_evidence_preregistration.schema.json"
ROADMAP = ROOT / "docs/post_v2_evidence_roadmap.md"
DOC = ROOT / "docs/post_v2_evidence_preregistration.md"


def semantic_errors(record: dict) -> list[str]:
    errors: list[str] = []
    programs = record.get("programs", [])
    expected_ids = {
        "realistic_governed_work_flagship",
        "matched_routing_and_deliberation",
        "real_update_causality_campaign",
    }
    if {row.get("program_id") for row in programs} != expected_ids:
        errors.append("preregistration must contain exactly the three roadmap programs")
    if sorted(row.get("priority") for row in programs) != [1, 2, 3]:
        errors.append("program priorities must be unique 1, 2, and 3")
    if any(row.get("state") != "preregistered_not_executed" for row in programs):
        errors.append("outcome state was recorded before execution")
    for row in programs:
        if not row.get("simpler_baseline"):
            errors.append(f"{row.get('program_id')}: missing simpler baseline")
        for field in ("metrics", "negative_controls"):
            if not row.get(field):
                errors.append(f"{row.get('program_id')}: missing {field}")
        disposition = str(row.get("disposition_rule", "")).lower()
        if "promot" in disposition and not any(term in disposition for term in ("no-change", "independent", "necessary but never sufficient")):
            errors.append(f"{row.get('program_id')}: disposition rule creates promotion pressure")
    runtime = record.get("environment", {}).get("model_runtime", {})
    if runtime.get("state") != "verified_local_generation_before_preregistration_freeze":
        errors.append("local model runtime was not verified before freeze")
    if runtime.get("revision") != "ea3f2471cf1b1f0db85067f1ef93848e38e88c25":
        errors.append("model revision is not exactly pinned")
    if runtime.get("parameter_count") != 494032768:
        errors.append("model parameter count drifted")
    allowed = set(record.get("allowed_outcomes", []))
    if allowed != {"no_change", "promote", "narrow", "demote", "refute"}:
        errors.append("allowed outcome set must preserve no-change and negative dispositions")
    lanes = record.get("conditional_lanes", [])
    if len(lanes) != 3 or any(row.get("state") != "deferred_activation_condition_absent" for row in lanes):
        errors.append("three conditional lanes must remain honestly deferred before activation")
    roadmap = ROADMAP.read_text(encoding="utf-8")
    for phrase in (
        "Priority 1 — Realistic governed-work flagship",
        "Priority 2 — Routing and deliberation comparisons",
        "Priority 3 — Real update-causality campaign",
        "no-change, narrowing, demotion, and refutation",
    ):
        if phrase not in roadmap:
            errors.append(f"roadmap missing preregistration boundary: {phrase}")
    doc = DOC.read_text(encoding="utf-8")
    for phrase in ("before outcome runs", "establishing runtime availability", "another schema fixture cannot close them"):
        if phrase not in doc:
            errors.append(f"readable preregistration missing boundary: {phrase}")
    return errors


def negative_controls(record: dict) -> list[str]:
    failures: list[str] = []
    mutations = []
    missing_baseline = copy.deepcopy(record)
    missing_baseline["programs"][0]["simpler_baseline"] = {}
    mutations.append(("missing baseline", missing_baseline))
    leaked_result = copy.deepcopy(record)
    leaked_result["programs"][1]["state"] = "passed"
    mutations.append(("outcome before execution", leaked_result))
    mutable_model = copy.deepcopy(record)
    mutable_model["environment"]["model_runtime"]["revision"] = "main"
    mutations.append(("mutable model revision", mutable_model))
    forced_positive = copy.deepcopy(record)
    forced_positive["allowed_outcomes"] = ["promote"]
    mutations.append(("forced positive result", forced_positive))
    fake_activation = copy.deepcopy(record)
    fake_activation["conditional_lanes"][0]["state"] = "completed_by_fixture"
    mutations.append(("fixture closes hardware lane", fake_activation))
    for label, mutation in mutations:
        schema_errors = validate_against_schema(mutation, load_json(SCHEMA), label)
        if not schema_errors and not semantic_errors(mutation):
            failures.append(f"negative control incorrectly accepted: {label}")
    return failures


def main() -> None:
    missing = [path.relative_to(ROOT).as_posix() for path in (RECORD, SCHEMA, ROADMAP, DOC) if not path.is_file()]
    if missing:
        raise SystemExit("missing post-v2 preregistration artifacts: " + ", ".join(missing))
    record = load_json(RECORD)
    errors = validate_against_schema(record, load_json(SCHEMA), RECORD.relative_to(ROOT).as_posix())
    errors.extend(semantic_errors(record))
    errors.extend(negative_controls(record))
    if errors:
        raise SystemExit("Post-v2 evidence preregistration validation failed:\n - " + "\n - ".join(errors))
    print("Post-v2 evidence preregistration passed: 3 frozen programs, pinned local model runtime, 3 honest conditional deferrals, and 5 rejecting negative controls.")


if __name__ == "__main__":
    main()
