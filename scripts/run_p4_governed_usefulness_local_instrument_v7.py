#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE_RUNNER = ROOT / "scripts" / "run_p4_governed_usefulness_local_instrument.py"


def load_base() -> Any:
    spec = importlib.util.spec_from_file_location("p4_local_instrument_base_v7", BASE_RUNNER)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import local instrument base runner")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    base = ROOT / "experiments" / "p4_governed_usefulness"
    module.PREREG = base / "local_instrument_preregistration_v7.json"
    module.TASKS = base / "local_instrument_tasks_v7.json"
    module.LABELS = base / "local_instrument_labels_v7.json"
    module.PROMPT = base / "local_instrument_prompt_v5.md"
    module.RAW = base / "raw" / "local_instrument_qualification_v7_codex.json"
    module.RESULT = base / "results" / "local_instrument_qualification_v7.json"
    return module


if __name__ == "__main__":
    load_base().main()
