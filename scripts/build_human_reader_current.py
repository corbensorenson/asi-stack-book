#!/usr/bin/env python3
"""Build the maintained Human Reader draft manifest and generated surfaces."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
from typing import Optional


ROOT = Path(__file__).resolve().parents[1]
EDITION = ROOT / "editions/reader_manuscript/current"
CHAPTERS = EDITION / "chapters"
GENERATED = EDITION / "generated"
MANIFEST = EDITION / "manifest.json"
QUARTO = EDITION / "_quarto.yml"
INDEX = EDITION / "index.qmd"
OUTLINE = ROOT / "docs/human_reader_26_unit_outline.md"
STRUCTURE = ROOT / "book_structure.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def visible_word_count(text: str) -> int:
    text = re.sub(r"^---.*?^---\s*", "", text, flags=re.MULTILINE | re.DOTALL)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    text = re.sub(r"\{\{<.*?>\}\}", "", text)
    return len(re.findall(r"\b[\w'-]+\b", text))


def outline_units() -> list[dict]:
    text = OUTLINE.read_text(encoding="utf-8")
    blocks = re.split(r"^## Unit ", text, flags=re.MULTILINE)[1:]
    units = []
    for block in blocks:
        heading, body = block.split("\n", 1)
        match = re.fullmatch(r"(\d+) - (.+)", heading.strip())
        if match is None:
            raise ValueError(f"Malformed unit heading: {heading!r}")

        def field(name: str, next_name: Optional[str] = None) -> str:
            end = rf"(?=\n\n\*\*{re.escape(next_name)}\.\*\*)" if next_name else r"(?=\n\n(?:\*\*|#)|\Z)"
            found = re.search(rf"\*\*{re.escape(name)}\.\*\*\s*(.*?){end}", body, flags=re.DOTALL)
            if found is None:
                raise ValueError(f"Unit {match.group(1)} missing {name}")
            return " ".join(found.group(1).split())

        target = field("Target length")
        length_match = re.fullmatch(r"([\d,]+)-([\d,]+) words\.", target)
        if length_match is None:
            raise ValueError(f"Unit {match.group(1)} has malformed target length")
        route_text = field("Canonical owner routes", "Narrative job")
        unit_id = f"unit-{int(match.group(1)):02d}"
        title = match.group(2).strip()
        units.append(
            {
                "unit_id": unit_id,
                "order": int(match.group(1)),
                "title": title,
                "owner_ids": re.findall(r"`([^`]+)`", route_text),
                "narrative_job": field("Narrative job", "Central question"),
                "central_question": field("Central question", "Argument moves"),
                "strongest_objection": field("Strongest objection", "Evidence that would change the conclusion"),
                "conclusion_change": field("Evidence that would change the conclusion", "Handoff"),
                "handoff": field("Handoff", "Target length"),
                "target_min_words": int(length_match.group(1).replace(",", "")),
                "target_max_words": int(length_match.group(2).replace(",", "")),
                "source_file": f"chapters/{unit_id}-{slugify(title)}.qmd",
            }
        )
    return units


def build() -> tuple[dict, dict[Path, str]]:
    structure = json.loads(STRUCTURE.read_text(encoding="utf-8"))
    owner_map = {
        chapter["id"]: chapter
        for part in structure["parts"]
        for chapter in part["chapters"]
    }
    units = outline_units()
    outputs: dict[Path, str] = {}
    records = []
    rendered_chapters = []
    for unit in units:
        source_path = EDITION / unit["source_file"]
        exists = source_path.is_file()
        words = visible_word_count(source_path.read_text(encoding="utf-8")) if exists else 0
        state = "not_started"
        if exists:
            state = (
                "target_length_reached_internal_review_pending"
                if unit["target_min_words"] <= words <= unit["target_max_words"]
                else "drafting"
            )
            rendered_chapters.append(unit["source_file"])
            panel_path = GENERATED / f"{unit['unit_id']}-status.qmd"
            support = sorted({owner_map[owner_id]["evidence_level"] for owner_id in unit["owner_ids"]})
            implemented_targets = sum(
                target.get("status") == "implemented"
                for owner_id in unit["owner_ids"]
                for target in owner_map[owner_id].get("proof_targets", [])
            )
            owner_links = ", ".join(
                f"[{owner_map[owner_id]['title']}](https://corbensorenson.github.io/asi-stack-book/chapters/{owner_id}.html)"
                for owner_id in unit["owner_ids"]
            )
            panel = (
                "::: {.callout-note collapse=\"true\"}\n"
                "## Research status\n\n"
                f"**Technical owners.** {len(unit['owner_ids'])} canonical routes.\n\n"
                f"**Owner routes.** {owner_links}.\n\n"
                f"**Core support states.** {', '.join(support)}.\n\n"
                f"**Implemented bounded proof targets.** {implemented_targets}.\n\n"
                "**Current boundary.** Editorial synthesis does not transfer support among owners and does not establish system-level efficiency, safety, deployment readiness, AGI, or ASI.\n\n"
                f"**What would change the conclusion.** {unit['conclusion_change']}\n\n"
                "**Technical evidence.** Follow the owner routes above and the live book's claim/evidence registry.\n"
                ":::\n"
            )
            outputs[panel_path] = panel
        records.append(
            {
                **unit,
                "state": state,
                "visible_word_count": words,
                "source_sha256": digest(source_path) if exists else None,
                "owner_support_states": sorted({owner_map[owner_id]["evidence_level"] for owner_id in unit["owner_ids"]}),
            }
        )

    part_titles = {
        1: "Part I - Why Intelligence Needs a Governed Stack",
        2: "Part II - Building Governed Cognition",
        3: "Part III - Learning, Resources, and Recursive Improvement",
    }
    chapter_lines = ["    - index.qmd"]
    for part_number, start, end in ((1, 1, 8), (2, 9, 18), (3, 19, 26)):
        part_files = [record["source_file"] for record in records if start <= record["order"] <= end and record["state"] != "not_started"]
        if part_files:
            chapter_lines.append(f"    - part: \"{part_titles[part_number]}\"")
            chapter_lines.append("      chapters:")
            chapter_lines.extend(f"        - {path}" for path in part_files)
    quarto = (
        "# Generated by scripts/build_human_reader_current.py\n"
        "project:\n  type: book\n  output-dir: _book\n\n"
        "book:\n  title: \"The ASI Stack\"\n"
        "  subtitle: \"Human Reader Edition - Maintained Draft\"\n"
        "  author: \"Corben Sorenson\"\n  chapters:\n"
        + "\n".join(chapter_lines)
        + "\n\nformat:\n  html:\n    toc: true\n    number-sections: true\n    theme: cosmo\nlang: en-US\n"
    )
    outputs[QUARTO] = quarto

    index_lines = [
        "# Human Reader Edition",
        "",
        "This is the maintained independent prose source for the 26-unit Human Reader edition. It is incomplete until every unit reaches its target range and passes editorial review; the live technical book remains the claim, proof, evidence, and source authority.",
        "",
        "| Unit | Chapter | State | Words |",
        "|---:|---|---|---:|",
    ]
    for record in records:
        title = record["title"]
        if record["state"] != "not_started":
            title = f"[{title}]({record['source_file']})"
        index_lines.append(f"| {record['order']} | {title} | `{record['state']}` | {record['visible_word_count']:,} |")
    outputs[INDEX] = "\n".join(index_lines) + "\n"

    manifest = {
        "schema_version": "asi_stack.human_reader_current.v1",
        "edition_id": "human-reader-current",
        "state": "independent_manuscript_in_progress",
        "source_graph": "book_structure.json",
        "source_outline": "docs/human_reader_26_unit_outline.md",
        "book_structure_sha256": digest(STRUCTURE),
        "outline_sha256": digest(OUTLINE),
        "unit_count": len(records),
        "owner_route_count": sum(len(record["owner_ids"]) for record in records),
        "started_unit_count": sum(record["state"] != "not_started" for record in records),
        "target_length_unit_count": sum(record["state"] == "target_length_reached_internal_review_pending" for record in records),
        "visible_word_count": sum(record["visible_word_count"] for record in records),
        "units": records,
        "support_state_effect": "none",
        "release_effect": "none",
        "non_claims": [
            "This maintained draft is not a major-version release or a generated excerpt of the live technical chapters.",
            "A routed owner does not transfer claim, proof, source, evidence, or authority ownership to the Human Reader unit.",
            "Word-count or render completion is not editorial approval, evidence, safety, readiness, AGI, or ASI.",
            "EPUB, PDF, DOCX, audio, and full release work remain deferred until content freeze.",
        ],
    }
    outputs[MANIFEST] = json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
    return manifest, outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    manifest, outputs = build()
    if args.write:
        CHAPTERS.mkdir(parents=True, exist_ok=True)
        GENERATED.mkdir(parents=True, exist_ok=True)
        for path, text in outputs.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
        print(
            f"Wrote Human Reader current: {manifest['started_unit_count']}/26 started, "
            f"{manifest['visible_word_count']} visible words."
        )
        return
    stale = [path.relative_to(ROOT).as_posix() for path, text in outputs.items() if not path.is_file() or path.read_text(encoding="utf-8") != text]
    if stale:
        raise SystemExit("Human Reader current derivatives are stale: " + ", ".join(stale))
    print(
        f"Human Reader current is synchronized: {manifest['started_unit_count']}/26 started, "
        f"{manifest['visible_word_count']} visible words."
    )


if __name__ == "__main__":
    main()
