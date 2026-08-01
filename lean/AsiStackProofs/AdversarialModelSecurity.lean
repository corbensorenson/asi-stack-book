import AsiStackProofs.AdversarialEvaluationRefinement

namespace AsiStackProofs.AdversarialModelSecurity

inductive AssuranceKind where
  | regionalCertificate
  | runtimeMonitor
  | recoveryProcedure
deriving DecidableEq, Repr

inductive AssuranceObligation where
  | boundedProperty
  | observableDetection
  | stateRestoration
deriving DecidableEq, Repr

def discharges : AssuranceKind -> AssuranceObligation -> Bool
  | .regionalCertificate, .boundedProperty => true
  | .runtimeMonitor, .observableDetection => true
  | .recoveryProcedure, .stateRestoration => true
  | _, _ => false

theorem certificate_does_not_discharge_monitoring :
    discharges .regionalCertificate .observableDetection = false := by rfl
theorem monitoring_does_not_discharge_recovery :
    discharges .runtimeMonitor .stateRestoration = false := by rfl
theorem recovery_does_not_discharge_certificate :
    discharges .recoveryProcedure .boundedProperty = false := by rfl

structure AttackTrace where
  traceId : Nat
  quarantined : Bool
deriving DecidableEq, Repr

def quarantineTrace (trace : AttackTrace) : AttackTrace := { trace with quarantined := true }
def quarantineAll : List AttackTrace -> List AttackTrace
  | [] => []
  | trace :: rest => quarantineTrace trace :: quarantineAll rest
def AllQuarantined (traces : List AttackTrace) : Prop :=
  forall trace, trace ∈ traces -> trace.quarantined = true

theorem quarantine_all_covers_every_finite_trace (traces : List AttackTrace) :
    AllQuarantined (quarantineAll traces) := by
  intro trace member
  induction traces with
  | nil => simp [quarantineAll] at member
  | cons head tail ih =>
      simp only [quarantineAll, List.mem_cons] at member
      rcases member with same | inTail
      · subst trace
        simp [quarantineTrace]
      · exact ih inTail

structure ThreatDossier where
  modelIdentityBound : Bool := true
  checkpointIdentityBound : Bool := true
  dataLineageBound : Bool := true
  servingConfigurationBound : Bool := true
  lifecycleStageBound : Bool := true
  modalityBound : Bool := true
  populationBound : Bool := true
  configurationVersion : Nat := 7
  authorizedConfigurationVersion : Nat := 7
  attackerAccessBound : Bool := true
  attackerKnowledgeBound : Bool := true
  attackerCapabilityBound : Bool := true
  attackerBudgetBound : Bool := true
  attackObjectiveBound : Bool := true
  attackSurfaceBound : Bool := true
  protectedAssetBound : Bool := true
  successCriterionBound : Bool := true
  attackClassesSeparated : Bool := true
  attackObjectivesSeparated : Bool := true
  attemptDenominatorComplete : Bool := true
  attemptTraceLineagePresent : Bool := true
  defenseAwareChallengePresent : Bool := true
  adaptiveChallengePresent : Bool := true
  transferChallengePresent : Bool := true
  knownVulnerableControlPresent : Bool := true
  knownVulnerableControlPassed : Bool := true
  benignPerturbationBaselinePresent : Bool := true
  cleanUtilityBaselinePresent : Bool := true
  matchedAttackDefenseBudgets : Bool := true
  independentChallengerPresent : Bool := true
  attackTracePresent : Bool := true
  observedEffectPresent : Bool := true
  attackedUtilityPresent : Bool := true
  detectorOutcomePresent : Bool := true
  falseAlarmRecordPresent : Bool := true
  costAndLatencyPresent : Bool := true
  failureCasesPreserved : Bool := true
  quarantineRoutePresent : Bool := true
  predecessorBound : Bool := true
  repairLineagePresent : Bool := true
  recoveryObservationPresent : Bool := true
  descendantIndexPresent : Bool := true
  unreachableResidualRecorded : Bool := true
  residualOwnerPresent : Bool := true
  certificateScopeBound : Bool := true
  monitorScopeBound : Bool := true
  recoveryScopeBound : Bool := true
  assuranceNonSubstitutionRecorded : Bool := true
  testAuthorizationPresent : Bool := true
  prohibitedRealEffectsExcluded : Bool := true
  exploitCustodyPresent : Bool := true
  stopConditionsPresent : Bool := true
  notificationAndRemediationRoutePresent : Bool := true
  publicationTierBound : Bool := true
  currentTick : Nat := 10
  expiresAt : Nat := 20
  generalRobustnessClaimed : Bool := false
  secureDeploymentClaimed : Bool := false
  attackAuthorizationRequested : Bool := false
  supportPromotionRequested : Bool := false
deriving DecidableEq, Repr

