import AsiStackProofs.EvidenceStates
import AsiStackProofs.BenchmarkRatchets

namespace AsiStackProofs.ScientificExperimentReview

/-!
A bounded review of authored scientific-experiment records. The model proves
custody, non-substitution, mutation rejection, scope invalidation, and local
consumer blocking. It does not prove hypothesis truth, causal identification,
instrument accuracy, replication success, laboratory safety, discovery,
support, release, or external effect.
-/

inductive EvidenceDecision where
  | insufficient | boundedObservation | eligibleForGovernedReview
deriving DecidableEq, Repr

inductive ScientificSignal where
  | hypothesisGenerated | experimentCompleted | significanceReported
  | workflowReplayed | dualUseReviewCompleted
deriving DecidableEq, Repr

def DecisionFromSingleSignal (_ : ScientificSignal) : EvidenceDecision := .insufficient

theorem generated_hypothesis_does_not_establish_discovery :
    DecisionFromSingleSignal .hypothesisGenerated = .insufficient := rfl
theorem completed_experiment_does_not_establish_causal_truth :
    DecisionFromSingleSignal .experimentCompleted = .insufficient := rfl
theorem significant_result_does_not_establish_reproducibility :
    DecisionFromSingleSignal .significanceReported = .insufficient := rfl
theorem replay_does_not_establish_independent_replication :
    DecisionFromSingleSignal .workflowReplayed = .insufficient := rfl
theorem dual_use_review_does_not_establish_safety :
    DecisionFromSingleSignal .dualUseReviewCompleted = .insufficient := rfl

inductive AttemptOutcome where
  | positive | negative | nullResult | contaminated | interrupted | inconclusive
deriving DecidableEq, Repr

structure ExperimentAttempt where
  attemptId : Nat
  outcome : AttemptOutcome
  includedInDenominator : Bool
deriving DecidableEq, Repr

def collectAttemptIds : List ExperimentAttempt -> List Nat
  | [] => []
  | attempt :: tail => attempt.attemptId :: collectAttemptIds tail

theorem attempt_id_collection_append_composes (before after : List ExperimentAttempt) :
    collectAttemptIds (before ++ after) =
      collectAttemptIds before ++ collectAttemptIds after := by
  induction before with
  | nil => rfl
  | cons head tail ih => simp [collectAttemptIds, ih]

theorem every_attempt_id_survives_collection
    (attempts : List ExperimentAttempt) (attempt : ExperimentAttempt)
    (member : attempt ∈ attempts) : attempt.attemptId ∈ collectAttemptIds attempts := by
  induction attempts with
  | nil => simp at member
  | cons head tail ih =>
      simp only [List.mem_cons] at member ⊢
      cases member with
      | inl same => subst head; simp [collectAttemptIds]
      | inr rest => right; exact ih rest

def CompleteAttemptDenominator (attempts : List ExperimentAttempt) : Prop :=
  forall attempt, attempt ∈ attempts -> attempt.includedInDenominator = true

theorem complete_denominator_counts_every_attempt
    (attempts : List ExperimentAttempt) (complete : CompleteAttemptDenominator attempts)
    (attempt : ExperimentAttempt) (member : attempt ∈ attempts) :
    attempt.includedInDenominator = true := complete attempt member

theorem omitted_attempt_rejects_complete_denominator
    (attempts : List ExperimentAttempt) (attempt : ExperimentAttempt)
    (member : attempt ∈ attempts) (omitted : attempt.includedInDenominator = false) :
    Not (CompleteAttemptDenominator attempts) := by
  intro complete
  have counted := complete attempt member
  simp [omitted] at counted

structure ConfirmatoryBranch where
  confirmatory : Bool
  preregisteredBeforeOutcome : Bool
  protectedOutcomeOpened : Bool
deriving DecidableEq, Repr

def ConfirmatoryIntegrity (branch : ConfirmatoryBranch) : Prop :=
  branch.confirmatory = true ->
    branch.preregisteredBeforeOutcome = true ∧ branch.protectedOutcomeOpened = false

theorem outcome_exposed_branch_rejects_confirmatory_integrity
    (branch : ConfirmatoryBranch) (confirmatory : branch.confirmatory = true)
    (opened : branch.protectedOutcomeOpened = true) :
    Not (ConfirmatoryIntegrity branch) := by
  intro integrity
  have closed := (integrity confirmatory).2
  simp [opened] at closed

