# Research Basis

## Contents

- Primary guidance
- 3Blue1Brown code study
- Published Manim authoring skills
- Automated educational-video systems
- ManimCE techniques
- Learning, narration, and TTS
- Compatibility and licensing

## Primary guidance

- [3Blue1Brown: About / video-making advice](https://www.3blue1brown.com/about/)
  recommends concrete examples before abstractions, avoiding definitions as
  openings, asking what picture clarifies the topic, and making every movement
  deliberate. Most importantly, visual movement should communicate the same
  point as narration rather than compete with it.
- [3Blue1Brown videos repository](https://github.com/3b1b/videos) contains the
  scene code used for the channel's explanatory videos and describes Grant
  Sanderson's interactive checkpoint-based iteration workflow.
- [Manim Community Example Gallery](https://docs.manim.community/en/stable/examples.html)
  provides MIT-licensed code and rendered examples across transforms, graphing,
  camera work, and updater-driven animation.
- [ManimCE animation composition](https://docs.manim.community/en/stable/reference/manim.animation.composition.html)
  documents `AnimationGroup`, `LaggedStart`, `LaggedStartMap`, and `Succession`.
- [ManimCE updater utilities](https://docs.manim.community/en/stable/reference/manim.animation.updaters.mobject_update_utils.html)
  documents continuously changing objects with `always_redraw` and other
  updater helpers.
- [ManimCE moving-camera examples](https://docs.manim.community/en/stable/reference/manim.scene.moving_camera_scene.html)
  show saved frame state, purposeful pan/zoom, graph following, and restoration.
- [ManimCE scene sections](https://docs.manim.community/en/stable/tutorials/output_and_config.html#sections)
  make semantic units separately renderable for iteration and review.
- [ManimCE rate functions](https://docs.manim.community/en/stable/reference/manim.utils.rate_functions.html)
  documents easing families and custom rate functions. Select a curve for its
  physical or semantic meaning rather than using one default everywhere.
- [Manim Voiceover guide](https://docs.manim.community/en/stable/guides/add_voiceovers.html)
  shows deriving animation run time from exact audio duration.
- [Manim Voiceover tracker API](https://voiceover.manim.community/en/stable/api.html)
  exposes bookmark timing and remaining-duration controls for phrase-level sync.
- [Google Technical Writing: short sentences](https://developers.google.com/tech-writing/one/short-sentences)
  recommends one idea per sentence and removing extraneous words.
- [Google Technical Writing: active voice](https://developers.google.com/tech-writing/one/active-voice)
  explains why actor–verb–target sentences are usually clearer and shorter.
- [Brame, “Effective Educational Videos”](https://pmc.ncbi.nlm.nih.gov/articles/PMC5132380/)
  synthesizes video design around cognitive load, engagement, and active
  learning, including signaling, segmenting, weeding, matching modality,
  guiding questions, and interpolated questions.
- [Mayer, “Research-based principles for the design of instructional messages”](https://doi.org/10.1075/dd.1.1.02may)
  grounds multimedia, contiguity, coherence, and modality principles in a
  model where corresponding verbal and pictorial representations must coexist
  in working memory.
- [Fiorella and Mayer, “Principles for Reducing Extraneous Processing”](https://doi.org/10.1017/9781108894333.019)
  covers coherence, signaling, redundancy, spatial contiguity, and temporal
  contiguity.
- [Guo, Kim, and Rubin, “How Video Production Affects Student Engagement”](https://juhokim.com/files/LAS2014-Engagement.pdf)
  reports viewing behavior from 6.9 million MOOC sessions. Use it as
  observational engagement evidence, not as direct learning evidence.
- [Fyfield et al., “Harnessing active engagement in educational videos”](https://doi.org/10.1103/PhysRevPhysEducRes.18.010148)
  reports a controlled physics-video study in which enhanced visuals and
  embedded questions were most effective together.
- [Tversky, Morrison, and Betrancourt, “Animation: can it facilitate?”](https://doi.org/10.1207/S15326985EP3704_3)
  argues that animation must satisfy congruence and apprehension: motion should
  match the represented structure and remain perceptually understandable.
- [YouTube: measure key moments for audience retention](https://support.google.com/youtube/answer/9314415)
  defines intro retention, top moments, spikes, and dips and explicitly notes
  that spikes can reflect either interest or confusion.
- [YouTube: understand content performance](https://support.google.com/youtube/answer/16559650)
  recommends a concise hook that delivers the title/thumbnail promise,
  thoughtful storytelling, anticipation, curiosity, and retention analysis.
- [CUNY SPS instructional-video script guide](https://openlab.sps.cuny.edu/media-team-vault/script-writing-guide-for-instructional-video/)
  recommends one large idea, deliberate scripting, rehearsal, and preserving
  a natural rather than flat delivery.
- [Microsoft Fluent 2 motion](https://fluent2.microsoft.design/motion)
  distinguishes easing, choreography, and hierarchy: ordered offsets guide
  attention and higher-priority elements receive stronger emphasis.
- [Apple reduced-motion evaluation criteria](https://developer.apple.com/help/app-store-connect/manage-app-accessibility/reduced-motion-evaluation-criteria)
  identifies parallax, spinning, multi-axis, vortex-like, and continual motion
  as discomfort risks and recommends preserving meaning with alternatives such
  as dissolves and highlights.
- [W3C audio/video accessibility guidance](https://www.w3.org/WAI/media/av/av-content/)
  covers captions, descriptive transcripts, audio description, player access,
  audio quality, and avoiding distracting background sound.
- [W3C descriptions guidance](https://www.w3.org/WAI/media/av/description/)
  explains how integrated description planned into a new video can convey
  essential visual information without a separate description track.
- [W3C low-or-no-background-audio guidance](https://www.w3.org/WAI/WCAG21/Understanding/low-or-no-background-audio)
  supplies a demanding 20 dB foreground/background difference as an enhanced
  speech-intelligibility criterion.
- [EBU loudness resources](https://tech.ebu.ch/groups/loudness) provide
  measurement concepts for integrated loudness, loudness range, and true peak.
  Use these measurements while pinning a project-appropriate online-delivery
  target; do not transplant the -23 LUFS broadcast target into YouTube by
  default.

## 3Blue1Brown code study

Study the recent transformer attention scene at
[`_2024/transformers/attention.py`](https://github.com/3b1b/videos/blob/master/_2024/transformers/attention.py).
Useful transferable patterns include:

- staggered word and relationship reveals rather than simultaneous dumping;
- arrows appearing when the relationship is introduced;
- earlier objects transforming into embeddings and derived query/key objects;
- `TransformFromCopy` and fade transforms to show derivation;
- focus isolation by fading context and restoring it later;
- camera motion coupled to the object under discussion;
- live matrix/vector manipulation instead of static formula cards; and
- visual questions and answers embodied as objects before abstraction.

The important pattern is a chain of small, semantically aligned state changes.
The lesson is not to maximize movement or copy a particular effect.

Also inspect domain-object patterns in recent public scenes such as
[`_2026/cross_entropy/distribution.py`](https://github.com/3b1b/videos/blob/master/_2026/cross_entropy/distribution.py)
and linked-representation patterns such as
[`_2025/zeta/play.py`](https://github.com/3b1b/videos/blob/master/_2025/zeta/play.py).
The transferable architecture is a persistent semantic object with operations
that change its state, plus trackers or updaters that keep dependent views
consistent. Exact code remains upstream-licensed pattern study.

Grant's public workflow also treats Manim as a clip renderer within a broader
editing process when that is the cleaner production choice. Do not force all
audio editing, titles, and assembly into scene code.

## Published Manim authoring skills

Public skill repositories are implementation examples, not research evidence:

- [Browser Use `video-use` Manim skill](https://github.com/browser-use/video-use/tree/main/skills/manim-video)
  usefully emphasizes an “aha” before code, low-quality iteration, and rendered
  frame inspection. Do not inherit its rigid pauses, palette prescriptions, or
  scene-by-scene novelty targets.
- [Yusuke710 `manim-skill`](https://github.com/Yusuke710/manim-skill)
  reinforces planning, exact synchronization points, independent scene renders,
  and low-resolution iteration. Its generic section/subtitle structure is not
  an ASI Stack story standard.
- [iart-ai `manim-skills`](https://github.com/iart-ai/manim-skills)
  is useful for deterministic render/inspect loops, API references, and common
  implementation failures; it does not replace pedagogical review.
- [makefinks `manim-generator`](https://github.com/makefinks/manim-generator)
  separates generation from review and supplies render evidence to a critic.
  Keep execution repair separate from learning and aesthetic critique.

Borrow tested process ideas, not surface templates. None of these sources
justifies a claim that generated videos are educationally effective.

## Automated educational-video systems

- [Code2Video](https://github.com/showlab/Code2Video) separates planner, coder,
  and visual critic roles and evaluates executable generation, aesthetics,
  efficiency, and knowledge transfer. Its lecture-text layout is not the ASI
  Stack visual model; retain the role separation and transfer evaluation.
- [TheoremExplainAgent](https://aclanthology.org/2025.acl-long.332/) reports
  that agentic planning helps long-form theorem videos and that multimodal
  explanation can expose reasoning defects hidden in text, while layout issues
  remain common.
- [OmniManim / “See Before You Code”](https://arxiv.org/abs/2605.15585) motivates
  shared scene state, sparse keyframe planning, interpolation-aware review,
  post-render diagnostics, and localized repair. It is recent research; treat
  reported benchmark gains as source claims until independently reproduced.
- [ManimAgent](https://arxiv.org/abs/2606.30296) proposes separate memories of
  successful patterns and validated pitfalls across tasks. Its code release and
  broader replication status must be rechecked before adoption. The local
  analogue stores only lessons demonstrated in completed ASI Stack reviews.

## ManimCE techniques

Use the official ManimCE 0.20.1 APIs because the repository pins that runtime.
Especially useful families are:

- matching-part transforms for algebra and identity;
- staggered animation composition for sequence and hierarchy;
- updaters and trackers for continuous relationships;
- `Graph` and animated edges for routing and dependencies;
- `MoveAlongPath` and traced paths for flow;
- moving and zoomed cameras for locality and scale; and
- scene sections for rapid, bounded iteration.

## Learning, narration, and TTS

Grant Sanderson's guidance supplies the pedagogical frame: concrete before
abstract, do not open with definitions, and make pictures and words reinforce
each other. Google's technical-writing guidance supplies sentence-level tools:
one idea per sentence, active voice, strong verbs, consistent terms, and
deletion of unnecessary words.

These are heuristics, not automatic quality guarantees. Full-speed listening
and viewing remain required.

The currently pinned Kokoro voice remains a qualified production choice, not a
permanent winner. Relevant candidate sources include the
[Kokoro-82M model card](https://huggingface.co/hexgrad/Kokoro-82M),
[Qwen3-TTS](https://github.com/QwenLM/Qwen3-TTS), and other systems whose exact
license, runtime, long-form continuity, pronunciation, alignment, and voice
rights can be tested. Compare candidates on the same excerpt at matched
loudness; do not select from demos or model size.

[WhisperX](https://github.com/m-bain/whisperX) combines speech recognition,
VAD, and forced phoneme alignment for word timestamps. Manim Voiceover offers
duration trackers and bookmarks. Either can support phrase-level sync, but the
chosen path must be version-pinned and manually checked around difficult terms.

## Compatibility and licensing

Manim Community Edition and 3b1b's ManimGL are related but incompatible
projects. Do not assume class or method parity.

ManimCE and its official example-gallery snippets are MIT-licensed. The
3b1b/videos repository is CC BY-NC-SA 4.0. Study its explanatory patterns, but
do not copy its scene implementation into the ASI Stack's differently licensed
publication pipeline without an explicit rights and compatibility review.
