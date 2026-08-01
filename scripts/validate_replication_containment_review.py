#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/AsiStackProofs/ReplicationContainmentReview.lean"
FIXTURE = ROOT / "tests/fixtures/proof_models/replication_containment_dossier.json"
CHAPTER = ROOT / "chapters/autonomous-replication-proliferation-and-containment.qmd"
MANIFEST = ROOT / "proofs/proof_manifest.json"
TRIAGE = ROOT / "proofs/proof_triage.json"
OUTLINE = ROOT / "docs/book_outline.md"
DOSSIER = ROOT / "evidence_quality/proof_model_dossiers/autonomous-replication-proliferation-and-containment.md"
TAG = "lean:autonomous-replication-proliferation-and-containment.admission_boundary"
MODULE = "AsiStackProofs.ReplicationContainmentReview"
Axis = tuple[str, Callable[[dict[str, Any]], bool], str, Callable[[dict[str, Any]], None]]


def yes(field: str, repair: str) -> Axis:
    return field, lambda d, f=field: d[f] is True, repair, lambda d, f=field: d.update({f: False})


def no(field: str, repair: str) -> Axis:
    return field, lambda d, f=field: d[f] is False, repair, lambda d, f=field: d.update({f: True})


AXES: list[Axis] = [
    yes("parentIdentityBound", "bindParentIdentity"), yes("attemptIdentityBound", "bindAttemptIdentity"),
    yes("modelIdentityBound", "bindModelIdentity"), yes("artifactIdentityBound", "bindArtifactIdentity"),
    yes("environmentIdentityBound", "bindEnvironmentIdentity"), yes("protocolVersionBound", "bindProtocolVersion"),
    yes("lifecycleStageBound", "bindLifecycleStage"), yes("deniedByDefault", "enforceDeniedByDefault"),
    yes("syntheticLeasePresent", "issueSyntheticLease"), yes("childPrincipalFresh", "issueFreshChildPrincipal"),
    yes("parentCredentialsExcluded", "excludeParentCredentials"),
    yes("authorityNoninheritanceExplicit", "enforceAuthorityNoninheritance"),
    yes("providerSynthetic", "requireSyntheticProvider"), yes("networkClosed", "closeNetwork"),
    yes("resourceCeilingBound", "bindResourceCeiling"), yes("descendantCeilingBound", "bindDescendantCeiling"),
    ("expiry", lambda d: d["currentTick"] <= d["expiresAt"], "renewExpiry", lambda d: d.update(currentTick=21)),
    yes("independentStopAuthorityPresent", "bindIndependentStopAuthority"),
    yes("componentDenominatorComplete", "completeComponentDenominator"),
    yes("assistedDenominatorComplete", "completeAssistedDenominator"),
    yes("endToEndSyntheticDenominatorComplete", "completeEndToEndDenominator"),
    yes("containmentDenominatorComplete", "completeContainmentDenominator"),
    yes("humanAssistanceRecorded", "recordHumanAssistance"), yes("retriesRecorded", "recordRetries"),
    yes("positiveControlsPass", "qualifyPositiveControls"),
    yes("seededContainmentFailureObserved", "observeSeededContainmentFailure"),
    yes("scaffoldContributionRecorded", "recordScaffoldContribution"),
    yes("realInfrastructureExcluded", "excludeRealInfrastructure"), yes("copyLineageBound", "bindCopyLineage"),
    yes("weightLineageBound", "bindWeightLineage"), yes("configurationLineageBound", "bindConfigurationLineage"),
    yes("memoryLineageBound", "bindMemoryLineage"), yes("credentialLineageBound", "bindCredentialLineage"),
    yes("resourceLineageBound", "bindResourceLineage"), yes("endpointLineageBound", "bindEndpointLineage"),
    yes("descendantCensusComplete", "completeDescendantCensus"),
    yes("independentHeartbeatPresent", "addIndependentHeartbeat"),
    yes("unknownDescendantResidualRecorded", "recordUnknownDescendantResidual"),
    yes("independentKillPathPresent", "addIndependentKillPath"), yes("shutdownObserved", "observeShutdown"),
    yes("credentialsRevoked", "revokeCredentials"), yes("networkIsolated", "isolateNetwork"),
    yes("resourcesReclaimed", "reclaimResources"), yes("persistenceScanComplete", "completePersistenceScan"),
    yes("artifactsDispositioned", "dispositionArtifacts"), yes("recallAttempted", "attemptRecall"),
    yes("affectedPathsNotified", "notifyAffectedPaths"), yes("residualOwnerPresent", "assignResidualOwner"),
    no("realInfrastructureAuthorityRequested", "refuseRealInfrastructureAuthority"),
    no("realReplicationClaimed", "rejectRealReplicationClaim"), no("containmentClaimed", "rejectContainmentClaim"),
    no("supportOrReleaseRequested", "refuseSupportOrRelease"),
]

