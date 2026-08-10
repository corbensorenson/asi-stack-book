#!/usr/bin/env python3
"""Validate the manifest-governed public author-paper library."""

from __future__ import annotations

import argparse
import hashlib
import html
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

from sync_paper_library import MANIFEST, RECEIPTS, load_json, synchronize


ROOT = Path(__file__).resolve().parents[1]
HREF_RE = re.compile(r'href=["\']([^"\']+)["\']', re.IGNORECASE)
CHAPTER_NUMBER_RE = re.compile(r'<span class="chapter-number">(\d+)</span>')


def rendered_errors(site: Path) -> list[str]:
    errors: list[str] = []
    manifest = load_json(MANIFEST)
    records = manifest.get("records", []) if isinstance(manifest, dict) else []
    receipt_data = load_json(RECEIPTS)
    receipts = {
        str(row.get("source_id")): row
        for row in receipt_data.get("records", [])
        if isinstance(row, dict) and row.get("source_id")
    } if isinstance(receipt_data, dict) else {}
    paper_root = site / "papers"
    index = paper_root / "index.html"
    appendix = site / "appendices" / "G_corben_source_corpus.html"
    landing = site / "index.html"

    for required in (index, appendix, landing):
        if not required.exists():
            errors.append(f"rendered paper-library dependency is missing: {required}")
    if errors:
        return errors

    index_text = index.read_text(encoding="utf-8", errors="ignore")
    appendix_text = appendix.read_text(encoding="utf-8", errors="ignore")
    landing_text = landing.read_text(encoding="utf-8", errors="ignore")
    if 'papers/index.html' not in landing_text and 'href="papers/"' not in landing_text:
        errors.append("rendered landing page does not link the paper library")

    numeric_chapters = [int(value) for value in CHAPTER_NUMBER_RE.findall(landing_text)]
    if not numeric_chapters or max(numeric_chapters) != 85:
        maximum = max(numeric_chapters) if numeric_chapters else "none"
        errors.append(f"rendered living-book navigation must end at canonical chapter 85, found {maximum}")

    html_pages = [index]
    for record in records:
        source_id = str(record.get("source_id", ""))
        expected_sha = record.get("sha256") or receipts.get(source_id, {}).get("sha256")
        expected_bytes = record.get("bytes") or receipts.get(source_id, {}).get("bytes")
        page = paper_root / f"{source_id}.html"
        source = paper_root / "source" / f"{source_id}.md"
        if not page.exists():
            errors.append(f"{source_id}: rendered HTML route is missing")
            continue
        html_pages.append(page)
        page_text = page.read_text(encoding="utf-8", errors="ignore")
        if 'class="chapter-number"' in page_text or re.search(r"\bChapter\s+(?:8[6-9]|9\d|\d{3,})\b", page_text):
            errors.append(f"{source_id}: paper page was incorrectly numbered as a book chapter")
        if source_id not in page_text or str(expected_sha) not in page_text:
            errors.append(f"{source_id}: rendered provenance panel is missing the source identity or digest")
        if f"source/{source_id}.md" not in page_text:
            errors.append(f"{source_id}: rendered page does not link its exact source copy")
        if f"{source_id}.html" not in index_text:
            errors.append(f"{source_id}: paper index does not link the rendered page")
        if f"../papers/{source_id}.html" not in appendix_text:
            errors.append(f"{source_id}: Appendix G does not link the rendered paper route")
        if not source.exists():
            errors.append(f"{source_id}: rendered exact-source resource is missing")
        else:
            payload = source.read_bytes()
            if hashlib.sha256(payload).hexdigest() != expected_sha or len(payload) != expected_bytes:
                errors.append(f"{source_id}: rendered exact-source resource does not match its manifest identity")

    for page in html_pages:
        page_text = page.read_text(encoding="utf-8", errors="ignore")
        for raw_href in HREF_RE.findall(page_text):
            href = html.unescape(raw_href)
            parsed = urlsplit(href)
            if parsed.scheme or parsed.netloc or href.startswith(("#", "/")):
                continue
            if parsed.path.endswith(".qmd"):
                errors.append(f"{page.relative_to(site)} leaks a source-format .qmd link: {href}")
                continue
            target = (page.parent / parsed.path).resolve()
            try:
                target.relative_to(site.resolve())
            except ValueError:
                errors.append(f"{page.relative_to(site)} has an escaping local link: {href}")
                continue
            if parsed.path and not target.exists():
                errors.append(f"{page.relative_to(site)} has a broken local link: {href}")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", type=Path, help="Also validate the rendered living-book and paper-library routes.")
    args = parser.parse_args()
    errors = synchronize(check=True)
    if args.site:
        errors.extend(rendered_errors(args.site.resolve()))
    if errors:
        print("Paper library validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)
    count = len(load_json(MANIFEST)["records"])
    suffix = " plus rendered-site route and byte integrity" if args.site else ""
    print(f"Paper library validation passed: {count} exact author manuscripts and HTML reader routes{suffix}.")


if __name__ == "__main__":
    main()
