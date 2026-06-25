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
    "claim-source mapping status",
    "formalization hooks",
]


def load_structure() -> dict:
    value = json.loads((ROOT / "book_structure.json").read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError("book_structure.json must contain an object")
    return value


def flatten_chapter_files(structure: dict) -> list[str]:
    files: list[str] = []
    for part in structure.get("parts", []):
        if not isinstance(part, dict):
            continue
        for chapter in part.get("chapters", []):
            if isinstance(chapter, dict) and isinstance(chapter.get("file"), str):
                files.append(chapter["file"])
    return files


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


def live_only_term_hits(text: str, terms: list[str]) -> list[dict[str, object]]:
    hits: list[dict[str, object]] = []
    lower_terms = [(term, term.lower()) for term in terms]
    for lineno, line in enumerate(text.splitlines(), start=1):
        lowered = line.lower()
        for original, lowered_term in lower_terms:
            if lowered_term in lowered:
                hits.append({"line": lineno, "term": original, "text": line.strip()})
    return hits


def validate_generated_reader(output_dir: Path) -> dict[str, object]:
    structure = load_structure()
    profile = build_reader_edition.find_profile("reader_release")
    policy = load_validation_policy()
    min_words = int(policy.get("minimum_chapter_word_count", DEFAULT_MIN_WORDS))
    hard_terms = policy.get("hard_blocked_terms", DEFAULT_HARD_TERMS)
    if not isinstance(hard_terms, list) or not all(isinstance(term, str) for term in hard_terms):
        raise TypeError("reader_spine_validation.hard_blocked_terms must be a list of strings")

    strip_headings = build_reader_edition.profile_strip_headings(profile)
    heading_violations = build_reader_edition.scan_for_stripped_headings(output_dir, strip_headings)

    chapter_records: list[dict[str, object]] = []
    errors: list[str] = []
    for relative in flatten_chapter_files(structure):
        path = output_dir / relative
        if not path.exists():
            errors.append(f"Generated reader chapter missing: {relative}")
            continue
        text = path.read_text(encoding="utf-8")
        words = count_reader_words(text)
        term_hits = live_only_term_hits(text, hard_terms)
        chapter_records.append(
            {
                "file": relative,
                "word_count_after_strip": words,
                "live_only_term_hits": term_hits,
            }
        )
        if words < min_words:
            errors.append(
                f"{relative}: reader spine has {words} words after stripping; "
                f"minimum is {min_words}."
            )
        for hit in term_hits:
            errors.append(
                f"{relative}:{hit['line']}: live-only term {hit['term']!r} remains "
                "in generated reader prose."
            )

    for violation in heading_violations:
        errors.append(f"Stripped heading remains in reader edition: {violation}")

    return {
        "schema_version": "0.1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "profile": "reader_release",
        "minimum_chapter_word_count": min_words,
        "hard_blocked_terms": hard_terms,
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
