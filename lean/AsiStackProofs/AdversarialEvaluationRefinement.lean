namespace AsiStackProofs.AdversarialEvaluationRefinement

inductive Stage where
  | draft | scoped | protocolBound | observed | independentlyProbed | adjudicated | decisionBound
deriving DecidableEq, Repr

inductive EventKind where
  | scope | bindProtocol | recordObservation | runIndependentProbe | adjudicate
  | requestDecisionReview | triggerReevaluation
deriving DecidableEq, Repr

inductive Route where
  | rejectWrongStage | rejectIdentitySubstitution | rejectReplay | rejectAuthorityLeak
  | requestConsumer | requestDecision | requestModelTask | requestElicitationContext
  | requestAuthorityContext | requestPermittedInference
  | requestSelectionContext | requestRewardProvenance | requestMonitorProvenance
  | requestHypothesisSet | requestOutcomeCriterion | requestProspectivePlan | requestBlinding
  | requestObservation | requestTranscript | requestCompleteDenominator
  | requestFailureCases | requestCostRecord
  | requestIndependentEvaluation | rejectEvaluatorDependency | requestCrossContextProbe
  | requestMatchedAccess | requestDependencyDisclosure | requestDiscrepancyRecord
  | requestAlternativeHypotheses
  | requestDiscrepancyDisposition | requestAlternativeDisposition | requestUncertainty
  | requestResidualOwner | rejectIntentLaundering | requestMitigationDescendant
  | requestQuarantineRecord | requestExpiry | rejectDecisionAuthorityLaundering
  | requestDecisionReviewRecord | requestDecisionConsumer
  | requestBoundedObservationStatus | rejectReleaseAuthorityLaundering
  | requestReevaluationTrigger | requestDescendantInvalidation
  | requestOrdinaryRouteBlock | rejectSuccessorVersion
  | acceptScope | acceptProtocol | acceptObservation | acceptIndependentProbe
  | acceptPromotionAdjudication | acceptQuarantineAdjudication | acceptObservationClosure
  | acceptDecisionReview | acceptReevaluation
deriving DecidableEq, Repr

structure Packet where
  consumerId : Nat
  decisionDigest : Nat
  modelDigest : Nat
  taskDigest : Nat
  protocolDigest : Nat
  policyDigest : Nat
  evaluatorDigest : Nat
  monitorDigest : Nat
  rewardDigest : Nat
  selectionDigest : Nat
  hypothesisDigest : Nat
  outcomeDigest : Nat
  currentProtocolVersion : Nat
  successorProtocolVersion : Nat
  eventDigest : Nat
  consumerPresent : Bool
  decisionPresent : Bool
  modelTaskPresent : Bool
  elicitationContextPresent : Bool
  authorityContextPresent : Bool
  permittedInferencePresent : Bool
  selectionContextPresent : Bool
  rewardProvenancePresent : Bool
  monitorProvenancePresent : Bool
  hypothesisSetPresent : Bool
  outcomeCriterionPresent : Bool
  prospectivePlanPresent : Bool
  blindingPresent : Bool
  observationPresent : Bool
  transcriptPresent : Bool
  denominatorComplete : Bool
  failureCasesPreserved : Bool
  costRecordPresent : Bool
  independentEvaluationPresent : Bool
  evaluatorSeparationPresent : Bool
  crossContextProbePresent : Bool
  matchedAccessPresent : Bool
  dependencyDisclosurePresent : Bool
  discrepancyRecorded : Bool
  alternativeHypothesesPreserved : Bool
  unresolvedDiscrepancy : Bool
  mitigationAttempted : Bool
  discrepancyDispositionPresent : Bool
  alternativeDispositionPresent : Bool
  uncertaintyPresent : Bool
  residualOwnerPresent : Bool
  noIntentInferenceRecorded : Bool
  mitigationDescendantPresent : Bool
  quarantineRecordPresent : Bool
  expiryPresent : Bool
  decisionAuthoritySeparated : Bool
  promotionRequested : Bool
  decisionReviewRecordPresent : Bool
  decisionConsumerPresent : Bool
  boundedObservationStatusPresent : Bool
  noReleaseAuthorityRecorded : Bool
  reevaluationTriggerPresent : Bool
  descendantInvalidationComplete : Bool
  ordinaryRouteBlocked : Bool
  supportAssignmentRequested : Bool
  externalEffectRequested : Bool
deriving DecidableEq, Repr

