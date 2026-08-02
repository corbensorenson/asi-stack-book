import AsiStackProofs.IntentExecutionRefinement

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

structure SchedulerStateProbeSummary where
  validSchedulerTracePresent : Bool
  localRepairTracePresent : Bool
  negativeControlsRejected : Bool
  costQualityLedgerPresent : Bool
  supportStateEffectNone : Bool
  nonClaimBoundary : Bool
deriving DecidableEq, Repr

def SchedulerStateProbeSummaryValid
    (summary : SchedulerStateProbeSummary) : Prop :=
  summary.validSchedulerTracePresent = true ∧
    summary.localRepairTracePresent = true ∧
    summary.negativeControlsRejected = true ∧
    summary.costQualityLedgerPresent = true ∧
    summary.supportStateEffectNone = true ∧
    summary.nonClaimBoundary = true

inductive RuntimeReplanDeltaRoute where
  | noReplan
  | blockAuthorityWidening
  | blockStopConditionErasure
  | blockUnscopedSubgraph
  | blockMissingContextDelta
  | blockMissingVerificationDelta
  | blockMissingResidual
  | blockBlockedAuthorityDispatch
  | blockSupportPromotion
  | blockMissingNonClaimBoundary
  | acceptRuntimeDelta
deriving DecidableEq, Repr

structure RuntimeReplanDeltaAudit where
  replanAttempted : Bool
  authorityPreserved : Bool
  stopConditionsPreserved : Bool
  affectedSubgraphOnly : Bool
  contextDeltaRecorded : Bool
  verificationDeltaRecorded : Bool
  residualsRecorded : Bool
  blockedAuthorityPath : Bool
  dispatchReceiptIssued : Bool
  supportStateEffectNone : Bool
  nonClaimBoundary : Bool
deriving DecidableEq, Repr

def RuntimeReplanDeltaRouteFor
    (audit : RuntimeReplanDeltaAudit) :
    RuntimeReplanDeltaRoute :=
  if !audit.replanAttempted then
    RuntimeReplanDeltaRoute.noReplan
  else if !audit.authorityPreserved then
    RuntimeReplanDeltaRoute.blockAuthorityWidening
  else if !audit.stopConditionsPreserved then
    RuntimeReplanDeltaRoute.blockStopConditionErasure
  else if !audit.affectedSubgraphOnly then
    RuntimeReplanDeltaRoute.blockUnscopedSubgraph
  else if !audit.contextDeltaRecorded then
    RuntimeReplanDeltaRoute.blockMissingContextDelta
  else if !audit.verificationDeltaRecorded then
    RuntimeReplanDeltaRoute.blockMissingVerificationDelta
  else if !audit.residualsRecorded then
    RuntimeReplanDeltaRoute.blockMissingResidual
  else if audit.blockedAuthorityPath && audit.dispatchReceiptIssued then
    RuntimeReplanDeltaRoute.blockBlockedAuthorityDispatch
  else if !audit.supportStateEffectNone then
    RuntimeReplanDeltaRoute.blockSupportPromotion
  else if !audit.nonClaimBoundary then
    RuntimeReplanDeltaRoute.blockMissingNonClaimBoundary
  else
    RuntimeReplanDeltaRoute.acceptRuntimeDelta

theorem runtime_replan_delta_authority_widening_rejected
    {audit : RuntimeReplanDeltaAudit} :
    audit.replanAttempted = true ->
    audit.authorityPreserved = false ->
    RuntimeReplanDeltaRouteFor audit =
      RuntimeReplanDeltaRoute.blockAuthorityWidening := by
  intro replan authorityWidened
  unfold RuntimeReplanDeltaRouteFor
  rw [replan, authorityWidened]
  simp

theorem runtime_replan_delta_stop_erasure_rejected
    {audit : RuntimeReplanDeltaAudit} :
    audit.replanAttempted = true ->
    audit.authorityPreserved = true ->
    audit.stopConditionsPreserved = false ->
    RuntimeReplanDeltaRouteFor audit =
      RuntimeReplanDeltaRoute.blockStopConditionErasure := by
  intro replan authorityOk stopsErased
  unfold RuntimeReplanDeltaRouteFor
  rw [replan, authorityOk, stopsErased]
  simp

