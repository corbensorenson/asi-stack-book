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

structure IntegrityIdentity where
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
deriving DecidableEq, Repr

def integrityIdentity (state : State) : IntegrityIdentity :=
  { recordDigest := state.recordDigest
    modelDigest := state.modelDigest
    checkpointDigest := state.checkpointDigest
    outerTargetDigest := state.outerTargetDigest
    signalLineageDigest := state.signalLineageDigest
    hypothesisSetDigest := state.hypothesisSetDigest
    evidencePlanDigest := state.evidencePlanDigest
    useEnvelopeDigest := state.useEnvelopeDigest
    reviewerDigest := state.reviewerDigest
    consumerDigest := state.consumerDigest
    residualDigest := state.residualDigest
    protocolVersion := state.protocolVersion
    hypothesisCount := state.hypothesisCount
    unresolvedHypothesisCount := state.unresolvedHypothesisCount }

def IntegrityNonAuthority (state : State) : Prop :=
  state.supportAssignmentCount = 0 ∧ state.externalAuthorityCount = 0

structure IntegrityInvariant (state : State) : Prop where
  pluralHypotheses : 2 <= state.hypothesisCount
  residualHypothesis : 0 < state.unresolvedHypothesisCount
  nonAuthority : IntegrityNonAuthority state

def IntegrityStep (state : State) (event : Event) : Option State :=
  if accepted (routeFor state event) then some (applyEvent state event).1
  else none

def IntegrityRun : State -> List Event -> Option State
  | state, [] => some state
  | state, event :: tail =>
      match IntegrityStep state event with
      | none => none
      | some next => IntegrityRun next tail

def IntegrityTraceAccepted : State -> List Event -> Prop
  | _, [] => True
  | state, event :: tail =>
      accepted (routeFor state event) = true ∧
        IntegrityTraceAccepted (applyEvent state event).1 tail

theorem integrity_accepted_step_is_accepted
    {state next : State} {event : Event}
    (stepped : IntegrityStep state event = some next) :
    accepted (routeFor state event) = true := by
  unfold IntegrityStep at stepped
  split at stepped
  · assumption
  · simp at stepped

theorem integrity_accepted_step_applies_event
    {state next : State} {event : Event}
    (stepped : IntegrityStep state event = some next) :
    next = (applyEvent state event).1 := by
  unfold IntegrityStep at stepped
  split at stepped
  · exact (Option.some.inj stepped).symm
  · simp at stepped

theorem apply_event_preserves_full_identity (state : State) (event : Event) :
    integrityIdentity (applyEvent state event).1 = integrityIdentity state := by
  by_cases acceptedEvent : accepted (routeFor state event) = true <;>
    simp [applyEvent, acceptedEvent, integrityIdentity]

theorem integrity_accepted_step_advances_stage
    {state next : State} {event : Event}
    (stepped : IntegrityStep state event = some next) :
    next.stage = advance state.stage := by
  rw [integrity_accepted_step_applies_event stepped]
  simp [applyEvent, integrity_accepted_step_is_accepted stepped]

theorem integrity_accepted_step_preserves_full_identity
    {state next : State} {event : Event}
    (stepped : IntegrityStep state event = some next) :
    integrityIdentity next = integrityIdentity state := by
  rw [integrity_accepted_step_applies_event stepped]
  exact apply_event_preserves_full_identity state event

theorem integrity_accepted_step_preserves_non_authority
    {state next : State} {event : Event}
    (bounded : IntegrityNonAuthority state)
    (stepped : IntegrityStep state event = some next) :
    IntegrityNonAuthority next := by
  rw [integrity_accepted_step_applies_event stepped]
  have preserved := apply_event_cannot_assign_support_or_external_authority
    state event
  exact ⟨preserved.1.trans bounded.1, preserved.2.trans bounded.2⟩

theorem integrity_accepted_step_adds_exact_receipt
    {state next : State} {event : Event}
    (stepped : IntegrityStep state event = some next) :
    next.receiptCount = state.receiptCount + 1 := by
  rw [integrity_accepted_step_applies_event stepped]
  exact accepted_event_adds_one_receipt state event
    (integrity_accepted_step_is_accepted stepped)

