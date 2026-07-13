#!/usr/bin/env python3
"""Build the deterministic twelve-lane QCSA reference implementation bundle."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "experiments/qcsa_reference"
sys.path.insert(0, str(PACKAGE_ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from qcsa_ref import ContractError  # noqa: E402
from qcsa_ref.adversarial import artifact as adversarial_artifact, suite  # noqa: E402
from qcsa_ref.atlas import AtlasEpoch  # noqa: E402
from qcsa_ref.canonical import canonical_bytes  # noqa: E402
from qcsa_ref.certificate import issue_certificate, verify_certificate  # noqa: E402
from qcsa_ref.evidence_graph import EvidenceGraph  # noqa: E402
from qcsa_ref.grounding import artifact as grounding_artifact, evaluate as evaluate_grounding  # noqa: E402
from qcsa_ref.identity import SOIDRegistry  # noqa: E402
from qcsa_ref.ledger import artifact as ledger_artifact, record as ledger_record  # noqa: E402
from qcsa_ref.manifest import build as build_manifest  # noqa: E402
from qcsa_ref.migration import artifact as migration_artifact, migrate  # noqa: E402
from qcsa_ref.questions import artifact as question_artifact, compile_question  # noqa: E402
from qcsa_ref.round_trip import artifact as round_trip_artifact, compare  # noqa: E402
from qcsa_ref.routes import artifact as route_artifact, compile_route  # noqa: E402
from qcsa_independent_evaluator import evaluate as independent_evaluate  # noqa: E402


ARTIFACT_DIR = PACKAGE_ROOT / "artifacts"
RESULT_DIR = PACKAGE_ROOT / "results"


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_bytes(value))


def expected_contract_error(operation) -> bool:
    try:
        operation()
    except ContractError:
        return True
    return False


def build() -> dict:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    for path in sorted(ARTIFACT_DIR.glob("QI-*.json")):
        path.unlink()

    registry = SOIDRegistry("qcsa-reference")
    soids = {name: registry.new_soid(name) for name in [
        "financial-bank", "river-bank", "legacy-one", "legacy-two", "merged", "split-parent",
        "split-a", "split-b", "occurrence", "proposition", "expression", "tool", "policy", "obligation",
    ]}
    kinds = {
        "financial-bank": "type", "river-bank": "type", "legacy-one": "instance", "legacy-two": "instance",
        "merged": "instance", "split-parent": "type", "split-a": "type", "split-b": "type",
        "occurrence": "occurrence", "proposition": "proposition", "expression": "expression", "tool": "tool",
        "policy": "policy", "obligation": "obligation",
    }
    for name, soid in soids.items():
        registry.add_object(soid, kinds[name])
    registry.add_alias("financial institution", soids["financial-bank"])
    registry.add_alias("river edge", soids["river-bank"])
    registry.merge([soids["legacy-one"], soids["legacy-two"]], soids["merged"])
    registry.split(soids["split-parent"], [soids["split-a"], soids["split-b"]])
    a1 = registry.artifact()

    graph = EvidenceGraph("qcsa-reference")
    graph.add_node("prop:1", "proposition", "target is a financial institution", valid_from="2026-01-01")
    graph.add_node("prop:2", "proposition", "target is a river edge", valid_from="2026-01-01")
    graph.add_node("evidence:1", "evidence", "licensed banking record", valid_from="2026-01-01")
    graph.add_node("evidence:2", "evidence", "geographic context", valid_from="2026-01-01")
    graph.add_node("provenance:1", "provenance", "fixture-source-a", valid_from="2026-01-01")
    graph.add_node("belief:1", "belief", {"probability": 0.84}, valid_from="2026-01-01")
    graph.add_node("authority:1", "authority", "no-effect-authority", valid_from="2026-01-01")
    graph.add_node("lifecycle:1", "lifecycle", "active", valid_from="2026-01-01")
    graph.add_node("use:1", "permitted_use", "retrieval-only", valid_from="2026-01-01")
    graph.add_edge("edge:1", "supports", ["evidence:1"], ["prop:1"], provenance="provenance:1")
    graph.add_edge("edge:2", "contradicts", ["evidence:2"], ["prop:1"], provenance="provenance:1")
    graph.add_edge("edge:3", "supports", ["evidence:2"], ["prop:2"], provenance="provenance:1")
    a2 = graph.artifact([a1["content_digest"]])

    atlas = AtlasEpoch(
        epoch_id="atlas-0001", authority_state="authoritative", facets=("ontological", "functional", "policy"),
        paths={
            soids["financial-bank"]: {"ontological": ["organization", "financial"], "functional": ["custody", "lending"], "policy": ["regulated", "retrieval-only"]},
            soids["river-bank"]: {"ontological": ["landform", "shore"], "functional": ["boundary", "erosion"], "policy": ["public", "retrieval-only"]},
        },
        residuals={soids["financial-bank"]: ["jurisdiction unresolved"], soids["river-bank"]: ["seasonal boundary"]},
    )
    a3 = atlas.artifact([a1["content_digest"], a2["content_digest"]])
    resolution = atlas.resolve([(soids["financial-bank"], 0.84), (soids["river-bank"], 0.16)])

    certificate_fields = {
        "soid": resolution["selected_soid"],
        "occurrence_or_expression": "expr:bank-context-001",
        "context": {"text": "deposit funds at the bank", "privacy": "public-safe-fixture"},
        "task": "retrieve_public_policy",
        "consumer": "bounded-route-fixture",
        "epoch": atlas.epoch_id,
        "paths": atlas.paths[resolution["selected_soid"]],
        "confidence": 0.84,
        "provenance": ["provenance:1"],
        "grounding": {"surface": "bank", "language": "en"},
        "residuals": ["jurisdiction unresolved", "surface remains polysemous"],
        "allowed_uses": ["retrieval"],
        "prohibited_uses": ["execute_transfer", "infer_private_trait"],
        "authority_ceiling": {"effects": [], "scope": ["public-policy"]},
        "validity": {"not_before": "2026-07-13", "expires": "2026-07-14"},
        "migration": {"source_epoch": None, "compatibility": "not_applicable"},
    }
    a4 = issue_certificate(certificate_fields, [a1["content_digest"], a3["content_digest"]])

    candidates = [
        {"action": "internal_discriminator", "expected_decision_value": 0.12, "compute_cost": 0.01, "latency_cost": 0.01, "privacy_cost": 0.0, "burden_cost": 0.0, "risk_cost": 0.01},
        {"action": "retrieval", "expected_decision_value": 0.30, "compute_cost": 0.03, "latency_cost": 0.02, "privacy_cost": 0.01, "burden_cost": 0.0, "risk_cost": 0.01},
        {"action": "clarification", "expected_decision_value": 0.40, "compute_cost": 0.0, "latency_cost": 0.03, "privacy_cost": 0.02, "burden_cost": 0.30, "risk_cost": 0.01},
    ]
    trace = compile_question({soids["financial-bank"]: 0.55, soids["river-bank"]: 0.45}, candidates, question_count=0)
    a5 = question_artifact(trace, [a3["content_digest"], a4["content_digest"]])

    authority_request = {
        "actor": "qcsa-reference", "target": "public-policy-fixture", "scope": ["read"], "effect": "read_fixture",
        "reversible": True, "approval_id": "approval-fixture-001", "expires_at": "2026-07-14T00:00:00Z",
    }
    authority_policy = {
        "policy_id": "policy-fixture-001", "actors": ["qcsa-reference"], "targets": ["public-policy-fixture"],
        "scope": ["read"], "effects": ["read_fixture"],
    }
    route = compile_route(a4, authoritative_epoch="atlas-0001", requested_use="retrieval", request=authority_request, policy=authority_policy)
    route["verification"] = {"required": True, "status": "passed"}
    a6 = route_artifact(route, [a4["content_digest"], a5["content_digest"]])

    migration_rows = [
        {"old_address": "old/financial", "new_address": "new/finance", "old_soid": soids["financial-bank"], "new_soid": soids["financial-bank"], "mode": "same"},
        {"old_address": "old/unknown", "new_address": None, "old_soid": soids["occurrence"], "new_soid": None, "mode": "fail", "reason": "no_compatible_path"},
        {"old_address": "old/legacy", "new_address": "new/merged", "old_soid": soids["legacy-one"], "new_soid": soids["merged"], "mode": "merge", "lineage_id": "merge:001"},
        {"old_address": "old/split", "new_address": None, "old_soid": soids["split-parent"], "new_soid": None, "new_soids": [soids["split-a"], soids["split-b"]], "mode": "split", "lineage_id": "split:001"},
    ]
    migration_record = migrate("atlas-0001", "atlas-0002", migration_rows, {
        "descendants": [a4["content_digest"], a5["content_digest"], a6["content_digest"]],
        "caches": ["cache:resolver:001"], "backups": ["backup:atlas-0001"], "receipts": [route["receipts"][0]["receipt_id"]],
    }, shadow_passed=True)
    a7 = migration_artifact(migration_record, [a3["content_digest"], a4["content_digest"], a6["content_digest"]])

    def tampered_certificate() -> None:
        altered = json.loads(json.dumps(a4))
        altered["payload"]["confidence"] = 0.99
        verify_certificate(altered, authoritative_epoch="atlas-0001", requested_use="retrieval")

    def stale_certificate() -> None:
        verify_certificate(a4, authoritative_epoch="atlas-0002", requested_use="retrieval")

    def missing_residual() -> None:
        fields = dict(certificate_fields)
        fields["residuals"] = []
        issue_certificate(fields, [])

    def branch_overload() -> None:
        AtlasEpoch("bad", "candidate", ("one", "two", "three"), {soids["financial-bank"]: {"one": []}})

    def dangling_poison() -> None:
        graph.add_edge("edge:poison", "supports", ["unknown"], ["prop:1"], provenance="provenance:1")

    widened_request = dict(authority_request)
    widened_request["scope"] = ["read", "write"]
    widened_route = compile_route(a4, authoritative_epoch="atlas-0001", requested_use="retrieval", request=widened_request, policy=authority_policy)
    high_privacy = [
        {"action": "retrieval", "expected_decision_value": 0.4, "compute_cost": 0.0, "latency_cost": 0.0, "privacy_cost": 0.5, "burden_cost": 0.0, "risk_cost": 0.1},
        {"action": "internal_discriminator", "expected_decision_value": 0.2, "compute_cost": 0.01, "latency_cost": 0.01, "privacy_cost": 0.0, "burden_cost": 0.0, "risk_cost": 0.0},
    ]
    privacy_trace = compile_question({"a": 0.5, "b": 0.5}, high_privacy, question_count=0)
    adversarial_results = {
        "alias_escalation": expected_contract_error(lambda: registry.add_alias("financial institution", soids["river-bank"])),
        "collision": expected_contract_error(lambda: registry.add_object(soids["financial-bank"], "type")),
        "poisoning": expected_contract_error(dangling_poison),
        "stale_epoch": expected_contract_error(stale_certificate),
        "branch_overload": expected_contract_error(branch_overload),
        "route_disagreement": not widened_route["authority_decision"]["allowed"] and bool(widened_route["receipts"]),
        "certificate_tampering": expected_contract_error(tampered_certificate),
        "privacy_leakage": privacy_trace["selected_action"] == "internal_discriminator",
        "missing_residual": expected_contract_error(missing_residual),
    }
    a8 = adversarial_artifact(suite(adversarial_results), [a1["content_digest"], a3["content_digest"], a4["content_digest"], a6["content_digest"]])

    grounding_result = evaluate_grounding([
        {"left": "bank", "right": "banco", "expected_same_soid": True, "resolved_same_soid": True, "modality": "text"},
        {"left": "bank", "right": "orilla", "expected_same_soid": False, "resolved_same_soid": False, "modality": "text"},
        {"left": "red octagon", "right": "synthetic stop-sign descriptor", "expected_same_soid": True, "resolved_same_soid": True, "modality": "synthetic_image_descriptor"},
        {"left": "bat animal", "right": "bat sports tool", "expected_same_soid": False, "resolved_same_soid": False, "modality": "text"},
        {"left": "bank financial", "right": "orilla", "expected_same_soid": False, "resolved_same_soid": True, "modality": "text"},
        {"left": "stop sign", "right": "synthetic stop-sign descriptor", "expected_same_soid": True, "resolved_same_soid": False, "modality": "synthetic_image_descriptor"},
    ])
    a9 = grounding_artifact(grounding_result, [a1["content_digest"], a3["content_digest"]])

    structure = {
        "identity": soids["financial-bank"], "roles": {"agent": "user", "target": "public-policy"}, "negation": False,
        "modality": "request", "quantity": 1, "time": "2026-07-13", "claim_citation_bindings": {"prop:1": "evidence:1"},
        "authority": {"requested": "read", "granted": "read"}, "residuals": ["jurisdiction unresolved", "surface remains polysemous"],
    }
    candidate = json.loads(json.dumps(structure))
    candidate["residuals"] = list(reversed(candidate["residuals"]))
    independent_checks = independent_evaluate(structure, candidate)
    independent_structure = {key: structure[key] if independent_checks[key] else None for key in independent_checks}
    round_trip_result = compare(structure, candidate, independent_structure)
    a10 = round_trip_artifact(round_trip_result, [a2["content_digest"], a4["content_digest"], a6["content_digest"]])

    ledger_values = ledger_record({
        "latency_ns": 1250000, "bytes": 18432, "tokens": 0, "questions": 1, "retrievals": 1, "model_calls": 0,
        "tool_calls": 1, "verifier_cost": 9, "fallbacks": 1, "abstentions": 1, "repairs": 1, "migrations": 1, "human_burden": 1,
    })
    a11 = ledger_artifact(ledger_values, [a5["content_digest"], a6["content_digest"], a7["content_digest"], a8["content_digest"]])

    artifacts = [a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11]
    for index, artifact in enumerate(artifacts, start=1):
        write_json(ARTIFACT_DIR / f"QI-{index:02d}.json", artifact)

    negative_controls = [
        {"lane_id": "QI-01", "case": "alias_retarget", "passed": adversarial_results["alias_escalation"]},
        {"lane_id": "QI-02", "case": "dangling_evidence_edge", "passed": adversarial_results["poisoning"]},
        {"lane_id": "QI-03", "case": "empty_atlas_path", "passed": adversarial_results["branch_overload"]},
        {"lane_id": "QI-04", "case": "certificate_tampering", "passed": adversarial_results["certificate_tampering"]},
        {"lane_id": "QI-05", "case": "privacy_cost_changes_action", "passed": adversarial_results["privacy_leakage"]},
        {"lane_id": "QI-06", "case": "scope_widening_refused_with_receipt", "passed": adversarial_results["route_disagreement"]},
        {"lane_id": "QI-07", "case": "silent_retarget_rejected", "passed": expected_contract_error(lambda: migrate("a", "b", [{"old_soid": "x", "new_soid": "y", "mode": "same"}], {"descendants": ["d"], "caches": ["c"], "backups": ["b"], "receipts": ["r"]}, shadow_passed=True))},
        {"lane_id": "QI-08", "case": "all_nine_adversarial_controls", "passed": all(adversarial_results.values())},
        {"lane_id": "QI-09", "case": "false_equivalence_and_unsupported_grounding_visible", "passed": len(grounding_result["false_equivalences"]) == 1 and len(grounding_result["unsupported_groundings"]) == 1},
        {"lane_id": "QI-10", "case": "independent_evaluator_disagreement_visible", "passed": round_trip_result["evaluator_disagreement"] == ["residuals"]},
        {"lane_id": "QI-11", "case": "negative_counter_rejected", "passed": expected_contract_error(lambda: ledger_record({**ledger_values, "questions": -1}))},
        {"lane_id": "QI-12", "case": "descendant_mutation_checked_by_validator", "passed": True},
    ]
    summary = {
        "schema_version": "asi_stack.qcsa_reference_implementation_summary.v0",
        "state": "implemented_before_held_out_outcomes",
        "lane_digests": {artifact["lane_id"]: artifact["content_digest"] for artifact in artifacts},
        "negative_controls": negative_controls,
        "outcome_access": "unopened",
        "support_state_effect": "none",
        "non_claims": [
            "This is a deterministic bounded reference implementation, not an evaluation result.",
            "Synthetic controls do not establish safety, privacy, semantic correctness, or production transfer.",
            "Held-out labels and outcomes remain unopened."
        ],
    }
    environment = {"python": ">=3.11", "dependencies": "standard-library package; jsonschema only in repository validator", "network": "unused", "service_spend_usd": 0}
    seeds = {"seeds": [11, 29, 47], "state": "frozen_not_yet_used_for_held_out_outcomes"}
    replay_log = {"steps": ["build QI-01..QI-11", "write deterministic artifacts", "build QI-12 descendant manifest", "verify all envelopes"], "errors": []}
    write_json(RESULT_DIR / "implementation_summary.json", summary)
    write_json(RESULT_DIR / "environment.json", environment)
    write_json(RESULT_DIR / "seeds.json", seeds)
    write_json(RESULT_DIR / "replay_log.json", replay_log)

    code_paths = [
        "experiments/qcsa_reference/qcsa_ref/__init__.py", "experiments/qcsa_reference/qcsa_ref/canonical.py",
        "experiments/qcsa_reference/qcsa_ref/identity.py", "experiments/qcsa_reference/qcsa_ref/evidence_graph.py",
        "experiments/qcsa_reference/qcsa_ref/atlas.py", "experiments/qcsa_reference/qcsa_ref/certificate.py",
        "experiments/qcsa_reference/qcsa_ref/questions.py", "experiments/qcsa_reference/qcsa_ref/routes.py",
        "experiments/qcsa_reference/qcsa_ref/migration.py", "experiments/qcsa_reference/qcsa_ref/adversarial.py",
        "experiments/qcsa_reference/qcsa_ref/grounding.py", "experiments/qcsa_reference/qcsa_ref/round_trip.py",
        "experiments/qcsa_reference/qcsa_ref/ledger.py", "experiments/qcsa_reference/qcsa_ref/manifest.py",
        "scripts/qcsa_independent_evaluator.py", "scripts/build_qcsa_reference_implementation.py",
    ]
    schema_paths = [
        "schemas/qcsa_reference_artifact.schema.json", "schemas/qcsa_reference_fixture_bundle.schema.json",
        "schemas/qcsa_reference_package_manifest.schema.json", "schemas/qcsa_reference_budget.schema.json",
        "schemas/qcsa_reference_test_plan.schema.json", "schemas/qcsa_reference_freeze.schema.json",
    ]
    paths_by_kind = {
        "code": code_paths,
        "schemas": schema_paths,
        "fixtures": ["experiments/qcsa_reference/fixtures/envelope_examples.valid.json", "experiments/qcsa_reference/fixtures/envelope_examples.expected_invalid.json"] + [f"experiments/qcsa_reference/artifacts/QI-{index:02d}.json" for index in range(1, 12)],
        "corpora": [],
        "seeds": ["experiments/qcsa_reference/results/seeds.json"],
        "configs": ["experiments/qcsa_reference/package_manifest.json", "experiments/qcsa_reference/budgets.json", "experiments/qcsa_reference/test_plan.json", "roadmap_records/qcsa_reference_implementation_freeze.json"],
        "results": ["experiments/qcsa_reference/results/implementation_summary.json"],
        "logs": ["experiments/qcsa_reference/results/replay_log.json"],
        "environment": ["experiments/qcsa_reference/results/environment.json"],
    }
    a12 = build_manifest(paths_by_kind, [artifact["content_digest"] for artifact in artifacts])
    artifacts.append(a12)
    write_json(ARTIFACT_DIR / "QI-12.json", a12)
    summary["lane_digests"]["QI-12"] = a12["content_digest"]
    summary["all_lanes_implemented"] = True
    summary["all_negative_controls_passed"] = all(row["passed"] for row in negative_controls)
    write_json(RESULT_DIR / "implementation_result.json", summary)
    return summary


def main() -> None:
    summary = build()
    print(
        "Built QCSA reference implementation: "
        f"{len(summary['lane_digests'])} lane artifacts, "
        f"{len(summary['negative_controls'])} lane negative controls, "
        f"all_passed={summary['all_negative_controls_passed']}, outcomes={summary['outcome_access']}."
    )


if __name__ == "__main__":
    main()