def Current (d : ThreatDossier) : Prop := d.currentTick <= d.expiresAt
def ConfigurationCurrent (d : ThreatDossier) : Prop :=
  d.configurationVersion = d.authorizedConfigurationVersion
instance currentDecidable (d : ThreatDossier) : Decidable (Current d) := by
  unfold Current; infer_instance
instance configurationCurrentDecidable (d : ThreatDossier) : Decidable (ConfigurationCurrent d) := by
  unfold ConfigurationCurrent; infer_instance

def IdentityComplete (d : ThreatDossier) : Prop :=
  d.modelIdentityBound = true ∧ d.checkpointIdentityBound = true ∧
  d.dataLineageBound = true ∧ d.servingConfigurationBound = true ∧
  d.lifecycleStageBound = true ∧ d.modalityBound = true ∧ d.populationBound = true ∧
  ConfigurationCurrent d
def ThreatComplete (d : ThreatDossier) : Prop :=
  d.attackerAccessBound = true ∧ d.attackerKnowledgeBound = true ∧
  d.attackerCapabilityBound = true ∧ d.attackerBudgetBound = true ∧
  d.attackObjectiveBound = true ∧ d.attackSurfaceBound = true ∧
  d.protectedAssetBound = true ∧ d.successCriterionBound = true ∧
  d.attackClassesSeparated = true ∧ d.attackObjectivesSeparated = true ∧
  d.attemptDenominatorComplete = true ∧ d.attemptTraceLineagePresent = true
def ChallengeComplete (d : ThreatDossier) : Prop :=
  d.defenseAwareChallengePresent = true ∧ d.adaptiveChallengePresent = true ∧
  d.transferChallengePresent = true ∧ d.knownVulnerableControlPresent = true ∧
  d.knownVulnerableControlPassed = true ∧ d.benignPerturbationBaselinePresent = true ∧
  d.cleanUtilityBaselinePresent = true ∧ d.matchedAttackDefenseBudgets = true ∧
  d.independentChallengerPresent = true
def ObservationComplete (d : ThreatDossier) : Prop :=
  d.attackTracePresent = true ∧ d.observedEffectPresent = true ∧
  d.attackedUtilityPresent = true ∧ d.detectorOutcomePresent = true ∧
  d.falseAlarmRecordPresent = true ∧ d.costAndLatencyPresent = true ∧
  d.failureCasesPreserved = true
def RecoveryComplete (d : ThreatDossier) : Prop :=
  d.quarantineRoutePresent = true ∧ d.predecessorBound = true ∧
  d.repairLineagePresent = true ∧ d.recoveryObservationPresent = true ∧
  d.descendantIndexPresent = true ∧ d.unreachableResidualRecorded = true ∧
  d.residualOwnerPresent = true
def AssuranceComplete (d : ThreatDossier) : Prop :=
  d.certificateScopeBound = true ∧ d.monitorScopeBound = true ∧
  d.recoveryScopeBound = true ∧ d.assuranceNonSubstitutionRecorded = true
def DisclosureBoundaryComplete (d : ThreatDossier) : Prop :=
  d.testAuthorizationPresent = true ∧ d.prohibitedRealEffectsExcluded = true ∧
  d.exploitCustodyPresent = true ∧ d.stopConditionsPresent = true ∧
  d.notificationAndRemediationRoutePresent = true ∧ d.publicationTierBound = true ∧
  Current d ∧ d.generalRobustnessClaimed = false ∧ d.secureDeploymentClaimed = false ∧
  d.attackAuthorizationRequested = false ∧ d.supportPromotionRequested = false

instance identityCompleteDecidable (d : ThreatDossier) : Decidable (IdentityComplete d) := by
  unfold IdentityComplete ConfigurationCurrent; infer_instance
instance threatCompleteDecidable (d : ThreatDossier) : Decidable (ThreatComplete d) := by
  unfold ThreatComplete; infer_instance
instance challengeCompleteDecidable (d : ThreatDossier) : Decidable (ChallengeComplete d) := by
  unfold ChallengeComplete; infer_instance
instance observationCompleteDecidable (d : ThreatDossier) : Decidable (ObservationComplete d) := by
  unfold ObservationComplete; infer_instance
instance recoveryCompleteDecidable (d : ThreatDossier) : Decidable (RecoveryComplete d) := by
  unfold RecoveryComplete; infer_instance
instance assuranceCompleteDecidable (d : ThreatDossier) : Decidable (AssuranceComplete d) := by
  unfold AssuranceComplete; infer_instance
instance disclosureBoundaryCompleteDecidable (d : ThreatDossier) : Decidable (DisclosureBoundaryComplete d) := by
  unfold DisclosureBoundaryComplete Current; infer_instance

def DossierAdmissible (d : ThreatDossier) : Prop :=
  IdentityComplete d ∧ ThreatComplete d ∧ ChallengeComplete d ∧ ObservationComplete d ∧
  RecoveryComplete d ∧ AssuranceComplete d ∧ DisclosureBoundaryComplete d
