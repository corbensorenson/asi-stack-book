#!/usr/bin/env python3
"""Validate the first dependency-safe C6 proof-rationalization transaction."""

from __future__ import annotations

import copy
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

import jsonschema

from build_proof_rationalization_registry import current_theorems, normalize
from build_proof_semantic_depth_overlay import statement_key, theorem_graph


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "proofs" / "proof_semantic_rationalization_ledger.json"
SCHEMA = ROOT / "schemas" / "proof_semantic_rationalization_ledger.schema.json"
CURRENT_OVERLAY = ROOT / "proofs" / "proof_semantic_depth_overlay.json"
HISTORICAL = ROOT / "proofs" / "proof_rationalization_registry.json"
STATUS = ROOT / "roadmap_records" / "post_v2_3_maintenance_transfer_and_publication_status.json"
ROADMAP = ROOT / "docs" / "post_v2_3_maintenance_transfer_and_publication_roadmap.md"
THEOREM_START = re.compile(r"(?m)^theorem\s+([A-Za-z_][A-Za-z0-9_']*)\b")
DECL_START = re.compile(
    r"(?m)^(?:theorem|def|abbrev|structure|inductive|class|instance|namespace|end)\b"
)


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def git_show(commit: str, path: str) -> bytes:
    return subprocess.run(
        ["git", "show", f"{commit}:{path}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout


def theorem_blocks(text: str) -> dict[str, dict[str, str]]:
    declarations = list(DECL_START.finditer(text))
    rows: dict[str, dict[str, str]] = {}
    for match in THEOREM_START.finditer(text):
        end = next(
            (candidate.start() for candidate in declarations if candidate.start() > match.start()),
            len(text),
        )
        block = text[match.start():end]
        signature = block.split(":= by", 1)[0]
        rows[match.group(1)] = {
            "block": block,
            "signature": normalize(signature),
        }
    return rows


def validation_errors(ledger: dict[str, Any], *, check_files: bool = True) -> list[str]:
    out: list[str] = []
    try:
        jsonschema.Draft202012Validator(load(SCHEMA)).validate(ledger)
    except jsonschema.ValidationError as exc:
        out.append(f"schema: {exc.message}")
        return out

    baseline = ledger["baseline"]
    action = ledger["actions"][0]
    retired_id = action["retired_theorem_id"]
    retained_id = action["retained_theorem_id"]
    retired_name = retired_id.split("::", 1)[1]
    retained_name = retained_id.split("::", 1)[1]

    if retired_id.split("::", 1)[0] != action["module_path"]:
        out.append("retired theorem is not bound to the declared module")
    if retained_id.split("::", 1)[0] != action["module_path"]:
        out.append("retained theorem is not bound to the declared module")

    if not check_files:
        return out

    try:
        baseline_overlay_bytes = git_show(baseline["commit"], baseline["overlay_path"])
        baseline_module_bytes = git_show(baseline["commit"], baseline["module_path"])
    except subprocess.CalledProcessError as exc:
        out.append(f"immutable baseline cannot be read: {exc}")
        return out

    if sha256_bytes(baseline_overlay_bytes) != baseline["overlay_sha256"]:
        out.append("baseline overlay digest drifted")
    if sha256_bytes(baseline_module_bytes) != baseline["module_sha256"]:
        out.append("baseline module digest drifted")

    baseline_overlay = json.loads(baseline_overlay_bytes)
    baseline_rows = {
        row["theorem_id"]: row for row in baseline_overlay.get("records", [])
    }
    if len(baseline_rows) != baseline["live_theorem_count"]:
        out.append("baseline theorem denominator drifted")
    baseline_action_count = sum(
        row.get("disposition") != "retain" for row in baseline_rows.values()
    )
    if baseline_action_count != baseline["rewrite_or_retire_count"]:
        out.append("baseline action denominator drifted")
    retired_row = baseline_rows.get(retired_id)
    retained_row = baseline_rows.get(retained_id)
    if retired_row is None or retained_row is None:
        out.append("baseline does not contain both retirement participants")
        return out
    if retired_row.get("disposition") != "retire_duplicate":
        out.append("baseline did not classify the retired declaration as a duplicate")
    if retired_row.get("duplicate_of") != retained_id:
        out.append("baseline canonical duplicate lineage drifted")
    if retired_row.get("module_path") != retained_row.get("module_path"):
        out.append("retirement participants are not in one authored model")
    if statement_key(retired_row["current_signature"]) != statement_key(
        retained_row["current_signature"]
    ):
        out.append("baseline normalized statements are not equal")
    normalized_digest = sha256_bytes(
        statement_key(retired_row["current_signature"]).encode("utf-8")
    )
    if normalized_digest != action["normalized_statement_sha256"]:
        out.append("normalized statement digest drifted")
    if retired_row.get("theorem_dependency_refs") != []:
        out.append("retired theorem had theorem dependencies")
    if retired_row.get("theorem_consumer_refs") != []:
        out.append("retired theorem had theorem consumers")

    blocks = theorem_blocks(baseline_module_bytes.decode("utf-8"))
    if retired_name not in blocks or retained_name not in blocks:
        out.append("baseline module does not contain both theorem blocks")
    else:
        if sha256_bytes(blocks[retired_name]["block"].encode("utf-8")) != action[
            "retired_block_sha256"
        ]:
            out.append("retired theorem block digest drifted")
        if sha256_bytes(blocks[retained_name]["block"].encode("utf-8")) != action[
            "retained_block_sha256"
        ]:
            out.append("retained theorem block digest drifted")

    current_rows = current_theorems()
    current_ids = {row["theorem_id"] for row in current_rows}
    if retired_id in current_ids:
        out.append("retired theorem remains live")
    if retained_id not in current_ids:
        out.append("retained canonical theorem is missing")
    dependencies, consumers = theorem_graph(current_rows)
    if consumers.get(retired_id, []):
        out.append("retired theorem still has current theorem consumers")
    module_text = (ROOT / action["module_path"]).read_text(encoding="utf-8")
    if re.search(rf"(?m)^theorem\s+{re.escape(retired_name)}\b", module_text):
        out.append("retired theorem declaration remains in the module")
    if not re.search(rf"(?m)^theorem\s+{re.escape(retained_name)}\b", module_text):
        out.append("retained theorem declaration is missing from the module")

    overlay = load(CURRENT_OVERLAY)
    summary = overlay.get("summary", {})
    expected_levels = {
        "P0": 49,
        "P1": 800,
        "P2": 25,
        "P3": 319,
        "P4": 93,
        "P5": 83,
        "P6": 0,
    }
    expected_dispositions = {
        "retain": 1209,
        "retire_narrow_projection": 63,
        "rewrite_scope_language": 2,
        "rewrite_with_stronger_model": 95,
    }
    if summary.get("current_theorem_count") != ledger["summary"]["current_live_theorem_count"]:
        out.append("current theorem count does not match the ledger")
    if summary.get("semantic_level_counts") != expected_levels:
        out.append("current semantic-level counts drifted")
    if summary.get("disposition_counts") != expected_dispositions:
        out.append("current disposition counts drifted")
    if sum(value for key, value in expected_dispositions.items() if key != "retain") != ledger[
        "summary"
    ]["remaining_action_count"]:
        out.append("remaining action denominator drifted")
    if ledger["summary"]["remaining_action_counts"] != {
        key: value for key, value in expected_dispositions.items() if key != "retain"
    }:
        out.append("remaining action family counts drifted")
    if summary.get("duplicate_group_count") != 0:
        out.append("same-model exact duplicate group remains after execution")

    historical = load(HISTORICAL)
    if len(historical.get("baseline_theorems", [])) != 1151:
        out.append("frozen historical theorem denominator changed")
    if len(historical.get("baseline_targets", [])) != 298:
        out.append("frozen historical target denominator changed")

    status = load(STATUS)["quality_uplift_program"]["post_review_convergence"][
        "c6_current_semantic_overlay"
    ]
    if status.get("rationalization_ledger_path") != str(LEDGER.relative_to(ROOT)):
        out.append("status does not bind the rationalization ledger")
    if status.get("theorem_count") != 1369 or status.get("remaining_action_count") != 160:
        out.append("status does not report the post-transaction denominator")
    roadmap = ROADMAP.read_text(encoding="utf-8")
    for phrase in [
        "first dependency-safe retirement transaction",
        "all 1,369 live theorem",
        "160 rewrite-or-retire actions remain",
        "`proofs/proof_semantic_rationalization_ledger.json`",
    ]:
        if phrase not in roadmap:
            out.append(f"roadmap does not report the transaction: {phrase}")
    if ledger["support_state_effect"] != "none" or ledger["release_effect"] != "none":
        out.append("rationalization transaction changed support or release state")
    return out


def main() -> None:
    ledger = load(LEDGER)
    failures = validation_errors(ledger)
    mutations: list[tuple[str, dict[str, Any]]] = []

    def mutate(label: str, fn: Any) -> None:
        candidate = copy.deepcopy(ledger)
        fn(candidate)
        mutations.append((label, candidate))

    mutate("baseline commit substitution", lambda c: c["baseline"].__setitem__("commit", "0" * 40))
    mutate("overlay digest substitution", lambda c: c["baseline"].__setitem__("overlay_sha256", "0" * 64))
    mutate("module digest substitution", lambda c: c["baseline"].__setitem__("module_sha256", "0" * 64))
    mutate("retired identity substitution", lambda c: c["actions"][0].__setitem__("retired_theorem_id", c["actions"][0]["retained_theorem_id"]))
    mutate("retained identity substitution", lambda c: c["actions"][0].__setitem__("retained_theorem_id", c["actions"][0]["retired_theorem_id"]))
    mutate("normalized statement substitution", lambda c: c["actions"][0].__setitem__("normalized_statement_sha256", "0" * 64))
    mutate("dependency laundering", lambda c: c["actions"][0]["dependency_check"]["retired_theorem_dependency_refs"].append("theorem:x"))
    mutate("consumer laundering", lambda c: c["actions"][0]["dependency_check"]["retired_theorem_consumer_refs"].append("theorem:x"))
    mutate("remaining denominator inflation", lambda c: c["summary"].__setitem__("remaining_action_count", 161))
    mutate("support promotion", lambda c: c.__setitem__("support_state_effect", "promotion"))

    for label, candidate in mutations:
        if not validation_errors(candidate, check_files=False):
            failures.append(f"negative mutation accepted: {label}")
    if failures:
        raise SystemExit(
            "Proof semantic-rationalization ledger validation failed:\n - "
            + "\n - ".join(failures)
        )
    print(
        "Proof semantic-rationalization ledger passed: one exact same-model duplicate "
        "retired, canonical theorem retained, 1,369 live theorems, 160 actions remain, "
        "10 rejecting mutations, no support or release effect."
    )


if __name__ == "__main__":
    main()
