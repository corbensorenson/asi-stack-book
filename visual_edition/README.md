# ASI Stack Visual Edition

This directory is the tracked source and accountability boundary for P7.3.
The canonical book remains the Quarto manuscript. The visual edition projects
each chapter into a Manim visual abstract, normally targeting three to six
minutes while allowing justified longer treatments when clarity requires them,
without changing the chapter's claim label, support state, maximum inference,
or release scope.

## Tracked

- the 84-entry derivative manifest;
- the exact toolchain lock and dependency lock;
- the candidate or ratified visual grammar;
- the canonical YouTube channel contract and generated 84-chapter
  publication/revision ledger;
- the repository-local v2 authoring skill, beat-plan/review schemas, and
  canonical generation-2 production ledger;
- owner-authorized unlisted-preview bindings, kept separate from final
  publication receipts;
- immutable generation receipts and exact, non-authorizing replacement plans;
- reusable Manim source;
- per-chapter packet metadata, storyboard, scene code, narration, reviewed
  captions, descriptive transcript, thumbnail, and render/platform receipts.

## Not tracked

Rendered video, narration audio, partial frames, and Manim caches belong under
`build/visual_edition/`. Published binaries belong on YouTube. No upload,
metadata change, playlist mutation, publication, replacement, or deletion is
authorized merely because a local packet passes.

## Local environment

Create the isolated environment and install the pinned direct dependency:

```bash
python3 -m venv build/visual_edition/venv
build/visual_edition/venv/bin/python -m pip install "manim==0.20.1"
```

Create the separate local narration and transcript-audit environment from the
exact resolved lock:

```bash
python3 -m venv build/visual_edition/tts_venv
build/visual_edition/tts_venv/bin/python -m pip install \
  -r visual_edition/narration_requirements.lock.txt
```

The ignored model cache must contain the exact Kokoro synthesis and
Whisper-small.en verification revisions and file digests recorded in
`narration_toolchain.json`. The voice, model weights, virtual environments,
raw narration, ASR JSON, and final media never enter Git or the Pages artifact.

Capture or verify the exact runtime:

```bash
python3 scripts/capture_manim_toolchain.py --python build/visual_edition/venv/bin/python
python3 scripts/validate_manim_toolchain.py
python3 scripts/validate_manim_toolchain.py --probe-runtime \
  --python build/visual_edition/venv/bin/python
```

Generate the 84-entry manifest and validate the edition:

```bash
python3 scripts/build_visual_edition_manifest.py
python3 scripts/build_youtube_ledger.py
python3 scripts/render_youtube_thumbnails.py --all-chapters
python3 scripts/build_youtube_thumbnail_review_sheets.py
python3 scripts/build_youtube_upload_plan.py
python3 scripts/build_youtube_publication_preflight.py
python3 scripts/validate_youtube_publication_preflight.py
python3 scripts/validate_youtube_preview_bindings.py
python3 scripts/validate_youtube_supersession_workflow.py
python3 scripts/validate_visual_edition.py
python3 scripts/sync_visual_edition_embeds.py
```

Generate and validate the fail-closed generation-2 production state:

```bash
python3 scripts/sync_manim_v2_production_ledger.py
python3 scripts/validate_manim_v2_production_ledger.py
```

`manim_v2_production_ledger.json` is the current generation-2 authority. It
derives all 84 targets in canonical book order, preserves every generation-one
master and the twelve unlisted preview identities, and prevents YouTube or
Quarto advancement before the complete audiovisual acceptance chain passes.

All counts are derived from current packets. A storyboard, scene stub, silent
preview, unreviewed caption file, upload, or placeholder embed is not a
completed chapter video.

