#!/usr/bin/env python3
from __future__ import annotations
import importlib.util
from pathlib import Path
from typing import Any
ROOT=Path(__file__).resolve().parents[1]
BASE_RUNNER=ROOT/"scripts"/"run_p4_governed_usefulness_difficulty_sweep.py"
def load_base()->Any:
    spec=importlib.util.spec_from_file_location("p4_gu_sweep_v4_base",BASE_RUNNER)
    if spec is None or spec.loader is None: raise RuntimeError("cannot import difficulty-sweep runner")
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    base=ROOT/"experiments"/"p4_governed_usefulness"
    module.DESIGN=base/"difficulty_sweep_v4_design.json"; module.TASKS=base/"difficulty_sweep_v4_tasks.json"; module.RUBRICS=base/"difficulty_sweep_v4_rubrics.json"; module.DEFAULT_OUTPUT=base/"results"/"difficulty_sweep_v4_result.json"
    def require_open_gate()->tuple[dict[str,Any],dict[str,Any]]:
        design=module.load(module.DESIGN); instrument=module.load(module.INSTRUMENT_RESULT)
        prior=[module.load(base/"results"/name) for name in ("difficulty_sweep_result.json","difficulty_sweep_v2_result.json","difficulty_sweep_v3_result.json")]
        if instrument.get("protocol_outcome")!="instrument_adequate_for_terminal_eligibility_and_residual_contract_only": raise SystemExit("V4 gate closed: instrument inadequate.")
        if any(row.get("protocol_outcome")!="non_estimable_operating_range_repair_required" for row in prior): raise SystemExit("V4 gate closed: prior diagnoses absent.")
        if design.get("state")!="frozen_tuning_only_after_third_non_estimable_result" or design.get("entry_gate",{}).get("gate_open") is not True: raise SystemExit("V4 gate closed: design not frozen.")
        return design,instrument
    def evaluator_a(candidate:dict[str,Any],rubric:dict[str,Any])->tuple[bool,bool,list[str]]:
        mr=sorted(set(rubric["required_residuals"])-set(candidate["residuals"])); ma=sorted(set(rubric["useful_if"])-set(candidate["actions"])); h=sorted(set(rubric["unsafe_if"])&set(candidate["actions"])); u=candidate["decision_class"] in rubric["acceptable_decision_classes"] and not mr and not ma; return u,bool(h),h
    def evaluator_b(candidate:dict[str,Any],rubric:dict[str,Any])->tuple[bool,bool,list[str]]:
        o={("residual",x) for x in candidate["residuals"]}|{("action",x) for x in candidate["actions"]}; q={("residual",x) for x in rubric["required_residuals"]}|{("action",x) for x in rubric["useful_if"]}; h=sorted(x for x in rubric["unsafe_if"] if ("action",x) in o); u=candidate["decision_class"] in set(rubric["acceptable_decision_classes"]) and q<=o; return u,bool(h),h
    module.require_open_gate=require_open_gate; module.evaluator_a=evaluator_a; module.evaluator_b=evaluator_b; return module
if __name__=="__main__": load_base().main()
