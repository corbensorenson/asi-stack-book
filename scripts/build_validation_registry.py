#!/usr/bin/env python3
"""Maintain canonical formatting for the authoritative validation registry.

The registry is the inventory source. This script no longer discovers artifacts
or commands from validate_book.py; doing so would recreate the dual authority
that the registry migration removed.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "validation" / "registry.json"
OVERRIDES = ROOT / "validation" / "unit_contract_overrides.json"


def build_registry() -> dict[str, Any]:
    value = json.loads(OUTPUT.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError("validation/registry.json must contain an object")
    return value


def canonical_body(value: dict[str, Any]) -> str:
    return json.dumps(value, indent=2, ensure_ascii=False) + "\n"


def authority_errors(value: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if value.get("schema_version") != "asi_stack.validation_registry.v1":
        errors.append("registry schema_version must be asi_stack.validation_registry.v1")
    if value.get("migration_state") != "complete_registry_is_sole_inventory_and_execution_authority":
        errors.append("registry migration_state does not declare completed sole authority")
    if value.get("inventory_authority") != "validation/registry.json":
        errors.append("registry inventory_authority must point to itself")
    if "legacy_source" in value:
        errors.append("registry must not retain a legacy validate_book authority")
    if value.get("exact_contract_source") != "validation/unit_contract_overrides.json":
        errors.append("registry exact contract source is missing or wrong")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    value = build_registry()
    errors = authority_errors(value)
    if errors:
        raise SystemExit("Validation registry authority check failed:\n - " + "\n - ".join(errors))
    body = canonical_body(value)
    if args.check:
        if OUTPUT.read_text(encoding="utf-8") != body:
            raise SystemExit(f"{OUTPUT.relative_to(ROOT)} is not canonically formatted; run without --check")
        print("Authoritative validation registry is canonically formatted.")
    else:
        OUTPUT.write_text(body, encoding="utf-8")
        print(f"Normalized authoritative {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
