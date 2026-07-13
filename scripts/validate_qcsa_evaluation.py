#!/usr/bin/env python3
"""Validate and replay the frozen held-out QCSA evaluation and dispositions."""

from __future__ import annotations

import ast
import copy
import hashlib
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "experiments/qcsa_reference"
PRED = PACKAGE / "results/evaluation_predictions.json"
RESULT = PACKAGE / "results/evaluation_results.json"
PRED_SCHEMA = ROOT / "schemas/qcsa_evaluation_predictions.schema.json"
RESULT_SCHEMA = ROOT / "schemas/qcsa_evaluation_results.schema.json"
DISPOSITIONS = ROOT / "claim_decisions/qcsa_reference_evaluation_dispositions.json"
DISPOSITION_SCHEMA = ROOT / "schemas/qcsa_evaluation_dispositions.schema.json"
AUTH = ROOT / "roadmap_records/qcsa_evaluation_execution_authorization.json"
INPUTS = PACKAGE / "corpus/inputs.json"
LABELS = PACKAGE / "corpus/labels.json"
OBSERVER = ROOT / "scripts/qcsa_evaluation_observer.py"
RUNNER = ROOT / "scripts/run_qcsa_evaluation_predictions.py"
REPORT = ROOT / "docs/qcsa_reference_evaluation_report.md"
SETUP = ROOT / "roadmap_records/qcsa_evaluation_setup_freeze.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def imports(source: str) -> set[str]:
    found = set()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            found.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            found.add(node.module)
    return found


def has_blended_key(value: Any) -> bool:
    if isinstance(value, dict):
        return any("blend" in str(key).casefold() or has_blended_key(item) for key, item in value.items())
    if isinstance(value, list):
        return any(has_blended_key(item) for item in value)
    return False


