namespace AsiStackProofs.DangerousCapabilityReview

structure CapabilityDossier where
  campaignRequested : Bool := true
  modelIdentityBound : Bool := true
  checkpointIdentityBound : Bool := true
  scaffoldIdentityBound : Bool := true
  toolAccessBound : Bool := true
  threatModelVersionCurrent : Bool := true
  domainsSeparated : Bool := true
  actorCohortBound : Bool := true
  expertiseStrataBound : Bool := true
  safeguardComparatorBound : Bool := true
  unassistedBaselinePresent : Bool := true
  accessibleFrontierBaselinePresent : Bool := true
  elicitationBudgetFrozen : Bool := true
  positiveControlPassed : Bool := true
  negativeControlPassed : Bool := true
  taskValidityReviewed : Bool := true
  attemptDenominator : Nat := 4
  attemptsRetained : Nat := 4
  outcomeAxesSeparated : Bool := true
  independentEvaluator : Bool := true
  informationHazardCustodyPresent : Bool := true
  uncertaintyBoundPresent : Bool := true
  currentTick : Nat := 5
  expiresAt : Nat := 8
  maximumInferencePresent : Bool := true
  residualCustodyPresent : Bool := true
  nonClaimBoundaryPresent : Bool := true
  supportAssignmentRequested : Bool := false
  releaseAuthorityRequested : Bool := false
  operationalDetailPublicationRequested : Bool := false
deriving DecidableEq, Repr

def AttemptsComplete (dossier : CapabilityDossier) : Prop :=
  0 < dossier.attemptDenominator ∧
    dossier.attemptsRetained = dossier.attemptDenominator

instance attemptsCompleteDecidable (dossier : CapabilityDossier) :
    Decidable (AttemptsComplete dossier) := by
  unfold AttemptsComplete
  infer_instance

def DossierCurrent (dossier : CapabilityDossier) : Prop :=
  dossier.currentTick <= dossier.expiresAt

instance dossierCurrentDecidable (dossier : CapabilityDossier) :
    Decidable (DossierCurrent dossier) := by
  unfold DossierCurrent
  infer_instance

def IdentityComplete (dossier : CapabilityDossier) : Prop :=
  dossier.campaignRequested = true ∧
    dossier.modelIdentityBound = true ∧
      dossier.checkpointIdentityBound = true ∧
        dossier.scaffoldIdentityBound = true ∧
          dossier.toolAccessBound = true

def ThreatComplete (dossier : CapabilityDossier) : Prop :=
  dossier.threatModelVersionCurrent = true ∧
    dossier.domainsSeparated = true ∧
      dossier.actorCohortBound = true ∧
        dossier.expertiseStrataBound = true ∧
          dossier.safeguardComparatorBound = true

def BaselineComplete (dossier : CapabilityDossier) : Prop :=
  dossier.unassistedBaselinePresent = true ∧
    dossier.accessibleFrontierBaselinePresent = true

def InstrumentComplete (dossier : CapabilityDossier) : Prop :=
  dossier.elicitationBudgetFrozen = true ∧
    dossier.positiveControlPassed = true ∧
      dossier.negativeControlPassed = true ∧
        dossier.taskValidityReviewed = true ∧
          AttemptsComplete dossier ∧
            dossier.outcomeAxesSeparated = true ∧
              dossier.independentEvaluator = true

def CustodyComplete (dossier : CapabilityDossier) : Prop :=
  dossier.informationHazardCustodyPresent = true ∧
    dossier.uncertaintyBoundPresent = true ∧
      DossierCurrent dossier

def BoundaryComplete (dossier : CapabilityDossier) : Prop :=
  dossier.maximumInferencePresent = true ∧
    dossier.residualCustodyPresent = true ∧
      dossier.nonClaimBoundaryPresent = true ∧
        dossier.supportAssignmentRequested = false ∧
          dossier.releaseAuthorityRequested = false ∧
            dossier.operationalDetailPublicationRequested = false

def DossierAdmissible (dossier : CapabilityDossier) : Prop :=
  IdentityComplete dossier ∧
    ThreatComplete dossier ∧
      BaselineComplete dossier ∧
        InstrumentComplete dossier ∧
          CustodyComplete dossier ∧
            BoundaryComplete dossier

