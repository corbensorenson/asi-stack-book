namespace AsiStackProofs.CapabilityThresholdRefinement

inductive Stage where
  | draft | scoped | assessed | adjudicated | controlled | readinessBound
deriving DecidableEq, Repr

inductive EventKind where
  | scope | assess | adjudicate | verifyControls | requestReadiness | triggerReassessment
deriving DecidableEq, Repr

inductive Route where
  | rejectWrongStage | rejectIdentitySubstitution | rejectReplay | rejectAuthorityLeak
  | requestCapabilityDomain | requestThreatModel | requestThresholdDefinition | requestCoverageDeadline
  | requestEvaluationEnvelope | requestElicitation | requestBaseline | requestUncertainty
  | requestIndependentEvaluator | requestAssessmentResult
  | requestThresholdDecision | requestDecisionUncertainty | requestAffectedPaths | requestResidualOwner
  | blockMissingSafeguards | blockMissingSafeguardVerifier | blockMissingBypassTest | blockMissingRollback
  | requestMonitoring | requestExceptionOwner | requestExceptionExpiry
  | requestCompensatingControls | requestExceptionReviewTrigger
  | requestDecisionAuthority | rejectAuthorityLaundering | requestReleasePath
  | requestReassessmentTrigger | requestDescendantInvalidation | requestOrdinaryRouteBlock
  | rejectSuccessorVersion
  | acceptScope | acceptAssessment | acceptAdjudication | acceptControls
  | acceptReadiness | acceptReassessment
deriving DecidableEq, Repr

structure Packet where
  capabilityId : Nat
  systemDigest : Nat
  policyDigest : Nat
  releasePathDigest : Nat
  envelopeDigest : Nat
  thresholdDigest : Nat
  baselineDigest : Nat
  evaluatorDigest : Nat
  safeguardDigest : Nat
  authorityDigest : Nat
  residualDigest : Nat
  currentAssessmentVersion : Nat
  successorAssessmentVersion : Nat
  eventDigest : Nat
  capabilityDomainPresent : Bool
  threatModelPresent : Bool
  thresholdDefinitionPresent : Bool
  coverageDeadlinePresent : Bool
  evaluationEnvelopePresent : Bool
  elicitationPresent : Bool
  baselinePresent : Bool
  uncertaintyPresent : Bool
  independentEvaluatorPresent : Bool
  assessmentResultPresent : Bool
  thresholdDecisionPresent : Bool
  decisionUncertaintyPresent : Bool
  thresholdCrossed : Bool
  affectedPathsPresent : Bool
  residualOwnerPresent : Bool
  safeguardPackagePresent : Bool
  safeguardVerifierPresent : Bool
  bypassTestPresent : Bool
  rollbackPlanPresent : Bool
  monitoringPresent : Bool
  exceptionRequested : Bool
  exceptionOwnerPresent : Bool
  exceptionExpiryPresent : Bool
  compensatingControlsPresent : Bool
  exceptionReviewTriggerPresent : Bool
  decisionAuthorityPresent : Bool
  authoritySeparationPresent : Bool
  releasePathPresent : Bool
  reassessmentTriggerPresent : Bool
  descendantInvalidationComplete : Bool
  ordinaryRouteBlocked : Bool
  supportAssignmentRequested : Bool
  externalEffectRequested : Bool
deriving DecidableEq, Repr

structure State where
  stage : Stage
  capabilityId : Nat
  systemDigest : Nat
  policyDigest : Nat
  releasePathDigest : Nat
  envelopeDigest : Nat
  thresholdDigest : Nat
  baselineDigest : Nat
  evaluatorDigest : Nat
  safeguardDigest : Nat
  authorityDigest : Nat
  residualDigest : Nat
  assessmentVersion : Nat
  thresholdCrossed : Bool
  lastEventDigest : Nat
  receiptCount : Nat
  readinessHandoffCount : Nat
  reassessmentCount : Nat
  supportAssignmentCount : Nat
  externalEffectCount : Nat
