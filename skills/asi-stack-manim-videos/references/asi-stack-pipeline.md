# ASI Stack Video Pipeline

## Contents

- Current repository diagnosis
- Beat-plan contract
- Authoring sequence
- Validation and review
- Existing-video revision
- YouTube supersession

## Current repository diagnosis

The 2026-08-08 baseline audit found 85 canonical chapters, 84 preserved
generation-one packets, and 24 generation-two narration drafts. The newly added
chapter has no legacy packet by design. Seventy-nine generation-one narrations
use the same seven-paragraph chapter-summary template; generation one remains
historical rather than an authoring source.

The same-day editorial pass replaced all 24 generation-two narrations with
case-first scripts under the revised standard. They now run from 364 to 436
words and pass the narration-only audit without warnings. Their earlier beat
plans, audio, captions, transcripts, scenes, renders, and reviews remain useful
history, but no longer describe the current scripts and must be regenerated
through the gates. The remaining 61 chapters enter generation two in canonical
order as one-promise visual abstracts, including the chapter with no legacy
predecessor.

The main defect is selection, not speech speed: scripts summarize chapters,
beats follow document sections, and visuals inherit card-like tableaux. The
legacy packet generator is a historical reproducibility tool. Do not use it to
author generation two or to fill a new chapter merely for count symmetry. Its
packet, timing, bulk-render, mux, and production commands require the explicit
`--historical-generation-one` acknowledgement.

Do not treat `ready_not_published`, a successful render, or an earlier review
as approval under the revised standard. Existing receipts preserve exact
historical identity. Any script or standard change reopens downstream timing,
captions, audio, scene, and experience gates without erasing those receipts.

## Beat-plan contract

Create a per-chapter `beat_plan.json` with this shape:

```json
{
  "schema_version": "asi_stack.manim_beat_plan.v2",
  "chapter_id": "example-chapter",
  "teaching_promise": "The viewer can predict when a route must abstain.",
  "target_duration_seconds": 240.0,
  "chapter_sha256": "<64 lowercase hex characters>",
  "source_commit": "<Git commit>",
  "story": {
    "concrete_case": "Two routes agree, but only one has authority.",
    "opening_question": "Which answer may act?",
    "payoff": "Agreement cannot grant authority.",
    "transfer": "Apply the same test to tools, memory, and model updates."
  },
  "art_direction": {
    "visual_thesis": "An answer travels farther than its authority token.",
    "signature_image": "Two equal answers at one gate, only one holding a key.",
    "visual_world": "A persistent request flowing through two routes and one gate.",
    "persistent_objects": ["request token", "route A", "route B", "authority key", "gate"],
    "composition_rule": "Flow left to right; gate is the fixed decision axis.",
    "palette_rule": "Accent marks active flow; warning marks blocked authority; uncertainty uses pattern plus label.",
    "typography_rule": "Object labels only; qualifiers remain adjacent to the gate.",
    "motion_character": "Precise routing with a firm stop at the boundary.",
    "camera_rule": "Reframe only to compare both routes or isolate the gate.",
    "surface_rule": "Flat field, restrained glow only at the active gate.",
    "ending_image": "Both answers remain equal while only the keyed path crosses."
  },
  "audio_direction": {
    "narration_style": "Warm, deliberate, with a pause before the gate test.",
    "pacing_arc": "Fast setup, slower prediction, crisp reveal, quiet evidence boundary.",
    "music_policy": "Rights-cleared bed only in setup and payoff; duck under the mechanism.",
    "sound_effect_policy": "One quiet semantic gate sound; no per-motion effects.",
    "review_devices": ["headphones", "earbuds", "laptop speakers", "phone speakers"]
  },
  "accessibility": {
    "color_redundancy": "Route state uses key shape, label, and color.",
    "motion_redundancy": "Crossing and blocking end in distinct stable positions.",
    "integrated_description": "Narration names the key and visible stop.",
    "caption_plan": "Exact narration plus the meaningful gate sound.",
    "reduced_motion_assessment": "No parallax, flash, spin, shake, or continuous zoom."
  },
  "beats": [
    {
      "id": "b01",
      "story_function": "hook",
      "start_seconds": 0.0,
      "end_seconds": 5.2,
      "narration": "Two routes return the same answer, but only one may act.",
      "sync_anchor": "only one may act",
      "visual_purpose": "Contrast output equality with authority inequality.",
      "visual_action": "split_path_and_block_unauthorized_token",
      "attention_target": "the blocked token at the gate",
      "semantic_encodings": ["relation", "authority", "contrast"],
      "object_before": "one request and two untested routes",
      "object_after": "two equal answers with one path stopped at an authority gate",
      "continuity_objects": ["request token", "gate"],
      "composition": "Equal routes share a baseline; the gate divides the right third.",
      "motion_curve": "ease-out split, linear travel, ease-in stop",
      "camera_action": "static; the full comparison is already legible",
      "animation_techniques": ["TransformFromCopy", "MoveAlongPath"],
      "on_screen_text": ["same answer", "different authority"],
      "settle_seconds": 0.4,
      "hold_purpose": "Let the unequal endpoints register before narration continues.",
      "new_concepts": ["authority differs from agreement"],
      "claim_role": "concrete_example",
      "evidence_boundary": "illustrative mechanism, not deployment evidence"
    }
  ]
}
```

