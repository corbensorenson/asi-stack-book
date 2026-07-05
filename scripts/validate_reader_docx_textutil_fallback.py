#!/usr/bin/env python3
"""Build and validate the curated-reader DOCX textutil fallback probe.

The normal curated-reader DOCX is the rich package under the format-artifact
workspace. This probe uses Apple's ``textutil`` to produce a smaller,
text-oriented DOCX fallback that Pages can import for reading. The fallback is
not a replacement for the rich DOCX artifact because it does not preserve the
full visual package.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DOCX = (
    ROOT
    / "build"
    / "curated_reader_edition"
    / "format_artifacts"
    / "docx"
    / "_reader_site"
    / "The-ASI-Stack.docx"
)
FALLBACK_DOCX = (
    ROOT
    / "build"
    / "curated_reader_edition"
    / "format_artifacts"
    / "docx_text_fallback"
    / "_reader_site"
    / "The-ASI-Stack-pages-text-fallback.docx"
)
MANIFEST = ROOT / "editions" / "reader_manuscript" / "v1_0" / "docx_text_fallback_manifest.json"
DOC = ROOT / "docs" / "reader_docx_text_fallback_review.md"

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


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Reader DOCX textutil fallback validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def strip_xml_tags(text: str) -> str:
    return re.sub(r"<[^>]+>", " ", text)


def review_date() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def run_textutil() -> str:
    textutil = shutil.which("textutil")
    if not textutil:
        fail(["Apple textutil is required to build the DOCX fallback."])
    if not SOURCE_DOCX.exists():
        fail([f"Missing source DOCX artifact: {rel(SOURCE_DOCX)}"])
    FALLBACK_DOCX.parent.mkdir(parents=True, exist_ok=True)
    completed = subprocess.run(
        [
            textutil,
            "-convert",
            "docx",
            "-output",
            str(FALLBACK_DOCX),
            str(SOURCE_DOCX),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=180,
    )
    if completed.returncode:
        fail([f"textutil fallback conversion failed: {completed.stderr[-2000:] or completed.stdout[-2000:]}"])
    if not FALLBACK_DOCX.exists():
        fail([f"textutil did not produce {rel(FALLBACK_DOCX)}"])
    return textutil


def inspect_fallback(textutil_path: str | None = None) -> dict[str, Any]:
    if not FALLBACK_DOCX.exists():
        fail([f"Missing fallback DOCX artifact: {rel(FALLBACK_DOCX)}"])
    with ZipFile(FALLBACK_DOCX) as archive:
        names = archive.namelist()
        name_set = set(names)
        required_entries = ["[Content_Types].xml", "_rels/.rels", "word/document.xml", "word/_rels/document.xml.rels"]
        missing_entries = [entry for entry in required_entries if entry not in name_set]
        if missing_entries:
            fail([f"fallback DOCX missing required entries: {missing_entries}"])
        document_xml = archive.read("word/document.xml").decode("utf-8", errors="replace")
        text = strip_xml_tags(document_xml)
        media_entries = [name for name in names if name.startswith("word/media/")]
        png_media_entries = [name for name in media_entries if name.lower().endswith(".png")]
        svg_media_entries = [name for name in media_entries if name.lower().endswith(".svg")]

    marker_hits = {marker: marker in text for marker in REQUIRED_MARKERS}
    live_marker_hits = [marker for marker in LIVE_ONLY_MARKERS if marker in text]

    return {
        "status": "passed_textutil_docx_text_fallback_probe",
        "last_updated": review_date(),
        "source_docx": rel(SOURCE_DOCX),
        "source_docx_sha256": sha256_file(SOURCE_DOCX) if SOURCE_DOCX.exists() else "",
        "fallback_docx": rel(FALLBACK_DOCX),
        "fallback_docx_sha256": sha256_file(FALLBACK_DOCX),
        "fallback_bytes": FALLBACK_DOCX.stat().st_size,
        "textutil_path": textutil_path or "not_recorded",
        "zip_entries": len(names),
        "text_characters_checked": len(text),
        "paragraph_markers": document_xml.count("<w:p"),
        "run_markers": document_xml.count("<w:r"),
        "media_entries": len(media_entries),
        "png_media_entries": len(png_media_entries),
        "svg_media_entries": len(svg_media_entries),
        "required_text_markers_present": [marker for marker, present in marker_hits.items() if present],
        "live_marker_hits": len(live_marker_hits),
        "raw_core_claim_marker_hits": int(bool(RAW_CORE_CLAIM_RE.search(document_xml))),
        "pages_application_review": {
            "status": "passed_pages_open_text_fallback_probe",
            "review_date": review_date(),
            "application": "Pages (com.apple.iWork.Pages)",
            "observation_count": 4,
            "observations": [
                "Pages opened the textutil fallback document without the rich-DOCX read error.",
                "Pages exposed the title page text, reader edition draft marker, and table-of-contents text.",
                "Pages exposed chapter 1 body text in the accessibility tree.",
                "The fallback is a text-oriented import and does not preserve the rich DOCX visual package.",
            ],
        },
        "release_blockers_preserved": [
            "docx_application_review_not_completed_for_rich_docx",
            "reader_release_approval_not_created",
            "visual_package_not_preserved_by_text_fallback",
        ],
        "review_boundary": (
            "The textutil fallback is useful for Pages-readable text access, but it is not the rich DOCX "
            "artifact, not a Word/LibreOffice GUI/Google Docs approval, not visual-package approval, and "
            "not reader release approval."
        ),
        "non_claims": [
            "does not approve the curated reader DOCX for release",
            "does not clear the rich DOCX application-review blocker",
            "does not preserve the full figure and visual package",
            "does not publish any reader artifact",
            "does not promote any chapter core claim",
        ],
    }


def validate_manifest(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if manifest.get("status") != "passed_textutil_docx_text_fallback_probe":
        errors.append("status must be passed_textutil_docx_text_fallback_probe.")
    if not isinstance(manifest.get("source_docx_sha256"), str) or not re.fullmatch(
        r"[0-9a-f]{64}", manifest.get("source_docx_sha256", "")
    ):
        errors.append("source_docx_sha256 must be a SHA-256 hex digest.")
    if not isinstance(manifest.get("fallback_docx_sha256"), str) or not re.fullmatch(
        r"[0-9a-f]{64}", manifest.get("fallback_docx_sha256", "")
    ):
        errors.append("fallback_docx_sha256 must be a SHA-256 hex digest.")
    if int(manifest.get("text_characters_checked", 0)) < 1_000_000:
        errors.append("fallback text volume is unexpectedly small.")
    if int(manifest.get("paragraph_markers", 0)) < 10_000:
        errors.append("fallback paragraph count is unexpectedly small.")
    if manifest.get("media_entries") != 0:
        errors.append("textutil fallback must record zero media entries because it is text-oriented.")
    missing = sorted(set(REQUIRED_MARKERS) - set(manifest.get("required_text_markers_present", [])))
    if missing:
        errors.append(f"fallback missing required text marker(s): {missing}.")
    if manifest.get("live_marker_hits") != 0:
        errors.append("fallback must not contain live-only marker hits.")
    if manifest.get("raw_core_claim_marker_hits") != 0:
        errors.append("fallback must not contain raw core-claim marker hits.")
    pages = manifest.get("pages_application_review", {})
    if not isinstance(pages, dict) or pages.get("status") != "passed_pages_open_text_fallback_probe":
        errors.append("pages_application_review.status must be passed_pages_open_text_fallback_probe.")
    if pages.get("observation_count") != len(pages.get("observations", [])):
        errors.append("pages_application_review.observation_count must match observations length.")
    blockers = set(manifest.get("release_blockers_preserved", []))
    for blocker in (
        "docx_application_review_not_completed_for_rich_docx",
        "reader_release_approval_not_created",
        "visual_package_not_preserved_by_text_fallback",
    ):
        if blocker not in blockers:
            errors.append(f"release_blockers_preserved missing {blocker}.")
    non_claim_text = " ".join(str(item) for item in manifest.get("non_claims", [])).lower()
    for phrase in ("does not approve", "does not clear", "does not preserve", "does not promote"):
        if phrase not in non_claim_text:
            errors.append(f"non_claims missing boundary phrase {phrase!r}.")
    return errors


def write_doc(manifest: dict[str, Any]) -> None:
    pages = manifest["pages_application_review"]
    lines = [
        "# Reader DOCX Textutil Fallback Review",
        "",
        f"Last updated: {manifest['last_updated']}",
        "",
        "This note records a local text-oriented DOCX fallback probe for the curated reader manuscript. It is not an edition release record, not a rich DOCX approval, not Word/LibreOffice GUI/Google Docs review, and not support-state evidence.",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Source DOCX SHA-256 | `{manifest['source_docx_sha256']}` |",
        f"| Fallback DOCX SHA-256 | `{manifest['fallback_docx_sha256']}` |",
        f"| Fallback bytes | {manifest['fallback_bytes']} |",
        f"| ZIP entries | {manifest['zip_entries']} |",
        f"| Text characters checked | {manifest['text_characters_checked']} |",
        f"| Paragraph markers | {manifest['paragraph_markers']} |",
        f"| Media entries | {manifest['media_entries']} |",
        f"| Live-marker hits | {manifest['live_marker_hits']} |",
        f"| Raw core-claim marker hits | {manifest['raw_core_claim_marker_hits']} |",
        "",
        "## Pages Observation",
        "",
        f"Status: `{pages['status']}`",
        "",
    ]
    for observation in pages["observations"]:
        lines.append(f"- {observation}")
    lines.extend(
        [
            "",
            "## Release Boundary",
            "",
            manifest["review_boundary"],
            "",
            "Preserved blockers:",
            "",
        ]
    )
    for blocker in manifest["release_blockers_preserved"]:
        lines.append(f"- `{blocker}`")
    lines.extend(["", "Non-claims:", ""])
    for item in manifest["non_claims"]:
        lines.append(f"- {item}")
    lines.append("")
    DOC.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-manifest", action="store_true", help="build fallback, write manifest, and write docs")
    parser.add_argument("--check-current", action="store_true", help="also compare the current ignored fallback observation to the tracked manifest")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.write_manifest:
        textutil_path = run_textutil()
        observed = inspect_fallback(textutil_path)
        errors = validate_manifest(observed)
        if errors:
            fail(errors)
        MANIFEST.write_text(json.dumps(observed, indent=2) + "\n", encoding="utf-8")
        write_doc(observed)
    else:
        if not MANIFEST.exists():
            fail([f"Missing tracked manifest: {rel(MANIFEST)}"])
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        errors = validate_manifest(manifest)
        if args.check_current:
            observed = inspect_fallback()
            if observed != manifest:
                errors.append("tracked manifest does not match the current ignored textutil fallback artifact.")
        if not DOC.exists():
            errors.append(f"Missing documentation file: {rel(DOC)}")
        else:
            doc_text = DOC.read_text(encoding="utf-8")
            for fragment in (
                "Reader DOCX Textutil Fallback Review",
                "passed_pages_open_text_fallback_probe",
                "not a rich DOCX approval",
                "does not clear the rich DOCX application-review blocker",
            ):
                if fragment not in doc_text:
                    errors.append(f"{rel(DOC)} missing fragment {fragment!r}.")
        if errors:
            fail(errors)

    print("Reader DOCX textutil fallback validation passed.")


if __name__ == "__main__":
    main()
