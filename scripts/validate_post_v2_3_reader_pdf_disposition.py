#!/usr/bin/env python3
"""Validate the exact v2 PDF artifact and its honest blocked disposition."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import shutil

from audit_post_v2_3_reader_pdf_artifact import observe
from build_canonical_public_status import validate_against_schema


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "editions/reader_manuscript/v2_0"
DISPOSITION = BASE / "pdf_disposition.json"
SCHEMA = ROOT / "schemas/reader_format_disposition.schema.json"
PROFILE = BASE / "text_format_profile.json"
MATRIX = BASE / "format_review_matrix.json"
STATUS = ROOT / "roadmap_records/post_v2_3_handoff_reader_formats_and_evidence_renewal_status.json"
STRUCTURAL = BASE / "pdf_structural_and_page_inspection.json"
VISUAL = BASE / "pdf_visual_review.json"
APPLICATION = BASE / "pdf_application_review.json"
REPRODUCIBILITY = BASE / "pdf_reproducibility.json"
ROADMAP = ROOT / "docs/post_v2_3_handoff_reader_formats_and_evidence_renewal_roadmap.md"
RENDERER = ROOT / "scripts/render_curated_reader_formats.py"
EXTRACTOR = ROOT / "scripts/extract_rendered_mermaid_svgs.js"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot() -> dict:
    disposition = load(DISPOSITION)
    artifact = ROOT / disposition["artifact"]["path"]
    poppler_commands = ("pdffonts", "pdftotext", "pdftoppm")
    replay_available = all(shutil.which(command) for command in poppler_commands)
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
        "observed_structural": observe(artifact) if replay_available else None,
        "structural_replay_mode": (
            "full_local_poppler_replay" if replay_available else "exact_artifact_and_digest_bound_report_validation"
        ),
    }


def semantic_errors(data: dict) -> list[str]:
    errors = validate_against_schema(
        data["disposition"], data["schema"], str(DISPOSITION.relative_to(ROOT))
    )
    disposition = data["disposition"]
    artifact = disposition.get("artifact", {})
    if disposition.get("decision") != "blocked":
        errors.append("PDF disposition must remain blocked until exact Preview inspection passes")
    if artifact.get("sha256") != data["artifact_sha256"] or artifact.get("bytes") != data["artifact_bytes"]:
        errors.append("PDF disposition artifact digest or byte count drifted")
    if disposition.get("profile", {}).get("sha256") != data["profile_sha256"]:
        errors.append("PDF disposition profile digest drifted")

    evidence = {row.get("kind"): row for row in disposition.get("inspection_evidence", [])}
    evidence_expectations = {
        "all_page_structural_text_bbox_and_raster_inspection": (data["structural_sha256"], "passed_automated_page_complete_visual_review_pending"),
        "all_page_and_native_resolution_diagram_visual_review": (data["visual_sha256"], "passed_internal_page_complete_and_native_diagram_review"),
        "preview_application_inspection": (data["application_sha256"], "blocked_application_inspection"),
    }
    for kind, (digest, state) in evidence_expectations.items():
        row = evidence.get(kind, {})
        if row.get("sha256") != digest or row.get("state") != state:
            errors.append(f"PDF inspection evidence drifted: {kind}")
    if disposition.get("reproducibility", {}).get("sha256") != data["reproducibility_sha256"]:
        errors.append("PDF reproducibility evidence digest drifted")

    structural = data["structural"]
    if data["observed_structural"] is not None and structural != data["observed_structural"]:
        errors.append("PDF tracked structural/page report is stale or failing")
    if structural.get("errors"):
        errors.append("PDF tracked structural/page report records a failure")
    if structural.get("sha256") != data["artifact_sha256"] or structural.get("bytes") != data["artifact_bytes"]:
        errors.append("PDF tracked structural/page report is not bound to the exact artifact")
    expected = {
        "pages": 565,
        "outline_entries": 1142,
        "named_destinations": 1142,
        "link_annotations": 1418,
        "unresolved_link_annotations": 0,
    }
    if any(structural.get("pdf_objects", {}).get(key) != value for key, value in expected.items()):
        errors.append("PDF structural denominator drifted")
    if structural.get("fonts", {}).get("font_rows") != 4 or structural.get("fonts", {}).get("embedded_no_rows"):
        errors.append("PDF embedded-font evidence drifted")
    if structural.get("text", {}).get("pages_checked") != 565 or structural.get("text", {}).get("chapter_titles_checked_in_order") != 54:
        errors.append("PDF text or chapter-order denominator drifted")
    if structural.get("bbox", {}).get("word_boxes_checked") != 270359 or structural.get("bbox", {}).get("out_of_bounds_word_boxes"):
        errors.append("PDF bbox denominator or bounds result drifted")
    raster = structural.get("raster", {})
    if raster.get("pages_checked") != 565 or len(raster.get("contact_sheets", [])) != 29:
        errors.append("PDF page-raster denominator drifted")
    if any(raster.get(key) for key in ("blank_pages", "low_ink_pages", "near_edge_pages", "risk_pages")):
        errors.append("PDF raster report contains an unresolved page defect")

    visual = data["visual"]
    if visual.get("state") != "passed_internal_page_complete_and_native_diagram_review":
        errors.append("PDF internal visual review is not terminally passed")
    page_review = visual.get("page_complete_review", {})
    diagram_review = visual.get("diagram_review", {})
    if page_review.get("pages") != 565 or page_review.get("contact_sheets") != 29 or page_review.get("every_page_reviewed") is not True:
        errors.append("PDF page-complete visual review denominator drifted")
    if diagram_review.get("generated_diagrams") != 68 or diagram_review.get("native_resolution_contact_sheets") != 17 or diagram_review.get("all_reviewed") is not True:
        errors.append("PDF native-resolution diagram review denominator drifted")
    if diagram_review.get("residual_defects"):
        errors.append("PDF visual review retains an unresolved diagram defect")
    if visual.get("automated_report", {}).get("sha256") != data["structural_sha256"]:
        errors.append("PDF visual review is not bound to the exact automated report")

    application = data["application"]
    if application.get("state") != "blocked_application_inspection":
        errors.append("PDF application record launders or loses the blocked state")
    if len(application.get("attempts", [])) != 2 or any(
        row.get("error") != "Sky Computer Use native pipe startup failed"
        for row in application.get("attempts", [])
    ):
        errors.append("PDF application record lost the two exact failed control attempts")
    if any(not str(value).startswith("not_performed_") for value in application.get("application_checks", {}).values()):
        errors.append("PDF application record claims an unobserved application check")
    if application.get("automation_substitution") is not False or application.get("cleared_blockers"):
        errors.append("PDF application record improperly substitutes automation or clears a blocker")

    reproducibility = data["reproducibility"]
    replay_digests = [row.get("canonical_sha256") for row in reproducibility.get("replays", [])]
    if (
        reproducibility.get("state") != "exact_replay_passed"
        or reproducibility.get("exact_replay_equal") is not True
        or replay_digests != [data["artifact_sha256"], data["artifact_sha256"]]
    ):
        errors.append("PDF exact replay evidence is absent or inconsistent")
    frozen = reproducibility.get("frozen_inputs", {})
    if frozen.get("text_format_profile_sha256") != data["profile_sha256"]:
        errors.append("PDF reproducibility record is not bound to the current frozen profile")
    if frozen.get("renderer_sha256") != data["renderer_sha256"] or frozen.get("extractor_sha256") != data["extractor_sha256"]:
        errors.append("PDF reproducibility renderer or extractor digest drifted")
    pins = frozen.get("pinned_rasters", [])
    if len(pins) != 2:
        errors.append("PDF reproducibility record lost its two diagnosed raster pins")
    else:
        for row in pins:
            reference = ROOT / row.get("reference", "")
            if not reference.is_file() or sha256(reference) != row.get("sha256"):
                errors.append(f"PDF pinned raster reference drifted: {row.get('reference')}")

    profile_pdf = data["profile"].get("formats", {}).get("pdf", {})
    if profile_pdf.get("state") != "blocked_preview_application_inspection_after_exact_structural_visual_replay_candidate":
        errors.append("PDF profile state disagrees with the blocked disposition")
    if profile_pdf.get("exact_artifact_sha256") != data["artifact_sha256"]:
        errors.append("PDF profile is not bound to the exact artifact")
    profile_pins = data["profile"].get("shared_profile", {}).get("mermaid_policy", {}).get("pdf_pinned_raster_references", [])
    if len(profile_pins) != 2:
        errors.append("PDF profile lost its two diagnosed nondeterministic raster pins")

    matrix_pdf = data["matrix"].get("formats", {}).get("pdf", {})
    status_pdf = next((row for row in data["status"].get("reader_formats", []) if row.get("format") == "pdf"), {})
    m4 = next((row for row in data["status"].get("milestones", []) if row.get("id") == "M4"), {})
    if matrix_pdf.get("state") != "blocked" or status_pdf.get("state") != "blocked":
        errors.append("PDF matrix or roadmap state disagrees with the blocked disposition")
    if m4.get("state") != "completed":
        errors.append("M4 is not terminal despite the exact PDF disposition")
    if "M4 completed 2026-07-13 with a blocked PDF disposition" not in data["roadmap"]:
        errors.append("roadmap lacks the exact M4 completion boundary")
    if disposition.get("support_state_effect") != "none" or disposition.get("release_effect") != "none":
        errors.append("PDF disposition invents support or release effect")
    return errors


def main() -> None:
    data = snapshot()
    errors = semantic_errors(data)
    if errors:
        raise SystemExit("PDF disposition validation failed:\n - " + "\n - ".join(errors))

    controls = []
    mutations = [
        lambda d: d["disposition"].__setitem__("decision", "approved_exact_local_artifact"),
        lambda d: d["disposition"]["artifact"].__setitem__("sha256", "0" * 64),
        lambda d: d["structural"]["pdf_objects"].__setitem__("pages", 564),
        lambda d: d["visual"]["page_complete_review"].__setitem__("every_page_reviewed", False),
        lambda d: d["application"].__setitem__("state", "passed_preview"),
        lambda d: d["reproducibility"].__setitem__("exact_replay_equal", False),
        lambda d: next(row for row in d["status"]["milestones"] if row["id"] == "M4").__setitem__("state", "pending"),
        lambda d: d["disposition"].__setitem__("support_state_effect", "prototype-backed"),
    ]
    for mutation in mutations:
        changed = copy.deepcopy(data)
        mutation(changed)
        controls.append(bool(semantic_errors(changed)))
    if not all(controls):
        raise SystemExit("PDF disposition validation failed: a negative control was accepted")
    print(
        "PDF disposition validation passed: exact replayed 565-page artifact, page-complete "
        "automation and internal visual review, honest Preview blocker, eight rejecting controls, "
        f"no support or release effect; structural verification mode={data['structural_replay_mode']}."
    )


if __name__ == "__main__":
    main()
