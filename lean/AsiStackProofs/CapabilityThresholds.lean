namespace AsiStackProofs.CapabilityThresholds

inductive ThresholdCommitmentRoute where
  | retainAsAssessmentDraft
  | requireReevaluation
  | requireAccountableException
  | blockAffectedRelease
  | releaseToReadinessReview
deriving DecidableEq, Repr

structure ThresholdCommitmentRecord where
  capabilityDomainRecorded : Bool
  threatModelRecorded : Bool
  evaluationEnvelopeRecorded : Bool
  elicitationRecorded : Bool
  thresholdDefinitionRecorded : Bool
  coverageDateRecorded : Bool
  baselineRecorded : Bool
  uncertaintyRecorded : Bool
  thresholdCrossed : Bool
  requiredSafeguardsRecorded : Bool
  safeguardsVerified : Bool
  residualOwnerRecorded : Bool
  releaseDecisionRequested : Bool
deriving DecidableEq, Repr

def ThresholdCommitmentRouteFor
    (record : ThresholdCommitmentRecord) :
    ThresholdCommitmentRoute :=
  if record.capabilityDomainRecorded = false then
    ThresholdCommitmentRoute.retainAsAssessmentDraft
  else if record.threatModelRecorded = false then
    ThresholdCommitmentRoute.requireReevaluation
  else if record.evaluationEnvelopeRecorded = false then
    ThresholdCommitmentRoute.requireReevaluation
  else if record.elicitationRecorded = false then
    ThresholdCommitmentRoute.requireReevaluation
  else if record.thresholdDefinitionRecorded = false then
    ThresholdCommitmentRoute.requireReevaluation
  else if record.coverageDateRecorded = false then
    ThresholdCommitmentRoute.requireReevaluation
  else if record.baselineRecorded = false then
    ThresholdCommitmentRoute.requireReevaluation
  else if record.uncertaintyRecorded = false then
    ThresholdCommitmentRoute.requireReevaluation
  else if record.residualOwnerRecorded = false then
    ThresholdCommitmentRoute.requireAccountableException
  else if record.thresholdCrossed = true &&
      record.requiredSafeguardsRecorded = false then
    ThresholdCommitmentRoute.blockAffectedRelease
  else if record.thresholdCrossed = true &&
      record.safeguardsVerified = false then
    ThresholdCommitmentRoute.blockAffectedRelease
  else if record.releaseDecisionRequested = true then
    ThresholdCommitmentRoute.releaseToReadinessReview
  else
    ThresholdCommitmentRoute.retainAsAssessmentDraft

theorem crossed_threshold_without_verified_safeguards_blocks_release
    {record : ThresholdCommitmentRecord} :
    record.capabilityDomainRecorded = true ->
    record.threatModelRecorded = true ->
    record.evaluationEnvelopeRecorded = true ->
    record.elicitationRecorded = true ->
    record.thresholdDefinitionRecorded = true ->
    record.coverageDateRecorded = true ->
    record.baselineRecorded = true ->
    record.uncertaintyRecorded = true ->
    record.thresholdCrossed = true ->
    record.requiredSafeguardsRecorded = true ->
    record.safeguardsVerified = false ->
    record.residualOwnerRecorded = true ->
    record.releaseDecisionRequested = true ->
    ThresholdCommitmentRouteFor record =
      ThresholdCommitmentRoute.blockAffectedRelease := by
  intro capabilityDomain threatModel evaluationEnvelope elicitation
    thresholdDefinition coverageDate baseline uncertainty thresholdCrossed
    requiredSafeguards missingSafeguardVerification residualOwner releaseRequested
  unfold ThresholdCommitmentRouteFor
  simp [capabilityDomain, threatModel, evaluationEnvelope, elicitation,
    thresholdDefinition, coverageDate, baseline, uncertainty, thresholdCrossed,
    requiredSafeguards, missingSafeguardVerification, residualOwner]

theorem missing_evaluation_envelope_requires_reevaluation
    {record : ThresholdCommitmentRecord} :
    record.capabilityDomainRecorded = true ->
    record.threatModelRecorded = true ->
    record.evaluationEnvelopeRecorded = false ->
    ThresholdCommitmentRouteFor record =
      ThresholdCommitmentRoute.requireReevaluation := by
  intro capabilityDomain threatModel missingEvaluationEnvelope
  unfold ThresholdCommitmentRouteFor
  simp [capabilityDomain, threatModel, missingEvaluationEnvelope]

