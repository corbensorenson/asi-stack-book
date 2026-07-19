#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "evidence_quality/p7_2_t3_human_factors_reader_integration.json"
STATUS = ROOT / "roadmap_records/post_v2_3_maintenance_transfer_and_publication_status.json"
STRUCTURE = ROOT / "book_structure.json"
SOURCES = ROOT / "sources/source_inventory.json"
MANIFEST = ROOT / "proofs/proof_manifest.json"
CHAPTER_ID = "human-factors-and-meaningful-control-in-oversight"
EXPECTED_SOURCES = [
    "viea", "talos", "theseus_operator_os", "scf",
    "ext_humans_automation_1997", "ext_ironies_automation_1983",
    "ext_levels_automation_2000", "ext_complacency_bias_automation_2010",
    "ext_meaningful_human_control_actionable_2022", "ext_agentic_oversight_practice_2026",
]


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def errors(data: dict[str, Any]) -> list[str]:
    out: list[str] = []
    audit = data["audit"]
    if audit.get("state") != "terminal_integrated_argument_chapter" or audit.get("terminal_decision") != "integrate_at_argument_support":
        out.append("terminal chapter disposition drifted")
    if audit.get("chapter_id") != CHAPTER_ID or audit.get("reader_role") != "load-bearing-reference":
        out.append("chapter identity or reader role drifted")
    for path_key, digest_key, owner in (
        (("chapter_path",), "chapter_sha256", audit),
        (("formalization", "module_path"), "module_sha256", audit.get("formalization", {})),
        (("record_contract", "schema_path"), "schema_sha256", audit.get("record_contract", {})),
        (("record_contract", "fixture_path"), "fixture_sha256", audit.get("record_contract", {})),
        (("claim_bearing_empirical_lane", "protocol_path"), "protocol_sha256", audit.get("claim_bearing_empirical_lane", {})),
    ):
        value: Any = audit
        for part in path_key:
            value = value.get(part, {}) if isinstance(value, dict) else {}
        if not isinstance(value, str) or not (ROOT / value).is_file() or owner.get(digest_key) != sha(ROOT / value):
            out.append(f"digest or artifact drifted: {'.'.join(path_key)}")

    source_ids = audit.get("source_crosswalk", {}).get("primary_external_source_ids", []) + audit.get("source_crosswalk", {}).get("supporting_corben_source_ids", [])
    if set(source_ids) != set(EXPECTED_SOURCES) or audit.get("source_crosswalk", {}).get("assigned_source_count") != 10:
        out.append("source denominator drifted")
    inventory = {row["id"]: row for row in data["sources"]}
    if any(source_id not in inventory or CHAPTER_ID not in inventory[source_id].get("chapter_targets", []) for source_id in EXPECTED_SOURCES):
        out.append("source inventory target missing")
    structure_chapters = [chapter for part in data["structure"]["parts"] for chapter in part["chapters"]]
    chapter = next((row for row in structure_chapters if row["id"] == CHAPTER_ID), None)
    if chapter is None or set(chapter.get("source_ids", [])) != set(EXPECTED_SOURCES):
        out.append("manifest source assignment drifted")
    targets = [row for row in data["manifest"]["records"] if row.get("chapter_id") == CHAPTER_ID]
    if len(targets) != 2 or any(row.get("status") != "implemented" for row in targets):
        out.append("proof target implementation denominator drifted")
    formal = audit.get("formalization", {})
    if formal.get("public_target_count") != 2 or formal.get("implemented_target_count") != 2 or formal.get("theorem_declaration_count") != 9:
        out.append("formal denominator drifted")
    record = audit.get("record_contract", {})
    if record.get("fixture_disposition") != "safe_hold" or record.get("human_participants_observed") != 0 or record.get("semantic_mutations_rejected") != 15:
        out.append("record fixture or mutation boundary drifted")
    lane = audit.get("claim_bearing_empirical_lane", {})
    if lane.get("state") != "protocol_ready_ethics_and_resource_authority_required_not_executed":
        out.append("empirical protocol state drifted")
    expected_lane = {
        "arm_count": 4, "competence_gate_count": 9, "positive_control_count": 5,
        "adversarial_control_count": 7, "rescue_step_count": 6, "joint_outcome_count": 12,
        "human_participants_recruited": 0,
    }
    if any(lane.get(key) != value for key, value in expected_lane.items()):
        out.append("empirical denominator drifted")
    if lane.get("protected_outcomes_opened") is not False or lane.get("p2_displacement_allowed") is not False or lane.get("prepublication_human_review_substitution_allowed") is not False:
        out.append("outcome, P2, or review-isolation boundary drifted")
    integration = audit.get("reader_integration", {})
    required_integration = (
        "opening_map_updated", "role_classification_preserved", "exclusive_owner_section_present",
        "previous_handoff_updated", "next_handoff_updated", "overview_figure_updated",
        "claim_matrix_reconciled", "corben_source_appendix_reconciled",
        "external_source_appendix_reconciled", "final_synthesis_updated",
    )
    if any(integration.get(key) is not True for key in required_integration) or integration.get("glossary_terms_added") != 2:
        out.append("reader integration surface drifted")
    status = data["status"]
    immediate_packet = status["execution_readiness"].get("immediate_book_packet")
    if not isinstance(immediate_packet, str) or immediate_packet == "P7.2-T3-human-factors-and-meaningful-control-in-oversight":
        out.append("machine status did not advance beyond T3")
    first = status["quality_uplift_program"]["structural_completeness_tranche"]["first_tranche"]
    if first.get("completed_reader_chapter_count", 0) < 3 or CHAPTER_ID not in first.get("terminal_reader_chapter_ids", []) or CHAPTER_ID in first.get("remaining_reader_chapter_ids", []):
        out.append("first-tranche terminal denominator drifted")
    for key in ("support_state_effect", "release_effect", "publication_effect"):
        if audit.get(key) != "none":
            out.append(f"unauthorized {key}")

    surfaces = {
        "index": (ROOT / "index.qmd").read_text(encoding="utf-8"),
        "intent": (ROOT / "chapters/human-intent-as-a-formal-input.qmd").read_text(encoding="utf-8"),
        "constitution": (ROOT / "chapters/constitutional-alignment-substrate.qmd").read_text(encoding="utf-8"),
        "glossary": (ROOT / "appendices/B_glossary.qmd").read_text(encoding="utf-8"),
        "integration": (ROOT / "chapters/integrated-reference-architecture.qmd").read_text(encoding="utf-8"),
    }
    required_fragments = {
        "index": ["Human control-envelope check", "cannot infer a person's internal state"],
        "intent": ["Human Factors and Meaningful Control in Oversight"],
        "constitution": ["Human Factors", "operationally usable"],
        "glossary": ["Human control-envelope packet", "Ceremonial approval"],
        "integration": ["control-envelope packet", "does not prove comprehension"],
    }
    for surface, fragments in required_fragments.items():
        for fragment in fragments:
            if fragment not in surfaces[surface]:
                out.append(f"{surface} missing reader integration fragment: {fragment}")
    return out


