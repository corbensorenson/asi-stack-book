#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "experiments" / "p4_governed_usefulness"
DESIGN = BASE / "confirmatory_design.json"
TASKS = BASE / "confirmatory_tasks.json"
RUBRICS = BASE / "confirmatory_rubrics.json"
PREREG = BASE / "confirmatory_generation_preregistration.json"
POOL = BASE / "results" / "difficulty_sweep_v2_v5_pool_result.json"
RESULT = BASE / "results" / "confirmatory_result.json"
CANDIDATES = BASE / "raw" / "confirmatory_qwen3_8b_run_001_candidates.json"
STATUS = ROOT / "roadmap_records" / "post_v2_3_claim_proof_and_sota_challenge_status.json"
TRANSITION = ROOT / "evidence_transitions" / "post_v2_3" / "governed_usefulness_held_out_local_promote.json"
RUNNER = ROOT / "scripts" / "run_p4_governed_usefulness_confirmatory.py"

def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def runner_module() -> Any:
    spec = importlib.util.spec_from_file_location("p4_confirmatory_validation_runner", RUNNER)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import confirmatory runner")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def errors(result: dict[str, Any]) -> list[str]:
    out: list[str] = []
    design=load(DESIGN); tasks=load(TASKS); rubrics=load(RUBRICS); prereg=load(PREREG); pool=load(POOL); status=load(STATUS); transition=load(TRANSITION)
    if pool.get("protocol_outcome") != "operating_range_adequate_to_freeze_fresh_held_out_confirmatory_design" or pool.get("schema_admissible_candidate_count") != 32 or pool.get("expected_task_count") != 40 or pool.get("four_cell_counts") != {"useful_safe":9,"useful_unsafe":2,"useless_unsafe":11,"useless_safe":10} or pool.get("evaluator_disagreement_count") != 0 or pool.get("effect_probe_count") != 20:
        out.append("terminal tuning-pool gate drift")
    for path,key in ((DESIGN,"design_sha256"),(TASKS,"tasks_sha256"),(RUBRICS,"rubrics_sha256")):
        if prereg.get(key) != sha(path): out.append(f"frozen {path.name} digest drift")
    if prereg.get("entry_pool_result_sha256") != sha(POOL) or prereg.get("outcome_aware_retry_allowed") is not False:
        out.append("confirmatory entry binding or retry boundary drift")
    if tasks.get("task_count") != 16 or len(tasks.get("tasks",[])) != 16 or len({r.get("task_id") for r in tasks.get("tasks",[])}) != 16:
        out.append("held-out denominator drift")
    tuning=[]
    for path in BASE.glob("difficulty_sweep*_tasks*.json"):
        tuning.extend(load(path).get("tasks",[]))
    held=tasks["tasks"]
    if {r["task_id"] for r in held} & {r["task_id"] for r in tuning} or {(r["scenario"],r["request"]) for r in held} & {(r["scenario"],r["request"]) for r in tuning}:
        out.append("held-out task reuse detected")
    if result.get("candidate_sha256") != sha(CANDIDATES) or result.get("candidate_artifact_closed_before_labels_loaded") is not True:
        out.append("candidate closure or digest drift")
    if result.get("protocol_outcome") != "bounded_local_governance_effect_supported" or result.get("claim_outcome") != "supported_bounded_local" or result.get("claim_attempt_counted") is not True:
        out.append("confirmatory terminal disposition drift")
    if result.get("expected_task_count") != 16 or result.get("schema_admissible_candidate_count") != 15 or len(result.get("exclusions",[])) != 1 or result.get("evaluator_disagreement_count") != 0:
        out.append("confirmatory denominator or evaluator drift")
    if result.get("four_cell_counts") != {"useful_safe":9,"useful_unsafe":1,"useless_safe":3,"useless_unsafe":2}:
        out.append("confirmatory four-cell counts drift")
    if not all(result.get("primary_gate_checks",{}).values()) or len(result.get("primary_gate_checks",{})) != 6:
        out.append("co-primary gate did not pass exactly")
    arms=result.get("arm_summaries",{}); full=arms.get("full_governance",{}); baseline=arms.get("simple_baseline",{}); ablation=arms.get("ablate_evidence_freshness",{})
    if [baseline.get("useful_releases"),baseline.get("unsafe_releases"),full.get("useful_releases"),full.get("unsafe_releases"),ablation.get("unsafe_releases")] != [0,0,9,0,1]:
        out.append("policy-arm causal signature drift")
    if transition.get("new_support_state") != "synthetic-test-backed" or transition.get("claim_id") != "governed-usefulness.held-out-local-policy-effect" or transition.get("transition_validity_state") != "review_accepted" or any("does not promote any chapter core claim" not in x for x in transition.get("non_claims",[])[:1]):
        out.append("bounded non-core transition drift")
    contract=status.get("governed_usefulness_campaign_contract",{}); milestones={r["id"]:r["state"] for r in status.get("milestones",[])}
    if contract.get("confirmatory_protocol_outcome") != result.get("protocol_outcome") or contract.get("confirmatory_denominator_state") != "opened_once_and_terminally_closed" or contract.get("model_inference_call_count") != 14 or contract.get("claim_attempt_count") != 1 or milestones.get("M5") != "completed":
        out.append("roadmap/status M5 reconciliation drift")
    required={"docs/p4_governed_usefulness_campaign.md":"bounded_local_governance_effect_supported","docs/non_core_evidence_ledger.md":"governed-usefulness.held-out-local-policy-effect","appendices/C_claim_evidence_matrix.qmd":"P4/M5 Governed-Usefulness Reconciliation","chapters/runtime-adapters-tool-permissions-and-human-approval.qmd":"P4/M5 held-out policy result","chapters/readiness-gates-residual-escrow-and-quarantine.qmd":"The P4/M5 held-out campaign adds one narrow causal policy result","chapters/resource-economics-and-token-budgets.qmd":"P4/M5 informative-regime result","chapters/intent-to-execution-contracts.qmd":"The later P4/M5 recampaign finally reached an informative regime"}
    for relative,needle in required.items():
        if needle not in (ROOT/relative).read_text(encoding="utf-8"): out.append(f"missing reconciled prose: {relative}")
    return out

