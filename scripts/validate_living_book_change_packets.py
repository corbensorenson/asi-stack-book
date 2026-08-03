#!/usr/bin/env python3
"""Validate synthetic living-book change-packet records.

The harness checks record discipline only. It does not approve releases,
manuscript quality, source interpretation, reader artifacts, or support-state
movement.
"""

from __future__ import annotations

import copy
import json
import re
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "living_book_change_packet.schema.json"
FIXTURE_DIR = ROOT / "experiments" / "living_book_change_packets" / "fixtures"
LEAN = ROOT / "lean" / "AsiStackProofs" / "LivingBook.lean"
REQUIRED_THEOREMS = {
    "manifest_chapter_missing_outline_targets_or_claim_placeholders_rejected",
    "structural_update_marked_valid_without_sync_artifacts_rejected",
}
LIFECYCLE_THEOREMS = {
    "number_manifest_preserves_length",
    "number_manifest_preserves_stable_id_order",
    "number_manifest_derives_consecutive_ordinals",
    "manifest_change_rejected_event_is_noninterfering",
    "manifest_change_step_preserves_custody",
    "run_manifest_change_preserves_custody",
    "manifest_change_step_preserves_invariant",
    "run_manifest_change_preserves_invariant",
    "run_manifest_change_append",
    "reference_manifest_change_reaches_accepted_current",
    "reference_manifest_change_has_no_support_or_publication_authority",
    "reference_manifest_change_has_exact_receipt_count",
    "missing_proof_manifest_sync_rejects_without_state_change",
    "duplicate_stable_ids_reject_structure_sync_without_state_change",
    "failed_render_rejects_validation_without_state_change",
    "accepted_manifest_change_is_absorbing_one_step",
    "rolled_back_manifest_change_is_absorbing_one_step",
    "accepted_manifest_change_is_absorbing_for_any_suffix",
    "rolled_back_manifest_change_is_absorbing_for_any_suffix",
    "manifest_thin_summary_collides_across_acceptance",
    "no_manifest_thin_summary_classifier_recovers_acceptance",
}
LEAN_ROOT = ROOT / "lean"
REFERENCE_EVENTS = (
    ("structure", 701, 801, 84, True),
    ("evidence", 701, True, True, True),
    ("validate", 701, True, True),
    ("accept", 701, True, True),
)
LIFECYCLE_EVENTS = (
    *REFERENCE_EVENTS,
    ("structure", 999, 801, 84, True),
    ("structure", 701, 999, 84, True),
    ("structure", 701, 801, 83, True),
    ("structure", 701, 801, 84, False),
    ("evidence", 701, False, True, True),
    ("evidence", 701, True, False, True),
    ("evidence", 701, True, True, False),
    ("validate", 701, False, True),
    ("validate", 701, True, False),
    ("accept", 701, False, True),
    ("accept", 701, True, False),
    ("rollback", 701, True),
    ("rollback", 999, True),
    ("rollback", 701, False),
)

