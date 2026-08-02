namespace AsiStackProofs.EmbodiedPhysicalSafety

structure ControlLease where
  commandRequested : Bool
  plantIdentityBound : Bool
  leaseVersionCurrent : Bool
  currentTick : Nat
  leaseExpiresAt : Nat
  stateObservedAt : Nat
  maximumObservationAge : Nat
  worstCaseLatency : Nat
  controlPeriod : Nat
  deadlineSlack : Nat
  safeLower : Nat
  safeUpper : Nat
  estimateLower : Nat
  estimateUpper : Nat
  requestedMagnitude : Nat
  actuatorLimit : Nat
  stopDistanceUpperBound : Nat
  remainingDistanceMargin : Nat
  fallbackControllerReady : Bool
  independentStopArmed : Bool
  effectObservationReady : Bool
  residualCustodyPresent : Bool
  nonClaimBoundaryPresent : Bool
deriving DecidableEq, Repr

def LeaseCurrent (lease : ControlLease) : Prop :=
  lease.currentTick <= lease.leaseExpiresAt

instance leaseCurrentDecidable (lease : ControlLease) :
    Decidable (LeaseCurrent lease) := by
  unfold LeaseCurrent
  infer_instance

def ObservationFresh (lease : ControlLease) : Prop :=
  lease.stateObservedAt <= lease.currentTick ∧
    lease.currentTick <= lease.stateObservedAt + lease.maximumObservationAge

instance observationFreshDecidable (lease : ControlLease) :
    Decidable (ObservationFresh lease) := by
  unfold ObservationFresh
  infer_instance

def TimingWithinBudget (lease : ControlLease) : Prop :=
  lease.worstCaseLatency <= lease.controlPeriod ∧
    lease.worstCaseLatency <= lease.deadlineSlack

instance timingWithinBudgetDecidable (lease : ControlLease) :
    Decidable (TimingWithinBudget lease) := by
  unfold TimingWithinBudget
  infer_instance

def StateWithinEnvelope (lease : ControlLease) : Prop :=
  lease.safeLower <= lease.estimateLower ∧
    lease.estimateLower <= lease.estimateUpper ∧
      lease.estimateUpper <= lease.safeUpper

instance stateWithinEnvelopeDecidable (lease : ControlLease) :
    Decidable (StateWithinEnvelope lease) := by
  unfold StateWithinEnvelope
  infer_instance

def CommandWithinActuatorEnvelope (lease : ControlLease) : Prop :=
  lease.requestedMagnitude <= lease.actuatorLimit

instance commandWithinActuatorEnvelopeDecidable (lease : ControlLease) :
    Decidable (CommandWithinActuatorEnvelope lease) := by
  unfold CommandWithinActuatorEnvelope
  infer_instance

def FallbackReachable (lease : ControlLease) : Prop :=
  lease.fallbackControllerReady = true ∧
    lease.stopDistanceUpperBound <= lease.remainingDistanceMargin

instance fallbackReachableDecidable (lease : ControlLease) :
    Decidable (FallbackReachable lease) := by
  unfold FallbackReachable
  infer_instance

def ControlLeaseAdmissible (lease : ControlLease) : Prop :=
  lease.commandRequested = true ∧
    lease.plantIdentityBound = true ∧
      lease.leaseVersionCurrent = true ∧
        LeaseCurrent lease ∧
          ObservationFresh lease ∧
            StateWithinEnvelope lease ∧
              TimingWithinBudget lease ∧
                CommandWithinActuatorEnvelope lease ∧
                  FallbackReachable lease ∧
                    lease.independentStopArmed = true ∧
                      lease.effectObservationReady = true ∧
                        lease.residualCustodyPresent = true ∧
                          lease.nonClaimBoundaryPresent = true

instance controlLeaseAdmissibleDecidable (lease : ControlLease) :
    Decidable (ControlLeaseAdmissible lease) := by
  unfold ControlLeaseAdmissible
  infer_instance

def ControlLeaseReady (lease : ControlLease) : Bool :=
  decide (ControlLeaseAdmissible lease)