structure State where
  stage : Stage
  consumerId : Nat
  decisionDigest : Nat
  modelDigest : Nat
  taskDigest : Nat
  protocolDigest : Nat
  policyDigest : Nat
  evaluatorDigest : Nat
  monitorDigest : Nat
  rewardDigest : Nat
  selectionDigest : Nat
  hypothesisDigest : Nat
  outcomeDigest : Nat
  protocolVersion : Nat
  unresolvedDiscrepancy : Bool
  mitigationAttempted : Bool
  lastEventDigest : Nat
  receiptCount : Nat
  decisionReviewHandoffCount : Nat
  reevaluationCount : Nat
  supportAssignmentCount : Nat
  externalEffectCount : Nat
deriving DecidableEq, Repr

def expectedKind : Stage -> EventKind
  | .draft => .scope
  | .scoped => .bindProtocol
  | .protocolBound => .recordObservation
  | .observed => .runIndependentProbe
  | .independentlyProbed => .adjudicate
  | .adjudicated => .requestDecisionReview
  | .decisionBound => .triggerReevaluation

def identityMatches (state : State) (packet : Packet) : Bool :=
  state.consumerId = packet.consumerId && state.decisionDigest = packet.decisionDigest &&
  state.modelDigest = packet.modelDigest && state.taskDigest = packet.taskDigest &&
  state.protocolDigest = packet.protocolDigest && state.policyDigest = packet.policyDigest &&
  state.evaluatorDigest = packet.evaluatorDigest && state.monitorDigest = packet.monitorDigest &&
  state.rewardDigest = packet.rewardDigest && state.selectionDigest = packet.selectionDigest &&
  state.hypothesisDigest = packet.hypothesisDigest && state.outcomeDigest = packet.outcomeDigest &&
  state.protocolVersion = packet.currentProtocolVersion

def routeFor (state : State) (kind : EventKind) (packet : Packet) : Route :=
  if kind != expectedKind state.stage then .rejectWrongStage
  else if identityMatches state packet = false then .rejectIdentitySubstitution
  else if packet.eventDigest = state.lastEventDigest then .rejectReplay
  else if packet.supportAssignmentRequested || packet.externalEffectRequested then .rejectAuthorityLeak
  else match state.stage with
  | .draft =>
      if packet.consumerPresent = false then .requestConsumer
      else if packet.decisionPresent = false then .requestDecision
      else if packet.modelTaskPresent = false then .requestModelTask
      else if packet.elicitationContextPresent = false then .requestElicitationContext
      else if packet.authorityContextPresent = false then .requestAuthorityContext
      else if packet.permittedInferencePresent = false then .requestPermittedInference
      else .acceptScope
  | .scoped =>
      if packet.selectionContextPresent = false then .requestSelectionContext
      else if packet.rewardProvenancePresent = false then .requestRewardProvenance
      else if packet.monitorProvenancePresent = false then .requestMonitorProvenance
      else if packet.hypothesisSetPresent = false then .requestHypothesisSet
      else if packet.outcomeCriterionPresent = false then .requestOutcomeCriterion
      else if packet.prospectivePlanPresent = false then .requestProspectivePlan
      else if packet.blindingPresent = false then .requestBlinding
      else .acceptProtocol
  | .protocolBound =>
      if packet.observationPresent = false then .requestObservation
      else if packet.transcriptPresent = false then .requestTranscript
      else if packet.denominatorComplete = false then .requestCompleteDenominator
      else if packet.failureCasesPreserved = false then .requestFailureCases
      else if packet.costRecordPresent = false then .requestCostRecord
      else .acceptObservation
  | .observed =>
      if packet.independentEvaluationPresent = false then .requestIndependentEvaluation
      else if packet.evaluatorSeparationPresent = false then .rejectEvaluatorDependency
      else if packet.crossContextProbePresent = false then .requestCrossContextProbe
      else if packet.matchedAccessPresent = false then .requestMatchedAccess
      else if packet.dependencyDisclosurePresent = false then .requestDependencyDisclosure
      else if packet.discrepancyRecorded = false then .requestDiscrepancyRecord
      else if packet.alternativeHypothesesPreserved = false then .requestAlternativeHypotheses
      else .acceptIndependentProbe
  | .independentlyProbed =>
      if packet.discrepancyDispositionPresent = false then .requestDiscrepancyDisposition
      else if packet.alternativeDispositionPresent = false then .requestAlternativeDisposition
      else if packet.uncertaintyPresent = false then .requestUncertainty
      else if packet.residualOwnerPresent = false then .requestResidualOwner
      else if packet.noIntentInferenceRecorded = false then .rejectIntentLaundering
      else if state.mitigationAttempted && packet.mitigationDescendantPresent = false then
        .requestMitigationDescendant
      else if state.unresolvedDiscrepancy && packet.quarantineRecordPresent = false then
        .requestQuarantineRecord
      else if packet.expiryPresent = false then .requestExpiry
      else if packet.decisionAuthoritySeparated = false then .rejectDecisionAuthorityLaundering
      else if state.unresolvedDiscrepancy then .acceptQuarantineAdjudication
      else if packet.promotionRequested then .acceptPromotionAdjudication
      else .acceptObservationClosure
  | .adjudicated =>
      if packet.decisionReviewRecordPresent = false then .requestDecisionReviewRecord
      else if packet.decisionConsumerPresent = false then .requestDecisionConsumer
      else if packet.boundedObservationStatusPresent = false then .requestBoundedObservationStatus
      else if packet.noReleaseAuthorityRecorded = false then .rejectReleaseAuthorityLaundering
      else .acceptDecisionReview
  | .decisionBound =>
      if packet.reevaluationTriggerPresent = false then .requestReevaluationTrigger
      else if packet.descendantInvalidationComplete = false then .requestDescendantInvalidation
      else if packet.ordinaryRouteBlocked = false then .requestOrdinaryRouteBlock
      else if packet.successorProtocolVersion != state.protocolVersion + 1 then .rejectSuccessorVersion
      else .acceptReevaluation

