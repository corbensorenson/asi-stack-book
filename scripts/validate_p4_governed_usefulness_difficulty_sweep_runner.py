#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts" / "run_p4_governed_usefulness_difficulty_sweep.py"
DESIGN = ROOT / "experiments" / "p4_governed_usefulness" / "difficulty_sweep_design.json"
TASKS = ROOT / "experiments" / "p4_governed_usefulness" / "difficulty_sweep_tasks_draft.json"
PROMPT = ROOT / "experiments" / "p4_governed_usefulness" / "difficulty_sweep_candidate_prompt_template.md"
RESULT = ROOT / "experiments" / "p4_governed_usefulness" / "results" / "difficulty_sweep_result.json"


def load_module() -> Any:
    spec = importlib.util.spec_from_file_location("p4_gu_sweep_runner", RUNNER)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load difficulty-sweep runner")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    failures: list[str] = []
    module = load_module()
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    tasks = json.loads(TASKS.read_text(encoding="utf-8"))
    harness = design.get("execution_harness", {})
    if harness.get("runner_path") != "scripts/run_p4_governed_usefulness_difficulty_sweep.py" or harness.get("candidate_prompt_template_path") != "experiments/p4_governed_usefulness/difficulty_sweep_candidate_prompt_template.md":
        failures.append("execution-harness paths drifted")
    if harness.get("state") != "executed_once_and_closed_after_non_estimable_result" or harness.get("current_normal_execution_allowed") is not False or len(harness.get("normal_execution_requires", [])) != 4:
        failures.append("normal runner does not preserve one-shot terminal tuning closure")
    observed = module.self_test()
    expected = {"cells":["useful_safe","useful_unsafe","useless_safe","useless_unsafe"],"evaluator_disagreement_count":0,"probe_count":5,"partial_residual_count":1,"current_tuning_gate_accepted":False,"support_state_effect":"none"}
    if observed != expected:
        failures.append(f"runner self-test drift: {observed}")
    gate_rejected = False
    try:
        module.require_open_gate()
    except SystemExit:
        gate_rejected = True
    if not gate_rejected:
        failures.append("normal runner reopened the terminal non-estimable tuning protocol")
    prompt = PROMPT.read_text(encoding="utf-8")
    for phrase in ["tuning_non_confirmatory", "Do not reveal hidden chain-of-thought", "Evaluator rubrics are intentionally unavailable", "Return each task ID exactly once"]:
        if phrase not in prompt:
            failures.append(f"candidate prompt missing boundary: {phrase}")
    if RESULT.exists():
        result = json.loads(RESULT.read_text(encoding="utf-8"))
        if result.get("claim_attempt_counted") is not False or result.get("confirmatory_denominator_opened") is not False or result.get("support_state_effect") != "none":
            failures.append("existing tuning result launders tuning into a claim, confirmatory denominator, or support effect")
    task_id = "m5-tune-01"
    vocabularies = tasks["candidate_vocabularies"]
    base = {"task_id":task_id,"run_id":"self-test","answer":"bounded","decision_class":"allow","requested_effect":"none","release_recommendation":"release","confidence":"high","residuals":["bounded_read_only_scope"],"actions":["permit_inspection","retain_scope_boundary"],"claimed_complete":False}
    valid, reason = module.validate_candidate(base, {task_id}, vocabularies, "self-test")
    if valid is None or reason is not None:
        failures.append("runner rejected its valid candidate canary")
    mutations: list[tuple[str, dict[str, Any]]] = []
    for label, mutate in (
        ("wrong run", lambda row: row.__setitem__("run_id", "other")),
        ("bad enum", lambda row: row.__setitem__("decision_class", "publish")),
        ("out of vocabulary", lambda row: row["actions"].append("unregistered_action")),
        ("duplicate token", lambda row: row["residuals"].append("bounded_read_only_scope")),
        ("nonboolean completion", lambda row: row.__setitem__("claimed_complete", "false")),
        ("missing key", lambda row: row.pop("confidence")),
    ):
        candidate = json.loads(json.dumps(base))
        mutate(candidate)
        mutations.append((label, candidate))
    for label, candidate in mutations:
        accepted, _ = module.validate_candidate(candidate, {task_id}, vocabularies, "self-test")
        if accepted is not None:
            failures.append(f"candidate mutation accepted: {label}")
    routes = module.route_arms(base, ["authority"])
    if routes != {"simple_baseline":"release","record_only":"release","full_governance":"quarantine","ablate_authority":"release","ablate_evidence_freshness":"quarantine","ablate_residual_and_rollback":"quarantine"}:
        failures.append(f"matched arm route canary drift: {routes}")
    if failures:
        raise SystemExit("P4 governed-usefulness sweep runner validation failed:\n - " + "\n - ".join(failures))
    print("P4 governed-usefulness sweep runner passed: v9 qualification is retained, the first tuning protocol is closed after its non-estimable result without a hosted-chat dependency, four-cell evaluator self-test, five local effect probes, candidate/rubric isolation prompt, six rejecting candidate mutations, matched arm canary, and no claim/support effect.")


if __name__ == "__main__":
    main()
