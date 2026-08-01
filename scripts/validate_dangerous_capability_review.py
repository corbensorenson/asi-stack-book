#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean" / "AsiStackProofs" / "DangerousCapabilityReview.lean"
LEAN_ROOT = ROOT / "lean" / "AsiStackProofs.lean"
CHAPTER = ROOT / "chapters" / "dangerous-capability-domains-and-misuse-uplift.qmd"
DOSSIER = ROOT / "evidence_quality" / "proof_model_dossiers" / "dangerous-capability-domains-and-misuse-uplift.md"
MANIFEST = ROOT / "proofs" / "proof_manifest.json"
TRIAGE = ROOT / "proofs" / "proof_triage.json"
STRUCTURE = ROOT / "book_structure.json"
OUTLINE = ROOT / "docs" / "book_outline.md"
FIXTURE = ROOT / "tests" / "fixtures" / "proof_models" / "dangerous_capability_dossier.json"

TAG = "lean:dangerous-capability-domains-and-misuse-uplift.admission_boundary"
MODULE = "AsiStackProofs.DangerousCapabilityReview"
FORMAL_TARGET = (
    "A seven-stage finite dossier review preserves accumulated identity, threat, baseline, "
    "instrument, custody, and non-authorizing boundary obligations; one complete authored "
    "record reaches only a Project Theseus harmless-analogue campaign, while 29 admission-axis "
    "mutations reach exact repair or refusal states. Expiry and attempt shortfall remain rejecting "
    "under adverse monotone changes, and equal aggregate scores cannot recover a component-sensitive "
    "review rule. No theorem establishes dangerous capability, actor uplift, safeguard efficacy, "
    "realized harm, safety, support, release, transfer, or external effect."
)


GROUPS: list[list[tuple[str, Callable[[dict[str, Any]], bool], str]]] = [
    [
        ("campaignRequest", lambda d: d["campaignRequested"], "refusedNoCampaign"),
        ("modelIdentity", lambda d: d["modelIdentityBound"], "repairModelIdentity"),
        ("checkpointIdentity", lambda d: d["checkpointIdentityBound"], "repairCheckpointIdentity"),
        ("scaffoldIdentity", lambda d: d["scaffoldIdentityBound"], "repairScaffoldIdentity"),
        ("toolAccess", lambda d: d["toolAccessBound"], "repairToolAccess"),
    ],
    [
        ("threatModelVersion", lambda d: d["threatModelVersionCurrent"], "renewThreatModel"),
        ("domainSeparation", lambda d: d["domainsSeparated"], "separateDomains"),
        ("actorCohort", lambda d: d["actorCohortBound"], "bindActorCohort"),
        ("expertiseStrata", lambda d: d["expertiseStrataBound"], "bindExpertiseStrata"),
        ("safeguardComparator", lambda d: d["safeguardComparatorBound"], "bindSafeguardComparator"),
    ],
    [
        ("unassistedBaseline", lambda d: d["unassistedBaselinePresent"], "addUnassistedBaseline"),
        ("accessibleFrontierBaseline", lambda d: d["accessibleFrontierBaselinePresent"], "addAccessibleFrontierBaseline"),
    ],
    [
        ("elicitationBudget", lambda d: d["elicitationBudgetFrozen"], "freezeElicitationBudget"),
        ("positiveControl", lambda d: d["positiveControlPassed"], "repairPositiveControl"),
        ("negativeControl", lambda d: d["negativeControlPassed"], "repairNegativeControl"),
        ("taskValidity", lambda d: d["taskValidityReviewed"], "reviewTaskValidity"),
        ("attemptDenominator", lambda d: d["attemptDenominator"] > 0, "requirePositiveAttemptDenominator"),
        ("attemptRetention", lambda d: d["attemptsRetained"] == d["attemptDenominator"], "retainAllAttempts"),
        ("outcomeAxisSeparation", lambda d: d["outcomeAxesSeparated"], "separateOutcomeAxes"),
        ("independentEvaluator", lambda d: d["independentEvaluator"], "assignIndependentEvaluator"),
    ],
    [
        ("informationHazardCustody", lambda d: d["informationHazardCustodyPresent"], "assignInformationHazardCustody"),
        ("uncertaintyBound", lambda d: d["uncertaintyBoundPresent"], "bindUncertainty"),
        ("expiry", lambda d: d["currentTick"] <= d["expiresAt"], "renewExpiredDossier"),
    ],
    [
        ("maximumInference", lambda d: d["maximumInferencePresent"], "recordMaximumInference"),
        ("residualCustody", lambda d: d["residualCustodyPresent"], "assignResidualCustody"),
        ("nonClaimBoundary", lambda d: d["nonClaimBoundaryPresent"], "recordNonClaimBoundary"),
        ("supportAssignment", lambda d: not d["supportAssignmentRequested"], "refuseSupportAssignment"),
        ("releaseAuthority", lambda d: not d["releaseAuthorityRequested"], "refuseReleaseAuthority"),
        (
            "operationalDetailPublication",
            lambda d: not d["operationalDetailPublicationRequested"],
            "refuseOperationalDetailPublication",
        ),
    ],
]


