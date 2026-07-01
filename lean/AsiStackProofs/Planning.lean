namespace AsiStackProofs.Planning

inductive AuthorityLevel where
  | none
  | read
  | transform
  | write
  | execute
  | approve
deriving DecidableEq, Repr

def AuthorityLevel.rank : AuthorityLevel -> Nat
  | .none => 0
  | .read => 1
  | .transform => 2
  | .write => 3
  | .execute => 4
  | .approve => 5

structure ParentContract where
  authorityCeiling : AuthorityLevel
deriving DecidableEq, Repr

structure PlanNode where
  authorityCeiling : AuthorityLevel
  governanceLowering : Bool
  requiredConstraintsSatisfied : Bool
  stopConditionsDeclared : Bool
deriving DecidableEq, Repr

def AuthorityInheritanceValid (parent : ParentContract) (node : PlanNode) : Prop :=
  node.authorityCeiling = parent.authorityCeiling ∨
    (node.governanceLowering = true ∧
      node.authorityCeiling.rank <= parent.authorityCeiling.rank)

theorem plan_node_inherits_authority_without_governance_lowering
    {parent : ParentContract} {node : PlanNode} :
    AuthorityInheritanceValid parent node ->
    node.governanceLowering = false ->
    node.authorityCeiling = parent.authorityCeiling := by
  intro valid noLowering
  cases valid with
  | inl inherited =>
      exact inherited
  | inr lowered =>
      rw [noLowering] at lowered
      cases lowered.1

def Dispatchable (node : PlanNode) : Prop :=
  node.requiredConstraintsSatisfied = true ∧
    node.stopConditionsDeclared = true

theorem unsatisfied_required_constraints_block_dispatch
    {node : PlanNode} :
    node.requiredConstraintsSatisfied = false ->
    ¬ Dispatchable node := by
  intro unsatisfied dispatchable
  unfold Dispatchable at dispatchable
  rw [unsatisfied] at dispatchable
  cases dispatchable.1

inductive PlanDispatchState where
  | proposed
  | blocked
  | dispatchable
  | dispatched
  | replanned
  | stopped
deriving DecidableEq, Repr

structure PlanControlRecord where
  nodeState : PlanDispatchState
  parentAuthorityCeiling : AuthorityLevel
  nodeAuthorityCeiling : AuthorityLevel
  governanceLowering : Bool
  commandValidatedForPlanning : Bool
  requiredConstraintsSatisfied : Bool
  stopConditionsDeclared : Bool
  contextRequirementsDeclared : Bool
  verificationPlanDeclared : Bool
  blockedNodesPresent : Bool
  dispatchReceiptsPresent : Bool
  replanningPreservesAuthority : Bool
  replanningPreservesStopConditions : Bool
  residualRegisterPresent : Bool
  nonClaimsPresent : Bool
deriving DecidableEq, Repr

def PlanAuthorityWithinParent (record : PlanControlRecord) : Prop :=
  record.nodeAuthorityCeiling = record.parentAuthorityCeiling ∨
    (record.governanceLowering = true ∧
      record.nodeAuthorityCeiling.rank <= record.parentAuthorityCeiling.rank)

structure PlanControlRecordValid (record : PlanControlRecord) : Prop where
  nonClaimsPresent : record.nonClaimsPresent = true
  dispatchableCommandValidated :
    record.nodeState = PlanDispatchState.dispatchable ->
      record.commandValidatedForPlanning = true
  dispatchableConstraintsSatisfied :
    record.nodeState = PlanDispatchState.dispatchable ->
      record.requiredConstraintsSatisfied = true
  dispatchableStopConditionsDeclared :
    record.nodeState = PlanDispatchState.dispatchable ->
      record.stopConditionsDeclared = true
  dispatchableContextRequirementsDeclared :
    record.nodeState = PlanDispatchState.dispatchable ->
      record.contextRequirementsDeclared = true
  dispatchableVerificationPlanDeclared :
    record.nodeState = PlanDispatchState.dispatchable ->
      record.verificationPlanDeclared = true
  dispatchableHasNoBlockedNodes :
    record.nodeState = PlanDispatchState.dispatchable ->
      record.blockedNodesPresent = false
  dispatchableHasReceipt :
    record.nodeState = PlanDispatchState.dispatchable ->
      record.dispatchReceiptsPresent = true
  dispatchableAuthorityWithinParent :
    record.nodeState = PlanDispatchState.dispatchable ->
      PlanAuthorityWithinParent record
  blockedHasBlockedNodes :
    record.nodeState = PlanDispatchState.blocked ->
      record.blockedNodesPresent = true
  blockedHasNoReceipt :
    record.nodeState = PlanDispatchState.blocked ->
      record.dispatchReceiptsPresent = false
  replannedPreservesAuthority :
    record.nodeState = PlanDispatchState.replanned ->
      record.replanningPreservesAuthority = true
  replannedPreservesStopConditions :
    record.nodeState = PlanDispatchState.replanned ->
      record.replanningPreservesStopConditions = true
  replannedHasResidualRegister :
    record.nodeState = PlanDispatchState.replanned ->
      record.residualRegisterPresent = true

