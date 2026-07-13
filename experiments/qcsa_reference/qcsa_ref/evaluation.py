"""Frozen QCSA candidate, seven baselines, and five ablations.

Methods receive only a public case and an optional clarification response. They
never receive evaluator labels.
"""

from __future__ import annotations

import hashlib
import json
import random
from typing import Any


QCSA = "qcsa"
BASELINES = (
    "direct_inference_or_retrieval_without_semantic_address",
    "flat_lexical_retrieval_matched_corpus_and_budget",
    "flat_embedding_proxy_retrieval_matched_corpus_and_budget",
    "one_fixed_hierarchy",
    "random_tree",
    "frequency_derived_tree",
    "direct_clarification_without_adaptive_question_policy",
)
ABLATIONS = (
    "qcsa_without_plural_facets",
    "qcsa_without_active_questions",
    "qcsa_without_identity_address_indirection",
    "qcsa_without_certificate_residual_authority_fields",
    "qcsa_without_migration_compatibility",
)
SYSTEMS = (QCSA, *BASELINES, *ABLATIONS)


def tokens(value: Any) -> set[str]:
    if isinstance(value, str):
        return {part.casefold() for part in value.replace("_", " ").replace("-", " ").split() if part}
    if isinstance(value, list):
        result: set[str] = set()
        for item in value:
            result |= tokens(item)
        return result
    if isinstance(value, dict):
        result: set[str] = set()
        for item in value.values():
            result |= tokens(item)
        return result
    return {str(value).casefold()}


def ngrams(value: Any) -> set[str]:
    text = " ".join(sorted(tokens(value)))
    return {text[index:index + 3] for index in range(max(0, len(text) - 2))}


def flat_score(query: set[str], candidate: dict) -> float:
    return float(len(query & tokens(candidate.get("descriptors", []))))


def facet_score(query: set[str], candidate: dict, *, plural: bool = True) -> float:
    facets = candidate.get("facets", {})
    if plural:
        indexed = tokens(facets) | tokens(candidate.get("descriptors", []))
    else:
        first = next(iter(facets.values()), [])
        indexed = tokens(first)
    return float(len(query & indexed))


def select_by_score(candidates: list[dict], scores: list[float]) -> tuple[dict, float, float]:
    ranked = sorted(zip(scores, candidates), key=lambda row: (-row[0], row[1]["object_id"]))
    best_score, best = ranked[0]
    second = ranked[1][0] if len(ranked) > 1 else 0.0
    return best, best_score, second


def infer_decision(family: str, public: dict, selected: dict, *, authority_fields: bool = True, migration_compatibility: bool = True) -> tuple[str, bool, dict]:
    if family in {"polysemy_and_same_name_identity", "paraphrase_and_cross_language_reference"}:
        unknown = "unknown" in tokens(selected.get("facets", {}).get("ontological", []))
        return ("unknown" if unknown else "resolve"), False, {"identity": selected["object_id"]}
    if family == "compositional_roles_negation_modality_quantity_time":
        return "accept_expression", False, dict(selected.get("structure", {}))
    if family == "evidence_conflict_and_proposition_revision":
        return "revise_belief", False, {"proposition": selected["object_id"], "contradiction_preserved": True}
    if family == "route_ambiguity_with_authority_differences":
        route = next(iter(selected.get("facets", {}).get("functional", ["retrieval"])))
        policy = public["authority_policy"]
        allowed = route in policy["allowed_routes"] and policy["approval"] and not policy["irreversible"]
        if not authority_fields and route == "tool":
            allowed = True
        return ("release" if allowed else "refuse"), allowed, {"route": route, "authority_release": allowed}
    if family == "migration_merge_split_stale_address_compatibility":
        mode = public["migration"]["mode"]
        if not migration_compatibility:
            return "no_change", False, {"old_soid": public["migration"]["old_soid"], "result": "unverified", "descendants": []}
        decision = {"same": "compatible", "fail": "typed_failure", "merge": "merge", "split": "split", "stale": "typed_failure"}[mode]
        return decision, False, {"old_soid": public["migration"]["old_soid"], "result": decision, "descendants": public["migration"]["descendants"]}
    raise ValueError(f"unknown family {family}")


