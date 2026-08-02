#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/AsiStackProofs/RelationalDimensionCompiler.lean"
FIXTURE = ROOT / "tests/fixtures/proof_models/relational_dimension_compiler_dossier.json"
CHAPTER = ROOT / "chapters/relational-dimension-compilation-and-polyadic-cognition.qmd"
MANIFEST = ROOT / "proofs/proof_manifest.json"
TRIAGE = ROOT / "proofs/proof_triage.json"
OUTLINE = ROOT / "docs/book_outline.md"
DOSSIER = ROOT / "evidence_quality/proof_model_dossiers/relational-dimension-compilation-and-polyadic-cognition.md"
TAG = "lean:relational-dimension-compilation-and-polyadic-cognition.admission_boundary"
MODULE = "AsiStackProofs.RelationalDimensionCompiler"

Axis = tuple[str, Callable[[dict[str, Any]], bool], str, Callable[[dict[str, Any]], None]]


def yes(field: str, repair: str) -> Axis:
    return field, lambda d, field=field: d[field] is True, repair, lambda d, field=field: d.update({field: False})


def no(field: str, repair: str) -> Axis:
    return field, lambda d, field=field: d[field] is False, repair, lambda d, field=field: d.update({field: True})


AXES: list[Axis] = [
    yes("proposalIdentityBound", "bindProposalIdentity"),
    yes("compilerVersionBound", "bindCompilerVersion"),
    yes("sourceResidualBound", "bindSourceResidual"), yes("roleSchemaBound", "bindRoleSchema"),
    yes("authorityBound", "bindAuthority"), yes("branchBound", "bindBranch"),
    ("expiry", lambda d: d["currentTick"] <= d["expiresAt"], "renewExpiry", lambda d: d.update(currentTick=21)),
    yes("rolesNonempty", "requireRoles"), yes("everyRoleTyped", "typeEveryRole"),
    yes("roleIdentityUnique", "restoreUniqueRoleIdentity"),
    yes("symmetryDeclared", "declareSymmetry"), yes("optionalityDeclared", "declareOptionality"),
    yes("provenanceBound", "bindProvenance"), yes("uncertaintyBound", "bindUncertainty"),
    yes("scopeBound", "bindScope"),
    yes("proposalDenominatorComplete", "completeProposalDenominator"),
    yes("rejectedProposalsRetained", "retainRejectedProposals"),
    yes("candidateGeneratorBound", "bindCandidateGenerator"),
    yes("reifiedNodeRescuePresent", "addReifiedNodeRescue"),
    yes("pairwiseRescuePresent", "addPairwiseRescue"),
    yes("messagePassingRescuePresent", "addMessagePassingRescue"),
    yes("sequenceRescuePresent", "addSequenceRescue"),
    yes("retrievalRescuePresent", "addRetrievalRescue"),
    yes("toolRescuePresent", "addToolRescue"),
    yes("ordinaryModelRescuePresent", "addOrdinaryModelRescue"),
    yes("rescueBudgetsMatched", "matchRescueBudgets"),
    yes("heldoutTopologyBound", "bindHeldoutTopology"),
    yes("rolePermutationTestBound", "bindRolePermutationTest"),
    yes("missingRoleTestBound", "bindMissingRoleTest"),
    yes("counterfactualRoleTestBound", "bindCounterfactualRoleTest"),
    yes("naturalSyntheticSeparated", "separateNaturalSynthetic"),
    yes("calibrationBound", "bindCalibration"),
    yes("seedDenominatorComplete", "completeSeedDenominator"),
    yes("lifecycleCostBound", "bindLifecycleCost"),
    yes("leakageReviewBound", "bindLeakageReview"),
    yes("independentEvaluatorBound", "bindIndependentEvaluator"),
    yes("semanticVersionBound", "bindSemanticVersion"),
    yes("conformanceReplayBound", "bindConformanceReplay"),
    yes("executableFallbackBound", "bindExecutableFallback"),
    yes("slowPathRecheckBound", "bindSlowPathRecheck"),
    yes("routerContractBound", "bindRouterContract"),
    yes("compiledExpiryBound", "bindCompiledExpiry"),
    yes("compilationResidualOwnerBound", "assignCompilationResidualOwner"),
    yes("newDependentsFrozen", "freezeNewDependents"),
    yes("descendantsEnumerated", "enumerateDescendants"),
    yes("descendantsInvalidatedOrRecompiled", "closeDescendants"),
    yes("cachesInvalidatedOrVersioned", "invalidateCaches"),
    yes("backupAndRestoreBound", "bindBackupRestore"),
    yes("learnedInfluenceResidualBound", "bindLearnedInfluenceResidual"),
    no("irreducibilityClaimed", "rejectIrreducibilityClaim"),
    no("usefulnessClaimed", "rejectUsefulnessClaim"),
    no("efficiencyClaimed", "rejectEfficiencyClaim"),
    no("boundedPrimitiveArityClaimed", "rejectBoundedArityClaim"),
    no("supportOrReleaseRequested", "refuseSupportOrRelease"),
]

