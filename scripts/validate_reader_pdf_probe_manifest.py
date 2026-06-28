#!/usr/bin/env python3
"""Validate the tracked reader PDF probe manifest and summary."""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "editions" / "reader_manuscript" / "v1_0" / "pdf_probe_manifest.json"
SUMMARY = ROOT / "docs" / "reader_pdf_probe_manifest.md"
REQUIRED_COMMAND = (
    "LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 python3 scripts/render_reader_formats.py "
    "--output build/reader_edition_pdf_probe_utf8 --formats pdf"
)
REQUIRED_BLOCKERS = {
    "reader_release_record_not_created",
    "full_format_artifact_review_not_completed",
    "full_pdf_layout_review_not_completed",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Reader PDF probe manifest validation failed:")
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
    if manifest.get("status") != "local_pdf_probe_record":
        errors.append("status must be local_pdf_probe_record.")
    require_string("manifest", "purpose", manifest.get("purpose"), errors, min_words=14)

    commands = set(require_string_list("manifest", "source_commands", manifest.get("source_commands"), errors))
    if REQUIRED_COMMAND not in commands:
        errors.append(f"source_commands missing required command: {REQUIRED_COMMAND}")
    for expected in ("pdfinfo ", "pdftotext ", "pdftoppm "):
        if not any(command.startswith(expected) for command in commands):
            errors.append(f"source_commands missing {expected.strip()} inspection command.")

    for ref in require_string_list("manifest", "local_artifact_refs", manifest.get("local_artifact_refs"), errors):
        if not ref.startswith("build/"):
            errors.append(f"local_artifact_refs should point to ignored build outputs: {ref}")

    for ref in require_string_list("manifest", "tracked_evidence_refs", manifest.get("tracked_evidence_refs"), errors):
        validate_ref("tracked_evidence_refs", ref, errors)

    render = manifest.get("render_summary")
    if not isinstance(render, dict):
        errors.append("render_summary must be an object.")
        render = {}
    if render.get("format") != "pdf":
        errors.append("render_summary.format must be pdf.")
    if render.get("status") != "rendered":
        errors.append("render_summary.status must be rendered.")
    if render.get("reader_render_command") != REQUIRED_COMMAND:
        errors.append("render_summary.reader_render_command must match the required UTF-8 command.")
    require_string("render_summary", "local_artifact_path", render.get("local_artifact_path"), errors)

    pdfinfo = manifest.get("pdfinfo_summary")
    if not isinstance(pdfinfo, dict):
        errors.append("pdfinfo_summary must be an object.")
        pdfinfo = {}
    if pdfinfo.get("title") != "The ASI Stack":
        errors.append("pdfinfo_summary.title must be The ASI Stack.")
    if pdfinfo.get("author") != "Corben Sorenson":
        errors.append("pdfinfo_summary.author must be Corben Sorenson.")
    if pdfinfo.get("producer") != "LuaTeX-1.24.0":
        errors.append("pdfinfo_summary.producer must be LuaTeX-1.24.0.")
    if require_int("pdfinfo_summary", "pages", pdfinfo.get("pages"), errors, minimum=500) != 535:
        errors.append("pdfinfo_summary.pages must be the current recorded probe count: 535.")
    if require_int("pdfinfo_summary", "file_size_bytes", pdfinfo.get("file_size_bytes"), errors, minimum=1_000_000) != 8613924:
        errors.append("pdfinfo_summary.file_size_bytes must be the current recorded probe size: 8613924.")
    if pdfinfo.get("encrypted") is not False:
        errors.append("pdfinfo_summary.encrypted must be false.")
    if pdfinfo.get("page_size") != "612 x 792 pts (letter)":
        errors.append("pdfinfo_summary.page_size must be 612 x 792 pts (letter).")

    text = manifest.get("text_extraction_summary")
    if not isinstance(text, dict):
        errors.append("text_extraction_summary must be an object.")
        text = {}
    for key in ("title_found", "reader_edition_draft_found", "evidence_boundary_found"):
        if text.get(key) is not True:
            errors.append(f"text_extraction_summary.{key} must be true.")
    sampled_pages = text.get("sampled_pages")
    if sampled_pages != [1, 21, 25, 474, 497, 499, 535]:
        errors.append("text_extraction_summary.sampled_pages must be [1, 21, 25, 474, 497, 499, 535].")

    spot = manifest.get("spot_check_summary")
    if not isinstance(spot, dict):
        errors.append("spot_check_summary must be an object.")
        spot = {}
    if spot.get("status") != "representative_spot_check_with_residual":
        errors.append("spot_check_summary.status must be representative_spot_check_with_residual.")
    pages = spot.get("pages_sampled")
    if not isinstance(pages, list) or len(pages) != 7:
        errors.append("spot_check_summary.pages_sampled must contain exactly seven records.")
    else:
        observed_pages = [record.get("page") for record in pages if isinstance(record, dict)]
        if observed_pages != [1, 21, 25, 474, 497, 499, 535]:
            errors.append("spot_check_summary.pages_sampled must record pages 1, 21, 25, 474, 497, 499, and 535 in order.")
        page_text = " ".join(
            str(record.get("observation", "")) for record in pages if isinstance(record, dict)
        ).lower()
        for phrase in ("source-card", "without visible table-cell overlap"):
            if phrase not in page_text:
                errors.append(f"spot_check_summary must record source-card inspection phrase: {phrase}")

    residuals = require_string_list("spot_check_summary", "layout_residuals", spot.get("layout_residuals"), errors)
    residual_text = " ".join(residuals).lower()
    for phrase in ("source cards", "full page-by-page pdf layout review", "ignored local probe artifact"):
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
        "Reader PDF Probe Manifest",
        REQUIRED_COMMAND,
        "| Pages | 535 |",
        "| File size | 8,613,924 bytes |",
        "| Producer | LuaTeX-1.24.0 |",
        "evidence boundary: architectural argument",
        "source cards",
        "Full page-by-page PDF layout review has not been completed",
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
    print("Reader PDF probe manifest validation passed: 535-page UTF-8 PDF probe recorded with source-card residuals.")


if __name__ == "__main__":
    main()
