namespace AsiStackProofs.FailureModes

structure ComponentRecord where
  requiredInvariantHolds : Bool
  authorityBounded : Bool
deriving DecidableEq, Repr

def PromotionAllowed (component : ComponentRecord) : Prop :=
  component.requiredInvariantHolds = true ∧
    component.authorityBounded = true

def GovernanceFailure (component : ComponentRecord) : Prop :=
  component.requiredInvariantHolds = false ∨
    component.authorityBounded = false

theorem failed_required_invariant_blocks_promotion
    {component : ComponentRecord} :
    component.requiredInvariantHolds = false ->
    ¬ PromotionAllowed component := by
  intro failed promoted
  unfold PromotionAllowed at promoted
  rw [failed] at promoted
  cases promoted.1

theorem unbounded_authority_detected_as_governance_failure
    {component : ComponentRecord} :
    component.authorityBounded = false ->
    GovernanceFailure component := by
  intro unbounded
  exact Or.inr unbounded

end AsiStackProofs.FailureModes
