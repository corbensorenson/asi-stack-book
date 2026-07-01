#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

from validate_protocol_examples import validate_value


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "experiments" / "routing_decision_lease" / "fixtures"
SCHEMAS = {
    "specialist_registry": ROOT / "schemas" / "specialist_registry_record.schema.json",
    "routing_decision": ROOT / "schemas" / "routing_decision_record.schema.json",
    "moecot_orchestration": ROOT / "schemas" / "moecot_orchestration_record.schema.json",
}
READY_STATES = {"canary", "qualified", "default"}
SOURCE_ONLY_STATES = {"design_example", "source_reported"}
PROMOTED_SOURCE_STATES = {"imported_artifact", "locally_reproduced"}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def fixture_expectation(path: Path) -> bool | None:
    if path.name.startswith("valid_"):
        return True
    if path.name.startswith("invalid_"):
        return False
    return None


def text_blob(*values: Any) -> str:
    pieces: list[str] = []
    for value in values:
        if isinstance(value, list):
            pieces.extend(str(item) for item in value)
        elif isinstance(value, dict):
            pieces.extend(f"{key}: {child}" for key, child in value.items())
        else:
            pieces.append(str(value))
    return "\n".join(pieces).lower()


def require_object(record: dict[str, Any], field: str, errors: list[str], relative: str) -> dict[str, Any]:
    value = record.get(field)
    if not isinstance(value, dict):
        errors.append(f"{relative}: {field} must be an object.")
        return {}
    return value


def require_list(record: dict[str, Any], field: str, errors: list[str], relative: str, *, nonempty: bool = False) -> list[Any]:
    value = record.get(field)
    if not isinstance(value, list) or (nonempty and not value):
        kind = "a non-empty list" if nonempty else "a list"
        errors.append(f"{relative}: {field} must be {kind}.")
        return []
    return value


def require_boundary(items: list[Any], errors: list[str], relative: str) -> None:
    blob = text_blob(items)
    if "does not" not in blob:
        errors.append(f"{relative}: non_claims must include explicit 'does not' boundaries.")
    if "promote" not in blob and "support state" not in blob:
        errors.append(f"{relative}: non_claims must mention support-state non-promotion.")


def schema_errors(value: dict[str, Any], schemas: dict[str, Any], relative: str) -> list[str]:
    errors: list[str] = []
    registries = value.get("specialist_registry")
    if not isinstance(registries, list) or not registries:
        errors.append(f"{relative}: specialist_registry must be a non-empty list.")
    else:
        for index, registry in enumerate(registries):
            errors.extend(validate_value(registry, schemas["specialist_registry"], f"{relative}:specialist_registry[{index}]"))
    for field in ("routing_decision", "moecot_orchestration"):
        record = value.get(field)
        if not isinstance(record, dict):
            errors.append(f"{relative}: {field} must be an object.")
            continue
        errors.extend(validate_value(record, schemas[field], f"{relative}:{field}"))
    return errors


def registry_by_id(registries: list[Any]) -> dict[str, dict[str, Any]]:
    return {
        str(record.get("specialist_id")): record
        for record in registries
        if isinstance(record, dict) and record.get("specialist_id")
    }


def has_capabilities(registry: dict[str, Any], required: set[str]) -> bool:
    capabilities = {str(item) for item in registry.get("capabilities", [])}
    return required.issubset(capabilities)


def is_ready(registry: dict[str, Any]) -> bool:
    return str(registry.get("readiness_state", "")) in READY_STATES


