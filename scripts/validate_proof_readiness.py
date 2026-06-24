#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "proofs" / "proof_manifest.json"
TRIAGE = ROOT / "proofs" / "proof_triage.json"

ALLOWED_TRIAGE = {
    "formal-invariant",
    "schema-contract",
    "process-contract",
    "research-agenda",
}

ALLOWLIST_MODULES = {"AsiStackProofs"}


def read_json(path: Path) -> object:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def module_for_path(path: Path) -> str:
    rel = path.relative_to(ROOT / "lean")
    if rel == Path("AsiStackProofs.lean"):
        return "AsiStackProofs"
    return "AsiStackProofs." + ".".join(rel.with_suffix("").parts[1:])


def main() -> None:
    manifest = read_json(MANIFEST)
    triage = read_json(TRIAGE)
    if not isinstance(manifest, dict) or not isinstance(triage, dict):
        raise SystemExit("proof manifest and proof triage must contain objects.")

    records = manifest.get("records", [])
    triage_records = triage.get("records", [])
    if not isinstance(records, list) or not isinstance(triage_records, list):
        raise SystemExit("proof manifest and proof triage records must be lists.")

    by_tag = {record.get("tag"): record for record in triage_records if isinstance(record, dict)}
    manifest_tags = {record.get("tag") for record in records if isinstance(record, dict)}
    errors: list[str] = []

    missing_triage = sorted(tag for tag in manifest_tags if tag not in by_tag)
    if missing_triage:
        errors.append("Missing proof triage entries: " + ", ".join(missing_triage))

    extra_triage = sorted(tag for tag in by_tag if tag not in manifest_tags)
    if extra_triage:
        errors.append("Proof triage has tags not in manifest: " + ", ".join(extra_triage))

    for record in triage_records:
        if not isinstance(record, dict):
            errors.append("Proof triage contains a non-object record")
            continue
        tag = record.get("tag")
        triage_class = record.get("triage")
        if triage_class not in ALLOWED_TRIAGE:
            errors.append(f"{tag}: invalid triage class {triage_class!r}")
        if not record.get("rationale"):
            errors.append(f"{tag}: missing rationale")

    referenced_modules = {record.get("module") for record in records if isinstance(record, dict)}
    for record in records:
        if not isinstance(record, dict):
            continue
        if record.get("status") == "implemented":
            module_path = ROOT / str(record.get("module_path"))
            if not module_path.exists():
                errors.append(f"{record.get('tag')}: implemented target missing {record.get('module_path')}")

    lean_files = sorted((ROOT / "lean").glob("AsiStackProofs*.lean")) + sorted((ROOT / "lean" / "AsiStackProofs").glob("*.lean"))
    for path in lean_files:
        module = module_for_path(path)
        if module in ALLOWLIST_MODULES:
            continue
        if module not in referenced_modules:
            errors.append(f"Lean module {module} is not referenced by any proof target")

    if errors:
        print("Proof-readiness validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    print(f"Proof-readiness validation passed: {len(records)} targets triaged.")


if __name__ == "__main__":
    main()
