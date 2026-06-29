#!/usr/bin/env python3
"""Generate a derived human-reader edition draft from the living book source.

The generated files are written under build/ by default and are ignored by git.
This script does not render EPUB, PDF, DOCX, or audio artifacts. It only creates
the cleaned Quarto source needed for those later release steps.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
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
READER_SCAFFOLD_TERM_REPLACEMENTS = [
    (re.compile(r"\bCodex workflows\b", re.IGNORECASE), "automation workflows"),
    (re.compile(r"\bCodex workflow\b", re.IGNORECASE), "automation workflow"),
    (re.compile(r"\bsource crosswalks\b", re.IGNORECASE), "source maps"),
    (re.compile(r"\bsource crosswalk\b", re.IGNORECASE), "source map"),
    (re.compile(r"\bconnector-only/source-note mapped\b", re.IGNORECASE), "connector-only review context"),
    (re.compile(r"\bconnector/source-note mapped\b", re.IGNORECASE), "connector review context"),
    (re.compile(r"\bconnector/source-note context\b", re.IGNORECASE), "connector review context"),
    (re.compile(r"\bconnector/source-note\b", re.IGNORECASE), "connector review"),
    (re.compile(r"\bsource-noted\b", re.IGNORECASE), "source-reviewed"),
    (re.compile(r"\bsource-note-only\b", re.IGNORECASE), "source-review-only"),
    (re.compile(r"\bsource-note-available\b", re.IGNORECASE), "source-review-available"),
    (re.compile(r"\bsource-note-", re.IGNORECASE), "source-review-"),
    (re.compile(r"\bsource-note\b", re.IGNORECASE), "source review"),
]
CORE_CLAIM_MARKER_RE = re.compile(
    r"^\[(?P<chapter_id>[A-Za-z0-9_-]+)\.core,\s*"
    r"label:\s*(?P<label>[^,\]]+),\s*"
    r"support:\s*(?P<support>[^\]]+)\]\s+",
    re.MULTILINE,
)
CORE_CLAIM_MARKER_LINE_RE = re.compile(
    r"^\[(?P<chapter_id>[A-Za-z0-9_-]+)\.core,\s*"
    r"label:\s*(?P<label>[^,\]]+),\s*"
    r"support:\s*(?P<support>[^\]]+)\]\s*(?P<claim_text>.*?)\s*$",
    re.MULTILINE,
)
SUPPORT_BOILERPLATE_RE = re.compile(
    r"The claim remains at `argument` support\.|"
    r"The current support state is `argument`\.|"
    r"The current support state is `argument`, so the claim should be read as a design rationale unless a later evidence bundle promotes it\."
)
HUMAN_ARGUMENT_BOUNDARY = "Evidence boundary: architectural argument."
NON_HEADING_TRANSFORM_KEYS = {
    "core_claim_markers_removed",
    "support_boilerplate_humanized",
    "reader_scaffold_terms_humanized",
    "reader_source_appendix_tables_converted",
}
WORD_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9'_-]*")
OVERLAY_ACTIONS = {
    "replace_section",
    "prepend_to_section",
    "append_to_section",
    "insert_before_section",
    "insert_after_section",
}
OVERLAY_STATUSES = {"active", "planned", "retired"}
DEFAULT_DELTA_REPORT = "reader_delta_report.md"
DELTA_EXCERPT_CHARS = 900


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


def reader_support_boundary(support: str) -> str:
    normalized = support.strip().lower()
    if normalized == "argument":
        return "evidence boundary: architectural argument"
    return f"support remains `{support.strip()}`"


def append_parenthetical_boundary(claim_text: str, support: str) -> str:
    claim = claim_text.strip()
    if not claim:
        return f"({reader_support_boundary(support)})."
    boundary = reader_support_boundary(support)
    if claim[-1:] in ".?!":
        return f"{claim[:-1]} ({boundary}){claim[-1]}"
    return f"{claim} ({boundary})."


def strip_core_claim_markers(text: str) -> tuple[str, int]:
    def replacement(match: re.Match[str]) -> str:
        return append_parenthetical_boundary(match.group("claim_text"), match.group("support"))

    cleaned, count = CORE_CLAIM_MARKER_LINE_RE.subn(replacement, text)
    return cleaned, count


def humanize_support_boilerplate(text: str) -> tuple[str, int]:
    cleaned, count = SUPPORT_BOILERPLATE_RE.subn("", text)
    cleaned = re.sub(r"(?m)^[ \t]+", "", cleaned)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned, count


def normalize_reader_spacing(text: str) -> str:
    return re.sub(r"(?<=[.!?]) {2,}(?=[A-Z0-9`])", " ", text)


def split_markdown_table_row(line: str) -> list[str]:
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        return []
    return [cell.strip() for cell in stripped.strip("|").split("|")]


def replace_markdown_table_with_cards(text: str, header: str, columns: list[str], intro: str) -> tuple[str, int]:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.strip() != header:
            continue
        separator_index = index + 1
        if separator_index >= len(lines) or not lines[separator_index].lstrip().startswith("|---"):
            return text, 0
        end = separator_index + 1
        while end < len(lines) and lines[end].strip().startswith("|"):
            end += 1
        row_lines = lines[separator_index + 1 : end]
        card_lines = ["## Reader Source List", "", intro.strip(), ""]
        converted = 0
        for row_line in row_lines:
            cells = split_markdown_table_row(row_line)
            if len(cells) != len(columns):
                continue
            record = dict(zip(columns, cells))
            title = record.get("Title", "").strip() or record.get("Source ID", "").strip()
            card_lines.extend([f"### {title}", ""])
            for column in columns:
                if column == "Title":
                    continue
                value = record.get(column, "").strip()
                if value:
                    card_lines.append(f"- {column}: {value}")
            card_lines.append("")
            converted += 1
        if not converted:
            return text, 0
        while card_lines and not card_lines[-1]:
            card_lines.pop()
        replacement = lines[:index] + card_lines + lines[end:]
        return "\n".join(replacement).strip() + "\n", 1
    return text, 0


def reader_source_appendix_intro(kind: str) -> str:
    if kind == "corben":
        return (
            "The live book keeps this corpus as a wide audit table. The reader "
            "edition uses source cards so long source IDs, chapter assignments, "
            "and citation status notes wrap cleanly in PDF and e-reader formats."
        )
    return (
        "The live book keeps these external records as a wide audit table. The "
        "reader edition uses source cards so long source IDs, citations, chapter "
        "assignments, and notes wrap cleanly in PDF and e-reader formats."
    )


def transform_reader_source_appendix(path: Path, relative_path: str) -> int:
    text = path.read_text(encoding="utf-8")
    if relative_path == "appendices/G_corben_source_corpus.qmd":
        transformed, count = replace_markdown_table_with_cards(
            text,
            "| Source ID | Title | Priority | Layer | Link | Current use | Bibliographic status |",
            ["Source ID", "Title", "Priority", "Layer", "Link", "Current use", "Bibliographic status"],
            reader_source_appendix_intro("corben"),
        )
    elif relative_path == "appendices/H_external_sources.qmd":
        transformed, count = replace_markdown_table_with_cards(
            text,
            "| Source ID | Title | Citation or primary record | Layer | Current use | Source review state | Notes |",
            ["Source ID", "Title", "Citation or primary record", "Layer", "Current use", "Source review state", "Notes"],
            reader_source_appendix_intro("external"),
        )
    else:
        return 0
    if count:
        path.write_text(transformed, encoding="utf-8")
    return count


def humanize_reader_scaffold_terms(text: str) -> tuple[str, int]:
    count = 0
    cleaned = text
    for pattern, replacement in READER_SCAFFOLD_TERM_REPLACEMENTS:
        def preserve_initial_case(match: re.Match[str]) -> str:
            if match.group(0)[:1].isupper():
                return replacement[:1].upper() + replacement[1:]
            return replacement

        cleaned, replacements = pattern.subn(preserve_initial_case, cleaned)
        count += replacements
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


def normalized_relative_path(value: object, owner: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{owner}: path must be a non-empty string.")
    path = Path(value.strip())
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"{owner}: path must be a safe repository-relative path: {value!r}.")
    return path.as_posix()


def operation_content(operation: dict) -> str:
    if isinstance(operation.get("content"), str):
        return str(operation["content"]).strip()
    lines = operation.get("content_lines")
    if isinstance(lines, list) and all(isinstance(line, str) for line in lines):
        return "\n".join(lines).strip()
    return ""


def text_digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def excerpt_lines(lines: list[str], limit: int = DELTA_EXCERPT_CHARS) -> str:
    text = "\n".join(line.rstrip() for line in lines).strip()
    text = re.sub(r"\n{3,}", "\n\n", text)
    if len(text) <= limit:
        return text
    return text[:limit].rstrip() + "\n..."


def excerpt_lines_tail(lines: list[str], limit: int = DELTA_EXCERPT_CHARS) -> str:
    text = "\n".join(line.rstrip() for line in lines).strip()
    text = re.sub(r"\n{3,}", "\n\n", text)
    if len(text) <= limit:
        return text
    return "...\n" + text[-limit:].lstrip()


def normalize_overlay_operation(
    operation: object,
    source_path: str,
    index: int,
    default_target_file: str | None = None,
) -> dict[str, object]:
    if not isinstance(operation, dict):
        raise TypeError(f"{source_path}: operations[{index}] must be an object.")

    operation_id = operation.get("id")
    if not isinstance(operation_id, str) or not operation_id.strip():
        raise ValueError(f"{source_path}: operations[{index}] missing non-empty id.")

    status = str(operation.get("status", "active")).strip().lower()
    if status not in OVERLAY_STATUSES:
        raise ValueError(
            f"{source_path}: operation {operation_id!r} status must be one of "
            f"{sorted(OVERLAY_STATUSES)}."
        )

    action = operation.get("action")
    if not isinstance(action, str) or action not in OVERLAY_ACTIONS:
        raise ValueError(
            f"{source_path}: operation {operation_id!r} action must be one of "
            f"{sorted(OVERLAY_ACTIONS)}."
        )

    target_file_value = operation.get("target_file", default_target_file)
    target_file = normalized_relative_path(target_file_value, f"{source_path}:{operation_id}.target_file")
    if not target_file.endswith(".qmd"):
        raise ValueError(f"{source_path}: operation {operation_id!r} target_file must end with .qmd.")

    section = operation.get("section")
    if not isinstance(section, dict):
        raise ValueError(f"{source_path}: operation {operation_id!r} section must be an object.")
    level = section.get("level")
    title = section.get("title")
    if not isinstance(level, int) or level < 1 or level > 6:
        raise ValueError(f"{source_path}: operation {operation_id!r} section.level must be 1..6.")
    if not isinstance(title, str) or not title.strip():
        raise ValueError(f"{source_path}: operation {operation_id!r} section.title must be non-empty.")
    aliases_value = section.get("aliases", [])
    if aliases_value is None:
        aliases_value = []
    if not isinstance(aliases_value, list) or not all(isinstance(alias, str) for alias in aliases_value):
        raise ValueError(f"{source_path}: operation {operation_id!r} section.aliases must be a list of strings.")
    aliases = [alias.strip() for alias in aliases_value if alias.strip()]

    content = operation_content(operation)
    if status == "active" and not content:
        raise ValueError(f"{source_path}: operation {operation_id!r} active operations need content.")

    rationale = operation.get("rationale", "")
    if rationale is not None and not isinstance(rationale, str):
        raise ValueError(f"{source_path}: operation {operation_id!r} rationale must be a string.")

    return {
        "id": operation_id.strip(),
        "status": status,
        "action": action,
        "target_file": target_file,
        "section": {"level": level, "title": title.strip(), "aliases": aliases},
        "content": content,
        "rationale": str(rationale).strip(),
        "source_path": source_path,
    }


def load_overlay_operations_from_file(path: Path, manifest_dir: Path) -> list[dict[str, object]]:
    data = load_json(path)
    if not isinstance(data, dict):
        raise TypeError(f"{path}: overlay operation file must contain an object.")
    if data.get("schema_version") != "0.1":
        raise ValueError(f"{path}: schema_version must be 0.1.")
    default_target_file = data.get("target_file")
    if default_target_file is not None:
        default_target_file = normalized_relative_path(default_target_file, f"{path}.target_file")
    operations = data.get("operations", [])
    if not isinstance(operations, list):
        raise TypeError(f"{path}: operations must be a list.")
    source_path = path.relative_to(ROOT).as_posix()
    return [
        normalize_overlay_operation(operation, source_path, index, default_target_file)
        for index, operation in enumerate(operations)
    ]


def load_reader_overlay_context(profile: dict) -> dict[str, object]:
    manifest_ref = profile.get("reader_overlay_manifest")
    if manifest_ref is None:
        return {
            "configured": False,
            "manifest_path": None,
            "manifest": {},
            "operations": [],
            "applied_records": [],
            "skipped_records": [],
            "applied_ids": set(),
        }

    manifest_rel = normalized_relative_path(manifest_ref, "reader_overlay_manifest")
    manifest_path = ROOT / manifest_rel
    if not manifest_path.exists():
        raise FileNotFoundError(f"Reader overlay manifest not found: {manifest_rel}")

    manifest = load_json(manifest_path)
    if not isinstance(manifest, dict):
        raise TypeError(f"{manifest_rel}: reader overlay manifest must contain an object.")
    if manifest.get("schema_version") != "0.1":
        raise ValueError(f"{manifest_rel}: schema_version must be 0.1.")
    for key in ("id", "label", "purpose"):
        value = manifest.get(key)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{manifest_rel}: {key} must be a non-empty string.")
    status = manifest.get("status")
    if status not in ("active", "planned", "retired"):
        raise ValueError(f"{manifest_rel}: status must be active, planned, or retired.")
    if manifest.get("applies_to_profile") not in (None, profile.get("id")):
        raise ValueError(
            f"{manifest_rel}: applies_to_profile must match {profile.get('id')!r} when present."
        )

    operations: list[dict[str, object]] = []
    manifest_operations = manifest.get("operations", [])
    if not isinstance(manifest_operations, list):
        raise TypeError(f"{manifest_rel}: operations must be a list.")
    operations.extend(
        normalize_overlay_operation(operation, manifest_rel, index)
        for index, operation in enumerate(manifest_operations)
    )

    manifest_dir = manifest_path.parent
    operation_globs = manifest.get("operation_globs", [])
    if not isinstance(operation_globs, list) or not all(isinstance(pattern, str) for pattern in operation_globs):
        raise TypeError(f"{manifest_rel}: operation_globs must be a list of strings.")
    operation_files: list[str] = []
    for pattern in operation_globs:
        normalized_pattern = normalized_relative_path(pattern, f"{manifest_rel}.operation_globs")
        for path in sorted(manifest_dir.glob(normalized_pattern)):
            if path.is_file():
                operation_files.append(path.relative_to(ROOT).as_posix())
                operations.extend(load_overlay_operations_from_file(path, manifest_dir))

    ids: set[str] = set()
    skipped_records: list[dict[str, object]] = []
    for operation in operations:
        operation_id = str(operation["id"])
        if operation_id in ids:
            raise ValueError(f"{manifest_rel}: duplicate reader overlay operation id: {operation_id}")
        ids.add(operation_id)
        if operation["status"] != "active":
            skipped_records.append({
                "id": operation_id,
                "status": operation["status"],
                "target_file": operation["target_file"],
                "action": operation["action"],
                "section": operation["section"],
                "source_path": operation["source_path"],
            })

    return {
        "configured": True,
        "manifest_path": manifest_rel,
        "manifest": manifest,
        "operation_files": operation_files,
        "operations": operations,
        "applied_records": [],
        "skipped_records": skipped_records,
        "applied_ids": set(),
    }


def markdown_table_cell(value: object, limit: int = 220) -> str:
    text = re.sub(r"\s+", " ", str(value).strip())
    if len(text) > limit:
        text = text[: limit - 3].rstrip() + "..."
    return text.replace("|", "\\|")


def load_companion_routing(companion_policy: dict) -> dict[str, object]:
    routing_ref = companion_policy.get("routing_manifest")
    if routing_ref is None:
        return {"configured": False, "manifest_path": None, "records": []}

    routing_rel = normalized_relative_path(routing_ref, "companion_material_policy.routing_manifest")
    routing_path = ROOT / routing_rel
    if not routing_path.exists():
        raise FileNotFoundError(f"Companion-note routing manifest not found: {routing_rel}")

    data = load_json(routing_path)
    if not isinstance(data, dict):
        raise TypeError(f"{routing_rel}: companion-note routing manifest must contain an object.")
    if data.get("schema_version") != "0.1":
        raise ValueError(f"{routing_rel}: schema_version must be 0.1.")
    records = data.get("records", [])
    if not isinstance(records, list):
        raise TypeError(f"{routing_rel}: records must be a list.")

    return {
        "configured": True,
        "manifest_path": routing_rel,
        "status": data.get("status"),
        "purpose": data.get("purpose", ""),
        "records": records,
        "non_claims": data.get("non_claims", []),
    }


def heading_spans(text: str) -> list[dict[str, object]]:
    lines = text.splitlines()
    spans: list[dict[str, object]] = []
    for index, line in enumerate(lines):
        match = HEADING_RE.match(line)
        if not match:
            continue
        level = len(match.group(1))
        title = normalize_heading_title(match.group(2))
        end = len(lines)
        for next_index in range(index + 1, len(lines)):
            next_match = HEADING_RE.match(lines[next_index])
            if next_match and len(next_match.group(1)) <= level:
                end = next_index
                break
        spans.append({"start": index, "body_start": index + 1, "end": end, "level": level, "title": title})
    return spans


def find_section_span(lines: list[str], operation: dict[str, object]) -> dict[str, object]:
    section = operation["section"]
    if not isinstance(section, dict):
        raise TypeError("reader overlay operation section must be an object")
    expected_level = int(section["level"])
    expected_titles = {normalize_heading_title(str(section["title"]))}
    aliases = section.get("aliases", [])
    if isinstance(aliases, list):
        expected_titles.update(normalize_heading_title(str(alias)) for alias in aliases if str(alias).strip())
    matches = [
        span
        for span in heading_spans("\n".join(lines))
        if int(span["level"]) == expected_level and str(span["title"]) in expected_titles
    ]
    if not matches:
        raise ValueError(
            f"{operation['id']}: target section not found in {operation['target_file']}: "
            f"{'#' * expected_level} {section['title']}"
        )
    if len(matches) > 1:
        raise ValueError(
            f"{operation['id']}: target section is ambiguous in {operation['target_file']}: "
            f"{'#' * expected_level} {section['title']}"
        )
    return matches[0]


def content_block_lines(content: str) -> list[str]:
    lines = content.strip().splitlines()
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return [""] + lines + [""]


def apply_reader_overlay_operation(text: str, operation: dict[str, object]) -> tuple[str, dict[str, object]]:
    before_words = len(WORD_RE.findall(text))
    lines = text.splitlines()
    span = find_section_span(lines, operation)
    block = content_block_lines(str(operation["content"]))
    action = str(operation["action"])
    start = int(span["start"])
    body_start = int(span["body_start"])
    end = int(span["end"])
    before_excerpt = excerpt_lines(lines[start:end])

    if action == "replace_section":
        new_lines = lines[:body_start] + block + lines[end:]
    elif action == "prepend_to_section":
        new_lines = lines[:body_start] + block + lines[body_start:]
    elif action == "append_to_section":
        new_lines = lines[:end] + block + lines[end:]
    elif action == "insert_before_section":
        new_lines = lines[:start] + block + lines[start:]
    elif action == "insert_after_section":
        new_lines = lines[:end] + block + lines[end:]
    else:
        raise ValueError(f"Unsupported reader overlay action: {action}")

    cleaned = "\n".join(new_lines).strip() + "\n"
    after_words = len(WORD_RE.findall(cleaned))
    if action in {"replace_section", "prepend_to_section"}:
        after_span = find_section_span(new_lines, operation)
        after_excerpt = excerpt_lines(new_lines[int(after_span["start"]):int(after_span["end"])])
    elif action == "append_to_section":
        after_span = find_section_span(new_lines, operation)
        after_excerpt = excerpt_lines_tail(new_lines[int(after_span["start"]):int(after_span["end"])])
    elif action == "insert_before_section":
        after_excerpt = excerpt_lines(new_lines[start:min(len(new_lines), start + len(block) + (end - start))])
    else:
        after_excerpt = excerpt_lines(new_lines[end:min(len(new_lines), end + len(block))])
    section = operation["section"]
    record = {
        "id": operation["id"],
        "target_file": operation["target_file"],
        "action": operation["action"],
        "section": section,
        "source_path": operation["source_path"],
        "rationale": operation.get("rationale", ""),
        "word_delta": after_words - before_words,
        "target_line_span": {"start": start + 1, "end": end},
        "content_sha256_16": text_digest(str(operation["content"])),
        "content_excerpt": excerpt_lines(str(operation["content"]).splitlines()),
        "before_excerpt": before_excerpt,
        "after_excerpt": after_excerpt,
    }
    return cleaned, record


def apply_reader_overlay_to_file(output_path: Path, relative_path: str, context: dict[str, object]) -> None:
    if not context.get("configured"):
        return
    operations = [
        operation
        for operation in context.get("operations", [])
        if isinstance(operation, dict)
        and operation.get("status") == "active"
        and operation.get("target_file") == relative_path
    ]
    if not operations:
        return

    text = output_path.read_text(encoding="utf-8")
    for operation in operations:
        text, record = apply_reader_overlay_operation(text, operation)
        applied_records = context.get("applied_records")
        if isinstance(applied_records, list):
            applied_records.append(record)
        applied_ids = context.get("applied_ids")
        if isinstance(applied_ids, set):
            applied_ids.add(str(operation["id"]))
    output_path.write_text(text, encoding="utf-8")


def finalize_reader_overlay_context(context: dict[str, object]) -> None:
    if not context.get("configured"):
        return
    applied_ids = context.get("applied_ids")
    if not isinstance(applied_ids, set):
        applied_ids = set()
    unapplied = [
        operation
        for operation in context.get("operations", [])
        if isinstance(operation, dict)
        and operation.get("status") == "active"
        and str(operation.get("id")) not in applied_ids
    ]
    if unapplied:
        lines = [
            f"{operation['id']} -> {operation['target_file']} ({operation['action']})"
            for operation in unapplied
        ]
        raise ValueError("Active reader overlay operations were not applied: " + "; ".join(lines))


def reader_overlay_summary(context: dict[str, object]) -> dict[str, object]:
    applied_records = context.get("applied_records", [])
    skipped_records = context.get("skipped_records", [])
    manifest = context.get("manifest", {})
    if not isinstance(manifest, dict):
        manifest = {}
    if not isinstance(applied_records, list):
        applied_records = []
    if not isinstance(skipped_records, list):
        skipped_records = []
    active_operations = [
        operation
        for operation in context.get("operations", [])
        if isinstance(operation, dict) and operation.get("status") == "active"
    ]
    target_files = sorted({str(record.get("target_file", "")) for record in applied_records if record.get("target_file")})
    action_counts: dict[str, int] = {}
    for record in applied_records:
        action = str(record.get("action", ""))
        action_counts[action] = action_counts.get(action, 0) + 1
    return {
        "configured": bool(context.get("configured")),
        "manifest_path": context.get("manifest_path"),
        "manifest_id": context.get("manifest", {}).get("id") if isinstance(context.get("manifest"), dict) else None,
        "operation_files": context.get("operation_files", []),
        "active_operations": len(active_operations),
        "applied_operations": len(applied_records),
        "skipped_operations": len(skipped_records),
        "target_files": target_files,
        "action_counts": action_counts,
        "applied_records": applied_records,
        "skipped_records": skipped_records,
        "manual_edit_policy": manifest.get("manual_edit_policy", []),
        "delta_source_policy": manifest.get("delta_source_policy", []),
        "generated_report_contract": manifest.get("generated_report_contract", {}),
    }


def write_reader_delta_report(
    output_dir: Path,
    profile: dict,
    summary: dict[str, object],
    overlay_summary: dict[str, object],
) -> str:
    report_path = DEFAULT_DELTA_REPORT
    lines = [
        "# Reader Delta Report",
        "",
        "Status: generated report for the derived reader edition.",
        "",
        "This report records the semantic difference between the live-book source and the generated human-reader source. It is regenerated by `scripts/build_reader_edition.py`; do not hand-edit the generated reader manuscript as the canonical source.",
        "",
        "## Source",
        "",
        f"- Profile: `{profile.get('id', 'reader_release')}`",
        f"- Generated at UTC: `{datetime.now(timezone.utc).isoformat()}`",
        f"- Overlay configured: `{str(overlay_summary.get('configured', False)).lower()}`",
        f"- Overlay manifest: `{overlay_summary.get('manifest_path') or 'not configured'}`",
        f"- Overlay manifest id: `{overlay_summary.get('manifest_id') or 'not configured'}`",
        f"- Active overlay operations: {overlay_summary.get('active_operations', 0)}",
        f"- Applied overlay operations: {overlay_summary.get('applied_operations', 0)}",
        f"- Skipped overlay operations: {overlay_summary.get('skipped_operations', 0)}",
        "",
        "## Editable Delta Source",
        "",
        f"- Canonical editable delta source: `{overlay_summary.get('manifest_path') or 'not configured'}`",
        "- Chapter-level overlay operations belong under `editions/reader_overlays/<version>/chapters/`.",
        "- Generated reader files under `build/reader_edition/` are disposable derivations.",
        f"- This generated report path is `{DEFAULT_DELTA_REPORT}`; review it, but do not edit it to change reader prose.",
        "",
        "### Overlay Source Files",
        "",
    ]

    operation_files = overlay_summary.get("operation_files", [])
    if isinstance(operation_files, list) and operation_files:
        for operation_file in operation_files:
            lines.append(f"- `{operation_file}`")
    else:
        lines.append("No chapter-level overlay operation files were loaded for this generation.")

    delta_source_policy = overlay_summary.get("delta_source_policy", [])
    if isinstance(delta_source_policy, list) and delta_source_policy:
        lines.extend(["", "### Source Policy", ""])
        for item in delta_source_policy:
            lines.append(f"- {item}")

    lines.extend([
        "",
        "## Generator Transformations",
        "",
        f"- Live-only heading sections removed: {summary.get('stripped_heading_count', 0)}",
        f"- AI-only fenced blocks removed: {summary.get('ai_only_blocks_removed', 0)}",
        f"- Human-only fenced blocks unwrapped: {summary.get('human_only_blocks_unwrapped', 0)}",
        f"- Raw core-claim markers removed: {summary.get('removed_sections', {}).get('core_claim_markers_removed', 0) if isinstance(summary.get('removed_sections'), dict) else 0}",
        f"- Repeated support boilerplate humanized: {summary.get('removed_sections', {}).get('support_boilerplate_humanized', 0) if isinstance(summary.get('removed_sections'), dict) else 0}",
        f"- Reader scaffold terms humanized: {summary.get('reader_scaffold_terms_humanized', 0)}",
        "",
        "## Applied Overlay Operations",
        "",
    ])

    applied_records = overlay_summary.get("applied_records", [])
    if isinstance(applied_records, list) and applied_records:
        lines.extend([
            "| Operation | Target file | Action | Section | Word delta | Content digest | Rationale |",
            "|---|---|---|---|---:|---|---|",
        ])
        for record in applied_records:
            section = record.get("section", {})
            if isinstance(section, dict):
                section_label = f"{'#' * int(section.get('level', 2))} {section.get('title', '')}"
            else:
                section_label = ""
            rationale = str(record.get("rationale", "")).replace("|", "\\|")
            lines.append(
                f"| `{record.get('id', '')}` | `{record.get('target_file', '')}` | "
                f"`{record.get('action', '')}` | `{section_label}` | "
                f"{record.get('word_delta', 0)} | `{record.get('content_sha256_16', '')}` | "
                f"{rationale or 'n/a'} |"
            )
    else:
        lines.append("No active reader overlay operations were applied.")

    lines.extend([
        "",
        "## Applied Overlay Operation Details",
        "",
        "These excerpts are generated review evidence. They are not patch instructions and should not be edited by hand.",
        "",
    ])
    if isinstance(applied_records, list) and applied_records:
        for record in applied_records:
            span = record.get("target_line_span", {})
            if isinstance(span, dict):
                span_label = f"{span.get('start', '?')}-{span.get('end', '?')}"
            else:
                span_label = "unknown"
            lines.extend([
                f"### {record.get('id', '')}",
                "",
                f"- Source operation file: `{record.get('source_path', '')}`",
                f"- Target: `{record.get('target_file', '')}` lines `{span_label}` after reader-source derivation and before overlay application",
                f"- Action: `{record.get('action', '')}`",
                f"- Operation content digest: `{record.get('content_sha256_16', '')}`",
                "",
                "Operation content excerpt:",
                "",
                "````markdown",
                str(record.get("content_excerpt", "")).strip() or "(empty)",
                "````",
                "",
                "Target before excerpt:",
                "",
                "````markdown",
                str(record.get("before_excerpt", "")).strip() or "(empty)",
                "````",
                "",
                "Reader output excerpt after operation:",
                "",
                "````markdown",
                str(record.get("after_excerpt", "")).strip() or "(empty)",
                "````",
                "",
            ])
    else:
        lines.append("No operation-level before/after excerpts exist because no active reader overlay operations were applied.")

    skipped_records = overlay_summary.get("skipped_records", [])
    if isinstance(skipped_records, list) and skipped_records:
        lines.extend([
            "",
            "## Skipped Overlay Operations",
            "",
            "| Operation | Status | Target file | Action |",
            "|---|---|---|---|",
        ])
        for record in skipped_records:
            lines.append(
                f"| `{record.get('id', '')}` | `{record.get('status', '')}` | "
                f"`{record.get('target_file', '')}` | `{record.get('action', '')}` |"
            )

    lines.extend([
        "",
        "## Review Checklist",
        "",
        "- [ ] Confirm every active overlay operation is intentional for this major reader version.",
        "- [ ] Confirm no generated reader `.qmd` file was edited as source.",
        "- [ ] Confirm reader-only prose deltas belong in the overlay rather than the canonical AI/research chapter.",
        "- [ ] Confirm any architecture, source, proof, evidence, or future-writing change was made in the canonical live source instead of the overlay.",
        "",
        "## Review Notes",
        "",
        "- Edit tracked overlay files under `editions/reader_overlays/` when a major reader version needs human-edition prose deltas that should survive regeneration.",
        "- Edit live chapter source when the change should also affect AI view, Human view, research releases, proof hooks, source maps, or future writing runs.",
        "- Keep reader overlays semantic: target stable files and headings, not generated line numbers.",
        "",
        "## Non-Claims",
        "",
        "- This report does not claim that an EPUB, PDF, DOCX, HTML reader artifact, audiobook, or audio-embedded EPUB exists.",
        "- This report does not promote any claim support state.",
        "- This report is not a reviewed major-version release record.",
        "",
    ])

    (output_dir / report_path).write_text("\n".join(lines), encoding="utf-8")
    return report_path


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
    cleaned, reader_scaffold_terms_count = humanize_reader_scaffold_terms(cleaned)
    cleaned = normalize_reader_spacing(cleaned)
    if chapter_title:
        cleaned = f"# {chapter_title}\n\n{cleaned.lstrip()}"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(cleaned, encoding="utf-8")
    removed.update({key: count for key, count in view_block_counts.items() if count})
    if marker_count:
        removed["core_claim_markers_removed"] = marker_count
    if support_boilerplate_count:
        removed["support_boilerplate_humanized"] = support_boilerplate_count
    if reader_scaffold_terms_count:
        removed["reader_scaffold_terms_humanized"] = reader_scaffold_terms_count
    return removed


def stripped_heading_count(summary: dict[str, object]) -> int:
    removed_sections = summary.get("removed_sections", {})
    if not isinstance(removed_sections, dict):
        return 0
    return sum(
        int(count)
        for key, count in removed_sections.items()
        if key not in NON_HEADING_TRANSFORM_KEYS
    )


def write_reader_index(output_dir: Path, structure: dict) -> None:
    title = structure.get("title", "The ASI Stack")
    subtitle = structure.get("subtitle", "")
    text = f"""# {title} {{.unnumbered}}