def semantic_errors(value: dict[str, Any], relative: str) -> list[str]:
    errors: list[str] = []
    non_claims = require_list(value, "non_claims", errors, relative, nonempty=True)
    if non_claims:
        require_boundary(non_claims, errors, f"{relative}:non_claims")

    routing = require_object(value, "routing_decision", errors, relative)
    moecot = require_object(value, "moecot_orchestration", errors, relative)
    registries = value.get("specialist_registry")
    if not isinstance(registries, list) or not registries:
        errors.append(f"{relative}: specialist_registry must be a non-empty list.")
        registries = []
    if errors:
        return errors

    for record_name, record in (
        ("routing_decision", routing),
        ("moecot_orchestration", moecot),
    ):
        record_non_claims = require_list(record, "non_claims", errors, f"{relative}:{record_name}", nonempty=True)
        if record_non_claims:
            require_boundary(record_non_claims, errors, f"{relative}:{record_name}.non_claims")
    for index, registry in enumerate(registries):
        if not isinstance(registry, dict):
            errors.append(f"{relative}: specialist_registry[{index}] must be an object.")
            continue
        registry_non_claims = require_list(registry, "non_claims", errors, f"{relative}:specialist_registry[{index}]", nonempty=True)
        if registry_non_claims:
            require_boundary(registry_non_claims, errors, f"{relative}:specialist_registry[{index}].non_claims")

    by_id = registry_by_id(registries)
    required_capabilities = {str(item) for item in require_list(value, "required_capabilities", errors, relative, nonempty=True)}
    ranks = value.get("authority_ranks")
    if not isinstance(ranks, dict) or not ranks:
        errors.append(f"{relative}: authority_ranks must be a non-empty object.")
        ranks = {}
    max_rank = value.get("max_authority_rank")
    if not isinstance(max_rank, int):
        errors.append(f"{relative}: max_authority_rank must be an integer.")
        max_rank = 0

    selected = str(routing.get("selected_specialist", ""))
    fallback_route = str(routing.get("fallback_route", ""))
    candidates = {str(item) for item in routing.get("candidate_specialists", [])}
    rejected = {str(item) for item in routing.get("rejected_candidates", [])}
    non_selection_blob = text_blob(routing.get("non_selection_evidence", []))
    granted_authority = {
        str(item)
        for item in require_list(
            routing,
            "granted_authority_subset",
            errors,
            f"{relative}:routing_decision",
        )
    }
    expected_route = str(value.get("expected_route", ""))
    if expected_route not in {"selected", "fallback", "residual", "blocked"}:
        errors.append(f"{relative}: expected_route must be selected, fallback, residual, or blocked.")
    if selected not in candidates:
        errors.append(f"{relative}: selected_specialist must be listed in candidate_specialists.")
    if selected not in by_id:
        errors.append(f"{relative}: selected_specialist must have a specialist registry record.")
    missing_candidates = sorted(candidates - set(by_id))
    if missing_candidates:
        errors.append(f"{relative}: every candidate specialist must have a registry record; missing {missing_candidates}.")
    if fallback_route not in candidates:
        errors.append(f"{relative}: fallback_route must also be a candidate specialist.")

    selected_registry = by_id.get(selected, {})
    if selected_registry:
        selected_envelope = {str(item) for item in selected_registry.get("authority_envelope", [])}
        outside_envelope = sorted(granted_authority - selected_envelope)
        if outside_envelope:
            errors.append(
                f"{relative}: granted_authority_subset contains authority outside "
                f"the selected specialist envelope: {outside_envelope}."
            )

    for expected in value.get("expected_rejections", []):
        if not isinstance(expected, dict):
            errors.append(f"{relative}: expected_rejections entries must be objects.")
            continue
        candidate = str(expected.get("specialist_id", ""))
        if candidate not in rejected:
            errors.append(f"{relative}: expected rejected candidate {candidate!r} is not listed in rejected_candidates.")
        for token in expected.get("must_mention", []):
            if str(token).lower() not in non_selection_blob:
                errors.append(f"{relative}: non_selection_evidence must mention {token!r} for rejected candidate {candidate!r}.")

    eligible: list[tuple[int, str]] = []
    overprivileged: list[str] = []
    for candidate in candidates:
        registry = by_id.get(candidate)
        if not registry:
            continue
        rank = ranks.get(candidate)
        if not isinstance(rank, int):
            errors.append(f"{relative}: authority_ranks missing integer rank for {candidate}.")
            continue
        if rank > max_rank:
            overprivileged.append(candidate)
        if has_capabilities(registry, required_capabilities) and is_ready(registry) and rank <= max_rank:
            eligible.append((rank, candidate))

    if expected_route == "selected":
        if not eligible:
            errors.append(f"{relative}: selected route requires at least one eligible specialist.")
        else:
            best_rank = min(rank for rank, _candidate in eligible)
            best_candidates = {candidate for rank, candidate in eligible if rank == best_rank}
            if selected not in best_candidates:
                errors.append(f"{relative}: selected_specialist must be one of the least-authority eligible specialists {sorted(best_candidates)}.")
        if selected_registry and not has_capabilities(selected_registry, required_capabilities):
            errors.append(f"{relative}: selected specialist does not cover required capabilities.")
        if selected_registry and not is_ready(selected_registry):
            errors.append(f"{relative}: selected specialist readiness_state is not canary, qualified, or default.")
        if routing.get("authority_check") != "passed":
            errors.append(f"{relative}: selected route requires authority_check passed.")
        if routing.get("readiness_check") != "ready":
            errors.append(f"{relative}: selected route requires readiness_check ready.")
    else:
        if selected != fallback_route and routing.get("route_shape") != "fallback":
            errors.append(f"{relative}: fallback/residual/blocked route must select the fallback route or declare route_shape fallback.")
        require_list(routing, "residuals", errors, f"{relative}:routing_decision", nonempty=True)
        if not str(routing.get("residual_owner", "")).strip():
            errors.append(f"{relative}: fallback/residual route must name a residual_owner.")

    if overprivileged and not routing.get("denied_authority"):
        errors.append(f"{relative}: overprivileged candidates require denied_authority entries.")
    for candidate in overprivileged:
        if candidate == selected:
            errors.append(f"{relative}: selected_specialist cannot exceed max_authority_rank.")
        if candidate not in rejected:
            errors.append(f"{relative}: overprivileged candidate {candidate} must be rejected.")

    stale_or_expired = "expired" in text_blob(routing.get("context_lease"), routing.get("tool_lease"), routing.get("expiry"))
    if stale_or_expired and expected_route == "selected":
        errors.append(f"{relative}: expired route lease cannot remain selected.")
    if stale_or_expired and not routing.get("residuals"):
        errors.append(f"{relative}: expired route lease requires residuals.")

    runtime_state = str(moecot.get("runtime_packet_state", ""))
    source_claim_state = str(moecot.get("source_claim_state", ""))
    locally_reproduced = moecot.get("locally_reproduced_fields", [])
    replay_refs = moecot.get("replay_refs", [])
    if runtime_state in SOURCE_ONLY_STATES and not locally_reproduced:
        if source_claim_state in PROMOTED_SOURCE_STATES:
            errors.append(f"{relative}: source-only MoECOT packet cannot claim imported or locally reproduced source state.")
        require_list(moecot, "promotion_blockers", errors, f"{relative}:moecot_orchestration", nonempty=True)
        require_list(moecot, "missing_replay_refs", errors, f"{relative}:moecot_orchestration", nonempty=True)
    if source_claim_state in PROMOTED_SOURCE_STATES:
        if not locally_reproduced:
            errors.append(f"{relative}: promoted MoECOT source state requires locally_reproduced_fields.")
        if not replay_refs or "not-run" in text_blob(replay_refs):
            errors.append(f"{relative}: promoted MoECOT source state requires concrete replay_refs.")

    return errors


def main() -> None:
    schemas = {name: load_json(path) for name, path in SCHEMAS.items()}
    fixtures = sorted(FIXTURE_DIR.glob("*.json"))
    if not fixtures:
        raise SystemExit(f"No routing decision lease fixtures found in {FIXTURE_DIR.relative_to(ROOT)}.")

    errors: list[str] = []
    valid_count = 0
    invalid_count = 0
    for fixture in fixtures:
        relative = str(fixture.relative_to(ROOT))
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
            errors.append(f"{relative}: scenario must contain a JSON object.")
            continue
        scenario_errors = schema_errors(value, schemas, relative)
        if not scenario_errors:
            scenario_errors.extend(semantic_errors(value, relative))
        if expect_valid:
            valid_count += 1
            errors.extend(scenario_errors)
        else:
            invalid_count += 1
            if not scenario_errors:
                errors.append(f"{relative}: invalid fixture unexpectedly passed routing decision lease checks.")

    if errors:
        print("Routing decision lease harness failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    print(
        "Routing decision lease harness passed: "
        f"{valid_count} valid fixture(s), {invalid_count} expected-invalid fixture(s)."
    )


if __name__ == "__main__":
    main()
