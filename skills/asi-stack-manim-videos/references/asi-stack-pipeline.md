# ASI Stack Video Pipeline

## Contents

- Current repository diagnosis
- Beat-plan contract
- Authoring sequence
- Validation and review
- Existing-video revision
- YouTube supersession

## Current repository diagnosis

The 2026-07-31 audit found that the first uploaded chapter is hand-authored,
but videos 2–5 are 12-line wrappers around the shared `AsiChapterScene`. The
shared class creates seven paragraph-level tableaux, performs a few short
entrance animations, and waits until each narration paragraph ends. The scripts
run near 119–127 words per minute, so the main defect is not speech speed. It is
low semantic animation density, generic card layouts, and paragraph-level
rather than idea-level synchronization.

Do not treat the current `ready_not_published` status as an aesthetic quality
approval. Existing receipts establish technical identity and bounded review,
not that the video meets this stronger teaching standard.

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
2. Lock one teaching promise and one concrete case.
3. Write the art-direction, audio, and accessibility briefs.
4. Draft narration and beat plan together.
5. Run `audit_video_plan.py`; resolve every error and inspect warnings.
6. Synthesize narration and align words or phrases.
7. Replace estimated beat times with audio-derived anchors.
8. Implement a low-resolution animatic with chapter-specific objects.
9. Review every beat and repair story, composition, continuity, and rhythm.
10. Lock geometry, easing, camera, narration, captions, and sound.
11. Run `audit_av_experience.py` for mechanical freeze, silence, and loudness
    diagnostics; investigate every finding in playback.
12. Render the pinned 1920×1080/30 release profile and mux exact audio.
13. Run `build_caption_review_sheet.py` against the mux and final VTT; reject
    overlaps, sub-320-millisecond cues, overlong cues, or captions that obscure
    the active visual region in the representative exact-frame sheet.
14. Run repository visual, caption, transcript, receipt, and publication
    validators.
15. Perform the complete experience review in `experience-review.md`.

## Validation and review

The structural audit is necessary, not sufficient. It enforces story-function
coverage, timing, narration bounds, art/audio/accessibility briefs,
visual-state declarations, short labels, persistent-object declarations, and
exact narration agreement. Technique and beat-density counts remain warnings,
not creative targets. The audit cannot judge whether the metaphor is
insightful, motion is beautiful, voice is pleasant, or explanation is true.

For contact sheets, sample at least three frames per beat. A scene-midpoint-only
review can miss a late reveal, early mismatch, or long static interval.

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

After the cohort passes, revise the remaining seven uploaded previews before
uploading more chapters. Then propagate the improved engine and review standard
through all 84 local generations.

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
