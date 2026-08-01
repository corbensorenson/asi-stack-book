namespace AsiStackProofs.LearnedObjectiveIntegrity

inductive ObjectiveHypothesis where
  | intendedRule
  | shortcutRule
  | conditionalRule
deriving DecidableEq, Repr

inductive Action where
  | comply
  | refuse
  | exploit
deriving DecidableEq, Repr

structure PolicyWorld where
  objective : ObjectiveHypothesis
  observedTrace : List Action
  opportunityAction : Action
deriving DecidableEq, Repr

def intendedWorld : PolicyWorld :=
  { objective := .intendedRule
    observedTrace := [.comply, .comply, .comply]
    opportunityAction := .comply }

def shortcutWorld : PolicyWorld :=
  { objective := .shortcutRule
    observedTrace := [.comply, .comply, .comply]
    opportunityAction := .exploit }

theorem equal_trace_distinct_objectives_not_both_identified
    (left right : PolicyWorld)
    (infer : List Action -> ObjectiveHypothesis)
    (sameTrace : left.observedTrace = right.observedTrace)
    (differentObjectives : left.objective ≠ right.objective) :
    ¬ (infer left.observedTrace = left.objective ∧
       infer right.observedTrace = right.objective) := by
  intro identified
  have objectivesEqual : left.objective = right.objective := by
    calc
      left.objective = infer left.observedTrace := identified.1.symm
      _ = infer right.observedTrace := by rw [sameTrace]
      _ = right.objective := identified.2
  exact differentObjectives objectivesEqual

theorem compliant_trace_has_distinct_objective_witness :
    intendedWorld.observedTrace = shortcutWorld.observedTrace ∧
    intendedWorld.objective ≠ shortcutWorld.objective := by
  decide

theorem compliant_behavior_alone_cannot_identify_both_worlds
    (infer : List Action -> ObjectiveHypothesis) :
    ¬ (infer intendedWorld.observedTrace = intendedWorld.objective ∧
       infer shortcutWorld.observedTrace = shortcutWorld.objective) := by
  exact equal_trace_distinct_objectives_not_both_identified
    intendedWorld shortcutWorld infer rfl (by decide)

theorem separating_opportunity_distinguishes_the_witness :
    intendedWorld.opportunityAction ≠ shortcutWorld.opportunityAction := by
  decide

inductive Stage where
  | scoped
  | hypothesesBound
  | evidenceBound
  | interventionReviewed
  | mitigationReviewed
  | useBound
  | handedOff
  | invalidated
deriving DecidableEq, Repr

inductive EventKind where
  | registerHypotheses
  | bindEvidence
  | reviewInterventions
  | reviewMitigation
  | bindUse
  | handoffForReadiness
  | invalidateForChange
deriving DecidableEq, Repr

inductive Route where
  | rejectWrongStage
  | rejectIdentitySubstitution
  | rejectReplay
  | rejectAuthorityLeak
  | rejectObjectiveCertainty
  | requestOuterTarget
  | requestSignalLineage
  | requestPluralHypotheses
  | requestDistinctHypotheses
  | requestCompetenceControl
  | requestBehavioralEvidence
  | requestTrainingProcessEvidence
  | requestCausalEvidence
  | requestWhiteBoxEvidence
  | requestIndependentEvaluator
  | requestSealedIntervention
  | requestDistributionShift
  | requestRelevantOpportunity
  | requestConditionalPositiveControl
  | requestIndependentMonitor
  | requestMonitorDisagreement
  | requestSeparationOutcome
  | requestMitigationOutcome
  | requestConcealmentTest
  | requestCapabilityDamageTest
  | requestMitigationResidual
  | requestResidualHypothesis
  | requestBoundedAuthority
  | requestExpiry
  | requestRollback
  | requestDescendantCustody
  | requestResidualOwner
  | requestIndependentReview
  | requestMaximumInference
  | requestMaterialChange
  | requestDescendantInvalidation
  | requestOrdinaryRouteBlock
  | requestRereviewRoute
  | acceptHypotheses
  | acceptEvidence
  | acceptInterventionReview
  | acceptMitigationReview
  | acceptUseBinding
  | acceptHandoff
  | acceptInvalidation
