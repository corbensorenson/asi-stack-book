#!/usr/bin/env python3
"""Project the Authority grant-to-effect refinement into manifest and triage."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STRUCTURE = ROOT / "book_structure.json"
TRIAGE = ROOT / "proofs/proof_triage.json"
TARGETS = {
    "lean:authority.ceiling.operational_invariant": "Every accepted issuance, dispatch, and effect in the finite reachable grant model remains within the caller ceiling and exactly binds grant ID, principal, operation, target, epoch, expiry, remaining uses, approval, dispatch, and effect custody.",
    "lean:authority.ceiling.failure_blocks_promotion": "The reachable model and independent consumer reject authority widening, confused-deputy substitution, stale or expired grants, missing approval/dispatch/effect receipts, post-revocation dispatch, effect without dispatch, and consumed one-shot reuse.",
}


def main() -> None:
    value = json.loads(STRUCTURE.read_text(encoding="utf-8"))
    chapter = next(ch for part in value["parts"] for ch in part["chapters"] if ch["id"] == "system-boundaries-and-authority")
    for target in chapter["proof_targets"]:
        if target["tag"] in TARGETS:
            target["target"] = TARGETS[target["tag"]]
            target["module"] = "AsiStackProofs.AuthorityEffectRefinement"
    if not any(test.get("name") == "Executed Authority grant-to-effect refinement" for test in chapter["codex_tests"]):
        chapter["codex_tests"].append({
            "name": "Executed Authority grant-to-effect refinement",
            "purpose": "Refine exact grant binding, ceiling, epoch, expiry, approval, dispatch, effect observation, revocation, one-shot use, and rollback against existing executed local evidence.",
            "implementation_status": "implemented",
            "result_status": "passes via `python3 scripts/validate_authority_effect_refinement.py`: 6 authority fixtures, 6 reachable events, 1 executed effect, 1 independent observation, 1 exact rollback, 2 pre-effect denials, 5 revocation entries, 9 governed scenarios, and 38/38 rejected mutations; support-state effect none",
            "status": "implemented bounded local refinement; no authentic identity/receipt, deployed authorization, concurrent revocation, production security, reproduction, transfer, safety, or chapter-core support claim",
        })
    STRUCTURE.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")

    triage = json.loads(TRIAGE.read_text(encoding="utf-8"))
    for target in triage["records"]:
        if target.get("tag") in TARGETS:
            target["formal_target"] = TARGETS[target["tag"]]
            target["module"] = "AsiStackProofs.AuthorityEffectRefinement"
            target["rationale"] = "Replaced the weaker target owner with a reachable grant-to-effect transition model and an independent consumer over executed effect, denial, revocation, authority-fixture, and governed-repository evidence plus 38 rejecting mutations; support-state effect remains none."
    TRIAGE.write_text(json.dumps(triage, indent=2) + "\n", encoding="utf-8")
    print("Integrated two Authority proof targets and one executed refinement test.")


if __name__ == "__main__":
    main()
