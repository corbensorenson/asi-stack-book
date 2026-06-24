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

end AsiStackProofs.IntentToExecution
