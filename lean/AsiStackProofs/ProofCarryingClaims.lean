namespace AsiStackProofs.ProofCarryingClaims

structure FormalTierClaimReview where
  formalSupportTier : Bool
  validJustificationArtifactRef : Bool
deriving DecidableEq, Repr

def FormalTierHasJustificationArtifact
    (review : FormalTierClaimReview) : Prop :=
  review.formalSupportTier = true ->
    review.validJustificationArtifactRef = true

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

structure AdversarialReviewDossierProbeSummary where
  scopedAcceptDossierPresent : Bool
  mismatchRejectionDossierPresent : Bool
  negativeControlsRejected : Bool
  llmJudgeOnlyRejected : Bool
  supportStateEffectNone : Bool
  nonClaimBoundary : Bool
deriving DecidableEq, Repr

def AdversarialReviewDossierProbeSummaryValid
    (summary : AdversarialReviewDossierProbeSummary) : Prop :=
  summary.scopedAcceptDossierPresent = true ∧
    summary.mismatchRejectionDossierPresent = true ∧
    summary.negativeControlsRejected = true ∧
    summary.llmJudgeOnlyRejected = true ∧
    summary.supportStateEffectNone = true ∧
    summary.nonClaimBoundary = true

end AsiStackProofs.ProofCarryingClaims