inductive ControlReviewRoute where
  | noCommandRequested
  | repairPlantIdentity
  | renewLeaseVersion
  | renewExpiredLease
  | refreshStateEstimate
  | restoreStateEnvelope
  | restoreTimingBudget
  | reduceCommandMagnitude
  | restoreFallbackReachability
  | armIndependentStop
  | restoreEffectObservation
  | assignResidualCustody
  | recordNonClaimBoundary
  | eligibleForTheseusClosedLoopTrial
deriving DecidableEq, Repr

def ControlReviewRouteFor (lease : ControlLease) : ControlReviewRoute :=
  if ! lease.commandRequested then .noCommandRequested
  else if ! lease.plantIdentityBound then .repairPlantIdentity
  else if ! lease.leaseVersionCurrent then .renewLeaseVersion
  else if ! decide (LeaseCurrent lease) then .renewExpiredLease
  else if ! decide (ObservationFresh lease) then .refreshStateEstimate
  else if ! decide (StateWithinEnvelope lease) then .restoreStateEnvelope
  else if ! decide (TimingWithinBudget lease) then .restoreTimingBudget
  else if ! decide (CommandWithinActuatorEnvelope lease) then .reduceCommandMagnitude
  else if ! decide (FallbackReachable lease) then .restoreFallbackReachability
  else if ! lease.independentStopArmed then .armIndependentStop
  else if ! lease.effectObservationReady then .restoreEffectObservation
  else if ! lease.residualCustodyPresent then .assignResidualCustody
  else if ! lease.nonClaimBoundaryPresent then .recordNonClaimBoundary
  else .eligibleForTheseusClosedLoopTrial

def completeControlLease : ControlLease where
  commandRequested := true
  plantIdentityBound := true
  leaseVersionCurrent := true
  currentTick := 5
  leaseExpiresAt := 8
  stateObservedAt := 4
  maximumObservationAge := 2
  worstCaseLatency := 2
  controlPeriod := 3
  deadlineSlack := 3
  safeLower := 2
  safeUpper := 10
  estimateLower := 4
  estimateUpper := 7
  requestedMagnitude := 4
  actuatorLimit := 6
  stopDistanceUpperBound := 3
  remainingDistanceMargin := 5
  fallbackControllerReady := true
  independentStopArmed := true
  effectObservationReady := true
  residualCustodyPresent := true
  nonClaimBoundaryPresent := true

inductive ControlAxis where
  | commandRequest
  | plantIdentity
  | leaseVersion
  | leaseCurrent
  | observationFreshness
  | stateEnvelope
  | timingBudget
  | actuatorEnvelope
  | fallbackReachability
  | independentStop
  | effectObservation
  | residualCustody
  | nonClaimBoundary
deriving DecidableEq, Repr

def omitControlAxis (axis : ControlAxis) : ControlLease :=
  match axis with
  | .commandRequest => { completeControlLease with commandRequested := false }
  | .plantIdentity => { completeControlLease with plantIdentityBound := false }
  | .leaseVersion => { completeControlLease with leaseVersionCurrent := false }
  | .leaseCurrent => { completeControlLease with leaseExpiresAt := 4 }
  | .observationFreshness =>
      { completeControlLease with stateObservedAt := 1, maximumObservationAge := 2 }
  | .stateEnvelope => { completeControlLease with estimateUpper := 11 }
  | .timingBudget => { completeControlLease with worstCaseLatency := 4 }
  | .actuatorEnvelope => { completeControlLease with requestedMagnitude := 7 }
  | .fallbackReachability =>
      { completeControlLease with stopDistanceUpperBound := 6 }
  | .independentStop => { completeControlLease with independentStopArmed := false }
  | .effectObservation => { completeControlLease with effectObservationReady := false }
  | .residualCustody => { completeControlLease with residualCustodyPresent := false }
  | .nonClaimBoundary => { completeControlLease with nonClaimBoundaryPresent := false }

