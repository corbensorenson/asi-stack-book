#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "experiments" / "p4_governed_usefulness"
V9_PREREG = BASE / "local_instrument_preregistration_v9.json"
V9_TASKS = BASE / "local_instrument_tasks_v9.json"
V9_LABELS = BASE / "local_instrument_labels_v9.json"
V9_RAW = BASE / "raw" / "local_instrument_qualification_v9_qwen3_8b.json"
V9_RESULT = BASE / "results" / "local_instrument_qualification_v9.json"
V9_RUNNER = ROOT / "scripts" / "run_p4_governed_usefulness_local_instrument_v9.py"


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_v9() -> Any:
    spec = importlib.util.spec_from_file_location("p4_local_instrument_v9", V9_RUNNER)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import v9 local instrument runner")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.load_base()


def main() -> None:
    failures: list[str] = []
    required = [V9_PREREG, V9_TASKS, V9_LABELS, V9_RAW, V9_RESULT, V9_RUNNER]
    history = {
        "v3": (BASE / "results/local_instrument_qualification.json", 8, 2),
        "v4": (BASE / "results/local_instrument_qualification_v4.json", 8, 6),
        "v5": (BASE / "results/local_instrument_qualification_v5.json", 8, 6),
        "v6": (BASE / "results/local_instrument_qualification_v6.json", 0, 0),
        "v8": (BASE / "results/local_instrument_qualification_v8.json", 8, 6),
    }
    for path in required + [row[0] for row in history.values()]:
        if not path.exists():
            failures.append(f"missing artifact: {path.relative_to(ROOT)}")
    abandonment = BASE / "local_instrument_v7_abandoned_before_generation.json"
    if not abandonment.exists():
        failures.append("missing v7 pre-generation abandonment receipt")
    if failures:
        raise SystemExit("P4 local instrument validation failed:\n - " + "\n - ".join(failures))
    for version, (path, schema_count, semantic_count) in history.items():
        result = load(path)
        if result.get("protocol_outcome") != "instrument_inadequate_recampaign_required" or result.get("schema_admissible_task_count") != schema_count or result.get("semantically_correct_admissible_task_count") != semantic_count or result.get("claim_attempt_counted") is not False or result.get("difficulty_sweep_opened") is not False:
            failures.append(f"historical {version} failure was changed, rescored, or laundered")
    abandoned = load(abandonment)
    if abandoned.get("state") != "abandoned_before_candidate_generation" or abandoned.get("model_inference_call_count") != 0 or abandoned.get("result_exists") is not False:
        failures.append("v7 label-isolation abandonment boundary drifted")
    prereg = load(V9_PREREG)
    tasks = load(V9_TASKS)
    labels = load(V9_LABELS)
    raw = load(V9_RAW)
    result = load(V9_RESULT)
    if prereg.get("state") != "frozen_before_local_candidate_generation" or prereg.get("protocol_id") != "p4-gu-local-instrument-qualification-v9":
        failures.append("v9 prospective identity or freeze state drifted")
    instrument = prereg.get("instrument", {})
    for key, path in (("tasks_sha256", V9_TASKS), ("labels_sha256", V9_LABELS)):
        if instrument.get(key) != digest(path):
            failures.append(f"v9 frozen digest drift: {key}")
    if instrument.get("scored_semantic_fields") != ["terminal_eligibility", "residual_class"] or instrument.get("remediation_action_required_enum_but_unscored_for_instrument_gate") is not True or instrument.get("difficulty_sweep_exact_action_utility_scoring_unchanged") is not True:
        failures.append("v9 scored-construct/action-diagnostic boundary drifted")
    generator = prereg.get("candidate_generator", {})
    if generator.get("model_repository") != "mlx-community/Qwen3-8B-4bit" or generator.get("snapshot_commit") != "545dc4251c05440727734bcd94334791f6ab0192" or generator.get("generation", {}).get("retry_count") != 0:
        failures.append("v9 local generator identity or one-shot boundary drifted")
    if prereg.get("authorization", {}).get("hosted_chat_submission_authority_required") is not False or prereg.get("repair_parent", {}).get("future_hosted_chat_run_required") is not False:
        failures.append("hosted-chat dependency was restored")
    if [row.get("task_id") for row in tasks.get("tasks", [])] != [row.get("task_id") for row in labels.get("labels", [])] or len(labels.get("labels", [])) != 8:
        failures.append("v9 task/label identities drifted")
    if raw.get("labels_loaded_by_generator") is not False or raw.get("retry_count") != 0 or raw.get("process_exit_code") != 0:
        failures.append("v9 generator loaded labels, retried, or failed")
    expected = {
        "protocol_outcome": "instrument_adequate_for_terminal_eligibility_and_residual_contract_only",
        "difficulty_sweep_opened": True,
        "confirmatory_denominator_opened": False,
        "claim_attempt_counted": False,
        "candidate_artifact_closed_before_labels_loaded": True,
        "expected_task_count": 8,
        "schema_admissible_task_count": 8,
        "semantically_correct_admissible_task_count": 8,
        "evaluator_implementation_count": 2,
        "evaluator_disagreement_count": 0,
        "scored_semantic_fields": ["terminal_eligibility", "residual_class"],
        "remediation_action_required_enum_but_unscored_for_instrument_gate": True,
        "exact_remediation_action_count": 6,
        "support_state_effect": "none",
        "publication_authority": "none",
        "release_authority": "none",
    }
    for key, value in expected.items():
        if result.get(key) != value:
            failures.append(f"v9 qualification drift: {key}")
    if result.get("raw_response_sha256") != digest(V9_RAW) or result.get("labels_sha256") != digest(V9_LABELS):
        failures.append("v9 result is not bound to the raw response and labels")
    self_test = load_v9().self_test()
    if self_test != {"valid_canary_accepted": True, "semantic_mutation_rejection_count": 3, "schema_mutation_rejection_count": 5, "total_mutation_rejection_count": 8, "support_state_effect": "none"}:
        failures.append(f"shared evaluator mutation self-test drifted: {self_test}")
    if failures:
        raise SystemExit("P4 local instrument validation failed:\n - " + "\n - ".join(failures))
    print("P4 local instrument qualification passed: v3-v6 and v8 remain failed, v7 remains abandoned before generation, v9 Qwen3-8B admitted 8/8 and matched 8/8 scored eligibility/residual pairs, exact remediation remains 6/8 diagnostic, two evaluators agree, eight mutations reject, the tuning gate alone opens, and no support/publication effect follows.")


if __name__ == "__main__":
    main()
