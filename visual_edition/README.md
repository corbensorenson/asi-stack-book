# ASI Stack Visual Edition

This directory is the tracked source and accountability boundary for P7.3.
The canonical book remains the Quarto manuscript. The visual edition projects
each chapter into a three-to-six-minute Manim visual abstract without changing
the chapter's claim label, support state, maximum inference, or release scope.

## Tracked

- the 84-entry derivative manifest;
- the exact toolchain lock and dependency lock;
- the candidate or ratified visual grammar;
- the canonical YouTube channel contract and generated 84-chapter
  publication/revision ledger;
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
python3 scripts/validate_visual_edition.py
python3 scripts/sync_visual_edition_embeds.py
```

All counts are derived from current packets. A storyboard, scene stub, silent
preview, unreviewed caption file, upload, or placeholder embed is not a
completed chapter video.

Current checkpoint: all 84 chapters have validated final
1920×1080/30-fps H.264/AAC masters in ignored local storage. Narration uses
the pinned Apache-2.0 Kokoro-82M bf16 model and `af_heart` voice through the
MIT-licensed `kokoro-mlx` implementation. Exact narration receipts drive the
canonical caption timing; a pinned local MLX Whisper audit checks complete
beginning/end coverage, requires content-normalized word error at or below
3%, and rejects an internal expected-token gap above eight. Across all 84
masters, word error is 0–2.8658%, the largest expected-token gap is four, and
duration is 227.765–331.005 seconds.

The shared visual grammar and narration path are `ratified` and
`qualified_for_all_chapters`. All 84 packets are `ready_not_published`, with
reviewed captions, descriptive transcripts, validated final masters, render
and mux receipts, and seven exact scene-midpoint review frames. The local
masters total 1,015,153,522 bytes outside Git and Pages. YouTube, playlist,
publication, and embed counts remain zero. A local validated master is not a
publication.

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

After platform processing and public observation, use
`record_youtube_platform_receipt.py` to bind the exact video, playlist item,
metadata, reviewed caption, thumbnail, local master, chapter, source commit,
authorization scope, and public observation. Once all 84 receipts exist,
`reconcile_youtube_publication_receipts.py` validates the complete set before
changing any tracked file. Its `--write` mode then updates all packets,
channel/playlist identity, manifest, revision ledger, and managed Quarto
blocks as one complete-edition reconciliation; it never calls YouTube itself.
