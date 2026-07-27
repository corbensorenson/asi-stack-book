#!/usr/bin/env python3
from __future__ import annotations

import copy
import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any, Callable

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "evidence_quality/p7_1a_w3_inheritance_guard.json"
SCHEMA = ROOT / "schemas/p7_1a_w3_inheritance_guard.schema.json"
REPORT = ROOT / "docs/p7_1a_w3_inheritance_guard.md"
BUILDER = ROOT / "scripts/build_p7_1a_w3_inheritance_guard.py"
COPIED = ROOT / "tests/fixtures/p7_1a_w3_inheritance_guard/copied_scaffold.qmd"
DISTINCT = ROOT / "tests/fixtures/p7_1a_w3_inheritance_guard/distinct_chapter.qmd"
METHOD_LINK = "living-book-methodology.qmd#shared-chapter-lifecycle-method"
COMMON_DIAGRAM = 'A["Declared purpose and bounded authority"]'
COMMON_TEST = "| Contract completeness | Reject missing identity, authority, scope, version, consumer, residual, or expiry fields. | planned |"
GENERIC_EVIDENCE = "freeze the mechanism, authority, comparator set, tuning and"
GENERIC_HANDOFF = "consumes this chapter's bounded outputs without inheriting"


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_builder() -> Any:
    spec = importlib.util.spec_from_file_location("p7_1a_w3_builder", BUILDER)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import W3 builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def admission_errors(text: str) -> list[str]:
    out: list[str] = []
    inherited = [
        COMMON_DIAGRAM in text,
        COMMON_TEST in text,
        GENERIC_EVIDENCE in text,
        GENERIC_HANDOFF in text,
    ]
    if sum(inherited) >= 2:
        out.append("candidate inherits two or more retired scaffold signals")
    source_ids = re.findall(r"(?m)^\s{2}-\s+([a-zA-Z0-9_.-]+)\s*$", text)
    test_rows = re.findall(r"(?m)^\| [^-\n][^|]* \| [^|]+ \| (?:planned|implemented) \|$", text)
    distinctness = {
        "methodology_link": METHOD_LINK in text,
        "unique_claim": "support:" in text and "[Synthetic" not in text[:200],
        "multiple_sources": len(source_ids) >= 2,
        "ownership_boundary": "## Interfaces and ownership boundary" in text and "owns only" in text,
        "evidence_plan": "## Evidence and falsification program" in text and "simpler baseline" in text,
        "unique_diagram": "```{mermaid}" in text and COMMON_DIAGRAM not in text,
        "specific_test_matrix": len(test_rows) >= 4 and COMMON_TEST not in text,
        "specific_handoff": "## Handoff" in text and GENERIC_HANDOFF not in text,
    }
    if sum(distinctness.values()) < 6:
        missing = sorted(key for key, value in distinctness.items() if not value)
        out.append("candidate lacks distinct chapter contract: " + ", ".join(missing))
    return out


