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

inductive OversightUseRoute where
  | retainAsDraft
  | requireAccessRepair
  | requireProtocolRedesign
  | requireDependencyReview
  | requireOutcomeAudit
  | requireAbstentionEvidence
  | rejectAuthorityLaundering
  | admitBoundedUse
deriving DecidableEq, Repr

structure OversightUseRecord where
  protocolDigestRecorded : Bool
  taskCohortRecorded : Bool
  capabilityEnvelopesRecorded : Bool
  evidenceViewsRecorded : Bool
  sharedDependenciesRecorded : Bool
  directReviewBaselineRecorded : Bool
  independentOutcomeAuditRecorded : Bool
  residualRecorded : Bool
  permittedConsumerRecorded : Bool
  expiryRecorded : Bool
  noAuthorityGrantRecorded : Bool
  highRiskUse : Bool
  downstreamUseRequested : Bool
  abstentionRequested : Bool
  abstentionEvidenceRecorded : Bool
  abstentionDefeaterRecorded : Bool
deriving DecidableEq, Repr

def OversightUseRouteFor (record : OversightUseRecord) : OversightUseRoute :=
  if record.protocolDigestRecorded = false then
    OversightUseRoute.retainAsDraft
  else if record.taskCohortRecorded = false then
    OversightUseRoute.retainAsDraft
  else if record.capabilityEnvelopesRecorded = false then
    OversightUseRoute.requireAccessRepair
  else if record.evidenceViewsRecorded = false then
    OversightUseRoute.requireAccessRepair
  else if record.sharedDependenciesRecorded = false then
    OversightUseRoute.requireDependencyReview
  else if record.directReviewBaselineRecorded = false then
    OversightUseRoute.requireProtocolRedesign
  else if record.highRiskUse = true &&
      record.independentOutcomeAuditRecorded = false then
    OversightUseRoute.requireOutcomeAudit
  else if record.residualRecorded = false then
    OversightUseRoute.requireDependencyReview
  else if record.permittedConsumerRecorded = false then
    OversightUseRoute.retainAsDraft
  else if record.expiryRecorded = false then
    OversightUseRoute.retainAsDraft
  else if record.downstreamUseRequested = true &&
      record.noAuthorityGrantRecorded = false then
    OversightUseRoute.rejectAuthorityLaundering
  else if record.abstentionRequested = true &&
      (record.abstentionEvidenceRecorded = false ||
        record.abstentionDefeaterRecorded = false) then
    OversightUseRoute.requireAbstentionEvidence
  else if record.downstreamUseRequested = true then
    OversightUseRoute.admitBoundedUse
  else
    OversightUseRoute.retainAsDraft

theorem complete_bounded_use_is_admitted
    {record : OversightUseRecord} :
    record.protocolDigestRecorded = true ->
    record.taskCohortRecorded = true ->
    record.capabilityEnvelopesRecorded = true ->
    record.evidenceViewsRecorded = true ->
    record.sharedDependenciesRecorded = true ->
    record.directReviewBaselineRecorded = true ->
    record.independentOutcomeAuditRecorded = true ->
    record.residualRecorded = true ->
    record.permittedConsumerRecorded = true ->
    record.expiryRecorded = true ->
    record.noAuthorityGrantRecorded = true ->
    record.downstreamUseRequested = true ->
    record.abstentionRequested = false ->
    OversightUseRouteFor record = OversightUseRoute.admitBoundedUse := by
  intro digest cohort envelopes views dependencies baseline audit residual
    consumer expiry noAuthority downstream noAbstention
  unfold OversightUseRouteFor
  simp [digest, cohort, envelopes, views, dependencies, baseline, audit,
    residual, consumer, expiry, noAuthority, downstream, noAbstention]

