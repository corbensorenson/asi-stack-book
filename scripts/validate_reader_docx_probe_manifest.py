#!/usr/bin/env python3
"""Validate the tracked reader DOCX conversion probe manifest and summary."""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "editions" / "reader_manuscript" / "v1_0" / "docx_probe_manifest.json"
SUMMARY = ROOT / "docs" / "reader_docx_probe_manifest.md"
REQUIRED_COMMAND_FRAGMENTS = (
    "python3 scripts/render_reader_formats.py --formats html epub docx",
    "python3 scripts/inspect_reader_format_artifacts.py",
    "render_docx.py build/reader_edition/format_artifacts/docx/_reader_site/The-ASI-Stack.docx --output_dir build/reader_docx_probe --emit_pdf",
    "pdfinfo build/reader_docx_probe/The-ASI-Stack.pdf",
)
REQUIRED_BLOCKERS = {
    "reader_release_record_not_created",
    "full_format_artifact_review_not_completed",
}
SAMPLED_PAGES = [1, 25, 447, 472, 474, 514]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Reader DOCX probe manifest validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def require_string(owner: str, key: str, value: Any, errors: list[str], *, min_words: int = 1) -> str:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{owner}: {key} must be a non-empty string.")
        return ""
    if len(value.split()) < min_words:
        errors.append(f"{owner}: {key} must contain at least {min_words} words.")
    return value


def require_string_list(owner: str, key: str, value: Any, errors: list[str]) -> list[str]:
    if not isinstance(value, list) or not value:
        errors.append(f"{owner}: {key} must be a non-empty list.")
        return []
    result: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            errors.append(f"{owner}: {key} entries must be non-empty strings.")
        else:
            result.append(item)
    return result


def require_int(owner: str, key: str, value: Any, errors: list[str], *, minimum: int = 0) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        errors.append(f"{owner}: {key} must be an integer.")
        return 0
    if value < minimum:
        errors.append(f"{owner}: {key} must be at least {minimum}.")
    return value


def validate_ref(owner: str, ref: str, errors: list[str], *, tracked_only: bool = True) -> None:
    path_part = ref.split("#", 1)[0]
    if not path_part:
        errors.append(f"{owner}: ref must include a path before any anchor: {ref!r}.")
        return
    if tracked_only and not (ROOT / path_part).exists():
        errors.append(f"{owner}: referenced tracked path does not exist: {path_part}.")


