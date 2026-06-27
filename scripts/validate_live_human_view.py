#!/usr/bin/env python3
"""Validate the rendered live-site Human view surface after Quarto render.

This is a static rendered-HTML check. It verifies that every rendered chapter
page includes the reading-mode toggle asset and that the live-only headings in
the chapter source are present in HTML at levels the runtime script can mark
and hide in Human view. It does not claim that a reviewed reader release,
ebook, or audiobook exists.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from html.parser import HTMLParser
import json
import re
import sys
from pathlib import Path

import build_reader_edition

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SITE = ROOT / "_site"
DEFAULT_REPORT = ROOT / "build" / "live_human_view_report.json"


class HeadingParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.current_level: int | None = None
        self.current_anchor: str | None = None
        self.current_text: list[str] = []
        self.headings: list[tuple[int, str, str | None]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if re.fullmatch(r"h[1-6]", tag):
            attr_map = dict(attrs)
            self.current_level = int(tag[1])
            self.current_anchor = attr_map.get("data-anchor-id") or attr_map.get("id")
            self.current_text = []

    def handle_endtag(self, tag: str) -> None:
        if self.current_level is None or tag != f"h{self.current_level}":
            return
        text = normalize_html_heading(" ".join(self.current_text))
        if text:
            self.headings.append((self.current_level, text, self.current_anchor))
        self.current_level = None
        self.current_anchor = None
        self.current_text = []

    def handle_data(self, data: str) -> None:
        if self.current_level is not None:
            self.current_text.append(data)


class ClassCounter(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.classes: dict[str, int] = {}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if name != "class" or value is None:
                continue
            for css_class in value.split():
                self.classes[css_class] = self.classes.get(css_class, 0) + 1


def load_structure() -> dict:
    value = json.loads((ROOT / "book_structure.json").read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError("book_structure.json must contain an object")
    return value


def flatten_chapters(structure: dict) -> list[dict]:
    chapters: list[dict] = []
    for part in structure.get("parts", []):
        if not isinstance(part, dict):
            continue
        for chapter in part.get("chapters", []):
            if isinstance(chapter, dict):
                chapters.append(chapter)
    return chapters


def normalize_html_heading(title: str) -> str:
    normalized = re.sub(r"\s+", " ", title.strip())
    normalized = re.sub(r"^\d+(\.\d+)*\s+", "", normalized)
    return normalized.lower()


def source_live_heading_keys(path: Path, strip_headings: set[tuple[int, str]]) -> list[tuple[int, str]]:
    keys: list[tuple[int, str]] = []
    for line in build_reader_edition.strip_frontmatter(path.read_text(encoding="utf-8")).splitlines():
        match = build_reader_edition.HEADING_RE.match(line)
        if not match:
            continue
        key = (len(match.group(1)), build_reader_edition.normalize_heading_title(match.group(2)))
        if key in strip_headings:
            keys.append(key)
    return keys


def source_view_class_counts(path: Path) -> dict[str, int]:
    text = path.read_text(encoding="utf-8")
    return {
        css_class: len(re.findall(rf"\.{re.escape(css_class)}\b", text))
        for css_class in ("asi-human-only", "asi-ai-only", "asi-live-only")
    }


def rendered_headings(path: Path) -> set[tuple[int, str]]:
    parser = HeadingParser()
    parser.feed(path.read_text(encoding="utf-8", errors="ignore"))
    return {(level, text) for level, text, _anchor in parser.headings}


def rendered_heading_anchors(path: Path) -> dict[tuple[int, str], str]:
    parser = HeadingParser()
    parser.feed(path.read_text(encoding="utf-8", errors="ignore"))
    return {
        (level, text): anchor
        for level, text, anchor in parser.headings
        if anchor
    }


def rendered_toc_targets(html: str) -> set[str]:
    targets = set(re.findall(r'data-scroll-target="#([^"]+)"', html))
    targets.update(re.findall(r'href="#([^"]+)"', html))
    return targets


def rendered_class_counts(path: Path) -> dict[str, int]:
    parser = ClassCounter()
    parser.feed(path.read_text(encoding="utf-8", errors="ignore"))
    return {
        css_class: parser.classes.get(css_class, 0)
        for css_class in ("asi-human-only", "asi-ai-only", "asi-live-only")
    }


def validate(site_dir: Path) -> dict[str, object]:
    structure = load_structure()
    profile = build_reader_edition.find_profile("reader_release")
    strip_headings = build_reader_edition.profile_strip_headings(profile)

    errors: list[str] = []
    records: list[dict[str, object]] = []
    total_live_headings = 0
    total_live_toc_targets = 0
    total_view_blocks = {"asi-human-only": 0, "asi-ai-only": 0, "asi-live-only": 0}

    if not site_dir.exists():
        errors.append(f"Rendered site directory is missing: {site_dir.relative_to(ROOT)}")

    for chapter in flatten_chapters(structure):
        source_file = str(chapter.get("file", ""))
        source_path = ROOT / source_file
        html_path = site_dir / Path(source_file).with_suffix(".html")
        expected = source_live_heading_keys(source_path, strip_headings)
        expected_view_classes = source_view_class_counts(source_path)
        total_live_headings += len(expected)
        for css_class, count in expected_view_classes.items():
            total_view_blocks[css_class] += count

        record: dict[str, object] = {
            "chapter_id": chapter.get("id", ""),
            "source_file": source_file,
            "html_file": str(html_path.relative_to(ROOT)) if html_path.exists() else str(html_path),
            "live_only_heading_count": len(expected),
            "live_only_toc_target_count": 0,
            "view_mode_blocks": expected_view_classes,
        }

        if not html_path.exists():
            errors.append(f"{source_file}: rendered chapter HTML is missing at {html_path}")
            records.append(record)
            continue

        html = html_path.read_text(encoding="utf-8", errors="ignore")
        for needle in (
            "asi-stack-reading-mode",
            "data-asi-reading-choice=\"ai\"",
            "data-asi-reading-choice=\"human\"",
            "control.setAttribute(\"aria-describedby\", \"asi-reading-mode-description\")",
            "role=\"status\"",
            "aria-live=\"polite\"",
            "data-asi-reading-mode-status",
            "data-asi-live-toc-link",
            "function markLiveTocLinks",
            "AI/research view active.",
            "Human view active.",
            "AI view",
            "Human view",
        ):
            if needle not in html:
                errors.append(f"{html_path.relative_to(ROOT)}: missing reading-mode toggle text {needle!r}")

        headings = rendered_headings(html_path)
        heading_anchors = rendered_heading_anchors(html_path)
        toc_targets = rendered_toc_targets(html)
        missing_headings = sorted(set(expected) - headings)
        if missing_headings:
            record["missing_rendered_live_headings"] = [
                f"h{level}:{title}" for level, title in missing_headings
            ]
            errors.append(
                f"{html_path.relative_to(ROOT)}: live-only source headings are not present "
                f"as rendered headings: {record['missing_rendered_live_headings']}"
            )
        missing_toc_targets: list[str] = []
        for key in expected:
            anchor = heading_anchors.get(key)
            if not anchor:
                continue
            if anchor not in toc_targets:
                missing_toc_targets.append(f"h{key[0]}:{key[1]} -> #{anchor}")
        live_toc_count = len(expected) - len(missing_toc_targets)
        record["live_only_toc_target_count"] = live_toc_count
        total_live_toc_targets += live_toc_count
        if missing_toc_targets:
            record["missing_live_toc_targets"] = missing_toc_targets
            errors.append(
                f"{html_path.relative_to(ROOT)}: live-only rendered headings are not present "
                f"as TOC targets: {missing_toc_targets}"
            )

        actual_view_classes = rendered_class_counts(html_path)
        missing_view_classes: list[str] = []
        for css_class, expected_count in expected_view_classes.items():
            if actual_view_classes.get(css_class, 0) < expected_count:
                missing_view_classes.append(
                    f"{css_class}: expected {expected_count}, rendered {actual_view_classes.get(css_class, 0)}"
                )
        if missing_view_classes:
            record["missing_rendered_view_classes"] = missing_view_classes
            errors.append(
                f"{html_path.relative_to(ROOT)}: source view-mode blocks did not survive render: "
                f"{missing_view_classes}"
            )

        records.append(record)

    return {
        "schema_version": "0.1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "site_dir": str(site_dir),
        "chapter_count": len(records),
        "live_only_heading_count": total_live_headings,
        "live_only_toc_target_count": total_live_toc_targets,
        "view_mode_blocks": total_view_blocks,
        "status": "pass" if not errors else "fail",
        "chapter_records": records,
        "errors": errors,
        "non_claims": [
            "This static check validates rendered live-site Human view wiring only.",
            "It does not claim a reviewed reader edition, ebook, PDF, DOCX, audiobook, or support-state promotion exists.",
        ],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site", default=str(DEFAULT_SITE), help="rendered Quarto site directory")
    parser.add_argument("--report", help="optional JSON report path")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report = validate(Path(args.site))
    if args.report:
        path = Path(args.report)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    if report["status"] != "pass":
        print("Live Human view validation failed:")
        for error in report["errors"]:
            print(f" - {error}")
        sys.exit(1)

    print(
        "Live Human view validation passed: "
        f"{report['chapter_count']} rendered chapter pages, "
        f"{report['live_only_heading_count']} live-only headings available for runtime hiding, "
        f"{report['live_only_toc_target_count']} live-only TOC targets available for runtime hiding, "
        f"{report['view_mode_blocks']} view-mode blocks rendered."
    )


if __name__ == "__main__":
    main()
