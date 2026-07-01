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

theorem tribunal_route_missing_review_rejects :
    TribunalReviewRouteFor {
      reviewRequested := false,
      dossierPresent := false,
      highRisk := false,
      adversarialProbeRecorded := false,
      independentReviewerPresent := false,
      evidenceRefsPresent := false,
      priorReviewReused := false,
      evidenceUnchanged := false,
      dissentPresent := false,
      dissentRecorded := false,
      actionVerdict := false,
      requiredActionRecorded := false,
      constraintsRecorded := false,
      supportStateChangeRequested := false,
      evidenceTransitionRecordPresent := false
    } = TribunalReviewRoute.rejectMissingReview := by
  simp [TribunalReviewRouteFor]

theorem high_risk_without_probe_routes_to_adversarial_probe :
    TribunalReviewRouteFor {
      reviewRequested := true,
      dossierPresent := true,
      highRisk := true,
      adversarialProbeRecorded := false,
      independentReviewerPresent := true,
      evidenceRefsPresent := true,
      priorReviewReused := false,
      evidenceUnchanged := true,
      dissentPresent := false,
      dissentRecorded := false,
      actionVerdict := false,
      requiredActionRecorded := true,
      constraintsRecorded := true,
      supportStateChangeRequested := false,
      evidenceTransitionRecordPresent := true
    } = TribunalReviewRoute.requestAdversarialProbe := by
  simp [TribunalReviewRouteFor]

theorem high_risk_without_independent_reviewer_routes_to_independent_review :
    TribunalReviewRouteFor {
      reviewRequested := true,
      dossierPresent := true,
      highRisk := true,
      adversarialProbeRecorded := true,
      independentReviewerPresent := false,
      evidenceRefsPresent := true,
      priorReviewReused := false,
      evidenceUnchanged := true,
      dissentPresent := false,
      dissentRecorded := false,
      actionVerdict := false,
      requiredActionRecorded := true,
      constraintsRecorded := true,
      supportStateChangeRequested := false,
      evidenceTransitionRecordPresent := true
    } = TribunalReviewRoute.requestIndependentReviewer := by
  simp [TribunalReviewRouteFor]

theorem changed_evidence_blocks_prior_review_reuse :
    TribunalReviewRouteFor {
      reviewRequested := true,
      dossierPresent := true,
      highRisk := false,
      adversarialProbeRecorded := true,
      independentReviewerPresent := true,
      evidenceRefsPresent := true,
      priorReviewReused := true,
      evidenceUnchanged := false,
      dissentPresent := false,
      dissentRecorded := false,
      actionVerdict := false,
      requiredActionRecorded := true,
      constraintsRecorded := true,
      supportStateChangeRequested := false,
      evidenceTransitionRecordPresent := true
    } = TribunalReviewRoute.rejectChangedEvidenceReuse := by
  simp [TribunalReviewRouteFor]

theorem unrecorded_dissent_routes_to_dissent_preservation :
    TribunalReviewRouteFor {
      reviewRequested := true,
      dossierPresent := true,
      highRisk := false,
      adversarialProbeRecorded := true,
      independentReviewerPresent := true,
      evidenceRefsPresent := true,
      priorReviewReused := false,
      evidenceUnchanged := true,
      dissentPresent := true,
      dissentRecorded := false,
      actionVerdict := false,
      requiredActionRecorded := true,
      constraintsRecorded := true,
      supportStateChangeRequested := false,
      evidenceTransitionRecordPresent := true
    } = TribunalReviewRoute.preserveDissent := by
  simp [TribunalReviewRouteFor]

theorem action_verdict_without_constraints_routes_to_action_constraints :
    TribunalReviewRouteFor {
      reviewRequested := true,
      dossierPresent := true,
      highRisk := false,
      adversarialProbeRecorded := true,
      independentReviewerPresent := true,
      evidenceRefsPresent := true,
      priorReviewReused := false,
      evidenceUnchanged := true,
      dissentPresent := false,
      dissentRecorded := false,
      actionVerdict := true,
      requiredActionRecorded := false,
      constraintsRecorded := true,
      supportStateChangeRequested := false,
      evidenceTransitionRecordPresent := true
    } = TribunalReviewRoute.requestActionConstraints := by
  simp [TribunalReviewRouteFor]

theorem support_change_without_evidence_transition_routes_to_evidence_review :
    TribunalReviewRouteFor {
      reviewRequested := true,
      dossierPresent := true,
      highRisk := false,
      adversarialProbeRecorded := true,
      independentReviewerPresent := true,
      evidenceRefsPresent := true,
      priorReviewReused := false,
      evidenceUnchanged := true,
      dissentPresent := false,
      dissentRecorded := false,
      actionVerdict := false,
      requiredActionRecorded := true,
      constraintsRecorded := true,
      supportStateChangeRequested := true,
      evidenceTransitionRecordPresent := false
    } = TribunalReviewRoute.requestEvidenceTransition := by
  simp [TribunalReviewRouteFor]

theorem complete_bounded_tribunal_review_accepts :
    TribunalReviewRouteFor {
      reviewRequested := true,
      dossierPresent := true,
      highRisk := true,
      adversarialProbeRecorded := true,
      independentReviewerPresent := true,
      evidenceRefsPresent := true,
      priorReviewReused := true,
      evidenceUnchanged := true,
      dissentPresent := true,
      dissentRecorded := true,
      actionVerdict := true,
      requiredActionRecorded := true,
      constraintsRecorded := true,
      supportStateChangeRequested := false,
      evidenceTransitionRecordPresent := true
    } = TribunalReviewRoute.acceptBoundedVerdict := by
  simp [TribunalReviewRouteFor]

end AsiStackProofs.Tribunal
