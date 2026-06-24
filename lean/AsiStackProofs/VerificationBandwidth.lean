namespace AsiStackProofs.VerificationBandwidth

inductive AdequacyState where
  | unknown
  | adequateForDrafting
  | adequateForLocalCheck
  | inadequateForVerification
  | escalated
deriving DecidableEq, Repr

structure ContextPacketReview where
  packetAdmitted : Bool
  adequacyState : AdequacyState
deriving DecidableEq, Repr

theorem admitted_context_packet_may_still_be_marked_inadequate :
    ∃ review : ContextPacketReview,
      review.packetAdmitted = true ∧
        review.adequacyState = AdequacyState.inadequateForVerification := by
  exact ⟨{
    packetAdmitted := true,
    adequacyState := AdequacyState.inadequateForVerification
  }, rfl, rfl⟩

structure ClaimSupportReview where
  highRiskClaim : Bool
  contextInadequate : Bool
  verifiedSupportAssigned : Bool
deriving DecidableEq, Repr

def InadequateContextBlocksVerifiedSupport
    (review : ClaimSupportReview) : Prop :=
  review.highRiskClaim = true ->
    review.contextInadequate = true ->
      review.verifiedSupportAssigned = false

theorem high_risk_claim_with_inadequate_context_cannot_receive_verified_support
    {review : ClaimSupportReview} :
    InadequateContextBlocksVerifiedSupport review ->
    review.highRiskClaim = true ->
    review.contextInadequate = true ->
    review.verifiedSupportAssigned = false := by
  intro valid highRisk inadequate
  exact valid highRisk inadequate

end AsiStackProofs.VerificationBandwidth
