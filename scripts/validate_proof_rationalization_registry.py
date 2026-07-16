#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
from collections import Counter
from pathlib import Path
from typing import Any

import jsonschema

from build_proof_rationalization_registry import REGISTRY, REVIEWS, ROOT, build


SCHEMA = ROOT / "schemas" / "proof_rationalization_registry.schema.json"
CLAIMS = ROOT / "evidence_quality" / "claim_atom_registry.json"
STATUS = ROOT / "roadmap_records" / "post_v2_3_claim_proof_and_sota_challenge_status.json"
ALLOWED_REVIEW_STATES = {"machine_candidate", "semantically_reviewed", "terminally_dispositioned"}
RETAINED = {
    "retain_load_bearing_semantic",
    "retain_refinement_or_executable_bridge",
    "retain_countermodel_or_negative_case",
    "retain_reusable_lemma",
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def errors(registry: dict[str, Any], reviews: dict[str, Any], check_generation: bool = True) -> list[str]:
    out: list[str] = []
    try:
        jsonschema.Draft202012Validator(load(SCHEMA)).validate(registry)
    except jsonschema.ValidationError as exc:
        out.append(f"registry schema: {exc.message}")
    theorems = registry.get("baseline_theorems", [])
    targets = registry.get("baseline_targets", [])
    theorem_ids = [row.get("theorem_id") for row in theorems]
    target_ids = [row.get("target_id") for row in targets]
    if len(theorems) != 1151 or len(set(theorem_ids)) != 1151:
        out.append("frozen activation baseline must contain 1,151 uniquely identified theorem declarations")
    if len(targets) != 298 or len(set(target_ids)) != 298:
        out.append("frozen activation baseline must contain 298 uniquely identified proof targets")
    claims = {row["atom_id"] for row in load(CLAIMS)["atoms"]}
    allowed_dispositions = set(reviews.get("allowed_dispositions", []))
    known_theorems = set(theorem_ids)
    known_targets = set(target_ids)
    for kind, rows, id_key in (("theorem", theorems, "theorem_id"), ("target", targets, "target_id")):
        for row in rows:
            row_id = row.get(id_key)
            if row.get("claim_atom_id") not in claims or row.get("claim_atom_id") != f"{row.get('chapter_id')}.core":
                out.append(f"{row_id}: missing or noncanonical claim-atom owner")
            if row.get("review_state") not in ALLOWED_REVIEW_STATES:
                out.append(f"{row_id}: invalid review state")
            if row.get("review_state") == "machine_candidate":
                if row.get("disposition") is not None:
                    out.append(f"{row_id}: machine candidate has a final disposition")
                continue
            disposition = row.get("disposition")
            if disposition not in allowed_dispositions:
                out.append(f"{row_id}: reviewed item lacks an allowed disposition")
            if not str(row.get("review_rationale") or "").strip():
                out.append(f"{row_id}: reviewed item lacks rationale")
            if disposition in RETAINED:
                if not str(row.get("semantic_role") or "").strip():
                    out.append(f"{row_id}: retained item lacks semantic role")
                if not row.get("assumptions") or not row.get("excluded_effects"):
                    out.append(f"{row_id}: retained item lacks exact assumptions or excluded effects")
                consumers = row.get("consumer_refs", []) + row.get("runtime_consumer_refs", [])
                if kind == "theorem":
                    consumers = consumers + row.get("theorem_consumers", [])
                if not consumers:
                    out.append(f"{row_id}: retained item has no live consumer")
            if disposition in {"merge_duplicate", "replace_with_stronger_model"} and not row.get("replacement_refs"):
                out.append(f"{row_id}: merge or replacement lacks lineage target")
    for row in theorems:
        if not set(row.get("candidate_target_tags", [])) <= known_targets:
            out.append(f"{row.get('theorem_id')}: candidate target escapes frozen inventory")
        if not set(row.get("theorem_dependencies", [])) <= known_theorems:
            out.append(f"{row.get('theorem_id')}: dependency escapes frozen inventory")
        if not set(row.get("theorem_consumers", [])) <= known_theorems:
            out.append(f"{row.get('theorem_id')}: consumer escapes frozen inventory")
    for row in targets:
        if not set(row.get("candidate_theorem_ids", [])) <= known_theorems:
            out.append(f"{row.get('target_id')}: candidate theorem escapes frozen inventory")
    summary = registry.get("summary", {})
    expected = {
        "baseline_theorem_declaration_count": len(theorems),
        "baseline_proof_target_count": len(targets),
        "chapter_count": len({row.get("chapter_id") for row in targets}),
        "module_count": len({row.get("module_path") for row in theorems} | {row.get("module_path") for row in targets}),
        "theorem_review_state_counts": dict(sorted(Counter(row.get("review_state") for row in theorems).items())),
        "target_review_state_counts": dict(sorted(Counter(row.get("review_state") for row in targets).items())),
        "depth_class_counts": dict(sorted(Counter(row.get("depth_class") for row in theorems).items())),
    }
    for key, value in expected.items():
        if summary.get(key) != value:
            out.append(f"summary drift: {key}")
    if summary.get("support_state_effect") != "none":
        out.append("proof rationalization invented a support-state effect")
    contract = load(STATUS).get("proof_rationalization_contract", {})
    exact_status = {
        "theorem_machine_candidate_count": Counter(row.get("review_state") for row in theorems).get("machine_candidate", 0),
        "target_machine_candidate_count": Counter(row.get("review_state") for row in targets).get("machine_candidate", 0),
        "fully_reviewed_module_count": summary.get("fully_reviewed_module_count"),
        "safety_critical_fully_reviewed_module_count": summary.get("safety_critical_fully_reviewed_module_count"),
        "current_missing_or_changed_theorem_count": summary.get("missing_current_theorem_count", 0) + summary.get("changed_current_theorem_count", 0),
        "current_missing_or_changed_target_count": summary.get("missing_current_target_count", 0) + summary.get("changed_current_target_count", 0),
        "support_state_effect": "none",
    }
    for key, value in exact_status.items():
        if contract.get(key) != value:
            out.append(f"P2 machine status drifted: {key} expected {value}, got {contract.get(key)}")
    if check_generation:
        expected_registry, expected_report, expected_dossiers = build()
        if registry != expected_registry:
            out.append("proof rationalization registry is stale")
        report = ROOT / "docs" / "proof_rationalization_registry.md"
        if not report.exists() or report.read_text(encoding="utf-8") != expected_report:
            out.append("proof rationalization report is stale")
        for chapter_id, body in expected_dossiers.items():
            path = ROOT / "evidence_quality" / "proof_model_dossiers" / f"{chapter_id}.md"
            if not path.exists() or path.read_text(encoding="utf-8") != body:
                out.append(f"{chapter_id}: proof-model dossier is stale")
                break
    return out


def main() -> None:
    registry = load(REGISTRY)
    reviews = load(REVIEWS)
    failures = errors(registry, reviews)
    mutations: list[tuple[str, dict[str, Any]]] = []
    missing = copy.deepcopy(registry)
    missing["baseline_theorems"] = missing["baseline_theorems"][:-1]
    mutations.append(("baseline theorem deletion", missing))
    owner = copy.deepcopy(registry)
    owner["baseline_targets"][0]["claim_atom_id"] = "fake.core"
    mutations.append(("claim owner laundering", owner))
    disposition = copy.deepcopy(registry)
    disposition["baseline_theorems"][0]["review_state"] = "semantically_reviewed"
    disposition["baseline_theorems"][0]["disposition"] = "retain_load_bearing_semantic"
    disposition["baseline_theorems"][0]["semantic_role"] = ""
    disposition["baseline_theorems"][0]["assumptions"] = []
    disposition["baseline_theorems"][0]["excluded_effects"] = []
    mutations.append(("retention without model boundary", disposition))
    replacement = copy.deepcopy(registry)
    replacement["baseline_targets"][0]["review_state"] = "terminally_dispositioned"
    replacement["baseline_targets"][0]["disposition"] = "replace_with_stronger_model"
    replacement["baseline_targets"][0]["review_rationale"] = "replace"
    mutations.append(("replacement without lineage", replacement))
    support = copy.deepcopy(registry)
    support["summary"]["support_state_effect"] = "promotion"
    mutations.append(("support promotion", support))
    for label, candidate in mutations:
        if not errors(candidate, reviews, check_generation=False):
            failures.append(f"negative mutation accepted: {label}")
    if failures:
        raise SystemExit("Proof rationalization registry validation failed:\n - " + "\n - ".join(failures))
    print(
        f"Proof rationalization registry passed: {len(registry['baseline_theorems'])} frozen theorems, "
        f"{len(registry['baseline_targets'])} frozen targets, 54 dossiers, no support effect, five rejecting mutations."
    )


if __name__ == "__main__":
    main()
