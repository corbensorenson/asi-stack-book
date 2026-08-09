#!/usr/bin/env python3
"""Idempotently register the Manim generation-2 production-ledger gate."""

from __future__ import annotations

import json
from pathlib import Path

from validate_manim_v2_production_ledger import EXPECTED_REJECTING_CONTROL_COUNT


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_manim_v2_production_ledger.py"
ARTIFACTS = [
    "visual_edition/manim_v2_production_ledger.json",
    "schemas/manim_v2_production_ledger.schema.json",
    "schemas/manim_treatment.schema.json",
    "schemas/manim_beat_plan.schema.json",
    "schemas/manim_experience_review.schema.json",
    "schemas/manim_review_context_manifest.schema.json",
    "schemas/manim_av_diagnostics.schema.json",
    "schemas/manim_frame_sample_manifest.schema.json",
    "schemas/manim_render_receipt.schema.json",
    "schemas/manim_sandbox_policy_receipt.schema.json",
    "schemas/manim_primitive_regression.schema.json",
    "schemas/manim_toolchain.schema.json",
    "schemas/narration_toolchain.schema.json",
    "scripts/sync_manim_v2_production_ledger.py",
    "scripts/validate_manim_v2_production_ledger.py",
    "scripts/register_manim_v2_production_validator.py",
    "scripts/render_visual_narration.py",
    "scripts/transcribe_visual_narrations.py",
    "scripts/build_visual_captions_from_narration_receipt.py",
    "scripts/validate_visual_narration.py",
    "scripts/validate_visual_master.py",
    "skills/asi-stack-manim-videos/SKILL.md",
    "skills/asi-stack-manim-videos/agents/openai.yaml",
    "skills/asi-stack-manim-videos/references/art-direction-and-motion.md",
    "skills/asi-stack-manim-videos/references/asi-stack-pipeline.md",
    "skills/asi-stack-manim-videos/references/audio-and-accessibility.md",
    "skills/asi-stack-manim-videos/references/experience-review.md",
    "skills/asi-stack-manim-videos/references/learning-and-engagement.md",
    "skills/asi-stack-manim-videos/references/manim-patterns.md",
    "skills/asi-stack-manim-videos/references/research-basis.md",
    "skills/asi-stack-manim-videos/references/writing-and-story.md",
    "skills/asi-stack-manim-videos/scripts/audit_video_plan.py",
    "skills/asi-stack-manim-videos/scripts/audit_av_experience.py",
    "skills/asi-stack-manim-videos/scripts/audit_scene_source.py",
    "skills/asi-stack-manim-videos/scripts/render_scene_isolated.py",
    "skills/asi-stack-manim-videos/scripts/build_final_render_receipt.py",
    "skills/asi-stack-manim-videos/scripts/audit_primitive_regression.py",
    "skills/asi-stack-manim-videos/scripts/build_caption_review_sheet.py",
    "skills/asi-stack-manim-videos/scripts/sample_video_beats.py",
    "book_structure.json",
    "visual_edition/manifest.json",
    "visual_edition/visual_grammar.json",
    "visual_edition/toolchain.json",
    "visual_edition/lib/asi_visuals.py",
    "visual_edition/primitive_regression_manifest.json",
    "visual_edition/tests/primitive_regression_scenes.py",
    "visual_edition/tests/control_data/asi_visuals_v1.npz",
    "visual_edition/youtube_preview_bindings.json",
    "visual_edition/narration_toolchain.json",
    "visual_edition/narration_requirements.lock.txt",
    "visual_edition/narration_pronunciations.json",
]