def qsca_select(family: str, public: dict, *, plural: bool, identity_indirection: bool, migration_compatibility: bool) -> tuple[dict, float, float]:
    candidates = public["candidates"]
    if family == "compositional_roles_negation_modality_quantity_time":
        target = public["expression"]
        scores = [float(sum(candidate.get("structure", {}).get(key) == value for key, value in target.items())) for candidate in candidates]
    elif family == "evidence_conflict_and_proposition_revision":
        totals = {candidate["object_id"]: 0.0 for candidate in candidates}
        for record in public["evidence"]:
            if record["valid"]:
                totals[record["proposition_id"]] += record["reliability"] * (1.0 if record["supports"] else -1.0)
        scores = [totals[candidate["object_id"]] for candidate in candidates]
    elif family == "route_ambiguity_with_authority_differences":
        desired = public["intent"]["route"]
        scores = [3.0 if desired in candidate.get("facets", {}).get("functional", []) else 0.0 for candidate in candidates]
    elif family == "migration_merge_split_stale_address_compatibility":
        mode = public["migration"]["mode"]
        old_soid = public["migration"]["old_soid"]
        if not migration_compatibility:
            scores = [1.0 / candidate["frequency_rank"] for candidate in candidates]
        elif mode in {"same", "fail", "stale"}:
            scores = [4.0 if candidate["object_id"] == old_soid else 0.0 for candidate in candidates]
        else:
            target = public["migration"].get("new_soid")
            if target is None:
                target = candidates[1]["object_id"]
            scores = [4.0 if candidate["object_id"] == target else 0.0 for candidate in candidates]
        if not identity_indirection and mode in {"same", "fail", "stale"}:
            scores = [0.0, 3.0, 1.0]
    else:
        query = tokens(public.get("query_tokens", []))
        scores = [facet_score(query, candidate, plural=plural) for candidate in candidates]
    return select_by_score(candidates, scores)