def repairRouteForAxis : ControlAxis -> ControlReviewRoute
  | .commandRequest => .noCommandRequested
  | .plantIdentity => .repairPlantIdentity
  | .leaseVersion => .renewLeaseVersion
  | .leaseCurrent => .renewExpiredLease
  | .observationFreshness => .refreshStateEstimate
  | .stateEnvelope => .restoreStateEnvelope
  | .timingBudget => .restoreTimingBudget
  | .actuatorEnvelope => .reduceCommandMagnitude
  | .fallbackReachability => .restoreFallbackReachability
  | .independentStop => .armIndependentStop
  | .effectObservation => .restoreEffectObservation
  | .residualCustody => .assignResidualCustody
  | .nonClaimBoundary => .recordNonClaimBoundary

theorem complete_control_lease_is_ready :
    ControlLeaseReady completeControlLease = true := by decide

theorem complete_control_lease_routes_only_to_theseus_trial :
    ControlReviewRouteFor completeControlLease =
      .eligibleForTheseusClosedLoopTrial := by decide

theorem admissible_control_lease_is_ready
    (lease : ControlLease)
    (admissible : ControlLeaseAdmissible lease) :
    ControlLeaseReady lease = true := by
  exact decide_eq_true admissible

theorem every_control_axis_omission_blocks_readiness (axis : ControlAxis) :
    ControlLeaseReady (omitControlAxis axis) = false := by
  cases axis <;> decide

theorem every_control_axis_omission_reaches_exact_repair_route
    (axis : ControlAxis) :
    ControlReviewRouteFor (omitControlAxis axis) = repairRouteForAxis axis := by
  cases axis <;> decide

theorem every_control_axis_omission_blocks_trial_eligibility
    (axis : ControlAxis) :
    ControlReviewRouteFor (omitControlAxis axis) !=
      .eligibleForTheseusClosedLoopTrial := by
  cases axis <;> decide

theorem reduced_latency_preserves_timing_validity
    (lease : ControlLease) (reducedLatency : Nat)
    (reduced : reducedLatency <= lease.worstCaseLatency)
    (valid : TimingWithinBudget lease) :
    TimingWithinBudget { lease with worstCaseLatency := reducedLatency } := by
  unfold TimingWithinBudget at valid ⊢
  change reducedLatency <= lease.controlPeriod ∧
    reducedLatency <= lease.deadlineSlack
  omega

theorem lower_state_violation_persists_under_downward_widening
    (lease : ControlLease) (widerLower : Nat)
    (wider : widerLower <= lease.estimateLower)
    (violated : lease.estimateLower < lease.safeLower) :
    ¬ StateWithinEnvelope { lease with estimateLower := widerLower } := by
  intro claimed
  unfold StateWithinEnvelope at claimed
  change lease.safeLower <= widerLower ∧
    widerLower <= lease.estimateUpper ∧
      lease.estimateUpper <= lease.safeUpper at claimed
  omega

theorem fallback_distance_violation_persists_when_bound_grows
    (lease : ControlLease) (largerStopDistance : Nat)
    (larger : lease.stopDistanceUpperBound <= largerStopDistance)
    (violated : lease.remainingDistanceMargin < lease.stopDistanceUpperBound) :
    ¬ FallbackReachable
      { lease with stopDistanceUpperBound := largerStopDistance } := by
  intro claimed
  unfold FallbackReachable at claimed
  change lease.fallbackControllerReady = true ∧
    largerStopDistance <= lease.remainingDistanceMargin at claimed
  omega

theorem readiness_requires_command_request
    (lease : ControlLease) (ready : ControlLeaseReady lease = true) :
    lease.commandRequested = true := by
  have admissible : ControlLeaseAdmissible lease := of_decide_eq_true ready
  exact admissible.1

theorem readiness_requires_plant_identity
    (lease : ControlLease) (ready : ControlLeaseReady lease = true) :
    lease.plantIdentityBound = true := by
  have admissible : ControlLeaseAdmissible lease := of_decide_eq_true ready
  exact admissible.2.1

