#!/usr/bin/env python3
"""Validate the contribution novelty ledger and public summary."""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "contribution_novelty_ledger.json"
SUMMARY = ROOT / "docs" / "contribution_novelty_ledger.md"
README = ROOT / "README.md"
INDEX = ROOT / "index.qmd"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"

EXPECTED_IDEAS = {
    "verification_bandwidth",
    "governed_cognition_pattern_language",
    "governance_economics",
    "residual_honesty",
    "support_state_ladder",
    "stable_capability_identity",
    "bounded_self_improvement",
    "human_oversight_degradation",
    "receipt_faithfulness_gap",
}
REQUIRED_FIELDS = {
    "idea_id",
    "signature_phrase",
    "chapter_refs",
    "claimed_contribution",
    "closest_prior_art_refs",
    "audited_delta",
    "non_obvious_consequence",
    "strongest_objection",
    "answer_status",
    "confidence_state",
    "needed_next_artifact",
    "support_state_effect",
    "non_claims",
}
REQUIRED_SUMMARY_FRAGMENTS = [
    "Contribution Novelty Ledger",
    "Rows: 9 signature ideas",
    "not proof of novelty",
    "Record-reality gap",
    "Human oversight degradation",
    "receipt_faithfulness_gap",
    "all 44 chapter core claims remain",
    "does not approve reader, release, ebook, PDF, DOCX, audio",
]
REQUIRED_PUBLIC_LINK = "docs/contribution_novelty_ledger.md"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Contribution novelty ledger validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def text_blob(*values: Any) -> str:
    parts: list[str] = []
    for value in values:
        if isinstance(value, str):
            parts.append(value)
        elif isinstance(value, list):
            parts.extend(str(item) for item in value)
    return " ".join(parts).lower()


def inventory_ids() -> set[str]:
    inventory = load_json(ROOT / "sources" / "source_inventory.json")
    if not isinstance(inventory, list):
        raise SystemExit("sources/source_inventory.json must contain a list.")
    return {str(record.get("id")) for record in inventory if isinstance(record, dict)}


def chapter_ids() -> set[str]:
    structure = load_json(ROOT / "book_structure.json")
    if not isinstance(structure, dict):
        raise SystemExit("book_structure.json must contain an object.")
    ids: set[str] = set()
    for part in structure.get("parts", []):
        if not isinstance(part, dict):
            continue
        for chapter in part.get("chapters", []):
            if isinstance(chapter, dict) and isinstance(chapter.get("id"), str):
                ids.add(chapter["id"])
    return ids


