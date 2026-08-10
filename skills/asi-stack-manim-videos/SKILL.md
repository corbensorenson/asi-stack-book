---
name: asi-stack-manim-videos
description: Design, write, art-direct, implement, synchronize, caption, audit, review, revise, render, and maintain ManimCE or Manim-composited hybrid visual abstracts for chapters of Corben Sorenson's living book The ASI Stack. Use for treatment and teaching-promise selection, narration, semantic keyframes, storyboards, beat plans, Manim scene code, TTS and forced alignment, audiovisual review, accessibility, thumbnails, YouTube supersession, or diagnosing videos that are inaccurate, wordy, static, generic, visually monotonous, uncomfortable, inaccessible, or out of sync.
---

# ASI Stack Manim Videos

Make an original visual explanation whose pictures and words change the same mental
model at the same time. The canonical chapter and evidence surfaces remain
authoritative; a derivative video never strengthens a book claim.

## Non-negotiable contract

1. **One transferable promise.** A short video selects one consequential idea, not
   a chapter summary. Its case, representation bridge, and signature change must
   earn chapter-specific identity rather than reuse a noun-swapped series template.
2. **Standalone audience.** Default to a curious adult interested in AI, with no
   research background or prior-chapter context. Record any different assumptions.
3. **Source-bound truth.** Bind every spoken or visual inference to chapter
   claim IDs or verified source IDs. Record assumptions, non-claims, notation,
   units, simplifications, and truth checks. Do not speak repository metadata
   unless repository mechanics are themselves the teaching subject.
4. **Co-design before production.** Iterate narration, rough keyframes, and the
   concrete case together. Do not lock ideas that cannot earn pictures or polish
   scenes for an unstable story.
5. **Audio owns final time.** Editorial estimates support planning only;
   synthesis-block timing supports an animatic; manually reviewed forced
   alignment is required for picture-and-sound lock.
6. **Motion carries meaning.** Motion may encode identity, relation, causality,
   sequence, quantity, uncertainty, contrast, containment, authority,
   rollback, or attention. Intentional stillness is valid when it gives time to
   predict, compare, read, or absorb; declare it as a hold and introduce
   nothing new during it.
7. **Two release reviews.** A source-aware critic checks claim fidelity. A
   separate cold audience proxy checks comprehension and changed-condition
   transfer without source, script, code, or answer-key access. An AI proxy is
   diagnostic evidence about the artifact, not evidence of human learning.
8. **Accessibility and rights are design inputs.** Meaning must survive color
   loss, motion reduction, captions, and ordinary playback. Every external
   asset, font, voice, music cue, and effect needs provenance and usable rights.
   Citation is not permission, and generated media is not factual evidence.
9. **Receipts over declarations.** Every passing gate binds exact artifact
   digests and review evidence. A material upstream edit reopens every dependent
   gate.
10. **No false superlatives.** Report observed strengths, passed checks, known
    defects, and untested conditions. Never call a video optimal, proven to
    teach, or “best possible.”

## Load only the needed references

- Narration, promise, or story work: [writing-and-story.md](references/writing-and-story.md)
  and [learning-and-engagement.md](references/learning-and-engagement.md).
- Treatment, composition, keyframes, motion, or visual critique:
  [art-direction-and-motion.md](references/art-direction-and-motion.md).
- Manim architecture, scene implementation, or reusable primitives:
  [manim-patterns.md](references/manim-patterns.md).
- TTS, alignment, captions, mix, or motion comfort:
  [audio-and-accessibility.md](references/audio-and-accessibility.md).
- Any production-state or repository change:
  [asi-stack-pipeline.md](references/asi-stack-pipeline.md).
- Any animatic, lock, or release decision:
  [experience-review.md](references/experience-review.md).
- Research rationale, upstream examples, compatibility, or licensing:
  [research-basis.md](references/research-basis.md).

