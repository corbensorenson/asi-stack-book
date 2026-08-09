# ManimCE Explanatory Patterns

## Contents

- Pattern selection
- Domain objects and shared scene state
- Object continuity
- Timing composition
- Live relationships
- Renderer-in-the-loop repair
- Camera and focus
- Text and equations
- Toolchain and regression checks
- Anti-patterns

## Pattern selection

Select motion by meaning:

| Meaning | Useful ManimCE pattern |
|---|---|
| identity persists | `Transform`, `ReplacementTransform`, matching-part transform |
| one object derives from another | `TransformFromCopy`, `FadeTransformPieces` |
| ordered flow | moving token, `MoveAlongPath`, `Succession` |
| parallel or staggered work | `AnimationGroup`, `LaggedStart`, `LaggedStartMap` |
| changing quantity | `ValueTracker`, `DecimalNumber`, updater |
| changing dependency | `always_redraw`, mobject updater, animated graph edge |
| uncertainty or alternatives | branching paths, opacity/width encoding plus labels |
| boundary or authority | visible gate, enclosure, key, blocked path, state label |
| rollback | transform current state back to a retained prior-state object |
| comparison | synchronized before/after states with shared coordinates |
| scale or locality | restrained `MovingCameraScene` pan/zoom |

An animation should answer “what changed, and why does that change matter?”

## Domain objects and shared scene state

Model the mechanism in code before scripting individual effects. A
chapter-specific mobject should expose semantic operations such as
`set_authority`, `route_request`, `revoke_lease`, `restore_snapshot`,
`highlight_range`, or `renormalize_distribution`. Each operation owns the
geometry, labels, dependent arrows, and animation required to move between
valid states.

This is the most reusable lesson in recent 3Blue1Brown source: explanatory
objects carry state and offer mechanism-level transformations. Scenes then
compose those operations while preserving identity. Do not encode the lesson
as a succession of unrelated `FadeIn` calls or as strings passed to a generic
card factory.

Keep one explicit scene-state model for objects that persist across sections.
Record only meaningful state, not every pixel. This gives localized repair a
stable boundary: fix one operation without reconstructing the whole scene.

## Object continuity

Build a stable visual vocabulary early. Reuse the same object for the same
entity. Transform it when its state changes. Copy from it when information or
authority derives from it. Do not replace it with a new card merely because the
narration entered a new paragraph.

Progressive construction reduces reorientation cost:

1. introduce the concrete object;
2. reveal one relation;
3. transform the affected state;
4. dim irrelevant context;
5. test the relation under a changed input; and
6. restore the complete system for the conclusion.

Recent 3Blue1Brown transformer scene code illustrates this style: words gain
rectangles, arrows, embeddings, and derived query/key structures while earlier
objects persist. The code repeatedly uses staggered reveals, transforms from
existing objects, focus isolation, and camera reframing. Study those patterns;
do not copy ManimGL or CC BY-NC-SA implementation code into this project.

## Timing composition

- Use `AnimationGroup` for simultaneous changes that express one relation.
- Use `LaggedStart` or `LaggedStartMap` when order within a group matters.
- Use `Succession` for explicit stages.
- Keep lag ratios large enough for the viewer to perceive order and small
  enough that the final objects coexist for comparison.
- Use linear rate functions for quantities intended to represent uniform time
  or flow. Use easing for attention and object manipulation.
- Use ease-out for arrival and settling, ease-in for departure or removal, and
  ease-in-out for state transformation or deliberate camera reframing.
- Reserve anticipation and overshoot for cases where that physical quality
  encodes the concept. Bounce, shake, and spin are not generic emphasis
  controls; named flash effects remain blocked by the accepted source gate.
- Give the primary transformation greater duration or contrast than secondary
  motions. Stagger supporting changes in the same direction as the logical or
  spatial flow.
- End the animation when the narrated idea resolves. Avoid completing it on
  the first word and holding the result under the rest of the explanation.
- Let a dense result settle briefly before the next construction begins. Vary
  durations by semantic weight instead of repeating one metronomic cadence.

Use `Scene.next_section()` to make semantic beats or coherent beat groups
independently renderable and reviewable. A section may contain an intentional
hold; do not add decorative motion merely to satisfy an animation count.

## Renderer-in-the-loop repair

Treat successful Python execution as the first check, not the final result.
Use a bounded loop:

1. render the changed section at low quality;
2. inspect renderer errors and repair API or geometry failures;
3. inspect five or more frames across every changed transition;
4. compare the frames with the planned attention target and object state;
5. play the section at speed with narration; and
6. localize the next repair to the responsible operation or beat.

Consult the pinned ManimCE documentation when an API is uncertain. Do not
guess from ManimGL examples. Code-level and rendered-visual checks are
complementary: either can fail while the other passes.

## Live relationships

Use `ValueTracker` with updaters when the viewer should see a parameter change
continuously. Use `always_redraw` for a dependent object such as a tangent,
boundary, arrow, or label whose geometry changes with another object. Prefer
mobject updaters over scene updaters under Cairo, as the ManimCE documentation
warns that scene-updater mutations may not be detected as moving mobjects.

