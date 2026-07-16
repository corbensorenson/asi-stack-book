namespace AsiStackProofs.ScalableOversightRefinement

inductive Stage where
  | draft | scoped | protocolBound | reviewed | audited | adjudicated | useBound
deriving DecidableEq, Repr

inductive EventKind where
  | scopeProtocol | bindProtocol | recordReview | runOutcomeAudit
  | adjudicateUse | requestBoundedUse | triggerReadmission
deriving DecidableEq, Repr

inductive Route where
  | rejectWrongStage | rejectIdentitySubstitution | rejectReplay | rejectAuthorityLeak
  | requestTaskScope | requestConsumer | requestAuthorityScope | requestRiskTier
  | requestPermittedInference | requestEscalationOwner | acceptScope
  | requestSupervisorEnvelope | requestSystemEnvelope | requestCapabilityEnvelope
  | requestInformationAccess | requestRolesAndIncentives | requestTaskCohort
  | requestFailureRule | requestExpiry | acceptProtocol
  | requestEvidenceViews | requestDirectReviewBaseline | requestReviewOutcome
  | requestDisagreementRecord | requestCompleteDenominator | requestCoverageRecord
  | requestAbstentionReason | requestCostRecord | acceptReview
  | requestIndependentOutcomeAudit | rejectAuditorDependency
  | requestSharedDependencyDisclosure | requestCorrelationChallenge
  | requestOutcomeCriterion | requestAuditOutcome | requestFailureCases | acceptAudit
  | requestUncertainty | requestResidualOwner | requestDisagreementDisposition
  | requestAbstentionEvidence | requestAbstentionDefeater | requestEscalationRoute
  | rejectCompetenceInference | rejectPolicyAuthorityLaundering
  | acceptUseAdjudication | acceptAbstentionEscalation
  | requestPermittedConsumer | requestBoundedUseRecord | requestProtocolBinding
  | requestExpiryCheck | rejectReleaseAuthorityLaundering | acceptBoundedUse
  | requestMaterialChangeTrigger | requestDescendantInvalidation
  | requestOrdinaryRouteBlock | rejectSuccessorVersion | acceptReadmission
deriving DecidableEq, Repr

structure Packet where
  taskId : Nat
  consumerId : Nat
  protocolDigest : Nat
  cohortDigest : Nat
  systemDigest : Nat
  supervisorDigest : Nat
  evidenceViewDigest : Nat
  dependencyDigest : Nat
  baselineDigest : Nat
  auditorDigest : Nat
  policyDigest : Nat
  residualDigest : Nat
  authorityDigest : Nat
  currentProtocolVersion : Nat
  successorProtocolVersion : Nat
  eventDigest : Nat
  taskScopePresent : Bool
  consumerPresent : Bool
  authorityScopePresent : Bool
  riskTierPresent : Bool
  permittedInferencePresent : Bool
  escalationOwnerPresent : Bool
  supervisorEnvelopePresent : Bool
  systemEnvelopePresent : Bool
  capabilityEnvelopePresent : Bool
  informationAccessPresent : Bool
  rolesAndIncentivesPresent : Bool
  taskCohortPresent : Bool
  prospectiveFailureRulePresent : Bool
  expiryPresent : Bool
  evidenceViewsPresent : Bool
  directReviewBaselinePresent : Bool
  reviewOutcomePresent : Bool
  disagreementRecorded : Bool
  completeDenominator : Bool
  coverageRecorded : Bool
  abstentionReasonRecorded : Bool
  costRecordPresent : Bool
  independentOutcomeAuditPresent : Bool
  auditorSeparationPresent : Bool
  sharedDependenciesDisclosed : Bool
  correlationChallengePresent : Bool
  outcomeCriterionPresent : Bool
  auditOutcomePresent : Bool
  failureCasesPreserved : Bool
  uncertaintyPresent : Bool
  residualOwnerPresent : Bool
  disagreementDispositionPresent : Bool
  abstentionEvidencePresent : Bool
  abstentionDefeaterPresent : Bool
  escalationRoutePresent : Bool
  noCompetenceInferenceRecorded : Bool
  policyAuthoritySeparated : Bool
  permittedConsumerPresent : Bool
  boundedUseRecordPresent : Bool
  protocolDigestBound : Bool
  expiryChecked : Bool
  noReleaseAuthorityRecorded : Bool
  materialChangeTriggerPresent : Bool
  descendantInvalidationComplete : Bool
  ordinaryRouteBlocked : Bool
  highRiskUse : Bool
  abstentionRequested : Bool
  supportAssignmentRequested : Bool
  externalEffectRequested : Bool
deriving DecidableEq, Repr

