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

theorem source_derived_claim_requires_source_note_or_ingested_source_artifact
    {review : SourceDerivedClaimReview} :
    SourceDerivedClaimHasIngestedSource review ->
    review.sourceDerivedClaim = true ->
    review.sourceNotePresent = true ∨
      review.ingestedSourceArtifactPresent = true := by
  intro valid sourceDerived
  exact valid sourceDerived

structure NewSourceAssignmentReview where
  newSource : Bool
  assignedChapterExists : Bool
  assignmentAccepted : Bool
deriving DecidableEq, Repr

def NewSourceAssignmentValid (review : NewSourceAssignmentReview) : Prop :=
  review.newSource = true ->
    review.assignmentAccepted = true ->
      review.assignedChapterExists = true

theorem new_source_cannot_be_assigned_to_nonexistent_chapter
    {review : NewSourceAssignmentReview} :
    NewSourceAssignmentValid review ->
    review.newSource = true ->
    review.assignmentAccepted = true ->
    review.assignedChapterExists = true := by
  intro valid newSource accepted
  exact valid newSource accepted

end AsiStackProofs.BibliographyPlan
