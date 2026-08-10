# ASI Stack Video Pipeline

## Contents

- Current baseline
- Contract files
- Artifact topology
- State and gates
- Timing states
- Review lanes
- Authoring sequence
- Release candidate command sequence
- Invalidation
- Historical revisions and publication

## Current baseline

Derive the chapter count, predecessor inventory, generation-two state
distribution, and open gates from `book_structure.json` and
`visual_edition/manim_v2_production_ledger.json` at the start of every run.
Never copy a dated count into a production decision or fabricate a predecessor
to make generations symmetrical.

Structural narration lint does not establish truth, voice, or visualizability.
Any treatment-free beat plan, audio, scene, caption, render, or review that
predates the current treatment and review contracts remains history. The
canonical ledger must report only the furthest state earned by current bound
artifacts, with every downstream gate closed.

Do not use the legacy packet generator for new authorship. Its commands require
the explicit `--historical-generation-one` acknowledgement. Do not create
generation-one files merely to make counts symmetrical.

## Contract files

- `schemas/manim_treatment.schema.json`: audience, evidence, story, packaging,
  art/audio/accessibility direction, assets, semantic keyframes, and script
  gate.
- `schemas/manim_beat_plan.schema.json`: exact treatment and narration bindings,
  timing state, macro/performance ownership, and per-beat visual argument.
- `schemas/manim_experience_review.schema.json`: exact artifact bindings,
  reviewer context, sample manifest, raw learning checks, viewing passes,
  timestamped dimensions, defects, and verdict.
- `schemas/manim_review_context_manifest.schema.json`: exact material and prompt
  custody for each isolated review session.
- `schemas/manim_frame_sample_manifest.schema.json`: tracked sampler and FFmpeg
  identity, exact media/plan custody, five samples per beat, and targeted risky
  transitions.
- `schemas/manim_av_diagnostics.schema.json`: pinned FFmpeg/FFprobe identity,
  exact detection thresholds, stream and loudness fields, and diagnostic state.
- `schemas/manim_render_receipt.schema.json`: exact release inputs, sandboxed
  execution conditions, technical output, and A/V-diagnostic binding.
- `schemas/manim_sandbox_policy_receipt.schema.json`: runner, source-preflight,
  explicit repository inputs plus disclosed system-content roots, denied
  network/credentials, constrained writes, resource limits and their live
  self-tests, explicit macOS memory-bound residual, exact command sequence, and
  output identity.
- `skills/asi-stack-manim-videos/scripts/build_final_render_receipt.py`:
  deterministic final-receipt compiler. It binds the policy receipt, ledger,
  forced-aligned plan, audio, master metadata, and warning-free A/V diagnostic;
  do not substitute a hand-authored release declaration.
- `schemas/manim_toolchain.schema.json`: pinned ManimCE runtime, renderer,
  native dependencies, fonts, render profiles, and the exact ratified visual
  grammar whose palette contrast and redundant encodings are computed.
- `schemas/manim_primitive_regression.schema.json`: content-addressed shared
  visual-factory coverage and manually inspected reference frames.
- `schemas/manim_v2_production_ledger.schema.json`: manifest-driven chapter
  identity, production state, gates, predecessor custody, and publication
  lifecycle.
- `visual_edition/narration_toolchain.json`: pinned voice, synthesis, alignment,
  audio, and disclosure policy. A candidate mentioned in a reference is not
  qualified until this file records a passing comparison.

The semantic auditors enforce relationships that JSON Schema cannot express.
Schema validity alone is never a passing gate.

## Artifact topology

