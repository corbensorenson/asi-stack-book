#!/usr/bin/env python3
"""Evaluator-only process for post-v2.1 routing and deliberation."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


def canonical_sha(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def normalize(text: str) -> str:
    value = text.strip()
    blocks = re.findall(r"```(?:json|text)?\s*(.*?)```", value, flags=re.I | re.S)
    if blocks:
        value = blocks[-1].strip()
    value = re.sub(r"^(?:answer|final|output)\s*:\s*", "", value, flags=re.I).strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        value = value[1:-1]
    return " ".join(value.split()).strip().lower()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", type=Path, required=True)
    parser.add_argument("--request-id", required=True)
    parser.add_argument("--mode", choices=("candidate", "route"), required=True)
    parser.add_argument("--candidate", type=Path)
    parser.add_argument("--selected-action")
    args = parser.parse_args()
    request = next(row for row in json.loads(args.corpus.read_text())["requests"] if row["request_id"] == args.request_id)
    if args.mode == "candidate":
        if not args.candidate:
            raise SystemExit("--candidate is required in candidate mode")
        raw = args.candidate.read_text(encoding="utf-8")
        observed = normalize(raw)
        expected = normalize(str(request["answer_key"]))
        payload = {
            "evaluator_id": "post-v2-1-p2-answer-criterion-process-v0",
            "request_id": args.request_id,
            "mode": "candidate",
            "candidate_sha256": hashlib.sha256(raw.encode()).hexdigest(),
            "observed": observed,
            "correct": observed == expected,
            "parse_failure": observed == "",
        }
    else:
        payload = {
            "evaluator_id": "post-v2-1-p2-route-criterion-process-v0",
            "request_id": args.request_id,
            "mode": "route",
            "selected_action": args.selected_action,
            "correct": args.selected_action == request["gold_action"],
        }
    payload["evaluation_sha256"] = canonical_sha(payload)
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
