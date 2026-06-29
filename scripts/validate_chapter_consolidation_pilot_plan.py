#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "docs" / "chapter_consolidation_pilot_plan.md"
STRUCTURE = ROOT / "book_structure.json"

PILOT_IDS = {
    "constitutional-alignment-substrate",
    "agency-dignity-and-corrigibility",
    "moral-uncertainty-and-value-conflict",
    "governance-rights-fork-exit-and-audit",
}
REQUIRED_SOURCE_IDS = {
    "alignment_field",
    "field_of_god",
    "ethica_mechanica",
    "eternal_code",
    "coherence_exchange",
    "spinoza",
    "field_of_god_ai_constitution",
    "uat",
    "ladon_manhattan",
}
REQUIRED_LEAN_TAGS = {
    "lean:alignment.constitution.operational_invariant",
    "lean:alignment.constitution.failure_blocks_promotion",
    "lean:corrigibility.agency.operational_invariant",
    "lean:corrigibility.agency.failure_blocks_promotion",
    "lean:values.conflict.operational_invariant",
    "lean:values.conflict.failure_blocks_promotion",
    "lean:governance.rights.operational_invariant",
    "lean:governance.rights.failure_blocks_promotion",
}
REQUIRED_FRAGMENTS = (
    "does not edit `book_structure.json`",
    "Constitutional Alignment, Agency, and Corrigibility",
    "Moral Uncertainty, Value Conflict, and Contestable Governance",
    "one chapter skeleton",
    "not two pasted skeletons",
    "Run `python3 scripts/chapter_adjacency_report.py",
    "Do not merge any Circle, coil, Theseus, execution-artifact, or recursive",
    "Do not target a fixed final chapter count.",
    "This plan does not merge chapters.",
    "This plan does not change `book_structure.json`.",
    "This plan does not change any support state.",
)


def fail(errors: list[str]) -> None:
    print("Chapter consolidation pilot-plan validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def load_structure() -> dict:
    value = json.loads(STRUCTURE.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit("book_structure.json must contain an object.")
    return value


def main() -> None:
    errors: list[str] = []
    text = PLAN.read_text(encoding="utf-8")
    structure = load_structure()
    manifest_ids = {
        str(chapter.get("id"))
        for part in structure.get("parts", [])
        for chapter in part.get("chapters", [])
    }

    missing_manifest = sorted(PILOT_IDS - manifest_ids)
    if missing_manifest:
        errors.append(f"Pilot source chapters are already missing from manifest: {missing_manifest}")
    for chapter_id in sorted(PILOT_IDS):
        if f"`{chapter_id}`" not in text:
            errors.append(f"Plan does not reference pilot chapter `{chapter_id}`.")
    for source_id in sorted(REQUIRED_SOURCE_IDS):
        if f"`{source_id}`" not in text:
            errors.append(f"Plan does not preserve source ID `{source_id}`.")
    for tag in sorted(REQUIRED_LEAN_TAGS):
        if f"`{tag}`" not in text:
            errors.append(f"Plan does not preserve Lean tag `{tag}`.")
    for fragment in REQUIRED_FRAGMENTS:
        if fragment not in text:
            errors.append(f"Missing required fragment: {fragment}")
    if "support-state promotion" in text.lower() and "Do not promote any chapter core claim." not in text:
        errors.append("Plan mentions support-state promotion without the no-promotion boundary.")

    if errors:
        fail(errors)

    print("Chapter consolidation pilot-plan validation passed: four source chapters, two proposed merges.")


if __name__ == "__main__":
    main()