theorem missing_evidence_views_requires_access_repair
    {record : OversightUseRecord} :
    record.protocolDigestRecorded = true ->
    record.taskCohortRecorded = true ->
    record.capabilityEnvelopesRecorded = true ->
    record.evidenceViewsRecorded = false ->
    OversightUseRouteFor record = OversightUseRoute.requireAccessRepair := by
  intro digest cohort envelopes missingViews
  unfold OversightUseRouteFor
  simp [digest, cohort, envelopes, missingViews]

theorem undisclosed_shared_dependencies_require_review
    {record : OversightUseRecord} :
    record.protocolDigestRecorded = true ->
    record.taskCohortRecorded = true ->
    record.capabilityEnvelopesRecorded = true ->
    record.evidenceViewsRecorded = true ->
    record.sharedDependenciesRecorded = false ->
    OversightUseRouteFor record = OversightUseRoute.requireDependencyReview := by
  intro digest cohort envelopes views missingDependencies
  unfold OversightUseRouteFor
  simp [digest, cohort, envelopes, views, missingDependencies]

theorem high_risk_use_without_outcome_audit_requires_audit
    {record : OversightUseRecord} :
    record.protocolDigestRecorded = true ->
    record.taskCohortRecorded = true ->
    record.capabilityEnvelopesRecorded = true ->
    record.evidenceViewsRecorded = true ->
    record.sharedDependenciesRecorded = true ->
    record.directReviewBaselineRecorded = true ->
    record.highRiskUse = true ->
    record.independentOutcomeAuditRecorded = false ->
    OversightUseRouteFor record = OversightUseRoute.requireOutcomeAudit := by
  intro digest cohort envelopes views dependencies baseline highRisk missingAudit
  unfold OversightUseRouteFor
  simp [digest, cohort, envelopes, views, dependencies, baseline, highRisk,
    missingAudit]

theorem unjustified_abstention_requires_evidence
    {record : OversightUseRecord} :
    record.protocolDigestRecorded = true ->
    record.taskCohortRecorded = true ->
    record.capabilityEnvelopesRecorded = true ->
    record.evidenceViewsRecorded = true ->
    record.sharedDependenciesRecorded = true ->
    record.directReviewBaselineRecorded = true ->
    record.highRiskUse = false ->
    record.residualRecorded = true ->
    record.permittedConsumerRecorded = true ->
    record.expiryRecorded = true ->
    record.downstreamUseRequested = true ->
    record.noAuthorityGrantRecorded = true ->
    record.abstentionRequested = true ->
    record.abstentionEvidenceRecorded = false ->
    OversightUseRouteFor record =
      OversightUseRoute.requireAbstentionEvidence := by
  intro digest cohort envelopes views dependencies baseline lowRisk residual
    consumer expiry downstream noAuthority abstention missingEvidence
  unfold OversightUseRouteFor
  simp [digest, cohort, envelopes, views, dependencies, baseline, lowRisk,
    residual, consumer, expiry, downstream, noAuthority, abstention,
    missingEvidence]

theorem downstream_use_cannot_launder_authority
    {record : OversightUseRecord} :
    record.protocolDigestRecorded = true ->
    record.taskCohortRecorded = true ->
    record.capabilityEnvelopesRecorded = true ->
    record.evidenceViewsRecorded = true ->
    record.sharedDependenciesRecorded = true ->
    record.directReviewBaselineRecorded = true ->
    record.highRiskUse = false ->
    record.residualRecorded = true ->
    record.permittedConsumerRecorded = true ->
    record.expiryRecorded = true ->
    record.downstreamUseRequested = true ->
    record.noAuthorityGrantRecorded = false ->
    OversightUseRouteFor record =
      OversightUseRoute.rejectAuthorityLaundering := by
  intro digest cohort envelopes views dependencies baseline lowRisk residual
    consumer expiry downstream authorityLaundering
  unfold OversightUseRouteFor
  simp [digest, cohort, envelopes, views, dependencies, baseline, lowRisk,
    residual, consumer, expiry, downstream, authorityLaundering]

end AsiStackProofs.ScalableOversight
