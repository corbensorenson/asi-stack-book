#!/usr/bin/env python3
"""Validate the R16-B content-addressed current-reader freshness packet."""

from __future__ import annotations

import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any, Callable

import build_r16_b_current_reader_freshness as builder
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "editions/reader_manuscript/reader_2026_07_26/manifest.json"
REPORT = ROOT / "editions/reader_manuscript/reader_2026_07_26/freshness_report.md"
SCHEMA = ROOT / "schemas/r16_b_current_reader_freshness.schema.json"
EXPECTED_ROLES = {
    "thesis-bearing": 11,
    "load-bearing-reference": 54,
    "implementation-case": 7,
    "speculative-research": 12,
}
EXPECTED_FORMATS = {"virtual_qmd", "html", "pdf", "epub", "docx", "audio"}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def failures(record: dict[str, Any]) -> list[str]:
    out: list[str] = []
    snapshot = record.get("source_snapshot", {})
    chapters = record.get("chapter_records", [])
    chapter_ids = snapshot.get("chapter_ids", [])
    surfaces = record.get("reader_surfaces", {})
    formats = record.get("format_dispositions", {})
    historical = record.get("historical_release", {})
    freshness = record.get("freshness_checks", {})

    if record.get("state") != "terminal_local_source_freshness_formats_deferred":
        out.append("packet is not terminal at local source freshness")
    if snapshot.get("source_content_commit") != builder.SOURCE_COMMIT:
        out.append("source commit drifted")
    if snapshot.get("chapter_count") != 84 or len(chapter_ids) != 84:
        out.append("84-chapter source denominator drifted")
    if len(chapter_ids) != len(set(chapter_ids)):
        out.append("source chapter identities are not unique")
    if len(chapters) != 84:
        out.append("84 chapter records are not present")
    if [row.get("chapter_id") for row in chapters] != chapter_ids:
        out.append("chapter record identity or order drifted")
    if [row.get("manifest_order") for row in chapters] != list(range(1, 85)):
        out.append("manifest order drifted")

    expected_book_bytes = builder.git_bytes("book_structure.json")
    if snapshot.get("book_structure_sha256") != sha256(expected_book_bytes):
        out.append("book-structure digest drifted")
    if snapshot.get("chapter_ids_sha256") != sha256(
        json.dumps(chapter_ids, separators=(",", ":")).encode("utf-8")
    ):
        out.append("chapter-identity bundle digest drifted")

    role_counts = {role: 0 for role in EXPECTED_ROLES}
    unit_ids: set[str] = set()
    bundle = hashlib.sha256()
    for index, row in enumerate(chapters):
        chapter_id = row.get("chapter_id")
        source_path = row.get("source_path")
        try:
            source_bytes = builder.git_bytes(source_path)
        except (TypeError, ValueError):
            out.append(f"source missing at frozen commit: {chapter_id}")
            continue
        source = source_bytes.decode("utf-8")
        derived = builder.projection(source).encode("utf-8")
        derived_sha = sha256(derived)
        if row.get("source_sha256") != sha256(source_bytes):
            out.append(f"source digest drifted: {chapter_id}")
        if row.get("reader_projection_sha256") != derived_sha:
            out.append(f"projection digest drifted: {chapter_id}")
        if row.get("reader_projection_word_count") != len(
            re.findall(r"\b[\w'-]+\b", derived.decode("utf-8"))
        ):
            out.append(f"projection word count drifted: {chapter_id}")
        bundle.update(chapter_id.encode("utf-8") + b"\0" + derived_sha.encode("ascii") + b"\n")
        role = row.get("role")
        if role not in role_counts:
            out.append(f"unknown chapter role: {chapter_id}/{role}")
        else:
            role_counts[role] += 1
        unit_ids.add(row.get("narrative_unit_id"))
        if row.get("human_path_ref") != f"{source_path}#human-reading-path":
            out.append(f"Human Reading Path reference drifted: {chapter_id}")
        if row.get("summary_ref") != f"{source_path}#summary":
            out.append(f"Summary reference drifted: {chapter_id}")
        if row.get("handoff_ref") != f"{source_path}#handoff":
            out.append(f"Handoff reference drifted: {chapter_id}")
        expected_next = chapter_ids[index + 1] if index + 1 < len(chapter_ids) else None
        if row.get("next_chapter_id") != expected_next:
            out.append(f"adjacent handoff identity drifted: {chapter_id}")
        if row.get("materialization_state") != "content_addressed_virtual_projection_not_duplicated":
            out.append(f"source-copy policy drifted: {chapter_id}")
    if role_counts != EXPECTED_ROLES:
        out.append(f"chapter-role partition drifted: {role_counts}")
    if len(unit_ids) != 22 or None in unit_ids:
        out.append("22-unit narrative route drifted")
    if record.get("derivation", {}).get("chapter_bundle_sha256") != bundle.hexdigest():
        out.append("combined projection digest drifted")
    derivation = record.get("derivation", {})
    if derivation.get("chapter_projection_count") != 84:
        out.append("projection count drifted")
    if derivation.get("source_duplication_avoided") is not True:
        out.append("source duplication safeguard erased")

    if set(surfaces) != set(builder.SURFACES):
        out.append("required reader-surface set drifted")
    for name, path in builder.SURFACES.items():
        row = surfaces.get(name, {})
        if row.get("path") != path:
            out.append(f"reader-surface path drifted: {name}")
            continue
        if row.get("sha256") != sha256(builder.git_bytes(path)):
            out.append(f"reader-surface digest drifted: {name}")
    if set(freshness) != {
        "all_current_manifest_chapters",
        "opening_map",
        "chapter_role_classification",
        "adjacent_handoffs",
        "overview_figure",
        "glossary",
        "source_appendix",
        "claim_evidence_projection",
        "final_synthesis",
        "narrative_22_unit_route",
    } or any(value is not True for value in freshness.values()):
        out.append("freshness-check set drifted")

    if historical.get("release_id") != "reader-2026-07-18":
        out.append("historical reader identity drifted")
    historical_path = historical.get("manifest_path")
    if historical_path != builder.HISTORICAL_PATH:
        out.append("historical reader path drifted")
    elif historical.get("manifest_sha256") != sha256(builder.git_bytes(historical_path)):
        out.append("historical reader digest drifted")
    if historical.get("state") != "immutable_published_history_not_rewritten":
        out.append("historical reader immutability erased")

    if set(formats) != EXPECTED_FORMATS:
        out.append("format-disposition set drifted")
    if formats.get("virtual_qmd", {}).get("state") != "terminal_content_addressed_source_projection":
        out.append("virtual QMD is not terminal")
    for name in EXPECTED_FORMATS - {"virtual_qmd"}:
        if not formats.get(name, {}).get("state", "").startswith("deferred_not_generated"):
            out.append(f"unreviewed format laundered as generated: {name}")
        if not formats.get(name, {}).get("reason"):
            out.append(f"deferred format lacks reason: {name}")
    if len(record.get("non_claims", [])) < 5:
        out.append("non-claim envelope erased")
    for effect in ("support_state_effect", "release_effect", "publication_effect"):
        if record.get(effect) != "none":
            out.append(f"unauthorized {effect}")
    if not REPORT.is_file() or builder.SOURCE_COMMIT not in REPORT.read_text(encoding="utf-8"):
        out.append("freshness report missing or detached from source commit")
    if not SCHEMA.is_file():
        out.append("packet schema missing")
    return out


