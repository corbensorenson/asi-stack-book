#!/usr/bin/env python3
"""Generate one-shot baseline and governed outputs for P4/M8 Campaign 4."""

from __future__ import annotations

import argparse
import importlib.metadata
import json
import platform
import time

import mlx.core as mx
from mlx_lm import generate, load as load_model
from mlx_lm.sample_utils import make_sampler

from p4_m8_residual_verifier_common import BASE, MODEL_SNAPSHOT, baseline_prompt, governed_prompt, load, parse_object, sha, sha_bytes


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("preflight", "heldout"), required=True)
    args = parser.parse_args()
    prereg = load(BASE / "preregistration.json")
    design = load(BASE / "design.json")
    tasks_path = BASE / f"{args.phase}_tasks.json"
    raw_path = BASE / "raw" / f"{args.phase}_generation.json"
    if raw_path.exists():
        raise SystemExit(f"one-shot output already exists: {raw_path}")
    if sha(BASE / "design.json") != prereg["design_sha256"] or sha(tasks_path) != prereg[f"{args.phase}_tasks_sha256"]:
        raise SystemExit("frozen design or task bytes drifted")
    if args.phase == "heldout":
        qualification = load(BASE / "results/preflight_qualification.json")
        if qualification.get("protocol_outcome") != "instrument_adequate" or qualification.get("heldout_opened") is not True:
            raise SystemExit("heldout gate closed")
    if not MODEL_SNAPSHOT.is_dir():
        raise SystemExit(f"exact model snapshot unavailable: {MODEL_SNAPSHOT}")
    model, tokenizer = load_model(MODEL_SNAPSHOT.as_posix(), tokenizer_config={"trust_remote_code": False})
    sampler = make_sampler(temp=design["generation"]["temperature"])
    tasks = load(tasks_path)
    records = []
    started = time.perf_counter()
    for index, task in enumerate(tasks["tasks"]):
        outputs = {}
        for lane_index, lane in enumerate(("baseline", "governed")):
            prompt = baseline_prompt(task, prereg["run_id"]) if lane == "baseline" else governed_prompt(task, prereg["run_id"])
            rendered = tokenizer.apply_chat_template([{"role": "user", "content": prompt}], tokenize=False, add_generation_prompt=True, enable_thinking=False)
            mx.random.seed(812801 + index * 2 + lane_index)
            call_started = time.perf_counter()
            raw = generate(model, tokenizer, prompt=rendered, max_tokens=design["generation"][f"{lane}_max_tokens"], sampler=sampler, verbose=False).strip()
            try:
                token_count = len(tokenizer.encode(raw))
            except Exception:
                token_count = len(raw.split())
            outputs[lane] = {"prompt_sha256": sha_bytes(prompt.encode()), "raw_sha256": sha_bytes(raw.encode()), "raw": raw, "parsed": parse_object(raw), "elapsed_seconds": round(time.perf_counter() - call_started, 6), "token_count": token_count}
        records.append({"task_id": task["task_id"], "outputs": outputs})
        print(f"P4/M8 {args.phase} {index + 1}/{tasks['task_count']} closed", flush=True)
    receipt = {
        "schema_version": "asi_stack.p4_m8_residual_verifier_generation.v1",
        "phase": args.phase,
        "run_id": prereg["run_id"],
        "model_repository": design["generation"]["model_repository"],
        "snapshot_commit": design["generation"]["snapshot_commit"],
        "thinking": False,
        "retry_count": 0,
        "task_count": tasks["task_count"],
        "model_call_count": tasks["task_count"] * 2,
        "labels_loaded_by_generator": False,
        "environment": {"platform": platform.platform(), "mlx_lm": importlib.metadata.version("mlx-lm")},
        "elapsed_seconds": round(time.perf_counter() - started, 6),
        "records": records,
        "support_state_effect": "none_pending_adjudication",
    }
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    raw_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(f"P4/M8 {args.phase} generation closed: {sha(raw_path)}")


if __name__ == "__main__":
    main()
