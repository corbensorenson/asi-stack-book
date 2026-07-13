namespace AsiStackProofs.OpenEndedImprovement

inductive CampaignAdmissionRoute where
  | retainAsDraft
  | requireEvaluatorSeparation
  | requireBudgetRepair
  | requireStopAuthority
  | requireArchiveRepair
  | requireResidualOwner
  | rejectAuthorityLaundering
  | releaseToGovernorReview
deriving DecidableEq, Repr

structure CampaignAdmissionRecord where
  objectiveDigestRecorded : Bool
  taskPolicyDigestRecorded : Bool
  generatorIdentityRecorded : Bool
  evaluatorIdentityRecorded : Bool
  evaluatorDependenciesRecorded : Bool
  independentQualificationRecorded : Bool
  resourceBillRecorded : Bool
  withinRegisteredBudget : Bool
  stopAuthorityRecorded : Bool
  failureHistoryPreserved : Bool
  archiveDispositionRecorded : Bool
  residualOwnerRecorded : Bool
  permittedConsumerRecorded : Bool
  noAuthorityGrantRecorded : Bool
  admissionRequested : Bool
deriving DecidableEq, Repr

def CampaignAdmissionRouteFor
    (record : CampaignAdmissionRecord) : CampaignAdmissionRoute :=
  if record.objectiveDigestRecorded = false then
    CampaignAdmissionRoute.retainAsDraft
  else if record.taskPolicyDigestRecorded = false then
    CampaignAdmissionRoute.retainAsDraft
  else if record.generatorIdentityRecorded = false then
    CampaignAdmissionRoute.retainAsDraft
  else if record.evaluatorIdentityRecorded = false then
    CampaignAdmissionRoute.requireEvaluatorSeparation
  else if record.evaluatorDependenciesRecorded = false then
    CampaignAdmissionRoute.requireEvaluatorSeparation
  else if record.independentQualificationRecorded = false then
    CampaignAdmissionRoute.requireEvaluatorSeparation
  else if record.resourceBillRecorded = false ||
      record.withinRegisteredBudget = false then
    CampaignAdmissionRoute.requireBudgetRepair
  else if record.stopAuthorityRecorded = false then
    CampaignAdmissionRoute.requireStopAuthority
  else if record.failureHistoryPreserved = false ||
      record.archiveDispositionRecorded = false then
    CampaignAdmissionRoute.requireArchiveRepair
  else if record.residualOwnerRecorded = false then
    CampaignAdmissionRoute.requireResidualOwner
  else if record.permittedConsumerRecorded = false then
    CampaignAdmissionRoute.retainAsDraft
  else if record.admissionRequested = true &&
      record.noAuthorityGrantRecorded = false then
    CampaignAdmissionRoute.rejectAuthorityLaundering
  else if record.admissionRequested = true then
    CampaignAdmissionRoute.releaseToGovernorReview
  else
    CampaignAdmissionRoute.retainAsDraft

theorem complete_candidate_reaches_governor_review
    {record : CampaignAdmissionRecord} :
    record.objectiveDigestRecorded = true ->
    record.taskPolicyDigestRecorded = true ->
    record.generatorIdentityRecorded = true ->
    record.evaluatorIdentityRecorded = true ->
    record.evaluatorDependenciesRecorded = true ->
    record.independentQualificationRecorded = true ->
    record.resourceBillRecorded = true ->
    record.withinRegisteredBudget = true ->
    record.stopAuthorityRecorded = true ->
    record.failureHistoryPreserved = true ->
    record.archiveDispositionRecorded = true ->
    record.residualOwnerRecorded = true ->
    record.permittedConsumerRecorded = true ->
    record.noAuthorityGrantRecorded = true ->
    record.admissionRequested = true ->
    CampaignAdmissionRouteFor record =
      CampaignAdmissionRoute.releaseToGovernorReview := by
  intro objective policy generator evaluator dependencies qualification bill
    budget stop failures archive residual consumer noAuthority requested
  unfold CampaignAdmissionRouteFor
  simp [objective, policy, generator, evaluator, dependencies, qualification,
    bill, budget, stop, failures, archive, residual, consumer, noAuthority,
    requested]

theorem missing_independent_qualification_requires_separation
    {record : CampaignAdmissionRecord} :
    record.objectiveDigestRecorded = true ->
    record.taskPolicyDigestRecorded = true ->
    record.generatorIdentityRecorded = true ->
    record.evaluatorIdentityRecorded = true ->
    record.evaluatorDependenciesRecorded = true ->
    record.independentQualificationRecorded = false ->
    CampaignAdmissionRouteFor record =
      CampaignAdmissionRoute.requireEvaluatorSeparation := by
  intro objective policy generator evaluator dependencies missingQualification
  unfold CampaignAdmissionRouteFor
  simp [objective, policy, generator, evaluator, dependencies,
    missingQualification]

