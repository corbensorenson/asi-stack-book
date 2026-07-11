#!/usr/bin/env python3
"""Recompute and validate the post-v2 routing/deliberation study."""
from __future__ import annotations

import copy

from build_canonical_public_status import ROOT, load_json, validate_against_schema
from run_post_v2_routing_deliberation import (
    CORPUS,
    DELIBERATION_ARMS,
    FAMILIES,
    ROUTING_ARMS,
    SEEDS,
    aggregate_deliberation,
    aggregate_routing,
    canonical_sha,
    deliberate_one,
    fit_router,
    route_one,
    specialist,
)


RESULT = ROOT / "experiments/post_v2_routing_deliberation/results/2026-07-10-local.json"
SCHEMA = ROOT / "schemas/post_v2_routing_deliberation_result.schema.json"
DOC = ROOT / "docs/post_v2_routing_deliberation.md"


def semantic_errors(result: dict, recompute: bool = True) -> list[str]:
    errors: list[str] = []
    corpus = load_json(CORPUS)
    if result.get("corpus_sha256") != corpus.get("corpus_sha256"):
        errors.append("result does not bind the frozen corpus digest")
    payload = copy.deepcopy(result)
    claimed = payload.pop("bundle_sha256", None)
    if claimed != canonical_sha(payload):
        errors.append("result bundle digest mismatch")
    if result.get("seeds") != [17, 29, 43]:
        errors.append("selective seed reporting detected")
    routing = result.get("routing", {})
    deliberation = result.get("deliberation", {})
    route_rows = routing.get("records", [])
    deliberation_rows = deliberation.get("records", [])
    if len(route_rows) != 900 or len(deliberation_rows) != 540 or len(routing.get("interference_counterfactuals", [])) != 180:
        errors.append("per-example record counts must be 900 routing, 540 deliberation, and 180 interference")
    if set(routing.get("arms", [])) != set(ROUTING_ARMS) or set(deliberation.get("arms", [])) != set(DELIBERATION_ARMS):
        errors.append("registered arms are missing or extra")
    if any(row.get("candidate_operations_used", 99) > row.get("candidate_operation_budget", -1) for row in route_rows + deliberation_rows):
        errors.append("retry or compute-budget inflation detected")
    oracle = [row for row in route_rows if row.get("arm") == "oracle_router"]
    if not oracle or any(not row.get("oracle_comparator_only") or not row.get("oracle_label_used") for row in oracle):
        errors.append("oracle comparator boundary was erased")
    fallback = [row for row in route_rows if row.get("arm") == "fallback_abstention"]
    if not fallback or sum(row.get("fallback_used", False) for row in fallback) != 0 or sum(row.get("abstained", False) for row in fallback) != 0:
        errors.append("tracked zero-use fallback/abstention result drifted")
    if sum(row.get("extra_compute_harm", False) for row in deliberation_rows if row.get("arm") == "fixed_three_step") != 15:
        errors.append("fixed-step extra-compute harm must retain all 15 cases")

    if recompute:
        train = [row for row in corpus["examples"] if row["split"] == "train"]
        test = [row for row in corpus["examples"] if row["split"] == "test"]
        fresh_routes, fresh_deliberation, fresh_interference = [], [], []
        for seed in SEEDS:
            learned = fit_router(train, seed)
            for example in test:
                fresh_routes.extend(route_one(example, arm, seed, learned) for arm in ROUTING_ARMS)
                fresh_interference.append({
                    "example_id": example["example_id"],
                    "seed": seed,
                    "correct_specialists": [family for family in FAMILIES if specialist(example, family, seed) == example["answer"]],
                    "wrong_specialist_outputs": {family: specialist(example, family, seed) for family in FAMILIES if family != example["family"]},
                })
                fresh_deliberation.extend(deliberate_one(example, arm, seed) for arm in DELIBERATION_ARMS)
        if fresh_routes != route_rows or aggregate_routing(fresh_routes) != routing.get("summary"):
            errors.append("routing records or summaries do not recompute")
        if fresh_interference != routing.get("interference_counterfactuals"):
            errors.append("specialist interference counterfactuals do not recompute")
        if fresh_deliberation != deliberation_rows or aggregate_deliberation(fresh_deliberation) != deliberation.get("summary"):
            errors.append("deliberation records or summaries do not recompute")
    if any(row.get("disposition") != "no_change" for row in result.get("claim_dispositions", [])) or result.get("support_state_effect") != "none":
        errors.append("bounded study cannot silently change chapter-core support")
    return errors


def main() -> None:
    missing = [path.relative_to(ROOT).as_posix() for path in (RESULT, SCHEMA, DOC, CORPUS) if not path.is_file()]
    if missing:
        raise SystemExit("missing routing/deliberation result artifacts: " + ", ".join(missing))
    result = load_json(RESULT)
    errors = validate_against_schema(result, load_json(SCHEMA), RESULT.relative_to(ROOT).as_posix())
    errors.extend(semantic_errors(result))
    doc = DOC.read_text(encoding="utf-8")
    for phrase in ("162 correct answers", "fallback/abstention thresholds never", "| Adaptive verifier stop | 179 | 236", "| Fixed three-step | 154 | 540", "15 initially correct answers wrong", "dispositioned independently"):
        if phrase not in doc:
            errors.append(f"readable report missing result boundary: {phrase}")
    mutations = []
    wrong_digest = copy.deepcopy(result); wrong_digest["bundle_sha256"] = "0" * 64; mutations.append(wrong_digest)
    seed_erasure = copy.deepcopy(result); seed_erasure["seeds"] = [17, 29]; mutations.append(seed_erasure)
    retry = copy.deepcopy(result); retry["deliberation"]["records"][0]["candidate_operations_used"] = 4; mutations.append(retry)
    oracle = copy.deepcopy(result); oracle["routing"]["records"][0]["oracle_comparator_only"] = False; mutations.append(oracle)
    fallback = copy.deepcopy(result); fallback["routing"]["records"][0]["fallback_used"] = True; mutations.append(fallback)
    harm = copy.deepcopy(result); next(row for row in harm["deliberation"]["records"] if row["arm"] == "fixed_three_step" and row["extra_compute_harm"])["extra_compute_harm"] = False; mutations.append(harm)
    promote = copy.deepcopy(result); promote["claim_dispositions"][0]["disposition"] = "promote"; mutations.append(promote)
    for mutation in mutations:
        if not semantic_errors(mutation, recompute=False):
            errors.append("a routing/deliberation outcome mutation was accepted")
    if errors:
        raise SystemExit("Routing/deliberation validation failed:\n - " + "\n - ".join(errors))
    print("Routing/deliberation validation passed: 3 seeds, 900 routing and 540 deliberation records recomputed; specialist routes 162/180 vs generalist 130/180; adaptive 179/180 in 236 steps, fixed 154/180 in 540 with 15 harms; zero fallback activations retained; 2 independent no-change dispositions; 7 rejecting mutations.")


if __name__ == "__main__":
    main()