instance dossierAdmissibleDecidable (d : ThreatDossier) : Decidable (DossierAdmissible d) := by
  unfold DossierAdmissible IdentityComplete ConfigurationCurrent ThreatComplete ChallengeComplete
    ObservationComplete RecoveryComplete AssuranceComplete DisclosureBoundaryComplete Current
  infer_instance
def DossierReady (d : ThreatDossier) : Bool := decide (DossierAdmissible d)

inductive ReviewState where
  | proposed | identityReviewed | threatReviewed | challengeReviewed | observationReviewed
  | recoveryReviewed | assuranceReviewed | boundaryReviewed | repairRequired
  | eligibleForTheseusModelSecurityCampaign
deriving DecidableEq, Repr

def ReviewStepFor (d : ThreatDossier) : ReviewState -> ReviewState
  | .proposed => if decide (IdentityComplete d) then .identityReviewed else .repairRequired
  | .identityReviewed => if decide (ThreatComplete d) then .threatReviewed else .repairRequired
  | .threatReviewed => if decide (ChallengeComplete d) then .challengeReviewed else .repairRequired
  | .challengeReviewed => if decide (ObservationComplete d) then .observationReviewed else .repairRequired
  | .observationReviewed => if decide (RecoveryComplete d) then .recoveryReviewed else .repairRequired
  | .recoveryReviewed => if decide (AssuranceComplete d) then .assuranceReviewed else .repairRequired
  | .assuranceReviewed =>
      if decide (DisclosureBoundaryComplete d) then .boundaryReviewed else .repairRequired
  | .boundaryReviewed => .eligibleForTheseusModelSecurityCampaign
  | state => state
def ReviewRun (d : ThreatDossier) : Nat -> ReviewState
  | 0 => .proposed
  | n + 1 => ReviewStepFor d (ReviewRun d n)
def StageInvariant (d : ThreatDossier) : ReviewState -> Prop
  | .proposed => True
  | .identityReviewed => IdentityComplete d
  | .threatReviewed => IdentityComplete d ∧ ThreatComplete d
  | .challengeReviewed => IdentityComplete d ∧ ThreatComplete d ∧ ChallengeComplete d
  | .observationReviewed =>
      IdentityComplete d ∧ ThreatComplete d ∧ ChallengeComplete d ∧ ObservationComplete d
  | .recoveryReviewed =>
      IdentityComplete d ∧ ThreatComplete d ∧ ChallengeComplete d ∧ ObservationComplete d ∧
      RecoveryComplete d
  | .assuranceReviewed =>
      IdentityComplete d ∧ ThreatComplete d ∧ ChallengeComplete d ∧ ObservationComplete d ∧
      RecoveryComplete d ∧ AssuranceComplete d
  | .boundaryReviewed | .eligibleForTheseusModelSecurityCampaign => DossierAdmissible d
  | .repairRequired => True

theorem review_step_preserves_stage_invariant (d : ThreatDossier) (state : ReviewState)
    (h : StageInvariant d state) : StageInvariant d (ReviewStepFor d state) := by
  cases state <;> simp only [ReviewStepFor]
  case proposed => split <;> simp_all [StageInvariant]
  case identityReviewed => split <;> simp_all [StageInvariant]
  case threatReviewed => split <;> simp_all [StageInvariant]
  case challengeReviewed => split <;> simp_all [StageInvariant]
  case observationReviewed => split <;> simp_all [StageInvariant]
  case recoveryReviewed => split <;> simp_all [StageInvariant]
  case assuranceReviewed => split <;> simp_all [StageInvariant, DossierAdmissible]
  all_goals simp_all [StageInvariant]
theorem review_run_preserves_stage_invariant (d : ThreatDossier) (n : Nat) :
    StageInvariant d (ReviewRun d n) := by
  induction n with
  | zero => simp [ReviewRun, StageInvariant]
  | succ n ih => simpa [ReviewRun] using review_step_preserves_stage_invariant d _ ih
theorem campaign_eligibility_requires_admissible_dossier (d : ThreatDossier) (n : Nat)
    (h : ReviewRun d n = .eligibleForTheseusModelSecurityCampaign) : DossierAdmissible d := by
  have invariant := review_run_preserves_stage_invariant d n
  simpa [h, StageInvariant] using invariant

def completeDossier : ThreatDossier := {}
theorem complete_dossier_is_ready : DossierReady completeDossier = true := by decide
theorem complete_dossier_reaches_only_model_security_campaign :
    ReviewRun completeDossier 8 = .eligibleForTheseusModelSecurityCampaign := by decide

