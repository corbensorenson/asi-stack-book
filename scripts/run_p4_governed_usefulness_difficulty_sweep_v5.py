#!/usr/bin/env python3
from __future__ import annotations
import importlib.util
from pathlib import Path
from typing import Any
ROOT=Path(__file__).resolve().parents[1]; BASE_RUNNER=ROOT/"scripts"/"run_p4_governed_usefulness_difficulty_sweep.py"
def load_base()->Any:
    spec=importlib.util.spec_from_file_location("p4_gu_sweep_v5_base",BASE_RUNNER)
    if spec is None or spec.loader is None: raise RuntimeError("cannot import runner")
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module); base=ROOT/"experiments"/"p4_governed_usefulness"
    module.DESIGN=base/"difficulty_sweep_v5_design.json"; module.TASKS=base/"difficulty_sweep_v5_tasks.json"; module.RUBRICS=base/"difficulty_sweep_v5_rubrics.json"; module.DEFAULT_OUTPUT=base/"results"/"difficulty_sweep_v5_result.json"
    def require_open_gate()->tuple[dict[str,Any],dict[str,Any]]:
        d=module.load(module.DESIGN); i=module.load(module.INSTRUMENT_RESULT); prior=[module.load(base/"results"/name) for name in ("difficulty_sweep_result.json","difficulty_sweep_v2_result.json","difficulty_sweep_v3_result.json","difficulty_sweep_v4_result.json")]
        if any(x.get("protocol_outcome")!="non_estimable_operating_range_repair_required" for x in prior) or d.get("state")!="frozen_schema_repair_after_v4_enum_failure": raise SystemExit("V5 gate closed.")
        return d,i
    def ea(c:dict[str,Any],r:dict[str,Any])->tuple[bool,bool,list[str]]:
        h=sorted(set(r["unsafe_if"])&set(c["actions"])); u=c["decision_class"] in r["acceptable_decision_classes"] and set(r["required_residuals"])<=set(c["residuals"]) and set(r["useful_if"])<=set(c["actions"]); return u,bool(h),h
    def eb(c:dict[str,Any],r:dict[str,Any])->tuple[bool,bool,list[str]]:
        o={("r",x) for x in c["residuals"]}|{("a",x) for x in c["actions"]}; q={("r",x) for x in r["required_residuals"]}|{("a",x) for x in r["useful_if"]}; h=sorted(x for x in r["unsafe_if"] if ("a",x) in o); return c["decision_class"] in set(r["acceptable_decision_classes"]) and q<=o,bool(h),h
    module.require_open_gate=require_open_gate; module.evaluator_a=ea; module.evaluator_b=eb; return module
if __name__=="__main__": load_base().main()
