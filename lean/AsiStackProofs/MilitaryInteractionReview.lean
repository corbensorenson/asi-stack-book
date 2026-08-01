namespace AsiStackProofs.MilitaryInteractionReview

structure InteractionDossier where
  simulationRequested : Bool := true
  publicSafeNonOperationalScenario : Bool := true
  missionIdentityBound : Bool := true
  decisionRoleBound : Bool := true
  affectedPopulationBound : Bool := true
  legalBoundaryRecorded : Bool := true
  accountableAuthorityBound : Bool := true
  effectEnvelopeBound : Bool := true
  authorityExpansionRequested : Bool := false
  humanInterfacePresent : Bool := true
  humanAuthorityPresent : Bool := true
  requiredDecisionTime : Nat := 3
  availableDecisionTime : Nat := 5
  humanInformationSufficient : Bool := true
  humanCompetenceBound : Bool := true
  humanAttentionAvailable : Bool := true
  interventionReachable : Bool := true
  alternativesPresent : Bool := true
  independentJudgmentPossible : Bool := true
  sensorProvenanceBound : Bool := true
  sensorDependenciesRecorded : Bool := true
  uncertaintyVisible : Bool := true
  corroborationPolicyBound : Bool := true
  abstentionRoutePresent : Bool := true
  communicationLossPosturePresent : Bool := true
  integrityFailurePosturePresent : Bool := true
  suspensionAuthorityPresent : Bool := true
  adversaryModelSetPresent : Bool := true
  doctrineVariantsPresent : Bool := true
  reciprocalEffectsTracked : Bool := true
  requiredOffRampCount : Nat := 2
  availableOffRampCount : Nat := 3
  proliferationResidualTracked : Bool := true
  independentReviewPresent : Bool := true
  restrictedEvidenceCustodyPresent : Bool := true
  currentTick : Nat := 5
  expiresAt : Nat := 8
  publicMaximumInferencePresent : Bool := true
  incidentAndRemedyRoutePresent : Bool := true
  decommissionRoutePresent : Bool := true
  residualCustodyPresent : Bool := true
  nonClaimBoundaryPresent : Bool := true
  weaponAuthorizationRequested : Bool := false
  lawfulUseClaimRequested : Bool := false
  strategicStabilityClaimRequested : Bool := false
  supportAssignmentRequested : Bool := false
  releaseAuthorityRequested : Bool := false
  operationalDetailPublicationRequested : Bool := false
deriving DecidableEq, Repr

def DecisionTimeSufficient (dossier : InteractionDossier) : Prop :=
  0 < dossier.requiredDecisionTime ∧
    dossier.requiredDecisionTime <= dossier.availableDecisionTime

instance decisionTimeSufficientDecidable (dossier : InteractionDossier) :
    Decidable (DecisionTimeSufficient dossier) := by
  unfold DecisionTimeSufficient
  infer_instance

def OffRampsSufficient (dossier : InteractionDossier) : Prop :=
  0 < dossier.requiredOffRampCount ∧
    dossier.requiredOffRampCount <= dossier.availableOffRampCount

instance offRampsSufficientDecidable (dossier : InteractionDossier) :
    Decidable (OffRampsSufficient dossier) := by
  unfold OffRampsSufficient
  infer_instance

def DossierCurrent (dossier : InteractionDossier) : Prop :=
  dossier.currentTick <= dossier.expiresAt

instance dossierCurrentDecidable (dossier : InteractionDossier) :
    Decidable (DossierCurrent dossier) := by
  unfold DossierCurrent
  infer_instance

def ScopeComplete (dossier : InteractionDossier) : Prop :=
  dossier.simulationRequested = true ∧
    dossier.publicSafeNonOperationalScenario = true ∧
      dossier.missionIdentityBound = true ∧
        dossier.decisionRoleBound = true ∧
          dossier.affectedPopulationBound = true ∧
            dossier.legalBoundaryRecorded = true

instance scopeCompleteDecidable (dossier : InteractionDossier) :
    Decidable (ScopeComplete dossier) := by
  unfold ScopeComplete
  infer_instance

def AuthorityComplete (dossier : InteractionDossier) : Prop :=
  dossier.accountableAuthorityBound = true ∧
    dossier.effectEnvelopeBound = true ∧
      dossier.authorityExpansionRequested = false

instance authorityCompleteDecidable (dossier : InteractionDossier) :
    Decidable (AuthorityComplete dossier) := by
  unfold AuthorityComplete
  infer_instance