inductive AdmissionAxis where
  | modelIdentity | checkpointIdentity | dataLineage | servingConfiguration | lifecycleStage
  | modality | population | configurationVersion | attackerAccess | attackerKnowledge
  | attackerCapability | attackerBudget | attackObjective | attackSurface | protectedAsset
  | successCriterion | attackClassSeparation | attackObjectiveSeparation | attemptDenominator
  | attemptTraceLineage | defenseAwareChallenge | adaptiveChallenge | transferChallenge
  | knownVulnerableControl | knownVulnerableControlOutcome | benignPerturbationBaseline
  | cleanUtilityBaseline | matchedBudgets | independentChallenger | attackTrace | observedEffect
  | attackedUtility | detectorOutcome | falseAlarmRecord | costAndLatency | failureCases
  | quarantineRoute | predecessor | repairLineage | recoveryObservation | descendantIndex
  | unreachableResidual | residualOwner | certificateScope | monitorScope | recoveryScope
  | assuranceNonSubstitution | testAuthorization | prohibitedRealEffects | exploitCustody
  | stopConditions | notificationAndRemediation | publicationTier | expiry | generalRobustness
  | secureDeployment | attackAuthorization | supportPromotion
deriving DecidableEq, Repr

def omitAxis : AdmissionAxis -> ThreatDossier
  | .modelIdentity => { completeDossier with modelIdentityBound := false }
  | .checkpointIdentity => { completeDossier with checkpointIdentityBound := false }
  | .dataLineage => { completeDossier with dataLineageBound := false }
  | .servingConfiguration => { completeDossier with servingConfigurationBound := false }
  | .lifecycleStage => { completeDossier with lifecycleStageBound := false }
  | .modality => { completeDossier with modalityBound := false }
  | .population => { completeDossier with populationBound := false }
  | .configurationVersion => { completeDossier with configurationVersion := 8 }
  | .attackerAccess => { completeDossier with attackerAccessBound := false }
  | .attackerKnowledge => { completeDossier with attackerKnowledgeBound := false }
  | .attackerCapability => { completeDossier with attackerCapabilityBound := false }
  | .attackerBudget => { completeDossier with attackerBudgetBound := false }
  | .attackObjective => { completeDossier with attackObjectiveBound := false }
  | .attackSurface => { completeDossier with attackSurfaceBound := false }
  | .protectedAsset => { completeDossier with protectedAssetBound := false }
  | .successCriterion => { completeDossier with successCriterionBound := false }
  | .attackClassSeparation => { completeDossier with attackClassesSeparated := false }
  | .attackObjectiveSeparation => { completeDossier with attackObjectivesSeparated := false }
  | .attemptDenominator => { completeDossier with attemptDenominatorComplete := false }
  | .attemptTraceLineage => { completeDossier with attemptTraceLineagePresent := false }
  | .defenseAwareChallenge => { completeDossier with defenseAwareChallengePresent := false }
  | .adaptiveChallenge => { completeDossier with adaptiveChallengePresent := false }
  | .transferChallenge => { completeDossier with transferChallengePresent := false }
  | .knownVulnerableControl => { completeDossier with knownVulnerableControlPresent := false }
  | .knownVulnerableControlOutcome => { completeDossier with knownVulnerableControlPassed := false }
  | .benignPerturbationBaseline => { completeDossier with benignPerturbationBaselinePresent := false }
  | .cleanUtilityBaseline => { completeDossier with cleanUtilityBaselinePresent := false }
  | .matchedBudgets => { completeDossier with matchedAttackDefenseBudgets := false }
  | .independentChallenger => { completeDossier with independentChallengerPresent := false }
  | .attackTrace => { completeDossier with attackTracePresent := false }
  | .observedEffect => { completeDossier with observedEffectPresent := false }
  | .attackedUtility => { completeDossier with attackedUtilityPresent := false }
  | .detectorOutcome => { completeDossier with detectorOutcomePresent := false }
  | .falseAlarmRecord => { completeDossier with falseAlarmRecordPresent := false }
  | .costAndLatency => { completeDossier with costAndLatencyPresent := false }
  | .failureCases => { completeDossier with failureCasesPreserved := false }
  | .quarantineRoute => { completeDossier with quarantineRoutePresent := false }
  | .predecessor => { completeDossier with predecessorBound := false }
  | .repairLineage => { completeDossier with repairLineagePresent := false }
  | .recoveryObservation => { completeDossier with recoveryObservationPresent := false }
  | .descendantIndex => { completeDossier with descendantIndexPresent := false }
  | .unreachableResidual => { completeDossier with unreachableResidualRecorded := false }
  | .residualOwner => { completeDossier with residualOwnerPresent := false }
  | .certificateScope => { completeDossier with certificateScopeBound := false }
  | .monitorScope => { completeDossier with monitorScopeBound := false }
  | .recoveryScope => { completeDossier with recoveryScopeBound := false }
  | .assuranceNonSubstitution => { completeDossier with assuranceNonSubstitutionRecorded := false }
  | .testAuthorization => { completeDossier with testAuthorizationPresent := false }
  | .prohibitedRealEffects => { completeDossier with prohibitedRealEffectsExcluded := false }
  | .exploitCustody => { completeDossier with exploitCustodyPresent := false }
  | .stopConditions => { completeDossier with stopConditionsPresent := false }
  | .notificationAndRemediation => { completeDossier with notificationAndRemediationRoutePresent := false }
  | .publicationTier => { completeDossier with publicationTierBound := false }
  | .expiry => { completeDossier with currentTick := 21 }
  | .generalRobustness => { completeDossier with generalRobustnessClaimed := true }
  | .secureDeployment => { completeDossier with secureDeploymentClaimed := true }
  | .attackAuthorization => { completeDossier with attackAuthorizationRequested := true }
  | .supportPromotion => { completeDossier with supportPromotionRequested := true }