inductive PlanControlRoute where
  | holdForPlanning
  | blockForMissingGate
  | keepBlocked
  | allowDispatch
  | replanWithResidual
  | stop
deriving DecidableEq, Repr

def PlanDispatchReady (record : PlanControlRecord) : Bool :=
  record.commandValidatedForPlanning &&
    record.requiredConstraintsSatisfied &&
      record.stopConditionsDeclared &&
        record.contextRequirementsDeclared &&
          record.verificationPlanDeclared &&
            !record.blockedNodesPresent &&
              record.dispatchReceiptsPresent

def PlanControlRouteFor (record : PlanControlRecord) : PlanControlRoute :=
  match record.nodeState with
  | PlanDispatchState.proposed => PlanControlRoute.holdForPlanning
  | PlanDispatchState.blocked => PlanControlRoute.keepBlocked
  | PlanDispatchState.dispatchable =>
      if PlanDispatchReady record then
        PlanControlRoute.allowDispatch
      else
        PlanControlRoute.blockForMissingGate
  | PlanDispatchState.dispatched => PlanControlRoute.allowDispatch
  | PlanDispatchState.replanned => PlanControlRoute.replanWithResidual
  | PlanDispatchState.stopped => PlanControlRoute.stop

theorem valid_dispatchable_plan_has_required_gates
    {record : PlanControlRecord} :
    PlanControlRecordValid record ->
    record.nodeState = PlanDispatchState.dispatchable ->
    record.commandValidatedForPlanning = true ∧
      record.requiredConstraintsSatisfied = true ∧
        record.stopConditionsDeclared = true ∧
          record.contextRequirementsDeclared = true ∧
            record.verificationPlanDeclared = true := by
  intro valid dispatchable
  exact ⟨
    valid.dispatchableCommandValidated dispatchable,
    valid.dispatchableConstraintsSatisfied dispatchable,
    valid.dispatchableStopConditionsDeclared dispatchable,
    valid.dispatchableContextRequirementsDeclared dispatchable,
    valid.dispatchableVerificationPlanDeclared dispatchable
  ⟩

theorem valid_dispatchable_plan_has_receipt_and_no_blocked_nodes
    {record : PlanControlRecord} :
    PlanControlRecordValid record ->
    record.nodeState = PlanDispatchState.dispatchable ->
    record.dispatchReceiptsPresent = true ∧
      record.blockedNodesPresent = false := by
  intro valid dispatchable
  exact ⟨
    valid.dispatchableHasReceipt dispatchable,
    valid.dispatchableHasNoBlockedNodes dispatchable
  ⟩

theorem valid_dispatchable_plan_preserves_parent_authority
    {record : PlanControlRecord} :
    PlanControlRecordValid record ->
    record.nodeState = PlanDispatchState.dispatchable ->
    PlanAuthorityWithinParent record := by
  intro valid dispatchable
  exact valid.dispatchableAuthorityWithinParent dispatchable

theorem valid_blocked_plan_has_no_dispatch_receipt
    {record : PlanControlRecord} :
    PlanControlRecordValid record ->
    record.nodeState = PlanDispatchState.blocked ->
    record.blockedNodesPresent = true ∧
      record.dispatchReceiptsPresent = false := by
  intro valid blocked
  exact ⟨
    valid.blockedHasBlockedNodes blocked,
    valid.blockedHasNoReceipt blocked
  ⟩

