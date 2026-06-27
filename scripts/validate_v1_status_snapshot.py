#!/usr/bin/env python3
"""Validate headline counts in docs/v1_0_candidate_status.md.

The v1.0 status page is a public-safe readiness surface. This script checks
that its snapshot counts still match the current repository artifacts; it does
not assert that the book is a v1.0 evidence release.
"""

from __future__ import annotations

from collections import Counter
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "docs" / "v1_0_candidate_status.md"
FRONT_MATTER_RE = re.compile(r"\A---\n.*?\n---\n?", re.DOTALL)
WORD_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9'_-]*")
HUMAN_BLOCK_RE = re.compile(r"::: \{\.asi-human-only\}\n## Human Reading Path\n\n(.*?)\n:::", re.DOTALL)
TEMPLATE_BRIDGE_PHRASES = (
    "The useful",
    "The practical",
    "The point is",
    "useful only when",
    "The mature test",
    "The mature version is",
)


def fail(errors: list[str]) -> None:
    print("v1.0 status snapshot validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def flatten_chapters(structure: dict) -> list[dict]:
    return [chapter for part in structure.get("parts", []) for chapter in part.get("chapters", [])]


def chapter_word_counts() -> tuple[int, int, int]:
    chapter_files = sorted((ROOT / "chapters").glob("*.qmd"))
    body_words = 0
    raw_words = 0
    for path in chapter_files:
        text = path.read_text(encoding="utf-8")
        raw_words += len(WORD_RE.findall(text))
        body_words += len(WORD_RE.findall(FRONT_MATTER_RE.sub("", text, count=1)))
    return len(chapter_files), body_words, raw_words


def summary_metric(path: Path, metric: str) -> str | None:
    text = path.read_text(encoding="utf-8", errors="ignore")
    match = re.search(rf"^\|\s*{re.escape(metric)}\s*\|\s*(.*?)\s*\|$", text, re.MULTILINE)
    return match.group(1).strip() if match else None


def human_bridge_metrics(chapters: list[dict]) -> tuple[int, int, int, int]:
    values: list[int] = []
    opening_values: list[int] = []
    closing_values: list[int] = []
    template_phrase_hits = 0
    for chapter in chapters:
        path = ROOT / str(chapter.get("file", ""))
        text = path.read_text(encoding="utf-8", errors="ignore")
        match = HUMAN_BLOCK_RE.search(text)
        if not match:
            continue
        bridge_text = re.sub(r"\s+", " ", match.group(1).strip())
        normalized_bridge = bridge_text.lower()
        template_phrase_hits += sum(normalized_bridge.count(phrase.lower()) for phrase in TEMPLATE_BRIDGE_PHRASES)
        values.append(len(WORD_RE.findall(bridge_text)))
        sentences = [sentence.strip() for sentence in re.split(r"(?<=[.!?])\s+", bridge_text) if sentence.strip()]
        if sentences:
            opening_values.append(len(WORD_RE.findall(sentences[0])))
            closing_values.append(len(WORD_RE.findall(sentences[-1])))
    return (
        min(values) if values else 0,
        min(opening_values) if opening_values else 0,
        min(closing_values) if closing_values else 0,
        template_phrase_hits,
    )


def main() -> None:
    errors: list[str] = []
    status_text = STATUS.read_text(encoding="utf-8")
    structure = load_json(ROOT / "book_structure.json")
    if not isinstance(structure, dict):
        fail(["book_structure.json must contain an object."])
    chapters = flatten_chapters(structure)
    appendices = structure.get("appendices", [])
    front_matter = structure.get("front_matter", [])
    book_page_count = len(front_matter) + len(chapters) + len(appendices)
    source_records = load_json(ROOT / "sources" / "source_inventory.json")
    proof_manifest = load_json(ROOT / "proofs" / "proof_manifest.json")
    if not isinstance(source_records, list):
        fail(["sources/source_inventory.json must contain a list."])
    if not isinstance(proof_manifest, dict):
        fail(["proofs/proof_manifest.json must contain an object."])

    chapter_file_count, body_words, raw_words = chapter_word_counts()
    source_note_ids = {
        path.stem
        for path in (ROOT / "sources" / "source_notes").glob("*.md")
        if path.name not in {"README.md", "_template.md"}
    }
    source_ids = {str(record.get("id", "")) for record in source_records}
    missing_notes = sorted(source_ids - source_note_ids)
    evidence_counts = Counter(str(chapter.get("evidence_level", "")) for chapter in chapters)
    schema_count = len(list((ROOT / "schemas").glob("*.schema.json")))
    fixture_count = len(list((ROOT / "tests" / "fixtures" / "protocol_records").glob("*.json")))
    release_count = len(list((ROOT / "release_records").glob("*.json")))
    (
        human_min_words,
        human_min_opening_words,
        human_min_closing_words,
        human_template_phrase_hits,
    ) = human_bridge_metrics(chapters)

    assigned_pairs = summary_metric(ROOT / "docs" / "source_evidence_audit.md", "Assigned source/chapter pairs")
    exact_mappings = summary_metric(ROOT / "docs" / "source_evidence_audit.md", "Exact claim-source mappings")
    passage_reviewed = summary_metric(ROOT / "docs" / "source_evidence_audit.md", "Passage-reviewed mappings recorded")
    proof_targets = str(proof_manifest.get("proof_target_count", ""))

    expected_fragments = [
        f"| Book structure | {len(structure.get('parts', []))} parts, {len(chapters)} manifest-driven chapters, {len(appendices)} appendices |",
        f"| Manuscript scale | {chapter_file_count} chapter files; {body_words:,} chapter words excluding YAML front matter; {raw_words:,} raw chapter-file words including metadata and live scaffolding |",
        f"| Source inventory | {len(source_records)} public-safe source records, each with a matching public source note;",
        "| Source appendix ownership | Appendix G (`Corben's Sources and Local Projects`) and Appendix H (`External Sources by Other Authors`) are independent top-level appendices: G contains Corben's source corpus and local-project records; H contains external records by other authors marked `external_literature` |",
        f"| Claim/source traceability | {assigned_pairs} assigned source/chapter pairs, {exact_mappings} exact claim-source mappings, {passage_reviewed} passage-reviewed mappings |",
        f"| Support states | {evidence_counts.get('argument', 0)} chapter core claims at `argument`; no support-state promotion in the v1.0 improvement pass |",
        f"| Proof envelope | {proof_targets} proof targets, all implemented as narrow finite-record Lean predicates |",
        f"| Schemas and fixtures | {schema_count} JSON Schemas, {fixture_count} valid protocol fixtures, {release_count} public release record |",
        f"| Implementation horizons | {len(chapters)} generated chapter build horizons with manifest-sourced minimum viable implementation and beyond-state-of-the-art endpoint fields |",
        "browser Human-view gate checks rendered Mermaid SVG visibility",
        "`Failure closure:`",
        "`detect and route failure modes such as`",
        "`This is a target architecture, not a current-result claim`",
        "`It remains beyond the chapter's present support state`",
        "`The public schema now records`",
        "`None of those passages show`",
        "`The evidence map is narrower now`",
        "`The Lean coverage stays at`",
        f"All {book_page_count} rendered book pages carry the persistent and shareable `AI view` / `Human view` switch",
        "browser smoke validation can exercise every manifest chapter across desktop and mobile viewports with `--all-chapters --all-viewports`, including reading-mode control visibility and horizontal-overflow checks, when Playwright/Chrome is available",
        f"must be at least 165 words excluding the source-only heading, must open with at least 8 words, must close with at least 7 words, must avoid known repeated bridge formulas, with the current bridge minimum at {human_min_words} words, opening-sentence minimum at {human_min_opening_words} words, closing-sentence minimum at {human_min_closing_words} words, and targeted template-phrase count at {human_template_phrase_hits}",
    ]

    if len(chapters) != chapter_file_count:
        errors.append(f"Manifest has {len(chapters)} chapters but chapters/ has {chapter_file_count} .qmd files.")
    if missing_notes:
        errors.append(f"Source inventory records missing source notes: {missing_notes}")
    if assigned_pairs is None or exact_mappings is None or passage_reviewed is None:
        errors.append("docs/source_evidence_audit.md is missing required summary metrics.")
    if not proof_targets:
        errors.append("proofs/proof_manifest.json is missing proof_target_count.")
    if human_min_words < 165:
        errors.append(f"Human Reading Path prose minimum is {human_min_words}, below 165.")
    if human_min_opening_words < 8:
        errors.append(f"Human Reading Path opening-sentence minimum is {human_min_opening_words}, below 8.")
    if human_min_closing_words < 7:
        errors.append(f"Human Reading Path closing-sentence minimum is {human_min_closing_words}, below 7.")
    if human_template_phrase_hits != 0:
        errors.append(f"Human Reading Path targeted template-phrase count is {human_template_phrase_hits}, expected 0.")

    for fragment in expected_fragments:
        if fragment not in status_text:
            errors.append(f"docs/v1_0_candidate_status.md is missing current fragment: {fragment}")

    if errors:
        fail(errors)

    print(
        "v1.0 status snapshot validation passed: "
        f"{len(chapters)} chapters, {body_words:,} body words, "
        f"{len(source_records)} sources, {proof_targets} proof targets."
    )


if __name__ == "__main__":
    main()
