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

inductive FailureIncidentRoute where
  | ordinaryOperation
  | escalateAuthorityReview
  | quarantineContext
  | freezeEvaluator
  | blockClaimPromotion
deriving DecidableEq, Repr

structure FailureIncidentRecord where
  authorityOverCeiling : Bool
  contextTainted : Bool
  contextAuthorityGrantPresent : Bool
  evaluatorModifiedBySubject : Bool
  claimPromotionRequested : Bool
  verificationPassed : Bool
deriving DecidableEq, Repr

def FailureIncidentRouteFor (incident : FailureIncidentRecord) : FailureIncidentRoute :=
  if incident.authorityOverCeiling = true then
    FailureIncidentRoute.escalateAuthorityReview
  else if incident.contextTainted = true ∧ incident.contextAuthorityGrantPresent = false then
    FailureIncidentRoute.quarantineContext
  else if incident.evaluatorModifiedBySubject = true then
    FailureIncidentRoute.freezeEvaluator
  else if incident.claimPromotionRequested = true ∧ incident.verificationPassed = false then
    FailureIncidentRoute.blockClaimPromotion
  else
    FailureIncidentRoute.ordinaryOperation

theorem authority_over_ceiling_routes_to_review
    {incident : FailureIncidentRecord} :
    incident.authorityOverCeiling = true ->
    FailureIncidentRouteFor incident = FailureIncidentRoute.escalateAuthorityReview := by
  intro overCeiling
  unfold FailureIncidentRouteFor
  simp [overCeiling]

theorem tainted_context_without_authority_grant_quarantines
    {incident : FailureIncidentRecord} :
    incident.authorityOverCeiling = false ->
    incident.contextTainted = true ->
    incident.contextAuthorityGrantPresent = false ->
    FailureIncidentRouteFor incident = FailureIncidentRoute.quarantineContext := by
  intro withinCeiling tainted noGrant
  unfold FailureIncidentRouteFor
  simp [withinCeiling, tainted, noGrant]

theorem subject_modified_evaluator_freezes_review
    {incident : FailureIncidentRecord} :
    incident.authorityOverCeiling = false ->
    incident.contextTainted = false ->
    incident.evaluatorModifiedBySubject = true ->
    FailureIncidentRouteFor incident = FailureIncidentRoute.freezeEvaluator := by
  intro withinCeiling cleanContext evaluatorModified
  unfold FailureIncidentRouteFor
  simp [withinCeiling, cleanContext, evaluatorModified]

theorem unverified_claim_promotion_blocks
    {incident : FailureIncidentRecord} :
    incident.authorityOverCeiling = false ->
    incident.contextTainted = false ->
    incident.evaluatorModifiedBySubject = false ->
    incident.claimPromotionRequested = true ->
    incident.verificationPassed = false ->
    FailureIncidentRouteFor incident = FailureIncidentRoute.blockClaimPromotion := by
  intro withinCeiling cleanContext evaluatorStable promotionRequested verificationFailed
  unfold FailureIncidentRouteFor
  simp [withinCeiling, cleanContext, evaluatorStable, promotionRequested, verificationFailed]

end AsiStackProofs.FailureModes