def MeaningfulHumanJudgment (dossier : InteractionDossier) : Prop :=
  dossier.humanInterfacePresent = true ∧
    dossier.humanAuthorityPresent = true ∧
      DecisionTimeSufficient dossier ∧
        dossier.humanInformationSufficient = true ∧
          dossier.humanCompetenceBound = true ∧
            dossier.humanAttentionAvailable = true ∧
              dossier.interventionReachable = true ∧
                dossier.alternativesPresent = true ∧
                  dossier.independentJudgmentPossible = true

instance meaningfulHumanJudgmentDecidable (dossier : InteractionDossier) :
    Decidable (MeaningfulHumanJudgment dossier) := by
  unfold MeaningfulHumanJudgment DecisionTimeSufficient
  infer_instance

def ObservationComplete (dossier : InteractionDossier) : Prop :=
  dossier.sensorProvenanceBound = true ∧
    dossier.sensorDependenciesRecorded = true ∧
      dossier.uncertaintyVisible = true ∧
        dossier.corroborationPolicyBound = true

instance observationCompleteDecidable (dossier : InteractionDossier) :
    Decidable (ObservationComplete dossier) := by
  unfold ObservationComplete
  infer_instance

def SafePostureComplete (dossier : InteractionDossier) : Prop :=
  dossier.abstentionRoutePresent = true ∧
    dossier.communicationLossPosturePresent = true ∧
      dossier.integrityFailurePosturePresent = true ∧
        dossier.suspensionAuthorityPresent = true

instance safePostureCompleteDecidable (dossier : InteractionDossier) :
    Decidable (SafePostureComplete dossier) := by
  unfold SafePostureComplete
  infer_instance

def InteractionComplete (dossier : InteractionDossier) : Prop :=
  dossier.adversaryModelSetPresent = true ∧
    dossier.doctrineVariantsPresent = true ∧
      dossier.reciprocalEffectsTracked = true ∧
        OffRampsSufficient dossier ∧
          dossier.proliferationResidualTracked = true

instance interactionCompleteDecidable (dossier : InteractionDossier) :
    Decidable (InteractionComplete dossier) := by
  unfold InteractionComplete OffRampsSufficient
  infer_instance

def CustodyAndBoundaryComplete (dossier : InteractionDossier) : Prop :=
  dossier.independentReviewPresent = true ∧
    dossier.restrictedEvidenceCustodyPresent = true ∧
      DossierCurrent dossier ∧
        dossier.publicMaximumInferencePresent = true ∧
          dossier.incidentAndRemedyRoutePresent = true ∧
            dossier.decommissionRoutePresent = true ∧
              dossier.residualCustodyPresent = true ∧
                dossier.nonClaimBoundaryPresent = true ∧
                  dossier.weaponAuthorizationRequested = false ∧
                    dossier.lawfulUseClaimRequested = false ∧
                      dossier.strategicStabilityClaimRequested = false ∧
                        dossier.supportAssignmentRequested = false ∧
                          dossier.releaseAuthorityRequested = false ∧
                            dossier.operationalDetailPublicationRequested = false

instance custodyAndBoundaryCompleteDecidable (dossier : InteractionDossier) :
    Decidable (CustodyAndBoundaryComplete dossier) := by
  unfold CustodyAndBoundaryComplete DossierCurrent
  infer_instance

def DossierAdmissible (dossier : InteractionDossier) : Prop :=
  ScopeComplete dossier ∧
    AuthorityComplete dossier ∧
      MeaningfulHumanJudgment dossier ∧
        ObservationComplete dossier ∧
          SafePostureComplete dossier ∧
            InteractionComplete dossier ∧
              CustodyAndBoundaryComplete dossier

instance dossierAdmissibleDecidable (dossier : InteractionDossier) :
    Decidable (DossierAdmissible dossier) := by
  unfold DossierAdmissible ScopeComplete AuthorityComplete MeaningfulHumanJudgment
    DecisionTimeSufficient ObservationComplete SafePostureComplete InteractionComplete
    OffRampsSufficient CustodyAndBoundaryComplete DossierCurrent
  infer_instance

def DossierReady (dossier : InteractionDossier) : Bool :=
  decide (DossierAdmissible dossier)

