namespace AsiStackProofs.ProceduralMemory

structure GeneratedToolRecordReview where
  generatedTool : Bool
  sourceTracesPresent : Bool
  parametersPresent : Bool
  verificationResultRecorded : Bool
deriving DecidableEq, Repr

def GeneratedToolHasClosureArtifacts
    (review : GeneratedToolRecordReview) : Prop :=
  review.generatedTool = true ->
    review.sourceTracesPresent = true ∧
      review.parametersPresent = true ∧
        review.verificationResultRecorded = true

theorem generated_tool_records_source_traces_parameters_and_verification_result
    {review : GeneratedToolRecordReview} :
    GeneratedToolHasClosureArtifacts review ->
    review.generatedTool = true ->
    review.sourceTracesPresent = true ∧
      review.parametersPresent = true ∧
        review.verificationResultRecorded = true := by
  intro valid generated
  exact valid generated

theorem generated_tool_missing_closure_artifact_rejected
    {review : GeneratedToolRecordReview} :
    review.generatedTool = true ->
      (review.sourceTracesPresent = false ∨
        review.parametersPresent = false ∨
          review.verificationResultRecorded = false) ->
        ¬ GeneratedToolHasClosureArtifacts review := by
  intro generated missingArtifact valid
  have closure := valid generated
  cases missingArtifact with
  | inl missingSourceTraces =>
      rw [missingSourceTraces] at closure
      cases closure.1
  | inr rest =>
      cases rest with
      | inl missingParameters =>
          rw [missingParameters] at closure
          cases closure.2.1
      | inr missingVerification =>
          rw [missingVerification] at closure
          cases closure.2.2

structure RegressionPromotionReview where
  regressionFailed : Bool
  routableStatusPromoted : Bool
deriving DecidableEq, Repr

def FailedRegressionBlocksRoutablePromotion
    (review : RegressionPromotionReview) : Prop :=
  review.regressionFailed = true ->
    review.routableStatusPromoted = false

theorem tool_with_failed_regression_cannot_be_promoted_to_routable_status
    {review : RegressionPromotionReview} :
    FailedRegressionBlocksRoutablePromotion review ->
    review.regressionFailed = true ->
    review.routableStatusPromoted = false := by
  intro valid failed
  exact valid failed

theorem failed_regression_with_routable_promotion_rejected
    {review : RegressionPromotionReview} :
    review.regressionFailed = true ->
      review.routableStatusPromoted = true ->
        ¬ FailedRegressionBlocksRoutablePromotion review := by
  intro failed promoted valid
  have blocked := valid failed
  rw [promoted] at blocked
  contradiction

end AsiStackProofs.ProceduralMemory
