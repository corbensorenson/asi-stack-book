namespace AsiStackProofs.GovernedOperations

inductive DegradedRoute where
  | rejectIdentity | rejectAuthorityWidening | rejectLease
  | requestContainment | acceptDegraded
deriving DecidableEq, Repr

inductive RecoveryRoute where
  | rejectIdentity | requestStateInventory | requestExternalEffectDisposition
  | requestFreshAcceptance | requestIndependentVerifier | requestEmergencyExpiry
  | safeHold | acceptRecovery
deriving DecidableEq, Repr

structure AuthorityEnvelope where
  capability : Nat
  data : Nat
  tools : Nat
  population : Nat
  durationSeconds : Nat
deriving DecidableEq, Repr

structure OperationsPacket where
  deploymentDigest : Nat := 7101
  incidentDigest : Nat := 7102
  commandDigest : Nat := 7103
  candidateDigest : Nat := 7104
  expectedDeploymentDigest : Nat := 7101
  expectedIncidentDigest : Nat := 7102
  expectedCommandDigest : Nat := 7103
  expectedCandidateDigest : Nat := 7104
  currentAuthority : AuthorityEnvelope := { capability := 4, data := 4, tools := 4, population := 4, durationSeconds := 3600 }
  degradedAuthority : AuthorityEnvelope := { capability := 2, data := 2, tools := 1, population := 1, durationSeconds := 900 }
  incidentDeclared : Bool := true
  commandBound : Bool := true
  containmentIndependent : Bool := true
  emergencyLeasePresent : Bool := true
  emergencyLeaseExpired : Bool := true
  requiredStateCount : Nat := 11
  reconciledStateCount : Nat := 11
  descendantInventoryComplete : Bool := true
  externalEffectsEnumerated : Bool := true
  externalEffectsDispositionComplete : Bool := true
  irreversibleResidualAccepted : Bool := true
  acceptanceFresh : Bool := true
  independentVerifier : Bool := true
  fallbackQualified : Bool := true
  supportPromotionRequested : Bool := false
  releaseRequested : Bool := false
  externalEffectAuthorityRequested : Bool := false
deriving DecidableEq, Repr

def exactIdentity (p : OperationsPacket) : Bool :=
  p.deploymentDigest == p.expectedDeploymentDigest &&
  p.incidentDigest == p.expectedIncidentDigest &&
  p.commandDigest == p.expectedCommandDigest &&
  p.candidateDigest == p.expectedCandidateDigest

def authorityWithin (current proposed : AuthorityEnvelope) : Bool :=
  decide (proposed.capability ≤ current.capability) &&
  decide (proposed.data ≤ current.data) &&
  decide (proposed.tools ≤ current.tools) &&
  decide (proposed.population ≤ current.population) &&
  decide (proposed.durationSeconds ≤ current.durationSeconds)

def authorityLeakRequested (p : OperationsPacket) : Bool :=
  p.supportPromotionRequested || p.releaseRequested || p.externalEffectAuthorityRequested

def recoveryComplete (p : OperationsPacket) : Bool :=
  decide (p.reconciledStateCount = p.requiredStateCount) &&
  p.descendantInventoryComplete && p.externalEffectsEnumerated &&
  p.externalEffectsDispositionComplete && p.irreversibleResidualAccepted &&
  p.acceptanceFresh && p.independentVerifier && p.emergencyLeaseExpired &&
  p.fallbackQualified && ! authorityLeakRequested p

def degradationRoute (p : OperationsPacket) : DegradedRoute :=
  if ! exactIdentity p then .rejectIdentity
  else if ! authorityWithin p.currentAuthority p.degradedAuthority then .rejectAuthorityWidening
  else if ! p.emergencyLeasePresent || authorityLeakRequested p then .rejectLease
  else if ! p.incidentDeclared || ! p.commandBound || ! p.containmentIndependent then .requestContainment
  else .acceptDegraded

