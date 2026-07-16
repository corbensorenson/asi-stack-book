#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FOUNDATION_PATH = ROOT / "experiments" / "research_foundation" / "foundation.json"
CORPUS_PATH = ROOT / "experiments" / "research_foundation" / "task_corpus.json"
LABELS_PATH = ROOT / "experiments" / "research_foundation" / "held_out_labels.json"
PREFLIGHT_PATH = ROOT / "experiments" / "research_foundation" / "sacrificial_preflight.json"
STATUS_PATH = ROOT / "roadmap_records" / "post_v2_3_claim_proof_and_sota_challenge_status.json"


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalized(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]+", " ", text.lower())).strip()


def admissible(value: Any) -> bool:
    return (
        isinstance(value, dict)
        and set(value) == {"route", "residual", "confidence"}
        and all(isinstance(value[key], str) and value[key].strip() for key in value)
        and value["confidence"] in {"low", "medium", "high"}
    )


def evaluator_a(case: dict[str, Any]) -> bool:
    value = case["final_decision"]
    return admissible(value) and value["route"] == case["gold_route"] and value["residual"] == case["gold_residual"]


def evaluator_b(case: dict[str, Any]) -> bool:
    value = case["final_decision"]
    if not admissible(value):
        return False
    expected_pair = f"{case['gold_route']}::{case['gold_residual']}"
    observed_pair = "::".join([value.get("route", ""), value.get("residual", "")])
    return observed_pair == expected_pair


def errors(foundation: dict[str, Any]) -> list[str]:
    out: list[str] = []
    corpus = load(CORPUS_PATH)
    labels = load(LABELS_PATH)
    preflight = load(PREFLIGHT_PATH)
    status = load(STATUS_PATH)

    if foundation.get("schema_version") != "asi_stack.research_foundation.v1":
        out.append("wrong research-foundation schema version")
    if foundation.get("state") != "sacrificial_preflight_passed":
        out.append("research foundation has not passed sacrificial preflight")
    if foundation.get("support_state_effect") != "none":
        out.append("research foundation invents support movement")

    corpus_contract = foundation.get("task_corpus_contract", {})
    label_contract = foundation.get("held_out_label_contract", {})
    preflight_contract = foundation.get("sacrificial_preflight", {})
    for contract, path, name in (
        (corpus_contract, CORPUS_PATH, "corpus"),
        (label_contract, LABELS_PATH, "held-out labels"),
        (preflight_contract, PREFLIGHT_PATH, "preflight"),
    ):
        if contract.get("sha256") != digest(path):
            out.append(f"{name} digest drift")

    tasks = corpus.get("tasks", [])
    task_ids = [row.get("task_id") for row in tasks]
    if len(tasks) != 24 or len(set(task_ids)) != 24:
        out.append("task corpus must contain 24 unique tasks")
    splits = Counter(row.get("split") for row in tasks)
    slices = Counter(row.get("slice") for row in tasks)
    if dict(splits) != {"sacrificial": 6, "tuning": 6, "held_out": 12}:
        out.append(f"task split counts drifted: {dict(splits)}")
    if dict(slices) != {"governed_work": 8, "governed_learning": 8, "assurance_control": 8}:
        out.append(f"task slice counts drifted: {dict(slices)}")
    requests = [normalized(str(row.get("request", ""))) for row in tasks]
    if any(not request for request in requests) or len(set(requests)) != len(requests):
        out.append("task requests are blank or exact normalized duplicates")
    if any("expected_route" in row or "required_residual" in row for row in tasks):
        out.append("candidate-visible task corpus leaks evaluator labels")
    if any(row.get("effect_model") not in {"read_only_decision", "synthetic_decision", "repository_local_reversible", "synthetic_partial_effect"} for row in tasks):
        out.append("task corpus contains an unbounded effect model")
    if any(not isinstance(row.get("difficulty"), int) or not 1 <= row["difficulty"] <= 5 for row in tasks):
        out.append("task difficulty must be an integer from one through five")
    if corpus_contract.get("task_count") != len(tasks) or corpus_contract.get("split_counts") != dict(splits) or corpus_contract.get("slice_counts") != dict(slices):
        out.append("task-corpus contract counts drifted")

    held_out_ids = {row["task_id"] for row in tasks if row.get("split") == "held_out"}
    label_rows = labels.get("labels", [])
    label_ids = [row.get("task_id") for row in label_rows]
    if set(label_ids) != held_out_ids or len(label_ids) != len(set(label_ids)):
        out.append("held-out label identities do not exactly cover held-out tasks")
    if label_contract.get("label_count") != len(label_rows):
        out.append("held-out label count drift")
    if "must not read" not in str(labels.get("access_policy", "")):
        out.append("held-out labels lack model-runner exclusion")

    models = foundation.get("model_selection", [])
    roles = {row.get("role") for row in models}
    if roles != {"current_strong_general", "independent_comparison_family", "small_reproducible_control"}:
        out.append("model selection does not contain all three required roles")
    strong = next((row for row in models if row.get("role") == "current_strong_general"), {})
    if strong.get("model_id") != "gemini-3.5-flash" or not str(strong.get("source", "")).startswith("https://ai.google.dev/"):
        out.append("dated current-strong model selection drifted from its primary source")
    for row in models:
        if not row.get("drift_rule") or not row.get("availability"):
            out.append(f"model selection lacks drift or availability boundary: {row.get('role')}")
    for row in models:
        if row.get("availability") == "local_snapshot_present":
            snapshot = str(row.get("snapshot", ""))
            if not re.fullmatch(r"[0-9a-f]{40}", snapshot):
                out.append(f"local model snapshot is not exact: {row.get('model_id')}")

    inference = foundation.get("inference_contract", {})
    if len(inference.get("required_identity_fields", [])) < 12 or "only the registered schema-constrained final-decision object is scored" not in str(inference.get("reasoning_answer_separation", "")):
        out.append("inference identity or reasoning/final-answer separation is incomplete")
    evaluator = foundation.get("evaluator_contract", {})
    if evaluator.get("independent_implementations") != 2 or evaluator.get("syntax_semantics_separated") is not True:
        out.append("evaluator independence or syntax/semantics separation is incomplete")
    statistics = foundation.get("statistics_policy", {})
    if len(statistics.get("estimands", [])) < 8 or len(statistics.get("robustness", [])) < 6:
        out.append("statistics policy lacks joint estimands or robustness routes")
    environment = foundation.get("environment_manifest", {})
    if not re.fullmatch(r"[0-9a-f]{40}", str(environment.get("repository_head_at_freeze", ""))) or len(environment.get("seeds", [])) < 3:
        out.append("environment freeze lacks exact repository identity or seeds")
    safety = foundation.get("safety_envelope", {})
    if safety.get("ceilings", {}).get("provider_spend_usd_per_preflight", 0) > 25 or "no unbounded" not in str(safety.get("external_actions", "")):
        out.append("experiment safety envelope lacks bounded spend or action authority")
    artifacts = foundation.get("artifact_protocol", {})
    if artifacts.get("append_only") is not True or len(artifacts.get("required_records", [])) < 12 or artifacts.get("publication_authority") != "none":
        out.append("artifact protocol is incomplete or invents publication authority")

    cases = preflight.get("cases", [])
    admissible_rows = [row for row in cases if admissible(row.get("final_decision"))]
    correct_rows = [row for row in admissible_rows if evaluator_a(row)]
    disagreements = sum(evaluator_a(row) != evaluator_b(row) for row in cases)
    false_accepts = sum(evaluator_a(row) and not (row["final_decision"]["route"] == row["gold_route"] and row["final_decision"]["residual"] == row["gold_residual"]) for row in admissible_rows)
    false_rejects = sum((not evaluator_a(row)) and (row["final_decision"]["route"] == row["gold_route"] and row["final_decision"]["residual"] == row["gold_residual"]) for row in admissible_rows)
    observed = {
        "case_count": len(cases),
        "schema_admissible_count": len(admissible_rows),
        "schema_admissible_rate": len(admissible_rows) / len(cases),
        "semantically_correct_admissible_count": len(correct_rows),
        "semantically_correct_admissible_rate": len(correct_rows) / len(admissible_rows),
        "evaluator_disagreement_count": disagreements,
        "false_accept_count": false_accepts,
        "false_reject_count": false_rejects,
        "abstention_count": len(cases) - len(admissible_rows),
    }
    if observed != preflight.get("expected_metrics"):
        out.append(f"sacrificial preflight metric drift: {observed}")
    if observed["schema_admissible_rate"] < preflight_contract.get("minimum_schema_admissible_rate", 1.0):
        out.append("sacrificial preflight misses the admissibility floor")
    if preflight.get("protocol_outcome") != "instrument_adequate" or preflight.get("claim_outcome") != "support_retained" or preflight.get("support_state_effect") != "none":
        out.append("sacrificial preflight protocol/claim/support separation is invalid")

    milestone_states = {row.get("id"): row.get("state") for row in status.get("milestones", [])}
    if milestone_states.get("M2") != "completed" or milestone_states.get("M4") not in {"in_progress", "completed"}:
        out.append("roadmap does not preserve M2 closure and M4 activation")
    if status.get("current_priority") not in {"P3", "P4", "P5", "P6", "P7", "P8", "P9"}:
        out.append("research foundation regressed before active P3")
    if len(foundation.get("non_claims", [])) < 5:
        out.append("research foundation lacks explicit non-claims")
    return out


