namespace AsiStackProofs.Tribunal

structure TribunalVerdictReview where
  verdictIssued : Bool
  reviewerRolesPresent : Bool
  evidenceRefsPresent : Bool
  unresolvedDissentRecorded : Bool
deriving DecidableEq, Repr

def VerdictIncludesReviewArtifacts (review : TribunalVerdictReview) : Prop :=
  review.verdictIssued = true ->
    review.reviewerRolesPresent = true ∧
      review.evidenceRefsPresent = true ∧
        review.unresolvedDissentRecorded = true

theorem tribunal_verdict_includes_roles_evidence_and_unresolved_dissent
    {review : TribunalVerdictReview} :
    VerdictIncludesReviewArtifacts review ->
    review.verdictIssued = true ->
    review.reviewerRolesPresent = true ∧
      review.evidenceRefsPresent = true ∧
        review.unresolvedDissentRecorded = true := by
  intro valid issued
  exact valid issued

structure HighRiskArtifactAcceptanceReview where
  highRiskArtifact : Bool
  tribunalReviewRequired : Bool
  tribunalReviewPresent : Bool
  artifactAccepted : Bool
deriving DecidableEq, Repr

def MissingRequiredTribunalBlocksAcceptance
    (review : HighRiskArtifactAcceptanceReview) : Prop :=
  review.highRiskArtifact = true ->
    review.tribunalReviewRequired = true ->
      review.tribunalReviewPresent = false ->
        review.artifactAccepted = false

theorem high_risk_artifact_without_required_tribunal_review_cannot_be_accepted
    {review : HighRiskArtifactAcceptanceReview} :
    MissingRequiredTribunalBlocksAcceptance review ->
    review.highRiskArtifact = true ->
    review.tribunalReviewRequired = true ->
    review.tribunalReviewPresent = false ->
    review.artifactAccepted = false := by
  intro valid highRisk required missing
  exact valid highRisk required missing

structure HighRiskTribunalProbeReview where
  highRiskReview : Bool
  verdictAccepted : Bool
  adversarialProbesPresent : Bool
  reviewerIndependenceRecorded : Bool
deriving DecidableEq, Repr

def HighRiskAcceptedVerdictHasProbeDiscipline
    (review : HighRiskTribunalProbeReview) : Prop :=
  review.highRiskReview = true ->
    review.verdictAccepted = true ->
      review.adversarialProbesPresent = true ∧
        review.reviewerIndependenceRecorded = true

theorem high_risk_accepted_verdict_without_probes_or_independence_rejected
    {review : HighRiskTribunalProbeReview} :
    review.highRiskReview = true ->
    review.verdictAccepted = true ->
    (review.adversarialProbesPresent = false ∨
      review.reviewerIndependenceRecorded = false) ->
    ¬ HighRiskAcceptedVerdictHasProbeDiscipline review := by
  intro highRisk accepted missing valid
  unfold HighRiskAcceptedVerdictHasProbeDiscipline at valid
  have discipline := valid highRisk accepted
  cases discipline with
  | intro probesPresent independencePresent =>
      cases missing with
      | inl probesMissing =>
          rw [probesMissing] at probesPresent
          contradiction
      | inr independenceMissing =>
          rw [independenceMissing] at independencePresent
          contradiction

structure PriorReviewReuseReview where
  verdictAccepted : Bool
  priorReviewRefsPresent : Bool
  evidenceChanged : Bool
  unchangedEvidenceGuardPresent : Bool
deriving DecidableEq, Repr

def AcceptedPriorReviewReuseHasGuard (review : PriorReviewReuseReview) : Prop :=
  review.verdictAccepted = true ->
    review.priorReviewRefsPresent = true ->
      review.evidenceChanged = false ->
        review.unchangedEvidenceGuardPresent = true

theorem accepted_prior_review_reuse_without_unchanged_evidence_guard_rejected
    {review : PriorReviewReuseReview} :
    review.verdictAccepted = true ->
    review.priorReviewRefsPresent = true ->
    review.evidenceChanged = false ->
    review.unchangedEvidenceGuardPresent = false ->
    ¬ AcceptedPriorReviewReuseHasGuard review := by
  intro accepted priorRefs unchanged missingGuard valid
  unfold AcceptedPriorReviewReuseHasGuard at valid
  have guardPresent := valid accepted priorRefs unchanged
  rw [missingGuard] at guardPresent
  contradiction

structure TribunalActionConstraintReview where
  verdictIssued : Bool
  verdictRequiresAction : Bool
  requiredActionsRecorded : Bool
  constraintEffectsRecorded : Bool
deriving DecidableEq, Repr

def ActionVerdictRecordsActionsAndConstraints
    (review : TribunalActionConstraintReview) : Prop :=
  review.verdictIssued = true ->
    review.verdictRequiresAction = true ->
      review.requiredActionsRecorded = true ∧
        review.constraintEffectsRecorded = true

theorem action_verdict_without_actions_or_constraints_rejected
    {review : TribunalActionConstraintReview} :
    review.verdictIssued = true ->
    review.verdictRequiresAction = true ->
    (review.requiredActionsRecorded = false ∨
      review.constraintEffectsRecorded = false) ->
    ¬ ActionVerdictRecordsActionsAndConstraints review := by
  intro issued requiresAction missing valid
  unfold ActionVerdictRecordsActionsAndConstraints at valid
  have recorded := valid issued requiresAction
  cases recorded with
  | intro actionsRecorded constraintsRecorded =>
      cases missing with
      | inl actionsMissing =>
          rw [actionsMissing] at actionsRecorded
          contradiction
      | inr constraintsMissing =>
          rw [constraintsMissing] at constraintsRecorded
          contradiction

end AsiStackProofs.Tribunal