def incompleteRecoveryRoute (p : OperationsPacket) : RecoveryRoute :=
  if p.reconciledStateCount != p.requiredStateCount || ! p.descendantInventoryComplete then .requestStateInventory
  else if ! p.externalEffectsEnumerated then .requestExternalEffectDisposition
  else if ! p.externalEffectsDispositionComplete then .safeHold
  else if ! p.irreversibleResidualAccepted then .requestExternalEffectDisposition
  else if ! p.acceptanceFresh then .requestFreshAcceptance
  else if ! p.independentVerifier then .requestIndependentVerifier
  else if ! p.emergencyLeaseExpired then .requestEmergencyExpiry
  else .safeHold

def recoveryRoute (p : OperationsPacket) : RecoveryRoute :=
  if ! exactIdentity p then .rejectIdentity
  else if recoveryComplete p then .acceptRecovery
  else incompleteRecoveryRoute p

theorem incomplete_recovery_route_never_accepts (p : OperationsPacket) :
    incompleteRecoveryRoute p ≠ .acceptRecovery := by
  unfold incompleteRecoveryRoute
  repeat split <;> simp_all

theorem accepted_degradation_preserves_or_narrows_all_authority_dimensions
    (p : OperationsPacket)
    (h : degradationRoute p = .acceptDegraded) :
    authorityWithin p.currentAuthority p.degradedAuthority = true := by
  cases hIdentity : exactIdentity p <;>
    cases hWithin : authorityWithin p.currentAuthority p.degradedAuthority <;>
    simp_all [degradationRoute]

theorem widening_capability_rejects_degradation :
    degradationRoute { ({} : OperationsPacket) with degradedAuthority := { capability := 5, data := 2, tools := 1, population := 1, durationSeconds := 900 } } = .rejectAuthorityWidening := by native_decide

theorem widening_data_rejects_degradation :
    degradationRoute { ({} : OperationsPacket) with degradedAuthority := { capability := 2, data := 5, tools := 1, population := 1, durationSeconds := 900 } } = .rejectAuthorityWidening := by native_decide

theorem widening_tools_rejects_degradation :
    degradationRoute { ({} : OperationsPacket) with degradedAuthority := { capability := 2, data := 2, tools := 5, population := 1, durationSeconds := 900 } } = .rejectAuthorityWidening := by native_decide

theorem widening_population_rejects_degradation :
    degradationRoute { ({} : OperationsPacket) with degradedAuthority := { capability := 2, data := 2, tools := 1, population := 5, durationSeconds := 900 } } = .rejectAuthorityWidening := by native_decide

theorem widening_duration_rejects_degradation :
    degradationRoute { ({} : OperationsPacket) with degradedAuthority := { capability := 2, data := 2, tools := 1, population := 1, durationSeconds := 7200 } } = .rejectAuthorityWidening := by native_decide

theorem accepted_recovery_requires_complete_declared_state_effect_and_expiry
    (p : OperationsPacket)
    (h : recoveryRoute p = .acceptRecovery) :
    recoveryComplete p = true := by
  cases hIdentity : exactIdentity p
  · simp [recoveryRoute, hIdentity] at h
  · cases hComplete : recoveryComplete p
    · simp [recoveryRoute, hIdentity, hComplete] at h
      exact False.elim ((incomplete_recovery_route_never_accepts p) h)
    · rfl

theorem missing_state_class_blocks_recovery :
    recoveryRoute { ({} : OperationsPacket) with reconciledStateCount := 10 } = .requestStateInventory := by native_decide

theorem unknown_external_effect_routes_to_safe_hold :
    recoveryRoute { ({} : OperationsPacket) with externalEffectsDispositionComplete := false } = .safeHold := by native_decide

theorem stale_acceptance_blocks_recovery :
    recoveryRoute { ({} : OperationsPacket) with acceptanceFresh := false } = .requestFreshAcceptance := by native_decide

theorem active_emergency_lease_blocks_recovery :
    recoveryRoute { ({} : OperationsPacket) with emergencyLeaseExpired := false } = .requestEmergencyExpiry := by native_decide

theorem complete_declared_inventory_accepts_recovery_without_new_authority :
    degradationRoute ({} : OperationsPacket) = .acceptDegraded ∧
    recoveryRoute ({} : OperationsPacket) = .acceptRecovery ∧
    authorityLeakRequested ({} : OperationsPacket) = false := by native_decide

end AsiStackProofs.GovernedOperations
