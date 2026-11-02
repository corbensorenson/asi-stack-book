"""Inspect current projection dependencies declared in the validation registry.

This plans invalidation and named checks. It cannot approve prose, refresh a
review receipt, reopen historical evidence, or execute a rebuild.
"""

from __future__ import annotations

import fnmatch
import json
from functools import lru_cache
from pathlib import Path, PurePosixPath

from run_validation_registry import execution_contract


@lru_cache(maxsize=8192)
def normalized_path(value: str) -> str:
    path = PurePosixPath(value)
    if not value or path.is_absolute() or ".." in path.parts or "\\" in value or path.as_posix() != value:
        raise ValueError(f"expected a normalized repository-relative path: {value!r}")
    return value


def matches(path: str, selector: str) -> bool:
    normalized_path(path)
    normalized_path(selector)
    return fnmatch.fnmatchcase(path, selector)


def graph_errors(registry: dict) -> list[str]:
    errors = []
    nodes = registry.get("current_projections", [])
    if not isinstance(nodes, list) or not nodes:
        return ["current projection owners must be a non-empty list"]
    if not all(isinstance(row, dict) and isinstance(row.get("id"), str) and row["id"] for row in nodes):
        return ["current projection rows require nonempty string owner IDs"]
    for row in nodes:
        for field in ("inputs", "outputs", "checks", "depends_on"):
            if not isinstance(row.get(field), list) or not all(isinstance(value, str) for value in row[field]):
                errors.append(f"{row['id']}: {field} must be a string list")
    if errors:
        return errors
    ids = [row.get("id") for row in nodes]
    units = {unit["id"] for unit in registry["units"]}
    if len(set(ids)) != len(ids):
        errors.append("current projection owner IDs must be unique")
    positions = {name: index for index, name in enumerate(ids)}
    for row in nodes:
        prefix = row.get("id", "missing")
        if not isinstance(prefix, str) or not prefix:
            errors.append("projection owner ID is missing")
        if row.get("mode") not in {"generated", "review_required", "ignored_output"}:
            errors.append(f"{prefix}: historical or unknown objects cannot be current rebuild owners")
        for field in ("inputs", "outputs", "checks", "depends_on"):
            if not isinstance(row.get(field), list) or not all(isinstance(value, str) for value in row[field]):
                errors.append(f"{prefix}: {field} must be a string list")
        for field in ("inputs", "outputs"):
            for value in row.get(field, []):
                try:
                    normalized_path(value)
                except ValueError as error:
                    errors.append(f"{prefix}: {error}")
        if not row.get("inputs") or not row.get("outputs") or not row.get("checks"):
            errors.append(f"{prefix}: inputs, outputs and named consumers are required")
        if any(name not in units for name in row.get("checks", [])):
            errors.append(f"{prefix}: check does not resolve in the sole validation inventory")
        if any(name not in positions or positions[name] >= positions.get(prefix, -1)
               for name in row.get("depends_on", [])):
            errors.append(f"{prefix}: dependencies must name preceding current projection owners")
        command = row.get("rebuild")
        if not isinstance(command, list) or not command or not all(isinstance(value, str) for value in command):
            errors.append(f"{prefix}: a reviewable rebuild command is required")
        if row.get("mode") == "review_required" and not row.get("review_boundary"):
            errors.append(f"{prefix}: a manual review boundary is required")
        if row.get("bound_input_owner") not in {None, "human_reader_current"}:
            errors.append(f"{prefix}: unknown dynamic input owner")
    return errors


def expanded_outputs(root: Path, selectors: list[str]) -> list[str]:
    outputs = set()
    for selector in selectors:
        normalized_path(selector)
        if any(char in selector for char in "*?["):
            outputs.update(path.relative_to(root).as_posix() for path in root.glob(selector) if path.is_file())
        else:
            outputs.add(selector)
    return sorted(outputs)


