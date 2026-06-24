namespace AsiStackProofs.TypedJobs

inductive JobState where
  | draft
  | locked
  | awaitingApproval
  | dispatchable
  | running
  | adjudicating
  | delivered
  | failed
  | blocked
  | replayed
  | retired
deriving DecidableEq, Repr

structure JobTransition where
  fromState : JobState
  toState : JobState
deriving DecidableEq, Repr

def ValidTransition : JobTransition -> Prop
  | { fromState := .draft, toState := .locked } => True
  | { fromState := .locked, toState := .awaitingApproval } => True
  | { fromState := .locked, toState := .dispatchable } => True
  | { fromState := .awaitingApproval, toState := .dispatchable } => True
  | { fromState := .awaitingApproval, toState := .blocked } => True
  | { fromState := .dispatchable, toState := .running } => True
  | { fromState := .running, toState := .adjudicating } => True
  | { fromState := .running, toState := .failed } => True
  | { fromState := .running, toState := .blocked } => True
  | { fromState := .adjudicating, toState := .delivered } => True
  | { fromState := .delivered, toState := .replayed } => True
  | { fromState := .delivered, toState := .retired } => True
  | { fromState := .failed, toState := .retired } => True
  | { fromState := .blocked, toState := .retired } => True
  | { fromState := .replayed, toState := .retired } => True
  | _ => False

structure TransitionRecord where
  transition : JobTransition
  recordedAsValid : Bool
deriving DecidableEq, Repr

def TransitionRecordValid (record : TransitionRecord) : Prop :=
  record.recordedAsValid = true -> ValidTransition record.transition

theorem recorded_valid_job_transition_uses_declared_lifecycle_relation
    {record : TransitionRecord} :
    TransitionRecordValid record ->
    record.recordedAsValid = true ->
    ValidTransition record.transition := by
  intro valid markedValid
  exact valid markedValid

structure ApprovalRecord where
  approvalRequired : Bool
  approvalRecorded : Bool
  targetState : JobState
deriving DecidableEq, Repr

def ExecutionAllowed (record : ApprovalRecord) : Prop :=
  record.targetState = JobState.running ∧
    (record.approvalRequired = false ∨ record.approvalRecorded = true)

theorem job_requiring_approval_cannot_run_without_approval
    {record : ApprovalRecord} :
    record.approvalRequired = true ->
    record.approvalRecorded = false ->
    ¬ ExecutionAllowed record := by
  intro required missing allowed
  unfold ExecutionAllowed at allowed
  cases allowed.2 with
  | inl notRequired =>
      rw [required] at notRequired
      cases notRequired
  | inr approved =>
      rw [missing] at approved
      cases approved

end AsiStackProofs.TypedJobs
