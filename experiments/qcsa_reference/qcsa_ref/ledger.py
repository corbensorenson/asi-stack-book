"""QI-11: resource and governance accounting."""

from __future__ import annotations

from .canonical import ContractError, make_envelope


FIELDS = ("latency_ns", "bytes", "tokens", "questions", "retrievals", "model_calls", "tool_calls", "verifier_cost", "fallbacks", "abstentions", "repairs", "migrations", "human_burden")


def record(values: dict[str, int]) -> dict:
    if set(values) != set(FIELDS) or any(not isinstance(value, int) or value < 0 for value in values.values()):
        raise ContractError("resource ledger requires exact nonnegative integer fields")
    return {key: values[key] for key in FIELDS}


def artifact(result: dict, input_digests: list[str]) -> dict:
    return make_envelope(
        "QI-11", "ledger:bounded-reference-run", ["routing-heads-and-specialist-cores"], result,
        input_digests=input_digests,
        non_claim_boundary="Local operation counters and latency fixture only; no production cost, efficiency, or human-burden result.",
    )