structure ExperimentDossier where
  claimIdentityBound : Bool := true
  hypothesisIdentityBound : Bool := true
  hypothesisVersionBound : Bool := true
  hypothesisAncestryBound : Bool := true
  exploratoryConfirmatoryBound : Bool := true
  protocolVersionBound : Bool := true
  instrumentVersionBound : Bool := true
  dataSnapshotBound : Bool := true
  analysisVersionBound : Bool := true
  environmentBound : Bool := true
  preregistrationBound : Bool := true
  outcomesFrozenBeforeOpen : Bool := true
  samplingPlanBound : Bool := true
  powerPrecisionBound : Bool := true
  controlsBound : Bool := true
  randomizationBound : Bool := true
  blindingBound : Bool := true
  holdoutBound : Bool := true
  stoppingRuleBound : Bool := true
  exclusionsBound : Bool := true
  alternativesBound : Bool := true
  causalAssumptionsBound : Bool := true
  instrumentLeaseBound : Bool := true
  calibrationBound : Bool := true
  operatingEnvelopeBound : Bool := true
  sampleIdentityBound : Bool := true
  safetyInterlocksBound : Bool := true
  independentStopAuthorityBound : Bool := true
  attemptDenominatorComplete : Bool := true
  humanInterventionsPreserved : Bool := true
  protocolDeviationsPreserved : Bool := true
  rawObservationsPreserved : Bool := true
  codeParametersBound : Bool := true
  contaminationDriftControlsBound : Bool := true
  independentAnalysisBound : Bool := true
  robustnessChecksBound : Bool := true
  nullNegativeResultsPreserved : Bool := true
  correctionLineagePresent : Bool := true
  replicationContractBound : Bool := true
  replicationIndependenceBound : Bool := true
  disagreementPreserved : Bool := true
  dualUseQuestionReviewed : Bool := true
  dualUseProtocolReviewed : Bool := true
  dualUseExecutionReviewed : Bool := true
  dualUseArtifactReviewed : Bool := true
  dualUseDisclosureReviewed : Bool := true
  accessTierBound : Bool := true
  residualOwnerBound : Bool := true
  currentTick : Nat := 10
  expiresAt : Nat := 20
  causalTruthClaimed : Bool := false
  generalDiscoveryClaimed : Bool := false
  reproducibilityClaimed : Bool := false
  safetyClaimed : Bool := false
  supportOrReleaseRequested : Bool := false
deriving DecidableEq, Repr

def Current (d : ExperimentDossier) : Prop := d.currentTick <= d.expiresAt
instance currentDecidable (d : ExperimentDossier) : Decidable (Current d) := by
  unfold Current; infer_instance

def IdentityComplete (d : ExperimentDossier) : Prop :=
  d.claimIdentityBound = true ∧ d.hypothesisIdentityBound = true ∧
  d.hypothesisVersionBound = true ∧ d.hypothesisAncestryBound = true ∧
  d.exploratoryConfirmatoryBound = true ∧ d.protocolVersionBound = true ∧
  d.instrumentVersionBound = true ∧ d.dataSnapshotBound = true ∧
  d.analysisVersionBound = true ∧ d.environmentBound = true

def DesignComplete (d : ExperimentDossier) : Prop :=
  d.preregistrationBound = true ∧ d.outcomesFrozenBeforeOpen = true ∧
  d.samplingPlanBound = true ∧ d.powerPrecisionBound = true ∧
  d.controlsBound = true ∧ d.randomizationBound = true ∧ d.blindingBound = true ∧
  d.holdoutBound = true ∧ d.stoppingRuleBound = true ∧ d.exclusionsBound = true ∧
  d.alternativesBound = true ∧ d.causalAssumptionsBound = true

def ExecutionComplete (d : ExperimentDossier) : Prop :=
  d.instrumentLeaseBound = true ∧ d.calibrationBound = true ∧
  d.operatingEnvelopeBound = true ∧ d.sampleIdentityBound = true ∧
  d.safetyInterlocksBound = true ∧ d.independentStopAuthorityBound = true ∧
  d.attemptDenominatorComplete = true ∧ d.humanInterventionsPreserved = true ∧
  d.protocolDeviationsPreserved = true ∧ d.rawObservationsPreserved = true ∧
  d.codeParametersBound = true ∧ d.contaminationDriftControlsBound = true

def AnalysisComplete (d : ExperimentDossier) : Prop :=
  d.independentAnalysisBound = true ∧ d.robustnessChecksBound = true ∧
  d.nullNegativeResultsPreserved = true ∧ d.correctionLineagePresent = true

def ReplicationComplete (d : ExperimentDossier) : Prop :=
  d.replicationContractBound = true ∧ d.replicationIndependenceBound = true ∧
  d.disagreementPreserved = true

def GovernanceComplete (d : ExperimentDossier) : Prop :=
  d.dualUseQuestionReviewed = true ∧ d.dualUseProtocolReviewed = true ∧
  d.dualUseExecutionReviewed = true ∧ d.dualUseArtifactReviewed = true ∧
  d.dualUseDisclosureReviewed = true ∧ d.accessTierBound = true ∧
  d.residualOwnerBound = true ∧ Current d

