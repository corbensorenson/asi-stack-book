"""QI-08: explicit adversarial addressing controls."""

from __future__ import annotations

from .canonical import ContractError, make_envelope


CASES = (
    "alias_escalation", "collision", "poisoning", "stale_epoch", "branch_overload",
    "route_disagreement", "certificate_tampering", "privacy_leakage", "missing_residual",
)


def suite(results: dict[str, bool]) -> dict:
    if set(results) != set(CASES):
        raise ContractError("adversarial suite case set incomplete")
    return {**results, "disposition": "all_rejected" if all(results.values()) else "residual_failures"}


def artifact(result: dict, input_digests: list[str]) -> dict:
    return make_envelope(
        "QI-08", "adversarial:bounded-suite", ["runtime-adapters-tool-permissions-and-human-approval"], result,
        input_digests=input_digests,
        non_claim_boundary="Synthetic adversarial controls only; blocked fixtures are not a safety, security, privacy, or deployment result.",
    )