def accepted : Route -> Bool
  | .acceptScope | .acceptProtocol | .acceptObservation | .acceptIndependentProbe
  | .acceptPromotionAdjudication | .acceptQuarantineAdjudication | .acceptObservationClosure
  | .acceptDecisionReview | .acceptReevaluation => true
  | _ => false

def nextStage : Stage -> Stage
  | .draft => .scoped
  | .scoped => .protocolBound
  | .protocolBound => .observed
  | .observed => .independentlyProbed
  | .independentlyProbed => .adjudicated
  | .adjudicated => .decisionBound
  | .decisionBound => .scoped

def applyEvent (state : State) (kind : EventKind) (packet : Packet) : State × Route :=
  let route := routeFor state kind packet
  if accepted route then
    ({ state with
       stage := nextStage state.stage
       protocolVersion := if route = .acceptReevaluation then packet.successorProtocolVersion else state.protocolVersion
       unresolvedDiscrepancy := if route = .acceptIndependentProbe then packet.unresolvedDiscrepancy else state.unresolvedDiscrepancy
       mitigationAttempted := if route = .acceptIndependentProbe then packet.mitigationAttempted else state.mitigationAttempted
       lastEventDigest := packet.eventDigest
       receiptCount := state.receiptCount + 1
       decisionReviewHandoffCount := state.decisionReviewHandoffCount +
         (if route = .acceptDecisionReview then 1 else 0)
       reevaluationCount := state.reevaluationCount + (if route = .acceptReevaluation then 1 else 0) }, route)
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
  { consumerId := 901, decisionDigest := 902, modelDigest := 903, taskDigest := 904,
    protocolDigest := 905, policyDigest := 906, evaluatorDigest := 907,
    monitorDigest := 908, rewardDigest := 909, selectionDigest := 910,
    hypothesisDigest := 911, outcomeDigest := 912, currentProtocolVersion := 1,
    successorProtocolVersion := 1, eventDigest := 1, consumerPresent := true,
    decisionPresent := true, modelTaskPresent := true, elicitationContextPresent := true,
    authorityContextPresent := true, permittedInferencePresent := true,
    selectionContextPresent := true, rewardProvenancePresent := true,
    monitorProvenancePresent := true, hypothesisSetPresent := true,
    outcomeCriterionPresent := true, prospectivePlanPresent := true, blindingPresent := true,
    observationPresent := true, transcriptPresent := true, denominatorComplete := true,
    failureCasesPreserved := true, costRecordPresent := true,
    independentEvaluationPresent := true, evaluatorSeparationPresent := true,
    crossContextProbePresent := true, matchedAccessPresent := true,
    dependencyDisclosurePresent := true, discrepancyRecorded := true,
    alternativeHypothesesPreserved := true, unresolvedDiscrepancy := false,
    mitigationAttempted := false, discrepancyDispositionPresent := true,
    alternativeDispositionPresent := true, uncertaintyPresent := true,
    residualOwnerPresent := true, noIntentInferenceRecorded := true,
    mitigationDescendantPresent := true, quarantineRecordPresent := true,
    expiryPresent := true, decisionAuthoritySeparated := true, promotionRequested := true,
    decisionReviewRecordPresent := true, decisionConsumerPresent := true,
    boundedObservationStatusPresent := true, noReleaseAuthorityRecorded := true,
    reevaluationTriggerPresent := true, descendantInvalidationComplete := true,
    ordinaryRouteBlocked := true, supportAssignmentRequested := false,
    externalEffectRequested := false }

