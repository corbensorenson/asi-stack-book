#!/usr/bin/env python3
"""Validate P2 source/completeness closure and rejecting controls."""
from __future__ import annotations

import copy
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "evidence_quality/post_v2_3_source_and_completeness_residuals.json"
STATUS = ROOT / "roadmap_records/post_v2_3_handoff_reader_formats_and_evidence_renewal_status.json"
ALLOWED = {"insert", "narrow", "already_covered", "watch", "defer", "reject"}
ACCEPTED = {"ext_faithfulness_information_flow_2026", "ext_monitorbench_2026", "ext_v_jepa_2_2025", "ext_embedded_agency_2019"}


def load(path: Path):
    return json.loads(path.read_text())


def semantic_errors(data: dict, *, inspect_files: bool = True) -> list[str]:
    errors = []
    ten = data.get("ten_chapter_audit", [])
    tier = data.get("tier_2_disposition_audit", [])
    if len(ten) != 10 or len({r.get("chapter_id") for r in ten}) != 10:
        errors.append("ten-chapter audit must contain ten unique rows")
    if [r.get("id") for r in tier] != [f"T2-{n:02d}" for n in range(1, 38)]:
        errors.append("Tier-2 audit must contain the exact 37 ordered rows")
    for row in ten + tier:
        if row.get("disposition") not in ALLOWED:
            errors.append("unknown terminal disposition")
    if data.get("ownership_test", {}).get("new_chapter_warranted") is not False or data.get("active_chapter_count") != 54:
        errors.append("ownership test or 54-chapter breadth freeze drifted")
    if data.get("status") != "completed" or data.get("support_state_effect") != "none" or data.get("release_effect") != "none":
        errors.append("audit status or no-effect boundary drifted")
    accepted_decisions = {r.get("source_id") for r in data.get("source_decisions", []) if r.get("decision") == "insert"}
    if accepted_decisions != ACCEPTED:
        errors.append("accepted source set drifted or citation padding entered")
    if inspect_files:
        inventory = {r["id"] for r in load(ROOT / "sources/source_inventory.json")}
        structure = load(ROOT / "book_structure.json")
        chapters = {c["id"]: c for p in structure["parts"] for c in p["chapters"]}
        for sid in ACCEPTED:
            if sid not in inventory:
                errors.append(f"accepted source missing inventory record: {sid}")
            if not (ROOT / f"sources/source_notes/{sid}.md").is_file():
                errors.append(f"accepted source missing source note: {sid}")
            if sid not in (ROOT / "appendices/H_external_sources.qmd").read_text():
                errors.append(f"accepted source missing Appendix H: {sid}")
        for row in ten:
            cid = row["chapter_id"]
            chapter = chapters.get(cid, {})
            text = (ROOT / chapter.get("file", "missing")).read_text() if chapter else ""
            reader = ROOT / f"editions/reader_manuscript/v2_1/chapters/{cid}.qmd"
            for sid in row.get("accepted_source_ids", []):
                mapping = next((m for m in chapter.get("claim_source_mappings", []) if m.get("source_id") == sid), None)
                if not mapping or mapping.get("passage_review_state") != "reviewed" or not mapping.get("passage_refs"):
                    errors.append(f"accepted source lacks passage-reviewed mapping: {cid}:{sid}")
                if sid not in text:
                    errors.append(f"accepted source lacks live prose use: {cid}:{sid}")
                if not reader.is_file() or sid not in reader.read_text():
                    errors.append(f"accepted source lacks successor reader prose: {cid}:{sid}")
        reader_manifest = ROOT / "editions/reader_manuscript/v2_1/manifest.json"
        if not reader_manifest.is_file():
            errors.append("v2.1 successor reader manifest missing")
        else:
            rm = load(reader_manifest)
            if rm.get("chapter_count") != 54 or rm.get("status") != "reconciled_source_only" or rm.get("predecessor", {}).get("edition_id") != "asi-stack-curated-reader-v2.0":
                errors.append("v2.1 successor reader identity/status drifted")
        status = load(STATUS)
        p2 = next(r for r in status["priorities"] if r["id"] == "P2")
        m6 = next(r for r in status["milestones"] if r["id"] == "M6")
        if p2.get("state") != "completed" or m6.get("state") != "completed":
            errors.append("P2/M6 machine status is not completed")
        if len(inventory) != data.get("source_count"):
            errors.append("audit source count is stale")
    return errors


def main() -> None:
    data = load(AUDIT)
    errors = semantic_errors(data)
    mutants = []
    x = copy.deepcopy(data); x["ten_chapter_audit"].pop(); mutants.append(("missing ten-chapter row", x))
    x = copy.deepcopy(data); x["tier_2_disposition_audit"].pop(); mutants.append(("missing Tier-2 row", x))
    x = copy.deepcopy(data); x["source_decisions"][0]["decision"] = "watch"; mutants.append(("accepted source erased", x))
    x = copy.deepcopy(data); x["source_decisions"].append({"source_id": "ext_padding", "decision": "insert"}); mutants.append(("citation padding", x))
    x = copy.deepcopy(data); x["ownership_test"]["new_chapter_warranted"] = True; mutants.append(("unearned new chapter", x))
    x = copy.deepcopy(data); x["active_chapter_count"] = 55; mutants.append(("breadth drift", x))
    x = copy.deepcopy(data); x["status"] = "pending"; mutants.append(("nonterminal audit", x))
    x = copy.deepcopy(data); x["support_state_effect"] = "promote"; mutants.append(("support laundering", x))
    x = copy.deepcopy(data); x["tier_2_disposition_audit"][0]["disposition"] = "accepted_by_count"; mutants.append(("invalid disposition", x))
    rejected = 0
    for name, mutant in mutants:
        if semantic_errors(mutant, inspect_files=False):
            rejected += 1
        else:
            errors.append(f"negative control escaped: {name}")
    if errors:
        raise SystemExit("P2 source audit validation failed:\n- " + "\n- ".join(errors))
    print(f"P2 source audit validation passed: 10 chapter rows, 37 Tier-2 rows, 4 accepted sources, {rejected}/9 rejecting controls.")


if __name__ == "__main__":
    main()
