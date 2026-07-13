#!/usr/bin/env python3
"""Independent structural evaluator for the bounded QCSA round-trip lane.

This implementation intentionally does not import qcsa_ref.round_trip.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


FIELDS = ("identity", "roles", "negation", "modality", "quantity", "time", "claim_citation_bindings", "authority", "residuals")


def normalize(value: object) -> object:
    if isinstance(value, dict):
        return {key: normalize(value[key]) for key in sorted(value)}
    if isinstance(value, list):
        normalized = [normalize(item) for item in value]
        return sorted(normalized, key=lambda item: json.dumps(item, sort_keys=True, ensure_ascii=False))
    if isinstance(value, str):
        return " ".join(value.split())
    return value


def evaluate(source: dict, candidate: dict) -> dict[str, bool]:
    missing = [field for field in FIELDS if field not in source or field not in candidate]
    if missing:
        raise ValueError(f"missing structural fields: {missing}")
    return {field: normalize(source[field]) == normalize(candidate[field]) for field in FIELDS}


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: qcsa_independent_evaluator.py SOURCE.json CANDIDATE.json")
    source = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    candidate = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    print(json.dumps(evaluate(source, candidate), sort_keys=True))


if __name__ == "__main__":
    main()
