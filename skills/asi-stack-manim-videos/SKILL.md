---
name: asi-stack-manim-videos
description: Art-direct, write, animate, mix, revise, audit, render, and maintain beautiful ManimCE visual abstracts for chapters of Corben Sorenson's living book The ASI Stack. Use for chapter-video narration, beat sheets, storyboards, composition, motion design, Manim scene code, audio/visual synchronization, sound and accessibility review, captions, YouTube replacement planning, or diagnosing videos that are wordy, static, generic, visually monotonous, uncomfortable, or out of sync.
---

# ASI Stack Manim Videos

Build each video as a visual explanation, not a narrated slide deck. Make the
animation and narration teach the same idea at the same moment. Preserve the
book as canonical and preserve every claim/evidence boundary.

## Read the right context

1. Read the complete canonical chapter, its packet, source notes, core claim,
   evidence ceiling, non-claims, and handoff.
2. Read `visual_edition/README.md`, `visual_edition/visual_grammar.json`, the
   YouTube ledger, and the chapter's current visual packet when working in the
   ASI Stack repository.
3. Read [writing-and-story.md](references/writing-and-story.md) before drafting
   narration.
4. Read [learning-and-engagement.md](references/learning-and-engagement.md)
   before choosing the hook, questions, pacing, or entertainment devices.
5. Read [art-direction-and-motion.md](references/art-direction-and-motion.md)
   before storyboarding, selecting a visual world, or judging beauty.
6. Read [manim-patterns.md](references/manim-patterns.md) before designing or
   coding visuals.
7. Read [audio-and-accessibility.md](references/audio-and-accessibility.md)
   before synthesizing, mixing, captioning, or reviewing final narration.
8. Read [experience-review.md](references/experience-review.md) before accepting
   an animatic, picture-and-sound lock, or release candidate.
9. Read [asi-stack-pipeline.md](references/asi-stack-pipeline.md) before
   modifying an existing chapter video or any publication state.
10. Read [research-basis.md](references/research-basis.md) when checking the
   rationale, upstream examples, compatibility, or licensing boundary.

## Choose one teaching promise

State one sentence the viewer should understand or be able to predict after
watching. Choose one concrete case that makes the promise visible. A chapter
video is a selective visual abstract, not a compressed reading of every
section.

Build around this order unless the chapter demands a better one:

1. Pose a concrete puzzle, failure, or decision.
2. Let the viewer make a prediction.
3. Manipulate the concrete case.
4. Extract the general mechanism from what changed.
5. Run one worked trace or counterexample.
6. Show the evidence boundary and the next question.

Do not begin with a definition, chapter summary, taxonomy, or phrases such as
“This chapter asks a specific question,” “the tempting shortcut,” or “the
chapter's core claim is.” Avoid repeating a seven-part verbal template across
chapters.

## Make attention serve understanding

Treat entertainment as sustained, useful attention—not decoration. Build a
small curiosity loop: expose a concrete mismatch, let the viewer predict an
outcome, reveal the mechanism progressively, and pay off the opening question.
Use surprise only when the surprising result teaches the chapter's mechanism
or defeats a plausible shortcut.

- Make the first 15 seconds deliver the title-and-thumbnail promise through a
  visible problem or consequence.
- Create micro-suspense with an unresolved route, hidden state, competing
  prediction, or impending failure. Resolve it within the same visual world.
- Give important objects agency: tokens move, gates decide, ledgers change,
  backups restore, and branches visibly win or fail.
- Use one or two genuine prediction prompts in a short video. Pause long
  enough to think, then make the answer visible before explaining it.
- Vary the explanatory form across chapters—trace, puzzle, counterexample,
  comparison, construction, diagnosis—while preserving the visual grammar.
- Use an energetic, conversational delivery with real changes in emphasis.
  Do not manufacture excitement with hype, exaggerated certainty, or speed.
- Cut jokes, music, backgrounds, visual flourishes, and side facts that do not
  strengthen curiosity, orientation, mechanism, consequence, or recall.

Apply coherence, signaling, segmenting, spatial contiguity, temporal
contiguity, modality, and redundancy principles. Put a short label beside the
object it names exactly when it matters. Pair spoken explanation with a
complementary picture; do not make viewers read the same sentence they hear.

## Write for speech and pictures

- Target 3–6 minutes and usually 350–700 spoken words. Prefer a shorter video
  that lands one idea over a dense synopsis.
- Target roughly 110–145 spoken words per minute after synthesis. Do not speed
  up an overlong script to make it fit.
- Use active voice, concrete nouns, specific verbs, and one idea per sentence.
- Put the actor and action early. Split sentences above roughly 24 words unless
  their rhythm is demonstrably clear when spoken.
- Introduce jargon only after a viewer has seen the problem it names. Define a
  term once and use it consistently.
- Write conversational transitions that express causality: “because,” “so,”
  “but,” and “therefore.” Remove paper-like signposting and throat-clearing.
- Ask questions only when the visual gives the viewer time and evidence to
  answer.
