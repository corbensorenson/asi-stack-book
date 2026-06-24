namespace AsiStackProofs.SecurityKernel

inductive ClearanceLevel where
  | publicData
  | internalData
  | restricted
  | secret
deriving DecidableEq, Repr

def ClearanceLevel.rank : ClearanceLevel -> Nat
  | .publicData => 0
  | .internalData => 1
  | .restricted => 2
  | .secret => 3

structure ExecutionBoundary where
  authorized : Bool
  permitsSecretSubstitution : Bool
  clearance : ClearanceLevel
deriving DecidableEq, Repr

structure SecretHandle where
  requiredClearance : ClearanceLevel
deriving DecidableEq, Repr

def SecretSubstitutionAllowed (boundary : ExecutionBoundary) (handle : SecretHandle) : Prop :=
  boundary.authorized = true ∧
    boundary.permitsSecretSubstitution = true ∧
    handle.requiredClearance.rank <= boundary.clearance.rank

theorem secret_substitution_requires_authorized_boundary
    {boundary : ExecutionBoundary} {handle : SecretHandle} :
    SecretSubstitutionAllowed boundary handle ->
    boundary.authorized = true := by
  intro allowed
  exact allowed.1

structure ContextPacket where
  clearance : ClearanceLevel
deriving DecidableEq, Repr

structure DigitalScif where
  isProtected : Bool
  requiredClearance : ClearanceLevel
deriving DecidableEq, Repr

def ScifAdmissionAllowed (packet : ContextPacket) (scif : DigitalScif) : Prop :=
  scif.isProtected = false ∨ scif.requiredClearance.rank <= packet.clearance.rank

theorem insufficient_clearance_blocks_protected_scif_entry
    {packet : ContextPacket} {scif : DigitalScif} :
    scif.isProtected = true ->
    packet.clearance.rank < scif.requiredClearance.rank ->
    ¬ ScifAdmissionAllowed packet scif := by
  intro isProtected insufficient allowed
  cases allowed with
  | inl unprotected =>
      rw [isProtected] at unprotected
      contradiction
  | inr enoughClearance =>
      exact Nat.not_le_of_gt insufficient enoughClearance

end AsiStackProofs.SecurityKernel
