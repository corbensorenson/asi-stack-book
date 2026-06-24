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

end AsiStackProofs.Planning