theorem apply_event_handoff_count_monotone (state : State) (event : Event) :
    state.handoffCount <= (applyEvent state event).1.handoffCount := by
  by_cases acceptedEvent : accepted (routeFor state event) = true <;>
    simp [applyEvent, acceptedEvent]

theorem apply_event_invalidation_count_monotone
    (state : State) (event : Event) :
    state.invalidationCount <= (applyEvent state event).1.invalidationCount := by
  by_cases acceptedEvent : accepted (routeFor state event) = true <;>
    simp [applyEvent, acceptedEvent]

theorem integrity_accepted_step_preserves_invariant
    {state next : State} {event : Event}
    (safe : IntegrityInvariant state)
    (stepped : IntegrityStep state event = some next) :
    IntegrityInvariant next := by
  have identity := integrity_accepted_step_preserves_full_identity stepped
  have hypothesisCountPreserved :
      next.hypothesisCount = state.hypothesisCount := by
    simpa [integrityIdentity] using
      congrArg IntegrityIdentity.hypothesisCount identity
  have unresolvedCountPreserved :
      next.unresolvedHypothesisCount = state.unresolvedHypothesisCount := by
    simpa [integrityIdentity] using
      congrArg IntegrityIdentity.unresolvedHypothesisCount identity
  exact {
    pluralHypotheses := by
      rw [hypothesisCountPreserved]
      exact safe.pluralHypotheses
    residualHypothesis := by
      rw [unresolvedCountPreserved]
      exact safe.residualHypothesis
    nonAuthority := integrity_accepted_step_preserves_non_authority
      safe.nonAuthority stepped }

theorem integrity_run_preserves_full_identity
    {state final : State} {events : List Event}
    (ran : IntegrityRun state events = some final) :
    integrityIdentity final = integrityIdentity state := by
  induction events generalizing state with
  | nil => simp [IntegrityRun] at ran; subst final; rfl
  | cons event tail ih =>
      cases stepped : IntegrityStep state event with
      | none => simp [IntegrityRun, stepped] at ran
      | some next =>
          have tailRan : IntegrityRun next tail = some final := by
            simpa [IntegrityRun, stepped] using ran
          exact (ih tailRan).trans
            (integrity_accepted_step_preserves_full_identity stepped)

theorem integrity_run_preserves_invariant
    {state final : State} {events : List Event}
    (safe : IntegrityInvariant state)
    (ran : IntegrityRun state events = some final) :
    IntegrityInvariant final := by
  induction events generalizing state with
  | nil => simp [IntegrityRun] at ran; subst final; exact safe
  | cons event tail ih =>
      cases stepped : IntegrityStep state event with
      | none => simp [IntegrityRun, stepped] at ran
      | some next =>
          have tailRan : IntegrityRun next tail = some final := by
            simpa [IntegrityRun, stepped] using ran
          exact ih (integrity_accepted_step_preserves_invariant safe stepped) tailRan

theorem integrity_run_accounts_exact_receipts
    {state final : State} {events : List Event}
    (ran : IntegrityRun state events = some final) :
    final.receiptCount = state.receiptCount + events.length := by
  induction events generalizing state with
  | nil => simp [IntegrityRun] at ran; subst final; simp
  | cons event tail ih =>
      cases stepped : IntegrityStep state event with
      | none => simp [IntegrityRun, stepped] at ran
      | some next =>
          have tailRan : IntegrityRun next tail = some final := by
            simpa [IntegrityRun, stepped] using ran
          calc
            final.receiptCount = next.receiptCount + tail.length := ih tailRan
            _ = (state.receiptCount + 1) + tail.length := by
              rw [integrity_accepted_step_adds_exact_receipt stepped]
            _ = state.receiptCount + (event :: tail).length := by
              simp only [List.length_cons]
              omega

