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

inductive SemanticLoweringRoute where
  | rejectSourcePlan
  | requestSemanticIR
  | routeToRepair
  | blockLowering
  | requireValidator
  | requireLoweringReceipt
  | requireLedgerUpdate
  | recordResidual
  | acceptLowering
deriving DecidableEq, Repr

structure SemanticLoweringReview where
  sourcePlanAccepted : Bool
  atomsDeclared : Bool
  obligationsLinked : Bool
  dependenciesAcyclic : Bool
  authorityWithinContract : Bool
  assumptionsRecorded : Bool
  targetDeclared : Bool
  validatorsDeclared : Bool
  validatorsPassed : Bool
  loweringReceiptPresent : Bool
  obligationsPreserved : Bool
  repairInvalidatesObligation : Bool
  repairLedgerUpdated : Bool
  residualKnown : Bool
  acceptRequested : Bool
deriving DecidableEq, Repr

def SemanticLoweringRouteFor
    (review : SemanticLoweringReview) : SemanticLoweringRoute :=
  if review.sourcePlanAccepted = false then
    SemanticLoweringRoute.rejectSourcePlan
  else if review.atomsDeclared = false then
    SemanticLoweringRoute.requestSemanticIR
  else if review.obligationsLinked = false then
    SemanticLoweringRoute.requestSemanticIR
  else if review.dependenciesAcyclic = false then
    SemanticLoweringRoute.routeToRepair
  else if review.authorityWithinContract = false then
    SemanticLoweringRoute.blockLowering
  else if review.assumptionsRecorded = false then
    SemanticLoweringRoute.requestSemanticIR
  else if review.targetDeclared = false then
    SemanticLoweringRoute.requestSemanticIR
  else if review.validatorsDeclared = false then
    SemanticLoweringRoute.requireValidator
  else if review.validatorsPassed = false then
    SemanticLoweringRoute.routeToRepair
  else if review.loweringReceiptPresent = false then
    SemanticLoweringRoute.requireLoweringReceipt
  else if review.obligationsPreserved = false then
    SemanticLoweringRoute.blockLowering
  else if review.repairInvalidatesObligation = true ∧
      review.repairLedgerUpdated = false then
    SemanticLoweringRoute.requireLedgerUpdate
  else if review.residualKnown = true then
    SemanticLoweringRoute.recordResidual
  else if review.acceptRequested = true then
    SemanticLoweringRoute.acceptLowering
  else
    SemanticLoweringRoute.requestSemanticIR

theorem missing_source_plan_rejects_semantic_lowering
    {review : SemanticLoweringReview} :
    review.sourcePlanAccepted = false ->
    SemanticLoweringRouteFor review =
      SemanticLoweringRoute.rejectSourcePlan := by
  intro missingSourcePlan
  unfold SemanticLoweringRouteFor
  simp [missingSourcePlan]

theorem missing_atoms_request_semantic_ir
    {review : SemanticLoweringReview} :
    review.sourcePlanAccepted = true ->
    review.atomsDeclared = false ->
    SemanticLoweringRouteFor review =
      SemanticLoweringRoute.requestSemanticIR := by
  intro sourcePlanAccepted missingAtoms
  unfold SemanticLoweringRouteFor
  simp [sourcePlanAccepted, missingAtoms]

theorem missing_obligation_links_request_semantic_ir
    {review : SemanticLoweringReview} :
    review.sourcePlanAccepted = true ->
    review.atomsDeclared = true ->
    review.obligationsLinked = false ->
    SemanticLoweringRouteFor review =
      SemanticLoweringRoute.requestSemanticIR := by
  intro sourcePlanAccepted atomsDeclared missingObligationLinks
  unfold SemanticLoweringRouteFor
  simp [sourcePlanAccepted, atomsDeclared, missingObligationLinks]

theorem cyclic_dependencies_route_to_repair
    {review : SemanticLoweringReview} :
    review.sourcePlanAccepted = true ->
    review.atomsDeclared = true ->
    review.obligationsLinked = true ->
    review.dependenciesAcyclic = false ->
    SemanticLoweringRouteFor review =
      SemanticLoweringRoute.routeToRepair := by
  intro sourcePlanAccepted atomsDeclared obligationsLinked cyclicDependencies
  unfold SemanticLoweringRouteFor
  simp [sourcePlanAccepted, atomsDeclared, obligationsLinked,
    cyclicDependencies]

