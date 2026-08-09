# Art Direction and Motion Language

## Contents

- Define beauty operationally
- Write an art-direction brief
- Choose the right medium
- Compose every frame
- Choreograph attention
- Give motion a grammar
- Design keyframes and transitions
- Build rhythm and continuity
- Study 3Blue1Brown without imitation
- Reject visual failure modes

## Define beauty operationally

Treat beauty as the felt result of clarity, proportion, continuity, rhythm,
restraint, and one memorable visual idea. It is not an effect count. A beautiful
explanation makes the important relation easy to see, gives the eye somewhere
to rest, and makes each transformation feel inevitable.

Judge the work on five independent qualities:

1. **Legibility:** the focal object and current relation are apparent at a
   glance, including on a phone-sized frame.
2. **Coherence:** color, type, stroke, spacing, depth, and movement belong to
   one visual world.
3. **Continuity:** object identity survives transformations so the viewer does
   not repeatedly rebuild the scene in working memory.
4. **Rhythm:** construction, movement, emphasis, stillness, and reveal vary in
   a deliberate cadence.
5. **Delight:** at least one visual payoff expresses the chapter's idea so
   cleanly that it is worth remembering. Do not manufacture delight with
   unrelated spectacle.

## Write an art-direction brief

During treatment and before writing detailed scene code, define:

- **visual thesis:** one sentence describing what the viewer will see become
  true;
- **signature image:** the frame or transformation that could identify this
  chapter without its title;
- **visual world:** the persistent stack, field, graph, machine, timeline,
  geometric construction, or worked artifact;
- **persistent objects:** the few entities whose identity carries the lesson;
- **visual invariants:** facts that must remain visibly true while state changes;
- **composition rule:** the spatial logic used to express hierarchy and
  causality;
- **palette rule:** semantic roles for accent, success, warning, uncertainty,
  boundary, and inactive context within the repository palette;
- **type rule:** roles for title, object label, numeric state, annotation, and
  evidence qualifier;
- **motion character:** precise, elastic, flowing, mechanical, tentative, or
  another concept-derived quality;
- **camera rule:** when reframing is allowed and what relationship it reveals;
- **surface rule:** how depth, line weight, texture, shadows, and glow are used
  or withheld; and
- **ending image:** how the signature image changes to pay off the opening.
- **semantic keyframes:** four to eight sparse states tied to the macro moves;
  and
- **asset plan:** source, role, repository-local path, provenance, license,
  digest, security review, status, and visual integration for every external
  bitmap, clip, font, dataset, code fragment, or audio asset. A planned URL is
  not a cleared render input. For generated media, provenance includes model,
  prompt or edit instruction, generation date, inputs, and manual factual and
  rights review.

The shared ASI Stack grammar supplies family resemblance. The chapter brief
supplies identity. Do not solve chapter identity with a new arbitrary palette.

## Choose the right medium

Animation earns its cost only when change over time teaches the idea. Apply the
congruence principle: motion should map to the concept's real structure. Apply
the apprehension principle: the viewer must be able to notice, parse, and retain
the change at playback speed.

Use Manim for transformations, linked representations, spatial derivation,
state machines, geometric reasoning, causal traces, and changing quantities.
Use a still diagram, annotated bitmap, screen recording, or conventional edit
when that medium explains the idea more directly. Manim may render modular
clips. In the current accepted repository path, however, the tracked ManimCE
runner must own final visual composition; other final-assembly backends remain
blocked until a tracked adapter emits equivalent execution and custody receipts.

Use generated raster media only where illustration adds explanatory value that
code-native geometry cannot. Never ask a bitmap generator to supply equations,
small labels, measured geometry, evidence-bearing charts, or a factual system
state. Build those deterministically in Manim; treat generated imagery as an
illustrated asset, not a source.

## Compose every frame

- Establish one dominant focal point. If two objects compete, either group
  them as one comparison or sequence their emphasis.
- Use negative space as working memory. Leave room where the next relation will
  appear instead of repeatedly shrinking the entire system.
- Align related objects to a stable grid or shared axis. Break alignment only
  when the break communicates conflict, exception, or motion.
- Keep labels adjacent to what they name. Avoid long leader lines and legends
  that force visual search.
- Reserve the brightest accent and greatest contrast for the current teaching
  target. Dim context without erasing it.
- Maintain consistent stroke weight, corner radius, arrow style, label scale,
  and depth convention within a video.
- Prefer a purposeful asymmetry to centered-card repetition. Balance visual
  mass across the frame without making every composition symmetrical.
- Check title-safe and caption-safe regions and inspect the result at phone
  size. A technically 1080p label can still be functionally unreadable.

## Choreograph attention

Motion is an attention budget. Arrange onset, order, overlap, and settling so
the eye reaches an object just before its spoken meaning arrives.

- Group changes that express one relation.
- Stagger related changes when sequence matters; let the stagger travel in the
  same spatial direction as the causal or logical flow.
- Give the most important transformation more time, distance, or contrast than
  its supporting motions.
- Avoid unrelated simultaneous movement. Background motion must not compete
  with the current teaching target.
- Let the frame settle after a dense transformation. A brief post-motion settle
  may be shorter than the visual grammar's 1.2-second material-hold default.
  A teaching beat whose state remains unchanged is a material hold: give it at
  least the grammar default unless playback demonstrates a better duration,
  and record its prediction, comparison, reading, or absorption purpose.
