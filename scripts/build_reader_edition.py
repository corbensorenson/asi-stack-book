#!/usr/bin/env python3
"""Generate a derived human-reader edition draft from the living book source.

The generated files are written under build/ by default and are ignored by git.
This script does not render EPUB, PDF, DOCX, or audio artifacts. It only creates
the cleaned Quarto source needed for those later release steps.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STRUCTURE_PATH = ROOT / "book_structure.json"
PROFILES_PATH = ROOT / "editions" / "release_profiles.json"
DEFAULT_OUTPUT = ROOT / "build" / "reader_edition"

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n?", re.DOTALL)


def load_json(path: Path) -> object:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def yaml_string(value: object) -> str:
    return json.dumps("" if value is None else str(value))


def normalize_heading_title(title: str) -> str:
    title = re.sub(r"\s+\{.*\}\s*$", "", title.strip())
    return title.strip().lower()


def strip_frontmatter(text: str) -> str:
    return FRONTMATTER_RE.sub("", text, count=1)


def strip_sections(text: str, strip_headings: set[tuple[int, str]]) -> tuple[str, dict[str, int]]:
    lines = strip_frontmatter(text).splitlines()
    output: list[str] = []
    removed: dict[str, int] = {}
    skip_level: int | None = None

    for line in lines:
        match = HEADING_RE.match(line)
        level = len(match.group(1)) if match else None
        title = normalize_heading_title(match.group(2)) if match else ""

        if skip_level is not None:
            if match and level is not None and level <= skip_level:
                skip_level = None
            else:
                continue

        if match and level is not None and (level, title) in strip_headings:
            removed[title] = removed.get(title, 0) + 1
            skip_level = level
            continue

        output.append(line)

    return "\n".join(output).strip() + "\n", removed


def find_profile(profile_id: str) -> dict:
    data = load_json(PROFILES_PATH)
    if not isinstance(data, dict):
        raise TypeError("editions/release_profiles.json must contain an object")
    profiles = data.get("profiles", [])
    if not isinstance(profiles, list):
        raise TypeError("release profile file must contain a profiles list")
    for profile in profiles:
        if isinstance(profile, dict) and profile.get("id") == profile_id:
            return profile
    raise KeyError(f"Profile not found: {profile_id}")


def flatten_parts(structure: dict) -> list[dict]:
    parts: list[dict] = []
    for part in structure.get("parts", []):
        if not isinstance(part, dict):
            continue
        parts.append(part)
    return parts


def profile_strip_headings(profile: dict) -> set[tuple[int, str]]:
    result: set[tuple[int, str]] = set()
    for record in profile.get("strip_headings", []):
        if not isinstance(record, dict):
            continue
        result.add((int(record["level"]), normalize_heading_title(str(record["title"]))))
    return result


def clean_file(src: Path, dst: Path, strip_headings: set[tuple[int, str]]) -> dict[str, int]:
    text = src.read_text(encoding="utf-8")
    cleaned, removed = strip_sections(text, strip_headings)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(cleaned, encoding="utf-8")
    return removed


def write_reader_index(output_dir: Path, structure: dict) -> None:
    title = structure.get("title", "The ASI Stack")
    subtitle = structure.get("subtitle", "")
    text = f"""# {title} {{.unnumbered}}

**{title}: {subtitle}** is a reader edition draft derived from the living technical book by Corben Sorenson.