- Never narrate visible text verbatim. On-screen text labels; narration
  explains relationships, causes, and consequences.
- Preserve qualifiers. A visual example, implementation sketch, or source
  report must not become proof, generality, safety, or deployment evidence.

Read the draft aloud before synthesis. Rewrite any line that needs punctuation
to be understood, contains multiple logical branches, or cannot be paired with
a meaningful picture.

## Art-direct before animating

Write a compact art-direction brief before scene code. Define the visual
thesis, signature image, persistent visual world, core objects, composition
rule, palette roles, typography roles, motion character, camera rule, surface
rule, and ending image. Store it in `beat_plan.json`.

Make the shared ASI Stack grammar recognizable without making every chapter
look the same. Give each chapter one visual idea that belongs to its mechanism,
not a generic stack of cards wearing a new title. Use the repository palette
semantically and preserve consistent type, stroke, radius, arrow, spacing, and
depth conventions.

Compose for immediate hierarchy. Maintain one dominant focal point, leave
negative space for the next relation, place labels beside their objects, and
reserve maximum contrast for the current teaching target. Inspect the work at
phone size as well as full resolution.

Create beauty through coherent composition, object continuity, meaningful
easing, varied rhythm, and a clean visual payoff. Do not pursue beauty through
effect count, constant motion, gradients, glow, particles, camera drift, or
imitation of another creator's surface style.

## Design a beat-synchronized visual argument

Create `beat_plan.json` before final scene code. Use the format in
[asi-stack-pipeline.md](references/asi-stack-pipeline.md), then run:

```bash
python3 ~/.codex/skills/asi-stack-manim-videos/scripts/audit_video_plan.py \
  path/to/beat_plan.json --narration path/to/narration.txt
```

A semantic beat is one spoken idea plus the visual change that explains it.
Most explanations naturally fall near 8–14 meaningful beats per minute, but
this is a diagnostic range, not a motion quota. Most beats should last 3–8
seconds. Split a beat longer than 12 seconds unless the viewer is tracing,
comparing, predicting, or absorbing a deliberate result; record that purpose.

For every beat, specify:

- the exact narration and a unique spoken sync anchor;
- the viewer's attention target and the relation being encoded;
- the relationship being taught;
- the object state before and after the beat;
- the purposeful visual action;
- the intended composition, easing, camera behavior, and settling time;
- the persistent objects that must remain trackable;
- the exact audio-derived start and end time;
- the few words, if any, shown on screen; and
- its claim role and evidence boundary.

Do not use movement merely to satisfy a density target. Each motion must encode
at least one of: identity, relation, causality, sequence, quantity, uncertainty,
contrast, containment, authority, rollback, or attention. Conversely, do not
leave the screen static while narration introduces a new relationship.

Technique-count and retention metrics are diagnostics, not targets. A scene
using three techniques coherently is better than a scene using six to satisfy
a checklist. Add a new technique only when it makes a distinct relationship or
state change easier to understand.

## Prefer continuity over card replacement

Choose one persistent visual world—a stack, graph, state machine, constrained
flow, geometric field, timeline, or worked artifact. Grow and transform it as
understanding changes. Reuse object identity across beats so the viewer can see
what persisted and what changed.

Prefer:

- `Transform`, `ReplacementTransform`, `TransformFromCopy`, and matching-part
  transforms for identity and derivation;
- `LaggedStart`, `LaggedStartMap`, `AnimationGroup`, and `Succession` for
  legible sequence and hierarchy;
- `ValueTracker`, mobject updaters, `always_redraw`, and moving dots or traces
  for changing quantities and live relationships;
- graph vertex movement, animated edges, path traversal, counters, gates, and
  state changes for mechanisms;
- focus isolation—dim context, emphasize the active objects, then restore;
- restrained camera movement when a zoom or pan reveals scale, locality, or
  hierarchy; and
- concrete counterexamples that visibly break the proposed shortcut.

Avoid:

- card grids that appear once and remain static under a long paragraph;
- clearing the entire scene after every paragraph when object continuity would
  teach more;
- decorative floating, spinning, pulsing, or camera motion;
- long lists, prose blocks, duplicated captions, and reading equations aloud;
- an animation that finishes before the narration introduces its meaning; and
- a fixed seven-scene template used regardless of chapter structure.

Use 3Blue1Brown code as pattern study, not as a copy source. That repository
uses ManimGL and CC BY-NC-SA code; the ASI Stack pipeline uses ManimCE 0.20.1.
Translate the explanatory technique with ManimCE's documented API and original
project code.

## Derive timing from final audio

Synthesize or record the narration before final timing. Obtain word or phrase
timestamps through the repository's pinned alignment path. Align each beat to
its unique spoken anchor.

Use one of two timing strategies:

1. For the existing external-audio pipeline, store exact beat timestamps and
   drive `self.play` calls to those anchors. Do not animate only at paragraph
   entry and call `wait_until` once at paragraph end.
2. If Manim Voiceover is intentionally adopted, use voiceover blocks and
   bookmarks so animation durations derive from the audio tracker.

