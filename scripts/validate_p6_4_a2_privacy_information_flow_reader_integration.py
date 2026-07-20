#!/usr/bin/env python3
"""Validate terminal P6.4-A2 source, proof, protocol, and reader integration."""

from __future__ import annotations
import copy, hashlib, json, re, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTER_ID = "privacy-data-rights-and-information-flow-governance"
AUDIT = ROOT / "evidence_quality/p6_4_a2_privacy_information_flow_reader_integration.json"
SOURCE_IDS = {"ext_nist_privacy_framework_2020", "ext_eu_gdpr_2016", "ext_w3c_dpv_2024", "ext_abadi_dpsgd_2016", "ext_algospec_purpose_limitation_2024", "ext_carlini_training_data_extraction_2021", "ext_choquette_choo_label_only_mia_2021", "ext_nist_differential_privacy_2025", "ext_mahloujifar_fdp_audit_2025"}
LOCAL_SOURCE_IDS = {"theseus_synthetic_data_curation"}
NEXT_ID = "perception-sensor-fusion-and-observation-trust"
NEXT_PACKET = f"P6.4-A3-{NEXT_ID}-adjudication"

def load(path: Path): return json.loads(path.read_text(encoding="utf-8"))
def sha(path: Path): return hashlib.sha256(path.read_bytes()).hexdigest()

def errors(data: dict) -> list[str]:
    out, audit = [], data["audit"]
    if audit.get("decision") != "admit_at_argument_support" or audit.get("candidate_id") != CHAPTER_ID: out.append("A2 decision or identity drifted")
    roles = audit.get("source_roles", {})
    if set(roles) != {"mechanism_or_capability", "limitation_or_failure", "competing_design", "measurement_or_evaluation"}: out.append("four-role vocabulary drifted")
    if {s for values in roles.values() for s in values} != SOURCE_IDS: out.append("nine-source role packet incomplete")
    chapters = [c for p in data["structure"]["parts"] for c in p["chapters"]]; ids = [c["id"] for c in chapters]
    if len(ids) != 61 or ids.count(CHAPTER_ID) != 1: out.append("61-chapter manifest or A2 uniqueness drifted")
    i = ids.index(CHAPTER_ID) if CHAPTER_ID in ids else -1
    if i < 1 or ids[i-1] != "security-kernel-and-digital-scifs" or ids[i+1] != "model-weight-custody-and-hardware-roots-of-trust": out.append("A2 placement drifted")
    chapter = next((c for c in chapters if c["id"] == CHAPTER_ID), {})
    if set(chapter.get("source_ids", [])) != SOURCE_IDS | LOCAL_SOURCE_IDS or chapter.get("evidence_level") != "argument": out.append("A2 manifest source/support boundary drifted")
    if set(chapter.get("source_queue", {}).get("primary", [])) != SOURCE_IDS or set(chapter.get("source_queue", {}).get("supporting", [])) != LOCAL_SOURCE_IDS: out.append("A2 external/local source roles drifted")
    inventory = {r["id"]: r for r in data["sources"]}
    for sid in SOURCE_IDS:
        note = ROOT / f"sources/source_notes/{sid}.md"
        if sid not in inventory or CHAPTER_ID not in inventory[sid].get("chapter_targets", []): out.append(f"source target missing: {sid}")
        if not note.is_file() or any(h not in note.read_text() for h in ("## Thesis", "## Mechanisms", "## Evidence", "## Failure Modes", "## Book Chapters Supported", "## Claims To Add Or Update", "## Open Questions")): out.append(f"source note incomplete: {sid}")
    for sid in LOCAL_SOURCE_IDS:
        note = ROOT / f"sources/source_notes/{sid}.md"
        if sid not in inventory or CHAPTER_ID not in inventory[sid].get("chapter_targets", []): out.append(f"local source target missing: {sid}")
        if not note.is_file() or CHAPTER_ID not in note.read_text(): out.append(f"local source note incomplete: {sid}")
    proofs = [r for r in data["proofs"]["records"] if r["chapter_id"] == CHAPTER_ID]
    if len(proofs) != 2 or any(r.get("status") != "implemented" or r.get("module") != "AsiStackProofs.PrivacyInformationFlow" for r in proofs): out.append("A2 proof packet drifted")
    if len(re.findall(r"^theorem\s+", (ROOT / "lean/AsiStackProofs/PrivacyInformationFlow.lean").read_text(), re.M)) != 11: out.append("A2 theorem denominator drifted")
    protocol = data["protocol"]
    if protocol.get("state") != "prospectively_frozen_unexecuted" or protocol.get("protected_outcomes_opened") is not False or len(protocol.get("arms", [])) != 6 or len(protocol.get("failure_families", [])) != 13 or len(protocol.get("competence_gates", [])) != 15: out.append("A2 campaign custody drifted")
    second = data["status"]["quality_uplift_program"]["structural_completeness_tranche"]["second_tranche"]
    if second.get("manifest_admitted_count") != 2 or second.get("active_candidate_id") != NEXT_ID or data["status"]["execution_readiness"].get("immediate_book_packet") != NEXT_PACKET: out.append("A2 status did not advance exactly to A3")
    if second.get("terminal_candidate_dispositions", {}).get(CHAPTER_ID) != "admitted_terminal_argument_reader_chapter": out.append("A2 terminal disposition missing")
    surfaces = data["surfaces"]
    required = {"index": ["Purpose-bounded information use and data rights"], "glossary": ["Information Lifecycle Transaction", "Purpose Lease"], "outline": ["### Privacy, Data Rights, and Information-Flow Governance"], "roadmap": [NEXT_PACKET, "P6.4-A1 and P6.4-A2"], "security": ["Privacy, Data Rights, and Information-Flow Governance now governs"], "custody": ["already constrained by Privacy, Data Rights"]}
    for name, fragments in required.items():
        for fragment in fragments:
            if fragment not in surfaces[name]: out.append(f"{name} missing: {fragment}")
    for relative in audit.get("artifacts", {}).values():
        if not (ROOT / relative).is_file() or audit.get("artifact_sha256", {}).get(relative) != sha(ROOT / relative): out.append(f"artifact digest drifted: {relative}")
    for sid in SOURCE_IDS:
        if audit.get("source_note_sha256", {}).get(sid) != sha(ROOT / f"sources/source_notes/{sid}.md"): out.append(f"source-note digest drifted: {sid}")
    for sid in LOCAL_SOURCE_IDS:
        if audit.get("local_source_note_sha256", {}).get(sid) != sha(ROOT / f"sources/source_notes/{sid}.md"): out.append(f"local source-note digest drifted: {sid}")
    if any(audit.get(k) != "none" for k in ("legal_compliance_effect", "support_state_effect", "release_effect", "publication_effect")): out.append("A2 claims unauthorized effect")
    return out