def BoundaryComplete (d : ExperimentDossier) : Prop :=
  d.causalTruthClaimed = false ∧ d.generalDiscoveryClaimed = false ∧
  d.reproducibilityClaimed = false ∧ d.safetyClaimed = false ∧
  d.supportOrReleaseRequested = false

instance identityDecidable (d : ExperimentDossier) : Decidable (IdentityComplete d) := by
  unfold IdentityComplete; infer_instance
instance designDecidable (d : ExperimentDossier) : Decidable (DesignComplete d) := by
  unfold DesignComplete; infer_instance
instance executionDecidable (d : ExperimentDossier) : Decidable (ExecutionComplete d) := by
  unfold ExecutionComplete; infer_instance
instance analysisDecidable (d : ExperimentDossier) : Decidable (AnalysisComplete d) := by
  unfold AnalysisComplete; infer_instance
instance replicationDecidable (d : ExperimentDossier) : Decidable (ReplicationComplete d) := by
  unfold ReplicationComplete; infer_instance
instance governanceDecidable (d : ExperimentDossier) : Decidable (GovernanceComplete d) := by
  unfold GovernanceComplete Current; infer_instance
instance boundaryDecidable (d : ExperimentDossier) : Decidable (BoundaryComplete d) := by
  unfold BoundaryComplete; infer_instance

def DossierAdmissible (d : ExperimentDossier) : Prop :=
  IdentityComplete d ∧ DesignComplete d ∧ ExecutionComplete d ∧
  AnalysisComplete d ∧ ReplicationComplete d ∧ GovernanceComplete d ∧
  BoundaryComplete d
instance admissibleDecidable (d : ExperimentDossier) : Decidable (DossierAdmissible d) := by
  unfold DossierAdmissible IdentityComplete DesignComplete ExecutionComplete
    AnalysisComplete ReplicationComplete GovernanceComplete Current BoundaryComplete
  infer_instance
def DossierReady (d : ExperimentDossier) : Bool := decide (DossierAdmissible d)

inductive ReviewState where
  | proposed | identityReviewed | designReviewed | executionReviewed
  | analysisReviewed | replicationReviewed | governanceReviewed | boundaryReviewed
  | repairRequired | eligibleForTheseusGovernedExperimentCampaign
deriving DecidableEq, Repr

def ReviewStepFor (d : ExperimentDossier) : ReviewState -> ReviewState
  | .proposed => if decide (IdentityComplete d) then .identityReviewed else .repairRequired
  | .identityReviewed => if decide (DesignComplete d) then .designReviewed else .repairRequired
  | .designReviewed => if decide (ExecutionComplete d) then .executionReviewed else .repairRequired
  | .executionReviewed => if decide (AnalysisComplete d) then .analysisReviewed else .repairRequired
  | .analysisReviewed => if decide (ReplicationComplete d) then .replicationReviewed else .repairRequired
  | .replicationReviewed => if decide (GovernanceComplete d) then .governanceReviewed else .repairRequired
  | .governanceReviewed => if decide (BoundaryComplete d) then .boundaryReviewed else .repairRequired
  | .boundaryReviewed => .eligibleForTheseusGovernedExperimentCampaign
  | state => state

def ReviewRun (d : ExperimentDossier) : Nat -> ReviewState
  | 0 => .proposed
  | n + 1 => ReviewStepFor d (ReviewRun d n)

def StageInvariant (d : ExperimentDossier) : ReviewState -> Prop
  | .proposed => True
  | .identityReviewed => IdentityComplete d
  | .designReviewed => IdentityComplete d ∧ DesignComplete d
  | .executionReviewed => IdentityComplete d ∧ DesignComplete d ∧ ExecutionComplete d
  | .analysisReviewed =>
      IdentityComplete d ∧ DesignComplete d ∧ ExecutionComplete d ∧ AnalysisComplete d
  | .replicationReviewed =>
      IdentityComplete d ∧ DesignComplete d ∧ ExecutionComplete d ∧
        AnalysisComplete d ∧ ReplicationComplete d
  | .governanceReviewed =>
      IdentityComplete d ∧ DesignComplete d ∧ ExecutionComplete d ∧
        AnalysisComplete d ∧ ReplicationComplete d ∧ GovernanceComplete d
  | .boundaryReviewed | .eligibleForTheseusGovernedExperimentCampaign => DossierAdmissible d
  | .repairRequired => True

