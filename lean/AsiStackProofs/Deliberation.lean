namespace AsiStackProofs.Deliberation

inductive DeliberationAdmissionRoute where
  | retainAsDraft
  | requireIndependentReview
  | stopAndEscrowResidual
  | releaseToPlanning
deriving DecidableEq, Repr

structure DeliberationAdmissionRecord where
  requestRecorded : Bool
  highRiskRequest : Bool
  thinkBudgetRecorded : Bool
  searchModeRecorded : Bool
  verifierScopeRecorded : Bool
  independentVerifierRecorded : Bool
  stopConditionRecorded : Bool
  residualOwnerRecorded : Bool
  budgetExhausted : Bool
  executionRequested : Bool
deriving DecidableEq, Repr

def DeliberationAdmissionRouteFor
    (record : DeliberationAdmissionRecord) :
    DeliberationAdmissionRoute :=
  if record.requestRecorded = false then
    DeliberationAdmissionRoute.retainAsDraft
  else if record.thinkBudgetRecorded = false then
    DeliberationAdmissionRoute.requireIndependentReview
  else if record.searchModeRecorded = false then
    DeliberationAdmissionRoute.requireIndependentReview
  else if record.verifierScopeRecorded = false then
    DeliberationAdmissionRoute.requireIndependentReview
  else if record.stopConditionRecorded = false then
    DeliberationAdmissionRoute.requireIndependentReview
  else if record.residualOwnerRecorded = false then
    DeliberationAdmissionRoute.requireIndependentReview
  else if record.budgetExhausted = true then
    DeliberationAdmissionRoute.stopAndEscrowResidual
  else if record.executionRequested = true && record.highRiskRequest = true &&
      record.independentVerifierRecorded = false then
    DeliberationAdmissionRoute.requireIndependentReview
  else if record.executionRequested = true then
    DeliberationAdmissionRoute.releaseToPlanning
  else
    DeliberationAdmissionRoute.retainAsDraft

theorem missing_independent_verifier_blocks_high_risk_execution
    {record : DeliberationAdmissionRecord} :
    record.requestRecorded = true ->
    record.highRiskRequest = true ->
    record.thinkBudgetRecorded = true ->
    record.searchModeRecorded = true ->
    record.verifierScopeRecorded = true ->
    record.independentVerifierRecorded = false ->
    record.stopConditionRecorded = true ->
    record.residualOwnerRecorded = true ->
    record.budgetExhausted = false ->
    record.executionRequested = true ->
    DeliberationAdmissionRouteFor record =
      DeliberationAdmissionRoute.requireIndependentReview := by
  intro requestRecorded highRisk thinkBudget searchMode verifierScope
    missingIndependentVerifier stopCondition residualOwner budgetNotExhausted executionRequested
  unfold DeliberationAdmissionRouteFor
  simp [requestRecorded, highRisk, thinkBudget, searchMode, verifierScope,
    missingIndependentVerifier, stopCondition, residualOwner, budgetNotExhausted,
    executionRequested]

theorem exhausted_deliberation_budget_escrows_residual
    {record : DeliberationAdmissionRecord} :
    record.requestRecorded = true ->
    record.thinkBudgetRecorded = true ->
    record.searchModeRecorded = true ->
    record.verifierScopeRecorded = true ->
    record.stopConditionRecorded = true ->
    record.residualOwnerRecorded = true ->
    record.budgetExhausted = true ->
    DeliberationAdmissionRouteFor record =
      DeliberationAdmissionRoute.stopAndEscrowResidual := by
  intro requestRecorded thinkBudget searchMode verifierScope stopCondition residualOwner exhausted
  unfold DeliberationAdmissionRouteFor
  simp [requestRecorded, thinkBudget, searchMode, verifierScope, stopCondition,
    residualOwner, exhausted]

end AsiStackProofs.Deliberation