def main() -> None:
    data = {"audit": load(AUDIT), "structure": load(ROOT/"book_structure.json"), "sources": load(ROOT/"sources/source_inventory.json"), "proofs": load(ROOT/"proofs/proof_manifest.json"), "protocol": load(ROOT/"experiments/privacy_information_flow_argument_exit/preregistration.json"), "status": load(ROOT/"roadmap_records/post_v2_3_maintenance_transfer_and_publication_status.json"), "surfaces": {"index": (ROOT/"index.qmd").read_text(), "glossary": (ROOT/"appendices/B_glossary.qmd").read_text(), "outline": (ROOT/"docs/book_outline.md").read_text(), "roadmap": (ROOT/"docs/post_v2_3_maintenance_transfer_and_publication_roadmap.md").read_text(), "security": (ROOT/"chapters/security-kernel-and-digital-scifs.qmd").read_text(), "custody": (ROOT/"chapters/model-weight-custody-and-hardware-roots-of-trust.qmd").read_text()}}
    failures = errors(data); baseline = set(failures)
    mutations = [("decision", lambda v: v["audit"].__setitem__("decision", "reject")), ("role", lambda v: v["audit"]["source_roles"]["measurement_or_evaluation"].clear()), ("manifest", lambda v: next(p for p in v["structure"]["parts"] if any(c["id"] == CHAPTER_ID for c in p["chapters"]))["chapters"].pop(next(i for i,c in enumerate(next(p for p in v["structure"]["parts"] if any(x["id"] == CHAPTER_ID for x in p["chapters"]))["chapters"]) if c["id"] == CHAPTER_ID))), ("proof", lambda v: next(r for r in v["proofs"]["records"] if r["chapter_id"] == CHAPTER_ID).__setitem__("status", "planned")), ("campaign", lambda v: v["protocol"].__setitem__("state", "complete")), ("outcomes", lambda v: v["protocol"].__setitem__("protected_outcomes_opened", True)), ("competence", lambda v: v["protocol"]["competence_gates"].pop()), ("terminal", lambda v: v["status"]["quality_uplift_program"]["structural_completeness_tranche"]["second_tranche"]["terminal_candidate_dispositions"].pop(CHAPTER_ID)), ("A3", lambda v: v["status"]["execution_readiness"].__setitem__("immediate_book_packet", "P6.4-A2-reopened")), ("compliance", lambda v: v["audit"].__setitem__("legal_compliance_effect", "claimed"))]
    for label, mutate in mutations:
        c = copy.deepcopy(data); mutate(c)
        if not set(errors(c)) - baseline: failures.append(f"negative mutation accepted: {label}")
    if failures: raise SystemExit("P6.4-A2 reader integration failed:\n- " + "\n- ".join(failures))
    probe = subprocess.run(["python3", "scripts/validate_information_lifecycle_transaction.py"], cwd=ROOT, capture_output=True, text=True)
    if probe.returncode: raise SystemExit(probe.stdout + probe.stderr)
    print("P6.4-A2 reader integration passed: terminal argument chapter, nine-source four-role packet plus one bounded local implementation-pressure record, 2 targets/11 theorems, 6 arms/13 failures/15 competence gates unopened, 26 transaction mutations plus 10 integration mutations, 61-chapter reconciliation, A3 active, no compliance/support/release effect.")

if __name__ == "__main__": main()