def artifact_errors(data: dict[str, Any]) -> list[str]:
    out: list[str] = []
    if data.get("state") != "terminal_complete":
        out.append("packet is not terminal")
    corpus = data.get("corpus", {})
    if corpus.get("manifest_chapter_count") != 84 or len(set(corpus.get("chapter_ids", []))) != 84:
        out.append("84-chapter corpus drifted")
    thresholds = data.get("thresholds_frozen_before_edits", {})
    if (
        thresholds.get("n_gram_size") != 12
        or thresholds.get("minimum_chapter_spread") != 8
        or thresholds.get("exact_block_minimum_word_tokens") != 24
        or thresholds.get("exact_block_minimum_chapter_spread") != 5
    ):
        out.append("frozen thresholds drifted")
    measurements = data.get("measurements", {})
    raw = measurements.get("raw_complete_qmd", {})
    editorial = measurements.get("editorial_narrative", {})
    if raw.get("baseline", {}).get("distinct_repeated_12_grams") != 1921:
        out.append("raw baseline repetition count drifted")
    if raw.get("baseline", {}).get("maximum_chapter_spread") != 64:
        out.append("raw generated-projection maximum spread drifted")
    if editorial.get("baseline", {}).get("distinct_repeated_12_grams") != 812:
        out.append("editorial baseline repetition count drifted")
    if editorial.get("baseline", {}).get("maximum_chapter_spread") != 14:
        out.append("editorial baseline maximum spread drifted")
    if editorial.get("current", {}).get("distinct_repeated_12_grams") != 0:
        out.append("current editorial projection contains an inherited high-spread 12-gram")
    for key in ("mermaid_fingerprints", "codex_test_table_fingerprints"):
        metric = measurements.get(key, {})
        if metric.get("baseline", {}).get("maximum_chapter_spread") != 10:
            out.append(f"{key}: copied baseline fingerprint not reproduced")
        if metric.get("current", {}).get("maximum_chapter_spread") != 0:
            out.append(f"{key}: copied fingerprint remains")
    contract = data.get("centralized_contract", {})
    if (
        contract.get("anchor") != "shared-chapter-lifecycle-method"
        or len(set(contract.get("repaired_chapter_ids", []))) != 10
    ):
        out.append("central method owner or ten-chapter repair set drifted")
    reviews = data.get("semantic_diff_review", [])
    if len(reviews) != 10:
        out.append("semantic review denominator drifted")
    for row in reviews:
        if not all(
            row.get(key) is True
            for key in ("methodology_link_present", "common_diagram_removed", "common_test_scaffold_removed")
        ):
            out.append(f"{row.get('chapter_id')}: local distinctness repair regressed")
        missing = row.get("missing_meaning_atoms", {})
        if any(missing.get(key) for key in missing):
            out.append(f"{row.get('chapter_id')}: meaning atom deleted")
        if row.get("support_state_movement") is not False:
            out.append(f"{row.get('chapter_id')}: support state moved")
    reconciliation = data.get("claim_review_reconciliation", {})
    expected_reconciliation = {
        "baseline_prose_candidate_count": 3444,
        "current_prose_candidate_count": 3386,
        "unchanged_prose_candidate_count": 3198,
        "retired_inherited_prose_candidate_count": 246,
        "added_domain_specific_prose_candidate_count": 188,
        "baseline_structured_atom_count": 4067,
        "current_structured_atom_count": 4058,
        "current_pending_prose_candidate_count": 0,
        "completed_semantic_chapter_sweep_count": 64,
        "affected_review_chapter_count": 11,
        "new_material_atom_count": 0,
        "support_state_effect": "none",
    }
    if reconciliation != expected_reconciliation:
        out.append("claim-review reconciliation denominator or no-promotion boundary drifted")
    custody = data.get("meaning_custody", {})
    zero_fields = (
        "unique_claim_markers_deleted",
        "assigned_source_ids_deleted",
        "equations_deleted",
        "proof_tags_deleted",
        "protocol_or_schema_refs_deleted",
        "chapter_core_support_movements",
    )
    if any(custody.get(key) != 0 for key in zero_fields):
        out.append("meaning-custody ledger records a deletion or support movement")
    if custody.get("generated_projection_owners_preserved") is not True:
        out.append("generated projection ownership was not preserved")
    guard = data.get("prospective_guard", {})
    if (
        guard.get("copied_scaffold_fixture_disposition") != "rejected"
        or guard.get("distinct_chapter_fixture_disposition") != "accepted"
        or guard.get("negative_mutations_rejected") != 18
    ):
        out.append("prospective fixture or mutation receipt drifted")
    if any(data.get(key) != "none" for key in ("support_state_effect", "release_effect", "publication_effect")):
        out.append("W3 claims an unauthorized support, release, or publication effect")
    return out