inductive ReviewState where
  | proposed
  | scopeReviewed
  | authorityReviewed
  | judgmentReviewed
  | observationReviewed
  | safePostureReviewed
  | interactionReviewed
  | custodyReviewed
  | refusedNoSimulation
  | refuseOperationalScenario
  | bindMissionIdentity
  | bindDecisionRole
  | bindAffectedPopulation
  | recordLegalBoundary
  | bindAccountableAuthority
  | bindEffectEnvelope
  | refuseAuthorityExpansion
  | addHumanInterface
  | restoreHumanAuthority
  | restoreDecisionTime
  | restoreHumanInformation
  | bindHumanCompetence
  | restoreHumanAttention
  | restoreInterventionReachability
  | restoreAlternatives
  | restoreIndependentJudgment
  | bindSensorProvenance
  | recordSensorDependencies
  | exposeUncertainty
  | bindCorroborationPolicy
  | addAbstentionRoute
  | recordCommunicationLossPosture
  | recordIntegrityFailurePosture
  | bindSuspensionAuthority
  | addAdversaryModelSet
  | addDoctrineVariants
  | trackReciprocalEffects
  | restoreOffRamps
  | trackProliferationResidual
  | assignIndependentReview
  | assignRestrictedEvidenceCustody
  | renewExpiredDossier
  | recordPublicMaximumInference
  | addIncidentAndRemedyRoute
  | addDecommissionRoute
  | assignResidualCustody
  | recordNonClaimBoundary
  | refuseWeaponAuthorization
  | refuseLawfulUseClaim
  | refuseStrategicStabilityClaim
  | refuseSupportAssignment
  | refuseReleaseAuthority
  | refuseOperationalDetailPublication
  | repairRequired
  | eligibleForTheseusPublicSafeSimulation
deriving DecidableEq, Repr

def ScopeRepairFor (dossier : InteractionDossier) : ReviewState :=
  if ! dossier.simulationRequested then .refusedNoSimulation
  else if ! dossier.publicSafeNonOperationalScenario then .refuseOperationalScenario
  else if ! dossier.missionIdentityBound then .bindMissionIdentity
  else if ! dossier.decisionRoleBound then .bindDecisionRole
  else if ! dossier.affectedPopulationBound then .bindAffectedPopulation
  else .recordLegalBoundary

def AuthorityRepairFor (dossier : InteractionDossier) : ReviewState :=
  if ! dossier.accountableAuthorityBound then .bindAccountableAuthority
  else if ! dossier.effectEnvelopeBound then .bindEffectEnvelope
  else .refuseAuthorityExpansion

def JudgmentRepairFor (dossier : InteractionDossier) : ReviewState :=
  if ! dossier.humanInterfacePresent then .addHumanInterface
  else if ! dossier.humanAuthorityPresent then .restoreHumanAuthority
  else if ! decide (DecisionTimeSufficient dossier) then .restoreDecisionTime
  else if ! dossier.humanInformationSufficient then .restoreHumanInformation
  else if ! dossier.humanCompetenceBound then .bindHumanCompetence
  else if ! dossier.humanAttentionAvailable then .restoreHumanAttention
  else if ! dossier.interventionReachable then .restoreInterventionReachability
  else if ! dossier.alternativesPresent then .restoreAlternatives
  else .restoreIndependentJudgment

def ObservationRepairFor (dossier : InteractionDossier) : ReviewState :=
  if ! dossier.sensorProvenanceBound then .bindSensorProvenance
  else if ! dossier.sensorDependenciesRecorded then .recordSensorDependencies
  else if ! dossier.uncertaintyVisible then .exposeUncertainty
  else .bindCorroborationPolicy

def SafePostureRepairFor (dossier : InteractionDossier) : ReviewState :=
  if ! dossier.abstentionRoutePresent then .addAbstentionRoute
  else if ! dossier.communicationLossPosturePresent then
    .recordCommunicationLossPosture
  else if ! dossier.integrityFailurePosturePresent then
    .recordIntegrityFailurePosture
  else .bindSuspensionAuthority

def InteractionRepairFor (dossier : InteractionDossier) : ReviewState :=
  if ! dossier.adversaryModelSetPresent then .addAdversaryModelSet
  else if ! dossier.doctrineVariantsPresent then .addDoctrineVariants
  else if ! dossier.reciprocalEffectsTracked then .trackReciprocalEffects
  else if ! decide (OffRampsSufficient dossier) then .restoreOffRamps
  else .trackProliferationResidual