In the book repository, also read the complete chapter, packet, source notes,
`visual_edition/README.md`, `visual_edition/visual_grammar.json`, generation-two
ledger, narration toolchain, and current generation directory. Generation one and
superseded generation-two artifacts are history, not automatic authoring inputs.

Bind the treatment to the ledger's exact chapter and source-context digests. The
latter covers every assigned source note and inventory record; memory or a stale
visual packet is not the current authority surface.

Run bundled commands from the repository root; otherwise set `ASI_STACK_BOOK_ROOT`.
Accepted renders must execute the tracked runner. The installed skill copy supplies
instructions and diagnostics, not a substitute executable identity.

## Artifacts and state

For each chapter, use this generation-two topology:

```text
generation-2/
  treatment.json       # source, audience, story, keyframes, assets, script gate
  narration.txt        # exact approved words after the script gate passes
  beat_plan.json       # exact narration split into audio-timed semantic beats
  scene.py             # deterministic chapter-specific implementation
  captions.vtt         # derived from qualified alignment, then manually edited
  transcript.md        # narration plus consequential visual description
  thumbnail.*          # honest promise with alt text and provenance
  av_diagnostics.json  # mechanical A/V findings bound to master and beat plan
  render_receipt.json  # compiler-derived exact release custody; never hand-authored
  receipts/            # timing, alignment, samples, and sandbox-policy evidence
  reviews/
    <pass>.json         # assessed review record
    <pass>.context.json # exact isolated material and prompt bindings
    <pass>.prompt.md    # prompt delivered in that review session
    <pass>.raw.md       # response preserved before assessment
```

The state order is `planned -> narration_draft -> treated -> script_passed ->
beat_planned -> animatic -> picture_and_sound_lock -> release_candidate -> accepted`.
A clean narration linter result is not `script_passed`; a render is not acceptance.

## Workflow

### 1. Establish truth, audience, and medium

Read the whole chapter and evidence surfaces. Extract only claims needed for one
visual argument and record what it must not imply. Verify external sources at
source-note depth; a search snippet or abstract is not evidence.

Write the audience assumptions and standalone context. Decide whether the
teaching mechanism is best served by Manim, a hybrid, stills, screen recording,
or conventional editing. Manim is preferred for state, geometry, derivation,
flow, and persistent identity, not because this is a Manim series. Record the
medium rationale and every planned external asset in `treatment.json`.
Use code-native diagrams for evidence-bearing geometry, quantities, labels, and
system state. A generated bitmap may supply an original illustrative object or
texture only when its prompt/model provenance, rights, digest, and factual
inspection are recorded; it must not silently invent evidence or tiny text.

The current accepted final compositor is the tracked ManimCE Cairo runner.
`hybrid` means rights-cleared, digest-bound media enters that audited Manim
scene as an asset; it does not authorize an unreceipted external final edit.
A still-, screen-recording-, or conventional-edit-primary treatment may be
explored, but its script gate and release path remain blocked until a tracked
adapter emits equivalent schema-validated execution and final-custody receipts.

### 2. Select the teaching promise

Generate three to five genuinely different candidate promises. Compare each on
consequence, visual mechanism, changed-case transfer, and evidence fit. Select
exactly one. Use one concrete case, one central mechanism, relationship, or
tradeoff, one discriminating test or counterexample, one local evidence
boundary, and at most three introduced terms.

Make the bridge explicit: concrete object -> causal change -> earned abstraction ->
changed case. Preserve a visible mapping and state where any analogy stops. A
closing disclaimer cannot repair an overbroad picture.

Do not force a misconception, naive shortcut, prediction prompt, joke, or
failure when the chapter supplies no honest basis for it. Record whether the
tension comes from an observed failure, documented misconception, design
tradeoff, open question, or counterexample. A useful question must be
answerable from the visual and receive thinking time; zero questions is valid.

### 3. Co-design treatment, narration, and keyframes

