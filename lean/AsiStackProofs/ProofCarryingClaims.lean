namespace AsiStackProofs.ProofCarryingClaims

structure FormalTierClaimReview where
  formalSupportTier : Bool
  validJustificationArtifactRef : Bool
deriving DecidableEq, Repr

def FormalTierHasJustificationArtifact
    (review : FormalTierClaimReview) : Prop :=
  review.formalSupportTier = true ->
    review.validJustificationArtifactRef = true

theorem formal_support_tier_requires_valid_justification_artifact
    {review : FormalTierClaimReview} :
    FormalTierHasJustificationArtifact review ->
    review.formalSupportTier = true ->
    review.validJustificationArtifactRef = true := by
  intro valid formalTier
  exact valid formalTier

structure FailedVerifierPromotionReview where
  verifierFailed : Bool
  claimDowngradedOrBlocked : Bool
  claimPromoted : Bool
deriving DecidableEq, Repr

def FailedVerifierBlocksPromotion
    (review : FailedVerifierPromotionReview) : Prop :=
  review.verifierFailed = true ->
    review.claimDowngradedOrBlocked = true ∧
      review.claimPromoted = false

theorem failed_verifier_result_downgrades_or_blocks_claim_promotion
    {review : FailedVerifierPromotionReview} :
    FailedVerifierBlocksPromotion review ->
    review.verifierFailed = true ->
    review.claimDowngradedOrBlocked = true ∧
      review.claimPromoted = false := by
  intro valid failed
  exact valid failed

inductive VerifierResult where
  | passed
  | failed
  | timeout
  | mismatch
  | notRun
deriving DecidableEq, Repr

inductive ClaimValidityEffect where
  | scopedUpdate
  | noUpdate
  | downgrade
  | block
  | tribunal
deriving DecidableEq, Repr

def NegativeVerifierResult : VerifierResult -> Prop
  | .failed => True
  | .timeout => True
  | .mismatch => True
  | .passed => False
  | .notRun => False

def NonPromotionalEffect : ClaimValidityEffect -> Prop
  | .scopedUpdate => False
  | .noUpdate => True
  | .downgrade => True
  | .block => True
  | .tribunal => True

structure ProofCarryingClaimRecord where
  requestedTierPresent : Bool
  interpretationMappingPresent : Bool
  interpretationConfidenceRecorded : Bool
  justificationArtifactRefPresent : Bool
  verifierArtifactRefsPresent : Bool
  formalScopeRecorded : Bool
  limitationsRecorded : Bool
  supportStateEffectRecorded : Bool
  verifierResult : VerifierResult
  claimValidityEffect : ClaimValidityEffect
  nonClaimsPresent : Bool
deriving DecidableEq, Repr

def ProofCarryingClaimRecordValid
    (record : ProofCarryingClaimRecord) : Prop :=
  record.requestedTierPresent = true ∧
    record.interpretationMappingPresent = true ∧
      record.interpretationConfidenceRecorded = true ∧
        record.justificationArtifactRefPresent = true ∧
          record.formalScopeRecorded = true ∧
            record.limitationsRecorded = true ∧
              record.supportStateEffectRecorded = true ∧
                record.nonClaimsPresent = true ∧
                  (record.verifierResult = VerifierResult.passed ->
                    record.verifierArtifactRefsPresent = true) ∧
                    (NegativeVerifierResult record.verifierResult ->
                      NonPromotionalEffect record.claimValidityEffect)

theorem valid_proof_carrying_claim_record_preserves_mapping_scope_limits_and_boundary
    {record : ProofCarryingClaimRecord} :
    ProofCarryingClaimRecordValid record ->
    record.requestedTierPresent = true ∧
      record.interpretationMappingPresent = true ∧
        record.interpretationConfidenceRecorded = true ∧
          record.justificationArtifactRefPresent = true ∧
            record.formalScopeRecorded = true ∧
              record.limitationsRecorded = true ∧
                record.supportStateEffectRecorded = true ∧
                  record.nonClaimsPresent = true := by
  intro valid
  exact And.intro valid.1
    (And.intro valid.2.1
      (And.intro valid.2.2.1
        (And.intro valid.2.2.2.1
          (And.intro valid.2.2.2.2.1
            (And.intro valid.2.2.2.2.2.1
              (And.intro valid.2.2.2.2.2.2.1 valid.2.2.2.2.2.2.2.1))))))

theorem passed_verifier_result_requires_verifier_artifact_reference
    {record : ProofCarryingClaimRecord} :
    ProofCarryingClaimRecordValid record ->
    record.verifierResult = VerifierResult.passed ->
    record.verifierArtifactRefsPresent = true := by
  intro valid passed
  exact valid.2.2.2.2.2.2.2.2.1 passed

theorem passed_verifier_without_artifact_reference_rejected
    {record : ProofCarryingClaimRecord} :
    record.verifierResult = VerifierResult.passed ->
    record.verifierArtifactRefsPresent = false ->
    ¬ ProofCarryingClaimRecordValid record := by
  intro passed missingRefs valid
  have refs :=
    passed_verifier_result_requires_verifier_artifact_reference valid passed
  rw [missingRefs] at refs
  contradiction

theorem negative_verifier_result_requires_non_promotional_effect
    {record : ProofCarryingClaimRecord} :
    ProofCarryingClaimRecordValid record ->
    NegativeVerifierResult record.verifierResult ->
    NonPromotionalEffect record.claimValidityEffect := by
  intro valid negative
  exact valid.2.2.2.2.2.2.2.2.2 negative

theorem negative_verifier_result_with_scoped_update_rejected
    {record : ProofCarryingClaimRecord} :
    NegativeVerifierResult record.verifierResult ->
    record.claimValidityEffect = ClaimValidityEffect.scopedUpdate ->
    ¬ ProofCarryingClaimRecordValid record := by
  intro negative scopedUpdate valid
  have effect :=
    negative_verifier_result_requires_non_promotional_effect valid negative
  rw [scopedUpdate] at effect
  contradiction

end AsiStackProofs.ProofCarryingClaims
