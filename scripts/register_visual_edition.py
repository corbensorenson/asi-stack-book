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
SUPERSESSION_SCRIPT = "validate_youtube_supersession_workflow.py"
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
    "scene_spec.json",
]
BASE_ARTIFACTS = [
    "visual_edition/README.md",
    "visual_edition/manifest.json",
    "visual_edition/toolchain.json",
    "visual_edition/requirements.lock.txt",
    "visual_edition/narration_toolchain.json",
    "visual_edition/narration_requirements.lock.txt",
    "visual_edition/narration_pronunciations.json",
    "visual_edition/manim.cfg",
    "visual_edition/visual_grammar.json",
    "visual_edition/youtube_channel.json",
    "visual_edition/youtube_ledger.json",
    "visual_edition/youtube_upload_plan.json",
    "visual_edition/youtube_mutation_scope.json",
    "visual_edition/youtube_publication_preflight.json",
    "visual_edition/lib/__init__.py",
    "visual_edition/lib/asi_visuals.py",
    "visual_edition/lib/chapter_scene.py",
    "visual_edition/scenes/primitive_gallery.py",
    "schemas/manim_toolchain.schema.json",
    "schemas/narration_toolchain.schema.json",
    "schemas/visual_grammar.schema.json",
    "schemas/visual_edition_manifest.schema.json",
    "schemas/visual_chapter_packet.schema.json",
    "schemas/youtube_channel.schema.json",
    "schemas/youtube_ledger.schema.json",
    "schemas/youtube_upload_plan.schema.json",
    "schemas/youtube_mutation_scope.schema.json",
    "schemas/youtube_publication_preflight.schema.json",
    "schemas/youtube_platform_receipt.schema.json",
    "schemas/youtube_supersession_plan.schema.json",
    "scripts/capture_manim_toolchain.py",
    "scripts/validate_manim_toolchain.py",
    "scripts/render_visual_narration.py",
    "scripts/build_visual_captions_from_narration_receipt.py",
    "scripts/validate_visual_narration.py",
    "scripts/validate_visual_master.py",
    "scripts/generate_visual_chapter_packets.py",
    "scripts/produce_visual_chapter.py",
    "scripts/transcribe_visual_narrations.py",
    "scripts/render_visual_scenes.py",
    "scripts/sync_visual_scene_timings.py",
    "scripts/finalize_visual_chapter_packets.py",
    "scripts/mux_visual_masters.py",
    "scripts/build_visual_review_sheets.py",
    "scripts/build_visual_edition_manifest.py",
    "scripts/build_youtube_ledger.py",
    "scripts/build_youtube_upload_plan.py",
    "scripts/build_youtube_publication_preflight.py",
    "scripts/render_youtube_thumbnails.py",
    "scripts/build_youtube_thumbnail_review_sheets.py",
    "scripts/validate_youtube_publication_preflight.py",
    "scripts/record_youtube_platform_receipt.py",
    "scripts/reconcile_youtube_publication_receipts.py",
    "scripts/visual_publication_lifecycle.py",
    "scripts/prepare_youtube_supersession.py",
    "scripts/record_youtube_supersession_receipt.py",
    "scripts/reconcile_youtube_supersession_receipt.py",
    "scripts/validate_youtube_supersession_workflow.py",
    "scripts/visual_chapter_source.py",
    "scripts/validate_visual_edition.py",
    "scripts/sync_visual_edition_embeds.py",
    "scripts/register_visual_edition.py",
]


def chapter_artifacts() -> list[str]:
    structure = json.loads((ROOT / "book_structure.json").read_text(encoding="utf-8"))
    result = []
    for part in structure["parts"]:
        for chapter in part["chapters"]:
            for filename in PACKET_FILES:
                relative = f"visual_edition/chapters/{chapter['id']}/{filename}"
                if (ROOT / relative).is_file():
                    result.append(relative)
    return result


