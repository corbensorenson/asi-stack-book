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
FENCED_DIV_OPEN_RE = re.compile(r"^(:{3,})\s+\{([^}]*)\}\s*$")
FENCED_DIV_CLOSE_RE = re.compile(r"^(:{3,})\s*$")
AI_ONLY_CLASS = "asi-ai-only"
HUMAN_ONLY_CLASS = "asi-human-only"
HUMAN_READING_PATH_HEADING = "## Human Reading Path"
CORE_CLAIM_MARKER_RE = re.compile(
    r"^\[(?P<chapter_id>[A-Za-z0-9_-]+)\.core,\s*"
    r"label:\s*(?P<label>[^,\]]+),\s*"
    r"support:\s*(?P<support>[^\]]+)\]\s+",
    re.MULTILINE,
)
SUPPORT_BOILERPLATE_RE = re.compile(
    r"The claim remains at `argument` support\.|"
    r"The current support state is `argument`\.|"
    r"The current support state is `argument`, so the claim should be read as a design rationale unless a later evidence bundle promotes it\."
)
HUMAN_ARGUMENT_BOUNDARY = "Evidence boundary: architectural argument."


def load_json(path: Path) -> object:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def load_release_profiles() -> dict:
    data = load_json(PROFILES_PATH)
    if not isinstance(data, dict):
        raise TypeError("editions/release_profiles.json must contain an object")
    return data


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
    preserved_block_fence: int | None = None

    for line in lines:
        if preserved_block_fence is not None:
            output.append(line)
            close_match = FENCED_DIV_CLOSE_RE.match(line)
            if close_match and len(close_match.group(1)) >= preserved_block_fence:
                preserved_block_fence = None
            continue

        open_match = FENCED_DIV_OPEN_RE.match(line)
        if skip_level is not None and open_match:
            classes = fenced_div_classes(open_match.group(2))
            if HUMAN_ONLY_CLASS in classes:
                preserved_block_fence = len(open_match.group(1))
                output.append(line)
                continue

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


def fenced_div_classes(attributes: str) -> set[str]:
    return {match.group(1) for match in re.finditer(r"\.([A-Za-z0-9_-]+)", attributes)}


def apply_reader_view_blocks(text: str) -> tuple[str, dict[str, int]]:
    """Remove live-AI-only blocks and unwrap human-only blocks for reader source.

    The live HTML toggle can use fenced divs such as `::: {.asi-human-only}` and
    `::: {.asi-ai-only}` for future chapter-specific reader adaptations. Reader
    releases should keep the human-only prose without carrying live CSS classes,
    and they should drop AI/research-only prose entirely.
    """

    output: list[str] = []
    stack: list[tuple[int, str]] = []
    counts = {"ai_only_blocks_removed": 0, "human_only_blocks_unwrapped": 0}

    def parent_is_stripped() -> bool:
        return any(action == "strip" for _, action in stack)

    for line in text.splitlines():
        open_match = FENCED_DIV_OPEN_RE.match(line)
        if open_match:
            classes = fenced_div_classes(open_match.group(2))
            if AI_ONLY_CLASS in classes:
                action = "strip"
                counts["ai_only_blocks_removed"] += 1
            elif HUMAN_ONLY_CLASS in classes:
                action = "unwrap"
                counts["human_only_blocks_unwrapped"] += 1
            else:
                action = "keep"
            suppress_open = action in {"strip", "unwrap"} or parent_is_stripped()
            stack.append((len(open_match.group(1)), action))
            if not suppress_open:
                output.append(line)
            continue

        close_match = FENCED_DIV_CLOSE_RE.match(line)
        if close_match and stack:
            _, action = stack.pop()
            if action == "unwrap" and not parent_is_stripped() and output and output[-1].strip():
                output.append("")
            if action not in {"strip", "unwrap"} and not parent_is_stripped():
                output.append(line)
            continue

        if stack and stack[-1][1] == "unwrap" and line.strip() == HUMAN_READING_PATH_HEADING:
            continue

        if not parent_is_stripped():
            output.append(line)

    return "\n".join(output).strip() + "\n", counts


def strip_core_claim_markers(text: str) -> tuple[str, int]:
    cleaned, count = CORE_CLAIM_MARKER_RE.subn("", text)
    return cleaned, count


