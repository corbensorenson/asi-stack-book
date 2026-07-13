"""QI-04: Semantic Address Certificate with fixture-level signing."""

from __future__ import annotations

from .canonical import ContractError, make_envelope, sha256


REQUIRED = {
    "soid", "occurrence_or_expression", "context", "task", "consumer", "epoch", "paths", "confidence",
    "provenance", "grounding", "residuals", "allowed_uses", "prohibited_uses", "authority_ceiling",
    "validity", "migration",
}


def issue_certificate(fields: dict, input_digests: list[str]) -> dict:
    missing = REQUIRED - set(fields)
    if missing:
        raise ContractError(f"certificate missing fields: {sorted(missing)}")
    if not 0.0 <= fields["confidence"] <= 1.0:
        raise ContractError("certificate confidence outside [0,1]")
    if not fields["residuals"]:
        raise ContractError("certificate must preserve residuals")
    if set(fields["allowed_uses"]) & set(fields["prohibited_uses"]):
        raise ContractError("certificate use policy conflicts")
    signature_body = {key: fields[key] for key in sorted(fields)}
    payload = dict(fields)
    payload["signature_fixture"] = {
        "algorithm": "sha256-fixture-not-cryptographic-identity",
        "value": sha256({"fixture_key": "qcsa-local-test-only", "body": signature_body}),
        "verified": True,
    }
    return make_envelope(
        "QI-04", f"certificate:{fields['soid']}:{fields['epoch']}:{fields['task']}",
        ["virtual-context-abi", "inter-stack-protocols-identity-and-economic-exchange"], payload,
        input_digests=input_digests,
        non_claim_boundary="Local integrity-shaped certificate only; signature fixture grants no trust, truth, or execution authority.",
    )


def verify_certificate(certificate: dict, *, authoritative_epoch: str, requested_use: str) -> None:
    payload = certificate["payload"]
    if payload["epoch"] != authoritative_epoch:
        raise ContractError("stale certificate epoch")
    if requested_use not in payload["allowed_uses"] or requested_use in payload["prohibited_uses"]:
        raise ContractError("certificate use not permitted")
    signature = payload["signature_fixture"]
    body = {key: payload[key] for key in payload if key != "signature_fixture"}
    expected = sha256({"fixture_key": "qcsa-local-test-only", "body": {key: body[key] for key in sorted(body)}})
    if signature.get("value") != expected:
        raise ContractError("certificate signature fixture mismatch")