Draft normally four to six macro changes in the viewer's mental model; use
three or seven when the explanation genuinely needs it. For each, sketch
a sparse semantic keyframe and state what remains invariant. Write narration
in coherent performance blocks while revising the keyframes. Let a strong
picture replace words; use narration for relationships, causes, consequences,
and qualifications that the picture cannot safely carry alone.

Before detailed keyframes or code, compare two or three cheap visual-mechanism
sketches. Choose by causal fidelity, apprehensibility, continuity, transfer,
accessibility, and production risk, not novelty. Compare the winner with current
generation-two work so series consistency does not become episode templating.

The treatment must record:

- audience, promise candidates, selection rationale, and transfer criterion;
- chapter claims, source IDs, non-claims, assumptions, visual simplifications,
  notation/symbol/unit ledger, and retained truth checks;
- concrete case, selected story form and authority basis, normally four to six
  macro moves expressed as viewer-before -> visible event -> viewer-after,
  opening, payoff, and predeclared comprehension and changed-case
  transfer prompts with success criteria;
- honest working title, thumbnail promise and alt text, first-15-second
  delivery, source end-card/description plan;
- medium, visual thesis, signature and ending images, persistent objects,
  invariants, normally four to eight semantic keyframes, and asset provenance;
- performance blocks, pronunciation items, music/effect policy, playback
  devices, caption-safe composition, description, contrast, and motion plan;
  and
- the narration path, digest, word count, reviews, defects, and gate verdict.

Retain failed or uncertain truth checks with their resolution path while
drafting. They block script approval; they must not be deleted to make Gate 0
look clean.

Normal form is roughly 2.5-4.5 minutes and 280-520 spoken words. These are selection
diagnostics, not quotas; never pad a short complete treatment. Above 600 words needs
a duration rationale; above 650 must be split or reselected. Do not accelerate a
bad script. Read it aloud. Reject inventory, paper signposting, internal status,
unexplained jargon, late qualifiers, or any sentence without a meaningful picture,
relationship, or deliberate audio-only purpose.

Structural lint can run during drafting:

```bash
python3 skills/asi-stack-manim-videos/scripts/audit_video_plan.py \
  --narration path/to/narration.txt --narration-only
python3 skills/asi-stack-manim-videos/scripts/audit_video_plan.py \
  --all-narrations visual_edition/chapters
```

The corpus diagnostics locate possible cadence and language reuse; they do not
reward arbitrary variation. Compare every trigger that affects the draft and
record its disposition in the treatment review or as an open defect. A warning
does not auto-fail a script, but unresolved noun-swappable templating blocks
Gate 0. Neither command approves truth, voice, or visualizability. Record all
three manual reviews in the treatment, bind the exact narration digest, and
then run Gate 0:

```bash
python3 skills/asi-stack-manim-videos/scripts/audit_video_plan.py \
  --treatment path/to/treatment.json \
  --narration path/to/narration.txt --treatment-only
```

### 4. Produce audio and the timed visual argument

After Gate 0, synthesize coherent performance blocks with the pinned local TTS. Preserve
prosody across regenerated lines. Record model/version, voice, settings,
license, disclosure, block digests, durations, and pronunciation results.
Audition the voice alone.

The current TTS and ASR virtual environment is a pinned local trusted-computing
base, not an OS sandbox. It loads only digest-bound local JSON, Safetensors, and
NPZ model files, uses offline library hints, and binds the exact FFmpeg
normalizer. Do not enable remote code, arbitrary model paths, escaped output
paths, or a different executable. Do not describe this boundary as network or
credential isolation; a future adapter must earn those claims with receipts.

Human-recorded narration may be auditioned, but the current acceptance contract
does not ingest it. It remains blocked until a tracked recording adapter binds
the performer or consent basis, session and edit provenance, exact audio,
processing chain, rights, and an equivalent content-verification receipt.