theorem review_step_preserves_stage_invariant
    (d : ExperimentDossier) (state : ReviewState) (h : StageInvariant d state) :
    StageInvariant d (ReviewStepFor d state) := by
  cases state <;> simp only [ReviewStepFor]
  case proposed => split <;> simp_all [StageInvariant]
  case identityReviewed => split <;> simp_all [StageInvariant]
  case designReviewed => split <;> simp_all [StageInvariant]
  case executionReviewed => split <;> simp_all [StageInvariant]
  case analysisReviewed => split <;> simp_all [StageInvariant]
  case replicationReviewed => split <;> simp_all [StageInvariant]
  case governanceReviewed => split <;> simp_all [StageInvariant, DossierAdmissible]
  all_goals simp_all [StageInvariant]

theorem review_run_preserves_stage_invariant (d : ExperimentDossier) (n : Nat) :
    StageInvariant d (ReviewRun d n) := by
  induction n with
  | zero => simp [ReviewRun, StageInvariant]
  | succ n ih => simpa [ReviewRun] using review_step_preserves_stage_invariant d _ ih

theorem campaign_eligibility_requires_admissible_dossier
    (d : ExperimentDossier) (n : Nat)
    (h : ReviewRun d n = .eligibleForTheseusGovernedExperimentCampaign) :
    DossierAdmissible d := by
  have invariant := review_run_preserves_stage_invariant d n
  simpa [h, StageInvariant] using invariant

def completeDossier : ExperimentDossier := {}
theorem complete_dossier_is_ready : DossierReady completeDossier = true := by decide
theorem complete_dossier_reaches_only_theseus_governed_experiment_campaign :
    ReviewRun completeDossier 8 = .eligibleForTheseusGovernedExperimentCampaign := by decide

inductive AdmissionAxis where
  | claimIdentity | hypothesisIdentity | hypothesisVersion | hypothesisAncestry
  | exploratoryConfirmatory | protocolVersion | instrumentVersion | dataSnapshot
  | analysisVersion | environment | preregistration | outcomesFrozen | samplingPlan
  | powerPrecision | controls | randomization | blinding | holdout | stoppingRule
  | exclusions | alternatives | causalAssumptions | instrumentLease | calibration
  | operatingEnvelope | sampleIdentity | safetyInterlocks | independentStopAuthority
  | attemptDenominator | humanInterventions | protocolDeviations | rawObservations
  | codeParameters | contaminationDriftControls | independentAnalysis | robustnessChecks
  | nullNegativeResults | correctionLineage | replicationContract
  | replicationIndependence | disagreement | dualUseQuestion | dualUseProtocol
  | dualUseExecution | dualUseArtifact | dualUseDisclosure | accessTier | residualOwner
  | expiry | causalTruthClaim | generalDiscoveryClaim | reproducibilityClaim
  | safetyClaim | supportOrRelease
deriving DecidableEq, Repr

def omitAxis : AdmissionAxis -> ExperimentDossier
  | .claimIdentity => { completeDossier with claimIdentityBound := false }
  | .hypothesisIdentity => { completeDossier with hypothesisIdentityBound := false }
  | .hypothesisVersion => { completeDossier with hypothesisVersionBound := false }
  | .hypothesisAncestry => { completeDossier with hypothesisAncestryBound := false }
  | .exploratoryConfirmatory => { completeDossier with exploratoryConfirmatoryBound := false }
  | .protocolVersion => { completeDossier with protocolVersionBound := false }
  | .instrumentVersion => { completeDossier with instrumentVersionBound := false }
  | .dataSnapshot => { completeDossier with dataSnapshotBound := false }
  | .analysisVersion => { completeDossier with analysisVersionBound := false }
  | .environment => { completeDossier with environmentBound := false }
  | .preregistration => { completeDossier with preregistrationBound := false }
  | .outcomesFrozen => { completeDossier with outcomesFrozenBeforeOpen := false }
  | .samplingPlan => { completeDossier with samplingPlanBound := false }
  | .powerPrecision => { completeDossier with powerPrecisionBound := false }
  | .controls => { completeDossier with controlsBound := false }
  | .randomization => { completeDossier with randomizationBound := false }
  | .blinding => { completeDossier with blindingBound := false }
  | .holdout => { completeDossier with holdoutBound := false }
  | .stoppingRule => { completeDossier with stoppingRuleBound := false }
  | .exclusions => { completeDossier with exclusionsBound := false }
  | .alternatives => { completeDossier with alternativesBound := false }
  | .causalAssumptions => { completeDossier with causalAssumptionsBound := false }
  | .instrumentLease => { completeDossier with instrumentLeaseBound := false }
  | .calibration => { completeDossier with calibrationBound := false }
  | .operatingEnvelope => { completeDossier with operatingEnvelopeBound := false }
  | .sampleIdentity => { completeDossier with sampleIdentityBound := false }
  | .safetyInterlocks => { completeDossier with safetyInterlocksBound := false }
  | .independentStopAuthority => { completeDossier with independentStopAuthorityBound := false }
  | .attemptDenominator => { completeDossier with attemptDenominatorComplete := false }
  | .humanInterventions => { completeDossier with humanInterventionsPreserved := false }
  | .protocolDeviations => { completeDossier with protocolDeviationsPreserved := false }
  | .rawObservations => { completeDossier with rawObservationsPreserved := false }
  | .codeParameters => { completeDossier with codeParametersBound := false }
  | .contaminationDriftControls => { completeDossier with contaminationDriftControlsBound := false }
  | .independentAnalysis => { completeDossier with independentAnalysisBound := false }
  | .robustnessChecks => { completeDossier with robustnessChecksBound := false }
  | .nullNegativeResults => { completeDossier with nullNegativeResultsPreserved := false }
  | .correctionLineage => { completeDossier with correctionLineagePresent := false }
  | .replicationContract => { completeDossier with replicationContractBound := false }
  | .replicationIndependence => { completeDossier with replicationIndependenceBound := false }
  | .disagreement => { completeDossier with disagreementPreserved := false }
  | .dualUseQuestion => { completeDossier with dualUseQuestionReviewed := false }
  | .dualUseProtocol => { completeDossier with dualUseProtocolReviewed := false }
  | .dualUseExecution => { completeDossier with dualUseExecutionReviewed := false }
  | .dualUseArtifact => { completeDossier with dualUseArtifactReviewed := false }
  | .dualUseDisclosure => { completeDossier with dualUseDisclosureReviewed := false }
  | .accessTier => { completeDossier with accessTierBound := false }
  | .residualOwner => { completeDossier with residualOwnerBound := false }
  | .expiry => { completeDossier with currentTick := 21 }
  | .causalTruthClaim => { completeDossier with causalTruthClaimed := true }
  | .generalDiscoveryClaim => { completeDossier with generalDiscoveryClaimed := true }
  | .reproducibilityClaim => { completeDossier with reproducibilityClaimed := true }
  | .safetyClaim => { completeDossier with safetyClaimed := true }
  | .supportOrRelease => { completeDossier with supportOrReleaseRequested := true }

