#!/usr/bin/env python3
"""Refresh source availability lines in existing chapter manuscripts.

This script is intentionally narrow: it updates each chapter's "Source loading
state" row and source-crosswalk readiness cells from the current source notes and
local cache state without rewriting chapter prose.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STRUCTURE = ROOT / "book_structure.json"
SOURCE_NOTES = ROOT / "sources" / "source_notes"
RAW_DIR = ROOT / "sources" / "raw" / "google_docs"
CACHE_MANIFEST = ROOT / "sources" / "cache" / "cache_manifest.json"


def load_json(path: Path) -> object:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def load_cache_records() -> dict[str, dict]:
    if not CACHE_MANIFEST.exists():
        return {}
    data = load_json(CACHE_MANIFEST)
    if not isinstance(data, dict):
        return {}
    records = data.get("records", [])
    if not isinstance(records, list):
        return {}
    return {
        str(record.get("id", "")): record
        for record in records
        if isinstance(record, dict) and record.get("id")
    }


def flatten_chapters(structure: dict) -> list[dict]:
    chapters: list[dict] = []
    for part in structure.get("parts", []):
        for chapter in part.get("chapters", []):
            chapters.append(chapter)
    return chapters


def inline_code_list(items: list[str]) -> str:
    return ", ".join(f"`{item}`" for item in items)


def source_note_exists(source_id: str) -> bool:
    return (SOURCE_NOTES / f"{source_id}.md").exists()


def local_raw_exists(source_id: str) -> bool:
    return any((RAW_DIR / f"{source_id}{suffix}").exists() for suffix in [".txt", ".md", ".bin"])


def source_readiness(source_id: str, cache_records: dict[str, dict]) -> str:
    labels: list[str] = []
    cache = cache_records.get(source_id, {})
    if source_note_exists(source_id):
        labels.append("source note available")
    if local_raw_exists(source_id):
        labels.append("local raw cache available")
    if cache.get("status") == "connector_required" and not local_raw_exists(source_id):
        labels.append("connector or recovery required")
    elif cache.get("status") and not local_raw_exists(source_id):
        labels.append(f"cache status: {cache['status']}")
    if not labels:
        labels.append("source note pending")
    return "; ".join(labels)


def source_summary(source_ids: list[str], cache_records: dict[str, dict]) -> str:
    note_ready = [sid for sid in source_ids if source_note_exists(sid)]
    raw_ready = [sid for sid in source_ids if local_raw_exists(sid)]
    pending_notes = [sid for sid in source_ids if not source_note_exists(sid)]
    recovery = [
        sid
        for sid in source_ids
        if cache_records.get(sid, {}).get("status") == "connector_required" and not local_raw_exists(sid)
    ]

    parts: list[str] = []
    if note_ready:
        parts.append(f"source notes: {inline_code_list(note_ready)}")
    if raw_ready:
        parts.append(f"raw cache: {inline_code_list(raw_ready)}")
    if pending_notes:
        parts.append(f"pending source notes: {inline_code_list(pending_notes)}")
    if recovery:
        parts.append(f"connector/recovery: {inline_code_list(recovery)}")
    return "; ".join(parts) if parts else "No sources assigned."


SOURCE_ROW_RE = re.compile(r"^\|\s*`([^`]+)`\s*\|")


def refresh_text(text: str, source_ids: list[str], cache_records: dict[str, dict]) -> str:
    summary = source_summary(source_ids, cache_records)
    lines = text.splitlines()
    updated: list[str] = []
    source_id_set = set(source_ids)
    for line in lines:
        if line.startswith("| Source loading state |"):
            updated.append(f"| Source loading state | {summary} |")
            continue

        match = SOURCE_ROW_RE.match(line.strip())
        if match and match.group(1) in source_id_set:
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if len(cells) >= 5:
                cells[-1] = source_readiness(match.group(1), cache_records)
                updated.append("| " + " | ".join(cells) + " |")
                continue
        updated.append(line)
    return "\n".join(updated) + ("\n" if text.endswith("\n") else "")


def main() -> None:
    structure = load_json(STRUCTURE)
    if not isinstance(structure, dict):
        raise SystemExit("book_structure.json must contain an object")
    cache_records = load_cache_records()
    changed = 0
    for chapter in flatten_chapters(structure):
        source_ids = list(dict.fromkeys(chapter.get("source_ids", [])))
        path = ROOT / chapter["file"]
        if not path.exists():
            continue
        old = path.read_text(encoding="utf-8")
        new = refresh_text(old, source_ids, cache_records)
        if new != old:
            path.write_text(new, encoding="utf-8")
            changed += 1
    print(f"Updated source status in {changed} chapter files.")


if __name__ == "__main__":
    main()
