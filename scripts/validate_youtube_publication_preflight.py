#!/usr/bin/env python3
"""Validate local YouTube inputs, route constraints, and rejecting controls."""

from __future__ import annotations

import copy
import json
from pathlib import Path

from jsonschema import Draft202012Validator

from build_youtube_publication_preflight import ROOT, OUT, build


SCHEMA = ROOT / "schemas/youtube_publication_preflight.schema.json"
RECEIPT_SCHEMA = ROOT / "schemas/youtube_platform_receipt.schema.json"
MUTATION_SCOPE_SCHEMA = ROOT / "schemas/youtube_mutation_scope.schema.json"
MUTATION_SCOPE = ROOT / "visual_edition/youtube_mutation_scope.json"


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def errors(value: dict, expected: dict) -> list[str]:
    failures = [
        f"schema:{'.'.join(map(str, error.path))}: {error.message}"
        for error in Draft202012Validator(read(SCHEMA)).iter_errors(value)
    ]
    receipt_schema = read(RECEIPT_SCHEMA)
    mutation_scope_schema = read(MUTATION_SCOPE_SCHEMA)
    try:
        Draft202012Validator.check_schema(receipt_schema)
        Draft202012Validator.check_schema(mutation_scope_schema)
    except Exception as error:  # jsonschema supplies the diagnostic.
        failures.append(f"YouTube publication schema invalid: {error}")
    failures.extend(
        f"mutation-scope-schema:{'.'.join(map(str, error.path))}: {error.message}"
        for error in Draft202012Validator(mutation_scope_schema).iter_errors(
            read(MUTATION_SCOPE)
        )
    )
    comparable = copy.deepcopy(expected)
    comparable["generated_at_utc"] = value.get("generated_at_utc")
    if value != comparable:
        failures.append("preflight artifact drifted from current local publication inputs")
    return failures


def main() -> None:
    value = read(OUT)
    expected = build()
    failures = errors(value, expected)
    mutations: list[tuple[str, dict]] = []

    def add(label: str, edit) -> None:
        candidate = copy.deepcopy(value)
        edit(candidate)
        mutations.append((label, candidate))

    if value["entries"]:
        add("entry deletion", lambda d: d["entries"].pop())
        add("master digest substitution", lambda d: d["entries"][0].__setitem__("master_sha256", "0" * 64))
        add("thumbnail oversize", lambda d: d["entries"][0].__setitem__("thumbnail_bytes", 2 * 1024 * 1024 + 1))
    else:
        # A clean checkout has no ignored local masters, captions, or
        # thumbnails. Keep the negative-control count meaningful without
        # manufacturing a fake entry just to exercise an index mutation.
        add("empty-plan entry insertion", lambda d: d["entries"].append({"chapter_id": "unprepared"}))
        add("empty-plan denominator", lambda d: d.__setitem__("entry_count", 1))
        add("empty-plan readiness", lambda d: d.__setitem__("ready_entry_count", 1))
    add("premature authority", lambda d: d.__setitem__("external_mutation_authorized_now", True))
    add("mutation scope substitution", lambda d: d.__setitem__("mutation_scope_sha256", "0" * 64))
    add("playlist title substitution", lambda d: d.__setitem__("playlist_title", "Ambiguous playlist"))
    add("studio batch widening", lambda d: d["studio_browser_route"].__setitem__("maximum_files_per_upload_dialog", 84))
    add("API quota-day collapse", lambda d: d["data_api_route"].__setitem__("minimum_quota_days_for_complete_batch", 1))
    add("forced-private boundary deletion", lambda d: d["data_api_route"].__setitem__("unverified_api_projects_force_private_uploads", False))
    add("support promotion", lambda d: d.__setitem__("support_state_effect", "promotion"))
    for label, candidate in mutations:
        if not errors(candidate, expected):
            failures.append(f"negative mutation accepted: {label}")
    if failures:
        raise SystemExit(
            "YouTube publication preflight validation failed:\n - "
            + "\n - ".join(failures)
        )
    print(
        "YouTube publication preflight passed: "
        f"{value['ready_entry_count']}/{value['entry_count']} masters, captions, and thumbnails exact; "
        f"{value['studio_browser_route']['batch_count']} bounded Studio batches; "
        f"{value['data_api_route']['minimum_quota_days_for_complete_batch']}-day default API-quota route; "
        "10/10 mutations rejected; no platform mutation authorized."
    )


if __name__ == "__main__":
    main()
