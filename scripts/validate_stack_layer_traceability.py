#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

from validate_protocol_examples import validate_value


ROOT = Path(__file__).resolve().parents[1]
CHAPTER_ID = "asi-is-a-stack-not-a-model"
CLAIM_ID = f"{CHAPTER_ID}.core"
FIXTURE = ROOT / "tests" / "fixtures" / "protocol_records" / "layer_boundary_record.valid.json"
SCHEMA = ROOT / "schemas" / "layer_boundary_record.schema.json"
BOOK_STRUCTURE = ROOT / "book_structure.json"
CLAIM_MATRIX = ROOT / "appendices" / "C_claim_evidence_matrix.qmd"
SOURCE_MATRIX = ROOT / "appendices" / "A_source_matrix.qmd"
OUTLINE = ROOT / "docs" / "book_outline.md"
CHAPTER = ROOT / "chapters" / "asi-is-a-stack-not-a-model.qmd"

REQUIRED_LOCAL_SOURCE_IDS = {"viea", "beastbrain", "aletheia", "talos", "moecot", "scf"}
EXPECTED_IMPLEMENTED_TESTS = {
    "Layer-boundary audit",
    "Source-to-layer traceability review",
    "Claim-support label audit",
}
REQUIRED_LAYER_RECORD_LISTS = {
    "chapter_refs",
    "input_artifacts",
    "output_artifacts",
    "contract_refs",
    "owned_invariants",
    "failure_modes",
    "evidence_gates",
    "downstream_interfaces",
    "promotion_blockers",
    "source_refs",
    "non_claims",
}
ALLOWED_SUPPORT_STATES = {
    "unsupported",
    "argument",
    "source-derived",
    "prototype-backed",
    "synthetic-test-backed",
    "empirical-test-backed",
    "external-literature-backed",
    "deprecated",
    "refuted",
}
ALLOWED_CLAIM_LABELS = {
    "Demonstrated",
    "Measured",
    "Mechanized",
    "Hypothesized",
    "Design rationale",
    "Speculative",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def flatten_chapters(structure: dict[str, Any]) -> list[dict[str, Any]]:
    chapters: list[dict[str, Any]] = []
    for part in structure.get("parts", []):
        if isinstance(part, dict):
            chapters.extend(ch for ch in part.get("chapters", []) if isinstance(ch, dict))
    return chapters


def require_text_boundary(items: list[Any], errors: list[str], relative: str) -> None:
    text = " ".join(str(item).lower() for item in items)
    if "does not" not in text:
        errors.append(f"{relative}: non_claims must include explicit 'does not' boundaries.")
    if "promote" in text:
        return
    if "support state" in text or "support-state" in text:
        return
    if "prove" not in text and "measure" not in text:
        errors.append(f"{relative}: non_claims must block proof/measurement/support-state overclaiming.")


def validate_layer_boundary_fixture(structure: dict[str, Any], errors: list[str]) -> None:
    fixture = load_json(FIXTURE)
    schema = load_json(SCHEMA)
    errors.extend(validate_value(fixture, schema, str(FIXTURE.relative_to(ROOT))))

    chapter_ids = {str(ch.get("id")) for ch in flatten_chapters(structure)}
    for field in REQUIRED_LAYER_RECORD_LISTS:
        value = fixture.get(field)
        if not isinstance(value, list) or not value:
            errors.append(f"{FIXTURE.relative_to(ROOT)}: {field} must be a non-empty list.")

    unknown_chapters = sorted(set(map(str, fixture.get("chapter_refs", []))) - chapter_ids)
    if unknown_chapters:
        errors.append(f"{FIXTURE.relative_to(ROOT)}: unknown chapter_refs {unknown_chapters}.")

    for source_ref in fixture.get("source_refs", []):
        path = ROOT / str(source_ref)
        if not path.exists():
            errors.append(f"{FIXTURE.relative_to(ROOT)}: source_ref {source_ref!r} does not exist.")

    for contract_ref in fixture.get("contract_refs", []):
        path = ROOT / str(contract_ref)
        if not path.exists():
            errors.append(f"{FIXTURE.relative_to(ROOT)}: contract_ref {contract_ref!r} does not exist.")

    if fixture.get("traceability_state") != "claim_mapped":
        errors.append(f"{FIXTURE.relative_to(ROOT)}: traceability_state must remain claim_mapped.")
    if fixture.get("support_state_effect") != "record_shape_only":
        errors.append(f"{FIXTURE.relative_to(ROOT)}: support_state_effect must remain record_shape_only.")
    non_claims = fixture.get("non_claims", [])
    if isinstance(non_claims, list):
        require_text_boundary(non_claims, errors, f"{FIXTURE.relative_to(ROOT)}:non_claims")


def validate_opener_manifest(structure: dict[str, Any], errors: list[str]) -> None:
    chapters = {str(ch.get("id")): ch for ch in flatten_chapters(structure)}
    chapter = chapters.get(CHAPTER_ID)
    if not chapter:
        errors.append(f"{BOOK_STRUCTURE.relative_to(ROOT)}: missing {CHAPTER_ID}.")
        return

    if chapter.get("claim_label") != "Design rationale":
        errors.append(f"{CHAPTER_ID}: claim_label must be Design rationale.")
    if chapter.get("evidence_level") != "argument":
        errors.append(f"{CHAPTER_ID}: evidence_level must remain argument.")

    source_ids = set(map(str, chapter.get("source_ids", [])))
    missing_local_sources = REQUIRED_LOCAL_SOURCE_IDS - source_ids
    unsupported_source_ids = {
        source_id
        for source_id in source_ids - REQUIRED_LOCAL_SOURCE_IDS
        if not source_id.startswith("ext_")
    }
    if missing_local_sources:
        errors.append(
            f"{CHAPTER_ID}: source_ids must retain local architecture sources "
            f"{sorted(REQUIRED_LOCAL_SOURCE_IDS)}; missing {sorted(missing_local_sources)}."
        )
    if unsupported_source_ids:
        errors.append(
            f"{CHAPTER_ID}: non-local positioning additions must use source-noted ext_ IDs; "
            f"got {sorted(unsupported_source_ids)}."
        )

    mappings = chapter.get("claim_source_mappings", [])
    mapped_sources = {str(mapping.get("source_id")) for mapping in mappings if isinstance(mapping, dict)}
    if mapped_sources != source_ids:
        errors.append(f"{CHAPTER_ID}: claim_source_mappings must cover every assigned source exactly.")

    for mapping in mappings:
        if not isinstance(mapping, dict):
            errors.append(f"{CHAPTER_ID}: claim_source_mappings entries must be objects.")
            continue
        source_id = str(mapping.get("source_id", ""))
        if mapping.get("passage_review_state") != "reviewed":
            errors.append(f"{CHAPTER_ID}: mapping {source_id} must have passage_review_state reviewed.")
        passage_refs = mapping.get("passage_refs")
        if not isinstance(passage_refs, list) or not passage_refs:
            errors.append(f"{CHAPTER_ID}: mapping {source_id} must have passage_refs.")
        for field in ("mapped_support", "limits", "passage_review_note"):
            value = mapping.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{CHAPTER_ID}: mapping {source_id} missing non-empty {field}.")
        limits = str(mapping.get("limits", "")).lower()
        if not any(term in limits for term in ("does not", "not ", "no ")):
            errors.append(f"{CHAPTER_ID}: mapping {source_id} limits must explicitly bound overclaiming.")

    implemented = set()
    for test in chapter.get("codex_tests", []):
        if isinstance(test, dict) and test.get("implementation_status") == "implemented":
            implemented.add(str(test.get("name")))
    missing_tests = sorted(EXPECTED_IMPLEMENTED_TESTS - implemented)
    if missing_tests:
        errors.append(f"{CHAPTER_ID}: codex_tests missing implemented audit rows {missing_tests}.")


def source_note_exists(source_id: str) -> bool:
    return (ROOT / "sources" / "source_notes" / f"{source_id}.md").exists()


def validate_source_to_layer_traceability(structure: dict[str, Any], errors: list[str]) -> None:
    source_matrix = SOURCE_MATRIX.read_text(encoding="utf-8", errors="ignore")
    chapter = next(ch for ch in flatten_chapters(structure) if ch.get("id") == CHAPTER_ID)
    for source_id in chapter.get("source_ids", []):
        source_id = str(source_id)
        if not source_note_exists(source_id):
            errors.append(f"{CHAPTER_ID}: missing source note for {source_id}.")
        source_rows = [line for line in source_matrix.splitlines() if line.startswith(f"| `{source_id}` ")]
        if len(source_rows) != 1:
            errors.append(f"{SOURCE_MATRIX.relative_to(ROOT)}: expected one row for source {source_id}.")
        elif CHAPTER_ID not in source_rows[0]:
            errors.append(f"{SOURCE_MATRIX.relative_to(ROOT)}: source {source_id} row is not visibly mapped to {CHAPTER_ID}.")

    for comparator_id in (
        "ext_mrkl_systems_2022",
        "ext_llm_agents_survey_2023",
        "ext_standard_model_mind_2017",
        "ext_subsumption_architecture_1986",
    ):
        if f"`{comparator_id}`" not in source_matrix:
            errors.append(f"{SOURCE_MATRIX.relative_to(ROOT)}: missing external comparator {comparator_id}.")
        if comparator_id not in CHAPTER.read_text(encoding="utf-8", errors="ignore"):
            errors.append(f"{CHAPTER.relative_to(ROOT)}: missing external comparator mention {comparator_id}.")


def split_markdown_row(row: str) -> list[str]:
    return [part.strip() for part in row.strip().strip("|").split("|")]


def validate_claim_support_labels(structure: dict[str, Any], errors: list[str]) -> None:
    matrix_text = CLAIM_MATRIX.read_text(encoding="utf-8", errors="ignore")
    rows = [line for line in matrix_text.splitlines() if line.startswith("| `") and ".core`" in line]
    expected_chapter_count = len(flatten_chapters(structure))
    if len(rows) != expected_chapter_count:
        errors.append(
            f"{CLAIM_MATRIX.relative_to(ROOT)}: expected {expected_chapter_count} core claim rows, found {len(rows)}."
        )

    opener_rows = [row for row in rows if f"`{CLAIM_ID}`" in row]
    if len(opener_rows) != 1:
        errors.append(f"{CLAIM_MATRIX.relative_to(ROOT)}: expected one row for {CLAIM_ID}.")
        return

    fields = split_markdown_row(opener_rows[0])
    if len(fields) < 11:
        errors.append(f"{CLAIM_MATRIX.relative_to(ROOT)}: row for {CLAIM_ID} has too few fields.")
        return
    if fields[3] != "Design rationale":
        errors.append(f"{CLAIM_ID}: Appendix C claim label must be Design rationale.")
    if fields[4] != "argument":
        errors.append(f"{CLAIM_ID}: Appendix C support state must remain argument.")
    for source_id in sorted(REQUIRED_LOCAL_SOURCE_IDS):
        if f"`{source_id}`" not in opener_rows[0]:
            errors.append(f"{CLAIM_ID}: Appendix C row missing assigned source {source_id}.")
    if "support remains" not in opener_rows[0].lower():
        errors.append(f"{CLAIM_ID}: Appendix C row must preserve support-state boundary wording.")

    for row in rows:
        fields = split_markdown_row(row)
        if len(fields) < 5:
            errors.append(f"{CLAIM_MATRIX.relative_to(ROOT)}: malformed core claim row {row[:80]!r}.")
            continue
        if fields[3] not in ALLOWED_CLAIM_LABELS:
            errors.append(f"{fields[0]}: invalid claim label {fields[3]!r}.")
        if fields[4] not in ALLOWED_SUPPORT_STATES:
            errors.append(f"{fields[0]}: invalid support state {fields[4]!r}.")


def validate_text_surfaces(errors: list[str]) -> None:
    chapter_text = CHAPTER.read_text(encoding="utf-8", errors="ignore")
    outline_text = OUTLINE.read_text(encoding="utf-8", errors="ignore")
    required_chapter_markers = [
        "Layer Boundary Record",
        "Stack Map",
        "No support-state promotion is implied",
        "[asi-is-a-stack-not-a-model.core, label: Design rationale, support: argument]",
        "source-to-layer traceability",
        "claim-support",
    ]
    for marker in required_chapter_markers:
        if marker not in chapter_text:
            errors.append(f"{CHAPTER.relative_to(ROOT)}: missing marker {marker!r}.")
    required_outline_markers = [
        "Exact Appendix C claim-source mappings",
        "python3 scripts/validate_stack_layer_traceability.py",
        "source-to-layer visibility",
        "claim/support labels",
    ]
    for marker in required_outline_markers:
        if marker not in outline_text:
            errors.append(f"{OUTLINE.relative_to(ROOT)}: missing marker {marker!r}.")


def main() -> None:
    structure = load_json(BOOK_STRUCTURE)
    if not isinstance(structure, dict):
        raise SystemExit("book_structure.json must contain an object.")

    errors: list[str] = []
    validate_layer_boundary_fixture(structure, errors)
    validate_opener_manifest(structure, errors)
    validate_source_to_layer_traceability(structure, errors)
    validate_claim_support_labels(structure, errors)
    validate_text_surfaces(errors)

    if errors:
        print("Stack layer traceability validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    opener = next(chapter for chapter in flatten_chapters(structure) if chapter.get("id") == CHAPTER_ID)
    mapped_sources = len(opener.get("source_ids", []))
    claim_rows = len(
        [
            line
            for line in CLAIM_MATRIX.read_text(encoding="utf-8", errors="ignore").splitlines()
            if line.startswith("| `") and ".core`" in line
        ]
    )
    print(
        "Stack layer traceability validation passed: "
        f"1 layer-boundary fixture, {mapped_sources} mapped source(s), {claim_rows} claim row(s)."
    )


if __name__ == "__main__":
    main()
