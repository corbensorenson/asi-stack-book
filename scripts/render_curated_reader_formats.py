#!/usr/bin/env python3
"""Render selected formats from the tracked curated reader manuscript.

This is the curated-reader counterpart to ``render_reader_formats.py``. It
builds the review workspace from tracked curated chapter files, renders the
requested Quarto formats, snapshots successful artifacts under ignored build
space, and writes a local report. It does not publish artifacts, clear release
blockers, or create an edition release record.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

import build_curated_reader_edition


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "build" / "curated_reader_edition"
DEFAULT_FORMATS = ("html", "epub", "docx")
FORMAT_EXTENSIONS = {
    "html": [".html"],
    "epub": [".epub"],
    "docx": [".docx"],
    "pdf": [".pdf"],
}
PRESERVED_ARTIFACT_DIR = "format_artifacts"
REPORT_NAME = "curated_reader_render_report.json"


def find_artifacts(output_dir: Path, fmt: str) -> list[str]:
    suffixes = FORMAT_EXTENSIONS.get(fmt, [])
    search_root = output_dir / "_reader_site" if fmt == "html" and (output_dir / "_reader_site").exists() else output_dir
    artifacts: list[str] = []
    for path in search_root.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(output_dir)
        if PRESERVED_ARTIFACT_DIR in relative.parts:
            continue
        if any(path.name.endswith(suffix) for suffix in suffixes):
            artifacts.append(str(relative))
    return sorted(artifacts)


def preserve_artifacts(output_dir: Path, fmt: str, artifacts: list[str]) -> list[str]:
    snapshot_dir = output_dir / PRESERVED_ARTIFACT_DIR / fmt
    if snapshot_dir.exists():
        shutil.rmtree(snapshot_dir)
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    if fmt == "html" and (output_dir / "_reader_site").is_dir():
        shutil.copytree(output_dir / "_reader_site", snapshot_dir / "_reader_site")
        return sorted(
            str(path.relative_to(output_dir))
            for path in snapshot_dir.rglob("*")
            if path.is_file()
        )

    preserved: list[str] = []
    for artifact in artifacts:
        src = output_dir / artifact
        if not src.is_file():
            continue
        dst = snapshot_dir / artifact
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        preserved.append(str(dst.relative_to(output_dir)))
    return sorted(preserved)


def run_render(output_dir: Path, fmt: str) -> dict[str, object]:
    command = ["quarto", "render", "--to", fmt]
    result = subprocess.run(
        command,
        cwd=output_dir,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    output = result.stdout or ""
    artifacts = find_artifacts(output_dir, fmt) if result.returncode == 0 else []
    preserved_artifacts = preserve_artifacts(output_dir, fmt, artifacts) if artifacts else []
    warning_lines = [line for line in output.splitlines() if "[WARNING]" in line]
    svg_conversion_warning_count = sum("Could not convert image" in line for line in warning_lines)
    return {
        "format": fmt,
        "status": "rendered" if result.returncode == 0 else "failed",
        "returncode": result.returncode,
        "command": " ".join(command),
        "artifacts": artifacts,
        "preserved_artifacts": preserved_artifacts,
        "warning_count": len(warning_lines),
        "svg_conversion_warning_count": svg_conversion_warning_count,
        "log_excerpt": output[-4000:],
    }


def write_report(
    output_dir: Path,
    generation_report: dict[str, object],
    render_records: list[dict[str, object]],
) -> dict[str, object]:
    report = {
        "schema_version": "0.1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_mode": "tracked_curated_reader_manuscript",
        "source_manifest": "editions/reader_manuscript/v1_0/manifest.json",
        "curated_generation": generation_report,
        "format_results": render_records,
        "review_status": "review_required",
        "release_blockers_preserved": [
            "curated_reconciliation_not_approved",
            "format_artifact_not_reviewed",
            "reader_release_record_not_created",
            "full_format_artifact_review_not_completed",
            "app_or_ereader_review_not_completed",
        ],
        "non_claims": [
            "This report records local curated-reader render attempts only.",
            "A rendered curated-reader file is not a published major-version edition until reviewed and listed in an edition release record.",
            "Preserved artifacts are local snapshots in an ignored review workspace, not release artifacts.",
            "EPUB and DOCX renders are structural review inputs only until application-level review is complete.",
            "PDF and audio artifacts are not produced by this curated-reader format renderer.",
            "This report does not promote any claim support state.",
        ],
    }
    (output_dir / REPORT_NAME).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", default="reader_release", help="reader profile id to use for scaffolding")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="generated curated reader workspace")
    parser.add_argument(
        "--formats",
        nargs="+",
        default=list(DEFAULT_FORMATS),
        help="Quarto formats to render, for example: html epub docx pdf",
    )
    parser.add_argument("--include-pdf", action="store_true", help="also attempt PDF if it is not already listed")
    parser.add_argument("--stop-on-fail", action="store_true", help="stop after the first failed format render")
    parser.add_argument("--check", action="store_true", help="validate setup in a temporary workspace without rendering formats")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    formats = list(dict.fromkeys(args.formats + (["pdf"] if args.include_pdf else [])))

    if args.check:
        if shutil.which("quarto") is None:
            raise SystemExit("Curated reader format render check failed: quarto is not on PATH.")
        with tempfile.TemporaryDirectory(prefix="asi-curated-reader-render-check-") as temp_dir:
            report = build_curated_reader_edition.generate(Path(temp_dir), args.profile)
            if not (Path(temp_dir) / "reader_manifest.json").exists():
                raise SystemExit("Curated reader format render check failed: missing reader_manifest.json.")
            print(
                "Curated reader format render check passed: "
                f"{report['chapter_count']} curated chapters ready for formats {', '.join(formats)}."
            )
            return

    if shutil.which("quarto") is None:
        raise SystemExit("Cannot render curated reader formats: quarto is not on PATH.")

    output_dir = Path(args.output)
    generation_report = build_curated_reader_edition.generate(output_dir, args.profile)
    render_records: list[dict[str, object]] = []
    for fmt in formats:
        record = run_render(output_dir, fmt)
        render_records.append(record)
        print(f"{fmt}: {record['status']}")
        if args.stop_on_fail and record["status"] != "rendered":
            break

    report = write_report(output_dir, generation_report, render_records)
    failed = [record["format"] for record in render_records if record["status"] != "rendered"]
    print(f"Curated reader render report wrote: {output_dir / REPORT_NAME}")
    if failed:
        print(f"Failed formats: {', '.join(str(value) for value in failed)}")
        raise SystemExit(1)
    print(f"Rendered curated reader formats recorded: {len(report['format_results'])}")


if __name__ == "__main__":
    main()