theorem valid_replanned_plan_preserves_control_residuals
    {record : PlanControlRecord} :
    PlanControlRecordValid record ->
    record.nodeState = PlanDispatchState.replanned ->
    record.replanningPreservesAuthority = true ∧
      record.replanningPreservesStopConditions = true ∧
        record.residualRegisterPresent = true := by
  intro valid replanned
  exact ⟨
    valid.replannedPreservesAuthority replanned,
    valid.replannedPreservesStopConditions replanned,
    valid.replannedHasResidualRegister replanned
  ⟩

theorem valid_plan_control_record_preserves_non_claim_boundary
    {record : PlanControlRecord} :
    PlanControlRecordValid record ->
    record.nonClaimsPresent = true := by
  intro valid
  exact valid.nonClaimsPresent

theorem valid_dispatchable_plan_routes_to_allow_dispatch
    {record : PlanControlRecord} :
    PlanControlRecordValid record ->
    record.nodeState = PlanDispatchState.dispatchable ->
    PlanControlRouteFor record = PlanControlRoute.allowDispatch := by
  intro valid dispatchable
  have gates := valid_dispatchable_plan_has_required_gates valid dispatchable
  have receipt := valid_dispatchable_plan_has_receipt_and_no_blocked_nodes valid dispatchable
  rcases gates with ⟨commandValid, constraintsSatisfied, stopDeclared, contextDeclared, verificationDeclared⟩
  rcases receipt with ⟨receiptPresent, noBlockedNodes⟩
  unfold PlanControlRouteFor PlanDispatchReady
  rw [
    dispatchable,
    commandValid,
    constraintsSatisfied,
    stopDeclared,
    contextDeclared,
    verificationDeclared,
    noBlockedNodes,
    receiptPresent
  ]
  simp

inductive PlanGraphAdmissionRoute where
  | missingCommandContract
  | missingDecomposition
  | cyclicGraph
  | unorderedDependencies
  | authorityEscalation
  | missingContextDemand
  | missingAdequacyContract
  | missingVerificationPlan
  | missingDispatchGate
  | missingDispatchReceipt
  | invalidReplanDelta
  | missingResidualRegister
  | missingNonClaimBoundary
  | admissible
deriving DecidableEq, Repr

structure PlanGraphAdmissionReview where
  commandContractAccepted : Bool
  decompositionComplete : Bool
  acyclicCertificate : Bool
  dependenciesOrdered : Bool
  authorityWithinParent : Bool
  contextDemandDeclared : Bool
  adequacyContractDeclared : Bool
  verificationPlanDeclared : Bool
  dispatchGateSatisfied : Bool
  dispatchReceiptPresent : Bool
  replanAttempted : Bool
  replanPreservesAuthority : Bool
  replanPreservesStopConditions : Bool
  residualRegisterPresent : Bool
  nonClaimsPresent : Bool
deriving DecidableEq, Repr

def ReplanControlsPreserved (review : PlanGraphAdmissionReview) : Prop :=
  review.replanAttempted = false ∨
    (review.replanPreservesAuthority = true ∧
      review.replanPreservesStopConditions = true ∧
        review.residualRegisterPresent = true)

def PlanGraphAdmissionRouteFor
    (review : PlanGraphAdmissionReview) :
    PlanGraphAdmissionRoute :=
  if !review.commandContractAccepted then
    PlanGraphAdmissionRoute.missingCommandContract
  else if !review.decompositionComplete then
    PlanGraphAdmissionRoute.missingDecomposition
  else if !review.acyclicCertificate then
    PlanGraphAdmissionRoute.cyclicGraph
  else if !review.dependenciesOrdered then
    PlanGraphAdmissionRoute.unorderedDependencies
  else if !review.authorityWithinParent then
    PlanGraphAdmissionRoute.authorityEscalation
  else if !review.contextDemandDeclared then
    PlanGraphAdmissionRoute.missingContextDemand
  else if !review.adequacyContractDeclared then
    PlanGraphAdmissionRoute.missingAdequacyContract
  else if !review.verificationPlanDeclared then
    PlanGraphAdmissionRoute.missingVerificationPlan
  else if !review.dispatchGateSatisfied then
    PlanGraphAdmissionRoute.missingDispatchGate
  else if !review.dispatchReceiptPresent then
    PlanGraphAdmissionRoute.missingDispatchReceipt
  else if review.replanAttempted then
    if review.replanPreservesAuthority &&
        review.replanPreservesStopConditions &&
          review.residualRegisterPresent then
      if review.nonClaimsPresent then
        PlanGraphAdmissionRoute.admissible
      else
        PlanGraphAdmissionRoute.missingNonClaimBoundary
    else
      PlanGraphAdmissionRoute.invalidReplanDelta
  else if !review.residualRegisterPresent then
    PlanGraphAdmissionRoute.missingResidualRegister
  else if !review.nonClaimsPresent then
    PlanGraphAdmissionRoute.missingNonClaimBoundary
  else
    PlanGraphAdmissionRoute.admissible

