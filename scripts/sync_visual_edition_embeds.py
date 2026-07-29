#!/usr/bin/env python3
"""Check or reconcile governed YouTube embeds and adjacent transcripts."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "visual_edition/manifest.json"
BEGIN = "<!-- BEGIN MANAGED VISUAL ABSTRACT:{chapter_id} -->"
END = "<!-- END MANAGED VISUAL ABSTRACT:{chapter_id} -->"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def transcript_body(path: Path) -> str:
    value = path.read_text(encoding="utf-8").strip()
    return re.sub(r"^# [^\n]+\n+", "", value, count=1)


def render_block(packet: dict) -> str:
    chapter_id = packet["chapter_id"]
    youtube_id = packet["youtube"]["video_id"]
    title = packet["quarto_embed"]["frame_title"]
    aria = packet["quarto_embed"]["aria_label"]
    transcript = transcript_body(ROOT / packet["artifacts"]["descriptive_transcript"])
    return f"""{BEGIN.format(chapter_id=chapter_id)}
::: {{#{packet["quarto_embed"]["chapter_anchor"]} .asi-visual-abstract}}
## Visual abstract

<div class="ratio ratio-16x9">
<iframe
  src="https://www.youtube-nocookie.com/embed/{youtube_id}"
  title="{title}"
  aria-label="{aria}"
  loading="lazy"
  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
  referrerpolicy="strict-origin-when-cross-origin"
  allowfullscreen>
</iframe>
</div>

<details class="asi-visual-transcript">
<summary>Read the descriptive transcript</summary>

{transcript}

</details>
:::
{END.format(chapter_id=chapter_id)}"""


def managed_pattern(chapter_id: str) -> re.Pattern[str]:
    return re.compile(
        re.escape(BEGIN.format(chapter_id=chapter_id))
        + r".*?"
        + re.escape(END.format(chapter_id=chapter_id)),
        re.DOTALL,
    )


def insert_after_front_matter(source: str, block: str) -> str:
    if not source.startswith("---\n"):
        raise ValueError("chapter lacks opening YAML front matter")
    close = source.find("\n---\n", 4)
    if close < 0:
        raise ValueError("chapter YAML front matter is not closed")
    at = close + len("\n---\n")
    return source[:at] + "\n" + block + "\n" + source[at:].lstrip("\n")


def reconcile(source: str, packet: dict) -> tuple[str, str | None]:
    chapter_id = packet["chapter_id"]
    pattern = managed_pattern(chapter_id)
    current = pattern.search(source)
    published = (
        packet["lifecycle_state"] == "published_current"
        and packet["youtube"]["publication_state"] == "published_current"
        and packet["quarto_embed"]["state"] == "published_current"
    )
    if published:
        expected = render_block(packet)
        if current:
            updated = source[:current.start()] + expected + source[current.end():]
        else:
            updated = insert_after_front_matter(source, expected)
        if updated != source:
            return updated, "published embed/transcript block is absent or stale"
        return source, None
    if current:
        updated = source[:current.start()] + source[current.end():]
        updated = re.sub(r"\n{3,}", "\n\n", updated)
        return updated, "non-current video retains a managed public embed"
    if "youtube.com/embed/" in source or "youtube-nocookie.com/embed/" in source:
        return source, "chapter contains an unmanaged YouTube embed"
    return source, None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--write",
        action="store_true",
        help="reconcile chapter blocks; the default is a no-write check",
    )
    args = parser.parse_args()
    manifest = load(MANIFEST)
    changes: list[tuple[Path, str]] = []
    failures: list[str] = []
    for row in manifest["chapters"]:
        packet_path = row.get("packet_path")
        chapter_path = ROOT / row["chapter_path"]
        if packet_path is None:
            source = chapter_path.read_text(encoding="utf-8")
            if "youtube.com/embed/" in source or "youtube-nocookie.com/embed/" in source:
                failures.append(f"{row['chapter_id']}: unmanaged YouTube embed without packet")
            continue
        packet = load(ROOT / packet_path)
        source = chapter_path.read_text(encoding="utf-8")
        try:
            updated, defect = reconcile(source, packet)
        except ValueError as error:
            failures.append(f"{row['chapter_id']}: {error}")
            continue
        if defect:
            if args.write and updated != source:
                changes.append((chapter_path, updated))
            else:
                failures.append(f"{row['chapter_id']}: {defect}")
    for path, source in changes:
        path.write_text(source, encoding="utf-8")
    if failures:
        raise SystemExit("Visual embed reconciliation failed:\n - " + "\n - ".join(failures))
    action = f"reconciled {len(changes)} chapter(s)" if args.write else "no-write check passed"
    print(
        f"Visual embed reconciliation {action}: "
        f"{manifest['counts']['youtube_videos_published']} published video(s), "
        f"{manifest['counts']['current_quarto_embeds']} current embed(s)."
    )


if __name__ == "__main__":
    main()
