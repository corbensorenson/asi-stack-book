#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

from run_vcm_resolver_certificate_probe import (
    EXPECTED_INVALID_IDS,
    NON_CLAIMS,
    PROBE_ID,
    RESULT,
    RESULT_COMMAND,
    ROOT,
    VALID_SCENARIO_IDS,
    decision_digest,
)


DOC = ROOT / "docs" / "vcm_resolver_certificate_probe.md"
STRUCTURE = ROOT / "book_structure.json"
OUTLINE = ROOT / "docs" / "book_outline.md"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
LIVE_CHAPTER = ROOT / "chapters" / "virtual-context-abi.qmd"
READER_CHAPTER = ROOT / "editions" / "reader_manuscript" / "v1_0" / "chapters" / "virtual-context-abi.qmd"
README = ROOT / "README.md"
PUBLICATION = ROOT / "docs" / "publication_readiness.md"
STATUS = ROOT / "docs" / "v1_0_candidate_status.md"

SURFACE_FRAGMENTS = (
    "VCM resolver/certificate probe",
    "valid_resolver_materialization_receipt",
    "valid_mandatory_miss_typed_fault",
    "invalid_address_mismatch_materialization_denied",
    "invalid_version_mismatch_materialization_denied",
    "invalid_snapshot_mismatch_materialization_denied",
    "invalid_mount_policy_denied",
    "invalid_lease_expired_reuse_blocked",
    "invalid_certificate_source_binding_mismatch_denied",
    "invalid_certificate_authority_escalation_denied",
    "invalid_certificate_truthfulness_overclaim_denied",
    "invalid_summary_fidelity_omission_denied",
    "no deployed-resolver, memory-store, context-compiler, open-domain-summary-fidelity, certificate-truthfulness, transaction-isolation, deletion-enforcement, model-facing-context-quality, VCM-Bench, leak-prevention, or support-state-promotion claim",
)

REQUIRED_NON_CLAIM_TERMS = (
    "does not promote any chapter core claim",
    "does not create a support-state transition",
    "deployed resolver correctness",
    "memory-store behavior",
    "planner-guided context compilation",
    "open-domain summary fidelity",
    "certificate truthfulness",
    "transaction isolation",
    "deletion enforcement",
    "model-facing context quality",
    "VCM-Bench performance",
    "leak prevention",
    "does not read private source text",
)

EXPECTED_VALID_ROUTES = {
    "valid_resolver_materialization_receipt": "materialize_context",
    "valid_mandatory_miss_typed_fault": "issue_typed_fault",
}

