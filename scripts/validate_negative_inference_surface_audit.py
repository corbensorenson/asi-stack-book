#!/usr/bin/env python3
"""Validate current negative-inference language and rejecting controls."""

from __future__ import annotations

import copy
import json
from pathlib import Path

from jsonschema import Draft202012Validator

from build_negative_inference_surface_audit import ROOT, OUT, audit


SCHEMA = ROOT / "schemas/negative_inference_surface_audit.schema.json"


def errors(value: dict, expected: dict) -> list[str]:
    out = []
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    for error in Draft202012Validator(schema).iter_errors(value):
        out.append(f"schema:{'.'.join(map(str, error.path))}: {error.message}")
    if value != expected:
        out.append("audit artifact drifted from current surface bytes or classifications")
    return out


def main() -> None:
    value = json.loads(OUT.read_text(encoding="utf-8"))
    expected = audit()
    failures = errors(value, expected)
    mutations = []

    def add(label, edit):
        candidate = copy.deepcopy(value)
        edit(candidate)
        mutations.append((label, candidate))

    add("erase surface", lambda d: d["surfaces"].pop())
    add("invent N3", lambda d: d["summary"]["accepted_transition_rehabilitation_counts"].__setitem__("N3", 1))
    add("broad inference", lambda d: d["summary"].__setitem__("broad_negative_inference_count", 1))
    add("core refutation", lambda d: d["summary"].__setitem__("chapter_core_refutation_count", 1))
    add("erase forbidden hit count", lambda d: d["summary"].__setitem__("forbidden_overbroad_phrase_count", -1))
    add("rewrite digest", lambda d: d["surfaces"][0].__setitem__("sha256", "0" * 64))
    add("mutate history", lambda d: d["scope"].__setitem__("historical_transition_files_mutated", 1))
    add("support promotion", lambda d: d["summary"].__setitem__("support_state_effect", "promotion"))
    for label, candidate in mutations:
        if not errors(candidate, expected):
            failures.append(f"negative mutation accepted: {label}")
    if failures:
        raise SystemExit("Negative-inference surface audit failed:\n - " + "\n - ".join(failures))
    print(
        f"Negative-inference surface audit passed: {value['scope']['surface_count']} current surfaces "
        f"including {value['scope']['chapter_count']}/{value['scope']['chapter_count']} chapters; "
        "zero forbidden overbroad phrases, zero missing rehabilitation boundaries, zero blocked-claim boundary failures; "
        "8/8 mutations rejected."
    )


if __name__ == "__main__":
    main()
