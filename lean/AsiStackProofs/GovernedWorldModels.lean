namespace AsiStackProofs.GovernedWorldModels

/-!
A finite custody and routing model for imagined world-model branches.  Every
field is a declared record predicate, not evidence that an observation is true,
a latent state is grounded, a calibration estimate is valid, or an action is
safe.  The model constrains admission and discrepancy handling only.
-/

inductive SupportClass where
  | qualified
  | unsupported
deriving DecidableEq, Repr

inductive RolloutRoute where
  | reject
  | reobserve
  | fallback
  | review
  | admitForPlanning
  | authorizeEffect
deriving DecidableEq, Repr

structure RolloutPacket where
  exactModelIdentity : Bool
  currentModelVersion : Bool
  observationFresh : Bool
  interventionSemanticsBound : Bool
  horizonBound : Bool
  calibrationRecorded : Bool
  supportClass : SupportClass
  materialDisagreement : Bool
  authorityCeilingPreserved : Bool
deriving DecidableEq, Repr

def RolloutRouteFor (packet : RolloutPacket) : RolloutRoute :=
  if packet.exactModelIdentity = false ∨
      packet.interventionSemanticsBound = false ∨
      packet.horizonBound = false ∨
      packet.authorityCeilingPreserved = false then
    .reject
  else if packet.currentModelVersion = false ∨ packet.observationFresh = false then
    .reobserve
  else if packet.supportClass = .unsupported ∨ packet.calibrationRecorded = false then
    .fallback
  else if packet.materialDisagreement = true then
    .review
  else
    .admitForPlanning

theorem rollout_never_authorizes_effect (packet : RolloutPacket) :
    RolloutRouteFor packet ≠ .authorizeEffect := by
  unfold RolloutRouteFor
  split <;> simp_all
  split <;> simp_all
  split <;> simp_all
  split <;> simp_all

theorem unsupported_rollout_no_authority
    (packet : RolloutPacket)
    (invalid :
      packet.currentModelVersion = false ∨
      packet.supportClass = .unsupported ∨
      packet.calibrationRecorded = false ∨
      packet.materialDisagreement = true) :
    RolloutRouteFor packet ≠ .admitForPlanning := by
  unfold RolloutRouteFor
  split <;> simp_all
  split <;> simp_all
  split <;> simp_all

theorem admitted_rollout_preserves_declared_boundary
    (packet : RolloutPacket)
    (admitted : RolloutRouteFor packet = .admitForPlanning) :
    packet.exactModelIdentity = true ∧
    packet.currentModelVersion = true ∧
    packet.observationFresh = true ∧
    packet.interventionSemanticsBound = true ∧
    packet.horizonBound = true ∧
    packet.calibrationRecorded = true ∧
    packet.supportClass = .qualified ∧
    packet.materialDisagreement = false ∧
    packet.authorityCeilingPreserved = true := by
  unfold RolloutRouteFor at admitted
  split at admitted <;> simp_all
  split at admitted <;> simp_all
  split at admitted <;> simp_all
  cases support : packet.supportClass <;> simp_all

inductive ResidualRoute where
  | continueModelBased
  | reestimate
  | fallback
  | review
  | safeHold
deriving DecidableEq, Repr

structure RealityResidual where
  material : Bool
  reestimationAvailable : Bool
  fallbackAvailable : Bool
  reviewAvailable : Bool
deriving DecidableEq, Repr

def ResidualRouteFor (residual : RealityResidual) : ResidualRoute :=
  if residual.material = false then
    .continueModelBased
  else if residual.reestimationAvailable = true then
    .reestimate
  else if residual.fallbackAvailable = true then
    .fallback
  else if residual.reviewAvailable = true then
    .review
  else
    .safeHold

theorem reality_residual_forces_route
    (residual : RealityResidual)
    (material : residual.material = true) :
    ResidualRouteFor residual ≠ .continueModelBased := by
  unfold ResidualRouteFor
  split <;> simp_all
  split <;> simp_all
  split <;> simp_all
  split <;> simp_all

theorem material_residual_selects_bounded_response
    (residual : RealityResidual)
    (material : residual.material = true) :
    ResidualRouteFor residual = .reestimate ∨
    ResidualRouteFor residual = .fallback ∨
    ResidualRouteFor residual = .review ∨
    ResidualRouteFor residual = .safeHold := by
  cases hm : residual.material <;>
    cases hre : residual.reestimationAvailable <;>
    cases hfa : residual.fallbackAvailable <;>
    cases hrv : residual.reviewAvailable <;>
    simp_all [ResidualRouteFor]

def qualifiedPacket : RolloutPacket where
  exactModelIdentity := true
  currentModelVersion := true
  observationFresh := true
  interventionSemanticsBound := true
  horizonBound := true
  calibrationRecorded := true
  supportClass := .qualified
  materialDisagreement := false
  authorityCeilingPreserved := true

def stalePacket : RolloutPacket :=
  { qualifiedPacket with currentModelVersion := false }

def unsupportedPacket : RolloutPacket :=
  { qualifiedPacket with supportClass := .unsupported }

def materialResidual : RealityResidual where
  material := true
  reestimationAvailable := false
  fallbackAvailable := false
  reviewAvailable := false

theorem qualified_fixture_admits_for_planning :
    RolloutRouteFor qualifiedPacket = .admitForPlanning := by native_decide

theorem stale_fixture_requires_reobservation :
    RolloutRouteFor stalePacket = .reobserve := by native_decide

theorem unsupported_fixture_falls_back :
    RolloutRouteFor unsupportedPacket = .fallback := by native_decide

theorem material_fixture_holds_safely :
    ResidualRouteFor materialResidual = .safeHold := by native_decide

end AsiStackProofs.GovernedWorldModels