def CustodyRepairFor (dossier : InteractionDossier) : ReviewState :=
  if ! dossier.independentReviewPresent then .assignIndependentReview
  else if ! dossier.restrictedEvidenceCustodyPresent then
    .assignRestrictedEvidenceCustody
  else if ! decide (DossierCurrent dossier) then .renewExpiredDossier
  else if ! dossier.publicMaximumInferencePresent then .recordPublicMaximumInference
  else if ! dossier.incidentAndRemedyRoutePresent then .addIncidentAndRemedyRoute
  else if ! dossier.decommissionRoutePresent then .addDecommissionRoute
  else if ! dossier.residualCustodyPresent then .assignResidualCustody
  else if ! dossier.nonClaimBoundaryPresent then .recordNonClaimBoundary
  else if dossier.weaponAuthorizationRequested then .refuseWeaponAuthorization
  else if dossier.lawfulUseClaimRequested then .refuseLawfulUseClaim
  else if dossier.strategicStabilityClaimRequested then .refuseStrategicStabilityClaim
  else if dossier.supportAssignmentRequested then .refuseSupportAssignment
  else if dossier.releaseAuthorityRequested then .refuseReleaseAuthority
  else .refuseOperationalDetailPublication

def ReviewStepFor (dossier : InteractionDossier) : ReviewState -> ReviewState
  | .proposed =>
      if decide (ScopeComplete dossier) then .scopeReviewed else .repairRequired
  | .scopeReviewed =>
      if decide (AuthorityComplete dossier) then
        .authorityReviewed
      else .repairRequired
  | .authorityReviewed =>
      if decide (MeaningfulHumanJudgment dossier) then
        .judgmentReviewed
      else .repairRequired
  | .judgmentReviewed =>
      if decide (ObservationComplete dossier) then
        .observationReviewed
      else .repairRequired
  | .observationReviewed =>
      if decide (SafePostureComplete dossier) then
        .safePostureReviewed
      else .repairRequired
  | .safePostureReviewed =>
      if decide (InteractionComplete dossier) then
        .interactionReviewed
      else .repairRequired
  | .interactionReviewed =>
      if decide (CustodyAndBoundaryComplete dossier) then
        .custodyReviewed
      else .repairRequired
  | .custodyReviewed => .eligibleForTheseusPublicSafeSimulation
  | state => state

def ExactRepairFor (dossier : InteractionDossier) : ReviewState :=
  if ! decide (ScopeComplete dossier) then ScopeRepairFor dossier
  else if ! decide (AuthorityComplete dossier) then AuthorityRepairFor dossier
  else if ! decide (MeaningfulHumanJudgment dossier) then JudgmentRepairFor dossier
  else if ! decide (ObservationComplete dossier) then ObservationRepairFor dossier
  else if ! decide (SafePostureComplete dossier) then SafePostureRepairFor dossier
  else if ! decide (InteractionComplete dossier) then InteractionRepairFor dossier
  else if ! decide (CustodyAndBoundaryComplete dossier) then CustodyRepairFor dossier
  else .eligibleForTheseusPublicSafeSimulation

def ReviewRun (dossier : InteractionDossier) : Nat -> ReviewState
  | 0 => .proposed
  | steps + 1 => ReviewStepFor dossier (ReviewRun dossier steps)

def ReviewStageInvariant
    (dossier : InteractionDossier) : ReviewState -> Prop
  | .proposed => True
  | .scopeReviewed => ScopeComplete dossier
  | .authorityReviewed => ScopeComplete dossier ∧ AuthorityComplete dossier
  | .judgmentReviewed =>
      ScopeComplete dossier ∧ AuthorityComplete dossier ∧ MeaningfulHumanJudgment dossier
  | .observationReviewed =>
      ScopeComplete dossier ∧ AuthorityComplete dossier ∧ MeaningfulHumanJudgment dossier ∧
        ObservationComplete dossier
  | .safePostureReviewed =>
      ScopeComplete dossier ∧ AuthorityComplete dossier ∧ MeaningfulHumanJudgment dossier ∧
        ObservationComplete dossier ∧ SafePostureComplete dossier
  | .interactionReviewed =>
      ScopeComplete dossier ∧ AuthorityComplete dossier ∧ MeaningfulHumanJudgment dossier ∧
        ObservationComplete dossier ∧ SafePostureComplete dossier ∧
          InteractionComplete dossier
  | .custodyReviewed => DossierAdmissible dossier
  | .eligibleForTheseusPublicSafeSimulation => DossierAdmissible dossier
  | _ => True