def mutate(
    record: dict[str, Any], label: str, fn: Callable[[dict[str, Any]], None], baseline: set[str]
) -> str | None:
    candidate = copy.deepcopy(record)
    fn(candidate)
    return None if set(failures(candidate)) - baseline else f"negative mutation accepted: {label}"


def main() -> None:
    record = load(ARTIFACT)
    out = failures(record)
    schema_errors = sorted(
        Draft202012Validator(load(SCHEMA)).iter_errors(record),
        key=lambda error: list(error.absolute_path),
    )
    out.extend(f"schema: {error.json_path}: {error.message}" for error in schema_errors)
    if record != builder.build():
        out.append("tracked packet is not the deterministic frozen-commit build")
    baseline = set(failures(record))
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("chapter deletion", lambda value: value["chapter_records"].pop()),
        ("chapter duplication", lambda value: value["chapter_records"].__setitem__(1, copy.deepcopy(value["chapter_records"][0]))),
        ("source digest rewrite", lambda value: value["chapter_records"][0].__setitem__("source_sha256", "0" * 64)),
        ("projection digest rewrite", lambda value: value["chapter_records"][0].__setitem__("reader_projection_sha256", "0" * 64)),
        ("role drift", lambda value: value["chapter_records"][0].__setitem__("role", "implementation-case")),
        ("unit erasure", lambda value: value["chapter_records"][0].__setitem__("narrative_unit_id", None)),
        ("Human Reading Path drift", lambda value: value["chapter_records"][0].__setitem__("human_path_ref", "missing")),
        ("adjacency drift", lambda value: value["chapter_records"][0].__setitem__("next_chapter_id", None)),
        ("surface deletion", lambda value: value["reader_surfaces"].pop("glossary")),
        ("surface digest rewrite", lambda value: value["reader_surfaces"]["source_appendix"].__setitem__("sha256", "0" * 64)),
        ("historical digest rewrite", lambda value: value["historical_release"].__setitem__("manifest_sha256", "0" * 64)),
        ("format laundering", lambda value: value["format_dispositions"]["pdf"].__setitem__("state", "published")),
        ("source duplication permission", lambda value: value["derivation"].__setitem__("source_duplication_avoided", False)),
        ("nonclaim erasure", lambda value: value.__setitem__("non_claims", [])),
        ("support promotion", lambda value: value.__setitem__("support_state_effect", "empirical-test-backed")),
        ("release invention", lambda value: value.__setitem__("release_effect", "published")),
    ]
    for label, fn in mutations:
        result = mutate(record, label, fn, baseline)
        if result:
            out.append(result)
    if out:
        raise SystemExit("R16-B reader freshness validation failed:\n - " + "\n - ".join(out))
    print(
        "R16-B reader freshness validation passed: 84 frozen-commit chapter projections, "
        "22 narrative units, role partition 11/54/7/12, 8 reader surfaces, 1 immutable "
        "historical release, 5 honestly deferred formats, 16 mutations rejected; "
        "support/release/publication effects none."
    )


if __name__ == "__main__":
    main()
