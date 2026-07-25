#!/usr/bin/env python3
"""Validate the current C6 P0-P6 proof semantic-depth overlay."""

from __future__ import annotations

from collections import Counter
import copy
import json
from pathlib import Path
from typing import Any

import jsonschema

from build_proof_rationalization_registry import current_theorems
from build_proof_semantic_depth_overlay import (
    LEVEL_MEANINGS,
    OUTPUT,
    REPORT,
    ROOT,
    active_chapter_ids,
    build,
    statement_key,
)


SCHEMA = ROOT / "schemas" / "proof_semantic_depth_overlay.schema.json"
HISTORICAL = ROOT / "proofs" / "proof_rationalization_registry.json"
ALLOWED_LEVELS = set(LEVEL_MEANINGS)
HIGH_LEVELS = {"P3", "P4", "P5", "P6"}
REWRITE_OR_RETIRE = {
    "rewrite_scope_language",
    "rewrite_with_stronger_model",
    "retire_duplicate",
    "retire_narrow_projection",
    "retire_unused_candidate",
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def errors(overlay: dict[str, Any], *, check_generation: bool = True) -> list[str]:
    out: list[str] = []
    try:
        jsonschema.Draft202012Validator(load(SCHEMA)).validate(overlay)
    except jsonschema.ValidationError as exc:
        out.append(f"schema: {exc.message}")

    rows = overlay.get("records", [])
    current = current_theorems()
    current_ids = {str(row["theorem_id"]) for row in current}
    row_ids = [str(row.get("theorem_id")) for row in rows]
    if len(rows) != len(current) or set(row_ids) != current_ids or len(set(row_ids)) != len(row_ids):
        out.append("overlay must cover every current theorem exactly once")

    active_ids = active_chapter_ids()
    historical_rows = {
        str(row["theorem_id"]): row
        for row in load(HISTORICAL).get("baseline_theorems", [])
    }
    by_id = {str(row.get("theorem_id")): row for row in rows}
    level_counts = Counter(row.get("semantic_level") for row in rows)
    disposition_counts = Counter(row.get("disposition") for row in rows)
    review_counts = Counter(row.get("review_basis") for row in rows)
    binding_counts = Counter(
        (row.get("implementation_binding") or {}).get("state") for row in rows
    )
    witness_counts = Counter((row.get("witness") or {}).get("state") for row in rows)

    for row in rows:
        theorem_id = str(row.get("theorem_id"))
        level = row.get("semantic_level")
        if level not in ALLOWED_LEVELS:
            out.append(f"{theorem_id}: invalid semantic level")
            continue
        if row.get("semantic_level_meaning") != LEVEL_MEANINGS[level]:
            out.append(f"{theorem_id}: semantic-level meaning drift")
        owners = set(row.get("semantic_owner_ids", []))
        if not owners or not owners <= active_ids:
            out.append(f"{theorem_id}: missing or inactive semantic owner")
        if len(row.get("assumptions", [])) < 2:
            out.append(f"{theorem_id}: assumptions are not explicit")
        if not str(row.get("maximum_inference", "")).strip():
            out.append(f"{theorem_id}: missing maximum inference")
        if not row.get("mutation_refs"):
            out.append(f"{theorem_id}: no mutation coverage is named")
        if row.get("support_state_effect") != "none":
            out.append(f"{theorem_id}: support-state effect invented")

        witness = row.get("witness", {})
        binding = row.get("implementation_binding", {})
        if level == "P2" and witness.get("state") != "bounded_local_witness_present":
            out.append(f"{theorem_id}: P2 lacks a named bounded witness")
        if level in HIGH_LEVELS and binding.get("state") != "validator_and_artifact_bound":
            out.append(f"{theorem_id}: {level} lacks validator-and-artifact binding")
        if level == "P6" and not row.get("empirical_observation_contract_refs"):
            out.append(f"{theorem_id}: P6 lacks a named empirical observation contract")
        if row.get("disposition") == "retain" and not row.get("consumer_refs"):
            out.append(f"{theorem_id}: retained theorem lacks a named consumer")

        duplicate_of = row.get("duplicate_of")
        if row.get("disposition") == "retire_duplicate":
            canonical = by_id.get(str(duplicate_of))
            if canonical is None:
                out.append(f"{theorem_id}: duplicate retirement lacks a live canonical theorem")
            elif row.get("duplicate_kind") == "exact_normalized_statement":
                if statement_key(str(canonical.get("current_signature", ""))) != statement_key(
                    str(row.get("current_signature", ""))
                ):
                    out.append(f"{theorem_id}: exact duplicate retirement statements differ")
            elif row.get("duplicate_kind") == "reviewed_semantic_duplicate":
                old = historical_rows.get(theorem_id, {})
                replacement = f"lean-theorem:{canonical.get('name')}"
                if old.get("disposition") != "merge_duplicate" or replacement not in old.get("replacement_refs", []):
                    out.append(f"{theorem_id}: semantic duplicate lacks frozen review lineage")
            else:
                out.append(f"{theorem_id}: duplicate retirement lacks duplicate kind")
        elif duplicate_of and duplicate_of != theorem_id:
            out.append(f"{theorem_id}: non-duplicate disposition carries duplicate lineage")
        elif row.get("duplicate_kind") is not None:
            out.append(f"{theorem_id}: duplicate kind exists without duplicate lineage")

    summary = overlay.get("summary", {})
    expected_summary = {
        "current_theorem_count": len(rows),
        "current_module_count": len({row.get("module_path") for row in rows}),
        "semantic_owner_chapter_count": len({
            owner for row in rows for owner in row.get("semantic_owner_ids", [])
        }),
        "semantic_level_counts": {
            key: level_counts.get(key, 0) for key in LEVEL_MEANINGS
        },
        "disposition_counts": dict(sorted(disposition_counts.items())),
        "review_basis_counts": dict(sorted(review_counts.items())),
        "implementation_binding_counts": dict(sorted(binding_counts.items())),
        "witness_state_counts": dict(sorted(witness_counts.items())),
        "support_state_effect": "none",
    }
    for key, value in expected_summary.items():
        if summary.get(key) != value:
            out.append(f"summary drift: {key}")
    if not any(row.get("disposition") in REWRITE_OR_RETIRE for row in rows):
        out.append("overlay rationalizes nothing: rewrite/retire queue is empty")
    if level_counts.get("P6", 0) and not all(
        row.get("empirical_observation_contract_refs")
        for row in rows if row.get("semantic_level") == "P6"
    ):
        out.append("P6 count includes an unbound empirical claim")

    historical = load(HISTORICAL)
    if len(historical.get("baseline_theorems", [])) != 1151:
        out.append("frozen 1,151-theorem historical rationalization registry changed")
    if len(historical.get("baseline_targets", [])) != 298:
        out.append("frozen 298-target historical rationalization registry changed")

    if check_generation:
        expected_overlay, expected_report = build()
        if overlay != expected_overlay:
            out.append("overlay is stale")
        if not REPORT.exists() or REPORT.read_text(encoding="utf-8") != expected_report:
            out.append("overlay report is stale")
    return out


def main() -> None:
    overlay = load(OUTPUT)
    failures = errors(overlay)
    mutations: list[tuple[str, dict[str, Any]]] = []

    missing = copy.deepcopy(overlay)
    missing["records"] = missing["records"][:-1]
    mutations.append(("theorem deletion", missing))

    owner = copy.deepcopy(overlay)
    owner["records"][0]["semantic_owner_ids"] = ["not-an-active-chapter"]
    mutations.append(("owner laundering", owner))

    assumptions = copy.deepcopy(overlay)
    assumptions["records"][0]["assumptions"] = []
    mutations.append(("assumption erasure", assumptions))

    mutation = copy.deepcopy(overlay)
    mutation["records"][0]["mutation_refs"] = []
    mutations.append(("mutation evidence erasure", mutation))

    p2 = copy.deepcopy(overlay)
    p2["records"][0]["semantic_level"] = "P2"
    p2["records"][0]["semantic_level_meaning"] = LEVEL_MEANINGS["P2"]
    p2["records"][0]["witness"]["state"] = "no_reachable_witness_identified"
    p2["records"][0]["witness"]["refs"] = []
    mutations.append(("unwitnessed P2", p2))

    p4 = copy.deepcopy(overlay)
    p4["records"][0]["semantic_level"] = "P4"
    p4["records"][0]["semantic_level_meaning"] = LEVEL_MEANINGS["P4"]
    p4["records"][0]["implementation_binding"]["state"] = "formal_model_only"
    p4["records"][0]["implementation_binding"]["validator_refs"] = []
    p4["records"][0]["implementation_binding"]["artifact_refs"] = []
    mutations.append(("unbound P4", p4))

    p6 = copy.deepcopy(overlay)
    p6["records"][0]["semantic_level"] = "P6"
    p6["records"][0]["semantic_level_meaning"] = LEVEL_MEANINGS["P6"]
    p6["records"][0]["empirical_observation_contract_refs"] = []
    mutations.append(("observation-free P6", p6))

    consumer = copy.deepcopy(overlay)
    retained = next(row for row in consumer["records"] if row["disposition"] == "retain")
    retained["consumer_refs"] = []
    mutations.append(("consumer-free retention", consumer))

    support = copy.deepcopy(overlay)
    support["records"][0]["support_state_effect"] = "promotion"
    mutations.append(("support promotion", support))

    disposition = copy.deepcopy(overlay)
    disposition["records"][0]["disposition"] = "retire_duplicate"
    disposition["records"][0]["duplicate_of"] = "missing"
    mutations.append(("duplicate without canonical theorem", disposition))

    for label, candidate in mutations:
        if not errors(candidate, check_generation=False):
            failures.append(f"negative mutation accepted: {label}")
    if failures:
        raise SystemExit(
            "Proof semantic-depth overlay validation failed:\n - "
            + "\n - ".join(failures)
        )
    print(
        "Proof semantic-depth overlay passed: "
        f"{len(overlay['records'])} live theorems, "
        f"{overlay['summary']['current_module_count']} theorem-bearing modules, "
        f"levels={overlay['summary']['semantic_level_counts']}, "
        f"dispositions={overlay['summary']['disposition_counts']}, "
        "10 rejecting mutations, no support-state effect."
    )


if __name__ == "__main__":
    main()