inductive RepairDisposition where
  | bindModelIdentity | bindCheckpointIdentity | bindDataLineage | bindServingConfiguration
  | bindLifecycleStage | bindModality | bindPopulation | reopenForConfigurationVersion
  | bindAttackerAccess | bindAttackerKnowledge | bindAttackerCapability | bindAttackerBudget
  | bindAttackObjective | bindAttackSurface | bindProtectedAsset | bindSuccessCriterion
  | separateAttackClasses | separateAttackObjectives | completeAttemptDenominator
  | bindAttemptTraceLineage | addDefenseAwareChallenge | addAdaptiveChallenge
  | addTransferChallenge | addKnownVulnerableControl | repairKnownVulnerableControl
  | addBenignPerturbationBaseline | addCleanUtilityBaseline | matchAttackDefenseBudgets
  | addIndependentChallenger | preserveAttackTrace | recordObservedEffect
  | recordAttackedUtility | recordDetectorOutcome | recordFalseAlarms | recordCostAndLatency
  | preserveFailureCases | addQuarantineRoute | bindPredecessor | bindRepairLineage
  | recordRecoveryObservation | completeDescendantIndex | recordUnreachableResidual
  | assignResidualOwner | bindCertificateScope | bindMonitorScope | bindRecoveryScope
  | recordAssuranceNonSubstitution | bindTestAuthorization | excludeProhibitedRealEffects
  | bindExploitCustody | bindStopConditions | addNotificationAndRemediation
  | bindPublicationTier | renewExpiry | rejectGeneralRobustness | rejectSecureDeployment
  | refuseAttackAuthorization | refuseSupportPromotion | eligibleForTheseusModelSecurityCampaign
deriving DecidableEq, Repr

def repairForAxis : AdmissionAxis -> RepairDisposition
  | .modelIdentity => .bindModelIdentity | .checkpointIdentity => .bindCheckpointIdentity
  | .dataLineage => .bindDataLineage | .servingConfiguration => .bindServingConfiguration
  | .lifecycleStage => .bindLifecycleStage | .modality => .bindModality
  | .population => .bindPopulation | .configurationVersion => .reopenForConfigurationVersion
  | .attackerAccess => .bindAttackerAccess | .attackerKnowledge => .bindAttackerKnowledge
  | .attackerCapability => .bindAttackerCapability | .attackerBudget => .bindAttackerBudget
  | .attackObjective => .bindAttackObjective | .attackSurface => .bindAttackSurface
  | .protectedAsset => .bindProtectedAsset | .successCriterion => .bindSuccessCriterion
  | .attackClassSeparation => .separateAttackClasses | .attackObjectiveSeparation => .separateAttackObjectives
  | .attemptDenominator => .completeAttemptDenominator | .attemptTraceLineage => .bindAttemptTraceLineage
  | .defenseAwareChallenge => .addDefenseAwareChallenge | .adaptiveChallenge => .addAdaptiveChallenge
  | .transferChallenge => .addTransferChallenge | .knownVulnerableControl => .addKnownVulnerableControl
  | .knownVulnerableControlOutcome => .repairKnownVulnerableControl
  | .benignPerturbationBaseline => .addBenignPerturbationBaseline
  | .cleanUtilityBaseline => .addCleanUtilityBaseline | .matchedBudgets => .matchAttackDefenseBudgets
  | .independentChallenger => .addIndependentChallenger | .attackTrace => .preserveAttackTrace
  | .observedEffect => .recordObservedEffect | .attackedUtility => .recordAttackedUtility
  | .detectorOutcome => .recordDetectorOutcome | .falseAlarmRecord => .recordFalseAlarms
  | .costAndLatency => .recordCostAndLatency | .failureCases => .preserveFailureCases
  | .quarantineRoute => .addQuarantineRoute | .predecessor => .bindPredecessor
  | .repairLineage => .bindRepairLineage | .recoveryObservation => .recordRecoveryObservation
  | .descendantIndex => .completeDescendantIndex | .unreachableResidual => .recordUnreachableResidual
  | .residualOwner => .assignResidualOwner | .certificateScope => .bindCertificateScope
  | .monitorScope => .bindMonitorScope | .recoveryScope => .bindRecoveryScope
  | .assuranceNonSubstitution => .recordAssuranceNonSubstitution
  | .testAuthorization => .bindTestAuthorization | .prohibitedRealEffects => .excludeProhibitedRealEffects
  | .exploitCustody => .bindExploitCustody | .stopConditions => .bindStopConditions
  | .notificationAndRemediation => .addNotificationAndRemediation | .publicationTier => .bindPublicationTier
  | .expiry => .renewExpiry | .generalRobustness => .rejectGeneralRobustness
  | .secureDeployment => .rejectSecureDeployment | .attackAuthorization => .refuseAttackAuthorization
  | .supportPromotion => .refuseSupportPromotion

