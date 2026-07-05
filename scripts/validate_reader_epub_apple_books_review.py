#!/usr/bin/env python3
"""Validate the curated-reader EPUB Apple Books review record."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "editions" / "reader_manuscript" / "v1_0" / "epub_apple_books_review_manifest.json"
DOC = ROOT / "docs" / "reader_epub_apple_books_review.md"
FORMAT_PROBE = ROOT / "editions" / "reader_manuscript" / "v1_0" / "curated_format_probe_manifest.json"
EPUB = ROOT / "build" / "curated_reader_edition" / "format_artifacts" / "epub" / "_reader_site" / "The-ASI-Stack.epub"

EXPECTED_STATUS = "passed_apple_books_epub_application_review"
EXPECTED_DIGEST = "bca694bc97bdfbc1757d58368df9d5d3f2e6152615938a80c7eab0b2a5519255"
EXPECTED_OBSERVATIONS = {
    "library_opened",
    "chapter_render_without_xml_error",
    "page_advance_to_figure",
    "table_of_contents_opened",
}
EXPECTED_CLEARED = ["app_or_ereader_review_not_completed"]
EXPECTED_PRESERVED = [
    "reader_release_approval_not_created",
    "reader_release_record_not_created",
    "audio_files_not_generated",
    "audio_edition_release_record_not_created",
]


def fail(errors: list[str]) -> None:
    print("Reader EPUB Apple Books review validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_string(owner: str, key: str, value: Any, errors: list[str], *, min_words: int = 1) -> str:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{owner}.{key} must be a non-empty string.")
        return ""
    if len(value.split()) < min_words:
        errors.append(f"{owner}.{key} must contain at least {min_words} words.")
    return value


def require_string_list(owner: str, key: str, value: Any, errors: list[str]) -> list[str]:
    if not isinstance(value, list) or not value:
        errors.append(f"{owner}.{key} must be a non-empty list.")
        return []
    result: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            errors.append(f"{owner}.{key} entries must be non-empty strings.")
        else:
            result.append(item)
    return result


def validate() -> list[str]:
    errors: list[str] = []
    for path in (MANIFEST, DOC, FORMAT_PROBE):
        if not path.exists():
            errors.append(f"required path missing: {rel(path)}")
    if errors:
        return errors

    manifest = load_json(MANIFEST)
    format_probe = load_json(FORMAT_PROBE)
    doc = DOC.read_text(encoding="utf-8")
    if not isinstance(manifest, dict):
        return [f"{rel(MANIFEST)} must contain a JSON object."]
    if not isinstance(format_probe, dict):
        return [f"{rel(FORMAT_PROBE)} must contain a JSON object."]

    if manifest.get("schema_version") != "asi_stack.reader_epub_apple_books_review.v0":
        errors.append("schema_version must be asi_stack.reader_epub_apple_books_review.v0.")
    if manifest.get("status") != EXPECTED_STATUS:
        errors.append(f"status must be {EXPECTED_STATUS}.")
    if manifest.get("source_artifact") != rel(EPUB):
        errors.append("source_artifact must point to the curated reader EPUB artifact.")
    if manifest.get("source_sha256") != EXPECTED_DIGEST:
        errors.append(f"source_sha256 must be {EXPECTED_DIGEST}.")
    if EPUB.exists() and sha256_file(EPUB) != EXPECTED_DIGEST:
        errors.append(f"local EPUB artifact digest does not match {EXPECTED_DIGEST}.")

    epub_content = format_probe.get("epub_content_audit", {})
    epub_browser = format_probe.get("epub_browser_review", {})
    if not isinstance(epub_content, dict):
        errors.append("format probe epub_content_audit must be an object.")
        epub_content = {}
    if not isinstance(epub_browser, dict):
        errors.append("format probe epub_browser_review must be an object.")
        epub_browser = {}
    if epub_content.get("source_sha256") != EXPECTED_DIGEST:
        errors.append("epub_content_audit.source_sha256 must match the Apple Books-reviewed EPUB digest.")
    if epub_browser.get("source_sha256") != EXPECTED_DIGEST:
        errors.append("epub_browser_review.source_sha256 must match the Apple Books-reviewed EPUB digest.")
    if epub_content.get("xml_parse_errors") != 0:
        errors.append("epub_content_audit.xml_parse_errors must be 0.")
    if epub_content.get("bare_class_attribute_hits") != 0:
        errors.append("epub_content_audit.bare_class_attribute_hits must be 0.")
    if epub_content.get("figure_paragraph_wrapper_hits") != 0:
        errors.append("epub_content_audit.figure_paragraph_wrapper_hits must be 0.")
    if epub_browser.get("status") != "passed_browser_xhtml_application_review":
        errors.append("epub_browser_review.status must be passed_browser_xhtml_application_review.")
    if epub_browser.get("failed_page_view_pairs") != 0:
        errors.append("epub_browser_review.failed_page_view_pairs must be 0.")

    app = manifest.get("application", {})
    if not isinstance(app, dict):
        errors.append("application must be an object.")
        app = {}
    if app.get("name") != "Apple Books":
        errors.append("application.name must be Apple Books.")
    if app.get("bundle_id") != "com.apple.iBooksX":
        errors.append("application.bundle_id must be com.apple.iBooksX.")
    require_string("application", "review_path", app.get("review_path"), errors, min_words=8)
    require_string("application", "stateful_side_effect", app.get("stateful_side_effect"), errors, min_words=10)

    observations = manifest.get("observations", [])
    if not isinstance(observations, list):
        errors.append("observations must be a list.")
        observations = []
    observed_ids = {row.get("id") for row in observations if isinstance(row, dict)}
    missing_observations = sorted(EXPECTED_OBSERVATIONS - observed_ids)
    if missing_observations:
        errors.append(f"observations missing required id(s): {missing_observations}.")
    for row in observations:
        if not isinstance(row, dict):
            errors.append("observation rows must be objects.")
            continue
        owner = f"observations[{row.get('id', '?')}]"
        if row.get("result") != "pass":
            errors.append(f"{owner}.result must be pass.")
        require_string(owner, "evidence", row.get("evidence"), errors, min_words=8)
        if row.get("xml_error_banner_visible") not in (False, None):
            errors.append(f"{owner}.xml_error_banner_visible must be false when present.")

    if manifest.get("cleared_blockers") != EXPECTED_CLEARED:
        errors.append(f"cleared_blockers must be {EXPECTED_CLEARED}.")
    preserved = require_string_list("manifest", "preserved_blockers", manifest.get("preserved_blockers"), errors)
    for blocker in EXPECTED_PRESERVED:
        if blocker not in preserved:
            errors.append(f"preserved_blockers missing {blocker}.")
    boundary = require_string("manifest", "release_boundary", manifest.get("release_boundary"), errors, min_words=24)
    for fragment in ("clears only", "does not approve", "does not publish", "does not promote"):
        if fragment not in boundary:
            errors.append(f"release_boundary must include {fragment!r}.")
    non_claim_text = " ".join(require_string_list("manifest", "non_claims", manifest.get("non_claims"), errors)).lower()
    for phrase in (
        "does not approve the curated reader edition",
        "does not create an edition release record",
        "does not approve audio",
        "does not promote any claim",
    ):
        if phrase not in non_claim_text:
            errors.append(f"non_claims missing boundary phrase: {phrase}")

    for fragment in (
        EXPECTED_STATUS,
        EXPECTED_DIGEST,
        "Apple Books",
        "zero XML parse errors",
        "clears only `app_or_ereader_review_not_completed`",
        "does not approve the curated reader edition",
    ):
        if fragment not in doc:
            errors.append(f"{rel(DOC)} missing required fragment: {fragment}")
    return errors


def main() -> None:
    errors = validate()
    if errors:
        fail(errors)
    print("Reader EPUB Apple Books review validation passed.")


if __name__ == "__main__":
    main()
