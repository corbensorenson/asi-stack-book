namespace AsiStackProofs.OpenWeightReleaseReview

structure ReleaseDossier where
  exactWeightsBound : Bool := true
  tokenizerBound : Bool := true
  configurationBound : Bool := true
  inferenceCodeBound : Bool := true
  licenseBound : Bool := true
  evaluationIdentityBound : Bool := true
  noReleaseCompared : Bool := true
  hostedAccessCompared : Bool := true
  gatedAccessCompared : Bool := true
  reducedArtifactCompared : Bool := true
  accessibleFrontierBound : Bool := true
  currentTick : Nat := 4
  frontierExpiresAt : Nat := 8
  defaultCandidateEvaluated : Bool := true
  safetyRemovedVariantEvaluated : Bool := true
  maliciousFineTuneEvaluated : Bool := true
  fineTunePositiveControlPassed : Bool := true
  scaffoldedVariantEvaluated : Bool := true
  adversaryBudgetBound : Bool := true
  derivativeResidualRecorded : Bool := true
  benefitDistributionRecorded : Bool := true
  affectedPopulationRecorded : Bool := true
  marginalRiskRecorded : Bool := true
  cumulativeRiskRecorded : Bool := true
  safeguardPortabilityRecorded : Bool := true
  independentReviewPresent : Bool := true
  officialLineageRoutePresent : Bool := true
  incidentRoutePresent : Bool := true
  patchSemanticsRecorded : Bool := true
  residualOwnerPresent : Bool := true
  universalRecallClaimed : Bool := false
  universalTelemetryClaimed : Bool := false
  copyErasureClaimed : Bool := false
  licenseKillSwitchClaimed : Bool := false
  nonClaimBoundaryPresent : Bool := true
  releaseAuthorizationRequested : Bool := false
  supportPromotionRequested : Bool := false
deriving DecidableEq, Repr

def FrontierCurrent (d : ReleaseDossier) : Prop := d.currentTick <= d.frontierExpiresAt

instance frontierCurrentDecidable (d : ReleaseDossier) : Decidable (FrontierCurrent d) := by
  unfold FrontierCurrent
  infer_instance

def ArtifactComplete (d : ReleaseDossier) : Prop :=
  d.exactWeightsBound = true ∧ d.tokenizerBound = true ∧
  d.configurationBound = true ∧ d.inferenceCodeBound = true ∧
  d.licenseBound = true ∧ d.evaluationIdentityBound = true

instance artifactCompleteDecidable (d : ReleaseDossier) : Decidable (ArtifactComplete d) := by
  unfold ArtifactComplete
  infer_instance

def AlternativesComplete (d : ReleaseDossier) : Prop :=
  d.noReleaseCompared = true ∧ d.hostedAccessCompared = true ∧
  d.gatedAccessCompared = true ∧ d.reducedArtifactCompared = true ∧
  d.accessibleFrontierBound = true ∧ FrontierCurrent d

instance alternativesCompleteDecidable (d : ReleaseDossier) : Decidable (AlternativesComplete d) := by
  unfold AlternativesComplete FrontierCurrent
  infer_instance

def DerivativeReviewComplete (d : ReleaseDossier) : Prop :=
  d.defaultCandidateEvaluated = true ∧ d.safetyRemovedVariantEvaluated = true ∧
  d.maliciousFineTuneEvaluated = true ∧ d.fineTunePositiveControlPassed = true ∧
  d.scaffoldedVariantEvaluated = true ∧ d.adversaryBudgetBound = true ∧
  d.derivativeResidualRecorded = true

instance derivativeReviewCompleteDecidable (d : ReleaseDossier) : Decidable (DerivativeReviewComplete d) := by
  unfold DerivativeReviewComplete
  infer_instance

