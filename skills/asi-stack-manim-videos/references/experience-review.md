# Audiovisual Experience Review

## Contents

- Use a script gate and three production gates
- Score without hiding weak dimensions
- Watch through multiple modes
- Review every beat
- Compare revisions fairly
- Record decisions

## Use a script gate and three production gates

### Gate 0: script

Review the teaching promise, selection budget, concrete case, macro moves,
spoken cadence, evidence fit, payoff, and cold transfer question before art
direction, TTS, or scene code. Listen to a read-aloud. Reject chapter synopsis,
internal status language, unsupported drama, decorative questions, and any
paragraph that cannot earn a meaningful picture. A script gate must be reopened
after a material narration edit.

### Gate 1: animatic

Use rough geometry, final or near-final narration, audio-derived timing, and no
expensive decorative polish. Mark estimates when the final aligner is not yet
qualified. Confirm the teaching promise, visual world, continuity, pacing arc,
hook, payoff, and evidence boundary. Rewrite freely at this gate.

### Gate 2: picture-and-sound lock

Use final object geometry, camera decisions, easing, narration, captions,
music policy, and transition timing. Review every beat at 1×. Do not proceed
because the render is technically valid.

### Gate 3: release candidate

Use the pinned release profile and final mux. Run technical validators,
accessibility review, full-device playback, and a predecessor comparison.

## Score without hiding weak dimensions

Score each dimension from 1 to 5 and attach timestamped notes:

| Dimension | Acceptance question |
|---|---|
| teaching clarity | Can the viewer explain or predict the promised mechanism? |
| composition | Does every frame have a legible focal hierarchy and breathing room? |
| motion quality | Does movement feel deliberate, smooth, semantically motivated, and comfortable? |
| synchronization | Do visual onset and resolution coincide with the idea being spoken? |
| continuity | Can the viewer track persistent objects and state across beats? |
| pacing | Do build, movement, pause, and reveal form a varied but coherent rhythm? |
| voice | Is delivery warm, intelligible, varied, and free of awkward edits? |
| sound mix | Is speech effortless to hear on every test device without harshness or distraction? |
| engagement | Does the opening create an honest question and the ending pay it off? |
| accessibility | Do captions, transcript, contrast, redundant encodings, and motion comfort pass? |
| claim fidelity | Does every example and visual qualifier stay within the chapter's evidence ceiling? |

Do not average away a failure. A release candidate needs at least 4 on every
dimension, with no unresolved critical timestamp. A score is an aid to
disciplined judgment, not a substitute for it.

The implementer and critic are logically separate roles even when one agent
performs them in sequence. The critic reviews the teaching promise, rendered
evidence, and playback experience without relying on implementation intent.
Execution errors and aesthetic or learning defects are separate queues.

## Watch through multiple modes

Review the entire release at 1× with audio. Then perform focused passes:

- **muted:** mechanism and state change remain legible;
- **audio only:** the narration remains coherent and pleasant;
- **captions on:** captions synchronize, remain readable, and do not obscure
  the active region;
- **phone-sized:** focal hierarchy and labels survive reduction;
- **large screen:** spacing, edges, gradients, and camera motion still look
  intentional;
- **headphones and speakers:** voice, music, silence, and edits remain
  comfortable; and
- **scrub test:** random frames look composed and reveal no accidental object
  states.

Also inspect the first 30 seconds, one randomly selected 30-second middle
segment, and the ending as standalone sequences. Each should have a clear
local purpose and visual rhythm.

## Review every beat

Generate start, quarter, midpoint, three-quarter, and end samples for each beat.
Add targeted samples around fast movement, camera reframing, or suspected
overlap. Examine:

- focal object and attention target;
- relationship between narration and visible state;
- incoming and outgoing object continuity;
- label density and safe areas;
- whether the frame has settled long enough to read;
- whether any object appears in an impossible intermediate state; and
- whether the final state earns the next beat.

Contact sheets reveal composition and continuity. They do not replace playback
review of easing, synchronization, sound, or motion comfort.

Run one comprehension check and one transfer check with a cold reviewer. The
comprehension prompt asks for the mechanism in the worked case. The transfer
prompt changes one condition and asks for a prediction. Record the answer and
the misconception, not a vague “clear” score. A wrong answer reopens the script
or visual model even when every technical gate passes.

## Compare revisions fairly

When revising an uploaded chapter, compare predecessor and candidate at matched
playback volume and display size. Ask which version better delivers the same
teaching promise. Keep improvements that solve a named problem; reject changes
whose only rationale is “more animated.”

If both versions fail in different ways, do not force a winner. Return to the
animatic and preserve the best local ideas from each.

## Record decisions

For each review note, record:

- timestamp or beat ID;
- observed viewer problem;
- likely cause;
- intended revision;
- result after revision; and
- disposition: resolved, accepted with rationale, or blocked.

Use the versioned experience-review record. It binds reviewer-role context,
five-or-more frame samples per beat, targeted interpolation samples, the cold
comprehension and transfer responses, all viewing passes, per-dimension scores,
and open defects. A release-candidate pass requires a cold reviewer to pass
both learning checks; a familiar author may diagnose a draft but cannot supply
that release evidence.

The authoring agent performs this review without creating an artificial
external-human gate. The owner may review the finished candidate and that
feedback becomes a new revision input.

Preserve only validated production lessons. Add a reusable pattern after it
solves the same named problem in at least two chapters. Add a pitfall after a
render or review demonstrates it. Record the trigger, observed failure,
repair, and scope; do not turn untested stylistic preferences into rules.
