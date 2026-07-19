#!/usr/bin/env python3
"""Build the P8 evidence-reconciled reader freeze and terminal format records."""

from __future__ import annotations

import hashlib
import json
import shutil
import zipfile
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "editions/reader_manuscript/v2_2"
SOURCE = ROOT / "build/p8_reader_evidence_freeze"
SITE = SOURCE / "format_artifacts/html/_reader_site"
EPUB = ROOT / "build/p8_reader_epub_retry/format_artifacts/epub/_reader_site/The-ASI-Stack.epub"
DOCX = ROOT / "build/p8_reader_docx_fixed/format_artifacts/docx/_reader_site/The-ASI-Stack.docx"
PDF = ROOT / "build/p8_reader_pdf/_reader_site/The-ASI-Stack.pdf"
REPORTS = {
    "html_browser": ROOT / "build/p8_reader_html_browser_report.json",
    "html_accessibility_tree": ROOT / "build/p8_reader_html_accessibility_tree_report.json",
    "html_keyboard": ROOT / "build/p8_reader_html_keyboard_report.json",
    "html_wcag_preparation": ROOT / "build/p8_reader_html_wcag_report.json",
    "docx_raster": ROOT / "build/p8_docx_contact_sheets/raster_audit.json",
    "pdf_raster": ROOT / "build/p8_pdf_contact_sheets/raster_audit.json",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def tree_records(root: Path) -> list[dict[str, object]]:
    records = []
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        records.append({
            "path": path.relative_to(root).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        })
    return records


def tree_digest(records: list[dict[str, object]]) -> str:
    payload = "".join(f"{r['sha256']}  {r['path']}\n" for r in records)
    return hashlib.sha256(payload.encode()).hexdigest()


def copy_source() -> list[dict[str, object]]:
    dest = OUT / "source"
    if dest.exists():
        shutil.rmtree(dest)
    excluded_roots = {".quarto", "_reader_site", "format_artifacts"}
    for path in sorted(p for p in SOURCE.rglob("*") if p.is_file()):
        rel = path.relative_to(SOURCE)
        if rel.parts[0] in excluded_roots or path.name in {".DS_Store"}:
            continue
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
    return tree_records(dest)


def deterministic_zip(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path in sorted(p for p in source.rglob("*") if p.is_file()):
            rel = path.relative_to(source).as_posix()
            info = zipfile.ZipInfo(rel, (1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, path.read_bytes())


def inspect_epub(path: Path) -> dict[str, object]:
    with zipfile.ZipFile(path) as zf:
        names = zf.namelist()
        bad = zf.testzip()
        xhtml = [n for n in names if n.lower().endswith((".xhtml", ".html"))]
        images = [n for n in names if n.lower().endswith((".png", ".jpg", ".jpeg", ".svg", ".gif", ".webp"))]
        mimetype_ok = bool(names and names[0] == "mimetype" and zf.getinfo("mimetype").compress_type == zipfile.ZIP_STORED)
        return {
            "zip_integrity": bad is None,
            "mimetype_first_and_uncompressed": mimetype_ok,
            "entry_count": len(names),
            "xhtml_entry_count": len(xhtml),
            "image_entry_count": len(images),
        }


def inspect_docx(path: Path) -> dict[str, object]:
    with zipfile.ZipFile(path) as zf:
        names = zf.namelist()
        document = zf.read("word/document.xml")
        return {
            "zip_integrity": zf.testzip() is None,
            "entry_count": len(names),
            "media_entry_count": sum(n.startswith("word/media/") for n in names),
            "paragraph_marker_count": document.count(b"<w:p"),
        }


def artifact_record(path: Path, rel: str) -> dict[str, object]:
    return {"path": rel, "bytes": path.stat().st_size, "sha256": sha256(path)}


def main() -> None:
    required = [SOURCE, SITE, EPUB, DOCX, PDF, *REPORTS.values()]
    missing = [str(p.relative_to(ROOT)) for p in required if not p.exists()]
    if missing:
        raise SystemExit("Missing P8 input(s): " + ", ".join(missing))

    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "artifacts").mkdir(parents=True)
    (OUT / "evidence").mkdir(parents=True)

    source_records = copy_source()
    html_zip = OUT / "artifacts/asi-stack-reader-v2.2-html.zip"
    deterministic_zip(SITE, html_zip)
    targets = {
        "epub": OUT / "artifacts/asi-stack-reader-v2.2.epub",
        "docx": OUT / "artifacts/asi-stack-reader-v2.2.docx",
        "pdf": OUT / "artifacts/asi-stack-reader-v2.2.pdf",
    }
    for src, dst in [(EPUB, targets["epub"]), (DOCX, targets["docx"]), (PDF, targets["pdf"])]:
        shutil.copy2(src, dst)

    copied_reports = {}
    for name, src in REPORTS.items():
        dst = OUT / "evidence" / f"{name}.json"
        shutil.copy2(src, dst)
        copied_reports[name] = dst

    reader_manifest = json.loads((SOURCE / "reader_manifest.json").read_text())
    browser = json.loads(REPORTS["html_browser"].read_text())
    accessibility = json.loads(REPORTS["html_accessibility_tree"].read_text())
    keyboard = json.loads(REPORTS["html_keyboard"].read_text())
    wcag = json.loads(REPORTS["html_wcag_preparation"].read_text())
    docx_raster = json.loads(REPORTS["docx_raster"].read_text())
    pdf_raster = json.loads(REPORTS["pdf_raster"].read_text())
    html_records = tree_records(SITE)
    pdf_reader = PdfReader(str(PDF))

    artifact_records = {
        "html": artifact_record(html_zip, "editions/reader_manuscript/v2_2/artifacts/asi-stack-reader-v2.2-html.zip"),
        "epub": artifact_record(targets["epub"], "editions/reader_manuscript/v2_2/artifacts/asi-stack-reader-v2.2.epub"),
        "docx": artifact_record(targets["docx"], "editions/reader_manuscript/v2_2/artifacts/asi-stack-reader-v2.2.docx"),
        "pdf": artifact_record(targets["pdf"], "editions/reader_manuscript/v2_2/artifacts/asi-stack-reader-v2.2.pdf"),
    }

    format_matrix = {
        "schema_version": "asi_stack.p8_reader_format_review.v1",
        "edition_id": "asi-stack-reader-v2.2-evidence-freeze",
        "formats": {
            "html": {
                "state": "approved_exact_local_artifact_not_published",
                "artifact": artifact_records["html"],
                "inspection": {
                    "html_pages": len([r for r in html_records if str(r["path"]).endswith(".html")]),
                    "chapter_entry_pages": int(reader_manifest["chapters"]),
                    "browser_page_view_pairs": browser["page_view_pairs"],
                    "browser_failures": len(browser["failures"]),
                    "accessibility_tree_page_view_pairs": accessibility["summary"]["page_view_pairs"],
                    "accessibility_tree_failures": accessibility["summary"]["failed_page_view_pairs"],
                    "keyboard_page_view_pairs": keyboard["summary"]["page_view_pairs"],
                    "keyboard_trap_candidates": keyboard["summary"]["keyboard_trap_candidates"],
                    "wcag_preparation_page_view_pairs": wcag["summary"]["page_view_pairs"],
                    "contrast_failure_samples": wcag["summary"]["contrast_failure_samples"],
                    "minimum_contrast_ratio": wcag["summary"]["minimum_contrast_ratio"],
                },
                "boundary": "Automated local browser, accessibility-tree, keyboard, and WCAG-preparation evidence; not screen-reader, device, independent-human, or legal WCAG certification.",
            },
            "epub": {
                "state": "bounded_local_application_inspection_not_release_approved",
                "artifact": artifact_records["epub"],
                "structural_inspection": inspect_epub(targets["epub"]),
                "application_inspection": {
                    "application": "Apple Books",
                    "observed": ["exact artifact imported", "cover opened", "Preface text rendered", "forward navigation worked", "accessibility tree exposed heading and body text"],
                    "scope": "bounded author-run local inspection",
                },
                "boundary": "Not a complete device, assistive-technology, screen-reader, or distribution review.",
            },
            "docx": {
                "state": "built_and_fully_raster_inspected_with_layout_residual_not_release_approved",
                "artifact": artifact_records["docx"],
                "structural_inspection": inspect_docx(targets["docx"]),
                "raster_inspection": {
                    "pages": docx_raster["page_count"],
                    "contact_sheets": docx_raster["contact_sheet_count"],
                    "blank_pages": docx_raster["blank_pages"],
                    "low_ink_pages": docx_raster["low_ink_pages"],
                    "outer_edge_ink_pages": docx_raster["outer_edge_ink_pages"],
                    "all_contact_sheets_visually_inspected": True,
                },
                "residual": "Page 6 contains an awkward near-empty figure break before the following diagram.",
                "boundary": "Not inspected in Microsoft Word and not approved for public release.",
            },
            "pdf": {
                "state": "built_but_layout_failed_not_release_approved",
                "artifact": artifact_records["pdf"],
                "structural_inspection": {
                    "pages": len(pdf_reader.pages),
                    "tagged_pdf": False,
                    "parseable": True,
                },
                "raster_inspection": {
                    "pages": pdf_raster["page_count"],
                    "contact_sheets": pdf_raster["contact_sheet_count"],
                    "blank_pages": pdf_raster["blank_pages"],
                    "low_ink_pages": pdf_raster["low_ink_pages"],
                    "outer_edge_ink_pages": pdf_raster["outer_edge_ink_pages"],
                    "all_contact_sheets_visually_inspected": True,
                    "confirmed_layout_failures": [
                        "Page 48 architecture diagram is cut across the page/bottom boundary.",
                        "Page 50 diagram extends beyond the right page edge.",
                    ],
                },
                "application_inspection": {"application": "Preview", "state": "blocked", "reason": "computer-use application bridge timed out twice"},
                "boundary": "The artifact is evidence of a failed PDF attempt, not a releasable PDF.",
            },
            "audio": {"state": "not_selected_not_generated"},
            "embedded_audio": {"state": "not_selected_not_generated"},
        },
        "support_state_effect": "none",
    }
    write_json(OUT / "format_review_matrix.json", format_matrix)

    release = {
        "schema_version": "asi_stack.p8_release_disposition.v1",
        "edition_id": "asi-stack-reader-v2.2-evidence-freeze",
        "decision": "evidence_freeze_ready_not_published_multiformat_release_not_approved",
        "decision_date": "2026-07-16",
        "living_book_public_release": "not_authorized_not_attempted",
        "public_reader_release": "not_approved_not_published",
        "approved_exact_local_formats": ["html"],
        "bounded_not_release_approved_formats": ["epub", "docx"],
        "failed_formats": ["pdf"],
        "not_generated_formats": ["audio", "embedded_audio"],
        "doi_archive": "not_authorized_not_attempted",
        "deployment": "not_authorized_not_attempted",
        "push_tag_commit": "not_authorized_not_attempted",
        "rights": {
            "authority": "LICENSE.md",
            "public_license_grant": False,
            "state": "all_rights_reserved_no_new_grant",
        },
        "support_state_effect": "none",
        "non_claims": [
            "This freeze is not a public release, deployment, DOI deposit, archive deposit, tag, push, or publication.",
            "Format construction is not format approval; each format keeps its own exact disposition.",
            "Automated accessibility preparation is not screen-reader review or legal WCAG certification.",
            "This derivative is not canonical claim, proof, source, or experiment authority for the live book.",
            "No chapter-core support state is promoted by this reader work.",
        ],
    }
    write_json(OUT / "release_disposition.json", release)

    evidence = {
        "schema_version": "asi_stack.p8_reader_evidence_freeze.v1",
        "freeze_id": "asi-stack-reader-v2.2-p8-2026-07-16",
        "created": "2026-07-16",
        "status": "complete_local_evidence_freeze_ready_not_published",
        "source": {
            "path": "editions/reader_manuscript/v2_2/source",
            "chapter_count": int(reader_manifest["chapters"]),
            "file_count": len(source_records),
            "tree_sha256": tree_digest(source_records),
            "files": source_records,
        },
        "html_site": {
            "file_count": len(html_records),
            "html_page_count": len([r for r in html_records if str(r["path"]).endswith(".html")]),
            "tree_sha256": tree_digest(html_records),
        },
        "artifacts": artifact_records,
        "evidence_reports": {
            name: {"path": dst.relative_to(ROOT).as_posix(), "sha256": sha256(dst)}
            for name, dst in copied_reports.items()
        },
        "format_review_matrix": "editions/reader_manuscript/v2_2/format_review_matrix.json",
        "release_disposition": "editions/reader_manuscript/v2_2/release_disposition.json",
        "canonical_claim_authority": "live book source and claim/evidence ledgers, not this reader derivative",
        "support_state_effect": "none",
    }
    write_json(OUT / "evidence_freeze.json", evidence)

    manifest = {
        "schema_version": "asi_stack.curated_reader_manifest.v2_2",
        "edition_id": "asi-stack-reader-v2.2-evidence-freeze",
        "status": "complete_local_evidence_freeze_ready_not_published",
        "predecessor": "editions/reader_manuscript/v2_1/manifest.json",
        "source_chapter_count": int(reader_manifest["chapters"]),
        "source_file_count": len(source_records),
        "evidence_freeze": "editions/reader_manuscript/v2_2/evidence_freeze.json",
        "format_review_matrix": "editions/reader_manuscript/v2_2/format_review_matrix.json",
        "release_disposition": "editions/reader_manuscript/v2_2/release_disposition.json",
        "publication_authority": "none",
        "support_state_effect": "none",
    }
    write_json(OUT / "manifest.json", manifest)
    terminal_record = {
        "schema_version": "asi_stack.p8_terminal_release_record.v1",
        "record_type": "reader_evidence_freeze_no_public_release",
        "record_date": "2026-07-16",
        "roadmap": "docs/post_v2_3_claim_proof_and_sota_challenge_roadmap.md",
        "priority": "P8",
        "milestone": "M11",
        "decision": release["decision"],
        "manifest": {
            "path": "editions/reader_manuscript/v2_2/manifest.json",
            "sha256": sha256(OUT / "manifest.json"),
        },
        "evidence_freeze": {
            "path": "editions/reader_manuscript/v2_2/evidence_freeze.json",
            "sha256": sha256(OUT / "evidence_freeze.json"),
        },
        "format_review_matrix": {
            "path": "editions/reader_manuscript/v2_2/format_review_matrix.json",
            "sha256": sha256(OUT / "format_review_matrix.json"),
        },
        "release_disposition": {
            "path": "editions/reader_manuscript/v2_2/release_disposition.json",
            "sha256": sha256(OUT / "release_disposition.json"),
        },
        "chapter_count": 55,
        "html_page_count": 60,
        "format_states": {name: value["state"] for name, value in format_matrix["formats"].items()},
        "publication_authority": "none",
        "publication_effect": "none",
        "release_effect": "none",
        "support_state_effect": "none",
        "non_claims": release["non_claims"],
    }
    write_json(ROOT / "release_records/2026-07-16-post-v2-3-p8-evidence-freeze-ready-not-published.json", terminal_record)
    print(json.dumps({
        "edition": str(OUT.relative_to(ROOT)),
        "source_files": len(source_records),
        "chapters": reader_manifest["chapters"],
        "html_pages": evidence["html_site"]["html_page_count"],
        "artifacts": {k: v["sha256"] for k, v in artifact_records.items()},
        "decision": release["decision"],
    }, indent=2))


if __name__ == "__main__":
    main()