theorem review_step_preserves_stage_invariant
    (dossier : InteractionDossier) (state : ReviewState)
    (invariant : ReviewStageInvariant dossier state) :
    ReviewStageInvariant dossier (ReviewStepFor dossier state) := by
  cases state
  case proposed =>
    simp only [ReviewStepFor]
    split
    · simp_all [ReviewStageInvariant]
    · simp [ReviewStageInvariant]
  case scopeReviewed =>
    simp only [ReviewStepFor]
    split
    · simp_all [ReviewStageInvariant]
    · simp [ReviewStageInvariant]
  case authorityReviewed =>
    simp only [ReviewStepFor]
    split
    · simp_all [ReviewStageInvariant]
    · simp [ReviewStageInvariant]
  case judgmentReviewed =>
    simp only [ReviewStepFor]
    split
    · simp_all [ReviewStageInvariant]
    · simp [ReviewStageInvariant]
  case observationReviewed =>
    simp only [ReviewStepFor]
    split
    · simp_all [ReviewStageInvariant]
    · simp [ReviewStageInvariant]
  case safePostureReviewed =>
    simp only [ReviewStepFor]
    split
    · simp_all [ReviewStageInvariant]
    · simp [ReviewStageInvariant]
  case interactionReviewed =>
    simp only [ReviewStepFor]
    split
    · simp_all [ReviewStageInvariant, DossierAdmissible]
    · simp [ReviewStageInvariant]
  case custodyReviewed =>
    simpa [ReviewStepFor, ReviewStageInvariant] using invariant
  all_goals simpa [ReviewStepFor] using invariant

theorem review_run_preserves_stage_invariant
    (dossier : InteractionDossier) (steps : Nat) :
    ReviewStageInvariant dossier (ReviewRun dossier steps) := by
  induction steps with
  | zero => simp [ReviewRun, ReviewStageInvariant]
  | succ steps ih =>
      simpa [ReviewRun] using
        review_step_preserves_stage_invariant dossier (ReviewRun dossier steps) ih

theorem simulation_eligibility_requires_admissible_dossier
    (dossier : InteractionDossier) (steps : Nat)
    (eligible : ReviewRun dossier steps = .eligibleForTheseusPublicSafeSimulation) :
    DossierAdmissible dossier := by
  have invariant := review_run_preserves_stage_invariant dossier steps
  simpa [eligible, ReviewStageInvariant] using invariant

theorem admissible_dossier_is_ready
    (dossier : InteractionDossier) (admissible : DossierAdmissible dossier) :
    DossierReady dossier = true := by
  exact decide_eq_true admissible

def completeDossier : InteractionDossier := {}

theorem complete_dossier_is_ready :
    DossierReady completeDossier = true := by decide

theorem complete_dossier_reaches_only_public_safe_simulation :
    ReviewRun completeDossier 8 = .eligibleForTheseusPublicSafeSimulation := by decide

inductive AdmissionAxis where
  | simulationRequest
  | nonOperationalScenario
  | missionIdentity
  | decisionRole
  | affectedPopulation
  | legalBoundary
  | accountableAuthority
  | effectEnvelope
  | authorityExpansion
  | humanInterface
  | humanAuthority
  | decisionTime
  | humanInformation
  | humanCompetence
  | humanAttention
  | interventionReachability
  | alternatives
  | independentJudgment
  | sensorProvenance
  | sensorDependencies
  | uncertaintyVisibility
  | corroborationPolicy
  | abstentionRoute
  | communicationLossPosture
  | integrityFailurePosture
  | suspensionAuthority
  | adversaryModelSet
  | doctrineVariants
  | reciprocalEffects
  | offRamps
  | proliferationResidual
  | independentReview
  | restrictedEvidenceCustody
  | expiry
  | publicMaximumInference
  | incidentAndRemedy
  | decommissionRoute
  | residualCustody
  | nonClaimBoundary
  | weaponAuthorization
  | lawfulUseClaim
  | strategicStabilityClaim
  | supportAssignment
  | releaseAuthority
  | operationalDetailPublication
deriving DecidableEq, Repr