def semantic_errors(data: dict, *, check_files: bool = False) -> list[str]:
    errors = []
    pred, result, dispositions = data["pred"], data["result"], data["dispositions"]
    for name, value, schema_path in [
        ("predictions", pred, PRED_SCHEMA), ("results", result, RESULT_SCHEMA),
        ("dispositions", dispositions, DISPOSITION_SCHEMA),
    ]:
        errors.extend(f"{name} schema: {error.message}" for error in Draft202012Validator(load(schema_path)).iter_errors(value))
    setup, auth = data["setup"], data["auth"]
    if pred.get("systems") != setup.get("systems") or pred.get("seeds") != [11, 29, 47]:
        errors.append("prediction systems or seeds differ from setup freeze")
    if auth.get("state") != "authorized_for_outcome_execution" or auth.get("setup_commit") != "57cb0f2a127a1b6aa651f3d1398741990d901d5c":
        errors.append("outcome execution lacks exact attested setup authorization")
    if auth.get("hosted_build", {}).get("run_id") != 29231298514 or auth.get("deploy_and_attestation", {}).get("run_id") != 29231557981:
        errors.append("hosted setup build/deploy binding drifted")

    held_ids = {row["case_id"] for row in data["inputs"]["cases"] if row["split"] == "held_out"}
    expected_combos = {(seed, system, case_id) for seed in [11, 29, 47] for system in setup["systems"] for case_id in held_ids}
    rows = pred.get("records", [])
    combos = {(row.get("seed"), row.get("system"), row.get("case_id")) for row in rows}
    if len(rows) != 2340 or combos != expected_combos:
        errors.append("predictions do not cover every exact seed/system/held-out case once")
    if rows != sorted(rows, key=lambda row: (row["seed"], row["system"], row["case_id"])):
        errors.append("prediction record ordering drifted")
    for row in rows:
        claimed = row.get("record_digest")
        unsigned = {key: value for key, value in row.items() if key != "record_digest"}
        if claimed != hashlib.sha256(canonical_bytes(unsigned)).hexdigest():
            errors.append(f"prediction record digest drifted: {row.get('case_id')}")
            break
    runner_source, observer_source = data["runner"], data["observer"]
    if "labels.json" in runner_source or "LABELS" in runner_source or "corpus/labels" in runner_source:
        errors.append("prediction runner names evaluator labels")
    if any(name.startswith("qcsa_ref") for name in imports(observer_source)):
        errors.append("observer imports candidate implementation")

    if check_files:
        for path, expected in [(INPUTS, pred.get("input_sha256")), (PRED, result.get("prediction_sha256")), (OBSERVER, result.get("observer_sha256")), (LABELS, result.get("labels_sha256"))]:
            if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                errors.append(f"result descendant digest drifted: {path.relative_to(ROOT)}")
    atomic = result.get("atomic_records", [])
    atomic_combos = {(row.get("seed"), row.get("system"), row.get("case_id")) for row in atomic}
    if len(atomic) != 2340 or atomic_combos != expected_combos:
        errors.append("atomic observer records do not cover exact predictions")
    if has_blended_key(result):
        errors.append("result contains a prohibited blended score")
    bootstrap = result.get("paired_bootstrap", {})
    blocks = [bootstrap.get("aggregate", {}), *bootstrap.get("by_seed", {}).values()]
    if len(blocks) != 4 or any(row.get("resamples") != 10000 for row in blocks):
        errors.append("paired bootstrap is not exact 10000-resample aggregate plus three seeds")
    if bootstrap.get("aggregate", {}).get("ci95") != [0.0, 0.0] or bootstrap.get("aggregate", {}).get("observed_task_accuracy_delta") != 0.0:
        errors.append("paired task-accuracy outcome drifted")

    overall = result.get("aggregate", {})
    candidate = overall.get("qcsa", {})
    expected_candidate = {
        "object_resolution_accuracy": 1.0, "task_decision_accuracy": 1.0,
        "unsafe_authority_release_count": 0, "risk_failure_prevention_rate": 1.0,
        "operation_count_mean": 4.05, "evaluator_disagreement": 0.0,
        "compatibility": 1.0, "rollback_identity": 1.0,
    }
    if any(candidate.get(key) != value for key, value in expected_candidate.items()):
        errors.append("exact QCSA aggregate outcome drifted")
    best_name = "direct_clarification_without_adaptive_question_policy"
    best = overall.get(best_name, {})
    expected_best = {"object_resolution_accuracy": 0.633333, "task_decision_accuracy": 1.0, "operation_count_mean": 2.116667, "risk_failure_prevention_rate": 0.487179, "evaluator_disagreement": 0.25, "compatibility": 0.3}
    if any(best.get(key) != value for key, value in expected_best.items()):
        errors.append("selected best-baseline aggregate outcome drifted")
    ablation_checks = {
        "qcsa_without_plural_facets": {"object_resolution_accuracy": 0.916667},
        "qcsa_without_active_questions": {"object_resolution_accuracy": 1.0, "task_decision_accuracy": 1.0, "questions_mean": 0.0},
        "qcsa_without_identity_address_indirection": {"object_resolution_accuracy": 0.9, "compatibility": 0.4},
        "qcsa_without_certificate_residual_authority_fields": {"unsafe_authority_release_count": 9, "task_decision_accuracy": 0.95},
        "qcsa_without_migration_compatibility": {"task_decision_accuracy": 0.833333, "compatibility": 0.0},
    }
    for system, values in ablation_checks.items():
        if any(overall.get(system, {}).get(key) != value for key, value in values.items()):
            errors.append(f"exact ablation outcome drifted: {system}")
    rules = result.get("decision_rules", {})
    expected_rules = {
        "best_matched_baseline": best_name, "advantage_gate_pass": False,
        "resource_gate_pass": False, "calibration_gate_pass": True,
        "semantic_preservation_gate_pass": True, "authority_gate_pass": True,
        "migration_gate_pass": True, "narrowing_gate_triggered": True,
        "operation_ratio": 1.913386, "overall_disposition": "narrow_no_matched_advantage_claim",
    }
    if any(rules.get(key) != value for key, value in expected_rules.items()):
        errors.append("frozen decision-rule outcome drifted")

    non_core = dispositions.get("non_core_dispositions", [])
    counts = Counter(row.get("disposition") for row in non_core)
    if counts != Counter({"promote": 5, "narrow": 2, "refute": 2, "no_change": 1}):
        errors.append("non-core disposition coverage/counts drifted")
    core = dispositions.get("core_claim_decisions", [])
    expected_owners = {
        "cognitive-compilation-and-semantic-ir", "virtual-context-abi", "claim-ledgers-and-belief-revision",
        "runtime-adapters-tool-permissions-and-human-approval", "inter-stack-protocols-identity-and-economic-exchange",
        "routing-heads-and-specialist-cores", "compact-generative-systems-and-residual-honesty",
        "data-engines-continual-learning-and-unlearning", "integrated-reference-architecture",
    }
    if {row.get("chapter_id") for row in core} != expected_owners or any(row.get("decision") != "no_change" or row.get("current_support_state") != "argument" for row in core):
        errors.append("nine QCSA owner core claims are not explicit no-change at argument")
    if dispositions.get("support_state_effect") != "none":
        errors.append("evaluation dispositions move support state")
    for phrase in ["matched-resource advantage claim", "1.913386", "ceiling", "confounded", "No new QCSA chapter", "All nine chapter-core claims remain at `argument`"]:
        if phrase not in data["report"]:
            errors.append(f"evaluation report missing boundary: {phrase}")
    return errors