deriving DecidableEq, Repr

def expectedKind : Stage -> EventKind
  | .draft => .scope
  | .scoped => .assess
  | .assessed => .adjudicate
  | .adjudicated => .verifyControls
  | .controlled => .requestReadiness
  | .readinessBound => .triggerReassessment

def identityMatches (state : State) (packet : Packet) : Bool :=
  state.capabilityId = packet.capabilityId && state.systemDigest = packet.systemDigest &&
  state.policyDigest = packet.policyDigest && state.releasePathDigest = packet.releasePathDigest &&
  state.envelopeDigest = packet.envelopeDigest && state.thresholdDigest = packet.thresholdDigest &&
  state.baselineDigest = packet.baselineDigest && state.evaluatorDigest = packet.evaluatorDigest &&
  state.safeguardDigest = packet.safeguardDigest && state.authorityDigest = packet.authorityDigest &&
  state.residualDigest = packet.residualDigest &&
  state.assessmentVersion = packet.currentAssessmentVersion

def routeFor (state : State) (kind : EventKind) (packet : Packet) : Route :=
  if kind != expectedKind state.stage then .rejectWrongStage
  else if identityMatches state packet = false then .rejectIdentitySubstitution
  else if packet.eventDigest = state.lastEventDigest then .rejectReplay
  else if packet.supportAssignmentRequested || packet.externalEffectRequested then .rejectAuthorityLeak
  else match state.stage with
  | .draft =>
      if packet.capabilityDomainPresent = false then .requestCapabilityDomain
      else if packet.threatModelPresent = false then .requestThreatModel
      else if packet.thresholdDefinitionPresent = false then .requestThresholdDefinition
      else if packet.coverageDeadlinePresent = false then .requestCoverageDeadline
      else .acceptScope
  | .scoped =>
      if packet.evaluationEnvelopePresent = false then .requestEvaluationEnvelope
      else if packet.elicitationPresent = false then .requestElicitation
      else if packet.baselinePresent = false then .requestBaseline
      else if packet.uncertaintyPresent = false then .requestUncertainty
      else if packet.independentEvaluatorPresent = false then .requestIndependentEvaluator
      else if packet.assessmentResultPresent = false then .requestAssessmentResult
      else .acceptAssessment
  | .assessed =>
      if packet.thresholdDecisionPresent = false then .requestThresholdDecision
      else if packet.decisionUncertaintyPresent = false then .requestDecisionUncertainty
      else if packet.affectedPathsPresent = false then .requestAffectedPaths
      else if packet.residualOwnerPresent = false then .requestResidualOwner
      else .acceptAdjudication
  | .adjudicated =>
      if state.thresholdCrossed && packet.safeguardPackagePresent = false then .blockMissingSafeguards
      else if state.thresholdCrossed && packet.safeguardVerifierPresent = false then .blockMissingSafeguardVerifier
      else if state.thresholdCrossed && packet.bypassTestPresent = false then .blockMissingBypassTest
      else if state.thresholdCrossed && packet.rollbackPlanPresent = false then .blockMissingRollback
      else .acceptControls
  | .controlled =>
      if packet.monitoringPresent = false then .requestMonitoring
      else if packet.exceptionRequested && packet.exceptionOwnerPresent = false then .requestExceptionOwner
      else if packet.exceptionRequested && packet.exceptionExpiryPresent = false then .requestExceptionExpiry
      else if packet.exceptionRequested && packet.compensatingControlsPresent = false then .requestCompensatingControls
      else if packet.exceptionRequested && packet.exceptionReviewTriggerPresent = false then .requestExceptionReviewTrigger
      else if packet.residualOwnerPresent = false then .requestResidualOwner
      else if packet.decisionAuthorityPresent = false then .requestDecisionAuthority
      else if packet.authoritySeparationPresent = false then .rejectAuthorityLaundering
      else if packet.releasePathPresent = false then .requestReleasePath
      else .acceptReadiness
  | .readinessBound =>
      if packet.reassessmentTriggerPresent = false then .requestReassessmentTrigger
      else if packet.descendantInvalidationComplete = false then .requestDescendantInvalidation
      else if packet.ordinaryRouteBlocked = false then .requestOrdinaryRouteBlock
      else if packet.successorAssessmentVersion != state.assessmentVersion + 1 then .rejectSuccessorVersion
      else .acceptReassessment