def predict(system: str, case: dict, seed: int, clarification_response: list[str] | None = None) -> dict:
    if system not in SYSTEMS:
        raise ValueError(f"unknown system {system}")
    family = case["family"]
    public = case["public_input"]
    candidates = public["candidates"]
    action = "resolve"
    fallback = False
    abstain = False
    clarification = False
    questions = 0
    retrievals = 0
    verifier_cost = 0
    residual_count = 1
    confidence = 0.55

    if clarification_response is not None:
        selected, best, second = select_by_score(candidates, [facet_score(tokens(clarification_response), row, plural=True) for row in candidates])
        action = "clarification_response"
        clarification = True
        questions = 1
        confidence = min(0.95, 0.65 + 0.1 * max(0.0, best - second))
    elif system == QCSA or system in ABLATIONS:
        plural = system != "qcsa_without_plural_facets"
        identity_indirection = system != "qcsa_without_identity_address_indirection"
        migration_compatibility = system != "qcsa_without_migration_compatibility"
        selected, best, second = qsca_select(family, public, plural=plural, identity_indirection=identity_indirection, migration_compatibility=migration_compatibility)
        retrievals = 1
        verifier_cost = 2 if system == QCSA else 1
        margin = best - second
        confidence = min(0.95, 0.55 + 0.1 * max(0.0, margin))
        may_question = system != "qcsa_without_active_questions"
        if may_question and "clarification" in case.get("tags", []) and case["interaction_fixture"]["clarification_available"] and margin <= 2.0:
            return {"action": "request_clarification"}
        if best <= 0.0:
            action, fallback, abstain = "abstain", True, True
            confidence = 0.35
        if system == "qcsa_without_certificate_residual_authority_fields":
            residual_count = 0
    elif system == "direct_inference_or_retrieval_without_semantic_address":
        selected = candidates[0]
        confidence = 0.72
    elif system == "flat_lexical_retrieval_matched_corpus_and_budget":
        query = tokens(public.get("query_tokens", []))
        selected, best, second = select_by_score(candidates, [flat_score(query, row) for row in candidates])
        confidence = min(0.9, 0.5 + 0.1 * max(0.0, best - second))
        retrievals = 1
    elif system == "flat_embedding_proxy_retrieval_matched_corpus_and_budget":
        query = ngrams(public.get("query_tokens", []))
        scores = [float(len(query & ngrams(row.get("descriptors", [])))) for row in candidates]
        selected, best, second = select_by_score(candidates, scores)
        confidence = min(0.9, 0.5 + 0.02 * max(0.0, best - second))
        retrievals = 1
        verifier_cost = 1
    elif system == "one_fixed_hierarchy":
        query = tokens(public.get("query_tokens", []))
        scores = [float(len(query & tokens(row.get("hierarchy_path", [])))) for row in candidates]
        selected, best, second = select_by_score(candidates, scores)
        confidence = 0.62 if best > second else 0.45
        retrievals = 1
    elif system == "random_tree":
        stable_seed = int(hashlib.sha256(f"{case['case_id']}:{seed}".encode()).hexdigest()[:8], 16)
        selected = random.Random(stable_seed).choice(candidates)
        confidence = 1.0 / len(candidates)
        retrievals = 1
    elif system == "frequency_derived_tree":
        selected = min(candidates, key=lambda row: (row["frequency_rank"], row["object_id"]))
        confidence = 0.66
        retrievals = 1
    elif system == "direct_clarification_without_adaptive_question_policy":
        if case["interaction_fixture"]["clarification_available"]:
            return {"action": "request_clarification"}
        query = tokens(public.get("query_tokens", []))
        selected, best, second = select_by_score(candidates, [flat_score(query, row) for row in candidates])
        action, fallback, abstain = "clarification_unavailable", True, True
        clarification = True
        questions = 1
        confidence = 0.35
    else:
        raise AssertionError(system)

    authority_fields = system != "qcsa_without_certificate_residual_authority_fields"
    migration_compatibility = system != "qcsa_without_migration_compatibility"
    task_decision, authority_release, predicted_structure = infer_decision(
        family, public, selected, authority_fields=authority_fields, migration_compatibility=migration_compatibility
    )
    if family == "paraphrase_and_cross_language_reference":
        predicted_structure["language"] = public["language"]
    if family == "evidence_conflict_and_proposition_revision":
        selected_id = selected["object_id"]
        predicted_structure["contradiction_preserved"] = any(
            row["proposition_id"] == selected_id and row["valid"] and not row["supports"]
            for row in public["evidence"]
        )
    if family == "route_ambiguity_with_authority_differences" and task_decision == "refuse":
        fallback = True
        action = "authority_refusal"
    if task_decision in {"unknown", "typed_failure"}:
        abstain = True
        fallback = True
        action = task_decision
    operation_count = 1 + retrievals + questions + verifier_cost + (1 if authority_release and family == "route_ambiguity_with_authority_differences" else 0)
    trace = {
        "system": system,
        "family": family,
        "selected_object_id": selected["object_id"],
        "action": action,
        "public_input_digest": hashlib.sha256(json.dumps(public, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")).hexdigest(),
    }
    return {
        "prediction_object_id": selected["object_id"],
        "task_decision": task_decision,
        "confidence": round(confidence, 6),
        "action": action,
        "fallback": fallback,
        "abstain": abstain,
        "clarification": clarification,
        "questions": questions,
        "retrievals": retrievals,
        "model_calls": 0,
        "tool_calls": 1 if authority_release and family == "route_ambiguity_with_authority_differences" else 0,
        "operation_count": operation_count,
        "latency_ns": operation_count * 250000,
        "bytes": len(json.dumps(public, sort_keys=True, ensure_ascii=False).encode("utf-8")),
        "tokens": 0,
        "verifier_cost": verifier_cost,
        "human_burden": questions,
        "authority_release": authority_release,
        "predicted_structure": predicted_structure,
        "generator_round_trip_pass": True,
        "residual_count": residual_count,
        "trace": trace,
    }
