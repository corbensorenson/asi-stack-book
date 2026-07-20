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
AUDIT = ROOT / "evidence_quality/p7_2_t4_governed_operations_reader_integration.json"
STATUS = ROOT / "roadmap_records/post_v2_3_maintenance_transfer_and_publication_status.json"
STRUCTURE = ROOT / "book_structure.json"
SOURCES = ROOT / "sources/source_inventory.json"
MANIFEST = ROOT / "proofs/proof_manifest.json"
CHAPTER_ID = "governed-operations-incident-command-and-graceful-degradation"
EXPECTED_SOURCES = ["scf", "deterministic_capability_compilation", "theseus_operator_os", "viea", "talos", "platonic_world_model", "ext_nist_ai_rmf_1_0_2023", "ext_nist_deployed_ai_monitoring_2026", "ext_nist_incident_response_2025"]


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def errors(data: dict[str, Any]) -> list[str]:
    out: list[str] = []
    audit = data["audit"]
    if audit.get("state") != "terminal_integrated_argument_chapter" or audit.get("terminal_decision") != "integrate_at_argument_support" or audit.get("chapter_id") != CHAPTER_ID:
        out.append("terminal chapter disposition drifted")
    for path_keys, digest_key, owner in (
        (("chapter_path",), "chapter_sha256", audit),
        (("formalization", "module_path"), "module_sha256", audit.get("formalization", {})),
        (("record_contract", "schema_path"), "schema_sha256", audit.get("record_contract", {})),
        (("record_contract", "fixture_path"), "fixture_sha256", audit.get("record_contract", {})),
        (("claim_bearing_empirical_lane", "protocol_path"), "protocol_sha256", audit.get("claim_bearing_empirical_lane", {})),
    ):
        value: Any = audit
        for key in path_keys:
            value = value.get(key, {}) if isinstance(value, dict) else {}
        if not isinstance(value, str) or not (ROOT / value).is_file() or owner.get(digest_key) != sha(ROOT / value):
            out.append(f"digest or artifact drifted: {'.'.join(path_keys)}")
    source_ids = audit["source_crosswalk"]["primary_external_source_ids"] + audit["source_crosswalk"]["supporting_corben_source_ids"]
    if set(source_ids) != set(EXPECTED_SOURCES) or audit["source_crosswalk"].get("assigned_source_count") != 9:
        out.append("source denominator drifted")
    inventory = {row["id"]: row for row in data["sources"]}
    if any(source_id not in inventory or CHAPTER_ID not in inventory[source_id].get("chapter_targets", []) for source_id in EXPECTED_SOURCES):
        out.append("source inventory target missing")
    chapters = [chapter for part in data["structure"]["parts"] for chapter in part["chapters"]]
    chapter = next((row for row in chapters if row["id"] == CHAPTER_ID), None)
    if chapter is None or set(chapter.get("source_ids", [])) != set(EXPECTED_SOURCES):
        out.append("manifest source assignment drifted")
    targets = [row for row in data["manifest"]["records"] if row.get("chapter_id") == CHAPTER_ID]
    if len(targets) != 2 or any(row.get("status") != "implemented" for row in targets):
        out.append("proof target implementation denominator drifted")
    formal = audit["formalization"]
    if formal.get("public_target_count") != 2 or formal.get("implemented_target_count") != 2 or formal.get("theorem_declaration_count") != 13:
        out.append("formal denominator drifted")
    record = audit["record_contract"]
    if record.get("fixture_degradation_route") != "accept_degraded" or record.get("fixture_recovery_route") != "safe_hold" or record.get("declared_state_class_count") != 11 or record.get("semantic_mutations_rejected") != 18 or record.get("natural_incidents_observed") != 0:
        out.append("record contract denominator or route drifted")
    lane = audit["claim_bearing_empirical_lane"]
    expected_lane = {"arm_count": 4, "competence_gate_count": 9, "positive_control_count": 5, "adversarial_control_count": 8, "rescue_step_count": 6, "joint_outcome_count": 13, "natural_tasks_run": 0, "fault_injections_run": 0, "operators_recruited": 0}
    if lane.get("state") != "protocol_ready_resource_and_environment_authority_required_not_executed" or any(lane.get(key) != value for key, value in expected_lane.items()):
        out.append("empirical lane state or denominator drifted")
    if lane.get("protected_outcomes_opened") is not False or lane.get("p2_q1_q2_overlap_allowed") is not False or lane.get("p2_displacement_allowed") is not False or lane.get("empirical_result") != "none":
        out.append("empirical custody drifted")
    flagship = audit["flagship_separation"]
    if flagship.get("authored_case_is_theseus_t4") is not False or flagship.get("theseus_t4_state") != "blocked_by_T2_and_T3" or flagship.get("flagship_outcomes_opened") is not False or flagship.get("flagship_support_transferred") is not False:
        out.append("flagship separation drifted")
    integration = audit["reader_integration"]
    required = ("opening_map_updated", "role_classification_preserved", "exclusive_owner_section_present", "previous_handoff_updated", "next_handoff_updated", "overview_figure_updated", "claim_matrix_reconciled", "corben_source_appendix_reconciled", "external_source_appendix_reconciled", "final_synthesis_updated")
    if any(integration.get(key) is not True for key in required) or integration.get("glossary_terms_added") != 2:
        out.append("reader integration surface drifted")
    status = data["status"]
    first = status["quality_uplift_program"]["structural_completeness_tranche"]["first_tranche"]
    if first.get("state") != "terminal_four_reader_chapters" or first.get("completed_reader_chapter_count") != 4 or CHAPTER_ID not in first.get("terminal_reader_chapter_ids", []) or first.get("remaining_reader_chapter_ids") != []:
        out.append("first-tranche terminal state drifted")
    if status["execution_readiness"].get("immediate_book_packet") != "P6.4-A2-privacy-data-rights-and-information-flow-governance-adjudication":
        out.append("execution board did not preserve terminal operations while advancing to second-tranche A2")
    for key in ("support_state_effect", "release_effect", "publication_effect"):
        if audit.get(key) != "none": out.append(f"unauthorized {key}")
    surfaces = {"index": (ROOT / "index.qmd").read_text(), "safety": (ROOT / "chapters/safety-cases-and-structured-assurance.qmd").read_text(), "policy": (ROOT / "chapters/policy-optimization-and-learning-from-feedback.qmd").read_text(), "glossary": (ROOT / "appendices/B_glossary.qmd").read_text(), "integration": (ROOT / "chapters/integrated-reference-architecture.qmd").read_text()}
    required_fragments = {"index": ["Governed operations and incident control", "operations loop is equally non-promotional"], "safety": ["Governed Operations, Incident Command, and Graceful Degradation"], "policy": ["Governed Operations may hand this layer"], "glossary": ["Operational continuity contract", "Effect-complete recovery"], "integration": ["Governed Operations control packet", "not the natural Theseus T4 trace"]}
    for surface, fragments in required_fragments.items():
        for fragment in fragments:
            if fragment not in surfaces[surface]: out.append(f"{surface} missing reader fragment: {fragment}")
    return out