def review_route(dossier: dict[str, Any]) -> str:
    for group in GROUPS:
        for _, predicate, repair in group:
            if not predicate(dossier):
                return repair
    return "eligibleForTheseusHarmlessAnalogueCampaign"


def ready(dossier: dict[str, Any]) -> bool:
    return all(predicate(dossier) for group in GROUPS for _, predicate, _ in group)


Mutation = Callable[[dict[str, Any]], None]
MUTATIONS: dict[str, Mutation] = {
    "campaignRequest": lambda d: d.update(campaignRequested=False),
    "modelIdentity": lambda d: d.update(modelIdentityBound=False),
    "checkpointIdentity": lambda d: d.update(checkpointIdentityBound=False),
    "scaffoldIdentity": lambda d: d.update(scaffoldIdentityBound=False),
    "toolAccess": lambda d: d.update(toolAccessBound=False),
    "threatModelVersion": lambda d: d.update(threatModelVersionCurrent=False),
    "domainSeparation": lambda d: d.update(domainsSeparated=False),
    "actorCohort": lambda d: d.update(actorCohortBound=False),
    "expertiseStrata": lambda d: d.update(expertiseStrataBound=False),
    "safeguardComparator": lambda d: d.update(safeguardComparatorBound=False),
    "unassistedBaseline": lambda d: d.update(unassistedBaselinePresent=False),
    "accessibleFrontierBaseline": lambda d: d.update(accessibleFrontierBaselinePresent=False),
    "elicitationBudget": lambda d: d.update(elicitationBudgetFrozen=False),
    "positiveControl": lambda d: d.update(positiveControlPassed=False),
    "negativeControl": lambda d: d.update(negativeControlPassed=False),
    "taskValidity": lambda d: d.update(taskValidityReviewed=False),
    "attemptDenominator": lambda d: d.update(attemptDenominator=0),
    "attemptRetention": lambda d: d.update(attemptsRetained=3),
    "outcomeAxisSeparation": lambda d: d.update(outcomeAxesSeparated=False),
    "independentEvaluator": lambda d: d.update(independentEvaluator=False),
    "informationHazardCustody": lambda d: d.update(informationHazardCustodyPresent=False),
    "uncertaintyBound": lambda d: d.update(uncertaintyBoundPresent=False),
    "expiry": lambda d: d.update(expiresAt=4),
    "maximumInference": lambda d: d.update(maximumInferencePresent=False),
    "residualCustody": lambda d: d.update(residualCustodyPresent=False),
    "nonClaimBoundary": lambda d: d.update(nonClaimBoundaryPresent=False),
    "supportAssignment": lambda d: d.update(supportAssignmentRequested=True),
    "releaseAuthority": lambda d: d.update(releaseAuthorityRequested=True),
    "operationalDetailPublication": lambda d: d.update(operationalDetailPublicationRequested=True),
}

