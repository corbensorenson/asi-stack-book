#!/usr/bin/env python3
import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "experiments/claim_family_bundle_coverage/result.json"
SCHEMA = ROOT / "schemas/claim_family_bundle_coverage.schema.json"
REGISTRY = ROOT / "validation/registry.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def structural_errors(value: dict) -> list[str]:
    errors = []
    bundles = value.get("bundles", [])
    if {row.get("family_id") for row in bundles} != {f"CF-{index:02d}" for index in range(1, 9)}:
        errors.append("family coverage")
    for row in bundles:
        result = ROOT / row.get("result_path", "missing")
        validator = ROOT / row.get("validator_path", "missing")
        receipt = ROOT / row.get("receipt_path", "missing")
        if not result.exists() or digest(result) != row.get("result_sha256"):
            errors.append(f"result digest: {row.get('family_id')}")
        if not validator.exists() or not receipt.exists():
            errors.append(f"bundle artifact: {row.get('family_id')}")
        if row.get("validator_passed") is not True or not row.get("negative_controls"):
            errors.append(f"competence boundary: {row.get('family_id')}")
    if value.get("blocked_atom_count_preserved") != 3698 or value.get("chapter_core_promotion_count") != 0:
        errors.append("gap or core boundary")
    return errors


def main() -> None:
    value = json.loads(RESULT.read_text())
    jsonschema.validate(value, json.loads(SCHEMA.read_text()))
    errors = structural_errors(value)
    registered = {row.get("script") for row in json.loads(REGISTRY.read_text()).get("units", [])}
    for row in value["bundles"]:
        name = Path(row["validator_path"]).name
        if name not in registered:
            errors.append(f"unregistered selected validator: {name}")
        completed = subprocess.run(
            [sys.executable, str(ROOT / row["validator_path"])],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        if completed.returncode != 0:
            errors.append(f"selected validator failed: {row['family_id']}: {completed.stdout}{completed.stderr}")
    mutations = [
        ("drop family", lambda data: data["bundles"].pop()),
        ("erase validator", lambda data: data["bundles"][0].__setitem__("validator_passed", False)),
        ("rewrite digest", lambda data: data["bundles"][0].__setitem__("result_sha256", "0" * 64)),
        ("invent core promotion", lambda data: data.__setitem__("chapter_core_promotion_count", 1)),
        ("erase blocked gaps", lambda data: data.__setitem__("blocked_atom_count_preserved", 0)),
    ]
    for label, mutate in mutations:
        candidate = copy.deepcopy(value)
        mutate(candidate)
        if not structural_errors(candidate):
            errors.append(f"mutation accepted: {label}")
    if errors:
        raise SystemExit("Claim-family bundle coverage failed:\n - " + "\n - ".join(errors))
    print("Claim-family bundle coverage passed: eight exact end-to-end or natural-work bundles, all selected validators replayed, 3,698 blocked atom gaps preserved, five mutations rejected, zero chapter-core movement.")


if __name__ == "__main__":
    main()
