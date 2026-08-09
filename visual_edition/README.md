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
5. `narration_toolchain.json` - pinned TTS, verification, rights, and alignment
   state.
6. `youtube_ledger.json` and `youtube_preview_bindings.json` - platform custody
   and current projection.

Do not infer current state from old scene files, render receipts, or prose in a
commit message. The generated ledgers are authoritative.

## Current State

As of 2026-08-09:

- The book has 85 canonical chapters.
- Generation one preserves 84 historical packets: 9 are source-current and 75
  are explicitly stale. The newest chapter has no fabricated predecessor.
- Generation two has 24 case-first narration scripts and 61 planned targets.
  The scripts are 364-436 words and pass the current narration audit.
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
2. Select one transferable teaching promise, one concrete case, one mechanism,
   one test or counterexample, and one natural evidence boundary.
3. Write and audit `generation-2/narration.txt` before creating motion.
4. Design four to six macro narrative moves, a persistent visual world, and
   sparse semantic keyframes.
5. Build an audio-timed `generation-2/beat_plan.json` whose narration exactly
   covers the script.
6. Synthesize coherent performance blocks. Use receipt timing only for an
   animatic until a pinned aligner passes qualification.
7. Implement a low-resolution animatic with chapter-specific domain objects.
8. Review complete playback plus at least five frame samples per beat. Run a
   cold comprehension and changed-condition transfer check.
9. Qualify alignment, then complete picture-and-sound lock and the release
   candidate gates.
10. Reconcile platform and Quarto state only after local acceptance and exact
    action-time authority.

Use the tracked skill scripts:

```bash
python3 ../skills/asi-stack-manim-videos/scripts/audit_video_plan.py \
  --narration chapters/<chapter-id>/generation-2/narration.txt \
  --narration-only

python3 ../skills/asi-stack-manim-videos/scripts/audit_video_plan.py \
  chapters/<chapter-id>/generation-2/beat_plan.json \
  --narration chapters/<chapter-id>/generation-2/narration.txt
```

The paths above assume the shell is in `visual_edition/`. From the repository
root, omit the leading `../` and prefix chapter paths with `visual_edition/`.

## Acceptance Gates

The production ledger fails closed. A later gate cannot pass before its
prerequisites.

- **Script:** one promise, concrete case, spoken cadence, evidence fit, and
  transfer question pass before TTS or scene code.
- **Beat plan:** exact narration coverage, semantic state changes, object
  continuity, audio-derived anchors, and a local evidence boundary.
- **Animatic:** story, visual model, pacing, continuity, and payoff work at low
  resolution.
- **Picture and sound lock:** final geometry, timing, narration, captions, mix,
  and qualified forced alignment.
- **Release candidate:** pinned render profile, complete playback, accessibility,
  five frame samples per beat, cold comprehension and transfer, and every
  experience dimension at least 4/5.
- **Acceptance:** independent release-candidate review, technical and claim
  fidelity gates, exact master and receipt identity, and no open defects.

Technical validity is never aesthetic or pedagogical acceptance.

## Validation

Regenerate and validate the dynamic production ledger after chapter, script,
standard, schema, or narration-toolchain changes:

```bash
python3 scripts/sync_manim_v2_production_ledger.py
python3 scripts/sync_manim_v2_production_ledger.py --check
python3 scripts/validate_manim_v2_production_ledger.py
python3 scripts/validate_visual_edition.py
```

Audit all current generation-two scripts:

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

- chapter scripts, beat plans, scene source, storyboards, captions,
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

## Publication Boundary

YouTube IDs, visibility, captions, thumbnails, playlist position, predecessor
state, Quarto embeds, and receipts form one governed transaction. A local
render, passing review, upload plan, or prior browser session supplies no
external mutation authority.

Preserve predecessor history. Publish a successor only after exact local
acceptance and action-time authorization, then reconcile the platform receipt
and live-book projection together.