def main() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    matches = [
        row for row in registry["units"]
        if row.get("script") == SCRIPT and row.get("args", []) == []
    ]
    if matches:
        unit = matches[0]
    else:
        order = len(registry["units"]) + 1
        unit = {
            "id": f"{SCRIPT}:{order}",
            "order": order,
            "script": SCRIPT,
            "args": [],
        }
        registry["units"].append(unit)
    previous_artifacts = set(unit.get("input_artifacts", []))
    unit.update({
        "execution_tier": "pr",
        "validation_class": "publication_gate",
        "input_contract": (
            "The canonical manifest-driven chapter set, preserved generation-one master and preview "
            "identities, tracked generation-two authoring standard, treatment, beat-plan, "
            "and experience-review schemas, chapter-specific production artifacts, and "
            "fail-closed YouTube and Quarto lifecycle states."
        ),
        "input_artifacts": ARTIFACTS,
        "output_contract": (
            "Reject chapter/order/cohort drift, fabricated predecessors, stale chapter, treatment, "
            "narration, plan, toolchain, or authoring digests, unapproved scripts, estimated final "
            "timing, review-score averaging, context-leaked cold review, fake sample coverage, "
            "missing raw transfer evidence, unqualified alignment, unsafe scene source, unreviewed shared-primitive input or baseline drift, "
            "unbound scene/grammar/toolchain, widened local helper import, non-isolated or malformed render receipt, master "
            "or receipt identity gaps, premature YouTube/Quarto advancement, predecessor "
            "erasure, support movement, and publication invention."
        ),
        "output_assertions": [
            "one generation-two target per canonical chapter in canonical order",
            "all canonical targets partition exactly into four lifecycle cohorts",
            "historical predecessors preserved and new chapters represented with null predecessors",
            "material chapter, treatment, narration, standard, schema, or toolchain changes reopen downstream gates",
            "exact treatment and narration identity for every passing beat plan",
            "exact scene, caption, transcript, thumbnail, visual-grammar, toolchain, primitive-library, and render-receipt identity",
            "static scene-source preflight plus a runner-produced, schema-valid, network-denied, credential-free, constrained-write render receipt",
            "portable content-addressed baseline custody and source coverage for every public shared primitive factory; graphical replay remains a pinned-macOS qualification",
            "read-aloud, truth, and visualizability review before script approval",
            "block timing before animatic and manually reviewed forced alignment before lock",
            "all applicable experience dimensions individually at least four with timestamped evidence",
            "manifest-proven frame samples for every beat and zero unresolved interpolation defects",
            "independent source-aware claim review and context-isolated cold comprehension plus transfer",
            "no unresolved defects on a passing experience review",
            "accepted masters bind exact render receipts and digests",
            "YouTube and Quarto states cannot advance before acceptance and reconciliation",
            "support, release, and publication effects none until exact receipts exist",
            f"{EXPECTED_REJECTING_CONTROL_COUNT} representative source, geometry, sandbox, narration-custody, render-receipt, media-metadata, identity, timing, sampling, independence, and lifecycle controls reject",
        ],
        "claim_scope": (
            "Generation-two visual-derivative identity, production-stage custody, review-gate "
            "integrity, predecessor preservation, and publication sequencing only."
        ),
        "negative_controls": f"validator_owned_{EXPECTED_REJECTING_CONTROL_COUNT}_source_geometry_sandbox_narration_custody_render_receipt_media_metadata_identity_treatment_alignment_review_sampling_independence_and_publication_controls",
        "negative_control_cases": [
            "chapter deletion",
            "predecessor identity erasure",
            "narration identity drift",
            "scene identity drift",
            "treatment gate promoted without a treatment",
            "picture-and-sound lock before alignment qualification",
            "acceptance before prerequisite gates",
            "YouTube advancement before acceptance",
            "Quarto advancement before public-current YouTube identity",
            "support invention",
            "required viewing mode failure",
            "cold-review context leakage",
            "review artifact digest drift",
            "false sample coverage",
            "unresolved interpolation defect",
            "author self-review in cold lane",
            "answer-key exposure",
            "source-fidelity score without source access",
            "source-aware critic involved in implementation",
            "post-hoc cold-review success criteria",
            "future release artifact injected into an animatic review",
            "final-mix score manufactured during animatic review",
            "cold-proxy learning result manufactured in a source-aware review",
            "narration renderer identity drift",
            "narration toolchain identity drift",
            "narration model-revision drift",
            "narration FFmpeg-normalizer identity drift",
            "narration audio identity drift",
            "narration duration drift",
            "narration text drift",
            "narration performance-block mismatch",
            "failed narration verification report",
            "failed narration verification check",
            "narration verification WER ceiling violation",
            "unsafe scene import, dynamic execution, filesystem effect, and unseeded randomness",
            "unbound local scene-helper import",
            "LaTeX constructor before toolchain qualification",
            "primitive pixel drift and primitive frame-count drift",
            "sandbox network or credential declaration widening",
            "sandbox repository-write-root widening",
            "sandbox runner or source-preflight identity drift",
            "release render-command weakening",
            "release mux-command widening",
            "render-seed receipt drift",
            "isolated master identity drift",
            "draft sandbox audio or release-profile laundering",
            "draft render-command weakening",
            "draft reviewed-animatic identity drift",
            "final render-receipt source-commit drift",
            "final render-receipt runner-binding drift",
            "final render-receipt compiler-binding drift",
            "final render-receipt network declaration widening",
            "final render-receipt master identity drift",
            "final render-receipt duration drift",
            "final render-receipt unresolved asset custody",
            "final receipt metadata missing audio stream",
            "final receipt metadata frame-rate drift",
            "final receipt metadata pixel-format drift",
            "final receipt metadata sample-rate drift",
        ],
        "prohibited_inference": (
            "A valid plan, scene, animatic, review, master, upload, playlist item, or embed "
            "does not prove learning, chapter truth, model quality, safety, SOTA, AGI, ASI, "
            "or authority for an unrecorded external mutation."
        ),
        "contract_precision": "exact",
        "semantic_review_state": "tracked_v3_treatment_script_timing_bound_dual_review_sampling_and_fail_closed_publication_contract",
    })
    for artifact in previous_artifacts - set(ARTIFACTS):
        used_elsewhere = any(
            row is not unit and artifact in row.get("input_artifacts", [])
            for row in registry["units"]
        )
        if not used_elsewhere and artifact in registry["required_artifacts"]:
            registry["required_artifacts"].remove(artifact)
    for artifact in ARTIFACTS:
        if artifact not in registry["required_artifacts"]:
            registry["required_artifacts"].append(artifact)
    registry["summary"] = {
        "required_artifact_count": len(registry["required_artifacts"]),
        "unit_count": len(registry["units"]),
    }
    REGISTRY.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(
        f"registered {SCRIPT}: {registry['summary']['unit_count']} units, "
        f"{registry['summary']['required_artifact_count']} artifacts"
    )


if __name__ == "__main__":
    main()