theorem readiness_requires_current_lease_version
    (lease : ControlLease) (ready : ControlLeaseReady lease = true) :
    lease.leaseVersionCurrent = true := by
  have admissible : ControlLeaseAdmissible lease := of_decide_eq_true ready
  exact admissible.2.2.1

theorem readiness_requires_unexpired_lease
    (lease : ControlLease) (ready : ControlLeaseReady lease = true) :
    LeaseCurrent lease := by
  have admissible : ControlLeaseAdmissible lease := of_decide_eq_true ready
  exact admissible.2.2.2.1

theorem readiness_requires_fresh_observation
    (lease : ControlLease) (ready : ControlLeaseReady lease = true) :
    ObservationFresh lease := by
  have admissible : ControlLeaseAdmissible lease := of_decide_eq_true ready
  exact admissible.2.2.2.2.1

theorem readiness_requires_state_envelope
    (lease : ControlLease) (ready : ControlLeaseReady lease = true) :
    StateWithinEnvelope lease := by
  have admissible : ControlLeaseAdmissible lease := of_decide_eq_true ready
  exact admissible.2.2.2.2.2.1

theorem readiness_requires_timing_budget
    (lease : ControlLease) (ready : ControlLeaseReady lease = true) :
    TimingWithinBudget lease := by
  have admissible : ControlLeaseAdmissible lease := of_decide_eq_true ready
  exact admissible.2.2.2.2.2.2.1

theorem readiness_requires_actuator_envelope
    (lease : ControlLease) (ready : ControlLeaseReady lease = true) :
    CommandWithinActuatorEnvelope lease := by
  have admissible : ControlLeaseAdmissible lease := of_decide_eq_true ready
  exact admissible.2.2.2.2.2.2.2.1

theorem readiness_requires_reachable_fallback
    (lease : ControlLease) (ready : ControlLeaseReady lease = true) :
    FallbackReachable lease := by
  have admissible : ControlLeaseAdmissible lease := of_decide_eq_true ready
  exact admissible.2.2.2.2.2.2.2.2.1

theorem readiness_requires_independent_stop
    (lease : ControlLease) (ready : ControlLeaseReady lease = true) :
    lease.independentStopArmed = true := by
  have admissible : ControlLeaseAdmissible lease := of_decide_eq_true ready
  exact admissible.2.2.2.2.2.2.2.2.2.1

theorem readiness_requires_effect_observation
    (lease : ControlLease) (ready : ControlLeaseReady lease = true) :
    lease.effectObservationReady = true := by
  have admissible : ControlLeaseAdmissible lease := of_decide_eq_true ready
  exact admissible.2.2.2.2.2.2.2.2.2.2.1

theorem readiness_requires_residual_custody
    (lease : ControlLease) (ready : ControlLeaseReady lease = true) :
    lease.residualCustodyPresent = true := by
  have admissible : ControlLeaseAdmissible lease := of_decide_eq_true ready
  exact admissible.2.2.2.2.2.2.2.2.2.2.2.1

theorem readiness_requires_non_claim_boundary
    (lease : ControlLease) (ready : ControlLeaseReady lease = true) :
    lease.nonClaimBoundaryPresent = true := by
  have admissible : ControlLeaseAdmissible lease := of_decide_eq_true ready
  exact admissible.2.2.2.2.2.2.2.2.2.2.2.2

inductive TrialStage where
  | proposed | leaseBound | independentlyReviewed | commandStaged
  | observationRecorded | stopRecorded | reconciled | closed
deriving DecidableEq, Repr

inductive TrialEventKind where
  | bindLease | reviewLease | stageCommand | recordObservation
  | recordStop | reconcile | close
deriving DecidableEq, Repr

inductive TrialRoute where
  | rejectWrongStage | rejectIdentitySubstitution | rejectEventReplay
  | rejectAuthorityLeak | requestLeaseRepair | requestIndependentReview
  | requestBoundedCommand | requestObservationReceipt | requestStopReceipt
  | requestResidualClosure | requestNonClaims
  | acceptLease | acceptReview | acceptCommandStage | acceptObservation
  | acceptStop | acceptReconciliation | acceptClosure
