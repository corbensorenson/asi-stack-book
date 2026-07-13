#!/usr/bin/env python3
"""Validate and replay the bounded QCSA governed vertical reference path."""

from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "experiments/qcsa_vertical_reference/results/vertical_result.json"
MANIFEST = ROOT / "experiments/qcsa_vertical_reference/results/artifact_manifest.json"
RESULT_SCHEMA = ROOT / "schemas/qcsa_vertical_reference_result.schema.json"
MANIFEST_SCHEMA = ROOT / "schemas/qcsa_vertical_reference_manifest.schema.json"
BUILDER = ROOT / "scripts/build_qcsa_vertical_reference.py"
REPORT = ROOT / "docs/qcsa_governed_vertical_reference_report.md"
STAGES = [
    "intent", "semantic_ir", "identity_and_address", "evidence_graph",
    "question_compiler", "context_materialization", "route_plan",
    "authority_decision", "bounded_adapter_action", "independent_verification",
    "artifact_and_receipt_graph", "migration", "rollback",
]
ATTACKS = {f"VA-{index:02d}" for index in range(1, 11)}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def semantic_errors(data: dict, *, check_files: bool = False) -> list[str]:
    result, manifest, report = data["result"], data["manifest"], data["report"]
    errors = [f"result schema: {error.message}" for error in Draft202012Validator(load(RESULT_SCHEMA)).iter_errors(result)]
    errors.extend(f"manifest schema: {error.message}" for error in Draft202012Validator(load(MANIFEST_SCHEMA)).iter_errors(manifest))
    if result.get("stage_order") != STAGES or set(result.get("stages", {})) != set(STAGES):
        errors.append("vertical trace must contain thirteen exact ordered stages")
    stages = result.get("stages", {})
    identity = stages.get("identity_and_address", {})
    if identity.get("resolution", {}).get("selected_soid") != identity.get("soid") or identity.get("epoch") != "atlas-vertical-v1":
        errors.append("stable identity/address resolution drifted")
    if stages.get("evidence_graph", {}).get("truth_inferred_from_position") is not False:
        errors.append("evidence graph launders position into truth")
    if stages.get("route_plan", {}).get("semantic_resolution_grants_authority") is not False:
        errors.append("semantic resolution improperly grants authority")
    if stages.get("authority_decision", {}).get("allowed") is not True:
        errors.append("recorded main effect lacks the exact separate allow decision")
    effect = result.get("effect_observation", {})
    verification = stages.get("independent_verification", {})
    if effect.get("before_sha256") == effect.get("after_sha256") or not effect.get("verified") or not verification.get("exact") or verification.get("unexpected_paths") != []:
        errors.append("effect was not independently observed as the exact intended change")
    receipt = stages.get("bounded_adapter_action", {})
    graph = stages.get("artifact_and_receipt_graph", {})
    if not receipt.get("observed") or not receipt.get("verification_exact") or not receipt.get("receipt_id") or not graph.get("all_effects_observed") or not graph.get("all_attempts_receipted"):
        errors.append("effect/receipt/artifact graph completeness drifted")
    lifecycle = result.get("migration_and_rollback", {})
    rollback = stages.get("rollback", {})
    if not all(lifecycle.get(key) is True for key in ["same_soid", "typed_lineage", "descendant_inventory_complete", "byte_exact_rollback"]) or lifecycle.get("hidden_effects_after_rollback") != [] or not rollback.get("byte_exact") or rollback.get("unexpected_paths_after") != []:
        errors.append("migration or rollback is not identity-preserving and effect-complete for the fixture")
    attacks = result.get("adversarial_matrix", [])
    if {row.get("case_id") for row in attacks} != ATTACKS or any(not row.get("rejected") or row.get("effect_released") for row in attacks):
        errors.append("ten adversarial paths are not all fail-closed without effects")
    ledger = result.get("resource_ledger", {})
    expected_ledger = {"network_calls": 0, "service_spend_usd": 0, "model_calls": 0, "external_humans": 0, "questions": 1, "tool_effects_attempted": 1, "tool_effects_released": 1, "effects_observed": 1, "receipts": 1, "rollbacks_attempted": 1, "rollbacks_exact": 1, "negative_controls": 10}
    if any(ledger.get(key) != value for key, value in expected_ledger.items()):
        errors.append("vertical resource/effect ledger drifted")
    residuals = result.get("residuals", [])
    if [row.get("id") for row in residuals] != [f"VR-{index:02d}" for index in range(1, 9)] or any(row.get("state") != "open" for row in residuals):
        errors.append("eight vertical residuals are not explicit and open")
    if result.get("support_state_effect") != "none" or manifest.get("support_state_effect") != "none":
        errors.append("vertical trace moves support state")
    if check_files:
        descendants = manifest.get("descendants", [])
        for row in descendants:
            path = ROOT / row["path"]
            if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != row["sha256"] or path.stat().st_size != row["bytes"]:
                errors.append(f"vertical descendant drifted: {row['path']}")
        if hashlib.sha256(RESULT.read_bytes()).hexdigest() != manifest.get("result_sha256"):
            errors.append("vertical result digest drifted")
        if manifest.get("total_bytes") != sum(row["bytes"] for row in descendants):
            errors.append("vertical manifest byte total drifted")
    for phrase in ["thirteen explicit stages", "real bytes", "Semantic resolution does not grant authority", "eight residuals stay open", "does not warrant a new QCSA chapter"]:
        if phrase not in report:
            errors.append(f"vertical report missing boundary: {phrase}")
    return errors


