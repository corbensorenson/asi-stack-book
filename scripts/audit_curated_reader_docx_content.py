#!/usr/bin/env python3
"""Audit curated-reader DOCX package content without approving release."""

from __future__ import annotations

import argparse
import hashlib
import json
import posixpath
import re
import sys
from pathlib import Path
from typing import Any
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "editions" / "reader_manuscript" / "v1_0" / "curated_format_probe_manifest.json"
DOCX = ROOT / "build" / "curated_reader_edition" / "format_artifacts" / "docx" / "_reader_site" / "The-ASI-Stack.docx"
DOCUMENT_XML = "word/document.xml"
DOCUMENT_RELS = "word/_rels/document.xml.rels"
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
REL_RE = re.compile(r"""<Relationship\b([^>]*)/>""")
ATTR_RE = re.compile(r"""([A-Za-z_:]+)=["']([^"']*)["']""")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Curated reader DOCX content audit failed:")
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


def strip_xml_tags(text: str) -> str:
    return re.sub(r"<[^>]+>", " ", text)


def relationship_attrs(rels_xml: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for match in REL_RE.finditer(rels_xml):
        rows.append(dict(ATTR_RE.findall(match.group(1))))
    return rows


def internal_target_exists(names: set[str], source_entry: str, target: str) -> bool:
    base_dir = posixpath.dirname(posixpath.dirname(source_entry))
    candidate = posixpath.normpath(posixpath.join(base_dir, target))
    return candidate in names


def observe() -> dict[str, Any]:
    if not DOCX.exists():
        fail([f"Missing DOCX artifact: {rel(DOCX)}. Run `python3 scripts/render_curated_reader_formats.py --formats docx` first."])

    with ZipFile(DOCX) as archive:
        names = archive.namelist()
        name_set = set(names)
        for required in ("[Content_Types].xml", "_rels/.rels", DOCUMENT_XML, DOCUMENT_RELS, "word/styles.xml"):
            if required not in name_set:
                fail([f"DOCX package missing required entry: {required}"])

        document_xml = archive.read(DOCUMENT_XML).decode("utf-8", errors="replace")
        rels_xml = archive.read(DOCUMENT_RELS).decode("utf-8", errors="replace")
        text = strip_xml_tags(document_xml)
        relationships = relationship_attrs(rels_xml)
        media_entries = sorted(name for name in names if name.startswith("word/media/"))
        png_entries = [name for name in media_entries if name.lower().endswith(".png")]
        svg_entries = [name for name in media_entries if name.lower().endswith(".svg")]

        external_hyperlinks = 0
        image_relationships = 0
        raw_qmd_targets: list[str] = []
        unresolved_internal_targets: list[str] = []
        for row in relationships:
            target = row.get("Target", "")
            rel_type = row.get("Type", "")
            if target.endswith(".qmd") or ".qmd#" in target:
                raw_qmd_targets.append(f"{row.get('Id', '')}: {target}")
            if rel_type.endswith("/image"):
                image_relationships += 1
            if rel_type.endswith("/hyperlink") and row.get("TargetMode") == "External":
                external_hyperlinks += 1
                continue
            if row.get("TargetMode") == "External" or not target:
                continue
            if not internal_target_exists(name_set, DOCUMENT_RELS, target):
                unresolved_internal_targets.append(f"{row.get('Id', '')}: {target}")

        required_marker_hits = {marker: marker in text for marker in REQUIRED_MARKERS}
        live_marker_hits = [marker for marker in LIVE_ONLY_MARKERS if marker in document_xml]
        raw_claim_hits = bool(RAW_CORE_CLAIM_RE.search(document_xml))

    return {
        "status": "passed_docx_document_xml_relationship_probe",
        "source_artifact": rel(DOCX),
        "source_sha256": sha256_file(DOCX),
        "zip_entries": len(names),
        "document_xml_characters": len(document_xml),
        "text_characters_checked": len(text),
        "paragraph_markers": document_xml.count("<w:p"),
        "run_markers": document_xml.count("<w:r"),
        "relationship_count": len(relationships),
        "image_relationships": image_relationships,
        "external_hyperlink_relationships": external_hyperlinks,
        "media_entries": len(media_entries),
        "png_media_entries": len(png_entries),
        "svg_media_entries": len(svg_entries),
        "raw_qmd_relationship_targets": len(raw_qmd_targets),
        "unresolved_internal_relationship_targets": len(unresolved_internal_targets),
        "live_marker_hits": len(live_marker_hits),
        "raw_core_claim_marker_hits": int(raw_claim_hits),
        "required_text_markers_present": [
            marker for marker, present in required_marker_hits.items() if present
        ],
        "review_boundary": (
            "DOCX document XML, media, and relationship checks are stronger local DOCX evidence than "
            "package inspection alone, but this is not Word, LibreOffice GUI, or Google Docs application "
            "review and does not approve the DOCX artifact for release."
        ),
    }


def validate_observed(observed: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    expected_exact = {
        "zip_entries": 77,
        "paragraph_markers": 17360,
        "media_entries": 61,
        "png_media_entries": 61,
        "svg_media_entries": 0,
        "raw_qmd_relationship_targets": 0,
        "unresolved_internal_relationship_targets": 0,
        "live_marker_hits": 0,
        "raw_core_claim_marker_hits": 0,
    }
    for key, value in expected_exact.items():
        if observed.get(key) != value:
            errors.append(f"DOCX audit expected {key}={value}, found {observed.get(key)}.")
    if observed["text_characters_checked"] < 1_000_000:
        errors.append("DOCX audit text volume is unexpectedly small.")
    if observed["relationship_count"] < 250:
        errors.append("DOCX audit relationship count is unexpectedly small.")
    if observed["image_relationships"] != 61:
        errors.append("DOCX audit expected 61 image relationships.")
    missing = sorted(set(REQUIRED_MARKERS) - set(observed["required_text_markers_present"]))
    if missing:
        errors.append(f"DOCX audit missing required marker(s): {missing}.")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-manifest", action="store_true", help="write observed DOCX audit into the curated format probe manifest")
    args = parser.parse_args()

    manifest = load_manifest()
    observed = observe()
    errors = validate_observed(observed)
    if errors:
        fail(errors)

    if args.write_manifest:
        manifest["docx_content_audit"] = observed
        MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    else:
        recorded = manifest.get("docx_content_audit")
        if recorded != observed:
            fail(["curated_format_probe_manifest.json docx_content_audit is stale; run `python3 scripts/audit_curated_reader_docx_content.py --write-manifest`."])

    print(
        "Curated reader DOCX content audit passed: "
        f"{observed['paragraph_markers']} paragraphs, "
        f"{observed['relationship_count']} relationships, "
        f"{observed['raw_qmd_relationship_targets']} raw .qmd relationship targets."
    )


if __name__ == "__main__":
    main()