def plan(registry: dict, changed: list[str], root: Path) -> dict:
    errors = graph_errors(registry)
    if errors:
        raise ValueError("invalid projection graph: " + "; ".join(errors))
    changed = sorted({normalized_path(path) for path in changed})
    selected = {}
    affected_paths = set(changed)
    for row in registry.get("current_projections", []):
        inputs = list(row["inputs"])
        if row.get("bound_input_owner") == "human_reader_current":
            # Reuse the named crosswalk's actual input catalogue, rather than
            # creating another maintained list of its evidence/proof routes.
            crosswalk = json.loads((root / "editions/reader_manuscript/current/conclusion_claim_crosswalk.json").read_text(encoding="utf-8"))
            inputs.extend(normalized_path(ref["path"]) for unit in crosswalk["units"]
                          for owner in unit["owners"] for ref in owner["artifact_refs"])
        direct = sorted(path for path in changed if any(matches(path, pattern) for pattern in inputs))
        changed_outputs = sorted(path for path in changed if any(matches(path, pattern) for pattern in row["outputs"]))
        parents = [name for name in row["depends_on"] if name in selected]
        # Explicit edges remain inspectable and do not accidentally infer cycles
        # from projections that edit a generated block inside their own input.
        if not direct and not changed_outputs and not parents:
            continue
        outputs = expanded_outputs(root, row["outputs"])
        affected_paths.update(outputs)
        selected[row["id"]] = {**row, "changed_inputs": direct, "changed_outputs": changed_outputs, "affected_upstream_owners": parents,
                                "expanded_outputs": outputs}
    consumers = {name for row in selected.values() for name in row["checks"]}
    unit_rows = []
    unknown = []
    for unit in registry["units"]:
        inputs = unit.get("input_artifacts", [])
        if not inputs:
            unknown.append(unit["id"])
        reasons = sorted(path for path in affected_paths if any(
            matches(path, pattern) or path.startswith(pattern.rstrip("/") + "/")
            for pattern in inputs))
        if unit["id"] in consumers or reasons or f"scripts/{unit['script']}" in changed:
            unit_rows.append({"id": unit["id"], "tier": unit["execution_tier"], "script": unit["script"],
                              "args": unit["args"], "affected_inputs": reasons,
                              "named_projection_consumer": unit["id"] in consumers})
    # Include prerequisite validators rather than pretending that selecting a
    # downstream check makes its preceding dependency already successful.
    by_id = {unit["id"]: unit for unit in registry["units"]}
    included = {row["id"] for row in unit_rows}
    pending = list(included)
    while pending:
        name = pending.pop()
        contract = {**registry.get("execution_defaults", {}), **by_id[name].get("execution", {})}
        for dependency in contract.get("depends_on", []):
            if dependency != "base-gate" and dependency not in included:
                included.add(dependency)
                pending.append(dependency)
    known_rows = {row["id"]: row for row in unit_rows}
    unit_rows = [known_rows.get(unit["id"], {"id": unit["id"], "tier": unit["execution_tier"],
                 "script": unit["script"], "args": unit["args"], "affected_inputs": [],
                 "named_projection_consumer": False, "selection_reason": "execution_prerequisite"})
                 for unit in registry["units"] if unit["id"] in included]
    for row in unit_rows:
        unit = by_id[row["id"]]
        row["execution_contract"] = execution_contract(registry, unit)
        row["projection_owners"] = [name for name, owner in selected.items() if row["id"] in owner["checks"]]
        if "selection_reason" not in row:
            row["selection_reason"] = "named_projection_consumer" if row["projection_owners"] else "declared_input_or_checker_changed"
    capabilities = sorted({name for row in unit_rows for name in row["execution_contract"].get("capabilities", [])})
    unreviewed = [row["id"] for row in unit_rows if row["execution_contract"].get("review_state") != "reviewed"]
    base_contract = execution_contract(registry, {"execution": {"side_effects": "read_only", "review_state": "reviewed", "depends_on": []}})
    return {"schema_version": "asi_stack.current_projection_plan.v1", "changed_paths": changed,
            "projections": list(selected.values()), "checks": unit_rows,
            "base_gate": {"script": registry.get("base_gate", {}).get("script", "validate_book.py"), "execution_contract": base_contract},
            "execution_preview": {"capabilities": capabilities, "unreviewed_contracts": unreviewed,
                                  "status": "incomplete_contract_review" if unreviewed else "declared_contracts_only",
                                  "scope": "Declared prerequisites, side effects and per-unit wall-time ceilings; budgets are not duration estimates and unreviewed defaults do not establish complete capability coverage."},
            "input_coverage_unknown_units": unknown,
            "scope": "Conservative invalidation for reviewed graph owners and declared validator inputs. Missing input metadata remains unknown; targeted checks cannot replace the complete CI gate. No writes or review approvals performed."}
