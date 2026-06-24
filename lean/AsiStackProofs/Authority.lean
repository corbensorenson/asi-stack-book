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

end AsiStackProofs.Authority
