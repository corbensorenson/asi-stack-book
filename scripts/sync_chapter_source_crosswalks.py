#!/usr/bin/env python3
"""Add manifest-assigned sources missing from chapter source crosswalks.

Generated rows preserve the strongest recorded mapping boundary: metadata-first
assignments remain metadata-first, while passage-reviewed claim mappings retain
their mapped support and limits. They are traceability supplements, never local
reproduction or support-state promotion.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STRUCTURE = ROOT / "book_structure.json"
INVENTORY = ROOT / "sources" / "source_inventory.json"
BLOCK_RE = re.compile(
    r"(?ms)^### Manifest source assignment reconciliation\n.*?^<!-- manifest-source-reconciliation:end -->\n?"
)


def qmd_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def load_records() -> tuple[list[dict], dict[str, dict]]:
    structure = json.loads(STRUCTURE.read_text(encoding="utf-8"))
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    if not isinstance(structure, dict) or not isinstance(inventory, list):
        raise TypeError("book structure and source inventory must be JSON objects/arrays")
    records = [chapter for part in structure.get("parts", []) if isinstance(part, dict) for chapter in part.get("chapters", []) if isinstance(chapter, dict)]
    by_id = {str(record.get("id")): record for record in inventory if isinstance(record, dict) and record.get("id")}
    return records, by_id


def source_rows(source_ids: list[str], inventory: dict[str, dict], chapter: dict) -> str:
    mappings = {
        str(row.get("source_id")): row
        for row in chapter.get("claim_source_mappings", [])
        if isinstance(row, dict) and row.get("source_id")
    }
    chapter_title = qmd_escape(chapter.get("title", chapter.get("id", "This chapter")))
    rows = [
        "### Manifest source assignment reconciliation",
        "",
        f"These rows keep {chapter_title}'s manifest assignments visible at their recorded review boundary. Passage review does not establish local reproduction, performance, safety, deployment, or support-state movement.",
        "",
        "| Source | Intake role | Boundary |",
        "|---|---|---|",
    ]
    for source_id in source_ids:
        record = inventory.get(source_id, {})
        title = qmd_escape(record.get("title", "Inventory record"))
        notes = qmd_escape(record.get("notes", "Metadata-first source intake; consult the public source note."))
        mapping = mappings.get(source_id, {})
        if mapping.get("passage_review_state") == "reviewed":
            support = qmd_escape(mapping.get("mapped_support", notes))
            limits = qmd_escape(mapping.get("limits", "The mapping remains bounded to the reviewed passages."))
            rows.append(
                f"| `{source_id}` | Passage-reviewed comparator: {title}. {support} | {limits} "
                "No local implementation, reproduction, performance, safety, deployment, support-state, or ASI result is established by this reconciliation row. |"
            )
        else:
            rows.append(
                f"| `{source_id}` | Metadata-first comparator: {title}. {notes} | "
                "No passage-level source claim, local implementation, reproduction, safety, performance, deployment, support-state, or ASI result is established by this reconciliation row. |"
            )
    rows.extend(["", "<!-- manifest-source-reconciliation:end -->", ""])
    return "\n".join(rows)


def synchronize_chapter_source_crosswalks(write: bool = False) -> int:
    chapters, inventory = load_records()
    changed = 0
    for chapter in chapters:
        relative = chapter.get("file")
        source_ids = [source_id for source_id in chapter.get("source_ids", []) if isinstance(source_id, str)]
        if not isinstance(relative, str) or not source_ids:
            continue
        path = ROOT / relative
        if not path.exists():
            continue
        original = path.read_text(encoding="utf-8")
        # Older generated blocks could land after a late authored insertion and
        # therefore outside the Source crosswalk. Remove them globally before
        # computing the one canonical block location.
        text = BLOCK_RE.sub("", original)
        heading = "## Source crosswalk\n"
        start = text.find(heading)
        if start < 0:
            continue
        section_start = start + len(heading)
        next_heading = re.search(r"(?m)^## ", text[section_start:])
        section_end = section_start + next_heading.start() if next_heading else len(text)
        section = text[section_start:section_end]
        authored_section = BLOCK_RE.sub("", section)
        missing = [source_id for source_id in source_ids if f"`{source_id}`" not in authored_section]
        generated = BLOCK_RE.search(section)
        if not missing:
            if text != original:
                changed += 1
                if write:
                    path.write_text(text, encoding="utf-8")
            continue
        replacement = source_rows(missing, inventory, chapter) if missing else ""
        if generated:
            updated_section = section[:generated.start()] + replacement + section[generated.end():]
        else:
            closing_fences = list(re.finditer(r"(?m)^:::\s*$", section))
            if closing_fences:
                closing = closing_fences[-1]
                updated_section = (
                    section[:closing.start()].rstrip()
                    + "\n\n"
                    + replacement
                    + section[closing.start():]
                )
            else:
                updated_section = section.rstrip() + "\n\n" + replacement
        updated = text[:section_start] + updated_section + text[section_end:]
        if updated != original:
            changed += 1
            if write:
                path.write_text(updated, encoding="utf-8")
    return changed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="Write missing source-crosswalk reconciliation rows.")
    args = parser.parse_args()
    changed = synchronize_chapter_source_crosswalks(write=args.write)
    action = "wrote" if args.write else "would write"
    print(f"Chapter source-crosswalk synchronization {action}: {changed} chapter file(s).")


if __name__ == "__main__":
    main()