Each beat uses one story function from `hook`, `setup`, `prediction`,
`construction`, `mechanism`, `worked_trace`, `comparison`, `counterexample`,
`failure`, `consequence`, `evidence_boundary`, `payoff`, or `handoff`. Every
video needs a hook, mechanism, evidence boundary, and payoff. Other functions
depend on the chapter. The first beat must hook and the payoff must follow the
mechanism, but do not force every chapter into the same seven-part sequence.

Use exact timestamps from final narration alignment, not word-count estimates.
The concatenated beat narration must equal `narration.txt` after whitespace and
punctuation normalization.

## Authoring sequence

1. Read the chapter and evidence surfaces.
2. Draft several teaching promises; select one outcome and one concrete case.
3. Write four to six macro narrative moves and one cold transfer question.
4. Draft narration, read it aloud, and pass the narration-only audit.
5. Write the art-direction, audio, and accessibility briefs.
6. Design sparse semantic keyframes and the persistent domain objects.
7. Build the timed beat plan and run the complete plan audit.
8. Synthesize narration in coherent blocks and force-align words or phrases.
9. Replace estimated beat times with audio-derived anchors.
10. Implement a low-resolution animatic with chapter-specific objects.
11. Review five samples per beat plus complete playback; repair story,
    composition, interpolation, continuity, synchronization, and rhythm.
12. Run the cold comprehension and transfer checks.
13. Lock geometry, easing, camera, narration, captions, and sound.
14. Run `audit_av_experience.py` for mechanical freeze, silence, and loudness
    diagnostics; investigate every finding in playback.
15. Render the pinned 1920×1080/30 release profile and mux exact audio.
16. Run `build_caption_review_sheet.py` against the mux and final VTT; reject
    overlaps, sub-320-millisecond cues, overlong cues, or captions that obscure
    the active visual region in the representative exact-frame sheet.
17. Run repository visual, caption, transcript, receipt, and publication
    validators.
18. Perform the complete experience review in `experience-review.md`.

## Validation and review

The structural audit is necessary, not sufficient. It enforces story-function
coverage, timing, narration bounds, art/audio/accessibility briefs,
visual-state declarations, short labels, persistent-object declarations, and
exact narration agreement. Technique and beat-density counts remain warnings,
not creative targets. The audit cannot judge whether the metaphor is
insightful, motion is beautiful, voice is pleasant, or explanation is true.

For contact sheets, sample at least five frames per beat. A start/middle/end
review can still miss a broken quarter-state, crossing label, or abrupt late
reveal.

Record review outcomes by beat:

- sync: visual onset and resolution match the spoken idea;
- comprehension: the visual reduces explanation cost;
- continuity: object identity remains legible;
- load: reading does not compete with listening;
- claim boundary: the picture is no broader than the chapter; and
- action: keep, revise, split, merge, or cut.

## Existing-video revision

Treat the first five uploaded videos as the initial revision cohort because the
owner has supplied direct viewing feedback. Do not merely add motion to the
generic card scenes. Rewrite each around a concrete case and beat plan. Preserve
useful custom work from video 1, but apply the same narration and sync audit.

After the cohort passes, revise the remaining uploaded previews before
uploading more chapters. Then author generation two in current canonical order.
New chapters enter automatically as planned targets with no fabricated
generation-one predecessor. Generate public derivatives only when content and
review gates justify the work; do not regenerate audio or publication bundles
for routine manuscript edits.

## YouTube supersession

YouTube cannot replace a video's binary in place. Follow the repository's
supersession workflow:

- keep stable internal chapter identity;
- create generation N+1 and an exact replacement plan;
- obtain action-time authority for that plan;
- upload the replacement with reviewed metadata, caption, and thumbnail;
- preserve the prior generation and normally make it unlisted;
- update playlist position, receipt, packet, ledger, and Quarto embed together;
- verify the live public or unlisted state; and
- never infer support-state movement from media quality.