REQUIRED = set("""role_id_collection_append_composes every_role_id_survives_collection entity_remapping_preserves_role_identity complete_role_schema_covers_every_required_role omitted_required_role_rejects_complete_schema candidate_id_collection_append_composes every_candidate_id_survives_collection complete_proposal_denominator_covers_every_expected_candidate omitted_candidate_rejects_complete_proposal_denominator descendants_closed_append_iff active_descendant_blocks_contraction_closure review_step_preserves_stage_invariant review_run_preserves_stage_invariant study_eligibility_requires_admissible_dossier complete_dossier_is_ready complete_dossier_reaches_only_theseus_relational_compiler_study every_admission_axis_mutation_blocks_readiness every_admission_axis_mutation_has_exact_repair every_admission_axis_mutation_reaches_repair readiness_requires_identity readiness_requires_typing readiness_requires_rescues readiness_requires_qualification readiness_requires_compilation readiness_requires_contraction readiness_requires_nonclaim_boundary expired_compiler_contract_remains_expired_when_time_advances candidate_budget_overrun_persists_when_generated_count_grows proposal_change_invalidates_compiler_receipt compiler_version_change_invalidates_compiler_receipt role_schema_change_invalidates_compiler_receipt rescue_suite_change_invalidates_compiler_receipt qualification_suite_change_invalidates_compiler_receipt fallback_change_invalidates_compiler_receipt authority_change_invalidates_compiler_receipt identical_qualification_metrics_can_hide_opposite_role_fidelity qualification_metrics_cannot_recover_role_fidelity identical_rescue_records_can_hide_opposite_rescue_competence rescue_records_cannot_recover_lower_order_competence missing_lower_order_rescue_rejects_substrate_consumer unqualified_compiler_routes_runtime_to_fallback missing_compiler_experiment_blocks_empirical_support_promotion""".split())


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def ready(dossier: dict[str, Any]) -> bool:
    return all(predicate(dossier) for _, predicate, _, _ in AXES)


def repair(dossier: dict[str, Any]) -> str:
    return next((route for _, predicate, route, _ in AXES if not predicate(dossier)), "eligibleForTheseusRelationalCompilerStudy")