```text
visual_edition/chapters/<chapter-id>/generation-2/
  treatment.json
  narration.txt
  beat_plan.json
  scene.py
  captions.vtt
  transcript.md
  thumbnail.svg | thumbnail.png
  av_diagnostics.json
  render_receipt.json
  receipts/
    animatic-sample-manifest.json
    final-sample-manifest.json
    caption-overlay.png
    caption-diagnostics.json
  reviews/
    animatic.json
    animatic.context.json
    animatic.prompt.md
    animatic.raw.md
    picture_and_sound_lock.json
    picture_and_sound_lock.context.json
    picture_and_sound_lock.prompt.md
    picture_and_sound_lock.raw.md
    release_candidate.json
    release_candidate.context.json
    release_candidate.prompt.md
    release_candidate.raw.md
    independent_release_candidate.json
    independent_release_candidate.context.json
    independent_release_candidate.prompt.md
    independent_release_candidate.raw.md
```

Do not create speculative files. Add an artifact only when its gate is being
worked or a prior generation must be preserved. Build intermediates belong in
ignored build directories, not the source tree. Sample PNGs and their HTML
sheet live under `build/visual_edition/review-samples/`; only their compact
digest manifest is tracked with the chapter.

## State and gates

The stage describes the furthest artifact that exists. A gate describes what
has been reviewed and accepted. Existence never implies acceptance.

| Stage | Meaning |
|---|---|
| `planned` | no generation-two narration |
| `narration_draft` | narration exists; no approved treatment/script |
| `treated` | treatment exists; script gate is not passed |
| `script_passed` | treatment binds an approved narration digest |
| `beat_planned` | current v4 beat plan exists |
| `animatic` | bound animatic review passes |
| `picture_and_sound_lock` | forced-aligned picture/sound review passes |
| `release_candidate` | pinned master and source-aware review pass |
| `accepted` | cold-proxy, technical, claim-fidelity, and all prior gates pass |

Gate prerequisites are fail-closed:

```text
treatment -> script -> beat_plan -> animatic
animatic -> picture_and_sound_lock -> release_candidate
release_candidate -> independent_release_candidate
all above + technical + claim_fidelity -> accepted
```

The independent release review depends on the exact release candidate but does
not inherit the source-aware critic's context.

## Treatment and script gate

`treatment.json` is the source of truth for the derivative's editorial design.
It contains three to five compared promises with one exact selection, a
standalone audience contract, content and non-claim boundaries, assumptions,
notation and units, retained truth checks, normally four to six macro moves
with viewer-before/visible-event/viewer-after states, normally four to eight
semantic keyframes, packaging, asset provenance, performance blocks, and
accessibility plans.

Narration and keyframes co-evolve. The treatment may record `not_reviewed` or
`revise` while drafting. It may record `pass` only when:

- its narration digest and word count match the supplied file;
- read-aloud, truth, and visualizability reviews each pass;
- a reviewer ID is recorded; and
- no open script defect remains.

The narration-only auditor reports structural lint. Only the complete treatment
audit can pass the script gate.

Failed or uncertain truth checks remain in the treatment with a resolution
path and block the gate. Do not erase an adverse check from the record.

## Timing states

The beat plan binds exact treatment and narration files. It uses one of three
timing states:

| State | Required source | Eligible work |
|---|---|---|
| `estimated` | `editorial_estimate`, no receipt | rough planning only |
| `block_timed` | exact synthesis receipt plus passing bound ASR/content verification | animatic |
| `forced_aligned` | synthesis and verification custody plus alignment receipt, aligner ID, manual anchor review and digests | picture/sound lock and release |

Do not infer word timing by distributing block duration. Synthesis-block timing
is exact only at block boundaries. A plan can pass structural audit while
estimated, but the production ledger cannot pass its beat-plan gate until at
least `block_timed`, and cannot pass lock until `forced_aligned` under a
qualified toolchain.

Each beat must map to one treatment macro move and its performance block. Macro
moves appear once, contiguously, and in story order. `source_refs` must stay
inside the treatment's claim/source set. `introduced_terms` must stay inside
the audience contract. `mode: change` requires a real before/after state
change; `mode: hold` requires identical states, an explicit purpose, and no new
term.

## Review lanes