Stop or remove updaters when the relationship no longer needs to animate.
Unbounded updaters complicate rendering and can create accidental motion.

## Camera and focus

Use camera motion only to reveal hierarchy, follow a causal trace, compare
scales, or focus on a dense local mechanism. Save and restore the frame state.
Avoid continuous drift.

To control attention without moving the camera:

- fade unrelated objects;
- use a restrained `Indicate`, `Circumscribe`, edge-weight, or opacity change;
- raise the active object in z-order;
- animate edge width or opacity together with a label; and
- restore the context after the local explanation.

Never encode meaning with color or motion alone.

## Text and equations

Use text for names, states, small quantities, and boundaries. Keep labels short.
Do not put narration paragraphs on screen.

The current pinned toolchain has no qualified LaTeX or `dvisvgm`; source
preflight therefore rejects `Tex`, `MathTex`, `SingleStringMathTex`, and
`TexTemplate`. Use Pango Unicode text or a provenance-bound, prevalidated SVG
until both dependencies and their graphical regressions are admitted. Only
after that qualification may `TransformMatchingTex` carry symbol identity.
Split admitted TeX into stable semantic pieces and use a key map only when the
intended correspondence differs. For prose transformations, use matching
shapes sparingly; viewers should understand the conceptual mapping, not admire
a typographic effect.

Every equation, symbol, and unit must appear in the treatment notation ledger.
Check algebraic or formal steps against the cited chapter statement, Lean
artifact, executable model, or recorded manual derivation before animating
them. Visual continuity is not mathematical validity.

## Toolchain and regression checks

Preflight the exact ManimCE runtime, renderer, fonts, LaTeX engine and packages,
FFmpeg/codecs, external assets, random seeds, resolution, and frame rate before
expensive rendering. Fail explicitly when a required font or TeX dependency is
missing; silent fallback can invalidate layout review.

Run the repository-owned live probe before a render:

```bash
python3 scripts/validate_manim_toolchain.py --probe-runtime
python3 skills/asi-stack-manim-videos/scripts/audit_scene_source.py \
  path/to/scene.py --treatment path/to/treatment.json
python3 skills/asi-stack-manim-videos/scripts/render_scene_isolated.py --self-test
```

Manim scene files execute arbitrary Python. Inspect downloaded or generated
code before execution; do not expose credentials or unrelated writable paths;
reject unexpected network, subprocess, dynamic-import, or filesystem behavior;
and bind every adopted dependency or asset by source, license, and digest. A
popular public skill or scene repository is not a trust boundary.

The static source audit rejects imports outside the narrow numerical and
ManimCE allowlist and permits exactly one local helper,
`visual_edition.lib.asi_visuals`, whose digest and graphical contract are bound
separately. It also rejects module-scope execution, dynamic imports;
filesystem, subprocess, and network effects; dynamic media paths; and unseeded
randomness. It cannot prove that an allowed dependency is harmless.

On macOS, `render_scene_isolated.py` constructs the release Manim and FFmpeg
commands, denies network access, strips the inherited environment, narrows
repository reads, restricts writes to `build/visual_edition`, limits resources,
and emits a schema-validated policy receipt. Run its live self-test outside an
already nested sandbox, then use it for every chapter render. Treat a new
container or CI backend as unqualified until a tracked adapter enforces and
records the same properties.

The current macOS adapter enforces wall, CPU, file-size, open-file,
process-count, and core-dump limits, but not a hard resident-memory ceiling;
its receipt records that residual. Do not convert an advisory memory setting or
successful smoke render into a hard memory-isolation claim.

Use ManimCE's graphical frame-comparison test support for shared primitives and
high-risk deterministic geometry. Bind a deliberate reference frame and review
every accepted update. Keep these tests narrow: they detect geometry, style,
and renderer regressions, not pacing, synchronization, accessibility, or
learning. Chapter scenes still need sample manifests and full-speed playback.

The repository's bounded equivalent is:

```bash
python3 skills/asi-stack-manim-videos/scripts/audit_primitive_regression.py
```

It renders two pinned Cairo reference frames, requires every public factory in
`visual_edition/lib/asi_visuals.py` to appear in the regression scenes, and
compares pixels using ManimCE's documented tolerance. Its regression scene must
pass the same static source preflight, and its hidden render worker refuses to
run unless the macOS filesystem/network sandbox is active; candidate capture
does not bypass those checks. To change the baseline,
capture a candidate and contact sheet, inspect both frames at original
resolution, repair unintended drift, and record the acceptance rationale. A
baseline update is a reviewed visual-contract change, not an automatic test
rewrite.

## Anti-patterns

- `FadeIn(card_grid); wait(35)` under a paragraph.
- Several objects moving for atmosphere with no semantic state change.
- Clearing the screen between every idea.
- Camera zoom used as emphasis when an object-level highlight is clearer.
- A moving token traversing a path before the narration names the transition.
- A result visible before the question or input.
- Tiny labels compensating for too many simultaneous objects.
- Copying 3b1b ManimGL calls directly into ManimCE code.
- Reaching correct keyframes through an overlapping, unreadable midpoint.
- A scene method named for an effect (`show_card_3`) rather than the mechanism
  (`revoke_lease`).