deriving DecidableEq, Repr

structure TrialState where
  stage : TrialStage
  plantDigest : Nat
  leaseDigest : Nat
  controllerDigest : Nat
  estimatorDigest : Nat
  policyDigest : Nat
  safetyEnvelopeDigest : Nat
  actuatorDigest : Nat
  observerDigest : Nat
  resultDigest : Nat
  lastEventDigest : Nat
  receiptCount : Nat := 0
  stopReceiptCount : Nat := 0
  supportAssigned : Bool := false
  externalEffectCommitted : Bool := false
deriving DecidableEq, Repr

structure TrialPacket where
  plantDigest : Nat := 7001
  leaseDigest : Nat := 7002
  controllerDigest : Nat := 7003
  estimatorDigest : Nat := 7004
  policyDigest : Nat := 7005
  safetyEnvelopeDigest : Nat := 7006
  actuatorDigest : Nat := 7007
  observerDigest : Nat := 7008
  resultDigest : Nat := 7009
  eventDigest : Nat := 1
  lease : ControlLease := completeControlLease
  independentReview : Bool := true
  boundedCommand : Bool := true
  observationReceipt : Bool := true
  stopReceipt : Bool := true
  residualClosure : Bool := true
  nonClaims : Bool := true
  supportRequested : Bool := false
  externalEffectRequested : Bool := false
deriving DecidableEq, Repr

structure TrialIdentity where
  plantDigest : Nat
  leaseDigest : Nat
  controllerDigest : Nat
  estimatorDigest : Nat
  policyDigest : Nat
  safetyEnvelopeDigest : Nat
  actuatorDigest : Nat
  observerDigest : Nat
  resultDigest : Nat
deriving DecidableEq, Repr

def trialIdentity (state : TrialState) : TrialIdentity :=
  { plantDigest := state.plantDigest
    leaseDigest := state.leaseDigest
    controllerDigest := state.controllerDigest
    estimatorDigest := state.estimatorDigest
    policyDigest := state.policyDigest
    safetyEnvelopeDigest := state.safetyEnvelopeDigest
    actuatorDigest := state.actuatorDigest
    observerDigest := state.observerDigest
    resultDigest := state.resultDigest }

def expectedTrialKind : TrialStage -> TrialEventKind
  | .proposed => .bindLease
  | .leaseBound => .reviewLease
  | .independentlyReviewed => .stageCommand
  | .commandStaged => .recordObservation
  | .observationRecorded => .recordStop
  | .stopRecorded => .reconcile
  | .reconciled => .close
  | .closed => .close

def trialAccepted : TrialRoute -> Bool
  | .acceptLease | .acceptReview | .acceptCommandStage | .acceptObservation
  | .acceptStop | .acceptReconciliation | .acceptClosure => true
  | _ => false

def trialRoute (state : TrialState) (kind : TrialEventKind)
    (packet : TrialPacket) : TrialRoute :=
  if kind != expectedTrialKind state.stage then .rejectWrongStage
  else if packet.plantDigest != state.plantDigest ||
      packet.leaseDigest != state.leaseDigest ||
      packet.controllerDigest != state.controllerDigest ||
      packet.estimatorDigest != state.estimatorDigest ||
      packet.policyDigest != state.policyDigest ||
      packet.safetyEnvelopeDigest != state.safetyEnvelopeDigest ||
      packet.actuatorDigest != state.actuatorDigest ||
      packet.observerDigest != state.observerDigest ||
      packet.resultDigest != state.resultDigest then .rejectIdentitySubstitution
  else if packet.eventDigest = state.lastEventDigest then .rejectEventReplay
  else if packet.supportRequested || packet.externalEffectRequested then .rejectAuthorityLeak
  else match state.stage with
  | .proposed =>
      if ControlLeaseReady packet.lease then .acceptLease else .requestLeaseRepair
  | .leaseBound =>
      if packet.independentReview then .acceptReview else .requestIndependentReview
  | .independentlyReviewed =>
      if packet.boundedCommand then .acceptCommandStage else .requestBoundedCommand
  | .commandStaged =>
      if packet.observationReceipt then .acceptObservation else .requestObservationReceipt
  | .observationRecorded =>
      if packet.stopReceipt then .acceptStop else .requestStopReceipt
  | .stopRecorded =>
      if packet.residualClosure then .acceptReconciliation else .requestResidualClosure
  | .reconciled =>
      if packet.nonClaims then .acceptClosure else .requestNonClaims
  | .closed => .rejectWrongStage