def negative_controls(base: dict) -> list[str]:
    mutations = []
    def mutate(label, fn):
        value = copy.deepcopy(base); fn(value); mutations.append((label, value))
    mutate("stage erased", lambda d: d["result"]["stages"].pop("semantic_ir"))
    mutate("stage order drift", lambda d: d["result"]["stage_order"].reverse())
    mutate("truth laundering", lambda d: d["result"]["stages"]["evidence_graph"].__setitem__("truth_inferred_from_position", True))
    mutate("authority laundering", lambda d: d["result"]["stages"]["route_plan"].__setitem__("semantic_resolution_grants_authority", True))
    mutate("effect unobserved", lambda d: d["result"]["effect_observation"].__setitem__("verified", False))
    mutate("receipt erased", lambda d: d["result"]["stages"]["bounded_adapter_action"].__setitem__("receipt_id", ""))
    mutate("migration retarget", lambda d: d["result"]["migration_and_rollback"].__setitem__("same_soid", False))
    mutate("rollback mismatch", lambda d: d["result"]["migration_and_rollback"].__setitem__("byte_exact_rollback", False))
    mutate("hidden effect", lambda d: d["result"]["migration_and_rollback"].__setitem__("hidden_effects_after_rollback", ["side-effect.log"]))
    mutate("attack erased", lambda d: d["result"]["adversarial_matrix"].pop())
    mutate("attack released", lambda d: d["result"]["adversarial_matrix"][0].__setitem__("effect_released", True))
    mutate("network hidden", lambda d: d["result"]["resource_ledger"].__setitem__("network_calls", 1))
    mutate("residual erased", lambda d: d["result"]["residuals"].pop())
    mutate("support promotion", lambda d: d["result"].__setitem__("support_state_effect", "prototype-backed"))
    mutate("descendant digest", lambda d: d["manifest"]["descendants"][0].__setitem__("sha256", "0" * 64))
    failures = []
    for label, value in mutations:
        if not semantic_errors(value, check_files=(label == "descendant digest")):
            failures.append(f"negative control accepted: {label}")
    return failures


def main() -> None:
    required = [RESULT, MANIFEST, RESULT_SCHEMA, MANIFEST_SCHEMA, BUILDER, REPORT]
    missing = [path.relative_to(ROOT).as_posix() for path in required if not path.is_file()]
    if missing:
        raise SystemExit("Missing QCSA vertical artifacts: " + ", ".join(missing))
    base = {"result": load(RESULT), "manifest": load(MANIFEST), "report": REPORT.read_text(encoding="utf-8")}
    errors = semantic_errors(base, check_files=True)
    errors.extend(negative_controls(base))
    before = (RESULT.read_bytes(), MANIFEST.read_bytes())
    for _ in range(2):
        subprocess.run([sys.executable, str(BUILDER)], cwd=ROOT, check=True, capture_output=True, text=True)
        if (RESULT.read_bytes(), MANIFEST.read_bytes()) != before:
            errors.append("vertical builder replay is not byte-identical")
            break
    if errors:
        raise SystemExit("QCSA vertical reference validation failed:\n - " + "\n - ".join(errors))
    print("QCSA governed vertical reference passed: 13 ordered stages, stable SOID/plural address/evidence separation, one separately authorized and independently observed temp-file effect, complete receipt graph, same-identity migration, byte-exact effect-complete rollback, 10 fail-closed adversarial paths, eight open residuals, two byte-identical replays, and 15 rejecting mutations; no support-state or chapter effect.")


if __name__ == "__main__":
    main()
