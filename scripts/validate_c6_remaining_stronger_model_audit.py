#!/usr/bin/env python3
"""Validate C6's terminal triage of the remaining stronger-model actions."""

from __future__ import annotations

import copy
import hashlib
import json
import subprocess
from pathlib import Path

from jsonschema import Draft202012Validator

from build_c6_remaining_stronger_model_audit import build
from build_c6_remaining_stronger_model_audit import BASELINE_COMMIT


ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "proofs/c6_remaining_stronger_model_audit.json"
SCHEMA = ROOT / "schemas/c6_remaining_stronger_model_audit.schema.json"
OVERLAY = ROOT / "proofs/proof_semantic_depth_overlay.json"
DOC = ROOT / "docs/c6_remaining_stronger_model_audit_2026_07_26.md"


def failures(record: dict, *, inspect_files: bool = True) -> list[str]:
    out: list[str] = []
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    for error in Draft202012Validator(schema).iter_errors(record):
        out.append(f"schema:{'.'.join(map(str, error.path))}: {error.message}")
    rows = record.get("records", [])
    ids = [row.get("theorem_id") for row in rows]
    if len(ids) != len(set(ids)):
        out.append("duplicate theorem identity")
    retire = [row for row in rows if row.get("recommended_action", "").startswith("retire_")]
    rewrite = [
        row
        for row in rows
        if row.get("recommended_action") == "rewrite_as_inverse_route_property"
    ]
    checks = [
        (len(rows) == 54, "record count is not 54"),
        (len(retire) == 53, "retirement count is not 53"),
        (len(rewrite) == 1, "inverse rewrite count is not one"),
        (
            rewrite and rewrite[0].get("name") == "complete_failure_record_closes_record",
            "wrong theorem selected for inverse rewrite",
        ),
        (
            all(not row.get("theorem_dependency_refs") for row in rows),
            "a candidate has a Lean dependency",
        ),
        (
            all(not row.get("theorem_consumer_refs") for row in rows),
            "a candidate has a theorem consumer",
        ),
        (
            all(row.get("support_state_effect") == "none" for row in rows),
            "an action moves support",
        ),
        (
            all(not row.get("new_formal_claim_required") for row in retire),
            "retirement invented a replacement formal claim",
        ),
        (
            sum(row.get("module_path", "").endswith("/TheseusReference.lean") for row in rows)
            == 43,
            "Theseus mirror count is not 43",
        ),
        (record.get("support_state_effect") == "none", "packet moves support"),
        (record.get("release_effect") == "none", "packet moves release state"),
    ]
    out.extend(message for passed, message in checks if not passed)
    if inspect_files:
        overlay_bytes = subprocess.run(
            ["git", "show", f"{BASELINE_COMMIT}:proofs/proof_semantic_depth_overlay.json"],
            cwd=ROOT,
            check=True,
            capture_output=True,
        ).stdout
        overlay = json.loads(overlay_bytes)
        expected_ids = {
            row["theorem_id"]
            for row in overlay["records"]
            if row["disposition"] == "rewrite_with_stronger_model"
        }
        if set(ids) != expected_ids:
            out.append("audit does not exactly cover the current stronger-model set")
        digest = hashlib.sha256(overlay_bytes).hexdigest()
        if record.get("source_overlay", {}).get("sha256") != digest:
            out.append("source overlay digest drifted")
        rebuilt, rebuilt_doc = build()
        if record != rebuilt:
            out.append("machine audit is not deterministic-current")
        if DOC.read_text(encoding="utf-8") != rebuilt_doc:
            out.append("human audit is not deterministic-current")
        doc = " ".join(DOC.read_text(encoding="utf-8").split())
        for phrase in [
            "Fifty-three are fixture or summary mirrors",
            "one Failure Modes witness",
            "not relabeled as Lean proofs",
            "Lean dependencies: 0",
            "Support or release movement: none",
        ]:
            if phrase not in doc:
                out.append(f"human audit missing boundary: {phrase}")
    return out


def main() -> None:
    record = json.loads(RECORD.read_text(encoding="utf-8"))
    out = failures(record)
    mutations: list[tuple[str, dict]] = []

    def add(label: str, edit) -> None:
        candidate = copy.deepcopy(record)
        edit(candidate)
        mutations.append((label, candidate))

    add("drop action", lambda r: r["records"].pop())
    add("duplicate identity", lambda r: r["records"][1].__setitem__("theorem_id", r["records"][0]["theorem_id"]))
    add("hide dependency", lambda r: r["records"][0]["theorem_dependency_refs"].append("theorem://hidden"))
    add("hide consumer", lambda r: r["records"][0]["theorem_consumer_refs"].append("theorem://consumer"))
    add("replacement bloat", lambda r: r["records"][0].__setitem__("new_formal_claim_required", True))
    add("support promotion", lambda r: r["records"][0].__setitem__("support_state_effect", "promotion"))
    add("packet promotion", lambda r: r.__setitem__("support_state_effect", "promotion"))
    add("release effect", lambda r: r.__setitem__("release_effect", "publish"))
    add("wrong inverse", lambda r: r["records"][0].__setitem__("recommended_action", "rewrite_as_inverse_route_property"))
    add("wrong Theseus action", lambda r: next(x for x in r["records"] if x["module_path"].endswith("/TheseusReference.lean")).__setitem__("recommended_action", "rewrite_as_inverse_route_property"))
    add("overlay digest drift", lambda r: r["source_overlay"].__setitem__("sha256", "x" * 64))
    add("count drift", lambda r: r["summary"].__setitem__("retire_without_replacement_count", 52))
    for label, candidate in mutations:
        if not failures(candidate, inspect_files=False):
            out.append(f"negative mutation accepted: {label}")
    if out:
        raise SystemExit("C6 stronger-model audit failed:\n - " + "\n - ".join(out))
    print(
        "C6 stronger-model audit passed: 54/54 exact actions, 53 retire, "
        "1 inverse rewrite, zero dependencies/consumers, 12/12 mutations rejected."
    )


if __name__ == "__main__":
    main()
