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

end AsiStackProofs.EmbodiedPhysicalSafety