theorem runtime_replan_delta_blocked_authority_dispatch_rejected
    {audit : RuntimeReplanDeltaAudit} :
    audit.replanAttempted = true ->
    audit.authorityPreserved = true ->
    audit.stopConditionsPreserved = true ->
    audit.affectedSubgraphOnly = true ->
    audit.contextDeltaRecorded = true ->
    audit.verificationDeltaRecorded = true ->
    audit.residualsRecorded = true ->
    audit.blockedAuthorityPath = true ->
    audit.dispatchReceiptIssued = true ->
    RuntimeReplanDeltaRouteFor audit =
      RuntimeReplanDeltaRoute.blockBlockedAuthorityDispatch := by
  intro replan authorityOk stopsOk scopeOk contextOk verificationOk residualsOk blocked issued
  unfold RuntimeReplanDeltaRouteFor
  rw [
    replan,
    authorityOk,
    stopsOk,
    scopeOk,
    contextOk,
    verificationOk,
    residualsOk,
    blocked,
    issued
  ]
  simp

theorem runtime_replan_delta_complete_audit_accepted
    {audit : RuntimeReplanDeltaAudit} :
    audit.replanAttempted = true ->
    audit.authorityPreserved = true ->
    audit.stopConditionsPreserved = true ->
    audit.affectedSubgraphOnly = true ->
    audit.contextDeltaRecorded = true ->
    audit.verificationDeltaRecorded = true ->
    audit.residualsRecorded = true ->
    audit.blockedAuthorityPath = false ->
    audit.supportStateEffectNone = true ->
    audit.nonClaimBoundary = true ->
    RuntimeReplanDeltaRouteFor audit =
      RuntimeReplanDeltaRoute.acceptRuntimeDelta := by
  intro replan authorityOk stopsOk scopeOk contextOk verificationOk residualsOk notBlocked noSupportEffect nonClaim
  unfold RuntimeReplanDeltaRouteFor
  rw [
    replan,
    authorityOk,
    stopsOk,
    scopeOk,
    contextOk,
    verificationOk,
    residualsOk,
    notBlocked,
    noSupportEffect,
    nonClaim
  ]
  simp

structure RuntimeReplanDeltaSummary where
  validLocalRepairTracePresent : Bool
  validBlockedAuthorityTracePresent : Bool
  negativeControlsRejected : Bool
  authorityPreserved : Bool
  stopConditionsPreserved : Bool
  affectedSubgraphScoped : Bool
  contextDeltaRecorded : Bool
  verificationDeltaRecorded : Bool
  residualsRecorded : Bool
  blockedAuthorityNoDispatch : Bool
  supportStateEffectNone : Bool
  nonClaimBoundary : Bool
deriving DecidableEq, Repr

def RuntimeReplanDeltaSummaryValid
    (summary : RuntimeReplanDeltaSummary) : Prop :=
  summary.validLocalRepairTracePresent = true ∧
    summary.validBlockedAuthorityTracePresent = true ∧
      summary.negativeControlsRejected = true ∧
        summary.authorityPreserved = true ∧
          summary.stopConditionsPreserved = true ∧
            summary.affectedSubgraphScoped = true ∧
              summary.contextDeltaRecorded = true ∧
                summary.verificationDeltaRecorded = true ∧
                  summary.residualsRecorded = true ∧
                    summary.blockedAuthorityNoDispatch = true ∧
                      summary.supportStateEffectNone = true ∧
                        summary.nonClaimBoundary = true

/-! ## Reachable planning-control refinement -/

inductive PlanningLifecyclePhase where
  | command
  | admitted
  | ready
  | lowered
  | feedback
  | blocked
deriving DecidableEq, Repr

inductive PlanningLifecycleEventKind where
  | admitPlan
  | markNodeReady
  | lowerJob
  | observeFeedback
  | applyReplan
  | blockPlan
deriving DecidableEq, Repr

structure PlanningLifecycleState where
  phase : PlanningLifecyclePhase
  rootContract : Nat
  currentArtifact : Nat
  parentAuthorityCeiling : Nat
  activeAuthority : Nat
  planVersion : Nat
  readyNodes : Nat
  loweredJobs : Nat
  feedbackCount : Nat
  replanCount : Nat
  residualCount : Nat
  stopConditionsPreserved : Bool
  pendingDispatch : Bool
  logicalTime : Nat
deriving DecidableEq, Repr

structure PlanningLifecycleEvent where
  kind : PlanningLifecycleEventKind
  fromPhase : PlanningLifecyclePhase
  toPhase : PlanningLifecyclePhase
  rootContract : Nat
  parentArtifact : Nat
  outputArtifact : Nat
  requestedAuthority : Nat
  logicalTime : Nat
  commandAccepted : Bool
  decompositionComplete : Bool
  graphAcyclic : Bool
  dependenciesOrdered : Bool
  dependenciesReady : Bool
  contextPresent : Bool
  adequacyContractPresent : Bool
  selectedRouteAdequate : Bool
  verificationPresent : Bool
  dispatchReceipt : Bool
  feedbackReceipt : Bool
  affectedSubgraphOnly : Bool
  authorityPreserved : Bool
  stopConditionsPreserved : Bool
  contextDeltaRecorded : Bool
  verificationDeltaRecorded : Bool
  blockedAuthorityPath : Bool
  hiddenOverrideApplied : Bool
  residualDelta : Nat