- Reframe the camera after the relation warrants it, not merely to create
  energy. One motivated camera move is better than several object-level
  animations fighting a pan or zoom.

Microsoft's Fluent motion guidance describes choreography as the order and
arrangement of motion, with short offsets used to guide gaze and stronger
emphasis reserved for higher-priority elements. Use that as a general design
principle, not a request to mimic a product interface.

## Design keyframes and transitions

Plan sparse semantic keyframes before polishing motion. Each keyframe must make
the active relationship legible as a still: setup, decisive precondition,
transformation, result, and payoff. Then inspect the path between them. Correct
endpoints do not guarantee correct interpolation; objects can overlap, labels
can cross, and hierarchy can disappear halfway through a transform.

- Reserve space in the earlier keyframe for the next relation.
- Bind each keyframe to a treatment macro move and state its visible invariant
  and unresolved question, if any.
- State which object owns identity through the transition.
- Keep dependent labels and arrows attached throughout motion.
- Avoid transforms whose shortest geometric path communicates the wrong cause.
- Sample at start, quarter, midpoint, three-quarter, and end, then add frames
  around any rapid or crowded transition.
- Localize repairs to the responsible object or beat when shared scene state is
  otherwise correct.

## Give motion a grammar

Choose easing by meaning:

- use `linear` only for genuinely uniform time, rate, scanning, or flow;
- use ease-out for an object arriving and settling into attention;
- use ease-in for departure, loss, or an object leaving the active model;
- use ease-in-out for state transformation and deliberate camera reframing;
- use restrained anticipation or overshoot only when elasticity, inertia,
  uncertainty, or correction is itself meaningful; and
- avoid bounce, spin, flash, shake, or elastic effects as generic emphasis.

Preserve spatial causality. Derived objects should emerge from their source;
rollback should return toward a retained state; blocked flow should stop at a
visible boundary; uncertainty should branch or diffuse rather than simply
change color.

Do not encode essential meaning with motion alone. Pair it with stable
position, shape, label, or state so the explanation survives pause, captions,
and reduced-motion viewing.

## Build rhythm and continuity

Alternate among four kinds of time:

1. **build:** introduce an object or relation;
2. **transform:** make the mechanism act;
3. **hold:** let the result become legible;
4. **reveal:** expose a consequence, exception, or larger frame.

Avoid metronomic sequences in which every object fades in over the same
duration and every beat ends with the same pause. Vary timing according to
semantic weight. Preserve a recognizable object across cuts or transformations
whenever it carries causal identity.

Use an animatic pass to assess the whole rhythm before polishing details. A
beautiful local transition does not rescue a monotonous four-minute sequence.

## Study 3Blue1Brown without imitation

3Blue1Brown's public advice emphasizes concrete examples before abstraction,
visual thinking, and movement that communicates the same point as the
narration. Recent transformer scene code shows a persistent visual world:
words become embeddings, copied objects become queries and keys, context dims
and returns, and the camera follows the relation being explained.

Transfer these principles:

- make object identity do explanatory work;
- construct complexity in small, local transformations;
- preserve context while isolating attention;
- use checkpoints or scene sections for fast visual iteration; and
- design one chapter-specific visual payoff.

Recent public scenes also encapsulate mechanism-specific objects with semantic
methods that update a distribution, highlight a range, renormalize a state, or
link representations. Follow that architectural pattern: build a small visual
model of the chapter's mechanism, then animate its state. Do not build a generic
card renderer and feed it chapter nouns.

Do not copy composition, voice, jokes, music, or implementation. The public
3Blue1Brown scene repository uses ManimGL and CC BY-NC-SA code, while this
project uses ManimCE and its own publication rights.

## Reject visual failure modes

- generic dashboard or card-grid compositions used as a substitute for a
  mechanism;
- evenly spaced motion with no contrast in semantic weight;
- objects materializing far from their source when derivation matters;
- labels, arrows, and glow accumulating until no element dominates;
- decorative particles, gradients, depth, or camera drift that add atmosphere
  but no understanding;
- tiny text created by preserving too many objects at once;
- a signature frame that looks polished but cannot be explained in one
  sentence;
- correct keyframes joined by an unreadable or semantically false transition;
- visually attractive shorthand whose symbol, unit, or spatial inference is
  absent from the treatment's truth contract;
- motion whose conceptual mapping is weak enough that a still would teach more;
- chapter-specific labels attached to generic card choreography; and
- aesthetic polish that broadens a claim beyond the chapter's evidence.

## Sources

- [3Blue1Brown: About / video-making advice](https://www.3blue1brown.com/about/)
- [3Blue1Brown video source repository](https://github.com/3b1b/videos)
- [Tversky, Morrison, and Betrancourt: Animation: can it facilitate?](https://doi.org/10.1207/S15326985EP3704_3)
- [ManimCE rate functions](https://docs.manim.community/en/stable/reference/manim.utils.rate_functions.html)
- [ManimCE building blocks](https://docs.manim.community/en/stable/tutorials/building_blocks.html)
- [Microsoft Fluent 2 motion](https://fluent2.microsoft.design/motion)
- [Apple reduced-motion evaluation criteria](https://developer.apple.com/help/app-store-connect/manage-app-accessibility/reduced-motion-evaluation-criteria)
