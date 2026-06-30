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

inductive ScfLifecycleRoute where
  | defaultRoute
  | canaryRoute
  | requireRequalification
  | requireRollback
  | requestGovernanceReview
  | rejectReplacement
deriving DecidableEq, Repr

structure ScfLifecycleReview where
  fieldIdentityMatches : Bool
  qualificationSatisfied : Bool
  evidenceRefsPresent : Bool
  leaseFresh : Bool
  evaluatorIndependent : Bool
  authorityWithinCeiling : Bool
  governanceGrant : Bool
  rollbackReady : Bool
  regressionFloorPreserved : Bool
  incidentOpen : Bool
  defaultRequested : Bool
deriving DecidableEq, Repr

def ScfLifecycleRouteFor (review : ScfLifecycleReview) : ScfLifecycleRoute :=
  if review.fieldIdentityMatches = false then
    ScfLifecycleRoute.rejectReplacement
  else if review.qualificationSatisfied = false then
    ScfLifecycleRoute.requireRequalification
  else if review.evidenceRefsPresent = false then
    ScfLifecycleRoute.requireRequalification
  else if review.leaseFresh = false then
    ScfLifecycleRoute.requireRequalification
  else if review.evaluatorIndependent = false then
    ScfLifecycleRoute.requestGovernanceReview
  else if review.authorityWithinCeiling = false ∧ review.governanceGrant = false then
    ScfLifecycleRoute.requestGovernanceReview
  else if review.incidentOpen = true then
    ScfLifecycleRoute.requireRollback
  else if review.rollbackReady = false then
    ScfLifecycleRoute.requireRollback
  else if review.regressionFloorPreserved = false then
    ScfLifecycleRoute.requireRollback
  else if review.defaultRequested = true then
    ScfLifecycleRoute.defaultRoute
  else
    ScfLifecycleRoute.canaryRoute

theorem field_identity_mismatch_rejects_replacement
    {review : ScfLifecycleReview} :
    review.fieldIdentityMatches = false ->
    ScfLifecycleRouteFor review = ScfLifecycleRoute.rejectReplacement := by
  intro identityMismatch
  unfold ScfLifecycleRouteFor
  simp [identityMismatch]

theorem stale_qualification_lease_requires_requalification
    {review : ScfLifecycleReview} :
    review.fieldIdentityMatches = true ->
    review.qualificationSatisfied = true ->
    review.evidenceRefsPresent = true ->
    review.leaseFresh = false ->
    ScfLifecycleRouteFor review =
      ScfLifecycleRoute.requireRequalification := by
  intro identityMatches qualified evidencePresent staleLease
  unfold ScfLifecycleRouteFor
  simp [identityMatches, qualified, evidencePresent, staleLease]

theorem missing_evidence_requires_requalification
    {review : ScfLifecycleReview} :
    review.fieldIdentityMatches = true ->
    review.qualificationSatisfied = true ->
    review.evidenceRefsPresent = false ->
    ScfLifecycleRouteFor review =
      ScfLifecycleRoute.requireRequalification := by
  intro identityMatches qualified missingEvidence
  unfold ScfLifecycleRouteFor
  simp [identityMatches, qualified, missingEvidence]

theorem captured_evaluator_routes_to_governance_review
    {review : ScfLifecycleReview} :
    review.fieldIdentityMatches = true ->
    review.qualificationSatisfied = true ->
    review.evidenceRefsPresent = true ->
    review.leaseFresh = true ->
    review.evaluatorIndependent = false ->
    ScfLifecycleRouteFor review =
      ScfLifecycleRoute.requestGovernanceReview := by
  intro identityMatches qualified evidencePresent freshLease capturedEvaluator
  unfold ScfLifecycleRouteFor
  simp [identityMatches, qualified, evidencePresent, freshLease,
    capturedEvaluator]

theorem authority_expansion_without_grant_routes_to_governance_review
    {review : ScfLifecycleReview} :
    review.fieldIdentityMatches = true ->
    review.qualificationSatisfied = true ->
    review.evidenceRefsPresent = true ->
    review.leaseFresh = true ->
    review.evaluatorIndependent = true ->
    review.authorityWithinCeiling = false ->
    review.governanceGrant = false ->
    ScfLifecycleRouteFor review =
      ScfLifecycleRoute.requestGovernanceReview := by
  intro identityMatches qualified evidencePresent freshLease evaluatorIndependent
    exceedsCeiling noGrant
  unfold ScfLifecycleRouteFor
  simp [identityMatches, qualified, evidencePresent, freshLease,
    evaluatorIndependent, exceedsCeiling, noGrant]

theorem open_incident_requires_rollback
    {review : ScfLifecycleReview} :
    review.fieldIdentityMatches = true ->
    review.qualificationSatisfied = true ->
    review.evidenceRefsPresent = true ->
    review.leaseFresh = true ->
    review.evaluatorIndependent = true ->
    review.authorityWithinCeiling = true ->
    review.incidentOpen = true ->
    ScfLifecycleRouteFor review = ScfLifecycleRoute.requireRollback := by
  intro identityMatches qualified evidencePresent freshLease evaluatorIndependent
    withinCeiling incidentOpen
  unfold ScfLifecycleRouteFor
  simp [identityMatches, qualified, evidencePresent, freshLease,
    evaluatorIndependent, withinCeiling, incidentOpen]

theorem complete_default_review_routes_to_default
    {review : ScfLifecycleReview} :
    review.fieldIdentityMatches = true ->
    review.qualificationSatisfied = true ->
    review.evidenceRefsPresent = true ->
    review.leaseFresh = true ->
    review.evaluatorIndependent = true ->
    review.authorityWithinCeiling = true ->
    review.incidentOpen = false ->
    review.rollbackReady = true ->
    review.regressionFloorPreserved = true ->
    review.defaultRequested = true ->
    ScfLifecycleRouteFor review = ScfLifecycleRoute.defaultRoute := by
  intro identityMatches qualified evidencePresent freshLease evaluatorIndependent
    withinCeiling noIncident rollbackReady regressionPreserved defaultRequested
  unfold ScfLifecycleRouteFor
  simp [identityMatches, qualified, evidencePresent, freshLease,
    evaluatorIndependent, withinCeiling, noIncident, rollbackReady,
    regressionPreserved, defaultRequested]

end AsiStackProofs.StableCapabilityFields