def validate_ledger(value: dict[str, Any], errors: list[str]) -> None:
    if value.get("schema_version") != "0.1":
        errors.append(f"{rel(LEDGER)}: schema_version must be 0.1.")
    if value.get("status") != "source_noted_positioning":
        errors.append(f"{rel(LEDGER)}: status must be source_noted_positioning.")
    purpose = value.get("purpose")
    purpose_lower = purpose.lower() if isinstance(purpose, str) else ""
    if (
        not isinstance(purpose, str)
        or ("not" not in purpose_lower and "without" not in purpose_lower)
        or "support-state" not in purpose_lower
    ):
        errors.append(f"{rel(LEDGER)}: purpose must state the no-support-state boundary.")
    records = value.get("records")
    if not isinstance(records, list):
        errors.append(f"{rel(LEDGER)}: records must be a list.")
        return
    if len(records) != len(EXPECTED_IDEAS):
        errors.append(f"{rel(LEDGER)}: expected {len(EXPECTED_IDEAS)} records, found {len(records)}.")

    source_ids = inventory_ids()
    chapters = chapter_ids()
    seen: set[str] = set()
    confidence_states: set[str] = set()
    for index, record in enumerate(records):
        owner = f"{rel(LEDGER)}:records[{index}]"
        if not isinstance(record, dict):
            errors.append(f"{owner}: record must be an object.")
            continue
        missing = sorted(REQUIRED_FIELDS - set(record))
        if missing:
            errors.append(f"{owner}: missing required fields {missing}.")
        idea_id = record.get("idea_id")
        if not isinstance(idea_id, str) or idea_id not in EXPECTED_IDEAS:
            errors.append(f"{owner}: idea_id must be one of {sorted(EXPECTED_IDEAS)}.")
        elif idea_id in seen:
            errors.append(f"{owner}: duplicate idea_id {idea_id}.")
        else:
            seen.add(idea_id)

        for field in ("signature_phrase", "answer_status", "confidence_state"):
            value_field = record.get(field)
            if not isinstance(value_field, str) or not value_field.strip():
                errors.append(f"{owner}: {field} must be a non-empty string.")

        for field in ("claimed_contribution", "audited_delta", "non_obvious_consequence", "strongest_objection", "needed_next_artifact"):
            value_field = record.get(field)
            if not isinstance(value_field, str) or len(value_field.split()) < 3:
                errors.append(f"{owner}: {field} must be a substantive string.")

        chapter_refs = record.get("chapter_refs")
        if not isinstance(chapter_refs, list) or not chapter_refs:
            errors.append(f"{owner}: chapter_refs must be a non-empty list.")
            chapter_refs = []
        for chapter_ref in chapter_refs:
            if chapter_ref not in chapters:
                errors.append(f"{owner}: chapter ref does not exist in book_structure.json: {chapter_ref}")

        prior_art_refs = record.get("closest_prior_art_refs")
        if not isinstance(prior_art_refs, list) or len(prior_art_refs) < 3:
            errors.append(f"{owner}: closest_prior_art_refs must list at least three source IDs.")
            prior_art_refs = []
        for source_id in prior_art_refs:
            if source_id not in source_ids:
                errors.append(f"{owner}: source id not found in source_inventory.json: {source_id}")
            note = ROOT / "sources" / "source_notes" / f"{source_id}.md"
            if not note.exists():
                errors.append(f"{owner}: source note missing for prior-art ref: {source_id}")

        if record.get("support_state_effect") != "none":
            errors.append(f"{owner}: support_state_effect must be none.")
        non_claims = record.get("non_claims")
        if not isinstance(non_claims, list) or len(non_claims) < 3:
            errors.append(f"{owner}: non_claims must list at least three boundaries.")
            non_claims = []
        blob = text_blob(non_claims, record.get("claimed_contribution"), record.get("audited_delta"))
        for phrase in ("does not promote", "does not prove"):
            if phrase not in blob:
                errors.append(f"{owner}: non_claims must include '{phrase}'.")
        confidence_states.add(str(record.get("confidence_state")))

    missing_ideas = sorted(EXPECTED_IDEAS - seen)
    if missing_ideas:
        errors.append(f"{rel(LEDGER)}: missing expected idea rows {missing_ideas}.")
    unresolved_markers = (
        "not_defended",
        "not_deployed",
        "not_empirical",
        "not_open_world",
        "not_novelty_proven",
    )
    if not any(any(marker in state for marker in unresolved_markers) for state in confidence_states):
        errors.append(f"{rel(LEDGER)}: at least one row must honestly preserve an unresolved confidence state.")
    top_non_claims = value.get("non_claims")
    if not isinstance(top_non_claims, list):
        errors.append(f"{rel(LEDGER)}: top-level non_claims must be a list.")
    else:
        top_blob = text_blob(top_non_claims)
        for phrase in ("not proof of novelty", "does not promote", "does not approve"):
            if phrase not in top_blob:
                errors.append(f"{rel(LEDGER)}: top-level non_claims missing {phrase!r}.")


def validate_surfaces(errors: list[str]) -> None:
    summary = SUMMARY.read_text(encoding="utf-8") if SUMMARY.exists() else ""
    if not summary:
        errors.append(f"Missing {rel(SUMMARY)}.")
    for fragment in REQUIRED_SUMMARY_FRAGMENTS:
        if fragment not in summary:
            errors.append(f"{rel(SUMMARY)} missing required fragment: {fragment}")

    for path in (README, INDEX, ROADMAP):
        text = path.read_text(encoding="utf-8")
        if REQUIRED_PUBLIC_LINK not in text:
            errors.append(f"{rel(path)} missing contribution novelty ledger link: {REQUIRED_PUBLIC_LINK}")
    roadmap_text = " ".join(ROADMAP.read_text(encoding="utf-8").split())
    if "Novelty claims without a ledger row do not belong in reader prose" not in roadmap_text:
        errors.append(f"{rel(ROADMAP)} missing ledger prose guardrail.")


def main() -> None:
    value = load_json(LEDGER)
    if not isinstance(value, dict):
        fail([f"{rel(LEDGER)} must contain an object."])
    errors: list[str] = []
    validate_ledger(value, errors)
    validate_surfaces(errors)
    if errors:
        fail(errors)
    print("Contribution novelty ledger validation passed: 9 signature ideas, source-noted comparators, no support-state effect.")


if __name__ == "__main__":
    main()
