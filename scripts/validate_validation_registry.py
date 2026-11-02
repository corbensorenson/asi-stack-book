#!/usr/bin/env python3
"""Validate the authoritative registry, exact overrides, and sole-source boundary."""

from __future__ import annotations

import copy
import json
import re
from pathlib import Path
import sys
from typing import Any

from build_validation_registry import OUTPUT, OVERRIDES, ROOT, authority_errors
from validation_projection_plan import graph_errors


VALIDATE_BOOK = ROOT / "scripts" / "validate_book.py"
REQUIRED_UNIT_FIELDS = (
    "id", "order", "script", "args", "execution_tier", "validation_class",
    "input_contract", "output_contract", "claim_scope", "negative_controls",
    "prohibited_inference",
)
EXACT_FIELDS = (
    "input_contract", "input_artifacts", "output_contract", "output_assertions",
    "claim_scope", "negative_controls", "negative_control_cases",
    "prohibited_inference", "contract_precision", "semantic_review_state",
)


def execution_errors(registry: dict[str, Any]) -> list[str]:
    errors = []
    defaults = registry.get("execution_defaults", {})
    fields = {'capabilities', 'side_effects', 'review_state', 'network', 'historical_mode',
              'timeout_seconds', 'depends_on'}
    if set(defaults) - fields:
        errors.append(f"execution defaults contain unknown fields: {sorted(set(defaults) - fields)}")
    ids = {unit.get("id") for unit in registry.get("units", [])} | {"base-gate"}
    for unit in registry.get("units", []):
        if set(unit.get('execution', {})) - fields:
            errors.append(f"{unit.get('id')}: unknown execution fields: {sorted(set(unit['execution']) - fields)}")
        contract = {**defaults, **unit.get("execution", {})}
        prefix = str(unit.get("id"))
        capabilities = contract.get("capabilities")
        if not isinstance(capabilities, list) or not capabilities or not all(isinstance(x, str) for x in capabilities):
            errors.append(f"{prefix}: execution capabilities must be explicit")
        elif any(name not in {'python', 'unix_process_groups'} and not re.fullmatch(
            r'(?:module|tool):[A-Za-z0-9_][A-Za-z0-9_.-]*', name
        ) for name in capabilities):
            errors.append(f"{prefix}: unknown capability name or malformed module/tool capability")
        if contract.get("side_effects") not in {"read_only", "ignored_outputs", "owned_tracked_outputs", "unreviewed"}:
            errors.append(f"{prefix}: invalid side-effect contract")
        if contract.get("review_state") not in {"reviewed", "unreviewed"}:
            errors.append(f"{prefix}: invalid execution review state")
        if contract.get("review_state") == "reviewed" and contract.get("side_effects") == "unreviewed":
            errors.append(f"{prefix}: reviewed contract has unknown side effects")
        budget = contract.get("timeout_seconds")
        if isinstance(budget, bool) or not isinstance(budget, (int, float)) or not 0 < budget <= 86400:
            errors.append(f"{prefix}: invalid execution budget")
        deps = contract.get("depends_on")
        if not isinstance(deps, list) or not all(isinstance(x, str) for x in deps):
            errors.append(f"{prefix}: dependencies must be a list")
            continue
        if any(dep not in ids or dep == prefix for dep in deps):
            errors.append(f"{prefix}: unknown or self dependency")
        positions = {row['id']: row['order'] for row in registry['units']}
        if any(dep != 'base-gate' and positions.get(dep, 0) >= unit['order'] for dep in deps):
            errors.append(f"{prefix}: dependencies must precede the consumer")
        if contract.get("network") not in {"none", "required", "unreviewed"}:
            errors.append(f"{prefix}: invalid network contract")
        if contract.get("historical_mode") not in {"current", "retained_commit", "frozen_bytes", "mixed", "unreviewed"}:
            errors.append(f"{prefix}: invalid custody contract")
    return errors


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def semantic_errors(registry: dict[str, Any]) -> list[str]:
    errors = authority_errors(registry)
    errors.extend(execution_errors(registry))
    errors.extend(graph_errors(registry))
    units = registry.get("units", [])
    artifacts = registry.get("required_artifacts", [])
    summary = registry.get("summary", {})
    if not isinstance(units, list) or not units:
        errors.append("registry units must be a non-empty list")
        units = []
    if not isinstance(artifacts, list) or not artifacts:
        errors.append("registry required_artifacts must be a non-empty list")
        artifacts = []
    if summary.get("unit_count") != len(units):
        errors.append("registry unit summary does not match units")
    if summary.get("required_artifact_count") != len(artifacts):
        errors.append("registry artifact summary does not match required_artifacts")
    if len(set(artifacts)) != len(artifacts):
        errors.append("registry required_artifacts contains duplicates")
    missing_artifacts = [path for path in artifacts if not isinstance(path, str) or not (ROOT / path).exists()]
    if missing_artifacts:
        errors.append(f"registry required artifacts missing: {missing_artifacts[:10]}")
    orders = [unit.get("order") for unit in units]
    if orders != list(range(1, len(units) + 1)):
        errors.append("registry unit order is not contiguous")
    ids = [unit.get("id") for unit in units]
    if len(set(ids)) != len(ids):
        errors.append("registry unit IDs are not unique")
    commands: list[tuple[str, tuple[str, ...]]] = []
    for unit in units:
        missing_fields = [field for field in REQUIRED_UNIT_FIELDS if not unit.get(field) and field not in {"args"}]
        if missing_fields:
            errors.append(f"{unit.get('id')}: missing required metadata {missing_fields}")
        script = unit.get("script", "")
        args = unit.get("args", [])
        if not isinstance(args, list) or not all(isinstance(arg, str) for arg in args):
            errors.append(f"{unit.get('id')}: args must be a string list")
            args = []
        commands.append((script, tuple(args)))
        if not isinstance(script, str) or not (ROOT / "scripts" / script).exists():
            errors.append(f"missing registry script: {script}")
        if unit.get("execution_tier") not in registry.get("tier_order", []):
            errors.append(f"{unit.get('id')}: unknown execution tier")
        if unit.get("validation_class") not in registry.get("class_contracts", {}):
            errors.append(f"{unit.get('id')}: unknown validation class")
    if len(set(commands)) != len(commands):
        errors.append("registry contains duplicate script/argument commands")
    if {unit.get("execution_tier") for unit in units} != {"pr", "deep", "release"}:
        errors.append("registry must contain pr, deep, and release units")
    base = registry.get("base_gate", {})
    if base != {"script": "validate_book.py", "environment": {}}:
        errors.append("base gate must be validate_book.py with no legacy child-suppression environment")
    validate_book = VALIDATE_BOOK.read_text(encoding="utf-8", errors="ignore")
    for forbidden in ("run_validator(", "ASI_VALIDATION_REGISTRY_CHILD", "REQUIRED = ["):
        if forbidden in validate_book:
            errors.append(f"validate_book.py retains legacy inventory/orchestration marker: {forbidden}")
    for required in ("REGISTRY = ROOT / \"validation\" / \"registry.json\"", "registry_required_artifacts"):
        if required not in validate_book:
            errors.append(f"validate_book.py does not consume registry authority: {required}")

    override_data = load(OVERRIDES)
    override_rows = override_data.get("contracts", [])
    override_keys = [(row.get("script"), tuple(row.get("args", []))) for row in override_rows]
    if len(set(override_keys)) != len(override_keys):
        errors.append("exact contract overrides contain duplicate commands")
    if len(override_rows) < 18:
        errors.append("high-impact exact contract audit unexpectedly covers fewer than 18 units")
    by_command = {(unit.get("script"), tuple(unit.get("args", []))): unit for unit in units}
    for row, key in zip(override_rows, override_keys):
        unit = by_command.get(key)
        if unit is None:
            errors.append(f"exact contract override does not resolve: {key}")
            continue
        for field in EXACT_FIELDS:
            if unit.get(field) != row.get(field):
                errors.append(f"{unit.get('id')}: exact contract field {field} differs from override")
    exact_units = [unit for unit in units if unit.get("contract_precision") == "exact_high_impact"]
    if len(exact_units) != len(override_rows):
        errors.append("registry exact-contract count differs from override source")
    return errors


