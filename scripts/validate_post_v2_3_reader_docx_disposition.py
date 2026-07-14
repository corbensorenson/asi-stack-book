#!/usr/bin/env python3
"""Validate the exact v2 DOCX artifact and bounded local approval."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

from audit_post_v2_3_reader_docx_artifact import observe
from build_canonical_public_status import validate_against_schema


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "editions/reader_manuscript/v2_0"
DISPOSITION = BASE / "docx_disposition.json"
SCHEMA = ROOT / "schemas/reader_format_disposition.schema.json"
PROFILE = BASE / "text_format_profile.json"
MATRIX = BASE / "format_review_matrix.json"
STATUS = ROOT / "roadmap_records/post_v2_3_handoff_reader_formats_and_evidence_renewal_status.json"
STRUCTURAL = BASE / "docx_package_and_page_inspection.json"
VISUAL = BASE / "docx_visual_review.json"
APPLICATION = BASE / "docx_application_review.json"
REPRODUCIBILITY = BASE / "docx_reproducibility.json"
ROADMAP = ROOT / "docs/post_v2_3_handoff_reader_formats_and_evidence_renewal_roadmap.md"
RENDERER = ROOT / "scripts/render_curated_reader_formats.py"
EXTRACTOR = ROOT / "scripts/extract_rendered_mermaid_svgs.js"
LOCAL_RENDER = ROOT / "build/post_v2_3_docx_review/repaired_exact"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot() -> dict:
    disposition = load(DISPOSITION)
    artifact = ROOT / disposition["artifact"]["path"]
    replay_available = (
        (LOCAL_RENDER / f"{artifact.stem}.pdf").is_file()
        and (LOCAL_RENDER / "page-1.png").is_file()
    )
    return {
        "disposition": disposition,
        "schema": load(SCHEMA),
        "profile": load(PROFILE),
        "matrix": load(MATRIX),
        "status": load(STATUS),
        "structural": load(STRUCTURAL),
        "visual": load(VISUAL),
        "application": load(APPLICATION),
        "reproducibility": load(REPRODUCIBILITY),
        "roadmap": ROADMAP.read_text(encoding="utf-8"),
        "artifact_path": artifact,
        "artifact_sha256": sha256(artifact),
        "artifact_bytes": artifact.stat().st_size,
        "profile_sha256": sha256(PROFILE),
        "renderer_sha256": sha256(RENDERER),
        "extractor_sha256": sha256(EXTRACTOR),
        "structural_sha256": sha256(STRUCTURAL),
        "visual_sha256": sha256(VISUAL),
        "application_sha256": sha256(APPLICATION),
        "reproducibility_sha256": sha256(REPRODUCIBILITY),
        "observed_structural": observe(artifact, LOCAL_RENDER) if replay_available else None,
        "replay_mode": "full_local_package_and_page_replay" if replay_available else "exact_artifact_and_digest_bound_report_validation",
    }


def semantic_errors(data: dict) -> list[str]:
    errors = validate_against_schema(data["disposition"], data["schema"], str(DISPOSITION.relative_to(ROOT)))
    disposition = data["disposition"]
    artifact = disposition.get("artifact", {})
    if disposition.get("decision") != "approved_exact_local_artifact":
        errors.append("DOCX disposition must approve only the exact local artifact")
    if disposition.get("blockers"):
        errors.append("approved DOCX disposition retains a format blocker")
    if artifact.get("sha256") != data["artifact_sha256"] or artifact.get("bytes") != data["artifact_bytes"]:
        errors.append("DOCX disposition artifact digest or byte count drifted")
    if disposition.get("profile", {}).get("sha256") != data["profile_sha256"]:
        errors.append("DOCX disposition profile digest drifted")

    evidence = {row.get("kind"): row for row in disposition.get("inspection_evidence", [])}
    expected_evidence = {
        "ooxml_package_and_page_automation": (data["structural_sha256"], "passed_package_and_page_automation_visual_review_pending"),
        "all_page_internal_visual_review": (data["visual_sha256"], "passed_internal_page_complete_review"),
        "pinned_libreoffice_writer_application_engine_review": (data["application_sha256"], "passed_pinned_libreoffice_headless_application_engine_review"),
    }
    for kind, (digest, state) in expected_evidence.items():
        row = evidence.get(kind, {})
        if row.get("sha256") != digest or row.get("state") != state:
            errors.append(f"DOCX inspection evidence drifted: {kind}")
    if disposition.get("reproducibility", {}).get("sha256") != data["reproducibility_sha256"]:
        errors.append("DOCX reproducibility evidence digest drifted")

    structural = data["structural"]
    if data["observed_structural"] is not None and structural != data["observed_structural"]:
        errors.append("DOCX tracked package/page report is stale or failing")
    if structural.get("errors"):
        errors.append("DOCX package/page report records a failure")
    if structural.get("sha256") != data["artifact_sha256"] or structural.get("bytes") != data["artifact_bytes"]:
        errors.append("DOCX package/page report is not bound to the exact artifact")
    package = structural.get("package", {})
    expected_package = {
        "zip_members": 95,
        "xml_members_parsed": 16,
        "style_definitions": 196,
        "paragraphs": 7878,
        "list_paragraphs": 3405,
        "tables": 33,
        "drawings": 79,
        "drawing_descriptions": 79,
        "media_entries": 79,
        "hyperlinks": 274,
        "bookmarks": 1169,
        "native_omml_equations": 0,
    }
    if any(package.get(key) != value for key, value in expected_package.items()):
        errors.append("DOCX OOXML denominator drifted")
    if package.get("missing_required_members") or package.get("unresolved_relationship_targets") or package.get("missing_drawing_descriptions"):
        errors.append("DOCX package has an unresolved member, relationship, or drawing description")
    if package.get("chapter_titles_checked_in_order") != 54 or package.get("heading_level_jumps") != 0:
        errors.append("DOCX chapter order or heading hierarchy drifted")
    if package.get("core_properties", {}).get("language") != "en-US" or package.get("style_languages") != ["en-US"]:
        errors.append("DOCX language metadata drifted")
    conversion = structural.get("libreoffice_conversion", {})
    if conversion.get("pages") != 644 or conversion.get("chapter_titles_checked_in_order") != 54:
        errors.append("DOCX LibreOffice page or chapter denominator drifted")
    if conversion.get("tagged") != "yes" or conversion.get("encrypted") != "no" or conversion.get("replacement_characters") != 0:
        errors.append("DOCX LibreOffice conversion boundary drifted")
    raster = structural.get("raster", {})
    if raster.get("pages_checked") != 644 or len(raster.get("contact_sheets", [])) != 33:
        errors.append("DOCX raster denominator drifted")
    if any(raster.get(key) for key in ("blank_pages", "low_ink_pages", "near_edge_pages")):
        errors.append("DOCX raster report contains an unresolved page defect")

    visual = data["visual"]
    page_review = visual.get("page_complete_review", {})
    if visual.get("state") != "passed_internal_page_complete_review" or visual.get("residual_defects"):
        errors.append("DOCX visual review is not terminally passed")
    if page_review.get("pages") != 644 or page_review.get("contact_sheets") != 33 or page_review.get("every_page_reviewed") is not True:
        errors.append("DOCX page-complete visual review denominator drifted")
    if visual.get("automated_report", {}).get("sha256") != data["structural_sha256"]:
        errors.append("DOCX visual review is not bound to the automated report")
    repairs = visual.get("repairs", [])
    if len(repairs) != 1 or repairs[0].get("canonical_prose_changed") is not False:
        errors.append("DOCX rejected-candidate glossary repair boundary drifted")

    application = data["application"]
    observed = application.get("observed_conversion", {})
    if application.get("state") != "passed_pinned_libreoffice_headless_application_engine_review":
        errors.append("DOCX pinned application-engine review is not passed")
    if observed.get("pages") != 644 or observed.get("application_engine_path_passed") is not True:
        errors.append("DOCX application-engine denominator drifted")
    if application.get("remaining_blockers"):
        errors.append("DOCX application record retains a blocker")
    if application.get("application_checks", {}).get("Microsoft_Word") != "not_performed":
        errors.append("DOCX application record launders Microsoft Word review")

    reproducibility = data["reproducibility"]
    replay_digests = [row.get("canonical_sha256") for row in reproducibility.get("replays", [])]
    if reproducibility.get("state") != "exact_replay_passed" or reproducibility.get("exact_replay_equal") is not True or replay_digests != [data["artifact_sha256"], data["artifact_sha256"]]:
        errors.append("DOCX exact replay evidence is absent or inconsistent")
    frozen = reproducibility.get("frozen_inputs", {})
    if frozen.get("text_format_profile_sha256") != data["profile_sha256"]:
        errors.append("DOCX reproducibility is not bound to the current profile")
    if frozen.get("renderer_sha256") != data["renderer_sha256"] or frozen.get("extractor_sha256") != data["extractor_sha256"]:
        errors.append("DOCX reproducibility renderer or extractor digest drifted")
    canonical = reproducibility.get("canonicalization", {})
    if canonical.get("empty_image_descriptions_after_repair") != 0 or canonical.get("member_count") != 95:
        errors.append("DOCX canonicalization boundary drifted")

    profile_docx = data["profile"].get("formats", {}).get("docx", {})
    if profile_docx.get("state") != "approved_exact_local_artifact_after_package_application_engine_page_and_replay_review":
        errors.append("DOCX profile state disagrees with the disposition")
    if profile_docx.get("exact_artifact_sha256") != data["artifact_sha256"]:
        errors.append("DOCX profile is not bound to the exact artifact")
    if profile_docx.get("layout_fallback", {}).get("canonical_source_restored_after_render") is not True:
        errors.append("DOCX profile lost the bounded glossary fallback")

    matrix_docx = data["matrix"].get("formats", {}).get("docx", {})
    status_docx = next((row for row in data["status"].get("reader_formats", []) if row.get("format") == "docx"), {})
    p1 = next((row for row in data["status"].get("priorities", []) if row.get("id") == "P1"), {})
    m5 = next((row for row in data["status"].get("milestones", []) if row.get("id") == "M5"), {})
    if matrix_docx.get("state") != "approved_exact_local_artifact" or status_docx.get("state") != "approved_exact_local_artifact":
        errors.append("DOCX matrix or roadmap format state disagrees with approval")
    if p1.get("state") != "completed" or m5.get("state") != "completed":
        errors.append("P1 or M5 is not terminal despite all three format dispositions")
    if "M5 completed 2026-07-13 with an `approved_exact_local_artifact` DOCX" not in data["roadmap"]:
        errors.append("roadmap lacks the exact M5 completion boundary")
    if disposition.get("support_state_effect") != "none" or disposition.get("release_effect") != "none":
        errors.append("DOCX disposition invents support or release effect")
    return errors


def main() -> None:
    data = snapshot()
    errors = semantic_errors(data)
    if errors:
        raise SystemExit("DOCX disposition validation failed:\n - " + "\n - ".join(errors))
    mutations = [
        lambda d: d["disposition"].__setitem__("decision", "approved_public_artifact"),
        lambda d: d["disposition"]["artifact"].__setitem__("sha256", "0" * 64),
        lambda d: d["structural"]["package"].__setitem__("drawings", 78),
        lambda d: d["structural"]["raster"].__setitem__("blank_pages", [525]),
        lambda d: d["visual"]["page_complete_review"].__setitem__("every_page_reviewed", False),
        lambda d: d["application"]["application_checks"].__setitem__("Microsoft_Word", "passed"),
        lambda d: d["reproducibility"].__setitem__("exact_replay_equal", False),
        lambda d: next(row for row in d["status"]["milestones"] if row["id"] == "M5").__setitem__("state", "pending"),
        lambda d: d["disposition"].__setitem__("support_state_effect", "prototype-backed"),
    ]
    controls = []
    for mutation in mutations:
        changed = copy.deepcopy(data)
        mutation(changed)
        controls.append(bool(semantic_errors(changed)))
    if not all(controls):
        raise SystemExit("DOCX disposition validation failed: a negative control was accepted")
    print(
        "DOCX disposition validation passed: exact 644-page office-engine artifact, "
        "page-complete review, exact replay, nine rejecting controls, no support or "
        f"release effect; verification mode={data['replay_mode']}."
    )


if __name__ == "__main__":
    main()