inductive RepairDisposition where
  | bindClaimIdentity | bindHypothesisIdentity | bindHypothesisVersion
  | bindHypothesisAncestry | separateExplorationConfirmation | bindProtocolVersion
  | bindInstrumentVersion | bindDataSnapshot | bindAnalysisVersion | bindEnvironment
  | preregisterBeforeOpening | freezeOutcomes | bindSamplingPlan | bindPowerPrecision
  | bindControls | bindRandomization | bindBlinding | bindHoldout | bindStoppingRule
  | bindExclusions | bindAlternatives | bindCausalAssumptions | bindInstrumentLease
  | bindCalibration | bindOperatingEnvelope | bindSampleIdentity | bindSafetyInterlocks
  | bindIndependentStopAuthority | completeAttemptDenominator | preserveHumanInterventions
  | preserveProtocolDeviations | preserveRawObservations | bindCodeParameters
  | bindContaminationDriftControls | bindIndependentAnalysis | bindRobustnessChecks
  | preserveNullNegativeResults | addCorrectionLineage | bindReplicationContract
  | bindReplicationIndependence | preserveDisagreement | reviewDualUseQuestion
  | reviewDualUseProtocol | reviewDualUseExecution | reviewDualUseArtifact
  | reviewDualUseDisclosure | bindAccessTier | assignResidualOwner | renewExpiry
  | rejectCausalTruthClaim | rejectGeneralDiscoveryClaim | rejectReproducibilityClaim
  | rejectSafetyClaim | refuseSupportOrRelease
  | eligibleForTheseusGovernedExperimentCampaign
deriving DecidableEq, Repr

