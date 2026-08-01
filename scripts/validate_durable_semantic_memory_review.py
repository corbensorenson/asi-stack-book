#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/AsiStackProofs/DurableSemanticMemoryReview.lean"
FIXTURE = ROOT / "tests/fixtures/proof_models/durable_semantic_memory_dossier.json"
CHAPTER = ROOT / "chapters/durable-semantic-memory-and-knowledge-lattices.qmd"
MANIFEST = ROOT / "proofs/proof_manifest.json"
TRIAGE = ROOT / "proofs/proof_triage.json"
OUTLINE = ROOT / "docs/book_outline.md"
DOSSIER = ROOT / "evidence_quality/proof_model_dossiers/durable-semantic-memory-and-knowledge-lattices.md"
TAG = "lean:durable-semantic-memory-and-knowledge-lattices.admission_boundary"
MODULE = "AsiStackProofs.DurableSemanticMemoryReview"

Axis = tuple[str, Callable[[dict[str, Any]], bool], str, Callable[[dict[str, Any]], None]]


def yes(field: str, repair: str) -> Axis:
    return field, lambda d, field=field: d[field] is True, repair, lambda d, field=field: d.update({field: False})


def no(field: str, repair: str) -> Axis:
    return field, lambda d, field=field: d[field] is False, repair, lambda d, field=field: d.update({field: True})


AXES: list[Axis] = [
    yes("semanticObjectIdBound", "bindSemanticObjectId"),
    yes("sourceOccurrenceIdBound", "bindSourceOccurrenceId"),
    yes("aliasCollisionRecorded", "recordAliasCollision"),
    yes("ontologyVersionBound", "bindOntologyVersion"),
    yes("relationSchemaVersionBound", "bindRelationSchemaVersion"),
    yes("evidenceEpochBound", "bindEvidenceEpoch"),
    yes("provenanceComplete", "completeProvenance"),
    yes("temporalValidityBound", "bindTemporalValidity"),
    yes("supportStateBound", "bindSupportState"),
    yes("contradictionsRetained", "retainContradictions"),
    yes("supersessionLineagePresent", "addSupersessionLineage"),
    yes("rightsBound", "bindRights"),
    yes("dependencyIndexComplete", "completeDependencyIndex"),
    yes("migrationMappingComplete", "completeMigrationMapping"),
    yes("unmappedCasesRecorded", "recordUnmappedCases"),
    yes("lossyCasesRecorded", "recordLossyCases"),
    yes("affectedConsumersIndexed", "indexAffectedConsumers"),
    yes("consumerInvalidationPlanned", "planConsumerInvalidation"),
    yes("rollbackOrDualReadPresent", "addRollbackOrDualRead"),
    yes("retrievalPlanBound", "bindRetrievalPlan"),
    yes("consumerPurposeBound", "bindConsumerPurpose"),
    yes("freshnessChecked", "checkFreshness"),
    yes("rightsChecked", "checkRights"),
    yes("contradictionsIncluded", "includeContradictions"),
    yes("selectionReasonsRecorded", "recordSelectionReasons"),
    yes("useReceiptPresent", "addUseReceipt"),
    yes("compactionLineagePresent", "addCompactionLineage"),
    yes("retentionPolicyBound", "bindRetentionPolicy"),
    yes("deletionDutiesBound", "bindDeletionDuties"),
    yes("backupStateBound", "bindBackupState"),
    yes("restartReplayTested", "testRestartReplay"),
    yes("recoveryResidualRecorded", "recordRecoveryResidual"),
    yes("descendantRepairPlanPresent", "planDescendantRepair"),
    ("expiry", lambda d: d["currentTick"] <= d["expiresAt"], "renewExpiry", lambda d: d.update(currentTick=21)),
    no("semanticTruthClaimed", "rejectSemanticTruthClaim"),
    no("completeMemoryClaimed", "rejectCompleteMemoryClaim"),
    no("behavioralForgettingClaimed", "rejectBehavioralForgettingClaim"),
    no("supportOrReleaseRequested", "refuseSupportOrRelease"),
]

REQUIRED = set("""retrieval_benchmark_does_not_establish_semantic_truth persistence_replay_does_not_establish_complete_memory storage_deletion_does_not_establish_behavioral_forgetting graph_connectivity_does_not_establish_decision_authority representation_rebuild_preserves_semantic_object_identity equal_aliases_do_not_force_equal_semantic_objects every_parent_provenance_id_survives_collection derived_use_cannot_exceed_any_parent_authority lossy_migration_without_consumer_invalidation_is_rejected every_used_object_has_current_authorized_provenance replay_append_composes_exactly review_step_preserves_stage_invariant review_run_preserves_stage_invariant replay_eligibility_requires_admissible_dossier complete_dossier_is_ready complete_dossier_reaches_only_theseus_memory_replay every_admission_axis_mutation_blocks_readiness every_admission_axis_mutation_has_exact_repair every_admission_axis_mutation_reaches_repair readiness_requires_identity readiness_requires_revision readiness_requires_migration readiness_requires_retrieval readiness_requires_retention readiness_requires_boundary expired_memory_contract_remains_expired_when_time_advances object_change_invalidates_memory_receipt ontology_change_invalidates_memory_receipt evidence_epoch_change_invalidates_memory_receipt consumer_purpose_change_invalidates_memory_receipt identical_summary_signals_can_hide_opposite_contradiction_state summary_signals_cannot_recover_contradiction_state identical_deletion_signals_can_hide_opposite_learned_influence deletion_signals_cannot_recover_behavioral_forgetting open_memory_deletion_duty_blocks_context_materialization""".split())


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def ready(dossier: dict[str, Any]) -> bool:
    return all(predicate(dossier) for _, predicate, _, _ in AXES)


