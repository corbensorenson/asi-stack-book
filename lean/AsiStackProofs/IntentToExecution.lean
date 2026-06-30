namespace AsiStackProofs.IntentToExecution

structure ExecutionCompilationReview where
  parentConstraintsDeclared : Bool
  compiledJobPreservesConstraints : Bool
deriving DecidableEq, Repr

def ParentConstraintsPreserved (review : ExecutionCompilationReview) : Prop :=
  review.parentConstraintsDeclared = true ->
    review.compiledJobPreservesConstraints = true

theorem compiled_execution_job_preserves_parent_contract_constraints
    {review : ExecutionCompilationReview} :
    ParentConstraintsPreserved review ->
    review.parentConstraintsDeclared = true ->
    review.compiledJobPreservesConstraints = true := by
  intro valid declared
  exact valid declared

structure ExecutionApprovalReview where
  requiredApproval : Bool
  requiredApprovalPresent : Bool
  transitionsToRunning : Bool
deriving DecidableEq, Repr

def MissingApprovalBlocksRunning (review : ExecutionApprovalReview) : Prop :=
  review.requiredApproval = true ->
    review.requiredApprovalPresent = false ->
      review.transitionsToRunning = false

theorem execution_job_without_required_approval_cannot_transition_to_running
    {review : ExecutionApprovalReview} :
    MissingApprovalBlocksRunning review ->
    review.requiredApproval = true ->
    review.requiredApprovalPresent = false ->
    review.transitionsToRunning = false := by
  intro valid required missing
  exact valid required missing

inductive ExecutionDispatchRoute where
  | rejectContract
  | requestClarification
  | requireApproval
  | blockDispatch
  | routeToVerification
  | recordResidual
  | dispatchReady
deriving DecidableEq, Repr

structure ExecutionDispatchReview where
  contractPresent : Bool
  objectivePresent : Bool
  constraintsPresent : Bool
  authoritySpecified : Bool
  authorityWithinParent : Bool
  requiredApproval : Bool
  approvalPresent : Bool
  hiddenOverrideDetected : Bool
  artifactsDeclared : Bool
  verificationPlanPresent : Bool
  failureBehaviorPresent : Bool
  residualKnown : Bool
  dispatchRequested : Bool
deriving DecidableEq, Repr

def ExecutionDispatchRouteFor
    (review : ExecutionDispatchReview) : ExecutionDispatchRoute :=
  if review.contractPresent = false then
    ExecutionDispatchRoute.rejectContract
  else if review.objectivePresent = false then
    ExecutionDispatchRoute.requestClarification
  else if review.constraintsPresent = false then
    ExecutionDispatchRoute.requestClarification
  else if review.authoritySpecified = false then
    ExecutionDispatchRoute.requestClarification
  else if review.failureBehaviorPresent = false then
    ExecutionDispatchRoute.requestClarification
  else if review.authorityWithinParent = false then
    ExecutionDispatchRoute.blockDispatch
  else if review.hiddenOverrideDetected = true then
    ExecutionDispatchRoute.blockDispatch
  else if review.requiredApproval = true ∧ review.approvalPresent = false then
    ExecutionDispatchRoute.requireApproval
  else if review.artifactsDeclared = false then
    ExecutionDispatchRoute.requestClarification
  else if review.verificationPlanPresent = false then
    ExecutionDispatchRoute.routeToVerification
  else if review.residualKnown = true then
    ExecutionDispatchRoute.recordResidual
  else if review.dispatchRequested = true then
    ExecutionDispatchRoute.dispatchReady
  else
    ExecutionDispatchRoute.requestClarification

theorem missing_contract_rejects_execution_dispatch
    {review : ExecutionDispatchReview} :
    review.contractPresent = false ->
    ExecutionDispatchRouteFor review =
      ExecutionDispatchRoute.rejectContract := by
  intro missingContract
  unfold ExecutionDispatchRouteFor
  simp [missingContract]

theorem missing_objective_requests_execution_clarification
    {review : ExecutionDispatchReview} :
    review.contractPresent = true ->
    review.objectivePresent = false ->
    ExecutionDispatchRouteFor review =
      ExecutionDispatchRoute.requestClarification := by
  intro contractPresent missingObjective
  unfold ExecutionDispatchRouteFor
  simp [contractPresent, missingObjective]

theorem authority_widening_blocks_execution_dispatch
    {review : ExecutionDispatchReview} :
    review.contractPresent = true ->
    review.objectivePresent = true ->
    review.constraintsPresent = true ->
    review.authoritySpecified = true ->
    review.failureBehaviorPresent = true ->
    review.authorityWithinParent = false ->
    ExecutionDispatchRouteFor review =
      ExecutionDispatchRoute.blockDispatch := by
  intro contractPresent objectivePresent constraintsPresent authoritySpecified
    failureBehavior authorityWidening
  unfold ExecutionDispatchRouteFor
  simp [contractPresent, objectivePresent, constraintsPresent,
    authoritySpecified, failureBehavior, authorityWidening]

theorem hidden_override_blocks_execution_dispatch
    {review : ExecutionDispatchReview} :
    review.contractPresent = true ->
    review.objectivePresent = true ->
    review.constraintsPresent = true ->
    review.authoritySpecified = true ->
    review.failureBehaviorPresent = true ->
    review.authorityWithinParent = true ->
    review.hiddenOverrideDetected = true ->
    ExecutionDispatchRouteFor review =
      ExecutionDispatchRoute.blockDispatch := by
  intro contractPresent objectivePresent constraintsPresent authoritySpecified
    failureBehavior authorityWithin hiddenOverride
  unfold ExecutionDispatchRouteFor
  simp [contractPresent, objectivePresent, constraintsPresent,
    authoritySpecified, failureBehavior, authorityWithin, hiddenOverride]