deriving DecidableEq, Repr

def PlanningLifecycleEventSpecificValid
    (state : PlanningLifecycleState)
    (event : PlanningLifecycleEvent) : Bool :=
  match event.kind with
  | .admitPlan =>
      decide (event.fromPhase = .command) &&
        decide (event.toPhase = .admitted) &&
          event.commandAccepted && event.decompositionComplete &&
            event.graphAcyclic && event.dependenciesOrdered &&
              event.adequacyContractPresent &&
                event.verificationPresent &&
                  decide (event.residualDelta = 0)
  | .markNodeReady =>
      decide (event.fromPhase = .admitted) &&
        decide (event.toPhase = .ready) &&
          event.dependenciesReady && event.contextPresent &&
            event.adequacyContractPresent &&
              event.selectedRouteAdequate && event.verificationPresent &&
                !event.blockedAuthorityPath && !event.dispatchReceipt &&
                  decide (event.residualDelta = 0)
  | .lowerJob =>
      decide (event.fromPhase = .ready) &&
        decide (event.toPhase = .lowered) && state.pendingDispatch &&
          event.dispatchReceipt && !event.blockedAuthorityPath &&
            decide (event.residualDelta = 0)
  | .observeFeedback =>
      decide (event.fromPhase = .lowered) &&
        decide (event.toPhase = .feedback) && event.feedbackReceipt &&
          !event.dispatchReceipt && decide (event.residualDelta = 0)
  | .applyReplan =>
      decide (event.fromPhase = .feedback) &&
        decide (event.toPhase = .admitted) &&
          event.affectedSubgraphOnly && event.authorityPreserved &&
            event.stopConditionsPreserved && event.contextDeltaRecorded &&
              event.verificationDeltaRecorded && !event.dispatchReceipt &&
                decide (0 < event.residualDelta)
  | .blockPlan =>
      decide (event.toPhase = .blocked) && !event.dispatchReceipt &&
        decide (0 < event.residualDelta)

def PlanningLifecycleEventAdmissible
    (state : PlanningLifecycleState)
    (event : PlanningLifecycleEvent) : Prop :=
  state.phase = event.fromPhase ∧
    state.rootContract = event.rootContract ∧
      state.currentArtifact = event.parentArtifact ∧
        state.logicalTime < event.logicalTime ∧
          event.requestedAuthority ≤ state.parentAuthorityCeiling ∧
            event.stopConditionsPreserved = true ∧
              event.hiddenOverrideApplied = false ∧
                PlanningLifecycleEventSpecificValid state event = true

instance planningLifecycleEventAdmissibleDecidable
    (state : PlanningLifecycleState) (event : PlanningLifecycleEvent) :
    Decidable (PlanningLifecycleEventAdmissible state event) := by
  unfold PlanningLifecycleEventAdmissible
  infer_instance

def ApplyPlanningLifecycleEvent
    (state : PlanningLifecycleState)
    (event : PlanningLifecycleEvent) : PlanningLifecycleState :=
  { state with
    phase := event.toPhase
    currentArtifact := event.outputArtifact
    activeAuthority := event.requestedAuthority
    planVersion := state.planVersion +
      (if event.kind = .applyReplan then 1 else 0)
    readyNodes := state.readyNodes +
      (if event.kind = .markNodeReady then 1 else 0)
    loweredJobs := state.loweredJobs +
      (if event.kind = .lowerJob then 1 else 0)
    feedbackCount := state.feedbackCount +
      (if event.kind = .observeFeedback then 1 else 0)
    replanCount := state.replanCount +
      (if event.kind = .applyReplan then 1 else 0)
    residualCount := state.residualCount + event.residualDelta
    stopConditionsPreserved :=
      state.stopConditionsPreserved && event.stopConditionsPreserved
    pendingDispatch := event.kind = .markNodeReady
    logicalTime := event.logicalTime }

def PlanningLifecycleStep
    (state : PlanningLifecycleState)
    (event : PlanningLifecycleEvent) : Option PlanningLifecycleState :=
  if PlanningLifecycleEventAdmissible state event then
    some (ApplyPlanningLifecycleEvent state event)
  else
    none

