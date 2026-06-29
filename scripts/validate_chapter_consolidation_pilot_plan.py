#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "docs" / "chapter_consolidation_pilot_plan.md"
DRY_RUN = ROOT / "docs" / "chapter_consolidation_dry_run_constitutional_alignment.md"
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
    "ext_constitutional_ai_2022",
    "ext_collective_constitutional_ai_2024",
    "ext_reinforcement_learning_moral_uncertainty_2020",
    "ext_contestable_ai_design_2022",
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
DRY_RUN_REQUIRED_SOURCE_IDS = {
    "alignment_field",
    "field_of_god",
    "ethica_mechanica",
    "eternal_code",
    "coherence_exchange",
    "spinoza",
    "field_of_god_ai_constitution",
    "ext_constitutional_ai_2022",
    "ext_collective_constitutional_ai_2024",
    "ext_corrigibility_2015",
    "ext_off_switch_game_2016",
}
DRY_RUN_REQUIRED_LEAN_TAGS = {
    "lean:alignment.constitution.operational_invariant",
    "lean:alignment.constitution.failure_blocks_promotion",
    "lean:corrigibility.agency.operational_invariant",
    "lean:corrigibility.agency.failure_blocks_promotion",
}
REQUIRED_FRAGMENTS = (
    "does not edit `book_structure.json`",
    "Constitutional Alignment: Agency, Dignity, and Corrigibility",
    "Moral Uncertainty, Value Conflict, and Contestable Governance",
    "one chapter skeleton",
    "not two pasted skeletons",
    "Produce a dry-run merge package before editing `book_structure.json`.",
    "Dry-Run Merge Package",
    "proposed `book_structure.json` diff for only one destination chapter",
    "Appendix C row plan",
    "URL, redirect, and retired-file policy",
    "validation commands and expected generated-file updates",
    "Run `python3 scripts/chapter_adjacency_report.py",
    "Do not merge any Circle, coil, Theseus, execution-artifact, or recursive",
    "Do not target a fixed final chapter count.",
    "This plan does not merge chapters.",
    "This plan does not change `book_structure.json`.",
    "This plan does not change any support state.",
)
DRY_RUN_REQUIRED_FRAGMENTS = (
    "This is the first dry-run merge package",
    "does not edit `book_structure.json`",
    "Constitutional Alignment: Agency, Dignity, and Corrigibility",
    "agency-dignity-and-corrigibility",
    "Proposed `book_structure.json` Diff",
    "This proposed `book_structure.json` diff is illustrative and unapplied.",
    "Destination Section Outline",
    "one chapter skeleton, not two pasted skeletons",
    "Appendix C Row Plan",
    "No-support-state-change language",
    "Source Union",
    "External-source union",
    "Lean Module And Proof-Manifest Treatment",
    "Keep both Lean modules",
    "Test, Schema, And Harness Rows To Move",
    "Reader Path, Handoff, And Review Repairs",
    "MVI And Beyond-SOTA Merge",
    "URL, Redirect, And Retired-File Policy",
    "Expected Generated-File Updates If Applied",
    "Validation Commands Before Any Real Merge Commit",
    "No new result is created by this dry run.",
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
    if not DRY_RUN.exists():
        errors.append(f"Missing dry-run merge package: {DRY_RUN.relative_to(ROOT)}")
        dry_run_text = ""
    else:
        dry_run_text = DRY_RUN.read_text(encoding="utf-8")
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
    for fragment in DRY_RUN_REQUIRED_FRAGMENTS:
        if fragment not in dry_run_text:
            errors.append(f"Dry-run package missing required fragment: {fragment}")
    for source_id in sorted(DRY_RUN_REQUIRED_SOURCE_IDS):
        if f"`{source_id}`" not in dry_run_text:
            errors.append(f"Dry-run package does not preserve source ID `{source_id}`.")
    for tag in sorted(DRY_RUN_REQUIRED_LEAN_TAGS):
        if f"`{tag}`" not in dry_run_text:
            errors.append(f"Dry-run package does not preserve Lean tag `{tag}`.")
    if "support-state promotion" in text.lower() and "Do not promote any chapter core claim." not in text:
        errors.append("Plan mentions support-state promotion without the no-promotion boundary.")

    if errors:
        fail(errors)

    print("Chapter consolidation pilot-plan validation passed: four source chapters, two proposed merges.")


if __name__ == "__main__":
    main()
