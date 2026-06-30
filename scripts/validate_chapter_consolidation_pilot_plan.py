#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "docs" / "chapter_consolidation_pilot_plan.md"
DRY_RUN_ALIGNMENT = ROOT / "docs" / "chapter_consolidation_dry_run_constitutional_alignment.md"
DRY_RUN_CONTESTABLE = ROOT / "docs" / "chapter_consolidation_dry_run_contestable_governance.md"
DESTINATION_DRAFT_ALIGNMENT = ROOT / "docs" / "chapter_consolidation_destination_draft_constitutional_alignment.md"
DESTINATION_DRAFT_CONTESTABLE = ROOT / "docs" / "chapter_consolidation_destination_draft_contestable_governance.md"
URL_HISTORY_POLICY = ROOT / "docs" / "chapter_consolidation_url_history_policy.md"
EXTERNAL_REVIEW_PACKET = ROOT / "docs" / "chapter_consolidation_external_review_packet.md"
DECISION_REVIEW = ROOT / "docs" / "chapter_consolidation_decision_review.md"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
STRUCTURE = ROOT / "book_structure.json"

PILOT_IDS = {
    "constitutional-alignment-substrate",
    "agency-dignity-and-corrigibility",
    "moral-uncertainty-and-value-conflict",
    "governance-rights-fork-exit-and-audit",
}
PILOT_DESTINATION_IDS = {
    "constitutional-alignment-substrate",
    "moral-uncertainty-and-value-conflict",
}
PILOT_RETIRED_IDS = {
    "agency-dignity-and-corrigibility",
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
ALIGNMENT_DRY_RUN_REQUIRED_SOURCE_IDS = {
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
ALIGNMENT_DRY_RUN_REQUIRED_LEAN_TAGS = {
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
    "URL, redirect, retired-file, and chapter-history treatment",
    "validation commands and expected generated-file updates",
    "Run `python3 scripts/chapter_adjacency_report.py",
    "Do not merge any Circle, coil, Theseus, execution-artifact, or recursive",
    "Do not target a fixed final chapter count.",
    "This plan does not merge chapters.",
    "This plan does not change `book_structure.json`.",
    "This plan does not change any support state.",
)
ALIGNMENT_DRY_RUN_REQUIRED_FRAGMENTS = (
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
ALIGNMENT_DESTINATION_DRAFT_REQUIRED_FRAGMENTS = (
    "Status: review-ready draft; human/external review not completed.",
    "does not edit `book_structure.json`",
    "Constitutional Alignment: Agency, Dignity, and Corrigibility",
    "one chapter skeleton",
    "No manifest edit has been made.",
    "No chapter core claim is promoted above `argument`.",
    "Constitutional Predicate Record",
    "Agency Rights Checklist",
    "Review Checklist Before Any Manifest Merge",
    "This draft is ready for human or external review. It is not yet reviewed.",
    "Manifest consolidation remains blocked",
)
CONTESTABLE_DESTINATION_DRAFT_REQUIRED_FRAGMENTS = (
    "Status: review-ready draft; human/external review not completed.",
    "does not edit `book_structure.json`",
    "Moral Uncertainty, Value Conflict, and Contestable Governance",
    "one chapter skeleton",
    "No manifest edit has been made.",
    "No chapter core claim is promoted above `argument`.",
    "Value Conflict Record",
    "Governance Right Record",
    "Review Checklist Before Any Manifest Merge",
    "This draft is ready for human or external review. It is not yet reviewed.",
    "Manifest consolidation remains blocked",
)
CONTESTABLE_DRY_RUN_REQUIRED_FRAGMENTS = (
    "This is the second dry-run merge package",
    "does not edit `book_structure.json`",
    "Moral Uncertainty, Value Conflict, and Contestable Governance",
    "governance-rights-fork-exit-and-audit",
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
CONTESTABLE_DRY_RUN_REQUIRED_SOURCE_IDS = {
    "ethica_mechanica",
    "alignment_field",
    "coherence_exchange",
    "uat",
    "spinoza",
    "field_of_god_ai_constitution",
    "ladon_manhattan",
    "ext_reinforcement_learning_moral_uncertainty_2020",
    "ext_contestable_ai_design_2022",
    "ext_collective_constitutional_ai_2024",
    "ext_corrigibility_2015",
    "ext_off_switch_game_2016",
}
CONTESTABLE_DRY_RUN_REQUIRED_LEAN_TAGS = {
    "lean:values.conflict.operational_invariant",
    "lean:values.conflict.failure_blocks_promotion",
    "lean:governance.rights.operational_invariant",
    "lean:governance.rights.failure_blocks_promotion",
}
DECISION_REVIEW_REQUIRED_FRAGMENTS = (
    "Decision: defer manifest consolidation until review and public URL/history",
    "docs/chapter_consolidation_url_history_policy.md",
    "no retired URL redirect or historical stub has been implemented",
    "does not edit `book_structure.json`",
    "does not authorize a",
    "merge, and does not approve a reader artifact.",
    "docs/chapter_consolidation_external_review_packet.md",
    "Constitutional Alignment: Agency, Dignity, and Corrigibility",
    "Moral Uncertainty, Value Conflict, and Contestable Governance",
    "docs/chapter_consolidation_dry_run_constitutional_alignment.md",
    "docs/chapter_consolidation_dry_run_contestable_governance.md",
    "external review",
    "Human-reader curation may proceed",
    "No support state changes.",
    "No chapter core claim is promoted.",
)
URL_HISTORY_POLICY_REQUIRED_FRAGMENTS = (
    "Chapter Consolidation URL and History Policy",
    "active policy for future consolidation execution",
    "applied to the 2026-06-30 Part I pilot through static historical stubs",
    "Default URL Policy",
    "Preserve every retired source chapter's public URL",
    "Pilot Defaults",
    "/chapters/agency-dignity-and-corrigibility.html",
    "/chapters/governance-rights-fork-exit-and-audit.html",
    "The 2026-06-30 Part I execution package, not this policy text alone, implemented two historical stubs and changed the manifest to 52 chapters.",
)
EXTERNAL_REVIEW_PACKET_REQUIRED_FRAGMENTS = (
    "Chapter Consolidation External Review Packet",
    "https://github.com/corbensorenson/asi-stack-book/issues/1",
    "Review Boundary",
    "This packet does not edit `book_structure.json`",
    "Reviewer comments are review input, not source evidence",
    "docs/chapter_consolidation_pilot_plan.md",
    "docs/chapter_consolidation_url_history_policy.md",
    "docs/chapter_consolidation_destination_draft_constitutional_alignment.md",
    "docs/chapter_consolidation_destination_draft_contestable_governance.md",
    "Constitutional Alignment decision",
    "Contestable Governance decision",
    "execute, revise, defer, or reject each proposed merge",
    "This packet does not mean an external review has happened.",
    "This packet does not authorize either merge.",
    "This packet does not change `book_structure.json`.",
)
ROADMAP_REQUIRED_FRAGMENTS = (
    "Decision from the 2026-06-29 consolidation review",
    "The right response is re-consolidation into chapter-owning artifacts",
    "roughly 44 deeper chapters",
    "closer to 47 chapters",
    "`mathematical-and-search-substrates`",
    "`project-theseus-as-report-first-implementation-reference`",
    "`semantic-representation-and-tree-structured-models`",
    "`runtime-adapters-tool-permissions-and-human-approval`",
    "The merged chapter should be deeper than either input chapter",
    "Governed consolidation review",
    "walk the governed consolidation decision queue before broad human-reader curation",
    "chapter_consolidation_decision_review.md",
    "chapter_consolidation_url_history_policy.md",
    "chapter_consolidation_external_review_packet.md",
)


def read_required_file(path: Path, errors: list[str]) -> str:
    if not path.exists():
        errors.append(f"Missing dry-run merge package: {path.relative_to(ROOT)}")
        return ""
    return path.read_text(encoding="utf-8")


def require_fragments(label: str, text: str, fragments: tuple[str, ...], errors: list[str]) -> None:
    for fragment in fragments:
        if fragment not in text:
            errors.append(f"{label} missing required fragment: {fragment}")


def require_backticked_ids(label: str, text: str, ids: set[str], errors: list[str]) -> None:
    for item_id in sorted(ids):
        if f"`{item_id}`" not in text:
            errors.append(f"{label} does not preserve `{item_id}`.")


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
    roadmap_text = ROADMAP.read_text(encoding="utf-8")
    alignment_dry_run_text = read_required_file(DRY_RUN_ALIGNMENT, errors)
    contestable_dry_run_text = read_required_file(DRY_RUN_CONTESTABLE, errors)
    alignment_destination_draft_text = read_required_file(DESTINATION_DRAFT_ALIGNMENT, errors)
    contestable_destination_draft_text = read_required_file(DESTINATION_DRAFT_CONTESTABLE, errors)
    url_history_policy_text = read_required_file(URL_HISTORY_POLICY, errors)
    external_review_packet_text = read_required_file(EXTERNAL_REVIEW_PACKET, errors)
    decision_review_text = read_required_file(DECISION_REVIEW, errors)
    structure = load_structure()
    manifest_ids = {
        str(chapter.get("id"))
        for part in structure.get("parts", [])
        for chapter in part.get("chapters", [])
    }

    missing_destinations = sorted(PILOT_DESTINATION_IDS - manifest_ids)
    if missing_destinations:
        errors.append(f"Pilot destination chapters are missing from manifest: {missing_destinations}")
    still_rendered_retired = sorted(PILOT_RETIRED_IDS & manifest_ids)
    if still_rendered_retired:
        errors.append(f"Pilot retired source chapters still appear in manifest: {still_rendered_retired}")
    for chapter_id in sorted(PILOT_IDS):
        if f"`{chapter_id}`" not in text:
            errors.append(f"Plan does not reference pilot chapter `{chapter_id}`.")
    for source_id in sorted(REQUIRED_SOURCE_IDS):
        if f"`{source_id}`" not in text:
            errors.append(f"Plan does not preserve source ID `{source_id}`.")
    for tag in sorted(REQUIRED_LEAN_TAGS):
        if f"`{tag}`" not in text:
            errors.append(f"Plan does not preserve Lean tag `{tag}`.")
    require_fragments("Plan", text, REQUIRED_FRAGMENTS, errors)
    require_fragments("Roadmap", roadmap_text, ROADMAP_REQUIRED_FRAGMENTS, errors)
    require_fragments("URL/history policy", url_history_policy_text, URL_HISTORY_POLICY_REQUIRED_FRAGMENTS, errors)
    require_fragments(
        "Constitutional-alignment dry-run package",
        alignment_dry_run_text,
        ALIGNMENT_DRY_RUN_REQUIRED_FRAGMENTS,
        errors,
    )
    require_backticked_ids(
        "Constitutional-alignment dry-run package",
        alignment_dry_run_text,
        ALIGNMENT_DRY_RUN_REQUIRED_SOURCE_IDS,
        errors,
    )
    require_backticked_ids(
        "Constitutional-alignment dry-run package",
        alignment_dry_run_text,
        ALIGNMENT_DRY_RUN_REQUIRED_LEAN_TAGS,
        errors,
    )
    require_fragments(
        "Constitutional-alignment destination draft",
        alignment_destination_draft_text,
        ALIGNMENT_DESTINATION_DRAFT_REQUIRED_FRAGMENTS,
        errors,
    )
    require_backticked_ids(
        "Constitutional-alignment destination draft",
        alignment_destination_draft_text,
        ALIGNMENT_DRY_RUN_REQUIRED_SOURCE_IDS,
        errors,
    )
    require_backticked_ids(
        "Constitutional-alignment destination draft",
        alignment_destination_draft_text,
        ALIGNMENT_DRY_RUN_REQUIRED_LEAN_TAGS,
        errors,
    )
    require_fragments(
        "Contestable-governance dry-run package",
        contestable_dry_run_text,
        CONTESTABLE_DRY_RUN_REQUIRED_FRAGMENTS,
        errors,
    )
    require_backticked_ids(
        "Contestable-governance dry-run package",
        contestable_dry_run_text,
        CONTESTABLE_DRY_RUN_REQUIRED_SOURCE_IDS,
        errors,
    )
    require_backticked_ids(
        "Contestable-governance dry-run package",
        contestable_dry_run_text,
        CONTESTABLE_DRY_RUN_REQUIRED_LEAN_TAGS,
        errors,
    )
    require_fragments(
        "Contestable-governance destination draft",
        contestable_destination_draft_text,
        CONTESTABLE_DESTINATION_DRAFT_REQUIRED_FRAGMENTS,
        errors,
    )
    require_backticked_ids(
        "Contestable-governance destination draft",
        contestable_destination_draft_text,
        CONTESTABLE_DRY_RUN_REQUIRED_SOURCE_IDS,
        errors,
    )
    require_backticked_ids(
        "Contestable-governance destination draft",
        contestable_destination_draft_text,
        CONTESTABLE_DRY_RUN_REQUIRED_LEAN_TAGS,
        errors,
    )
    require_fragments(
        "Consolidation external-review packet",
        external_review_packet_text,
        EXTERNAL_REVIEW_PACKET_REQUIRED_FRAGMENTS,
        errors,
    )
    require_backticked_ids(
        "Consolidation external-review packet",
        external_review_packet_text,
        PILOT_IDS,
        errors,
    )
    require_fragments(
        "Consolidation decision review",
        decision_review_text,
        DECISION_REVIEW_REQUIRED_FRAGMENTS,
        errors,
    )
    if "support-state promotion" in text.lower() and "Do not promote any chapter core claim." not in text:
        errors.append("Plan mentions support-state promotion without the no-promotion boundary.")

    if errors:
        fail(errors)

    print(
        "Chapter consolidation pilot-plan validation passed: executed Part I pilot, "
        "two archived source chapters, two destination chapters, two dry-run packages, "
        "two destination drafts, and one external-review packet."
    )


if __name__ == "__main__":
    main()