**{title}: {subtitle}** is a reader edition draft derived from the living technical book by Corben Sorenson.

![Layered conceptual architecture for the ASI Stack](assets/images/asi-stack-hero.png){{#fig-reader-asi-stack-hero fig-alt="A light technical illustration of a layered transparent systems stack with routing nodes, ledgers, and controlled feedback loops."}}

## Reader Edition Note

This edition is meant for humans who want the cohesive argument without the live research scaffolding in every chapter. The canonical living book remains the source of truth for source maps, claim/evidence states, proof hooks, schemas, tests, release records, and current residuals.

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
        "lang: en-US",
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
        f"- Live-only sections removed: {summary.get('stripped_heading_count', stripped_heading_count(summary))}",
        f"- AI-only fenced blocks removed: {summary.get('ai_only_blocks_removed', 0)}",
        f"- Human-only fenced blocks unwrapped: {summary.get('human_only_blocks_unwrapped', 0)}",
        f"- Reader scaffold terms humanized: {summary.get('reader_scaffold_terms_humanized', 0)}",
        f"- Reader overlay manifest: `{summary.get('reader_overlay', {}).get('manifest_path') if isinstance(summary.get('reader_overlay'), dict) else 'not configured'}`",
        f"- Reader overlay operations applied: {summary.get('reader_overlay_operations_applied', 0)}",
        f"- Reader delta report: `{summary.get('reader_delta_report', DEFAULT_DELTA_REPORT)}`",
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
        "- [ ] Review the generated reader delta report and confirm any overlay operations are intentional for this major version.",
        "- [ ] Confirm generated reader source and `reader_delta_report.md` were not edited as canonical source for prose changes.",
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
    heading_sections = {
        str(heading): count
        for heading, count in removed_sections.items()
        if heading not in NON_HEADING_TRANSFORM_KEYS
    }
    if heading_sections:
        lines.extend(["| Heading | Removed count |", "|---|---:|"])
        for heading, count in sorted(heading_sections.items()):
            lines.append(f"| `{heading}` | {count} |")
    else:
        lines.append("No live-only sections were removed by the generator.")

    transform_counts = {
        str(key): count
        for key, count in removed_sections.items()
        if key in NON_HEADING_TRANSFORM_KEYS
    }
    if transform_counts:
        lines.extend([
            "",
            "## Reader-Language Transformations",
            "",
            "| Transform | Count |",
            "|---|---:|",
        ])
        for key, count in sorted(transform_counts.items()):
            lines.append(f"| `{key}` | {count} |")

    reader_overlay = summary.get("reader_overlay", {})
    if isinstance(reader_overlay, dict):
        lines.extend([
            "",
            "## Reader Overlay Delta",
            "",
            f"- Overlay manifest: `{reader_overlay.get('manifest_path') or 'not configured'}`",
            f"- Active operations: {reader_overlay.get('active_operations', 0)}",
            f"- Applied operations: {reader_overlay.get('applied_operations', 0)}",
            f"- Delta report: `{summary.get('reader_delta_report', DEFAULT_DELTA_REPORT)}`",
        ])
        target_files = reader_overlay.get("target_files", [])
        if isinstance(target_files, list) and target_files:
            lines.extend(["", "Overlay-touched reader files:"])
            for target_file in target_files:
                lines.append(f"- `{target_file}`")

    companion_routing = summary.get("companion_routing", {})
    if isinstance(companion_routing, dict) and companion_routing.get("configured"):
        records = companion_routing.get("records", [])
        lines.extend([
            "",
            "## Chapter-Level Routing Decisions",
            "",
            f"- Routing manifest: `{companion_routing.get('manifest_path')}`",
            f"- Routing status: `{companion_routing.get('status')}`",
            "",
        ])
        if isinstance(records, list) and records:
            lines.extend([
                "| Chapter | Decision | Reader treatment | Companion/audio route |",
                "|---|---|---|---|",
            ])
            for record in records:
                if not isinstance(record, dict):
                    continue
                companion_route = " ".join(
                    part
                    for part in (
                        str(record.get("companion_treatment", "")).strip(),
                        str(record.get("audio_treatment", "")).strip(),
                    )
                    if part
                )
                lines.append(
                    "| "
                    f"`{markdown_table_cell(record.get('chapter_id', ''))}` | "
                    f"`{markdown_table_cell(record.get('routing_decision', ''))}` | "
                    f"{markdown_table_cell(record.get('reader_treatment', ''))} | "
                    f"{markdown_table_cell(companion_route)} |"
                )
        lines.extend([
            "",
            "Routing note: meaning-critical caveats, support limits, proof boundaries, governance boundaries, release blockers, and non-claims must remain in the reader manuscript. Companion notes can help with glossary, quick-reference, and spoken-treatment support, but they are not a substitute for the reader spine.",
        ])

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
        "stripped_heading_count": summary.get("stripped_heading_count", stripped_heading_count(summary)),
        "removed_sections": summary["removed_sections"],
        "reader_scaffold_terms_humanized": summary.get("reader_scaffold_terms_humanized", 0),
        "ai_only_blocks_removed": summary.get("ai_only_blocks_removed", 0),
        "human_only_blocks_unwrapped": summary.get("human_only_blocks_unwrapped", 0),
        "reader_overlay": summary.get("reader_overlay", {}),
        "reader_delta_report": summary.get("reader_delta_report", DEFAULT_DELTA_REPORT),
        "companion_note_routing": summary.get("companion_routing", {}),
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
    overlay_context = load_reader_overlay_context(profile)

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
            apply_reader_overlay_to_file(output_dir / front_file, front_file, overlay_context)
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
            apply_reader_overlay_to_file(output_dir / chapter["file"], chapter["file"], overlay_context)
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
            output_path = output_dir / appendix
            removed = clean_file(src, output_path, strip_headings)
            apply_reader_overlay_to_file(output_path, appendix, overlay_context)
            converted = transform_reader_source_appendix(output_path, appendix)
            if converted:
                removed["reader_source_appendix_tables_converted"] = converted
            copied_files += 1
            for key, count in removed.items():
                if key == "ai_only_blocks_removed":
                    ai_only_blocks_removed += count
                elif key == "human_only_blocks_unwrapped":
                    human_only_blocks_unwrapped += count
                else:
                    removed_totals[key] = removed_totals.get(key, 0) + count

    finalize_reader_overlay_context(overlay_context)
    write_quarto(output_dir, structure, profile)
    overlay_summary = reader_overlay_summary(overlay_context)
    companion_routing = load_companion_routing(companion_policy)
    summary = {
        "output_dir": str(output_dir),
        "profile": profile_id,
        "chapters": chapter_count,
        "files": copied_files,
        "removed_sections": removed_totals,
        "stripped_heading_count": sum(
            count
            for key, count in removed_totals.items()
            if key not in NON_HEADING_TRANSFORM_KEYS
        ),
        "reader_scaffold_terms_humanized": removed_totals.get("reader_scaffold_terms_humanized", 0),
        "ai_only_blocks_removed": ai_only_blocks_removed,
        "human_only_blocks_unwrapped": human_only_blocks_unwrapped,
        "formats": profile.get("publication_formats", []),
        "reader_overlay": overlay_summary,
        "reader_overlay_operations_applied": overlay_summary.get("applied_operations", 0),
        "companion_routing": companion_routing,
    }
    delta_report_path = write_reader_delta_report(output_dir, profile, summary, overlay_summary)
    summary["reader_delta_report"] = delta_report_path
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


def scan_for_reader_scaffold_terms(output_dir: Path) -> list[str]:
    terms = ("codex workflow", "source crosswalk", "source-note")
    violations: list[str] = []
    for path in output_dir.rglob("*.qmd"):
        text = path.read_text(encoding="utf-8")
        lowered = text.lower()
        for term in terms:
            if term in lowered:
                violations.append(f"{path.relative_to(output_dir)}: retained reader scaffold term {term!r}")
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
            violations.extend(scan_for_reader_scaffold_terms(output_dir))
            if violations:
                print("Reader edition still contains stripped headings, live view markers, or scaffold terms:")
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
            companion_text = (output_dir / companion_path).read_text(encoding="utf-8")
            if (
                isinstance(companion_policy, dict)
                and companion_policy.get("routing_manifest")
                and "Chapter-Level Routing Decisions" not in companion_text
            ):
                raise SystemExit("Reader edition check failed: companion notes missing routing decisions.")
            delta_report_path = output_dir / str(summary.get("reader_delta_report", DEFAULT_DELTA_REPORT))
            if not delta_report_path.exists():
                raise SystemExit("Reader edition check failed: missing reader_delta_report.md.")
            manifest_path = output_dir / "reader_manifest.json"
            if not manifest_path.exists():
                raise SystemExit("Reader edition check failed: missing reader_manifest.json.")
            manifest = load_json(manifest_path)
            if not isinstance(manifest, dict):
                raise SystemExit("Reader edition check failed: reader_manifest.json must contain an object.")
            if not isinstance(manifest.get("reader_overlay"), dict):
                raise SystemExit("Reader edition check failed: manifest missing reader_overlay.")
            if manifest.get("reader_delta_report") != str(summary.get("reader_delta_report", DEFAULT_DELTA_REPORT)):
                raise SystemExit("Reader edition check failed: manifest reader_delta_report mismatch.")
            if (
                isinstance(companion_policy, dict)
                and companion_policy.get("routing_manifest")
                and not isinstance(manifest.get("companion_note_routing"), dict)
            ):
                raise SystemExit("Reader edition check failed: manifest missing companion_note_routing.")
            if not isinstance(manifest.get("reader_spine_validation"), dict):
                raise SystemExit("Reader edition check failed: manifest missing reader_spine_validation.")
            handoff_review = manifest.get("handoff_continuity_review")
            if not isinstance(handoff_review, dict) or handoff_review.get("required") is not True:
                raise SystemExit("Reader edition check failed: manifest missing required Handoff review.")
            print(
                "Reader edition check passed: "
                f"{summary['chapters']} chapters, {summary['files']} files, "
                f"{summary['stripped_heading_count']} live-only sections removed, "
                f"{summary.get('reader_scaffold_terms_humanized', 0)} reader scaffold terms humanized, "
                f"{summary.get('reader_overlay_operations_applied', 0)} reader overlay operations applied."
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
