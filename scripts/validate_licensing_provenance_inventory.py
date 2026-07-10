#!/usr/bin/env python3
"""Validate provenance coverage under the selected delayed-opening policy."""

from __future__ import annotations

import copy
import json
from pathlib import Path

from build_canonical_public_status import ROOT, load_json, validate_against_schema
from build_licensing_provenance_inventory import DECISION, OUTPUT, POLICY, build_inventory


POLICY_SCHEMA = ROOT / "schemas" / "licensing_provenance_policy.schema.json"
INVENTORY_SCHEMA = ROOT / "schemas" / "licensing_provenance_inventory.schema.json"
LICENSE = ROOT / "LICENSE.md"
DOC = ROOT / "docs" / "licensing_provenance_audit.md"


def semantic_errors(inventory: dict, expected: dict, decision: dict) -> list[str]:
    errors: list[str] = []
    if inventory != expected:
        errors.append("tracked provenance inventory differs from deterministic current-path classification")
    rows = inventory.get("files", [])
    paths = [row.get("path") for row in rows]
    if len(paths) != len(set(paths)):
        errors.append("provenance inventory contains duplicate paths")
    if any(row.get("current_effect") != "all_rights_reserved_no_permission_granted" for row in rows):
        errors.append("provenance inventory contains a premature outbound-license effect")
    if any("cleared" in str(row.get("provenance_status", "")).lower() for row in rows):
        errors.append("provenance inventory must not mark a path cleared before author/legal review")
    if decision.get("selected_option_id") != "delayed_opening" or decision.get("status") != "decided":
        errors.append("licensing provenance audit requires the decided delayed-opening policy")
    if inventory.get("decision_state") != "decided":
        errors.append("provenance inventory must record the decided policy state")
    for row in rows:
        path = str(row.get("path", ""))
        if path.startswith("sources/source_notes/ext_") and row.get("rule_id") != "external-source-commentary":
            errors.append(f"external source note escaped mixed-rights review: {path}")
        if (
            path.startswith("assets/")
            and Path(path).suffix.lower() in {".svg", ".png", ".jpg", ".jpeg", ".webp", ".gif", ".pdf", ".epub", ".docx", ".html"}
            and row.get("rule_id") != "figures-and-assets"
        ):
            errors.append(f"asset escaped asset-level provenance review: {path}")
    summary = inventory.get("summary", {})
    if summary.get("file_count") != len(rows):
        errors.append("provenance summary file count mismatch")
    return errors


def negative_controls(inventory: dict, expected: dict, decision: dict) -> list[str]:
    failures: list[str] = []
    removed = copy.deepcopy(inventory)
    removed["files"] = removed["files"][:-1]
    if not semantic_errors(removed, expected, decision):
        failures.append("negative control incorrectly accepted: omitted path")
    cleared = copy.deepcopy(inventory)
    cleared["files"][0]["provenance_status"] = "provenance_cleared"
    if not semantic_errors(cleared, expected, decision):
        failures.append("negative control incorrectly accepted: automatic clearance")
    source_laundering = copy.deepcopy(inventory)
    external = next(row for row in source_laundering["files"] if str(row["path"]).startswith("sources/source_notes/ext_"))
    external["rule_id"] = "public-metadata-and-governance-records"
    external["candidate_lane"] = "metadata_candidate"
    if not semantic_errors(source_laundering, expected, decision):
        failures.append("negative control incorrectly accepted: external-source metadata laundering")
    premature = copy.deepcopy(inventory)
    premature["files"][0]["current_effect"] = "CC-BY-4.0"
    if not semantic_errors(premature, expected, decision):
        failures.append("negative control incorrectly accepted: premature outbound license")
    return failures


def main() -> None:
    required = [POLICY, OUTPUT, DECISION, POLICY_SCHEMA, INVENTORY_SCHEMA, LICENSE, DOC]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
    if missing:
        raise SystemExit("missing licensing provenance artifacts: " + ", ".join(missing))
    policy = load_json(POLICY)
    inventory = load_json(OUTPUT)
    decision = load_json(DECISION)
    errors = validate_against_schema(policy, load_json(POLICY_SCHEMA), str(POLICY.relative_to(ROOT)))
    errors.extend(validate_against_schema(inventory, load_json(INVENTORY_SCHEMA), str(OUTPUT.relative_to(ROOT))))
    expected = build_inventory()
    errors.extend(semantic_errors(inventory, expected, decision))
    errors.extend(negative_controls(inventory, expected, decision))
    license_text = LICENSE.read_text(encoding="utf-8", errors="ignore")
    if "All rights reserved" not in license_text or "no license is granted" not in license_text:
        errors.append("operative LICENSE.md no longer preserves all-rights-reserved state")
    if errors:
        print("Licensing provenance inventory validation failed:")
        for error in errors:
            print(f" - {error}")
        raise SystemExit(1)
    print(
        f"Licensing provenance inventory passed: {inventory['summary']['file_count']} paths, "
        f"{inventory['summary']['unknown_quarantine_count']} unknown quarantine, "
        "0 paths cleared, and 4 rejecting negative controls."
    )


if __name__ == "__main__":
    main()
