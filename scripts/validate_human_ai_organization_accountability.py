#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean" / "AsiStackProofs" / "HumanAIOrganizations.lean"
LEAN_ROOT = ROOT / "lean" / "AsiStackProofs.lean"
CHAPTER = ROOT / "chapters" / "human-ai-organizations-delegation-and-accountability.qmd"
DOSSIER = ROOT / "evidence_quality" / "proof_model_dossiers" / "human-ai-organizations-delegation-and-accountability.md"
MANIFEST = ROOT / "proofs" / "proof_manifest.json"
TRIAGE = ROOT / "proofs" / "proof_triage.json"
STRUCTURE = ROOT / "book_structure.json"
OUTLINE = ROOT / "docs" / "book_outline.md"

TAG = "lean:human_ai_org.accountability_requires_authority"
MODULE = "AsiStackProofs.HumanAIOrganizations"
FORMAL_TARGET = (
    "A five-stage finite review preserves staged capacity, authority, independence, and remedy "
    "invariants over arbitrary run length; assignable accountability requires all 20 authored "
    "fields, while 17 closed mutations reach exact repair states. It establishes no field truth, "
    "lawful accountability, human control, organizational outcome, support, or external effect."
)

BASE_RECORD = {
    "assignmentRequested": True,
    "decisionIdentityPresent": True,
    "accountableActorPresent": True,
    "informationAvailable": True,
    "competenceCurrent": True,
    "timeAvailable": True,
    "workloadWithinLimit": True,
    "decisionAuthorityPresent": True,
    "interventionAuthorityPresent": True,
    "practicalAbilityToChange": True,
    "revocationPathPresent": True,
    "independentReviewPresent": True,
    "separationOfDutiesPresent": True,
    "conflictDispositionPresent": True,
    "stopPathPresent": True,
    "appealPathPresent": True,
    "remedyPathPresent": True,
    "evidenceAccessPresent": True,
    "residualCustodyPresent": True,
    "nonClaimBoundaryPresent": True,
}

EXPECTED_MUTATIONS = {
    "assignmentRequested": "refusedNoAssignment",
    "decisionIdentityPresent": "repairDecisionIdentity",
    "accountableActorPresent": "repairActorIdentity",
    "informationAvailable": "repairInformation",
    "competenceCurrent": "repairCompetence",
    "timeAvailable": "repairTime",
    "workloadWithinLimit": "repairWorkload",
    "decisionAuthorityPresent": "repairDecisionAuthority",
    "interventionAuthorityPresent": "repairInterventionAuthority",
    "practicalAbilityToChange": "repairPracticalControl",
    "revocationPathPresent": "repairRevocation",
    "independentReviewPresent": "repairIndependentReview",
    "separationOfDutiesPresent": "repairSeparationOfDuties",
    "conflictDispositionPresent": "repairConflictDisposition",
    "stopPathPresent": "repairStopPath",
    "appealPathPresent": "repairAppealPath",
    "remedyPathPresent": "repairRemedyPath",
    "evidenceAccessPresent": "repairEvidenceAccess",
    "residualCustodyPresent": "repairResidualCustody",
    "nonClaimBoundaryPresent": "repairNonClaimBoundary",
}