theorem missing_command_contract_blocks_plan_graph_admission
    {review : PlanGraphAdmissionReview} :
    review.commandContractAccepted = false ->
    PlanGraphAdmissionRouteFor review =
      PlanGraphAdmissionRoute.missingCommandContract := by
  intro missingContract
  unfold PlanGraphAdmissionRouteFor
  rw [missingContract]
  simp

theorem incomplete_decomposition_blocks_plan_graph_admission
    {review : PlanGraphAdmissionReview} :
    review.commandContractAccepted = true ->
    review.decompositionComplete = false ->
    PlanGraphAdmissionRouteFor review =
      PlanGraphAdmissionRoute.missingDecomposition := by
  intro commandAccepted incompleteDecomposition
  unfold PlanGraphAdmissionRouteFor
  rw [commandAccepted, incompleteDecomposition]
  simp

theorem cyclic_plan_graph_blocks_admission
    {review : PlanGraphAdmissionReview} :
    review.commandContractAccepted = true ->
    review.decompositionComplete = true ->
    review.acyclicCertificate = false ->
    PlanGraphAdmissionRouteFor review =
      PlanGraphAdmissionRoute.cyclicGraph := by
  intro commandAccepted decompositionComplete cyclicGraph
  unfold PlanGraphAdmissionRouteFor
  rw [commandAccepted, decompositionComplete, cyclicGraph]
  simp

theorem unordered_dependencies_block_plan_graph_admission
    {review : PlanGraphAdmissionReview} :
    review.commandContractAccepted = true ->
    review.decompositionComplete = true ->
    review.acyclicCertificate = true ->
    review.dependenciesOrdered = false ->
    PlanGraphAdmissionRouteFor review =
      PlanGraphAdmissionRoute.unorderedDependencies := by
  intro commandAccepted decompositionComplete acyclic unorderedDependencies
  unfold PlanGraphAdmissionRouteFor
  rw [
    commandAccepted,
    decompositionComplete,
    acyclic,
    unorderedDependencies
  ]
  simp

theorem authority_escalation_blocks_plan_graph_admission
    {review : PlanGraphAdmissionReview} :
    review.commandContractAccepted = true ->
    review.decompositionComplete = true ->
    review.acyclicCertificate = true ->
    review.dependenciesOrdered = true ->
    review.authorityWithinParent = false ->
    PlanGraphAdmissionRouteFor review =
      PlanGraphAdmissionRoute.authorityEscalation := by
  intro commandAccepted decompositionComplete acyclic ordered authorityEscalates
  unfold PlanGraphAdmissionRouteFor
  rw [
    commandAccepted,
    decompositionComplete,
    acyclic,
    ordered,
    authorityEscalates
  ]
  simp

theorem missing_context_demand_blocks_plan_graph_admission
    {review : PlanGraphAdmissionReview} :
    review.commandContractAccepted = true ->
    review.decompositionComplete = true ->
    review.acyclicCertificate = true ->
    review.dependenciesOrdered = true ->
    review.authorityWithinParent = true ->
    review.contextDemandDeclared = false ->
    PlanGraphAdmissionRouteFor review =
      PlanGraphAdmissionRoute.missingContextDemand := by
  intro commandAccepted decompositionComplete acyclic ordered authorityOk missingContext
  unfold PlanGraphAdmissionRouteFor
  rw [
    commandAccepted,
    decompositionComplete,
    acyclic,
    ordered,
    authorityOk,
    missingContext
  ]
  simp

