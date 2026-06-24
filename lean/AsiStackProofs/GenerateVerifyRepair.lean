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

theorem exact_reconstruction_claim_requires_generator_plus_repair
    {record : ReconstructionRecord} :
    ExactReconstructionClaimValid record ->
    record.exactClaim = true ->
    record.generatorOutput + record.repairResidual = record.target := by
  intro valid exactClaim
  exact valid exactClaim

structure VerificationReview where
  verificationPassed : Bool
  exactnessPromoted : Bool
deriving DecidableEq, Repr

def FailedVerificationBlocksPromotion (review : VerificationReview) : Prop :=
  review.verificationPassed = false -> review.exactnessPromoted = false

theorem failed_verification_blocks_exactness_promotion
    {review : VerificationReview} :
    FailedVerificationBlocksPromotion review ->
    review.verificationPassed = false ->
    review.exactnessPromoted = false := by
  intro valid failed
  exact valid failed

end AsiStackProofs.GenerateVerifyRepair
