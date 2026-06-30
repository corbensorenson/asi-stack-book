namespace AsiStackProofs.SimulationFidelity

structure SimulationClaimRecord where
  claimUsedAsEvidence : Bool
  scopeDeclared : Bool
  fidelityDeclared : Bool
  resourceBoundsDeclared : Bool
deriving DecidableEq, Repr

def SimulationClaimFieldsComplete (record : SimulationClaimRecord) : Prop :=
  record.scopeDeclared = true ∧
    record.fidelityDeclared = true ∧
      record.resourceBoundsDeclared = true

def SimulationClaimUseValid (record : SimulationClaimRecord) : Prop :=
  record.claimUsedAsEvidence = true -> SimulationClaimFieldsComplete record

theorem simulation_claim_used_as_evidence_includes_scope_fidelity_and_bounds
    {record : SimulationClaimRecord} :
    SimulationClaimUseValid record ->
    record.claimUsedAsEvidence = true ->
    record.scopeDeclared = true ∧
      record.fidelityDeclared = true ∧
        record.resourceBoundsDeclared = true := by
  intro valid used
  exact valid used

theorem evidence_use_without_scope_declaration_rejected
    {record : SimulationClaimRecord} :
    record.claimUsedAsEvidence = true ->
    record.scopeDeclared = false ->
    ¬ SimulationClaimUseValid record := by
  intro used missingScope valid
  have fields := valid used
  unfold SimulationClaimFieldsComplete at fields
  rw [missingScope] at fields
  cases fields.1

structure ExperimentResultRecord where
  promoted : Bool
  declaredFidelitySupportLevel : Nat
  claimedResultLevel : Nat
deriving DecidableEq, Repr

def ResultWithinDeclaredFidelity (record : ExperimentResultRecord) : Prop :=
  record.claimedResultLevel <= record.declaredFidelitySupportLevel

def ExperimentResultPromotionValid (record : ExperimentResultRecord) : Prop :=
  record.promoted = true -> ResultWithinDeclaredFidelity record

theorem promoted_experiment_result_cannot_exceed_declared_fidelity_support
    {record : ExperimentResultRecord} :
    ExperimentResultPromotionValid record ->
    record.promoted = true ->
    record.claimedResultLevel <= record.declaredFidelitySupportLevel := by
  intro valid promoted
  exact valid promoted

theorem promoted_result_above_declared_fidelity_rejected
    {record : ExperimentResultRecord} :
    record.promoted = true ->
    record.declaredFidelitySupportLevel < record.claimedResultLevel ->
    ¬ ExperimentResultPromotionValid record := by
  intro promoted exceeds valid
  have within := valid promoted
  exact Nat.not_lt_of_ge within exceeds

end AsiStackProofs.SimulationFidelity