theorem complete_crossed_threshold_reaches_readiness_review
    {record : ThresholdCommitmentRecord} :
    record.capabilityDomainRecorded = true -> record.threatModelRecorded = true ->
    record.evaluationEnvelopeRecorded = true -> record.elicitationRecorded = true ->
    record.thresholdDefinitionRecorded = true -> record.coverageDateRecorded = true ->
    record.baselineRecorded = true -> record.uncertaintyRecorded = true ->
    record.residualOwnerRecorded = true -> record.thresholdCrossed = true ->
    record.requiredSafeguardsRecorded = true -> record.safeguardsVerified = true ->
    record.releaseDecisionRequested = true ->
    ThresholdCommitmentRouteFor record = ThresholdCommitmentRoute.releaseToReadinessReview := by
  intro domain threat envelope elicitation threshold coverage baseline uncertainty residual crossed required verified release
  unfold ThresholdCommitmentRouteFor
  simp [domain, threat, envelope, elicitation, threshold, coverage, baseline,
    uncertainty, residual, crossed, required, verified, release]

theorem complete_non_crossing_reaches_readiness_review
    {record : ThresholdCommitmentRecord} :
    record.capabilityDomainRecorded = true -> record.threatModelRecorded = true ->
    record.evaluationEnvelopeRecorded = true -> record.elicitationRecorded = true ->
    record.thresholdDefinitionRecorded = true -> record.coverageDateRecorded = true ->
    record.baselineRecorded = true -> record.uncertaintyRecorded = true ->
    record.residualOwnerRecorded = true -> record.thresholdCrossed = false ->
    record.releaseDecisionRequested = true ->
    ThresholdCommitmentRouteFor record = ThresholdCommitmentRoute.releaseToReadinessReview := by
  intro domain threat envelope elicitation threshold coverage baseline uncertainty residual notCrossed release
  unfold ThresholdCommitmentRouteFor
  simp [domain, threat, envelope, elicitation, threshold, coverage, baseline,
    uncertainty, residual, notCrossed, release]

theorem missing_baseline_requires_reevaluation
    {record : ThresholdCommitmentRecord} :
    record.capabilityDomainRecorded = true -> record.threatModelRecorded = true ->
    record.evaluationEnvelopeRecorded = true -> record.elicitationRecorded = true ->
    record.thresholdDefinitionRecorded = true -> record.coverageDateRecorded = true ->
    record.baselineRecorded = false ->
    ThresholdCommitmentRouteFor record = ThresholdCommitmentRoute.requireReevaluation := by
  intro domain threat envelope elicitation threshold coverage baseline
  unfold ThresholdCommitmentRouteFor
  simp [domain, threat, envelope, elicitation, threshold, coverage, baseline]

theorem missing_uncertainty_requires_reevaluation
    {record : ThresholdCommitmentRecord} :
    record.capabilityDomainRecorded = true -> record.threatModelRecorded = true ->
    record.evaluationEnvelopeRecorded = true -> record.elicitationRecorded = true ->
    record.thresholdDefinitionRecorded = true -> record.coverageDateRecorded = true ->
    record.baselineRecorded = true -> record.uncertaintyRecorded = false ->
    ThresholdCommitmentRouteFor record = ThresholdCommitmentRoute.requireReevaluation := by
  intro domain threat envelope elicitation threshold coverage baseline uncertainty
  unfold ThresholdCommitmentRouteFor
  simp [domain, threat, envelope, elicitation, threshold, coverage, baseline, uncertainty]

theorem missing_residual_owner_requires_accountable_exception
    {record : ThresholdCommitmentRecord} :
    record.capabilityDomainRecorded = true -> record.threatModelRecorded = true ->
    record.evaluationEnvelopeRecorded = true -> record.elicitationRecorded = true ->
    record.thresholdDefinitionRecorded = true -> record.coverageDateRecorded = true ->
    record.baselineRecorded = true -> record.uncertaintyRecorded = true ->
    record.residualOwnerRecorded = false ->
    ThresholdCommitmentRouteFor record = ThresholdCommitmentRoute.requireAccountableException := by
  intro domain threat envelope elicitation threshold coverage baseline uncertainty residual
  unfold ThresholdCommitmentRouteFor
  simp [domain, threat, envelope, elicitation, threshold, coverage, baseline, uncertainty, residual]

theorem crossed_threshold_without_safeguard_record_blocks_release
    {record : ThresholdCommitmentRecord} :
    record.capabilityDomainRecorded = true -> record.threatModelRecorded = true ->
    record.evaluationEnvelopeRecorded = true -> record.elicitationRecorded = true ->
    record.thresholdDefinitionRecorded = true -> record.coverageDateRecorded = true ->
    record.baselineRecorded = true -> record.uncertaintyRecorded = true ->
    record.residualOwnerRecorded = true -> record.thresholdCrossed = true ->
    record.requiredSafeguardsRecorded = false ->
    ThresholdCommitmentRouteFor record = ThresholdCommitmentRoute.blockAffectedRelease := by
  intro domain threat envelope elicitation threshold coverage baseline uncertainty residual crossed required
  unfold ThresholdCommitmentRouteFor
  simp [domain, threat, envelope, elicitation, threshold, coverage, baseline,
    uncertainty, residual, crossed, required]

end AsiStackProofs.CapabilityThresholds
