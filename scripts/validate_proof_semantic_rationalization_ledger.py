#!/usr/bin/env python3
"""Validate cumulative dependency-safe C6 proof-rationalization transactions."""

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
MANIFEST = ROOT / "proofs" / "proof_manifest.json"
TRIAGE = ROOT / "proofs" / "proof_triage.json"
STATUS = ROOT / "roadmap_records" / "post_v2_3_maintenance_transfer_and_publication_status.json"
ROADMAP = ROOT / "docs" / "post_v2_3_maintenance_transfer_and_publication_roadmap.md"
THEOREM_START = re.compile(r"(?m)^theorem\s+([A-Za-z_][A-Za-z0-9_']*)\b")
DECL_START = re.compile(
    r"(?m)^(?:theorem|def|abbrev|structure|inductive|class|instance|namespace|end)\b"
)
EXPECTED_ACTION_IDS = [
    "C6-R1-scalable-oversight-same-model-duplicate",
    "C6-R2-bibliography-source-evidence-projection",
    "C6-R3-bibliography-chapter-assignment-projection",
]
EXPECTED_LEVELS = {
    "P0": 48,
    "P1": 799,
    "P2": 25,
    "P3": 319,
    "P4": 93,
    "P5": 83,
    "P6": 0,
}
EXPECTED_DISPOSITIONS = {
    "retain": 1209,
    "retire_narrow_projection": 61,
    "rewrite_scope_language": 2,
    "rewrite_with_stronger_model": 95,
}
EXPECTED_TARGETS = {
    "lean:bibliography.plan.operational_invariant": (
        "A source-derived claim with neither a source note nor an ingested artifact "
        "fails the finite source-evidence predicate."
    ),
    "lean:bibliography.plan.failure_blocks_promotion": (
        "An accepted new-source assignment to a nonexistent chapter fails the finite "
        "assignment predicate."
    ),
}


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
        signature = normalize(block.split(":= by", 1)[0])
        rows[match.group(1)] = {
            "block": block,
            "signature": signature,
            "statement_sha256": sha256_bytes(statement_key(signature).encode("utf-8")),
        }
    return rows


def schema_errors(ledger: dict[str, Any]) -> list[str]:
    try:
        jsonschema.Draft202012Validator(load(SCHEMA)).validate(ledger)
    except jsonschema.ValidationError as exc:
        return [f"schema: {exc.message}"]
    return []


