#!/usr/bin/env python3
"""Validate the P7.2-T1D six-chapter manuscript-maturity packet."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import build_p7_2_t1d_six_chapter_maturity as builder


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "evidence_quality/p7_2_t1d_six_chapter_maturity.json"
REPORT = ROOT / "docs/p7_2_t1d_six_chapter_maturity_and_source_role_review_2026_07_26.md"
BOOK = ROOT / "book_structure.json"
INVENTORY = ROOT / "sources/source_inventory.json"
CLAIMS = ROOT / "appendices/C_claim_evidence_matrix.qmd"
EXTERNAL = ROOT / "appendices/H_external_sources.qmd"
OUTLINE = ROOT / "docs/book_outline.md"

EXPECTED_CHAPTERS = [row["id"] for row in builder.CHAPTERS]
EXPECTED_CONDITIONS = set(builder.CONDITIONS)
EXPECTED_ROLES = {
    "mechanism_or_capability",
    "limitation_or_failure",
    "competing_design_or_simpler_baseline",
    "measurement_or_evaluation",
}
EXPECTED_WHITE_BOX = set(builder.WHITE_BOX_REQUIRED)


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def flatten(book: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {chapter["id"]: chapter for part in book["parts"] for chapter in part["chapters"]}


def errors(record: dict[str, Any]) -> list[str]:
    out: list[str] = []
    book = flatten(load(BOOK))
    inventory = {row["id"]: row for row in load(INVENTORY)}
    round_18 = load(ROOT / "evidence_quality/round_18_breadth_completion_claim_atoms.json")
    r16 = load(ROOT / "evidence_quality/post_activation_six_chapter_claim_atom_addendum.json")
    canonical_packet_atoms = {
        row["stable_claim_identity"] for row in round_18["atoms"]
    } | {
        atom_id for row in r16["chapter_reviews"] for atom_id in row["atom_ids"]
    }
    report = REPORT.read_text(encoding="utf-8") if REPORT.is_file() else ""
    claims = CLAIMS.read_text(encoding="utf-8")
    external = EXTERNAL.read_text(encoding="utf-8")
    outline = OUTLINE.read_text(encoding="utf-8")

    if record.get("state") != "terminal_manuscript_maturity_no_support_movement":
        out.append("packet state is not terminal manuscript maturity")
    if record.get("word_count_is_acceptance_gate") is not False:
        out.append("word count was laundered into an acceptance gate")
    rows = record.get("chapter_records", [])
    ids = [row.get("chapter_id") for row in rows]
    if ids != EXPECTED_CHAPTERS:
        out.append("six-chapter identity or order drifted")
    if len(ids) != len(set(ids)):
        out.append("duplicate chapter identity")
    for row in rows:
        chapter_id = row.get("chapter_id")
        if chapter_id not in book:
            out.append(f"manifest chapter missing: {chapter_id}")
            continue
        path = ROOT / row.get("chapter_path", "")
        text = path.read_text(encoding="utf-8") if path.is_file() else ""
        if not path.is_file() or row.get("chapter_sha256") != sha256(path):
            out.append(f"chapter digest drifted: {chapter_id}")
        conditions = row.get("maturity_conditions", {})
        if set(conditions) != EXPECTED_CONDITIONS:
            out.append(f"maturity condition set drifted: {chapter_id}")
        for condition, disposition in conditions.items():
            if disposition.get("status") != "passed_for_manuscript_maturity":
                out.append(f"maturity condition not passed: {chapter_id}/{condition}")
            locations = disposition.get("chapter_locations", [])
            if not locations or any(location not in text for location in locations):
                out.append(f"missing exact chapter location: {chapter_id}/{condition}")
        roles = row.get("source_roles", {})
        if set(roles) != EXPECTED_ROLES:
            out.append(f"source-role set drifted: {chapter_id}")
        for role, source_ids in roles.items():
            if not source_ids:
                out.append(f"empty source role: {chapter_id}/{role}")
            for source_id in source_ids:
                if source_id not in book[chapter_id].get("source_ids", []):
                    out.append(f"source-role laundering: {chapter_id}/{source_id}")
                note = ROOT / "sources/source_notes" / f"{source_id}.md"
                if source_id not in inventory or not note.is_file():
                    out.append(f"source record or note missing: {chapter_id}/{source_id}")
        expected_note_paths = {
            f"sources/source_notes/{source_id}.md"
            for source_ids in roles.values()
            for source_id in source_ids
        }
        if set(row.get("source_note_paths", [])) != expected_note_paths:
            out.append(f"source-note path set drifted: {chapter_id}")
        for note_path in row.get("source_note_paths", []):
            if not (ROOT / note_path).is_file():
                out.append(f"recorded source note missing: {chapter_id}/{note_path}")
        atoms = row.get("claim_atom_ids", [])
        if not atoms or any(atom not in canonical_packet_atoms for atom in atoms):
            out.append(f"claim-atom projection drifted: {chapter_id}")
        if atoms[0] not in claims:
            out.append(f"chapter-core claim projection drifted: {chapter_id}")
        reader = row.get("reader_projection", {})
        if any(key not in reader for key in ("human_path", "summary", "handoff", "source_crosswalk", "claim_matrix_atom_ids", "outline_surface")):
            out.append(f"reader projection incomplete: {chapter_id}")
        if chapter_id not in outline:
            out.append(f"outline projection missing: {chapter_id}")
        specificity = row.get("chapter_specificity_evidence", [])
        if len(specificity) != 2 or any(item.get("owner") != chapter_id or item.get("corpus_owner_count") != 1 for item in specificity):
            out.append(f"chapter-specific inheritance evidence drifted: {chapter_id}")
        if len(row.get("residuals", [])) < 2:
            out.append(f"residual envelope erased: {chapter_id}")
        if row.get("maximum_next_inference") != "competent_implementation_and_fair_test_design_only":
            out.append(f"maximum inference widened: {chapter_id}")
        if row.get("support_state_effect") != "none":
            out.append(f"chapter support movement invented: {chapter_id}")
        if chapter_id not in report:
            out.append(f"review report omits chapter: {chapter_id}")

    repairs = record.get("accepted_existing_owner_repairs", [])
    if len(repairs) != 4:
        out.append("existing-owner repair denominator drifted")
    for repair in repairs:
        path = ROOT / repair.get("path", "")
        if not path.is_file() or repair.get("anchor") not in path.read_text(encoding="utf-8"):
            out.append(f"existing-owner repair anchor missing: {repair.get('topic')}")
        if repair.get("state") != "meaning_bearing_prose_present" or repair.get("support_state_effect") != "none":
            out.append(f"existing-owner repair disposition drifted: {repair.get('topic')}")

    source_packet = record.get("white_box_source_packet", [])
    if {row.get("source_id") for row in source_packet} != EXPECTED_WHITE_BOX:
        out.append("White-Box source packet identity drifted")
    for row in source_packet:
        source_id = row.get("source_id")
        note = ROOT / row.get("source_note_path", "")
        if source_id not in inventory or not note.is_file() or row.get("source_note_sha256") != sha256(note):
            out.append(f"White-Box source receipt drifted: {source_id}")
        if source_id not in external:
            out.append(f"White-Box external appendix projection missing: {source_id}")
        if row.get("local_reproduction") != "none" or row.get("authority") != "external_comparator_only":
            out.append(f"White-Box source authority laundered: {source_id}")

    inheritance = record.get("chapter_specific_inheritance_audit", {})
    if inheritance.get("chapter_count") != 6 or inheritance.get("anchor_count") != 12 or inheritance.get("collisions") != 0:
        out.append("chapter-specific inheritance denominator drifted")
    atom = record.get("atom_reconciliation", {})
    if atom.get("chapter_count") != 6 or atom.get("atom_count") != 10 or atom.get("new_material_atoms") != 0:
        out.append("atom reconciliation denominator drifted")
    reader = record.get("reader_reconciliation", {})
    if reader.get("all_six_have_human_path_summary_handoff_and_source_crosswalk") is not True:
        out.append("reader reconciliation claims incomplete coverage")
    if reader.get("current_reader_derivative_required_after_packet") is not True:
        out.append("current-reader successor obligation erased")
    if len(record.get("non_claims", [])) < 5:
        out.append("packet non-claim envelope erased")
    for field in ("support_state_effect", "release_effect", "publication_effect"):
        if record.get(field) != "none":
            out.append(f"unauthorized {field}")
    white_text = (ROOT / book["white-box-evidence-interpretability-and-activation-governance"]["file"]).read_text(encoding="utf-8")
    for phrase in ("### Comparative method matrix", "### Evidence ladder and stop rules", "The white-box ladder is deliberately noninheritant."):
        if phrase not in white_text:
            out.append(f"White-Box meaning-bearing prose missing: {phrase}")
    return out


def main() -> None:
    record = load(ARTIFACT)
    failures = errors(record)
    if record != builder.build():
        failures.append("tracked packet is not the deterministic current build")
    mutations = [
        ("chapter deletion", lambda value: value["chapter_records"].pop()),
        ("duplicate chapter", lambda value: value["chapter_records"].__setitem__(1, copy.deepcopy(value["chapter_records"][0]))),
        ("condition failure", lambda value: value["chapter_records"][0]["maturity_conditions"]["field_decomposition"].__setitem__("status", "failed")),
        ("location deletion", lambda value: value["chapter_records"][0]["maturity_conditions"]["field_decomposition"].__setitem__("chapter_locations", [])),
        ("source role deletion", lambda value: value["chapter_records"][0]["source_roles"].pop("measurement_or_evaluation")),
        ("source role laundering", lambda value: value["chapter_records"][0]["source_roles"]["mechanism_or_capability"].append("ext_not_assigned")),
        ("source note path deletion", lambda value: value["chapter_records"][0].__setitem__("source_note_paths", [])),
        ("chapter digest rewrite", lambda value: value["chapter_records"][0].__setitem__("chapter_sha256", "0" * 64)),
        ("support promotion", lambda value: value["chapter_records"][0].__setitem__("support_state_effect", "empirical-test-backed")),
        ("maximum inference widening", lambda value: value["chapter_records"][0].__setitem__("maximum_next_inference", "mechanism_refuted")),
        ("residual erasure", lambda value: value["chapter_records"][0].__setitem__("residuals", [])),
        ("specificity collision", lambda value: value["chapter_records"][0]["chapter_specificity_evidence"][0].__setitem__("corpus_owner_count", 2)),
        ("repair deletion", lambda value: value["accepted_existing_owner_repairs"].pop()),
        ("White-Box source deletion", lambda value: value["white_box_source_packet"].pop()),
        ("atom count drift", lambda value: value["atom_reconciliation"].__setitem__("atom_count", 30)),
        ("reader obligation erasure", lambda value: value["reader_reconciliation"].__setitem__("current_reader_derivative_required_after_packet", False)),
        ("nonclaim erasure", lambda value: value.__setitem__("non_claims", [])),
        ("release invention", lambda value: value.__setitem__("release_effect", "published")),
    ]
    baseline = set(errors(record))
    for label, mutation in mutations:
        candidate = copy.deepcopy(record)
        mutation(candidate)
        if not set(errors(candidate)) - baseline:
            failures.append(f"negative mutation accepted: {label}")
    if failures:
        raise SystemExit("P7.2-T1D maturity validation failed:\n - " + "\n - ".join(failures))
    print(
        "P7.2-T1D maturity validation passed: 6 chapters, 36 maturity decisions, "
        "12 chapter-specific anchors, 4 existing-owner repairs, 5 White-Box source receipts, "
        "10 reconciled atom identities, 18 mutations rejected; support effect none."
    )


if __name__ == "__main__":
    main()