def humanize_support_boilerplate(text: str) -> tuple[str, int]:
    cleaned, count = SUPPORT_BOILERPLATE_RE.subn(HUMAN_ARGUMENT_BOUNDARY, text)
    return cleaned, count


def find_profile(profile_id: str) -> dict:
    data = load_release_profiles()
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


def clean_file(
    src: Path,
    dst: Path,
    strip_headings: set[tuple[int, str]],
    chapter_title: str | None = None,
) -> dict[str, int]:
    text = src.read_text(encoding="utf-8")
    cleaned, removed = strip_sections(text, strip_headings)
    cleaned, view_block_counts = apply_reader_view_blocks(cleaned)
    cleaned, marker_count = strip_core_claim_markers(cleaned)
    cleaned, support_boilerplate_count = humanize_support_boilerplate(cleaned)
    if chapter_title:
        cleaned = f"# {chapter_title}\n\n{cleaned.lstrip()}"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(cleaned, encoding="utf-8")
    removed.update({key: count for key, count in view_block_counts.items() if count})
    if marker_count:
        removed["core_claim_markers_removed"] = marker_count
    if support_boilerplate_count:
        removed["support_boilerplate_humanized"] = support_boilerplate_count
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


def write_reader_checklist(
    output_dir: Path,
    profile: dict,
    reader_policy: dict,
    spine_policy: dict,
    companion_policy: dict,
    bundle_policy: dict,
    summary: dict[str, object],
) -> str:
    checklist_path = str(reader_policy.get("generated_checklist_path", "READER_RELEASE_CHECKLIST.md"))
    companion_path = str(companion_policy.get("reader_companion_path", "companion_notes.md"))
    quality_checks = reader_policy.get("ebook_quality_checks", [])
    human_quality_floor = reader_policy.get("human_reader_quality_floor", [])
    downstream_formats = reader_policy.get("optional_downstream_formats", [])
    release_gate = profile.get("release_gate", [])
    spine_script = str(spine_policy.get("script", "scripts/validate_reader_spine.py"))
    min_handoff_words = spine_policy.get("minimum_handoff_word_count", "unconfigured")

    lines = [
        "# Reader Release Checklist",
        "",
        "Status: generated checklist for major-version reader review.",
        "",
        "This workspace is derived from the living book. It is not the canonical source and it is not a published reader edition until review, renders, and release records say so.",
        "",
        "## Generated Source",
        "",
        f"- Profile: `{profile.get('id', 'reader_release')}`",
        f"- Chapters: {summary['chapters']}",
        f"- Files: {summary['files']}",
        f"- Target formats: {', '.join(summary['formats'])}",
        f"- Live-only sections removed: {sum(summary['removed_sections'].values())}",
        f"- AI-only fenced blocks removed: {summary.get('ai_only_blocks_removed', 0)}",
        f"- Human-only fenced blocks unwrapped: {summary.get('human_only_blocks_unwrapped', 0)}",
        f"- Reader-spine validator: `{spine_script}`",
        f"- Handoff word floor: {min_handoff_words}",
        "",
        "## Required Gate",
        "",
    ]
    for item in release_gate:
        lines.append(f"- [ ] {item}")

    lines.extend([
        "",
        "## Reader Review",
        "",
        "- [ ] Read the generated manuscript for chapter-to-chapter continuity.",
        "- [ ] Confirm every generated chapter has exactly one `Handoff` section after `Summary`.",
        "- [ ] Confirm non-final Handoffs name the next manifest chapter title and the final Handoff closes the book-level arc.",
        "- [ ] Check that meaning-critical caveats and support-state limits remain in ordinary prose.",
        "- [ ] Check that stripped source crosswalks, proof hooks, and guardrails did not leave broken transitions.",
        "- [ ] Check that glossary, Corben corpus/local-project appendix, and separate external-literature appendix are sufficient for interested human readers.",
        f"- [ ] Review `{companion_path}` for omitted dense material and e-reader/audio companion needs.",
        "- [ ] Record residuals and non-claims in an edition release record.",
        "",
        "## E-Reader And Document Checks",
        "",
    ])
    for item in quality_checks:
        lines.append(f"- [ ] {item}")

    if human_quality_floor:
        lines.extend(["", "## Human Reader Quality Floor", ""])
        for item in human_quality_floor:
            lines.append(f"- [ ] {item}")

    if bundle_policy:
        lines.extend([
            "",
            "## Major-Version Human Bundle",
            "",
            f"- Canonical reader profile: `{bundle_policy.get('canonical_reader_profile', 'reader_release')}`",
            "- [ ] Confirm this reader workspace was generated from the tagged live-book state.",
            "- [ ] Confirm any optional e-reader conversion starts from the reviewed reader source or reviewed EPUB.",
            "- [ ] Keep audio packaging in a separate audio-release record unless that package has its own reviewed script and artifacts.",
            "",
            "### Human Quality Gates",
            "",
        ])
        for item in bundle_policy.get("human_quality_gates", []):
            lines.append(f"- [ ] {item}")

    if downstream_formats:
        lines.extend(["", "## Optional Downstream Formats", ""])
        for item in downstream_formats:
            lines.append(f"- [ ] {item}")

    lines.extend([
        "",
        "## Artifact Status Discipline",
        "",
        "- [ ] Treat every listed format as `target_not_rendered` until its specific render command succeeds.",
        "- [ ] Record EPUB, PDF, DOCX, HTML, AZW3, MOBI, Markdown, or plain-text artifacts only in an edition release record that names the actual path or URI.",
        "- [ ] Keep audio and audio-embedded EPUB work out of the reader release unless a separate audio release record covers it.",
    ])

    lines.extend([
        "",
        "## Non-Claims",
        "",
        "- This checklist does not claim EPUB, PDF, DOCX, AZW3, MOBI, or audio artifacts exist.",
        "- This checklist does not promote any live-book claim support state.",
        "- The live book remains the source of truth after any reader derivative is produced.",
        "",
    ])
    (output_dir / checklist_path).write_text("\n".join(lines), encoding="utf-8")
    return checklist_path