def main() -> None:
    data = {"audit": load(AUDIT), "status": load(STATUS), "structure": load(STRUCTURE), "sources": load(SOURCES), "manifest": load(MANIFEST)}
    failures = errors(data)
    mutations = [
        ("terminal removal", lambda v: v["audit"].__setitem__("terminal_decision", "remove")),
        ("source deletion", lambda v: v["audit"]["source_crosswalk"]["supporting_corben_source_ids"].pop()),
        ("digest drift", lambda v: v["audit"].__setitem__("chapter_sha256", "0" * 64)),
        ("proof reduction", lambda v: v["audit"]["formalization"].__setitem__("implemented_target_count", 1)),
        ("invent incident", lambda v: v["audit"]["record_contract"].__setitem__("natural_incidents_observed", 1)),
        ("claim recovery", lambda v: v["audit"]["record_contract"].__setitem__("fixture_recovery_route", "accept_recovery")),
        ("outcome opening", lambda v: v["audit"]["claim_bearing_empirical_lane"].__setitem__("protected_outcomes_opened", True)),
        ("denominator overlap", lambda v: v["audit"]["claim_bearing_empirical_lane"].__setitem__("p2_q1_q2_overlap_allowed", True)),
        ("flagship laundering", lambda v: v["audit"]["flagship_separation"].__setitem__("authored_case_is_theseus_t4", True)),
        ("role deletion", lambda v: v["audit"]["reader_integration"].__setitem__("exclusive_owner_section_present", False)),
        ("support laundering", lambda v: v["audit"].__setitem__("support_state_effect", "empirical-test-backed")),
        ("reopen first tranche", lambda v: v["status"]["quality_uplift_program"]["structural_completeness_tranche"]["first_tranche"].__setitem__("completed_reader_chapter_count", 3)),
        ("execution rollback", lambda v: v["status"]["execution_readiness"].__setitem__("immediate_book_packet", "P7.2-T4-governed-operations-incident-command-and-graceful-degradation")),
    ]
    baseline = set(errors(data))
    for label, mutation in mutations:
        candidate = copy.deepcopy(data); mutation(candidate)
        if not set(errors(candidate)) - baseline: failures.append(f"negative mutation accepted: {label}")
    contract = subprocess.run([sys.executable, "scripts/validate_governed_operations_control_contract.py"], cwd=ROOT, text=True, capture_output=True)
    if contract.returncode: failures.append((contract.stdout + contract.stderr).strip())
    if failures: raise SystemExit("P7.2-T4 reader integration failed:\n - " + "\n - ".join(failures))
    print("P7.2-T4 reader integration passed: first tranche terminal at 4 argument-level chapters, 9 source mappings, 2 implemented targets, 13 Lean declarations, authored safe hold, 4-arm campaign unexecuted, flagship separate, 13 integration mutations rejected; support/release/publication none.")


if __name__ == "__main__":
    main()
