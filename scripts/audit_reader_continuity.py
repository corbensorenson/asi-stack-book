#!/usr/bin/env python3
"""Generate or validate the Phase 2 reader-continuity audit.

This is a heuristic review aid. It derives the reader edition in a temporary
workspace, measures continuity and density signals, and writes a deterministic
public report. It does not claim manual review or release readiness.
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
import tempfile
from pathlib import Path
from typing import Any

import build_reader_edition


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT = ROOT / "docs" / "reader_continuity_audit.md"
WORD_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9'_-]*")
CODE_BLOCK_RE = re.compile(r"```.*?```", re.DOTALL)
MERMAID_RE = re.compile(r"```\{?mermaid\}?", re.IGNORECASE)
TABLE_ROW_RE = re.compile(r"^\s*\|.*\|\s*$", re.MULTILINE)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
DENSE_TERMS = (
    "schema",
    "json",
    "lean",
    "proof",
    "fixture",
    "validator",
    "validation",
    "benchmark",
    "release record",
    "source review",
    "appendix",
    "quarto",
    "ledger",
    "receipt",
    "record",
)
SOFT_META_TERMS = (
    "artifact",
    "authority",
    "boundary",
    "contract",
    "implementation",
    "residual",
)
REQUIRED_REPORT_PHRASES = (
    "not a manual 46-chapter review",
    "does not claim a reviewed reader release exists",
    "does not claim EPUB, PDF, DOCX, audio, or audio-embedded EPUB artifacts exist",
    "does not promote any claim support state",
)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def flatten_chapters(structure: dict[str, Any]) -> list[dict[str, str]]:
    chapters: list[dict[str, str]] = []
    for part in structure.get("parts", []):
        if not isinstance(part, dict):
            continue
        for chapter in part.get("chapters", []):
            if not isinstance(chapter, dict):
                continue
            chapter_id = chapter.get("id")
            title = chapter.get("title")
            file_path = chapter.get("file")
            if isinstance(chapter_id, str) and isinstance(title, str) and isinstance(file_path, str):
                chapters.append({"id": chapter_id, "title": title, "file": file_path})
    return chapters


def strip_analysis_noise(text: str) -> str:
    text = build_reader_edition.strip_frontmatter(text)
    text = CODE_BLOCK_RE.sub(" ", text)
    lines = [
        line
        for line in text.splitlines()
        if not line.lstrip().startswith("|") and not line.lstrip().startswith("!")
    ]
    return "\n".join(lines)


def prose_paragraphs(text: str) -> list[str]:
    text = build_reader_edition.strip_frontmatter(text)
    text = CODE_BLOCK_RE.sub(" ", text)
    paragraphs: list[str] = []
    for block in re.split(r"\n\s*\n", text):
        paragraph = re.sub(r"\s+", " ", block.strip())
        if not paragraph:
            continue
        if paragraph.startswith(("#", "|", "!", ":::", "- ", "* ")):
            continue
        if re.match(r"^\d+\.\s", paragraph):
            continue
        if len(WORD_RE.findall(paragraph)) >= 18:
            paragraphs.append(paragraph)
    return paragraphs


def count_term_hits(text: str, terms: tuple[str, ...]) -> int:
    lowered = text.lower()
    return sum(lowered.count(term) for term in terms)


def first_body_sentence(text: str) -> str:
    paragraphs = prose_paragraphs(text)
    if not paragraphs:
        return ""
    sentences = [sentence.strip() for sentence in re.split(r"(?<=[.!?])\s+", paragraphs[0]) if sentence.strip()]
    return sentences[0] if sentences else paragraphs[0]


def heading_titles(text: str) -> list[str]:
    return [match.group(2).strip() for match in HEADING_RE.finditer(build_reader_edition.strip_frontmatter(text))]


def chapter_priority(record: dict[str, Any]) -> tuple[str, int]:
    score = 0
    score += int(record["long_paragraphs"]) * 3
    score += int(record["tables"]) * 2
    score += int(record["code_blocks"])
    score += int(record["dense_term_hits"]) // 25
    score += int(record["soft_meta_hits"]) // 60
    if int(record["words"]) >= 5000:
        score += 4
    elif int(record["words"]) >= 4000:
        score += 2
    if int(record["diagrams"]) >= 2:
        score += 1

    if score >= 10:
        return "high", score
    if score >= 5:
        return "medium", score
    return "low", score


def analyze_reader_source(output_dir: Path, summary: dict[str, Any]) -> dict[str, Any]:
    structure = load_json(ROOT / "book_structure.json")
    if not isinstance(structure, dict):
        raise TypeError("book_structure.json must contain an object.")
    chapters = flatten_chapters(structure)
    records: list[dict[str, Any]] = []

    for chapter in chapters:
        path = output_dir / chapter["file"]
        text = path.read_text(encoding="utf-8")
        body = strip_analysis_noise(text)
        paragraphs = prose_paragraphs(text)
        long_paragraphs = sum(1 for paragraph in paragraphs if len(WORD_RE.findall(paragraph)) >= 160)
        code_blocks = max(0, text.count("```") // 2 - len(MERMAID_RE.findall(text)))
        record: dict[str, Any] = {
            "id": chapter["id"],
            "title": chapter["title"],
            "file": chapter["file"],
            "words": len(WORD_RE.findall(body)),
            "prose_paragraphs": len(paragraphs),
            "long_paragraphs": long_paragraphs,
            "tables": len(TABLE_ROW_RE.findall(text)),
            "diagrams": len(MERMAID_RE.findall(text)),
            "code_blocks": code_blocks,
            "dense_term_hits": count_term_hits(body, DENSE_TERMS),
            "soft_meta_hits": count_term_hits(body, SOFT_META_TERMS),
            "heading_count": len(heading_titles(text)),
            "first_sentence": first_body_sentence(text),
        }
        priority, score = chapter_priority(record)
        record["review_priority"] = priority
        record["priority_score"] = score
        records.append(record)

    word_counts = [int(record["words"]) for record in records]
    priority_counts = {
        priority: sum(1 for record in records if record["review_priority"] == priority)
        for priority in ("high", "medium", "low")
    }
    top_records = sorted(
        records,
        key=lambda record: (
            -int(record["priority_score"]),
            -int(record["dense_term_hits"]),
            -int(record["words"]),
            str(record["id"]),
        ),
    )[:12]
    opening_stems: dict[str, list[str]] = {}
    for record in records:
        words = WORD_RE.findall(str(record["first_sentence"]).lower())[:8]
        if len(words) < 6:
            continue
        stem = " ".join(words)
        opening_stems.setdefault(stem, []).append(str(record["id"]))
    repeated_openings = {
        stem: ids
        for stem, ids in sorted(opening_stems.items())
        if len(ids) > 1
    }

    overlay = summary.get("reader_overlay", {})
    if not isinstance(overlay, dict):
        overlay = {}

    return {
        "summary": {
            "chapters": len(records),
            "generated_files": summary.get("files", 0),
            "live_only_sections_removed": summary.get("stripped_heading_count", 0),
            "human_only_bridges_unwrapped": summary.get("human_only_blocks_unwrapped", 0),
            "reader_scaffold_terms_humanized": summary.get("reader_scaffold_terms_humanized", 0),
            "active_overlay_operations": overlay.get("active_operations", 0),
            "applied_overlay_operations": overlay.get("applied_operations", 0),
            "min_words": min(word_counts) if word_counts else 0,
            "median_words": int(statistics.median(word_counts)) if word_counts else 0,
            "max_words": max(word_counts) if word_counts else 0,
            "total_words": sum(word_counts),
            "priority_counts": priority_counts,
            "total_tables": sum(int(record["tables"]) for record in records),
            "total_diagrams": sum(int(record["diagrams"]) for record in records),
            "total_code_blocks": sum(int(record["code_blocks"]) for record in records),
            "long_paragraphs": sum(int(record["long_paragraphs"]) for record in records),
            "repeated_opening_stems": len(repeated_openings),
        },
        "records": records,
        "top_records": top_records,
        "repeated_openings": repeated_openings,
    }


def priority_reason(record: dict[str, Any]) -> str:
    reasons: list[str] = []
    if int(record["words"]) >= 5000:
        reasons.append("very long")
    elif int(record["words"]) >= 4000:
        reasons.append("long")
    if int(record["dense_term_hits"]) >= 120:
        reasons.append("dense technical terms")
    if int(record["long_paragraphs"]):
        reasons.append(f"{record['long_paragraphs']} long paragraph(s)")
    if int(record["tables"]):
        reasons.append(f"{record['tables']} table row(s)")
    if int(record["code_blocks"]):
        reasons.append(f"{record['code_blocks']} code block(s)")
    if not reasons:
        reasons.append("lower-density chapter")
    return "; ".join(reasons)


def render_report(audit: dict[str, Any]) -> str:
    summary = audit["summary"]
    records = audit["records"]
    top_records = audit["top_records"]
    repeated_openings = audit["repeated_openings"]

    lines = [
        "# Reader Continuity Audit",
        "",
        "Status: generated heuristic report for Phase 2 reader review.",
        "",
        "This report is generated by `python3 scripts/audit_reader_continuity.py --write` from a temporary reader-edition workspace. It is not a manual 46-chapter review, not a release record, and not proof that the normal reader manuscript is publication-ready.",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Reader chapters measured | {summary['chapters']} |",
        f"| Generated files | {summary['generated_files']} |",
        f"| Live-only sections removed before audit | {summary['live_only_sections_removed']} |",
        f"| Human-only bridges unwrapped | {summary['human_only_bridges_unwrapped']} |",
        f"| Reader scaffold terms humanized | {summary['reader_scaffold_terms_humanized']} |",
        f"| Active reader overlay operations | {summary['active_overlay_operations']} |",
        f"| Applied reader overlay operations | {summary['applied_overlay_operations']} |",
        f"| Reader words measured | {summary['total_words']:,} |",
        f"| Minimum chapter words | {summary['min_words']:,} |",
        f"| Median chapter words | {summary['median_words']:,} |",
        f"| Maximum chapter words | {summary['max_words']:,} |",
        f"| High-priority heuristic review chapters | {summary['priority_counts']['high']} |",
        f"| Medium-priority heuristic review chapters | {summary['priority_counts']['medium']} |",
        f"| Low-priority heuristic review chapters | {summary['priority_counts']['low']} |",
        f"| Table rows in generated reader chapters | {summary['total_tables']} |",
        f"| Mermaid diagrams in generated reader chapters | {summary['total_diagrams']} |",
        f"| Non-Mermaid code blocks in generated reader chapters | {summary['total_code_blocks']} |",
        f"| Paragraphs at or above 160 words | {summary['long_paragraphs']} |",
        f"| Repeated first-sentence stems detected | {summary['repeated_opening_stems']} |",
        "",
        "## How To Use This Audit",
        "",
        "- Treat high-priority rows as the first candidates for human continuity review, not as defects.",
        "- Classify each real issue as a canonical live-book edit, a reader-only overlay, companion-note treatment, or no action.",
        "- Preserve claim text, support boundaries, implementation horizons, and non-claim language inherited from the live book.",
        "- Do not render or publish reader artifacts from this audit alone.",
        "",
        "## Review Queue",
        "",
        "| Priority | Score | Chapter | Words | Dense hits | Tables | Code | Long paragraphs | Reason |",
        "|---|---:|---|---:|---:|---:|---:|---:|---|",
    ]
    for record in top_records:
        lines.append(
            f"| {record['review_priority']} | {record['priority_score']} | "
            f"`{record['id']}` | {int(record['words']):,} | "
            f"{record['dense_term_hits']} | {record['tables']} | {record['code_blocks']} | "
            f"{record['long_paragraphs']} | {priority_reason(record)} |"
        )

    lines.extend([
        "",
        "## Repeated Opening Stems",
        "",
    ])
    if repeated_openings:
        lines.extend(["| Opening stem | Chapters |", "|---|---|"])
        for stem, ids in repeated_openings.items():
            lines.append(f"| `{stem}` | {', '.join(f'`{item}`' for item in ids)} |")
    else:
        lines.append("No repeated first-sentence stems were detected with the current eight-word heuristic.")

    lines.extend([
        "",
        "## Chapter Metrics",
        "",
        "| Chapter | Words | Paragraphs | Dense hits | Tables | Diagrams | Code | Long paragraphs | Priority |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ])
    for record in records:
        lines.append(
            f"| `{record['id']}` | {int(record['words']):,} | {record['prose_paragraphs']} | "
            f"{record['dense_term_hits']} | {record['tables']} | {record['diagrams']} | "
            f"{record['code_blocks']} | {record['long_paragraphs']} | {record['review_priority']} |"
        )

    lines.extend([
        "",
        "## Non-Claims",
        "",
        "- This audit does not claim a reviewed reader release exists.",
        "- This audit does not claim EPUB, PDF, DOCX, audio, or audio-embedded EPUB artifacts exist.",
        "- This audit does not promote any claim support state.",
        "- This audit does not prove reader quality; it only creates a deterministic queue for human review.",
        "",
    ])
    return "\n".join(lines)


def build_audit() -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="asi-reader-continuity-") as temp_dir:
        output_dir = Path(temp_dir)
        summary = build_reader_edition.generate(output_dir, "reader_release")
        return analyze_reader_source(output_dir, summary)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help=f"write {DEFAULT_REPORT.relative_to(ROOT)}")
    parser.add_argument("--check", action="store_true", help="verify the tracked report is current")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    audit = build_audit()
    report = render_report(audit)

    for phrase in REQUIRED_REPORT_PHRASES:
        if phrase not in report:
            raise SystemExit(f"Reader continuity audit missing required non-claim phrase: {phrase}")

    if args.write:
        DEFAULT_REPORT.write_text(report, encoding="utf-8")
        print(
            "Reader continuity audit written: "
            f"{DEFAULT_REPORT.relative_to(ROOT)} "
            f"({audit['summary']['chapters']} chapters, "
            f"{audit['summary']['priority_counts']['high']} high-priority heuristic review chapter(s))."
        )
        return

    if args.check:
        if not DEFAULT_REPORT.exists():
            raise SystemExit(f"Reader continuity audit missing: {DEFAULT_REPORT.relative_to(ROOT)}")
        current = DEFAULT_REPORT.read_text(encoding="utf-8")
        if current != report:
            raise SystemExit(
                "Reader continuity audit is stale. Run `python3 scripts/audit_reader_continuity.py --write`."
            )
        print(
            "Reader continuity audit validated: "
            f"{audit['summary']['chapters']} chapters, "
            f"{audit['summary']['priority_counts']['high']} high-priority heuristic review chapter(s)."
        )
        return

    print(
        "Reader continuity audit generated in memory: "
        f"{audit['summary']['chapters']} chapters, "
        f"{audit['summary']['priority_counts']['high']} high-priority heuristic review chapter(s). "
        "Use --write to update docs/reader_continuity_audit.md."
    )


if __name__ == "__main__":
    main()
