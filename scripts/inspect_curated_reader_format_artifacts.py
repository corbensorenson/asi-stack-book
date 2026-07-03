#!/usr/bin/env python3
"""Inspect local curated-reader format snapshots without approving release."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
from zipfile import BadZipFile, ZipFile


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ARTIFACT_ROOT = ROOT / "build" / "curated_reader_edition" / "format_artifacts"
DEFAULT_REPORT = ROOT / "build" / "curated_reader_edition" / "curated_reader_artifact_inspection_report.json"
DEFAULT_PDF_SAMPLE_DIR = ROOT / "build" / "curated_reader_edition" / "pdf_probe_pages"
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
PDF_SAMPLE_PAGES = [1, 2, 25, 300, 500]


def run_command(command: list[str]) -> str:
    result = subprocess.run(
        command,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if result.returncode != 0:
        fail(f"command failed ({result.returncode}): {' '.join(command)}\n{result.stdout[-2000:]}")
    return result.stdout


def relative(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


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
        site_root / "chapters" / "open-research-agenda-and-bibliography-plan.html",
    ]
    missing = [relative(path) for path in required_files if not path.exists()]
    if missing:
        fail(f"missing required HTML snapshot file(s): {', '.join(missing)}")
    if len(chapter_files) != 44:
        fail(f"expected 44 curated reader chapter HTML files, found {len(chapter_files)}")
    if len(site_html_files) != 49:
        fail(f"expected 49 curated reader HTML files, found {len(site_html_files)}")

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
        fail("opening chapter HTML snapshot lacks compact evidence-boundary text")
    if "source_mode" in opening_text:
        fail("curated reader HTML leaked raw manifest metadata into chapter prose")

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
                fail(f"EPUB missing required entries: {', '.join(missing)}")
            if names[0] != "mimetype":
                fail("EPUB mimetype entry is not first")
            if archive.read("mimetype") != b"application/epub+zip":
                fail("EPUB mimetype entry has unexpected content")
            xhtml_count = sum(1 for name in names if name.endswith(".xhtml"))
            image_count = sum(1 for name in names if name.lower().endswith((".png", ".jpg", ".jpeg", ".svg")))
            if xhtml_count < 49:
                fail(f"EPUB has too few XHTML entries for the curated reader: {xhtml_count}")
            if image_count < 44:
                fail(f"EPUB has too few image entries for the curated reader: {image_count}")
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
        "sha256": sha256_file(path),
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
                fail(f"DOCX missing required entries: {', '.join(missing)}")
            media_names = [name for name in names if name.lower().startswith("word/media/")]
            image_count = len(media_names)
            png_count = sum(1 for name in media_names if name.lower().endswith(".png"))
            svg_count = sum(1 for name in media_names if name.lower().endswith(".svg"))
            if image_count < 44:
                fail(f"DOCX has too few embedded media files for the curated reader: {image_count}")
            if svg_count:
                fail(f"DOCX still contains SVG media entries after PNG fallback pass: {svg_count}")
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
        "sha256": sha256_file(path),
        "entries": len(names),
        "media_entries": image_count,
        "png_media_entries": png_count,
        "svg_media_entries": svg_count,
        "paragraph_markers": paragraph_count,
        "required_entries": sorted(required_entries),
    }


def inspect_pdf(root: Path, sample_dir: Path) -> dict[str, object]:
    path = root / "pdf" / "_reader_site" / "The-ASI-Stack.pdf"
    if not path.exists():
        fail(f"missing PDF snapshot: {relative(path)}")
    if path.stat().st_size < 1_000_000:
        fail(f"PDF snapshot is unexpectedly small: {path.stat().st_size} bytes")

    for command_name in ("pdfinfo", "pdftotext", "pdftoppm"):
        if shutil.which(command_name) is None:
            fail(f"{command_name} is required for curated PDF inspection")

    pdfinfo_output = run_command(["pdfinfo", str(path)])
    info: dict[str, str] = {}
    for line in pdfinfo_output.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        info[key.strip()] = value.strip()
    try:
        pages = int(info.get("Pages", "0"))
    except ValueError:
        pages = 0
    if pages < 100:
        fail(f"PDF has too few pages for the curated reader: {pages}")
    if info.get("Title") != "The ASI Stack":
        fail(f"PDF title metadata is unexpected: {info.get('Title')!r}")
    if info.get("Author") != "Corben Sorenson":
        fail(f"PDF author metadata is unexpected: {info.get('Author')!r}")
    if info.get("Encrypted") != "no":
        fail("PDF must not be encrypted")
    if info.get("Page size") and "612 x 792" not in info["Page size"]:
        fail(f"PDF page size should be letter, got {info['Page size']!r}")

    text = run_command(["pdftotext", str(path), "-"])
    required_text = [
        "The ASI Stack",
        "Reader Edition Draft",
        "evidence boundary",
        "Reader Source List",
        "External Citation Policy",
    ]
    missing_text = [marker for marker in required_text if marker not in text]
    if missing_text:
        fail(f"PDF text extraction missing required marker(s): {', '.join(missing_text)}")

    if sample_dir.exists():
        for existing in sample_dir.glob("*.png"):
            existing.unlink()
    sample_dir.mkdir(parents=True, exist_ok=True)
    sample_files: list[str] = []
    for page in PDF_SAMPLE_PAGES:
        if page > pages:
            continue
        prefix = sample_dir / f"page-{page}"
        run_command(["pdftoppm", "-f", str(page), "-l", str(page), "-png", "-r", "120", str(path), str(prefix)])
        produced = sorted(sample_dir.glob(f"page-{page}-*.png"))
        if not produced:
            fail(f"pdftoppm did not produce a PNG for page {page}")
        sample_files.extend(relative(item) for item in produced)

    return {
        "status": "passed",
        "path": relative(path),
        "bytes": path.stat().st_size,
        "sha256": sha256_file(path),
        "pages": pages,
        "title": info.get("Title", ""),
        "author": info.get("Author", ""),
        "producer": info.get("Producer", ""),
        "page_size": info.get("Page size", ""),
        "encrypted": info.get("Encrypted", ""),
        "sample_pages": [page for page in PDF_SAMPLE_PAGES if page <= pages],
        "sample_page_pngs": sample_files,
        "required_text_markers": required_text,
    }


def inspect(root: Path) -> dict[str, object]:
    html = inspect_html(root)
    epub = inspect_epub(root)
    docx = inspect_docx(root)
    pdf = inspect_pdf(root, DEFAULT_PDF_SAMPLE_DIR)
    return {
        "schema_version": "0.1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "artifact_root": relative(root),
        "source_mode": "tracked_curated_reader_manuscript",
        "status": "passed",
        "formats": {
            "html": html,
            "epub": epub,
            "docx": docx,
            "pdf": pdf,
        },
        "release_blockers_preserved": [
            "curated_reconciliation_not_approved",
            "format_artifact_not_reviewed",
            "reader_release_record_not_created",
            "full_format_artifact_review_not_completed",
            "app_or_ereader_review_not_completed",
        ],
        "non_claims": [
            "This is a local structural inspection of ignored curated-reader format snapshots only.",
            "Passing this inspection does not approve a reader release or edition release record.",
            "This inspection does not check full editorial quality, full layout quality, e-reader behavior, app behavior, full PDF page-by-page layout quality, audio output, source interpretation, proof adequacy, benchmark behavior, or runtime behavior.",
            "This inspection does not promote any claim support state.",
        ],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact-root", default=str(DEFAULT_ARTIFACT_ROOT), help="curated reader format_artifacts directory")
    parser.add_argument("--output", default=str(DEFAULT_REPORT), help="JSON report path")
    parser.add_argument("--check", action="store_true", help="inspect without writing a report")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path(args.artifact_root)
    try:
        report = inspect(root)
    except AssertionError as exc:
        raise SystemExit(f"Curated reader artifact inspection failed: {exc}") from exc

    if not args.check:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(f"Curated reader artifact inspection report wrote: {output}")
    print(
        "Curated reader artifact inspection passed: "
        f"{report['formats']['html']['html_files']} HTML files, "
        f"{report['formats']['epub']['xhtml_entries']} EPUB XHTML entries, "
        f"{report['formats']['docx']['png_media_entries']} DOCX PNG media entries, "
        f"{report['formats']['docx']['svg_media_entries']} DOCX SVG media entries, "
        f"{report['formats']['pdf']['pages']} PDF pages."
    )


if __name__ == "__main__":
    main()