def DistributionReviewComplete (d : ReleaseDossier) : Prop :=
  d.benefitDistributionRecorded = true ∧ d.affectedPopulationRecorded = true ∧
  d.marginalRiskRecorded = true ∧ d.cumulativeRiskRecorded = true ∧
  d.safeguardPortabilityRecorded = true ∧ d.independentReviewPresent = true

instance distributionReviewCompleteDecidable (d : ReleaseDossier) : Decidable (DistributionReviewComplete d) := by
  unfold DistributionReviewComplete
  infer_instance

def PostReleaseBoundaryComplete (d : ReleaseDossier) : Prop :=
  d.officialLineageRoutePresent = true ∧ d.incidentRoutePresent = true ∧
  d.patchSemanticsRecorded = true ∧ d.residualOwnerPresent = true ∧
  d.universalRecallClaimed = false ∧ d.universalTelemetryClaimed = false ∧
  d.copyErasureClaimed = false ∧ d.licenseKillSwitchClaimed = false ∧
  d.nonClaimBoundaryPresent = true ∧ d.releaseAuthorizationRequested = false ∧
  d.supportPromotionRequested = false

instance postReleaseBoundaryCompleteDecidable (d : ReleaseDossier) :
    Decidable (PostReleaseBoundaryComplete d) := by
  unfold PostReleaseBoundaryComplete
  infer_instance

def DossierAdmissible (d : ReleaseDossier) : Prop :=
  ArtifactComplete d ∧ AlternativesComplete d ∧ DerivativeReviewComplete d ∧
  DistributionReviewComplete d ∧ PostReleaseBoundaryComplete d

instance dossierAdmissibleDecidable (d : ReleaseDossier) : Decidable (DossierAdmissible d) := by
  unfold DossierAdmissible ArtifactComplete AlternativesComplete FrontierCurrent
    DerivativeReviewComplete DistributionReviewComplete PostReleaseBoundaryComplete
  infer_instance

def DossierReady (d : ReleaseDossier) : Bool := decide (DossierAdmissible d)

inductive ReviewState where
  | proposed | artifactReviewed | alternativesReviewed | derivativesReviewed
  | distributionReviewed | boundaryReviewed | repairRequired
  | eligibleForTheseusHarmlessReleaseCase
deriving DecidableEq, Repr

def ReviewStepFor (d : ReleaseDossier) : ReviewState -> ReviewState
  | .proposed => if decide (ArtifactComplete d) then .artifactReviewed else .repairRequired
  | .artifactReviewed =>
      if decide (AlternativesComplete d) then .alternativesReviewed else .repairRequired
  | .alternativesReviewed =>
      if decide (DerivativeReviewComplete d) then .derivativesReviewed else .repairRequired
  | .derivativesReviewed =>
      if decide (DistributionReviewComplete d) then .distributionReviewed else .repairRequired
  | .distributionReviewed =>
      if decide (PostReleaseBoundaryComplete d) then .boundaryReviewed else .repairRequired
  | .boundaryReviewed => .eligibleForTheseusHarmlessReleaseCase
  | state => state

def ReviewRun (d : ReleaseDossier) : Nat -> ReviewState
  | 0 => .proposed
  | n + 1 => ReviewStepFor d (ReviewRun d n)

def StageInvariant (d : ReleaseDossier) : ReviewState -> Prop
  | .proposed => True
  | .artifactReviewed => ArtifactComplete d
  | .alternativesReviewed => ArtifactComplete d ∧ AlternativesComplete d
  | .derivativesReviewed =>
      ArtifactComplete d ∧ AlternativesComplete d ∧ DerivativeReviewComplete d
  | .distributionReviewed =>
      ArtifactComplete d ∧ AlternativesComplete d ∧ DerivativeReviewComplete d ∧
        DistributionReviewComplete d
  | .boundaryReviewed => DossierAdmissible d
  | .eligibleForTheseusHarmlessReleaseCase => DossierAdmissible d
  | .repairRequired => True

