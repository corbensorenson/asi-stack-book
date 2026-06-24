namespace AsiStackProofs.StableCapabilityFields

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

structure StableCapabilityField where
  authorityCeiling : AuthorityLevel
deriving DecidableEq, Repr

structure ImplementationCandidate where
  satisfiesQualification : Bool
  requestedAuthority : AuthorityLevel
  governanceGrant : Bool
deriving DecidableEq, Repr

def ReplacementAllowed (field : StableCapabilityField) (candidate : ImplementationCandidate) : Prop :=
  candidate.satisfiesQualification = true ∧
    (candidate.requestedAuthority.rank <= field.authorityCeiling.rank ∨
      candidate.governanceGrant = true)

theorem replacement_requires_field_qualification
    {field : StableCapabilityField} {candidate : ImplementationCandidate} :
    ReplacementAllowed field candidate ->
    candidate.satisfiesQualification = true := by
  intro allowed
  exact allowed.1

theorem authority_expanding_replacement_without_grant_rejected
    {field : StableCapabilityField} {candidate : ImplementationCandidate} :
    field.authorityCeiling.rank < candidate.requestedAuthority.rank ->
    candidate.governanceGrant = false ->
    ¬ ReplacementAllowed field candidate := by
  intro expands noGrant allowed
  unfold ReplacementAllowed at allowed
  cases allowed.2 with
  | inl withinCeiling =>
      exact Nat.not_le_of_gt expands withinCeiling
  | inr grant =>
      rw [noGrant] at grant
      cases grant

end AsiStackProofs.StableCapabilityFields
