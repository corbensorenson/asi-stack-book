#!/usr/bin/env python3
"""Validate the tracked reader EPUB probe manifest and summary."""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "editions" / "reader_manuscript" / "v1_0" / "epub_probe_manifest.json"
SUMMARY = ROOT / "docs" / "reader_epub_probe_manifest.md"
REQUIRED_COMMAND_FRAGMENTS = (
    "python3 scripts/render_reader_formats.py --formats html epub docx",
    "python3 scripts/inspect_reader_format_artifacts.py",
    "inspect EPUB/content.opf, EPUB/nav.xhtml",
)
REQUIRED_BLOCKERS = {
    "reader_release_record_not_created",
    "full_format_artifact_review_not_completed",
    "app_or_ereader_review_not_completed",
}
SAMPLED_ENTRIES = [
    "EPUB/text/ch001.xhtml",
    "EPUB/text/ch003.xhtml",
    "EPUB/text/ch058.xhtml",
    "EPUB/text/ch059.xhtml",
]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Reader EPUB probe manifest validation failed:")
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
    if manifest.get("status") != "local_epub_probe_record":
        errors.append("status must be local_epub_probe_record.")
    require_string("manifest", "purpose", manifest.get("purpose"), errors, min_words=16)

    commands = "\n".join(require_string_list("manifest", "source_commands", manifest.get("source_commands"), errors))
    for fragment in REQUIRED_COMMAND_FRAGMENTS:
        if fragment not in commands:
            errors.append(f"source_commands missing required fragment: {fragment}")
    for ref in require_string_list("manifest", "local_artifact_refs", manifest.get("local_artifact_refs"), errors):
        if not ref.startswith("build/"):
            errors.append(f"local_artifact_refs should point to ignored build outputs: {ref}")
    for ref in require_string_list("manifest", "tracked_evidence_refs", manifest.get("tracked_evidence_refs"), errors):
        validate_ref("tracked_evidence_refs", ref, errors)

    container = manifest.get("epub_container_summary")
    if not isinstance(container, dict):
        errors.append("epub_container_summary must be an object.")
        container = {}
    if container.get("format") != "epub":
        errors.append("epub_container_summary.format must be epub.")
    if container.get("status") != "rendered_and_structurally_inspected":
        errors.append("epub_container_summary.status must be rendered_and_structurally_inspected.")
    if require_int("epub_container_summary", "file_size_bytes", container.get("file_size_bytes"), errors, minimum=1_000_000) != 9078787:
        errors.append("epub_container_summary.file_size_bytes must be 9078787.")
    expected_counts = {
        "zip_entries": 130,
        "xhtml_entries": 62,
        "text_xhtml_entries": 61,
        "image_entries": 62,
        "opf_item_count": 126,
        "opf_itemref_count": 62,
        "nav_href_count": 866,
        "nav_li_count": 866,
    }
    for key, expected in expected_counts.items():
        if require_int("epub_container_summary", key, container.get(key), errors, minimum=1) != expected:
            errors.append(f"epub_container_summary.{key} must be {expected}.")
    if container.get("mimetype_first") is not True:
        errors.append("epub_container_summary.mimetype_first must be true.")
    if container.get("mimetype_content") != "application/epub+zip":
        errors.append("epub_container_summary.mimetype_content must be application/epub+zip.")
    required_entries = set(
        require_string_list(
            "epub_container_summary",
            "required_entries_present",
            container.get("required_entries_present"),
            errors,
        )
    )
    for entry in {
        "mimetype",
        "META-INF/container.xml",
        "EPUB/content.opf",
        "EPUB/nav.xhtml",
        "EPUB/toc.ncx",
        "EPUB/text/title_page.xhtml",
    }:
        if entry not in required_entries:
            errors.append(f"epub_container_summary.required_entries_present missing {entry}.")

    metadata = manifest.get("metadata_summary")
    if not isinstance(metadata, dict):
        errors.append("metadata_summary must be an object.")
        metadata = {}
    if metadata.get("title") != "The ASI Stack":
        errors.append("metadata_summary.title must be The ASI Stack.")
    if metadata.get("creator") != "Corben Sorenson":
        errors.append("metadata_summary.creator must be Corben Sorenson.")
    if metadata.get("language") != "en-US":
        errors.append("metadata_summary.language must be en-US.")
    if "lang: en-US" not in str(metadata.get("language_source", "")):
        errors.append("metadata_summary.language_source must mention lang: en-US.")
    if metadata.get("cover_image_present") is not True:
        errors.append("metadata_summary.cover_image_present must be true.")

    spine = manifest.get("spine_sampling_summary")
    if not isinstance(spine, dict):
        errors.append("spine_sampling_summary must be an object.")
        spine = {}
    if spine.get("status") != "metadata_navigation_and_source_spine_sampled":
        errors.append("spine_sampling_summary.status must be metadata_navigation_and_source_spine_sampled.")
    entries = spine.get("sampled_entries")
    if not isinstance(entries, list) or len(entries) != len(SAMPLED_ENTRIES):
        errors.append(f"spine_sampling_summary.sampled_entries must contain {len(SAMPLED_ENTRIES)} records.")
    else:
        observed = [entry.get("entry") for entry in entries if isinstance(entry, dict)]
        if observed != SAMPLED_ENTRIES:
            errors.append(f"spine_sampling_summary.sampled_entries must record {SAMPLED_ENTRIES}.")
        text = " ".join(str(entry.get("observation", "")) for entry in entries if isinstance(entry, dict)).lower()
        for phrase in ("reader edition note", "evidence-boundary", "proof_carrying_circular_computation", "external citation policy", "concrete_ai_safety"):
            if phrase not in text:
                errors.append(f"spine_sampling_summary observations must include phrase: {phrase}")
    residuals = require_string_list("spine_sampling_summary", "residuals", spine.get("residuals"), errors)
    residual_text = " ".join(residuals).lower()
    for phrase in ("not been opened", "physical e-reader", "release-record approval"):
        if phrase not in residual_text:
            errors.append(f"spine_sampling_summary.residuals must include phrase: {phrase}")

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
        "Reader EPUB Probe Manifest",
        "python3 scripts/render_reader_formats.py --formats html epub docx",
        "| File size | 9,078,787 bytes |",
        "| Language | en-US |",
        "`lang: en-US`",
        "Reader Edition Note",
        "proof_carrying_circular_computation",
        "External Citation Policy",
        "app_or_ereader_review_not_completed",
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
    print("Reader EPUB probe manifest validation passed: en-US EPUB metadata and sampled source spine recorded.")


if __name__ == "__main__":
    main()
