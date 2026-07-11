#!/usr/bin/env python3
"""Build the deterministic frozen 300-example routing/deliberation corpus."""
from __future__ import annotations

import hashlib
import json
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "experiments/post_v2_routing_deliberation/input/corpus.json"
FAMILIES = ("arithmetic", "string_transformation", "policy_decision", "structured_extraction")


def text_features(text: str) -> list[float]:
    lower = text.lower()
    return [
        len(text) / 100,
        sum(char.isdigit() for char in text) / 10,
        text.count("=") / 4,
        sum(word in lower for word in ("access", "risk", "authorized", "approve")),
        sum(word in lower for word in ("uppercase", "reverse", "replace", "text")),
        sum(word in lower for word in ("add", "product", "difference", "compute")),
        sum(word in lower for word in ("extract", "field", "name", "count")),
    ]


def make_example(family: str, index: int, rng: random.Random) -> dict:
    if family == "arithmetic":
        a, b = rng.randint(-30, 50), rng.randint(1, 20)
        op = ("add", "product", "difference")[index % 3]
        request = f"Compute the {op} for {a} and {b}."
        answer = str(a + b if op == "add" else a * b if op == "product" else a - b)
        payload = {"a": a, "b": b, "op": op}
    elif family == "string_transformation":
        text = f"item{index}-{chr(97 + index % 26)}"
        op = ("uppercase", "reverse", "replace")[index % 3]
        request = f"{op.title()} the text {text}."
        answer = text.upper() if op == "uppercase" else text[::-1] if op == "reverse" else text.replace("-", "_")
        payload = {"text": text, "op": op}
    elif family == "policy_decision":
        risk = rng.randint(0, 9)
        authorized = index % 4 != 0
        request = f"Decide access: risk={risk}; authorized={'yes' if authorized else 'no'}."
        answer = "approve" if authorized and risk <= 4 else "deny"
        payload = {"risk": risk, "authorized": authorized}
    else:
        name = f"record{index}"
        count = rng.randint(0, 99)
        request = f"Extract fields from name={name};count={count}."
        answer = json.dumps({"count": count, "name": name}, sort_keys=True, separators=(",", ":"))
        payload = {"name": name, "count": count}
    split = "train" if index < 45 else "validation" if index < 60 else "test"
    return {
        "example_id": f"{family}-{index:03d}",
        "family": family,
        "split": split,
        "request": request,
        "payload": payload,
        "answer": answer,
        "features": text_features(request),
    }


def main() -> None:
    rng = random.Random(20260710)
    examples = [make_example(family, index, rng) for family in FAMILIES for index in range(75)]
    payload = {
        "schema_version": "asi_stack.post_v2_routing_deliberation_corpus.v0",
        "corpus_id": "post-v2-routing-deliberation-300-2026-07-10",
        "generation_seed": 20260710,
        "frozen_before_test_outcomes": True,
        "families": list(FAMILIES),
        "split_counts": {"train": 180, "validation": 60, "test": 60},
        "compute_contract": {
            "routing_candidate_operation_cap": 2,
            "deliberation_candidate_operation_cap": 3,
            "single_specialist_padding_is_counted": True,
            "oracle_router_is_comparator_only": True,
            "test_labels_forbidden_for_router_training": True
        },
        "examples": examples,
    }
    payload["corpus_sha256"] = hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)} with {len(examples)} examples")


if __name__ == "__main__":
    main()
