#!/usr/bin/env python3
"""Validate terminal P6.4-A1 source, proof, protocol, and reader integration."""

from __future__ import annotations

import copy
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTER_ID = "governed-model-training-distributed-optimization-and-scaling"
AUDIT = ROOT / "evidence_quality/p6_4_a1_governed_model_training_reader_integration.json"
SOURCE_IDS = {
    "ext_llama3_herd_2024", "ext_megatron_distributed_training_2021",
    "ext_zero_optimizer_2019", "ext_gspmd_2021", "ext_datastates_llm_2024",
    "ext_pytorch_distributed_checkpoint_2026", "ext_mlperf_training_v6_2026",
}
LOCAL_SOURCE_IDS = {"corbens_trainer_project"}
NEXT_PACKET = "P6.4-A2-privacy-data-rights-and-information-flow-governance-adjudication"


def load(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def errors(data: dict) -> list[str]:
    out: list[str] = []
    audit = data["audit"]
    if audit.get("decision") != "admit_at_argument_support" or audit.get("candidate_id") != CHAPTER_ID:
        out.append("A1 decision or candidate identity drifted")
    roles = audit.get("source_roles", {})
    if set(roles) != {"mechanism_or_capability", "limitation_or_failure", "competing_design", "measurement_or_evaluation"}:
        out.append("four-role source vocabulary drifted")
    if set(source for values in roles.values() for source in values) != SOURCE_IDS:
        out.append("four-role source packet incomplete")

    chapters = [chapter for part in data["structure"]["parts"] for chapter in part["chapters"]]
    ids = [chapter["id"] for chapter in chapters]
    if len(ids) != 60 or ids.count(CHAPTER_ID) != 1:
        out.append("60-chapter manifest or A1 uniqueness drifted")
    a1_index = ids.index(CHAPTER_ID) if CHAPTER_ID in ids else -1
    if a1_index < 1 or ids[a1_index - 1] != "replaceable-cognitive-substrates-beyond-transformer-monoculture" or ids[a1_index + 1] != "readiness-gates-residual-escrow-and-quarantine":
        out.append("A1 Part III placement drifted")
    chapter = next((row for row in chapters if row["id"] == CHAPTER_ID), {})
    if set(chapter.get("source_ids", [])) != SOURCE_IDS | LOCAL_SOURCE_IDS or chapter.get("evidence_level") != "argument" or chapter.get("claim_label") != "Design rationale":
        out.append("A1 manifest source or support boundary drifted")

    inventory = {row["id"]: row for row in data["sources"]}
    for source_id in SOURCE_IDS:
        if source_id not in inventory or CHAPTER_ID not in inventory[source_id].get("chapter_targets", []):
            out.append(f"source inventory target missing: {source_id}")
        note = ROOT / f"sources/source_notes/{source_id}.md"
        if not note.is_file() or any(section not in note.read_text(encoding="utf-8") for section in ("## Thesis", "## Mechanisms", "## Evidence", "## Failure Modes", "## Book Chapters Supported", "## Claims To Add Or Update", "## Open Questions")):
            out.append(f"source note incomplete: {source_id}")
    for source_id in LOCAL_SOURCE_IDS:
        if source_id not in inventory or CHAPTER_ID not in inventory[source_id].get("chapter_targets", []):
            out.append(f"local implementation source target missing: {source_id}")
        if source_id not in audit.get("local_implementation_references", []):
            out.append(f"local implementation source audit missing: {source_id}")

    proofs = [row for row in data["proofs"]["records"] if row["chapter_id"] == CHAPTER_ID]
    if len(proofs) != 2 or any(row.get("status") != "implemented" or row.get("module") != "AsiStackProofs.GovernedModelTraining" for row in proofs):
        out.append("A1 proof-target packet drifted")
    theorem_count = len(re.findall(r"^theorem\s+", (ROOT / "lean/AsiStackProofs/GovernedModelTraining.lean").read_text(), re.MULTILINE))
    if theorem_count != 13 or audit.get("formalization", {}).get("theorem_declaration_count") != 13:
        out.append("A1 theorem denominator drifted")

    protocol = data["protocol"]
    if protocol.get("state") != "prospectively_frozen_unexecuted" or len(protocol.get("arms", [])) != 5 or len(protocol.get("faults", [])) != 13 or len(protocol.get("competence_gates", [])) != 12:
        out.append("A1 empirical competence or denominator drifted")
    if audit.get("claim_bearing_empirical_lane", {}).get("protected_outcomes_opened") is not False:
        out.append("A1 protected outcome custody drifted")

    status = data["status"]
    tranche = status["quality_uplift_program"]["structural_completeness_tranche"]
    second = tranche["second_tranche"]
    if tranche.get("current_manifest_chapter_count") != 60 or second.get("manifest_admitted_count") != 1:
        out.append("A1 status chapter/admission denominator drifted")
    if second.get("adjudicated_candidate_ids") != [CHAPTER_ID] or second.get("terminal_candidate_dispositions", {}).get(CHAPTER_ID) != "admitted_terminal_argument_reader_chapter":
        out.append("A1 terminal status drifted")
    if second.get("active_candidate_id") != "privacy-data-rights-and-information-flow-governance" or status["execution_readiness"].get("immediate_book_packet") != NEXT_PACKET:
        out.append("A1 did not advance exactly to A2")

    surfaces = data["surfaces"]
    fragments = {
        "index": ["Governed training-run transaction", "all 60 working-manifest chapters", "Load-bearing reference | 31"],
        "replaceable": ["Governed Model Training, Distributed Optimization, and Scaling takes the next"],
        "integrated": ["Training candidates are transactions, not artifacts"],
        "glossary": ["Training Run Transaction", "Resume equivalence class"],
        "roadmap": ["P6.4-A2-privacy-data-rights-and-information-flow-governance-adjudication", "Terminal — admitted at argument support"],
    }
    for name, required in fragments.items():
        for fragment in required:
            if fragment not in surfaces[name]:
                out.append(f"{name} reader surface missing: {fragment}")

    artifact_hashes = audit.get("artifact_sha256", {})
    for relative in audit.get("artifacts", {}).values():
        path = ROOT / relative
        if not path.is_file() or artifact_hashes.get(relative) != sha(path):
            out.append(f"A1 artifact digest drifted: {relative}")
    for source_id in SOURCE_IDS:
        relative = f"sources/source_notes/{source_id}.md"
        if audit.get("source_note_sha256", {}).get(source_id) != sha(ROOT / relative):
            out.append(f"A1 source-note digest drifted: {source_id}")

    if any(audit.get(key) != "none" for key in ("support_state_effect", "release_effect", "publication_effect")):
        out.append("A1 claims unauthorized support, release, or publication effect")
    return out


def main() -> None:
    data = {
        "audit": load(AUDIT), "structure": load(ROOT / "book_structure.json"),
        "sources": load(ROOT / "sources/source_inventory.json"),
        "proofs": load(ROOT / "proofs/proof_manifest.json"),
        "protocol": load(ROOT / "experiments/governed_model_training_argument_exit/preregistration.json"),
        "status": load(ROOT / "roadmap_records/post_v2_3_maintenance_transfer_and_publication_status.json"),
        "surfaces": {
            "index": (ROOT / "index.qmd").read_text(),
            "replaceable": (ROOT / "chapters/replaceable-cognitive-substrates-beyond-transformer-monoculture.qmd").read_text(),
            "integrated": (ROOT / "chapters/integrated-reference-architecture.qmd").read_text(),
            "glossary": (ROOT / "appendices/B_glossary.qmd").read_text(),
            "roadmap": (ROOT / "docs/post_v2_3_maintenance_transfer_and_publication_roadmap.md").read_text(),
        },
    }
    failures = errors(data)
    mutations = [
        ("decision reversal", lambda v: v["audit"].__setitem__("decision", "reject")),
        ("source-role deletion", lambda v: v["audit"]["source_roles"]["competing_design"].pop()),
        ("manifest deletion", lambda v: next(part for part in v["structure"]["parts"] if any(c["id"] == CHAPTER_ID for c in part["chapters"]))["chapters"].pop(next(i for i,c in enumerate(next(part for part in v["structure"]["parts"] if any(x["id"] == CHAPTER_ID for x in part["chapters"]))["chapters"]) if c["id"] == CHAPTER_ID))),
        ("proof deimplementation", lambda v: next(row for row in v["proofs"]["records"] if row["chapter_id"] == CHAPTER_ID).__setitem__("status", "planned")),
        ("campaign execution invention", lambda v: v["protocol"].__setitem__("state", "complete")),
        ("competence gate deletion", lambda v: v["protocol"]["competence_gates"].pop()),
        ("terminal disposition deletion", lambda v: v["status"]["quality_uplift_program"]["structural_completeness_tranche"]["second_tranche"]["terminal_candidate_dispositions"].clear()),
        ("A2 rollback", lambda v: v["status"]["execution_readiness"].__setitem__("immediate_book_packet", "P6.4-A1-governed-model-training-distributed-optimization-and-scaling-adjudication")),
        ("support laundering", lambda v: v["audit"].__setitem__("support_state_effect", "promotion")),
    ]
    baseline = set(errors(data))
    for label, mutate in mutations:
        candidate = copy.deepcopy(data)
        mutate(candidate)
        if not set(errors(candidate)) - baseline:
            failures.append(f"negative mutation accepted: {label}")
    if failures:
        raise SystemExit("P6.4-A1 reader integration failed:\n- " + "\n- ".join(failures))

    transaction = subprocess.run(["python3", "scripts/validate_training_run_transaction.py"], cwd=ROOT, capture_output=True, text=True)
    if transaction.returncode:
        raise SystemExit(transaction.stdout + transaction.stderr)
    print("P6.4-A1 reader integration passed: terminal argument chapter, seven-source four-role packet, 2 targets/13 theorems, 5 arms/13 faults/12 competence gates unopened, 21 transaction mutations plus 9 integration mutations, 60-chapter reader reconciliation, A2 active, no support/release effect.")


if __name__ == "__main__":
    main()