structure State where
  stage : Stage
  taskId : Nat
  consumerId : Nat
  protocolDigest : Nat
  cohortDigest : Nat
  systemDigest : Nat
  supervisorDigest : Nat
  evidenceViewDigest : Nat
  dependencyDigest : Nat
  baselineDigest : Nat
  auditorDigest : Nat
  policyDigest : Nat
  residualDigest : Nat
  authorityDigest : Nat
  protocolVersion : Nat
  highRiskUse : Bool
  abstentionRequested : Bool
  lastEventDigest : Nat
  receiptCount : Nat
  boundedUseHandoffCount : Nat
  readmissionCount : Nat
  supportAssignmentCount : Nat
  externalEffectCount : Nat
deriving DecidableEq, Repr

def expectedKind : Stage -> EventKind
  | .draft => .scopeProtocol
  | .scoped => .bindProtocol
  | .protocolBound => .recordReview
  | .reviewed => .runOutcomeAudit
  | .audited => .adjudicateUse
  | .adjudicated => .requestBoundedUse
  | .useBound => .triggerReadmission

def identityMatches (state : State) (packet : Packet) : Bool :=
  state.taskId = packet.taskId && state.consumerId = packet.consumerId &&
  state.protocolDigest = packet.protocolDigest && state.cohortDigest = packet.cohortDigest &&
  state.systemDigest = packet.systemDigest && state.supervisorDigest = packet.supervisorDigest &&
  state.evidenceViewDigest = packet.evidenceViewDigest &&
  state.dependencyDigest = packet.dependencyDigest && state.baselineDigest = packet.baselineDigest &&
  state.auditorDigest = packet.auditorDigest && state.policyDigest = packet.policyDigest &&
  state.residualDigest = packet.residualDigest && state.authorityDigest = packet.authorityDigest &&
  state.protocolVersion = packet.currentProtocolVersion

def routeFor (state : State) (kind : EventKind) (packet : Packet) : Route :=
  if kind != expectedKind state.stage then .rejectWrongStage
  else if identityMatches state packet = false then .rejectIdentitySubstitution
  else if packet.eventDigest = state.lastEventDigest then .rejectReplay
  else if packet.supportAssignmentRequested || packet.externalEffectRequested then .rejectAuthorityLeak
  else match state.stage with
  | .draft =>
      if packet.taskScopePresent = false then .requestTaskScope
      else if packet.consumerPresent = false then .requestConsumer
      else if packet.authorityScopePresent = false then .requestAuthorityScope
      else if packet.riskTierPresent = false then .requestRiskTier
      else if packet.permittedInferencePresent = false then .requestPermittedInference
      else if packet.escalationOwnerPresent = false then .requestEscalationOwner
      else .acceptScope
  | .scoped =>
      if packet.supervisorEnvelopePresent = false then .requestSupervisorEnvelope
      else if packet.systemEnvelopePresent = false then .requestSystemEnvelope
      else if packet.capabilityEnvelopePresent = false then .requestCapabilityEnvelope
      else if packet.informationAccessPresent = false then .requestInformationAccess
      else if packet.rolesAndIncentivesPresent = false then .requestRolesAndIncentives
      else if packet.taskCohortPresent = false then .requestTaskCohort
      else if packet.prospectiveFailureRulePresent = false then .requestFailureRule
      else if packet.expiryPresent = false then .requestExpiry
      else .acceptProtocol
  | .protocolBound =>
      if packet.evidenceViewsPresent = false then .requestEvidenceViews
      else if packet.directReviewBaselinePresent = false then .requestDirectReviewBaseline
      else if packet.reviewOutcomePresent = false then .requestReviewOutcome
      else if packet.disagreementRecorded = false then .requestDisagreementRecord
      else if packet.completeDenominator = false then .requestCompleteDenominator
      else if packet.coverageRecorded = false then .requestCoverageRecord
      else if state.abstentionRequested && packet.abstentionReasonRecorded = false then
        .requestAbstentionReason
      else if packet.costRecordPresent = false then .requestCostRecord
      else .acceptReview
  | .reviewed =>
      if state.highRiskUse && packet.independentOutcomeAuditPresent = false then
        .requestIndependentOutcomeAudit
      else if packet.auditorSeparationPresent = false then .rejectAuditorDependency
      else if packet.sharedDependenciesDisclosed = false then .requestSharedDependencyDisclosure
      else if packet.correlationChallengePresent = false then .requestCorrelationChallenge
      else if packet.outcomeCriterionPresent = false then .requestOutcomeCriterion
      else if packet.auditOutcomePresent = false then .requestAuditOutcome
      else if packet.failureCasesPreserved = false then .requestFailureCases
      else .acceptAudit
  | .audited =>
      if packet.uncertaintyPresent = false then .requestUncertainty
      else if packet.residualOwnerPresent = false then .requestResidualOwner
      else if packet.disagreementDispositionPresent = false then .requestDisagreementDisposition
      else if state.abstentionRequested && packet.abstentionEvidencePresent = false then
        .requestAbstentionEvidence
      else if state.abstentionRequested && packet.abstentionDefeaterPresent = false then
        .requestAbstentionDefeater
      else if packet.escalationRoutePresent = false then .requestEscalationRoute
      else if packet.noCompetenceInferenceRecorded = false then .rejectCompetenceInference
      else if packet.policyAuthoritySeparated = false then .rejectPolicyAuthorityLaundering
      else if state.abstentionRequested then .acceptAbstentionEscalation
      else .acceptUseAdjudication
  | .adjudicated =>
      if packet.permittedConsumerPresent = false then .requestPermittedConsumer
      else if packet.boundedUseRecordPresent = false then .requestBoundedUseRecord
      else if packet.protocolDigestBound = false then .requestProtocolBinding
      else if packet.expiryChecked = false then .requestExpiryCheck
      else if packet.noReleaseAuthorityRecorded = false then .rejectReleaseAuthorityLaundering
      else .acceptBoundedUse
  | .useBound =>
      if packet.materialChangeTriggerPresent = false then .requestMaterialChangeTrigger
      else if packet.descendantInvalidationComplete = false then .requestDescendantInvalidation
      else if packet.ordinaryRouteBlocked = false then .requestOrdinaryRouteBlock
      else if packet.successorProtocolVersion != state.protocolVersion + 1 then
        .rejectSuccessorVersion
      else .acceptReadmission