def validation_errors(ledger: dict[str, Any], *, check_files: bool = True) -> list[str]:
    out = schema_errors(ledger)
    if out or not check_files:
        return out

    baseline = ledger["classification_baseline"]
    actions = ledger["actions"]
    if [row["action_id"] for row in actions] != EXPECTED_ACTION_IDS:
        out.append("action sequence or identity drifted")
    if [row["sequence"] for row in actions] != [1, 2, 3]:
        out.append("action sequence numbers drifted")

    try:
        baseline_overlay_bytes = git_show(baseline["commit"], baseline["overlay_path"])
    except subprocess.CalledProcessError as exc:
        return out + [f"immutable classification baseline cannot be read: {exc}"]
    if sha256_bytes(baseline_overlay_bytes) != baseline["overlay_sha256"]:
        out.append("classification-baseline overlay digest drifted")
    baseline_overlay = json.loads(baseline_overlay_bytes)
    baseline_rows = {
        row["theorem_id"]: row for row in baseline_overlay.get("records", [])
    }
    if len(baseline_rows) != baseline["live_theorem_count"]:
        out.append("classification-baseline theorem denominator drifted")
    if sum(row.get("disposition") != "retain" for row in baseline_rows.values()) != baseline[
        "rewrite_or_retire_count"
    ]:
        out.append("classification-baseline action denominator drifted")

    module_cache: dict[str, dict[str, dict[str, str]]] = {}
    module_bytes_cache: dict[str, bytes] = {}
    for action in actions:
        module = action["module_path"]
        retired_id = action["retired_theorem_id"]
        replacement_id = action["replacement_theorem_id"]
        if retired_id.split("::", 1)[0] != module or replacement_id.split("::", 1)[0] != module:
            out.append(f"{action['action_id']}: participants are not bound to one module")
            continue
        if module not in module_cache:
            try:
                module_bytes_cache[module] = git_show(baseline["commit"], module)
            except subprocess.CalledProcessError as exc:
                out.append(f"{action['action_id']}: baseline module cannot be read: {exc}")
                continue
            module_cache[module] = theorem_blocks(module_bytes_cache[module].decode("utf-8"))
        if sha256_bytes(module_bytes_cache[module]) != action["baseline_module_sha256"]:
            out.append(f"{action['action_id']}: baseline module digest drifted")
        retired_name = retired_id.split("::", 1)[1]
        replacement_name = replacement_id.split("::", 1)[1]
        retired_block = module_cache[module].get(retired_name)
        replacement_block = module_cache[module].get(replacement_name)
        if retired_block is None or replacement_block is None:
            out.append(f"{action['action_id']}: baseline theorem block is missing")
            continue
        if sha256_bytes(retired_block["block"].encode("utf-8")) != action["retired_block_sha256"]:
            out.append(f"{action['action_id']}: retired block digest drifted")
        if sha256_bytes(replacement_block["block"].encode("utf-8")) != action[
            "replacement_block_sha256"
        ]:
            out.append(f"{action['action_id']}: replacement block digest drifted")
        if retired_block["statement_sha256"] != action["retired_statement_sha256"]:
            out.append(f"{action['action_id']}: retired statement digest drifted")
        if replacement_block["statement_sha256"] != action["replacement_statement_sha256"]:
            out.append(f"{action['action_id']}: replacement statement digest drifted")

        retired_row = baseline_rows.get(retired_id)
        replacement_row = baseline_rows.get(replacement_id)
        if retired_row is None or replacement_row is None:
            out.append(f"{action['action_id']}: classification baseline lacks a participant")
            continue
        expected_disposition = (
            "retire_duplicate"
            if action["action"] == "retire_exact_same_model_duplicate"
            else "retire_narrow_projection"
        )
        if retired_row.get("disposition") != expected_disposition:
            out.append(f"{action['action_id']}: baseline retirement disposition drifted")
        if replacement_row.get("disposition") != "retain":
            out.append(f"{action['action_id']}: replacement was not retained at baseline")
        if retired_row.get("theorem_dependency_refs") != []:
            out.append(f"{action['action_id']}: retired theorem had theorem dependencies")
        if retired_row.get("theorem_consumer_refs") != []:
            out.append(f"{action['action_id']}: retired theorem had theorem consumers")

        if action["action"] == "retire_exact_same_model_duplicate":
            if statement_key(retired_block["signature"]) != statement_key(
                replacement_block["signature"]
            ):
                out.append(f"{action['action_id']}: exact duplicate statements differ")
            if action["target_migrations"] != []:
                out.append(f"{action['action_id']}: exact duplicate invented a target migration")
        else:
            if "exact valid" not in retired_block["block"]:
                out.append(f"{action['action_id']}: retired theorem is not the audited projection")
            if "have " not in replacement_block["block"] or "rw [" not in replacement_block["block"]:
                out.append(f"{action['action_id']}: replacement lacks derived counterexample steps")
            if len(action["target_migrations"]) != 1:
                out.append(f"{action['action_id']}: projection target migration is not singular")

    current_rows = current_theorems()
    current_ids = {row["theorem_id"] for row in current_rows}
    _, current_consumers = theorem_graph(current_rows)
    for action in actions:
        if action["retired_theorem_id"] in current_ids:
            out.append(f"{action['action_id']}: retired theorem remains live")
        if action["replacement_theorem_id"] not in current_ids:
            out.append(f"{action['action_id']}: replacement theorem is not live")
        if current_consumers.get(action["retired_theorem_id"], []):
            out.append(f"{action['action_id']}: retired theorem has a current Lean consumer")

    overlay = load(CURRENT_OVERLAY)
    summary = overlay.get("summary", {})
    if summary.get("current_theorem_count") != 1367:
        out.append("current theorem denominator drifted")
    if summary.get("semantic_level_counts") != EXPECTED_LEVELS:
        out.append("current semantic-level counts drifted")
    if summary.get("disposition_counts") != EXPECTED_DISPOSITIONS:
        out.append("current disposition counts drifted")
    if sum(value for key, value in EXPECTED_DISPOSITIONS.items() if key != "retain") != 158:
        out.append("expected remaining-action denominator is internally inconsistent")
    if ledger["summary"]["remaining_action_counts"] != {
        key: value for key, value in EXPECTED_DISPOSITIONS.items() if key != "retain"
    }:
        out.append("ledger remaining-action family counts drifted")
    if summary.get("duplicate_group_count") != 0:
        out.append("same-model exact duplicate group remains")

    bibliography_rows = [
        row
        for row in current_rows
        if row["module_path"] == "lean/AsiStackProofs/BibliographyPlan.lean"
    ]
    if len(bibliography_rows) != 2:
        out.append("BibliographyPlan must retain exactly the two derived counterexample theorems")
    if any(row.get("depth_class") != "derived_or_decomposed" for row in bibliography_rows):
        out.append("BibliographyPlan retained a direct projection")

    manifest_rows = {
        row["tag"]: row
        for row in load(MANIFEST).get("records", [])
        if row.get("module") == "AsiStackProofs.BibliographyPlan"
    }
    for target, expected in EXPECTED_TARGETS.items():
        if manifest_rows.get(target, {}).get("formal_target") != expected:
            out.append(f"proof target did not migrate to the counterexample gate: {target}")
    triage_rows = {row["tag"]: row for row in load(TRIAGE).get("records", [])}
    for target, expected in EXPECTED_TARGETS.items():
        if triage_rows.get(target, {}).get("formal_target") != expected:
            out.append(f"proof triage did not migrate to the counterexample gate: {target}")
    for path in [
        ROOT / "book_structure.json",
        ROOT / "docs/book_outline.md",
        ROOT / "chapters/open-research-agenda-and-bibliography-plan.qmd",
    ]:
        text = path.read_text(encoding="utf-8")
        for expected in EXPECTED_TARGETS.values():
            if expected not in text:
                out.append(f"{path.relative_to(ROOT)} lacks a migrated target")

    historical = load(HISTORICAL)
    if len(historical.get("baseline_theorems", [])) != 1151:
        out.append("frozen historical theorem denominator changed")
    if len(historical.get("baseline_targets", [])) != 298:
        out.append("frozen historical target denominator changed")

    status = load(STATUS)["quality_uplift_program"]["post_review_convergence"][
        "c6_current_semantic_overlay"
    ]
    if status.get("rationalization_ledger_path") != str(LEDGER.relative_to(ROOT)):
        out.append("status does not bind the cumulative rationalization ledger")
    if (
        status.get("theorem_count") != 1367
        or status.get("executed_retirement_count") != 3
        or status.get("remaining_action_count") != 158
    ):
        out.append("status does not report the cumulative post-transaction denominator")
    roadmap = ROADMAP.read_text(encoding="utf-8")
    roadmap_flat = " ".join(roadmap.split())
    for phrase in [
        "first narrow-projection tranche",
        "1,367 live theorem declarations",
        "158 rewrite-or-retire actions remain",
        "`proofs/proof_semantic_rationalization_ledger.json`",
    ]:
        if phrase not in roadmap_flat:
            out.append(f"roadmap does not report the cumulative transaction: {phrase}")
    if ledger["support_state_effect"] != "none" or ledger["release_effect"] != "none":
        out.append("rationalization transactions changed support or release state")
    return out


