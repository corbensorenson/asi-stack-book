#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "proofs" / "proof_manifest.json"
TRIAGE = ROOT / "proofs" / "proof_triage.json"
ROOT_LEAN_MODULE = ROOT / "lean" / "AsiStackProofs.lean"
PROOF_DEPTH_REPORT = ROOT / "docs" / "proof_depth_classification.md"
BOOK_STRUCTURE = ROOT / "book_structure.json"
RATIONALIZATION_REGISTRY = ROOT / "proofs" / "proof_rationalization_registry.json"

ALLOWED_TRIAGE = {
    "formal-invariant",
    "schema-contract",
    "process-contract",
    "research-agenda",
}

ALLOWED_STATUSES = {"planned", "scaffolded", "implemented", "blocked", "retired"}

ALLOWED_ROUTES = {
    "lean-candidate",
    "schema-first",
    "policy-model-first",
    "defer-until-narrowed",
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


def root_imports() -> set[str]:
    imports = set()
    for line in ROOT_LEAN_MODULE.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("import "):
            imports.add(stripped.removeprefix("import ").strip())
    return imports


def main() -> None:
    manifest = read_json(MANIFEST)
    triage = read_json(TRIAGE)
    structure = read_json(BOOK_STRUCTURE)
    if not isinstance(manifest, dict) or not isinstance(triage, dict) or not isinstance(structure, dict):
        raise SystemExit("proof manifest, proof triage, and book structure must contain objects.")

    records = manifest.get("records", [])
    triage_records = triage.get("records", [])
    if not isinstance(records, list) or not isinstance(triage_records, list):
        raise SystemExit("proof manifest and proof triage records must be lists.")

    imported_modules = root_imports()
    by_tag = {record.get("tag"): record for record in triage_records if isinstance(record, dict)}
    manifest_by_tag = {record.get("tag"): record for record in records if isinstance(record, dict)}
    manifest_tags = set(manifest_by_tag)
    errors: list[str] = []

    triage_tag_counts = Counter(record.get("tag") for record in triage_records if isinstance(record, dict))
    duplicate_triage_tags = sorted(tag for tag, count in triage_tag_counts.items() if tag is not None and count > 1)
    if duplicate_triage_tags:
        errors.append("Duplicate proof triage tags: " + ", ".join(duplicate_triage_tags))

    if "record_count" in triage and triage.get("record_count") != len(triage_records):
        errors.append(
            f"Proof triage record_count is {triage.get('record_count')!r}; expected {len(triage_records)}"
        )

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
        route = record.get("recommended_route")
        target_status = record.get("target_status")
        if triage_class not in ALLOWED_TRIAGE:
            errors.append(f"{tag}: invalid triage class {triage_class!r}")
        if route not in ALLOWED_ROUTES:
            errors.append(f"{tag}: invalid recommended route {route!r}")
        if target_status not in ALLOWED_STATUSES:
            errors.append(f"{tag}: invalid target status {target_status!r}")
        if not record.get("rationale"):
            errors.append(f"{tag}: missing rationale")
        manifest_record = manifest_by_tag.get(tag)
        if manifest_record is None:
            continue
        for field in ("chapter_id", "module", "formal_target"):
            if record.get(field) != manifest_record.get(field):
                errors.append(
                    f"{tag}: triage {field} {record.get(field)!r} does not match manifest {manifest_record.get(field)!r}"
                )
        if target_status != manifest_record.get("status"):
            errors.append(
                f"{tag}: triage target_status {target_status!r} does not match manifest status {manifest_record.get('status')!r}"
            )
        if target_status == "implemented":
            if triage_class != "formal-invariant":
                errors.append(f"{tag}: implemented proof targets must be triaged as formal-invariant")
            if route != "lean-candidate":
                errors.append(f"{tag}: implemented proof targets must use recommended_route 'lean-candidate'")

    referenced_modules = {record.get("module") for record in records if isinstance(record, dict)}
    # During rationalization, stable proof targets may move to a reachable
    # refinement module while a chapter deliberately retains narrower
    # contradiction, routing, or lineage lemmas in its declared legacy module.
    # A chapter-level lean_module declaration keeps that retained module owned
    # without forcing a fake target or deleting useful bounded lemmas.
    declared_chapter_modules = {
        chapter.get("lean_module")
        for part in structure.get("parts", [])
        if isinstance(part, dict)
        for chapter in part.get("chapters", [])
        if isinstance(chapter, dict) and chapter.get("lean_module")
    }
    referenced_modules.update(declared_chapter_modules)
    if RATIONALIZATION_REGISTRY.exists():
        rationalization = read_json(RATIONALIZATION_REGISTRY)
        retained_lineage_modules = {
            module_for_path(ROOT / row["module_path"])
            for row in rationalization.get("baseline_theorems", [])
            if isinstance(row, dict)
            and row.get("current_present") is True
            and isinstance(row.get("module_path"), str)
            and (ROOT / row["module_path"]).exists()
        }
        referenced_modules.update(retained_lineage_modules)
    for record in records:
        if not isinstance(record, dict):
            continue
        if record.get("status") == "implemented":
            module_path = ROOT / str(record.get("module_path"))
            if not module_path.exists():
                errors.append(f"{record.get('tag')}: implemented target missing {record.get('module_path')}")
            module = record.get("module")
            if module != "AsiStackProofs" and module not in imported_modules:
                errors.append(
                    f"{record.get('tag')}: implemented module {module} is not imported by lean/AsiStackProofs.lean"
                )

    lean_files = sorted((ROOT / "lean").glob("AsiStackProofs*.lean")) + sorted((ROOT / "lean" / "AsiStackProofs").glob("*.lean"))
    for path in lean_files:
        module = module_for_path(path)
        if module in ALLOWLIST_MODULES:
            continue
        if module not in referenced_modules:
            errors.append(f"Lean module {module} is not referenced by any proof target")

    if not PROOF_DEPTH_REPORT.exists():
        errors.append("Proof-depth classification report is missing; run scripts/validate_proof_depth.py --write")
    else:
        depth_text = PROOF_DEPTH_REPORT.read_text(encoding="utf-8", errors="ignore")
        if "projection-only traceability" not in depth_text:
            errors.append("Proof-depth classification report does not expose projection-only traceability classification.")

    if errors:
        print("Proof-readiness validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    print(
        f"Proof-readiness validation passed: {len(records)} targets triaged; "
        "proof-depth classification report present."
    )


if __name__ == "__main__":
    main()
