namespace AsiStackProofs.GenerateVerifyRepair

structure ReconstructionRecord where
  generatorOutput : Nat
  repairResidual : Nat
  target : Nat
  exactClaim : Bool
deriving DecidableEq, Repr

def ReconstructsTarget (record : ReconstructionRecord) : Prop :=
  record.generatorOutput + record.repairResidual = record.target

def ExactReconstructionClaimValid (record : ReconstructionRecord) : Prop :=
  record.exactClaim = true -> ReconstructsTarget record

theorem exact_reconstruction_claim_with_mismatched_repair_rejected
    {record : ReconstructionRecord} :
    record.exactClaim = true ->
    record.generatorOutput + record.repairResidual ≠ record.target ->
    ¬ ExactReconstructionClaimValid record := by
  intro exactClaim mismatch valid
  have reconstructs := valid exactClaim
  exact mismatch reconstructs

structure VerificationReview where
  verificationPassed : Bool
  exactnessPromoted : Bool
deriving DecidableEq, Repr

def FailedVerificationBlocksPromotion (review : VerificationReview) : Prop :=
  review.verificationPassed = false -> review.exactnessPromoted = false

theorem failed_verification_with_exactness_promotion_rejected
    {review : VerificationReview} :
    review.verificationPassed = false ->
    review.exactnessPromoted = true ->
    ¬ FailedVerificationBlocksPromotion review := by
  intro failed promoted valid
  have blocked := valid failed
  rw [promoted] at blocked
  cases blocked

end AsiStackProofs.GenerateVerifyRepair
