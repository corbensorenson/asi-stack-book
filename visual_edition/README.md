# ASI Stack Visual Edition

This directory contains the governed visual-abstract edition of *The ASI
Stack*. The book remains canonical. A video may explain a bounded chapter idea;
it cannot strengthen a claim, change an evidence state, or authorize its own
publication.

## Start Here

Read these sources in order:

1. `../skills/asi-stack-manim-videos/SKILL.md` - current authoring standard.
2. `manim_v2_production_ledger.json` - canonical generation-two targets and
   gates.
3. `manifest.json` - generation-one packet custody and source freshness.
4. `visual_grammar.json` - shared visual semantics.
5. `toolchain.json` - pinned Manim runtime, renderer, fonts, and render profile.
6. `primitive_regression_manifest.json` - reviewed shared-factory graphical
   baseline and exact dependency bindings.
7. `narration_toolchain.json` - pinned TTS, verification, rights, and alignment
   state.
8. `youtube_ledger.json` and `youtube_preview_bindings.json` - platform custody
   and current projection.

Do not infer current state from old scene files, render receipts, or prose in a
commit message. The generated ledgers are authoritative.

## Current State

As of 2026-08-09:

- The book has 85 canonical chapters.
- Generation one preserves 84 historical packets: 9 are source-current and 75
  are explicitly stale. The newest chapter has no fabricated predecessor.
- Generation two has 24 case-first narration drafts and 61 planned targets.
  The drafts are 364-436 words and pass structural narration lint. None is an
  approved script until its source-bound treatment passes read-aloud, truth,
  and visualizability review against the exact narration digest.
- Every pre-overhaul beat plan, audio file, caption file, transcript, scene,
  render, and review is downstream of an obsolete script or standard. Those
  artifacts remain historical, while all current acceptance gates are open.
- No generation-two video is accepted or current in Quarto.
- No YouTube preview is bound to the current projection, and no external
  mutation is authorized.
- Kokoro remains the pinned incumbent voice. Forced alignment is not yet
  qualified, so synthesis-block timing may support animatics but cannot close
  picture-and-sound lock.

## Authoring Workflow

For each chapter:

1. Read the canonical chapter, packet, sources, evidence ceiling, and
   non-claims.
2. Select one transferable teaching promise, one concrete case, one central
   mechanism, relationship, or tradeoff, one test or counterexample, and one
   natural evidence boundary.
3. Co-design `generation-2/treatment.json`, narration, normally four to six
   macro moves, sparse semantic keyframes, persistent objects, packaging, and
   accessibility.
4. Pass the treatment's read-aloud, truth, and visualizability script gate.
5. Synthesize coherent performance blocks and bind exact receipts.
6. Build `generation-2/beat_plan.json` from the exact treatment and narration.
   Use block timing only for an animatic until a pinned aligner passes
   qualification and manual anchor review.
7. Implement a low-resolution narration-bearing animatic with chapter-specific
   domain objects. A silent visual track is only an intermediate.
8. Pass static scene-source preflight, then use the tracked isolated runner so
   network denial, credential stripping, repository write confinement,
   enforceable resource limits, policy checks, explicit macOS memory-bound
   residual, and the exact render/mux commands receive a machine-valid receipt.
   Run the portable shared-primitive custody check in CI and the full graphical
   regression on the pinned macOS host whenever its inputs change. Never report
   the portable check as a render replay.
9. Review complete playback plus a bound manifest of five samples per beat and
   targeted risky transitions. Keep sample images in ignored build storage and
   reuse a current digest-bound set instead of rewriting it.
10. Qualify alignment, finish the scene/audio/caption/transcript candidate, use
    the release runner, sync the ledger, run A/V diagnostics, and compile the
    final receipt. Complete picture-and-sound lock against those exact
    artifacts; repair and repeat custody when needed. Then run an independent
    source-aware release review and context-isolated cold-proxy review. Never
    hand-author `render_receipt.json`.
11. Reconcile platform and Quarto state only after local acceptance and exact
    action-time authority.

Use the tracked skill scripts:

