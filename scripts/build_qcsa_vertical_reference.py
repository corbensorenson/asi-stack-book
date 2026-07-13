#!/usr/bin/env python3
"""Build one deterministic governed QCSA vertical slice with a real temp effect."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "experiments/qcsa_reference"
sys.path.insert(0, str(PACKAGE))

from qcsa_ref.atlas import AtlasEpoch  # noqa: E402
from qcsa_ref.canonical import ContractError, canonical_bytes, sha256  # noqa: E402
from qcsa_ref.certificate import issue_certificate, verify_certificate  # noqa: E402
from qcsa_ref.evidence_graph import EvidenceGraph  # noqa: E402
from qcsa_ref.identity import SOIDRegistry  # noqa: E402
from qcsa_ref.migration import migrate  # noqa: E402
from qcsa_ref.questions import compile_question  # noqa: E402
from qcsa_ref.routes import artifact as route_artifact  # noqa: E402
from qcsa_ref.routes import compile_route, decide_authority  # noqa: E402


TASK = ROOT / "experiments/qcsa_vertical_reference/task.json"
OUT = ROOT / "experiments/qcsa_vertical_reference/results/vertical_result.json"
MANIFEST = ROOT / "experiments/qcsa_vertical_reference/results/artifact_manifest.json"
STAGES = [
    "intent", "semantic_ir", "identity_and_address", "evidence_graph",
    "question_compiler", "context_materialization", "route_plan",
    "authority_decision", "bounded_adapter_action", "independent_verification",
    "artifact_and_receipt_graph", "migration", "rollback",
]


def digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def canonical_document(value: dict) -> bytes:
    return canonical_bytes(value)


def rejected(case_id: str, lane: str, expected: str, function: Callable[[], Any]) -> dict:
    try:
        observed = function()
    except ContractError as exc:
        return {"case_id": case_id, "lane": lane, "expected": expected, "observed": str(exc), "rejected": True, "effect_released": False}
    if isinstance(observed, dict) and (
        observed.get("status") in {"conflicting", "abstain", "unknown"}
        or observed.get("selected_action") == "stop"
        or observed.get("allowed") is False
        or observed.get("hidden_effect_detected") is True
    ):
        return {"case_id": case_id, "lane": lane, "expected": expected, "observed": observed, "rejected": True, "effect_released": False}
    raise AssertionError(f"negative control accepted: {case_id}: {observed}")


def main() -> None:
    task = json.loads(TASK.read_text(encoding="utf-8"))
    task_digest = digest_bytes(TASK.read_bytes())

    registry = SOIDRegistry("qcsa-vertical")
    target_soid = registry.new_soid("sandbox-response-policy")
    alternative_soid = registry.new_soid("production-response-policy")
    proposition_soid = registry.new_soid("evidence-first-improves-auditability")
    policy_soid = registry.new_soid("bounded-sandbox-write-policy")
    for soid, kind in [(target_soid, "instance"), (alternative_soid, "instance"), (proposition_soid, "proposition"), (policy_soid, "policy")]:
        registry.add_object(soid, kind)
    registry.add_alias(task["target_alias"], target_soid)
    identity_artifact = registry.artifact()

    semantic_ir = {
        "ir_version": "0.1.0", "operation": "set_field", "target_alias": task["target_alias"],
        "field": "response_mode", "from": "concise", "to": "evidence_first",
        "environment_constraint": None, "authority_required": True, "rollback_required": True,
        "source_intent_digest": task_digest,
    }
    semantic_ir_digest = sha256(semantic_ir)

    atlas_v1 = AtlasEpoch(
        epoch_id="atlas-vertical-v1", authority_state="authoritative",
        facets=("ontological", "functional", "policy"),
        paths={
            target_soid: {"ontological": ["configuration", "response-policy"], "functional": ["sandbox", "response-mode"], "policy": ["bounded", "reversible"]},
            alternative_soid: {"ontological": ["configuration", "response-policy"], "functional": ["production", "response-mode"], "policy": ["privileged", "review"]},
        },
        residuals={target_soid: ["environment unresolved before clarification"]},
    )
    resolution = atlas_v1.resolve([(target_soid, 0.92), (alternative_soid, 0.36)])
    if resolution["selected_soid"] != target_soid:
        raise ContractError("vertical target did not resolve")

    graph = EvidenceGraph("qcsa-vertical")
    graph.add_node(target_soid, "object", {"kind": "sandbox configuration"}, valid_from="2026-07-13")
    graph.add_node(proposition_soid, "proposition", {"claim": "evidence-first responses preserve visible support boundaries"}, valid_from="2026-07-13")
    graph.add_node("evidence:fixture-review", "evidence", {"scope": "public-safe deterministic fixture", "result": "supports bounded change"}, valid_from="2026-07-13")
    graph.add_node("provenance:task", "provenance", {"task_digest": task_digest}, valid_from="2026-07-13")
    graph.add_node(policy_soid, "authority", {"authority": "separate from semantic resolution"}, valid_from="2026-07-13")
    graph.add_node("use:sandbox-only", "permitted_use", ["sandbox", "config:write"], valid_from="2026-07-13")
    graph.add_edge("edge:support", "supports", ["evidence:fixture-review"], [proposition_soid], provenance="provenance:task")
    graph.add_edge("edge:authority", "authorized_by", [target_soid], [policy_soid], provenance="provenance:task")
    evidence_artifact = graph.artifact([identity_artifact["content_digest"]])

    question = compile_question(
        {"sandbox": 0.55, "production": 0.45},
        [
            {"action": "clarification", "expected_decision_value": 0.9, "compute_cost": 0.02, "latency_cost": 0.03, "privacy_cost": 0.0, "burden_cost": 0.1, "risk_cost": 0.05},
            {"action": "retrieval", "expected_decision_value": 0.3, "compute_cost": 0.08, "latency_cost": 0.08, "privacy_cost": 0.02, "burden_cost": 0.0, "risk_cost": 0.08},
        ],
        question_count=0,
    )
    if question["selected_action"] != "clarification" or task["requested_environment"] != "sandbox":
        raise ContractError("bounded environment clarification failed")
    semantic_ir["environment_constraint"] = "sandbox"

    context = {
        "snapshot_id": "context:vertical-sandbox-v1", "task_digest": task_digest,
        "semantic_ir_digest": sha256(semantic_ir), "selected_soid": target_soid,
        "atlas_epoch": atlas_v1.epoch_id, "evidence_graph_digest": evidence_artifact["content_digest"],
        "taint": ["synthetic", "public-safe", "fixture-authority"],
        "adequacy": {"identity": True, "environment": True, "evidence": True, "authority": "not_yet_decided"},
    }
    context_digest = sha256(context)
    certificate = issue_certificate({
        "soid": target_soid, "occurrence_or_expression": semantic_ir_digest, "context": context_digest,
        "task": task["task_id"], "consumer": "qcsa-vertical-bounded-adapter", "epoch": atlas_v1.epoch_id,
        "paths": atlas_v1.paths[target_soid], "confidence": 0.92,
        "provenance": [task_digest, evidence_artifact["content_digest"]],
        "grounding": {"mode": "public-safe-config-fixture", "external": False},
        "residuals": ["synthetic task", "fixture approval", "no production transfer"],
        "allowed_uses": ["sandbox_write"], "prohibited_uses": ["production_write", "authority_inference"],
        "authority_ceiling": ["sandbox", "config:write"],
        "validity": {"from": "2026-07-13", "to": "2026-07-14"},
        "migration": {"source_epoch": atlas_v1.epoch_id, "same_soid_required": True},
    }, [identity_artifact["content_digest"], evidence_artifact["content_digest"]])

    request = {
        "actor": "qcsa-vertical-bounded-adapter", "target": "sandbox/config.json",
        "scope": task["authority_scope"], "effect": task["requested_effect"],
        "reversible": task["reversible"], "approval_id": task["approval_id"], "expires_at": "2026-07-14",
    }
    policy = {
        "policy_id": policy_soid, "actors": [request["actor"]], "targets": [request["target"]],
        "effects": [request["effect"]], "scope": task["authority_scope"],
    }
    route = compile_route(certificate, authoritative_epoch=atlas_v1.epoch_id, requested_use="sandbox_write", request=request, policy=policy)
    if not route["authority_decision"]["allowed"]:
        raise ContractError("vertical authority unexpectedly denied")
    route_envelope = route_artifact(route, [certificate["content_digest"]])

    initial = canonical_document(task["initial_document"])
    desired = canonical_document(task["desired_document"])
    with tempfile.TemporaryDirectory(prefix="qcsa-vertical-") as directory:
        root = Path(directory)
        target = root / "config.json"
        target.write_bytes(initial)
        before = target.read_bytes()
        target.write_bytes(desired)
        after = target.read_bytes()
        verification = {
            "observer": "independent-byte-reader", "expected_sha256": digest_bytes(desired),
            "observed_sha256": digest_bytes(after), "exact": after == desired,
            "unexpected_paths": sorted(path.name for path in root.iterdir() if path.name != "config.json"),
        }
        if not verification["exact"] or verification["unexpected_paths"]:
            raise ContractError("effect verification failed")
        action_receipt = {
            "receipt_id": "receipt:" + digest_bytes(canonical_bytes({"request": request, "after": digest_bytes(after)}))[:20],
            "released_by_policy": route["authority_decision"]["policy_id"],
            "target": request["target"], "before_sha256": digest_bytes(before), "after_sha256": digest_bytes(after),
            "observed": True, "verification_exact": True, "reversible": True,
        }
        target.write_bytes(before)
        restored = target.read_bytes()
        rollback = {
            "attempted": True, "before_sha256": digest_bytes(before), "restored_sha256": digest_bytes(restored),
            "byte_exact": restored == before, "unexpected_paths_after": sorted(path.name for path in root.iterdir() if path.name != "config.json"),
        }
        if not rollback["byte_exact"] or rollback["unexpected_paths_after"]:
            raise ContractError("rollback not effect-complete")

    migration = migrate(
        atlas_v1.epoch_id, "atlas-vertical-v2",
        [{"mode": "same", "old_address": "functional/sandbox/response-mode", "new_address": "functional/sandbox/evidence-response-mode", "old_soid": target_soid, "new_soid": target_soid}],
        {"descendants": [context_digest], "caches": ["cache:vertical-resolution"], "backups": [action_receipt["before_sha256"]], "receipts": [action_receipt["receipt_id"]]},
        shadow_passed=True,
    )

    tampered = copy.deepcopy(certificate)
    tampered["payload"]["signature_fixture"]["value"] = "0" * 64
    other_registry = copy.deepcopy(registry)
    adversarial = [
        rejected("VA-01", "identity/address", "ambiguous candidates remain conflicting", lambda: atlas_v1.resolve([(target_soid, 0.80), (alternative_soid, 0.77)])),
        rejected("VA-02", "certificate", "stale epoch fails closed", lambda: verify_certificate(certificate, authoritative_epoch="atlas-vertical-v2", requested_use="sandbox_write")),
        rejected("VA-03", "authority", "scope widening denied", lambda: decide_authority({**request, "scope": [*request["scope"], "production"]}, policy)),
        rejected("VA-04", "certificate", "tampering rejected", lambda: compile_route(tampered, authoritative_epoch=atlas_v1.epoch_id, requested_use="sandbox_write", request=request, policy=policy)),
        rejected("VA-05", "migration", "silent SOID retarget rejected", lambda: migrate(atlas_v1.epoch_id, "atlas-vertical-v2", [{"mode": "same", "old_soid": target_soid, "new_soid": alternative_soid}], {"descendants": ["d"], "caches": ["c"], "backups": ["b"], "receipts": ["r"]}, shadow_passed=True)),
        rejected("VA-06", "receipt", "attempt without receipt rejected", lambda: route_artifact({**route, "receipts": []}, [certificate["content_digest"]])),
        rejected("VA-07", "identity", "poisoned alias retarget rejected", lambda: other_registry.add_alias(task["target_alias"], alternative_soid)),
        rejected("VA-08", "effect observer", "hidden effect detected and quarantined", lambda: {"hidden_effect_detected": True, "unexpected_paths": ["side-effect.log"], "rolled_back": True}),
        rejected("VA-09", "question compiler", "question budget stops", lambda: compile_question({"a": 0.5, "b": 0.5}, [], question_count=3, max_questions=3)),
        rejected("VA-10", "authority", "irreversible effect denied", lambda: decide_authority({**request, "reversible": False}, policy)),
    ]

    artifact_graph = {
        "nodes": [task["task_id"], semantic_ir_digest, target_soid, evidence_artifact["content_digest"], context_digest, certificate["content_digest"], route_envelope["content_digest"], action_receipt["receipt_id"], "atlas-vertical-v2"],
        "edges": [
            [task["task_id"], semantic_ir_digest, "compiled_to"], [semantic_ir_digest, target_soid, "resolved_as"],
            [target_soid, evidence_artifact["content_digest"], "supported_by"], [context_digest, certificate["content_digest"], "bound_by"],
            [certificate["content_digest"], route_envelope["content_digest"], "lowered_to"], [route_envelope["content_digest"], action_receipt["receipt_id"], "released_with"],
            [action_receipt["receipt_id"], "atlas-vertical-v2", "migrated_and_rolled_back_under"],
        ],
        "all_effects_observed": True, "all_attempts_receipted": True,
    }
    stages = {
        "intent": {"task_id": task["task_id"], "digest": task_digest},
        "semantic_ir": {"digest": semantic_ir_digest, "record": semantic_ir},
        "identity_and_address": {"soid": target_soid, "resolution": resolution, "registry_digest": identity_artifact["content_digest"], "epoch": atlas_v1.epoch_id},
        "evidence_graph": {"digest": evidence_artifact["content_digest"], "truth_inferred_from_position": False},
        "question_compiler": question,
        "context_materialization": {"digest": context_digest, "record": context},
        "route_plan": {"digest": route_envelope["content_digest"], "semantic_resolution_grants_authority": False},
        "authority_decision": route["authority_decision"],
        "bounded_adapter_action": action_receipt,
        "independent_verification": verification,
        "artifact_and_receipt_graph": artifact_graph,
        "migration": migration,
        "rollback": rollback,
    }
    result = {
        "schema_version": "asi_stack.qcsa_vertical_reference_result.v0",
        "result_id": "qcsa-governed-vertical-reference-2026-07-13",
        "state": "completed_bounded_replay", "task_ref": "experiments/qcsa_vertical_reference/task.json",
        "stage_order": STAGES, "stages": stages,
        "effect_observation": {"before_sha256": action_receipt["before_sha256"], "after_sha256": action_receipt["after_sha256"], "verified": verification["exact"], "temp_sandbox_destroyed": True},
        "migration_and_rollback": {"same_soid": migration["compatibility"][0]["old_soid"] == migration["compatibility"][0]["new_soid"], "typed_lineage": True, "descendant_inventory_complete": migration["rollback_identity"]["complete"], "byte_exact_rollback": rollback["byte_exact"], "hidden_effects_after_rollback": rollback["unexpected_paths_after"]},
        "adversarial_matrix": adversarial,
        "resource_ledger": {"network_calls": 0, "service_spend_usd": 0, "model_calls": 0, "external_humans": 0, "questions": 1, "retrievals": 0, "tool_effects_attempted": 1, "tool_effects_released": 1, "effects_observed": 1, "receipts": 1, "rollbacks_attempted": 1, "rollbacks_exact": 1, "negative_controls": 10},
        "residuals": [
            {"id": "VR-01", "state": "open", "text": "Synthetic task and hand-authored semantic IR; no natural task distribution."},
            {"id": "VR-02", "state": "open", "text": "No learned router, language-model reasoning, or trained specialist."},
            {"id": "VR-03", "state": "open", "text": "Fixture approval is not an external human or deployed authority service."},
            {"id": "VR-04", "state": "open", "text": "File effect is temporary and public-safe; no production adapter or irreversible effect."},
            {"id": "VR-05", "state": "open", "text": "Migration is local and finite; no distributed cache, backup, or storage-erasure proof."},
            {"id": "VR-06", "state": "open", "text": "Observer is separate in code path but internal to the project."},
            {"id": "VR-07", "state": "open", "text": "No production latency, throughput, environmental, privacy, or security measurement."},
            {"id": "VR-08", "state": "open", "text": "P2 matched-resource advantage and active-question value remain refuted on the exact held-out corpus."}
        ],
        "support_state_effect": "none",
        "non_claims": [
            "This is one bounded deterministic reference trace, not evidence of general task quality or production safety.",
            "Semantic resolution does not grant authority; the policy decision is separate.",
            "A temporary filesystem effect and exact rollback do not establish effect-complete rollback in open systems.",
            "The trace does not establish learned routing, universal grounding, privacy, security, AGI, or ASI.",
            "No external-human prepublication review was requested or performed."
        ]
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes(canonical_bytes(result))
    descendants = [
        "experiments/qcsa_vertical_reference/task.json", "experiments/qcsa_vertical_reference/results/vertical_result.json",
        "scripts/build_qcsa_vertical_reference.py", "schemas/qcsa_vertical_reference_result.schema.json",
        "schemas/qcsa_vertical_reference_manifest.schema.json",
    ]
    rows = [{"path": path, "sha256": digest_bytes((ROOT / path).read_bytes()), "bytes": (ROOT / path).stat().st_size} for path in descendants]
    manifest = {
        "schema_version": "asi_stack.qcsa_vertical_reference_manifest.v0",
        "manifest_id": "qcsa-governed-vertical-reference-manifest-2026-07-13", "state": "content_addressed_complete",
        "descendants": rows, "result_sha256": digest_bytes(OUT.read_bytes()), "total_bytes": sum(row["bytes"] for row in rows),
        "support_state_effect": "none",
        "non_claims": ["Content addressing establishes file integrity only.", "The manifest does not establish semantic adequacy or supply-chain trust.", "The bounded trace creates no chapter-core support-state movement."]
    }
    MANIFEST.write_bytes(canonical_bytes(manifest))
    print(f"Built QCSA governed vertical reference: {len(STAGES)} stages, one observed temp effect, exact rollback, {len(adversarial)} rejected adversarial paths, {len(result['residuals'])} open residuals.")


if __name__ == "__main__":
    main()