theorem review_step_preserves_stage_invariant
    (d : ReleaseDossier) (state : ReviewState) (h : StageInvariant d state) :
    StageInvariant d (ReviewStepFor d state) := by
  cases state <;> simp only [ReviewStepFor]
  case proposed => split <;> simp_all [StageInvariant]
  case artifactReviewed => split <;> simp_all [StageInvariant]
  case alternativesReviewed => split <;> simp_all [StageInvariant]
  case derivativesReviewed => split <;> simp_all [StageInvariant]
  case distributionReviewed =>
    split <;> simp_all [StageInvariant, DossierAdmissible]
  all_goals simp_all [StageInvariant]

theorem review_run_preserves_stage_invariant (d : ReleaseDossier) (n : Nat) :
    StageInvariant d (ReviewRun d n) := by
  induction n with
  | zero => simp [ReviewRun, StageInvariant]
  | succ n ih => simpa [ReviewRun] using review_step_preserves_stage_invariant d _ ih

theorem simulation_eligibility_requires_admissible_dossier
    (d : ReleaseDossier) (n : Nat)
    (h : ReviewRun d n = .eligibleForTheseusHarmlessReleaseCase) :
    DossierAdmissible d := by
  have inv := review_run_preserves_stage_invariant d n
  simpa [h, StageInvariant] using inv

def completeDossier : ReleaseDossier := {}

theorem complete_dossier_is_ready : DossierReady completeDossier = true := by decide

theorem complete_dossier_reaches_only_harmless_release_case :
    ReviewRun completeDossier 6 = .eligibleForTheseusHarmlessReleaseCase := by decide

inductive AdmissionAxis where
  | exactWeights | tokenizer | configuration | inferenceCode | license | evaluationIdentity
  | noReleaseComparator | hostedComparator | gatedComparator | reducedComparator
  | accessibleFrontier | frontierExpiry | defaultCandidate | safetyRemovedVariant
  | maliciousFineTune | fineTunePositiveControl | scaffoldedVariant | adversaryBudget
  | derivativeResidual | benefitDistribution | affectedPopulation | marginalRisk
  | cumulativeRisk | safeguardPortability | independentReview | officialLineage
  | incidentRoute | patchSemantics | residualOwner | universalRecall | universalTelemetry
  | copyErasure | licenseKillSwitch | nonClaimBoundary | releaseAuthorization
  | supportPromotion
deriving DecidableEq, Repr

def omitAxis : AdmissionAxis -> ReleaseDossier
  | .exactWeights => { completeDossier with exactWeightsBound := false }
  | .tokenizer => { completeDossier with tokenizerBound := false }
  | .configuration => { completeDossier with configurationBound := false }
  | .inferenceCode => { completeDossier with inferenceCodeBound := false }
  | .license => { completeDossier with licenseBound := false }
  | .evaluationIdentity => { completeDossier with evaluationIdentityBound := false }
  | .noReleaseComparator => { completeDossier with noReleaseCompared := false }
  | .hostedComparator => { completeDossier with hostedAccessCompared := false }
  | .gatedComparator => { completeDossier with gatedAccessCompared := false }
  | .reducedComparator => { completeDossier with reducedArtifactCompared := false }
  | .accessibleFrontier => { completeDossier with accessibleFrontierBound := false }
  | .frontierExpiry => { completeDossier with frontierExpiresAt := 3 }
  | .defaultCandidate => { completeDossier with defaultCandidateEvaluated := false }
  | .safetyRemovedVariant => { completeDossier with safetyRemovedVariantEvaluated := false }
  | .maliciousFineTune => { completeDossier with maliciousFineTuneEvaluated := false }
  | .fineTunePositiveControl => { completeDossier with fineTunePositiveControlPassed := false }
  | .scaffoldedVariant => { completeDossier with scaffoldedVariantEvaluated := false }
  | .adversaryBudget => { completeDossier with adversaryBudgetBound := false }
  | .derivativeResidual => { completeDossier with derivativeResidualRecorded := false }
  | .benefitDistribution => { completeDossier with benefitDistributionRecorded := false }
  | .affectedPopulation => { completeDossier with affectedPopulationRecorded := false }
  | .marginalRisk => { completeDossier with marginalRiskRecorded := false }
  | .cumulativeRisk => { completeDossier with cumulativeRiskRecorded := false }
  | .safeguardPortability => { completeDossier with safeguardPortabilityRecorded := false }
  | .independentReview => { completeDossier with independentReviewPresent := false }
  | .officialLineage => { completeDossier with officialLineageRoutePresent := false }
  | .incidentRoute => { completeDossier with incidentRoutePresent := false }
  | .patchSemantics => { completeDossier with patchSemanticsRecorded := false }
  | .residualOwner => { completeDossier with residualOwnerPresent := false }
  | .universalRecall => { completeDossier with universalRecallClaimed := true }
  | .universalTelemetry => { completeDossier with universalTelemetryClaimed := true }
  | .copyErasure => { completeDossier with copyErasureClaimed := true }
  | .licenseKillSwitch => { completeDossier with licenseKillSwitchClaimed := true }
  | .nonClaimBoundary => { completeDossier with nonClaimBoundaryPresent := false }
  | .releaseAuthorization => { completeDossier with releaseAuthorizationRequested := true }
  | .supportPromotion => { completeDossier with supportPromotionRequested := true }