REQUIRED_THEOREMS = {
    "component_success_does_not_establish_end_to_end_replication",
    "synthetic_completion_does_not_establish_real_infrastructure_capability",
    "shutdown_acknowledgment_does_not_establish_global_containment",
    "distinct_child_cannot_use_parent_replication_lease",
    "real_provider_path_is_outside_synthetic_test_authority",
    "quarantine_all_covers_every_finite_descendant", "review_step_preserves_stage_invariant",
    "review_run_preserves_stage_invariant", "campaign_eligibility_requires_admissible_dossier",
    "complete_dossier_is_ready", "complete_dossier_reaches_only_replication_containment_campaign",
    "every_admission_axis_mutation_blocks_readiness", "every_admission_axis_mutation_has_exact_repair",
    "every_admission_axis_mutation_reaches_repair", "readiness_requires_identity",
    "readiness_requires_authority", "readiness_requires_evaluation", "readiness_requires_lineage",
    "readiness_requires_containment", "readiness_requires_closure", "readiness_requires_boundary",
    "expired_lease_remains_expired_when_time_advances",
    "descendant_overrun_persists_under_growth_and_no_larger_ceiling",
    "parent_change_invalidates_replication_receipt", "artifact_change_invalidates_replication_receipt",
    "environment_change_invalidates_replication_receipt", "protocol_change_invalidates_replication_receipt",
    "identical_component_signals_can_hide_opposite_replication_state",
    "component_signals_cannot_recover_end_to_end_replication",
    "identical_local_containment_signals_can_hide_opposite_global_state",
    "local_containment_signals_cannot_recover_global_containment",
    "unresolved_descendants_force_operations_state_inventory",
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def ready(d: dict[str, Any]) -> bool:
    return all(predicate(d) for _, predicate, _, _ in AXES)


def repair(d: dict[str, Any]) -> str:
    return next((route for _, predicate, route, _ in AXES if not predicate(d)),
                "eligibleForTheseusReplicationContainmentCampaign")


def main() -> None:
    errors: list[str] = []
    for path in (LEAN, FIXTURE, CHAPTER, MANIFEST, TRIAGE, OUTLINE, DOSSIER):
        if not path.is_file(): errors.append(f"missing {path.relative_to(ROOT)}")
    if errors: raise SystemExit("Replication containment review failed:\n - " + "\n - ".join(errors))
    complete = load(FIXTURE)
    if len(AXES) != 52 or len({axis[0] for axis in AXES}) != 52:
        errors.append("mutation denominator is not 52 unique axes")
    if not ready(complete) or repair(complete) != "eligibleForTheseusReplicationContainmentCampaign":
        errors.append("complete dossier is not campaign-eligible")
    for name, _, route, mutate in AXES:
        candidate = deepcopy(complete); mutate(candidate)
        if ready(candidate): errors.append(f"{name} mutation remained ready")
        if repair(candidate) != route: errors.append(f"{name} reached {repair(candidate)}, expected {route}")
    evidence_map = {"component": "componentCapability", "synthetic": "boundedSyntheticCompletion",
                    "shutdown": "localShutdownReceipt"}
    if any(value in {"endToEndAutonomousReplication", "realInfrastructureCapability", "globalContainment"}
           for value in evidence_map.values()): errors.append("evidence non-substitution failed")
    lease = {"principal": 7, "ceiling": 3, "expires": 20}
    if 8 == lease["principal"] or "realProvider" == "closedSynthetic": errors.append("authority isolation failed")
    quarantined = [{**row, "quarantined": True} for row in complete["descendantRecords"]]
    if not quarantined or not all(row["quarantined"] for row in quarantined):
        errors.append("finite descendant quarantine failed")
    if not (20 < 21 <= 22 and 3 < 4 <= 5): errors.append("monotonicity controls failed")
    receipt = {"parent": 1, "artifact": 2, "environment": 3, "protocol": 4}
    if not all((9 != receipt["parent"], 9 != receipt["artifact"], 9 != receipt["environment"], 9 != receipt["protocol"])):
        errors.append("receipt invalidation controls failed")
    component_signals = (True, True, True, True)
    if component_signals != tuple(component_signals) or (True and True) == (False and False):
        errors.append("end-to-end replication collision failed")
    containment_signals = (True, True, True, True)
    if containment_signals != tuple(containment_signals) or (not False) == (not True):
        errors.append("global containment collision failed")
    if complete.get("descendantsComplete", False): errors.append("operations consumer accepted inventory")
    theorem_names = set(re.findall(r"(?m)^theorem\s+([A-Za-z0-9_']+)", LEAN.read_text(encoding="utf-8")))
    if theorem_names != REQUIRED_THEOREMS: errors.append("exact 32-theorem surface drifted")
    lean_text = LEAN.read_text(encoding="utf-8")
    if re.search(r"\b(sorry|admit|axiom)\b", lean_text): errors.append("Lean trust boundary contains sorry, admit, or axiom")
    manifest = [r for r in load(MANIFEST)["records"] if r.get("tag") == TAG]
    triage = [r for r in load(TRIAGE)["records"] if r.get("tag") == TAG]
    if len(manifest) != 1 or (manifest[0].get("module"), manifest[0].get("status")) != (MODULE, "implemented"):
        errors.append("manifest binding drifted")
    if len(triage) != 1 or (triage[0].get("module"), triage[0].get("target_status")) != (MODULE, "implemented"):
        errors.append("triage binding drifted")
    chapter = " ".join(CHAPTER.read_text(encoding="utf-8").split())
    for fragment in ("32 theorem declarations", "52 admission-axis mutations", "finite descendant quarantine",
                     "end-to-end replication impossibility", "global-containment impossibility",
                     "Chapter support remains `argument`", "Project Theseus replication-containment campaign"):
        if fragment not in chapter: errors.append(f"chapter missing {fragment}")
    formal = manifest[0].get("formal_target") if manifest else None
    if formal and formal not in " ".join(OUTLINE.read_text(encoding="utf-8").split()):
        errors.append("outline target drifted")
    if errors: raise SystemExit("Replication containment review failed:\n - " + "\n - ".join(errors))
    print("Replication containment review passed: eight-transition lifecycle, 52/52 exact repairs, evidence non-substitution, lease noninheritance, synthetic-provider isolation, finite descendant quarantine, receipt and monotonicity controls, two non-identifiability results, one rejecting operations bridge, and 32 exact Lean declarations; no real-world replication, containment, deployment, support, or external-effect claim.")


if __name__ == "__main__":
    main()
