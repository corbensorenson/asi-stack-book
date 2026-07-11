#!/usr/bin/env python3
"""Validate the frozen routing/deliberation corpus before outcome runs."""
from __future__ import annotations

import copy
import hashlib
import json

from build_canonical_public_status import ROOT, load_json, validate_against_schema


CORPUS = ROOT / "experiments/post_v2_routing_deliberation/input/corpus.json"
SCHEMA = ROOT / "schemas/post_v2_routing_deliberation_corpus.schema.json"
PREREG = ROOT / "experiments/post_v2_evidence_program/preregistration.json"
BUILDER = ROOT / "scripts/build_post_v2_routing_deliberation_corpus.py"
RUNNER = ROOT / "scripts/run_post_v2_routing_deliberation.py"
FAMILIES = {"arithmetic", "string_transformation", "policy_decision", "structured_extraction"}


def semantic_errors(corpus: dict) -> list[str]:
    errors: list[str] = []
    examples = corpus.get("examples", [])
    if len(examples) != 300 or len({row.get("example_id") for row in examples}) != 300:
        errors.append("corpus must contain 300 uniquely identified examples")
    counts = {split: sum(row.get("split") == split for row in examples) for split in ("train", "validation", "test")}
    if counts != {"train": 180, "validation": 60, "test": 60} or corpus.get("split_counts") != counts:
        errors.append("split must remain 180/60/60")
    if {row.get("family") for row in examples} != FAMILIES:
        errors.append("the four frozen task families are not exact")
    for split in counts:
        family_counts = {family: sum(row.get("split") == split and row.get("family") == family for row in examples) for family in FAMILIES}
        expected = 45 if split == "train" else 15
        if set(family_counts.values()) != {expected}:
            errors.append(f"{split} is not family balanced")
    if any(len(row.get("features", [])) != 7 for row in examples):
        errors.append("all router feature vectors must have seven request-derived values")
    contract = corpus.get("compute_contract", {})
    if contract.get("routing_candidate_operation_cap") != 2 or contract.get("deliberation_candidate_operation_cap") != 3:
        errors.append("matched operation caps drifted")
    if not contract.get("oracle_router_is_comparator_only") or not contract.get("test_labels_forbidden_for_router_training"):
        errors.append("oracle/leakage boundaries are not frozen")
    digest_payload = copy.deepcopy(corpus)
    claimed = digest_payload.pop("corpus_sha256", None)
    observed = hashlib.sha256(json.dumps(digest_payload, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
    if claimed != observed:
        errors.append("corpus digest mismatch")
    return errors


def main() -> None:
    missing = [path.relative_to(ROOT).as_posix() for path in (CORPUS, SCHEMA, PREREG, BUILDER, RUNNER) if not path.is_file()]
    if missing:
        raise SystemExit("missing routing/deliberation setup: " + ", ".join(missing))
    corpus = load_json(CORPUS)
    errors = validate_against_schema(corpus, load_json(SCHEMA), CORPUS.relative_to(ROOT).as_posix())
    errors.extend(semantic_errors(corpus))
    prereg = load_json(PREREG)
    program = next(row for row in prereg["programs"] if row["program_id"] == "matched_routing_and_deliberation")
    if program["workload"]["example_count"] != 300 or program["workload"]["split"] != {"train": 180, "validation": 60, "test": 60}:
        errors.append("corpus differs from preregistered workload")
    runner = RUNNER.read_text(encoding="utf-8")
    for phrase in ("fit_router(train, seed)", "ROUTING_ARMS", "DELIBERATION_ARMS", "candidate_operation_budget", "oracle_comparator_only"):
        if phrase not in runner:
            errors.append(f"runner missing frozen execution surface: {phrase}")
    mutations = []
    overlap = copy.deepcopy(corpus); overlap["examples"][0]["example_id"] = overlap["examples"][1]["example_id"]; mutations.append(overlap)
    split_drift = copy.deepcopy(corpus); split_drift["examples"][0]["split"] = "test"; mutations.append(split_drift)
    compute_drift = copy.deepcopy(corpus); compute_drift["compute_contract"]["deliberation_candidate_operation_cap"] = 9; mutations.append(compute_drift)
    oracle_leak = copy.deepcopy(corpus); oracle_leak["compute_contract"]["oracle_router_is_comparator_only"] = False; mutations.append(oracle_leak)
    mutable = copy.deepcopy(corpus); mutable["frozen_before_test_outcomes"] = False; mutations.append(mutable)
    for mutation in mutations:
        schema_errors = validate_against_schema(mutation, load_json(SCHEMA), "mutation")
        if not schema_errors and not semantic_errors(mutation):
            errors.append("a corpus negative control was accepted")
    if errors:
        raise SystemExit("Routing/deliberation setup validation failed:\n - " + "\n - ".join(errors))
    print("Routing/deliberation setup passed: 300 unique examples, balanced 180/60/60 splits, 4 families, frozen 2/3 operation caps, comparator-only oracle, leakage boundary, content digest, and 5 rejecting controls.")


if __name__ == "__main__":
    main()