```bash
python3 ../skills/asi-stack-manim-videos/scripts/audit_video_plan.py \
  --narration chapters/<chapter-id>/generation-2/narration.txt \
  --narration-only

python3 ../skills/asi-stack-manim-videos/scripts/audit_video_plan.py \
  --treatment chapters/<chapter-id>/generation-2/treatment.json \
  --narration chapters/<chapter-id>/generation-2/narration.txt \
  --treatment-only

python3 ../skills/asi-stack-manim-videos/scripts/audit_video_plan.py \
  chapters/<chapter-id>/generation-2/beat_plan.json \
  --treatment chapters/<chapter-id>/generation-2/treatment.json \
  --narration chapters/<chapter-id>/generation-2/narration.txt

../build/visual_edition/tts_venv/bin/python ../scripts/render_visual_narration.py \
  --text visual_edition/chapters/<chapter-id>/generation-2/narration.txt \
  --output build/visual_edition/audio/<chapter-id>-narration-master.wav \
  --speed 1.08
../build/visual_edition/tts_venv/bin/python ../scripts/transcribe_visual_narrations.py \
  --chapter <chapter-id>
../build/visual_edition/tts_venv/bin/python ../scripts/validate_visual_narration.py \
  --audio build/visual_edition/audio/<chapter-id>-narration-master.wav \
  --receipt build/visual_edition/audio/<chapter-id>-narration-master.receipt.json \
  --asr build/visual_edition/audio/<chapter-id>-narration-master.json \
  --report build/visual_edition/audio/<chapter-id>-narration-master.validation.json

python3 ../skills/asi-stack-manim-videos/scripts/audit_scene_source.py \
  chapters/<chapter-id>/generation-2/scene.py \
  --treatment chapters/<chapter-id>/generation-2/treatment.json

python3 ../skills/asi-stack-manim-videos/scripts/audit_primitive_regression.py --static-only
python3 ../skills/asi-stack-manim-videos/scripts/audit_primitive_regression.py

python3 ../skills/asi-stack-manim-videos/scripts/render_scene_isolated.py --self-test

python3 ../skills/asi-stack-manim-videos/scripts/render_scene_isolated.py \
  visual_edition/chapters/<chapter-id>/generation-2/scene.py <SceneClass> \
  --treatment visual_edition/chapters/<chapter-id>/generation-2/treatment.json \
  --audio-master build/visual_edition/audio/<chapter-id>-narration-master.wav \
  --profile draft \
  --receipt visual_edition/chapters/<chapter-id>/generation-2/receipts/animatic-sandbox.json
python3 ../skills/asi-stack-manim-videos/scripts/sample_video_beats.py \
  ../build/visual_edition/isolated-renders/<chapter-id>/draft/<chapter-id>-animatic.mp4 \
  chapters/<chapter-id>/generation-2/beat_plan.json \
  --sample-set animatic
```

When the candidate is ready for picture-and-sound lock, run the release
sequence from the repository root:

```bash
python3 skills/asi-stack-manim-videos/scripts/render_scene_isolated.py \
  visual_edition/chapters/<chapter-id>/generation-2/scene.py <SceneClass> \
  --treatment visual_edition/chapters/<chapter-id>/generation-2/treatment.json \
  --audio-master build/visual_edition/audio/<chapter-id>-narration-master.wav --profile release \
  --receipt visual_edition/chapters/<chapter-id>/generation-2/receipts/release-sandbox.json
python3 scripts/sync_manim_v2_production_ledger.py
python3 skills/asi-stack-manim-videos/scripts/audit_av_experience.py \
  build/visual_edition/generation-2/final/<chapter-id>.mp4 \
  --plan visual_edition/chapters/<chapter-id>/generation-2/beat_plan.json \
  --target-lufs -16 \
  --json-out visual_edition/chapters/<chapter-id>/generation-2/av_diagnostics.json

python3 skills/asi-stack-manim-videos/scripts/build_final_render_receipt.py \
  --sandbox-receipt visual_edition/chapters/<chapter-id>/generation-2/receipts/release-sandbox.json \
  --av-diagnostics visual_edition/chapters/<chapter-id>/generation-2/av_diagnostics.json \
  --output visual_edition/chapters/<chapter-id>/generation-2/render_receipt.json
python3 skills/asi-stack-manim-videos/scripts/sample_video_beats.py \
  build/visual_edition/generation-2/final/<chapter-id>.mp4 \
  visual_edition/chapters/<chapter-id>/generation-2/beat_plan.json \
  --sample-set final
python3 skills/asi-stack-manim-videos/scripts/build_caption_review_sheet.py \
  build/visual_edition/generation-2/final/<chapter-id>.mp4 \
  visual_edition/chapters/<chapter-id>/generation-2/captions.vtt \
  visual_edition/chapters/<chapter-id>/generation-2/receipts/caption-overlay.png \
  --report-json visual_edition/chapters/<chapter-id>/generation-2/receipts/caption-diagnostics.json
python3 scripts/sync_manim_v2_production_ledger.py
python3 scripts/validate_manim_v2_production_ledger.py
```

