#!/usr/bin/env python3
"""Validate EM0/EM1 role coverage without implying editorial cutover."""

from __future__ import annotations

import copy
import json
from pathlib import Path

from build_editorial_migration_preview import (
    OUTLINE,
    PREVIEW,
    ROOT,
    STATUS,
    STRUCTURE,
    build_preview,
    chapters,
    outline_units,
)


EXPECTED_ROLE_COUNTS = {
    "primary_architecture_owner": 54,
    "implementation_method_owner": 2,
    "publication_nest": 15,
    "method_detail_nest": 2,
    "semantic_merge_candidate": 1,
    "deployment_profile_owner": 7,
    "research_dossier_owner": 5,
    "generated_back_matter_owner": 1,
}
MAIN_ROLES = {"primary_architecture_owner", "implementation_method_owner"}
NEST_ROLES = {"publication_nest", "method_detail_nest", "semantic_merge_candidate"}
COLLECTION_ROLES = {
    "deployment_profile_owner",
    "research_dossier_owner",
    "generated_back_matter_owner",
}
EXPECTED_VISIBILITY = {
    "primary_architecture_owner": "main_book",
    "implementation_method_owner": "main_book",
    "publication_nest": "technical_detail",
    "method_detail_nest": "technical_detail",
    "semantic_merge_candidate": "technical_detail",
    "deployment_profile_owner": "deployment_profile",
    "research_dossier_owner": "research_dossier",
    "generated_back_matter_owner": "generated_back_matter",
}


def load(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def validate(structure: dict, status: dict, preview: dict) -> list[str]:
    errors: list[str] = []
    rows = chapters(structure)
    ids = {row.get("id") for row in rows}
    editorial = status.get("editorial_product_migration", {})
    expected_parent = {
        **editorial.get("merge_map", {}),
        **editorial.get("profile_map", {}),
        **editorial.get("dossier_map", {}),
        **editorial.get("back_matter_map", {}),
    }
    expected_role = dict(editorial.get("merge_mode_map", {}))
    expected_role.update({key: "deployment_profile_owner" for key in editorial.get("profile_map", {})})
    expected_role.update({key: "research_dossier_owner" for key in editorial.get("dossier_map", {})})
    expected_role.update({key: "generated_back_matter_owner" for key in editorial.get("back_matter_map", {})})
    expected_role.update({key: "implementation_method_owner" for key in editorial.get("implementation_method_ids", [])})

    role_counts = {role: 0 for role in EXPECTED_ROLE_COUNTS}
    unit_routes: dict[str, list[str]] = {}
    for row in rows:
        chapter_id = row.get("id")
        publication = row.get("publication")
        if not isinstance(publication, dict):
            errors.append(f"{chapter_id}: missing publication metadata")
            continue
        role = publication.get("role")
        if role not in role_counts:
            errors.append(f"{chapter_id}: invalid publication role {role!r}")
            continue
        role_counts[role] += 1
        expected = expected_role.get(chapter_id, "primary_architecture_owner")
        if role != expected:
            errors.append(f"{chapter_id}: role {role!r} != reviewed disposition {expected!r}")
        if publication.get("visibility") != EXPECTED_VISIBILITY[role]:
            errors.append(f"{chapter_id}: visibility drift")
        parent_id = publication.get("parent_id")
        if parent_id != expected_parent.get(chapter_id):
            errors.append(f"{chapter_id}: parent drift")
        if role in MAIN_ROLES and parent_id is not None:
            errors.append(f"{chapter_id}: main-book owner has a parent")
        if role in NEST_ROLES and parent_id not in ids:
            errors.append(f"{chapter_id}: nested owner parent is not a canonical chapter")
        if role in COLLECTION_ROLES and not isinstance(parent_id, str):
            errors.append(f"{chapter_id}: collection owner has an invalid collection parent")
        if publication.get("legacy_id") != chapter_id or publication.get("legacy_file") != row.get("file"):
            errors.append(f"{chapter_id}: legacy identity or route drift")
        if publication.get("claim_ownership") != "preserved_local_no_inheritance":
            errors.append(f"{chapter_id}: claim ownership can be inherited")
        if publication.get("editorial_state") != "metadata_classified_prose_unchanged":
            errors.append(f"{chapter_id}: EM1 changed prose-composition state")
        if publication.get("support_state_effect") != "none":
            errors.append(f"{chapter_id}: metadata migration changed support state")
        unit_id = row.get("human_reader_unit_id")
        if not isinstance(unit_id, str):
            errors.append(f"{chapter_id}: missing Human Reader route")
        else:
            unit_routes.setdefault(unit_id, []).append(chapter_id)

    if role_counts != EXPECTED_ROLE_COUNTS:
        errors.append(f"publication role counts drifted: {role_counts}")
    outline = outline_units()
    expected_units = {unit["unit_id"]: sorted(unit["owner_ids"]) for unit in outline}
    actual_units = {unit_id: sorted(owner_ids) for unit_id, owner_ids in unit_routes.items()}
    if actual_units != expected_units:
        errors.append("Human Reader owner routes disagree with the canonical 26-unit outline")
    if len(outline) != 26 or set().union(*(set(unit["owner_ids"]) for unit in outline)) != ids:
        errors.append("Human Reader outline does not cover all canonical owners")
    if sum(len(unit["owner_ids"]) for unit in outline) != len(ids):
        errors.append("Human Reader outline duplicates an owner route")
    if preview != build_preview(structure):
        errors.append("editorial migration preview is not its canonical derivation")
    if editorial.get("em0_count_reconciliation_complete") is not True:
        errors.append("EM0 count reconciliation is not complete")
    if editorial.get("stale_active_product_count_literal_count") != 0:
        errors.append("EM0 still records stale active product counts")
    if editorial.get("state") != "em1_metadata_classified_preview_generated":
        errors.append("editorial migration state does not record EM1 completion")
    if editorial.get("support_state_effect") != "none" or editorial.get("release_effect") != "none":
        errors.append("editorial migration moved support or release state")
    return errors


def main() -> None:
    structure = load(STRUCTURE)
    status = load(STATUS)
    preview = load(PREVIEW)
    if not all(isinstance(value, dict) for value in (structure, status, preview)):
        raise SystemExit("editorial migration inputs must contain objects")
    errors = validate(structure, status, preview)

    mutations = []
    first = chapters(structure)[0]
    altered = copy.deepcopy(structure)
    chapters(altered)[0]["publication"]["support_state_effect"] = "promoted"
    mutations.append(("support promotion", altered))
    altered = copy.deepcopy(structure)
    chapters(altered)[0]["human_reader_unit_id"] = "unit-26"
    mutations.append(("owner reroute", altered))
    nested_index = next(i for i, row in enumerate(chapters(structure)) if row["publication"]["role"] in NEST_ROLES)
    altered = copy.deepcopy(structure)
    chapters(altered)[nested_index]["publication"]["parent_id"] = None
    mutations.append(("parent erasure", altered))
    for label, altered in mutations:
        if not validate(altered, status, build_preview(altered)):
            errors.append(f"negative control accepted: {label}")

    if errors:
        raise SystemExit("Editorial migration validation failed:\n - " + "\n - ".join(errors))
    print(
        "Editorial migration validation passed: 87 owners, 54+2 main-book owners, "
        "15 publication nests, 2 method-detail nests, 1 semantic candidate, "
        "7 profiles, 5 dossier owners, 1 back-matter owner, 26 Human Reader routes, "
        "and 3 rejecting controls."
    )


if __name__ == "__main__":
    main()
