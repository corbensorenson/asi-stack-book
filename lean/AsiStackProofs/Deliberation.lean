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

theorem exhausted_deliberation_budget_escrows_residual
    {record : DeliberationAdmissionRecord} :
    record.requestRecorded = true ->
    record.thinkBudgetRecorded = true ->
    record.searchModeRecorded = true ->
    record.verifierScopeRecorded = true ->
    record.candidateHistoryRecorded = true ->
    record.stopConditionRecorded = true ->
    record.residualOwnerRecorded = true ->
    record.traceAuthoritySeparated = true ->
    record.budgetExhausted = true ->
    DeliberationAdmissionRouteFor record =
      DeliberationAdmissionRoute.stopAndEscrowResidual := by
  intro requestRecorded thinkBudget searchMode verifierScope candidateHistory stopCondition
    residualOwner traceAuthority exhausted
  unfold DeliberationAdmissionRouteFor
  simp [requestRecorded, thinkBudget, searchMode, verifierScope, candidateHistory,
    stopCondition, residualOwner, traceAuthority, exhausted]

theorem complete_high_risk_record_reaches_planning
    {record : DeliberationAdmissionRecord} :
    record.requestRecorded = true -> record.highRiskRequest = true ->
    record.thinkBudgetRecorded = true -> record.searchModeRecorded = true ->
    record.verifierScopeRecorded = true -> record.independentVerifierRecorded = true ->
    record.candidateHistoryRecorded = true -> record.stopConditionRecorded = true ->
    record.residualOwnerRecorded = true -> record.traceAuthoritySeparated = true ->
    record.budgetExhausted = false -> record.executionRequested = true ->
    DeliberationAdmissionRouteFor record = DeliberationAdmissionRoute.releaseToPlanning := by
  intro request highRisk budget mode verifier independent history stop residual trace notExhausted execution
  unfold DeliberationAdmissionRouteFor
  simp [request, highRisk, budget, mode, verifier, independent, history, stop,
    residual, trace, notExhausted, execution]

theorem missing_budget_record_requires_review
    {record : DeliberationAdmissionRecord} :
    record.requestRecorded = true -> record.thinkBudgetRecorded = false ->
    DeliberationAdmissionRouteFor record = DeliberationAdmissionRoute.requireIndependentReview := by
  intro request budget
  unfold DeliberationAdmissionRouteFor
  simp [request, budget]

theorem missing_search_mode_requires_review
    {record : DeliberationAdmissionRecord} :
    record.requestRecorded = true -> record.thinkBudgetRecorded = true ->
    record.searchModeRecorded = false ->
    DeliberationAdmissionRouteFor record = DeliberationAdmissionRoute.requireIndependentReview := by
  intro request budget mode
  unfold DeliberationAdmissionRouteFor
  simp [request, budget, mode]

theorem missing_verifier_scope_requires_review
    {record : DeliberationAdmissionRecord} :
    record.requestRecorded = true -> record.thinkBudgetRecorded = true ->
    record.searchModeRecorded = true -> record.verifierScopeRecorded = false ->
    DeliberationAdmissionRouteFor record = DeliberationAdmissionRoute.requireIndependentReview := by
  intro request budget mode verifier
  unfold DeliberationAdmissionRouteFor
  simp [request, budget, mode, verifier]

theorem missing_candidate_history_requires_review
    {record : DeliberationAdmissionRecord} :
    record.requestRecorded = true -> record.thinkBudgetRecorded = true ->
    record.searchModeRecorded = true -> record.verifierScopeRecorded = true ->
    record.candidateHistoryRecorded = false ->
    DeliberationAdmissionRouteFor record = DeliberationAdmissionRoute.requireIndependentReview := by
  intro request budget mode verifier history
  unfold DeliberationAdmissionRouteFor
  simp [request, budget, mode, verifier, history]

theorem missing_stop_condition_requires_review
    {record : DeliberationAdmissionRecord} :
    record.requestRecorded = true -> record.thinkBudgetRecorded = true ->
    record.searchModeRecorded = true -> record.verifierScopeRecorded = true ->
    record.candidateHistoryRecorded = true -> record.stopConditionRecorded = false ->
    DeliberationAdmissionRouteFor record = DeliberationAdmissionRoute.requireIndependentReview := by
  intro request budget mode verifier history stop
  unfold DeliberationAdmissionRouteFor
  simp [request, budget, mode, verifier, history, stop]

theorem missing_residual_owner_requires_review
    {record : DeliberationAdmissionRecord} :
    record.requestRecorded = true -> record.thinkBudgetRecorded = true ->
    record.searchModeRecorded = true -> record.verifierScopeRecorded = true ->
    record.candidateHistoryRecorded = true -> record.stopConditionRecorded = true ->
    record.residualOwnerRecorded = false ->
    DeliberationAdmissionRouteFor record = DeliberationAdmissionRoute.requireIndependentReview := by
  intro request budget mode verifier history stop residual
  unfold DeliberationAdmissionRouteFor
  simp [request, budget, mode, verifier, history, stop, residual]

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