deriving DecidableEq, Repr

structure Packet where
  recordDigest : Nat
  modelDigest : Nat
  checkpointDigest : Nat
  outerTargetDigest : Nat
  signalLineageDigest : Nat
  hypothesisSetDigest : Nat
  evidencePlanDigest : Nat
  useEnvelopeDigest : Nat
  reviewerDigest : Nat
  consumerDigest : Nat
  residualDigest : Nat
  protocolVersion : Nat
  eventDigest : Nat
  hypothesisCount : Nat
  unresolvedHypothesisCount : Nat
  outerTargetPresent : Bool
  signalLineagePresent : Bool
  distinctHypothesesRecorded : Bool
  competenceControlPassed : Bool
  behavioralEvidencePresent : Bool
  trainingProcessEvidencePresent : Bool
  causalEvidencePresent : Bool
  whiteBoxEvidencePresent : Bool
  independentEvaluator : Bool
  interventionSealed : Bool
  distributionShiftTested : Bool
  opportunityRelevant : Bool
  conditionalPositiveControlPassed : Bool
  monitorIndependent : Bool
  monitorDisagreementRecorded : Bool
  separationOutcomeRecorded : Bool
  mitigationOutcomeRecorded : Bool
  concealmentTested : Bool
  capabilityDamageTested : Bool
  mitigationResidualRecorded : Bool
  authorityBounded : Bool
  expiryPresent : Bool
  rollbackPresent : Bool
  descendantCustodyPresent : Bool
  residualOwnerPresent : Bool
  independentReview : Bool
  maximumInferencePresent : Bool
  materialChangeRecorded : Bool
  descendantsInvalidated : Bool
  ordinaryRouteBlocked : Bool
  rereviewRoutePresent : Bool
  objectiveIdentityAsserted : Bool
  absenceOfDeceptionAsserted : Bool
  supportAssignmentRequested : Bool
  externalAuthorityRequested : Bool
deriving DecidableEq, Repr

structure Event where
  kind : EventKind
  packet : Packet
deriving DecidableEq, Repr

structure State where
  stage : Stage
  recordDigest : Nat
  modelDigest : Nat
  checkpointDigest : Nat
  outerTargetDigest : Nat
  signalLineageDigest : Nat
  hypothesisSetDigest : Nat
  evidencePlanDigest : Nat
  useEnvelopeDigest : Nat
  reviewerDigest : Nat
  consumerDigest : Nat
  residualDigest : Nat
  protocolVersion : Nat
  hypothesisCount : Nat
  unresolvedHypothesisCount : Nat
  lastEventDigest : Nat
  receiptCount : Nat
  handoffCount : Nat
  invalidationCount : Nat
  supportAssignmentCount : Nat
  externalAuthorityCount : Nat
deriving DecidableEq, Repr

def expectedKind : Stage -> EventKind
  | .scoped => .registerHypotheses
  | .hypothesesBound => .bindEvidence
  | .evidenceBound => .reviewInterventions
  | .interventionReviewed => .reviewMitigation
  | .mitigationReviewed => .bindUse
  | .useBound => .handoffForReadiness
  | .handedOff => .invalidateForChange
  | .invalidated => .invalidateForChange

def exactBinding (state : State) (packet : Packet) : Bool :=
  packet.recordDigest == state.recordDigest &&
  packet.modelDigest == state.modelDigest &&
  packet.checkpointDigest == state.checkpointDigest &&
  packet.outerTargetDigest == state.outerTargetDigest &&
  packet.signalLineageDigest == state.signalLineageDigest &&
  packet.hypothesisSetDigest == state.hypothesisSetDigest &&
  packet.evidencePlanDigest == state.evidencePlanDigest &&
  packet.useEnvelopeDigest == state.useEnvelopeDigest &&
  packet.reviewerDigest == state.reviewerDigest &&
  packet.consumerDigest == state.consumerDigest &&
  packet.residualDigest == state.residualDigest &&
  packet.protocolVersion == state.protocolVersion &&
  packet.hypothesisCount == state.hypothesisCount &&
  packet.unresolvedHypothesisCount == state.unresolvedHypothesisCount