def canonicalState (stage : Stage) : State :=
  { stage := stage, consumerId := 901, decisionDigest := 902, modelDigest := 903,
    taskDigest := 904, protocolDigest := 905, policyDigest := 906,
    evaluatorDigest := 907, monitorDigest := 908, rewardDigest := 909,
    selectionDigest := 910, hypothesisDigest := 911, outcomeDigest := 912,
    protocolVersion := 1, unresolvedDiscrepancy := false, mitigationAttempted := false,
    lastEventDigest := 0, receiptCount := 0, decisionReviewHandoffCount := 0,
    reevaluationCount := 0, supportAssignmentCount := 0, externalEffectCount := 0 }

theorem complete_integrity_lifecycle_reaches_promotion_review :
  routeFor (canonicalState .independentlyProbed) .adjudicate canonicalPacket =
    .acceptPromotionAdjudication := by rfl
theorem missing_selection_context_blocks_observation :
  routeFor (canonicalState .scoped) .bindProtocol
    { canonicalPacket with selectionContextPresent := false } = .requestSelectionContext := by rfl
theorem missing_reward_provenance_blocks_observation :
  routeFor (canonicalState .scoped) .bindProtocol
    { canonicalPacket with rewardProvenancePresent := false } = .requestRewardProvenance := by rfl
theorem missing_monitor_provenance_blocks_observation :
  routeFor (canonicalState .scoped) .bindProtocol
    { canonicalPacket with monitorProvenancePresent := false } = .requestMonitorProvenance := by rfl
theorem missing_independent_evaluation_blocks_probe :
  routeFor (canonicalState .observed) .runIndependentProbe
    { canonicalPacket with independentEvaluationPresent := false } = .requestIndependentEvaluation := by rfl
theorem missing_cross_context_probe_blocks_adjudication :
  routeFor (canonicalState .observed) .runIndependentProbe
    { canonicalPacket with crossContextProbePresent := false } = .requestCrossContextProbe := by rfl
theorem unresolved_discrepancy_requires_quarantine_record :
  routeFor { canonicalState .independentlyProbed with unresolvedDiscrepancy := true }
    .adjudicate { canonicalPacket with quarantineRecordPresent := false } =
    .requestQuarantineRecord := by rfl
theorem observation_cannot_launder_intent_inference :
  routeFor (canonicalState .independentlyProbed) .adjudicate
    { canonicalPacket with noIntentInferenceRecorded := false } = .rejectIntentLaundering := by rfl

def eventPacket (digest : Nat) : Packet := { canonicalPacket with eventDigest := digest }

theorem full_observation_lifecycle_requires_versioned_reevaluation :
  let s0 := canonicalState .draft
  let s1 := (applyEvent s0 .scope (eventPacket 1)).1
  let s2 := (applyEvent s1 .bindProtocol (eventPacket 2)).1
  let s3 := (applyEvent s2 .recordObservation (eventPacket 3)).1
  let s4 := (applyEvent s3 .runIndependentProbe (eventPacket 4)).1
  let s5 := (applyEvent s4 .adjudicate (eventPacket 5)).1
  let s6 := (applyEvent s5 .requestDecisionReview (eventPacket 6)).1
  let reeval := { eventPacket 7 with successorProtocolVersion := 2 }
  let s7 := (applyEvent s6 .triggerReevaluation reeval).1
  s7.stage = .scoped ∧ s7.protocolVersion = 2 ∧ s7.receiptCount = 7 ∧
    s7.decisionReviewHandoffCount = 1 ∧ s7.reevaluationCount = 1 ∧
    s7.supportAssignmentCount = 0 ∧ s7.externalEffectCount = 0 := by native_decide

end AsiStackProofs.AdversarialEvaluationRefinement