def accepted : Route -> Bool
  | .acceptScope | .acceptProtocol | .acceptReview | .acceptAudit
  | .acceptUseAdjudication | .acceptAbstentionEscalation
  | .acceptBoundedUse | .acceptReadmission => true
  | _ => false

def nextStage : Stage -> Stage
  | .draft => .scoped
  | .scoped => .protocolBound
  | .protocolBound => .reviewed
  | .reviewed => .audited
  | .audited => .adjudicated
  | .adjudicated => .useBound
  | .useBound => .scoped

def applyEvent (state : State) (kind : EventKind) (packet : Packet) : State × Route :=
  let route := routeFor state kind packet
  if accepted route then
    ({ state with
       stage := nextStage state.stage
       protocolVersion := if route = .acceptReadmission then packet.successorProtocolVersion else state.protocolVersion
       lastEventDigest := packet.eventDigest
       receiptCount := state.receiptCount + 1
       boundedUseHandoffCount := state.boundedUseHandoffCount +
         (if route = .acceptBoundedUse then 1 else 0)
       readmissionCount := state.readmissionCount + (if route = .acceptReadmission then 1 else 0) }, route)
  else (state, route)

theorem rejected_event_preserves_state (state : State) (kind : EventKind) (packet : Packet)
    (h : accepted (routeFor state kind packet) = false) :
    (applyEvent state kind packet).1 = state := by simp [applyEvent, h]

theorem accepted_event_adds_one_receipt (state : State) (kind : EventKind) (packet : Packet)
    (h : accepted (routeFor state kind packet) = true) :
    (applyEvent state kind packet).1.receiptCount = state.receiptCount + 1 := by
  simp [applyEvent, h]

theorem event_cannot_assign_support_or_external_effect (state : State) (kind : EventKind)
    (packet : Packet) :
    (applyEvent state kind packet).1.supportAssignmentCount = state.supportAssignmentCount ∧
    (applyEvent state kind packet).1.externalEffectCount = state.externalEffectCount := by
  by_cases h : accepted (routeFor state kind packet) = true <;> simp [applyEvent, h]

def canonicalPacket : Packet :=
  { taskId := 801, consumerId := 802, protocolDigest := 803, cohortDigest := 804,
    systemDigest := 805, supervisorDigest := 806, evidenceViewDigest := 807,
    dependencyDigest := 808, baselineDigest := 809, auditorDigest := 810,
    policyDigest := 811, residualDigest := 812, authorityDigest := 813,
    currentProtocolVersion := 1, successorProtocolVersion := 1, eventDigest := 1,
    taskScopePresent := true, consumerPresent := true, authorityScopePresent := true,
    riskTierPresent := true, permittedInferencePresent := true, escalationOwnerPresent := true,
    supervisorEnvelopePresent := true, systemEnvelopePresent := true,
    capabilityEnvelopePresent := true, informationAccessPresent := true,
    rolesAndIncentivesPresent := true, taskCohortPresent := true,
    prospectiveFailureRulePresent := true, expiryPresent := true,
    evidenceViewsPresent := true, directReviewBaselinePresent := true,
    reviewOutcomePresent := true, disagreementRecorded := true,
    completeDenominator := true, coverageRecorded := true,
    abstentionReasonRecorded := true, costRecordPresent := true,
    independentOutcomeAuditPresent := true, auditorSeparationPresent := true,
    sharedDependenciesDisclosed := true, correlationChallengePresent := true,
    outcomeCriterionPresent := true, auditOutcomePresent := true,
    failureCasesPreserved := true, uncertaintyPresent := true,
    residualOwnerPresent := true, disagreementDispositionPresent := true,
    abstentionEvidencePresent := true, abstentionDefeaterPresent := true,
    escalationRoutePresent := true, noCompetenceInferenceRecorded := true,
    policyAuthoritySeparated := true, permittedConsumerPresent := true,
    boundedUseRecordPresent := true, protocolDigestBound := true, expiryChecked := true,
    noReleaseAuthorityRecorded := true, materialChangeTriggerPresent := true,
    descendantInvalidationComplete := true, ordinaryRouteBlocked := true,
    highRiskUse := true, abstentionRequested := false,
    supportAssignmentRequested := false, externalEffectRequested := false }