def advanceTrialStage : TrialStage -> TrialStage
  | .proposed => .leaseBound
  | .leaseBound => .independentlyReviewed
  | .independentlyReviewed => .commandStaged
  | .commandStaged => .observationRecorded
  | .observationRecorded => .stopRecorded
  | .stopRecorded => .reconciled
  | .reconciled => .closed
  | .closed => .closed

def applyTrialEvent (state : TrialState) (kind : TrialEventKind)
    (packet : TrialPacket) : TrialState × TrialRoute :=
  let selectedRoute := trialRoute state kind packet
  if trialAccepted selectedRoute then
    ({state with
      stage := advanceTrialStage state.stage
      lastEventDigest := packet.eventDigest
      receiptCount := state.receiptCount + 1
      stopReceiptCount := if selectedRoute == .acceptStop then
        state.stopReceiptCount + 1 else state.stopReceiptCount}, selectedRoute)
  else (state, selectedRoute)

structure TrialEvent where
  kind : TrialEventKind
  packet : TrialPacket
deriving DecidableEq, Repr

def TrialStep (state : TrialState) (event : TrialEvent) : Option TrialState :=
  if state.stage = .closed then none
  else if trialAccepted (trialRoute state event.kind event.packet) then
    some (applyTrialEvent state event.kind event.packet).1
  else none

def TrialRun : TrialState -> List TrialEvent -> Option TrialState
  | state, [] => some state
  | state, event :: tail =>
      match TrialStep state event with
      | none => none
      | some next => TrialRun next tail

def TrialTraceAccepted : TrialState -> List TrialEvent -> Prop
  | _, [] => True
  | state, event :: tail =>
      trialAccepted (trialRoute state event.kind event.packet) = true ∧
      TrialTraceAccepted (applyTrialEvent state event.kind event.packet).1 tail

theorem accepted_trial_step_is_accepted
    {state next : TrialState} {event : TrialEvent}
    (stepped : TrialStep state event = some next) :
    trialAccepted (trialRoute state event.kind event.packet) = true := by
  unfold TrialStep at stepped
  split at stepped
  · simp at stepped
  · split at stepped
    · assumption
    · simp at stepped

theorem accepted_trial_step_applies_event
    {state next : TrialState} {event : TrialEvent}
    (stepped : TrialStep state event = some next) :
    next = (applyTrialEvent state event.kind event.packet).1 := by
  unfold TrialStep at stepped
  split at stepped
  · simp at stepped
  · split at stepped
    · exact Option.some.inj stepped |>.symm
    · simp at stepped

theorem apply_trial_event_preserves_identity (state : TrialState)
    (event : TrialEvent) :
    trialIdentity (applyTrialEvent state event.kind event.packet).1 =
      trialIdentity state := by
  by_cases accepted : trialAccepted (trialRoute state event.kind event.packet) = true <;>
    simp [applyTrialEvent, accepted, trialIdentity]

theorem accepted_trial_step_preserves_identity
    {state next : TrialState} {event : TrialEvent}
    (stepped : TrialStep state event = some next) :
    trialIdentity next = trialIdentity state := by
  rw [accepted_trial_step_applies_event stepped]
  exact apply_trial_event_preserves_identity state event