instance dossierAdmissibleDecidable (dossier : CapabilityDossier) :
    Decidable (DossierAdmissible dossier) := by
  unfold DossierAdmissible IdentityComplete ThreatComplete BaselineComplete
    InstrumentComplete CustodyComplete BoundaryComplete
  infer_instance

def DossierReady (dossier : CapabilityDossier) : Bool :=
  decide (DossierAdmissible dossier)

inductive ReviewState where
  | proposed
  | identityReviewed
  | threatReviewed
  | baselineReviewed
  | instrumentReviewed
  | custodyReviewed
  | boundaryReviewed
  | refusedNoCampaign
  | repairModelIdentity
  | repairCheckpointIdentity
  | repairScaffoldIdentity
  | repairToolAccess
  | renewThreatModel
  | separateDomains
  | bindActorCohort
  | bindExpertiseStrata
  | bindSafeguardComparator
  | addUnassistedBaseline
  | addAccessibleFrontierBaseline
  | freezeElicitationBudget
  | repairPositiveControl
  | repairNegativeControl
  | reviewTaskValidity
  | requirePositiveAttemptDenominator
  | retainAllAttempts
  | separateOutcomeAxes
  | assignIndependentEvaluator
  | assignInformationHazardCustody
  | bindUncertainty
  | renewExpiredDossier
  | recordMaximumInference
  | assignResidualCustody
  | recordNonClaimBoundary
  | refuseSupportAssignment
  | refuseReleaseAuthority
  | refuseOperationalDetailPublication
  | eligibleForTheseusHarmlessAnalogueCampaign
deriving DecidableEq, Repr

def ReviewStepFor (dossier : CapabilityDossier) : ReviewState -> ReviewState
  | .proposed =>
      if ! dossier.campaignRequested then .refusedNoCampaign
      else if ! dossier.modelIdentityBound then .repairModelIdentity
      else if ! dossier.checkpointIdentityBound then .repairCheckpointIdentity
      else if ! dossier.scaffoldIdentityBound then .repairScaffoldIdentity
      else if ! dossier.toolAccessBound then .repairToolAccess
      else .identityReviewed
  | .identityReviewed =>
      if ! dossier.threatModelVersionCurrent then .renewThreatModel
      else if ! dossier.domainsSeparated then .separateDomains
      else if ! dossier.actorCohortBound then .bindActorCohort
      else if ! dossier.expertiseStrataBound then .bindExpertiseStrata
      else if ! dossier.safeguardComparatorBound then .bindSafeguardComparator
      else .threatReviewed
  | .threatReviewed =>
      if ! dossier.unassistedBaselinePresent then .addUnassistedBaseline
      else if ! dossier.accessibleFrontierBaselinePresent then
        .addAccessibleFrontierBaseline
      else .baselineReviewed
  | .baselineReviewed =>
      if ! dossier.elicitationBudgetFrozen then .freezeElicitationBudget
      else if ! dossier.positiveControlPassed then .repairPositiveControl
      else if ! dossier.negativeControlPassed then .repairNegativeControl
      else if ! dossier.taskValidityReviewed then .reviewTaskValidity
      else if dossier.attemptDenominator == 0 then .requirePositiveAttemptDenominator
      else if dossier.attemptsRetained != dossier.attemptDenominator then .retainAllAttempts
      else if ! dossier.outcomeAxesSeparated then .separateOutcomeAxes
      else if ! dossier.independentEvaluator then .assignIndependentEvaluator
      else .instrumentReviewed
  | .instrumentReviewed =>
      if ! dossier.informationHazardCustodyPresent then
        .assignInformationHazardCustody
      else if ! dossier.uncertaintyBoundPresent then .bindUncertainty
      else if ! decide (DossierCurrent dossier) then .renewExpiredDossier
      else .custodyReviewed
  | .custodyReviewed =>
      if ! dossier.maximumInferencePresent then .recordMaximumInference
      else if ! dossier.residualCustodyPresent then .assignResidualCustody
      else if ! dossier.nonClaimBoundaryPresent then .recordNonClaimBoundary
      else if dossier.supportAssignmentRequested then .refuseSupportAssignment
      else if dossier.releaseAuthorityRequested then .refuseReleaseAuthority
      else if dossier.operationalDetailPublicationRequested then
        .refuseOperationalDetailPublication
      else .boundaryReviewed
  | .boundaryReviewed => .eligibleForTheseusHarmlessAnalogueCampaign
  | state => state