Current checkpoint: the 84-chapter generation-one baseline remains preserved
as ignored local history, while generation two is the active quality lane.
Generation-two chapters 1–15 have passed beat-plan, animatic, and
picture-and-sound-lock gates; chapters 16–84 remain planned. Generation two
does not yet have a release candidate, accepted video, YouTube-current video,
or current Quarto embed. Chapter 14 is intentionally 06:41.90: the six-minute
value is a preferred soft range, and shortening its allocation puzzle, standing
repair, rights receipt, fork/export duties, evidence boundary, or handoff would
collapse distinct teaching responsibilities. Narration uses the pinned
Apache-2.0 Kokoro-82M bf16 model and `af_heart` voice through the MIT-licensed
`kokoro-mlx` implementation. Exact narration receipts drive canonical caption
timing; local AV diagnostics and receipt-derived beat reviews are evidence for
the audiovisual derivative only, not for any book claim. Chapter 15 is
intentionally 07:00.77: the six-minute value remains a preferred soft range,
and compressing typed identities, affected-party standing, consumer leases,
proxy interventions, ontology reopening, descendant retirement, or the public
authority handoff would remove load-bearing teaching distinctions.

The original technical visual grammar and narration path are `ratified` and
`qualified_for_all_chapters`. All 84 packets are `ready_not_published`, with
reviewed captions, descriptive transcripts, validated final masters, render
and mux receipts, and seven exact scene-midpoint review frames. The local
masters total 1,015,153,522 bytes outside Git and Pages. Twelve exact masters
are now staged as unlisted YouTube videos in the private canonical playlist
and projected into their chapters as visibly labeled preview players with
adjacent descriptive transcripts. Published-current videos, final platform
receipts, and published-current Quarto embeds remain zero. A local validated
master or an unlisted preview is not a publication.

Owner viewing of the first five previews exposed a stricter pedagogical
failure that these technical receipts do not measure. Videos 2–5 are thin
wrappers over a generic seven-tableau engine; their few entrance animations
often finish well before the narrated idea. They are technically intact but
not accepted for final publication. P7.3-F9 now requires a v2 beat-level plan;
chapter-specific art direction, signature image, and persistent visual world;
purposeful state change for every substantive spoken idea; semantic easing and
camera rules; audio-derived clause-level anchors; directed narration and sound;
integrated accessibility; and three-gate animatic, picture-and-sound-lock, and
release-candidate review. Full experience review covers 1×, muted, audio-only,
captions-on, phone/large-screen, headphone/speaker, and random-frame passes and
requires at least 4/5 independently for clarity, composition, motion, sync,
continuity, pacing, voice, mix, engagement, accessibility, and claim fidelity.
The first five form the remediation cohort, the remaining seven previews
followed, and chapters 13–84 were held until the revised method passed. Chapters
13–15 are now through picture-and-sound lock under that method; chapters
16–84 remain gated behind the same production chain. Existing unlisted embeds remain
historical review previews, not publication-quality acceptance.

The generation-2 ledger currently has 69 planned chapters and fifteen chapters
through both animatic and picture-and-sound lock. The first fifteen
replacements use chapter-specific persistent worlds, audio-derived beat timing,
exhaustive caption-boundary review, and independent per-dimension scores without
average laundering. Chapter 10, `human-factors-and-meaningful-control-in-oversight`,
turns one synthetic transfer episode into a worked distinction among nominal
approval, informed review, effective intervention, and meaningful control; it
tests an eight-condition control envelope, exercises the safe-hold path, and
keeps the task record separate from any score of the person. Rejected
animatics remain preserved as generation history. Chapter 12,
`constitutional-alignment-substrate`, follows Lina's threatened midnight
housing-payment suspension through a noncompensating four-plane review,
inaccessible-appeal failure, bounded pre-effect correction, self-weakening
constitutional update, descendant-handle preservation, and explicitly finite
proof envelope. Chapter 13, `inner-alignment-mesa-optimization-and-learned-objective-integrity`,
uses an identical-trace sorting-lab puzzle, a sealed stripe intervention,
camera-aware policy test, four evidence lanes, mitigation transfer, and a
finite objective-integrity boundary. Chapter 14,
`moral-uncertainty-and-value-conflict`, uses one emergency generator, two
defensible obligations, a value-conflict record, a bounded decision lease, a
linked rights receipt, fail-closed standing repair, custody separation,
replacement/fork requalification, and an explicit non-claim boundary. Chapter
15, `governed-objective-formation-value-learning-and-goal-integrity`, uses a
Rivergate flood-harm charter to keep purpose, target property, evidence, proxy,
signal, planner, affected-party standing, consumer leases, evaluator authority,
and descendant retirement distinct; its sealed proxy intervention,
hidden-neighborhood counterexample, finite registry, and public-authority
handoff remain explicitly bounded. All fifteen delivery masters remain
candidates only: no generation-2 video has passed release-candidate,
independent, technical, claim-fidelity, or acceptance gates, and none is
uploaded or current in Quarto.

