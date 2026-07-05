#!/usr/bin/env python3
"""Audit curated-reader EPUB package content without approving release."""

from __future__ import annotations

import argparse
import hashlib
import json
import posixpath
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "editions" / "reader_manuscript" / "v1_0" / "curated_format_probe_manifest.json"
EPUB = ROOT / "build" / "curated_reader_edition" / "format_artifacts" / "epub" / "_reader_site" / "The-ASI-Stack.epub"
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
HREF_RE = re.compile(r"""href=["']([^"']+)["']""")
BARE_CLASS_ATTR_RE = re.compile(r"""<([A-Za-z][\w:.-]*)(?:[^<>]*?)\sclass(?=(?:\s|/|>))(?:[^<>]*?)>""")
FIGURE_PARAGRAPH_WRAPPER_RE = re.compile(r"""<p>\s*</?figure[^>]*>\s*</p>""")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Curated reader EPUB content audit failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_manifest() -> dict[str, Any]:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def href_target_exists(names: set[str], owner: str, href: str) -> bool:
    if href.startswith(("http://", "https://", "mailto:", "#")):
        return True
    target = href.split("#", 1)[0]
    if not target:
        return True
    base = posixpath.normpath(posixpath.join(posixpath.dirname(owner), target))
    return base in names


def observe() -> dict[str, Any]:
    if not EPUB.exists():
        fail([f"Missing EPUB artifact: {rel(EPUB)}. Run `python3 scripts/render_curated_reader_formats.py --formats epub` first."])

    with ZipFile(EPUB) as archive:
        names = archive.namelist()
        name_set = set(names)
        xhtml_entries = sorted(name for name in names if name.endswith(".xhtml"))
        content_xhtml_entries = sorted(name for name in xhtml_entries if name.startswith("EPUB/text/ch"))
        nav_text = archive.read("EPUB/nav.xhtml").decode("utf-8", errors="replace")
        opf_text = archive.read("EPUB/content.opf").decode("utf-8", errors="replace")

        live_marker_hits: list[str] = []
        raw_claim_marker_hits: list[str] = []
        empty_xhtml_entries: list[str] = []
        unresolved_hrefs: list[str] = []
        bare_class_attribute_hits: list[str] = []
        figure_paragraph_wrapper_hits: list[str] = []
        xml_parse_errors: list[str] = []
        required_marker_hits: dict[str, int] = {marker: 0 for marker in REQUIRED_MARKERS}
        total_text_chars = 0

        for name in xhtml_entries:
            text = archive.read(name).decode("utf-8", errors="replace")
            try:
                ET.fromstring(text)
            except ET.ParseError as exc:
                xml_parse_errors.append(f"{name}: {exc}")
            stripped_text = re.sub(r"<[^>]+>", " ", text)
            if not stripped_text.strip():
                empty_xhtml_entries.append(name)
            total_text_chars += len(stripped_text)
            for marker in LIVE_ONLY_MARKERS:
                if marker in text:
                    live_marker_hits.append(f"{name}: {marker}")
            if RAW_CORE_CLAIM_RE.search(text):
                raw_claim_marker_hits.append(name)
            for marker in REQUIRED_MARKERS:
                if marker in text:
                    required_marker_hits[marker] += 1
            for href in HREF_RE.findall(text):
                if not href_target_exists(name_set, name, href):
                    unresolved_hrefs.append(f"{name} -> {href}")
            for match in BARE_CLASS_ATTR_RE.finditer(text):
                bare_class_attribute_hits.append(f"{name}: <{match.group(1)} class>")
            for _match in FIGURE_PARAGRAPH_WRAPPER_RE.finditer(text):
                figure_paragraph_wrapper_hits.append(name)

    return {
        "status": "passed_epub_package_content_navigation_probe",
        "source_artifact": rel(EPUB),
        "source_sha256": sha256_file(EPUB),
        "xhtml_entries_checked": len(xhtml_entries),
        "content_xhtml_entries_checked": len(content_xhtml_entries),
        "total_text_characters_checked": total_text_chars,
        "nav_href_count": nav_text.count("href="),
        "opf_item_count": len(re.findall(r"<item\b", opf_text)),
        "opf_itemref_count": len(re.findall(r"<itemref\b", opf_text)),
        "empty_xhtml_entries": len(empty_xhtml_entries),
        "live_marker_hits": len(live_marker_hits),
        "raw_core_claim_marker_hits": len(raw_claim_marker_hits),
        "unresolved_internal_hrefs": len(unresolved_hrefs),
        "bare_class_attribute_hits": len(bare_class_attribute_hits),
        "figure_paragraph_wrapper_hits": len(figure_paragraph_wrapper_hits),
        "xml_parse_errors": len(xml_parse_errors),
        "required_text_markers_present": [
            marker for marker, count in required_marker_hits.items() if count > 0
        ],
        "review_boundary": (
            "All-XHTML EPUB package, content-marker, and internal-link checks are "
            "stronger local EPUB evidence than container inspection alone, including "
            "guards against Apple Books XML parse failures from bare class attributes and "
            "paragraph-wrapped figure tags, but this "
            "is not e-reader application review and does not approve the EPUB artifact for release."
        ),
    }


def validate_observed(observed: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if observed["xhtml_entries_checked"] != 52:
        errors.append("EPUB audit must check exactly 52 XHTML entries.")
    if observed["content_xhtml_entries_checked"] != 49:
        errors.append("EPUB audit must check exactly 49 packaged content XHTML entries.")
    if observed["total_text_characters_checked"] < 500_000:
        errors.append("EPUB audit text volume is unexpectedly small.")
    for zero_key in (
        "empty_xhtml_entries",
        "live_marker_hits",
        "raw_core_claim_marker_hits",
        "unresolved_internal_hrefs",
        "bare_class_attribute_hits",
        "figure_paragraph_wrapper_hits",
        "xml_parse_errors",
    ):
        if observed[zero_key] != 0:
            errors.append(f"EPUB audit expected {zero_key}=0, found {observed[zero_key]}.")
    missing = sorted(set(REQUIRED_MARKERS) - set(observed["required_text_markers_present"]))
    if missing:
        errors.append(f"EPUB audit missing required marker(s): {missing}.")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-manifest", action="store_true", help="write observed EPUB audit into the curated format probe manifest")
    args = parser.parse_args()

    manifest = load_manifest()
    observed = observe()
    errors = validate_observed(observed)
    if errors:
        fail(errors)

    if args.write_manifest:
        manifest["epub_content_audit"] = observed
        MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    else:
        recorded = manifest.get("epub_content_audit")
        if recorded != observed:
            fail(["curated_format_probe_manifest.json epub_content_audit is stale; run `python3 scripts/audit_curated_reader_epub_content.py --write-manifest`."])

    print(
        "Curated reader EPUB content audit passed: "
        f"{observed['xhtml_entries_checked']} XHTML entries, "
        f"{observed['content_xhtml_entries_checked']} content entries, "
        f"{observed['unresolved_internal_hrefs']} unresolved internal hrefs."
    )


if __name__ == "__main__":
    main()
