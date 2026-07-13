namespace AsiStackProofs.SafetyCases

inductive SafetyCaseRoute where
  | retainAsCaseDraft
  | requireCaseRepair
  | requireEvidenceRepair
  | requireCountercaseReview
  | requireIndependentReview
  | requireAccountableReview
  | rejectAuthorityLaundering
  | releaseToReadinessReview
deriving DecidableEq, Repr

structure SafetyCaseRecord where
  deploymentContextRecorded : Bool
  topClaimScoped : Bool
  hazardModelRecorded : Bool
  argumentStrategiesRecorded : Bool
  evidenceReferencesRecorded : Bool
  evidenceDependenciesCurrent : Bool
  assumptionsRecorded : Bool
  countercaseReviewRecorded : Bool
  independentReviewRecorded : Bool
  unresolvedDefeaterPresent : Bool
  acceptanceCriterionRecorded : Bool
  residualOwnerRecorded : Bool
  decisionAuthorityRecorded : Bool
  authoritySeparationRecorded : Bool
  affectedReleaseRequested : Bool
deriving DecidableEq, Repr

def SafetyCaseRouteFor
    (record : SafetyCaseRecord) :
    SafetyCaseRoute :=
  if record.deploymentContextRecorded = false then
    SafetyCaseRoute.retainAsCaseDraft
  else if record.topClaimScoped = false then
    SafetyCaseRoute.requireCaseRepair
  else if record.hazardModelRecorded = false then
    SafetyCaseRoute.requireCaseRepair
  else if record.argumentStrategiesRecorded = false then
    SafetyCaseRoute.requireCaseRepair
  else if record.evidenceReferencesRecorded = false then
    SafetyCaseRoute.requireCaseRepair
  else if record.evidenceDependenciesCurrent = false then
    SafetyCaseRoute.requireEvidenceRepair
  else if record.assumptionsRecorded = false then
    SafetyCaseRoute.requireCaseRepair
  else if record.countercaseReviewRecorded = false then
    SafetyCaseRoute.requireCountercaseReview
  else if record.independentReviewRecorded = false then
    SafetyCaseRoute.requireIndependentReview
  else if record.unresolvedDefeaterPresent = true then
    SafetyCaseRoute.requireAccountableReview
  else if record.acceptanceCriterionRecorded = false then
    SafetyCaseRoute.requireCaseRepair
  else if record.residualOwnerRecorded = false then
    SafetyCaseRoute.requireCaseRepair
  else if record.decisionAuthorityRecorded = false then
    SafetyCaseRoute.requireAccountableReview
  else if record.authoritySeparationRecorded = false then
    SafetyCaseRoute.rejectAuthorityLaundering
  else if record.affectedReleaseRequested = true then
    SafetyCaseRoute.releaseToReadinessReview
  else
    SafetyCaseRoute.retainAsCaseDraft

theorem complete_case_reaches_readiness_review
    {record : SafetyCaseRecord} :
    record.deploymentContextRecorded = true ->
    record.topClaimScoped = true ->
    record.hazardModelRecorded = true ->
    record.argumentStrategiesRecorded = true ->
    record.evidenceReferencesRecorded = true ->
    record.evidenceDependenciesCurrent = true ->
    record.assumptionsRecorded = true ->
    record.countercaseReviewRecorded = true ->
    record.independentReviewRecorded = true ->
    record.unresolvedDefeaterPresent = false ->
    record.acceptanceCriterionRecorded = true ->
    record.residualOwnerRecorded = true ->
    record.decisionAuthorityRecorded = true ->
    record.authoritySeparationRecorded = true ->
    record.affectedReleaseRequested = true ->
    SafetyCaseRouteFor record = SafetyCaseRoute.releaseToReadinessReview := by
  intro deploymentContext topClaim hazardModel argumentStrategies evidenceReferences
    evidenceCurrent assumptions countercaseReview independentReview noDefeater
    acceptanceCriterion residualOwner decisionAuthority authoritySeparation releaseRequested
  unfold SafetyCaseRouteFor
  simp [deploymentContext, topClaim, hazardModel, argumentStrategies,
    evidenceReferences, evidenceCurrent, assumptions, countercaseReview,
    independentReview, noDefeater, acceptanceCriterion, residualOwner,
    decisionAuthority, authoritySeparation, releaseRequested]

theorem missing_deployment_context_retains_draft
    {record : SafetyCaseRecord} :
    record.deploymentContextRecorded = false ->
    SafetyCaseRouteFor record = SafetyCaseRoute.retainAsCaseDraft := by
  intro missingContext
  unfold SafetyCaseRouteFor
  simp [missingContext]

theorem missing_hazard_model_requires_case_repair
    {record : SafetyCaseRecord} :
    record.deploymentContextRecorded = true ->
    record.topClaimScoped = true ->
    record.hazardModelRecorded = false ->
    SafetyCaseRouteFor record = SafetyCaseRoute.requireCaseRepair := by
  intro deploymentContext topClaim missingHazardModel
  unfold SafetyCaseRouteFor
  simp [deploymentContext, topClaim, missingHazardModel]