The repository-local `skills/asi-stack-manim-videos/` authoring skill includes
a structural v2 beat-plan audit,
start/middle/end frame extraction for every beat, and mechanical A/V
diagnostics for freezes, black intervals, silence, duration drift, loudness,
and true peak. On the Chapter 14 picture-and-sound lock, the diagnostic found
thirteen
intentional 6.0–9.9-second reading holds while the audio measured -16.4 LUFS
integrated, 3.1 LU loudness range, and -1.3 dBTP. Each hold is paired with
narrated reasoning and a visible state transition; mechanical checks locate
review risks and do not certify beauty, comfort, truth, or learning.

The preview exception is narrow and explicit. A managed player may appear
before full publication only when an exact row in
`youtube_preview_bindings.json` binds the owner authorization, canonical
position, YouTube identity, local master, chapter digest, source commit,
caption, transcript, thumbnail state, and unlisted visibility. The player and
landing-page roster must identify the incomplete denominator, and preview
counts must remain separate from `published_current`. The current preview is
12/84; local caption tracks still need platform attachment for all twelve, and
custom thumbnails still need application for videos 7–12.

Each packet keeps an editable SVG thumbnail source in Git. Upload preparation
rasterizes it to an ignored 3840×2160 PNG, binds both source and output
digests, rejects files above the YouTube Data API's 2 MB ceiling, and builds
bounded contact sheets for visual review. The publication plan stages every
first-generation upload as `unlisted`; the reconciled set becomes `public`
only after video processing, metadata, captions, thumbnails, playlist order,
receipts, and embeds all pass.

`youtube_publication_preflight.json` proves that all 84 exact local master,
caption, and thumbnail triples remain ready without claiming an upload. It
binds `youtube_mutation_scope.json`, the immutable allowlist, prohibition list,
stop conditions, channel identity, and exact upload-plan digest to which
action-time approval and every platform receipt must refer. Preparing or
hashing that scope is not authorization. The preflight also records two honest
execution routes. YouTube Studio accepts at most 15
files in one upload dialog, so the browser route uses batches of
15/15/15/15/15/9 and stops cleanly on the channel-specific daily video or
thumbnail limit. The Data API fallback uses resumable uploads, but its default
100-video insert bucket and 10,000-unit general bucket require at least five
quota days to attach 84 reviewed caption tracks, thumbnails, ordered playlist
items, and final privacy transitions. An unverified API project also
force-restricts uploads to private, so it is not a publication shortcut.

Visual QA samples the midpoint of each exact narration scene from the mux
receipt, not arbitrary fractions of total runtime. The 84-chapter review is 21
bounded contact sheets covering 588 scene-midpoint frames. This sampling
contract caught and replaced an earlier percentage-based reviewer that could
land inside transitions and misrepresent scene completeness.

Release renders use the exact 1920×1080/30-fps values in `manim.cfg` with no
quality shortcut flag. In particular, `-qh` is not the release command because
ManimCE 0.20.1 expands that shortcut to 1080p60 and would override the pinned
frame-rate contract.

The embed synchronizer is a no-write check by default. After an exact packet is
`published_current`, run it with `--write` to place the
`youtube-nocookie.com` player and the packet's full descriptive transcript
next to one another in the canonical chapter. It removes managed blocks for
videos that are no longer current and rejects unmanaged YouTube embeds.
Chapter freshness is computed over canonical manuscript content with this
managed block excluded. Consequently, inserting or replacing the generated
player cannot make its own packet stale, while any material prose or source
change outside the block still changes the bound digest.

Not every digest change requires a new video. Source-assignment metadata,
passage-review status, or added prose can change canonical chapter bytes while
leaving the visual abstract's problem, mechanism, trace, failure boundary,
evidence ceiling, non-claims, and handoff intact. In that case,
`reconcile_visual_chapter_bindings.py` permits an identity-only rebind: all
seven generated semantic fields must match byte for byte, or a hand-authored
pilot must have an explicit reviewed rationale. The command preserves media,
receipts, lifecycle, and support state and records every decision in
`chapter_binding_revalidation.json`. Any semantic mismatch fails closed and
requires regeneration.