REQUIRED_THEOREMS = {
    "accountability_review_step_preserves_stage_invariant",
    "accountability_review_run_preserves_stage_invariant",
    "assignable_accountability_requires_complete_authority_record",
    "complete_accountability_record_reaches_assignment",
    "missing_information_blocks_accountability_assignment",
    "missing_competence_blocks_accountability_assignment",
    "missing_time_blocks_accountability_assignment",
    "excessive_workload_blocks_accountability_assignment",
    "missing_decision_authority_blocks_accountability_assignment",
    "missing_intervention_authority_blocks_accountability_assignment",
    "missing_practical_control_blocks_accountability_assignment",
    "missing_revocation_blocks_accountability_assignment",
    "missing_independent_review_blocks_accountability_assignment",
    "collapsed_separation_of_duties_blocks_accountability_assignment",
    "undisposed_conflict_blocks_accountability_assignment",
    "missing_stop_path_blocks_accountability_assignment",
    "missing_appeal_blocks_accountability_assignment",
    "missing_remedy_blocks_accountability_assignment",
    "missing_evidence_access_blocks_accountability_assignment",
    "orphaned_residuals_block_accountability_assignment",
    "missing_non_claim_boundary_blocks_accountability_assignment",
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def step(record: dict[str, bool], state: str) -> str:
    if state == "proposed":
        checks = (
            ("assignmentRequested", "refusedNoAssignment"),
            ("decisionIdentityPresent", "repairDecisionIdentity"),
            ("accountableActorPresent", "repairActorIdentity"),
        )
        next_state = "capacityReview"
    elif state == "capacityReview":
        checks = (
            ("informationAvailable", "repairInformation"),
            ("competenceCurrent", "repairCompetence"),
            ("timeAvailable", "repairTime"),
            ("workloadWithinLimit", "repairWorkload"),
        )
        next_state = "authorityReview"
    elif state == "authorityReview":
        checks = (
            ("decisionAuthorityPresent", "repairDecisionAuthority"),
            ("interventionAuthorityPresent", "repairInterventionAuthority"),
            ("practicalAbilityToChange", "repairPracticalControl"),
            ("revocationPathPresent", "repairRevocation"),
        )
        next_state = "independenceReview"
    elif state == "independenceReview":
        checks = (
            ("independentReviewPresent", "repairIndependentReview"),
            ("separationOfDutiesPresent", "repairSeparationOfDuties"),
            ("conflictDispositionPresent", "repairConflictDisposition"),
        )
        next_state = "remedyReview"
    elif state == "remedyReview":
        checks = (
            ("stopPathPresent", "repairStopPath"),
            ("appealPathPresent", "repairAppealPath"),
            ("remedyPathPresent", "repairRemedyPath"),
            ("evidenceAccessPresent", "repairEvidenceAccess"),
            ("residualCustodyPresent", "repairResidualCustody"),
            ("nonClaimBoundaryPresent", "repairNonClaimBoundary"),
        )
        next_state = "accountabilityAssignable"
    else:
        return state
    for field, rejected_state in checks:
        if not record[field]:
            return rejected_state
    return next_state


def run(record: dict[str, bool], steps: int) -> str:
    state = "proposed"
    for _ in range(steps):
        state = step(record, state)
    return state


def fail(errors: list[str]) -> None:
    if errors:
        raise SystemExit("Human-AI organization accountability validation failed:\n" + "\n".join(f" - {e}" for e in errors))


def main() -> None:
    errors: list[str] = []
    for path in (LEAN, LEAN_ROOT, CHAPTER, DOSSIER, MANIFEST, TRIAGE, STRUCTURE, OUTLINE):
        if not path.exists():
            errors.append(f"missing {path.relative_to(ROOT)}")
    fail(errors)

    expected_stages = [
        "proposed",
        "capacityReview",
        "authorityReview",
        "independenceReview",
        "remedyReview",
        "accountabilityAssignable",
    ]
    observed_stages = [run(BASE_RECORD, steps) for steps in range(6)]
    if observed_stages != expected_stages:
        errors.append(f"complete route mismatch: {observed_stages}")
    if not all(BASE_RECORD.values()):
        errors.append("complete record must contain twenty true fields")
    if len(BASE_RECORD) != 20 or set(BASE_RECORD) != set(EXPECTED_MUTATIONS):
        errors.append("independent mutation denominator must cover all twenty record fields")
    for field, expected in EXPECTED_MUTATIONS.items():
        mutated = dict(BASE_RECORD)
        mutated[field] = False
        actual = run(mutated, 5)
        if actual != expected:
            errors.append(f"mutation {field} reached {actual}, expected {expected}")
        if step(mutated, actual) != actual:
            errors.append(f"mutation {field} did not remain blocked after rejection")

    lean_text = LEAN.read_text(encoding="utf-8")
    theorem_names = set(re.findall(r"(?m)^theorem\s+([A-Za-z0-9_']+)", lean_text))
    if theorem_names != REQUIRED_THEOREMS:
        errors.append(
            f"Lean theorem surface mismatch: missing={sorted(REQUIRED_THEOREMS - theorem_names)}, "
            f"extra={sorted(theorem_names - REQUIRED_THEOREMS)}"
        )
    if "import AsiStackProofs.HumanAIOrganizations" not in LEAN_ROOT.read_text(encoding="utf-8"):
        errors.append("root Lean module does not import HumanAIOrganizations")
    for forbidden in (
        "legalAccountabilityEstablished",
        "organizationalEffectivenessEstablished",
        "humanControlEstablished",
        "supportStatePromoted",
        "externalEffectAllowed",
    ):
        if forbidden in lean_text:
            errors.append(f"forbidden overclaim surface present: {forbidden}")

    manifest_rows = [row for row in load(MANIFEST)["records"] if row.get("tag") == TAG]
    triage_rows = [row for row in load(TRIAGE)["records"] if row.get("tag") == TAG]
    if len(manifest_rows) != 1 or len(triage_rows) != 1:
        errors.append("proof manifest and triage must each contain exactly one target row")
    else:
        manifest_row = manifest_rows[0]
        triage_row = triage_rows[0]
        if (manifest_row.get("module"), manifest_row.get("formal_target"), manifest_row.get("status")) != (
            MODULE,
            FORMAL_TARGET,
            "implemented",
        ):
            errors.append("proof manifest target binding drifted")
        if (triage_row.get("module"), triage_row.get("formal_target"), triage_row.get("target_status")) != (
            MODULE,
            FORMAL_TARGET,
            "implemented",
        ):
            errors.append("proof triage target binding drifted")

    chapters = [chapter for part in load(STRUCTURE)["parts"] for chapter in part.get("chapters", [])]
    chapter_rows = [row for row in chapters if row.get("id") == "human-ai-organizations-delegation-and-accountability"]
    if len(chapter_rows) != 1:
        errors.append("book structure must contain exactly one owner chapter")
    else:
        targets = chapter_rows[0].get("proof_targets", [])
        if not any(row.get("tag") == TAG and row.get("status") == "implemented" for row in targets):
            errors.append("book structure target is not implemented")

    chapter_text = CHAPTER.read_text(encoding="utf-8")
    dossier_text = DOSSIER.read_text(encoding="utf-8")
    outline_text = OUTLINE.read_text(encoding="utf-8")
    for fragment in (
        TAG,
        "21 theorem declarations",
        "17 closed mutations",
        "does not prove",
        "remains `argument`",
    ):
        if fragment not in chapter_text:
            errors.append(f"chapter missing boundary fragment: {fragment}")
    for fragment in ("five-stage finite review", "seventeen closed", "support_state_effect` remains `none"):
        if fragment not in dossier_text:
            errors.append(f"proof-model dossier missing fragment: {fragment}")
    if f"| `{TAG}` | `{MODULE}` | {FORMAL_TARGET} | implemented |" not in outline_text:
        errors.append("outline target row drifted")

    fail(errors)
    print(
        "Human-AI organization accountability validation passed: five reachable review stages, "
        "one complete route, 20/20 independent field mutations, and 21 exact Lean declarations; "
        "no human-control, legal-accountability, organizational-outcome, support, or external-effect claim."
    )


if __name__ == "__main__":
    main()
