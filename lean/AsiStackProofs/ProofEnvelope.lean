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

theorem implemented_target_missing_module_or_build_rejected
    {target : ProofTargetReview} :
    target.status = ProofTargetStatus.implemented ->
    (target.moduleExists = false ∨ target.buildPassed = false) ->
    ¬ ImplementedTargetValid target := by
  intro implemented missing valid
  have complete := valid implemented
  cases complete with
  | intro moduleExists buildPassed =>
      cases missing with
      | inl moduleMissing =>
          rw [moduleMissing] at moduleExists
          contradiction
      | inr buildMissing =>
          rw [buildMissing] at buildPassed
          contradiction

inductive ProofArtifactLane where
  | lean
  | schema
  | processValidator
  | behaviorTest
  | benchmark
  | externalTheorem
  | researchBacklog
deriving DecidableEq, Repr

inductive VerifierResult where
  | passed
  | failed
  | timedOut
  | notRun
deriving DecidableEq, Repr

inductive SemanticAdequacy where
  | adequateFiniteRecord
  | projectionOnlyTraceability
  | inadequate
  | notReviewed
deriving DecidableEq, Repr

inductive SupportStateEffect where
  | noChange
  | proofStateOnly
  | supportPromotion
  | demotion
deriving DecidableEq, Repr

structure ProofArtifactReview where
  lane : ProofArtifactLane
  verifierResult : VerifierResult
  artifactRefsPresent : Bool
  verifierCommandRecorded : Bool
  semanticAdequacy : SemanticAdequacy
  limitationsRecorded : Bool
  nonClaimsRecorded : Bool
  consumerRequirementsMatched : Bool
  claimedLeanProof : Bool
  externalTheoremIdsResolved : Bool
  supportStateEffect : SupportStateEffect
  evidenceTransitionAccepted : Bool
deriving DecidableEq, Repr

def LeanProofClaimValid (review : ProofArtifactReview) : Prop :=
  review.claimedLeanProof = true ->
    review.lane = ProofArtifactLane.lean ∧
      review.verifierResult = VerifierResult.passed ∧
        review.artifactRefsPresent = true ∧
          review.verifierCommandRecorded = true

theorem non_lean_artifact_cannot_claim_lean_proof
    {review : ProofArtifactReview} :
    review.claimedLeanProof = true ->
    review.lane ≠ ProofArtifactLane.lean ->
    ¬ LeanProofClaimValid review := by
  intro claimed nonLean valid
  unfold LeanProofClaimValid at valid
  have proofBoundary := valid claimed
  exact nonLean proofBoundary.1

def SupportPromotionValid (review : ProofArtifactReview) : Prop :=
  review.supportStateEffect = SupportStateEffect.supportPromotion ->
    review.evidenceTransitionAccepted = true ∧
      review.semanticAdequacy = SemanticAdequacy.adequateFiniteRecord ∧
        review.limitationsRecorded = true ∧
          review.nonClaimsRecorded = true ∧
            review.consumerRequirementsMatched = true

theorem support_promotion_without_transition_or_boundaries_rejected
    {review : ProofArtifactReview} :
    review.supportStateEffect = SupportStateEffect.supportPromotion ->
    (review.evidenceTransitionAccepted = false ∨
      review.semanticAdequacy ≠ SemanticAdequacy.adequateFiniteRecord ∨
        review.limitationsRecorded = false ∨
          review.nonClaimsRecorded = false ∨
            review.consumerRequirementsMatched = false) ->
    ¬ SupportPromotionValid review := by
  intro promotion missing valid
  unfold SupportPromotionValid at valid
  have complete := valid promotion
  cases complete with
  | intro transitionAccepted rest =>
      cases rest with
      | intro adequate rest =>
          cases rest with
          | intro limitations rest =>
              cases rest with
              | intro nonClaims consumerRequirements =>
                  cases missing with
                  | inl transitionMissing =>
                      rw [transitionMissing] at transitionAccepted
                      contradiction
                  | inr restMissing =>
                      cases restMissing with
                      | inl adequacyMissing =>
                          exact adequacyMissing adequate
                      | inr restMissing =>
                          cases restMissing with
                          | inl limitationsMissing =>
                              rw [limitationsMissing] at limitations
                              contradiction
                          | inr restMissing =>
                              cases restMissing with
                              | inl nonClaimsMissing =>
                                  rw [nonClaimsMissing] at nonClaims
                                  contradiction
                              | inr consumerMissing =>
                                  rw [consumerMissing] at consumerRequirements
                                  contradiction

def ExternalTheoremReferenceValid (review : ProofArtifactReview) : Prop :=
  review.lane = ProofArtifactLane.externalTheorem ->
    review.artifactRefsPresent = true ∧
      review.externalTheoremIdsResolved = true ∧
        review.nonClaimsRecorded = true

theorem external_theorem_without_ids_or_boundary_rejected
    {review : ProofArtifactReview} :
    review.lane = ProofArtifactLane.externalTheorem ->
    (review.artifactRefsPresent = false ∨
      review.externalTheoremIdsResolved = false ∨
        review.nonClaimsRecorded = false) ->
    ¬ ExternalTheoremReferenceValid review := by
  intro externalRef missing valid
  unfold ExternalTheoremReferenceValid at valid
  have complete := valid externalRef
  cases complete with
  | intro artifactRefs rest =>
      cases rest with
      | intro theoremIds nonClaims =>
          cases missing with
          | inl artifactMissing =>
              rw [artifactMissing] at artifactRefs
              contradiction
          | inr restMissing =>
              cases restMissing with
              | inl idsMissing =>
                  rw [idsMissing] at theoremIds
                  contradiction
              | inr nonClaimsMissing =>
                  rw [nonClaimsMissing] at nonClaims
                  contradiction

end AsiStackProofs.ProofEnvelope
