#!/usr/bin/env python3
"""Validate the exact v2 EPUB artifact and its honest blocked disposition."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

from audit_post_v2_3_reader_epub_artifact import observe
from build_canonical_public_status import validate_against_schema


ROOT = Path(__file__).resolve().parents[1]
DISPOSITION = ROOT / "editions/reader_manuscript/v2_0/epub_disposition.json"
SCHEMA = ROOT / "schemas/reader_format_disposition.schema.json"
PROFILE = ROOT / "editions/reader_manuscript/v2_0/text_format_profile.json"
MATRIX = ROOT / "editions/reader_manuscript/v2_0/format_review_matrix.json"
STATUS = ROOT / "roadmap_records/post_v2_3_handoff_reader_formats_and_evidence_renewal_status.json"
STRUCTURAL = ROOT / "editions/reader_manuscript/v2_0/epub_structural_inspection.json"
APPLICATION = ROOT / "editions/reader_manuscript/v2_0/epub_application_review.json"
REPRODUCIBILITY = ROOT / "editions/reader_manuscript/v2_0/epub_reproducibility.json"
ROADMAP = ROOT / "docs/post_v2_3_handoff_reader_formats_and_evidence_renewal_roadmap.md"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot() -> dict:
    disposition = load(DISPOSITION)
    artifact = ROOT / disposition["artifact"]["path"]
    return {
        "disposition": disposition,
        "schema": load(SCHEMA),
        "profile": load(PROFILE),
        "matrix": load(MATRIX),
        "status": load(STATUS),
        "structural": load(STRUCTURAL),
        "application": load(APPLICATION),
        "reproducibility": load(REPRODUCIBILITY),
        "roadmap": ROADMAP.read_text(encoding="utf-8"),
        "artifact_path": artifact,
        "artifact_sha256": sha256(artifact),
        "artifact_bytes": artifact.stat().st_size,
        "profile_sha256": sha256(PROFILE),
        "structural_sha256": sha256(STRUCTURAL),
        "application_sha256": sha256(APPLICATION),
        "reproducibility_sha256": sha256(REPRODUCIBILITY),
        "observed_structural": observe(artifact),
    }


def semantic_errors(data: dict) -> list[str]:
    errors = validate_against_schema(data["disposition"], data["schema"], str(DISPOSITION.relative_to(ROOT)))
    disposition = data["disposition"]
    artifact = disposition.get("artifact", {})
    if disposition.get("decision") != "blocked":
        errors.append("EPUB disposition must remain blocked until exact Apple Books inspection passes")
    if artifact.get("sha256") != data["artifact_sha256"] or artifact.get("bytes") != data["artifact_bytes"]:
        errors.append("EPUB disposition artifact digest or byte count drifted")
    if disposition.get("profile", {}).get("sha256") != data["profile_sha256"]:
        errors.append("EPUB disposition profile digest drifted")

    evidence = {row.get("kind"): row for row in disposition.get("inspection_evidence", [])}
    structural_ref = evidence.get("all_member_and_all_xhtml_structural_inspection", {})
    application_ref = evidence.get("apple_books_application_inspection", {})
    if structural_ref.get("sha256") != data["structural_sha256"]:
        errors.append("EPUB structural evidence digest drifted")
    if application_ref.get("sha256") != data["application_sha256"]:
        errors.append("EPUB application evidence digest drifted")
    if disposition.get("reproducibility", {}).get("sha256") != data["reproducibility_sha256"]:
        errors.append("EPUB reproducibility evidence digest drifted")
    if data["structural"] != data["observed_structural"] or data["structural"].get("errors"):
        errors.append("EPUB tracked structural report is stale or failing")
    expected_counts = {
        "archive_members": 148,
        "xhtml_entries": 62,
        "content_entries": 59,
        "opf_manifest_items": 144,
        "opf_spine_items": 62,
        "chapter_entry_points_checked": 54,
        "internal_hrefs_checked": 1415,
        "images_checked": 79,
        "tables_checked": 23,
    }
    if any(data["structural"].get(key) != value for key, value in expected_counts.items()):
        errors.append("EPUB structural denominator drifted")

    application = data["application"]
    if application.get("state") != "blocked_application_inspection":
        errors.append("EPUB application record launders or loses the blocked state")
    if len(application.get("attempts", [])) != 2 or any(
        row.get("error") != "Sky Computer Use native pipe startup failed"
        for row in application.get("attempts", [])
    ):
        errors.append("EPUB application record lost the two exact failed control attempts")
    if any(not str(value).startswith("not_performed_") for value in application.get("application_checks", {}).values()):
        errors.append("EPUB application record claims an unobserved application check")
    if application.get("cleared_blockers"):
        errors.append("EPUB application record clears a blocker without application evidence")

    reproducibility = data["reproducibility"]
    replay_digests = [row.get("canonical_sha256") for row in reproducibility.get("replays", [])]
    if (
        reproducibility.get("state") != "exact_replay_passed"
        or reproducibility.get("exact_replay_equal") is not True
        or replay_digests != [data["artifact_sha256"], data["artifact_sha256"]]
    ):
        errors.append("EPUB exact replay evidence is absent or inconsistent")
    if reproducibility.get("frozen_inputs", {}).get("text_format_profile_sha256") != data["profile_sha256"]:
        errors.append("EPUB reproducibility record is not bound to the current frozen profile")

    profile_epub = data["profile"].get("formats", {}).get("epub", {})
    if profile_epub.get("state") != "blocked_application_inspection_after_exact_structural_candidate":
        errors.append("EPUB profile state disagrees with the blocked disposition")
    if profile_epub.get("exact_artifact_sha256") != data["artifact_sha256"]:
        errors.append("EPUB profile is not bound to the exact artifact")
    pinned = data["profile"].get("shared_profile", {}).get("mermaid_policy", {}).get("epub_pinned_raster_members", [])
    if len(pinned) != 2:
        errors.append("EPUB profile lost its two diagnosed nondeterministic raster pins")
    else:
        for row in pinned:
            reference = ROOT / row.get("reference", "")
            if not reference.is_file() or sha256(reference) != row.get("sha256"):
                errors.append(f"EPUB pinned raster reference drifted: {row.get('reference')}")

    matrix_epub = data["matrix"].get("formats", {}).get("epub", {})
    status_epub = next(
        (row for row in data["status"].get("reader_formats", []) if row.get("format") == "epub"), {}
    )
    m3 = next((row for row in data["status"].get("milestones", []) if row.get("id") == "M3"), {})
    if matrix_epub.get("state") != "blocked" or status_epub.get("state") != "blocked":
        errors.append("EPUB matrix or roadmap state disagrees with the blocked disposition")
    if m3.get("state") != "completed":
        errors.append("M3 is not terminal despite the exact EPUB disposition")
    if "M3 completed 2026-07-13 with a blocked EPUB disposition" not in data["roadmap"]:
        errors.append("roadmap lacks the exact M3 completion boundary")
    if disposition.get("support_state_effect") != "none" or disposition.get("release_effect") != "none":
        errors.append("EPUB disposition invents support or release effect")
    return errors


def main() -> None:
    data = snapshot()
    errors = semantic_errors(data)
    if errors:
        raise SystemExit("EPUB disposition validation failed:\n - " + "\n - ".join(errors))

    controls = []
    mutations = [
        lambda d: d["disposition"].__setitem__("decision", "approved_exact_local_artifact"),
        lambda d: d["disposition"]["artifact"].__setitem__("sha256", "0" * 64),
        lambda d: d["structural"].__setitem__("errors", ["injected failure"]),
        lambda d: d["application"].__setitem__("state", "passed_apple_books"),
        lambda d: d["reproducibility"].__setitem__("exact_replay_equal", False),
        lambda d: next(row for row in d["status"]["milestones"] if row["id"] == "M3").__setitem__("state", "pending"),
        lambda d: d["disposition"].__setitem__("support_state_effect", "prototype-backed"),
    ]
    for mutation in mutations:
        changed = copy.deepcopy(data)
        mutation(changed)
        controls.append(bool(semantic_errors(changed)))
    if not all(controls):
        raise SystemExit("EPUB disposition validation failed: a negative control was accepted")
    print(
        "EPUB disposition validation passed: exact replayed artifact, deep structural audit, "
        "honest Apple Books blocker, seven rejecting controls, no support or release effect."
    )


if __name__ == "__main__":
    main()