theorem accepted_trial_step_preserves_non_authority
    {state next : TrialState} {event : TrialEvent}
    (stepped : TrialStep state event = some next) :
    next.supportAssigned = state.supportAssigned ∧
    next.externalEffectCommitted = state.externalEffectCommitted := by
  rw [accepted_trial_step_applies_event stepped]
  simp [applyTrialEvent, accepted_trial_step_is_accepted stepped]

theorem accepted_trial_step_adds_exactly_one_receipt
    {state next : TrialState} {event : TrialEvent}
    (stepped : TrialStep state event = some next) :
    next.receiptCount = state.receiptCount + 1 := by
  rw [accepted_trial_step_applies_event stepped]
  simp [applyTrialEvent, accepted_trial_step_is_accepted stepped]

theorem accepted_trial_step_advances_stage
    {state next : TrialState} {event : TrialEvent}
    (stepped : TrialStep state event = some next) :
    next.stage = advanceTrialStage state.stage := by
  rw [accepted_trial_step_applies_event stepped]
  simp [applyTrialEvent, accepted_trial_step_is_accepted stepped]

theorem apply_trial_event_stop_count_monotone (state : TrialState)
    (event : TrialEvent) :
    state.stopReceiptCount ≤
      (applyTrialEvent state event.kind event.packet).1.stopReceiptCount := by
  cases routed : trialRoute state event.kind event.packet <;>
    simp [applyTrialEvent, routed, trialAccepted]

theorem accepted_trial_step_stop_count_monotone
    {state next : TrialState} {event : TrialEvent}
    (stepped : TrialStep state event = some next) :
    state.stopReceiptCount ≤ next.stopReceiptCount := by
  rw [accepted_trial_step_applies_event stepped]
  exact apply_trial_event_stop_count_monotone state event

theorem accepted_trial_run_preserves_identity
    {state final : TrialState} {events : List TrialEvent}
    (ran : TrialRun state events = some final) :
    trialIdentity final = trialIdentity state := by
  induction events generalizing state with
  | nil => simp [TrialRun] at ran; subst final; rfl
  | cons event tail ih =>
      cases stepped : TrialStep state event with
      | none => simp [TrialRun, stepped] at ran
      | some next =>
          have tailRan : TrialRun next tail = some final := by
            simpa [TrialRun, stepped] using ran
          exact (ih tailRan).trans (accepted_trial_step_preserves_identity stepped)

theorem accepted_trial_run_preserves_support
    {state final : TrialState} {events : List TrialEvent}
    (ran : TrialRun state events = some final) :
    final.supportAssigned = state.supportAssigned := by
  induction events generalizing state with
  | nil => simp [TrialRun] at ran; subst final; rfl
  | cons event tail ih =>
      cases stepped : TrialStep state event with
      | none => simp [TrialRun, stepped] at ran
      | some next =>
          have tailRan : TrialRun next tail = some final := by
            simpa [TrialRun, stepped] using ran
          exact (ih tailRan).trans
            (accepted_trial_step_preserves_non_authority stepped).1

theorem accepted_trial_run_preserves_external_effect
    {state final : TrialState} {events : List TrialEvent}
    (ran : TrialRun state events = some final) :
    final.externalEffectCommitted = state.externalEffectCommitted := by
  induction events generalizing state with
  | nil => simp [TrialRun] at ran; subst final; rfl
  | cons event tail ih =>
      cases stepped : TrialStep state event with
      | none => simp [TrialRun, stepped] at ran
      | some next =>
          have tailRan : TrialRun next tail = some final := by
            simpa [TrialRun, stepped] using ran
          exact (ih tailRan).trans
            (accepted_trial_step_preserves_non_authority stepped).2

theorem accepted_trial_run_accounts_exact_receipts
    {state final : TrialState} {events : List TrialEvent}
    (ran : TrialRun state events = some final) :
    final.receiptCount = state.receiptCount + events.length := by
  induction events generalizing state with
  | nil => simp [TrialRun] at ran; subst final; simp
  | cons event tail ih =>
      cases stepped : TrialStep state event with
      | none => simp [TrialRun, stepped] at ran
      | some next =>
          have tailRan : TrialRun next tail = some final := by
            simpa [TrialRun, stepped] using ran
          calc
            final.receiptCount = next.receiptCount + tail.length := ih tailRan
            _ = (state.receiptCount + 1) + tail.length := by
              rw [accepted_trial_step_adds_exactly_one_receipt stepped]
            _ = state.receiptCount + (event :: tail).length := by
              simp only [List.length_cons]
              omega