theorem authority_escape_blocks_semantic_lowering
    {review : SemanticLoweringReview} :
    review.sourcePlanAccepted = true ->
    review.atomsDeclared = true ->
    review.obligationsLinked = true ->
    review.dependenciesAcyclic = true ->
    review.authorityWithinContract = false ->
    SemanticLoweringRouteFor review =
      SemanticLoweringRoute.blockLowering := by
  intro sourcePlanAccepted atomsDeclared obligationsLinked dependenciesAcyclic
    authorityEscape
  unfold SemanticLoweringRouteFor
  simp [sourcePlanAccepted, atomsDeclared, obligationsLinked,
    dependenciesAcyclic, authorityEscape]

theorem missing_validators_require_validator
    {review : SemanticLoweringReview} :
    review.sourcePlanAccepted = true ->
    review.atomsDeclared = true ->
    review.obligationsLinked = true ->
    review.dependenciesAcyclic = true ->
    review.authorityWithinContract = true ->
    review.assumptionsRecorded = true ->
    review.targetDeclared = true ->
    review.validatorsDeclared = false ->
    SemanticLoweringRouteFor review =
      SemanticLoweringRoute.requireValidator := by
  intro sourcePlanAccepted atomsDeclared obligationsLinked dependenciesAcyclic
    authorityWithin assumptionsRecorded targetDeclared missingValidators
  unfold SemanticLoweringRouteFor
  simp [sourcePlanAccepted, atomsDeclared, obligationsLinked,
    dependenciesAcyclic, authorityWithin, assumptionsRecorded, targetDeclared,
    missingValidators]

theorem validator_failure_routes_to_repair
    {review : SemanticLoweringReview} :
    review.sourcePlanAccepted = true ->
    review.atomsDeclared = true ->
    review.obligationsLinked = true ->
    review.dependenciesAcyclic = true ->
    review.authorityWithinContract = true ->
    review.assumptionsRecorded = true ->
    review.targetDeclared = true ->
    review.validatorsDeclared = true ->
    review.validatorsPassed = false ->
    SemanticLoweringRouteFor review =
      SemanticLoweringRoute.routeToRepair := by
  intro sourcePlanAccepted atomsDeclared obligationsLinked dependenciesAcyclic
    authorityWithin assumptionsRecorded targetDeclared validatorsDeclared
    validatorFailure
  unfold SemanticLoweringRouteFor
  simp [sourcePlanAccepted, atomsDeclared, obligationsLinked,
    dependenciesAcyclic, authorityWithin, assumptionsRecorded, targetDeclared,
    validatorsDeclared, validatorFailure]

theorem missing_lowering_receipt_requires_receipt
    {review : SemanticLoweringReview} :
    review.sourcePlanAccepted = true ->
    review.atomsDeclared = true ->
    review.obligationsLinked = true ->
    review.dependenciesAcyclic = true ->
    review.authorityWithinContract = true ->
    review.assumptionsRecorded = true ->
    review.targetDeclared = true ->
    review.validatorsDeclared = true ->
    review.validatorsPassed = true ->
    review.loweringReceiptPresent = false ->
    SemanticLoweringRouteFor review =
      SemanticLoweringRoute.requireLoweringReceipt := by
  intro sourcePlanAccepted atomsDeclared obligationsLinked dependenciesAcyclic
    authorityWithin assumptionsRecorded targetDeclared validatorsDeclared
    validatorsPassed missingReceipt
  unfold SemanticLoweringRouteFor
  simp [sourcePlanAccepted, atomsDeclared, obligationsLinked,
    dependenciesAcyclic, authorityWithin, assumptionsRecorded, targetDeclared,
    validatorsDeclared, validatorsPassed, missingReceipt]

theorem obligation_loss_blocks_semantic_lowering
    {review : SemanticLoweringReview} :
    review.sourcePlanAccepted = true ->
    review.atomsDeclared = true ->
    review.obligationsLinked = true ->
    review.dependenciesAcyclic = true ->
    review.authorityWithinContract = true ->
    review.assumptionsRecorded = true ->
    review.targetDeclared = true ->
    review.validatorsDeclared = true ->
    review.validatorsPassed = true ->
    review.loweringReceiptPresent = true ->
    review.obligationsPreserved = false ->
    SemanticLoweringRouteFor review =
      SemanticLoweringRoute.blockLowering := by
  intro sourcePlanAccepted atomsDeclared obligationsLinked dependenciesAcyclic
    authorityWithin assumptionsRecorded targetDeclared validatorsDeclared
    validatorsPassed receiptPresent obligationLoss
  unfold SemanticLoweringRouteFor
  simp [sourcePlanAccepted, atomsDeclared, obligationsLinked,
    dependenciesAcyclic, authorityWithin, assumptionsRecorded, targetDeclared,
    validatorsDeclared, validatorsPassed, receiptPresent, obligationLoss]