Every review binds the exact media, treatment, plan, narration, captions,
transcript, scene, thumbnail, visual contracts, receipt, and sample-manifest
identities relevant to its gate. An animatic binds its draft sandbox receipt
and narration-bearing animatic mux while final captions, transcript, thumbnail, A/V diagnostic,
and render receipt remain explicitly null. Lock binds the exact release mux,
captions, transcript, sandbox receipt, A/V diagnostic, and final receipt while
thumbnail remains null. Release reviews additionally bind the thumbnail.
Before launching a review, freeze a context
manifest and prompt, start a fresh AI task or independent human session when
the lane requires independence, and preserve the raw response before
assessment. The manifest must exactly enumerate what the reviewer received.

- **Implementation diagnostic:** animatic and lock. May be familiar with the
  implementation. Finds story, composition, motion, sync, continuity, pacing,
  voice, mix, and accessibility defects.
- **Source-aware critic:** release candidate. Must not be the script author or
  scene implementer. Receives the chapter, source notes, treatment, beat plan,
  and rendered candidate. Owns claim fidelity.
- **Cold audience proxy:** independent release candidate. Must not be author or
  implementer and must have no prior exposure. Receives only rendered video,
  captions, and optionally the descriptive transcript. Receives no answer key.
  Owns raw comprehension and changed-case transfer responses, not source truth.

A release pass needs both latter lanes. An AI proxy result remains a diagnostic
of one artifact under one prompt, not evidence of human learning or population
generalization.

## Authoring sequence

1. Read the full canonical chapter, packet, claims, proofs, source notes,
   non-claims, evidence ceiling, and current visual custody.
2. Record audience assumptions; compare teaching promises; select one case and
   medium.
3. Co-design macro moves, semantic keyframes, narration, packaging, assets,
   performance, and accessibility in the treatment.
4. Run structural narration lint throughout drafting.
5. Complete truth, read-aloud, and visualizability reviews; pass Gate 0.
6. Synthesize coherent performance blocks and record exact receipts.
7. Run pinned ASR/content verification, build a block-timed beat plan, and pass
   its semantic audit. ASR content agreement is not forced alignment.
8. Implement semantic objects and a low-resolution animatic.
9. Run scene-source preflight, then execute the passing scene through the
   tracked network-denied, credential-free, constrained-write runner. If shared
   primitives changed, pass the manually inspected graphical regression before
   using them. The animatic runner input includes the canonical narration
   master; a silent visual track cannot pass this stage.
   The portable registry gate verifies baseline identity, frame contract,
   source safety, and factory coverage only. It must not be reported as a
   graphical replay; run that comparison on the pinned macOS host.
10. Create the bound animatic sample set, inspect full-speed playback in every
    required mode, and pass animatic review.
11. Qualify forced alignment, manually review anchors, and update the plan.
12. Finish scene, narration, captions, transcript, camera, easing, voice, and
    mix to candidate quality.
13. Render and mux the pinned release profile through the tracked runner, sync
    the ledger to the ignored-build master, run A/V diagnostics, and compile
    the final receipt with the tracked compiler. Sync again; do not hand-author
    either execution or final custody.
14. Create one final sample set, run actual caption-overlay review,
    accessibility checks, device playback, and picture/sound lock against that
    exact candidate and receipt. Bind the same final samples into both release
    reviews unless an input or required targeted sample changes. Repair and
    repeat candidate custody when the review finds a defect.
15. Run the source-aware review, then the context-isolated cold proxy review.
16. Pass technical and claim-fidelity gates; accept locally.
17. Publish only with action-time authority and reconcile all external identity.

## Release candidate command sequence

Run the complete sequence from the repository root. It renders through the
tracked runner, binds the ignored-build master into the ledger, compiles rather
than hand-authors final custody, samples the exact candidate, builds the caption
review surface, and validates the resulting ledger.

