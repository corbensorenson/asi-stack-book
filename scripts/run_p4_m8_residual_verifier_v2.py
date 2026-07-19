#!/usr/bin/env python3
"""Run the one-shot v2 residual/verifier preflight or sealed heldout phase."""

from __future__ import annotations

import argparse
import importlib.metadata
import json
import platform
import time

import mlx.core as mx
from mlx_lm import generate, load as load_model
from mlx_lm.sample_utils import make_sampler

from p4_m8_residual_verifier_v2_common import BASE, MODEL_SNAPSHOT, baseline_prompt, governed_prompt, load, parse_object, sha, sha_bytes


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("--phase", choices=("preflight", "heldout"), required=True); args = parser.parse_args()
    prereg, design = load(BASE / "preregistration.json"), load(BASE / "design.json")
    tasks_path, out = BASE / f"{args.phase}_tasks.json", BASE / "raw" / f"{args.phase}_generation.json"
    if out.exists(): raise SystemExit(f"one-shot output already exists: {out}")
    if sha(BASE / "design.json") != prereg["design_sha256"] or sha(tasks_path) != prereg[f"{args.phase}_tasks_sha256"]: raise SystemExit("frozen inputs drifted")
    if args.phase == "heldout":
        q = load(BASE / "results/preflight_qualification.json")
        if q.get("protocol_outcome") != "instrument_adequate" or q.get("heldout_opened") is not True: raise SystemExit("heldout gate closed")
    if not MODEL_SNAPSHOT.is_dir(): raise SystemExit(f"model unavailable: {MODEL_SNAPSHOT}")
    model, tokenizer = load_model(MODEL_SNAPSHOT.as_posix(), tokenizer_config={"trust_remote_code": False})
    sampler = make_sampler(temp=design["model"]["temperature"]); tasks = load(tasks_path); records = []; started = time.perf_counter()
    for index, task in enumerate(tasks["tasks"]):
        outputs = {}
        for lane_index, lane in enumerate(("baseline", "governed")):
            prompt = baseline_prompt(task, prereg["run_id"]) if lane == "baseline" else governed_prompt(task, prereg["run_id"])
            rendered = tokenizer.apply_chat_template([{"role": "user", "content": prompt}], tokenize=False, add_generation_prompt=True, enable_thinking=False)
            mx.random.seed(822801 + index * 2 + lane_index); call_started = time.perf_counter()
            raw = generate(model, tokenizer, prompt=rendered, max_tokens=design["model"][f"{lane}_max_tokens"], sampler=sampler, verbose=False).strip()
            try: tokens = len(tokenizer.encode(raw))
            except Exception: tokens = len(raw.split())
            outputs[lane] = {"prompt_sha256": sha_bytes(prompt.encode()), "raw_sha256": sha_bytes(raw.encode()), "raw": raw, "parsed": parse_object(raw), "elapsed_seconds": round(time.perf_counter() - call_started, 6), "token_count": tokens}
        records.append({"task_id": task["task_id"], "outputs": outputs}); print(f"P4/M8 v2 {args.phase} {index + 1}/{tasks['task_count']} closed", flush=True)
    receipt = {"schema_version": "asi_stack.p4_m8_residual_verifier_generation.v2", "phase": args.phase, "run_id": prereg["run_id"], "model": design["model"], "task_count": tasks["task_count"], "model_call_count": tasks["task_count"] * 2, "labels_loaded_by_generator": False, "retry_count": 0, "environment": {"platform": platform.platform(), "mlx_lm": importlib.metadata.version("mlx-lm")}, "elapsed_seconds": round(time.perf_counter() - started, 6), "records": records, "support_state_effect": "none_pending_adjudication", "publication_authority": "none", "release_authority": "none"}
    out.parent.mkdir(parents=True, exist_ok=True); out.write_text(json.dumps(receipt, indent=2) + "\n"); print(f"P4/M8 v2 {args.phase} generation closed: {sha(out)}")


if __name__ == "__main__": main()