def main() -> None:
    data = {
        "audit": load(AUDIT), "status": load(STATUS), "structure": load(STRUCTURE),
        "sources": load(SOURCES), "manifest": load(MANIFEST),
    }
    failures = errors(data)
    mutations = [
        ("terminal removal", lambda value: value["audit"].__setitem__("terminal_decision", "remove")),
        ("source deletion", lambda value: value["audit"]["source_crosswalk"]["primary_external_source_ids"].pop()),
        ("digest drift", lambda value: value["audit"].__setitem__("chapter_sha256", "0" * 64)),
        ("proof reduction", lambda value: value["audit"]["formalization"].__setitem__("implemented_target_count", 1)),
        ("invent participant", lambda value: value["audit"]["claim_bearing_empirical_lane"].__setitem__("human_participants_recruited", 1)),
        ("outcome opening", lambda value: value["audit"]["claim_bearing_empirical_lane"].__setitem__("protected_outcomes_opened", True)),
        ("P2 displacement", lambda value: value["audit"]["claim_bearing_empirical_lane"].__setitem__("p2_displacement_allowed", True)),
        ("review substitution", lambda value: value["audit"]["claim_bearing_empirical_lane"].__setitem__("prepublication_human_review_substitution_allowed", True)),
        ("role deletion", lambda value: value["audit"]["reader_integration"].__setitem__("exclusive_owner_section_present", False)),
        ("glossary deletion", lambda value: value["audit"]["reader_integration"].__setitem__("glossary_terms_added", 1)),
        ("support laundering", lambda value: value["audit"].__setitem__("support_state_effect", "empirical-test-backed")),
        ("reopen status", lambda value: value["status"]["execution_readiness"].__setitem__("immediate_book_packet", "P7.2-T3-human-factors-and-meaningful-control-in-oversight")),
        ("remove terminal chapter", lambda value: value["status"]["quality_uplift_program"]["structural_completeness_tranche"]["first_tranche"]["terminal_reader_chapter_ids"].remove(CHAPTER_ID)),
    ]
    baseline = set(errors(data))
    for label, mutation in mutations:
        candidate = copy.deepcopy(data)
        mutation(candidate)
        if not set(errors(candidate)) - baseline:
            failures.append(f"negative mutation accepted: {label}")
    contract = subprocess.run(
        [sys.executable, "scripts/validate_human_oversight_control_contract.py"],
        cwd=ROOT, text=True, capture_output=True,
    )
    if contract.returncode:
        failures.append((contract.stdout + contract.stderr).strip())
    if failures:
        raise SystemExit("P7.2-T3 reader integration failed:\n - " + "\n - ".join(failures))
    print(
        "P7.2-T3 reader integration passed: 1 terminal argument-level chapter, "
        "10 source mappings, 2 implemented public proof targets, 9 theorem declarations, "
        "4 arms, 9 competence gates, no participants, protected outcomes closed, "
        "13 integration mutations rejected; support/release/publication none."
    )


if __name__ == "__main__":
    main()
