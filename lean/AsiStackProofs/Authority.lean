namespace AsiStackProofs.Authority

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

structure GovernanceGrant where
  active : Bool
  scopeMatches : Bool
  maxCeiling : AuthorityLevel
deriving DecidableEq, Repr

def GrantAuthorizesLevel (grant : GovernanceGrant) (level : AuthorityLevel) : Prop :=
  grant.active = true ∧
    grant.scopeMatches = true ∧
    level.rank <= grant.maxCeiling.rank

structure AuthorityTransition where
  before : AuthorityLevel
  after : AuthorityLevel
  grant : Option GovernanceGrant
deriving DecidableEq, Repr

def ValidAuthorityTransition (transition : AuthorityTransition) : Prop :=
  transition.after.rank <= transition.before.rank ∨
    ∃ grant, transition.grant = some grant ∧ GrantAuthorizesLevel grant transition.after

theorem valid_transition_without_grant_preserves_ceiling
    {transition : AuthorityTransition} :
    ValidAuthorityTransition transition ->
    transition.grant = none ->
    transition.after.rank <= transition.before.rank := by
  intro valid noGrant
  cases valid with
  | inl preserved =>
      exact preserved
  | inr granted =>
      rcases granted with ⟨grant, grantPresent, _authorizes⟩
      rw [noGrant] at grantPresent
      contradiction

structure ExecutionRequest where
  activeCeiling : AuthorityLevel
  required : AuthorityLevel
  grant : Option GovernanceGrant
deriving DecidableEq, Repr

def ExecutionAuthorized (request : ExecutionRequest) : Prop :=
  request.required.rank <= request.activeCeiling.rank ∨
    ∃ grant, request.grant = some grant ∧ GrantAuthorizesLevel grant request.required

theorem missing_grant_blocks_over_ceiling_execution
    {request : ExecutionRequest} :
    request.activeCeiling.rank < request.required.rank ->
    request.grant = none ->
    ¬ ExecutionAuthorized request := by
  intro exceeds noGrant authorized
  cases authorized with
  | inl withinCeiling =>
      exact Nat.not_le_of_gt exceeds withinCeiling
  | inr granted =>
      rcases granted with ⟨grant, grantPresent, _authorizes⟩
      rw [noGrant] at grantPresent
      contradiction

inductive AuthorityDecision where
  | allow
  | deny
  | escalate
deriving DecidableEq, Repr

structure AuthorityDecisionRecord where
  callerCeiling : AuthorityLevel
  activeCeiling : AuthorityLevel
  targetRequired : AuthorityLevel
  decision : AuthorityDecision
  effectReceiptPresent : Bool
  denialReasonPresent : Bool
  auditRefsPresent : Bool
  nonClaimsPresent : Bool
  reviewRoutePresent : Bool
  grantExpired : Bool
  grantRevoked : Bool
deriving DecidableEq, Repr

def CommonAuthorityRecordValid (record : AuthorityDecisionRecord) : Prop :=
  record.auditRefsPresent = true ∧
    record.nonClaimsPresent = true

def AuthorityDecisionValid (record : AuthorityDecisionRecord) : Prop :=
  CommonAuthorityRecordValid record ∧
    match record.decision with
    | .allow =>
        record.effectReceiptPresent = true ∧
          record.denialReasonPresent = false ∧
          record.grantExpired = false ∧
          record.grantRevoked = false ∧
          record.activeCeiling.rank <= record.callerCeiling.rank ∧
          record.targetRequired.rank <= record.activeCeiling.rank
    | .deny =>
        record.effectReceiptPresent = false ∧
          record.denialReasonPresent = true
    | .escalate =>
        record.effectReceiptPresent = false ∧
          record.denialReasonPresent = true ∧
          record.reviewRoutePresent = true

theorem valid_authority_decision_has_audit_and_nonclaims
    {record : AuthorityDecisionRecord} :
    AuthorityDecisionValid record ->
    record.auditRefsPresent = true ∧ record.nonClaimsPresent = true := by
  intro valid
  exact valid.1

theorem valid_allow_decision_has_effect_receipt
    {record : AuthorityDecisionRecord} :
    AuthorityDecisionValid record ->
    record.decision = AuthorityDecision.allow ->
    record.effectReceiptPresent = true := by
  intro valid isAllow
  unfold AuthorityDecisionValid at valid
  rcases valid with ⟨_common, decisionValid⟩
  rw [isAllow] at decisionValid
  exact decisionValid.1

theorem valid_allow_decision_preserves_caller_ceiling
    {record : AuthorityDecisionRecord} :
    AuthorityDecisionValid record ->
    record.decision = AuthorityDecision.allow ->
    record.activeCeiling.rank <= record.callerCeiling.rank := by
  intro valid isAllow
  unfold AuthorityDecisionValid at valid
  rcases valid with ⟨_common, decisionValid⟩
  rw [isAllow] at decisionValid
  exact decisionValid.2.2.2.2.1

theorem valid_allow_decision_target_within_active_ceiling
    {record : AuthorityDecisionRecord} :
    AuthorityDecisionValid record ->
    record.decision = AuthorityDecision.allow ->
    record.targetRequired.rank <= record.activeCeiling.rank := by
  intro valid isAllow
  unfold AuthorityDecisionValid at valid
  rcases valid with ⟨_common, decisionValid⟩
  rw [isAllow] at decisionValid
  exact decisionValid.2.2.2.2.2

theorem valid_deny_decision_has_no_effect_receipt
    {record : AuthorityDecisionRecord} :
    AuthorityDecisionValid record ->
    record.decision = AuthorityDecision.deny ->
    record.effectReceiptPresent = false := by
  intro valid isDeny
  unfold AuthorityDecisionValid at valid
  rcases valid with ⟨_common, decisionValid⟩
  rw [isDeny] at decisionValid
  exact decisionValid.1

theorem valid_escalation_routes_to_review
    {record : AuthorityDecisionRecord} :
    AuthorityDecisionValid record ->
    record.decision = AuthorityDecision.escalate ->
    record.reviewRoutePresent = true := by
  intro valid isEscalate
  unfold AuthorityDecisionValid at valid
  rcases valid with ⟨_common, decisionValid⟩
  rw [isEscalate] at decisionValid
  exact decisionValid.2.2

end AsiStackProofs.Authority
