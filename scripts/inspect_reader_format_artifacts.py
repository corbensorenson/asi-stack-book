#!/usr/bin/env python3
"""Inspect local reader-format snapshots without treating them as a release."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys
from zipfile import BadZipFile, ZipFile

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ARTIFACT_ROOT = ROOT / "build" / "reader_edition" / "format_artifacts"
DEFAULT_REPORT = ROOT / "build" / "reader_edition" / "reader_artifact_inspection_report.json"
RAW_CORE_CLAIM_RE = re.compile(r"\[[A-Za-z0-9_-]+\.core,\s*label:\s*[^,\]]+,\s*support:\s*[^\]]+\]")
DC_TITLE_RE = re.compile(r"<dc:title[^>]*>(.*?)</dc:title>", re.DOTALL)
DC_CREATOR_RE = re.compile(r"<dc:creator[^>]*>(.*?)</dc:creator>", re.DOTALL)
DC_LANGUAGE_RE = re.compile(r"<dc:language[^>]*>(.*?)</dc:language>", re.DOTALL)
LIVE_ONLY_MARKERS = [
    "Chapter status",
    "Drafting guardrail",
    "Codex test plan",
    "Source crosswalk",
    "Claim-source mapping status",
    "Formalization hooks",
]


def relative(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def fail(message: str) -> None:
    raise AssertionError(message)


def inspect_html(root: Path) -> dict[str, object]:
    site_root = root / "html" / "_reader_site"
    if not site_root.exists():
        fail(f"missing HTML site snapshot: {relative(site_root)}")

    html_files = sorted((root / "html").rglob("*.html"))
    site_html_files = sorted(site_root.rglob("*.html"))
    chapter_files = sorted((site_root / "chapters").glob("*.html"))
    required_files = [
        site_root / "index.html",
        site_root / "preface.html",
        site_root / "appendices" / "B_glossary.html",
        site_root / "appendices" / "G_corben_source_corpus.html",
        site_root / "appendices" / "H_external_sources.html",
        site_root / "chapters" / "asi-is-a-stack-not-a-model.html",
    ]
    missing = [relative(path) for path in required_files if not path.exists()]
    if missing:
        fail(f"missing required HTML snapshot file(s): {', '.join(missing)}")
    if len(chapter_files) != 54:
        fail(f"expected 54 reader chapter HTML files, found {len(chapter_files)}")

    marker_hits: list[str] = []
    raw_claim_hits: list[str] = []
    checked_files = 0
    for path in site_html_files:
        text = path.read_text(encoding="utf-8", errors="ignore")
        checked_files += 1
        for marker in LIVE_ONLY_MARKERS:
            if marker in text:
                marker_hits.append(f"{relative(path)}: {marker}")
        if RAW_CORE_CLAIM_RE.search(text):
            raw_claim_hits.append(relative(path))

    if marker_hits:
        fail("live-only marker(s) leaked into HTML snapshot: " + "; ".join(marker_hits[:10]))
    if raw_claim_hits:
        fail("raw core-claim marker(s) leaked into HTML snapshot: " + "; ".join(raw_claim_hits[:10]))

    index_text = (site_root / "index.html").read_text(encoding="utf-8", errors="ignore")
    opening_text = (site_root / "chapters" / "asi-is-a-stack-not-a-model.html").read_text(
        encoding="utf-8",
        errors="ignore",
    )
    if "The ASI Stack" not in index_text or "The ASI Stack" not in opening_text:
        fail("expected book title missing from HTML index or opening chapter")
    if "evidence boundary" not in opening_text.lower():
        fail("opening chapter HTML snapshot lacks the compact evidence boundary")

    return {
        "status": "passed",
        "html_files": len(html_files),
        "site_html_files": len(site_html_files),
        "chapter_files": len(chapter_files),
        "required_files": [relative(path) for path in required_files],
        "checked_files_for_live_marker_leaks": checked_files,
        "live_marker_leaks": 0,
        "raw_core_claim_marker_leaks": 0,
    }


def inspect_epub(root: Path) -> dict[str, object]:
    path = root / "epub" / "_reader_site" / "The-ASI-Stack.epub"
    if not path.exists():
        fail(f"missing EPUB snapshot: {relative(path)}")
    if path.stat().st_size < 1_000_000:
        fail(f"EPUB snapshot is unexpectedly small: {path.stat().st_size} bytes")

    required_entries = {
        "mimetype",
        "META-INF/container.xml",
        "EPUB/content.opf",
        "EPUB/nav.xhtml",
        "EPUB/toc.ncx",
    }
    try:
        with ZipFile(path) as archive:
            names = archive.namelist()
            missing = sorted(required_entries.difference(names))
            if missing:
                fail(f"EPUB missing required entrie(s): {', '.join(missing)}")
            if names[0] != "mimetype":
                fail("EPUB mimetype entry is not first")
            if archive.read("mimetype") != b"application/epub+zip":
                fail("EPUB mimetype entry has unexpected content")
            xhtml_count = sum(1 for name in names if name.endswith(".xhtml"))
            image_count = sum(1 for name in names if name.lower().endswith((".png", ".jpg", ".jpeg", ".svg")))
            if xhtml_count < 58:
                fail(f"EPUB has too few XHTML entries: {xhtml_count}")
            if image_count < 54:
                fail(f"EPUB has too few image entries: {image_count}")
            title_page = archive.read("EPUB/text/title_page.xhtml").decode("utf-8", errors="ignore")
            nav = archive.read("EPUB/nav.xhtml").decode("utf-8", errors="ignore")
            opf = archive.read("EPUB/content.opf").decode("utf-8", errors="ignore")
            if "The ASI Stack" not in title_page or "The ASI Stack" not in nav:
                fail("EPUB title page or navigation lacks the book title")
            title_matches = DC_TITLE_RE.findall(opf)
            creator_matches = DC_CREATOR_RE.findall(opf)
            language_matches = DC_LANGUAGE_RE.findall(opf)
            if title_matches != ["The ASI Stack"]:
                fail(f"EPUB OPF title metadata is unexpected: {title_matches}")
            if creator_matches != ["Corben Sorenson"]:
                fail(f"EPUB OPF creator metadata is unexpected: {creator_matches}")
            if language_matches != ["en-US"]:
                fail(f"EPUB OPF language metadata is unexpected: {language_matches}")
            opf_item_count = len(re.findall(r"<item\b", opf))
            opf_itemref_count = len(re.findall(r"<itemref\b", opf))
            nav_href_count = nav.count("href=")
    except BadZipFile as exc:
        fail(f"EPUB is not a readable zip container: {exc}")

    return {
        "status": "passed",
        "path": relative(path),
        "bytes": path.stat().st_size,
        "entries": len(names),
        "xhtml_entries": xhtml_count,
        "image_entries": image_count,
        "opf_title": title_matches[0],
        "opf_creator": creator_matches[0],
        "opf_language": language_matches[0],
        "opf_item_count": opf_item_count,
        "opf_itemref_count": opf_itemref_count,
        "nav_href_count": nav_href_count,
        "required_entries": sorted(required_entries),
    }


def inspect_docx(root: Path) -> dict[str, object]:
    path = root / "docx" / "_reader_site" / "The-ASI-Stack.docx"
    if not path.exists():
        fail(f"missing DOCX snapshot: {relative(path)}")
    if path.stat().st_size < 1_000_000:
        fail(f"DOCX snapshot is unexpectedly small: {path.stat().st_size} bytes")

    required_entries = {
        "[Content_Types].xml",
        "_rels/.rels",
        "word/document.xml",
        "word/styles.xml",
        "word/_rels/document.xml.rels",
    }
    try:
        with ZipFile(path) as archive:
            names = archive.namelist()
            missing = sorted(required_entries.difference(names))
            if missing:
                fail(f"DOCX missing required entrie(s): {', '.join(missing)}")
            image_count = sum(1 for name in names if name.lower().startswith("word/media/"))
            if image_count < 54:
                fail(f"DOCX has too few embedded media files: {image_count}")
            document_xml = archive.read("word/document.xml").decode("utf-8", errors="ignore")
            paragraph_count = document_xml.count("<w:p")
            if paragraph_count < 1000:
                fail(f"DOCX document has too few paragraph markers: {paragraph_count}")
            if "The ASI Stack" not in document_xml:
                fail("DOCX document XML lacks the book title")
            if "evidence boundary" not in document_xml.lower():
                fail("DOCX document XML lacks compact evidence-boundary text")
    except BadZipFile as exc:
        fail(f"DOCX is not a readable zip container: {exc}")

    return {
        "status": "passed",
        "path": relative(path),
        "bytes": path.stat().st_size,
        "entries": len(names),
        "media_entries": image_count,
        "paragraph_markers": paragraph_count,
        "required_entries": sorted(required_entries),
    }


def inspect(root: Path) -> dict[str, object]:
    html = inspect_html(root)
    epub = inspect_epub(root)
    docx = inspect_docx(root)
    return {
        "schema_version": "0.1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "artifact_root": relative(root),
        "status": "passed",
        "formats": {
            "html": html,
            "epub": epub,
            "docx": docx,
        },
        "non_claims": [
            "This is a local structural inspection of ignored reader-format snapshots only.",
            "Passing this inspection does not approve a reader release or edition release record.",
            "This inspection does not check editorial quality, e-reader layout quality, source interpretation, proof adequacy, benchmark behavior, runtime behavior, PDF output, or audio output.",
        ],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact-root", default=str(DEFAULT_ARTIFACT_ROOT), help="reader format_artifacts directory")
    parser.add_argument("--output", default=str(DEFAULT_REPORT), help="JSON report path")
    parser.add_argument("--check", action="store_true", help="inspect without writing a report")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path(args.artifact_root)
    try:
        report = inspect(root)
    except AssertionError as exc:
        raise SystemExit(f"Reader artifact inspection failed: {exc}") from exc

    if not args.check:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(f"Reader artifact inspection report wrote: {output}")
    print(
        "Reader artifact inspection passed: "
        f"{report['formats']['html']['html_files']} HTML files, "
        f"{report['formats']['epub']['xhtml_entries']} EPUB XHTML entries, "
        f"{report['formats']['docx']['media_entries']} DOCX media entries."
    )


if __name__ == "__main__":
    main()