def repairForAxis : AdmissionAxis -> RepairDisposition
  | .claimIdentity => .bindClaimIdentity | .hypothesisIdentity => .bindHypothesisIdentity
  | .hypothesisVersion => .bindHypothesisVersion | .hypothesisAncestry => .bindHypothesisAncestry
  | .exploratoryConfirmatory => .separateExplorationConfirmation
  | .protocolVersion => .bindProtocolVersion | .instrumentVersion => .bindInstrumentVersion
  | .dataSnapshot => .bindDataSnapshot | .analysisVersion => .bindAnalysisVersion
  | .environment => .bindEnvironment | .preregistration => .preregisterBeforeOpening
  | .outcomesFrozen => .freezeOutcomes | .samplingPlan => .bindSamplingPlan
  | .powerPrecision => .bindPowerPrecision | .controls => .bindControls
  | .randomization => .bindRandomization | .blinding => .bindBlinding
  | .holdout => .bindHoldout | .stoppingRule => .bindStoppingRule
  | .exclusions => .bindExclusions | .alternatives => .bindAlternatives
  | .causalAssumptions => .bindCausalAssumptions | .instrumentLease => .bindInstrumentLease
  | .calibration => .bindCalibration | .operatingEnvelope => .bindOperatingEnvelope
  | .sampleIdentity => .bindSampleIdentity | .safetyInterlocks => .bindSafetyInterlocks
  | .independentStopAuthority => .bindIndependentStopAuthority
  | .attemptDenominator => .completeAttemptDenominator
  | .humanInterventions => .preserveHumanInterventions
  | .protocolDeviations => .preserveProtocolDeviations
  | .rawObservations => .preserveRawObservations | .codeParameters => .bindCodeParameters
  | .contaminationDriftControls => .bindContaminationDriftControls
  | .independentAnalysis => .bindIndependentAnalysis | .robustnessChecks => .bindRobustnessChecks
  | .nullNegativeResults => .preserveNullNegativeResults
  | .correctionLineage => .addCorrectionLineage | .replicationContract => .bindReplicationContract
  | .replicationIndependence => .bindReplicationIndependence
  | .disagreement => .preserveDisagreement | .dualUseQuestion => .reviewDualUseQuestion
  | .dualUseProtocol => .reviewDualUseProtocol | .dualUseExecution => .reviewDualUseExecution
  | .dualUseArtifact => .reviewDualUseArtifact | .dualUseDisclosure => .reviewDualUseDisclosure
  | .accessTier => .bindAccessTier | .residualOwner => .assignResidualOwner
  | .expiry => .renewExpiry | .causalTruthClaim => .rejectCausalTruthClaim
  | .generalDiscoveryClaim => .rejectGeneralDiscoveryClaim
  | .reproducibilityClaim => .rejectReproducibilityClaim
  | .safetyClaim => .rejectSafetyClaim | .supportOrRelease => .refuseSupportOrRelease

def ExactRepairFor (d : ExperimentDossier) : RepairDisposition :=
  if !d.claimIdentityBound then .bindClaimIdentity
  else if !d.hypothesisIdentityBound then .bindHypothesisIdentity
  else if !d.hypothesisVersionBound then .bindHypothesisVersion
  else if !d.hypothesisAncestryBound then .bindHypothesisAncestry
  else if !d.exploratoryConfirmatoryBound then .separateExplorationConfirmation
  else if !d.protocolVersionBound then .bindProtocolVersion
  else if !d.instrumentVersionBound then .bindInstrumentVersion
  else if !d.dataSnapshotBound then .bindDataSnapshot
  else if !d.analysisVersionBound then .bindAnalysisVersion
  else if !d.environmentBound then .bindEnvironment
  else if !d.preregistrationBound then .preregisterBeforeOpening
  else if !d.outcomesFrozenBeforeOpen then .freezeOutcomes
  else if !d.samplingPlanBound then .bindSamplingPlan
  else if !d.powerPrecisionBound then .bindPowerPrecision
  else if !d.controlsBound then .bindControls
  else if !d.randomizationBound then .bindRandomization
  else if !d.blindingBound then .bindBlinding
  else if !d.holdoutBound then .bindHoldout
  else if !d.stoppingRuleBound then .bindStoppingRule
  else if !d.exclusionsBound then .bindExclusions
  else if !d.alternativesBound then .bindAlternatives
  else if !d.causalAssumptionsBound then .bindCausalAssumptions
  else if !d.instrumentLeaseBound then .bindInstrumentLease
  else if !d.calibrationBound then .bindCalibration
  else if !d.operatingEnvelopeBound then .bindOperatingEnvelope
  else if !d.sampleIdentityBound then .bindSampleIdentity
  else if !d.safetyInterlocksBound then .bindSafetyInterlocks
  else if !d.independentStopAuthorityBound then .bindIndependentStopAuthority
  else if !d.attemptDenominatorComplete then .completeAttemptDenominator
  else if !d.humanInterventionsPreserved then .preserveHumanInterventions
  else if !d.protocolDeviationsPreserved then .preserveProtocolDeviations
  else if !d.rawObservationsPreserved then .preserveRawObservations
  else if !d.codeParametersBound then .bindCodeParameters
  else if !d.contaminationDriftControlsBound then .bindContaminationDriftControls
  else if !d.independentAnalysisBound then .bindIndependentAnalysis
  else if !d.robustnessChecksBound then .bindRobustnessChecks
  else if !d.nullNegativeResultsPreserved then .preserveNullNegativeResults
  else if !d.correctionLineagePresent then .addCorrectionLineage
  else if !d.replicationContractBound then .bindReplicationContract
  else if !d.replicationIndependenceBound then .bindReplicationIndependence
  else if !d.disagreementPreserved then .preserveDisagreement
  else if !d.dualUseQuestionReviewed then .reviewDualUseQuestion
  else if !d.dualUseProtocolReviewed then .reviewDualUseProtocol
  else if !d.dualUseExecutionReviewed then .reviewDualUseExecution
  else if !d.dualUseArtifactReviewed then .reviewDualUseArtifact
  else if !d.dualUseDisclosureReviewed then .reviewDualUseDisclosure
  else if !d.accessTierBound then .bindAccessTier
  else if !d.residualOwnerBound then .assignResidualOwner
  else if !decide (Current d) then .renewExpiry
  else if d.causalTruthClaimed then .rejectCausalTruthClaim
  else if d.generalDiscoveryClaimed then .rejectGeneralDiscoveryClaim
  else if d.reproducibilityClaimed then .rejectReproducibilityClaim
  else if d.safetyClaimed then .rejectSafetyClaim
  else if d.supportOrReleaseRequested then .refuseSupportOrRelease
  else .eligibleForTheseusGovernedExperimentCampaign

