#!/usr/bin/env python3
"""Validate semantic reader overlays and generated reader delta reports."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
import tempfile

import build_reader_edition
import sync_reader_overlay_asset

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT = ROOT / "build" / "reader_overlay_report.json"


def write_report(report: dict[str, object], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")


def validate_overlay(profile_id: str) -> dict[str, object]:
    errors: list[str] = []
    profile = build_reader_edition.find_profile(profile_id)

    try:
        overlay_context = build_reader_edition.load_reader_overlay_context(profile)
    except Exception as exc:
        return {
            "schema_version": "0.1",
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "profile": profile_id,
            "status": "fail",
            "errors": [f"overlay context failed to load: {exc}"],
            "non_claims": [
                "This report validates reader overlay mechanics only.",
                "It does not claim any reader format or audio artifact exists.",
            ],
        }

    overlay_summary = build_reader_edition.reader_overlay_summary(overlay_context)
    if profile_id == "reader_release" and not overlay_summary.get("configured"):
        errors.append("reader_release must configure a reader overlay manifest.")

    manifest_path = overlay_summary.get("manifest_path")
    if overlay_summary.get("configured"):
        if not isinstance(manifest_path, str) or not manifest_path:
            errors.append("configured overlay is missing manifest_path.")
        elif not (ROOT / manifest_path).exists():
            errors.append(f"configured overlay manifest does not exist: {manifest_path}")

    generated_overlay_summary = overlay_summary
    try:
        sync_payload = sync_reader_overlay_asset.sync_asset(
            sync_reader_overlay_asset.DEFAULT_OUTPUT,
            profile_id,
            check=True,
        )
    except Exception as exc:
        errors.append(f"reader overlay live asset check failed: {exc}")
        sync_payload = {}

    try:
        with tempfile.TemporaryDirectory(prefix="asi-reader-overlay-") as temp_dir:
            output_dir = Path(temp_dir)
            generation_summary = build_reader_edition.generate(output_dir, profile_id)
            generated_overlay = generation_summary.get("reader_overlay")
            if isinstance(generated_overlay, dict):
                generated_overlay_summary = generated_overlay
            delta_report = output_dir / str(
                generation_summary.get("reader_delta_report", build_reader_edition.DEFAULT_DELTA_REPORT)
            )
            if not delta_report.exists():
                errors.append("generated reader edition is missing reader_delta_report.md.")
            else:
                delta_text = delta_report.read_text(encoding="utf-8", errors="ignore")
                for needle in (
                    "Reader Delta Report",
                    "Applied Overlay Operations",
                    "Generator Transformations",
                    "Non-Claims",
                ):
                    if needle not in delta_text:
                        errors.append(f"reader_delta_report.md is missing required section: {needle}")

            reader_manifest_path = output_dir / "reader_manifest.json"
            if not reader_manifest_path.exists():
                errors.append("generated reader edition is missing reader_manifest.json.")
                reader_manifest: dict[str, object] = {}
            else:
                loaded_manifest = json.loads(reader_manifest_path.read_text(encoding="utf-8"))
                reader_manifest = loaded_manifest if isinstance(loaded_manifest, dict) else {}
                if not isinstance(reader_manifest, dict):
                    errors.append("reader_manifest.json must contain an object.")

            manifest_overlay = reader_manifest.get("reader_overlay")
            if not isinstance(manifest_overlay, dict):
                errors.append("reader_manifest.json is missing reader_overlay object.")
            else:
                if manifest_overlay.get("manifest_path") != manifest_path:
                    errors.append("reader_manifest.json reader_overlay.manifest_path does not match overlay manifest.")
                if generation_summary.get("reader_overlay_operations_applied") != manifest_overlay.get("applied_operations"):
                    errors.append("reader overlay applied-operation count differs between summary and manifest.")
            if reader_manifest.get("reader_delta_report") != generation_summary.get("reader_delta_report"):
                errors.append("reader_manifest.json reader_delta_report does not match generation summary.")
    except Exception as exc:
        errors.append(f"reader generation with overlays failed: {exc}")
        generation_summary = {}
        reader_manifest = {}

    return {
        "schema_version": "0.1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "profile": profile_id,
        "overlay": generated_overlay_summary,
        "live_human_view_asset": sync_payload,
        "reader_generation": generation_summary,
        "reader_manifest_overlay": reader_manifest.get("reader_overlay") if isinstance(reader_manifest, dict) else None,
        "status": "pass" if not errors else "fail",
        "errors": errors,
        "non_claims": [
            "This report validates reader overlay mechanics and generated delta-report wiring only.",
            "It does not claim that EPUB, PDF, DOCX, HTML, audio, or audio-embedded EPUB artifacts exist.",
            "It does not promote any claim support state.",
        ],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", default="reader_release", help="release profile to validate")
    parser.add_argument("--report", default=str(DEFAULT_REPORT), help="report path for non-check runs")
    parser.add_argument("--check", action="store_true", help="validate without writing build/ report")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report = validate_overlay(args.profile)
    if not args.check:
        write_report(report, Path(args.report))

    if report["status"] != "pass":
        print("Reader overlay validation failed:")
        for error in report["errors"]:
            print(f" - {error}")
        sys.exit(1)

    overlay = report.get("overlay", {})
    applied = overlay.get("applied_operations", 0) if isinstance(overlay, dict) else 0
    active = overlay.get("active_operations", 0) if isinstance(overlay, dict) else 0
    print(
        "Reader overlay validation passed: "
        f"{active} active operations, {applied} applied operations."
    )


if __name__ == "__main__":
    main()
