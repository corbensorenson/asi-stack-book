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

inductive TribunalReviewRoute where
  | rejectMissingReview
  | requestDossier
  | requestAdversarialProbe
  | requestIndependentReviewer
  | rejectChangedEvidenceReuse
  | preserveDissent
  | requestActionConstraints
  | requestEvidenceTransition
  | acceptBoundedVerdict
deriving DecidableEq, Repr

structure TribunalReviewLifecycle where
  reviewRequested : Bool
  dossierPresent : Bool
  highRisk : Bool
  adversarialProbeRecorded : Bool
  independentReviewerPresent : Bool
  evidenceRefsPresent : Bool
  priorReviewReused : Bool
  evidenceUnchanged : Bool
  dissentPresent : Bool
  dissentRecorded : Bool
  actionVerdict : Bool
  requiredActionRecorded : Bool
  constraintsRecorded : Bool
  supportStateChangeRequested : Bool
  evidenceTransitionRecordPresent : Bool
deriving DecidableEq, Repr

def TribunalReviewRouteFor (review : TribunalReviewLifecycle) :
    TribunalReviewRoute :=
  if review.reviewRequested = false then
    TribunalReviewRoute.rejectMissingReview
  else if review.dossierPresent = false then
    TribunalReviewRoute.requestDossier
  else if review.evidenceRefsPresent = false then
    TribunalReviewRoute.requestDossier
  else if review.highRisk = true ∧ review.adversarialProbeRecorded = false then
    TribunalReviewRoute.requestAdversarialProbe
  else if review.highRisk = true ∧ review.independentReviewerPresent = false then
    TribunalReviewRoute.requestIndependentReviewer
  else if review.priorReviewReused = true ∧ review.evidenceUnchanged = false then
    TribunalReviewRoute.rejectChangedEvidenceReuse
  else if review.dissentPresent = true ∧ review.dissentRecorded = false then
    TribunalReviewRoute.preserveDissent
  else if review.actionVerdict = true ∧
      (review.requiredActionRecorded = false ∨
        review.constraintsRecorded = false) then
    TribunalReviewRoute.requestActionConstraints
  else if review.supportStateChangeRequested = true ∧
      review.evidenceTransitionRecordPresent = false then
    TribunalReviewRoute.requestEvidenceTransition
  else
    TribunalReviewRoute.acceptBoundedVerdict

end AsiStackProofs.Tribunal
