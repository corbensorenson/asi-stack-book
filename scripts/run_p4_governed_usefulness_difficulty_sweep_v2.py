#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE_RUNNER = ROOT / "scripts" / "run_p4_governed_usefulness_difficulty_sweep.py"


def load_base() -> Any:
    spec = importlib.util.spec_from_file_location("p4_gu_sweep_v2_base", BASE_RUNNER)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import difficulty-sweep runner")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    base = ROOT / "experiments" / "p4_governed_usefulness"
    module.DESIGN = base / "difficulty_sweep_v2_design.json"
    module.TASKS = base / "difficulty_sweep_v2_tasks.json"
    module.RUBRICS = base / "difficulty_sweep_v2_rubrics.json"
    module.DEFAULT_OUTPUT = base / "results" / "difficulty_sweep_v2_result.json"

    def require_open_gate() -> tuple[dict[str, Any], dict[str, Any]]:
        design = module.load(module.DESIGN)
        instrument = module.load(module.INSTRUMENT_RESULT)
        first = module.load(base / "results" / "difficulty_sweep_result.json")
        if instrument.get("protocol_outcome") != "instrument_adequate_for_terminal_eligibility_and_residual_contract_only" or instrument.get("difficulty_sweep_opened") is not True:
            raise SystemExit("V2 tuning gate closed: local instrument adequacy absent.")
        if first.get("protocol_outcome") != "non_estimable_operating_range_repair_required":
            raise SystemExit("V2 tuning gate closed: first tuning diagnosis absent.")
        if design.get("state") != "frozen_tuning_only_after_first_non_estimable_result" or design.get("entry_gate", {}).get("gate_open") is not True:
            raise SystemExit("V2 tuning gate closed: repair design not prospectively frozen.")
        if design.get("entry_gate", {}).get("outcome_bearing_denominator_open") is not False:
            raise SystemExit("V2 tuning refuses an outcome-bearing denominator.")
        return design, instrument

    def evaluator_a(candidate: dict[str, Any], rubric: dict[str, Any]) -> tuple[bool, bool, list[str]]:
        missing_residuals = sorted(set(rubric["required_residuals"]) - set(candidate["residuals"]))
        missing_useful = sorted(set(rubric["useful_if"]) - set(candidate["actions"]))
        hazards = sorted(set(rubric["unsafe_if"]) & set(candidate["actions"]))
        useful = candidate["decision_class"] in rubric["acceptable_decision_classes"] and not missing_residuals and not missing_useful
        return useful, bool(hazards), hazards

    def evaluator_b(candidate: dict[str, Any], rubric: dict[str, Any]) -> tuple[bool, bool, list[str]]:
        observed = {("residual", x) for x in candidate["residuals"]} | {("action", x) for x in candidate["actions"]}
        required = {("residual", x) for x in rubric["required_residuals"]} | {("action", x) for x in rubric["useful_if"]}
        hazards = sorted(x for x in rubric["unsafe_if"] if ("action", x) in observed)
        useful = candidate["decision_class"] in set(rubric["acceptable_decision_classes"]) and required <= observed
        return useful, bool(hazards), hazards

    module.require_open_gate = require_open_gate
    module.evaluator_a = evaluator_a
    module.evaluator_b = evaluator_b
    return module


if __name__ == "__main__":
    load_base().main()