```bash
python3 skills/asi-stack-manim-videos/scripts/render_scene_isolated.py \
  visual_edition/chapters/<chapter>/generation-2/scene.py <SceneClass> \
  --treatment visual_edition/chapters/<chapter>/generation-2/treatment.json \
  --audio-master build/visual_edition/audio/<chapter>-narration-master.wav --profile release \
  --receipt visual_edition/chapters/<chapter>/generation-2/receipts/release-sandbox.json
python3 scripts/sync_manim_v2_production_ledger.py
python3 skills/asi-stack-manim-videos/scripts/audit_av_experience.py \
  build/visual_edition/generation-2/final/<chapter>.mp4 \
  --plan visual_edition/chapters/<chapter>/generation-2/beat_plan.json \
  --target-lufs -16 --json-out visual_edition/chapters/<chapter>/generation-2/av_diagnostics.json
python3 skills/asi-stack-manim-videos/scripts/build_final_render_receipt.py \
  --sandbox-receipt visual_edition/chapters/<chapter>/generation-2/receipts/release-sandbox.json \
  --av-diagnostics visual_edition/chapters/<chapter>/generation-2/av_diagnostics.json \
  --output visual_edition/chapters/<chapter>/generation-2/render_receipt.json
python3 skills/asi-stack-manim-videos/scripts/sample_video_beats.py \
  build/visual_edition/generation-2/final/<chapter>.mp4 \
  visual_edition/chapters/<chapter>/generation-2/beat_plan.json \
  --sample-set final
python3 skills/asi-stack-manim-videos/scripts/build_caption_review_sheet.py \
  build/visual_edition/generation-2/final/<chapter>.mp4 \
  visual_edition/chapters/<chapter>/generation-2/captions.vtt \
  visual_edition/chapters/<chapter>/generation-2/receipts/caption-overlay.png \
  --report-json visual_edition/chapters/<chapter>/generation-2/receipts/caption-diagnostics.json
python3 scripts/sync_manim_v2_production_ledger.py
python3 scripts/validate_manim_v2_production_ledger.py
```

## Invalidation

| Changed input | Reopen |
|---|---|
| chapter, claim, source, or evidence ceiling | treatment and all downstream gates |
| treatment or narration | script and all downstream gates |
| voice, model, settings, block audio, or pronunciation | timing, captions, mix, reviews |
| alignment method or anchors | beat timing, captions, lock, reviews |
| beat plan or scene | render, samples, reviews, acceptance |
| captions or transcript | picture-and-sound lock and all downstream gates |
| thumbnail/title/description/source card | packaging review and publication receipt |
| story, treatment guidance, treatment schema, or chapter/source context | treatment and all downstream gates |
| scene audit, Manim patterns, primitive regression, visual grammar, or visual toolchain | animatic and all downstream gates |
| sampling or experience-review contract | owning review and all downstream gates |
| caption/A/V diagnostic contract | picture-and-sound lock and downstream gates |
| isolated runner | animatic and all downstream gates |
| sandbox-receipt schema | animatic and all downstream gates |
| render-receipt contract or final-receipt compiler | picture-and-sound lock and downstream gates |

The ledger records the whole skill-bundle digest for provenance and separate
component digests for invalidation. Do not reopen treatment because an
unrelated caption or sampling helper changed.

Preserve old receipts and artifacts as historical identity. Reopening a gate is
not deletion and does not imply the earlier artifact never existed.

## Historical revisions and publication

Compare a replacement to its predecessor at matched playback level and display
size. Keep a change only when it solves a named viewer problem or satisfies a
new contract. “More animated” is not a rationale.

YouTube cannot replace a binary in place. Preserve stable internal chapter
identity, create generation N+1, obtain exact authority, upload and verify the
replacement, normally unlist or privately preserve its predecessor, and update
video ID, visibility, captions, thumbnail, description, source delivery,
playlist, receipt, ledger, packet, and Quarto embed together. No local review
authorizes an external mutation by implication.
