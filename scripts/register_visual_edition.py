#!/usr/bin/env python3
"""Register the governed P7.3 visual-edition validator."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_visual_edition.py"
EMBED_SCRIPT = "sync_visual_edition_embeds.py"
TOOLCHAIN_SCRIPT = "validate_manim_toolchain.py"
PILOTS = [
    "asi-is-a-stack-not-a-model",
    "capability-replacement-and-rollback",
    "context-transactions-snapshots-mounts-and-taint",
    "replaceable-cognitive-substrates-beyond-transformer-monoculture",
    "living-book-methodology",
]
PACKET_FILES = [
    "packet.json",
    "storyboard.md",
    "scene.py",
    "narration.txt",
    "captions.vtt",
    "transcript.md",
    "thumbnail.svg",
]
ARTIFACTS = [
    "visual_edition/README.md",
    "visual_edition/manifest.json",
    "visual_edition/toolchain.json",
    "visual_edition/requirements.lock.txt",
    "visual_edition/manim.cfg",
    "visual_edition/visual_grammar.json",
    "visual_edition/youtube_channel.json",
    "visual_edition/youtube_ledger.json",
    "visual_edition/lib/__init__.py",
    "visual_edition/lib/asi_visuals.py",
    "visual_edition/scenes/primitive_gallery.py",
    "schemas/manim_toolchain.schema.json",
    "schemas/visual_grammar.schema.json",
    "schemas/visual_edition_manifest.schema.json",
    "schemas/visual_chapter_packet.schema.json",
    "schemas/youtube_channel.schema.json",
    "schemas/youtube_ledger.schema.json",
    "scripts/capture_manim_toolchain.py",
    "scripts/validate_manim_toolchain.py",
    "scripts/build_visual_edition_manifest.py",
    "scripts/build_youtube_ledger.py",
    "scripts/validate_visual_edition.py",
    "scripts/sync_visual_edition_embeds.py",
    "scripts/register_visual_edition.py",
] + [
    f"visual_edition/chapters/{pilot}/{filename}"
    for pilot in PILOTS
    for filename in PACKET_FILES
]


def main() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    registry["units"] = [
        unit for unit in registry["units"]
        if unit.get("script") not in {SCRIPT, EMBED_SCRIPT, TOOLCHAIN_SCRIPT}
    ]
    used = {unit["order"] for unit in registry["units"]}
    order = next(index for index in range(1, len(registry["units"]) + 2) if index not in used)
    registry["units"].append({
        "id": f"{SCRIPT}:{order}",
        "order": order,
        "script": SCRIPT,
        "args": [],
        "execution_tier": "pr",
        "validation_class": "publication_gate",
        "input_contract": "Current 84-chapter book_structure manifest; exact P7.3 five-pilot identity and complete tracked source packets; pinned ARM-native ManimCE toolchain record; candidate visual grammar; exact authenticated YouTube channel contract and generated 84-chapter publication/revision ledger; zero or more schema-valid chapter derivative packets; ignored build-output and YouTube-hosting boundary.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Reject chapter identity or digest drift, premature pilot or visual-grammar completion, incomplete packet artifacts, stale chapter bindings, invalid publication/embed states, missing render identity, out-of-range validated duration, tracked or Pages-hosted media binaries, and support-state movement. The separately registered embed reconciler rejects missing, stale, or unmanaged public embed surfaces.",
        "output_assertions": [
            "84 canonical visual-edition rows in book order",
            "five exact pilot identities",
            "Manim Community Edition 0.20.1 contract",
            "YouTube canonical binary host",
            "exact canonical YouTube channel and 84-chapter revision ledger",
            "no current external publication authority",
            "all packet and lifecycle counts derived",
            "zero tracked or Pages-hosted video/audio binaries",
            "eight rejecting mutations",
            "support-state effect none",
        ],
        "claim_scope": "Visual-edition derivation identity, accessibility artifacts, freshness, binary custody, and publication/embed lifecycle only.",
        "negative_controls": "validator_owned_eight_manifest_pilot_host_authority_support_grammar_motion_caption_mutations",
        "negative_control_cases": [
            "chapter deletion",
            "pilot substitution",
            "binary host widening",
            "premature publication authority",
            "support promotion",
            "premature grammar ratification",
            "motion-only meaning",
            "caption deletion",
        ],
        "prohibited_inference": "A valid toolchain, scene, render, packet, caption, transcript, thumbnail, upload, playlist entry, or embed does not prove or promote a chapter claim, validate ASI, establish safety or SOTA, or authorize an external mutation.",
        "contract_precision": "exact",
        "semantic_review_state": "checked_visual_derivative_identity_accessibility_freshness_binary_hosting_publication_and_support_boundaries",
    })
    used.add(order)
    embed_order = next(index for index in range(1, len(registry["units"]) + 3) if index not in used)
    registry["units"].append({
        "id": f"{EMBED_SCRIPT}:{embed_order}",
        "order": embed_order,
        "script": EMBED_SCRIPT,
        "args": [],
        "execution_tier": "pr",
        "validation_class": "publication_gate",
        "input_contract": "Current visual-edition manifest and chapter packets; canonical QMD chapters; publication and Quarto-embed lifecycle states.",
        "input_artifacts": [
            "visual_edition/manifest.json",
            "scripts/sync_visual_edition_embeds.py",
        ],
        "output_contract": "Reject a missing or stale managed YouTube embed/transcript block for published_current packets, a managed public block for a non-current packet, or any unmanaged YouTube embed.",
        "output_assertions": [
            "no placeholder player before publication",
            "published player uses youtube-nocookie.com",
            "descriptive transcript is adjacent to every current player",
            "non-current managed players are absent",
        ],
        "claim_scope": "Quarto projection of already-authorized current YouTube publications only.",
        "negative_controls": "structural_exact_block_reconciliation_against_packet_lifecycle",
        "negative_control_cases": [],
        "prohibited_inference": "An exact embed and transcript do not validate video content, promote evidence, or authorize YouTube publication.",
        "contract_precision": "exact",
        "semantic_review_state": "checked_embed_transcript_and_publication_lifecycle_projection",
    })
    used.add(embed_order)
    toolchain_order = next(
        index for index in range(1, len(registry["units"]) + 4) if index not in used
    )
    registry["units"].append({
        "id": f"{TOOLCHAIN_SCRIPT}:{toolchain_order}",
        "order": toolchain_order,
        "script": TOOLCHAIN_SCRIPT,
        "args": [],
        "execution_tier": "pr",
        "validation_class": "publication_gate",
        "input_contract": "Pinned ManimCE dependency lock, exact ARM64 toolchain record, deterministic Cairo configuration, and ignored build-output boundary.",
        "input_artifacts": [
            "visual_edition/toolchain.json",
            "visual_edition/requirements.lock.txt",
            "visual_edition/manim.cfg",
            "schemas/manim_toolchain.schema.json",
            "scripts/validate_manim_toolchain.py",
        ],
        "output_contract": "Reject architecture, Manim distribution/version, environment class, lock/config digest, 1080p30 release profile, or support-state drift.",
        "output_assertions": [
            "Manim Community Edition 0.20.1",
            "ARM64 CPython environment",
            "exact frozen dependency lock",
            "Cairo renderer and ignored media path",
            "release profile exactly 1920x1080 at 30 fps",
            "seven rejecting mutations",
        ],
        "claim_scope": "Local animation-build reproducibility and binary custody only.",
        "negative_controls": "validator_owned_seven_architecture_distribution_version_environment_digest_frame_rate_and_support_mutations",
        "negative_control_cases": [
            "architecture widening",
            "ManimGL substitution",
            "version drift",
            "global environment",
            "binary path drift",
            "1080p60 shortcut substitution",
            "support promotion",
        ],
        "prohibited_inference": "A qualified animation toolchain does not validate a video, prove a chapter claim, or authorize publication.",
        "contract_precision": "exact",
        "semantic_review_state": "checked_arm_runtime_lock_renderer_release_profile_binary_and_support_boundaries",
    })
    for artifact in ARTIFACTS:
        if artifact not in registry["required_artifacts"]:
            registry["required_artifacts"].append(artifact)
    registry["units"].sort(key=lambda unit: unit["order"])
    registry["summary"] = {
        "required_artifact_count": len(registry["required_artifacts"]),
        "unit_count": len(registry["units"]),
    }
    REGISTRY.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
    print(
        f"Registered {SCRIPT}: {registry['summary']['unit_count']} units, "
        f"{registry['summary']['required_artifact_count']} artifacts."
    )


if __name__ == "__main__":
    main()
