#!/usr/bin/env python3
"""Create or validate the exact v2.0 curated-reader HTML release record."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
EDITION = ROOT / "editions/reader_manuscript/v2_0"
RECORD = EDITION / "reader_release_record.json"
SCHEMA = ROOT / "schemas/post_v2_3_reader_html_release_record.schema.json"
ARTIFACT_MANIFEST = EDITION / "html_artifact_manifest.json"
INSPECTION = EDITION / "html_release_inspection.json"
SOURCE_MANIFEST = EDITION / "manifest.json"
REPORTS = {
    "browser": EDITION / "html_browser_report.json",
    "accessibility_tree": EDITION / "html_accessibility_tree_report.json",
    "keyboard": EDITION / "html_keyboard_report.json",
    "wcag_preparation": EDITION / "html_wcag_report.json",
}


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def build() -> dict:
    manifest = load(SOURCE_MANIFEST)
    artifact = load(ARTIFACT_MANIFEST)
    inspection = load(INSPECTION)
    reports = {name: load(path) for name, path in REPORTS.items()}
    if inspection.get("status") != "passed_exact_html_release_inspection":
        raise ValueError("exact HTML release inspection has not passed")
    archive = ROOT / artifact["archive"]
    if not archive.is_file() or sha(archive) != artifact["archive_sha256"]:
        raise ValueError("artifact archive is missing or digest-invalid")
    return {
        "schema_version": "asi_stack.curated_reader_html_release_record.v2",
        "record_type": "edition_release",
        "release_id": f"2026-07-13-v2-curated-reader-html-{artifact['archive_sha256'][:8]}",
        "edition_id": "asi-stack-curated-reader-v2.0",
        "decision": "approved_exact_local_html_archive",
        "decision_date": "2026-07-13",
        "source_authority": {
            "manifest": rel(SOURCE_MANIFEST),
            "source_tree_sha256": manifest["source_snapshot"]["source_tree_sha256"],
            "book_structure_sha256": manifest["source_snapshot"]["book_structure_sha256"],
            "generated_baseline_bundle_sha256": manifest["generated_baseline"]["chapter_bundle_sha256"],
            "curated_chapter_count": 54,
            "core_support_snapshot": {"argument": 54},
            "canonical_relationship": "parallel derivative; live book remains claim/evidence authority"
        },
        "artifact": {
            "format": "canonical_curated_html",
            "archive": artifact["archive"],
            "archive_sha256": artifact["archive_sha256"],
            "archive_bytes": artifact["archive_bytes"],
            "site_tree_sha256": artifact["site_tree_sha256"],
            "format_profile_sha256": artifact["format_profile_sha256"],
            "html_page_count": 59,
            "chapter_entry_point_count": 54,
            "publication_state": "tracked_local_archive_not_publicly_deployed"
        },
        "inspection_evidence": {
            "exact_archive_and_link_inspection": {
                "path": rel(INSPECTION),
                "sha256": sha(INSPECTION),
                "internal_links_checked": inspection["internal_links_checked"],
                "internal_anchors_checked": inspection["internal_anchors_checked"],
                "unresolved": inspection["unresolved_internal_links_or_anchors"]
            },
            "browser": {
                "path": rel(REPORTS["browser"]),
                "sha256": sha(REPORTS["browser"]),
                "page_view_pairs": reports["browser"]["page_view_pairs"],
                "failures": len(reports["browser"].get("failures", [])),
                "reflow_overflow_failures": sum(int(row.get("horizontal_overflow_px", 0)) > 0 for row in reports["browser"]["results"])
            },
            "accessibility_tree": {
                "path": rel(REPORTS["accessibility_tree"]),
                "sha256": sha(REPORTS["accessibility_tree"]),
                "page_view_pairs": reports["accessibility_tree"]["summary"]["page_view_pairs"],
                "failed_page_view_pairs": reports["accessibility_tree"]["summary"]["failed_page_view_pairs"],
                "unnamed_interactive_elements": reports["accessibility_tree"]["summary"]["unnamed_interactive_elements"],
                "duplicate_id_page_views": reports["accessibility_tree"]["summary"]["duplicate_id_page_views"]
            },
            "keyboard": {
                "path": rel(REPORTS["keyboard"]),
                "sha256": sha(REPORTS["keyboard"]),
                "page_view_pairs": reports["keyboard"]["summary"]["page_view_pairs"],
                "failed_page_view_pairs": reports["keyboard"]["summary"]["failed_page_view_pairs"],
                "keyboard_trap_candidates": reports["keyboard"]["summary"]["keyboard_trap_candidates"]
            },
            "wcag_preparation": {
                "path": rel(REPORTS["wcag_preparation"]),
                "sha256": sha(REPORTS["wcag_preparation"]),
                "page_view_pairs": reports["wcag_preparation"]["summary"]["page_view_pairs"],
                "text_contrast_samples": reports["wcag_preparation"]["summary"]["text_contrast_samples"],
                "contrast_failure_samples": reports["wcag_preparation"]["summary"]["contrast_failure_samples"],
                "minimum_contrast_ratio": reports["wcag_preparation"]["summary"]["minimum_contrast_ratio"]
            }
        },
        "review_boundaries": {
            "all_chapter_entry_points_desktop_and_mobile": True,
            "automated_accessibility_tree": True,
            "automated_keyboard_traversal": True,
            "rendered_text_contrast": True,
            "static_internal_links_and_anchors": True,
            "screen_reader_review": "not_performed_not_required_for_selected_scope",
            "independent_external_human_review": False,
            "third_party_or_legal_wcag_certification": False
        },
        "rights_snapshot": {
            "authority": "LICENSE.md",
            "license_route": "all_rights_reserved_untagged_or_later_drafting_path",
            "public_license_grant": False,
            "note": "This local artifact is not included in an exact tagged release routing ledger; no license grant is inferred from historical tagged releases."
        },
        "approved_formats": ["canonical_curated_html"],
        "deferred_formats": ["epub", "docx", "pdf", "audio", "embedded_audio"],
        "selected_format_blockers": [],
        "residuals": [
            "The approved archive is tracked locally and is not a public deployment or hosted attestation.",
            "No independent external-human, screen-reader, or assistive-technology review occurred.",
            "Automated WCAG-preparation evidence is not third-party or legal WCAG certification.",
            "EPUB, DOCX, PDF, audio, and embedded-audio editions were not selected, generated, or approved in this cycle.",
            "The curated prose begins as an exact generated Human baseline; byte identity is meaning reconciliation, not proof of literary perfection."
        ],
        "support_state_effect": "none",
        "non_claims": [
            "This record does not approve any format other than the exact digest-bound canonical HTML archive.",
            "This record does not claim public deployment, independent review, screen-reader review, or legal WCAG conformance.",
            "This reader artifact is not canonical claim, source, proof, experiment, or release authority for the live book.",
            "This record does not promote any chapter core claim above argument.",
            "This record does not establish model quality, capability, safety, readiness, governance efficacy, AGI, or ASI."
        ]
    }


def validate(record: dict, expected: dict) -> list[str]:
    errors: list[str] = []
    try:
        jsonschema.validate(record, load(SCHEMA))
    except jsonschema.ValidationError as exc:
        errors.append(f"schema violation: {exc.message}")
    if record != expected:
        errors.append("release record differs from exact current artifact/evidence reconstruction")
    if record.get("artifact", {}).get("archive_sha256") != sha(ROOT / expected["artifact"]["archive"]):
        errors.append("release record archive digest does not match archive bytes")
    if record.get("support_state_effect") != "none":
        errors.append("release record launders support movement")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    expected = build()
    if args.write:
        artifact = load(ARTIFACT_MANIFEST)
        artifact["render_state"] = "released_exact_archive"
        ARTIFACT_MANIFEST.write_text(json.dumps(artifact, indent=2) + "\n")
        RECORD.write_text(json.dumps(expected, indent=2) + "\n")
    if not RECORD.is_file():
        raise SystemExit("Reader HTML release-record validation failed: record absent; run with --write")
    record = load(RECORD)
    errors = validate(record, expected)
    mutations = [
        ("decision", "blocked"),
        ("support_state_effect", "prototype-backed"),
        ("approved_formats", ["canonical_curated_html", "epub"]),
        ("selected_format_blockers", ["unresolved"]),
    ]
    for key, value in mutations:
        candidate = copy.deepcopy(record)
        candidate[key] = value
        if not validate(candidate, expected):
            errors.append(f"negative mutation accepted: {key}")
    candidate = copy.deepcopy(record)
    candidate["artifact"]["archive_sha256"] = "0" * 64
    if not validate(candidate, expected):
        errors.append("negative mutation accepted: archive_sha256")
    if errors:
        raise SystemExit("Reader HTML release-record validation failed:\n - " + "\n - ".join(errors))
    print(
        f"Reader HTML release record passed: {record['release_id']}, exact {record['artifact']['archive_sha256'][:12]} archive, "
        "one approved format, zero selected-format blockers, no support movement, and 5 rejecting mutations."
    )


if __name__ == "__main__":
    main()