theorem accepted_trial_run_stop_count_monotone
    {state final : TrialState} {events : List TrialEvent}
    (ran : TrialRun state events = some final) :
    state.stopReceiptCount ≤ final.stopReceiptCount := by
  induction events generalizing state with
  | nil => simp [TrialRun] at ran; subst final; exact Nat.le_refl _
  | cons event tail ih =>
      cases stepped : TrialStep state event with
      | none => simp [TrialRun, stepped] at ran
      | some next =>
          have tailRan : TrialRun next tail = some final := by
            simpa [TrialRun, stepped] using ran
          exact Nat.le_trans (accepted_trial_step_stop_count_monotone stepped)
            (ih tailRan)

theorem accepted_trial_run_has_accepted_trace
    {state final : TrialState} {events : List TrialEvent}
    (ran : TrialRun state events = some final) :
    TrialTraceAccepted state events := by
  induction events generalizing state with
  | nil => trivial
  | cons event tail ih =>
      cases stepped : TrialStep state event with
      | none => simp [TrialRun, stepped] at ran
      | some next =>
          have tailRan : TrialRun next tail = some final := by
            simpa [TrialRun, stepped] using ran
          exact ⟨accepted_trial_step_is_accepted stepped, by
            rw [← accepted_trial_step_applies_event stepped]
            exact ih tailRan⟩

theorem trial_run_append (state : TrialState) (first second : List TrialEvent) :
    TrialRun state (first ++ second) =
      (TrialRun state first).bind fun intermediate => TrialRun intermediate second := by
  induction first generalizing state with
  | nil => simp [TrialRun]
  | cons event tail ih =>
      simp only [List.cons_append, TrialRun]
      cases TrialStep state event <;> simp [ih]

theorem closed_trial_state_accepts_no_event
    (state : TrialState) (event : TrialEvent)
    (closed : state.stage = .closed) :
    TrialStep state event = none := by
  simp [TrialStep, closed]

def initialTrialState : TrialState :=
  { stage := .proposed
    plantDigest := 7001
    leaseDigest := 7002
    controllerDigest := 7003
    estimatorDigest := 7004
    policyDigest := 7005
    safetyEnvelopeDigest := 7006
    actuatorDigest := 7007
    observerDigest := 7008
    resultDigest := 7009
    lastEventDigest := 0 }

def trialEventAt (kind : TrialEventKind) (digest : Nat) : TrialEvent :=
  { kind := kind, packet := { eventDigest := digest } }

def completeTrialEvents : List TrialEvent :=
  [ trialEventAt .bindLease 1
  , trialEventAt .reviewLease 2
  , trialEventAt .stageCommand 3
  , trialEventAt .recordObservation 4
  , trialEventAt .recordStop 5
  , trialEventAt .reconcile 6
  , trialEventAt .close 7 ]

def completeTrialFinal : TrialState :=
  { initialTrialState with
    stage := .closed
    lastEventDigest := 7
    receiptCount := 7
    stopReceiptCount := 1 }

theorem complete_trial_reaches_closed_with_receipts_and_stop :
    TrialRun initialTrialState completeTrialEvents = some completeTrialFinal := by
  decide

def missingSafetyAxisEvent (axis : ControlAxis) : TrialEvent :=
  { kind := .bindLease
    packet := { lease := omitControlAxis axis, eventDigest := 1 } }

theorem missing_safety_axis_cannot_start_trial (axis : ControlAxis) :
    TrialStep initialTrialState (missingSafetyAxisEvent axis) = none := by
  cases axis <;> decide

end AsiStackProofs.EmbodiedPhysicalSafety