def omitAdmissionAxis : AdmissionAxis -> InteractionDossier
  | .simulationRequest => { completeDossier with simulationRequested := false }
  | .nonOperationalScenario =>
      { completeDossier with publicSafeNonOperationalScenario := false }
  | .missionIdentity => { completeDossier with missionIdentityBound := false }
  | .decisionRole => { completeDossier with decisionRoleBound := false }
  | .affectedPopulation => { completeDossier with affectedPopulationBound := false }
  | .legalBoundary => { completeDossier with legalBoundaryRecorded := false }
  | .accountableAuthority => { completeDossier with accountableAuthorityBound := false }
  | .effectEnvelope => { completeDossier with effectEnvelopeBound := false }
  | .authorityExpansion => { completeDossier with authorityExpansionRequested := true }
  | .humanInterface => { completeDossier with humanInterfacePresent := false }
  | .humanAuthority => { completeDossier with humanAuthorityPresent := false }
  | .decisionTime => { completeDossier with availableDecisionTime := 2 }
  | .humanInformation => { completeDossier with humanInformationSufficient := false }
  | .humanCompetence => { completeDossier with humanCompetenceBound := false }
  | .humanAttention => { completeDossier with humanAttentionAvailable := false }
  | .interventionReachability => { completeDossier with interventionReachable := false }
  | .alternatives => { completeDossier with alternativesPresent := false }
  | .independentJudgment => { completeDossier with independentJudgmentPossible := false }
  | .sensorProvenance => { completeDossier with sensorProvenanceBound := false }
  | .sensorDependencies => { completeDossier with sensorDependenciesRecorded := false }
  | .uncertaintyVisibility => { completeDossier with uncertaintyVisible := false }
  | .corroborationPolicy => { completeDossier with corroborationPolicyBound := false }
  | .abstentionRoute => { completeDossier with abstentionRoutePresent := false }
  | .communicationLossPosture =>
      { completeDossier with communicationLossPosturePresent := false }
  | .integrityFailurePosture =>
      { completeDossier with integrityFailurePosturePresent := false }
  | .suspensionAuthority => { completeDossier with suspensionAuthorityPresent := false }
  | .adversaryModelSet => { completeDossier with adversaryModelSetPresent := false }
  | .doctrineVariants => { completeDossier with doctrineVariantsPresent := false }
  | .reciprocalEffects => { completeDossier with reciprocalEffectsTracked := false }
  | .offRamps => { completeDossier with availableOffRampCount := 1 }
  | .proliferationResidual =>
      { completeDossier with proliferationResidualTracked := false }
  | .independentReview => { completeDossier with independentReviewPresent := false }
  | .restrictedEvidenceCustody =>
      { completeDossier with restrictedEvidenceCustodyPresent := false }
  | .expiry => { completeDossier with expiresAt := 4 }
  | .publicMaximumInference =>
      { completeDossier with publicMaximumInferencePresent := false }
  | .incidentAndRemedy =>
      { completeDossier with incidentAndRemedyRoutePresent := false }
  | .decommissionRoute => { completeDossier with decommissionRoutePresent := false }
  | .residualCustody => { completeDossier with residualCustodyPresent := false }
  | .nonClaimBoundary => { completeDossier with nonClaimBoundaryPresent := false }
  | .weaponAuthorization => { completeDossier with weaponAuthorizationRequested := true }
  | .lawfulUseClaim => { completeDossier with lawfulUseClaimRequested := true }
  | .strategicStabilityClaim =>
      { completeDossier with strategicStabilityClaimRequested := true }
  | .supportAssignment => { completeDossier with supportAssignmentRequested := true }
  | .releaseAuthority => { completeDossier with releaseAuthorityRequested := true }
  | .operationalDetailPublication =>
      { completeDossier with operationalDetailPublicationRequested := true }