def ExactRepairFor (d : ThreatDossier) : RepairDisposition :=
  if !d.modelIdentityBound then .bindModelIdentity else if !d.checkpointIdentityBound then .bindCheckpointIdentity
  else if !d.dataLineageBound then .bindDataLineage else if !d.servingConfigurationBound then .bindServingConfiguration
  else if !d.lifecycleStageBound then .bindLifecycleStage else if !d.modalityBound then .bindModality
  else if !d.populationBound then .bindPopulation else if d.configurationVersion != d.authorizedConfigurationVersion then .reopenForConfigurationVersion
  else if !d.attackerAccessBound then .bindAttackerAccess else if !d.attackerKnowledgeBound then .bindAttackerKnowledge
  else if !d.attackerCapabilityBound then .bindAttackerCapability else if !d.attackerBudgetBound then .bindAttackerBudget
  else if !d.attackObjectiveBound then .bindAttackObjective else if !d.attackSurfaceBound then .bindAttackSurface
  else if !d.protectedAssetBound then .bindProtectedAsset else if !d.successCriterionBound then .bindSuccessCriterion
  else if !d.attackClassesSeparated then .separateAttackClasses else if !d.attackObjectivesSeparated then .separateAttackObjectives
  else if !d.attemptDenominatorComplete then .completeAttemptDenominator else if !d.attemptTraceLineagePresent then .bindAttemptTraceLineage
  else if !d.defenseAwareChallengePresent then .addDefenseAwareChallenge else if !d.adaptiveChallengePresent then .addAdaptiveChallenge
  else if !d.transferChallengePresent then .addTransferChallenge else if !d.knownVulnerableControlPresent then .addKnownVulnerableControl
  else if !d.knownVulnerableControlPassed then .repairKnownVulnerableControl else if !d.benignPerturbationBaselinePresent then .addBenignPerturbationBaseline
  else if !d.cleanUtilityBaselinePresent then .addCleanUtilityBaseline else if !d.matchedAttackDefenseBudgets then .matchAttackDefenseBudgets
  else if !d.independentChallengerPresent then .addIndependentChallenger else if !d.attackTracePresent then .preserveAttackTrace
  else if !d.observedEffectPresent then .recordObservedEffect else if !d.attackedUtilityPresent then .recordAttackedUtility
  else if !d.detectorOutcomePresent then .recordDetectorOutcome else if !d.falseAlarmRecordPresent then .recordFalseAlarms
  else if !d.costAndLatencyPresent then .recordCostAndLatency else if !d.failureCasesPreserved then .preserveFailureCases
  else if !d.quarantineRoutePresent then .addQuarantineRoute else if !d.predecessorBound then .bindPredecessor
  else if !d.repairLineagePresent then .bindRepairLineage else if !d.recoveryObservationPresent then .recordRecoveryObservation
  else if !d.descendantIndexPresent then .completeDescendantIndex else if !d.unreachableResidualRecorded then .recordUnreachableResidual
  else if !d.residualOwnerPresent then .assignResidualOwner else if !d.certificateScopeBound then .bindCertificateScope
  else if !d.monitorScopeBound then .bindMonitorScope else if !d.recoveryScopeBound then .bindRecoveryScope
  else if !d.assuranceNonSubstitutionRecorded then .recordAssuranceNonSubstitution else if !d.testAuthorizationPresent then .bindTestAuthorization
  else if !d.prohibitedRealEffectsExcluded then .excludeProhibitedRealEffects else if !d.exploitCustodyPresent then .bindExploitCustody
  else if !d.stopConditionsPresent then .bindStopConditions else if !d.notificationAndRemediationRoutePresent then .addNotificationAndRemediation
  else if !d.publicationTierBound then .bindPublicationTier else if !decide (Current d) then .renewExpiry
  else if d.generalRobustnessClaimed then .rejectGeneralRobustness else if d.secureDeploymentClaimed then .rejectSecureDeployment
  else if d.attackAuthorizationRequested then .refuseAttackAuthorization else if d.supportPromotionRequested then .refuseSupportPromotion
  else .eligibleForTheseusModelSecurityCampaign