def canonicalState (stage : Stage) : State :=
  { stage := stage, taskId := 801, consumerId := 802, protocolDigest := 803,
    cohortDigest := 804, systemDigest := 805, supervisorDigest := 806,
    evidenceViewDigest := 807, dependencyDigest := 808, baselineDigest := 809,
    auditorDigest := 810, policyDigest := 811, residualDigest := 812,
    authorityDigest := 813, protocolVersion := 1, highRiskUse := true,
    abstentionRequested := false, lastEventDigest := 0, receiptCount := 0,
    boundedUseHandoffCount := 0, readmissionCount := 0,
    supportAssignmentCount := 0, externalEffectCount := 0 }

theorem missing_outcome_audit_blocks_high_risk_admission :
    routeFor (canonicalState .reviewed) .runOutcomeAudit
      { canonicalPacket with independentOutcomeAuditPresent := false } =
      .requestIndependentOutcomeAudit := by native_decide

theorem missing_baseline_requires_protocol_redesign :
    routeFor (canonicalState .protocolBound) .recordReview
      { canonicalPacket with directReviewBaselinePresent := false } =
      .requestDirectReviewBaseline := by native_decide

theorem complete_bounded_use_is_admitted :
    routeFor (canonicalState .adjudicated) .requestBoundedUse canonicalPacket =
      .acceptBoundedUse := by native_decide

theorem missing_evidence_views_requires_access_repair :
    routeFor (canonicalState .protocolBound) .recordReview
      { canonicalPacket with evidenceViewsPresent := false } = .requestEvidenceViews := by
  native_decide

theorem undisclosed_shared_dependencies_require_review :
    routeFor (canonicalState .reviewed) .runOutcomeAudit
      { canonicalPacket with sharedDependenciesDisclosed := false } =
      .requestSharedDependencyDisclosure := by native_decide

theorem high_risk_use_without_outcome_audit_requires_audit :
    routeFor (canonicalState .reviewed) .runOutcomeAudit
      { canonicalPacket with independentOutcomeAuditPresent := false } =
      .requestIndependentOutcomeAudit := by native_decide

theorem unjustified_abstention_requires_evidence :
    routeFor { canonicalState .audited with abstentionRequested := true } .adjudicateUse
      { canonicalPacket with abstentionEvidencePresent := false } =
      .requestAbstentionEvidence := by native_decide

theorem downstream_use_cannot_launder_authority :
    routeFor (canonicalState .adjudicated) .requestBoundedUse
      { canonicalPacket with noReleaseAuthorityRecorded := false } =
      .rejectReleaseAuthorityLaundering := by native_decide

theorem complete_lifecycle_reaches_version_two_readmission :
    let s0 := canonicalState .draft
    let s1 := (applyEvent s0 .scopeProtocol { canonicalPacket with eventDigest := 1 }).1
    let s2 := (applyEvent s1 .bindProtocol { canonicalPacket with eventDigest := 2 }).1
    let s3 := (applyEvent s2 .recordReview { canonicalPacket with eventDigest := 3 }).1
    let s4 := (applyEvent s3 .runOutcomeAudit { canonicalPacket with eventDigest := 4 }).1
    let s5 := (applyEvent s4 .adjudicateUse { canonicalPacket with eventDigest := 5 }).1
    let s6 := (applyEvent s5 .requestBoundedUse { canonicalPacket with eventDigest := 6 }).1
    let s7 := (applyEvent s6 .triggerReadmission
      { canonicalPacket with eventDigest := 7, successorProtocolVersion := 2 }).1
    s7.stage = .scoped ∧ s7.protocolVersion = 2 ∧ s7.receiptCount = 7 ∧
      s7.boundedUseHandoffCount = 1 ∧ s7.readmissionCount = 1 := by native_decide

end AsiStackProofs.ScalableOversightRefinement
