"""QI-10: structural semantic round-trip comparison."""

from __future__ import annotations

from .canonical import ContractError, make_envelope, sha256


DIMENSIONS = ("identity", "roles", "negation", "modality", "quantity", "time", "claim_citation_bindings", "authority", "residuals")


def compare(source: dict, candidate: dict, independent: dict) -> dict:
    if any(key not in source or key not in candidate or key not in independent for key in DIMENSIONS):
        raise ContractError("round-trip structure missing dimension")
    candidate_checks = {key: source[key] == candidate[key] for key in DIMENSIONS}
    independent_checks = {key: source[key] == independent[key] for key in DIMENSIONS}
    disagreement = [key for key in DIMENSIONS if candidate_checks[key] != independent_checks[key]]
    return {
        "candidate_digest": sha256(candidate),
        "evaluator_implementation": "scripts/qcsa_independent_evaluator.py",
        **candidate_checks,
        "evaluator_disagreement": disagreement,
    }


def artifact(result: dict, input_digests: list[str]) -> dict:
    return make_envelope(
        "QI-10", f"roundtrip:{result['candidate_digest']}",
        ["compact-generative-systems-and-residual-honesty", "claim-ledgers-and-belief-revision"], result,
        input_digests=input_digests,
        non_claim_boundary="Finite structural field comparison only; no general semantic equivalence, factuality, or evaluator independence claim.",
    )