def PlanningLifecycleRun :
    PlanningLifecycleState → List PlanningLifecycleEvent →
      Option PlanningLifecycleState
  | state, [] => some state
  | state, event :: tail =>
      match PlanningLifecycleStep state event with
      | none => none
      | some next => PlanningLifecycleRun next tail

def PlanningLifecycleInvariant (state : PlanningLifecycleState) : Prop :=
  state.activeAuthority ≤ state.parentAuthorityCeiling ∧
    state.loweredJobs ≤ state.readyNodes ∧
      state.feedbackCount ≤ state.loweredJobs ∧
        state.replanCount ≤ state.feedbackCount ∧
          state.planVersion = state.replanCount + 1 ∧
            state.stopConditionsPreserved = true ∧
              (state.phase = .ready →
                state.pendingDispatch = true ∧
                  state.loweredJobs < state.readyNodes) ∧
                (state.phase = .lowered →
                  state.pendingDispatch = false ∧
                    state.feedbackCount < state.loweredJobs) ∧
                  (state.phase = .feedback →
                    state.pendingDispatch = false ∧
                      state.replanCount < state.feedbackCount) ∧
                    (state.phase = .blocked →
                      state.pendingDispatch = false)

theorem accepted_planning_lifecycle_step_is_admissible
    {state next : PlanningLifecycleState}
    {event : PlanningLifecycleEvent}
    (accepted : PlanningLifecycleStep state event = some next) :
    PlanningLifecycleEventAdmissible state event := by
  unfold PlanningLifecycleStep at accepted
  split at accepted
  · assumption
  · simp at accepted

theorem accepted_planning_lifecycle_step_applies_event
    {state next : PlanningLifecycleState}
    {event : PlanningLifecycleEvent}
    (accepted : PlanningLifecycleStep state event = some next) :
    next = ApplyPlanningLifecycleEvent state event := by
  unfold PlanningLifecycleStep at accepted
  split at accepted
  · simp_all
  · simp at accepted

