namespace AsiStackProofs.CognitiveCompilation

structure CompiledArtifactReview where
  requiredObligationsDeclared : Bool
  requiredObligationsPreserved : Bool
deriving DecidableEq, Repr

def RequiredIRObligationsPreserved
    (review : CompiledArtifactReview) : Prop :=
  review.requiredObligationsDeclared = true ->
    review.requiredObligationsPreserved = true

theorem compiled_artifact_preserves_all_required_ir_obligations
    {review : CompiledArtifactReview} :
    RequiredIRObligationsPreserved review ->
    review.requiredObligationsDeclared = true ->
    review.requiredObligationsPreserved = true := by
  intro valid declared
  exact valid declared

structure RepairAcceptanceReview where
  invalidatesExistingObligation : Bool
  ledgerUpdated : Bool
  repairAccepted : Bool
deriving DecidableEq, Repr

def InvalidatingRepairRequiresLedgerUpdate
    (review : RepairAcceptanceReview) : Prop :=
  review.invalidatesExistingObligation = true ->
    review.repairAccepted = true ->
      review.ledgerUpdated = true

theorem repair_invalidating_existing_obligation_requires_ledger_update
    {review : RepairAcceptanceReview} :
    InvalidatingRepairRequiresLedgerUpdate review ->
    review.invalidatesExistingObligation = true ->
    review.repairAccepted = true ->
    review.ledgerUpdated = true := by
  intro valid invalidates accepted
  exact valid invalidates accepted

end AsiStackProofs.CognitiveCompilation