theorem invalidating_repair_without_ledger_requires_update
    {review : SemanticLoweringReview} :
    review.sourcePlanAccepted = true ->
    review.atomsDeclared = true ->
    review.obligationsLinked = true ->
    review.dependenciesAcyclic = true ->
    review.authorityWithinContract = true ->
    review.assumptionsRecorded = true ->
    review.targetDeclared = true ->
    review.validatorsDeclared = true ->
    review.validatorsPassed = true ->
    review.loweringReceiptPresent = true ->
    review.obligationsPreserved = true ->
    review.repairInvalidatesObligation = true ->
    review.repairLedgerUpdated = false ->
    SemanticLoweringRouteFor review =
      SemanticLoweringRoute.requireLedgerUpdate := by
  intro sourcePlanAccepted atomsDeclared obligationsLinked dependenciesAcyclic
    authorityWithin assumptionsRecorded targetDeclared validatorsDeclared
    validatorsPassed receiptPresent obligationsPreserved invalidatingRepair
    ledgerMissing
  unfold SemanticLoweringRouteFor
  simp [sourcePlanAccepted, atomsDeclared, obligationsLinked,
    dependenciesAcyclic, authorityWithin, assumptionsRecorded, targetDeclared,
    validatorsDeclared, validatorsPassed, receiptPresent, obligationsPreserved,
    invalidatingRepair, ledgerMissing]

theorem known_residual_records_lowering_residual
    {review : SemanticLoweringReview} :
    review.sourcePlanAccepted = true ->
    review.atomsDeclared = true ->
    review.obligationsLinked = true ->
    review.dependenciesAcyclic = true ->
    review.authorityWithinContract = true ->
    review.assumptionsRecorded = true ->
    review.targetDeclared = true ->
    review.validatorsDeclared = true ->
    review.validatorsPassed = true ->
    review.loweringReceiptPresent = true ->
    review.obligationsPreserved = true ->
    review.repairInvalidatesObligation = false ->
    review.residualKnown = true ->
    SemanticLoweringRouteFor review =
      SemanticLoweringRoute.recordResidual := by
  intro sourcePlanAccepted atomsDeclared obligationsLinked dependenciesAcyclic
    authorityWithin assumptionsRecorded targetDeclared validatorsDeclared
    validatorsPassed receiptPresent obligationsPreserved noInvalidatingRepair
    residualKnown
  unfold SemanticLoweringRouteFor
  simp [sourcePlanAccepted, atomsDeclared, obligationsLinked,
    dependenciesAcyclic, authorityWithin, assumptionsRecorded, targetDeclared,
    validatorsDeclared, validatorsPassed, receiptPresent, obligationsPreserved,
    noInvalidatingRepair, residualKnown]

theorem complete_lowering_review_accepts
    {review : SemanticLoweringReview} :
    review.sourcePlanAccepted = true ->
    review.atomsDeclared = true ->
    review.obligationsLinked = true ->
    review.dependenciesAcyclic = true ->
    review.authorityWithinContract = true ->
    review.assumptionsRecorded = true ->
    review.targetDeclared = true ->
    review.validatorsDeclared = true ->
    review.validatorsPassed = true ->
    review.loweringReceiptPresent = true ->
    review.obligationsPreserved = true ->
    review.repairInvalidatesObligation = false ->
    review.residualKnown = false ->
    review.acceptRequested = true ->
    SemanticLoweringRouteFor review =
      SemanticLoweringRoute.acceptLowering := by
  intro sourcePlanAccepted atomsDeclared obligationsLinked dependenciesAcyclic
    authorityWithin assumptionsRecorded targetDeclared validatorsDeclared
    validatorsPassed receiptPresent obligationsPreserved noInvalidatingRepair
    noResidual acceptRequested
  unfold SemanticLoweringRouteFor
  simp [sourcePlanAccepted, atomsDeclared, obligationsLinked,
    dependenciesAcyclic, authorityWithin, assumptionsRecorded, targetDeclared,
    validatorsDeclared, validatorsPassed, receiptPresent, obligationsPreserved,
    noInvalidatingRepair, noResidual, acceptRequested]

end AsiStackProofs.CognitiveCompilation