theorem apply_planning_lifecycle_event_preserves_invariant
    {state : PlanningLifecycleState}
    {event : PlanningLifecycleEvent}
    (invariant : PlanningLifecycleInvariant state)
    (admissible : PlanningLifecycleEventAdmissible state event) :
    PlanningLifecycleInvariant (ApplyPlanningLifecycleEvent state event) := by
  rcases invariant with
    ⟨authority, loweredReady, feedbackLowered, replanFeedback,
      version, stops, readyState, loweredState, feedbackState, blockedState⟩
  rcases admissible with
    ⟨phase, _root, _artifact, _time, requested, eventStops,
      _override, specific⟩
  cases kind : event.kind
  · simp [PlanningLifecycleEventSpecificValid, kind] at specific
    have phasePair :
        event.fromPhase = .command ∧ event.toPhase = .admitted :=
      specific.1.1.1.1.1.1.1
    have statePhase : state.phase = .command := phase.trans phasePair.1
    refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
    · exact requested
    · simpa [ApplyPlanningLifecycleEvent, kind] using loweredReady
    · simpa [ApplyPlanningLifecycleEvent, kind] using feedbackLowered
    · simpa [ApplyPlanningLifecycleEvent, kind] using replanFeedback
    · simpa [ApplyPlanningLifecycleEvent, kind] using version
    · simp [ApplyPlanningLifecycleEvent, kind, stops, eventStops]
    · simp [ApplyPlanningLifecycleEvent, kind, phasePair.2]
    · simp [ApplyPlanningLifecycleEvent, kind, phasePair.2]
    · simp [ApplyPlanningLifecycleEvent, kind, phasePair.2]
    · simp [ApplyPlanningLifecycleEvent, kind, phasePair.2]
  · simp [PlanningLifecycleEventSpecificValid, kind] at specific
    have phasePair :
        event.fromPhase = .admitted ∧ event.toPhase = .ready :=
      specific.1.1.1.1.1.1.1.1
    refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
    · exact requested
    · simp [ApplyPlanningLifecycleEvent, kind]
      omega
    · simpa [ApplyPlanningLifecycleEvent, kind] using feedbackLowered
    · simpa [ApplyPlanningLifecycleEvent, kind] using replanFeedback
    · simpa [ApplyPlanningLifecycleEvent, kind] using version
    · simp [ApplyPlanningLifecycleEvent, kind, stops, eventStops]
    · simp [ApplyPlanningLifecycleEvent, kind, phasePair.2]
      omega
    · simp [ApplyPlanningLifecycleEvent, kind, phasePair.2]
    · simp [ApplyPlanningLifecycleEvent, kind, phasePair.2]
    · simp [ApplyPlanningLifecycleEvent, kind, phasePair.2]
  · simp [PlanningLifecycleEventSpecificValid, kind] at specific
    have phasePair :
        event.fromPhase = .ready ∧ event.toPhase = .lowered :=
      specific.1.1.1.1
    have currentReady := readyState (phase.trans phasePair.1)
    refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
    · exact requested
    · simp [ApplyPlanningLifecycleEvent, kind]
      exact currentReady.2
    · simp [ApplyPlanningLifecycleEvent, kind]
      omega
    · simpa [ApplyPlanningLifecycleEvent, kind] using replanFeedback
    · simpa [ApplyPlanningLifecycleEvent, kind] using version
    · simp [ApplyPlanningLifecycleEvent, kind, stops, eventStops]
    · simp [ApplyPlanningLifecycleEvent, kind, phasePair.2]
    · simp [ApplyPlanningLifecycleEvent, kind, phasePair.2]
      omega
    · simp [ApplyPlanningLifecycleEvent, kind, phasePair.2]
    · simp [ApplyPlanningLifecycleEvent, kind, phasePair.2]
  · simp [PlanningLifecycleEventSpecificValid, kind] at specific
    have phasePair :
        event.fromPhase = .lowered ∧ event.toPhase = .feedback :=
      specific.1.1.1
    have currentLowered := loweredState (phase.trans phasePair.1)
    refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
    · exact requested
    · simpa [ApplyPlanningLifecycleEvent, kind] using loweredReady
    · simp [ApplyPlanningLifecycleEvent, kind]
      exact currentLowered.2
    · simp [ApplyPlanningLifecycleEvent, kind]
      omega
    · simpa [ApplyPlanningLifecycleEvent, kind] using version
    · simp [ApplyPlanningLifecycleEvent, kind, stops, eventStops]
    · simp [ApplyPlanningLifecycleEvent, kind, phasePair.2]
    · simp [ApplyPlanningLifecycleEvent, kind, phasePair.2]
    · simp [ApplyPlanningLifecycleEvent, kind, phasePair.2]
      omega
    · simp [ApplyPlanningLifecycleEvent, kind, phasePair.2]
  · simp [PlanningLifecycleEventSpecificValid, kind] at specific
    have phasePair :
        event.fromPhase = .feedback ∧ event.toPhase = .admitted :=
      specific.1.1.1.1.1.1.1
    have currentFeedback := feedbackState (phase.trans phasePair.1)
    refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
    · exact requested
    · simpa [ApplyPlanningLifecycleEvent, kind] using loweredReady
    · simpa [ApplyPlanningLifecycleEvent, kind] using feedbackLowered
    · simp [ApplyPlanningLifecycleEvent, kind]
      exact currentFeedback.2
    · simp [ApplyPlanningLifecycleEvent, kind, version]
    · simp [ApplyPlanningLifecycleEvent, kind, stops, eventStops]
    · simp [ApplyPlanningLifecycleEvent, kind, phasePair.2]
    · simp [ApplyPlanningLifecycleEvent, kind, phasePair.2]
    · simp [ApplyPlanningLifecycleEvent, kind, phasePair.2]
    · simp [ApplyPlanningLifecycleEvent, kind, phasePair.2]
  · simp [PlanningLifecycleEventSpecificValid, kind] at specific
    have toPhase : event.toPhase = .blocked := specific.1.1
    refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
    · exact requested
    · simpa [ApplyPlanningLifecycleEvent, kind] using loweredReady
    · simpa [ApplyPlanningLifecycleEvent, kind] using feedbackLowered
    · simpa [ApplyPlanningLifecycleEvent, kind] using replanFeedback
    · simpa [ApplyPlanningLifecycleEvent, kind] using version
    · simp [ApplyPlanningLifecycleEvent, kind, stops, eventStops]
    · simp [ApplyPlanningLifecycleEvent, kind, toPhase]
    · simp [ApplyPlanningLifecycleEvent, kind, toPhase]
    · simp [ApplyPlanningLifecycleEvent, kind, toPhase]
    · simp [ApplyPlanningLifecycleEvent, kind, toPhase]

theorem accepted_planning_lifecycle_step_preserves_invariant
    {state next : PlanningLifecycleState}
    {event : PlanningLifecycleEvent}
    (invariant : PlanningLifecycleInvariant state)
    (accepted : PlanningLifecycleStep state event = some next) :
    PlanningLifecycleInvariant next := by
  rw [accepted_planning_lifecycle_step_applies_event accepted]
  exact apply_planning_lifecycle_event_preserves_invariant invariant
    (accepted_planning_lifecycle_step_is_admissible accepted)

