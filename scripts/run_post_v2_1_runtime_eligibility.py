#!/usr/bin/env python3
"""Run the frozen, development-only post-v2.1 local-model eligibility gate."""

from __future__ import annotations

import argparse
import gc
import hashlib
import importlib.metadata
import json
import os
import platform
import re
import time
from datetime import datetime, timezone
from pathlib import Path

import torch
from huggingface_hub import snapshot_download
from transformers import AutoModelForCausalLM, AutoTokenizer


ROOT = Path(__file__).resolve().parents[1]
PLAN_PATH = ROOT / "experiments/post_v2_1_evidence_program/runtime_eligibility_plan.json"
RESULT_PATH = ROOT / "experiments/post_v2_1_evidence_program/results/2026-07-10-runtime-eligibility.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_answer(text: str) -> str | None:
    blocks = re.findall(r"\{[^{}]*\}", text, flags=re.DOTALL)
    for block in reversed(blocks):
        try:
            value = json.loads(block)
        except json.JSONDecodeError:
            continue
        answer = value.get("answer") if isinstance(value, dict) else None
        if isinstance(answer, (str, int, float)):
            return str(answer).strip().lower()
    return None


def snapshot_manifest(path: Path) -> list[dict[str, object]]:
    rows = []
    for child in sorted(path.iterdir()):
        if child.is_file() and (child.suffix in {".json", ".model", ".txt"} or child.name.endswith(".safetensors")):
            rows.append({"name": child.name, "bytes": child.stat().st_size, "sha256": sha256(child)})
    return rows


def render_prompt(tokenizer, prompt: str, model_id: str) -> str:
    messages = [
        {"role": "system", "content": "Follow the requested observable output format. Do not reveal hidden reasoning."},
        {"role": "user", "content": prompt},
    ]
    kwargs = {"tokenize": False, "add_generation_prompt": True}
    if "Qwen3" in model_id:
        kwargs["enable_thinking"] = False
    try:
        return tokenizer.apply_chat_template(messages, **kwargs)
    except TypeError:
        kwargs.pop("enable_thinking", None)
        return tokenizer.apply_chat_template(messages, **kwargs)


def run_candidate(candidate: dict, tasks: list[dict], allow_download: bool, requested_device: str) -> dict:
    started = time.perf_counter()
    model_id = candidate["model_id"]
    revision = candidate["revision"]
    snapshot = Path(snapshot_download(
        repo_id=model_id,
        revision=revision,
        local_files_only=not allow_download,
        allow_patterns=["*.json", "*.model", "*.txt", "*.safetensors"],
    ))
    device = requested_device
    if device == "mps" and not torch.backends.mps.is_available():
        raise RuntimeError("requested MPS device is unavailable")
    dtype = torch.float16 if device == "mps" else torch.float32
    tokenizer = AutoTokenizer.from_pretrained(snapshot, local_files_only=True, trust_remote_code=False)
    model = AutoModelForCausalLM.from_pretrained(
        snapshot,
        local_files_only=True,
        trust_remote_code=False,
        torch_dtype=dtype,
        low_cpu_mem_usage=True,
    ).to(device)
    model.eval()
    observations = []
    for index, task in enumerate(tasks):
        torch.manual_seed(7100 + index)
        rendered = render_prompt(tokenizer, task["prompt"], model_id)
        inputs = tokenizer(rendered, return_tensors="pt").to(device)
        call_started = time.perf_counter()
        with torch.inference_mode():
            generated = model.generate(
                **inputs,
                do_sample=False,
                max_new_tokens=96,
                pad_token_id=tokenizer.eos_token_id,
            )
        new_tokens = generated[0, inputs["input_ids"].shape[1]:]
        output = tokenizer.decode(new_tokens, skip_special_tokens=True).strip()
        answer = parse_answer(output)
        observations.append({
            "task_id": task["task_id"],
            "expected": task["expected"],
            "parsed_answer": answer,
            "exact": answer == str(task["expected"]).lower(),
            "output": output,
            "input_tokens": int(inputs["input_ids"].shape[1]),
            "output_tokens": int(new_tokens.shape[0]),
            "latency_seconds": round(time.perf_counter() - call_started, 6),
        })
    exact = sum(int(row["exact"]) for row in observations)
    manifest = snapshot_manifest(snapshot)
    result = {
        "candidate_id": candidate["candidate_id"],
        "model_id": model_id,
        "revision": revision,
        "license": candidate["license"],
        "device": device,
        "dtype": str(dtype).replace("torch.", ""),
        "snapshot_manifest": manifest,
        "snapshot_manifest_sha256": hashlib.sha256(json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
        "observations": observations,
        "exact_count": exact,
        "task_count": len(tasks),
        "eligible": exact >= 3,
        "elapsed_seconds": round(time.perf_counter() - started, 6),
    }
    del model, tokenizer
    gc.collect()
    if torch.backends.mps.is_available():
        torch.mps.empty_cache()
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--allow-download", action="store_true")
    parser.add_argument("--write-result", action="store_true")
    parser.add_argument("--device", choices=["cpu", "mps"], default="cpu")
    args = parser.parse_args()
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    started = time.perf_counter()
    results = []
    for candidate in plan["candidates"]:
        try:
            results.append(run_candidate(candidate, plan["development_tasks"], args.allow_download, args.device))
        except Exception as exc:
            results.append({
                "candidate_id": candidate["candidate_id"],
                "model_id": candidate["model_id"],
                "revision": candidate["revision"],
                "eligible": False,
                "error_type": type(exc).__name__,
                "error": str(exc)[:1000],
            })
    total_calls = sum(len(row.get("observations", [])) for row in results)
    total_tokens = sum(obs["output_tokens"] for row in results for obs in row.get("observations", []))
    record = {
        "schema_version": plan["schema_version"],
        "record_type": "eligibility_result",
        "plan_id": plan["plan_id"],
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "environment": {
            "platform": platform.platform(),
            "python": platform.python_version(),
            "torch": torch.__version__,
            "transformers": importlib.metadata.version("transformers"),
            "huggingface_hub": importlib.metadata.version("huggingface-hub"),
            "tokenizers_parallelism": os.environ.get("TOKENIZERS_PARALLELISM", "unset"),
        },
        "candidate_results": results,
        "aggregate": {
            "candidate_count": len(results),
            "eligible_count": sum(int(row.get("eligible", False)) for row in results),
            "model_calls": total_calls,
            "generated_tokens": total_tokens,
            "elapsed_seconds": round(time.perf_counter() - started, 6),
            "within_call_budget": total_calls <= plan["resource_budget"]["model_calls"],
            "within_token_budget": total_tokens <= plan["resource_budget"]["generated_token_ceiling"],
        },
        "support_state_effect": "none",
        "non_claims": [
            "Eligibility outputs are development-only and not outcome evidence.",
            "Exact answers on four tasks do not establish general model quality.",
            "The runner does not request or preserve hidden chain-of-thought.",
            "Local model-role separation is not external independence."
        ],
    }
    rendered = json.dumps(record, indent=2, ensure_ascii=False) + "\n"
    if args.write_result:
        RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
        RESULT_PATH.write_text(rendered, encoding="utf-8")
        print(f"Wrote {RESULT_PATH.relative_to(ROOT)}")
    else:
        print(rendered)
    if record["aggregate"]["eligible_count"] == 0:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
