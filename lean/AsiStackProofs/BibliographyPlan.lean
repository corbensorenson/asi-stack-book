namespace AsiStackProofs.BibliographyPlan

structure SourceDerivedClaimReview where
  sourceDerivedClaim : Bool
  sourceNotePresent : Bool
  ingestedSourceArtifactPresent : Bool
deriving DecidableEq, Repr

def SourceDerivedClaimHasIngestedSource (review : SourceDerivedClaimReview) : Prop :=
  review.sourceDerivedClaim = true ->
    review.sourceNotePresent = true ∨
      review.ingestedSourceArtifactPresent = true

theorem source_derived_claim_without_source_record_rejected
    {review : SourceDerivedClaimReview} :
    review.sourceDerivedClaim = true ->
    review.sourceNotePresent = false ->
    review.ingestedSourceArtifactPresent = false ->
    ¬ SourceDerivedClaimHasIngestedSource review := by
  intro sourceDerived noteMissing artifactMissing valid
  have sourceEvidence := valid sourceDerived
  cases sourceEvidence with
  | inl notePresent =>
      rw [noteMissing] at notePresent
      cases notePresent
  | inr artifactPresent =>
      rw [artifactMissing] at artifactPresent
      cases artifactPresent

structure NewSourceAssignmentReview where
  newSource : Bool
  assignedChapterExists : Bool
  assignmentAccepted : Bool
deriving DecidableEq, Repr

def NewSourceAssignmentValid (review : NewSourceAssignmentReview) : Prop :=
  review.newSource = true ->
    review.assignmentAccepted = true ->
      review.assignedChapterExists = true

theorem accepted_new_source_assignment_to_nonexistent_chapter_rejected
    {review : NewSourceAssignmentReview} :
    review.newSource = true ->
    review.assignmentAccepted = true ->
    review.assignedChapterExists = false ->
    ¬ NewSourceAssignmentValid review := by
  intro newSource accepted missingChapter valid
  have existingChapter := valid newSource accepted
  rw [missingChapter] at existingChapter
  cases existingChapter

end AsiStackProofs.BibliographyPlan
