#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "experiments" / "p4_governed_usefulness"
PREREG = BASE / "difficulty_sweep_generation_preregistration.json"
TASKS = BASE / "difficulty_sweep_tasks_draft.json"
PROMPT = BASE / "difficulty_sweep_candidate_prompt_template.md"
RECEIPT = BASE / "raw" / "difficulty_sweep_qwen3_8b_run_001_generation.json"
CANDIDATES = BASE / "raw" / "difficulty_sweep_qwen3_8b_run_001_candidates.json"
MODEL = Path.home() / ".cache" / "huggingface" / "hub" / "models--mlx-community--Qwen3-8B-4bit" / "snapshots" / "545dc4251c05440727734bcd94334791f6ab0192"


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def digest(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def parse_document(text: str) -> dict[str, Any]:
    value = text.strip()
    if value.startswith("```json"):
        value = value[7:]
    elif value.startswith("```"):
        value = value[3:]
    if value.endswith("```"):
        value = value[:-3]
    start, end = value.find("{"), value.rfind("}")
    if start < 0 or end < start:
        raise ValueError("no JSON object in model output")
    parsed = json.loads(value[start:end + 1])
    if not isinstance(parsed, dict):
        raise ValueError("candidate document is not an object")
    return parsed


def main() -> None:
    if RECEIPT.exists() or CANDIDATES.exists():
        raise SystemExit("Tuning candidate generation is one-shot; an output already exists.")
    prereg = load(PREREG)
    tasks = load(TASKS)
    if digest(TASKS) != prereg["tasks_sha256"] or digest(PROMPT) != prereg["prompt_template_sha256"]:
        raise SystemExit("Frozen task or prompt digest drifted.")
    visible = {"corpus_id": tasks["corpus_id"], "candidate_vocabularies": tasks["candidate_vocabularies"], "tasks": tasks["tasks"]}
    prompt = PROMPT.read_text(encoding="utf-8").replace("PROVIDED_RUN_ID", prereg["run_id"]) + "\n\nCANDIDATE-VISIBLE INPUT\n" + json.dumps(visible, indent=2)
    generation = prereg["candidate_generator"]
    command = ["mlx_lm.generate", "--model", str(MODEL), "--prompt", "-", "--max-tokens", str(generation["maximum_new_tokens"]), "--temp", str(generation["temperature"]), "--seed", str(generation["seed"]), "--chat-template-config", '{"enable_thinking":false}', "--verbose", "False"]
    started = time.perf_counter()
    completed = subprocess.run(command, input=prompt, text=True, capture_output=True, check=False)
    elapsed = round(time.perf_counter() - started, 6)
    parse_error: str | None = None
    document: dict[str, Any] | None = None
    try:
        document = parse_document(completed.stdout)
    except (ValueError, json.JSONDecodeError) as error:
        parse_error = str(error)
    receipt = {
        "schema_version": "asi_stack.p4_governed_usefulness_difficulty_sweep_generation_receipt.v1",
        "run_id": prereg["run_id"],
        "candidate_generator_role": prereg["candidate_generator"]["role"],
        "model_repository": prereg["candidate_generator"]["model_repository"],
        "snapshot_commit": prereg["candidate_generator"]["snapshot_commit"],
        "claim_ceiling": prereg["candidate_generator"]["claim_ceiling"],
        "prompt_sha256": digest_bytes(prompt.encode("utf-8")),
        "tasks_sha256": digest(TASKS),
        "rubrics_loaded_by_generator": False,
        "process_exit_code": completed.returncode,
        "elapsed_seconds": elapsed,
        "retry_count": 0,
        "parse_error": parse_error,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "claim_attempt_counted": False,
        "support_state_effect": "none"
    }
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    if completed.returncode != 0 or document is None:
        raise SystemExit(f"Candidate generation failed closed: exit={completed.returncode}, parse_error={parse_error}")
    CANDIDATES.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    print(f"P4 tuning candidates closed before rubric load: elapsed={elapsed}s, candidate_sha256={digest(CANDIDATES)}, receipt_sha256={digest(RECEIPT)}")


if __name__ == "__main__":
    main()
