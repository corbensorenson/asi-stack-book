#!/usr/bin/env python3
"""Validate the generated human-reader spine.

The live book may contain AI/research scaffolding, but the reader edition must
still work as a coherent manuscript after that scaffolding is stripped. This
validator derives the reader edition in a temporary workspace, checks that the
stripped sections are gone, and fails on obviously live-only terms inside
generated chapter prose.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import re
import tempfile
from pathlib import Path
import sys

import build_reader_edition

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT = ROOT / "build" / "reader_spine_report.json"

WORD_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9'_-]*")
CODE_BLOCK_RE = re.compile(r"```.*?```", re.DOTALL)
DEFAULT_MIN_WORDS = 300
DEFAULT_HARD_TERMS = [
    "drafting guardrail",
    "codex test plan",
    "codex workflow",
    "claim-source mapping status",
    "formalization hooks",
    "source crosswalk",
    "source-note",
]
DEFAULT_BLOCKED_META_PHRASES = [
    "this chapter",
    "the chapter",
]
DEFAULT_BLOCKED_PARAGRAPH_STARTS = [
    "Evidence boundary: architectural argument.",
]
DEFAULT_BLOCKED_LOWERCASE_SENTENCE_STARTS = [
    "automation workflow",
    "connector review",
    "connector-only review context",
    "source map",
    "source review",
]
GENERIC_HANDOFF_PHRASES = (
    "the next boundary",
    "the next move",
    "the next question",
    "the handoff is",
    "the handoff moves",
    "this is the handoff",
)
DEFAULT_REQUIRED_READER_HEADINGS = [
    "Problem",
    "Why existing approaches are insufficient",
    "Core Claim",
    "Mechanism",
    "Interfaces",
    "Invariants",
    "Failure modes",
    "Minimum Viable Implementation",
    "Beyond the State of the Art",
    "Summary",
    "Handoff",
]
DEFAULT_MIN_HANDOFF_WORDS = 45
DEFAULT_MIN_SECTION_WORD_COUNTS = {
    "Problem": 120,
    "Why existing approaches are insufficient": 110,
    "Core Claim": 40,
    "Mechanism": 300,
    "Interfaces": 120,
    "Invariants": 100,
    "Failure modes": 100,
    "Minimum Viable Implementation": 110,
    "Beyond the State of the Art": 180,
    "Summary": 110,
    "Handoff": 45,
}
DEFAULT_MIN_SECTION_PROSE_PARAGRAPH_COUNTS = {
    "Problem": 2,
    "Why existing approaches are insufficient": 2,
    "Core Claim": 1,
    "Mechanism": 4,
    "Interfaces": 1,
    "Invariants": 1,
    "Failure modes": 1,
    "Minimum Viable Implementation": 2,
    "Beyond the State of the Art": 3,
    "Summary": 2,
    "Handoff": 1,
}
PROSE_PARAGRAPH_MIN_WORDS = 18
HANDOFF_HEADING_RE = re.compile(r"^## Handoff\s*$", re.MULTILINE)
SUMMARY_HEADING_RE = re.compile(r"^## Summary\s*$", re.MULTILINE)
NEXT_HEADING_RE = re.compile(r"^##\s+", re.MULTILINE)
SECTION_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
NUMBERED_CHAPTER_RE = re.compile(r"\bchapter\s+\d+\b", re.IGNORECASE)


def load_structure() -> dict:
    value = json.loads((ROOT / "book_structure.json").read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError("book_structure.json must contain an object")
    return value


def flatten_chapters(structure: dict) -> list[dict[str, str]]:
    chapters: list[dict[str, str]] = []
    for part in structure.get("parts", []):
        if not isinstance(part, dict):
            continue
        for chapter in part.get("chapters", []):
            if (
                isinstance(chapter, dict)
                and isinstance(chapter.get("file"), str)
                and isinstance(chapter.get("title"), str)
            ):
                chapters.append({"file": chapter["file"], "title": chapter["title"]})
    return chapters


def load_validation_policy() -> dict:
    profiles = build_reader_edition.load_release_profiles()
    policy = profiles.get("reader_spine_validation", {})
    if not isinstance(policy, dict):
        return {}
    return policy


def count_reader_words(text: str) -> int:
    text = build_reader_edition.strip_frontmatter(text)
    text = CODE_BLOCK_RE.sub(" ", text)
    lines = [
        line
        for line in text.splitlines()
        if not line.lstrip().startswith("|") and not line.lstrip().startswith("!")
    ]
    return len(WORD_RE.findall("\n".join(lines)))


def count_section_words(text: str) -> int:
    text = CODE_BLOCK_RE.sub(" ", text)
    lines = [
        line
        for line in text.splitlines()
        if not line.lstrip().startswith("|") and not line.lstrip().startswith("!")
    ]
    return len(WORD_RE.findall("\n".join(lines)))


def prose_paragraph_count(text: str) -> int:
    text = CODE_BLOCK_RE.sub(" ", text)
    count = 0
    for block in re.split(r"\n\s*\n", text.strip()):
        paragraph = block.strip()
        if not paragraph:
            continue
        if paragraph.startswith(("|", "!", ":::", "- ", "* ", "#")):
            continue
        if re.match(r"^\d+\.\s", paragraph):
            continue
        if len(WORD_RE.findall(paragraph)) >= PROSE_PARAGRAPH_MIN_WORDS:
            count += 1
    return count


def reader_sections(text: str) -> dict[str, dict[str, str]]:
    stripped = build_reader_edition.strip_frontmatter(text)
    matches = list(SECTION_HEADING_RE.finditer(stripped))
    sections: dict[str, dict[str, str]] = {}
    for index, match in enumerate(matches):
        title = match.group(2).strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(stripped)
        sections.setdefault(
            normalize_heading(title),
            {
                "title": title,
                "body": stripped[start:end].strip(),
            },
        )
    return sections


def live_only_term_hits(text: str, terms: list[str]) -> list[dict[str, object]]:
    hits: list[dict[str, object]] = []
    lower_terms = [(term, term.lower()) for term in terms]
    for lineno, line in enumerate(text.splitlines(), start=1):
        lowered = line.lower()
        for original, lowered_term in lower_terms:
            if lowered_term in lowered:
                hits.append({"line": lineno, "term": original, "text": line.strip()})
    return hits


def meta_phrase_hits(text: str, phrases: list[str]) -> list[dict[str, object]]:
    hits: list[dict[str, object]] = []
    patterns = []
    for phrase in phrases:
        escaped = re.escape(phrase).replace(r"\ ", r"\s+")
        patterns.append((phrase, re.compile(rf"\b{escaped}\b", re.IGNORECASE)))
    for lineno, line in enumerate(text.splitlines(), start=1):
        for phrase, pattern in patterns:
            if pattern.search(line):
                hits.append({"line": lineno, "phrase": phrase, "text": line.strip()})
    return hits


def paragraph_start_hits(text: str, starts: list[str]) -> list[dict[str, object]]:
    hits: list[dict[str, object]] = []
    paragraphs = re.split(r"\n\s*\n", build_reader_edition.strip_frontmatter(text))
    line_cursor = 1
    for paragraph in paragraphs:
        stripped = paragraph.strip()
        start_line = line_cursor
        line_cursor += paragraph.count("\n") + 2
        if not stripped or stripped.startswith(("#", "|", "!", ":::", "- ", "* ")):
            continue
        normalized = re.sub(r"\s+", " ", stripped)
        for start in starts:
            if normalized.startswith(start):
                hits.append({"line": start_line, "phrase": start, "text": normalized[:180]})
    return hits


def lowercase_sentence_start_hits(text: str, starts: list[str]) -> list[dict[str, object]]:
    hits: list[dict[str, object]] = []
    patterns = [
        (
            phrase,
            re.compile(rf"(^|[.!?]\s+)({re.escape(phrase)})\b"),
        )
        for phrase in starts
    ]
    cleaned = CODE_BLOCK_RE.sub(" ", build_reader_edition.strip_frontmatter(text))
    for lineno, line in enumerate(cleaned.splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith(("#", "|", "!", ":::", "- ", "* ")):
            continue
        if re.match(r"^\d+\.\s", stripped):
            continue
        for phrase, pattern in patterns:
            match = pattern.search(stripped)
            if match:
                hits.append({"line": lineno, "phrase": phrase, "text": stripped[:180]})
    return hits


def normalize_heading(title: str) -> str:
    return re.sub(r"\s+", " ", title.strip()).lower()


def reader_headings(text: str) -> set[str]:
    headings: set[str] = set()
    for line in build_reader_edition.strip_frontmatter(text).splitlines():
        match = build_reader_edition.HEADING_RE.match(line)
        if match:
            headings.add(normalize_heading(match.group(2)))
    return headings


def first_heading(text: str) -> tuple[int, str] | None:
    for line in build_reader_edition.strip_frontmatter(text).splitlines():
        match = build_reader_edition.HEADING_RE.match(line)
        if match:
            return len(match.group(1)), match.group(2).strip()
    return None


def section_body_after(text: str, match: re.Match[str]) -> str:
    tail = text[match.end() :]
    next_heading = NEXT_HEADING_RE.search(tail)
    if next_heading:
        return tail[: next_heading.start()].strip()
    return tail.strip()


def validate_generated_reader(output_dir: Path) -> dict[str, object]:
    structure = load_structure()
    profile = build_reader_edition.find_profile("reader_release")
    policy = load_validation_policy()
    min_words = int(policy.get("minimum_chapter_word_count", DEFAULT_MIN_WORDS))
    hard_terms = policy.get("hard_blocked_terms", DEFAULT_HARD_TERMS)
    if not isinstance(hard_terms, list) or not all(isinstance(term, str) for term in hard_terms):
        raise TypeError("reader_spine_validation.hard_blocked_terms must be a list of strings")
    blocked_meta_phrases = policy.get("blocked_meta_phrases", DEFAULT_BLOCKED_META_PHRASES)
    if not isinstance(blocked_meta_phrases, list) or not all(isinstance(term, str) for term in blocked_meta_phrases):
        raise TypeError("reader_spine_validation.blocked_meta_phrases must be a list of strings")
    blocked_paragraph_starts = policy.get("blocked_paragraph_starts", DEFAULT_BLOCKED_PARAGRAPH_STARTS)
    if not isinstance(blocked_paragraph_starts, list) or not all(isinstance(term, str) for term in blocked_paragraph_starts):
        raise TypeError("reader_spine_validation.blocked_paragraph_starts must be a list of strings")
    blocked_lowercase_sentence_starts = policy.get(
        "blocked_lowercase_sentence_starts",
        DEFAULT_BLOCKED_LOWERCASE_SENTENCE_STARTS,
    )
    if (
        not isinstance(blocked_lowercase_sentence_starts, list)
        or not all(isinstance(term, str) for term in blocked_lowercase_sentence_starts)
    ):
        raise TypeError("reader_spine_validation.blocked_lowercase_sentence_starts must be a list of strings")
    required_headings = policy.get("required_reader_headings", DEFAULT_REQUIRED_READER_HEADINGS)
    if not isinstance(required_headings, list) or not all(isinstance(heading, str) for heading in required_headings):
        raise TypeError("reader_spine_validation.required_reader_headings must be a list of strings")
    normalized_required_headings = [normalize_heading(heading) for heading in required_headings]
    min_handoff_words = int(policy.get("minimum_handoff_word_count", DEFAULT_MIN_HANDOFF_WORDS))
    min_section_word_counts = policy.get("minimum_section_word_counts", DEFAULT_MIN_SECTION_WORD_COUNTS)
    if (
        not isinstance(min_section_word_counts, dict)
        or not all(isinstance(key, str) and isinstance(value, int) for key, value in min_section_word_counts.items())
    ):
        raise TypeError("reader_spine_validation.minimum_section_word_counts must be an object of integer floors")
    min_section_prose_paragraph_counts = policy.get(
        "minimum_section_prose_paragraph_counts",
        DEFAULT_MIN_SECTION_PROSE_PARAGRAPH_COUNTS,
    )
    if (
        not isinstance(min_section_prose_paragraph_counts, dict)
        or not all(
            isinstance(key, str) and isinstance(value, int)
            for key, value in min_section_prose_paragraph_counts.items()
        )
    ):
        raise TypeError(
            "reader_spine_validation.minimum_section_prose_paragraph_counts must be an object of integer floors"
        )

    strip_headings = build_reader_edition.profile_strip_headings(profile)
    heading_violations = build_reader_edition.scan_for_stripped_headings(output_dir, strip_headings)
    view_marker_violations = build_reader_edition.scan_for_view_block_markers(output_dir)

    chapter_records: list[dict[str, object]] = []
    errors: list[str] = []
    chapters = flatten_chapters(structure)
    for index, chapter in enumerate(chapters):
        relative = chapter["file"]
        expected_title = chapter["title"]
        next_chapter = chapters[index + 1] if index + 1 < len(chapters) else None
        path = output_dir / relative
        if not path.exists():
            errors.append(f"Generated reader chapter missing: {relative}")
            continue
        text = path.read_text(encoding="utf-8")
        words = count_reader_words(text)
        term_hits = live_only_term_hits(text, hard_terms)
        meta_hits = meta_phrase_hits(text, blocked_meta_phrases)
        paragraph_start_hit_records = paragraph_start_hits(text, blocked_paragraph_starts)
        lowercase_sentence_start_hit_records = lowercase_sentence_start_hits(text, blocked_lowercase_sentence_starts)
        headings = reader_headings(text)
        sections = reader_sections(text)
        section_word_counts: dict[str, int] = {}
        section_prose_paragraph_counts: dict[str, int] = {}
        section_word_violations: list[dict[str, object]] = []
        section_prose_paragraph_violations: list[dict[str, object]] = []
        for heading, minimum in min_section_word_counts.items():
            section = sections.get(normalize_heading(heading))
            section_words = count_section_words(section["body"]) if section else 0
            section_word_counts[heading] = section_words
            if section_words < minimum:
                section_word_violations.append(
                    {"heading": heading, "word_count": section_words, "minimum": minimum}
                )
        for heading, minimum in min_section_prose_paragraph_counts.items():
            section = sections.get(normalize_heading(heading))
            paragraph_count = prose_paragraph_count(section["body"]) if section else 0
            section_prose_paragraph_counts[heading] = paragraph_count
            if paragraph_count < minimum:
                section_prose_paragraph_violations.append(
                    {"heading": heading, "paragraph_count": paragraph_count, "minimum": minimum}
                )
        first = first_heading(text)
        title_ok = first == (1, expected_title)
        source_marker_heading_count = text.count("Human Reading Path")
        handoff_matches = list(HANDOFF_HEADING_RE.finditer(text))
        summary_match = SUMMARY_HEADING_RE.search(text)
        handoff_word_count = 0
        handoff_after_summary = False
        handoff_names_next = False
        handoff_closes_book = False
        handoff_numbered_chapter_ref = False
        handoff_generic_phrase_hits: list[str] = []
        if len(handoff_matches) == 1:
            handoff_after_summary = bool(summary_match and handoff_matches[0].start() > summary_match.start())
            handoff_body = section_body_after(text, handoff_matches[0])
            handoff_word_count = len(WORD_RE.findall(handoff_body))
            handoff_numbered_chapter_ref = bool(NUMBERED_CHAPTER_RE.search(handoff_body))
            lowered_handoff = handoff_body.lower()
            handoff_generic_phrase_hits = [
                phrase for phrase in GENERIC_HANDOFF_PHRASES if phrase in lowered_handoff
            ]
            if next_chapter is None:
                handoff_closes_book = "book" in lowered_handoff
            else:
                next_title = str(next_chapter.get("title", "")).strip()
                handoff_names_next = bool(next_title and next_title in handoff_body)
        missing_headings = [
            required_headings[index]
            for index, normalized in enumerate(normalized_required_headings)
            if normalized not in headings
        ]
        chapter_records.append(
            {
                "file": relative,
                "expected_title": expected_title,
                "first_heading": {"level": first[0], "title": first[1]} if first else None,
                "source_marker_heading_count": source_marker_heading_count,
                "handoff_section_count": len(handoff_matches),
                "handoff_after_summary": handoff_after_summary,
                "handoff_word_count": handoff_word_count,
                "handoff_names_next_chapter": handoff_names_next if next_chapter is not None else None,
                "handoff_closes_book": handoff_closes_book if next_chapter is None else None,
                "handoff_numbered_chapter_ref": handoff_numbered_chapter_ref,
                "handoff_generic_phrase_hits": handoff_generic_phrase_hits,
                "word_count_after_strip": words,
                "section_word_counts": section_word_counts,
                "section_prose_paragraph_counts": section_prose_paragraph_counts,
                "section_word_violations": section_word_violations,
                "section_prose_paragraph_violations": section_prose_paragraph_violations,
                "live_only_term_hits": term_hits,
                "meta_phrase_hits": meta_hits,
                "paragraph_start_hits": paragraph_start_hit_records,
                "lowercase_sentence_start_hits": lowercase_sentence_start_hit_records,
                "missing_reader_headings": missing_headings,
            }
        )
        if not title_ok:
            errors.append(
                f"{relative}: generated reader chapter must start with manifest title "
                f"{expected_title!r}; first heading is {first!r}."
            )
        if source_marker_heading_count:
            errors.append(
                f"{relative}: source-only Human Reading Path marker remains in reader edition."
            )
        if len(handoff_matches) != 1:
            errors.append(
                f"{relative}: reader spine must contain exactly one Handoff section; "
                f"found {len(handoff_matches)}."
            )
        else:
            if not handoff_after_summary:
                errors.append(f"{relative}: reader Handoff section must appear after Summary.")
            if handoff_word_count < min_handoff_words:
                errors.append(
                    f"{relative}: reader Handoff has {handoff_word_count} words; "
                    f"minimum is {min_handoff_words}."
                )
            if handoff_numbered_chapter_ref:
                errors.append(f"{relative}: reader Handoff uses a numbered chapter reference.")
            for phrase in handoff_generic_phrase_hits:
                errors.append(f"{relative}: reader Handoff uses generic transition formula {phrase!r}.")
            if next_chapter is None:
                if not handoff_closes_book:
                    errors.append(f"{relative}: final reader Handoff should close the book-level arc.")
            elif not handoff_names_next:
                next_title = str(next_chapter.get("title", "")).strip()
                errors.append(
                    f"{relative}: reader Handoff must name next manifest chapter title {next_title!r}."
                )
        if words < min_words:
            errors.append(
                f"{relative}: reader spine has {words} words after stripping; "
                f"minimum is {min_words}."
            )
        if missing_headings:
            errors.append(
                f"{relative}: reader spine is missing required headings after stripping: "
                + ", ".join(missing_headings)
            )
        for violation in section_word_violations:
            errors.append(
                f"{relative}: reader section {violation['heading']!r} has "
                f"{violation['word_count']} words; minimum is {violation['minimum']}."
            )
        for violation in section_prose_paragraph_violations:
            errors.append(
                f"{relative}: reader section {violation['heading']!r} has "
                f"{violation['paragraph_count']} substantial prose paragraphs; "
                f"minimum is {violation['minimum']}."
            )
        for hit in term_hits:
            errors.append(
                f"{relative}:{hit['line']}: live-only term {hit['term']!r} remains "
                "in generated reader prose."
            )
        for hit in meta_hits:
            errors.append(
                f"{relative}:{hit['line']}: reader meta phrase {hit['phrase']!r} remains "
                "in generated reader prose."
            )
        for hit in paragraph_start_hit_records:
            errors.append(
                f"{relative}:{hit['line']}: generated reader paragraph starts with "
                f"{hit['phrase']!r}; keep compact evidence boundaries inline with claim prose."
            )
        for hit in lowercase_sentence_start_hit_records:
            errors.append(
                f"{relative}:{hit['line']}: generated reader prose starts a sentence with "
                f"lower-case scaffold term {hit['phrase']!r}; preserve sentence capitalization."
            )

    for violation in heading_violations:
        errors.append(f"Stripped heading remains in reader edition: {violation}")
    for violation in view_marker_violations:
        errors.append(f"Reader view marker remains in reader edition: {violation}")

    return {
        "schema_version": "0.1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "profile": "reader_release",
        "minimum_chapter_word_count": min_words,
        "minimum_handoff_word_count": min_handoff_words,
        "minimum_section_word_counts": min_section_word_counts,
        "minimum_section_prose_paragraph_counts": min_section_prose_paragraph_counts,
        "hard_blocked_terms": hard_terms,
        "blocked_meta_phrases": blocked_meta_phrases,
        "blocked_paragraph_starts": blocked_paragraph_starts,
        "blocked_lowercase_sentence_starts": blocked_lowercase_sentence_starts,
        "required_reader_headings": required_headings,
        "chapter_count": len(chapter_records),
        "chapter_word_count_min": min(
            (int(record["word_count_after_strip"]) for record in chapter_records),
            default=0,
        ),
        "chapter_records": chapter_records,
        "stripped_heading_violations": heading_violations,
        "status": "pass" if not errors else "fail",
        "errors": errors,
        "non_claims": [
            "This report validates reader-spine structure only.",
            "It does not claim EPUB, PDF, DOCX, MP3, M4B, or audio-embedded EPUB artifacts exist.",
            "It does not promote any claim support state.",
        ],
    }


def write_report(report: dict[str, object], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validate in a temporary workspace without writing a report")
    parser.add_argument("--report", default=str(DEFAULT_REPORT), help="report path for non-check runs")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    with tempfile.TemporaryDirectory(prefix="asi-reader-spine-") as temp_dir:
        output_dir = Path(temp_dir)
        summary = build_reader_edition.generate(output_dir, "reader_release")
        report = validate_generated_reader(output_dir)
        report["reader_generation"] = summary

    if not args.check:
        write_report(report, Path(args.report))

    if report["status"] != "pass":
        print("Reader spine validation failed:")
        for error in report["errors"]:
            print(f" - {error}")
        sys.exit(1)

    print(
        "Reader spine validation passed: "
        f"{report['chapter_count']} chapters, "
        f"minimum reader-spine words {report['chapter_word_count_min']}."
    )


if __name__ == "__main__":
    main()