theorem planning_lifecycle_run_preserves_invariant
    {state next : PlanningLifecycleState}
    {events : List PlanningLifecycleEvent}
    (invariant : PlanningLifecycleInvariant state)
    (run : PlanningLifecycleRun state events = some next) :
    PlanningLifecycleInvariant next := by
  induction events generalizing state with
  | nil =>
      simp [PlanningLifecycleRun] at run
      subst next
      exact invariant
  | cons event tail ih =>
      simp [PlanningLifecycleRun] at run
      cases step : PlanningLifecycleStep state event with
      | none => simp [step] at run
      | some middle =>
          simp [step] at run
          exact ih
            (accepted_planning_lifecycle_step_preserves_invariant invariant step)
            run

def initialPlanningLifecycleState : PlanningLifecycleState where
  phase := .command
  rootContract := 101
  currentArtifact := 1002
  parentAuthorityCeiling := 3
  activeAuthority := 0
  planVersion := 1
  readyNodes := 0
  loweredJobs := 0
  feedbackCount := 0
  replanCount := 0
  residualCount := 0
  stopConditionsPreserved := true
  pendingDispatch := false
  logicalTime := 1

def basePlanningLifecycleEvent : PlanningLifecycleEvent where
  kind := .admitPlan
  fromPhase := .command
  toPhase := .admitted
  rootContract := 101
  parentArtifact := 1002
  outputArtifact := 1003
  requestedAuthority := 3
  logicalTime := 2
  commandAccepted := true
  decompositionComplete := true
  graphAcyclic := true
  dependenciesOrdered := true
  dependenciesReady := true
  contextPresent := true
  adequacyContractPresent := true
  selectedRouteAdequate := true
  verificationPresent := true
  dispatchReceipt := false
  feedbackReceipt := false
  affectedSubgraphOnly := true
  authorityPreserved := true
  stopConditionsPreserved := true
  contextDeltaRecorded := true
  verificationDeltaRecorded := true
  blockedAuthorityPath := false
  hiddenOverrideApplied := false
  residualDelta := 0

def completePlanningLifecycleTrace : List PlanningLifecycleEvent := [
  basePlanningLifecycleEvent,
  { basePlanningLifecycleEvent with
      kind := .markNodeReady
      fromPhase := .admitted
      toPhase := .ready
      parentArtifact := 1003
      outputArtifact := 1003
      logicalTime := 3 },
  { basePlanningLifecycleEvent with
      kind := .lowerJob
      fromPhase := .ready
      toPhase := .lowered
      parentArtifact := 1003
      outputArtifact := 1004
      dispatchReceipt := true
      logicalTime := 4 },
  { basePlanningLifecycleEvent with
      kind := .observeFeedback
      fromPhase := .lowered
      toPhase := .feedback
      parentArtifact := 1004
      outputArtifact := 1004
      feedbackReceipt := true
      logicalTime := 5 },
  { basePlanningLifecycleEvent with
      kind := .applyReplan
      fromPhase := .feedback
      toPhase := .admitted
      parentArtifact := 1004
      outputArtifact := 1005
      residualDelta := 1
      logicalTime := 6 },
  { basePlanningLifecycleEvent with
      kind := .markNodeReady
      fromPhase := .admitted
      toPhase := .ready
      parentArtifact := 1005
      outputArtifact := 1005
      logicalTime := 7 },
  { basePlanningLifecycleEvent with
      kind := .lowerJob
      fromPhase := .ready
      toPhase := .lowered
      parentArtifact := 1005
      outputArtifact := 1006
      dispatchReceipt := true
      logicalTime := 8 }
]

theorem initial_planning_lifecycle_state_satisfies_invariant :
    PlanningLifecycleInvariant initialPlanningLifecycleState := by
  simp [PlanningLifecycleInvariant, initialPlanningLifecycleState]

theorem complete_planning_lifecycle_trace_reaches_replanned_lowering :
    PlanningLifecycleRun initialPlanningLifecycleState
      completePlanningLifecycleTrace =
      some {
        phase := .lowered
        rootContract := 101
        currentArtifact := 1006
        parentAuthorityCeiling := 3
        activeAuthority := 3
        planVersion := 2
        readyNodes := 2
        loweredJobs := 2
        feedbackCount := 1
        replanCount := 1
        residualCount := 1
        stopConditionsPreserved := true
        pendingDispatch := false
        logicalTime := 8 } := by
  decide

theorem planning_lifecycle_denial_is_state_noninterfering
    {state : PlanningLifecycleState} {event : PlanningLifecycleEvent}
    (denied : PlanningLifecycleStep state event = none) :
    ¬ ∃ next, PlanningLifecycleStep state event = some next := by
  intro accepted
  rcases accepted with ⟨next, accepted⟩
  rw [denied] at accepted
  contradiction

