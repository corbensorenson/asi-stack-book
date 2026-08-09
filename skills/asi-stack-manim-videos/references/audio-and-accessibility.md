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

Narration need not describe every decorative detail. It must convey any visual
fact required to understand the teaching promise.

## Review motion comfort

Avoid rapid flashes and flag any sequence approaching three flashes per
second. Review parallax, spinning, multi-axis movement, vortex-like movement,
continuous zoom, shake, and large-field motion for discomfort.

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
- [EBU loudness resources](https://tech.ebu.ch/groups/loudness)
- [EBU R128s4 internet-delivery guidance](https://tech.ebu.ch/files/live/sites/tech/files/shared/r/r128s4.pdf)
- [Kokoro-82M model card](https://huggingface.co/hexgrad/Kokoro-82M)
- [Qwen3-TTS reference implementation](https://github.com/QwenLM/Qwen3-TTS)
- [WhisperX paper and implementation](https://github.com/m-bain/whisperX)
- [Montreal Forced Aligner documentation](https://montreal-forced-aligner.readthedocs.io/)
- [Manim Voiceover documentation](https://voiceover.manim.community/en/stable/)
- [Apple reduced-motion evaluation criteria](https://developer.apple.com/help/app-store-connect/manage-app-accessibility/reduced-motion-evaluation-criteria)