theorem exhausted_budget_requires_repair
    {record : CampaignAdmissionRecord} :
    record.objectiveDigestRecorded = true ->
    record.taskPolicyDigestRecorded = true ->
    record.generatorIdentityRecorded = true ->
    record.evaluatorIdentityRecorded = true ->
    record.evaluatorDependenciesRecorded = true ->
    record.independentQualificationRecorded = true ->
    record.resourceBillRecorded = true ->
    record.withinRegisteredBudget = false ->
    CampaignAdmissionRouteFor record =
      CampaignAdmissionRoute.requireBudgetRepair := by
  intro objective policy generator evaluator dependencies qualification bill
    exhausted
  unfold CampaignAdmissionRouteFor
  simp [objective, policy, generator, evaluator, dependencies, qualification,
    bill, exhausted]

theorem missing_stop_authority_blocks_admission
    {record : CampaignAdmissionRecord} :
    record.objectiveDigestRecorded = true ->
    record.taskPolicyDigestRecorded = true ->
    record.generatorIdentityRecorded = true ->
    record.evaluatorIdentityRecorded = true ->
    record.evaluatorDependenciesRecorded = true ->
    record.independentQualificationRecorded = true ->
    record.resourceBillRecorded = true ->
    record.withinRegisteredBudget = true ->
    record.stopAuthorityRecorded = false ->
    CampaignAdmissionRouteFor record =
      CampaignAdmissionRoute.requireStopAuthority := by
  intro objective policy generator evaluator dependencies qualification bill
    budget missingStop
  unfold CampaignAdmissionRouteFor
  simp [objective, policy, generator, evaluator, dependencies, qualification,
    bill, budget, missingStop]

theorem erased_failure_history_requires_archive_repair
    {record : CampaignAdmissionRecord} :
    record.objectiveDigestRecorded = true ->
    record.taskPolicyDigestRecorded = true ->
    record.generatorIdentityRecorded = true ->
    record.evaluatorIdentityRecorded = true ->
    record.evaluatorDependenciesRecorded = true ->
    record.independentQualificationRecorded = true ->
    record.resourceBillRecorded = true ->
    record.withinRegisteredBudget = true ->
    record.stopAuthorityRecorded = true ->
    record.failureHistoryPreserved = false ->
    CampaignAdmissionRouteFor record =
      CampaignAdmissionRoute.requireArchiveRepair := by
  intro objective policy generator evaluator dependencies qualification bill
    budget stop erasedFailures
  unfold CampaignAdmissionRouteFor
  simp [objective, policy, generator, evaluator, dependencies, qualification,
    bill, budget, stop, erasedFailures]

theorem missing_residual_owner_blocks_admission
    {record : CampaignAdmissionRecord} :
    record.objectiveDigestRecorded = true ->
    record.taskPolicyDigestRecorded = true ->
    record.generatorIdentityRecorded = true ->
    record.evaluatorIdentityRecorded = true ->
    record.evaluatorDependenciesRecorded = true ->
    record.independentQualificationRecorded = true ->
    record.resourceBillRecorded = true ->
    record.withinRegisteredBudget = true ->
    record.stopAuthorityRecorded = true ->
    record.failureHistoryPreserved = true ->
    record.archiveDispositionRecorded = true ->
    record.residualOwnerRecorded = false ->
    CampaignAdmissionRouteFor record =
      CampaignAdmissionRoute.requireResidualOwner := by
  intro objective policy generator evaluator dependencies qualification bill
    budget stop failures archive missingResidual
  unfold CampaignAdmissionRouteFor
  simp [objective, policy, generator, evaluator, dependencies, qualification,
    bill, budget, stop, failures, archive, missingResidual]

theorem candidate_cannot_launder_admission_authority
    {record : CampaignAdmissionRecord} :
    record.objectiveDigestRecorded = true ->
    record.taskPolicyDigestRecorded = true ->
    record.generatorIdentityRecorded = true ->
    record.evaluatorIdentityRecorded = true ->
    record.evaluatorDependenciesRecorded = true ->
    record.independentQualificationRecorded = true ->
    record.resourceBillRecorded = true ->
    record.withinRegisteredBudget = true ->
    record.stopAuthorityRecorded = true ->
    record.failureHistoryPreserved = true ->
    record.archiveDispositionRecorded = true ->
    record.residualOwnerRecorded = true ->
    record.permittedConsumerRecorded = true ->
    record.admissionRequested = true ->
    record.noAuthorityGrantRecorded = false ->
    CampaignAdmissionRouteFor record =
      CampaignAdmissionRoute.rejectAuthorityLaundering := by
  intro objective policy generator evaluator dependencies qualification bill
    budget stop failures archive residual consumer requested authorityLaundering
  unfold CampaignAdmissionRouteFor
  simp [objective, policy, generator, evaluator, dependencies, qualification,
    bill, budget, stop, failures, archive, residual, consumer, requested,
    authorityLaundering]

end AsiStackProofs.OpenEndedImprovement