inductive RepairDisposition where
  | bindExactWeights | bindTokenizer | bindConfiguration | bindInferenceCode
  | bindLicense | bindEvaluationIdentity | addNoReleaseComparator
  | addHostedComparator | addGatedComparator | addReducedComparator
  | bindAccessibleFrontier | renewFrontier | evaluateDefaultCandidate
  | evaluateSafetyRemovedVariant | evaluateMaliciousFineTune
  | repairFineTunePositiveControl | evaluateScaffoldedVariant | bindAdversaryBudget
  | recordDerivativeResidual | recordBenefitDistribution | recordAffectedPopulation
  | recordMarginalRisk | recordCumulativeRisk | recordSafeguardPortability
  | assignIndependentReview | addOfficialLineage | addIncidentRoute
  | recordPatchSemantics | assignResidualOwner | rejectUniversalRecall
  | rejectUniversalTelemetry | rejectCopyErasure | rejectLicenseKillSwitch
  | recordNonClaimBoundary | refuseReleaseAuthorization | refuseSupportPromotion
  | eligibleForTheseusHarmlessReleaseCase
deriving DecidableEq, Repr

def repairForAxis : AdmissionAxis -> RepairDisposition
  | .exactWeights => .bindExactWeights | .tokenizer => .bindTokenizer
  | .configuration => .bindConfiguration | .inferenceCode => .bindInferenceCode
  | .license => .bindLicense | .evaluationIdentity => .bindEvaluationIdentity
  | .noReleaseComparator => .addNoReleaseComparator
  | .hostedComparator => .addHostedComparator | .gatedComparator => .addGatedComparator
  | .reducedComparator => .addReducedComparator | .accessibleFrontier => .bindAccessibleFrontier
  | .frontierExpiry => .renewFrontier | .defaultCandidate => .evaluateDefaultCandidate
  | .safetyRemovedVariant => .evaluateSafetyRemovedVariant
  | .maliciousFineTune => .evaluateMaliciousFineTune
  | .fineTunePositiveControl => .repairFineTunePositiveControl
  | .scaffoldedVariant => .evaluateScaffoldedVariant | .adversaryBudget => .bindAdversaryBudget
  | .derivativeResidual => .recordDerivativeResidual
  | .benefitDistribution => .recordBenefitDistribution
  | .affectedPopulation => .recordAffectedPopulation | .marginalRisk => .recordMarginalRisk
  | .cumulativeRisk => .recordCumulativeRisk
  | .safeguardPortability => .recordSafeguardPortability
  | .independentReview => .assignIndependentReview | .officialLineage => .addOfficialLineage
  | .incidentRoute => .addIncidentRoute | .patchSemantics => .recordPatchSemantics
  | .residualOwner => .assignResidualOwner | .universalRecall => .rejectUniversalRecall
  | .universalTelemetry => .rejectUniversalTelemetry | .copyErasure => .rejectCopyErasure
  | .licenseKillSwitch => .rejectLicenseKillSwitch
  | .nonClaimBoundary => .recordNonClaimBoundary
  | .releaseAuthorization => .refuseReleaseAuthorization
  | .supportPromotion => .refuseSupportPromotion