def validate_manifest(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if manifest.get("schema_version") != "0.1":
        errors.append("schema_version must be 0.1.")
    if manifest.get("major_version") != "v1.0":
        errors.append("major_version must be v1.0.")
    if manifest.get("status") != "local_docx_conversion_probe_record":
        errors.append("status must be local_docx_conversion_probe_record.")
    require_string("manifest", "purpose", manifest.get("purpose"), errors, min_words=16)

    commands = require_string_list("manifest", "source_commands", manifest.get("source_commands"), errors)
    joined_commands = "\n".join(commands)
    for fragment in REQUIRED_COMMAND_FRAGMENTS:
        if fragment not in joined_commands:
            errors.append(f"source_commands missing required fragment: {fragment}")
    for ref in require_string_list("manifest", "local_artifact_refs", manifest.get("local_artifact_refs"), errors):
        if not ref.startswith("build/"):
            errors.append(f"local_artifact_refs should point to ignored build outputs: {ref}")
    for ref in require_string_list("manifest", "tracked_evidence_refs", manifest.get("tracked_evidence_refs"), errors):
        validate_ref("tracked_evidence_refs", ref, errors)

    source = manifest.get("docx_source_summary")
    if not isinstance(source, dict):
        errors.append("docx_source_summary must be an object.")
        source = {}
    if source.get("format") != "docx":
        errors.append("docx_source_summary.format must be docx.")
    if source.get("status") != "rendered_and_structurally_inspected":
        errors.append("docx_source_summary.status must be rendered_and_structurally_inspected.")
    if require_int("docx_source_summary", "file_size_bytes", source.get("file_size_bytes"), errors, minimum=1_000_000) != 7059440:
        errors.append("docx_source_summary.file_size_bytes must be 7059440.")
    if require_int("docx_source_summary", "zip_entries", source.get("zip_entries"), errors, minimum=1) != 77:
        errors.append("docx_source_summary.zip_entries must be 77.")
    if require_int("docx_source_summary", "media_entries", source.get("media_entries"), errors, minimum=1) != 61:
        errors.append("docx_source_summary.media_entries must be 61.")
    if require_int("docx_source_summary", "paragraph_markers", source.get("paragraph_markers"), errors, minimum=1000) != 19229:
        errors.append("docx_source_summary.paragraph_markers must be 19229.")

    conversion = manifest.get("conversion_summary")
    if not isinstance(conversion, dict):
        errors.append("conversion_summary must be an object.")
        conversion = {}
    if conversion.get("format") != "docx_to_pdf":
        errors.append("conversion_summary.format must be docx_to_pdf.")
    if conversion.get("status") != "converted":
        errors.append("conversion_summary.status must be converted.")
    if "LibreOffice" not in str(conversion.get("producer", "")):
        errors.append("conversion_summary.producer must identify LibreOffice.")
    if conversion.get("title") != "The ASI Stack":
        errors.append("conversion_summary.title must be The ASI Stack.")
    if conversion.get("author") != "Corben Sorenson":
        errors.append("conversion_summary.author must be Corben Sorenson.")
    if require_int("conversion_summary", "pages", conversion.get("pages"), errors, minimum=500) != 514:
        errors.append("conversion_summary.pages must be 514.")
    if require_int("conversion_summary", "file_size_bytes", conversion.get("file_size_bytes"), errors, minimum=1_000_000) != 8190127:
        errors.append("conversion_summary.file_size_bytes must be 8190127.")
    if conversion.get("encrypted") is not False:
        errors.append("conversion_summary.encrypted must be false.")
    if conversion.get("tagged") is not True:
        errors.append("conversion_summary.tagged must be true.")
    if conversion.get("page_size") != "612 x 792 pts (letter)":
        errors.append("conversion_summary.page_size must be 612 x 792 pts (letter).")

    text = manifest.get("text_extraction_summary")
    if not isinstance(text, dict):
        errors.append("text_extraction_summary must be an object.")
        text = {}
    for key in (
        "title_found",
        "reader_edition_draft_found",
        "evidence_boundary_found",
        "reader_source_list_found",
        "external_citation_policy_found",
    ):
        if text.get(key) is not True:
            errors.append(f"text_extraction_summary.{key} must be true.")
    if text.get("sampled_pages") != SAMPLED_PAGES:
        errors.append(f"text_extraction_summary.sampled_pages must be {SAMPLED_PAGES}.")

    spot = manifest.get("spot_check_summary")
    if not isinstance(spot, dict):
        errors.append("spot_check_summary must be an object.")
        spot = {}
    if spot.get("status") != "representative_libreoffice_conversion_spot_check":
        errors.append("spot_check_summary.status must be representative_libreoffice_conversion_spot_check.")
    pages = spot.get("pages_sampled")
    if not isinstance(pages, list) or len(pages) != len(SAMPLED_PAGES):
        errors.append(f"spot_check_summary.pages_sampled must contain {len(SAMPLED_PAGES)} records.")
    else:
        observed_pages = [record.get("page") for record in pages if isinstance(record, dict)]
        if observed_pages != SAMPLED_PAGES:
            errors.append(f"spot_check_summary.pages_sampled must record pages {SAMPLED_PAGES}.")
        page_text = " ".join(str(record.get("observation", "")) for record in pages if isinstance(record, dict)).lower()
        for phrase in ("reader edition draft", "source-card", "without visible table-cell overlap", "final external citation-policy"):
            if phrase not in page_text:
                errors.append(f"spot_check_summary observations must include phrase: {phrase}")
    residuals = require_string_list("spot_check_summary", "layout_residuals", spot.get("layout_residuals"), errors)
    residual_text = " ".join(residuals).lower()
    for phrase in ("not a full docx application review", "ignored local probe artifacts", "full format-artifact review"):
        if phrase not in residual_text:
            errors.append(f"layout_residuals must include phrase: {phrase}")

    blockers = set(require_string_list("manifest", "release_blockers_preserved", manifest.get("release_blockers_preserved"), errors))
    for blocker in REQUIRED_BLOCKERS:
        if blocker not in blockers:
            errors.append(f"release_blockers_preserved missing {blocker}.")
    non_claims = require_string_list("manifest", "non_claims", manifest.get("non_claims"), errors)
    non_claim_text = " ".join(non_claims).lower()
    for phrase in ("not a reader release", "does not approve", "does not check full editorial quality", "does not promote"):
        if phrase not in non_claim_text:
            errors.append(f"non_claims must include boundary phrase: {phrase}")

    return errors


def validate_summary(errors: list[str]) -> None:
    if not SUMMARY.exists():
        errors.append(f"Missing {rel(SUMMARY)}.")
        return
    text = SUMMARY.read_text(encoding="utf-8")
    required_fragments = [
        "Reader DOCX Probe Manifest",
        "render_docx.py",
        "| File size | 7,059,440 bytes |",
        "| Pages | 514 |",
        "| File size | 8,190,127 bytes |",
        "LibreOfficeDev 26.8.0.0.alpha0 (AARCH64)",
        "Reader Source List",
        "proof_carrying_circular_computation",
        "representative LibreOffice conversion",
        "reader_release_record_not_created",
        "full_format_artifact_review_not_completed",
        "This manifest is not a reader release",
        "does not promote any claim support state",
    ]
    for fragment in required_fragments:
        if fragment not in text:
            errors.append(f"{rel(SUMMARY)} missing required fragment: {fragment}")


def main() -> None:
    manifest = load_json(MANIFEST)
    if not isinstance(manifest, dict):
        fail([f"{rel(MANIFEST)} must contain an object."])
    errors = validate_manifest(manifest)
    validate_summary(errors)
    if errors:
        fail(errors)
    print("Reader DOCX probe manifest validation passed: 514-page LibreOffice conversion probe recorded.")


if __name__ == "__main__":
    main()