theorem missing_adequacy_contract_blocks_plan_graph_admission
    {review : PlanGraphAdmissionReview} :
    review.commandContractAccepted = true ->
    review.decompositionComplete = true ->
    review.acyclicCertificate = true ->
    review.dependenciesOrdered = true ->
    review.authorityWithinParent = true ->
    review.contextDemandDeclared = true ->
    review.adequacyContractDeclared = false ->
    PlanGraphAdmissionRouteFor review =
      PlanGraphAdmissionRoute.missingAdequacyContract := by
  intro commandAccepted decompositionComplete acyclic ordered authorityOk contextOk missingAdequacy
  unfold PlanGraphAdmissionRouteFor
  rw [
    commandAccepted,
    decompositionComplete,
    acyclic,
    ordered,
    authorityOk,
    contextOk,
    missingAdequacy
  ]
  simp

theorem missing_verification_plan_blocks_plan_graph_admission
    {review : PlanGraphAdmissionReview} :
    review.commandContractAccepted = true ->
    review.decompositionComplete = true ->
    review.acyclicCertificate = true ->
    review.dependenciesOrdered = true ->
    review.authorityWithinParent = true ->
    review.contextDemandDeclared = true ->
    review.adequacyContractDeclared = true ->
    review.verificationPlanDeclared = false ->
    PlanGraphAdmissionRouteFor review =
      PlanGraphAdmissionRoute.missingVerificationPlan := by
  intro commandAccepted decompositionComplete acyclic ordered authorityOk contextOk adequacyOk missingVerification
  unfold PlanGraphAdmissionRouteFor
  rw [
    commandAccepted,
    decompositionComplete,
    acyclic,
    ordered,
    authorityOk,
    contextOk,
    adequacyOk,
    missingVerification
  ]
  simp

theorem missing_dispatch_gate_blocks_plan_graph_admission
    {review : PlanGraphAdmissionReview} :
    review.commandContractAccepted = true ->
    review.decompositionComplete = true ->
    review.acyclicCertificate = true ->
    review.dependenciesOrdered = true ->
    review.authorityWithinParent = true ->
    review.contextDemandDeclared = true ->
    review.adequacyContractDeclared = true ->
    review.verificationPlanDeclared = true ->
    review.dispatchGateSatisfied = false ->
    PlanGraphAdmissionRouteFor review =
      PlanGraphAdmissionRoute.missingDispatchGate := by
  intro commandAccepted decompositionComplete acyclic ordered authorityOk contextOk adequacyOk verificationOk missingGate
  unfold PlanGraphAdmissionRouteFor
  rw [
    commandAccepted,
    decompositionComplete,
    acyclic,
    ordered,
    authorityOk,
    contextOk,
    adequacyOk,
    verificationOk,
    missingGate
  ]
  simp

theorem missing_dispatch_receipt_blocks_plan_graph_admission
    {review : PlanGraphAdmissionReview} :
    review.commandContractAccepted = true ->
    review.decompositionComplete = true ->
    review.acyclicCertificate = true ->
    review.dependenciesOrdered = true ->
    review.authorityWithinParent = true ->
    review.contextDemandDeclared = true ->
    review.adequacyContractDeclared = true ->
    review.verificationPlanDeclared = true ->
    review.dispatchGateSatisfied = true ->
    review.dispatchReceiptPresent = false ->
    PlanGraphAdmissionRouteFor review =
      PlanGraphAdmissionRoute.missingDispatchReceipt := by
  intro commandAccepted decompositionComplete acyclic ordered authorityOk contextOk adequacyOk verificationOk gateOk missingReceipt
  unfold PlanGraphAdmissionRouteFor
  rw [
    commandAccepted,
    decompositionComplete,
    acyclic,
    ordered,
    authorityOk,
    contextOk,
    adequacyOk,
    verificationOk,
    gateOk,
    missingReceipt
  ]
  simp

theorem replanning_without_authority_preservation_blocks_admission
    {review : PlanGraphAdmissionReview} :
    review.commandContractAccepted = true ->
    review.decompositionComplete = true ->
    review.acyclicCertificate = true ->
    review.dependenciesOrdered = true ->
    review.authorityWithinParent = true ->
    review.contextDemandDeclared = true ->
    review.adequacyContractDeclared = true ->
    review.verificationPlanDeclared = true ->
    review.dispatchGateSatisfied = true ->
    review.dispatchReceiptPresent = true ->
    review.replanAttempted = true ->
    review.replanPreservesAuthority = false ->
    PlanGraphAdmissionRouteFor review =
      PlanGraphAdmissionRoute.invalidReplanDelta := by
  intro commandAccepted decompositionComplete acyclic ordered authorityOk contextOk adequacyOk verificationOk gateOk receiptOk replan attemptedWidening
  unfold PlanGraphAdmissionRouteFor
  rw [
    commandAccepted,
    decompositionComplete,
    acyclic,
    ordered,
    authorityOk,
    contextOk,
    adequacyOk,
    verificationOk,
    gateOk,
    receiptOk,
    replan,
    attemptedWidening
  ]
  simp