theorem authority_widening_is_rejected_before_plan_admission :
    PlanningLifecycleStep initialPlanningLifecycleState
      { basePlanningLifecycleEvent with requestedAuthority := 4 } = none := by
  decide

theorem incomplete_decomposition_is_rejected_before_plan_admission :
    PlanningLifecycleStep initialPlanningLifecycleState
      { basePlanningLifecycleEvent with decompositionComplete := false } = none := by
  decide

def admittedPlanningLifecycleState : PlanningLifecycleState :=
  ApplyPlanningLifecycleEvent initialPlanningLifecycleState
    basePlanningLifecycleEvent

def readyPlanningLifecycleEvent : PlanningLifecycleEvent :=
  { basePlanningLifecycleEvent with
      kind := .markNodeReady
      fromPhase := .admitted
      toPhase := .ready
      parentArtifact := 1003
      outputArtifact := 1003
      logicalTime := 3 }

theorem missing_context_is_rejected_before_node_readiness :
    PlanningLifecycleStep admittedPlanningLifecycleState
      { readyPlanningLifecycleEvent with contextPresent := false } = none := by
  decide

theorem inadequate_selected_route_is_rejected_before_node_readiness :
    PlanningLifecycleStep admittedPlanningLifecycleState
      { readyPlanningLifecycleEvent with selectedRouteAdequate := false } = none := by
  decide

def readyPlanningLifecycleState : PlanningLifecycleState :=
  ApplyPlanningLifecycleEvent admittedPlanningLifecycleState
    readyPlanningLifecycleEvent

def lowerPlanningLifecycleEvent : PlanningLifecycleEvent :=
  { basePlanningLifecycleEvent with
      kind := .lowerJob
      fromPhase := .ready
      toPhase := .lowered
      parentArtifact := 1003
      outputArtifact := 1004
      dispatchReceipt := true
      logicalTime := 4 }

theorem missing_dispatch_receipt_is_rejected_before_job_lowering :
    PlanningLifecycleStep readyPlanningLifecycleState
      { lowerPlanningLifecycleEvent with dispatchReceipt := false } = none := by
  decide

theorem blocked_authority_path_is_rejected_before_job_lowering :
    PlanningLifecycleStep readyPlanningLifecycleState
      { lowerPlanningLifecycleEvent with blockedAuthorityPath := true } = none := by
  decide

def loweredPlanningLifecycleState : PlanningLifecycleState :=
  ApplyPlanningLifecycleEvent readyPlanningLifecycleState
    lowerPlanningLifecycleEvent

theorem feedback_before_job_lowering_is_rejected :
    PlanningLifecycleStep readyPlanningLifecycleState
      { basePlanningLifecycleEvent with
          kind := .observeFeedback
          fromPhase := .lowered
          toPhase := .feedback
          parentArtifact := 1004
          outputArtifact := 1004
          feedbackReceipt := true
          logicalTime := 5 } = none := by
  decide

def feedbackPlanningLifecycleEvent : PlanningLifecycleEvent :=
  { basePlanningLifecycleEvent with
      kind := .observeFeedback
      fromPhase := .lowered
      toPhase := .feedback
      parentArtifact := 1004
      outputArtifact := 1004
      feedbackReceipt := true
      logicalTime := 5 }

def feedbackPlanningLifecycleState : PlanningLifecycleState :=
  ApplyPlanningLifecycleEvent loweredPlanningLifecycleState
    feedbackPlanningLifecycleEvent

def replanPlanningLifecycleEvent : PlanningLifecycleEvent :=
  { basePlanningLifecycleEvent with
      kind := .applyReplan
      fromPhase := .feedback
      toPhase := .admitted
      parentArtifact := 1004
      outputArtifact := 1005
      residualDelta := 1
      logicalTime := 6 }

theorem stop_condition_erasure_is_rejected_before_replan :
    PlanningLifecycleStep feedbackPlanningLifecycleState
      { replanPlanningLifecycleEvent with
          stopConditionsPreserved := false } = none := by
  decide

theorem unscoped_repair_is_rejected_before_replan :
    PlanningLifecycleStep feedbackPlanningLifecycleState
      { replanPlanningLifecycleEvent with
          affectedSubgraphOnly := false } = none := by
  decide

theorem missing_replan_residual_is_rejected :
    PlanningLifecycleStep feedbackPlanningLifecycleState
      { replanPlanningLifecycleEvent with residualDelta := 0 } = none := by
  decide