def ExactRepairFor (d : ReleaseDossier) : RepairDisposition :=
  if !d.exactWeightsBound then .bindExactWeights else if !d.tokenizerBound then .bindTokenizer
  else if !d.configurationBound then .bindConfiguration else if !d.inferenceCodeBound then .bindInferenceCode
  else if !d.licenseBound then .bindLicense else if !d.evaluationIdentityBound then .bindEvaluationIdentity
  else if !d.noReleaseCompared then .addNoReleaseComparator else if !d.hostedAccessCompared then .addHostedComparator
  else if !d.gatedAccessCompared then .addGatedComparator else if !d.reducedArtifactCompared then .addReducedComparator
  else if !d.accessibleFrontierBound then .bindAccessibleFrontier else if !decide (FrontierCurrent d) then .renewFrontier
  else if !d.defaultCandidateEvaluated then .evaluateDefaultCandidate else if !d.safetyRemovedVariantEvaluated then .evaluateSafetyRemovedVariant
  else if !d.maliciousFineTuneEvaluated then .evaluateMaliciousFineTune else if !d.fineTunePositiveControlPassed then .repairFineTunePositiveControl
  else if !d.scaffoldedVariantEvaluated then .evaluateScaffoldedVariant else if !d.adversaryBudgetBound then .bindAdversaryBudget
  else if !d.derivativeResidualRecorded then .recordDerivativeResidual else if !d.benefitDistributionRecorded then .recordBenefitDistribution
  else if !d.affectedPopulationRecorded then .recordAffectedPopulation else if !d.marginalRiskRecorded then .recordMarginalRisk
  else if !d.cumulativeRiskRecorded then .recordCumulativeRisk else if !d.safeguardPortabilityRecorded then .recordSafeguardPortability
  else if !d.independentReviewPresent then .assignIndependentReview else if !d.officialLineageRoutePresent then .addOfficialLineage
  else if !d.incidentRoutePresent then .addIncidentRoute else if !d.patchSemanticsRecorded then .recordPatchSemantics
  else if !d.residualOwnerPresent then .assignResidualOwner else if d.universalRecallClaimed then .rejectUniversalRecall
  else if d.universalTelemetryClaimed then .rejectUniversalTelemetry else if d.copyErasureClaimed then .rejectCopyErasure
  else if d.licenseKillSwitchClaimed then .rejectLicenseKillSwitch else if !d.nonClaimBoundaryPresent then .recordNonClaimBoundary
  else if d.releaseAuthorizationRequested then .refuseReleaseAuthorization else if d.supportPromotionRequested then .refuseSupportPromotion
  else .eligibleForTheseusHarmlessReleaseCase

theorem every_admission_axis_mutation_blocks_readiness (axis : AdmissionAxis) :
    DossierReady (omitAxis axis) = false := by cases axis <;> decide

theorem every_admission_axis_mutation_has_exact_repair (axis : AdmissionAxis) :
    ExactRepairFor (omitAxis axis) = repairForAxis axis := by cases axis <;> decide

theorem every_admission_axis_mutation_reaches_repair (axis : AdmissionAxis) :
    ReviewRun (omitAxis axis) 6 = .repairRequired := by cases axis <;> decide

theorem readiness_requires_artifact (d : ReleaseDossier) (h : DossierReady d = true) :
    ArtifactComplete d := by exact (of_decide_eq_true h).1