theorem integrity_run_handoff_count_monotone
    {state final : State} {events : List Event}
    (ran : IntegrityRun state events = some final) :
    state.handoffCount <= final.handoffCount := by
  induction events generalizing state with
  | nil => simp [IntegrityRun] at ran; subst final; exact Nat.le_refl _
  | cons event tail ih =>
      cases stepped : IntegrityStep state event with
      | none => simp [IntegrityRun, stepped] at ran
      | some next =>
          have tailRan : IntegrityRun next tail = some final := by
            simpa [IntegrityRun, stepped] using ran
          have stepMonotone : state.handoffCount <= next.handoffCount := by
            rw [integrity_accepted_step_applies_event stepped]
            exact apply_event_handoff_count_monotone state event
          exact Nat.le_trans stepMonotone (ih tailRan)

theorem integrity_run_invalidation_count_monotone
    {state final : State} {events : List Event}
    (ran : IntegrityRun state events = some final) :
    state.invalidationCount <= final.invalidationCount := by
  induction events generalizing state with
  | nil => simp [IntegrityRun] at ran; subst final; exact Nat.le_refl _
  | cons event tail ih =>
      cases stepped : IntegrityStep state event with
      | none => simp [IntegrityRun, stepped] at ran
      | some next =>
          have tailRan : IntegrityRun next tail = some final := by
            simpa [IntegrityRun, stepped] using ran
          have stepMonotone : state.invalidationCount <= next.invalidationCount := by
            rw [integrity_accepted_step_applies_event stepped]
            exact apply_event_invalidation_count_monotone state event
          exact Nat.le_trans stepMonotone (ih tailRan)

theorem integrity_successful_run_has_accepted_trace
    {state final : State} {events : List Event}
    (ran : IntegrityRun state events = some final) :
    IntegrityTraceAccepted state events := by
  induction events generalizing state with
  | nil => trivial
  | cons event tail ih =>
      cases stepped : IntegrityStep state event with
      | none => simp [IntegrityRun, stepped] at ran
      | some next =>
          have tailRan : IntegrityRun next tail = some final := by
            simpa [IntegrityRun, stepped] using ran
          exact ⟨integrity_accepted_step_is_accepted stepped, by
            rw [← integrity_accepted_step_applies_event stepped]
            exact ih tailRan⟩

theorem integrity_run_composes_across_event_batches
    (state : State) (first second : List Event) :
    IntegrityRun state (first ++ second) =
      (IntegrityRun state first).bind fun intermediate =>
        IntegrityRun intermediate second := by
  induction first generalizing state with
  | nil => simp [IntegrityRun]
  | cons event tail ih =>
      simp only [List.cons_append, IntegrityRun]
      cases IntegrityStep state event <;> simp [ih]

theorem invalidated_integrity_state_accepts_no_event
    (state : State) (event : Event) (invalidated : state.stage = .invalidated) :
    IntegrityStep state event = none := by
  by_cases expected : event.kind = .invalidateForChange <;>
  by_cases bound : exactBinding state event.packet = true <;>
  by_cases fresh : event.packet.eventDigest = state.lastEventDigest <;>
  by_cases authority : authorityLeakRequested event.packet = true <;>
  by_cases certainty : certaintyOverclaim event.packet = true <;>
    simp [IntegrityStep, routeFor, invalidated, expectedKind, expected, bound,
      fresh, authority, certainty, accepted]

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

def canonicalIntegrityEvents : List Event :=
  [ eventFor .registerHypotheses 1
  , eventFor .bindEvidence 2
  , eventFor .reviewInterventions 3
  , eventFor .reviewMitigation 4
  , eventFor .bindUse 5
  , eventFor .handoffForReadiness 6
  , eventFor .invalidateForChange 7 ]

def canonicalInvalidatedState : State :=
  { canonicalState .scoped with
      stage := .invalidated
      lastEventDigest := 7
      receiptCount := 7
      handoffCount := 1
      invalidationCount := 1 }

theorem canonical_integrity_initial_state_is_invariant :
    IntegrityInvariant (canonicalState .scoped) := by
  exact {
    pluralHypotheses := by decide
    residualHypothesis := by decide
    nonAuthority := ⟨rfl, rfl⟩ }

theorem canonical_integrity_run_reaches_exact_invalidated_state :
    IntegrityRun (canonicalState .scoped) canonicalIntegrityEvents =
      some canonicalInvalidatedState := by
  native_decide

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
