#!/usr/bin/env python3
"""Idempotently register the Manim generation-2 production-ledger gate."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_manim_v2_production_ledger.py"
ARTIFACTS = [
    "visual_edition/manim_v2_production_ledger.json",
    "schemas/manim_v2_production_ledger.schema.json",
    "schemas/manim_beat_plan.schema.json",
    "schemas/manim_experience_review.schema.json",
    "schemas/narration_toolchain.schema.json",
    "scripts/sync_manim_v2_production_ledger.py",
    "scripts/validate_manim_v2_production_ledger.py",
    "scripts/register_manim_v2_production_validator.py",
    "skills/asi-stack-manim-videos/SKILL.md",
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
    "skills/asi-stack-manim-videos/scripts/sample_video_beats.py",
    "visual_edition/chapters/asi-is-a-stack-not-a-model/generation-2/narration.txt",
    "visual_edition/chapters/asi-is-a-stack-not-a-model/generation-2/beat_plan.json",
    "visual_edition/chapters/asi-is-a-stack-not-a-model/generation-2/storyboard.md",
    "visual_edition/chapters/asi-is-a-stack-not-a-model/generation-2/captions.vtt",
    "visual_edition/chapters/asi-is-a-stack-not-a-model/generation-2/scene.py",
    "visual_edition/chapters/asi-is-a-stack-not-a-model/generation-2/reviews/animatic-r1.json",
    "visual_edition/chapters/asi-is-a-stack-not-a-model/generation-2/reviews/animatic-r2.json",
    "book_structure.json",
    "visual_edition/manifest.json",
    "visual_edition/youtube_preview_bindings.json",
    "visual_edition/narration_toolchain.json",
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
    unit.update({
        "execution_tier": "pr",
        "validation_class": "publication_gate",
        "input_contract": (
            "The canonical manifest-driven chapter set, preserved generation-one master and preview "
            "identities, tracked generation-two authoring standard, beat-plan and "
            "experience-review schemas, chapter-specific production artifacts, and "
            "fail-closed YouTube and Quarto lifecycle states."
        ),
        "input_artifacts": ARTIFACTS,
        "output_contract": (
            "Reject chapter/order/cohort drift, fabricated predecessors, stale chapter, narration, "
            "toolchain, or authoring digests, narration and beat-plan disagreement, review-score "
            "averaging, missing cold transfer or frame sampling, unqualified alignment, master "
            "or receipt identity gaps, premature YouTube/Quarto advancement, predecessor "
            "erasure, support movement, and publication invention."
        ),
        "output_assertions": [
            "one generation-two target per canonical chapter in canonical order",
            "all canonical targets partition exactly into four lifecycle cohorts",
            "historical predecessors preserved and new chapters represented with null predecessors",
            "material chapter, narration, standard, schema, or toolchain changes reopen downstream gates",
            "exact narration-to-beat-plan agreement for every passing beat plan",
            "all eleven experience dimensions individually at least four",
            "five or more frame samples per beat and cold comprehension plus transfer at release",
            "picture-and-sound lock remains closed until forced alignment is qualified",
            "no unresolved defects on a passing experience review",
            "accepted masters bind exact render receipts and digests",
            "YouTube and Quarto states cannot advance before acceptance and reconciliation",
            "support, release, and publication effects none until exact receipts exist",
            "nine representative custody and lifecycle mutations reject",
        ],
        "claim_scope": (
            "Generation-two visual-derivative identity, production-stage custody, review-gate "
            "integrity, predecessor preservation, and publication sequencing only."
        ),
        "negative_controls": "validator_owned_nine_identity_script_alignment_gate_score_and_publication_mutations",
        "negative_control_cases": [
            "chapter deletion",
            "predecessor identity erasure",
            "narration identity drift",
            "rejected sub-four review promoted to pass",
            "picture-and-sound lock before alignment qualification",
            "acceptance before prerequisite gates",
            "YouTube advancement before acceptance",
            "Quarto advancement before public-current YouTube identity",
            "support invention",
        ],
        "prohibited_inference": (
            "A valid plan, scene, animatic, review, master, upload, playlist item, or embed "
            "does not prove learning, chapter truth, model quality, safety, SOTA, AGI, ASI, "
            "or authority for an unrecorded external mutation."
        ),
        "contract_precision": "exact",
        "semantic_review_state": "tracked_v2_manifest_dynamic_script_digest_alignment_learning_and_fail_closed_publication_contract",
    })
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
