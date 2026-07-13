"""QI-05: deterministic expected-decision-value question compiler."""

from __future__ import annotations

from .canonical import ContractError, make_envelope


ACTIONS = {"internal_discriminator", "retrieval", "sensor_fixture", "tool_fixture", "specialist_request", "clarification", "stop"}
COSTS = ("compute_cost", "latency_cost", "privacy_cost", "burden_cost", "risk_cost")


def compile_question(posterior_before: dict[str, float], candidates: list[dict], *, question_count: int, max_questions: int = 3) -> dict:
    if question_count >= max_questions:
        selected = {"action": "stop", "expected_decision_value": 0.0, **{key: 0.0 for key in COSTS}}
        stop_reason = "question_budget_exhausted"
    else:
        scored = []
        for candidate in candidates:
            if candidate.get("action") not in ACTIONS - {"stop"}:
                raise ContractError("unknown question action")
            if any(float(candidate.get(key, -1)) < 0 for key in COSTS):
                raise ContractError("question cost must be nonnegative")
            net = float(candidate["expected_decision_value"]) - sum(float(candidate[key]) for key in COSTS)
            scored.append((net, candidate["action"], candidate))
        selected = max(scored, default=(0.0, "stop", {"action": "stop", "expected_decision_value": 0.0, **{key: 0.0 for key in COSTS}}))[2]
        stop_reason = "positive_net_value" if selected["action"] != "stop" else "no_positive_action"
    posterior_after = dict(posterior_before)
    payload = {
        "posterior_before": posterior_before,
        "candidate_actions": candidates,
        "expected_decision_value": selected["expected_decision_value"],
        **{key: selected[key] for key in COSTS},
        "selected_action": selected["action"],
        "posterior_after": posterior_after,
        "stop_reason": stop_reason,
    }
    return payload


def artifact(trace: dict, input_digests: list[str]) -> dict:
    return make_envelope(
        "QI-05", f"question:{input_digests[0] if input_digests else 'root'}",
        ["cognitive-compilation-and-semantic-ir", "routing-heads-and-specialist-cores"], trace,
        input_digests=input_digests,
        non_claim_boundary="Deterministic value-minus-cost selection on declared candidates only; no learned policy or optimality claim.",
    )
