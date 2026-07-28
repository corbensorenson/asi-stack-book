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
ARTIFACT = ROOT / "evidence_quality/p6_9_proof_evidence_handoff.json"
SCHEMA = ROOT / "schemas/p6_9_proof_evidence_handoff.schema.json"
REPORT = ROOT / "docs/p6_9_proof_evidence_handoff.md"
BUILDER = ROOT / "scripts/build_p6_9_proof_evidence_handoff.py"
CONTRACT = ROOT / "evidence_quality/chapter_substance_contract.json"
RAW_AUDIT = ROOT / "evidence_quality/p6_9_raw_scaffold_ownership_audit.json"
W3 = ROOT / "evidence_quality/p7_1a_w3_inheritance_guard.json"


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_builder() -> Any:
    spec = importlib.util.spec_from_file_location("p6_9_handoff_builder", BUILDER)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import P6.9 handoff builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def errors(value: dict[str, Any]) -> list[str]:
    out: list[str] = []
    summary = value.get("summary", {})
    chapters = value.get("chapter_records", [])
    if value.get("state") != "terminal_complete":
        out.append("handoff is not terminal")
    if value.get("source_contract", {}).get("sha256") != hashlib.sha256(CONTRACT.read_bytes()).hexdigest():
        out.append("chapter-substance digest binding drifted")
    if value.get("raw_scaffold_exit", {}).get("sha256") != hashlib.sha256(RAW_AUDIT.read_bytes()).hexdigest():
        out.append("raw-scaffold digest binding drifted")
    if value.get("w3_binding", {}).get("sha256") != hashlib.sha256(W3.read_bytes()).hexdigest():
        out.append("W3 digest binding drifted")
    if len(chapters) != 23 or len({row.get("chapter_id") for row in chapters}) != 23:
        out.append("chapter denominator or identity drifted")
    concept_keys = set()
    for chapter in chapters:
        if (
            chapter.get("concept_count") != 8
            or len(chapter.get("concepts", [])) != 8
            or chapter.get("chapter_sha256") != chapter.get("semantic_review_sha256")
        ):
            out.append(f"{chapter.get('chapter_id')}: digest or concept denominator drifted")
        for concept in chapter.get("concepts", []):
            key = (chapter.get("chapter_id"), concept.get("concept_id"))
            if key in concept_keys:
                out.append("duplicate concept identity")
            concept_keys.add(key)
            if not concept.get("source_ids") or not concept.get("atom_refs"):
                out.append(f"{key}: source or atom identity missing")
            for ref in concept.get("atom_refs", []):
                if ref.get("owner") != chapter.get("chapter_id"):
                    out.append(f"{key}: atom owner mismatch")
                if not all(
                    ref.get(field)
                    for field in (
                        "atom_id",
                        "proposition",
                        "falsifier",
                        "evidence_lanes",
                        "evidence_route",
                        "maximum_inference",
                        "unresolved_challenge",
                    )
                ):
                    out.append(f"{key}: handoff identity incomplete")
    exact_counts = (
        "chapter_count",
        "concept_count",
        "concepts_with_source_identity_count",
        "concepts_with_atom_identity_count",
        "concepts_with_falsifier_count",
        "concepts_with_evidence_lane_count",
        "concepts_with_maximum_inference_count",
        "concepts_with_unresolved_challenge_count",
    )
    expected = {
        "chapter_count": 23,
        "concept_count": 184,
        "concepts_with_source_identity_count": 184,
        "concepts_with_atom_identity_count": 184,
        "concepts_with_falsifier_count": 184,
        "concepts_with_evidence_lane_count": 184,
        "concepts_with_maximum_inference_count": 184,
        "concepts_with_unresolved_challenge_count": 184,
    }
    if any(summary.get(key) != expected[key] for key in exact_counts):
        out.append("handoff completion denominator drifted")
    if summary.get("missing_handoff_identity_count") != 0:
        out.append("handoff reports missing identities")
    if value.get("raw_scaffold_exit", {}).get("exit_passed") is not True:
        out.append("raw-scaffold exit bypassed")
    if value.get("w3_binding", {}).get("reader_facing_repeated_12_gram_count") != 0:
        out.append("W3 terminal boundary bypassed")
    if value.get("support_state_effect") != "none" or value.get("release_effect") != "none":
        out.append("handoff claims support or release movement")
    return sorted(set(out))


def main() -> None:
    value = load(ARTIFACT)
    jsonschema.Draft202012Validator(load(SCHEMA)).validate(value)
    failures = errors(value)
    if load_builder().build() != value:
        failures.append("tracked handoff does not match a fresh deterministic rebuild")
    report = " ".join(REPORT.read_text(encoding="utf-8").split())
    for phrase in (
        "terminal complete",
        "hands off **184** reviewed concepts",
        "across **23** exact chapter digests",
        "missing identity count is **0**",
    ):
        if phrase not in report:
            failures.append(f"report missing: {phrase}")

    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("state", lambda item: item.__setitem__("state", "active")),
        ("contract digest", lambda item: item["source_contract"].__setitem__("sha256", "0" * 64)),
        ("raw digest", lambda item: item["raw_scaffold_exit"].__setitem__("sha256", "0" * 64)),
        ("W3 digest", lambda item: item["w3_binding"].__setitem__("sha256", "0" * 64)),
        ("chapter deletion", lambda item: item["chapter_records"].pop()),
        ("concept deletion", lambda item: item["chapter_records"][0]["concepts"].pop()),
        ("source identity", lambda item: item["chapter_records"][0]["concepts"][0].__setitem__("source_ids", [])),
        ("atom identity", lambda item: item["chapter_records"][0]["concepts"][0].__setitem__("atom_refs", [])),
        ("falsifier", lambda item: item["chapter_records"][0]["concepts"][0]["atom_refs"][0].__setitem__("falsifier", "")),
        ("evidence lane", lambda item: item["chapter_records"][0]["concepts"][0]["atom_refs"][0].__setitem__("evidence_lanes", [])),
        ("maximum inference", lambda item: item["chapter_records"][0]["concepts"][0]["atom_refs"][0].__setitem__("maximum_inference", "")),
        ("unresolved challenge", lambda item: item["chapter_records"][0]["concepts"][0]["atom_refs"][0].__setitem__("unresolved_challenge", "")),
        ("raw exit", lambda item: item["raw_scaffold_exit"].__setitem__("exit_passed", False)),
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
            "P6.9 proof/evidence handoff failed:\n - "
            + "\n - ".join(sorted(set(failures)))
        )
    print(
        "P6.9 proof/evidence handoff passed: 23 chapters, 184 concepts, "
        "all required identities present, 14 mutations rejected, support effect none."
    )


if __name__ == "__main__":
    main()
