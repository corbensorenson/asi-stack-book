#!/usr/bin/env python3
"""Reject stale, inflated, or artifact-divergent P8 reader freeze claims."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
import zipfile
from pathlib import Path

from jsonschema import Draft202012Validator
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
FREEZE_PATH = ROOT / "editions/reader_manuscript/v2_2/evidence_freeze.json"
MATRIX_PATH = ROOT / "editions/reader_manuscript/v2_2/format_review_matrix.json"
RELEASE_PATH = ROOT / "editions/reader_manuscript/v2_2/release_disposition.json"
SCHEMA_PATH = ROOT / "schemas/p8_reader_evidence_freeze.schema.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def tree_digest(records: list[dict]) -> str:
    payload = "".join(f"{r['sha256']}  {r['path']}\n" for r in records)
    return hashlib.sha256(payload.encode()).hexdigest()


def semantic_errors(freeze: dict) -> list[str]:
    errors: list[str] = []
    schema = load(SCHEMA_PATH)
    for error in sorted(Draft202012Validator(schema).iter_errors(freeze), key=lambda e: list(e.path)):
        errors.append(f"schema:{'.'.join(map(str, error.path))}: {error.message}")

    source_root = ROOT / freeze.get("source", {}).get("path", "missing")
    records = freeze.get("source", {}).get("files", [])
    if len(records) != freeze.get("source", {}).get("file_count"):
        errors.append("source file_count does not equal the digest record count")
    seen = set()
    for record in records:
        rel = record.get("path", "")
        if rel in seen:
            errors.append(f"duplicate source record: {rel}")
        seen.add(rel)
        path = source_root / rel
        if not path.is_file():
            errors.append(f"missing frozen source: {rel}")
            continue
        if path.stat().st_size != record.get("bytes") or digest(path) != record.get("sha256"):
            errors.append(f"frozen source digest mismatch: {rel}")
    if records and tree_digest(records) != freeze.get("source", {}).get("tree_sha256"):
        errors.append("source tree digest mismatch")
    chapter_files = list((source_root / "chapters").glob("*.qmd")) if source_root.exists() else []
    if len(chapter_files) != 55:
        errors.append(f"frozen chapter count must be 55; found {len(chapter_files)}")

    for name, record in freeze.get("artifacts", {}).items():
        path = ROOT / record.get("path", "missing")
        if not path.is_file():
            errors.append(f"missing {name} artifact")
        elif path.stat().st_size != record.get("bytes") or digest(path) != record.get("sha256"):
            errors.append(f"{name} artifact digest mismatch")
    for name, record in freeze.get("evidence_reports", {}).items():
        path = ROOT / record.get("path", "missing")
        if not path.is_file() or digest(path) != record.get("sha256"):
            errors.append(f"{name} evidence report missing or digest-divergent")

    matrix = load(MATRIX_PATH)
    release = load(RELEASE_PATH)
    fmts = matrix.get("formats", {})
    expected_states = {
        "html": "approved_exact_local_artifact_not_published",
        "epub": "bounded_local_application_inspection_not_release_approved",
        "docx": "built_and_fully_raster_inspected_with_layout_residual_not_release_approved",
        "pdf": "built_but_layout_failed_not_release_approved",
    }
    for name, state in expected_states.items():
        if fmts.get(name, {}).get("state") != state:
            errors.append(f"{name} disposition must remain {state}")

    html = fmts.get("html", {}).get("inspection", {})
    exact_html = {
        "html_pages": 60,
        "chapter_entry_pages": 55,
        "browser_page_view_pairs": 120,
        "browser_failures": 0,
        "accessibility_tree_page_view_pairs": 120,
        "accessibility_tree_failures": 0,
        "keyboard_page_view_pairs": 120,
        "keyboard_trap_candidates": 0,
        "wcag_preparation_page_view_pairs": 120,
        "contrast_failure_samples": 0,
    }
    for key, value in exact_html.items():
        if html.get(key) != value:
            errors.append(f"HTML {key} must be {value}; found {html.get(key)}")
    if float(html.get("minimum_contrast_ratio", 0)) < 4.5:
        errors.append("HTML minimum contrast ratio fell below 4.5")

    epub = fmts.get("epub", {})
    if epub.get("structural_inspection", {}).get("xhtml_entry_count") != 63:
        errors.append("EPUB XHTML entry count must be 63")
    epub_path = ROOT / freeze.get("artifacts", {}).get("epub", {}).get("path", "missing")
    if epub_path.is_file():
        with zipfile.ZipFile(epub_path) as zf:
            if zf.testzip() is not None or not zf.namelist() or zf.namelist()[0] != "mimetype":
                errors.append("EPUB container integrity/mimetype contract failed")

    docx = fmts.get("docx", {})
    if docx.get("structural_inspection", {}).get("media_entry_count") != 81:
        errors.append("DOCX media entry count must be 81")
    dr = docx.get("raster_inspection", {})
    if dr.get("pages") != 726 or dr.get("blank_pages") != [] or dr.get("outer_edge_ink_pages") != [] or dr.get("low_ink_pages") != [6]:
        errors.append("DOCX raster evidence changed or residual was suppressed")
    if "Page 6" not in docx.get("residual", ""):
        errors.append("DOCX page-6 layout residual is missing")

    pdf = fmts.get("pdf", {})
    pr = pdf.get("raster_inspection", {})
    if pdf.get("structural_inspection", {}).get("pages") != 912 or pdf.get("structural_inspection", {}).get("tagged_pdf") is not False:
        errors.append("PDF must remain 912-page and explicitly untagged")
    if pr.get("blank_pages") != [47, 697] or len(pr.get("outer_edge_ink_pages", [])) != 72:
        errors.append("PDF raster failures changed or were suppressed")
    confirmed = " ".join(pr.get("confirmed_layout_failures", []))
    if "Page 48" not in confirmed or "Page 50" not in confirmed:
        errors.append("PDF confirmed page-48/page-50 layout failures are missing")
    pdf_path = ROOT / freeze.get("artifacts", {}).get("pdf", {}).get("path", "missing")
    if pdf_path.is_file() and len(PdfReader(str(pdf_path)).pages) != 912:
        errors.append("PDF artifact does not parse as 912 pages")

    if release.get("decision") != "evidence_freeze_ready_not_published_multiformat_release_not_approved":
        errors.append("release decision was inflated")
    if release.get("rights", {}).get("public_license_grant") is not False:
        errors.append("freeze must not invent a public license grant")
    for key in ("living_book_public_release", "public_reader_release", "doi_archive", "deployment", "push_tag_commit"):
        if any(word in str(release.get(key, "")) for word in ("published", "deployed", "approved", "completed")) and key != "public_reader_release":
            errors.append(f"unauthorized external state claimed in {key}")
    if release.get("public_reader_release") != "not_approved_not_published":
        errors.append("public reader release must remain not approved/not published")
    if freeze.get("support_state_effect") != "none" or matrix.get("support_state_effect") != "none" or release.get("support_state_effect") != "none":
        errors.append("reader work cannot change claim support state")
    return errors


def mutation_rejections(freeze: dict) -> tuple[int, list[str]]:
    mutations = []
    def add(label, fn):
        candidate = copy.deepcopy(freeze); fn(candidate); mutations.append((label, candidate))
    add("chapter_count_inflated", lambda d: d["source"].__setitem__("chapter_count", 56))
    add("html_page_count_stale", lambda d: d["html_site"].__setitem__("html_page_count", 59))
    add("source_tree_digest_changed", lambda d: d["source"].__setitem__("tree_sha256", "0" * 64))
    add("epub_digest_changed", lambda d: d["artifacts"]["epub"].__setitem__("sha256", "0" * 64))
    add("support_inflated", lambda d: d.__setitem__("support_state_effect", "promotion"))
    add("status_published", lambda d: d.__setitem__("status", "published"))
    add("report_digest_changed", lambda d: d["evidence_reports"]["html_browser"].__setitem__("sha256", "f" * 64))
    rejected, escaped = 0, []
    for label, candidate in mutations:
        if semantic_errors(candidate):
            rejected += 1
        else:
            escaped.append(label)
    return rejected, escaped


def main() -> int:
    freeze = load(FREEZE_PATH)
    errors = semantic_errors(freeze)
    rejected, escaped = mutation_rejections(freeze)
    if rejected != 7:
        errors.append(f"mutation rejection count must be 7; found {rejected}; escaped={escaped}")
    if errors:
        print("P8 reader evidence-freeze validation failed:", file=sys.stderr)
        for error in errors:
            print(f" - {error}", file=sys.stderr)
        return 1
    print("P8 reader evidence freeze passed: 55 chapters, 60 HTML pages, four digest-bound formats, 7/7 mutations rejected; only HTML is locally approved and nothing was published.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