def negative_controls(registry: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    duplicate_order = copy.deepcopy(registry)
    duplicate_order["units"][1]["order"] = duplicate_order["units"][0]["order"]
    missing_script = copy.deepcopy(registry)
    missing_script["units"][0]["script"] = "missing_validator.py"
    missing_override = copy.deepcopy(registry)
    for unit in missing_override["units"]:
        if unit.get("contract_precision") == "exact_high_impact":
            unit["contract_precision"] = "inherited"
            break
    legacy = copy.deepcopy(registry)
    legacy["legacy_source"] = "scripts/validate_book.py"
    invalid_budget = copy.deepcopy(registry)
    invalid_budget["execution_defaults"]["timeout_seconds"] = 0
    dependency_cycle = copy.deepcopy(registry)
    dependency_cycle["units"][0].setdefault("execution", {})["depends_on"] = [dependency_cycle["units"][0]["id"]]
    unknown_field = copy.deepcopy(registry)
    unknown_field['execution_defaults']['network_access'] = 'none'
    missing_graph = copy.deepcopy(registry)
    missing_graph.pop('current_projections')
    historical_refresh = copy.deepcopy(registry)
    historical_refresh['current_projections'][0]['mode'] = 'historical'
    escaped_output = copy.deepcopy(registry)
    escaped_output['current_projections'][0]['outputs'] = ['../outside']
    missing_consumer = copy.deepcopy(registry)
    missing_consumer['current_projections'][0]['checks'] = ['not-a-registered-consumer']
    projection_cycle = copy.deepcopy(registry)
    projection_cycle['current_projections'][0]['depends_on'] = [projection_cycle['current_projections'][-1]['id']]
    controls = (
        ("duplicate order", duplicate_order),
        ("missing script", missing_script),
        ("unresolved exact override", missing_override),
        ("legacy authority marker", legacy),
        ("invalid execution budget", invalid_budget),
        ("dependency cycle", dependency_cycle),
        ("unknown execution field", unknown_field),
        ("missing current projection graph", missing_graph),
        ("historical object in current rebuild graph", historical_refresh),
        ("projection output escapes repository", escaped_output),
        ("unregistered projection consumer", missing_consumer),
        ("projection dependency cycle", projection_cycle),
    )
    for label, mutation in controls:
        if not semantic_errors(mutation):
            failures.append(f"negative control was incorrectly accepted: {label}")
    return failures


def main() -> None:
    registry = load(OUTPUT)
    errors = semantic_errors(registry)
    if not errors:
        errors.extend(negative_controls(registry))
    else:
        print("Registry negative controls skipped: the canonical baseline is invalid.")
    if errors:
        print("Validation registry validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)
    counts = {tier: sum(unit["execution_tier"] == tier for unit in registry["units"]) for tier in registry["tier_order"]}
    exact = sum(unit.get("contract_precision") == "exact_high_impact" for unit in registry["units"])
    print(
        f"Authoritative validation registry passed: {len(registry['units'])} units, "
        f"{len(registry['required_artifacts'])} artifacts, {exact} exact high-impact contracts, "
        f"tiers={counts}, 12 rejecting negative controls."
    )


if __name__ == "__main__":
    main()