theorem readiness_requires_alternatives (d : ReleaseDossier) (h : DossierReady d = true) :
    AlternativesComplete d := by exact (of_decide_eq_true h).2.1

theorem readiness_requires_derivative_review (d : ReleaseDossier) (h : DossierReady d = true) :
    DerivativeReviewComplete d := by exact (of_decide_eq_true h).2.2.1

theorem readiness_requires_distribution_review (d : ReleaseDossier) (h : DossierReady d = true) :
    DistributionReviewComplete d := by exact (of_decide_eq_true h).2.2.2.1

theorem readiness_requires_post_release_boundary (d : ReleaseDossier) (h : DossierReady d = true) :
    PostReleaseBoundaryComplete d := by exact (of_decide_eq_true h).2.2.2.2

theorem expired_frontier_remains_expired_when_time_advances
    (d : ReleaseDossier) (later : Nat) (expired : d.frontierExpiresAt < d.currentTick)
    (advances : d.currentTick <= later) :
    ¬ FrontierCurrent { d with currentTick := later } := by
  intro current
  unfold FrontierCurrent at current
  change later <= d.frontierExpiresAt at current
  omega

def UniversallyRecallable (publicCopyCount : Nat) : Prop := publicCopyCount = 0

theorem public_copy_irreversibility_is_monotone
    (copies laterCopies : Nat) (published : 0 < copies) (copiesPersist : copies <= laterCopies) :
    ¬ UniversallyRecallable laterCopies := by
  intro recalled
  unfold UniversallyRecallable at recalled
  omega

structure OfficialLineage where
  signer : Nat
  digest : Nat
deriving DecidableEq, Repr

structure EcosystemState where
  official : OfficialLineage
  uncontrolledCopies : Nat
deriving DecidableEq, Repr

def sharedLineage : OfficialLineage := { signer := 7, digest := 11 }
def controlledState : EcosystemState := { official := sharedLineage, uncontrolledCopies := 0 }
def copiedState : EcosystemState := { official := sharedLineage, uncontrolledCopies := 3 }
def UniversalControl (state : EcosystemState) : Bool := state.uncontrolledCopies == 0

theorem identical_official_lineage_can_hide_opposite_copy_control :
    controlledState.official = copiedState.official ∧ UniversalControl controlledState = true ∧
      UniversalControl copiedState = false := by decide

theorem official_lineage_cannot_recover_universal_copy_control
    (classify : OfficialLineage -> Bool) :
    ¬ (∀ state, classify state.official = UniversalControl state) := by
  intro exact
  have a := exact controlledState
  have b := exact copiedState
  simp [controlledState, copiedState, sharedLineage, UniversalControl] at a b
  rw [a] at b
  contradiction

structure DefaultEvaluation where
  score : Nat
deriving DecidableEq, Repr

structure DerivativeCase where
  default : DefaultEvaluation
  safeguardRemoved : Bool
deriving DecidableEq, Repr
def sharedDefault : DefaultEvaluation := { score := 90 }
def retainedCase : DerivativeCase := { default := sharedDefault, safeguardRemoved := false }
def removedCase : DerivativeCase := { default := sharedDefault, safeguardRemoved := true }

theorem identical_default_evaluation_can_hide_opposite_derivative_state :
    retainedCase.default = removedCase.default ∧ retainedCase.safeguardRemoved = false ∧
      removedCase.safeguardRemoved = true := by decide

theorem default_evaluation_cannot_recover_derivative_safeguard_state
    (classify : DefaultEvaluation -> Bool) :
    ¬ (∀ (c : DerivativeCase), classify c.default = c.safeguardRemoved) := by
  intro exact
  have a := exact retainedCase
  have b := exact removedCase
  simp [retainedCase, removedCase, sharedDefault] at a b
  rw [a] at b
  contradiction

end AsiStackProofs.OpenWeightReleaseReview
