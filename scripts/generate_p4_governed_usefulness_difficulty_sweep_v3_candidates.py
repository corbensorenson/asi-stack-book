#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BASE_SCRIPT = ROOT / "scripts" / "generate_p4_governed_usefulness_difficulty_sweep_candidates.py"

def load_base() -> Any:
    spec = importlib.util.spec_from_file_location("p4_gu_generator_v3_base", BASE_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import tuning generator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    base = ROOT / "experiments" / "p4_governed_usefulness"
    module.PREREG = base / "difficulty_sweep_v3_generation_preregistration.json"
    module.TASKS = base / "difficulty_sweep_v3_tasks.json"
    module.PROMPT = base / "difficulty_sweep_v3_candidate_prompt.md"
    module.RECEIPT = base / "raw" / "difficulty_sweep_v3_qwen3_8b_run_001_generation.json"
    module.CANDIDATES = base / "raw" / "difficulty_sweep_v3_qwen3_8b_run_001_candidates.json"
    return module

if __name__ == "__main__":
    load_base().main()