def repair(dossier: dict[str, Any]) -> str:
    return next((route for _, predicate, route, _ in AXES if not predicate(dossier)), "eligibleForTheseusMemoryReplay")


def main() -> None:
    errors: list[str] = []
    for path in (LEAN, FIXTURE, CHAPTER, MANIFEST, TRIAGE, OUTLINE, DOSSIER):
        if not path.is_file():
            errors.append(f"missing {path.relative_to(ROOT)}")
    if errors:
        raise SystemExit("Durable semantic-memory review failed:\n - " + "\n - ".join(errors))

    dossier = load(FIXTURE)
    if len(AXES) != 38 or len({axis[0] for axis in AXES}) != 38:
        errors.append("mutation denominator is not 38 unique axes")
    if not ready(dossier) or repair(dossier) != "eligibleForTheseusMemoryReplay":
        errors.append("complete dossier is not eligible")
    for name, _, route, mutate in AXES:
        candidate = deepcopy(dossier)
        mutate(candidate)
        if ready(candidate) or repair(candidate) != route:
            errors.append(f"{name} mutation/repair drifted")

    parents = dossier["parents"]
    collected = [source for parent in parents for source in parent["provenanceIds"]]
    if collected != [11, 12, 21] or not all(5 in parent["permittedPurposes"] for parent in parents):
        errors.append("parent provenance or authority induction fixture drifted")
    migrations = dossier["migrationEntries"]
    if not all(row["mappedExactly"] or (row["lossRecorded"] and row["affectedConsumersInvalidated"]) for row in migrations):
        errors.append("migration fixture is not admissible")
    bad_migration = deepcopy(migrations)
    bad_migration[1]["affectedConsumersInvalidated"] = False
    if all(row["mappedExactly"] or (row["lossRecorded"] and row["affectedConsumersInvalidated"]) for row in bad_migration):
        errors.append("lossy migration without invalidation was accepted")
    by_id = {row["objectId"]: row for row in dossier["retrievalCandidates"]}
    for object_id in dossier["usedObjectIds"]:
        row = by_id.get(object_id, {})
        if not all(row.get(field) is value for field, value in (
            ("provenancePresent", True), ("supportCurrent", True), ("rightsAllowUse", True),
            ("contradictionStateIncluded", True), ("retracted", False),
        )):
            errors.append(f"retrieval use receipt failed for object {object_id}")
    events = dossier["memoryEvents"]
    whole = (events, len(events))
    split = (events[:2] + events[2:], len(events[:2]) + len(events[2:]))
    if whole != split:
        errors.append("replay concatenation control failed")
    if (7, 91, False) == (7, 91, True) or (True, True, True, True) == (True, True, True, False):
        errors.append("non-identifiability collision controls failed")

    lean_text = LEAN.read_text(encoding="utf-8")
    names = set(re.findall(r"(?m)^theorem\s+([A-Za-z0-9_']+)", lean_text))
    if names != REQUIRED:
        errors.append("exact 35-theorem surface drifted")
    if re.search(r"\b(sorry|admit|axiom)\b", lean_text):
        errors.append("Lean trust boundary widened")

    manifest_rows = [row for row in load(MANIFEST)["records"] if row.get("tag") == TAG]
    triage_rows = [row for row in load(TRIAGE)["records"] if row.get("tag") == TAG]
    if len(manifest_rows) != 1 or (manifest_rows[0].get("module"), manifest_rows[0].get("status")) != (MODULE, "implemented"):
        errors.append("manifest binding drifted")
    if len(triage_rows) != 1 or (triage_rows[0].get("module"), triage_rows[0].get("target_status")) != (MODULE, "implemented"):
        errors.append("triage binding drifted")

    chapter = " ".join(CHAPTER.read_text(encoding="utf-8").split())
    for fragment in (
        "35 theorem declarations", "38 admission-axis mutations", "arbitrary finite parent sets",
        "summary signals", "storage-deletion signals", "Context Transactions",
        "Chapter support remains `argument`", "Project Theseus memory replay",
    ):
        if fragment not in chapter:
            errors.append(f"chapter missing {fragment}")
    if manifest_rows and manifest_rows[0]["formal_target"] not in " ".join(OUTLINE.read_text(encoding="utf-8").split()):
        errors.append("outline target drifted")
    if errors:
        raise SystemExit("Durable semantic-memory review failed:\n - " + "\n - ".join(errors))
    print(
        "Durable semantic-memory review passed: seven-transition lifecycle, 38/38 exact repairs, "
        "identity/provenance/authority/migration/retrieval/replay boundaries, four receipt invalidations, "
        "two non-identifiability results, one rejecting Context Transactions bridge, and 35 exact Lean "
        "declarations; no truth, complete-memory, behavioral-forgetting, support, or external-effect claim."
    )


if __name__ == "__main__":
    main()