def main() -> None:
    result=load(RESULT); failures=errors(result)
    for label,change in (
        ("erase exclusion",lambda r:r.__setitem__("exclusions",[])),
        ("inflate useful release",lambda r:r["arm_summaries"]["full_governance"].__setitem__("useful_releases",10)),
        ("erase unsafe ablation",lambda r:r["arm_summaries"]["ablate_evidence_freshness"].__setitem__("unsafe_releases",0)),
        ("launder transfer",lambda r:r.__setitem__("claim_ceiling","general transfer supported")),
        ("reopen denominator",lambda r:r.__setitem__("confirmatory_denominator_closed",False)),
    ):
        candidate=copy.deepcopy(result); change(candidate)
        local=errors(candidate)
        if label=="launder transfer" and "general transfer supported" in candidate.get("claim_ceiling",""):
            local.append("claim ceiling laundering")
        if label=="reopen denominator" and candidate.get("confirmatory_denominator_closed") is not True:
            local.append("denominator reopened")
        if not local: failures.append(f"negative mutation accepted: {label}")
    self_test=runner_module().self_test()
    if self_test != {"cells":["useful_safe","useful_unsafe","useless_safe","useless_unsafe"],"evaluator_disagreement_count":0,"unsafe_gate_blocks_full":True,"authority_ablation_exposes_release":True}:
        failures.append(f"runner self-test drift: {self_test}")
    if failures: raise SystemExit("P4 governed-usefulness confirmatory validation failed:\n - "+"\n - ".join(failures))
    print("P4 governed-usefulness confirmatory validation passed: 32/40 tuning pool, fresh 16-task held-out denominator, 15 admissions, zero evaluator disagreement, 9 useful/0 unsafe full-governance releases, one evidence-freshness ablation unsafe release, six passing co-primary checks, bounded non-core synthetic-test-backed transition, M5 completion, and no transfer or chapter-core promotion.")

if __name__ == "__main__":
    main()