def authorityLeakRequested (packet : Packet) : Bool :=
  packet.supportAssignmentRequested || packet.externalAuthorityRequested

def certaintyOverclaim (packet : Packet) : Bool :=
  packet.objectiveIdentityAsserted || packet.absenceOfDeceptionAsserted

def routeFor (state : State) (event : Event) : Route :=
  if event.kind != expectedKind state.stage then .rejectWrongStage
  else if ! exactBinding state event.packet then .rejectIdentitySubstitution
  else if event.packet.eventDigest == state.lastEventDigest then .rejectReplay
  else if authorityLeakRequested event.packet then .rejectAuthorityLeak
  else if certaintyOverclaim event.packet then .rejectObjectiveCertainty
  else match state.stage with
  | .scoped =>
      if ! event.packet.outerTargetPresent then .requestOuterTarget
      else if ! event.packet.signalLineagePresent then .requestSignalLineage
      else if event.packet.hypothesisCount < 2 then .requestPluralHypotheses
      else if ! event.packet.distinctHypothesesRecorded then .requestDistinctHypotheses
      else .acceptHypotheses
  | .hypothesesBound =>
      if ! event.packet.competenceControlPassed then .requestCompetenceControl
      else if ! event.packet.behavioralEvidencePresent then .requestBehavioralEvidence
      else if ! event.packet.trainingProcessEvidencePresent then .requestTrainingProcessEvidence
      else if ! event.packet.causalEvidencePresent then .requestCausalEvidence
      else if ! event.packet.whiteBoxEvidencePresent then .requestWhiteBoxEvidence
      else if ! event.packet.independentEvaluator then .requestIndependentEvaluator
      else .acceptEvidence
  | .evidenceBound =>
      if ! event.packet.interventionSealed then .requestSealedIntervention
      else if ! event.packet.distributionShiftTested then .requestDistributionShift
      else if ! event.packet.opportunityRelevant then .requestRelevantOpportunity
      else if ! event.packet.conditionalPositiveControlPassed then
        .requestConditionalPositiveControl
      else if ! event.packet.monitorIndependent then .requestIndependentMonitor
      else if ! event.packet.monitorDisagreementRecorded then .requestMonitorDisagreement
      else if ! event.packet.separationOutcomeRecorded then .requestSeparationOutcome
      else .acceptInterventionReview
  | .interventionReviewed =>
      if ! event.packet.mitigationOutcomeRecorded then .requestMitigationOutcome
      else if ! event.packet.concealmentTested then .requestConcealmentTest
      else if ! event.packet.capabilityDamageTested then .requestCapabilityDamageTest
      else if ! event.packet.mitigationResidualRecorded then .requestMitigationResidual
      else .acceptMitigationReview
  | .mitigationReviewed =>
      if event.packet.unresolvedHypothesisCount = 0 then .requestResidualHypothesis
      else if ! event.packet.authorityBounded then .requestBoundedAuthority
      else if ! event.packet.expiryPresent then .requestExpiry
      else if ! event.packet.rollbackPresent then .requestRollback
      else if ! event.packet.descendantCustodyPresent then .requestDescendantCustody
      else if ! event.packet.residualOwnerPresent then .requestResidualOwner
      else .acceptUseBinding
  | .useBound =>
      if ! event.packet.independentReview then .requestIndependentReview
      else if ! event.packet.maximumInferencePresent then .requestMaximumInference
      else .acceptHandoff
  | .handedOff =>
      if ! event.packet.materialChangeRecorded then .requestMaterialChange
      else if ! event.packet.descendantsInvalidated then .requestDescendantInvalidation
      else if ! event.packet.ordinaryRouteBlocked then .requestOrdinaryRouteBlock
      else if ! event.packet.rereviewRoutePresent then .requestRereviewRoute
      else .acceptInvalidation
  | .invalidated => .rejectWrongStage

