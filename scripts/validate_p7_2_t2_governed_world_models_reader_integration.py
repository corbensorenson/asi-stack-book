#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "evidence_quality/p7_2_t2_governed_world_models_reader_integration.json"
BOOK = ROOT / "book_structure.json"
INVENTORY = ROOT / "sources/source_inventory.json"
MANIFEST = ROOT / "proofs/proof_manifest.json"
STATUS = ROOT / "roadmap_records/post_v2_3_maintenance_transfer_and_publication_status.json"
ROLES = ROOT / "evidence_quality/p7_1a_w2_narrative_audit.json"
CHAPTER_ID = "governed-world-models-and-reality-grounding"


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def errors(data: dict[str, Any]) -> list[str]:
    out: list[str] = []
    audit = data["audit"]
    chapter_rows = [chapter for part in data["book"]["parts"] for chapter in part.get("chapters", []) if chapter.get("id") == CHAPTER_ID]
    if len(chapter_rows) != 1 or audit.get("chapter_id") != CHAPTER_ID:
        out.append("chapter is not uniquely manifest admitted")
    if audit.get("state") != "terminal_integrated_argument_chapter" or audit.get("terminal_decision") != "integrate_at_argument_support":
        out.append("terminal integration decision drifted")
    if audit.get("reader_role") != "load-bearing-reference" or CHAPTER_ID not in data["roles"]["chapter_roles"].get("load-bearing-reference", []):
        out.append("reader-role classification drifted")
    for key, path_key in (("chapter_sha256", "chapter_path"),):
        if audit.get(key) != digest(ROOT / audit[path_key]):
            out.append(f"digest drifted: {key}")
    formal = audit["formalization"]
    contract = audit["record_contract"]
    lane = audit["claim_bearing_empirical_lane"]
    for expected, path in (
        (formal["module_sha256"], formal["module_path"]),
        (contract["schema_sha256"], contract["schema_path"]),
        (contract["fixture_sha256"], contract["fixture_path"]),
        (lane["protocol_sha256"], lane["protocol_path"]),
    ):
        if expected != digest(ROOT / path):
            out.append(f"digest drifted: {path}")
    if (formal.get("public_target_count"), formal.get("implemented_target_count"), formal.get("theorem_declaration_count")) != (2, 2, 9):
        out.append("formal denominator drifted")
    if sum(record.get("module") == formal["module"] for record in data["manifest"].get("records", [])) != 2:
        out.append("proof manifest target denominator drifted")
    if len(re.findall(r"(?m)^theorem ", (ROOT / formal["module_path"]).read_text(encoding="utf-8"))) != 9:
        out.append("Lean theorem denominator drifted")
    if contract.get("fixture_disposition") != "safe_hold" or contract.get("semantic_mutations_rejected") != 13 or contract.get("record_shape_only") is not True:
        out.append("record-contract custody drifted")

    assigned = audit["source_crosswalk"]["primary_external_source_ids"] + audit["source_crosswalk"]["supporting_corben_source_ids"]
    if len(assigned) != 10 or audit["source_crosswalk"].get("assigned_source_count") != 10:
        out.append("source denominator drifted")
    inventory = {row["id"]: row for row in data["inventory"]}
    for source_id in assigned:
        if source_id not in inventory or CHAPTER_ID not in inventory[source_id].get("chapter_targets", []):
            out.append(f"source target missing: {source_id}")
    if audit["source_crosswalk"].get("external_results_inherited_as_local_support") is not False:
        out.append("external source support laundering")

    predecessor = audit["predecessor_evidence"]
    if predecessor.get("disposition") != "adjacent_bounded_synthetic_evidence_only" or predecessor.get("chapter_core_support_transfer") != "none":
        out.append("P4/M8 predecessor evidence boundary drifted")
    if (predecessor.get("authored_environment_count"), predecessor.get("episode_count"), predecessor.get("heldout_episode_count"), predecessor.get("governed_replacement_and_rollback_count")) != (2, 11250, 6000, 10):
        out.append("P4/M8 bounded denominator drifted")

    protocol = load(ROOT / lane["protocol_path"])
    if lane.get("state") != "protocol_ready_resource_isolated_not_executed" or lane.get("protected_outcomes_opened") is not False:
        out.append("audited claim-bearing lane state drifted")
    if protocol.get("state") != lane.get("state") or protocol.get("protected_outcomes_opened") is not False:
        out.append("claim-bearing protocol state drifted")
    if (lane.get("arm_count"), lane.get("competence_gate_count"), lane.get("rescue_step_count"), lane.get("joint_outcome_count"), lane.get("causal_ablation_count")) != (6, 8, 7, 10, 6):
        out.append("claim-bearing denominator drifted")
    if lane.get("p2_displacement_allowed") is not False or lane.get("empirical_result") != "none":
        out.append("claim-bearing lane displaced P2 or invented a result")

    surfaces = {
        "index": (ROOT / "index.qmd").read_text(encoding="utf-8"),
        "chapter": (ROOT / audit["chapter_path"]).read_text(encoding="utf-8"),
        "previous": (ROOT / "chapters/planning-as-a-control-layer.qmd").read_text(encoding="utf-8"),
        "next": (ROOT / "chapters/cognitive-compilation-and-semantic-ir.qmd").read_text(encoding="utf-8"),
        "glossary": (ROOT / "appendices/B_glossary.qmd").read_text(encoding="utf-8"),
        "claims": (ROOT / "appendices/C_claim_evidence_matrix.qmd").read_text(encoding="utf-8"),
        "corben": (ROOT / "appendices/G_corben_source_corpus.qmd").read_text(encoding="utf-8"),
        "external": (ROOT / "appendices/H_external_sources.qmd").read_text(encoding="utf-8"),
        "synthesis": (ROOT / "chapters/integrated-reference-architecture.qmd").read_text(encoding="utf-8"),
    }
    required = {
        "index": ["Qualified world-model branches", "Reality-residual records"],
        "chapter": ["Why this boundary earns a chapter", "integrate at argument support", "protocol-ready and resource-isolated, not executed", "does not establish the chapter core"],
        "previous": ["qualified branch packets", "cannot authorize an effect"],
        "next": ["qualified branch packet", "may not compile an imagined consequence"],
        "glossary": ["Qualified branch packet", "Reality-residual record"],
        "claims": ["governed-world-models-and-reality-grounding.core"],
        "synthesis": ["Qualified branch packets", "reality-residual records"],
    }
    for surface, phrases in required.items():
        normalized_surface = re.sub(r"\s+", " ", surfaces[surface])
        for phrase in phrases:
            if phrase not in normalized_surface:
                out.append(f"reader integration missing from {surface}: {phrase}")
    for source_id in audit["source_crosswalk"]["supporting_corben_source_ids"]:
        if source_id not in surfaces["corben"] or CHAPTER_ID not in surfaces["corben"]:
            out.append(f"Corben appendix integration missing: {source_id}")
    for source_id in audit["source_crosswalk"]["primary_external_source_ids"]:
        if source_id not in surfaces["external"] or CHAPTER_ID not in surfaces["external"]:
            out.append(f"external appendix integration missing: {source_id}")

    tranche = data["status"]["quality_uplift_program"]["structural_completeness_tranche"]["first_tranche"]
    if tranche.get("completed_reader_chapter_count", 0) < 2 or CHAPTER_ID not in tranche.get("terminal_reader_chapter_ids", []) or CHAPTER_ID in tranche.get("remaining_reader_chapter_ids", []):
        out.append("machine status lacks terminal T2 custody")
    if any(audit.get(key) != "none" for key in ("support_state_effect", "release_effect", "publication_effect")):
        out.append("integration packet claims unauthorized state movement")
    return out


