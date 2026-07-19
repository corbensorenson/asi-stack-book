#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import re
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "tests/fixtures/protocol_records/white_box_evidence_packet.valid.json"
PROTOCOL = ROOT / "experiments/white_box_argument_exit/preregistration.json"
LEAN = ROOT / "lean/AsiStackProofs/WhiteBoxEvidence.lean"
CHAPTER = ROOT / "chapters/white-box-evidence-interpretability-and-activation-governance.qmd"


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def packet_errors(packet: dict[str, Any]) -> list[str]:
    out: list[str] = []
    if packet.get("schema_version") != "asi_stack.white_box_evidence_packet.v1":
        out.append("packet schema identity drifted")
    identity = packet.get("identity", {})
    for field in (
        "model_id", "checkpoint_digest", "tokenizer_digest", "substrate",
        "runtime_digest", "capture_site", "population_id", "captured_at",
    ):
        if not identity.get(field):
            out.append(f"packet identity missing {field}")
    method = packet.get("method", {})
    if not method.get("assumptions") or not method.get("implementation_digest") or not method.get("configuration_digest"):
        out.append("method assumptions or identity missing")
    interpretation = packet.get("interpretation", {})
    if not interpretation.get("hard_counterexamples") or not interpretation.get("alternative_hypotheses"):
        out.append("interpretation alternatives or counterexamples missing")
    causal = packet.get("causal_evidence", {})
    if not causal.get("negative_controls") or not causal.get("positive_controls"):
        out.append("positive or negative control denominator missing")
    if packet.get("disposition") == "causal_bounded":
        if causal.get("status") not in {"necessity_bounded", "sufficiency_bounded", "mediation_bounded"}:
            out.append("bounded-causal disposition launders a noncausal state")
        if not causal.get("behavioral_cross_check") or not causal.get("interventions"):
            out.append("bounded-causal disposition lacks cross-check or intervention")
        stability = packet.get("stability", {})
        if not all(stability.get(key) for key in ("held_out_prompts", "seed_variation", "transformation_tests", "checkpoint_tests")):
            out.append("bounded-causal disposition lacks stability coverage")
        if not packet.get("independence", {}).get("separate_implementation"):
            out.append("bounded-causal disposition lacks separate evaluator implementation")
    coverage = packet.get("coverage_and_residual", {})
    for field in (
        "reconstruction_ref", "dead_or_missing_objects_ref", "split_merge_ref",
        "unexplained_residual_ref", "method_disagreement_ref",
    ):
        if not coverage.get(field):
            out.append(f"coverage/residual record missing {field}")
    if coverage.get("complete_mechanism_claimed") is not False:
        out.append("packet claims a complete mechanism")
    governance = packet.get("governance", {})
    if governance.get("policy_effect") not in {"preserve", "restrict", "escalate", "reject"}:
        out.append("packet requests an unauthorized governance effect")
    if governance.get("authority_delta") not in {"none", "reduced"}:
        out.append("packet widens authority")
    if governance.get("release_authority") is not False:
        out.append("packet claims release authority")
    expiry = packet.get("expiry", {})
    if expiry.get("material_change_observed") is True:
        if packet.get("disposition") != "expired" or governance.get("policy_effect") != "reject":
            out.append("materially changed packet remains consumable")
    if packet.get("support_state_effect") != "none":
        out.append("packet claims support movement")
    non_claims = " ".join(packet.get("non_claims", [])).lower()
    for phrase in ("no model", "no feature", "support", "agi", "asi"):
        if phrase not in non_claims:
            out.append(f"packet non-claim boundary missing {phrase}")
    return out


def protocol_errors(protocol: dict[str, Any]) -> list[str]:
    out: list[str] = []
    if protocol.get("campaign_id") != "WHITE-BOX-ARGUMENT-EXIT-01":
        out.append("campaign identity drifted")
    if protocol.get("state") != "protocol_ready_resource_isolated_not_executed":
        out.append("protocol execution state drifted")
    if protocol.get("protected_outcomes_opened") is not False:
        out.append("protected white-box outcomes were opened")
    if protocol.get("support_state_effect") != "none" or protocol.get("current_support_state") != "argument":
        out.append("protocol launders support")
    selection = protocol.get("selection_before_outcomes", {})
    if len(selection.get("behavior_candidates", [])) != 3 or len(selection.get("forbidden_selection_inputs", [])) != 5:
        out.append("prospective behavior selection or forbidden-input denominator drifted")
    methods = protocol.get("method_families", [])
    if len(methods) != 2 or len({row.get("implementation_owner") for row in methods}) != 2:
        out.append("two independently owned method families are not frozen")
    if len(protocol.get("comparators", [])) < 6:
        out.append("comparator set is incomplete")
    custody = protocol.get("data_custody", {})
    if not all(custody.get(key) for key in ("development_split", "qualification_split", "held_out_split", "transfer_split", "denominator_separation")):
        out.append("split custody is incomplete")
    if len(protocol.get("competence_gates", [])) != 7:
        out.append("seven-gate competence denominator drifted")
    if len(protocol.get("rescue_ladder", [])) != 6:
        out.append("bounded rescue ladder drifted")
    if len(protocol.get("outcomes", [])) != 9:
        out.append("joint outcome denominator drifted")
    decision = protocol.get("decision_rule", {})
    if not all(decision.get(key) for key in ("positive", "negative_exact", "inconclusive")):
        out.append("positive, exact-negative, or inconclusive rule missing")
    if not str(decision.get("maximum_negative_level", "")).startswith("N3 for the exact frozen"):
        out.append("negative inference ceiling exceeds N3 exact scope")
    resource = protocol.get("resource_and_isolation_gate", {})
    if resource.get("minimum_free_space_before_materialization_gib") != 62:
        out.append("resource isolation floor drifted")
    if resource.get("p2_reserved_storage_may_be_reclaimed") is not False or resource.get("p2_images_or_denominators_may_be_changed") is not False:
        out.append("white-box lane may displace protected P2 work")
    if len(protocol.get("artifact_contract", [])) != 9:
        out.append("claim-bearing artifact contract drifted")
    non_claims = " ".join(protocol.get("non_claims", [])).lower()
    for phrase in ("not an interpretability experiment", "no support", "agi", "asi"):
        if phrase not in non_claims:
            out.append(f"protocol non-claim boundary missing {phrase}")
    return out