theorem required_approval_missing_routes_to_approval
    {review : ExecutionDispatchReview} :
    review.contractPresent = true ->
    review.objectivePresent = true ->
    review.constraintsPresent = true ->
    review.authoritySpecified = true ->
    review.failureBehaviorPresent = true ->
    review.authorityWithinParent = true ->
    review.hiddenOverrideDetected = false ->
    review.requiredApproval = true ->
    review.approvalPresent = false ->
    ExecutionDispatchRouteFor review =
      ExecutionDispatchRoute.requireApproval := by
  intro contractPresent objectivePresent constraintsPresent authoritySpecified
    failureBehavior authorityWithin noHiddenOverride approvalRequired
    missingApproval
  unfold ExecutionDispatchRouteFor
  simp [contractPresent, objectivePresent, constraintsPresent,
    authoritySpecified, failureBehavior, authorityWithin, noHiddenOverride,
    approvalRequired, missingApproval]

theorem missing_artifacts_request_execution_clarification
    {review : ExecutionDispatchReview} :
    review.contractPresent = true ->
    review.objectivePresent = true ->
    review.constraintsPresent = true ->
    review.authoritySpecified = true ->
    review.failureBehaviorPresent = true ->
    review.authorityWithinParent = true ->
    review.hiddenOverrideDetected = false ->
    review.requiredApproval = false ->
    review.artifactsDeclared = false ->
    ExecutionDispatchRouteFor review =
      ExecutionDispatchRoute.requestClarification := by
  intro contractPresent objectivePresent constraintsPresent authoritySpecified
    failureBehavior authorityWithin noHiddenOverride approvalNotRequired
    missingArtifacts
  unfold ExecutionDispatchRouteFor
  simp [contractPresent, objectivePresent, constraintsPresent,
    authoritySpecified, failureBehavior, authorityWithin, noHiddenOverride,
    approvalNotRequired, missingArtifacts]

theorem missing_verification_plan_routes_to_verification
    {review : ExecutionDispatchReview} :
    review.contractPresent = true ->
    review.objectivePresent = true ->
    review.constraintsPresent = true ->
    review.authoritySpecified = true ->
    review.failureBehaviorPresent = true ->
    review.authorityWithinParent = true ->
    review.hiddenOverrideDetected = false ->
    review.requiredApproval = false ->
    review.artifactsDeclared = true ->
    review.verificationPlanPresent = false ->
    ExecutionDispatchRouteFor review =
      ExecutionDispatchRoute.routeToVerification := by
  intro contractPresent objectivePresent constraintsPresent authoritySpecified
    failureBehavior authorityWithin noHiddenOverride approvalNotRequired
    artifactsDeclared missingVerification
  unfold ExecutionDispatchRouteFor
  simp [contractPresent, objectivePresent, constraintsPresent,
    authoritySpecified, failureBehavior, authorityWithin, noHiddenOverride,
    approvalNotRequired, artifactsDeclared, missingVerification]

theorem known_residual_records_execution_residual
    {review : ExecutionDispatchReview} :
    review.contractPresent = true ->
    review.objectivePresent = true ->
    review.constraintsPresent = true ->
    review.authoritySpecified = true ->
    review.failureBehaviorPresent = true ->
    review.authorityWithinParent = true ->
    review.hiddenOverrideDetected = false ->
    review.requiredApproval = false ->
    review.artifactsDeclared = true ->
    review.verificationPlanPresent = true ->
    review.residualKnown = true ->
    ExecutionDispatchRouteFor review =
      ExecutionDispatchRoute.recordResidual := by
  intro contractPresent objectivePresent constraintsPresent authoritySpecified
    failureBehavior authorityWithin noHiddenOverride approvalNotRequired
    artifactsDeclared verificationPlan residualKnown
  unfold ExecutionDispatchRouteFor
  simp [contractPresent, objectivePresent, constraintsPresent,
    authoritySpecified, failureBehavior, authorityWithin, noHiddenOverride,
    approvalNotRequired, artifactsDeclared, verificationPlan, residualKnown]

theorem complete_dispatch_review_is_ready
    {review : ExecutionDispatchReview} :
    review.contractPresent = true ->
    review.objectivePresent = true ->
    review.constraintsPresent = true ->
    review.authoritySpecified = true ->
    review.failureBehaviorPresent = true ->
    review.authorityWithinParent = true ->
    review.hiddenOverrideDetected = false ->
    review.requiredApproval = false ->
    review.artifactsDeclared = true ->
    review.verificationPlanPresent = true ->
    review.residualKnown = false ->
    review.dispatchRequested = true ->
    ExecutionDispatchRouteFor review =
      ExecutionDispatchRoute.dispatchReady := by
  intro contractPresent objectivePresent constraintsPresent authoritySpecified
    failureBehavior authorityWithin noHiddenOverride approvalNotRequired
    artifactsDeclared verificationPlan noResidual dispatchRequested
  unfold ExecutionDispatchRouteFor
  simp [contractPresent, objectivePresent, constraintsPresent,
    authoritySpecified, failureBehavior, authorityWithin, noHiddenOverride,
    approvalNotRequired, artifactsDeclared, verificationPlan, noResidual,
    dispatchRequested]

end AsiStackProofs.IntentToExecution