def main() -> None:
    data = {
        "audit": load(AUDIT), "book": load(BOOK), "inventory": load(INVENTORY),
        "manifest": load(MANIFEST), "status": load(STATUS), "roles": load(ROLES),
    }
    failures = errors(data)
    mutations = [
        ("remove chapter", lambda value: next(part for part in value["book"]["parts"] if any(ch.get("id") == CHAPTER_ID for ch in part.get("chapters", [])))["chapters"].pop(next(i for i, ch in enumerate(next(part for part in value["book"]["parts"] if any(ch.get("id") == CHAPTER_ID for ch in part.get("chapters", [])))["chapters"]) if ch.get("id") == CHAPTER_ID))),
        ("change decision", lambda value: value["audit"].__setitem__("terminal_decision", "remove")),
        ("change chapter digest", lambda value: value["audit"].__setitem__("chapter_sha256", "0" * 64)),
        ("lower proof count", lambda value: value["audit"]["formalization"].__setitem__("public_target_count", 1)),
        ("borrow predecessor", lambda value: value["audit"]["predecessor_evidence"].__setitem__("chapter_core_support_transfer", "argument")),
        ("open outcomes", lambda value: value["audit"]["claim_bearing_empirical_lane"].__setitem__("protected_outcomes_opened", True)),
        ("change protocol state", lambda value: value["audit"]["claim_bearing_empirical_lane"].__setitem__("state", "completed")),
        ("allow P2 displacement", lambda value: value["audit"]["claim_bearing_empirical_lane"].__setitem__("p2_displacement_allowed", True)),
        ("erase role", lambda value: value["roles"]["chapter_roles"]["load-bearing-reference"].remove(CHAPTER_ID)),
        ("erase completion custody", lambda value: value["status"]["quality_uplift_program"]["structural_completeness_tranche"]["first_tranche"].__setitem__("terminal_reader_chapter_ids", [])),
        ("invent support", lambda value: value["audit"].__setitem__("support_state_effect", "empirical-test-backed")),
        ("invent publication", lambda value: value["audit"].__setitem__("publication_effect", "published")),
        ("erase source target", lambda value: next(row for row in value["inventory"] if row["id"] == "ext_world_models_2018")["chapter_targets"].remove(CHAPTER_ID)),
    ]
    baseline = set(errors(data))
    for label, mutation in mutations:
        candidate = copy.deepcopy(data)
        mutation(candidate)
        if not set(errors(candidate)) - baseline:
            failures.append(f"negative mutation accepted: {label}")
    contract = subprocess.run([sys.executable, "scripts/validate_governed_world_model_contract.py"], cwd=ROOT, text=True, capture_output=True)
    if contract.returncode:
        failures.append("governed world-model contract failed: " + (contract.stdout + contract.stderr).strip())
    if failures:
        raise SystemExit("P7.2-T2 reader integration failed:\n - " + "\n - ".join(failures))
    print(
        "P7.2-T2 reader integration passed: 1 terminal argument-level chapter, 10 source "
        "mappings, 2 implemented public proof targets, 9 theorem declarations, 6 arms, "
        "8 competence gates, protected outcomes closed, 13 integration mutations rejected; "
        "support/release/publication none."
    )


if __name__ == "__main__":
    main()