def accepted : Route -> Bool
  | .acceptHypotheses | .acceptEvidence | .acceptInterventionReview
  | .acceptMitigationReview | .acceptUseBinding | .acceptHandoff
  | .acceptInvalidation => true
  | _ => false

def advance : Stage -> Stage
  | .scoped => .hypothesesBound
  | .hypothesesBound => .evidenceBound
  | .evidenceBound => .interventionReviewed
  | .interventionReviewed => .mitigationReviewed
  | .mitigationReviewed => .useBound
  | .useBound => .handedOff
  | .handedOff => .invalidated
  | .invalidated => .invalidated

def applyEvent (state : State) (event : Event) : State × Route :=
  let route := routeFor state event
  if accepted route then
    ({ state with
       stage := advance state.stage
       lastEventDigest := event.packet.eventDigest
       receiptCount := state.receiptCount + 1
       handoffCount := state.handoffCount + (if route = .acceptHandoff then 1 else 0)
       invalidationCount := state.invalidationCount +
         (if route = .acceptInvalidation then 1 else 0) }, route)
  else (state, route)

theorem rejected_event_preserves_exact_state (state : State) (event : Event)
    (rejected : accepted (routeFor state event) = false) :
    (applyEvent state event).1 = state := by
  simp [applyEvent, rejected]

theorem apply_event_preserves_identity (state : State) (event : Event) :
    (applyEvent state event).1.recordDigest = state.recordDigest ∧
    (applyEvent state event).1.modelDigest = state.modelDigest ∧
    (applyEvent state event).1.checkpointDigest = state.checkpointDigest ∧
    (applyEvent state event).1.hypothesisSetDigest = state.hypothesisSetDigest ∧
    (applyEvent state event).1.protocolVersion = state.protocolVersion := by
  by_cases h : accepted (routeFor state event) = true <;> simp [applyEvent, h]

theorem apply_event_cannot_assign_support_or_external_authority
    (state : State) (event : Event) :
    (applyEvent state event).1.supportAssignmentCount = state.supportAssignmentCount ∧
    (applyEvent state event).1.externalAuthorityCount = state.externalAuthorityCount := by
  by_cases h : accepted (routeFor state event) = true <;> simp [applyEvent, h]

theorem accepted_event_adds_one_receipt (state : State) (event : Event)
    (acceptedEvent : accepted (routeFor state event) = true) :
    (applyEvent state event).1.receiptCount = state.receiptCount + 1 := by
  simp [applyEvent, acceptedEvent]

def canonicalPacket : Packet :=
  { recordDigest := 701, modelDigest := 702, checkpointDigest := 703,
    outerTargetDigest := 704, signalLineageDigest := 705,
    hypothesisSetDigest := 706, evidencePlanDigest := 707,
    useEnvelopeDigest := 708, reviewerDigest := 709, consumerDigest := 710,
    residualDigest := 711, protocolVersion := 1, eventDigest := 1,
    hypothesisCount := 2, unresolvedHypothesisCount := 1,
    outerTargetPresent := true, signalLineagePresent := true,
    distinctHypothesesRecorded := true, competenceControlPassed := true,
    behavioralEvidencePresent := true, trainingProcessEvidencePresent := true,
    causalEvidencePresent := true, whiteBoxEvidencePresent := true,
    independentEvaluator := true, interventionSealed := true,
    distributionShiftTested := true, opportunityRelevant := true,
    conditionalPositiveControlPassed := true, monitorIndependent := true,
    monitorDisagreementRecorded := true, separationOutcomeRecorded := true,
    mitigationOutcomeRecorded := true, concealmentTested := true,
    capabilityDamageTested := true, mitigationResidualRecorded := true,
    authorityBounded := true, expiryPresent := true, rollbackPresent := true,
    descendantCustodyPresent := true, residualOwnerPresent := true,
    independentReview := true, maximumInferencePresent := true,
    materialChangeRecorded := true, descendantsInvalidated := true,
    ordinaryRouteBlocked := true, rereviewRoutePresent := true,
    objectiveIdentityAsserted := false, absenceOfDeceptionAsserted := false,
    supportAssignmentRequested := false, externalAuthorityRequested := false }