## YouTube identity and chapter updates

`youtube_channel.json` binds this edition to the verified **corben sorenson**
channel, ID `UCX7Tu67cGmKfT6O38xxiQFA`. Authentication proves access only; it
does not authorize an upload or another mutation. The all-84 local validation
prerequisite is satisfied, but the canonical playlist remains uncreated until
exact action-time authority is given.

`youtube_ledger.json` is generated in book order and provides one row for every
canonical chapter, including chapters without packets. Each row preserves the
stable internal identity `asi-video-<chapter-id>`, current chapter digest,
packet and lifecycle state, YouTube channel/video/playlist identity, upload
generation, uploaded render digest, bound chapter digest and source commit,
publication receipt, predecessor video, and the next required action. Rebuild
the ledger after any chapter, packet, publication, or playlist change.

YouTube does not replace an uploaded binary at the same URL. A material chapter
revision therefore creates a new video generation and new YouTube video ID.
The prior generation and receipt remain historical; by default the prior video
becomes unlisted and points to the current generation. In the same governed
transaction, the new upload enters the canonical playlist position, its packet
becomes `published_current`, the old packet generation becomes `superseded`,
and the Quarto embed is reconciled to the new ID. The validator rejects a stale
ledger, a mismatched uploaded/render digest, a missing platform receipt, a
wrong channel, or an embed that does not match the current publication state.
Regenerating a packet preserves any existing platform identity as `stale`
instead of resetting it to an unpublished blank. The ledger derives its
append-only `generations` history from immutable receipts under
`visual_edition/platform_receipts/generation-N/`; it rejects gaps, duplicate
video IDs, broken predecessor chains, or disagreement between the latest
receipt and the packet's current platform projection.

After a published chapter is materially revised and its new local derivative
is validated, prepare its replacement transaction:

```bash
python3 scripts/prepare_youtube_supersession.py \
  --chapter-id <chapter-id> \
  --change-reason "<material revision>" \
  --write
python3 scripts/validate_youtube_supersession_workflow.py
```

The resulting `visual_edition/supersession_plans/<chapter-id>-gN.json` is the
complete allowlist, ordering, rollback, stop-condition, predecessor, and
replacement contract for that one generation. Its file SHA-256 is the only
valid action-time authorization scope for that replacement. Generation-one
publication authority cannot be reused, and preparing the plan is not
authorization. After the exact platform steps have been performed and both
the replacement and predecessor disposition have been observed, record and
reconcile them:

```bash
python3 scripts/record_youtube_supersession_receipt.py \
  --plan visual_edition/supersession_plans/<chapter-id>-gN.json \
  --authorization-scope-sha256 <exact-plan-sha256> \
  <observed-platform-arguments> \
  --write
python3 scripts/reconcile_youtube_supersession_receipt.py \
  --plan visual_edition/supersession_plans/<chapter-id>-gN.json \
  --receipt visual_edition/platform_receipts/generation-N/<chapter-id>.json
python3 scripts/reconcile_youtube_supersession_receipt.py \
  --plan visual_edition/supersession_plans/<chapter-id>-gN.json \
  --receipt visual_edition/platform_receipts/generation-N/<chapter-id>.json \
  --write
```

The reconciler verifies the new public video, exact master and metadata,
caption and thumbnail, playlist position, predecessor pointer, predecessor
`unlisted` state, and removal of only the predecessor playlist item. Its
rollback restores tracked repository bytes and never deletes either YouTube
generation. The no-write reconciliation command is the required preview.

After platform processing and public observation, use
`record_youtube_platform_receipt.py` to bind the exact video, playlist item,
metadata, reviewed caption, thumbnail, local master, chapter, source commit,
authorization scope, and public observation. Once all 84 receipts exist,
`reconcile_youtube_publication_receipts.py` validates the complete set before
changing any tracked file. Its `--write` mode then updates all packets,
channel/playlist identity, manifest, revision ledger, and managed Quarto
blocks as one complete-edition reconciliation; it never calls YouTube itself.