EXPECTED_INVALID_ROUTES = {
    "invalid_address_mismatch_materialization_denied": "issue_typed_fault",
    "invalid_version_mismatch_materialization_denied": "issue_typed_fault",
    "invalid_snapshot_mismatch_materialization_denied": "issue_typed_fault",
    "invalid_mount_policy_denied": "deny_mount_policy",
    "invalid_lease_expired_reuse_blocked": "deny_expired_lease",
    "invalid_certificate_source_binding_mismatch_denied": "reject_source_binding_mismatch",
    "invalid_certificate_authority_escalation_denied": "reject_authority_escalation",
    "invalid_certificate_truthfulness_overclaim_denied": "reject_truthfulness_overclaim",
    "invalid_summary_fidelity_omission_denied": "reject_undeclared_omission",
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def text_blob(value: Any) -> str:
    if isinstance(value, dict):
        return "\n".join(f"{key}: {text_blob(child)}" for key, child in value.items())
    if isinstance(value, list):
        return "\n".join(text_blob(item) for item in value)
    return str(value)


def normalize(text: str) -> str:
    return " ".join(text.lower().split())


def require_fragments(owner: str, text: str, fragments: tuple[str, ...], errors: list[str]) -> None:
    normalized = normalize(text)
    for fragment in fragments:
        if normalize(fragment) not in normalized:
            errors.append(f"{owner} missing required fragment: {fragment}")


def chapter_record(structure: dict[str, Any], chapter_id: str) -> dict[str, Any]:
    for part in structure.get("parts", []):
        if not isinstance(part, dict):
            continue
        for chapter in part.get("chapters", []):
            if isinstance(chapter, dict) and chapter.get("id") == chapter_id:
                return chapter
    return {}


def fail(errors: list[str]) -> None:
    print("VCM resolver/certificate probe validation failed:", file=sys.stderr)
    for error in errors:
        print(f" - {error}", file=sys.stderr)
    raise SystemExit(1)


def require_sha(value: Any, owner: str, errors: list[str]) -> None:
    if not re.fullmatch(r"[0-9a-f]{64}", str(value)):
        errors.append(f"{owner} must be a SHA-256 hex digest.")


def require_no_overclaim_effects(scenario: dict[str, Any], owner: str, errors: list[str]) -> None:
    outcome = scenario.get("outcome", {})
    if outcome.get("model_called") is not False:
        errors.append(f"{owner}: model_called must be false.")
    if outcome.get("network_used") is not False:
        errors.append(f"{owner}: network_used must be false.")
    if outcome.get("private_source_read") is not False:
        errors.append(f"{owner}: private_source_read must be false.")
    if outcome.get("support_state_effect") != "none":
        errors.append(f"{owner}: support_state_effect must be none.")
    if outcome.get("chapter_core_support_effect") != "none":
        errors.append(f"{owner}: chapter_core_support_effect must be none.")


def main() -> None:
    errors: list[str] = []
    paths = (RESULT, DOC, STRUCTURE, OUTLINE, ROADMAP, LIVE_CHAPTER, READER_CHAPTER, README, PUBLICATION, STATUS)
    for path in paths:
        if not path.exists():
            errors.append(f"Missing {rel(path)}.")
    if errors:
        fail(errors)

    result = load_json(RESULT)
    structure = load_json(STRUCTURE)
    blob = text_blob(result)
    if "/Users/" in blob or "/var/folders/" in blob:
        errors.append(f"{rel(RESULT)} must not publish local absolute paths.")

    expected_scalars = {
        "probe_id": PROBE_ID,
        "record_kind": "vcm_resolver_certificate_probe",
        "command": RESULT_COMMAND,
        "local_only": True,
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
        "pass": True,
    }
    for key, expected in expected_scalars.items():
        if result.get(key) != expected:
            errors.append(f"{rel(RESULT)}: {key} must be {expected!r}.")
    if not isinstance(result.get("recorded_at_utc"), str) or not result["recorded_at_utc"].endswith("Z"):
        errors.append(f"{rel(RESULT)}: recorded_at_utc must end with Z.")

    source = result.get("synthetic_source_cell", {})
    if source.get("cell_id") != "cell://vcm-probe/source/vcm-public-static-abi":
        errors.append(f"{rel(RESULT)}: synthetic_source_cell.cell_id mismatch.")
    require_sha(source.get("facts_sha256"), f"{rel(RESULT)} synthetic_source_cell.facts_sha256", errors)
    if source.get("fact_keys") != ["authority_boundary", "fault_contract", "stable_address"]:
        errors.append(f"{rel(RESULT)}: synthetic_source_cell.fact_keys mismatch.")

    valid = result.get("valid_scenarios", [])
    invalid = result.get("expected_invalid_controls", [])
    if not isinstance(valid, list) or len(valid) != 2:
        errors.append(f"{rel(RESULT)}: expected two valid scenarios.")
        valid = []
    if not isinstance(invalid, list) or len(invalid) != 9:
        errors.append(f"{rel(RESULT)}: expected nine invalid controls.")
        invalid = []

    seen_valid = {scenario.get("scenario_id") for scenario in valid if isinstance(scenario, dict)}
    seen_invalid = {scenario.get("scenario_id") for scenario in invalid if isinstance(scenario, dict)}
    if seen_valid != VALID_SCENARIO_IDS:
        errors.append(f"{rel(RESULT)}: valid scenario ids mismatch: {sorted(seen_valid)}.")
    if seen_invalid != EXPECTED_INVALID_IDS:
        errors.append(f"{rel(RESULT)}: invalid control ids mismatch: {sorted(seen_invalid)}.")

    for scenario in valid:
        scenario_id = scenario.get("scenario_id")
        owner = f"{rel(RESULT)} {scenario_id}"
        if scenario.get("expected_valid") is not True:
            errors.append(f"{owner}: expected_valid must be true.")
        if scenario.get("actual_route") != EXPECTED_VALID_ROUTES.get(scenario_id):
            errors.append(f"{owner}: route mismatch.")
        if scenario.get("scenario_pass") is not True:
            errors.append(f"{owner}: scenario_pass must be true.")
        require_no_overclaim_effects(scenario, owner, errors)
        outcome = scenario.get("outcome", {})
        if scenario_id == "valid_resolver_materialization_receipt":
            if outcome.get("materialization_emitted") is not True:
                errors.append(f"{owner}: materialization_emitted must be true.")
        if scenario_id == "valid_mandatory_miss_typed_fault":
            if outcome.get("typed_fault_emitted") is not True:
                errors.append(f"{owner}: typed_fault_emitted must be true.")
            if outcome.get("materialization_emitted") is not False:
                errors.append(f"{owner}: typed fault must not emit materialization.")

    for scenario in invalid:
        scenario_id = scenario.get("scenario_id")
        owner = f"{rel(RESULT)} {scenario_id}"
        if scenario.get("expected_valid") is not False:
            errors.append(f"{owner}: expected_valid must be false.")
        if scenario.get("actual_route") != EXPECTED_INVALID_ROUTES.get(scenario_id):
            errors.append(f"{owner}: route mismatch.")
        if scenario.get("scenario_pass") is not True:
            errors.append(f"{owner}: scenario_pass must be true.")
        require_no_overclaim_effects(scenario, owner, errors)
        if scenario.get("outcome", {}).get("materialization_emitted") is not False:
            errors.append(f"{owner}: invalid controls must not emit materialization.")

    summary = result.get("summary", {})
    if summary.get("valid_scenarios") != 2:
        errors.append(f"{rel(RESULT)}: summary.valid_scenarios must be 2.")
    if summary.get("expected_invalid_controls") != 9:
        errors.append(f"{rel(RESULT)}: summary.expected_invalid_controls must be 9.")
    expected_digest = decision_digest(valid, invalid)
    if summary.get("decision_digest") != expected_digest:
        errors.append(f"{rel(RESULT)}: decision_digest mismatch.")
    require_sha(summary.get("decision_digest"), f"{rel(RESULT)} summary.decision_digest", errors)

    if result.get("non_claims") != NON_CLAIMS:
        errors.append(f"{rel(RESULT)}: non_claims must match runner boundaries.")
    require_fragments(rel(RESULT), text_blob(result.get("non_claims", [])), REQUIRED_NON_CLAIM_TERMS, errors)

    for owner, path in (
        (rel(DOC), DOC),
        (rel(OUTLINE), OUTLINE),
        (rel(ROADMAP), ROADMAP),
        (rel(LIVE_CHAPTER), LIVE_CHAPTER),
        (rel(READER_CHAPTER), READER_CHAPTER),
        (rel(README), README),
        (rel(PUBLICATION), PUBLICATION),
        (rel(STATUS), STATUS),
    ):
        require_fragments(owner, path.read_text(encoding="utf-8"), SURFACE_FRAGMENTS, errors)

    record = chapter_record(structure, "virtual-context-abi")
    if record.get("evidence_level") != "argument":
        errors.append("virtual-context-abi: evidence_level must remain argument.")
    require_fragments(
        "book_structure virtual-context-abi tests",
        text_blob(record.get("codex_tests", [])),
        (
            "VCM resolver/certificate probe",
            "valid_resolver_materialization_receipt",
            "valid_mandatory_miss_typed_fault",
            "nine expected-invalid controls",
            "no deployed-resolver, memory-store, context-compiler, open-domain-summary-fidelity, certificate-truthfulness, transaction-isolation, deletion-enforcement, model-facing-context-quality, VCM-Bench, leak-prevention, or support-state-promotion claim",
        ),
        errors,
    )

    if errors:
        fail(errors)
    print(
        "VCM resolver/certificate probe validation passed: "
        "2 valid routes and 9 expected-invalid controls checked with no deployed resolver or support-state movement."
    )


if __name__ == "__main__":
    main()
