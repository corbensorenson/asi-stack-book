#!/usr/bin/env python3
"""Validate the executable three-product projections and their negative controls."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
import tempfile

from build_canonical_public_status import ROOT, build_status, validate_against_schema
from build_product_projections import (
    CONTRACTS,
    CONTRIBUTIONS,
    MANIFEST_SCHEMA_VERSION,
    SPINE,
    STRUCTURE,
    UNIT_CROSSWALK,
    build_evidence,
    build_narrative,
    build_reference,
    canonical_chapters,
    sha256_file,
    write_json,
)
from build_reader_edition import (
    filter_structure_for_narrative_spine,
    generate as generate_reader,
    load_narrative_spine,
)


SPINE_SCHEMA = ROOT / "schemas" / "narrative_product_spine.schema.json"
PROJECTION_SCHEMA = ROOT / "schemas" / "product_projection_manifest.schema.json"
DOC = ROOT / "docs" / "product_projection_artifacts.md"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_into(output: Path, status: dict) -> None:
    structure = load(STRUCTURE)
    spine = load(SPINE)
    contribution_data = load(CONTRIBUTIONS)
    canonical = canonical_chapters(structure)
    assignments = {row["chapter_id"]: row for row in contribution_data["chapter_assignments"]}
    narrative = build_narrative(output, canonical, spine, assignments)
    reference = build_reference(output, canonical, assignments)
    evidence = build_evidence(output, status)
    root = {
        "schema_version": MANIFEST_SCHEMA_VERSION,
        "generated_from": {
            "canonical_status_id": status["status_id"],
            "source_commit": status["source_commit"],
            "chapter_count": status["counts"]["chapters"],
            "source_count": status["counts"]["sources"],
            "structure_sha256": sha256_file(STRUCTURE),
            "contract_sha256": sha256_file(CONTRACTS),
            "narrative_spine_sha256": sha256_file(SPINE),
            "narrative_unit_crosswalk_sha256": sha256_file(UNIT_CROSSWALK),
        },
        "products": [
            {
                "id": "narrative_book",
                "status": narrative["status"],
                "entry_path": "narrative-book/index.html",
                "manifest_path": "narrative-book/manifest.json",
                "entry_count": narrative["selected_chapter_count"],
            },
            {
                "id": "architecture_reference",
                "status": reference["status"],
                "entry_path": "architecture-reference/index.html",
                "manifest_path": "architecture-reference/manifest.json",
                "entry_count": reference["chapter_count"],
            },
            {
                "id": "evidence_registry",
                "status": evidence["status"],
                "entry_path": "evidence-registry/index.html",
                "manifest_path": "evidence-registry/manifest.json",
                "entry_count": evidence["entry_count"],
            },
        ],
        "non_claims": [
            "Product projection is not product approval or publication review.",
            "Projection changes navigation and density, not canonical claim support.",
            "The canonical source tree and its evidence records remain authoritative.",
        ],
    }
    write_json(output / "product-projections.json", root)


def snapshot_errors(output: Path, evidence: dict) -> list[str]:
    errors: list[str] = []
    for group in evidence.get("groups", []):
        for entry in group.get("entries", []):
            if entry.get("publication_mode") != "content_addressed_snapshot":
                continue
            path = output / "evidence-registry" / entry["projection_path"]
            if not path.is_file():
                errors.append(f"missing evidence snapshot {entry['projection_path']}")
            elif sha256(path) != entry.get("sha256"):
                errors.append(f"evidence snapshot digest mismatch {entry['projection_path']}")
            canonical = ROOT / str(entry.get("canonical_path", ""))
            if canonical.is_file() and sha256(canonical) != entry.get("sha256"):
                errors.append(f"evidence snapshot is stale against canonical source {entry['canonical_path']}")
    return errors


def narrative_projection_errors(spine: dict) -> list[str]:
    errors: list[str] = []
    projection_fields = (
        "plain_language_thesis",
        "normative_engineering_rule",
        "machine_contract",
    )
    for record in spine.get("chapters", []):
        for field in projection_fields:
            if len(str(record.get(field, "")).strip()) < (64 if field == "machine_contract" else 48):
                errors.append(f"{record.get('chapter_id')}: missing bounded narrative projection {field}")
        machine_contract = str(record.get("machine_contract", "")).lower()
        if "does not" not in machine_contract and "no " not in machine_contract:
            errors.append(f"{record.get('chapter_id')}: machine contract lacks an explicit noninheritance boundary")
    return errors


def narrative_routing_errors(
    narrative: dict,
    units: list[dict],
    canonical: list[dict],
    html_text: str,
) -> list[str]:
    """Require every specialist owner to be visible under its narrative unit."""
    errors: list[str] = []
    canonical_by_id = {row["chapter_id"]: row for row in canonical}
    unit_by_representative = {
        unit["representative_chapter_id"]: unit
        for unit in units
    }
    unit_by_chapter = {
        chapter_id: unit
        for unit in units
        for chapter_id in unit.get("chapter_ids", [])
    }
    selected = narrative.get("chapters", [])
    routed_ids: list[str] = []
    for row in selected:
        chapter_id = row.get("chapter_id")
        unit = unit_by_representative.get(chapter_id)
        if unit is None:
            errors.append(f"{chapter_id}: narrative representative has no unit")
            continue
        if row.get("unit_id") != unit.get("unit_id") or row.get("unit_label") != unit.get("label"):
            errors.append(f"{chapter_id}: narrative unit metadata does not match the crosswalk")
        expected_ids = [
            owner_id
            for owner_id in unit.get("chapter_ids", [])
            if owner_id != chapter_id
        ]
        owners = row.get("reference_owners", [])
        owner_ids = [owner.get("chapter_id") for owner in owners]
        if row.get("reference_owner_count") != len(expected_ids):
            errors.append(f"{chapter_id}: specialist-owner count does not match the crosswalk")
        if owner_ids != expected_ids:
            errors.append(f"{chapter_id}: specialist-owner routes do not match crosswalk order")
        routed_ids.extend(owner_ids)
        for owner in owners:
            owner_id = owner.get("chapter_id")
            canonical_owner = canonical_by_id.get(owner_id)
            if canonical_owner is None:
                errors.append(f"{chapter_id}: unknown specialist owner {owner_id!r}")
                continue
            expected_record = {
                "chapter_id": owner_id,
                "title": canonical_owner["title"],
                "canonical_order": canonical_owner["order"],
                "core_claim_ref": canonical_owner["core_claim_ref"],
                "architecture_reference_path": canonical_owner["public_path"],
            }
            if owner != expected_record:
                errors.append(f"{chapter_id}: specialist owner {owner_id} is stale against canonical metadata")
            if canonical_owner["title"] not in html_text:
                errors.append(f"{chapter_id}: specialist owner {owner_id} is hidden from the narrative page")
            if f'{canonical_owner["public_path"]}?view=human' not in html_text:
                errors.append(f"{chapter_id}: specialist owner {owner_id} lacks a direct Human-view route")

    expected_routed_ids = [
        chapter_id
        for unit in units
        for chapter_id in unit.get("chapter_ids", [])
        if chapter_id != unit.get("representative_chapter_id")
    ]
    if routed_ids != expected_routed_ids:
        errors.append("narrative product does not visibly route every specialist owner exactly once")
    if len(routed_ids) != len(set(routed_ids)):
        errors.append("narrative product visibly routes a specialist owner more than once")

    omitted = narrative.get("reference_only_chapters", [])
    omitted_by_id = {row.get("chapter_id"): row for row in omitted}
    if set(omitted_by_id) != set(expected_routed_ids):
        errors.append("reference-only chapter index does not match visible specialist-owner routing")
    for chapter_id in expected_routed_ids:
        row = omitted_by_id.get(chapter_id)
        unit = unit_by_chapter.get(chapter_id)
        if row is None or unit is None:
            continue
        representative = unit.get("representative_chapter_id")
        if (
            row.get("nearest_narrative_owner") != representative
            or row.get("unit_id") != unit.get("unit_id")
            or row.get("unit_label") != unit.get("label")
        ):
            errors.append(f"{chapter_id}: reference-only unit route does not match the crosswalk")
    return errors


def validate_rendered_site(site: Path, projection_schema: dict) -> list[str]:
    errors: list[str] = []
    products = site / "products"
    status_path = site / "status" / "canonical-public-status.json"
    root_path = products / "product-projections.json"
    if not status_path.is_file() or not root_path.is_file():
        return ["rendered site is missing canonical status or product-projections manifest"]
    status = load(status_path)
    root_manifest = load(root_path)
    errors.extend(validate_against_schema(root_manifest, projection_schema, "rendered product-projections.json"))
    generated = root_manifest.get("generated_from", {})
    expected_binding = {
        "canonical_status_id": status.get("status_id"),
        "source_commit": status.get("source_commit"),
        "chapter_count": status.get("counts", {}).get("chapters"),
        "source_count": status.get("counts", {}).get("sources"),
        "structure_sha256": sha256_file(STRUCTURE),
        "contract_sha256": sha256_file(CONTRACTS),
        "narrative_spine_sha256": sha256_file(SPINE),
        "narrative_unit_crosswalk_sha256": sha256_file(UNIT_CROSSWALK),
    }
    if generated != expected_binding:
        errors.append("rendered product projection is not bound to canonical status and current source digests")
    for row in root_manifest.get("products", []):
        for field in ("entry_path", "manifest_path"):
            target = products / str(row.get(field, ""))
            if not target.is_file():
                errors.append(f"rendered product projection missing {field}: {row.get(field)!r}")
    narrative_path = products / "narrative-book" / "manifest.json"
    reference_path = products / "architecture-reference" / "manifest.json"
    evidence_path = products / "evidence-registry" / "manifest.json"
    if not all(path.is_file() for path in (narrative_path, reference_path, evidence_path)):
        return errors
    narrative = load(narrative_path)
    reference = load(reference_path)
    evidence = load(evidence_path)
    narrative_html = (products / "narrative-book" / "index.html").read_text(
        encoding="utf-8",
        errors="ignore",
    )
    errors.extend(
        narrative_routing_errors(
            narrative,
            load(UNIT_CROSSWALK).get("units", []),
            canonical_chapters(load(STRUCTURE)),
            narrative_html,
        )
    )
    errors.extend(snapshot_errors(products, evidence))
    for row in narrative.get("chapters", []):
        if not (site / row.get("public_path", "")).is_file():
            errors.append(f"rendered narrative route target missing: {row.get('public_path')!r}")
    for row in reference.get("chapters", []):
        if not (site / row.get("public_path", "")).is_file():
            errors.append(f"rendered architecture route target missing: {row.get('public_path')!r}")
    for group in evidence.get("groups", []):
        for entry in group.get("entries", []):
            if entry.get("publication_mode") != "rendered_site_route":
                continue
            canonical_path = str(entry.get("canonical_path", ""))
            if not (site / canonical_path).is_file():
                errors.append(f"rendered evidence route target missing: {canonical_path!r}")
    latest_products = site / "latest" / "products"
    if (site / "latest").is_dir() and not (latest_products / "product-projections.json").is_file():
        errors.append("moving latest mirror is missing the product-projection manifest")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", type=Path, help="also validate generated product pages inside a rendered site")
    args = parser.parse_args()
    errors: list[str] = []
    required = [STRUCTURE, CONTRACTS, SPINE, UNIT_CROSSWALK, CONTRIBUTIONS, SPINE_SCHEMA, PROJECTION_SCHEMA, DOC]
    for path in required:
        if not path.exists():
            errors.append(f"missing {path.relative_to(ROOT)}")
    if errors:
        fail(errors)
    structure = load(STRUCTURE)
    spine = load(SPINE)
    status = build_status()
    spine_schema = load(SPINE_SCHEMA)
    projection_schema = load(PROJECTION_SCHEMA)
    errors.extend(validate_against_schema(spine, spine_schema, str(SPINE.relative_to(ROOT))))
    canonical = canonical_chapters(structure)
    canonical_ids = [row["chapter_id"] for row in canonical]
    selected_ids = [row["chapter_id"] for row in spine["chapters"]]
    unit_crosswalk = load(UNIT_CROSSWALK)
    units = unit_crosswalk.get("units", [])
    if len(units) != 22 or [row.get("order") for row in units] != list(range(1, 23)):
        errors.append("narrative unit crosswalk must contain 22 ordered units")
    if [row.get("representative_chapter_id") for row in units] != selected_ids:
        errors.append("narrative unit representatives do not match the narrative spine")
    assigned_ids = [
        chapter_id
        for unit in units
        for chapter_id in unit.get("chapter_ids", [])
    ]
    if len(assigned_ids) != len(set(assigned_ids)):
        errors.append("narrative unit crosswalk assigns at least one chapter more than once")
    if set(assigned_ids) != set(canonical_ids) or len(assigned_ids) != len(canonical_ids):
        errors.append("narrative unit crosswalk does not assign all 84 canonical chapters exactly once")
    for unit in units:
        if unit.get("representative_chapter_id") not in unit.get("chapter_ids", []):
            errors.append(f"{unit.get('unit_id')}: representative chapter is absent from its unit")
    errors.extend(narrative_projection_errors(spine))
    if len(selected_ids) != 22:
        errors.append("narrative product must contain exactly 22 representative chapters")
    if selected_ids != [chapter_id for chapter_id in canonical_ids if chapter_id in set(selected_ids)]:
        errors.append("narrative product spine does not preserve canonical manifest order")
    if status["claim_state_distribution"]["support_states"] != {"argument": len(canonical)}:
        errors.append("product projection must preserve all chapter-core support states at argument")

    with tempfile.TemporaryDirectory(prefix="asi-products-") as temp:
        output = Path(temp) / "products"
        output.mkdir(parents=True)
        build_into(output, status)
        root_manifest = load(output / "product-projections.json")
        errors.extend(validate_against_schema(root_manifest, projection_schema, "product-projections.json"))
        if {row["id"] for row in root_manifest["products"]} != {"narrative_book", "architecture_reference", "evidence_registry"}:
            errors.append("projection manifest must contain exactly the three product IDs")
        narrative = load(output / "narrative-book" / "manifest.json")
        reference = load(output / "architecture-reference" / "manifest.json")
        evidence = load(output / "evidence-registry" / "manifest.json")
        narrative_html = (output / "narrative-book" / "index.html").read_text(
            encoding="utf-8",
            errors="ignore",
        )
        errors.extend(narrative_routing_errors(narrative, units, canonical, narrative_html))
        if narrative.get("selected_chapter_count") != len(selected_ids):
            errors.append("narrative projection selected count mismatch")
        if narrative.get("canonical_chapter_count") != len(canonical):
            errors.append("narrative projection canonical count mismatch")
        if len(narrative.get("reference_only_chapters", [])) != len(canonical) - len(selected_ids):
            errors.append("narrative projection does not route every omitted chapter")
        if [row["chapter_id"] for row in reference.get("chapters", [])] != canonical_ids:
            errors.append("architecture-reference projection is not the complete canonical chapter order")
        if reference.get("chapter_count") != len(canonical):
            errors.append("architecture-reference chapter count mismatch")
        errors.extend(snapshot_errors(output, evidence))
        if evidence.get("chapter_count") != len(canonical) or evidence.get("source_count") != status["counts"]["sources"]:
            errors.append("evidence-registry projection does not match canonical counts")
        for relative in (
            "index.html",
            "narrative-book/index.html",
            "architecture-reference/index.html",
            "evidence-registry/index.html",
        ):
            if not (output / relative).is_file() and relative != "index.html":
                errors.append(f"missing generated product page {relative}")

        reader_output = Path(temp) / "narrative-reader"
        summary = generate_reader(reader_output, "reader_release", SPINE)
        if summary.get("chapters") != len(selected_ids) or summary.get("omitted_canonical_chapter_count") != len(canonical) - len(selected_ids):
            errors.append("bounded narrative reader summary count mismatch")
        if summary.get("selected_chapter_ids") != selected_ids:
            errors.append("bounded narrative reader selected ID mismatch")
        for record in spine["chapters"]:
            chapter_file = next(row["source_file"] for row in canonical if row["chapter_id"] == record["chapter_id"])
            generated = reader_output / chapter_file
            text = generated.read_text(encoding="utf-8") if generated.exists() else ""
            for phrase in (
                "Narrative orientation",
                "**Plain-language thesis.**",
                "**Engineering rule.**",
                "**Machine contract.**",
                "**Question.**",
                "**Running example.**",
                "**Strongest objection.**",
                "**Failure story.**",
                "**What would change the conclusion.**",
                record["core_claim_ref"],
                "adds no evidence and changes no support state",
            ):
                if phrase not in text:
                    errors.append(f"{record['chapter_id']}: generated orientation missing {phrase!r}")
        omitted_files = {
            row["source_file"]
            for row in canonical
            if row["chapter_id"] not in set(selected_ids)
        }
        leaked = sorted(path for path in omitted_files if (reader_output / path).exists())
        if leaked:
            errors.append(f"bounded narrative reader copied omitted chapter files: {leaked[:3]}")

        # Reject a too-wide narrative product.
        too_wide = copy.deepcopy(spine)
        extra_id = next(chapter_id for chapter_id in canonical_ids if chapter_id not in set(selected_ids))
        extra = copy.deepcopy(too_wide["chapters"][-1])
        extra["order"] = 23
        extra["chapter_id"] = extra_id
        extra["core_claim_ref"] = f"{extra_id}.core"
        too_wide["chapters"].append(extra)
        too_wide_path = Path(temp) / "too-wide.json"
        write_json(too_wide_path, too_wide)
        try:
            load_narrative_spine(too_wide_path)
        except ValueError:
            pass
        else:
            errors.append("negative control failed: 23-unit narrative spine was accepted")

        # Reject a missing editorial field.
        missing_field = copy.deepcopy(spine)
        del missing_field["chapters"][0]["machine_contract"]
        if not validate_against_schema(missing_field, spine_schema, "negative.missing_field"):
            errors.append("negative control failed: missing machine contract was accepted")

        # Reject a substantial-looking machine contract that omits the
        # noninheritance boundary.
        unbounded_contract = copy.deepcopy(spine)
        unbounded_contract["chapters"][0]["machine_contract"] = (
            "The transition record binds source identity, target identity, authority, "
            "obligations, evidence, residuals, consumers, expiry, and recovery state."
        )
        if not narrative_projection_errors(unbounded_contract):
            errors.append("negative control failed: machine contract without noninheritance was accepted")

        # Reject selection order that disagrees with the canonical manifest.
        wrong_order = copy.deepcopy(spine)
        wrong_order["chapters"][0], wrong_order["chapters"][1] = wrong_order["chapters"][1], wrong_order["chapters"][0]
        wrong_order["chapters"][0]["order"] = 1
        wrong_order["chapters"][1]["order"] = 2
        try:
            filter_structure_for_narrative_spine(structure, wrong_order)
        except ValueError:
            pass
        else:
            errors.append("negative control failed: out-of-order narrative spine was accepted")

        # Reject a changed evidence snapshot against its content digest.
        snapshot = next(
            output / "evidence-registry" / entry["projection_path"]
            for group in evidence["groups"]
            for entry in group["entries"]
            if entry["publication_mode"] == "content_addressed_snapshot"
        )
        snapshot.write_bytes(snapshot.read_bytes() + b"\nmutation")
        if not snapshot_errors(output, evidence):
            errors.append("negative control failed: changed evidence snapshot was accepted")

        # Reject a specialist owner that exists in the crosswalk but is hidden
        # from the narrative unit's visible route.
        hidden_owner = copy.deepcopy(narrative)
        unit_with_specialists = next(
            row for row in hidden_owner["chapters"]
            if row.get("reference_owners")
        )
        unit_with_specialists["reference_owners"].pop()
        unit_with_specialists["reference_owner_count"] -= 1
        if not narrative_routing_errors(hidden_owner, units, canonical, narrative_html):
            errors.append("negative control failed: hidden specialist owner was accepted")

    doc = DOC.read_text(encoding="utf-8", errors="ignore")
    for phrase in (
        f"{len(selected_ids)}-unit",
        f"{len(canonical)}-chapter",
        "content-addressed",
        "not a reviewed reader release",
    ):
        if phrase not in doc:
            errors.append(f"{DOC.relative_to(ROOT)} missing {phrase!r}")
    if args.site is not None:
        site = args.site if args.site.is_absolute() else ROOT / args.site
        errors.extend(validate_rendered_site(site, projection_schema))
    fail(errors)
    print(
        f"Product-projection validation passed: {len(selected_ids)} narrative chapters, "
        f"{len(selected_ids) * 3} explicit unit projections, "
        f"{len(canonical) - len(selected_ids)} reference-routed omissions, "
        f"{len(canonical) - len(selected_ids)} visible specialist-owner routes, "
        f"{len(canonical)} reference chapters, {evidence['entry_count']} evidence routes, "
        "and 6 rejecting negative controls."
    )


def fail(errors: list[str]) -> None:
    if not errors:
        return
    print("Product-projection validation failed:")
    for error in errors:
        print(f" - {error}")
    raise SystemExit(1)


if __name__ == "__main__":
    main()
