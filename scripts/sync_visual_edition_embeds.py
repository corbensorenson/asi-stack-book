#!/usr/bin/env python3
"""Check or reconcile governed YouTube embeds and adjacent transcripts."""

from __future__ import annotations

import argparse
import html
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "visual_edition/manifest.json"
PREVIEW_BINDINGS = ROOT / "visual_edition/youtube_preview_bindings.json"
INDEX = ROOT / "index.qmd"
BEGIN = "<!-- BEGIN MANAGED VISUAL ABSTRACT:{chapter_id} -->"
END = "<!-- END MANAGED VISUAL ABSTRACT:{chapter_id} -->"
ROSTER_BEGIN = "<!-- BEGIN MANAGED VISUAL PREVIEW ROSTER -->"
ROSTER_END = "<!-- END MANAGED VISUAL PREVIEW ROSTER -->"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def transcript_body(path: Path) -> str:
    value = path.read_text(encoding="utf-8").strip()
    value = re.sub(r"^# [^\n]+\n+", "", value, count=1)
    rendered = subprocess.run(
        ["quarto", "pandoc", "--from", "gfm", "--to", "html", "-"],
        input=value,
        text=True,
        capture_output=True,
        check=True,
    ).stdout.strip()
    # Raw HTML headings remain inside <details>; Markdown headings would be
    # sectionized by the outer Quarto render and escape the disclosure widget.
    rendered = rendered.replace("<h2", '<h3 class="asi-visual-transcript-heading"')
    rendered = rendered.replace("</h2>", "</h3>")
    return rendered


def render_block(packet: dict, preview: dict | None = None) -> str:
    chapter_id = packet["chapter_id"]
    youtube_id = (
        preview["video_id"] if preview is not None
        else packet["youtube"]["video_id"]
    )
    title = html.escape(packet["quarto_embed"]["frame_title"], quote=True)
    aria = html.escape(packet["quarto_embed"]["aria_label"], quote=True)
    transcript = transcript_body(ROOT / packet["artifacts"]["descriptive_transcript"])
    preview_class = (
        " .asi-visual-abstract--preview" if preview is not None else ""
    )
    heading = "Visual abstract preview" if preview is not None else "Visual abstract"
    preview_notice = ""
    if preview is not None:
        preview_notice = f"""
<div class="asi-visual-preview-notice" role="status">
<strong>Visual-edition preview — {preview["position"]} of 84.</strong>
This is an unlisted staging preview from the first 12 uploaded chapters. The
complete edition is not public yet; the reviewed local caption track has not
yet been attached on YouTube, and this preview does not count as
<code>published_current</code> or change any book claim.
</div>
"""
    return f"""{BEGIN.format(chapter_id=chapter_id)}
::: {{#{packet["quarto_embed"]["chapter_anchor"]} .asi-visual-abstract{preview_class}}}
## {heading}

{preview_notice}
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

<p class="asi-visual-preview-links"><a href="https://www.youtube.com/watch?v={youtube_id}">Open this unlisted preview on YouTube</a></p>

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


def reconcile(
    source: str,
    packet: dict,
    preview: dict | None = None,
) -> tuple[str, str | None]:
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
    if preview is not None:
        expected = render_block(packet, preview)
        if current:
            updated = source[:current.start()] + expected + source[current.end():]
        else:
            updated = insert_after_front_matter(source, expected)
        if updated != source:
            return updated, "preview embed/transcript block is absent or stale"
        return source, None
    if current:
        updated = source[:current.start()] + source[current.end():]
        updated = re.sub(r"\n{3,}", "\n\n", updated)
        return updated, "non-current video retains a managed public embed"
    if "youtube.com/embed/" in source or "youtube-nocookie.com/embed/" in source:
        return source, "chapter contains an unmanaged YouTube embed"
    return source, None


def roster_pattern() -> re.Pattern[str]:
    return re.compile(
        re.escape(ROSTER_BEGIN) + r".*?" + re.escape(ROSTER_END),
        re.DOTALL,
    )


def render_roster(preview: dict) -> str:
    entries = preview["entries"]
    lines = [
        ROSTER_BEGIN,
        "## Visual edition preview",
        "",
        (
            f"The first **{len(entries)} of 84** visual abstracts are embedded "
            "in their canonical chapters for integrated review. They remain "
            "unlisted staging previews, not a completed or published-current "
            "visual edition. Every preview includes an adjacent descriptive "
            "transcript; final YouTube caption and thumbnail reconciliation "
            "is still open."
        ),
        "",
        "::: {.asi-visual-preview-roster}",
    ]
    for entry in entries:
        chapter_title = re.sub(
            r"^\d{2}\.\s+|\s+—\s+The ASI Stack$",
            "",
            entry["title"],
        )
        lines.append(
            f"{entry['position']}. "
            f"[{chapter_title}]({entry['chapter_path']}#visual-abstract)"
        )
    lines.extend([":::", ROSTER_END])
    return "\n".join(lines)


def reconcile_roster(source: str, preview: dict) -> tuple[str, str | None]:
    expected = render_roster(preview)
    pattern = roster_pattern()
    current = pattern.search(source)
    if current:
        updated = source[:current.start()] + expected + source[current.end():]
    else:
        marker = "## 60-Second Trust Surface"
        at = source.find(marker)
        if at < 0:
            raise ValueError("landing page lacks the Trust Surface insertion point")
        updated = source[:at] + expected + "\n\n" + source[at:]
    if updated != source:
        return updated, "landing-page preview roster is absent or stale"
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
    preview = load(PREVIEW_BINDINGS)
    preview_by_chapter = {
        entry["chapter_id"]: entry for entry in preview["entries"]
    }
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
            updated, defect = reconcile(
                source,
                packet,
                preview_by_chapter.get(row["chapter_id"]),
            )
        except ValueError as error:
            failures.append(f"{row['chapter_id']}: {error}")
            continue
        if defect:
            if args.write and updated != source:
                changes.append((chapter_path, updated))
            else:
                failures.append(f"{row['chapter_id']}: {defect}")
    index_source = INDEX.read_text(encoding="utf-8")
    try:
        index_updated, index_defect = reconcile_roster(index_source, preview)
    except ValueError as error:
        failures.append(f"landing-page: {error}")
    else:
        if index_defect:
            if args.write and index_updated != index_source:
                changes.append((INDEX, index_updated))
            else:
                failures.append(f"landing-page: {index_defect}")
    for path, source in changes:
        path.write_text(source, encoding="utf-8")
    if failures:
        raise SystemExit("Visual embed reconciliation failed:\n - " + "\n - ".join(failures))
    action = f"reconciled {len(changes)} chapter(s)" if args.write else "no-write check passed"
    print(
        f"Visual embed reconciliation {action}: "
        f"{manifest['counts']['youtube_videos_published']} published video(s), "
        f"{manifest['counts']['current_quarto_embeds']} current embed(s), "
        f"{len(preview_by_chapter)} unlisted preview embed(s)."
    )


if __name__ == "__main__":
    main()