theorem every_admission_axis_mutation_blocks_readiness (axis : AdmissionAxis) :
    DossierReady (omitAxis axis) = false := by cases axis <;> decide
theorem every_admission_axis_mutation_has_exact_repair (axis : AdmissionAxis) :
    ExactRepairFor (omitAxis axis) = repairForAxis axis := by cases axis <;> decide
theorem every_admission_axis_mutation_reaches_repair (axis : AdmissionAxis) :
    ReviewRun (omitAxis axis) 8 = .repairRequired := by cases axis <;> decide

theorem readiness_requires_identity (d : ExperimentDossier) (h : DossierReady d = true) :
    IdentityComplete d := by exact (of_decide_eq_true h).1
theorem readiness_requires_design (d : ExperimentDossier) (h : DossierReady d = true) :
    DesignComplete d := by exact (of_decide_eq_true h).2.1
theorem readiness_requires_execution (d : ExperimentDossier) (h : DossierReady d = true) :
    ExecutionComplete d := by exact (of_decide_eq_true h).2.2.1
theorem readiness_requires_analysis (d : ExperimentDossier) (h : DossierReady d = true) :
    AnalysisComplete d := by exact (of_decide_eq_true h).2.2.2.1
theorem readiness_requires_replication (d : ExperimentDossier) (h : DossierReady d = true) :
    ReplicationComplete d := by exact (of_decide_eq_true h).2.2.2.2.1
theorem readiness_requires_governance (d : ExperimentDossier) (h : DossierReady d = true) :
    GovernanceComplete d := by exact (of_decide_eq_true h).2.2.2.2.2.1
theorem readiness_requires_boundary (d : ExperimentDossier) (h : DossierReady d = true) :
    BoundaryComplete d := by exact (of_decide_eq_true h).2.2.2.2.2.2

theorem expired_experiment_contract_remains_expired_when_time_advances
    (expiresAt now later : Nat) (expired : expiresAt < now) (advances : now <= later) :
    expiresAt < later := Nat.lt_of_lt_of_le expired advances

theorem omitted_attempt_gap_persists_when_included_count_falls
    (included total includedLater : Nat) (gap : included < total)
    (falls : includedLater <= included) : includedLater < total :=
  Nat.lt_of_le_of_lt falls gap

theorem replication_gap_persists_when_independent_count_falls
    (independent required independentLater : Nat) (gap : independent < required)
    (falls : independentLater <= independent) : independentLater < required :=
  Nat.lt_of_le_of_lt falls gap

structure ExperimentReceiptScope where
  hypothesisId : Nat
  protocolVersion : Nat
  instrumentVersion : Nat
  dataSnapshotId : Nat
  analysisVersion : Nat
  environmentId : Nat
  claimCeilingId : Nat
deriving DecidableEq, Repr

def ReceiptApplies (receipt current : ExperimentReceiptScope) : Prop := receipt = current

theorem hypothesis_change_invalidates_experiment_receipt
    (r : ExperimentReceiptScope) (changed : r.hypothesisId ≠ h) :
    Not (ReceiptApplies r { r with hypothesisId := h }) := by intro same; exact changed (congrArg ExperimentReceiptScope.hypothesisId same)
theorem protocol_change_invalidates_experiment_receipt
    (r : ExperimentReceiptScope) (changed : r.protocolVersion ≠ p) :
    Not (ReceiptApplies r { r with protocolVersion := p }) := by intro same; exact changed (congrArg ExperimentReceiptScope.protocolVersion same)
theorem instrument_change_invalidates_experiment_receipt
    (r : ExperimentReceiptScope) (changed : r.instrumentVersion ≠ i) :
    Not (ReceiptApplies r { r with instrumentVersion := i }) := by intro same; exact changed (congrArg ExperimentReceiptScope.instrumentVersion same)
