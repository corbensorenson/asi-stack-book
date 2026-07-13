"""QI-06: semantic-to-physical route lowering and effect receipts."""

from __future__ import annotations

from .canonical import ContractError, make_envelope, sha256, verify_envelope
from .certificate import verify_certificate


def decide_authority(request: dict, policy: dict) -> dict:
    required = {"actor", "target", "scope", "effect", "reversible", "approval_id", "expires_at"}
    if set(request) != required:
        raise ContractError("authority request shape invalid")
    reasons = []
    if request["actor"] not in policy["actors"]:
        reasons.append("actor_not_allowed")
    if request["target"] not in policy["targets"]:
        reasons.append("target_not_allowed")
    if request["effect"] not in policy["effects"]:
        reasons.append("effect_not_allowed")
    if not set(request["scope"]).issubset(set(policy["scope"])):
        reasons.append("scope_widening")
    if not request["reversible"]:
        reasons.append("irreversible_effect_refused")
    if not request["approval_id"]:
        reasons.append("approval_missing")
    return {"allowed": not reasons, "reasons": reasons, "policy_id": policy["policy_id"]}


def compile_route(certificate: dict, *, authoritative_epoch: str, requested_use: str, request: dict, policy: dict) -> dict:
    verify_envelope(certificate)
    verify_certificate(certificate, authoritative_epoch=authoritative_epoch, requested_use=requested_use)
    decision = decide_authority(request, policy)
    steps = [
        {"kind": "model", "purpose": "materialize bounded response"},
        {"kind": "verification", "purpose": "check structural commitments"},
    ]
    if decision["allowed"]:
        steps.insert(1, {"kind": "tool_fixture", "purpose": request["effect"]})
    else:
        steps.insert(1, {"kind": "fallback", "purpose": "authority_refusal"})
    attempted = [{"effect": request["effect"], "attempted": True, "released": decision["allowed"]}]
    receipts = [{
        "receipt_id": sha256({"request": request, "decision": decision})[:24],
        "effect": request["effect"],
        "released": decision["allowed"],
        "reversible": request["reversible"],
        "decision_reasons": decision["reasons"],
    }]
    return {
        "certificate_digest": certificate["content_digest"],
        "steps": steps,
        "authority_request": request,
        "authority_decision": decision,
        "attempted_effects": attempted,
        "receipts": receipts,
        "verification": {"required": True, "status": "pending"},
        "fallback": {"used": not decision["allowed"], "reason": decision["reasons"]},
    }


def artifact(route: dict, input_digests: list[str]) -> dict:
    if len(route["receipts"]) != len(route["attempted_effects"]):
        raise ContractError("every attempted effect requires a receipt")
    return make_envelope(
        "QI-06", f"route:{route['certificate_digest']}",
        ["routing-heads-and-specialist-cores", "runtime-adapters-tool-permissions-and-human-approval"], route,
        input_digests=input_digests,
        non_claim_boundary="Local deterministic adapter route only; semantic resolution does not grant authority or production effects.",
    )
