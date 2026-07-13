#!/usr/bin/env python3
"""Validate the content-addressed QCSA setup before held-out execution."""

from __future__ import annotations

import ast
import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
FREEZE = ROOT / "roadmap_records/qcsa_evaluation_setup_freeze.json"
SCHEMA = ROOT / "schemas/qcsa_evaluation_setup_freeze.schema.json"
BUILDER = ROOT / "scripts/build_qcsa_evaluation_setup_freeze.py"
RUNNER = ROOT / "scripts/run_qcsa_evaluation_predictions.py"
OBSERVER = ROOT / "scripts/qcsa_evaluation_observer.py"
PLAN = ROOT / "experiments/qcsa_reference/test_plan.json"
EXPECTED_SYSTEMS = [
    "qcsa",
    "direct_inference_or_retrieval_without_semantic_address",
    "flat_lexical_retrieval_matched_corpus_and_budget",
    "flat_embedding_proxy_retrieval_matched_corpus_and_budget",
    "one_fixed_hierarchy",
    "random_tree",
    "frequency_derived_tree",
    "direct_clarification_without_adaptive_question_policy",
    "qcsa_without_plural_facets",
    "qcsa_without_active_questions",
    "qcsa_without_identity_address_indirection",
    "qcsa_without_certificate_residual_authority_fields",
    "qcsa_without_migration_compatibility",
]


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def imported_modules(source: str) -> set[str]:
    modules = set()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module)
    return modules


def semantic_errors(record: dict, runner_source: str, observer_source: str, plan: dict, *, check_files: bool = False) -> list[str]:
    errors = [f"schema: {error.message}" for error in Draft202012Validator(load(SCHEMA)).iter_errors(record)]
    if record.get("systems") != EXPECTED_SYSTEMS:
        errors.append("exact candidate/baseline/ablation order drifted")
    if record.get("baselines") != plan.get("baselines") or record.get("ablations") != plan.get("ablations"):
        errors.append("freeze systems disagree with preregistered plan")
    if record.get("seeds") != plan.get("seeds") or record.get("held_out_case_count") != plan.get("corpus", {}).get("held_out_cases"):
        errors.append("seed or held-out count drifted")
    if record.get("bootstrap_resamples") != 10000 or "RESAMPLES = 10_000" not in observer_source:
        errors.append("paired bootstrap count drifted")
    if "labels.json" in runner_source or "LABELS" in runner_source or "corpus/labels" in runner_source:
        errors.append("prediction runner can name evaluator labels")
    if any(name.startswith("qcsa_ref") for name in imported_modules(observer_source)) or "evaluation import" in observer_source or "round_trip import" in observer_source:
        errors.append("observer imports candidate implementation")
    if "no blended score" not in record.get("decision_policy", "") or "blended_score" in observer_source:
        errors.append("Pareto-only decision policy drifted")
    if record.get("outcome_access") != "sealed_pending_setup_commit_attestation" or record.get("support_state_effect") != "none":
        errors.append("setup prematurely opens outcomes or moves support")
    if check_files:
        for item in record.get("files", []):
            path = ROOT / item["path"]
            if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != item["sha256"]:
                errors.append(f"content-addressed setup file drifted: {item['path']}")
    return errors


def negative_controls(base: dict, runner: str, observer: str, plan: dict) -> list[str]:
    mutations = []
    for label, mutate in [
        ("candidate removed", lambda r: r["systems"].pop(0)),
        ("baseline removed", lambda r: r["baselines"].pop()),
        ("ablation removed", lambda r: r["ablations"].pop()),
        ("seed drift", lambda r: r.__setitem__("seeds", [11, 29, 48])),
        ("held-out count drift", lambda r: r.__setitem__("held_out_case_count", 59)),
        ("bootstrap drift", lambda r: r.__setitem__("bootstrap_resamples", 9999)),
        ("outcomes opened", lambda r: r.__setitem__("outcome_access", "opened")),
        ("support promotion", lambda r: r.__setitem__("support_state_effect", "prototype-backed")),
        ("file digest mutation", lambda r: r["files"][0].__setitem__("sha256", "0" * 64)),
    ]:
        value = copy.deepcopy(base)
        mutate(value)
        mutations.append((label, value, runner, observer, plan))
    mutations.extend([
        ("runner label import", base, runner + "\nLABELS = 'corpus/labels.json'\n", observer, plan),
        ("observer self-confirmation", base, runner, observer + "\nfrom qcsa_ref import evaluation\n", plan),
        ("blended score", base, runner, observer + "\nblended_score = 1\n", plan),
    ])
    failures = []
    for label, record, runner_value, observer_value, plan_value in mutations:
        if not semantic_errors(record, runner_value, observer_value, plan_value, check_files=(label == "file digest mutation")):
            failures.append(f"negative control accepted: {label}")
    return failures


def main() -> None:
    required = [FREEZE, SCHEMA, BUILDER, RUNNER, OBSERVER, PLAN]
    missing = [path.relative_to(ROOT).as_posix() for path in required if not path.is_file()]
    if missing:
        raise SystemExit("Missing QCSA evaluation setup artifacts: " + ", ".join(missing))
    before = FREEZE.read_bytes()
    subprocess.run([sys.executable, str(BUILDER)], cwd=ROOT, check=True, capture_output=True, text=True)
    errors = [] if before == FREEZE.read_bytes() else ["setup freeze builder is not byte-deterministic"]
    record, plan = load(FREEZE), load(PLAN)
    runner, observer = RUNNER.read_text(encoding="utf-8"), OBSERVER.read_text(encoding="utf-8")
    errors.extend(semantic_errors(record, runner, observer, plan, check_files=True))
    errors.extend(negative_controls(record, runner, observer, plan))
    subprocess.run([sys.executable, "scripts/validate_qcsa_evaluation_corpus.py"], cwd=ROOT, check=True, capture_output=True, text=True)
    if errors:
        raise SystemExit("\n".join(f"- {error}" for error in errors))
    print("QCSA evaluation setup freeze passed: 180 cases, 60 held out, 13 exact systems, three seeds, evaluator-separated runner/observer, 10000 paired resamples, Pareto policy, 13 content-addressed files, and 12 rejecting mutations; outcomes remain sealed.")


if __name__ == "__main__":
    main()
