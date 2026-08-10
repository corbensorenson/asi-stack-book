# Audio, Captions, and Viewing Comfort

## Contents

- Direct the voice
- Qualify and align TTS
- Mix for comprehension
- Use music and sound effects sparingly
- Integrate accessibility into authorship
- Review motion comfort
- Measure without mistaking measurement for quality

## Direct the voice

Write and synthesize for a human thought process, not a document reader.

- Mark the operative word in each sentence and vary emphasis around it.
- Use short pauses before a prediction, after a reveal, and between distinct
  causal steps. Do not insert identical pauses after every sentence.
- Let pace accelerate through an already-understood construction and slow at a
  new mechanism, failure, or evidence boundary.
- Create a pronunciation sheet for names, acronyms, symbols, and chapter terms.
- Remove clicks, clipped breaths, duplicated syllables, abrupt edits, and
  changes in voice character between regenerated lines.
- Prefer a warm, direct delivery over announcer intensity. Excitement should
  come from the idea becoming visible.

Listen to the narration without video. If its structure is unclear on its own,
the animation is being asked to repair the script.

Synthesize coherent performance blocks rather than isolated sentences. A block
should carry one thought, pacing instruction, and emotional contour. Preserve
enough surrounding text when regenerating a line to avoid a visible change in
prosody, then crossfade only at a natural boundary. Fixed pauses after every
sentence create a mechanical cadence; direct pauses by meaning.

## Qualify and align TTS

Keep the current pinned voice until a controlled audition demonstrates a better
choice. Model novelty is not a reason to regenerate a series. For a candidate
voice or model, synthesize the same 60–90 second excerpt and compare at matched
loudness without revealing the provider when practical. Score:

- intelligibility and pronunciation;
- naturalness across a complete thought;
- controllable emphasis, contrast, questions, and pauses;
- consistency across regenerated blocks and a long-form passage;
- alignment quality and caption timing;
- latency, reproducibility, hardware and dependency burden;
- license, redistribution, disclosure, privacy, and cost; and
- voice-likeness or cloning rights.

Keep production and audition custody separate. The production renderer accepts
only the canonical chapter narration path, ignored-build audio root, pinned
local model directory, pronunciation lexicon, settings, and digest-bound
FFmpeg normalizer. The local TTS/ASR virtual environment is part of the trusted
computing base; offline library flags are not an OS network sandbox and do not
prove credential isolation. A candidate that requires remote code, an online
download during synthesis, pickle-style model execution, or an arbitrary
normalizer remains outside the production route until a separately reviewed
adapter can bind and constrain it.

Do not clone or imitate a person's voice without explicit consent and usable
publication rights. Record the selected model, exact version, voice, settings,
license, and disclosure policy in the tracked toolchain. Candidate systems such
as Kokoro, Qwen3-TTS, Chatterbox, Fish Audio, or a hosted service must pass the
same audition; this document does not pre-approve any of them.

After final synthesis, use forced alignment for word or phrase timestamps.
Whisper transcription is useful for content verification but is not by itself
a precise synchronization contract. Prefer a pinned WhisperX, Montreal Forced
Aligner, stable-ts, or equivalent route whose language, model, and failure
behavior are recorded. Manually inspect anchors around names, symbols, pauses,
and regenerated joins.

Keep three states distinct. Editorial timing is a planning estimate.
Synthesis-block durations are exact only at block boundaries and may time an
animatic. Final beat and caption timing requires a qualified aligner plus a
bound manual anchor review. Never create apparent word precision by evenly
distributing a block duration.

Whisper segment timestamps may help an editor find a phrase during a
block-timed animatic, but they remain diagnostic localization. Keep those cue
hints out of governed beat boundaries and captions, check each consequential
event by listening to the mux, and preserve any disagreement for alignment
review. When one synthesis block exceeds 20 seconds and owns several semantic
events, create provisional scene-internal cue windows around the heard phrases;
whole-block interpolation is not synchronization.

Qualifying an aligner requires a tracked adapter and receipt schema, not a
toolchain label edited by hand. Bind the implementation, version, acoustic
model, lexicon, language, exact transcript and audio, settings, runner digest,
and output digest. Freeze a human-reviewed fixture that covers ordinary prose,
coined terms, acronyms, numbers, pauses, questions, and regenerated joins.
Predeclare the scoring method before running candidates. At 30 fps, require at
least 95% of reviewed cue-onset anchors within two frames of the gold anchor;
permit no consequential name, symbol, pause, join, beat boundary, or question
anchor beyond four frames after recorded manual correction. Require monotonic
complete token custody, exact paragraph order, stable repeated output, and no
beat crossing. Reject corrupted audio, transcript, model, lexicon, runner,
settings, non-monotonic timestamps, missing tokens, duplicated tokens, and
out-of-range boundaries in negative controls. Preserve corrections as a bound
manual review; never silently edit the VTT and retain the old alignment receipt.

