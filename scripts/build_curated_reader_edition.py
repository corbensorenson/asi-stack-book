#!/usr/bin/env python3
"""Generate a Quarto workspace from the tracked curated reader manuscript.

The ordinary reader generator derives a cleaned manuscript from the live book.
This script keeps that generated workspace machinery, then replaces the chapter
body files with the tracked curated-reader manuscript drafts. The result is a
local renderable workspace for human-reader review, not a release artifact and
not a parallel authority for claims, support states, source boundaries, proof
status, implementation horizons, or release records.
"""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import shutil
import tempfile
from typing import Any

import build_reader_edition


ROOT = Path(__file__).resolve().parents[1]
STRUCTURE_PATH = ROOT / "book_structure.json"
MANIFEST_PATH = ROOT / "editions" / "reader_manuscript" / "v1_0" / "manifest.json"
DEFAULT_OUTPUT = ROOT / "build" / "curated_reader_edition"
REPORT_NAME = "curated_reader_build_report.json"
CHECKLIST_NAME = "CURATED_READER_REVIEW_CHECKLIST.md"
SOURCE_READER_ASSET_PREFIX = "../../../../assets/"
GENERATED_READER_ASSET_PREFIX = "../assets/"
GENERATED_ASSET_REF_RE = re.compile(r"\]\((\.\./assets/[^)]+)\)")
LIVE_ONLY_HEADINGS = {
    "## Chapter status",
    "## Drafting guardrail",
    "## Codex test plan",
    "## External literature queue",
    "## Source crosswalk",
    "## Claim labels",
    "## Why Codex tests matter",
    "## Formalization hooks",
    "### Claim-source mapping status",
}
REQUIRED_RELEASE_BLOCKERS = {
    "reader_release_record_not_created",
    "format_artifact_not_reviewed",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Curated reader edition build failed:")
    for error in errors:
        print(f" - {error}")
    raise SystemExit(1)


def manifest_chapters(structure: dict[str, Any]) -> list[dict[str, str]]:
    chapters: list[dict[str, str]] = []
    for part in structure.get("parts", []):
        if not isinstance(part, dict):
            continue
        for chapter in part.get("chapters", []):
            if not isinstance(chapter, dict):
                continue
            chapter_id = chapter.get("id")
            file_path = chapter.get("file")
            title = chapter.get("title")
            if isinstance(chapter_id, str) and isinstance(file_path, str) and isinstance(title, str):
                chapters.append({"chapter_id": chapter_id, "file": file_path, "title": title})
    return chapters


def historical_snapshot_ids(manifest: dict[str, Any]) -> list[str] | None:
    """Return the frozen chapter order for a historical reader candidate."""

    if manifest.get("edition_scope") != "historical_release_snapshot":
        return None
    snapshot = manifest.get("historical_spine_snapshot")
    if not isinstance(snapshot, dict):
        raise ValueError("historical reader manifest is missing historical_spine_snapshot")
    chapter_ids = snapshot.get("chapter_ids")
    if not isinstance(chapter_ids, list) or not chapter_ids or not all(
        isinstance(chapter_id, str) and chapter_id.strip() for chapter_id in chapter_ids
    ):
        raise ValueError("historical reader snapshot chapter_ids must be a non-empty string list")
    if len(chapter_ids) != len(set(chapter_ids)):
        raise ValueError("historical reader snapshot chapter_ids contains duplicates")
    expected_digest = hashlib.sha256(
        json.dumps(chapter_ids, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    ).hexdigest()
    if snapshot.get("chapter_ids_sha256") != expected_digest:
        raise ValueError("historical reader snapshot chapter_ids_sha256 does not match chapter_ids")
    return chapter_ids


def historical_snapshot_chapters(
    chapter_ids: list[str],
    records: dict[str, dict[str, Any]],
    active_chapters: list[dict[str, str]] | None = None,
) -> list[dict[str, str]]:
    """Build source-validation records from immutable reader metadata.

    Curated record paths identify tracked source. Generated workspaces retain
    the active Quarto-relative target paths while the active spine still
    exactly matches the frozen snapshot.
    """

    active_by_id = {
        chapter["chapter_id"]: chapter for chapter in active_chapters or []
    }
    chapters: list[dict[str, str]] = []
    for chapter_id in chapter_ids:
        record = records.get(chapter_id)
        if not isinstance(record, dict):
            continue
        active = active_by_id.get(chapter_id, {})
        title = active.get("title", record.get("title"))
        file_path = active.get("file", record.get("file"))
        if isinstance(title, str) and isinstance(file_path, str):
            chapters.append({"chapter_id": chapter_id, "title": title, "file": file_path})
    return chapters


def active_chapter_ids(chapters: list[dict[str, str]]) -> list[str]:
    return [chapter["chapter_id"] for chapter in chapters]


def missing_snapshot_records(chapter_ids: list[str], records: dict[str, dict[str, Any]]) -> list[str]:
    return [chapter_id for chapter_id in chapter_ids if chapter_id not in records]


def curated_record_map(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    records = manifest.get("chapter_records")
    if not isinstance(records, list):
        raise TypeError("curated reader manifest chapter_records must be a list")
    result: dict[str, dict[str, Any]] = {}
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            raise TypeError(f"chapter_records[{index}] must be an object")
        chapter_id = record.get("chapter_id")
        if not isinstance(chapter_id, str) or not chapter_id.strip():
            raise ValueError(f"chapter_records[{index}] missing chapter_id")
        if chapter_id in result:
            raise ValueError(f"duplicate curated reader chapter_id: {chapter_id}")
        result[chapter_id] = record
    return result


def validate_curated_sources(
    chapters: list[dict[str, str]],
    records: dict[str, dict[str, Any]],
) -> list[str]:
    errors: list[str] = []
    expected_ids = {chapter["chapter_id"] for chapter in chapters}
    record_ids = set(records)
    missing = sorted(expected_ids - record_ids)
    extra = sorted(record_ids - expected_ids)
    if missing:
        errors.append(f"curated manifest missing active chapter(s): {missing}")
    if extra:
        errors.append(f"curated manifest has non-active chapter record(s): {extra}")

    for chapter in chapters:
        chapter_id = chapter["chapter_id"]
        record = records.get(chapter_id, {})
        file_value = record.get("file")
        if not isinstance(file_value, str) or not file_value:
            errors.append(f"{chapter_id}: curated record missing file")
            continue
        path = ROOT / file_value
        if not file_value.startswith("editions/reader_manuscript/v1_0/chapters/"):
            errors.append(f"{chapter_id}: curated file must stay under editions/reader_manuscript/v1_0/chapters/")
        if not path.exists():
            errors.append(f"{chapter_id}: curated file does not exist: {file_value}")
            continue
        text = path.read_text(encoding="utf-8")
        if f"chapter_id: {chapter_id}" not in text[:1200]:
            errors.append(f"{chapter_id}: curated file header does not name the matching chapter_id")
        if text.count("\n## Handoff") != 1:
            errors.append(f"{chapter_id}: curated file must contain exactly one Handoff section")
        for heading in LIVE_ONLY_HEADINGS:
            if heading in text:
                errors.append(f"{chapter_id}: curated file still contains live-only heading {heading!r}")
        blockers = record.get("release_blockers")
        if not isinstance(blockers, list):
            errors.append(f"{chapter_id}: release_blockers must be a list")
            blockers = []
        missing_blockers = sorted(REQUIRED_RELEASE_BLOCKERS - {str(item) for item in blockers})
        if missing_blockers:
            errors.append(f"{chapter_id}: release_blockers missing {missing_blockers}")
        if record.get("reconciliation_status") not in {"drafting", "reconciled"}:
            errors.append(f"{chapter_id}: reconciliation_status must be drafting or reconciled")
        if record.get("canonical_change_required") is not False:
            errors.append(f"{chapter_id}: canonical_change_required must remain false for a renderable draft")
    return errors


def copy_curated_chapters(
    output_dir: Path,
    chapters: list[dict[str, str]],
    records: dict[str, dict[str, Any]],
) -> list[dict[str, str]]:
    copied: list[dict[str, str]] = []
    for chapter in chapters:
        chapter_id = chapter["chapter_id"]
        record = records[chapter_id]
        src = ROOT / str(record["file"])
        dst = output_dir / chapter["file"]
        dst.parent.mkdir(parents=True, exist_ok=True)
        text = src.read_text(encoding="utf-8").replace(
            SOURCE_READER_ASSET_PREFIX, GENERATED_READER_ASSET_PREFIX
        )
        dst.write_text(text, encoding="utf-8")
        shutil.copystat(src, dst)
        copied.append(
            {
                "chapter_id": chapter_id,
                "title": chapter["title"],
                "curated_source": rel(src),
                "generated_target": str(dst.relative_to(output_dir)),
                "reconciliation_status": str(record.get("reconciliation_status")),
            }
        )
    return copied


def copy_reader_assets(output_dir: Path) -> None:
    """Make tracked diagram/image references renderable in the derived workspace."""

    source_assets = ROOT / "assets"
    target_assets = output_dir / "assets"
    if not source_assets.exists():
        raise FileNotFoundError("tracked assets directory is missing")
    shutil.copytree(source_assets, target_assets, dirs_exist_ok=True)


def write_curated_checklist(output_dir: Path, copied: list[dict[str, str]]) -> str:
    lines = [
        "# Curated Reader Review Checklist",
        "",
        "Status: local curated-reader build checklist; not a release record.",
        "",
        "This workspace renders the tracked curated-reader chapter drafts as a Quarto book. It is a review input only. The live AI/research book remains canonical for claims, evidence states, source boundaries, proof/test status, implementation horizons, and release records.",
        "",
        "## Scope",
        "",
        f"- Curated chapters copied: {len(copied)}",
        "- Source manifest: `editions/reader_manuscript/v1_0/manifest.json`",
        f"- Build report: `{REPORT_NAME}`",
        "",
        "## Review Gate",
        "",
        "- [ ] Read the curated manuscript as a continuous book, not chapter-by-chapter fragments.",
        "- [ ] Confirm every chapter preserves the live chapter's claim boundary, support state, source boundary, proof/test status, and implementation horizon.",
        "- [ ] Confirm reader-only reordering or compression did not remove meaning-critical caveats.",
        "- [ ] Confirm chapter handoffs preserve the manifest order and final chapter closes the book-level arc.",
        "- [ ] Treat `reader_delta_report.md` and reader-overlay metadata as baseline-generator context only; the tracked curated chapter files are the source under review in this workspace.",
        "- [ ] Run `node scripts/validate_reader_html_artifact_browser.js --strict --site build/curated_reader_edition/_reader_site --manifest build/curated_reader_edition/reader_manifest.json --report build/curated_reader_edition/curated_reader_html_browser_report.json` after rendering curated HTML.",
        "- [ ] Render any target formats only after this source-level review passes.",
        "- [ ] Keep EPUB, DOCX, PDF, HTML, e-reader, and audio approvals separate until exact artifacts are reviewed and release-recorded.",
        "",
        "## Non-Claims",
        "",
        "- This checklist does not approve the curated reader manuscript.",
        "- This checklist does not approve any generated format artifact.",
        "- This checklist does not promote any claim support state.",
    ]
    (output_dir / CHECKLIST_NAME).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return CHECKLIST_NAME


def release_blocker_counts(records: dict[str, dict[str, Any]]) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for record in records.values():
        blockers = record.get("release_blockers", [])
        if isinstance(blockers, list):
            for blocker in blockers:
                if isinstance(blocker, str) and blocker:
                    counts[blocker] += 1
    return dict(sorted(counts.items()))


def write_report(
    output_dir: Path,
    baseline_summary: dict[str, Any],
    copied: list[dict[str, str]],
    records: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    report = {
        "schema_version": "0.1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "curated_reader_source_renderable",
        "source_mode": "tracked_curated_reader_manuscript",
        "source_manifest": rel(MANIFEST_PATH),
        "baseline_generator": "scripts/build_reader_edition.py",
        "baseline_summary": baseline_summary,
        "chapter_count": len(copied),
        "chapters": copied,
        "release_blocker_counts": release_blocker_counts(records),
        "review_status": "review_required",
        "review_checklist": CHECKLIST_NAME,
        "baseline_delta_report_note": (
            "reader_delta_report.md and reader_overlay fields are inherited from "
            "the generated reader baseline before curated chapter replacement; "
            "review the tracked curated chapter files and this build report for "
            "the curated source path."
        ),
        "non_claims": [
            "This local workspace is not the canonical living book.",
            "This local workspace is not a reader release record or artifact approval.",
            "Curated reader prose is a derivative review source and does not change claim meaning, support states, source boundaries, proof/test status, implementation horizons, or release records.",
            "EPUB, DOCX, PDF, HTML, e-reader, and audio artifacts remain unapproved unless exact rendered artifacts are separately reviewed and release-recorded.",
        ],
    }
    (output_dir / REPORT_NAME).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


def update_reader_manifest(output_dir: Path, report: dict[str, Any]) -> None:
    path = output_dir / "reader_manifest.json"
    data = load_json(path)
    if not isinstance(data, dict):
        raise TypeError("generated reader_manifest.json must contain an object")
    data["source_mode"] = "tracked_curated_reader_manuscript"
    data["curated_reader_manifest"] = rel(MANIFEST_PATH)
    data["curated_reader_build_report"] = REPORT_NAME
    data["curated_reader_review_checklist"] = CHECKLIST_NAME
    data["curated_reader_release_blocker_counts"] = report["release_blocker_counts"]
    data["baseline_delta_report_note"] = report["baseline_delta_report_note"]
    data["review_status"] = "curated_review_required"
    data["non_claims"] = list(data.get("non_claims", [])) + [
        "This workspace uses tracked curated-reader chapter drafts as review input, but the live AI/research book remains canonical for claims and evidence.",
        "Curated-reader source rendering does not approve any reader format artifact or release record.",
    ]
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def validate_generated_workspace(output_dir: Path, chapters: list[dict[str, str]]) -> list[str]:
    errors: list[str] = []
    if not (output_dir / "_quarto.yml").exists():
        errors.append("generated workspace missing _quarto.yml")
    if not (output_dir / REPORT_NAME).exists():
        errors.append(f"generated workspace missing {REPORT_NAME}")
    if not (output_dir / CHECKLIST_NAME).exists():
        errors.append(f"generated workspace missing {CHECKLIST_NAME}")
    errors.extend(build_reader_edition.scan_for_view_block_markers(output_dir))
    for chapter in chapters:
        path = output_dir / chapter["file"]
        if not path.exists():
            errors.append(f"{chapter['chapter_id']}: missing generated curated chapter {chapter['file']}")
            continue
        text = path.read_text(encoding="utf-8")
        if text.count("\n## Handoff") != 1:
            errors.append(f"{chapter['chapter_id']}: generated curated chapter must contain exactly one Handoff")
        for heading in LIVE_ONLY_HEADINGS:
            if heading in text:
                errors.append(f"{chapter['chapter_id']}: generated curated chapter contains live-only heading {heading!r}")
        if SOURCE_READER_ASSET_PREFIX in text:
            errors.append(
                f"{chapter['chapter_id']}: generated curated chapter still contains source-relative asset paths"
            )
        for ref in GENERATED_ASSET_REF_RE.findall(text):
            asset_path = (path.parent / ref).resolve()
            if not asset_path.exists():
                errors.append(
                    f"{chapter['chapter_id']}: generated curated asset reference does not exist: {ref}"
                )
    return errors


def generate(output_dir: Path, profile_id: str = "reader_release") -> dict[str, Any]:
    structure = load_json(STRUCTURE_PATH)
    manifest = load_json(MANIFEST_PATH)
    if not isinstance(structure, dict) or not isinstance(manifest, dict):
        raise TypeError("book_structure.json and curated reader manifest must contain objects")

    active_chapters = manifest_chapters(structure)
    records = curated_record_map(manifest)
    snapshot_ids = historical_snapshot_ids(manifest)
    chapters = active_chapters
    if snapshot_ids is not None:
        missing_records = missing_snapshot_records(snapshot_ids, records)
        if missing_records:
            fail(f"historical reader snapshot missing curated record(s): {missing_records}")
        chapters = historical_snapshot_chapters(snapshot_ids, records, active_chapters)
    errors = validate_curated_sources(chapters, records)
    if errors:
        fail(errors)

    if snapshot_ids is not None and active_chapter_ids(active_chapters) != snapshot_ids:
        fail(
            "historical reader snapshot cannot be rendered from a divergent active spine; "
            "create a later reader-edition directory and release record for the active chapters"
        )

    baseline_summary = build_reader_edition.generate(output_dir, profile_id)
    copy_reader_assets(output_dir)
    copied = copy_curated_chapters(output_dir, chapters, records)
    write_curated_checklist(output_dir, copied)
    report = write_report(output_dir, baseline_summary, copied, records)
    update_reader_manifest(output_dir, report)

    workspace_errors = validate_generated_workspace(output_dir, chapters)
    if workspace_errors:
        fail(workspace_errors)
    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", default="reader_release", help="reader profile id to use for scaffolding")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="output directory for generated Quarto workspace")
    parser.add_argument("--check", action="store_true", help="generate into a temporary directory and validate only")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.check:
        manifest = load_json(MANIFEST_PATH)
        structure = load_json(STRUCTURE_PATH)
        if not isinstance(manifest, dict) or not isinstance(structure, dict):
            fail("book_structure.json and curated reader manifest must contain objects")
        records = curated_record_map(manifest)
        snapshot_ids = historical_snapshot_ids(manifest)
        active_chapters = manifest_chapters(structure)
        if snapshot_ids is not None and active_chapter_ids(active_chapters) != snapshot_ids:
            missing_records = missing_snapshot_records(snapshot_ids, records)
            if missing_records:
                fail(f"historical reader snapshot missing curated record(s): {missing_records}")
            errors = validate_curated_sources(historical_snapshot_chapters(snapshot_ids, records), records)
            if errors:
                fail(errors)
            print(
                "Curated historical reader source check passed: "
                f"{len(snapshot_ids)} frozen chapters remain valid while the active spine has "
                f"{len(active_chapters)} chapters; no historical workspace was rendered."
            )
            return
        with tempfile.TemporaryDirectory(prefix="asi-curated-reader-") as temp_dir:
            report = generate(Path(temp_dir), args.profile)
            print(
                "Curated reader edition check passed: "
                f"{report['chapter_count']} curated chapters renderable as Quarto source; "
                f"review status {report['review_status']}."
            )
            return

    output_dir = Path(args.output)
    report = generate(output_dir, args.profile)
    print(f"Curated reader edition wrote: {output_dir}")
    print(f"Curated reader build report wrote: {output_dir / REPORT_NAME}")
    print(
        "Curated reader edition ready for local source review: "
        f"{report['chapter_count']} chapters, review status {report['review_status']}."
    )


if __name__ == "__main__":
    main()