def main() -> None:
    artifacts = BASE_ARTIFACTS + chapter_artifacts()
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    registry["units"] = [
        unit for unit in registry["units"]
        if unit.get("script") not in {
            SCRIPT,
            EMBED_SCRIPT,
            TOOLCHAIN_SCRIPT,
            SUPERSESSION_SCRIPT,
        }
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
        "input_contract": "Current 84-chapter book_structure manifest; exact P7.3 five-pilot identity and complete tracked source packets for all 84 chapters; pinned ARM-native ManimCE, local Kokoro narration, and MLX Whisper verification contracts; ratified visual grammar; exact authenticated YouTube channel contract, non-authorizing upload plan, 84-row master/caption/thumbnail publication preflight, platform-receipt schema, generated 84-chapter publication/revision ledger, canonical chapter digest excluding only the exact managed visual block, and ignored build-output/YouTube-hosting boundary.",
        "input_artifacts": artifacts,
        "output_contract": "Reject chapter identity or canonical-digest drift, managed-block self-staleness, upload-plan or row-level publication-preflight drift, premature or missing post-pilot visual-grammar ratification, narration-toolchain input drift, incomplete packet artifacts, invalid publication/embed states, missing render identity, out-of-range validated duration, partial or non-unique platform-receipt sets, receipt source/metadata/caption/thumbnail/authority drift, tracked or Pages-hosted media binaries, and support-state movement. The separately registered embed reconciler rejects missing, stale, or unmanaged public embed surfaces.",
        "output_assertions": [
            "84 canonical visual-edition rows in book order",
            "five exact pilot identities",
            "Manim Community Edition 0.20.1 contract",
            "YouTube canonical binary host",
            "exact canonical YouTube channel and 84-chapter revision ledger",
            "84 exact publication-preflight rows",
            "zero-or-84 platform-receipt reconciliation",
            "managed visual block excluded from canonical chapter digest",
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
            "premature ratification or post-gate deratification",
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
    used.add(toolchain_order)
    supersession_order = next(
        index for index in range(1, len(registry["units"]) + 5)
        if index not in used
    )
    registry["units"].append({
        "id": f"{SUPERSESSION_SCRIPT}:{supersession_order}",
        "order": supersession_order,
        "script": SUPERSESSION_SCRIPT,
        "args": [],
        "execution_tier": "pr",
        "validation_class": "publication_gate",
        "input_contract": "Visual packet regeneration, immutable generation receipts, current YouTube ledger, generation-N supersession-plan schema, replacement receipt schema, exact predecessor disposition, idempotency, rollback, and no-authority contracts.",
        "input_artifacts": [
            "visual_edition/youtube_ledger.json",
            "schemas/youtube_ledger.schema.json",
            "schemas/youtube_platform_receipt.schema.json",
            "schemas/youtube_supersession_plan.schema.json",
            "scripts/visual_publication_lifecycle.py",
            "scripts/generate_visual_chapter_packets.py",
            "scripts/build_youtube_ledger.py",
            "scripts/prepare_youtube_supersession.py",
            "scripts/record_youtube_supersession_receipt.py",
            "scripts/reconcile_youtube_supersession_receipt.py",
            "scripts/validate_youtube_supersession_workflow.py",
        ],
        "output_contract": "Reject predecessor erasure during regeneration, generation gaps, broken predecessor chains, identical replacements, idempotency drift, premature authority, deletion permission, incomplete rollback, reused video IDs, missing or wrong predecessor disposition, and support promotion.",
        "output_assertions": [
            "published predecessor preserved as stale during regeneration",
            "generation receipts remain contiguous and append-only",
            "one exact predecessor per replacement",
            "replacement video ID differs from predecessor",
            "predecessor becomes unlisted outside canonical playlist",
            "rollback never deletes either generation",
            "twelve rejecting mutations",
            "support-state effect none",
        ],
        "claim_scope": "Visual-publication revision identity, generation custody, playlist/embed handoff, predecessor retention, and rollback only.",
        "negative_controls": "validator_owned_twelve_generation_predecessor_idempotency_authority_deletion_rollback_receipt_and_support_mutations",
        "negative_control_cases": [
            "generation gap",
            "identical predecessor",
            "idempotency drift",
            "premature authority",
            "delete permission",
            "rollback deletion",
            "support promotion",
            "video ID reuse",
            "missing predecessor disposition",
            "wrong old playlist item",
            "predecessor deletion",
            "support promotion receipt",
        ],
        "prohibited_inference": "A correct replacement transaction does not validate the chapter claim, promote evidence, establish safety, or authorize any platform mutation.",
        "contract_precision": "exact",
        "semantic_review_state": "checked_generation_chain_predecessor_retention_idempotency_rollback_playlist_embed_and_support_boundaries",
    })
    for artifact in artifacts:
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