theorem hidden_override_is_rejected_before_planning_transition :
    PlanningLifecycleStep initialPlanningLifecycleState
      { basePlanningLifecycleEvent with hiddenOverrideApplied := true } = none := by
  decide

def ProjectPlanningPhaseToVerticalLayer :
    PlanningLifecyclePhase →
      AsiStackProofs.IntentExecutionRefinement.VerticalLayer
  | .command => .command
  | .admitted => .plan
  | .ready => .plan
  | .lowered => .job
  | .feedback => .plan
  | .blocked => .blocked

def ProjectPlanningStateToVertical
    (state : PlanningLifecycleState) :
    AsiStackProofs.IntentExecutionRefinement.VerticalState where
  layer := ProjectPlanningPhaseToVerticalLayer state.phase
  rootContract := state.rootContract
  currentArtifact := state.currentArtifact
  authorityCeiling := state.parentAuthorityCeiling
  activeAuthority := state.activeAuthority
  requiredApproval := false
  approvalPresent := false
  dispatchReceipt := false
  attemptedEffects := 0
  observedEffects := 0
  artifactBound := false
  verificationComplete := false
  delivered := false
  openResiduals := state.residualCount
  stopped := state.phase = .blocked
  logicalTime := state.logicalTime

def ProjectPlanningEventToVertical
    (event : PlanningLifecycleEvent) :
    AsiStackProofs.IntentExecutionRefinement.VerticalEvent where
  kind := if event.kind = .admitPlan then .lowerPlan else .lowerJob
  fromLayer := ProjectPlanningPhaseToVerticalLayer event.fromPhase
  toLayer := ProjectPlanningPhaseToVerticalLayer event.toPhase
  rootContract := event.rootContract
  parentArtifact := event.parentArtifact
  outputArtifact := event.outputArtifact
  requestedAuthority := event.requestedAuthority
  approvalReceipt := false
  dispatchReceipt := false
  hiddenOverrideApplied := event.hiddenOverrideApplied
  effectDelta := 0
  observationDelta := 0
  observationReceipt := false
  artifactParentBound := false
  independentVerifier := false
  verificationReceipt := false
  deliveryReceipt := false
  blockReceipt := false
  residualDelta := event.residualDelta
  rollbackExact := false
  logicalTime := event.logicalTime

theorem admitted_plan_event_refines_vertical_lower_plan
    {state : PlanningLifecycleState} {event : PlanningLifecycleEvent}
    (kind : event.kind = .admitPlan)
    (admissible : PlanningLifecycleEventAdmissible state event) :
    AsiStackProofs.IntentExecutionRefinement.VerticalEventValid
      (ProjectPlanningStateToVertical state)
      (ProjectPlanningEventToVertical event) := by
  rcases admissible with
    ⟨phase, root, artifact, time, authority, _stops, hidden, specific⟩
  simp [PlanningLifecycleEventSpecificValid, kind] at specific
  have phasePair :
      event.fromPhase = .command ∧ event.toPhase = .admitted :=
    specific.1.1.1.1.1.1.1
  simp [AsiStackProofs.IntentExecutionRefinement.VerticalEventValid,
    AsiStackProofs.IntentExecutionRefinement.EventSpecificValid,
    ProjectPlanningStateToVertical, ProjectPlanningEventToVertical,
    ProjectPlanningPhaseToVerticalLayer, kind, phase, root, artifact, time,
    authority, hidden, phasePair.1, phasePair.2]

theorem lowered_job_event_refines_vertical_lower_job
    {state : PlanningLifecycleState} {event : PlanningLifecycleEvent}
    (kind : event.kind = .lowerJob)
    (admissible : PlanningLifecycleEventAdmissible state event) :
    AsiStackProofs.IntentExecutionRefinement.VerticalEventValid
      (ProjectPlanningStateToVertical state)
      (ProjectPlanningEventToVertical event) := by
  rcases admissible with
    ⟨phase, root, artifact, time, authority, _stops, hidden, specific⟩
  simp [PlanningLifecycleEventSpecificValid, kind] at specific
  have phasePair :
      event.fromPhase = .ready ∧ event.toPhase = .lowered :=
    specific.1.1.1.1
  simp [AsiStackProofs.IntentExecutionRefinement.VerticalEventValid,
    AsiStackProofs.IntentExecutionRefinement.EventSpecificValid,
    ProjectPlanningStateToVertical, ProjectPlanningEventToVertical,
    ProjectPlanningPhaseToVerticalLayer, kind, phase, root, artifact, time,
    authority, hidden, phasePair.1, phasePair.2]

end AsiStackProofs.Planning
