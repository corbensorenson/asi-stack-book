#!/usr/bin/env python3
"""Execute the frozen matched routing and deliberation program."""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import time
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import sklearn
from sklearn.linear_model import LogisticRegression


ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "experiments/post_v2_routing_deliberation/input/corpus.json"
RESULT = ROOT / "experiments/post_v2_routing_deliberation/results/2026-07-10-local.json"
SEEDS = (17, 29, 43)
FAMILIES = ("arithmetic", "string_transformation", "policy_decision", "structured_extraction")
ROUTING_ARMS = ("oracle_router", "learned_router", "rule_router", "single_general_specialist", "fallback_abstention")
DELIBERATION_ARMS = ("adaptive_deliberation", "fixed_three_step", "no_deliberation")


def canonical_sha(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def unit_float(*parts: object) -> float:
    digest = hashlib.sha256("|".join(map(str, parts)).encode("utf-8")).hexdigest()
    return int(digest[:12], 16) / float(16**12)


def truth(example: dict) -> str:
    family, payload = example["family"], example["payload"]
    if family == "arithmetic":
        a, b, op = payload["a"], payload["b"], payload["op"]
        return str(a + b if op == "add" else a * b if op == "product" else a - b)
    if family == "string_transformation":
        text, op = payload["text"], payload["op"]
        return text.upper() if op == "uppercase" else text[::-1] if op == "reverse" else text.replace("-", "_")
    if family == "policy_decision":
        return "approve" if payload["authorized"] and payload["risk"] <= 4 else "deny"
    return json.dumps({"count": payload["count"], "name": payload["name"]}, sort_keys=True, separators=(",", ":"))


def corrupt(answer: str) -> str:
    return "__incorrect__" if answer != "__incorrect__" else "__incorrect_again__"


def specialist(example: dict, selected_family: str, seed: int) -> str:
    if selected_family != example["family"]:
        return "__unhandled__"
    answer = truth(example)
    return corrupt(answer) if unit_float("specialist", example["example_id"], seed) < 0.08 else answer


def general_specialist(example: dict, seed: int) -> str:
    answer = truth(example)
    return answer if unit_float("general", example["example_id"], seed) < 0.72 else corrupt(answer)


def rule_route(request: str) -> str:
    lower = request.lower()
    if any(word in lower for word in ("extract", "field", "name=")):
        return "structured_extraction"
    if any(word in lower for word in ("access", "risk=", "authorized=")):
        return "policy_decision"
    if any(word in lower for word in ("uppercase", "reverse", "replace", " text ")):
        return "string_transformation"
    return "arithmetic"


def fit_router(train: list[dict], seed: int) -> LogisticRegression:
    x_train = np.asarray([row["features"] for row in train], dtype=float)
    y_train = np.asarray([row["family"] for row in train])
    model = LogisticRegression(max_iter=500, random_state=seed)
    model.fit(x_train, y_train)
    return model


def route_one(example: dict, arm: str, seed: int, learned: LogisticRegression) -> dict:
    expected = example["answer"]
    fallback_used = False
    abstained = False
    confidence = None
    if arm == "oracle_router":
        selected = example["family"]
        output = specialist(example, selected, seed)
    elif arm == "rule_router":
        selected = rule_route(example["request"])
        output = specialist(example, selected, seed)
    elif arm == "learned_router":
        probabilities = learned.predict_proba(np.asarray([example["features"]], dtype=float))[0]
        index = int(np.argmax(probabilities))
        selected = str(learned.classes_[index])
        confidence = float(probabilities[index])
        output = specialist(example, selected, seed)
    elif arm == "single_general_specialist":
        selected = "general"
        output = general_specialist(example, seed)
    else:
        probabilities = learned.predict_proba(np.asarray([example["features"]], dtype=float))[0]
        index = int(np.argmax(probabilities))
        selected = str(learned.classes_[index])
        confidence = float(probabilities[index])
        if confidence < 0.45:
            abstained, output = True, None
        elif confidence < 0.92:
            fallback_used, selected = True, "general"
            output = general_specialist(example, seed)
        else:
            output = specialist(example, selected, seed)
    return {
        "example_id": example["example_id"],
        "family": example["family"],
        "seed": seed,
        "arm": arm,
        "selected_route": selected,
        "confidence": None if confidence is None else round(confidence, 8),
        "output": output,
        "correct": output == expected,
        "covered": output is not None,
        "fallback_used": fallback_used,
        "abstained": abstained,
        "candidate_operation_budget": 2,
        "candidate_operations_used": 2,
        "padding_operation_counted": arm == "single_general_specialist",
        "oracle_label_used": arm == "oracle_router",
        "oracle_comparator_only": arm == "oracle_router",
    }


def critic_candidate(example: dict, seed: int, prior: str) -> str:
    computed = truth(example)
    if unit_float("critic", example["example_id"], seed) < 0.16:
        return corrupt(computed)
    return computed


def verify(example: dict, candidate: str) -> bool:
    return candidate == truth(example)


def deliberate_one(example: dict, arm: str, seed: int) -> dict:
    candidates = [
        general_specialist(example, seed),
        specialist(example, rule_route(example["request"]), seed),
    ]
    candidates.append(critic_candidate(example, seed, candidates[-1]))
    correctness = [verify(example, candidate) for candidate in candidates]
    if arm == "no_deliberation":
        used, final, stop = 1, candidates[0], "no_deliberation_reference"
    elif arm == "fixed_three_step":
        used, final, stop = 3, candidates[2], "fixed_budget_exhausted"
    else:
        first = next((index for index, passed in enumerate(correctness, start=1) if passed), None)
        used = first or 3
        final = candidates[used - 1]
        stop = "independent_verifier_accept" if first else "budget_exhausted_without_verified_candidate"
    used_correctness = correctness[:used]
    first_hit = next((index for index, passed in enumerate(used_correctness, start=1) if passed), None)
    last_correct = next((index for index in range(len(used_correctness), 0, -1) if used_correctness[index - 1]), None)
    return {
        "example_id": example["example_id"],
        "family": example["family"],
        "seed": seed,
        "arm": arm,
        "candidates": candidates[:used],
        "candidate_correctness": used_correctness,
        "final_output": final,
        "final_correct": final == example["answer"],
        "candidate_operation_budget": 3,
        "candidate_operations_used": used,
        "first_hit_step": first_hit,
        "last_correct_step": last_correct,
        "stop_reason": stop,
        "branch_credit": sum(not used_correctness[index - 1] and used_correctness[index] for index in range(1, len(used_correctness))),
        "dissent_count": len(set(candidates[:used])) - 1,
        "answer_changes": sum(candidates[index] != candidates[index - 1] for index in range(1, used)),
        "extra_compute_harm": correctness[0] and final != example["answer"],
        "verifier_identity": "deterministic-task-recomputation-v0",
    }


def aggregate_routing(rows: list[dict]) -> list[dict]:
    groups = defaultdict(list)
    for row in rows:
        groups[(row["arm"], row["seed"])].append(row)
    output = []
    for (arm, seed), group in sorted(groups.items()):
        output.append({
            "arm": arm,
            "seed": seed,
            "examples": len(group),
            "correct": sum(row["correct"] for row in group),
            "accuracy": round(sum(row["correct"] for row in group) / len(group), 6),
            "coverage": round(sum(row["covered"] for row in group) / len(group), 6),
            "abstentions": sum(row["abstained"] for row in group),
            "fallbacks": sum(row["fallback_used"] for row in group),
            "candidate_operations": sum(row["candidate_operations_used"] for row in group),
        })
    return output


def aggregate_deliberation(rows: list[dict]) -> list[dict]:
    groups = defaultdict(list)
    for row in rows:
        groups[(row["arm"], row["seed"])].append(row)
    output = []
    for (arm, seed), group in sorted(groups.items()):
        output.append({
            "arm": arm,
            "seed": seed,
            "examples": len(group),
            "correct": sum(row["final_correct"] for row in group),
            "accuracy": round(sum(row["final_correct"] for row in group) / len(group), 6),
            "candidate_operations": sum(row["candidate_operations_used"] for row in group),
            "mean_steps": round(sum(row["candidate_operations_used"] for row in group) / len(group), 6),
            "first_hits": sum(row["first_hit_step"] is not None for row in group),
            "branch_credit": sum(row["branch_credit"] for row in group),
            "dissent": sum(row["dissent_count"] for row in group),
            "answer_changes": sum(row["answer_changes"] for row in group),
            "extra_compute_harm": sum(row["extra_compute_harm"] for row in group),
            "stop_reasons": dict(sorted(Counter(row["stop_reason"] for row in group).items())),
        })
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    if RESULT.exists() and not args.force:
        raise SystemExit(f"result already exists: {RESULT.relative_to(ROOT)}")
    corpus = json.loads(CORPUS.read_text(encoding="utf-8"))
    train = [row for row in corpus["examples"] if row["split"] == "train"]
    test = [row for row in corpus["examples"] if row["split"] == "test"]
    started = time.perf_counter()
    routing_rows, deliberation_rows, interference = [], [], []
    for seed in SEEDS:
        learned = fit_router(train, seed)
        for example in test:
            for arm in ROUTING_ARMS:
                routing_rows.append(route_one(example, arm, seed, learned))
            interference.append({
                "example_id": example["example_id"],
                "seed": seed,
                "correct_specialists": [family for family in FAMILIES if specialist(example, family, seed) == example["answer"]],
                "wrong_specialist_outputs": {family: specialist(example, family, seed) for family in FAMILIES if family != example["family"]},
            })
            for arm in DELIBERATION_ARMS:
                deliberation_rows.append(deliberate_one(example, arm, seed))
    result = {
        "schema_version": "asi_stack.post_v2_routing_deliberation_result.v0",
        "program_id": "matched_routing_and_deliberation",
        "recorded_date": "2026-07-10",
        "execution_state": "completed_exact_preregistered_test_runs",
        "corpus_ref": CORPUS.relative_to(ROOT).as_posix(),
        "corpus_sha256": corpus["corpus_sha256"],
        "environment": {"platform": platform.platform(), "python": platform.python_version(), "numpy": np.__version__, "scikit_learn": sklearn.__version__},
        "seeds": list(SEEDS),
        "routing": {"arms": list(ROUTING_ARMS), "records": routing_rows, "summary": aggregate_routing(routing_rows), "interference_counterfactuals": interference},
        "deliberation": {"arms": list(DELIBERATION_ARMS), "records": deliberation_rows, "summary": aggregate_deliberation(deliberation_rows)},
        "program_wall_seconds": round(time.perf_counter() - started, 6),
        "claim_dispositions": [
            {"claim_id": "routing-heads-and-specialist-cores.core", "disposition": "no_change", "basis": "The frozen synthetic held-out comparison measures route behavior but does not establish model-scale or production transfer."},
            {"claim_id": "governed-deliberation-and-test-time-scaling.core", "disposition": "no_change", "basis": "The deterministic candidate/verifier study measures benefit and harm under matched caps but does not establish language-model deliberation transfer."}
        ],
        "support_state_effect": "none",
        "non_claims": [
            "Oracle routing is a comparator and not a deployable result.",
            "The synthetic four-family workload does not establish production routing or language-model transfer.",
            "Task recomputation is a bounded verifier, not an open-world correctness oracle.",
            "No chapter-core support state changes from this result."
        ]
    }
    result["bundle_sha256"] = canonical_sha(result)
    RESULT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {RESULT.relative_to(ROOT)} bundle_sha256={result['bundle_sha256']}")


if __name__ == "__main__":
    main()