REQUIRED_THEOREMS = {
    "review_step_preserves_stage_invariant",
    "review_run_preserves_stage_invariant",
    "campaign_eligibility_requires_admissible_dossier",
    "admissible_dossier_is_ready",
    "complete_dossier_is_ready",
    "complete_dossier_reaches_only_harmless_analogue_campaign",
    "every_admission_axis_mutation_blocks_readiness",
    "every_admission_axis_mutation_reaches_exact_repair",
    "every_admission_axis_mutation_blocks_campaign_eligibility",
    "readiness_requires_identity_review",
    "readiness_requires_threat_review",
    "readiness_requires_baselines",
    "readiness_requires_instrument_competence",
    "readiness_requires_custody_and_currentness",
    "readiness_requires_non_authorizing_boundary",
    "expired_dossier_remains_expired_when_time_advances",
    "attempt_shortfall_persists_when_retention_decreases",
    "equal_aggregate_score_can_hide_distinct_outcome_vectors",
    "equal_aggregate_score_can_require_opposite_component_reviews",
    "aggregate_score_cannot_recover_component_sensitive_review",
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def fail(errors: list[str]) -> None:
    if errors:
        raise SystemExit(
            "Dangerous-capability review validation failed:\n"
            + "\n".join(f" - {error}" for error in errors)
        )


def main() -> None:
    errors: list[str] = []
    for path in (LEAN, LEAN_ROOT, CHAPTER, DOSSIER, MANIFEST, TRIAGE, STRUCTURE, OUTLINE, FIXTURE):
        if not path.exists():
            errors.append(f"missing {path.relative_to(ROOT)}")
    fail(errors)

    complete = load(FIXTURE)
    expected_routes = {axis: route for group in GROUPS for axis, _, route in group}
    if set(MUTATIONS) != set(expected_routes) or len(MUTATIONS) != 29:
        errors.append("mutation denominator must cover exactly 29 admission axes")
    if not ready(complete) or review_route(complete) != "eligibleForTheseusHarmlessAnalogueCampaign":
        errors.append("complete dossier must reach only the harmless-analogue Theseus campaign")
    for axis, mutate in MUTATIONS.items():
        dossier = deepcopy(complete)
        mutate(dossier)
        if ready(dossier):
            errors.append(f"{axis} mutation remained ready")
        route = review_route(dossier)
        if route != expected_routes[axis]:
            errors.append(f"{axis} mutation reached {route}, expected {expected_routes[axis]}")

    expired = deepcopy(complete)
    expired.update(currentTick=9, expiresAt=8)
    for later_tick in range(9, 15):
        later = deepcopy(expired)
        later["currentTick"] = later_tick
        if later["currentTick"] <= later["expiresAt"]:
            errors.append(f"later tick {later_tick} laundered an expired dossier")
    shortfall = deepcopy(complete)
    shortfall.update(attemptDenominator=4, attemptsRetained=3)
    for fewer_retained in range(4):
        fewer = deepcopy(shortfall)
        fewer["attemptsRetained"] = fewer_retained
        if fewer["attemptDenominator"] > 0 and fewer["attemptsRetained"] == fewer["attemptDenominator"]:
            errors.append(f"lower retained count {fewer_retained} laundered an attempt shortfall")

    uplift_concentrated = (0, 0, 0, 4, 0)
    capability_concentrated = (4, 0, 0, 0, 0)
    aggregate = lambda vector: sum(vector)
    component_review = lambda vector: vector[2] >= 3 or vector[3] >= 3
    if aggregate(uplift_concentrated) != aggregate(capability_concentrated):
        errors.append("scalar collision witnesses no longer have equal totals")
    if uplift_concentrated == capability_concentrated:
        errors.append("scalar collision witnesses no longer preserve distinct vectors")
    if not component_review(uplift_concentrated) or component_review(capability_concentrated):
        errors.append("equal-score witnesses no longer require opposite component review decisions")

    lean_text = LEAN.read_text(encoding="utf-8")
    theorem_names = set(re.findall(r"(?m)^theorem\s+([A-Za-z0-9_']+)", lean_text))
    if theorem_names != REQUIRED_THEOREMS:
        errors.append(
            f"Lean theorem surface mismatch: missing={sorted(REQUIRED_THEOREMS - theorem_names)}, "
            f"extra={sorted(theorem_names - REQUIRED_THEOREMS)}"
        )
    if "import AsiStackProofs.DangerousCapabilityReview" not in LEAN_ROOT.read_text(encoding="utf-8"):
        errors.append("root Lean module does not import DangerousCapabilityReview")
    for forbidden in (
        "dangerousCapabilityEstablished",
        "actorUpliftEstablished",
        "safeguardEffectivenessEstablished",
        "realizedHarmEstablished",
        "safetyEstablished",
        "supportStatePromoted",
        "releaseAuthorized",
        "externalEffectAllowed",
    ):
        if forbidden in lean_text:
            errors.append(f"forbidden overclaim surface present: {forbidden}")

    manifest_rows = [row for row in load(MANIFEST)["records"] if row.get("tag") == TAG]
    triage_rows = [row for row in load(TRIAGE)["records"] if row.get("tag") == TAG]
    if len(manifest_rows) != 1 or len(triage_rows) != 1:
        errors.append("proof manifest and triage must each contain exactly one target row")
    else:
        if (
            manifest_rows[0].get("module"),
            manifest_rows[0].get("formal_target"),
            manifest_rows[0].get("status"),
        ) != (MODULE, FORMAL_TARGET, "implemented"):
            errors.append("proof manifest target binding drifted")
        if (
            triage_rows[0].get("module"),
            triage_rows[0].get("formal_target"),
            triage_rows[0].get("target_status"),
        ) != (MODULE, FORMAL_TARGET, "implemented"):
            errors.append("proof triage target binding drifted")

    chapters = [chapter for part in load(STRUCTURE)["parts"] for chapter in part.get("chapters", [])]
    owners = [row for row in chapters if row.get("id") == "dangerous-capability-domains-and-misuse-uplift"]
    if len(owners) != 1:
        errors.append("book structure must contain exactly one owner chapter")
    elif not any(
        row.get("tag") == TAG and row.get("status") == "implemented"
        for row in owners[0].get("proof_targets", [])
    ):
        errors.append("book structure target is not implemented")

    chapter_text = CHAPTER.read_text(encoding="utf-8")
    dossier_flat = re.sub(r"\s+", " ", DOSSIER.read_text(encoding="utf-8"))
    for fragment in (
        TAG,
        "20 theorem declarations",
        "29 independently checkable admission-axis mutations",
        "aggregate-score impossibility result",
        "Chapter support remains `argument`",
        "Project Theseus harmless-analogue campaign",
    ):
        if fragment not in chapter_text:
            errors.append(f"chapter missing boundary fragment: {fragment}")
    for fragment in (
        "29 exact mutation routes",
        "two arithmetic monotonicity controls",
        "one aggregate-score impossibility result",
        "support_state_effect` remains `none",
    ):
        if fragment not in dossier_flat:
            errors.append(f"proof-model dossier missing fragment: {fragment}")
    outline_text = OUTLINE.read_text(encoding="utf-8")
    if f"| `{TAG}` | `{MODULE}` | {FORMAL_TARGET} | implemented |" not in outline_text:
        errors.append("outline target row drifted")

    fail(errors)
    print(
        "Dangerous-capability review validation passed: seven-stage finite lifecycle, "
        "29/29 exact admission-axis mutations, two monotonic rejection controls, one "
        "aggregate-score impossibility result, and 20 exact Lean declarations; no dangerous-"
        "capability, uplift, safeguard-efficacy, harm, safety, support, release, transfer, or "
        "external-effect claim."
    )


if __name__ == "__main__":
    main()
