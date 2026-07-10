namespace AsiStackProofs.ScalableOversight

inductive OversightAdmissionRoute where
  | retainAsProtocolDraft
  | requireProtocolRedesign
  | requireAccountableEscalation
  | releaseToBoundedReview
deriving DecidableEq, Repr

structure OversightProtocolRecord where
  taskScopeRecorded : Bool
  authorityScopeRecorded : Bool
  highRiskRequest : Bool
  supervisorEnvelopeRecorded : Bool
  systemEnvelopeRecorded : Bool
  informationAccessRecorded : Bool
  rolesAndIncentivesRecorded : Bool
  directReviewBaselineRecorded : Bool
  independentOutcomeAuditRecorded : Bool
  correlationRiskRecorded : Bool
  residualOwnerRecorded : Bool
  escalationOwnerRecorded : Bool
  downstreamAdmissionRequested : Bool
deriving DecidableEq, Repr

def OversightAdmissionRouteFor
    (record : OversightProtocolRecord) :
    OversightAdmissionRoute :=
  if record.taskScopeRecorded = false then
    OversightAdmissionRoute.retainAsProtocolDraft
  else if record.authorityScopeRecorded = false then
    OversightAdmissionRoute.requireAccountableEscalation
  else if record.supervisorEnvelopeRecorded = false then
    OversightAdmissionRoute.requireAccountableEscalation
  else if record.systemEnvelopeRecorded = false then
    OversightAdmissionRoute.requireAccountableEscalation
  else if record.informationAccessRecorded = false then
    OversightAdmissionRoute.requireAccountableEscalation
  else if record.rolesAndIncentivesRecorded = false then
    OversightAdmissionRoute.requireAccountableEscalation
  else if record.directReviewBaselineRecorded = false then
    OversightAdmissionRoute.requireProtocolRedesign
  else if record.correlationRiskRecorded = false then
    OversightAdmissionRoute.requireAccountableEscalation
  else if record.residualOwnerRecorded = false then
    OversightAdmissionRoute.requireAccountableEscalation
  else if record.escalationOwnerRecorded = false then
    OversightAdmissionRoute.requireAccountableEscalation
  else if record.highRiskRequest = true &&
      record.downstreamAdmissionRequested = true &&
      record.independentOutcomeAuditRecorded = false then
    OversightAdmissionRoute.requireAccountableEscalation
  else if record.downstreamAdmissionRequested = true then
    OversightAdmissionRoute.releaseToBoundedReview
  else
    OversightAdmissionRoute.retainAsProtocolDraft

theorem missing_outcome_audit_blocks_high_risk_admission
    {record : OversightProtocolRecord} :
    record.taskScopeRecorded = true ->
    record.authorityScopeRecorded = true ->
    record.highRiskRequest = true ->
    record.supervisorEnvelopeRecorded = true ->
    record.systemEnvelopeRecorded = true ->
    record.informationAccessRecorded = true ->
    record.rolesAndIncentivesRecorded = true ->
    record.directReviewBaselineRecorded = true ->
    record.independentOutcomeAuditRecorded = false ->
    record.correlationRiskRecorded = true ->
    record.residualOwnerRecorded = true ->
    record.escalationOwnerRecorded = true ->
    record.downstreamAdmissionRequested = true ->
    OversightAdmissionRouteFor record =
      OversightAdmissionRoute.requireAccountableEscalation := by
  intro taskScope authorityScope highRisk supervisorEnvelope systemEnvelope
    informationAccess rolesAndIncentives directReviewBaseline missingOutcomeAudit
    correlationRisk residualOwner escalationOwner downstreamAdmission
  unfold OversightAdmissionRouteFor
  simp [taskScope, authorityScope, highRisk, supervisorEnvelope, systemEnvelope,
    informationAccess, rolesAndIncentives, directReviewBaseline, missingOutcomeAudit,
    correlationRisk, residualOwner, escalationOwner, downstreamAdmission]

theorem missing_baseline_requires_protocol_redesign
    {record : OversightProtocolRecord} :
    record.taskScopeRecorded = true ->
    record.authorityScopeRecorded = true ->
    record.supervisorEnvelopeRecorded = true ->
    record.systemEnvelopeRecorded = true ->
    record.informationAccessRecorded = true ->
    record.rolesAndIncentivesRecorded = true ->
    record.directReviewBaselineRecorded = false ->
    OversightAdmissionRouteFor record =
      OversightAdmissionRoute.requireProtocolRedesign := by
  intro taskScope authorityScope supervisorEnvelope systemEnvelope informationAccess
    rolesAndIncentives missingBaseline
  unfold OversightAdmissionRouteFor
  simp [taskScope, authorityScope, supervisorEnvelope, systemEnvelope,
    informationAccess, rolesAndIncentives, missingBaseline]

end AsiStackProofs.ScalableOversight
