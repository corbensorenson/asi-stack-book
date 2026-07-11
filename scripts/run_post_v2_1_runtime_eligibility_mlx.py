#!/usr/bin/env python3
"""Run the single-candidate MLX eligibility amendment for post-v2.1 M2."""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path

import mlx.core as mx
from huggingface_hub import snapshot_download
from mlx_lm import generate, load


ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "experiments/post_v2_1_evidence_program/runtime_eligibility_plan.json"
AMENDMENT = ROOT / "experiments/post_v2_1_evidence_program/amendments/runtime_candidate_v1.json"
RESULT = ROOT / "experiments/post_v2_1_evidence_program/results/2026-07-10-runtime-eligibility-amendment-v1.json"


def hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def manifest(snapshot: Path) -> list[dict[str, object]]:
    rows = []
    for path in sorted(snapshot.iterdir()):
        if path.is_file() and (path.suffix in {".json", ".model", ".txt"} or path.name.endswith(".safetensors")):
            rows.append({"name": path.name, "bytes": path.stat().st_size, "sha256": hash_file(path)})
    return rows


def parse_answer(text: str) -> str | None:
    for block in reversed(re.findall(r"\{[^{}]*\}", text, flags=re.DOTALL)):
        try:
            value = json.loads(block)
        except json.JSONDecodeError:
            continue
        answer = value.get("answer") if isinstance(value, dict) else None
        if isinstance(answer, (str, int, float)):
            return str(answer).strip().lower()
    stripped = text.strip().lower()
    return stripped if stripped in {"42", "blue", "clarify", "refuse"} else None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--allow-download", action="store_true")
    parser.add_argument("--write-result", action="store_true")
    args = parser.parse_args()
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    amendment = json.loads(AMENDMENT.read_text(encoding="utf-8"))
    candidate = amendment["changes"]["added_candidate"]
    started = time.perf_counter()
    snapshot = Path(snapshot_download(
        candidate["model_id"],
        revision=candidate["revision"],
        local_files_only=not args.allow_download,
        allow_patterns=["*.json", "*.model", "*.txt", "*.safetensors"],
    ))
    model, tokenizer = load(str(snapshot), tokenizer_config={"trust_remote_code": False})
    observations = []
    for task in plan["development_tasks"]:
        messages = [
            {"role": "system", "content": "Return only the requested observable JSON. Do not reveal hidden reasoning."},
            {"role": "user", "content": task["prompt"]},
        ]
        kwargs = {"tokenize": False, "add_generation_prompt": True}
        if "Qwen3" in candidate["model_id"]:
            kwargs["enable_thinking"] = False
        prompt = tokenizer.apply_chat_template(messages, **kwargs)
        call_started = time.perf_counter()
        output = generate(model, tokenizer, prompt=prompt, max_tokens=96, verbose=False).strip()
        parsed = parse_answer(output)
        observations.append({
            "task_id": task["task_id"],
            "expected": task["expected"],
            "parsed_answer": parsed,
            "exact": parsed == str(task["expected"]).lower(),
            "output": output,
            "output_tokens_approx": len(tokenizer.encode(output, add_special_tokens=False)),
            "latency_seconds": round(time.perf_counter() - call_started, 6),
        })
    exact = sum(int(row["exact"]) for row in observations)
    files = manifest(snapshot)
    total_tokens = sum(row["output_tokens_approx"] for row in observations)
    record = {
        "schema_version": "asi_stack.post_v2_1_runtime_eligibility.v0",
        "record_type": "eligibility_result",
        "plan_id": plan["plan_id"],
        "amendment_id": amendment["amendment_id"],
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "environment": {
            "runtime": "mlx-lm",
            "mlx": importlib.metadata.version("mlx"),
            "mlx_lm": importlib.metadata.version("mlx-lm"),
            "device": "Apple Metal via MLX",
            "peak_memory_bytes": int(mx.get_peak_memory()),
        },
        "candidate_results": [{
            "candidate_id": candidate["candidate_id"],
            "model_id": candidate["model_id"],
            "revision": candidate["revision"],
            "license": candidate["license"],
            "quantization": candidate["quantization"],
            "snapshot_manifest": files,
            "snapshot_manifest_sha256": hashlib.sha256(json.dumps(files, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
            "observations": observations,
            "exact_count": exact,
            "task_count": len(observations),
            "eligible": exact >= 3,
        }],
        "aggregate": {
            "candidate_count": 1,
            "eligible_count": int(exact >= 3),
            "model_calls": len(observations),
            "generated_tokens_approx": total_tokens,
            "elapsed_seconds": round(time.perf_counter() - started, 6),
            "within_amended_call_budget": len(observations) <= amendment["budget_impact"]["additional_model_calls"],
            "within_amended_token_budget": total_tokens <= amendment["budget_impact"]["additional_generated_token_ceiling"],
        },
        "support_state_effect": "none",
        "non_claims": [
            "This amended eligibility run is development-only and not outcome evidence.",
            "A passing threshold would establish runtime eligibility, not general model quality.",
            "The model is a third-party quantized conversion of an upstream open-weight model.",
            "No hidden chain-of-thought is requested or retained."
        ]
    }
    rendered = json.dumps(record, indent=2, ensure_ascii=False) + "\n"
    if args.write_result:
        RESULT.write_text(rendered, encoding="utf-8")
        print(f"Wrote {RESULT.relative_to(ROOT)}")
    else:
        print(rendered)
    if exact < 3:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