For the pinned local toolchain, preserve paragraph boundaries as performance
blocks and use its exact speed and canonical ignored-build filename. Then run
the pinned ASR/content validator. This establishes audio identity and content
agreement, not final word timing or voice quality:

```bash
build/visual_edition/tts_venv/bin/python scripts/render_visual_narration.py \
  --text visual_edition/chapters/<chapter>/generation-2/narration.txt \
  --output build/visual_edition/audio/<chapter>-narration-master.wav \
  --speed 1.08
build/visual_edition/tts_venv/bin/python scripts/transcribe_visual_narrations.py \
  --chapter <chapter>
build/visual_edition/tts_venv/bin/python scripts/validate_visual_narration.py \
  --audio build/visual_edition/audio/<chapter>-narration-master.wav \
  --receipt build/visual_edition/audio/<chapter>-narration-master.receipt.json \
  --asr build/visual_edition/audio/<chapter>-narration-master.json \
  --report build/visual_edition/audio/<chapter>-narration-master.validation.json
```

The transcriber invokes that validator automatically; the explicit command is
the reproducible replay. Both must pass on current digests. Neither establishes
word timing, naturalness, or listener preference.

When verification fails, follow the localization and regeneration procedure in
[audio-and-accessibility.md](references/audio-and-accessibility.md); never weaken
the WER, beginning, ending, or omission thresholds. A passing rerun closes
content custody only; acoustic audition remains required.

```bash
build/visual_edition/tts_venv/bin/python \
  skills/asi-stack-manim-videos/scripts/diagnose_narration_asr.py \
  --receipt build/visual_edition/audio/<chapter>-narration-master.receipt.json \
  --asr build/visual_edition/audio/<chapter>-narration-master.json
```

Create `beat_plan.json` by splitting the exact narration at semantic and audio
anchors. Each beat binds its treatment macro move, performance block, source
references, claim role, visual inference, evidence boundary, attention target,
object state, composition, motion, text, and timing state.

- `estimated`: editorial estimate; no fake receipt; planning only.
- `block_timed`: exact synthesis-block receipt plus its passing, digest-bound
  ASR/content verification report; eligible for an animatic.
- `forced_aligned`: version-pinned alignment plus bound manual anchor review;
  required for picture-and-sound lock.

Read the current narration toolchain before timing work. The accepted route is
exact-text, phrase-scoped stable-ts alignment through pinned MLX Whisper. It
qualifies unique positive-duration phrase anchors, caption-line boundaries,
and generation-block joins; it does not qualify phoneme timing or isolated
instantaneous word boundaries. Never relabel block timing or raw ASR
timestamps as forced alignment.

Run the tracked adapter with the pinned alignment environment. The raw
alignment remains under ignored build custody; the compact receipt is tracked.
The adapter must exit nonzero on transcript, ordering, overlap, edge, anchor,
instant-word-fraction, or generation-join failure.

```bash
build/visual_edition/alignment_venv/bin/python \
  skills/asi-stack-manim-videos/scripts/align_visual_narration.py \
  --audio build/visual_edition/audio/<chapter>-narration-master.wav \
  --narration visual_edition/chapters/<chapter>/generation-2/narration.txt \
  --beat-plan visual_edition/chapters/<chapter>/generation-2/beat_plan.json \
  --narration-receipt build/visual_edition/audio/<chapter>-narration-master.receipt.json \
  --narration-verification build/visual_edition/audio/<chapter>-narration-master.validation.json \
  --output build/visual_edition/audio/<chapter>-alignment.json \
  --receipt visual_edition/chapters/<chapter>/generation-2/receipts/alignment.json
```

Listen to every consequential phrase anchor in context and bind a distinct
zero-failure `alignment-review.json` to the exact audio and receipt before
using `forced_aligned`. Never cue a semantic event from a zero-duration word;
use a reviewed multiword phrase span. Regeneration invalidates the receipt and
review even when the written text is unchanged.

