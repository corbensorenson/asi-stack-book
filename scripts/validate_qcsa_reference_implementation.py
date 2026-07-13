#!/usr/bin/env python3
"""Validate deterministic behavior and artifacts for all twelve QCSA lanes."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "experiments/qcsa_reference"
sys.path.insert(0, str(PACKAGE_ROOT))

from qcsa_ref.canonical import ContractError, body_digest, verify_envelope  # noqa: E402


MANIFEST = PACKAGE_ROOT / "package_manifest.json"
RESULT = PACKAGE_ROOT / "results/implementation_result.json"
ARTIFACT_DIR = PACKAGE_ROOT / "artifacts"
BUILDER = ROOT / "scripts/build_qcsa_reference_implementation.py"
LANES = [f"QI-{index:02d}" for index in range(1, 13)]
KINDS = {"occurrence", "type", "instance", "proposition", "expression", "tool", "policy", "obligation"}
ROUND_TRIP_FIELDS = {"identity", "roles", "negation", "modality", "quantity", "time", "claim_citation_bindings", "authority", "residuals"}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def redigest(artifact: dict) -> None:
    artifact["content_digest"] = body_digest(artifact)


def snapshot_outputs() -> dict[str, bytes]:
    paths = sorted(ARTIFACT_DIR.glob("QI-*.json")) + sorted((PACKAGE_ROOT / "results").glob("*.json"))
    return {path.relative_to(ROOT).as_posix(): path.read_bytes() for path in paths}


def descendant_errors(artifact: dict) -> list[str]:
    errors = []
    payload = artifact["payload"]
    if payload.get("missing_descendants") or payload.get("mutated_descendants"):
        errors.append("manifest reports missing or mutated descendants")
    for kind in ("code", "schemas", "fixtures", "corpora", "seeds", "configs", "results", "logs", "environment"):
        if kind not in payload:
            errors.append(f"manifest missing category {kind}")
            continue
        for row in payload[kind]:
            path = ROOT / row["path"]
            if not path.is_file():
                errors.append(f"manifest descendant absent: {row['path']}")
                continue
            import hashlib
            if hashlib.sha256(path.read_bytes()).hexdigest() != row["sha256"] or path.stat().st_size != row["bytes"]:
                errors.append(f"manifest descendant mutated: {row['path']}")
    return errors


def semantic_errors(data: dict) -> list[str]:
    errors: list[str] = []
    manifest = data["manifest"]
    result = data["result"]
    artifacts = data["artifacts"]
    lanes = manifest.get("lanes", [])
    if [row.get("id") for row in lanes] != LANES or sorted(artifacts) != LANES:
        errors.append("implementation must contain QI-01 through QI-12 exactly")
        return errors
    if result.get("state") != "implemented_before_held_out_outcomes" or result.get("outcome_access") != "unopened":
        errors.append("implementation result improperly opens held-out outcomes")
    if not result.get("all_lanes_implemented") or not result.get("all_negative_controls_passed"):
        errors.append("implementation result does not record all lanes and controls passing")
    controls = result.get("negative_controls", [])
    if [row.get("lane_id") for row in controls] != LANES or not all(row.get("passed") for row in controls):
        errors.append("one rejecting behavioral control per lane must pass")
    if result.get("support_state_effect") != "none":
        errors.append("implementation improperly moves support state")

    seen_digests = set()
    for lane in lanes:
        lane_id = lane["id"]
        artifact = artifacts[lane_id]
        try:
            verify_envelope(artifact)
        except ContractError as exc:
            errors.append(f"{lane_id}: {exc}")
            continue
        if artifact["lane_id"] != lane_id:
            errors.append(f"{lane_id}: envelope lane mismatch")
        if artifact["owner_chapters"] != lane["owner_chapters"]:
            errors.append(f"{lane_id}: chapter owner drift")
        if set(artifact["payload"]) != set(lane["required_payload_fields"]):
            errors.append(f"{lane_id}: payload differs from frozen field contract")
        if result.get("lane_digests", {}).get(lane_id) != artifact["content_digest"]:
            errors.append(f"{lane_id}: result digest drift")
        if any(parent not in seen_digests for parent in artifact["input_digests"]):
            errors.append(f"{lane_id}: input digest is absent or forward-referenced")
        seen_digests.add(artifact["content_digest"])

    p1 = artifacts["QI-01"]["payload"]
    if {row["kind"] for row in p1["objects"]} != KINDS:
        errors.append("QI-01 does not separate all eight object kinds")
    if len({row["soid"] for row in p1["objects"]}) != len(p1["objects"]) or p1["retarget_controls"].get("alias_new_target") != "reject":
        errors.append("QI-01 duplicate or silent-retarget control missing")
    if not p1["merge_lineage"] or not p1["split_lineage"]:
        errors.append("QI-01 merge/split lineage missing")

    p2 = artifacts["QI-02"]["payload"]
    node_ids = {row["id"] for row in p2["nodes"]}
    if not p2["contradictions"] or any(ref not in node_ids for edge in p2["hyperedges"] for ref in edge["sources"] + edge["targets"]):
        errors.append("QI-02 contradiction or dangling-reference control failed")
    if not all(p2[key] for key in ["propositions", "evidence", "provenance", "beliefs", "authorities", "lifecycles", "permitted_uses"]):
        errors.append("QI-02 collapses required evidence-state types")

    p3 = artifacts["QI-03"]["payload"]
    if len(p3["facets"]) < 3 or p3["authority_state"] != "authoritative" or p3["candidate_epoch"].get("authority_state") != "candidate" or p3["candidate_epoch"].get("may_route_effects"):
        errors.append("QI-03 candidate/authoritative plural-atlas boundary failed")
    if not p3["immutable"] or not p3["unknowns"] or not p3["conflicts"] or not p3["abstentions"]:
        errors.append("QI-03 immutable open-world outcomes missing")

    p4 = artifacts["QI-04"]["payload"]
    if not p4["residuals"] or p4["signature_fixture"].get("algorithm") != "sha256-fixture-not-cryptographic-identity" or p4["authority_ceiling"].get("effects"):
        errors.append("QI-04 residual, fixture-signature, or zero-effect ceiling boundary failed")
    if set(p4["allowed_uses"]) & set(p4["prohibited_uses"]):
        errors.append("QI-04 allowed/prohibited uses conflict")

    p5 = artifacts["QI-05"]["payload"]
    selected = next((row for row in p5["candidate_actions"] if row["action"] == p5["selected_action"]), None)
    if selected is None or p5["selected_action"] != "retrieval" or any(p5[key] != selected[key] for key in ["expected_decision_value", "compute_cost", "latency_cost", "privacy_cost", "burden_cost", "risk_cost"]):
        errors.append("QI-05 selected action is not the frozen value-minus-cost decision")

    p6 = artifacts["QI-06"]["payload"]
    if len(p6["attempted_effects"]) != len(p6["receipts"]) or not p6["authority_decision"].get("allowed") or p6["verification"].get("status") != "passed":
        errors.append("QI-06 receipt, authority, or verification contract failed")
    if not any(step["kind"] == "tool_fixture" for step in p6["steps"]):
        errors.append("QI-06 has no bounded adapter step")

    p7 = artifacts["QI-07"]["payload"]
    if any(row["old_soid"] != row["new_soid"] for row in p7["compatibility"]) or not p7["typed_failures"] or not p7["merge_lineage"] or not p7["split_lineage"]:
        errors.append("QI-07 same-SOID compatibility or typed lineage failed")
    if not p7["rollback_identity"].get("complete") or not all(p7[key] for key in ["descendants", "caches", "backups", "receipts"]):
        errors.append("QI-07 rollback or descendant inventory incomplete")

    p8 = artifacts["QI-08"]["payload"]
    adversarial_keys = {"alias_escalation", "collision", "poisoning", "stale_epoch", "branch_overload", "route_disagreement", "certificate_tampering", "privacy_leakage", "missing_residual"}
    if not all(p8.get(key) is True for key in adversarial_keys) or p8.get("disposition") != "all_rejected":
        errors.append("QI-08 adversarial suite did not reject all nine controls")

    p9 = artifacts["QI-09"]["payload"]
    if len(p9["false_equivalences"]) != 1 or len(p9["unsupported_groundings"]) != 1 or p9["coverage_boundary"].get("open_world") is not False:
        errors.append("QI-09 false-equivalence, unsupported-grounding, or coverage boundary missing")

    p10 = artifacts["QI-10"]["payload"]
    if p10["evaluator_implementation"] != "scripts/qcsa_independent_evaluator.py" or set(p10) != ROUND_TRIP_FIELDS | {"candidate_digest", "evaluator_implementation", "evaluator_disagreement"}:
        errors.append("QI-10 independent evaluator or structural dimensions drifted")
    if p10["evaluator_disagreement"] != ["residuals"]:
        errors.append("QI-10 evaluator-disagreement control is not preserved")

    p11 = artifacts["QI-11"]["payload"]
    if any(not isinstance(value, int) or value < 0 for value in p11.values()) or not all(key in p11 for key in ["latency_ns", "questions", "retrievals", "tool_calls", "verifier_cost", "fallbacks", "abstentions", "repairs", "migrations", "human_burden"]):
        errors.append("QI-11 resource/governance ledger is incomplete or invalid")

    errors.extend(f"QI-12: {message}" for message in descendant_errors(artifacts["QI-12"]))
    if set(artifacts["QI-12"]["input_digests"]) != {artifacts[lane]["content_digest"] for lane in LANES[:-1]}:
        errors.append("QI-12 does not bind all eleven upstream lane artifacts")
    return errors


def negative_controls(base: dict) -> list[str]:
    failures: list[str] = []
    mutations: list[tuple[str, dict]] = []

    def mutated(label: str, lane: str, update) -> None:
        value = copy.deepcopy(base)
        update(value["artifacts"][lane])
        redigest(value["artifacts"][lane])
        value["result"]["lane_digests"][lane] = value["artifacts"][lane]["content_digest"]
        mutations.append((label, value))

    broken_digest = copy.deepcopy(base)
    broken_digest["artifacts"]["QI-01"]["content_digest"] = "0" * 64
    mutations.append(("content digest tampering", broken_digest))
    mutated("object-kind collapse", "QI-01", lambda row: row["payload"]["objects"].__setitem__(0, {**row["payload"]["objects"][0], "kind": "type"}))
    mutated("dangling evidence edge", "QI-02", lambda row: row["payload"]["hyperedges"][0]["sources"].append("missing"))
    mutated("candidate epoch may route", "QI-03", lambda row: row["payload"]["candidate_epoch"].__setitem__("may_route_effects", True))
    mutated("signature fixture laundering", "QI-04", lambda row: row["payload"]["signature_fixture"].__setitem__("algorithm", "production-signature"))
    mutated("question selection drift", "QI-05", lambda row: row["payload"].__setitem__("selected_action", "clarification"))
    mutated("effect receipt erased", "QI-06", lambda row: row["payload"]["receipts"].clear())
    mutated("migration silent retarget", "QI-07", lambda row: row["payload"]["compatibility"][0].__setitem__("new_soid", "soid:different"))
    mutated("adversarial miss hidden", "QI-08", lambda row: row["payload"].__setitem__("poisoning", False))
    mutated("grounding residual erased", "QI-09", lambda row: row["payload"]["false_equivalences"].clear())
    mutated("evaluator self-confirmation", "QI-10", lambda row: row["payload"].__setitem__("evaluator_implementation", "experiments/qcsa_reference/qcsa_ref/round_trip.py"))
    mutated("negative governance counter", "QI-11", lambda row: row["payload"].__setitem__("questions", -1))
    mutated("descendant digest mutation", "QI-12", lambda row: row["payload"]["code"][0].__setitem__("sha256", "0" * 64))

    failed_control = copy.deepcopy(base)
    failed_control["result"]["negative_controls"][0]["passed"] = False
    mutations.append(("failed lane control hidden", failed_control))
    outcomes_opened = copy.deepcopy(base)
    outcomes_opened["result"]["outcome_access"] = "opened"
    mutations.append(("held-out outcomes opened", outcomes_opened))

    for label, value in mutations:
        if not semantic_errors(value):
            failures.append(f"negative control was accepted: {label}")
    return failures


def build_base() -> dict:
    manifest = load(MANIFEST)
    result = load(RESULT)
    artifacts = {lane: load(ARTIFACT_DIR / f"{lane}.json") for lane in LANES}
    return {"manifest": manifest, "result": result, "artifacts": artifacts}


def main() -> None:
    required = [MANIFEST, RESULT, BUILDER] + [ARTIFACT_DIR / f"{lane}.json" for lane in LANES]
    missing = [path.relative_to(ROOT).as_posix() for path in required if not path.is_file()]
    if missing:
        raise SystemExit("Missing QCSA implementation artifacts: " + ", ".join(missing))
    before = snapshot_outputs()
    first = subprocess.run([sys.executable, str(BUILDER)], cwd=ROOT, check=True, capture_output=True, text=True)
    after_first = snapshot_outputs()
    second = subprocess.run([sys.executable, str(BUILDER)], cwd=ROOT, check=True, capture_output=True, text=True)
    after_second = snapshot_outputs()
    errors = []
    if before != after_first or after_first != after_second:
        errors.append("two clean builder replays were not byte-deterministic")
    if "12 lane artifacts" not in first.stdout or "all_passed=True" not in second.stdout:
        errors.append("builder completion output drifted")
    base = build_base()
    errors.extend(semantic_errors(base))
    errors.extend(negative_controls(base))
    if errors:
        raise SystemExit("\n".join(f"- {error}" for error in errors))
    print("QCSA reference implementation passed: 12 deterministic content-addressed lane artifacts, 8 identity kinds, typed evidence and contradiction, plural candidate/authoritative atlas states, certificate residuals, value-cost questions, separate authority with receipts, migration/rollback inventory, 9 adversarial controls, bounded grounding residuals, independent-evaluator disagreement, governance ledger, descendant replay, 12 lane controls, and 15 rejecting validator mutations; held-out outcomes remain unopened.")


if __name__ == "__main__":
    main()