def main() -> None:
    ledger = load(LEDGER)
    failures = validation_errors(ledger)
    mutations: list[tuple[str, dict[str, Any]]] = []

    def mutate(label: str, fn: Any) -> None:
        candidate = copy.deepcopy(ledger)
        fn(candidate)
        mutations.append((label, candidate))

    mutate("baseline commit substitution", lambda c: c["classification_baseline"].__setitem__("commit", "0" * 40))
    mutate("overlay digest substitution", lambda c: c["classification_baseline"].__setitem__("overlay_sha256", "0" * 64))
    mutate("action deletion", lambda c: c["actions"].pop())
    mutate("action reordering", lambda c: c["actions"].reverse())
    mutate("retired identity substitution", lambda c: c["actions"][1].__setitem__("retired_theorem_id", c["actions"][1]["replacement_theorem_id"]))
    mutate("replacement identity substitution", lambda c: c["actions"][2].__setitem__("replacement_theorem_id", c["actions"][2]["retired_theorem_id"]))
    mutate("statement substitution", lambda c: c["actions"][1].__setitem__("retired_statement_sha256", "0" * 64))
    mutate("dependency laundering", lambda c: c["actions"][1]["dependency_check"]["retired_theorem_dependency_refs"].append("theorem:x"))
    mutate("consumer laundering", lambda c: c["actions"][2]["dependency_check"]["retired_theorem_consumer_refs"].append("theorem:x"))
    mutate("target migration erasure", lambda c: c["actions"][1].__setitem__("target_migrations", []))
    mutate("remaining denominator inflation", lambda c: c["summary"].__setitem__("remaining_action_count", 159))
    mutate("support promotion", lambda c: c.__setitem__("support_state_effect", "promotion"))

    for label, candidate in mutations:
        if not validation_errors(candidate):
            failures.append(f"negative mutation accepted: {label}")
    if failures:
        raise SystemExit(
            "Proof semantic-rationalization ledger validation failed:\n - "
            + "\n - ".join(failures)
        )
    print(
        "Proof semantic-rationalization ledger passed: three dependency-safe "
        "retirements, two counterexample target migrations, 1,367 live theorems, "
        "158 actions remain, 12 rejecting mutations, no support or release effect."
    )


if __name__ == "__main__":
    main()
