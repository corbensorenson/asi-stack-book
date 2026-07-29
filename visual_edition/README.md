# ASI Stack Visual Edition

This directory is the tracked source and accountability boundary for P7.3.
The canonical book remains the Quarto manuscript. The visual edition projects
each chapter into a three-to-six-minute Manim visual abstract without changing
the chapter's claim label, support state, maximum inference, or release scope.

## Tracked

- the 84-entry derivative manifest;
- the exact toolchain lock and dependency lock;
- the candidate or ratified visual grammar;
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
python3 scripts/validate_visual_edition.py
python3 scripts/sync_visual_edition_embeds.py
```

All counts are derived from current packets. A storyboard, scene stub, silent
preview, unreviewed caption file, upload, or placeholder embed is not a
completed chapter video.

Current checkpoint: all five representative pilots have complete source
packets and visually reviewed draft and 1920×1080/30-fps release-profile
visuals. All five remain `rendered`, not `validated`: the local Samantha tracks
are pacing aids whose publication rights are not cleared, final captions have
not been listened against an authorized narration master, and no final A/V
master exists. The grammar therefore remains `candidate`, the other 79
chapters remain `planned`, and YouTube/playlist/embed counts remain zero.

Release renders use the exact 1920×1080/30-fps values in `manim.cfg` with no
quality shortcut flag. In particular, `-qh` is not the release command because
ManimCE 0.20.1 expands that shortcut to 1080p60 and would override the pinned
frame-rate contract.

The embed synchronizer is a no-write check by default. After an exact packet is
`published_current`, run it with `--write` to place the
`youtube-nocookie.com` player and the packet's full descriptive transcript
next to one another in the canonical chapter. It removes managed blocks for
videos that are no longer current and rejects unmanaged YouTube embeds.