def accepted : Route -> Bool
  | .acceptScope | .acceptAssessment | .acceptAdjudication | .acceptControls
  | .acceptReadiness | .acceptReassessment => true
  | _ => false

def nextStage : Stage -> Stage
  | .draft => .scoped
  | .scoped => .assessed
  | .assessed => .adjudicated
  | .adjudicated => .controlled
  | .controlled => .readinessBound
  | .readinessBound => .scoped

def applyEvent (state : State) (kind : EventKind) (packet : Packet) : State × Route :=
  let route := routeFor state kind packet
  if accepted route then
    ({ state with
       stage := nextStage state.stage
       assessmentVersion := if route = .acceptReassessment then packet.successorAssessmentVersion else state.assessmentVersion
       thresholdCrossed := if route = .acceptAdjudication then packet.thresholdCrossed else state.thresholdCrossed
       lastEventDigest := packet.eventDigest
       receiptCount := state.receiptCount + 1
       readinessHandoffCount := state.readinessHandoffCount + (if route = .acceptReadiness then 1 else 0)
       reassessmentCount := state.reassessmentCount + (if route = .acceptReassessment then 1 else 0) }, route)
  else (state, route)

theorem rejected_event_preserves_state (state : State) (kind : EventKind) (packet : Packet)
    (h : accepted (routeFor state kind packet) = false) :
    (applyEvent state kind packet).1 = state := by simp [applyEvent, h]

theorem accepted_event_adds_one_receipt (state : State) (kind : EventKind) (packet : Packet)
    (h : accepted (routeFor state kind packet) = true) :
    (applyEvent state kind packet).1.receiptCount = state.receiptCount + 1 := by simp [applyEvent, h]

theorem event_cannot_assign_support_or_external_effect (state : State) (kind : EventKind)
    (packet : Packet) :
    (applyEvent state kind packet).1.supportAssignmentCount = state.supportAssignmentCount ∧
    (applyEvent state kind packet).1.externalEffectCount = state.externalEffectCount := by
  by_cases h : accepted (routeFor state kind packet) = true <;> simp [applyEvent, h]

def canonicalPacket : Packet :=
  { capabilityId := 801, systemDigest := 802, policyDigest := 803, releasePathDigest := 804,
    envelopeDigest := 805, thresholdDigest := 806, baselineDigest := 807,
    evaluatorDigest := 808, safeguardDigest := 809, authorityDigest := 810,
    residualDigest := 811, currentAssessmentVersion := 1, successorAssessmentVersion := 1,
    eventDigest := 1, capabilityDomainPresent := true, threatModelPresent := true,
    thresholdDefinitionPresent := true, coverageDeadlinePresent := true,
    evaluationEnvelopePresent := true, elicitationPresent := true, baselinePresent := true,
    uncertaintyPresent := true, independentEvaluatorPresent := true,
    assessmentResultPresent := true, thresholdDecisionPresent := true,
    decisionUncertaintyPresent := true, thresholdCrossed := true, affectedPathsPresent := true,
    residualOwnerPresent := true, safeguardPackagePresent := true,
    safeguardVerifierPresent := true, bypassTestPresent := true, rollbackPlanPresent := true,
    monitoringPresent := true, exceptionRequested := false, exceptionOwnerPresent := true,
    exceptionExpiryPresent := true, compensatingControlsPresent := true,
    exceptionReviewTriggerPresent := true, decisionAuthorityPresent := true,
    authoritySeparationPresent := true, releasePathPresent := true,
    reassessmentTriggerPresent := true, descendantInvalidationComplete := true,
    ordinaryRouteBlocked := true, supportAssignmentRequested := false,
    externalEffectRequested := false }

