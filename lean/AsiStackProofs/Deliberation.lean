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
  candidateHistoryRecorded : Bool
  stopConditionRecorded : Bool
  residualOwnerRecorded : Bool
  traceAuthoritySeparated : Bool
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
  else if record.candidateHistoryRecorded = false then
    DeliberationAdmissionRoute.requireIndependentReview
  else if record.stopConditionRecorded = false then
    DeliberationAdmissionRoute.requireIndependentReview
  else if record.residualOwnerRecorded = false then
    DeliberationAdmissionRoute.requireIndependentReview
  else if record.traceAuthoritySeparated = false then
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
    record.candidateHistoryRecorded = true ->
    record.stopConditionRecorded = true ->
    record.residualOwnerRecorded = true ->
    record.traceAuthoritySeparated = true ->
    record.budgetExhausted = false ->
    record.executionRequested = true ->
    DeliberationAdmissionRouteFor record =
      DeliberationAdmissionRoute.requireIndependentReview := by
  intro requestRecorded highRisk thinkBudget searchMode verifierScope
    missingIndependentVerifier candidateHistory stopCondition residualOwner
    traceAuthority budgetNotExhausted executionRequested
  unfold DeliberationAdmissionRouteFor
  simp [requestRecorded, highRisk, thinkBudget, searchMode, verifierScope,
    missingIndependentVerifier, candidateHistory, stopCondition, residualOwner,
    traceAuthority, budgetNotExhausted, executionRequested]

theorem trace_cannot_launder_execution_authority
    {record : DeliberationAdmissionRecord} :
    record.requestRecorded = true -> record.thinkBudgetRecorded = true ->
    record.searchModeRecorded = true -> record.verifierScopeRecorded = true ->
    record.candidateHistoryRecorded = true -> record.stopConditionRecorded = true ->
    record.residualOwnerRecorded = true -> record.traceAuthoritySeparated = false ->
    DeliberationAdmissionRouteFor record = DeliberationAdmissionRoute.requireIndependentReview := by
  intro request budget mode verifier history stop residual trace
  unfold DeliberationAdmissionRouteFor
  simp [request, budget, mode, verifier, history, stop, residual, trace]

end AsiStackProofs.Deliberation