![Layered conceptual architecture for the ASI Stack](assets/images/asi-stack-hero.png){{#fig-reader-asi-stack-hero fig-alt="A light technical illustration of a layered transparent systems stack with routing nodes, ledgers, and controlled feedback loops."}}

## Reader Edition Note

This edition is meant for humans who want the cohesive argument without the live research scaffolding in every chapter. The canonical living book remains the source of truth for source crosswalks, claim/evidence states, proof hooks, schemas, tests, release records, and current residuals.

## Core Thesis

Efficient ASI should not be treated as one giant opaque model. It should be treated as a governed cognitive stack: alignment, governance, planning, memory, reasoning, execution, routing, compression, evidence, and recursive self-improvement cooperating through typed boundaries, verification, artifact memory, and bounded authority.

## Reading Path

Read Part I for the thesis, boundaries, alignment, and governance substrate. Read Part II as the operational spine: intent, planning, memory, reasoning, execution, and artifacts. Read Part III for routing, compression, representation, mathematical substrates, and cyclic/proof-carrying mechanisms. Read Part IV for evidence, implementation, feedback learning, reference architecture, and the living-book method.
"""
    (output_dir / "index.qmd").write_text(text, encoding="utf-8")


def write_quarto(output_dir: Path, structure: dict, profile: dict) -> None:
    formats = list(profile.get("publication_formats", []))
    lines = [
        "# This file is generated by scripts/build_reader_edition.py.",
        "# Edit the living book source or edition profile, then regenerate.",
        "",
        "project:",
        "  type: book",
        "  output-dir: _reader_site",
        "",
        "book:",
        f"  title: {yaml_string(structure.get('title', 'The ASI Stack'))}",
        '  subtitle: "Reader Edition Draft"',
        f"  author: {yaml_string(structure.get('author', ''))}",
        "  chapters:",
        "    - index.qmd",
    ]
    if (output_dir / "preface.qmd").exists():
        lines.append("    - preface.qmd")

    for part in flatten_parts(structure):
        lines.append(f"    - part: {yaml_string(part['title'])}")
        lines.append("      chapters:")
        for chapter in part.get("chapters", []):
            lines.append(f"        - {chapter['file']}")

    appendices = profile.get("include_appendices", [])
    if appendices:
        lines.append("  appendices:")
        for appendix in appendices:
            lines.append(f"    - {appendix}")

    lines.extend(["", "format:"])
    if "html" in formats:
        lines.extend([
            "  html:",
            "    toc: true",
            "    number-sections: true",
            "    theme:",
            "      - cosmo",
            "      - assets/styles.scss",
            "    link-external-newwindow: true",
        ])
    if "epub" in formats:
        lines.extend([
            "  epub:",
            "    toc: true",
            "    cover-image: assets/images/asi-stack-hero.png",
        ])
    if "docx" in formats:
        lines.extend([
            "  docx:",
            "    toc: true",
        ])
    if "pdf" in formats:
        lines.extend([
            "  pdf:",
            "    toc: true",
            "    number-sections: true",
        ])

    lines.extend(["", "execute:", "  freeze: auto", ""])
    (output_dir / "_quarto.yml").write_text("\n".join(lines), encoding="utf-8")


def copy_assets(output_dir: Path) -> None:
    src = ROOT / "assets"
    dst = output_dir / "assets"
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns(".DS_Store"))


def generate(output_dir: Path, profile_id: str) -> dict[str, object]:
    structure = load_json(STRUCTURE_PATH)
    if not isinstance(structure, dict):
        raise TypeError("book_structure.json must contain an object")
    profile = find_profile(profile_id)
    strip_headings = profile_strip_headings(profile)

    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    copy_assets(output_dir)
    write_reader_index(output_dir, structure)

    removed_totals: dict[str, int] = {}
    copied_files = 1
    for front_file in structure.get("front_matter", []):
        if front_file == "index.qmd":
            continue
        src = ROOT / front_file
        if src.exists():
            removed = clean_file(src, output_dir / front_file, strip_headings)
            copied_files += 1
            for key, count in removed.items():
                removed_totals[key] = removed_totals.get(key, 0) + count

    chapter_count = 0
    for part in flatten_parts(structure):
        for chapter in part.get("chapters", []):
            src = ROOT / chapter["file"]
            removed = clean_file(src, output_dir / chapter["file"], strip_headings)
            copied_files += 1
            chapter_count += 1
            for key, count in removed.items():
                removed_totals[key] = removed_totals.get(key, 0) + count

    for appendix in profile.get("include_appendices", []):
        src = ROOT / appendix
        if src.exists():
            removed = clean_file(src, output_dir / appendix, strip_headings)
            copied_files += 1
            for key, count in removed.items():
                removed_totals[key] = removed_totals.get(key, 0) + count

    write_quarto(output_dir, structure, profile)
    return {
        "output_dir": str(output_dir),
        "profile": profile_id,
        "chapters": chapter_count,
        "files": copied_files,
        "removed_sections": removed_totals,
        "formats": profile.get("publication_formats", []),
    }


def scan_for_stripped_headings(output_dir: Path, strip_headings: set[tuple[int, str]]) -> list[str]:
    violations: list[str] = []
    for path in output_dir.rglob("*.qmd"):
        text = path.read_text(encoding="utf-8")
        for line in text.splitlines():
            match = HEADING_RE.match(line)
            if not match:
                continue
            level = len(match.group(1))
            title = normalize_heading_title(match.group(2))
            if (level, title) in strip_headings:
                violations.append(f"{path.relative_to(output_dir)}: {line}")
    return violations


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", default="reader_release", help="edition profile id to generate")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="output directory for generated Quarto source")
    parser.add_argument("--check", action="store_true", help="generate into a temporary directory and verify stripped headings")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    profile = find_profile(args.profile)
    strip_headings = profile_strip_headings(profile)

    if args.check:
        with tempfile.TemporaryDirectory(prefix="asi-reader-edition-") as temp_dir:
            output_dir = Path(temp_dir)
            summary = generate(output_dir, args.profile)
            violations = scan_for_stripped_headings(output_dir, strip_headings)
            if violations:
                print("Reader edition still contains stripped headings:")
                for violation in violations:
                    print(f" - {violation}")
                raise SystemExit(1)
            print(
                "Reader edition check passed: "
                f"{summary['chapters']} chapters, {summary['files']} files, "
                f"{sum(summary['removed_sections'].values())} live-only sections removed."
            )
            return

    output_dir = Path(args.output)
    summary = generate(output_dir, args.profile)
    print(
        "Reader edition generated: "
        f"{summary['output_dir']} "
        f"({summary['chapters']} chapters, formats: {', '.join(summary['formats'])})."
    )
    print("Render specific formats from the generated directory only after reviewing the manuscript.")


if __name__ == "__main__":
    main()
