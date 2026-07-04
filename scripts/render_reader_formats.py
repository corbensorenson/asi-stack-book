#!/usr/bin/env python3
"""Render selected reader-edition formats and record actual outcomes.

This helper generates the reader-edition Quarto source, runs Quarto for the
requested formats, snapshots each successful format output under the ignored
reader workspace, and writes a local render report. It does not publish
artifacts and it does not mark a release complete. A major-version edition still
needs review and an edition release record.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

import build_reader_edition

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "build" / "reader_edition"
DEFAULT_FORMATS = ("html", "epub", "docx")
FORMAT_EXTENSIONS = {
    "html": [".html"],
    "epub": [".epub"],
    "docx": [".docx"],
    "pdf": [".pdf"],
}
PRESERVED_ARTIFACT_DIR = "format_artifacts"


def find_artifacts(output_dir: Path, fmt: str) -> list[str]:
    suffixes = FORMAT_EXTENSIONS.get(fmt, [])
    artifacts: list[str] = []
    search_root = output_dir / "_reader_site" if fmt == "html" and (output_dir / "_reader_site").exists() else output_dir
    for path in search_root.rglob("*"):
        if not path.is_file():
            continue
        if PRESERVED_ARTIFACT_DIR in path.relative_to(output_dir).parts:
            continue
        if any(path.name.endswith(suffix) for suffix in suffixes):
            artifacts.append(str(path.relative_to(output_dir)))
    return sorted(artifacts)


def preserve_artifacts(output_dir: Path, fmt: str, artifacts: list[str]) -> list[str]:
    """Snapshot format outputs before a later Quarto render cleans the directory."""

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
    with tempfile.NamedTemporaryFile("w+", encoding="utf-8", errors="ignore") as log_file:
        result = subprocess.run(
            command,
            cwd=output_dir,
            check=False,
            text=True,
            stdout=log_file,
            stderr=subprocess.STDOUT,
        )
        log_file.seek(0)
        output = log_file.read()
    artifacts = find_artifacts(output_dir, fmt) if result.returncode == 0 else []
    preserved_artifacts = preserve_artifacts(output_dir, fmt, artifacts) if artifacts else []
    return {
        "format": fmt,
        "status": "rendered" if result.returncode == 0 else "failed",
        "returncode": result.returncode,
        "command": " ".join(command),
        "artifacts": artifacts,
        "preserved_artifacts": preserved_artifacts,
        "log_excerpt": output[-4000:],
    }


def write_report(
    output_dir: Path,
    profile_id: str,
    generation_summary: dict[str, object],
    render_records: list[dict[str, object]],
) -> dict[str, object]:
    report = {
        "schema_version": "0.1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_profile": profile_id,
        "reader_generation": generation_summary,
        "format_results": render_records,
        "review_status": "review_required",
        "non_claims": [
            "This report records local render attempts only.",
            "A rendered file is not a published major-version edition until reviewed and listed in an edition release record.",
            "Preserved artifacts are local snapshots in an ignored review workspace, not release artifacts.",
            "PDF may fail on machines without local Quarto PDF dependencies.",
            "Audio artifacts are not produced by this reader-format renderer."
        ],
    }
    (output_dir / "reader_render_report.json").write_text(
        json.dumps(report, indent=2) + "\n",
        encoding="utf-8",
    )
    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", default="reader_release", help="reader profile id to generate")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="generated reader-edition source directory")
    parser.add_argument(
        "--formats",
        nargs="+",
        default=list(DEFAULT_FORMATS),
        help="Quarto formats to render, for example: html epub docx pdf",
    )
    parser.add_argument("--include-pdf", action="store_true", help="also attempt PDF if it is not already listed")
    parser.add_argument("--stop-on-fail", action="store_true", help="stop after the first failed format render")
    parser.add_argument("--check", action="store_true", help="validate setup in a temporary reader workspace without rendering formats")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    formats = list(dict.fromkeys(args.formats + (["pdf"] if args.include_pdf else [])))

    if args.check:
        if shutil.which("quarto") is None:
            raise SystemExit("Reader format render check failed: quarto is not on PATH.")
        with tempfile.TemporaryDirectory(prefix="asi-reader-render-check-") as temp_dir:
            summary = build_reader_edition.generate(Path(temp_dir), args.profile)
            if not (Path(temp_dir) / "reader_manifest.json").exists():
                raise SystemExit("Reader format render check failed: missing reader_manifest.json.")
            print(
                "Reader format render check passed: "
                f"{summary['chapters']} chapters ready for formats {', '.join(formats)}."
            )
            return

    if shutil.which("quarto") is None:
        raise SystemExit("Cannot render reader formats: quarto is not on PATH.")

    output_dir = Path(args.output)
    summary = build_reader_edition.generate(output_dir, args.profile)
    render_records: list[dict[str, object]] = []
    for fmt in formats:
        record = run_render(output_dir, fmt)
        render_records.append(record)
        print(f"{fmt}: {record['status']}")
        if args.stop_on_fail and record["status"] != "rendered":
            break

    report = write_report(output_dir, args.profile, summary, render_records)
    report_path = output_dir / "reader_render_report.json"
    failed = [record["format"] for record in render_records if record["status"] != "rendered"]
    print(f"Reader render report wrote: {report_path}")
    if failed:
        print(f"Failed formats: {', '.join(str(value) for value in failed)}")
        raise SystemExit(1)
    print(f"Rendered formats recorded: {len(report['format_results'])}")


if __name__ == "__main__":
    main()
