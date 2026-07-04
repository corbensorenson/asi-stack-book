#!/usr/bin/env python3
"""Validate curated-reader PDF extracted-text reading flow without approving PDF release."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "editions" / "reader_manuscript" / "v1_0" / "curated_format_probe_manifest.json"
STRUCTURE = ROOT / "book_structure.json"
REPORT = ROOT / "build" / "curated_reader_edition" / "curated_reader_pdf_reading_flow_report.json"
COMMAND = "python3 scripts/validate_curated_reader_pdf_reading_flow.py --write-manifest"
REQUIRED_MARKERS = (
    "The ASI Stack",
    "Reader Edition Draft",
    "evidence boundary",
    "Reader Source List",
    "External Citation Policy",
)
LIVE_ONLY_MARKERS = (
    "Chapter status",
    "Drafting guardrail",
    "Codex test plan",
    "Source crosswalk",
    "Claim-source mapping status",
    "Formalization hooks",
)
RAW_CORE_CLAIM_RE = re.compile(r"\[[A-Za-z0-9_-]+\.core,\s*label:\s*[^,\]]+,\s*support:\s*[^\]]+\]")
APPENDIX_HEADINGS = (
    ("A", "Glossary"),
    ("B", "Corben’s Own Sources, Papers, and Local Projects"),
    ("C", "External Sources by Other Authors"),
)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Curated reader PDF reading-flow review failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    if completed.returncode:
        fail([f"command failed ({completed.returncode}): {' '.join(command)}\n{completed.stderr[-2000:]}"])
    return completed


def parse_pdfinfo(pdf_path: Path) -> dict[str, str]:
    if shutil.which("pdfinfo") is None:
        fail(["pdfinfo is required for curated-reader PDF reading-flow review."])
    result: dict[str, str] = {}
    for line in run(["pdfinfo", str(pdf_path)]).stdout.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip()
    return result


def extract_text(pdf_path: Path) -> str:
    if shutil.which("pdftotext") is None:
        fail(["pdftotext is required for curated-reader PDF reading-flow review."])
    return run(["pdftotext", str(pdf_path), "-"]).stdout


def page_index(text: str, offset: int) -> int:
    return text[:offset].count("\f") + 1


def flexible_heading_re(prefix: str, title: str) -> re.Pattern[str]:
    words = title.split()
    title_pattern = r"\s+".join(re.escape(word) for word in words)
    return re.compile(r"\f\s*" + re.escape(prefix) + r"\s+" + title_pattern)


def chapter_titles() -> list[str]:
    structure = load_json(STRUCTURE)
    titles: list[str] = []
    for part in structure.get("parts", []):
        if not isinstance(part, dict):
            continue
        for chapter in part.get("chapters", []):
            if isinstance(chapter, dict) and isinstance(chapter.get("title"), str):
                titles.append(chapter["title"])
    return titles


def heading_hits(text: str, titles: list[str]) -> tuple[list[dict[str, Any]], list[str]]:
    missing: list[str] = []
    hits: list[dict[str, Any]] = []
    first_pattern = flexible_heading_re("1", titles[0])
    first = first_pattern.search(text)
    if not first:
        return [], [f"missing body heading 1: {titles[0]}"]
    body_start = first.start()
    previous_offset = body_start - 1
    for index, title in enumerate(titles, start=1):
        pattern = flexible_heading_re(str(index), title)
        matches = [match for match in pattern.finditer(text) if match.start() >= body_start]
        if not matches:
            missing.append(f"missing body heading {index}: {title}")
            continue
        match = matches[0]
        if match.start() <= previous_offset:
            missing.append(f"body heading {index} is out of order: {title}")
        previous_offset = match.start()
        hits.append(
            {
                "chapter_number": index,
                "title": title,
                "text_offset": match.start(),
                "pdf_text_page_index": page_index(text, match.start()),
            }
        )
    return hits, missing


def appendix_hits(text: str, after_offset: int) -> tuple[list[dict[str, Any]], list[str]]:
    missing: list[str] = []
    hits: list[dict[str, Any]] = []
    previous_offset = after_offset
    for letter, title in APPENDIX_HEADINGS:
        pattern = flexible_heading_re(letter, title)
        matches = [match for match in pattern.finditer(text) if match.start() > after_offset]
        if not matches:
            missing.append(f"missing appendix heading {letter}: {title}")
            continue
        match = matches[0]
        if match.start() <= previous_offset:
            missing.append(f"appendix heading {letter} is out of order: {title}")
        previous_offset = match.start()
        hits.append(
            {
                "appendix_letter": letter,
                "title": title,
                "text_offset": match.start(),
                "pdf_text_page_index": page_index(text, match.start()),
            }
        )
    return hits, missing


def observe() -> dict[str, Any]:
    manifest = load_json(MANIFEST)
    pdf_audit = manifest.get("pdf_layout_audit", {})
    if not isinstance(pdf_audit, dict):
        fail(["curated format manifest must contain pdf_layout_audit before PDF reading-flow review."])
    source_artifact = pdf_audit.get("source_artifact")
    if not isinstance(source_artifact, str) or not source_artifact:
        fail(["pdf_layout_audit.source_artifact must be present before PDF reading-flow review."])
    pdf_path = ROOT / source_artifact
    if not pdf_path.exists():
        fail([f"Missing PDF artifact: {source_artifact}"])

    info = parse_pdfinfo(pdf_path)
    text = extract_text(pdf_path)
    pages = text.split("\f")
    text_pages = pages[:-1] if pages and pages[-1] == "" else pages
    page_char_counts = [len(page.strip()) for page in text_pages]
    low_text_pages = [index for index, count in enumerate(page_char_counts, start=1) if count < 300]
    titles = chapter_titles()
    chapters, chapter_errors = heading_hits(text, titles)
    appendices, appendix_errors = appendix_hits(text, chapters[-1]["text_offset"] if chapters else 0)
    marker_hits = {marker: marker in text for marker in REQUIRED_MARKERS}
    live_marker_hits = [marker for marker in LIVE_ONLY_MARKERS if marker in text]
    raw_claim_hits = bool(RAW_CORE_CLAIM_RE.search(text))
    words = re.findall(r"\S+", text)

    return {
        "status": "passed_pdf_extracted_text_reading_flow_review" if not (chapter_errors or appendix_errors) else "failed_pdf_extracted_text_reading_flow_review",
        "source_artifact": source_artifact,
        "source_sha256": sha256_file(pdf_path),
        "report_ref": rel(REPORT),
        "review_command": COMMAND,
        "text_extractor": "pdftotext",
        "pdfinfo_pages": int(info.get("Pages", "0")),
        "pdfinfo_title": info.get("Title", ""),
        "pdfinfo_author": info.get("Author", ""),
        "pdfinfo_encrypted": info.get("Encrypted", ""),
        "pdfinfo_page_size": info.get("Page size", ""),
        "text_characters_checked": len(text),
        "word_tokens_checked": len(words),
        "form_feed_count": text.count("\f"),
        "text_pages_checked": len(text_pages),
        "nonempty_text_pages": sum(1 for count in page_char_counts if count > 0),
        "min_page_text_characters": min(page_char_counts),
        "max_page_text_characters": max(page_char_counts),
        "pages_under_300_text_characters": len(low_text_pages),
        "sample_pages_under_300_text_characters": low_text_pages[:10],
        "max_word_characters": max(len(word) for word in words),
        "replacement_character_count": text.count("\ufffd"),
        "required_text_markers_present": [
            marker for marker, present in marker_hits.items() if present
        ],
        "live_marker_hits": len(live_marker_hits),
        "raw_core_claim_marker_hits": int(raw_claim_hits),
        "chapter_headings_checked": len(chapters),
        "chapter_heading_errors": chapter_errors,
        "first_chapter_pdf_text_page_index": chapters[0]["pdf_text_page_index"] if chapters else 0,
        "last_chapter_pdf_text_page_index": chapters[-1]["pdf_text_page_index"] if chapters else 0,
        "chapter_heading_samples": chapters[:3] + chapters[-3:] if len(chapters) >= 6 else chapters,
        "appendix_headings_checked": len(appendices),
        "appendix_heading_errors": appendix_errors,
        "appendix_heading_samples": appendices,
        "review_boundary": (
            "This pdftotext reading-flow review checks extracted text volume, page text presence, "
            "chapter heading order, appendix heading order, reader markers, and live-marker leakage. "
            "It is not manual PDF page-by-page reading-flow review, not PDF viewer approval, and does not approve the PDF artifact."
        ),
        "non_claims": [
            "does not approve the PDF artifact for release",
            "does not replace manual PDF page-by-page reading-flow review",
            "does not replace PDF viewer review",
            "does not publish or archive a reader artifact",
            "does not approve EPUB, DOCX, e-reader, audio, or final figure artifacts",
            "does not promote any chapter core claim or support state",
        ],
    }


def validate_observed(observed: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    expected_exact = {
        "status": "passed_pdf_extracted_text_reading_flow_review",
        "source_artifact": "build/curated_reader_edition/format_artifacts/pdf/_reader_site/The-ASI-Stack.pdf",
        "pdfinfo_pages": 506,
        "pdfinfo_title": "The ASI Stack",
        "pdfinfo_author": "Corben Sorenson",
        "pdfinfo_encrypted": "no",
        "pdfinfo_page_size": "612 x 792 pts (letter)",
        "text_characters_checked": 1104355,
        "word_tokens_checked": 169502,
        "form_feed_count": 506,
        "text_pages_checked": 506,
        "nonempty_text_pages": 506,
        "min_page_text_characters": 44,
        "max_page_text_characters": 3828,
        "pages_under_300_text_characters": 17,
        "max_word_characters": 83,
        "replacement_character_count": 0,
        "live_marker_hits": 0,
        "raw_core_claim_marker_hits": 0,
        "chapter_headings_checked": 44,
        "chapter_heading_errors": [],
        "first_chapter_pdf_text_page_index": 28,
        "last_chapter_pdf_text_page_index": 412,
        "appendix_headings_checked": 3,
        "appendix_heading_errors": [],
    }
    for key, expected in expected_exact.items():
        if observed.get(key) != expected:
            errors.append(f"PDF reading-flow review expected {key}={expected!r}, found {observed.get(key)!r}.")
    if not re.fullmatch(r"[0-9a-f]{64}", str(observed.get("source_sha256", ""))):
        errors.append("source_sha256 must be a SHA-256 digest.")
    missing = sorted(set(REQUIRED_MARKERS) - set(observed.get("required_text_markers_present", [])))
    if missing:
        errors.append(f"missing required text marker(s): {missing}.")
    samples = observed.get("chapter_heading_samples", [])
    if not isinstance(samples, list) or len(samples) != 6:
        errors.append("chapter_heading_samples must carry first/last three chapter headings.")
    appendix_samples = observed.get("appendix_heading_samples", [])
    if not isinstance(appendix_samples, list) or len(appendix_samples) != 3:
        errors.append("appendix_heading_samples must carry three appendix headings.")
    boundary = str(observed.get("review_boundary", ""))
    if "not manual PDF page-by-page reading-flow review" not in boundary or "does not approve the PDF artifact" not in boundary:
        errors.append("review_boundary must preserve manual-review and release-approval boundaries.")
    non_claim_text = " ".join(str(item) for item in observed.get("non_claims", [])).lower()
    for phrase in (
        "does not approve the pdf artifact",
        "does not replace manual pdf page-by-page reading-flow review",
        "does not promote any chapter core claim",
    ):
        if phrase not in non_claim_text:
            errors.append(f"non_claims missing boundary phrase: {phrase}")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-manifest", action="store_true", help="write observed review into the curated format probe manifest")
    args = parser.parse_args()

    manifest = load_json(MANIFEST)
    observed = observe()
    report = {
        "schema_version": "0.1",
        "review_type": "curated_reader_pdf_extracted_text_reading_flow_review",
        "manifest": observed,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    errors = validate_observed(observed)
    if errors:
        fail(errors)

    if args.write_manifest:
        commands = manifest.setdefault("source_commands", [])
        if COMMAND not in commands:
            commands.append(COMMAND)
        refs = manifest.setdefault("local_report_refs", [])
        if rel(REPORT) not in refs:
            refs.append(rel(REPORT))
        manifest["pdf_reading_flow_review"] = observed
        MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    else:
        recorded = manifest.get("pdf_reading_flow_review")
        if recorded != observed:
            fail(
                [
                    "curated_format_probe_manifest.json pdf_reading_flow_review is stale; "
                    "run `python3 scripts/validate_curated_reader_pdf_reading_flow.py --write-manifest`."
                ]
            )

    print(
        "Curated reader PDF reading-flow review passed: "
        f"{observed['chapter_headings_checked']} chapter headings, "
        f"{observed['appendix_headings_checked']} appendix headings, "
        f"{observed['nonempty_text_pages']} nonempty text pages."
    )


if __name__ == "__main__":
    main()