theorem missing_residual_register_blocks_new_plan_admission
    {review : PlanGraphAdmissionReview} :
    review.commandContractAccepted = true ->
    review.decompositionComplete = true ->
    review.acyclicCertificate = true ->
    review.dependenciesOrdered = true ->
    review.authorityWithinParent = true ->
    review.contextDemandDeclared = true ->
    review.adequacyContractDeclared = true ->
    review.verificationPlanDeclared = true ->
    review.dispatchGateSatisfied = true ->
    review.dispatchReceiptPresent = true ->
    review.replanAttempted = false ->
    review.residualRegisterPresent = false ->
    PlanGraphAdmissionRouteFor review =
      PlanGraphAdmissionRoute.missingResidualRegister := by
  intro commandAccepted decompositionComplete acyclic ordered authorityOk contextOk adequacyOk verificationOk gateOk receiptOk noReplan missingResiduals
  unfold PlanGraphAdmissionRouteFor
  rw [
    commandAccepted,
    decompositionComplete,
    acyclic,
    ordered,
    authorityOk,
    contextOk,
    adequacyOk,
    verificationOk,
    gateOk,
    receiptOk,
    noReplan,
    missingResiduals
  ]
  simp

theorem complete_new_plan_graph_routes_to_admissible
    {review : PlanGraphAdmissionReview} :
    review.commandContractAccepted = true ->
    review.decompositionComplete = true ->
    review.acyclicCertificate = true ->
    review.dependenciesOrdered = true ->
    review.authorityWithinParent = true ->
    review.contextDemandDeclared = true ->
    review.adequacyContractDeclared = true ->
    review.verificationPlanDeclared = true ->
    review.dispatchGateSatisfied = true ->
    review.dispatchReceiptPresent = true ->
    review.replanAttempted = false ->
    review.residualRegisterPresent = true ->
    review.nonClaimsPresent = true ->
    PlanGraphAdmissionRouteFor review =
      PlanGraphAdmissionRoute.admissible := by
  intro commandAccepted decompositionComplete acyclic ordered authorityOk contextOk adequacyOk verificationOk gateOk receiptOk noReplan residuals nonClaims
  unfold PlanGraphAdmissionRouteFor
  rw [
    commandAccepted,
    decompositionComplete,
    acyclic,
    ordered,
    authorityOk,
    contextOk,
    adequacyOk,
    verificationOk,
    gateOk,
    receiptOk,
    noReplan,
    residuals,
    nonClaims
  ]
  simp

theorem complete_replanned_graph_routes_to_admissible
    {review : PlanGraphAdmissionReview} :
    review.commandContractAccepted = true ->
    review.decompositionComplete = true ->
    review.acyclicCertificate = true ->
    review.dependenciesOrdered = true ->
    review.authorityWithinParent = true ->
    review.contextDemandDeclared = true ->
    review.adequacyContractDeclared = true ->
    review.verificationPlanDeclared = true ->
    review.dispatchGateSatisfied = true ->
    review.dispatchReceiptPresent = true ->
    review.replanAttempted = true ->
    review.replanPreservesAuthority = true ->
    review.replanPreservesStopConditions = true ->
    review.residualRegisterPresent = true ->
    review.nonClaimsPresent = true ->
    PlanGraphAdmissionRouteFor review =
      PlanGraphAdmissionRoute.admissible := by
  intro commandAccepted decompositionComplete acyclic ordered authorityOk contextOk adequacyOk verificationOk gateOk receiptOk replan authorityPreserved stopsPreserved residuals nonClaims
  unfold PlanGraphAdmissionRouteFor
  rw [
    commandAccepted,
    decompositionComplete,
    acyclic,
    ordered,
    authorityOk,
    contextOk,
    adequacyOk,
    verificationOk,
    gateOk,
    receiptOk,
    replan,
    authorityPreserved,
    stopsPreserved,
    residuals,
    nonClaims
  ]
  simp

end AsiStackProofs.Planning