theorem data_change_invalidates_experiment_receipt
    (r : ExperimentReceiptScope) (changed : r.dataSnapshotId ≠ s) :
    Not (ReceiptApplies r { r with dataSnapshotId := s }) := by intro same; exact changed (congrArg ExperimentReceiptScope.dataSnapshotId same)
theorem analysis_change_invalidates_experiment_receipt
    (r : ExperimentReceiptScope) (changed : r.analysisVersion ≠ a) :
    Not (ReceiptApplies r { r with analysisVersion := a }) := by intro same; exact changed (congrArg ExperimentReceiptScope.analysisVersion same)
theorem environment_change_invalidates_experiment_receipt
    (r : ExperimentReceiptScope) (changed : r.environmentId ≠ e) :
    Not (ReceiptApplies r { r with environmentId := e }) := by intro same; exact changed (congrArg ExperimentReceiptScope.environmentId same)
theorem claim_ceiling_change_invalidates_experiment_receipt
    (r : ExperimentReceiptScope) (changed : r.claimCeilingId ≠ c) :
    Not (ReceiptApplies r { r with claimCeilingId := c }) := by intro same; exact changed (congrArg ExperimentReceiptScope.claimCeilingId same)

structure SignificanceSignals where
  pValueBand : Nat
  effectBand : Nat
deriving DecidableEq, Repr
structure SignificanceCase where
  signals : SignificanceSignals
  preregistrationIntact : Bool
deriving DecidableEq, Repr

def significantIntact : SignificanceCase := { signals := { pValueBand := 1, effectBand := 3 }, preregistrationIntact := true }
def significantPostHoc : SignificanceCase := { signals := { pValueBand := 1, effectBand := 3 }, preregistrationIntact := false }

theorem identical_significance_can_hide_opposite_preregistration_integrity :
    significantIntact.signals = significantPostHoc.signals ∧
      significantIntact.preregistrationIntact ≠ significantPostHoc.preregistrationIntact := by decide

theorem significance_signals_cannot_recover_preregistration_integrity
    (classify : SignificanceSignals -> Bool) :
    Not (forall c : SignificanceCase, classify c.signals = c.preregistrationIntact) := by
  intro exactClassifier
  have left := exactClassifier significantIntact
  have right := exactClassifier significantPostHoc
  simp [significantIntact, significantPostHoc] at left right
  rw [left] at right
  simp at right

structure ReplicationSignals where
  successfulRuns : Nat
  resultBand : Nat
deriving DecidableEq, Repr
structure ReplicationCase where
  signals : ReplicationSignals
  independent : Bool
deriving DecidableEq, Repr

def independentReplication : ReplicationCase := { signals := { successfulRuns := 2, resultBand := 5 }, independent := true }
def sharedDefectReplication : ReplicationCase := { signals := { successfulRuns := 2, resultBand := 5 }, independent := false }

theorem identical_replication_counts_can_hide_opposite_independence :
    independentReplication.signals = sharedDefectReplication.signals ∧
      independentReplication.independent ≠ sharedDefectReplication.independent := by decide

theorem replication_counts_cannot_recover_independence
    (classify : ReplicationSignals -> Bool) :
    Not (forall c : ReplicationCase, classify c.signals = c.independent) := by
  intro exactClassifier
  have left := exactClassifier independentReplication
  have right := exactClassifier sharedDefectReplication
  simp [independentReplication, sharedDefectReplication] at left right
  rw [left] at right
  simp at right

def evidenceWithoutIndependentReplication : EvidenceBundle :=
  { sourceNote := True, prototypeInspection := True, syntheticTestRun := True,
    empiricalTestRun := False, externalLiterature := True }

theorem missing_independent_replication_blocks_empirical_support_promotion :
    Not (PromotionAllowed evidenceWithoutIndependentReplication
      SupportState.argument SupportState.empiricalTestBacked) := by
  apply missing_required_evidence_blocks_promotion
  simp [RequiredEvidence, evidenceWithoutIndependentReplication]

def ratchetWithoutNullResults : BenchmarkRatchets.RatchetDecisionReview :=
  { lifecycle := .frontier, benchmarkSaturated := false,
    contaminationSuspected := false, transferOrMutationCheckPresent := true,
    regressionRecordsPreserved := true, negativeResultsPreserved := false,
    decision := .promoteReadiness }

theorem missing_null_results_rejects_benchmark_ratchet_promotion :
    Not (BenchmarkRatchets.RatchetDecisionAccepted ratchetWithoutNullResults) := by
  simp [BenchmarkRatchets.RatchetDecisionAccepted, ratchetWithoutNullResults]

end AsiStackProofs.ScientificExperimentReview
