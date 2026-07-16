namespace AsiStackProofs.Corrigibility

inductive AgencyActionRoute where
  | allowed
  | blockedForReview
deriving DecidableEq, Repr

structure AgencyActionDecision where
  highImpactAction : Bool
  usableReviewPath : Bool
  currentApproval : Bool
  route : AgencyActionRoute
deriving DecidableEq, Repr

def AgencyActionCorrigible (decision : AgencyActionDecision) : Prop :=
  if decision.highImpactAction &&
      (!decision.usableReviewPath || !decision.currentApproval) then
    decision.route = AgencyActionRoute.blockedForReview
  else
    True

theorem high_impact_action_without_usable_review_routes_to_review
    {decision : AgencyActionDecision} :
    AgencyActionCorrigible decision ->
    decision.highImpactAction = true ->
    decision.usableReviewPath = false ->
    decision.route = AgencyActionRoute.blockedForReview := by
  intro safe highImpact missingReview
  unfold AgencyActionCorrigible at safe
  rw [highImpact, missingReview] at safe
  simp at safe
  exact safe

inductive AgencyControlPhase where
  | proposed
  | preEffectReview
  | delegated
  | denied
  | active
  | residualized
deriving DecidableEq, Repr

inductive AgencyControlRoute where
  | allow
  | blockForReview
  | narrowDelegation
  | preserveAuditResidual
deriving DecidableEq, Repr

structure AgencyControlDecision where
  phase : AgencyControlPhase
  highImpactAction : Bool
  affectedPartyNotified : Bool
  delegationBounded : Bool
  reviewBeforeEffect : Bool
  appealAvailable : Bool
  interruptAvailable : Bool
  rollbackAvailable : Bool
  actionDenied : Bool
  accountablePrincipalRecorded : Bool
  route : AgencyControlRoute
deriving DecidableEq, Repr

def AgencyControlRequiresReview (decision : AgencyControlDecision) : Bool :=
  decision.highImpactAction &&
    (!decision.reviewBeforeEffect ||
      !decision.appealAvailable ||
      !decision.interruptAvailable)

def AgencyControlSafe (decision : AgencyControlDecision) : Prop :=
  if AgencyControlRequiresReview decision then
    decision.route = AgencyControlRoute.blockForReview
  else if !decision.delegationBounded then
    decision.route = AgencyControlRoute.narrowDelegation
  else if decision.actionDenied && !decision.accountablePrincipalRecorded then
    decision.route = AgencyControlRoute.preserveAuditResidual
  else
    True

def unsafeAgencyControlWithoutPreEffectReview :
    AgencyControlDecision :=
  { phase := AgencyControlPhase.preEffectReview,
    highImpactAction := true,
    affectedPartyNotified := true,
    delegationBounded := true,
    reviewBeforeEffect := false,
    appealAvailable := true,
    interruptAvailable := true,
    rollbackAvailable := true,
    actionDenied := false,
    accountablePrincipalRecorded := true,
    route := AgencyControlRoute.blockForReview }

def unboundedDelegationNarrowed :
    AgencyControlDecision :=
  { phase := AgencyControlPhase.delegated,
    highImpactAction := false,
    affectedPartyNotified := true,
    delegationBounded := false,
    reviewBeforeEffect := true,
    appealAvailable := true,
    interruptAvailable := true,
    rollbackAvailable := true,
    actionDenied := false,
    accountablePrincipalRecorded := true,
    route := AgencyControlRoute.narrowDelegation }

def deniedActionWithoutAccountabilityResidualized :
    AgencyControlDecision :=
  { phase := AgencyControlPhase.denied,
    highImpactAction := false,
    affectedPartyNotified := true,
    delegationBounded := true,
    reviewBeforeEffect := true,
    appealAvailable := true,
    interruptAvailable := true,
    rollbackAvailable := true,
    actionDenied := true,
    accountablePrincipalRecorded := false,
    route := AgencyControlRoute.preserveAuditResidual }

theorem high_impact_action_without_pre_effect_review_blocks
    {decision : AgencyControlDecision} :
    AgencyControlSafe decision ->
    decision.highImpactAction = true ->
    decision.reviewBeforeEffect = false ->
    decision.route = AgencyControlRoute.blockForReview := by
  intro safe highImpact missingReview
  unfold AgencyControlSafe AgencyControlRequiresReview at safe
  rw [highImpact, missingReview] at safe
  simp at safe
  exact safe

theorem low_risk_unbounded_delegation_routes_to_narrowing
    {decision : AgencyControlDecision} :
    AgencyControlSafe decision ->
    decision.highImpactAction = false ->
    decision.delegationBounded = false ->
    decision.route = AgencyControlRoute.narrowDelegation := by
  intro safe lowRisk unbounded
  unfold AgencyControlSafe AgencyControlRequiresReview at safe
  rw [lowRisk, unbounded] at safe
  simp at safe
  exact safe

theorem denied_action_without_accountable_principal_preserves_audit
    {decision : AgencyControlDecision} :
    AgencyControlSafe decision ->
    decision.highImpactAction = false ->
    decision.delegationBounded = true ->
    decision.actionDenied = true ->
    decision.accountablePrincipalRecorded = false ->
    decision.route = AgencyControlRoute.preserveAuditResidual := by
  intro safe lowRisk bounded denied missingPrincipal
  unfold AgencyControlSafe AgencyControlRequiresReview at safe
  rw [lowRisk, bounded, denied, missingPrincipal] at safe
  simp at safe
  exact safe

end AsiStackProofs.Corrigibility