theorem stale_evidence_dependency_requires_repair
    {record : SafetyCaseRecord} :
    record.deploymentContextRecorded = true ->
    record.topClaimScoped = true ->
    record.hazardModelRecorded = true ->
    record.argumentStrategiesRecorded = true ->
    record.evidenceReferencesRecorded = true ->
    record.evidenceDependenciesCurrent = false ->
    SafetyCaseRouteFor record = SafetyCaseRoute.requireEvidenceRepair := by
  intro deploymentContext topClaim hazardModel argumentStrategies evidenceReferences staleEvidence
  unfold SafetyCaseRouteFor
  simp [deploymentContext, topClaim, hazardModel, argumentStrategies,
    evidenceReferences, staleEvidence]

theorem missing_countercase_review_requires_review
    {record : SafetyCaseRecord} :
    record.deploymentContextRecorded = true ->
    record.topClaimScoped = true ->
    record.hazardModelRecorded = true ->
    record.argumentStrategiesRecorded = true ->
    record.evidenceReferencesRecorded = true ->
    record.evidenceDependenciesCurrent = true ->
    record.assumptionsRecorded = true ->
    record.countercaseReviewRecorded = false ->
    SafetyCaseRouteFor record = SafetyCaseRoute.requireCountercaseReview := by
  intro deploymentContext topClaim hazardModel argumentStrategies evidenceReferences
    evidenceCurrent assumptions missingCountercaseReview
  unfold SafetyCaseRouteFor
  simp [deploymentContext, topClaim, hazardModel, argumentStrategies,
    evidenceReferences, evidenceCurrent, assumptions, missingCountercaseReview]

theorem missing_independent_review_requires_review
    {record : SafetyCaseRecord} :
    record.deploymentContextRecorded = true ->
    record.topClaimScoped = true ->
    record.hazardModelRecorded = true ->
    record.argumentStrategiesRecorded = true ->
    record.evidenceReferencesRecorded = true ->
    record.evidenceDependenciesCurrent = true ->
    record.assumptionsRecorded = true ->
    record.countercaseReviewRecorded = true ->
    record.independentReviewRecorded = false ->
    SafetyCaseRouteFor record = SafetyCaseRoute.requireIndependentReview := by
  intro deploymentContext topClaim hazardModel argumentStrategies evidenceReferences
    evidenceCurrent assumptions countercaseReview missingIndependentReview
  unfold SafetyCaseRouteFor
  simp [deploymentContext, topClaim, hazardModel, argumentStrategies,
    evidenceReferences, evidenceCurrent, assumptions, countercaseReview,
    missingIndependentReview]

theorem unresolved_defeater_requires_accountable_review
    {record : SafetyCaseRecord} :
    record.deploymentContextRecorded = true ->
    record.topClaimScoped = true ->
    record.hazardModelRecorded = true ->
    record.argumentStrategiesRecorded = true ->
    record.evidenceReferencesRecorded = true ->
    record.evidenceDependenciesCurrent = true ->
    record.assumptionsRecorded = true ->
    record.countercaseReviewRecorded = true ->
    record.independentReviewRecorded = true ->
    record.unresolvedDefeaterPresent = true ->
    record.acceptanceCriterionRecorded = true ->
    record.residualOwnerRecorded = true ->
    record.decisionAuthorityRecorded = true ->
    record.affectedReleaseRequested = true ->
    SafetyCaseRouteFor record = SafetyCaseRoute.requireAccountableReview := by
  intro deploymentContext topClaim hazardModel argumentStrategies evidenceReferences
    evidenceCurrent assumptions countercaseReview independentReview unresolvedDefeater
    acceptanceCriterion residualOwner decisionAuthority releaseRequested
  unfold SafetyCaseRouteFor
  simp [deploymentContext, topClaim, hazardModel, argumentStrategies,
    evidenceReferences, evidenceCurrent, assumptions, countercaseReview,
    independentReview, unresolvedDefeater]

theorem case_cannot_launder_release_authority
    {record : SafetyCaseRecord} :
    record.deploymentContextRecorded = true ->
    record.topClaimScoped = true ->
    record.hazardModelRecorded = true ->
    record.argumentStrategiesRecorded = true ->
    record.evidenceReferencesRecorded = true ->
    record.evidenceDependenciesCurrent = true ->
    record.assumptionsRecorded = true ->
    record.countercaseReviewRecorded = true ->
    record.independentReviewRecorded = true ->
    record.unresolvedDefeaterPresent = false ->
    record.acceptanceCriterionRecorded = true ->
    record.residualOwnerRecorded = true ->
    record.decisionAuthorityRecorded = true ->
    record.authoritySeparationRecorded = false ->
    record.affectedReleaseRequested = true ->
    SafetyCaseRouteFor record = SafetyCaseRoute.rejectAuthorityLaundering := by
  intro deploymentContext topClaim hazardModel argumentStrategies evidenceReferences
    evidenceCurrent assumptions countercaseReview independentReview noDefeater
    acceptanceCriterion residualOwner decisionAuthority missingSeparation releaseRequested
  unfold SafetyCaseRouteFor
  simp [deploymentContext, topClaim, hazardModel, argumentStrategies,
    evidenceReferences, evidenceCurrent, assumptions, countercaseReview,
    independentReview, noDefeater, acceptanceCriterion, residualOwner,
    decisionAuthority, missingSeparation]

end AsiStackProofs.SafetyCases
