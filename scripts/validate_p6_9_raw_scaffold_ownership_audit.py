#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any, Callable

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "evidence_quality/p6_9_raw_scaffold_ownership_audit.json"
SCHEMA = ROOT / "schemas/p6_9_raw_scaffold_ownership_audit.schema.json"
REPORT = ROOT / "docs/p6_9_raw_scaffold_ownership_audit.md"
BUILDER = ROOT / "scripts/build_p6_9_raw_scaffold_ownership_audit.py"
W3 = ROOT / "evidence_quality/p7_1a_w3_inheritance_guard.json"
W3_VALIDATOR = ROOT / "scripts/validate_p7_1a_w3_inheritance_guard.py"
COPIED = ROOT / "tests/fixtures/p7_1a_w3_inheritance_guard/copied_scaffold.qmd"


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_module(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def errors(value: dict[str, Any]) -> list[str]:
    out: list[str] = []
    summary = value.get("summary", {})
    binding = value.get("w3_binding", {})
    records = value.get("widest_block_records", [])
    if value.get("state") != "terminal_complete":
        out.append("audit is not terminal")
    if (
        binding.get("raw_repeated_12_gram_count") != 1281
        or binding.get("raw_maximum_chapter_spread") != 69
        or binding.get("reader_facing_repeated_12_gram_count") != 0
        or binding.get("reader_facing_maximum_chapter_spread") != 0
    ):
        out.append("W3 raw/editorial binding drifted")
    if binding.get("sha256") != hashlib.sha256(W3.read_bytes()).hexdigest():
        out.append("W3 digest binding drifted")
    if len(records) != 21 or summary.get("widest_block_count") != 21:
        out.append("widest-block denominator drifted")
    if len({row.get("sha256") for row in records}) != len(records):
        out.append("widest-block fingerprints are not unique")
    for row in records:
        text = row.get("normalized_text", "")
        if row.get("sha256") != hashlib.sha256(text.encode("utf-8")).hexdigest():
            out.append("widest-block text fingerprint drifted")
        chapter_ids = row.get("chapter_ids", [])
        expected_ids = hashlib.sha256(
            json.dumps(chapter_ids, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        if row.get("chapter_ids_sha256") != expected_ids:
            out.append("widest-block chapter-set fingerprint drifted")
        if (
            row.get("chapter_spread") != 69
            or len(chapter_ids) != 69
            or row.get("word_tokens") != 12
        ):
            out.append("widest-block scope drifted")
        if (
            row.get("reader_visible") is not False
            or row.get("generated") is not True
            or row.get("structured") is not True
            or row.get("source_only") is not True
            or row.get("owner") != "scripts/sync_chapter_source_crosswalks.py"
            or row.get("disposition") != "generate"
        ):
            out.append("widest-block ownership classification drifted")
    if (
        summary.get("classified_block_count") != 21
        or summary.get("generated_source_reconciliation_block_count") != 21
        or summary.get("reader_visible_widest_block_count") != 0
        or summary.get("unjustified_widest_block_count") != 0
        or summary.get("exit_passed") is not True
    ):
        out.append("raw-scaffold exit summary drifted")
    control = value.get("negative_control", {})
    if control.get("copied_reader_facing_prose_disposition") != "rejected":
        out.append("copied reader-facing negative control drifted")
    if value.get("support_state_effect") != "none" or value.get("release_effect") != "none":
        out.append("audit claims support or release movement")
    return sorted(set(out))


def main() -> None:
    value = load(ARTIFACT)
    jsonschema.Draft202012Validator(load(SCHEMA)).validate(value)
    failures = errors(value)
    rebuilt = load_module(BUILDER, "p6_9_raw_builder").build()
    if rebuilt != value:
        failures.append("tracked audit does not match a fresh deterministic rebuild")
    w3_validator = load_module(W3_VALIDATOR, "p7_1a_w3_validator")
    if not w3_validator.admission_errors(COPIED.read_text(encoding="utf-8")):
        failures.append("copied reader-facing scaffold negative control was accepted")
    report = " ".join(REPORT.read_text(encoding="utf-8").split())
    for phrase in (
        "terminal complete",
        "All **21** widest fingerprints",
        "unjustified count is **0**",
        "copied-scaffold negative fixture remains rejected",
    ):
        if phrase not in report:
            failures.append(f"report missing: {phrase}")

    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("state", lambda item: item.__setitem__("state", "active")),
        ("raw denominator", lambda item: item["w3_binding"].__setitem__("raw_repeated_12_gram_count", 0)),
        ("raw spread", lambda item: item["w3_binding"].__setitem__("raw_maximum_chapter_spread", 66)),
        ("W3 digest", lambda item: item["w3_binding"].__setitem__("sha256", "0" * 64)),
        ("record deletion", lambda item: item["widest_block_records"].pop()),
        ("fingerprint", lambda item: item["widest_block_records"][0].__setitem__("sha256", "0" * 64)),
        ("chapter set", lambda item: item["widest_block_records"][0]["chapter_ids"].pop()),
        ("reader visibility", lambda item: item["widest_block_records"][0].__setitem__("reader_visible", True)),
        ("generated ownership", lambda item: item["widest_block_records"][0].__setitem__("generated", False)),
        ("owner", lambda item: item["widest_block_records"][0].__setitem__("owner", "unowned")),
        ("exit", lambda item: item["summary"].__setitem__("exit_passed", False)),
        ("support", lambda item: item.__setitem__("support_state_effect", "promoted")),
    ]
    baseline = set(errors(value))
    for label, mutation in mutations:
        candidate = copy.deepcopy(value)
        mutation(candidate)
        if not set(errors(candidate)) - baseline:
            failures.append(f"negative mutation accepted: {label}")
    if failures:
        raise SystemExit(
            "P6.9 raw-scaffold ownership audit failed:\n - "
            + "\n - ".join(sorted(set(failures)))
        )
    print(
        "P6.9 raw-scaffold ownership audit passed: 21/21 widest fingerprints "
        "generated and owned; zero reader-visible or unjustified; 12 mutations rejected."
    )


if __name__ == "__main__":
    main()
