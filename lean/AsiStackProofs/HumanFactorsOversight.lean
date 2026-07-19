namespace AsiStackProofs.HumanFactorsOversight

/-!
A finite routing model for necessary operational conditions of an assigned
human-control role. Every field is an authored record predicate. The model does
not measure cognition, establish moral responsibility, validate consent, prove
intervention efficacy, or decide that control is meaningful.
-/

inductive ControlRoute where
  | boundedReview
  | addCapacity
  | reduceAutonomy
  | safeHold
  | rejectResponsibility
  | rejectAuthorityLeak
deriving DecidableEq, Repr

structure ControlEnvelope where
  controllerIdentified : Bool
  taskAuthorityPresent : Bool
  evidenceObservable : Bool
  representationCompatible : Bool
  comprehensionDispositionPresent : Bool
  workloadInsideBound : Bool
  decisionWindowPositive : Bool
  interventionChannelReachable : Bool
  systemResponseInsideWindow : Bool
  safeStateReachable : Bool
  conflictManaged : Bool
  responsibilityInsideEffectiveControl : Bool
  supportAssignmentRequested : Bool
  externalEffectRequested : Bool
deriving DecidableEq, Repr

def ControlRouteFor (packet : ControlEnvelope) : ControlRoute :=
  if packet.supportAssignmentRequested = true ∨
      packet.externalEffectRequested = true then
    .rejectAuthorityLeak
  else if packet.controllerIdentified = false ∨
      packet.taskAuthorityPresent = false then
    .safeHold
  else if packet.responsibilityInsideEffectiveControl = false then
    .rejectResponsibility
  else if packet.evidenceObservable = false ∨
      packet.representationCompatible = false ∨
      packet.comprehensionDispositionPresent = false ∨
      packet.workloadInsideBound = false ∨
      packet.conflictManaged = false then
    .addCapacity
  else if packet.decisionWindowPositive = false ∨
      packet.interventionChannelReachable = false ∨
      packet.systemResponseInsideWindow = false then
    .reduceAutonomy
  else if packet.safeStateReachable = false then
    .safeHold
  else
    .boundedReview

theorem control_route_never_grants_support_or_effect
    (packet : ControlEnvelope) :
    ControlRouteFor packet = .boundedReview ->
    packet.supportAssignmentRequested = false ∧
    packet.externalEffectRequested = false := by
  intro admitted
  unfold ControlRouteFor at admitted
  split at admitted <;> simp_all

theorem control_envelope_blocks_action
    (packet : ControlEnvelope)
    (missing :
      packet.taskAuthorityPresent = false ∨
      packet.evidenceObservable = false ∨
      packet.representationCompatible = false ∨
      packet.comprehensionDispositionPresent = false ∨
      packet.workloadInsideBound = false ∨
      packet.decisionWindowPositive = false ∨
      packet.interventionChannelReachable = false ∨
      packet.systemResponseInsideWindow = false ∨
      packet.safeStateReachable = false ∨
      packet.conflictManaged = false) :
    ControlRouteFor packet ≠ .boundedReview := by
  unfold ControlRouteFor
  split <;> simp_all
  split <;> simp_all
  split <;> simp_all
  split <;> simp_all
  split <;> simp_all

theorem responsibility_requires_control
    (packet : ControlEnvelope)
    (exceeds : packet.responsibilityInsideEffectiveControl = false) :
    ControlRouteFor packet ≠ .boundedReview := by
  unfold ControlRouteFor
  split <;> simp_all
  split <;> simp_all

theorem bounded_review_preserves_declared_conditions
    (packet : ControlEnvelope)
    (admitted : ControlRouteFor packet = .boundedReview) :
    packet.controllerIdentified = true ∧
    packet.taskAuthorityPresent = true ∧
    packet.evidenceObservable = true ∧
    packet.representationCompatible = true ∧
    packet.comprehensionDispositionPresent = true ∧
    packet.workloadInsideBound = true ∧
    packet.decisionWindowPositive = true ∧
    packet.interventionChannelReachable = true ∧
    packet.systemResponseInsideWindow = true ∧
    packet.safeStateReachable = true ∧
    packet.conflictManaged = true ∧
    packet.responsibilityInsideEffectiveControl = true ∧
    packet.supportAssignmentRequested = false ∧
    packet.externalEffectRequested = false := by
  unfold ControlRouteFor at admitted
  split at admitted <;> simp_all
  split at admitted <;> simp_all
  split at admitted <;> simp_all
  split at admitted <;> simp_all
  split at admitted <;> simp_all

def completeEnvelope : ControlEnvelope where
  controllerIdentified := true
  taskAuthorityPresent := true
  evidenceObservable := true
  representationCompatible := true
  comprehensionDispositionPresent := true
  workloadInsideBound := true
  decisionWindowPositive := true
  interventionChannelReachable := true
  systemResponseInsideWindow := true
  safeStateReachable := true
  conflictManaged := true
  responsibilityInsideEffectiveControl := true
  supportAssignmentRequested := false
  externalEffectRequested := false

def overloadedEnvelope : ControlEnvelope :=
  { completeEnvelope with workloadInsideBound := false }

def lateEnvelope : ControlEnvelope :=
  { completeEnvelope with systemResponseInsideWindow := false }

def blameWithoutControlEnvelope : ControlEnvelope :=
  { completeEnvelope with responsibilityInsideEffectiveControl := false }

def authorityLeakEnvelope : ControlEnvelope :=
  { completeEnvelope with supportAssignmentRequested := true }

theorem complete_fixture_routes_to_bounded_review :
    ControlRouteFor completeEnvelope = .boundedReview := by native_decide

theorem overloaded_fixture_requests_capacity :
    ControlRouteFor overloadedEnvelope = .addCapacity := by native_decide

theorem late_fixture_reduces_autonomy :
    ControlRouteFor lateEnvelope = .reduceAutonomy := by native_decide

theorem blame_without_control_is_rejected :
    ControlRouteFor blameWithoutControlEnvelope = .rejectResponsibility := by native_decide

theorem authority_leak_is_rejected :
    ControlRouteFor authorityLeakEnvelope = .rejectAuthorityLeak := by native_decide

end AsiStackProofs.HumanFactorsOversight