For a block-timed animatic, raw ASR segment boundaries may locate provisional
playback windows only. Record them as diagnostic cue hints outside the governed
beat times; do not use them for captions, claim phrase precision, or change the
timing state. A performance block longer than 20 seconds that contains more than
one denial, collision, transfer test, comparison, or proof boundary must use
separate scene-internal cue windows checked against the mux. Do not stretch one
`LaggedStart`, `Succession`, or generic scheduler across the whole block and
infer that source order synchronized the events. If ASR segmentation and heard
phrasing disagree, the heard phrase controls the draft repair and the mismatch
remains open until qualified alignment.

Use `mode: change` when an object or relation changes. Use `mode: hold` only
when before and after states match, the purpose is explicit, and no term or
relationship is introduced. A brief post-motion settle can be shorter than the
visual grammar's 1.2-second material hold; do not mislabel settling as a new
teaching beat. Beat density and technique count are diagnostics, never targets.

```bash
python3 skills/asi-stack-manim-videos/scripts/audit_video_plan.py \
  path/to/beat_plan.json \
  --treatment path/to/treatment.json \
  --narration path/to/narration.txt
```

### 5. Implement semantic objects, not slides

Use one persistent visual world and preserve object identity across changes.
Create chapter-specific objects with meaningful state setters; use transforms,
trackers, updaters, graph movement, matching parts, and focus isolation when
they reveal the mechanism. Keep labels adjacent to objects and short enough to
scan without competing with speech.

Before rendering, preflight the pinned ManimCE runtime, fonts, LaTeX/packages,
codecs, external assets, licenses, random seeds, resolution, frame rate, and
audio tools. Do not assume ManimGL examples are API-compatible with ManimCE.
Use `Scene.next_section()` at semantic boundaries and render low-resolution
sections during iteration.

Mechanical diagnostics are search tools, not optimization objectives. After a
warning-driven revision, compare the new normal-speed playback and sampled
transition frames with the prior artifact. Revert a revision that reduces a
freeze or black-frame count by introducing distorted interpolation, duplicated
objects, premature answers, off-canvas geometry, or motion without explanatory
work. Keep the warning open and advance timing evidence instead of repeatedly
tuning motion to the detector.

```bash
python3 scripts/validate_manim_toolchain.py --probe-runtime
python3 skills/asi-stack-manim-videos/scripts/audit_scene_source.py \
  path/to/scene.py --treatment path/to/treatment.json
# Portable custody check; this does not claim a graphical replay.
python3 skills/asi-stack-manim-videos/scripts/audit_primitive_regression.py --static-only
# Full graphical replay on the pinned macOS runtime.
python3 skills/asi-stack-manim-videos/scripts/audit_primitive_regression.py
python3 skills/asi-stack-manim-videos/scripts/render_scene_isolated.py --self-test
python3 skills/asi-stack-manim-videos/scripts/build_final_render_receipt.py --self-test
```

Treat every downloaded scene, plugin, model, font, media file, and build command
as untrusted until its provenance, license, digest, and behavior are reviewed.
Manim scenes are arbitrary Python: never execute copied or generated code just
because it renders in an example repository. Keep network access and secrets
out of render execution, reject unexpected subprocess or filesystem behavior,
and vendor only the smallest reviewed dependency needed.

The source audit is a narrow static preflight, not a security boundary. It
permits only the digest-bound `visual_edition.lib.asi_visuals` local helper;
adding another helper requires extending its audit, digest, and regression
contract first. Execute even a passing scene under an OS, container, CI, or
Codex sandbox that denies network access, strips credential-bearing environment
variables, and restricts repository writes to `build/visual_edition/`.

On the pinned macOS toolchain, use the tracked runner instead of a direct Manim
command. Its live policy self-test must pass in a non-nested shell before use:

```bash
python3 skills/asi-stack-manim-videos/scripts/render_scene_isolated.py \
  visual_edition/chapters/<chapter>/generation-2/scene.py <SceneClass> \
  --treatment visual_edition/chapters/<chapter>/generation-2/treatment.json \
  --audio-master build/visual_edition/audio/<chapter>-narration-master.wav \
  --profile draft \
  --receipt visual_edition/chapters/<chapter>/generation-2/receipts/animatic-sandbox.json
python3 skills/asi-stack-manim-videos/scripts/audit_av_experience.py \
  build/visual_edition/isolated-renders/<chapter>/draft/<chapter>-animatic.mp4 \
  --plan visual_edition/chapters/<chapter>/generation-2/beat_plan.json \
  --target-lufs -16 --animatic-preflight
python3 skills/asi-stack-manim-videos/scripts/sample_video_beats.py \
  build/visual_edition/isolated-renders/<chapter>/draft/<chapter>-animatic.mp4 \
  visual_edition/chapters/<chapter>/generation-2/beat_plan.json \
  --sample-set animatic
```

The runner enforces network, read, write, executable, wall-time, CPU-time,
file-size, open-file, process-count, environment, and core-dump boundaries and
emits the exact policy, command sequence, preflight identity, and outputs.
Its receipt lists the broad system-content roots required by Python, Manim, and
native libraries while denying unlisted repository file contents.
macOS does not provide this adapter a hard resident-memory bound; the receipt
must retain that explicit non-claim. Preserve and validate the runner-produced
receipt. Do not hand-author an isolation declaration or run a direct
unsandboxed Manim or mux command for an accepted artifact. A container or CI
backend is not accepted until it emits an equivalently schema-validated receipt
and gains a tracked adapter.

Put a primitive in `visual_edition/lib/` only after at least two chapters share
the behavior. Add a Manim graphical frame-comparison regression test for every
shared primitive and for high-risk deterministic geometry. Chapter scenes
still require rendered playback review; a snapshot cannot judge teaching,
motion, or synchronization.

Never update a graphical baseline merely to make a failure disappear. Capture
candidate frames, inspect them at original resolution for geometry, typography,
clipping, overlap, and hierarchy, record the reason for accepting the change,
then update the content-addressed baseline and rerun the regression.

### 6. Iterate at the cheapest valid gate

1. **Animatic:** rough geometry, near-final audio, at least block-timed beats.
   Repair promise, story, keyframes, continuity, and pacing before polish.
2. **Picture-and-sound lock:** final geometry, narration, manually reviewed
   forced alignment, captions, transcript, easing, camera, voice, mix, and the
   exact release-profile mux and receipts that will be reviewed.
3. **Release candidate:** pinned 1920x1080/30 master, exact receipts,
   descriptive transcript, thumbnail, source delivery, and complete checks.

Once the scene, audio, captions, transcript, and alignment are ready for lock,
render the release-profile candidate through the tracked runner. Sync the
ledger so it owns the ignored-build master, run the A/V diagnostic against
that master and the forced-aligned beat plan, compile `render_receipt.json`
from those exact artifacts, and sync again. Run picture-and-sound lock review
against this exact candidate and its receipt; any resulting edit creates a new
candidate and reopens the review. Never hand-author the final receipt.