def ReviewRun (dossier : CapabilityDossier) : Nat -> ReviewState
  | 0 => .proposed
  | steps + 1 => ReviewStepFor dossier (ReviewRun dossier steps)

def ReviewStageInvariant
    (dossier : CapabilityDossier) : ReviewState -> Prop
  | .proposed => True
  | .identityReviewed => IdentityComplete dossier
  | .threatReviewed => IdentityComplete dossier ∧ ThreatComplete dossier
  | .baselineReviewed =>
      IdentityComplete dossier ∧ ThreatComplete dossier ∧ BaselineComplete dossier
  | .instrumentReviewed =>
      IdentityComplete dossier ∧ ThreatComplete dossier ∧ BaselineComplete dossier ∧
        InstrumentComplete dossier
  | .custodyReviewed =>
      IdentityComplete dossier ∧ ThreatComplete dossier ∧ BaselineComplete dossier ∧
        InstrumentComplete dossier ∧ CustodyComplete dossier
  | .boundaryReviewed => DossierAdmissible dossier
  | .eligibleForTheseusHarmlessAnalogueCampaign => DossierAdmissible dossier
  | _ => True

theorem review_step_preserves_stage_invariant
    (dossier : CapabilityDossier) (state : ReviewState)
    (invariant : ReviewStageInvariant dossier state) :
    ReviewStageInvariant dossier (ReviewStepFor dossier state) := by
  cases state <;> simp only [ReviewStepFor]
  all_goals
    repeat' split
  all_goals
    simp_all [ReviewStageInvariant, DossierAdmissible, IdentityComplete,
      ThreatComplete, BaselineComplete, InstrumentComplete, CustodyComplete,
      BoundaryComplete, AttemptsComplete, DossierCurrent]
  all_goals omega

theorem review_run_preserves_stage_invariant
    (dossier : CapabilityDossier) (steps : Nat) :
    ReviewStageInvariant dossier (ReviewRun dossier steps) := by
  induction steps with
  | zero => simp [ReviewRun, ReviewStageInvariant]
  | succ steps ih =>
      simpa [ReviewRun] using
        review_step_preserves_stage_invariant dossier (ReviewRun dossier steps) ih

theorem campaign_eligibility_requires_admissible_dossier
    (dossier : CapabilityDossier) (steps : Nat)
    (eligible :
      ReviewRun dossier steps = .eligibleForTheseusHarmlessAnalogueCampaign) :
    DossierAdmissible dossier := by
  have invariant := review_run_preserves_stage_invariant dossier steps
  simpa [eligible, ReviewStageInvariant] using invariant

theorem admissible_dossier_is_ready
    (dossier : CapabilityDossier)
    (admissible : DossierAdmissible dossier) :
    DossierReady dossier = true := by
  exact decide_eq_true admissible

def completeDossier : CapabilityDossier := {}

theorem complete_dossier_is_ready :
    DossierReady completeDossier = true := by decide

theorem complete_dossier_reaches_only_harmless_analogue_campaign :
    ReviewRun completeDossier 7 =
      .eligibleForTheseusHarmlessAnalogueCampaign := by decide

inductive AdmissionAxis where
  | campaignRequest
  | modelIdentity
  | checkpointIdentity
  | scaffoldIdentity
  | toolAccess
  | threatModelVersion
  | domainSeparation
  | actorCohort
  | expertiseStrata
  | safeguardComparator
  | unassistedBaseline
  | accessibleFrontierBaseline
  | elicitationBudget
  | positiveControl
  | negativeControl
  | taskValidity
  | attemptDenominator
  | attemptRetention
  | outcomeAxisSeparation
  | independentEvaluator
  | informationHazardCustody
  | uncertaintyBound
  | expiry
  | maximumInference
  | residualCustody
  | nonClaimBoundary
  | supportAssignment
  | releaseAuthority
  | operationalDetailPublication
deriving DecidableEq, Repr

