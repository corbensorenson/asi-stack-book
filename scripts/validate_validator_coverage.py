#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
WORKFLOW_DIR = ROOT / ".github" / "workflows"
HARNESS_REGISTRY = ROOT / "experiments" / "phase5_harness_registry.json"
ALLOWLIST = SCRIPTS_DIR / "validator_coverage_allowlist.json"
VALIDATION_REGISTRY = ROOT / "validation" / "registry.json"

REQUIRED_VALIDATORS = {
    "validate_architecture_red_team.py",
    "validate_core_claim_decisions.py",
    "validate_external_sota_positioning.py",
    "validate_release_reproducibility.py",
    "validate_ci_supply_chain_pins.py",
    "validate_tested_artifact_deployment.py",
    "validate_release_channels.py",
    "validate_evidence_quality_vectors.py",
    "validate_reviewer_capacity.py",
    "validate_external_review_program.py",
    "validate_author_decision_packets.py",
    "validate_source_notes.py",
    "validate_proof_readiness.py",
    "validate_evidence_transitions.py",
}


def read_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def covered_by_workflow(script_name: str, text: str) -> bool:
    return bool(re.search(rf"python3\s+scripts/{re.escape(script_name)}(?:\s|$)", text))


def load_allowlist() -> dict[str, str]:
    if not ALLOWLIST.exists():
        raise SystemExit(f"{ALLOWLIST.relative_to(ROOT)} is missing.")
    data = read_json(ALLOWLIST)
    if not isinstance(data, dict):
        raise SystemExit(f"{ALLOWLIST.relative_to(ROOT)} must contain an object.")
    rows = data.get("allowlisted_validators", [])
    if not isinstance(rows, list):
        raise SystemExit("allowlisted_validators must be a list.")
    allowlisted: dict[str, str] = {}
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            raise SystemExit(f"allowlisted_validators[{index}] must be an object.")
        script = row.get("script")
        reason = row.get("reason")
        if not isinstance(script, str) or not script:
            raise SystemExit(f"allowlisted_validators[{index}] missing script.")
        if not isinstance(reason, str) or not reason.strip():
            raise SystemExit(f"allowlisted_validators[{index}] missing reason.")
        allowlisted[Path(script).name] = reason.strip()
    return allowlisted


def load_harness_scripts() -> set[str]:
    registry = read_json(HARNESS_REGISTRY)
    if not isinstance(registry, list):
        raise SystemExit(f"{HARNESS_REGISTRY.relative_to(ROOT)} must contain a list.")
    scripts: set[str] = set()
    for index, record in enumerate(registry):
        if not isinstance(record, dict):
            raise SystemExit(f"phase5_harness_registry[{index}] must be an object.")
        script = record.get("script")
        command = record.get("command")
        if not isinstance(script, str) or not script:
            raise SystemExit(f"phase5_harness_registry[{index}] missing script.")
        if not isinstance(command, str) or Path(script).name not in command:
            raise SystemExit(
                f"phase5_harness_registry[{index}] command does not name {Path(script).name}."
            )
        scripts.add(Path(script).name)
    return scripts


def main() -> None:
    workflow_text = "\n".join(
        path.read_text(encoding="utf-8", errors="ignore")
        for path in sorted((*WORKFLOW_DIR.glob("*.yml"), *WORKFLOW_DIR.glob("*.yaml")))
    )
    allowlisted = load_allowlist()
    harness_scripts = load_harness_scripts()
    registry = read_json(VALIDATION_REGISTRY)
    registry_scripts = {
        Path(unit["script"]).name
        for unit in registry.get("units", [])
        if isinstance(unit, dict) and isinstance(unit.get("script"), str)
    }
    base_script = Path(registry.get("base_gate", {}).get("script", "")).name
    if base_script:
        registry_scripts.add(base_script)
    validator_paths = sorted(SCRIPTS_DIR.glob("validate_*.py"))
    validator_names = {path.name for path in validator_paths}

    errors: list[str] = []
    covered_direct: set[str] = set()

    stale_allowlist = sorted(name for name in allowlisted if name not in validator_names)
    for name in stale_allowlist:
        errors.append(f"Allow-listed validator {name} does not exist under scripts/.")

    for name in sorted(validator_names):
        direct = covered_by_workflow(name, workflow_text)
        registered = name in registry_scripts
        if direct:
            covered_direct.add(name)
        if not direct and not registered and name not in allowlisted:
            errors.append(
                f"{name} is not covered by the validation registry, a workflow, or the allow-list."
            )

    for name in sorted(REQUIRED_VALIDATORS):
        if name not in validator_names:
            errors.append(f"Required validator {name} is missing.")
        elif name in allowlisted:
            errors.append(f"Required validator {name} must be covered, not allow-listed.")
        elif name not in covered_direct and name not in registry_scripts:
            errors.append(f"Required validator {name} is not covered.")

    for name in sorted(harness_scripts):
        if name not in validator_names:
            errors.append(f"Phase 5 harness script {name} is missing from scripts/.")
        elif name in allowlisted:
            errors.append(f"Phase 5 harness script {name} must be covered, not allow-listed.")
        elif name not in covered_direct and name not in registry_scripts:
            errors.append(f"Phase 5 harness script {name} is not covered.")

    if errors:
        print("Validator coverage validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    print(
        "Validator coverage validation passed: "
        f"{len(validator_names)} validate_*.py scripts, "
        f"{len(harness_scripts)} registered Phase 5 harnesses, "
        f"{len(allowlisted)} allow-listed validator(s)."
    )


if __name__ == "__main__":
    main()