PUBLIC_SURFACE_PACKET_TYPES = {
    "chapter_revision",
    "outline_only",
    "proof_manifest_shift",
    "reader_edition_generation",
    "source_ingestion",
    "schema_fixture_update",
    "evidence_transition_review",
}
DERIVED_RELEASE_TARGETS = {"reader_source", "reader_format", "audio_script"}
CHANGELOG_PACKET_TYPES = {
    "chapter_revision",
    "outline_only",
    "proof_manifest_shift",
    "reader_edition_generation",
    "source_ingestion",
    "schema_fixture_update",
    "evidence_transition_review",
}
PROMOTION_EFFECTS = {"eligible_for_review", "upward_transition"}
BOUNDARY_REQUIRED_TERMS = {"not equal authority", "derived", "projection", "not approved", "not release"}
NON_CLAIM_TERMS = {"no support-state promotion", "does not promote", "not support-state promotion"}
RENDER_COMMAND_TERMS = {"quarto render", "validate_live_human_view"}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def type_ok(value: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    return True


def validate_value(value: Any, schema: dict[str, Any], path: str) -> list[str]:
    errors: list[str] = []
    expected_type = schema.get("type")
    if expected_type and not type_ok(value, expected_type):
        return [f"{path}: expected {expected_type}, got {type(value).__name__}"]

    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: value {value!r} not in enum {schema['enum']!r}")

    if expected_type == "string" and schema.get("minLength", 0) > len(value):
        errors.append(f"{path}: string shorter than minLength {schema['minLength']}")

    if expected_type == "array":
        item_schema = schema.get("items", {})
        for index, item in enumerate(value):
            errors.extend(validate_value(item, item_schema, f"{path}[{index}]"))

    if expected_type == "object":
        required = schema.get("required", [])
        for key in required:
            if key not in value:
                errors.append(f"{path}: missing required key {key!r}")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            for key in value:
                if key not in properties:
                    errors.append(f"{path}: unexpected key {key!r}")
        for key, child_schema in properties.items():
            if key in value:
                errors.extend(validate_value(value[key], child_schema, f"{path}.{key}"))

    return errors


def has_any(text: str, needles: set[str]) -> bool:
    lowered = text.lower()
    return any(needle in lowered for needle in needles)


def joined(values: list[str]) -> str:
    return " ".join(str(value) for value in values)


def semantic_errors(record: dict[str, Any], relative: str) -> list[str]:
    errors: list[str] = []

    packet_id = str(record.get("packet_id", ""))
    packet_type = str(record.get("packet_type", ""))
    release_target = str(record.get("release_target", ""))
    validation_status = str(record.get("validation_status", ""))
    render_result = str(record.get("render_result", ""))
    support_state_effect = str(record.get("support_state_effect", ""))
    boundary = str(record.get("derived_artifact_boundary", ""))
    commands = record.get("validation_commands", [])
    changelog_refs = record.get("changelog_refs", [])
    evidence_refs = record.get("evidence_transition_refs", [])
    residuals = record.get("residuals", [])
    non_claims = record.get("non_claims", [])

    commands_text = joined(commands).lower() if isinstance(commands, list) else ""
    non_claims_text = joined(non_claims).lower() if isinstance(non_claims, list) else ""
    residuals_text = joined(residuals).lower() if isinstance(residuals, list) else ""

    if not packet_id.startswith("change-packet://"):
        errors.append(f"{relative}: packet_id must use change-packet:// identity.")

    if packet_type in PUBLIC_SURFACE_PACKET_TYPES and not changelog_refs:
        errors.append(f"{relative}: public-surface change packets must name changelog_refs.")

    if validation_status == "pass" and not commands:
        errors.append(f"{relative}: passing change packets must record validation_commands.")

    if render_result == "pass" and not has_any(commands_text, RENDER_COMMAND_TERMS):
        errors.append(f"{relative}: render_result pass requires a render or live-view validation command.")

    if release_target in DERIVED_RELEASE_TARGETS:
        if not has_any(boundary, BOUNDARY_REQUIRED_TERMS):
            errors.append(f"{relative}: derived reader/audio targets must state a non-equal-authority or non-approval boundary.")
        if "equal authority" in boundary.lower() and "not equal authority" not in boundary.lower():
            errors.append(f"{relative}: reader/audio derivatives cannot be equal authority to the live book.")

    if support_state_effect in PROMOTION_EFFECTS and not evidence_refs:
        errors.append(f"{relative}: promotion-eligible effects require evidence_transition_refs.")

    if support_state_effect == "upward_transition" and "accepted evidence transition" not in joined(evidence_refs).lower():
        errors.append(f"{relative}: upward transitions require an accepted evidence transition reference.")

    if not non_claims:
        errors.append(f"{relative}: change packets must preserve explicit non_claims.")
    elif not has_any(non_claims_text, NON_CLAIM_TERMS) and support_state_effect != "blocks_promotion":
        errors.append(f"{relative}: non_claims must state the support-state promotion boundary.")

    if validation_status in {"fail", "blocked", "partial", "pending"} and not residuals:
        errors.append(f"{relative}: incomplete or blocked change packets must name residuals.")

    if validation_status == "blocked" and "blocked" not in residuals_text:
        errors.append(f"{relative}: blocked change packets must name the blocked condition in residuals.")

    return errors


def number_manifest(chapters: list[dict[str, int]], start: int = 1) -> list[dict[str, int]]:
    return [
        {
            "ordinal": start + offset,
            "stable_id": chapter["stable_id"],
            "part_id": chapter["part_id"],
            "title_digest": chapter["title_digest"],
        }
        for offset, chapter in enumerate(chapters)
    ]


def consecutive_ordinals(rows: list[dict[str, int]], start: int = 1) -> bool:
    return all(row["ordinal"] == start + offset for offset, row in enumerate(rows))


def reference_change() -> dict[str, Any]:
    return {
        "stage": "proposed",
        "change_digest": 701,
        "expected_change_digest": 701,
        "prior_manifest_digest": 800,
        "candidate_manifest_digest": 801,
        "expected_candidate_manifest_digest": 801,
        "prior_chapter_count": 83,
        "candidate_chapter_count": 84,
        "rendered_chapter_count": 0,
        "stable_ids_unique": False,
        "scaffold_synced": False,
        "outline_synced": False,
        "proof_manifest_synced": False,
        "source_matrix_synced": False,
        "render_validated": False,
        "validators_passed": False,
        "changelog_recorded": False,
        "non_claims_recorded": False,
        "receipts": 0,
        "authority_ceiling": 1,
        "expected_authority_ceiling": 1,
        "support_assignments": 0,
        "publication_effects": 0,
    }


def change_step(state: dict[str, Any], event: tuple[Any, ...]) -> tuple[str, dict[str, Any]]:
    kind, *args = event
    next_state = copy.deepcopy(state)
    accepted = False
    if kind == "structure":
        change, candidate, rendered, unique = args
        accepted = (
            state["stage"] == "proposed"
            and change == state["change_digest"]
            and candidate == state["candidate_manifest_digest"]
            and candidate == state["expected_candidate_manifest_digest"]
            and rendered == state["candidate_chapter_count"]
            and unique is True
        )
        if accepted:
            next_state.update(
                stage="structure_synced",
                rendered_chapter_count=rendered,
                stable_ids_unique=True,
                scaffold_synced=True,
            )
    elif kind == "evidence":
        change, outline, proof_manifest, source_matrix = args
        accepted = (
            state["stage"] == "structure_synced"
            and change == state["change_digest"]
            and outline is True
            and proof_manifest is True
            and source_matrix is True
        )
        if accepted:
            next_state.update(
                stage="evidence_synced",
                outline_synced=True,
                proof_manifest_synced=True,
                source_matrix_synced=True,
            )
    elif kind == "validate":
        change, render_passed, validators_passed = args
        accepted = (
            state["stage"] == "evidence_synced"
            and change == state["change_digest"]
            and render_passed is True
            and validators_passed is True
        )
        if accepted:
            next_state.update(
                stage="validated",
                render_validated=True,
                validators_passed=True,
            )
    elif kind == "accept":
        change, changelog, non_claims = args
        accepted = (
            state["stage"] == "validated"
            and change == state["change_digest"]
            and changelog is True
            and non_claims is True
        )
        if accepted:
            next_state.update(
                stage="accepted_current",
                changelog_recorded=True,
                non_claims_recorded=True,
            )
    elif kind == "rollback":
        change, residual_owned = args
        accepted = (
            state["stage"] not in {"accepted_current", "rolled_back"}
            and change == state["change_digest"]
            and residual_owned is True
        )
        if accepted:
            next_state.update(
                stage="rolled_back",
                candidate_manifest_digest=state["prior_manifest_digest"],
                expected_candidate_manifest_digest=state["prior_manifest_digest"],
                candidate_chapter_count=state["prior_chapter_count"],
                rendered_chapter_count=state["prior_chapter_count"],
            )
    else:
        raise ValueError(f"unknown manifest change event: {event}")
    if accepted:
        next_state["receipts"] += 1
        return "accepted", next_state
    return "rejected", copy.deepcopy(state)


def run_change(state: dict[str, Any], events: tuple[tuple[Any, ...], ...]) -> dict[str, Any]:
    current = copy.deepcopy(state)
    for event in events:
        _, current = change_step(current, event)
    return current


def change_custody(state: dict[str, Any]) -> bool:
    return (
        state["change_digest"] == state["expected_change_digest"]
        and state["candidate_manifest_digest"] == state["expected_candidate_manifest_digest"]
        and state["authority_ceiling"] == state["expected_authority_ceiling"]
    )


def change_invariant(state: dict[str, Any]) -> bool:
    if not change_custody(state):
        return False
    if state["support_assignments"] != 0 or state["publication_effects"] != 0:
        return False
    structural = (
        state["stable_ids_unique"] is True
        and state["scaffold_synced"] is True
        and state["rendered_chapter_count"] == state["candidate_chapter_count"]
    )
    evidence = (
        state["outline_synced"] is True
        and state["proof_manifest_synced"] is True
        and state["source_matrix_synced"] is True
    )
    validated = state["render_validated"] is True and state["validators_passed"] is True
    accepted = state["changelog_recorded"] is True and state["non_claims_recorded"] is True
    required = {
        "proposed": True,
        "structure_synced": structural,
        "evidence_synced": structural and evidence,
        "validated": structural and evidence and validated,
        "accepted_current": structural and evidence and validated and accepted,
        "rolled_back": True,
    }
    return required[state["stage"]]


def state_key(state: dict[str, Any]) -> tuple[Any, ...]:
    return tuple(state[key] for key in state)


def explore_changes(root: dict[str, Any]) -> dict[tuple[Any, ...], dict[str, Any]]:
    reachable = {state_key(root): copy.deepcopy(root)}
    frontier = list(reachable.values())
    while frontier:
        state = frontier.pop()
        for event in LIFECYCLE_EVENTS:
            _, next_state = change_step(state, event)
            key = state_key(next_state)
            if key not in reachable:
                reachable[key] = next_state
                frontier.append(next_state)
    return reachable


def validate_formal_lifecycle(errors: list[str]) -> dict[str, int]:
    lean_text = LEAN.read_text(encoding="utf-8")
    theorem_names = set(re.findall(r"(?m)^theorem\s+([A-Za-z_][A-Za-z0-9_']*)", lean_text))
    missing = sorted((REQUIRED_THEOREMS | LIFECYCLE_THEOREMS) - theorem_names)
    if missing:
        errors.append(f"{LEAN.relative_to(ROOT)} missing theorem(s): {missing}")
    if len(theorem_names) != 39:
        errors.append(f"LivingBook theorem count must be 39, observed {len(theorem_names)}")
    completed = subprocess.run(
        ["lake", "env", "lean", "AsiStackProofs/LivingBook.lean"],
        cwd=LEAN_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        errors.append(f"LivingBook Lean compilation failed: {completed.stdout}{completed.stderr}")

    chapters = [
        {"stable_id": 10, "part_id": 1, "title_digest": 101},
        {"stable_id": 20, "part_id": 1, "title_digest": 202},
        {"stable_id": 30, "part_id": 2, "title_digest": 303},
    ]
    inserted = chapters[:1] + [{"stable_id": 15, "part_id": 1, "title_digest": 151}] + chapters[1:]
    numbered = number_manifest(inserted)
    if [row["stable_id"] for row in numbered] != [10, 15, 20, 30]:
        errors.append("manifest numbering changed stable chapter identity or order")
    if not consecutive_ordinals(numbered) or [row["ordinal"] for row in numbered] != [1, 2, 3, 4]:
        errors.append("manifest numbering did not derive contiguous ordinals after insertion")

    initial = reference_change()
    final = run_change(initial, REFERENCE_EVENTS)
    if final["stage"] != "accepted_current" or final["receipts"] != 4:
        errors.append("reference manifest change did not reach exact accepted-current state")
    if final["support_assignments"] != 0 or final["publication_effects"] != 0:
        errors.append("reference manifest change gained support or publication authority")

    split_count = 0
    for index in range(len(REFERENCE_EVENTS) + 1):
        left = REFERENCE_EVENTS[:index]
        right = REFERENCE_EVENTS[index:]
        if run_change(initial, REFERENCE_EVENTS) != run_change(run_change(initial, left), right):
            errors.append(f"manifest lifecycle composition failed at split {index}")
        else:
            split_count += 1

    reachable = explore_changes(initial)
    transition_count = 0
    rejection_count = 0
    terminal_states: list[dict[str, Any]] = []
    custody_fields = (
        "change_digest",
        "expected_change_digest",
        "prior_manifest_digest",
        "prior_chapter_count",
        "authority_ceiling",
        "expected_authority_ceiling",
        "support_assignments",
        "publication_effects",
    )
    for state in reachable.values():
        if not change_invariant(state):
            errors.append(f"reachable manifest change violates invariant: {state}")
        if state["stage"] in {"accepted_current", "rolled_back"}:
            terminal_states.append(state)
        for event in LIFECYCLE_EVENTS:
            transition_count += 1
            route, next_state = change_step(state, event)
            if any(next_state[field] != state[field] for field in custody_fields):
                errors.append(f"manifest custody changed through {state['stage']}:{event[0]}")
            if change_invariant(state) and not change_invariant(next_state):
                errors.append(f"manifest invariant failed through {state['stage']}:{event[0]}")
            if route == "rejected":
                rejection_count += 1
                if next_state != state:
                    errors.append(f"rejected manifest event changed state: {state['stage']}:{event}")

    absorbing_transitions = 0
    for state in terminal_states:
        for event in LIFECYCLE_EVENTS:
            absorbing_transitions += 1
            _, next_state = change_step(state, event)
            if next_state != state:
                errors.append(f"terminal manifest state reopened through {event}")

    semantic_mutations = 0
    for field in (
        "change_digest",
        "candidate_manifest_digest",
        "authority_ceiling",
        "support_assignments",
        "publication_effects",
    ):
        mutation = copy.deepcopy(final)
        mutation[field] += 1
        if change_invariant(mutation):
            errors.append(f"manifest lifecycle mutation was not detected for {field}")
        else:
            semantic_mutations += 1
    for field in (
        "stable_ids_unique",
        "scaffold_synced",
        "outline_synced",
        "proof_manifest_synced",
        "source_matrix_synced",
        "render_validated",
        "validators_passed",
        "changelog_recorded",
        "non_claims_recorded",
    ):
        mutation = copy.deepcopy(final)
        mutation[field] = False
        if change_invariant(mutation):
            errors.append(f"manifest stage-coherence mutation was not detected for {field}")
        else:
            semantic_mutations += 1
    ordinal_mutation = copy.deepcopy(numbered)
    ordinal_mutation[2]["ordinal"] = ordinal_mutation[1]["ordinal"]
    if consecutive_ordinals(ordinal_mutation):
        errors.append("duplicate manifest ordinal mutation was not detected")
    else:
        semantic_mutations += 1

    if (final["candidate_manifest_digest"], final["candidate_chapter_count"]) != (
        initial["candidate_manifest_digest"],
        initial["candidate_chapter_count"],
    ) or final["stage"] == initial["stage"]:
        errors.append("manifest thin-summary collision witness drifted")

    return {
        "trace_splits": split_count,
        "reachable_states": len(reachable),
        "transitions": transition_count,
        "rejections": rejection_count,
        "terminal_states": len(terminal_states),
        "absorbing_transitions": absorbing_transitions,
        "semantic_mutations": semantic_mutations,
    }


def main() -> None:
    schema = load_json(SCHEMA_PATH)
    errors: list[str] = []
    valid_count = 0
    invalid_count = 0

    fixture_paths = sorted(FIXTURE_DIR.glob("*.json"))
    if not fixture_paths:
        raise SystemExit("No living-book change-packet fixtures found.")

    for path in fixture_paths:
        relative = str(path.relative_to(ROOT))
        record = load_json(path)
        record_errors = validate_value(record, schema, relative)
        if not record_errors:
            record_errors.extend(semantic_errors(record, relative))

        expect_invalid = path.name.startswith("invalid_")
        if expect_invalid:
            invalid_count += 1
            if not record_errors:
                errors.append(f"{relative}: expected-invalid fixture unexpectedly passed.")
        else:
            valid_count += 1
            errors.extend(record_errors)

    if valid_count != 3:
        errors.append(f"Expected exactly 3 valid fixtures, found {valid_count}.")
    if invalid_count != 6:
        errors.append(f"Expected exactly 6 expected-invalid fixtures, found {invalid_count}.")

    lifecycle = validate_formal_lifecycle(errors)

    if errors:
        for error in errors:
            print(error)
        raise SystemExit(1)

    print(
        "Living-book change-packet harness passed: "
        f"{valid_count} valid fixture(s), {invalid_count} expected-invalid fixture(s), "
        "39 Lean declarations, "
        f"{lifecycle['trace_splits']}/5 trace splits, {lifecycle['reachable_states']} reachable states "
        f"through {lifecycle['transitions']} transitions ({lifecycle['rejections']} rejections), "
        f"{lifecycle['terminal_states']} terminal states through "
        f"{lifecycle['absorbing_transitions']} absorbing transitions, and "
        f"{lifecycle['semantic_mutations']} semantic mutations."
    )


if __name__ == "__main__":
    main()
