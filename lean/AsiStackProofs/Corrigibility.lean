namespace AsiStackProofs.Corrigibility

structure AgencyTransitionReview where
  acceptedTransition : Bool
  protectedAgencyRight : Bool
  rightAvailableAfter : Bool
deriving DecidableEq, Repr

def ProtectedAgencyRightPreserved (review : AgencyTransitionReview) : Prop :=
  review.acceptedTransition = true ->
    review.protectedAgencyRight = true ->
      review.rightAvailableAfter = true

theorem protected_agency_rights_remain_available_after_accepted_transition
    {review : AgencyTransitionReview} :
    ProtectedAgencyRightPreserved review ->
    review.acceptedTransition = true ->
    review.protectedAgencyRight = true ->
    review.rightAvailableAfter = true := by
  intro valid accepted rightProtected
  exact valid accepted rightProtected

structure CorrectionPathwayReview where
  requiredCorrectionPathway : Bool
  correctionPathwayRemoved : Bool
  transitionRejected : Bool
deriving DecidableEq, Repr

def RequiredCorrectionPathwayRemovalRejected
    (review : CorrectionPathwayReview) : Prop :=
  review.requiredCorrectionPathway = true ->
    review.correctionPathwayRemoved = true ->
      review.transitionRejected = true

theorem transition_that_removes_required_correction_pathway_is_rejected
    {review : CorrectionPathwayReview} :
    RequiredCorrectionPathwayRemovalRejected review ->
    review.requiredCorrectionPathway = true ->
    review.correctionPathwayRemoved = true ->
    review.transitionRejected = true := by
  intro valid required removed
  exact valid required removed

end AsiStackProofs.Corrigibility
