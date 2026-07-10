namespace AsiStackProofs.SafetyCases

inductive SafetyCaseRoute where
  | retainAsCaseDraft
  | requireCaseRepair
  | requireCountercaseReview
  | requireAccountableReview
  | releaseToReadinessReview
deriving DecidableEq, Repr

structure SafetyCaseRecord where
  deploymentContextRecorded : Bool
  topClaimScoped : Bool
  hazardModelRecorded : Bool
  argumentStrategiesRecorded : Bool
  evidenceReferencesRecorded : Bool
  assumptionsRecorded : Bool
  countercaseReviewRecorded : Bool
  unresolvedDefeaterPresent : Bool
  acceptanceCriterionRecorded : Bool
  residualOwnerRecorded : Bool
  decisionAuthorityRecorded : Bool
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
  else if record.assumptionsRecorded = false then
    SafetyCaseRoute.requireCaseRepair
  else if record.countercaseReviewRecorded = false then
    SafetyCaseRoute.requireCountercaseReview
  else if record.unresolvedDefeaterPresent = true then
    SafetyCaseRoute.requireAccountableReview
  else if record.acceptanceCriterionRecorded = false then
    SafetyCaseRoute.requireCaseRepair
  else if record.residualOwnerRecorded = false then
    SafetyCaseRoute.requireCaseRepair
  else if record.decisionAuthorityRecorded = false then
    SafetyCaseRoute.requireAccountableReview
  else if record.affectedReleaseRequested = true then
    SafetyCaseRoute.releaseToReadinessReview
  else
    SafetyCaseRoute.retainAsCaseDraft

theorem unresolved_defeater_requires_accountable_review
    {record : SafetyCaseRecord} :
    record.deploymentContextRecorded = true ->
    record.topClaimScoped = true ->
    record.hazardModelRecorded = true ->
    record.argumentStrategiesRecorded = true ->
    record.evidenceReferencesRecorded = true ->
    record.assumptionsRecorded = true ->
    record.countercaseReviewRecorded = true ->
    record.unresolvedDefeaterPresent = true ->
    record.acceptanceCriterionRecorded = true ->
    record.residualOwnerRecorded = true ->
    record.decisionAuthorityRecorded = true ->
    record.affectedReleaseRequested = true ->
    SafetyCaseRouteFor record = SafetyCaseRoute.requireAccountableReview := by
  intro deploymentContext topClaim hazardModel argumentStrategies evidenceReferences
    assumptions countercaseReview unresolvedDefeater acceptanceCriterion
    residualOwner decisionAuthority releaseRequested
  unfold SafetyCaseRouteFor
  simp [deploymentContext, topClaim, hazardModel, argumentStrategies,
    evidenceReferences, assumptions, countercaseReview, unresolvedDefeater]

theorem missing_countercase_review_requires_review
    {record : SafetyCaseRecord} :
    record.deploymentContextRecorded = true ->
    record.topClaimScoped = true ->
    record.hazardModelRecorded = true ->
    record.argumentStrategiesRecorded = true ->
    record.evidenceReferencesRecorded = true ->
    record.assumptionsRecorded = true ->
    record.countercaseReviewRecorded = false ->
    SafetyCaseRouteFor record = SafetyCaseRoute.requireCountercaseReview := by
  intro deploymentContext topClaim hazardModel argumentStrategies evidenceReferences
    assumptions missingCountercaseReview
  unfold SafetyCaseRouteFor
  simp [deploymentContext, topClaim, hazardModel, argumentStrategies,
    evidenceReferences, assumptions, missingCountercaseReview]

end AsiStackProofs.SafetyCases