def main() -> None:
    artifact = load(ARTIFACT)
    jsonschema.Draft202012Validator(load(SCHEMA)).validate(artifact)
    failures = artifact_errors(artifact)
    rebuilt = load_builder().build()
    if rebuilt != artifact:
        failures.append("tracked W3 artifact does not match a fresh deterministic rebuild")
    copied_errors = admission_errors(COPIED.read_text(encoding="utf-8"))
    distinct_errors = admission_errors(DISTINCT.read_text(encoding="utf-8"))
    if not copied_errors:
        failures.append("copied-scaffold negative fixture was accepted")
    if distinct_errors:
        failures.append("distinct positive fixture was rejected: " + "; ".join(distinct_errors))
    methodology = (ROOT / "chapters/living-book-methodology.qmd").read_text(encoding="utf-8")
    if "{#shared-chapter-lifecycle-method}" not in methodology or "prospective inheritance guard" not in methodology:
        failures.append("central methodology owner is missing")
    report = REPORT.read_text(encoding="utf-8")
    report_compact = re.sub(r"\s+", " ", report)
    for phrase in (
        "terminal complete",
        "812",
        "to **0** distinct repeated 12-grams",
        "source/evidence projections from reader-facing prose",
        "tracked copied-scaffold fixture is rejected",
    ):
        if phrase not in report_compact:
            failures.append(f"W3 report missing: {phrase}")

    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("state", lambda value: value.__setitem__("state", "active")),
        ("scope", lambda value: value["corpus"].__setitem__("manifest_chapter_count", 83)),
        ("duplicate chapter", lambda value: value["corpus"]["chapter_ids"].__setitem__(1, value["corpus"]["chapter_ids"][0])),
        ("ngram", lambda value: value["thresholds_frozen_before_edits"].__setitem__("n_gram_size", 10)),
        ("spread", lambda value: value["thresholds_frozen_before_edits"].__setitem__("minimum_chapter_spread", 12)),
        ("block words", lambda value: value["thresholds_frozen_before_edits"].__setitem__("exact_block_minimum_word_tokens", 100)),
        ("block spread", lambda value: value["thresholds_frozen_before_edits"].__setitem__("exact_block_minimum_chapter_spread", 9)),
        ("raw baseline", lambda value: value["measurements"]["raw_complete_qmd"]["baseline"].__setitem__("distinct_repeated_12_grams", 0)),
        ("editorial baseline", lambda value: value["measurements"]["editorial_narrative"]["baseline"].__setitem__("distinct_repeated_12_grams", 0)),
        ("editorial current", lambda value: value["measurements"]["editorial_narrative"]["current"].__setitem__("distinct_repeated_12_grams", 1)),
        ("diagram restored", lambda value: value["measurements"]["mermaid_fingerprints"]["current"].__setitem__("maximum_chapter_spread", 10)),
        ("tests restored", lambda value: value["measurements"]["codex_test_table_fingerprints"]["current"].__setitem__("maximum_chapter_spread", 10)),
        ("repair removed", lambda value: value["centralized_contract"]["repaired_chapter_ids"].pop()),
        ("method link deleted", lambda value: value["semantic_diff_review"][0].__setitem__("methodology_link_present", False)),
        ("claim deleted", lambda value: value["meaning_custody"].__setitem__("unique_claim_markers_deleted", 1)),
        ("source deleted", lambda value: value["meaning_custody"].__setitem__("assigned_source_ids_deleted", 1)),
        ("support moved", lambda value: value["meaning_custody"].__setitem__("chapter_core_support_movements", 1)),
        ("publication invented", lambda value: value.__setitem__("publication_effect", "published")),
    ]
    baseline_errors = set(artifact_errors(artifact))
    for label, mutation in mutations:
        candidate = copy.deepcopy(artifact)
        mutation(candidate)
        if not set(artifact_errors(candidate)) - baseline_errors:
            failures.append(f"negative mutation accepted: {label}")
    if len(mutations) != artifact["prospective_guard"]["negative_mutations_rejected"]:
        failures.append("negative mutation denominator drifted")
    if failures:
        raise SystemExit("P7.1a W3 inheritance guard failed:\n - " + "\n - ".join(failures))
    print(
        "P7.1a W3 inheritance guard passed: 84 chapters; editorial repeated "
        "12-grams 812 -> 0; copied diagram/test spread 10 -> 0; copied fixture "
        "rejected; distinct fixture accepted; 18 mutations rejected; support effect none."
    )


if __name__ == "__main__":
    main()