def source_errors(source: str, chapter: str) -> list[str]:
    out: list[str] = []
    normalized_chapter = re.sub(r"\s+", " ", chapter)
    required_lean = (
        "def ScientificallyAdmissible",
        "def WhiteBoxRouteFor",
        "theorem evidence_never_grants_authority",
        "theorem invalid_packet_rejected",
        "theorem admitted_causal_packet_records_crosscheck_intervention_and_evaluator",
        "theorem material_change_expires_admissible_packet",
        "GovernanceRoute.grantWidening",
    )
    for token in required_lean:
        if token not in source:
            out.append(f"Lean semantic surface missing {token}")
    if len(re.findall(r"(?m)^theorem ", source)) != 8:
        out.append("WhiteBoxEvidence theorem denominator drifted")
    for phrase in (
        "protocol-ready and resource-isolated, not executed",
        "record and workflow properties",
        "cannot grant execution or release authority",
        "No model-internal outcome was opened",
    ):
        if phrase not in normalized_chapter:
            out.append(f"chapter terminal boundary missing: {phrase}")
    return out


def errors(data: dict[str, Any]) -> list[str]:
    return packet_errors(data["packet"]) + protocol_errors(data["protocol"]) + source_errors(data["lean"], data["chapter"])


def main() -> None:
    data = {
        "packet": load(PACKET),
        "protocol": load(PROTOCOL),
        "lean": LEAN.read_text(encoding="utf-8"),
        "chapter": CHAPTER.read_text(encoding="utf-8"),
    }
    failures = errors(data)
    mutations = [
        ("grant release", lambda value: value["packet"]["governance"].__setitem__("release_authority", True)),
        ("widen authority", lambda value: value["packet"]["governance"].__setitem__("authority_delta", "widened")),
        ("claim completeness", lambda value: value["packet"]["coverage_and_residual"].__setitem__("complete_mechanism_claimed", True)),
        ("erase negative controls", lambda value: value["packet"]["causal_evidence"].__setitem__("negative_controls", [])),
        ("erase alternatives", lambda value: value["packet"]["interpretation"].__setitem__("alternative_hypotheses", [])),
        ("consume stale packet", lambda value: value["packet"].__setitem__("disposition", "observed")),
        ("open protected outcomes", lambda value: value["protocol"].__setitem__("protected_outcomes_opened", True)),
        ("claim execution", lambda value: value["protocol"].__setitem__("state", "completed_positive")),
        ("delete competence gate", lambda value: value["protocol"]["competence_gates"].pop()),
        ("raise negative scope", lambda value: value["protocol"]["decision_rule"].__setitem__("maximum_negative_level", "N5 field-wide")),
        ("take P2 storage", lambda value: value["protocol"]["resource_and_isolation_gate"].__setitem__("p2_reserved_storage_may_be_reclaimed", True)),
        ("invent support", lambda value: value["protocol"].__setitem__("support_state_effect", "empirical-test-backed")),
    ]
    baseline = set(errors(data))
    for label, mutation in mutations:
        candidate = copy.deepcopy(data)
        mutation(candidate)
        if not set(errors(candidate)) - baseline:
            failures.append(f"negative mutation accepted: {label}")
    lean_result = subprocess.run(
        ["lake", "env", "lean", "AsiStackProofs/WhiteBoxEvidence.lean"],
        cwd=ROOT / "lean", text=True, capture_output=True,
    )
    if lean_result.returncode:
        failures.append("WhiteBoxEvidence Lean check failed: " + (lean_result.stdout + lean_result.stderr).strip())
    if failures:
        raise SystemExit("White-box evidence contract failed:\n - " + "\n - ".join(failures))
    print(
        "White-box evidence contract passed: one schema fixture, two formal targets "
        "implemented through 8 theorem declarations, 2 independently owned method "
        "families, 7 competence gates, 6 rescue steps, 9 joint outcomes, 12 mutations "
        "rejected; empirical and support effects none."
    )


if __name__ == "__main__":
    main()
