#!/usr/bin/env python3
"""Validate runtime-log linkage and Lean alignment for four trace invariants."""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

from build_canonical_public_status import validate_against_schema
from run_governed_trace_invariants import (
    NON_CLAIMS,
    RESULT,
    ROOT,
    SOURCE,
    build_result,
    sha256_file,
)


SCHEMA = ROOT / "schemas" / "governed_trace_invariants_result.schema.json"
LEAN = ROOT / "lean" / "AsiStackProofs" / "GovernedRepositoryTrace.lean"
LEAN_ROOT = ROOT / "lean" / "AsiStackProofs.lean"
DOC = ROOT / "docs" / "governed_trace_invariants.md"
CHAPTER = ROOT / "chapters" / "integrated-reference-architecture.qmd"
OUTLINE = ROOT / "docs" / "book_outline.md"
MANIFEST = ROOT / "book_structure.json"
PROOF_TAG = "lean:reference_architecture.governed_trace.four_invariants"
THEOREMS = {
    "governed_fixture_authority_monotone",
    "governed_fixture_revocation_before_effect",
    "governed_fixture_evidence_integrity",
    "governed_fixture_residual_conserved",
    "governed_repository_trace_four_invariants",
    "authority_widening_negative_rejected",
    "effect_at_revocation_time_negative_rejected",
    "unrecorded_promotion_negative_rejected",
    "erased_open_residual_negative_rejected",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def require_fragments(path: Path, fragments: set[str], errors: list[str]) -> None:
    if not path.exists():
        errors.append(f"missing {path.relative_to(ROOT)}")
        return
    text = path.read_text(encoding="utf-8", errors="ignore")
    for fragment in sorted(fragments):
        if fragment not in text:
            errors.append(f"{path.relative_to(ROOT)} missing {fragment!r}")


def main() -> None:
    errors: list[str] = []
    for path in (SOURCE, RESULT, SCHEMA, LEAN, LEAN_ROOT, DOC, CHAPTER, OUTLINE, MANIFEST):
        if not path.exists():
            errors.append(f"missing {path.relative_to(ROOT)}")
    if errors:
        fail(errors)
    source = load_json(SOURCE)
    tracked = load_json(RESULT)
    schema = load_json(SCHEMA)
    errors.extend(validate_against_schema(tracked, schema, str(RESULT.relative_to(ROOT))))
    expected = build_result(source)
    if tracked != expected:
        errors.append(
            f"{RESULT.relative_to(ROOT)} is stale; run "
            "python3 scripts/run_governed_trace_invariants.py --write-result"
        )
    if tracked.get("source_result_sha256") != sha256_file(SOURCE):
        errors.append("source result digest does not bind the current executed vertical-slice record")
    invariant_results = tracked.get("invariant_results", {})
    negative_controls = tracked.get("negative_controls", {})
    if set(invariant_results) != {
        "authority_monotonicity",
        "revocation_before_effect_with_tie_precedence",
        "evidence_transition_integrity",
        "residual_conservation",
        "causal_parent_order",
    } or not all(invariant_results.values()):
        errors.append("all five runtime trace checks, including the four named invariants, must pass")
    if set(negative_controls) != {
        "authority_scope_widening_rejected",
        "effect_at_revocation_time_rejected",
        "support_change_without_transition_rejected",
        "open_residual_erasure_rejected",
    } or not all(negative_controls.values()):
        errors.append("all four invariant mutation controls must be rejected")
    if len(tracked.get("authority_handoffs", [])) != 3:
        errors.append("expected three authority handoffs")
    if len(tracked.get("revocation_effect_attempts", [])) != 3:
        errors.append("expected three timed effect attempts")
    if len(tracked.get("evidence_events", [])) != 9:
        errors.append("expected one evidence event per executed vertical-slice scenario")
    residuals = tracked.get("residual_deltas", [])
    if sum(row.get("created", 0) for row in residuals) != 2:
        errors.append("expected two created residuals")
    if sum(row.get("discharged", 0) for row in residuals) != 1:
        errors.append("expected one discharged residual")
    if tracked.get("final_open_residuals") != 1:
        errors.append("failed rollback must preserve one final open residual")
    race = next(
        (row for row in tracked.get("revocation_effect_attempts", []) if row.get("event_id") == "revocation-effect-race"),
        {},
    )
    if race.get("logical_time") != race.get("revocation_time") or race.get("effect_observed") is not False:
        errors.append("revocation/effect tie must apply revocation-wins precedence and observe no effect")
    if tracked.get("support_state_effect") != "none" or tracked.get("non_claims") != NON_CLAIMS:
        errors.append("trace result must preserve exact no-promotion and non-claim boundaries")

    require_fragments(LEAN, THEOREMS | {"finalOpen : Nat", "logicalTime : Nat", "revocationTime : Nat"}, errors)
    require_fragments(LEAN_ROOT, {"import AsiStackProofs.GovernedRepositoryTrace"}, errors)
    require_fragments(
        DOC,
        {
            "## Authority monotonicity",
            "## Revocation before effect",
            "## Evidence-transition integrity",
            "## Residual conservation",
            "revocation wins ties",
            "one final open residual",
        },
        errors,
    )
    require_fragments(
        CHAPTER,
        {"Four trace invariants over one executed log", PROOF_TAG, "scripts/validate_governed_trace_invariants.py"},
        errors,
    )
    require_fragments(OUTLINE, {PROOF_TAG, "Governed cross-stack trace invariants test"}, errors)
    manifest = load_json(MANIFEST)
    chapter = next(
        chapter
        for part in manifest["parts"]
        for chapter in part["chapters"]
        if chapter["id"] == "integrated-reference-architecture"
    )
    proof_tags = {row["tag"] for row in chapter["proof_targets"]}
    test_names = {row["name"] for row in chapter["codex_tests"]}
    if PROOF_TAG not in proof_tags:
        errors.append("integrated-reference-architecture manifest is missing the governed trace proof target")
    if "Governed cross-stack trace invariants test" not in test_names:
        errors.append("integrated-reference-architecture manifest is missing the governed trace Codex test")
    fail(errors)
    print(
        "Governed trace invariant validation passed: 3 authority handoffs, 3 timed effects, "
        "9 evidence events, 2 residuals created, 1 discharged, 1 open; 4 mutation controls rejected."
    )


def fail(errors: list[str]) -> None:
    if not errors:
        return
    print("Governed trace invariant validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


if __name__ == "__main__":
    main()