def canonicalState (stage : Stage) : State :=
  { stage := stage, capabilityId := 801, systemDigest := 802, policyDigest := 803,
    releasePathDigest := 804, envelopeDigest := 805, thresholdDigest := 806,
    baselineDigest := 807, evaluatorDigest := 808, safeguardDigest := 809,
    authorityDigest := 810, residualDigest := 811, assessmentVersion := 1,
    thresholdCrossed := true, lastEventDigest := 0, receiptCount := 0,
    readinessHandoffCount := 0, reassessmentCount := 0,
    supportAssignmentCount := 0, externalEffectCount := 0 }

theorem missing_evaluation_envelope_blocks_assessment :
  routeFor (canonicalState .scoped) .assess
    { canonicalPacket with evaluationEnvelopePresent := false } = .requestEvaluationEnvelope := by rfl
theorem missing_uncertainty_blocks_assessment :
  routeFor (canonicalState .scoped) .assess
    { canonicalPacket with uncertaintyPresent := false } = .requestUncertainty := by rfl
theorem crossed_threshold_without_safeguards_blocks_controls :
  routeFor (canonicalState .adjudicated) .verifyControls
    { canonicalPacket with safeguardPackagePresent := false } = .blockMissingSafeguards := by rfl
theorem crossed_threshold_without_bypass_test_blocks_controls :
  routeFor (canonicalState .adjudicated) .verifyControls
    { canonicalPacket with bypassTestPresent := false } = .blockMissingBypassTest := by rfl
theorem exception_without_expiry_blocks_readiness :
  routeFor (canonicalState .controlled) .requestReadiness
    { canonicalPacket with exceptionRequested := true, exceptionExpiryPresent := false } =
    .requestExceptionExpiry := by rfl
theorem authority_laundering_blocks_readiness :
  routeFor (canonicalState .controlled) .requestReadiness
    { canonicalPacket with authoritySeparationPresent := false } = .rejectAuthorityLaundering := by rfl
theorem incomplete_descendant_invalidation_blocks_reassessment :
  routeFor (canonicalState .readinessBound) .triggerReassessment
    { canonicalPacket with successorAssessmentVersion := 2, descendantInvalidationComplete := false } =
    .requestDescendantInvalidation := by rfl
theorem stale_successor_version_blocks_reassessment :
  routeFor (canonicalState .readinessBound) .triggerReassessment canonicalPacket =
    .rejectSuccessorVersion := by rfl

def eventPacket (digest : Nat) : Packet := { canonicalPacket with eventDigest := digest }

theorem full_threshold_lifecycle_requires_versioned_reassessment :
  let s0 := canonicalState .draft
  let s1 := (applyEvent s0 .scope (eventPacket 1)).1
  let s2 := (applyEvent s1 .assess (eventPacket 2)).1
  let s3 := (applyEvent s2 .adjudicate (eventPacket 3)).1
  let s4 := (applyEvent s3 .verifyControls (eventPacket 4)).1
  let s5 := (applyEvent s4 .requestReadiness (eventPacket 5)).1
  let reassess := { eventPacket 6 with successorAssessmentVersion := 2 }
  let s6 := (applyEvent s5 .triggerReassessment reassess).1
  s6.stage = .scoped ∧ s6.assessmentVersion = 2 ∧ s6.receiptCount = 6 ∧
    s6.readinessHandoffCount = 1 ∧ s6.reassessmentCount = 1 ∧
    s6.supportAssignmentCount = 0 ∧ s6.externalEffectCount = 0 := by native_decide

end AsiStackProofs.CapabilityThresholdRefinement