theorem every_admission_axis_mutation_blocks_readiness (axis : AdmissionAxis) :
    DossierReady (omitAxis axis) = false := by cases axis <;> decide
theorem every_admission_axis_mutation_has_exact_repair (axis : AdmissionAxis) :
    ExactRepairFor (omitAxis axis) = repairForAxis axis := by cases axis <;> decide
theorem every_admission_axis_mutation_reaches_repair (axis : AdmissionAxis) :
    ReviewRun (omitAxis axis) 8 = .repairRequired := by cases axis <;> decide

theorem readiness_requires_identity (d : ThreatDossier) (h : DossierReady d = true) :
    IdentityComplete d := by exact (of_decide_eq_true h).1
theorem readiness_requires_threat (d : ThreatDossier) (h : DossierReady d = true) :
    ThreatComplete d := by exact (of_decide_eq_true h).2.1
theorem readiness_requires_challenge (d : ThreatDossier) (h : DossierReady d = true) :
    ChallengeComplete d := by exact (of_decide_eq_true h).2.2.1
theorem readiness_requires_observation (d : ThreatDossier) (h : DossierReady d = true) :
    ObservationComplete d := by exact (of_decide_eq_true h).2.2.2.1
theorem readiness_requires_recovery (d : ThreatDossier) (h : DossierReady d = true) :
    RecoveryComplete d := by exact (of_decide_eq_true h).2.2.2.2.1
theorem readiness_requires_assurance (d : ThreatDossier) (h : DossierReady d = true) :
    AssuranceComplete d := by exact (of_decide_eq_true h).2.2.2.2.2.1
theorem readiness_requires_disclosure_boundary (d : ThreatDossier) (h : DossierReady d = true) :
    DisclosureBoundaryComplete d := by exact (of_decide_eq_true h).2.2.2.2.2.2

theorem expired_disposition_remains_expired_when_time_advances (d : ThreatDossier) (later : Nat)
    (expired : d.expiresAt < d.currentTick) (advances : d.currentTick <= later) :
    Not (Current { d with currentTick := later }) := by
  intro current
  unfold Current at current
  change later <= d.expiresAt at current
  omega

structure ThreatDisposition where
  modelId : Nat
  checkpointId : Nat
  configurationVersion : Nat
  attackSurfaceId : Nat
  attackerBudget : Nat
  expiresAt : Nat
deriving DecidableEq, Repr

def DispositionUseAllowed (d : ThreatDisposition)
    (model checkpoint configuration surface budget tick : Nat) : Prop :=
  model = d.modelId ∧ checkpoint = d.checkpointId ∧ configuration = d.configurationVersion ∧
  surface = d.attackSurfaceId ∧ budget <= d.attackerBudget ∧ tick <= d.expiresAt

theorem checkpoint_change_invalidates_disposition (d : ThreatDisposition) (checkpoint : Nat)
    (different : Not (checkpoint = d.checkpointId)) :
    Not (DispositionUseAllowed d d.modelId checkpoint d.configurationVersion
      d.attackSurfaceId d.attackerBudget d.expiresAt) := by
  intro allowed
  exact different allowed.2.1
theorem configuration_change_invalidates_disposition (d : ThreatDisposition) (configuration : Nat)
    (different : Not (configuration = d.configurationVersion)) :
    Not (DispositionUseAllowed d d.modelId d.checkpointId configuration
      d.attackSurfaceId d.attackerBudget d.expiresAt) := by
  intro allowed
  exact different allowed.2.2.1
theorem budget_widening_invalidates_disposition (d : ThreatDisposition) (budget : Nat)
    (wider : d.attackerBudget < budget) :
    Not (DispositionUseAllowed d d.modelId d.checkpointId d.configurationVersion
      d.attackSurfaceId budget d.expiresAt) := by
  intro allowed
  exact (Nat.not_le_of_gt wider) allowed.2.2.2.2.1

structure AggregateSignals where
  cleanAccuracy : Nat
  failedAttackCount : Nat
  redTeamCoverage : Nat
  certificatePresent : Bool
deriving DecidableEq, Repr
structure SecurityCase where
  signals : AggregateSignals
  adaptiveChallengePassed : Bool
  recoveryComplete : Bool
deriving DecidableEq, Repr
def sharedSignals : AggregateSignals :=
  { cleanAccuracy := 95, failedAttackCount := 100, redTeamCoverage := 80,
    certificatePresent := true }
def boundedCase : SecurityCase :=
  { signals := sharedSignals, adaptiveChallengePassed := true, recoveryComplete := true }
def maskingCase : SecurityCase :=
  { signals := sharedSignals, adaptiveChallengePassed := false, recoveryComplete := false }