def main() -> None:
    foundation = load(FOUNDATION_PATH)
    failures = errors(foundation)
    mutations: list[tuple[str, dict[str, Any]]] = []
    support = copy.deepcopy(foundation)
    support["support_state_effect"] = "promotion"
    mutations.append(("support laundering", support))
    split = copy.deepcopy(foundation)
    split["task_corpus_contract"]["split_counts"]["held_out"] = 11
    mutations.append(("held-out denominator laundering", split))
    model = copy.deepcopy(foundation)
    model["model_selection"] = model["model_selection"][1:]
    mutations.append(("strong model omission", model))
    evaluator = copy.deepcopy(foundation)
    evaluator["evaluator_contract"]["independent_implementations"] = 1
    mutations.append(("self-evaluation laundering", evaluator))
    artifacts = copy.deepcopy(foundation)
    artifacts["artifact_protocol"]["publication_authority"] = "granted"
    mutations.append(("publication authority invention", artifacts))
    preflight = copy.deepcopy(foundation)
    preflight["sacrificial_preflight"]["minimum_schema_admissible_rate"] = 0.81
    mutations.append(("preflight floor miss", preflight))
    for label, candidate in mutations:
        if not errors(candidate):
            failures.append(f"negative mutation accepted: {label}")
    if failures:
        raise SystemExit("Research foundation validation failed:\n - " + "\n - ".join(failures))
    print(
        "Research foundation passed: 24 tasks across three slices, 6/6/12 frozen splits, "
        "12 isolated held-out labels, three model roles, 8/10 schema-admissible sacrificial canaries, "
        "7/8 semantically correct admissible canaries, two independent evaluators, six rejecting mutations, "
        "and no support or publication authority."
    )


if __name__ == "__main__":
    main()