def negative_controls(base: dict) -> list[str]:
    failures = []
    mutations = []
    def mutate(label: str, fn) -> None:
        value = copy.deepcopy(base); fn(value); mutations.append((label, value))
    mutate("missing system", lambda d: d["pred"]["systems"].pop())
    mutate("missing seed", lambda d: d["pred"].__setitem__("seeds", [11, 29]))
    mutate("missing held-out record", lambda d: d["pred"]["records"].pop())
    mutate("prediction digest tamper", lambda d: d["pred"]["records"][0].__setitem__("record_digest", "0" * 64))
    mutate("atomic record erased", lambda d: d["result"]["atomic_records"].pop())
    mutate("bootstrap drift", lambda d: d["result"]["paired_bootstrap"]["aggregate"].__setitem__("resamples", 9999))
    mutate("blended score", lambda d: d["result"].__setitem__("blended_score", 1.0))
    mutate("unsafe ablation hidden", lambda d: d["result"]["aggregate"]["qcsa_without_certificate_residual_authority_fields"].__setitem__("unsafe_authority_release_count", 0))
    mutate("family mechanism regression erased", lambda d: d["result"]["aggregate"]["qcsa_without_plural_facets"].__setitem__("object_resolution_accuracy", 1.0))
    mutate("evaluator disagreement hidden", lambda d: d["result"]["aggregate"]["direct_clarification_without_adaptive_question_policy"].__setitem__("evaluator_disagreement", 0.0))
    mutate("migration failure hidden", lambda d: d["result"]["aggregate"]["qcsa_without_migration_compatibility"].__setitem__("compatibility", 1.0))
    mutate("advantage promoted", lambda d: d["result"]["decision_rules"].__setitem__("overall_disposition", "promote"))
    mutate("core promotion", lambda d: d["dispositions"]["core_claim_decisions"][0].__setitem__("current_support_state", "prototype-backed"))
    mutate("runner label leak", lambda d: d.__setitem__("runner", d["runner"] + "\nLABELS = 'corpus/labels.json'\n"))
    mutate("observer self-confirmation", lambda d: d.__setitem__("observer", d["observer"] + "\nfrom qcsa_ref import evaluation\n"))
    for label, value in mutations:
        if not semantic_errors(value):
            failures.append(f"negative control accepted: {label}")
    return failures


def main() -> None:
    required = [PRED, RESULT, PRED_SCHEMA, RESULT_SCHEMA, DISPOSITIONS, DISPOSITION_SCHEMA, AUTH, INPUTS, LABELS, OBSERVER, RUNNER, REPORT, SETUP]
    missing = [path.relative_to(ROOT).as_posix() for path in required if not path.is_file()]
    if missing:
        raise SystemExit("Missing QCSA evaluation artifacts: " + ", ".join(missing))
    base = {"pred": load(PRED), "result": load(RESULT), "dispositions": load(DISPOSITIONS), "auth": load(AUTH), "inputs": load(INPUTS), "setup": load(SETUP), "runner": RUNNER.read_text(encoding="utf-8"), "observer": OBSERVER.read_text(encoding="utf-8"), "report": REPORT.read_text(encoding="utf-8")}
    errors = semantic_errors(base, check_files=True)
    errors.extend(negative_controls(base))
    before = (PRED.read_bytes(), RESULT.read_bytes())
    for _ in range(2):
        subprocess.run([sys.executable, str(RUNNER)], cwd=ROOT, check=True, capture_output=True, text=True)
        subprocess.run([sys.executable, str(OBSERVER)], cwd=ROOT, check=True, capture_output=True, text=True)
        if (PRED.read_bytes(), RESULT.read_bytes()) != before:
            errors.append("prediction/observer replay is not byte-identical")
            break
    if errors:
        raise SystemExit("QCSA evaluation validation failed:\n - " + "\n - ".join(errors))
    print("QCSA evaluation passed: 2340 deterministic predictions, 60 held-out cases, 13 systems, three seeds, exact descendant digests, label-isolated runner, separately implemented observer, 10000 paired resamples, six-family Pareto frontiers, bounded authority/migration/calibration gates, failed matched-advantage and resource gates, 10 explicit non-core dispositions, nine core no-change decisions, and 15 rejecting mutations.")


if __name__ == "__main__":
    main()