def canonicalState (stage : Stage) : State :=
  { stage := stage, recordDigest := 701, modelDigest := 702,
    checkpointDigest := 703, outerTargetDigest := 704,
    signalLineageDigest := 705, hypothesisSetDigest := 706,
    evidencePlanDigest := 707, useEnvelopeDigest := 708,
    reviewerDigest := 709, consumerDigest := 710, residualDigest := 711,
    protocolVersion := 1, hypothesisCount := 2, unresolvedHypothesisCount := 1,
    lastEventDigest := 0, receiptCount := 0, handoffCount := 0,
    invalidationCount := 0, supportAssignmentCount := 0,
    externalAuthorityCount := 0 }

def eventFor (kind : EventKind) (digest : Nat) : Event :=
  { kind := kind, packet := { canonicalPacket with eventDigest := digest } }

theorem behavior_only_evidence_does_not_bind_integrity :
    routeFor (canonicalState .hypothesesBound)
      { kind := .bindEvidence,
        packet := { canonicalPacket with trainingProcessEvidencePresent := false } } =
      .requestTrainingProcessEvidence := by
  rfl

theorem objective_identity_overclaim_is_rejected :
    routeFor (canonicalState .useBound)
      { kind := .handoffForReadiness,
        packet := { canonicalPacket with objectiveIdentityAsserted := true } } =
      .rejectObjectiveCertainty := by
  rfl

theorem absence_of_deception_overclaim_is_rejected :
    routeFor (canonicalState .useBound)
      { kind := .handoffForReadiness,
        packet := { canonicalPacket with absenceOfDeceptionAsserted := true } } =
      .rejectObjectiveCertainty := by
  rfl

theorem unresolved_hypothesis_is_required_for_bounded_use :
    let state := { canonicalState .mitigationReviewed with
      unresolvedHypothesisCount := 0 }
    routeFor state
      { kind := .bindUse,
        packet := { canonicalPacket with unresolvedHypothesisCount := 0 } } =
      .requestResidualHypothesis := by
  rfl

theorem stale_descendants_block_invalidation :
    routeFor (canonicalState .handedOff)
      { kind := .invalidateForChange,
        packet := { canonicalPacket with descendantsInvalidated := false } } =
      .requestDescendantInvalidation := by
  rfl

theorem full_integrity_lifecycle_reaches_invalidated_state :
    let s0 := canonicalState .scoped
    let s1 := (applyEvent s0 (eventFor .registerHypotheses 1)).1
    let s2 := (applyEvent s1 (eventFor .bindEvidence 2)).1
    let s3 := (applyEvent s2 (eventFor .reviewInterventions 3)).1
    let s4 := (applyEvent s3 (eventFor .reviewMitigation 4)).1
    let s5 := (applyEvent s4 (eventFor .bindUse 5)).1
    let s6 := (applyEvent s5 (eventFor .handoffForReadiness 6)).1
    let s7 := (applyEvent s6 (eventFor .invalidateForChange 7)).1
    s7.stage = .invalidated ∧ s7.receiptCount = 7 ∧
      s7.handoffCount = 1 ∧ s7.invalidationCount = 1 ∧
      s7.supportAssignmentCount = 0 ∧ s7.externalAuthorityCount = 0 := by
  native_decide

end AsiStackProofs.LearnedObjectiveIntegrity