Use the exact [release candidate command sequence](references/asi-stack-pipeline.md#release-candidate-command-sequence);
do not reconstruct it from memory or omit either ledger synchronization.

Sample at least start, quarter, midpoint, three-quarter, and end of every beat,
plus risky interpolations. Store the sample manifest and digest. Watch motion
at 1x; contact sheets cannot judge easing or sync. Use
`sample_video_beats.py`, `audit_av_experience.py`, and
`build_caption_review_sheet.py` as diagnostics, not aesthetic judges.
Generate one final sample set per exact master/plan identity and bind that same
set into lock, source-aware, and cold reviews. Regenerate only when the media,
plan, sampler, FFmpeg identity, or required targeted samples change.

Caption review must use the exact final VTT and mux. The sheet can flag timing,
line, and reading-load risks; it cannot automatically prove that captions do
not cover the active mechanism. Inspect the actual caption overlay at normal
playback and phone size. Derive final cue timing only from qualified alignment,
not synthesis-block interpolation.

The static source gate blocks Manim's named flash effects. Deliberate flashing
remains release-blocking until a qualified full-frame WCAG flash-threshold
analyzer and manual review are bound; FFmpeg's photosensitivity diagnostic is
not a conformance proof.

### 7. Run both release reviews

Follow [experience-review.md](references/experience-review.md) and the v4
review schema. A passing review must bind the exact master, treatment, beat
plan, narration, captions, transcript, receipt, sample manifest, and digests;
pass every required viewing mode; score every applicable dimension at least
4/5 with timestamped evidence; and retain no unresolved material defect.

Create each release review in a fresh task or independent human session.
Before review, freeze a context manifest and prompt that enumerate the exact
allowed files and digests. Preserve the raw response before adding criteria,
scores, defect dispositions, or a verdict. A reviewer assertion of freshness
without the bound context, prompt, and raw response cannot pass.
If that independent context cannot be obtained, leave the gate blocked; the
authoring agent must not review its own work and relabel the result independent.

- **Source-aware release critic:** did not author the script or implement the
  scene; may read chapter, sources, treatment, and beat plan; must score claim
  fidelity and inspect every visual inference and qualifier.
- **Cold audience proxy:** did not author or implement anything and had no
  prior exposure; receives only rendered video plus captions or descriptive
  transcript; receives no answer key; records raw responses to comprehension
  and changed-condition transfer prompts against predeclared criteria. A pass
  binds an exact raw-response excerpt to a timestamped cue or causal transition
  in the artifact; generic prior-knowledge answers fail. This lane must not
  score claim fidelity.

An external human is welcome but is not an invented prepublication blocker.
When no human study exists, say so. Retention, proxy answers, and reviewer
scores are revision signals, not proof of human learning.

### 8. Accept, publish, and learn conservatively

Accept only after treatment, script, beat plan, animatic, lock, both release
reviews, technical checks, and claim-fidelity gates pass. Preserve prior
generations and receipts. Never overwrite an uploaded video in project
history, infer authorization, or claim that media acceptance changes chapter
support.

YouTube replacement requires action-time authority. Reconcile new video ID,
visibility, captions, thumbnail, source description, playlist position,
predecessor state, packet, ledger, and Quarto embed as one governed mutation.
After enough viewers exist, use retention dips/spikes only to form a recorded
revision hypothesis. Do not optimize for engagement at the expense of truth or
understanding.

## Invalidation and stopping rule

Reopen downstream work whenever its input identity changes:

- chapter/source/claim change -> treatment, script, timing, scene, captions,
  transcript, reviews, and acceptance;
- treatment or narration change -> script gate and everything after it;
- TTS/settings/audio change -> timing, captions, mix, playback reviews;
- beat plan or scene change -> render, samples, reviews, acceptance;
- caption/transcript/thumbnail change -> accessibility or packaging review and
  any release binding that includes it;
- skill/schema/toolchain change -> every gate affected by that contract.
- final-receipt compiler change -> release candidate and downstream gates.

Use component-scoped invalidation: a caption diagnostic change reopens caption
and lock review, a scene-audit or primitive-regression change reopens animatic
work, and a story or treatment-contract change reopens treatment. Preserve the
whole skill-bundle digest for provenance, but do not restart editorial work
solely because an unrelated helper changed.

Stop polishing only when the promise is delivered, every creative choice has a
teaching or accessibility rationale, all required gates bind current artifacts,
no material defect remains, and further change lacks a named viewer problem.
Report residual risks: no human-learning evidence, untested devices or
audiences, toolchain limitations, or any accepted minor defect.