The first command block assumes the shell is in `visual_edition/`; the isolated
runner's artifact arguments are deliberately repository-relative. From the
repository root, omit the leading `../` and prefix the other chapter paths with
`visual_edition/`. The release block already uses the repository root.

## Acceptance Gates

The production ledger fails closed. A later gate cannot pass before its
prerequisites.

- **Treatment and script:** audience, one promise, concrete case, source and
  non-claim contract, truth checks, keyframes, spoken cadence, and transfer
  criteria pass before TTS or detailed scene code.
- **Beat plan:** exact narration coverage, semantic state changes, object
  continuity, audio-derived anchors, and a local evidence boundary.
- **Animatic:** story, visual model, pacing, continuity, and payoff work at low
  resolution; scene source passes static preflight; shared factories pass their
  content-addressed graphical regression; render execution has a valid policy
  receipt.
- **Picture and sound lock:** final geometry, timing, narration, captions, mix,
  and qualified forced alignment.
- **Release candidate:** pinned render profile, complete playback, accessibility,
  manifest-proven frame samples, and an independent source-aware critic with
  every owned dimension at least 4/5.
- **Acceptance:** separate context-isolated cold comprehension and transfer,
  technical and claim-fidelity gates, exact master and receipt identity, and
  no open material defect. An AI proxy result is not human-learning evidence.

Technical validity is never aesthetic or pedagogical acceptance.

## Validation

Regenerate and validate the dynamic production ledger after chapter,
treatment, narration, standard, schema, or narration-toolchain changes:

```bash
python3 scripts/sync_manim_v2_production_ledger.py
python3 scripts/sync_manim_v2_production_ledger.py --check
python3 scripts/validate_manim_toolchain.py --probe-runtime
python3 skills/asi-stack-manim-videos/scripts/audit_scene_source.py --self-test
python3 skills/asi-stack-manim-videos/scripts/render_scene_isolated.py --self-test
python3 skills/asi-stack-manim-videos/scripts/build_final_render_receipt.py --self-test
python3 skills/asi-stack-manim-videos/scripts/audit_primitive_regression.py --static-only
python3 skills/asi-stack-manim-videos/scripts/audit_primitive_regression.py
python3 scripts/validate_manim_v2_production_ledger.py
python3 scripts/validate_visual_edition.py
```

Structurally lint all current generation-two narration drafts:

```bash
python3 skills/asi-stack-manim-videos/scripts/audit_video_plan.py \
  --all-narrations visual_edition/chapters
```

The manifest and YouTube builders derive counts from canonical structure and
current packet state. Never restore fixed chapter-count assumptions.

## Historical Generation One

Generation one is preserved for custody and comparison. It is not an authoring
template. Its seven-scene card renderer, packet generator, paragraph-timing
sync, bulk renderer, producer, and mux require the explicit
`--historical-generation-one` acknowledgement.

Do not use those commands to fill count symmetry, create a new chapter, or
produce a current candidate. Do not overwrite historical receipts.

## Storage Boundary

Track compact, reviewable sources and contracts:

- chapter treatments, narration drafts, beat plans, scene source, captions,
  transcripts, thumbnails, reviews, ledgers, schemas, and digest receipts;
- the shared visual grammar, pronunciation lexicon, dependency locks, and
  publication contracts.

Keep large reproducible artifacts under ignored `build/visual_edition/`:

- model weights and virtual environments;
- raw or normalized narration audio;
- Manim caches, partial renders, review frames, contact sheets, and final
  masters;
- ASR and alignment working output.

Do not regenerate large media merely to refresh status. Render when a script or
visual hypothesis is ready for its next review gate.

The ledger uses component-scoped invalidation. A caption diagnostic change
does not reopen treatment, while a story contract does; the full skill-bundle
digest remains recorded for provenance.

## Publication Boundary

YouTube IDs, visibility, captions, thumbnails, playlist position, predecessor
state, Quarto embeds, and receipts form one governed transaction. A local
render, passing review, upload plan, or prior browser session supplies no
external mutation authority.

Preserve predecessor history. Publish a successor only after exact local
acceptance and action-time authorization, then reconcile the platform receipt
and live-book projection together.
