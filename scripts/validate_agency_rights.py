#!/usr/bin/env python3
"""Validate synthetic agency-rights checklist fixtures."""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

from validate_protocol_examples import validate_value


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "experiments" / "agency_rights" / "fixtures"
SCHEMA = ROOT / "schemas" / "agency_rights_checklist.schema.json"

HIGH_STAKES_TERMS = {
    "external",
    "financial",
    "high",
    "irreversible",
    "legal",
    "medical",
    "public release",
    "replacement",
    "safety",
    "self-modification",
}
GOOD_REVIEW_TERMS = {"approval", "governance", "human", "maintainer", "owner", "review"}
GOOD_APPEAL_TERMS = {"appeal", "human", "issue", "maintainer", "override", "review", "tribunal"}
GOOD_USABILITY_TERMS = {
    "accessible",
    "available",
    "direct",
    "export",
    "interface",
    "reachable",
    "repository",
    "review",
    "usable",
}
BAD_USABILITY_TERMS = {
    "after the fact",
    "hidden",
    "inaccessible",
    "no interface",
    "not available",
    "policy only",
    "unavailable",
}
GOOD_TIMING_TERMS = {"before", "pre-effect", "pre effect", "prior"}
BAD_TIMING_TERMS = {"after irreversible", "after publish", "after the effect", "post-hoc", "retroactive only"}
GOOD_ROLLBACK_TERMS = {"cancel", "pause", "revert", "rollback", "shutdown", "stop"}
BAD_ROLLBACK_TERMS = {"impossible", "no rollback", "none", "not available"}
BAD_PRINCIPAL_TERMS = {"autonomous system", "no one", "none", "system itself"}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def as_text(value: Any) -> str:
    if isinstance(value, list):
        return " ".join(as_text(item) for item in value)
    if isinstance(value, dict):
        return " ".join(f"{key} {as_text(child)}" for key, child in value.items())
    return str(value)


def contains_any(text: str, terms: set[str]) -> bool:
    return any(term in text for term in terms)


def nonempty_list(record: dict[str, Any], key: str) -> bool:
    return isinstance(record.get(key), list) and bool(record[key])


def denial_or_degradation_applies(record: dict[str, Any]) -> bool:
    reason = str(record.get("denial_or_degradation_reason", "")).strip().lower()
    return reason not in {"", "none", "none for this low-risk fixture", "no denial", "not applicable"}


def is_high_stakes(record: dict[str, Any]) -> bool:
    text = " ".join(
        str(record.get(key, "")).lower()
        for key in ("delegation_scope", "manipulation_risk", "reversibility", "timing_requirement")
    )
    return contains_any(text, HIGH_STAKES_TERMS)


def semantic_errors(record: dict[str, Any], relative: str) -> list[str]:
    errors: list[str] = []
    material_usability = str(record.get("material_usability", "")).lower()
    timing = str(record.get("timing_requirement", "")).lower()
    review = str(record.get("review_channel", "")).lower()
    appeal = str(record.get("appeal_channel", "")).lower()
    rollback = str(record.get("shutdown_or_rollback_path", "")).lower()
    principal = str(record.get("accountable_principal", "")).lower()
    delegation = str(record.get("delegation_scope", "")).lower()
    residual_text = as_text(record.get("residual_dependency_risk", [])).lower()

    if not nonempty_list(record, "affected_parties"):
        errors.append(f"{relative}: affected_parties must be non-empty.")

    if contains_any(delegation, {"all authority", "unbounded", "unlimited"}):
        errors.append(f"{relative}: delegation_scope cannot erase authority boundaries.")

    if contains_any(material_usability, BAD_USABILITY_TERMS) or not contains_any(material_usability, GOOD_USABILITY_TERMS):
        errors.append(f"{relative}: material_usability must name a reachable usable interface, export, review path, or repository artifact.")

    if contains_any(timing, BAD_TIMING_TERMS) or not contains_any(timing, GOOD_TIMING_TERMS):
        errors.append(f"{relative}: timing_requirement must preserve review before the relevant effect.")

    if not contains_any(review, GOOD_REVIEW_TERMS):
        errors.append(f"{relative}: review_channel must route to a human, maintainer, owner, governance, approval, or review path.")

    if not contains_any(appeal, GOOD_APPEAL_TERMS):
        errors.append(f"{relative}: appeal_channel must preserve a usable appeal, human override, review, issue, or tribunal path.")

    if contains_any(rollback, BAD_ROLLBACK_TERMS) or not contains_any(rollback, GOOD_ROLLBACK_TERMS):
        errors.append(f"{relative}: shutdown_or_rollback_path must name a usable stop, pause, cancel, rollback, shutdown, or revert path.")

    if contains_any(principal, BAD_PRINCIPAL_TERMS):
        errors.append(f"{relative}: accountable_principal cannot be empty or the autonomous system itself.")

    if is_high_stakes(record):
        if record.get("approval_required") is not True:
            errors.append(f"{relative}: high-impact, irreversible, or public effects require approval_required true.")
        if "approval" not in review and "human" not in review and "maintainer" not in review:
            errors.append(f"{relative}: high-impact effects require human, maintainer, or approval review.")

    if denial_or_degradation_applies(record):
        if not nonempty_list(record, "residual_dependency_risk"):
            errors.append(f"{relative}: denied or degraded rights must preserve residual_dependency_risk.")
        if "residual" not in residual_text and "risk" not in residual_text:
            errors.append(f"{relative}: residual_dependency_risk must describe the preserved residual risk.")

    return errors


def fixture_expectation(path: Path) -> bool | None:
    if path.name.startswith("valid_"):
        return True
    if path.name.startswith("invalid_"):
        return False
    return None


def main() -> None:
    schema = load_json(SCHEMA)
    fixtures = sorted(FIXTURE_DIR.glob("*.json"))
    if not fixtures:
        raise SystemExit(f"No agency-rights fixtures found in {rel(FIXTURE_DIR)}.")

    errors: list[str] = []
    valid_count = 0
    invalid_count = 0
    for fixture in fixtures:
        relative = rel(fixture)
        expect_valid = fixture_expectation(fixture)
        if expect_valid is None:
            errors.append(f"{relative}: fixture name must start with valid_ or invalid_.")
            continue
        try:
            value = load_json(fixture)
        except Exception as exc:
            errors.append(f"{relative}: invalid JSON: {exc}")
            continue
        if not isinstance(value, dict):
            errors.append(f"{relative}: top-level fixture must be an object.")
            continue

        fixture_errors = validate_value(value, schema, relative) + semantic_errors(value, relative)
        if expect_valid:
            valid_count += 1
            errors.extend(fixture_errors)
        else:
            invalid_count += 1
            if not fixture_errors:
                errors.append(f"{relative}: expected invalid fixture passed validation.")

    if errors:
        print("Agency rights harness failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    print(
        "Agency rights harness passed: "
        f"{valid_count} valid fixture(s), {invalid_count} expected-invalid fixture(s)."
    )


if __name__ == "__main__":
    main()
