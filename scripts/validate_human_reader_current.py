#!/usr/bin/env python3
"""Validate the maintained independent 26-unit Human Reader manuscript."""

from __future__ import annotations

import copy
import json
from pathlib import Path

from build_human_reader_current import (
    EDITION,
    MANIFEST,
    ROOT,
    STRUCTURE,
    build,
)

STATUS = ROOT / "roadmap_records/post_v2_3_maintenance_transfer_and_publication_status.json"


UNIT_23_REQUIRED = [
    "## The Complete Bill",
    "## Speed Is a Qualified Route",
    "## Deliberation Has a Failure Surface",
    "## Compression Moves Burden",
    "## One Allocation Decision",
    "## The Allocation Lease",
    "## A Worked Budget",
    "## Failure Cases",
    "## Evidence and Experiments",
    "## Human Time and Organizational Cost",
    "## From Minimum Implementation to Mature System",
    "## What This Establishes",
    "evidentiary authority are separate claims",
    "does not establish that the proposed controller is economically optimal",
]
UNIT_04_REQUIRED = [
    "## A Change Can Be Correct and Still Be Unsafe",
    "## The Smallest Powerful Kernel",
    "## The Model Is Part of the Attack Surface",
    "## Privacy Is About Use, Not Merely Secrecy",
    "## Protected Computation Is Evidence, Not Permission",
    "## Model Weights Are a Custody Graph",
    "## The Supply Chain Is a Living Dependency Graph",
    "## Release Changes the Kind of Control",
    "## One End-to-End Custody Decision",
    "## Failure Cases",
    "## What the Current Evidence Can Establish",
    "## From Minimum Implementation to a Mature Security Fabric",
    "## The Strongest Objection",
    "## What This Establishes",
    "A successful local load is not release authority",
    "The conclusion should change if simpler systems prove equally effective",
]


def validate(manifest: dict, expected: dict) -> list[str]:
    errors: list[str] = []
    if manifest != expected:
        errors.append("manifest differs from its canonical graph/outline/manuscript derivation")
    if manifest.get("unit_count") != 26 or manifest.get("owner_route_count") != 87:
        errors.append("Human Reader denominator drift")
    units = manifest.get("units", [])
    owner_ids = [owner_id for unit in units for owner_id in unit.get("owner_ids", [])]
    if len(owner_ids) != len(set(owner_ids)):
        errors.append("a technical owner routes to more than one Human Reader unit")
    structure = json.loads(STRUCTURE.read_text(encoding="utf-8"))
    canonical_ids = {
        chapter["id"] for part in structure["parts"] for chapter in part["chapters"]
    }
    if set(owner_ids) != canonical_ids:
        errors.append("Human Reader routes omit or invent a canonical owner")
    for unit in units:
        path = EDITION / unit["source_file"]
        state = unit.get("state")
        if state == "not_started":
            if path.exists():
                errors.append(f"{unit['unit_id']}: existing source marked not started")
            continue
        if not path.is_file():
            errors.append(f"{unit['unit_id']}: started source is missing")
            continue
        text = path.read_text(encoding="utf-8")
        if "chapters/" in text and "{{< include" in text and "../generated/" not in text:
            errors.append(f"{unit['unit_id']}: source appears to include a live technical chapter")
        if state == "target_length_reached_internal_review_pending" and not (
            unit["target_min_words"] <= unit["visible_word_count"] <= unit["target_max_words"]
        ):
            errors.append(f"{unit['unit_id']}: false target-length completion")
        if unit.get("owner_support_states") != ["argument"]:
            errors.append(f"{unit['unit_id']}: routed owner support changed or was combined")
        panel_path = EDITION / "generated" / f"{unit['unit_id']}-status.qmd"
        if panel_path.is_file():
            panel = panel_path.read_text(encoding="utf-8")
            for owner_id in unit["owner_ids"]:
                owner_url = f"https://corbensorenson.github.io/asi-stack-book/chapters/{owner_id}.html"
                if owner_url not in panel:
                    errors.append(f"{unit['unit_id']}: missing discoverable owner route {owner_id}")
    unit_04 = next((unit for unit in units if unit.get("unit_id") == "unit-04"), None)
    if unit_04 is None or unit_04.get("state") != "target_length_reached_internal_review_pending":
        errors.append("Unit 4 has not reached its drafting target")
    else:
        text = (EDITION / unit_04["source_file"]).read_text(encoding="utf-8")
        for fragment in UNIT_04_REQUIRED:
            if fragment not in text:
                errors.append(f"Unit 4 missing required argument boundary: {fragment!r}")
    unit_23 = next((unit for unit in units if unit.get("unit_id") == "unit-23"), None)
    if unit_23 is None or unit_23.get("state") != "target_length_reached_internal_review_pending":
        errors.append("Unit 23 has not reached its drafting target")
    else:
        text = (EDITION / unit_23["source_file"]).read_text(encoding="utf-8")
        for fragment in UNIT_23_REQUIRED:
            if fragment not in text:
                errors.append(f"Unit 23 missing required argument boundary: {fragment!r}")
    if manifest.get("support_state_effect") != "none" or manifest.get("release_effect") != "none":
        errors.append("Human Reader drafting changed support or release state")
    status = json.loads(STATUS.read_text(encoding="utf-8"))["editorial_product_migration"]
    expected_status = {
        "human_reader_current_manifest_path": "editions/reader_manuscript/current/manifest.json",
        "human_reader_started_unit_count": manifest.get("started_unit_count"),
        "human_reader_target_length_unit_count": manifest.get("target_length_unit_count"),
        "human_reader_visible_word_count": manifest.get("visible_word_count"),
    }
    for field, value in expected_status.items():
        if status.get(field) != value:
            errors.append(f"roadmap Human Reader status drift: {field}")
    return errors


def main() -> None:
    expected, outputs = build()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    errors = validate(manifest, expected)
    stale = [
        path.relative_to(ROOT).as_posix()
        for path, text in outputs.items()
        if not path.is_file() or path.read_text(encoding="utf-8") != text
    ]
    if stale:
        errors.append("stale generated Human Reader derivatives: " + ", ".join(stale))

    altered = copy.deepcopy(manifest)
    altered["units"][0]["owner_ids"] = []
    if not validate(altered, expected):
        errors.append("negative control accepted: owner-route loss")
    altered = copy.deepcopy(manifest)
    altered["units"][22]["visible_word_count"] = 1
    if not validate(altered, expected):
        errors.append("negative control accepted: false length completion")
    altered = copy.deepcopy(manifest)
    altered["support_state_effect"] = "promoted"
    if not validate(altered, expected):
        errors.append("negative control accepted: support laundering")

    if errors:
        raise SystemExit("Human Reader current validation failed:\n - " + "\n - ".join(errors))
    print(
        f"Human Reader current validation passed: {manifest['started_unit_count']}/26 units started, "
        f"{manifest['target_length_unit_count']} at target length, 87 owners routed once, "
        f"{manifest['visible_word_count']} visible words, and 3 rejecting controls."
    )


if __name__ == "__main__":
    main()