Keep animation onset within roughly half a second of the phrase it explains.
Finish the explanatory change near the end of that idea, not at the start of a
much longer paragraph. Regenerate timing after any narration edit.

## Implement and iterate in sections

Use `Scene.next_section()` at semantic beats or coherent beat groups. Render
low-resolution sections during iteration, then render the complete pinned
release profile. Keep random seeds deterministic.

Work in three passes:

1. **Animatic:** use rough objects with final or near-final narration to solve
   story, visual thesis, continuity, timing, and payoff.
2. **Picture-and-sound lock:** finalize geometry, easing, camera, typography,
   narration, captions, music policy, and sound timing.
3. **Release candidate:** render the pinned profile, run technical checks, and
   perform the complete experience review.

Do not polish a transition while the story or visual world is still unstable.
Use scene sections and low-resolution renders as the ManimCE equivalent of an
interactive checkpoint workflow.

Build original reusable primitives in `visual_edition/lib/` only when at least
two chapters genuinely share the visual behavior. Keep chapter-specific
metaphors and transformations in chapter code. A short wrapper over a generic
scene is insufficient unless the generic engine consumes a complete beat plan
and produces chapter-specific transformations.

## Choreograph motion and sound

Use motion to guide the eye. Group simultaneous changes that express one
relation; stagger changes when order matters; give the central transformation
more duration, distance, or contrast than supporting motion; and let the frame
briefly settle after a dense reveal. Avoid unrelated simultaneous movement.

Choose easing by meaning. Use linear motion only for uniform time, rate, scan,
or flow; ease-out for arrival; ease-in for departure; and ease-in-out for state
transformation or deliberate reframing. Use bounce, shake, flash, spin,
overshoot, or continuous camera motion only when that physical quality teaches
the idea. Encode essential meaning redundantly so it survives pause and
reduced-motion viewing.

Treat narration as the primary audio signal. Direct emphasis, pause, pace, and
pronunciation; remove awkward synthesized splices; and audition the complete
voice without video. Use only original or rights-cleared music and effects.
Keep them well below speech, duck them under dense ideas, and remove them when
silence improves concentration. Measure loudness and true peak, but never
mistake a compliant meter for a pleasant mix.

## Review the experience, not just artifact validity

Do all of these before calling a revision ready:

1. Run the beat-plan audit and repository validators.
2. Render an animatic with final or near-final narration and exact beat timing.
3. Sample the start, midpoint, and end of every beat, not only seven paragraph
   midpoints. Inspect focal hierarchy, continuity, intermediate states, and
   visual breathing room.
4. Watch the picture-and-sound lock once at 1× with audio. Mark any idea where
   the picture leads or lags
   the words, the viewer must read and listen simultaneously, or the visual
   stops teaching.
5. Watch once muted. Confirm that the mechanism, state change, and failure are
   still legible.
6. Listen once without video. Remove dense clauses, template language, and
   unexplained terms.
7. Check captions, pronunciation, contrast, safe areas, text size, redundant
   encodings, motion comfort, and the descriptive transcript.
8. Audition voice and mix on headphones, earbuds, laptop or phone speakers,
   and captions-on playback. Check loudness consistency, true peak, silence,
   music ducking, and every regenerated audio splice.
9. Inspect the result at phone size and large-screen size. Scrub random frames
   for accidental states and poorly composed transitions.
10. Score every dimension in [experience-review.md](references/experience-review.md).
    Require at least 4/5 for teaching clarity, composition, motion quality,
    synchronization, continuity, pacing, voice, mix, engagement,
    accessibility, and claim fidelity. Do not average away a weak dimension.
11. Compare the result with the teaching promise. Cut beats that do not serve it.
12. Review the hook, prediction, reveal, and payoff as one loop. Reject a hook
   that is never resolved or a late payoff that should appear earlier.
13. For a revision, compare predecessor and candidate at matched playback
    volume and display size. Keep changes that solve a named problem.
14. After publication has enough viewers, inspect first-30-second retention,
    dips, spikes, and top moments. Treat these as diagnostic signals—not proof
    of learning—and record the revision hypothesis before changing the video.

Reject the video when any substantive spoken beat lacks an aligned visual;
when a long hold lacks recorded pedagogical purpose; when on-screen prose
competes with speech; when the composition has no clear focal hierarchy; when
motion, flashes, camera movement, or audio are uncomfortable; when the voice
or mix fails on an ordinary playback device; or when the scene is chiefly a
sequence of labeled cards. Technical validity is never aesthetic acceptance.

## Maintain the living edition

Treat visual quality revisions as material media revisions. Keep the stable
chapter video identity, create a new local generation, preserve the previous
YouTube generation, and follow the repository's supersession plan and
action-time authorization rules. Never overwrite receipts or imply that a new
video changes the chapter's support state.

When improving an existing uploaded preview, revise and validate the local
generation first. Upload only after exact platform authority exists. Reconcile
the new video ID, captions, thumbnail, playlist position, predecessor state,
packet, ledger, and Quarto embed as one governed transaction.