def write_reader_companion_notes(
    output_dir: Path,
    companion_policy: dict,
    summary: dict[str, object],
) -> str:
    companion_path = str(companion_policy.get("reader_companion_path", "companion_notes.md"))
    removed_sections = summary.get("removed_sections", {})
    if not isinstance(removed_sections, dict):
        removed_sections = {}

    lines = [
        "# Reader Companion Notes",
        "",
        "Status: generated starter notes for major-version human-reader review.",
        "",
        "These notes are derived from the living book reader-edition generator. They are review aids for e-reader, document, and future audio packaging; they are not the canonical evidence ledger and they do not claim any artifact has been rendered.",
        "",
        "## Purpose",
        "",
        str(companion_policy.get("purpose", "Keep companion decisions explicit for human-reader releases.")),
        "",
        "## Removed Live-Only Sections",
        "",
    ]
    if removed_sections:
        lines.extend(["| Heading | Removed count |", "|---|---:|"])
        for heading, count in sorted(removed_sections.items()):
            lines.append(f"| `{heading}` | {count} |")
    else:
        lines.append("No live-only sections were removed by the generator.")

    lines.extend([
        "",
        "## Companion Topics To Review",
        "",
    ])
    for item in companion_policy.get("required_topics", []):
        lines.append(f"- [ ] {item}")

    lines.extend([
        "",
        "## Review Requirements",
        "",
    ])
    for item in companion_policy.get("review_requirements", []):
        lines.append(f"- [ ] {item}")

    lines.extend([
        "",
        "## Artifact Notes",
        "",
        "- [ ] Confirm EPUB, PDF, DOCX, HTML, AZW3, MOBI, Markdown, or plain-text artifacts are named only after the corresponding render or conversion succeeds.",
        "- [ ] Confirm audio companion decisions are moved into the audio workspace before MP3, M4B, or audio-embedded EPUB work begins.",
        "- [ ] Confirm meaning-critical caveats remain in the reader manuscript, not only in these notes.",
        "",
        "## Non-Claims",
        "",
    ])
    for item in companion_policy.get("non_claims", []):
        lines.append(f"- {item}")
    lines.append("")

    (output_dir / companion_path).write_text("\n".join(lines), encoding="utf-8")
    return companion_path