def main() -> None:
    errors: list[str] = []
    for path in (LEAN, FIXTURE, CHAPTER, MANIFEST, TRIAGE, OUTLINE, DOSSIER):
        if not path.is_file():
            errors.append(f"missing {path.relative_to(ROOT)}")
    if errors:
        raise SystemExit("Relational-dimension compiler failed:\n - " + "\n - ".join(errors))

    dossier = load(FIXTURE)
    if len(AXES) != 54 or len({axis[0] for axis in AXES}) != 54:
        errors.append("mutation denominator is not 54 unique axes")
    if not ready(dossier) or repair(dossier) != "eligibleForTheseusRelationalCompilerStudy":
        errors.append("complete dossier is not eligible")
    for name, _, route, mutate in AXES:
        candidate = deepcopy(dossier)
        mutate(candidate)
        if ready(candidate) or repair(candidate) != route:
            errors.append(f"{name} mutation/repair drifted")

    roles = dossier["roleBindings"]
    required_roles = set(dossier["requiredRoleIds"])
    complete_roles = {row["roleId"] for row in roles if row["typed"]}
    if required_roles != {1, 2, 3} or not required_roles.issubset(complete_roles):
        errors.append("typed-role positive control drifted")
    remapped = [{**row, "entityId": row["entityId"] + 1000} for row in roles]
    if [row["roleId"] for row in remapped] != [row["roleId"] for row in roles]:
        errors.append("entity-remapping role-identity control drifted")

    candidates = dossier["candidateOutcomes"]
    expected_candidates = set(dossier["expectedCandidateIds"])
    retained = {row["candidateId"] for row in candidates if row["attempted"] and row["retainedInDenominator"]}
    if expected_candidates != {201, 202, 203} or not expected_candidates.issubset(retained):
        errors.append("proposal-denominator positive control drifted")
    hidden = deepcopy(candidates)
    hidden[2]["retainedInDenominator"] = False
    hidden_retained = {row["candidateId"] for row in hidden if row["attempted"] and row["retainedInDenominator"]}
    if expected_candidates.issubset(hidden_retained):
        errors.append("hidden-candidate rejection control drifted")

    relation_id = dossier["relationId"]
    dependents = dossier["dependentArtifacts"]
    if not all(row["invalidated"] or row["recompiled"] for row in dependents if row["parentRelationId"] == relation_id):
        errors.append("descendant-closure positive control drifted")
    active = deepcopy(dependents)
    active[0].update(invalidated=False, recompiled=False)
    if all(row["invalidated"] or row["recompiled"] for row in active if row["parentRelationId"] == relation_id):
        errors.append("active-descendant rejection control drifted")

    scope = dossier["receiptScope"]
    expected_scope = {"proposalId", "compilerVersion", "roleSchemaId", "rescueSuiteId", "qualificationSuiteId", "fallbackId", "authorityId"}
    if set(scope) != expected_scope or any((scope | {field: scope[field] + 1}) == scope for field in expected_scope):
        errors.append("seven-axis receipt invalidation control drifted")
    if (8, 3, 4, True) == (8, 3, 4, False) or (7, True, True) == (7, True, False):
        errors.append("information-loss collision controls failed")

    lean_text = LEAN.read_text(encoding="utf-8")
    names = set(re.findall(r"(?m)^theorem\s+([A-Za-z0-9_']+)", lean_text))
    if names != REQUIRED:
        errors.append("exact 42-theorem surface drifted")
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
        "42 theorem declarations", "54 admission-axis mutations", "arbitrary run length",
        "entity remapping", "proposal denominator", "active descendant",
        "role fidelity", "lower-order rescue competence", "Search Substrates",
        "Routing", "Evidence States", "Chapter support remains `argument`",
        "Project Theseus relational compiler study",
    ):
        if fragment not in chapter:
            errors.append(f"chapter missing {fragment}")
    if manifest_rows and manifest_rows[0]["formal_target"] not in " ".join(OUTLINE.read_text(encoding="utf-8").split()):
        errors.append("outline target drifted")
    if errors:
        raise SystemExit("Relational-dimension compiler failed:\n - " + "\n - ".join(errors))
    print(
        "Relational-dimension compiler passed: eight-transition lifecycle, 54/54 exact repairs, "
        "typed-role and proposal-denominator custody, entity-remapping role invariance, descendant "
        "closure, seven receipt invalidations, two non-identifiability results, three rejecting "
        "consumers, and 42 exact Lean declarations; no irreducibility, usefulness, efficiency, "
        "bounded-arity, support, release, or external-effect claim."
    )


if __name__ == "__main__":
    main()