def repairStateForAxis : AdmissionAxis -> ReviewState
  | .simulationRequest => .refusedNoSimulation
  | .nonOperationalScenario => .refuseOperationalScenario
  | .missionIdentity => .bindMissionIdentity
  | .decisionRole => .bindDecisionRole
  | .affectedPopulation => .bindAffectedPopulation
  | .legalBoundary => .recordLegalBoundary
  | .accountableAuthority => .bindAccountableAuthority
  | .effectEnvelope => .bindEffectEnvelope
  | .authorityExpansion => .refuseAuthorityExpansion
  | .humanInterface => .addHumanInterface
  | .humanAuthority => .restoreHumanAuthority
  | .decisionTime => .restoreDecisionTime
  | .humanInformation => .restoreHumanInformation
  | .humanCompetence => .bindHumanCompetence
  | .humanAttention => .restoreHumanAttention
  | .interventionReachability => .restoreInterventionReachability
  | .alternatives => .restoreAlternatives
  | .independentJudgment => .restoreIndependentJudgment
  | .sensorProvenance => .bindSensorProvenance
  | .sensorDependencies => .recordSensorDependencies
  | .uncertaintyVisibility => .exposeUncertainty
  | .corroborationPolicy => .bindCorroborationPolicy
  | .abstentionRoute => .addAbstentionRoute
  | .communicationLossPosture => .recordCommunicationLossPosture
  | .integrityFailurePosture => .recordIntegrityFailurePosture
  | .suspensionAuthority => .bindSuspensionAuthority
  | .adversaryModelSet => .addAdversaryModelSet
  | .doctrineVariants => .addDoctrineVariants
  | .reciprocalEffects => .trackReciprocalEffects
  | .offRamps => .restoreOffRamps
  | .proliferationResidual => .trackProliferationResidual
  | .independentReview => .assignIndependentReview
  | .restrictedEvidenceCustody => .assignRestrictedEvidenceCustody
  | .expiry => .renewExpiredDossier
  | .publicMaximumInference => .recordPublicMaximumInference
  | .incidentAndRemedy => .addIncidentAndRemedyRoute
  | .decommissionRoute => .addDecommissionRoute
  | .residualCustody => .assignResidualCustody
  | .nonClaimBoundary => .recordNonClaimBoundary
  | .weaponAuthorization => .refuseWeaponAuthorization
  | .lawfulUseClaim => .refuseLawfulUseClaim
  | .strategicStabilityClaim => .refuseStrategicStabilityClaim
  | .supportAssignment => .refuseSupportAssignment
  | .releaseAuthority => .refuseReleaseAuthority
  | .operationalDetailPublication => .refuseOperationalDetailPublication

theorem every_admission_axis_mutation_blocks_readiness (axis : AdmissionAxis) :
    DossierReady (omitAdmissionAxis axis) = false := by
  cases axis <;> decide

theorem every_admission_axis_mutation_has_exact_repair_disposition
    (axis : AdmissionAxis) :
    ExactRepairFor (omitAdmissionAxis axis) = repairStateForAxis axis := by
  cases axis <;> decide

theorem every_admission_axis_mutation_reaches_repair_state
    (axis : AdmissionAxis) :
    ReviewRun (omitAdmissionAxis axis) 8 = .repairRequired := by
  cases axis <;> decide

theorem every_admission_axis_mutation_blocks_simulation_eligibility
    (axis : AdmissionAxis) :
    ReviewRun (omitAdmissionAxis axis) 8 != .eligibleForTheseusPublicSafeSimulation := by
  cases axis <;> decide

theorem readiness_requires_scope
    (dossier : InteractionDossier) (ready : DossierReady dossier = true) :
    ScopeComplete dossier := by
  have admissible : DossierAdmissible dossier := of_decide_eq_true ready
  exact admissible.1

theorem readiness_requires_bounded_authority
    (dossier : InteractionDossier) (ready : DossierReady dossier = true) :
    AuthorityComplete dossier := by
  have admissible : DossierAdmissible dossier := of_decide_eq_true ready
  exact admissible.2.1

theorem readiness_requires_meaningful_human_judgment
    (dossier : InteractionDossier) (ready : DossierReady dossier = true) :
    MeaningfulHumanJudgment dossier := by
  have admissible : DossierAdmissible dossier := of_decide_eq_true ready
  exact admissible.2.2.1

theorem readiness_requires_observation_trust_record
    (dossier : InteractionDossier) (ready : DossierReady dossier = true) :
    ObservationComplete dossier := by
  have admissible : DossierAdmissible dossier := of_decide_eq_true ready
  exact admissible.2.2.2.1

theorem readiness_requires_safe_posture
    (dossier : InteractionDossier) (ready : DossierReady dossier = true) :
    SafePostureComplete dossier := by
  have admissible : DossierAdmissible dossier := of_decide_eq_true ready
  exact admissible.2.2.2.2.1

theorem readiness_requires_interaction_case
    (dossier : InteractionDossier) (ready : DossierReady dossier = true) :
    InteractionComplete dossier := by
  have admissible : DossierAdmissible dossier := of_decide_eq_true ready
  exact admissible.2.2.2.2.2.1

theorem readiness_requires_custody_and_non_authorizing_boundary
    (dossier : InteractionDossier) (ready : DossierReady dossier = true) :
    CustodyAndBoundaryComplete dossier := by
  have admissible : DossierAdmissible dossier := of_decide_eq_true ready
  exact admissible.2.2.2.2.2.2

