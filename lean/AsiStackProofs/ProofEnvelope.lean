namespace AsiStackProofs.ProofEnvelope

inductive ProofTargetStatus where
  | planned
  | scaffolded
  | implemented
  | blocked
  | retired
deriving DecidableEq, Repr

structure ProofTargetReview where
  status : ProofTargetStatus
  moduleExists : Bool
  buildPassed : Bool
  operationalClaim : Bool
deriving DecidableEq, Repr

def ImplementedTargetValid (target : ProofTargetReview) : Prop :=
  target.status = ProofTargetStatus.implemented ->
    target.moduleExists = true ∧ target.buildPassed = true

theorem implemented_target_has_module_and_passing_build
    {target : ProofTargetReview} :
    ImplementedTargetValid target ->
    target.status = ProofTargetStatus.implemented ->
      target.moduleExists = true ∧ target.buildPassed = true := by
  intro valid implemented
  exact valid implemented

def NonOperationalTargetRouted (target : ProofTargetReview) : Prop :=
  target.operationalClaim = false ->
    target.status = ProofTargetStatus.planned ∨
      target.status = ProofTargetStatus.blocked

theorem non_operational_target_remains_planned_or_blocked
    {target : ProofTargetReview} :
    NonOperationalTargetRouted target ->
    target.operationalClaim = false ->
      target.status = ProofTargetStatus.planned ∨
        target.status = ProofTargetStatus.blocked := by
  intro routed nonOperational
  exact routed nonOperational

theorem non_operational_target_not_implemented
    {target : ProofTargetReview} :
    NonOperationalTargetRouted target ->
    target.operationalClaim = false ->
    target.status ≠ ProofTargetStatus.implemented := by
  intro routed nonOperational implemented
  have routedStatus := routed nonOperational
  cases routedStatus with
  | inl planned =>
      rw [planned] at implemented
      contradiction
  | inr blocked =>
      rw [blocked] at implemented
      contradiction

end AsiStackProofs.ProofEnvelope