def write_reader_manifest(
    output_dir: Path,
    summary: dict[str, object],
    profile: dict,
    reader_policy: dict,
    spine_policy: dict,
    companion_policy: dict,
    bundle_policy: dict,
) -> None:
    manifest = {
        "schema_version": "0.1",
        "source_profile": profile.get("id", "reader_release"),
        "output_dir": summary["output_dir"],
        "formats": summary["formats"],
        "target_artifact_status": {
            str(fmt): "target_not_rendered"
            for fmt in summary["formats"]
        },
        "downstream_artifact_status": {
            str(fmt): "target_not_generated"
            for fmt in reader_policy.get("optional_downstream_formats", [])
        },
        "chapters": summary["chapters"],
        "files": summary["files"],
        "content_layer_policy": profile.get("content_layer_policy", {}),
        "stripped_heading_policy": profile.get("strip_headings", []),
        "removed_sections": summary["removed_sections"],
        "ai_only_blocks_removed": summary.get("ai_only_blocks_removed", 0),
        "human_only_blocks_unwrapped": summary.get("human_only_blocks_unwrapped", 0),
        "reader_review_required": profile.get("reader_review_required", True),
        "reader_review_checklist": summary.get("review_checklist", "READER_RELEASE_CHECKLIST.md"),
        "reader_spine_validation": spine_policy,
        "handoff_continuity_review": {
            "required": True,
            "required_section": "Handoff",
            "required_position": "after Summary",
            "non_final_rule": "Name the next manifest chapter title.",
            "final_rule": "Close the book-level arc.",
            "artifact_status": "review_required"
        },
        "companion_notes": summary.get(
            "companion_notes",
            companion_policy.get("reader_companion_path", "companion_notes.md"),
        ),
        "companion_material_policy": companion_policy,
        "human_consumption_bundle_policy": bundle_policy,
        "ebook_quality_checks": reader_policy.get("ebook_quality_checks", []),
        "human_reader_quality_floor": reader_policy.get("human_reader_quality_floor", []),
        "optional_downstream_formats": reader_policy.get("optional_downstream_formats", []),
        "review_status": "review_required",
        "audio_dependency": "Run scripts/build_audio_script.py only after this reader manuscript is reviewed for human continuity.",
        "non_claims": [
            "This generated source tree is not the canonical living book.",
            "Listed formats are targets, not rendered artifacts.",
            "EPUB, PDF, DOCX, HTML, AZW3, MOBI, Markdown, and plain-text outputs must not be claimed until the exact render or conversion succeeds and a release record says so.",
            "Audio and audio-embedded EPUB artifacts require a separate reviewed audio release path.",
            "A reader-edition draft still requires continuity, typography, figure, and appendix review before publication."
        ]
    }
    (output_dir / "reader_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )


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
    profile_data = load_release_profiles()
    reader_policy = profile_data.get("reader_manuscript_policy", {})
    if not isinstance(reader_policy, dict):
        raise TypeError("reader_manuscript_policy must be an object")
    companion_policy = profile_data.get("companion_material_policy", {})
    if not isinstance(companion_policy, dict):
        raise TypeError("companion_material_policy must be an object")
    spine_policy = profile_data.get("reader_spine_validation", {})
    if not isinstance(spine_policy, dict):
        raise TypeError("reader_spine_validation must be an object")
    bundle_policy = profile_data.get("human_consumption_bundle_policy", {})
    if not isinstance(bundle_policy, dict):
        raise TypeError("human_consumption_bundle_policy must be an object")
    profile = find_profile(profile_id)
    strip_headings = profile_strip_headings(profile)

    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    copy_assets(output_dir)
    write_reader_index(output_dir, structure)

    removed_totals: dict[str, int] = {}
    ai_only_blocks_removed = 0
    human_only_blocks_unwrapped = 0
    copied_files = 1
    for front_file in structure.get("front_matter", []):
        if front_file == "index.qmd":
            continue
        src = ROOT / front_file
        if src.exists():
            removed = clean_file(src, output_dir / front_file, strip_headings)
            copied_files += 1
            for key, count in removed.items():
                if key == "ai_only_blocks_removed":
                    ai_only_blocks_removed += count
                elif key == "human_only_blocks_unwrapped":
                    human_only_blocks_unwrapped += count
                else:
                    removed_totals[key] = removed_totals.get(key, 0) + count

    chapter_count = 0
    for part in flatten_parts(structure):
        for chapter in part.get("chapters", []):
            src = ROOT / chapter["file"]
            removed = clean_file(src, output_dir / chapter["file"], strip_headings, str(chapter["title"]))
            copied_files += 1
            chapter_count += 1
            for key, count in removed.items():
                if key == "ai_only_blocks_removed":
                    ai_only_blocks_removed += count
                elif key == "human_only_blocks_unwrapped":
                    human_only_blocks_unwrapped += count
                else:
                    removed_totals[key] = removed_totals.get(key, 0) + count

    for appendix in profile.get("include_appendices", []):
        src = ROOT / appendix
        if src.exists():
            removed = clean_file(src, output_dir / appendix, strip_headings)
            copied_files += 1
            for key, count in removed.items():
                if key == "ai_only_blocks_removed":
                    ai_only_blocks_removed += count
                elif key == "human_only_blocks_unwrapped":
                    human_only_blocks_unwrapped += count
                else:
                    removed_totals[key] = removed_totals.get(key, 0) + count

    write_quarto(output_dir, structure, profile)
    summary = {
        "output_dir": str(output_dir),
        "profile": profile_id,
        "chapters": chapter_count,
        "files": copied_files,
        "removed_sections": removed_totals,
        "ai_only_blocks_removed": ai_only_blocks_removed,
        "human_only_blocks_unwrapped": human_only_blocks_unwrapped,
        "formats": profile.get("publication_formats", []),
    }
    checklist_path = write_reader_checklist(
        output_dir,
        profile,
        reader_policy,
        spine_policy,
        companion_policy,
        bundle_policy,
        summary,
    )
    companion_path = write_reader_companion_notes(output_dir, companion_policy, summary)
    summary["review_checklist"] = checklist_path
    summary["companion_notes"] = companion_path
    write_reader_manifest(
        output_dir,
        summary,
        profile,
        reader_policy,
        spine_policy,
        companion_policy,
        bundle_policy,
    )
    return summary


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


def scan_for_view_block_markers(output_dir: Path) -> list[str]:
    violations: list[str] = []
    for path in output_dir.rglob("*.qmd"):
        text = path.read_text(encoding="utf-8")
        for marker in (f".{AI_ONLY_CLASS}", f".{HUMAN_ONLY_CLASS}"):
            if marker in text:
                violations.append(f"{path.relative_to(output_dir)}: retained reader-view marker {marker}")
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
            violations.extend(scan_for_view_block_markers(output_dir))
            if violations:
                print("Reader edition still contains stripped headings or live view markers:")
                for violation in violations:
                    print(f" - {violation}")
                raise SystemExit(1)
            if not (output_dir / "READER_RELEASE_CHECKLIST.md").exists():
                raise SystemExit("Reader edition check failed: missing READER_RELEASE_CHECKLIST.md.")
            checklist_text = (output_dir / "READER_RELEASE_CHECKLIST.md").read_text(encoding="utf-8")
            if "Handoff" not in checklist_text or "next manifest chapter title" not in checklist_text:
                raise SystemExit("Reader edition check failed: checklist missing Handoff continuity review.")
            profile_data = load_release_profiles()
            companion_policy = profile_data.get("companion_material_policy", {})
            companion_path = str(
                companion_policy.get("reader_companion_path", "companion_notes.md")
                if isinstance(companion_policy, dict)
                else "companion_notes.md"
            )
            if not (output_dir / companion_path).exists():
                raise SystemExit(f"Reader edition check failed: missing {companion_path}.")
            manifest_path = output_dir / "reader_manifest.json"
            if not manifest_path.exists():
                raise SystemExit("Reader edition check failed: missing reader_manifest.json.")
            manifest = load_json(manifest_path)
            if not isinstance(manifest, dict):
                raise SystemExit("Reader edition check failed: reader_manifest.json must contain an object.")
            if not isinstance(manifest.get("reader_spine_validation"), dict):
                raise SystemExit("Reader edition check failed: manifest missing reader_spine_validation.")
            handoff_review = manifest.get("handoff_continuity_review")
            if not isinstance(handoff_review, dict) or handoff_review.get("required") is not True:
                raise SystemExit("Reader edition check failed: manifest missing required Handoff review.")
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