def BoundedSecurityState (c : SecurityCase) : Bool :=
  c.adaptiveChallengePassed && c.recoveryComplete
theorem identical_aggregate_signals_can_hide_opposite_security_state :
    boundedCase.signals = maskingCase.signals ∧ BoundedSecurityState boundedCase = true ∧
    BoundedSecurityState maskingCase = false := by decide
theorem aggregate_scores_cannot_recover_bounded_security_state
    (classify : AggregateSignals -> Bool) :
    Not (forall c : SecurityCase, classify c.signals = BoundedSecurityState c) := by
  intro exact
  have bounded := exact boundedCase
  have masking := exact maskingCase
  simp [boundedCase, maskingCase, sharedSignals, BoundedSecurityState] at bounded masking
  rw [bounded] at masking
  contradiction

structure LocalComponentSignals where
  modelCheckPassed : Bool
  memoryCheckPassed : Bool
  toolCheckPassed : Bool
deriving DecidableEq, Repr
structure CompositionCase where
  componentSignals : LocalComponentSignals
  crossBoundaryPathReachable : Bool
deriving DecidableEq, Repr
def sharedLocalSignals : LocalComponentSignals :=
  { modelCheckPassed := true, memoryCheckPassed := true, toolCheckPassed := true }
def severedComposition : CompositionCase :=
  { componentSignals := sharedLocalSignals, crossBoundaryPathReachable := false }
def reachableComposition : CompositionCase :=
  { componentSignals := sharedLocalSignals, crossBoundaryPathReachable := true }
theorem identical_local_checks_can_hide_opposite_composition_state :
    severedComposition.componentSignals = reachableComposition.componentSignals ∧
    severedComposition.crossBoundaryPathReachable = false ∧
    reachableComposition.crossBoundaryPathReachable = true := by decide
theorem local_component_checks_cannot_recover_attack_path_reachability
    (classify : LocalComponentSignals -> Bool) :
    Not (forall c : CompositionCase, classify c.componentSignals = c.crossBoundaryPathReachable) := by
  intro exact
  have severed := exact severedComposition
  have reachable := exact reachableComposition
  simp [severedComposition, reachableComposition, sharedLocalSignals] at severed reachable
  rw [severed] at reachable
  contradiction

def toAdversarialEvaluationPacket (d : ThreatDossier) :
    AdversarialEvaluationRefinement.Packet :=
  { AdversarialEvaluationRefinement.canonicalPacket with
    modelTaskPresent := DossierReady d
    prospectivePlanPresent := DossierReady d
    observationPresent := d.observedEffectPresent
    transcriptPresent := d.attackTracePresent
    denominatorComplete := d.attemptDenominatorComplete
    failureCasesPreserved := d.failureCasesPreserved
    costRecordPresent := d.costAndLatencyPresent
    independentEvaluationPresent := d.independentChallengerPresent
    crossContextProbePresent := d.transferChallengePresent
    matchedAccessPresent := d.attackerAccessBound
    dependencyDisclosurePresent := d.attemptTraceLineagePresent
    uncertaintyPresent := true
    residualOwnerPresent := d.residualOwnerPresent
    expiryPresent := decide (Current d)
    noIntentInferenceRecorded := true
    decisionAuthoritySeparated := true
    noReleaseAuthorityRecorded := true
    supportAssignmentRequested := false
    externalEffectRequested := false }

theorem ready_dossier_supplies_bounded_adversarial_evaluation_fields
    (d : ThreatDossier) (ready : DossierReady d = true) :
    let packet := toAdversarialEvaluationPacket d
    packet.modelTaskPresent = true ∧ packet.prospectivePlanPresent = true ∧
    packet.observationPresent = true ∧ packet.transcriptPresent = true ∧
    packet.denominatorComplete = true ∧ packet.failureCasesPreserved = true ∧
    packet.costRecordPresent = true ∧ packet.independentEvaluationPresent = true ∧
    packet.crossContextProbePresent = true ∧ packet.matchedAccessPresent = true ∧
    packet.dependencyDisclosurePresent = true ∧ packet.residualOwnerPresent = true ∧
    packet.expiryPresent = true ∧ packet.noReleaseAuthorityRecorded = true ∧
    packet.supportAssignmentRequested = false ∧ packet.externalEffectRequested = false := by
  have threat := readiness_requires_threat d ready
  have challenge := readiness_requires_challenge d ready
  have observation := readiness_requires_observation d ready
  have recovery := readiness_requires_recovery d ready
  have boundary := readiness_requires_disclosure_boundary d ready
  simp [ThreatComplete, ChallengeComplete, ObservationComplete, RecoveryComplete,
    DisclosureBoundaryComplete] at threat challenge observation recovery boundary
  simp [toAdversarialEvaluationPacket, ready, threat, challenge, observation, recovery, boundary]

end AsiStackProofs.AdversarialModelSecurity
