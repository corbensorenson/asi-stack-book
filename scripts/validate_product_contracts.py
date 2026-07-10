#!/usr/bin/env python3
"""Validate the narrative/reference/registry product separation contract."""

from __future__ import annotations

import json
from pathlib import Path
import sys

from build_canonical_public_status import validate_against_schema


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "products" / "product_contracts.json"
SCHEMA = ROOT / "schemas" / "product_contracts.schema.json"
PROFILES = ROOT / "editions" / "release_profiles.json"
DOC = ROOT / "docs" / "product_contracts.md"
README = ROOT / "README.md"
INDEX = ROOT / "index.qmd"
EXPECTED_IDS = {"narrative_book", "architecture_reference", "evidence_registry"}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    errors: list[str] = []
    for path in (CONTRACT, SCHEMA, PROFILES, DOC, README, INDEX):
        if not path.exists():
            errors.append(f"missing {path.relative_to(ROOT)}")
    if errors:
        fail(errors)
    contract = load(CONTRACT)
    schema = load(SCHEMA)
    errors.extend(validate_against_schema(contract, schema, str(CONTRACT.relative_to(ROOT))))
    products = contract.get("products", [])
    by_id = {row.get("id"): row for row in products}
    if set(by_id) != EXPECTED_IDS or len(products) != 3:
        errors.append(f"product set must be exactly {sorted(EXPECTED_IDS)}")
    profiles = {row["id"] for row in load(PROFILES)["profiles"]}
    layers = {row["id"] for row in load(PROFILES)["content_layers"]}
    for product_id, product in by_id.items():
        if product.get("release_profile") not in profiles:
            errors.append(f"{product_id}: unknown release profile {product.get('release_profile')!r}")
        unknown_layers = sorted(set(product.get("source_layers", [])) - layers)
        if unknown_layers:
            errors.append(f"{product_id}: unknown source layers {unknown_layers}")
    for field in ("primary_audience", "reader_question", "navigation_contract", "density_contract", "review_gate"):
        values = [row.get(field) for row in products]
        if len(set(values)) != 3:
            errors.append(f"all three products must have distinct {field} values")
    narrative = by_id.get("narrative_book", {})
    reference = by_id.get("architecture_reference", {})
    registry = by_id.get("evidence_registry", {})
    if "index.html?view=human" not in narrative.get("entry_points", []):
        errors.append("narrative product must route to live Human view")
    if "products/narrative-book/index.html" not in narrative.get("entry_points", []):
        errors.append("narrative product must route through its generated product page")
    if narrative.get("release_profile") != "reader_release" or "not_a_reviewed_reader_release" not in narrative.get("current_status", ""):
        errors.append("narrative product must preserve the unreviewed live-projection boundary")
    if "chapters/integrated-reference-architecture.html?view=ai" not in reference.get("entry_points", []):
        errors.append("architecture reference must route to the integrated AI/research view")
    if "products/architecture-reference/index.html" not in reference.get("entry_points", []):
        errors.append("architecture reference must route through its generated complete index")
    if reference.get("release_profile") != "research_release":
        errors.append("architecture reference must use the research release profile")
    if "status/canonical-public-status.json" not in registry.get("entry_points", []):
        errors.append("evidence registry must begin at canonical public status")
    if "products/evidence-registry/index.html" not in registry.get("entry_points", []):
        errors.append("evidence registry must route through its generated registry page")
    if "appendices/C_claim_evidence_matrix.html" not in registry.get("entry_points", []):
        errors.append("evidence registry must route to Appendix C")
    shared = "\n".join(contract.get("shared_rules", [])).lower()
    for phrase in ("one canonical source tree", "uncertainty", "separate states", "no product contract promotes"):
        if phrase not in shared:
            errors.append(f"shared product rules missing {phrase!r}")
    for path in (README, INDEX):
        text = path.read_text(encoding="utf-8", errors="ignore")
        for phrase in (
            "Choose the product you need",
            "Narrative book",
            "Architecture reference",
            "Evidence registry",
            "docs/product_contracts.md",
        ):
            if phrase not in text:
                errors.append(f"{path.relative_to(ROOT)} missing product navigation phrase {phrase!r}")
    doc = DOC.read_text(encoding="utf-8", errors="ignore")
    for heading in ("## Narrative technical book", "## Architecture reference specification", "## Evidence, proof, and release registry"):
        if heading not in doc:
            errors.append(f"{DOC.relative_to(ROOT)} missing {heading!r}")
    fail(errors)
    print("Product contract validation passed: narrative, architecture-reference, and evidence-registry contracts are distinct and source-linked.")


def fail(errors: list[str]) -> None:
    if not errors:
        return
    print("Product contract validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


if __name__ == "__main__":
    main()
