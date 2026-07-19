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
AUDIT = ROOT / "evidence_quality/p7_2_t1_white_box_reader_integration.json"
BOOK = ROOT / "book_structure.json"
INVENTORY = ROOT / "sources/source_inventory.json"
MANIFEST = ROOT / "proofs/proof_manifest.json"
STATUS = ROOT / "roadmap_records/post_v2_3_maintenance_transfer_and_publication_status.json"
ROLES = ROOT / "evidence_quality/p7_1a_w2_narrative_audit.json"
CHAPTER_ID = "white-box-evidence-interpretability-and-activation-governance"


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def find_chapter(book: dict[str, Any]) -> dict[str, Any] | None:
    for part in book.get("parts", []):
        for chapter in part.get("chapters", []):
            if chapter.get("id") == CHAPTER_ID:
                return chapter
    return None


def errors(data: dict[str, Any]) -> list[str]:
    out: list[str] = []
    audit = data["audit"]
    if audit.get("state") != "terminal_integrated_argument_chapter" or audit.get("terminal_decision") != "integrate_at_argument_support":
        out.append("terminal chapter decision drifted")
    chapter_record = find_chapter(data["book"])
    if chapter_record is None:
        return out + ["manifest chapter missing"]
    expected_sources = audit["source_crosswalk"]["primary_external_source_ids"] + audit["source_crosswalk"]["supporting_corben_source_ids"]
    if chapter_record.get("source_ids") != audit["source_crosswalk"]["supporting_corben_source_ids"] + audit["source_crosswalk"]["primary_external_source_ids"]:
        out.append("manifest source order or denominator drifted")
    inventory_by_id = {row["id"]: row for row in data["inventory"]}
    for source_id in expected_sources:
        if source_id not in inventory_by_id or CHAPTER_ID not in inventory_by_id[source_id].get("chapter_targets", []):
            out.append(f"source inventory target missing: {source_id}")
    digest_surfaces = [
        ("chapter_sha256", audit["chapter_path"]),
        ("module_sha256", audit["formalization"]["module_path"]),
        ("schema_sha256", audit["record_contract"]["schema_path"]),
        ("fixture_sha256", audit["record_contract"]["fixture_path"]),
        ("protocol_sha256", audit["claim_bearing_empirical_lane"]["protocol_path"]),
    ]
    for digest_key, relative in digest_surfaces:
        owner = audit
        if digest_key == "module_sha256": owner = audit["formalization"]
        elif digest_key in {"schema_sha256", "fixture_sha256"}: owner = audit["record_contract"]
        elif digest_key == "protocol_sha256": owner = audit["claim_bearing_empirical_lane"]
        path = ROOT / relative
        if not path.is_file() or sha256(path) != owner.get(digest_key):
            out.append(f"digest drifted: {relative}")
    targets = [row for row in data["manifest"].get("records", []) if row.get("module") == "AsiStackProofs.WhiteBoxEvidence"]
    if len(targets) != 2 or any(row.get("status") != "implemented" for row in targets):
        out.append("white-box public proof targets are not both implemented")
    if audit["formalization"].get("public_target_count") != 2 or audit["formalization"].get("implemented_target_count") != 2 or audit["formalization"].get("theorem_declaration_count") != 8:
        out.append("audited formal denominator drifted")
    lean_text = (ROOT / audit["formalization"]["module_path"]).read_text(encoding="utf-8")
    if len(re.findall(r"(?m)^theorem ", lean_text)) != 8:
        out.append("white-box theorem denominator drifted")
    if CHAPTER_ID not in data["roles"]["chapter_roles"].get("load-bearing-reference", []):
        out.append("reader-role classification drifted")
    status_first = data["status"]["quality_uplift_program"]["structural_completeness_tranche"]["first_tranche"]
    if status_first.get("completed_reader_chapter_count") != 1 or status_first.get("terminal_reader_chapter_ids") != [CHAPTER_ID]:
        out.append("machine first-tranche completion custody drifted")
    protocol = load(ROOT / audit["claim_bearing_empirical_lane"]["protocol_path"])
    if protocol.get("state") != "protocol_ready_resource_isolated_not_executed" or protocol.get("protected_outcomes_opened") is not False:
        out.append("claim-bearing protocol state drifted")
    lane = audit["claim_bearing_empirical_lane"]
    if lane.get("state") != "protocol_ready_resource_isolated_not_executed" or lane.get("protected_outcomes_opened") is not False:
        out.append("audited claim-bearing lane state drifted")
    if (lane.get("method_family_count"), lane.get("competence_gate_count"), lane.get("rescue_step_count"), lane.get("joint_outcome_count")) != (2, 7, 6, 9):
        out.append("audited claim-bearing denominator drifted")
    if lane.get("p2_displacement_allowed") is not False or lane.get("empirical_result") != "none":
        out.append("claim-bearing lane displaced P2 or invented an empirical result")
    surfaces = {
        "index": (ROOT / "index.qmd").read_text(encoding="utf-8"),
        "chapter": (ROOT / audit["chapter_path"]).read_text(encoding="utf-8"),
        "previous": (ROOT / "chapters/benchmark-ratchets-and-anti-goodhart-evidence.qmd").read_text(encoding="utf-8"),
        "next": (ROOT / "chapters/capability-thresholds-and-deployment-commitments.qmd").read_text(encoding="utf-8"),
        "glossary": (ROOT / "appendices/B_glossary.qmd").read_text(encoding="utf-8"),
        "claims": (ROOT / "appendices/C_claim_evidence_matrix.qmd").read_text(encoding="utf-8"),
        "corben": (ROOT / "appendices/G_corben_source_corpus.qmd").read_text(encoding="utf-8"),
        "external": (ROOT / "appendices/H_external_sources.qmd").read_text(encoding="utf-8"),
        "synthesis": (ROOT / "chapters/integrated-reference-architecture.qmd").read_text(encoding="utf-8"),
    }
    required = {
        "index": ["White-box evidence packets", "never grant"],
        "chapter": ["Why this boundary earns a chapter", "integrate at argument support", "protocol-ready and resource-isolated, not executed"],
        "previous": ["White-Box Evidence, Interpretability, and Activation Governance"],
        "next": ["White-Box Evidence, Interpretability, and Activation Governance"],
        "glossary": ["Internal Evidence Packet", "Activation policy candidate"],
        "claims": ["white-box-evidence-interpretability-and-activation-governance.core"],
        "synthesis": ["Internal Evidence Packet", "never grant execution or release authority"],
    }
    for surface, phrases in required.items():
        for phrase in phrases:
            if phrase not in surfaces[surface]:
                out.append(f"reader integration missing from {surface}: {phrase}")
    for source_id in audit["source_crosswalk"]["supporting_corben_source_ids"]:
        if source_id not in surfaces["corben"] or CHAPTER_ID not in surfaces["corben"]:
            out.append(f"Corben appendix integration missing: {source_id}")
    for source_id in audit["source_crosswalk"]["primary_external_source_ids"]:
        if source_id not in surfaces["external"] or CHAPTER_ID not in surfaces["external"]:
            out.append(f"external appendix integration missing: {source_id}")
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
        ("remove source target", lambda value: next(row for row in value["inventory"] if row["id"] == "ext_circuit_tracing_2025")["chapter_targets"].remove(CHAPTER_ID)),
        ("change decision", lambda value: value["audit"].__setitem__("terminal_decision", "remove")),
        ("change chapter digest", lambda value: value["audit"].__setitem__("chapter_sha256", "0" * 64)),
        ("lower proof count", lambda value: value["audit"]["formalization"].__setitem__("public_target_count", 1)),
        ("open outcomes", lambda value: value["audit"]["claim_bearing_empirical_lane"].__setitem__("protected_outcomes_opened", True)),
        ("change protocol state", lambda value: value["audit"]["claim_bearing_empirical_lane"].__setitem__("state", "completed")),
        ("allow P2 displacement", lambda value: value["audit"]["claim_bearing_empirical_lane"].__setitem__("p2_displacement_allowed", True)),
        ("erase role", lambda value: value["roles"]["chapter_roles"]["load-bearing-reference"].remove(CHAPTER_ID)),
        ("erase completion custody", lambda value: value["status"]["quality_uplift_program"]["structural_completeness_tranche"]["first_tranche"].__setitem__("terminal_reader_chapter_ids", [])),
        ("invent support", lambda value: value["audit"].__setitem__("support_state_effect", "empirical-test-backed")),
        ("invent publication", lambda value: value["audit"].__setitem__("publication_effect", "published")),
    ]
    baseline = set(errors(data))
    for label, mutation in mutations:
        candidate = copy.deepcopy(data)
        mutation(candidate)
        if not set(errors(candidate)) - baseline:
            failures.append(f"negative mutation accepted: {label}")
    contract = subprocess.run(
        [sys.executable, "scripts/validate_white_box_evidence_contract.py"],
        cwd=ROOT, text=True, capture_output=True,
    )
    if contract.returncode:
        failures.append("white-box contract consumer failed: " + (contract.stdout + contract.stderr).strip())
    if failures:
        raise SystemExit("P7.2-T1 reader integration failed:\n - " + "\n - ".join(failures))
    print(
        "P7.2-T1 reader integration passed: 1 terminal argument-level chapter, 8 source "
        "mappings, 2 implemented public proof targets, 8 theorem declarations, 2 method "
        "families, 7 competence gates, protected outcomes closed, 12 integration mutations "
        "rejected; support effect none."
    )


if __name__ == "__main__":
    main()
