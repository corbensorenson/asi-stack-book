#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
from typing import Any

from validate_protocol_examples import validate_value

ROOT = Path(__file__).resolve().parents[1]
TRACE = ROOT / "products" / "narrative_running_example_trace.json"
SPINE = ROOT / "products" / "narrative_product_spine.json"
SCHEMA = ROOT / "schemas" / "narrative_running_example_trace.schema.json"
MUTATIONS = ROOT / "experiments" / "narrative_running_example" / "fixtures"
EDITORIAL_FIELDS = (
    "reader_question", "running_example", "strongest_objection", "failure_story",
    "evidence_that_would_change_the_conclusion", "handoff",
)


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def semantic_errors(trace: dict[str, Any], spine: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    steps = trace.get("steps", [])
    chapters = spine.get("chapters", [])
    expected_ids = [row.get("chapter_id") for row in chapters]
    if [row.get("chapter_id") for row in steps] != expected_ids:
        errors.append("running-example steps must match the fifteen-chapter narrative spine exactly")
    if [row.get("order") for row in steps] != list(range(1, 16)):
        errors.append("running-example step order must be contiguous from one through fifteen")
    for chapter in chapters:
        for field in EDITORIAL_FIELDS:
            if len(str(chapter.get(field, "")).strip()) < 24:
                errors.append(f"{chapter.get('chapter_id')}: editorial contract field {field} is missing or too short")
        if chapter.get("core_claim_ref") != f"{chapter.get('chapter_id')}.core":
            errors.append(f"{chapter.get('chapter_id')}: core claim reference does not match chapter identity")
        running = str(chapter.get("running_example", "")).lower()
        if not any(term in running for term in ("repository", "patch", "book chapter", "book itself", "critique remediation")):
            errors.append(f"{chapter.get('chapter_id')}: running example leaves the governed repository-change scenario")

    cumulative = set(trace.get("initial_artifact_refs", []))
    produced_ever: set[str] = set()
    for index, step in enumerate(steps):
        consumes = set(step.get("consumes", []))
        produces = set(step.get("produces", []))
        if not consumes.issubset(cumulative):
            errors.append(f"{step.get('chapter_id')}: running example consumes an artifact not carried from prior chapters")
        if produces & cumulative or produces & produced_ever:
            errors.append(f"{step.get('chapter_id')}: running example reuses an existing artifact identity as new output")
        expected_cumulative = cumulative | produces
        if set(step.get("cumulative_artifact_refs", [])) != expected_cumulative:
            errors.append(f"{step.get('chapter_id')}: cumulative running-example state reset or drifted")
        expected_handoff = expected_ids[index + 1] if index + 1 < len(expected_ids) else None
        if step.get("handoff_to") != expected_handoff:
            errors.append(f"{step.get('chapter_id')}: handoff does not point to the next narrative chapter")
        produced_ever |= produces
        cumulative = expected_cumulative
    if len(cumulative) != len(trace.get("initial_artifact_refs", [])) + 15:
        errors.append("the fifteen-chapter narrative must accumulate one distinct artifact at every stage")
    decision = trace.get("decision", {})
    if decision.get("support_state_effect") != "none" or decision.get("release_approved") is not False:
        errors.append("editorial continuity cannot promote support or approve a reader release")
    if len(trace.get("non_claims", [])) < 3:
        errors.append("narrative trace must retain explicit non-claims")
    return errors


def apply_mutation(base: dict[str, Any], mutation: dict[str, Any]) -> dict[str, Any]:
    value = deepcopy(base)
    target: Any = value
    for segment in mutation["path"][:-1]:
        target = target[segment]
    leaf = mutation["path"][-1]
    if mutation["operation"] == "set":
        target[leaf] = mutation["value"]
    elif mutation["operation"] == "delete":
        del target[leaf]
    elif mutation["operation"] == "merge":
        target[leaf].update(mutation["value"])
    else:
        raise ValueError(f"unsupported mutation operation {mutation['operation']!r}")
    return value


def main() -> None:
    trace = load(TRACE)
    spine = load(SPINE)
    schema = load(SCHEMA)
    errors = validate_value(trace, schema, str(TRACE.relative_to(ROOT))) + semantic_errors(trace, spine)
    if errors:
        raise SystemExit("Valid narrative running-example trace failed:\n - " + "\n - ".join(errors))
    mutations = sorted(MUTATIONS.glob("invalid_*.json"))
    if not mutations:
        raise SystemExit("No narrative running-example negative controls found.")
    for path in mutations:
        mutation = load(path)
        candidate = apply_mutation(trace, mutation)
        found = validate_value(candidate, schema, str(path.relative_to(ROOT))) + semantic_errors(candidate, spine)
        if not any(mutation["expected_error"] in error for error in found):
            raise SystemExit(f"{path.relative_to(ROOT)} did not produce {mutation['expected_error']!r}: {found}")
    print(
        "Narrative running-example validation passed: 15 editorial contracts, "
        f"16 cumulative artifacts, and {len(mutations)} rejecting continuity controls."
    )


if __name__ == "__main__":
    main()