The two-frame cue-onset target follows Netflix's published 30 fps timing
allowance; the 95% qualification rule and four-frame corrected-anchor ceiling
are this project's explicit operational criteria, not universal learning or
accessibility guarantees.

Use the repository's pinned route rather than relying on script defaults:

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

The transcription runner invokes the validator; the explicit command replays
the same digest-bound check without retranscribing. It is not a forced aligner.
The ASR validator treats duration ranges as diagnostics. A short explanation
does not fail merely for being short; never pad narration to satisfy a clock.
The synthesis receipt can seed block-timed animatic captions, but it cannot
produce a final forced-aligned caption track.

Treat an ASR failure as a localization task, not a reason to relax the gate.
Compare the exact expected and recognized tokens, then distinguish a clipped or
mispronounced performance from recognizer ambiguity. Rewrite nonessential
chapter-local wording when a fictional name, homophone, or segmentation choice
is needlessly ambiguous in speech. Reserve the shared pronunciation lexicon for
stable series-wide terms that have been auditioned in context; a lexicon edit
invalidates every affected master and must not be used to rescue one chapter at
the expense of the corpus. Regenerate the complete thought block, rerun ASR and
signal validation, and still listen to the result. Zero content error is strong
custody evidence, not proof of natural cadence or correct emphasis.

Use `diagnose_narration_asr.py` to print the exact raw and content-normalized
edit blocks with exact input, validator, and diagnostic digests. It is read-only
and diagnostic: it neither changes the canonical normalization contract nor
passes the content gate. Invoke it with the pinned TTS/ASR interpreter because
it imports the canonical signal validator rather than copying that validator's
normalization rules:

```bash
build/visual_edition/tts_venv/bin/python \
  skills/asi-stack-manim-videos/scripts/diagnose_narration_asr.py \
  --receipt build/visual_edition/audio/<chapter>-narration-master.receipt.json \
  --asr build/visual_edition/audio/<chapter>-narration-master.json
```

## Mix for comprehension

Treat speech as the primary signal. Pin a project loudness target and use it
consistently across the series. Measure integrated loudness, loudness range,
and true peak, but judge comfort on real playback systems as well.

- Keep true peak at or below -1 dBTP unless the repository declares a stricter
  target.
- Avoid large chapter-to-chapter loudness jumps.
- Keep background sound substantially below narration. A useful accessibility
  stress criterion is roughly 20 dB lower than foreground speech, based on
  WCAG's enhanced-audio guidance.
- Duck music further under dense terms, definitions, and evidence qualifiers.
- Preserve a low noise floor without aggressive processing that makes the
  voice brittle or pumping.
- Add short fades at audio boundaries and listen for discontinuities at every
  regenerated splice.
- Keep a lossless narration master. Encode distribution audio only after the
  final mix and caption alignment pass.

Do not apply the EBU R128 broadcast target of -23 LUFS as a universal YouTube
target. Use EBU measurement concepts and the -1 dBTP ceiling while following
the project's explicitly pinned online-delivery target.

## Use music and sound effects sparingly

Music can provide warmth, continuity, and a sense of progression. It must be
original, licensed for this publication, or drawn from a rights-cleared
library. Do not reuse 3Blue1Brown's music or imitate its melodies.

- Give music an arc that follows the explanatory arc; do not loop one dramatic
  bed at constant intensity.
- Remove music when silence improves concentration or gives a reveal weight.
- Use sound effects only to clarify a semantic event such as a gate closing,
  route switching, state restoring, or threshold crossing.
- Do not attach a sound to every motion. Repetition quickly becomes irritating
  and competes with narration.
- Include important non-speech sounds in captions.

## Integrate accessibility into authorship

Design narration so it naturally identifies meaningful visual objects and
changes. W3C notes that integrated description can make a newly produced video
accessible without a separate description track when the main audio already
contains the necessary information.

For every release:

- provide synchronized captions from the exact final narration;
- include meaningful sound cues in captions;
- provide a descriptive transcript that covers important visual information;
- avoid color-only, sound-only, or motion-only meaning;
- preserve sufficient contrast and readable text size;
- keep captions from covering the active mechanism; and
- verify captions, transcript, and media all describe the same generation.

