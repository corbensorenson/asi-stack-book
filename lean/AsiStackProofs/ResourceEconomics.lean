namespace AsiStackProofs.ResourceEconomics

structure BudgetGateReview where
  requiredSafetyGate : Bool
  requiredVerificationGate : Bool
  safetyGateDisabled : Bool
  verificationGateDisabled : Bool
deriving DecidableEq, Repr

def RequiredGatesPreserved (review : BudgetGateReview) : Prop :=
  (review.requiredSafetyGate = true -> review.safetyGateDisabled = false) ∧
    (review.requiredVerificationGate = true -> review.verificationGateDisabled = false)

theorem task_budget_cannot_disable_required_safety_or_verification_gates
    {review : BudgetGateReview} :
    RequiredGatesPreserved review ->
    review.requiredSafetyGate = true ->
    review.requiredVerificationGate = true ->
    review.safetyGateDisabled = false ∧ review.verificationGateDisabled = false := by
  intro preserved safetyRequired verificationRequired
  exact ⟨preserved.1 safetyRequired, preserved.2 verificationRequired⟩

inductive RiskClass where
  | low
  | medium
  | high
  | critical
deriving DecidableEq, Repr

def HighRisk : RiskClass -> Prop
  | .high => True
  | .critical => True
  | _ => False

inductive BudgetDecision where
  | dispatch
  | escalate
  | defer
  | shrinkScope
  | reject
  | residual
deriving DecidableEq, Repr

def BlockedOrEscalated : BudgetDecision -> Prop
  | .escalate => True
  | .defer => True
  | .shrinkScope => True
  | .reject => True
  | .residual => True
  | .dispatch => False

structure VerificationBudgetReview where
  riskClass : RiskClass
  verificationBudgetSufficient : Bool
  decision : BudgetDecision
deriving DecidableEq, Repr

def HighRiskVerificationBudgetValid (review : VerificationBudgetReview) : Prop :=
  HighRisk review.riskClass ->
    review.verificationBudgetSufficient = false ->
      BlockedOrEscalated review.decision

theorem high_risk_task_with_insufficient_verification_budget_is_not_dispatched
    {review : VerificationBudgetReview} :
    HighRiskVerificationBudgetValid review ->
    HighRisk review.riskClass ->
    review.verificationBudgetSufficient = false ->
    BlockedOrEscalated review.decision := by
  intro valid highRisk insufficient
  exact valid highRisk insufficient

end AsiStackProofs.ResourceEconomics