def omitAdmissionAxis : AdmissionAxis -> CapabilityDossier
  | .campaignRequest => { completeDossier with campaignRequested := false }
  | .modelIdentity => { completeDossier with modelIdentityBound := false }
  | .checkpointIdentity => { completeDossier with checkpointIdentityBound := false }
  | .scaffoldIdentity => { completeDossier with scaffoldIdentityBound := false }
  | .toolAccess => { completeDossier with toolAccessBound := false }
  | .threatModelVersion => { completeDossier with threatModelVersionCurrent := false }
  | .domainSeparation => { completeDossier with domainsSeparated := false }
  | .actorCohort => { completeDossier with actorCohortBound := false }
  | .expertiseStrata => { completeDossier with expertiseStrataBound := false }
  | .safeguardComparator => { completeDossier with safeguardComparatorBound := false }
  | .unassistedBaseline => { completeDossier with unassistedBaselinePresent := false }
  | .accessibleFrontierBaseline =>
      { completeDossier with accessibleFrontierBaselinePresent := false }
  | .elicitationBudget => { completeDossier with elicitationBudgetFrozen := false }
  | .positiveControl => { completeDossier with positiveControlPassed := false }
  | .negativeControl => { completeDossier with negativeControlPassed := false }
  | .taskValidity => { completeDossier with taskValidityReviewed := false }
  | .attemptDenominator => { completeDossier with attemptDenominator := 0 }
  | .attemptRetention => { completeDossier with attemptsRetained := 3 }
  | .outcomeAxisSeparation => { completeDossier with outcomeAxesSeparated := false }
  | .independentEvaluator => { completeDossier with independentEvaluator := false }
  | .informationHazardCustody =>
      { completeDossier with informationHazardCustodyPresent := false }
  | .uncertaintyBound => { completeDossier with uncertaintyBoundPresent := false }
  | .expiry => { completeDossier with expiresAt := 4 }
  | .maximumInference => { completeDossier with maximumInferencePresent := false }
  | .residualCustody => { completeDossier with residualCustodyPresent := false }
  | .nonClaimBoundary => { completeDossier with nonClaimBoundaryPresent := false }
  | .supportAssignment => { completeDossier with supportAssignmentRequested := true }
  | .releaseAuthority => { completeDossier with releaseAuthorityRequested := true }
  | .operationalDetailPublication =>
      { completeDossier with operationalDetailPublicationRequested := true }

def repairStateForAxis : AdmissionAxis -> ReviewState
  | .campaignRequest => .refusedNoCampaign
  | .modelIdentity => .repairModelIdentity
  | .checkpointIdentity => .repairCheckpointIdentity
  | .scaffoldIdentity => .repairScaffoldIdentity
  | .toolAccess => .repairToolAccess
  | .threatModelVersion => .renewThreatModel
  | .domainSeparation => .separateDomains
  | .actorCohort => .bindActorCohort
  | .expertiseStrata => .bindExpertiseStrata
  | .safeguardComparator => .bindSafeguardComparator
  | .unassistedBaseline => .addUnassistedBaseline
  | .accessibleFrontierBaseline => .addAccessibleFrontierBaseline
  | .elicitationBudget => .freezeElicitationBudget
  | .positiveControl => .repairPositiveControl
  | .negativeControl => .repairNegativeControl
  | .taskValidity => .reviewTaskValidity
  | .attemptDenominator => .requirePositiveAttemptDenominator
  | .attemptRetention => .retainAllAttempts
  | .outcomeAxisSeparation => .separateOutcomeAxes
  | .independentEvaluator => .assignIndependentEvaluator
  | .informationHazardCustody => .assignInformationHazardCustody
  | .uncertaintyBound => .bindUncertainty
  | .expiry => .renewExpiredDossier
  | .maximumInference => .recordMaximumInference
  | .residualCustody => .assignResidualCustody
  | .nonClaimBoundary => .recordNonClaimBoundary
  | .supportAssignment => .refuseSupportAssignment
  | .releaseAuthority => .refuseReleaseAuthority
  | .operationalDetailPublication => .refuseOperationalDetailPublication

theorem every_admission_axis_mutation_blocks_readiness (axis : AdmissionAxis) :
    DossierReady (omitAdmissionAxis axis) = false := by
  cases axis <;> decide

theorem every_admission_axis_mutation_reaches_exact_repair (axis : AdmissionAxis) :
    ReviewRun (omitAdmissionAxis axis) 7 = repairStateForAxis axis := by
  cases axis <;> decide

theorem every_admission_axis_mutation_blocks_campaign_eligibility
    (axis : AdmissionAxis) :
    ReviewRun (omitAdmissionAxis axis) 7 !=
      .eligibleForTheseusHarmlessAnalogueCampaign := by
  cases axis <;> decide

theorem readiness_requires_identity_review
    (dossier : CapabilityDossier) (ready : DossierReady dossier = true) :
    IdentityComplete dossier := by
  have admissible : DossierAdmissible dossier := of_decide_eq_true ready
  exact admissible.1