Preserve intentional caption line breaks in the VTT. The project's default
review thresholds (two lines, 42 characters per line, and 180 words per minute)
are conservative diagnostics, not universal accessibility laws; tighten them
for a younger or less technical audience and override only with a recorded
playback rationale. Risk-sample the fastest, shortest, longest, first, and last
cues as well as distributed coverage.

A generated caption contact sheet simulates one overlay style. It cannot prove
how YouTube or another target player renders the cue, and it cannot infer the
active teaching region from pixels. Review the exact final VTT in the actual
player at normal speed and phone size. Check synchronization, authored line
breaks, reading comfort, speaker changes, meaningful sound labels, and whether
the overlay covers the active mechanism.

Narration need not describe every decorative detail. It must convey any visual
fact required to understand the teaching promise.

Use WCAG 2.2 contrast ratios as conservative design floors for the rendered
pixels: 4.5:1 for ordinary text, 3:1 for genuinely large text, and 3:1 for
meaningful graphical boundaries. Measure the worst adjacent frame when a
background moves or changes. These checks improve video legibility; they do not
by themselves establish web-player conformance.

## Review motion comfort

Do not use Manim's `Flash` or `ShowPassingFlash` effects in the accepted route.
Avoid deliberate flashing altogether unless a qualified full-frame analyzer
tests the general and saturated-red WCAG thresholds at the largest expected
viewing scale and a manual reviewer passes the sequence. FFmpeg's
`photosensitivity` filter is an imperfect diagnostic, not a medical or WCAG
conformance test. Review parallax, spinning, multi-axis movement, vortex-like
movement, continuous zoom, shake, and large-field motion for discomfort.

When motion carries meaning, preserve that meaning through a label, change of
state, dissolve, highlight, or positional endpoint. Apple recommends replacing
some motion with fades, highlights, or color shifts rather than deleting its
meaning. Treat this as a design principle for the video, even though a rendered
video cannot fully honor an operating-system reduced-motion preference.

## Measure without mistaking measurement for quality

Mechanical checks can find clipping, silent gaps, black frames, long freezes,
caption drift, or an outlier loudness profile. They cannot determine whether a
voice is pleasant, music is emotionally appropriate, or a transition feels
graceful. Pair every report with full-speed listening on:

- studio or over-ear headphones;
- ordinary earbuds;
- laptop or phone speakers; and
- captions-on playback at normal volume.

Keep notes at the exact timestamp and identify the listener problem, not merely
the waveform symptom.

## Sources

- [W3C: Descriptions of visual information](https://www.w3.org/WAI/media/av/description/)
- [W3C: Easy checks for video accessibility](https://www.w3.org/WAI/test-evaluate/preliminary/)
- [W3C: Low or no background audio](https://www.w3.org/WAI/WCAG21/Understanding/low-or-no-background-audio)
- [W3C: Audio and video media guidance](https://www.w3.org/WAI/media/av/av-content/)
- [W3C: Captions and subtitles](https://www.w3.org/WAI/perspective-videos/captions/)
- [W3C: Three Flashes or Below Threshold](https://www.w3.org/WAI/WCAG22/Understanding/three-flashes-or-below-threshold)
- [W3C: WCAG 2.2 contrast criteria](https://www.w3.org/TR/WCAG22/#distinguishable)
- [Netflix: Subtitle Timing Guidelines](https://partnerhelp.netflixstudios.com/hc/en-us/articles/360051554394-Timed-Text-Style-Guide-Subtitle-Timing-Guidelines)
- [EBU loudness resources](https://tech.ebu.ch/groups/loudness)
- [EBU R128s4 internet-delivery guidance](https://tech.ebu.ch/files/live/sites/tech/files/shared/r/r128s4.pdf)
- [Kokoro-82M model card](https://huggingface.co/hexgrad/Kokoro-82M)
- [Qwen3-TTS reference implementation](https://github.com/QwenLM/Qwen3-TTS)
- [WhisperX paper and implementation](https://github.com/m-bain/whisperX)
- [Montreal Forced Aligner documentation](https://montreal-forced-aligner.readthedocs.io/)
- [Manim Voiceover documentation](https://voiceover.manim.community/en/stable/)
- [Apple reduced-motion evaluation criteria](https://developer.apple.com/help/app-store-connect/manage-app-accessibility/reduced-motion-evaluation-criteria)
