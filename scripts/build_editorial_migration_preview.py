#!/usr/bin/env python3
"""Initialize and derive the metadata-first editorial migration preview."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
STRUCTURE = ROOT / "book_structure.json"
STATUS = ROOT / "roadmap_records/post_v2_3_maintenance_transfer_and_publication_status.json"
OUTLINE = ROOT / "docs/human_reader_26_unit_outline.md"
PREVIEW = ROOT / "products/editorial_migration_preview.json"


def load(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def chapters(structure: dict) -> list[dict]:
    return [chapter for part in structure["parts"] for chapter in part["chapters"]]


def outline_units() -> list[dict]:
    text = OUTLINE.read_text(encoding="utf-8")
    blocks = re.split(r"^## Unit ", text, flags=re.MULTILINE)[1:]
    units: list[dict] = []
    for block in blocks:
        heading, body = block.split("\n", 1)
        match = re.fullmatch(r"(\d+) - (.+)", heading.strip())
        if match is None:
            raise ValueError(f"Malformed Human Reader unit heading: {heading!r}")
        route_match = re.search(
            r"\*\*Canonical owner routes\.\*\*(.*?)(?=\n\n\*\*Narrative job\.\*\*)",
            body,
            flags=re.DOTALL,
        )
        if route_match is None:
            raise ValueError(f"Unit {match.group(1)} has no canonical owner route")
        owner_ids = re.findall(r"`([^`]+)`", route_match.group(1))
        units.append(
            {
                "unit_id": f"unit-{int(match.group(1)):02d}",
                "title": match.group(2).strip(),
                "owner_ids": owner_ids,
            }
        )
    return units


def initialize_metadata(structure: dict, status: dict) -> None:
    editorial = status["editorial_product_migration"]
    merge_map = editorial["merge_map"]
    merge_modes = editorial["merge_mode_map"]
    profile_map = editorial["profile_map"]
    dossier_map = editorial["dossier_map"]
    back_matter_map = editorial["back_matter_map"]
    implementation_ids = set(editorial["implementation_method_ids"])
    unit_by_owner = {
        owner_id: unit["unit_id"]
        for unit in outline_units()
        for owner_id in unit["owner_ids"]
    }

    for chapter in chapters(structure):
        chapter_id = chapter["id"]
        if chapter_id in merge_map:
            role = merge_modes[chapter_id]
            parent_id = merge_map[chapter_id]
            visibility = "technical_detail"
        elif chapter_id in profile_map:
            role = "deployment_profile_owner"
            parent_id = profile_map[chapter_id]
            visibility = "deployment_profile"
        elif chapter_id in dossier_map:
            role = "research_dossier_owner"
            parent_id = dossier_map[chapter_id]
            visibility = "research_dossier"
        elif chapter_id in back_matter_map:
            role = "generated_back_matter_owner"
            parent_id = back_matter_map[chapter_id]
            visibility = "generated_back_matter"
        elif chapter_id in implementation_ids:
            role = "implementation_method_owner"
            parent_id = None
            visibility = "main_book"
        else:
            role = "primary_architecture_owner"
            parent_id = None
            visibility = "main_book"

        chapter["publication"] = {
            "role": role,
            "parent_id": parent_id,
            "visibility": visibility,
            "legacy_id": chapter_id,
            "legacy_file": chapter["file"],
            "claim_ownership": "preserved_local_no_inheritance",
            "editorial_state": "metadata_classified_prose_unchanged",
            "support_state_effect": "none",
        }
        chapter["human_reader_unit_id"] = unit_by_owner[chapter_id]


def build_preview(structure: dict) -> dict:
    all_chapters = chapters(structure)
    roles: dict[str, list[dict]] = {}
    for chapter in all_chapters:
        publication = chapter["publication"]
        roles.setdefault(publication["role"], []).append(
            {
                "id": chapter["id"],
                "title": chapter["title"],
                "file": chapter["file"],
                "parent_id": publication["parent_id"],
                "human_reader_unit_id": chapter["human_reader_unit_id"],
            }
        )
    for rows in roles.values():
        rows.sort(key=lambda row: row["id"])

    units = outline_units()
    main_roles = {"primary_architecture_owner", "implementation_method_owner"}
    return {
        "schema_version": 1,
        "product_id": "editorial-migration-metadata-preview",
        "state": "three_packages_composed_no_public_cutover",
        "sources": ["book_structure.json", "docs/human_reader_26_unit_outline.md"],
        "book_structure_sha256": digest(STRUCTURE),
        "human_reader_outline_sha256": digest(OUTLINE),
        "reference_owner_count": len(all_chapters),
        "main_book_owner_count": sum(
            len(rows) for role, rows in roles.items() if role in main_roles
        ),
        "role_counts": {role: len(rows) for role, rows in sorted(roles.items())},
        "roles": dict(sorted(roles.items())),
        "human_reader": {
            "state": "independent_manuscript_in_progress",
            "unit_count": len(units),
            "owner_route_count": sum(len(unit["owner_ids"]) for unit in units),
            "units": units,
        },
        "support_state_effect": "none",
        "public_route_effect": "none",
        "non_claims": [
            "Publication nesting does not transfer claim, proof, evidence, or authority ownership.",
            "Three composition packages do not complete the remaining publication nests or semantic merge candidate.",
            "The 26-unit outline and partial maintained manuscript are not a completed Human Reader edition.",
            "No support state, release state, safety, readiness, AGI, or ASI claim changes.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--initialize-metadata", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    structure = load(STRUCTURE)
    if not isinstance(structure, dict):
        raise SystemExit("book_structure.json must contain an object")
    if args.initialize_metadata:
        status = load(STATUS)
        if not isinstance(status, dict):
            raise SystemExit("roadmap status must contain an object")
        initialize_metadata(structure, status)
        STRUCTURE.write_text(json.dumps(structure, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    expected = build_preview(structure)
    rendered = json.dumps(expected, indent=2, ensure_ascii=False) + "\n"
    if args.write or args.initialize_metadata:
        PREVIEW.write_text(rendered, encoding="utf-8")
        print(
            f"Wrote editorial preview: {expected['reference_owner_count']} owners, "
            f"{expected['main_book_owner_count']} main-book owners, "
            f"{expected['human_reader']['unit_count']} Human Reader units."
        )
        return
    if not PREVIEW.exists() or PREVIEW.read_text(encoding="utf-8") != rendered:
        raise SystemExit("Editorial migration preview is stale; run with --write")
    print(
        f"Editorial preview is current: {expected['reference_owner_count']} owners, "
        f"{expected['human_reader']['unit_count']} Human Reader units."
    )


if __name__ == "__main__":
    main()