theorem readiness_requires_threat_review
    (dossier : CapabilityDossier) (ready : DossierReady dossier = true) :
    ThreatComplete dossier := by
  have admissible : DossierAdmissible dossier := of_decide_eq_true ready
  exact admissible.2.1

theorem readiness_requires_baselines
    (dossier : CapabilityDossier) (ready : DossierReady dossier = true) :
    BaselineComplete dossier := by
  have admissible : DossierAdmissible dossier := of_decide_eq_true ready
  exact admissible.2.2.1

theorem readiness_requires_instrument_competence
    (dossier : CapabilityDossier) (ready : DossierReady dossier = true) :
    InstrumentComplete dossier := by
  have admissible : DossierAdmissible dossier := of_decide_eq_true ready
  exact admissible.2.2.2.1

theorem readiness_requires_custody_and_currentness
    (dossier : CapabilityDossier) (ready : DossierReady dossier = true) :
    CustodyComplete dossier := by
  have admissible : DossierAdmissible dossier := of_decide_eq_true ready
  exact admissible.2.2.2.2.1

theorem readiness_requires_non_authorizing_boundary
    (dossier : CapabilityDossier) (ready : DossierReady dossier = true) :
    BoundaryComplete dossier := by
  have admissible : DossierAdmissible dossier := of_decide_eq_true ready
  exact admissible.2.2.2.2.2

theorem expired_dossier_remains_expired_when_time_advances
    (dossier : CapabilityDossier) (laterTick : Nat)
    (expired : dossier.expiresAt < dossier.currentTick)
    (later : dossier.currentTick <= laterTick) :
    ¬ DossierCurrent { dossier with currentTick := laterTick } := by
  intro current
  unfold DossierCurrent at current
  change laterTick <= dossier.expiresAt at current
  omega

theorem attempt_shortfall_persists_when_retention_decreases
    (dossier : CapabilityDossier) (fewerRetained : Nat)
    (fewer : fewerRetained <= dossier.attemptsRetained)
    (shortfall : dossier.attemptsRetained < dossier.attemptDenominator) :
    ¬ AttemptsComplete { dossier with attemptsRetained := fewerRetained } := by
  intro complete
  unfold AttemptsComplete at complete
  change 0 < dossier.attemptDenominator ∧
    fewerRetained = dossier.attemptDenominator at complete
  omega

structure OutcomeVector where
  capability : Nat
  propensity : Nat
  safeguardBypass : Nat
  actorUplift : Nat
  realizedHarm : Nat
deriving DecidableEq, Repr

def AggregateScore (outcome : OutcomeVector) : Nat :=
  outcome.capability + outcome.propensity + outcome.safeguardBypass +
    outcome.actorUplift + outcome.realizedHarm

def RequiresComponentReview (outcome : OutcomeVector) : Bool :=
  decide (3 <= outcome.safeguardBypass ∨ 3 <= outcome.actorUplift)

def upliftConcentrated : OutcomeVector where
  capability := 0
  propensity := 0
  safeguardBypass := 0
  actorUplift := 4
  realizedHarm := 0

def capabilityConcentrated : OutcomeVector where
  capability := 4
  propensity := 0
  safeguardBypass := 0
  actorUplift := 0
  realizedHarm := 0

theorem equal_aggregate_score_can_hide_distinct_outcome_vectors :
    AggregateScore upliftConcentrated = AggregateScore capabilityConcentrated ∧
      upliftConcentrated != capabilityConcentrated := by decide

theorem equal_aggregate_score_can_require_opposite_component_reviews :
    RequiresComponentReview upliftConcentrated = true ∧
      RequiresComponentReview capabilityConcentrated = false := by decide

theorem aggregate_score_cannot_recover_component_sensitive_review
    (classify : Nat -> Bool) :
    ¬ (∀ outcome, classify (AggregateScore outcome) = RequiresComponentReview outcome) := by
  intro exactForEveryOutcome
  have upliftCase := exactForEveryOutcome upliftConcentrated
  have capabilityCase := exactForEveryOutcome capabilityConcentrated
  simp [AggregateScore, RequiresComponentReview, upliftConcentrated,
    capabilityConcentrated] at upliftCase capabilityCase
  rw [upliftCase] at capabilityCase
  contradiction

end AsiStackProofs.DangerousCapabilityReview