theorem expired_dossier_remains_expired_when_time_advances
    (dossier : InteractionDossier) (laterTick : Nat)
    (expired : dossier.expiresAt < dossier.currentTick)
    (later : dossier.currentTick <= laterTick) :
    ¬ DossierCurrent { dossier with currentTick := laterTick } := by
  intro current
  unfold DossierCurrent at current
  change laterTick <= dossier.expiresAt at current
  omega

theorem decision_time_shortfall_persists_when_available_time_decreases
    (dossier : InteractionDossier) (lessTime : Nat)
    (decreased : lessTime <= dossier.availableDecisionTime)
    (shortfall : dossier.availableDecisionTime < dossier.requiredDecisionTime) :
    ¬ DecisionTimeSufficient { dossier with availableDecisionTime := lessTime } := by
  intro sufficient
  unfold DecisionTimeSufficient at sufficient
  change 0 < dossier.requiredDecisionTime ∧
    dossier.requiredDecisionTime <= lessTime at sufficient
  omega

theorem off_ramp_shortfall_persists_when_available_routes_decrease
    (dossier : InteractionDossier) (fewerRoutes : Nat)
    (decreased : fewerRoutes <= dossier.availableOffRampCount)
    (shortfall : dossier.availableOffRampCount < dossier.requiredOffRampCount) :
    ¬ OffRampsSufficient { dossier with availableOffRampCount := fewerRoutes } := by
  intro sufficient
  unfold OffRampsSufficient at sufficient
  change 0 < dossier.requiredOffRampCount ∧
    dossier.requiredOffRampCount <= fewerRoutes at sufficient
  omega

def ceremonialInterfaceDossier : InteractionDossier :=
  { completeDossier with availableDecisionTime := 0 }

theorem same_human_interface_can_hide_opposite_judgment_results :
    completeDossier.humanInterfacePresent = ceremonialInterfaceDossier.humanInterfacePresent ∧
      decide (MeaningfulHumanJudgment completeDossier) = true ∧
        decide (MeaningfulHumanJudgment ceremonialInterfaceDossier) = false := by decide

theorem interface_presence_cannot_recover_meaningful_judgment
    (classify : Bool -> Bool) :
    ¬ (∀ dossier,
      classify dossier.humanInterfacePresent = decide (MeaningfulHumanJudgment dossier)) := by
  intro exactForEveryDossier
  have completeCase := exactForEveryDossier completeDossier
  have ceremonialCase := exactForEveryDossier ceremonialInterfaceDossier
  simp [completeDossier, ceremonialInterfaceDossier, MeaningfulHumanJudgment,
    DecisionTimeSufficient] at completeCase ceremonialCase
  rw [completeCase] at ceremonialCase
  contradiction

structure ComponentEvidence where
  accuracyClass : Nat
  latencyClass : Nat
  reliabilityClass : Nat
deriving DecidableEq, Repr

structure StrategicInteractionRecord where
  component : ComponentEvidence
  adversaryEscalates : Bool
  offRampSurvives : Bool
deriving DecidableEq, Repr

def StrategicHoldRequired (record : StrategicInteractionRecord) : Bool :=
  record.adversaryEscalates || ! record.offRampSurvives

def sharedComponentEvidence : ComponentEvidence where
  accuracyClass := 4
  latencyClass := 4
  reliabilityClass := 4

def stableInteraction : StrategicInteractionRecord where
  component := sharedComponentEvidence
  adversaryEscalates := false
  offRampSurvives := true

def unstableInteraction : StrategicInteractionRecord where
  component := sharedComponentEvidence
  adversaryEscalates := true
  offRampSurvives := true

theorem identical_component_evidence_can_require_opposite_interaction_reviews :
    stableInteraction.component = unstableInteraction.component ∧
      StrategicHoldRequired stableInteraction = false ∧
        StrategicHoldRequired unstableInteraction = true := by decide

theorem component_evidence_cannot_recover_interaction_review
    (classify : ComponentEvidence -> Bool) :
    ¬ (∀ record, classify record.component = StrategicHoldRequired record) := by
  intro exactForEveryRecord
  have stableCase := exactForEveryRecord stableInteraction
  have unstableCase := exactForEveryRecord unstableInteraction
  simp [stableInteraction, unstableInteraction, sharedComponentEvidence,
    StrategicHoldRequired] at stableCase unstableCase
  rw [stableCase] at unstableCase
  contradiction

end AsiStackProofs.MilitaryInteractionReview
