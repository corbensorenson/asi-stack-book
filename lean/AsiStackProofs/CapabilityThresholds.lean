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

end AsiStackProofs.CapabilityThresholds
