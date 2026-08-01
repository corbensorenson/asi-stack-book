namespace AsiStackProofs.MultiAgentDynamics

inductive Agent where
  | human
  | systemA
  | systemB
deriving DecidableEq, Repr

inductive Resource where
  | compute
  | capital
deriving DecidableEq, Repr

inductive AffectedParty where
  | participant
  | bystander
deriving DecidableEq, Repr

structure PopulationRecord where
  populationRegistered : Bool
  pairwiseAuthorized : Agent -> Agent -> Bool
  modelLineage : Agent -> Nat
  resourceController : Resource -> Agent
  humanCanStop : Agent -> Bool
  affectedPartyCovered : AffectedParty -> Bool
  humanExitReachable : Bool
  recoveryReachable : Bool
  residualCustodyPresent : Bool
  nonClaimBoundaryPresent : Bool

def PairwiseValid (record : PopulationRecord) : Bool :=
  record.pairwiseAuthorized .human .systemA &&
    record.pairwiseAuthorized .systemA .human &&
      record.pairwiseAuthorized .human .systemB &&
        record.pairwiseAuthorized .systemB .human &&
          record.pairwiseAuthorized .systemA .systemB &&
            record.pairwiseAuthorized .systemB .systemA

def EffectiveDiversityPresent (record : PopulationRecord) : Bool :=
  decide (record.modelLineage .systemA != record.modelLineage .systemB)

def ResourceControlDiversified (record : PopulationRecord) : Bool :=
  decide (record.resourceController .compute != record.resourceController .capital)

def HumanStopReachable (record : PopulationRecord) : Bool :=
  record.humanCanStop .systemA && record.humanCanStop .systemB

def AffectedPartiesCovered (record : PopulationRecord) : Bool :=
  record.affectedPartyCovered .participant &&
    record.affectedPartyCovered .bystander

def PopulationCampaignReady (record : PopulationRecord) : Bool :=
  record.populationRegistered &&
    (PairwiseValid record &&
      (EffectiveDiversityPresent record &&
        (ResourceControlDiversified record &&
          (HumanStopReachable record &&
            (AffectedPartiesCovered record &&
              (record.humanExitReachable &&
                (record.recoveryReachable &&
                  (record.residualCustodyPresent &&
                    record.nonClaimBoundaryPresent))))))))

inductive PopulationReviewRoute where
  | repairPopulationRegistry
  | repairPairwiseAuthorization
  | mapCommonDependencies
  | diversifyResourceControl
  | restoreHumanStop
  | coverAffectedParties
  | restoreHumanExit
  | establishRecovery
  | assignResidualCustody
  | recordNonClaimBoundary
  | runTheseusPopulationCampaign
deriving DecidableEq, Repr

def PopulationReviewRouteFor (record : PopulationRecord) : PopulationReviewRoute :=
  if ! record.populationRegistered then .repairPopulationRegistry
  else if ! PairwiseValid record then .repairPairwiseAuthorization
  else if ! EffectiveDiversityPresent record then .mapCommonDependencies
  else if ! ResourceControlDiversified record then .diversifyResourceControl
  else if ! HumanStopReachable record then .restoreHumanStop
  else if ! AffectedPartiesCovered record then .coverAffectedParties
  else if ! record.humanExitReachable then .restoreHumanExit
  else if ! record.recoveryReachable then .establishRecovery
  else if ! record.residualCustodyPresent then .assignResidualCustody
  else if ! record.nonClaimBoundaryPresent then .recordNonClaimBoundary
  else .runTheseusPopulationCampaign

def completePopulation : PopulationRecord where
  populationRegistered := true
  pairwiseAuthorized := fun _ _ => true
  modelLineage
    | .human => 0
    | .systemA => 1
    | .systemB => 2
  resourceController
    | .compute => .systemA
    | .capital => .systemB
  humanCanStop := fun _ => true
  affectedPartyCovered := fun _ => true
  humanExitReachable := true
  recoveryReachable := true
  residualCustodyPresent := true
  nonClaimBoundaryPresent := true

def pairwiseOnlyPopulation : PopulationRecord where
  populationRegistered := true
  pairwiseAuthorized := fun _ _ => true
  modelLineage := fun _ => 0
  resourceController := fun _ => .systemA
  humanCanStop := fun _ => false
  affectedPartyCovered := fun _ => false
  humanExitReachable := false
  recoveryReachable := false
  residualCustodyPresent := false
  nonClaimBoundaryPresent := true

inductive SystemicAxis where
  | populationRegistry
  | effectiveDiversity
  | resourceConcentration
  | humanStop
  | affectedParties
  | humanExit
  | recovery
  | residualCustody
  | nonClaimBoundary
deriving DecidableEq, Repr

def omitSystemicAxis (axis : SystemicAxis) : PopulationRecord :=
  match axis with
  | .populationRegistry => { completePopulation with populationRegistered := false }
  | .effectiveDiversity => { completePopulation with modelLineage := fun _ => 0 }
  | .resourceConcentration =>
      { completePopulation with resourceController := fun _ => .systemA }
  | .humanStop => { completePopulation with humanCanStop := fun _ => false }
  | .affectedParties =>
      { completePopulation with affectedPartyCovered := fun _ => false }
  | .humanExit => { completePopulation with humanExitReachable := false }
  | .recovery => { completePopulation with recoveryReachable := false }
  | .residualCustody => { completePopulation with residualCustodyPresent := false }
  | .nonClaimBoundary => { completePopulation with nonClaimBoundaryPresent := false }

def repairRouteForAxis : SystemicAxis -> PopulationReviewRoute
  | .populationRegistry => .repairPopulationRegistry
  | .effectiveDiversity => .mapCommonDependencies
  | .resourceConcentration => .diversifyResourceControl
  | .humanStop => .restoreHumanStop
  | .affectedParties => .coverAffectedParties
  | .humanExit => .restoreHumanExit
  | .recovery => .establishRecovery
  | .residualCustody => .assignResidualCustody
  | .nonClaimBoundary => .recordNonClaimBoundary

theorem complete_population_has_pairwise_validity :
    PairwiseValid completePopulation = true := by decide

theorem complete_population_is_campaign_ready :
    PopulationCampaignReady completePopulation = true := by decide

theorem complete_population_routes_to_theseus_campaign :
    PopulationReviewRouteFor completePopulation =
      .runTheseusPopulationCampaign := by decide

theorem pairwise_only_population_has_pairwise_validity :
    PairwiseValid pairwiseOnlyPopulation = true := by decide

theorem pairwise_only_population_is_not_campaign_ready :
    PopulationCampaignReady pairwiseOnlyPopulation = false := by decide

theorem pairwise_only_population_routes_to_dependency_mapping :
    PopulationReviewRouteFor pairwiseOnlyPopulation =
      .mapCommonDependencies := by decide

theorem complete_and_pairwise_only_have_identical_pairwise_evidence :
    completePopulation.pairwiseAuthorized =
      pairwiseOnlyPopulation.pairwiseAuthorized := by rfl

theorem pairwise_validity_does_not_entail_population_campaign_readiness :
    ∃ record : PopulationRecord,
      PairwiseValid record = true ∧ PopulationCampaignReady record = false := by
  exact ⟨pairwiseOnlyPopulation, by decide, by decide⟩

theorem no_pairwise_only_classifier_exactly_recovers_campaign_readiness :
    ¬ ∃ classifier : (Agent -> Agent -> Bool) -> Bool,
      ∀ record : PopulationRecord,
        classifier record.pairwiseAuthorized = PopulationCampaignReady record := by
  rintro ⟨classifier, exactForEveryRecord⟩
  have completeResult := exactForEveryRecord completePopulation
  have pairwiseOnlyResult := exactForEveryRecord pairwiseOnlyPopulation
  rw [complete_population_is_campaign_ready] at completeResult
  rw [pairwise_only_population_is_not_campaign_ready] at pairwiseOnlyResult
  rw [complete_and_pairwise_only_have_identical_pairwise_evidence] at completeResult
  simp [completeResult] at pairwiseOnlyResult

theorem every_systemic_axis_omission_preserves_pairwise_validity
    (axis : SystemicAxis) :
    PairwiseValid (omitSystemicAxis axis) = true := by
  cases axis <;> decide

theorem every_systemic_axis_omission_blocks_campaign_readiness
    (axis : SystemicAxis) :
    PopulationCampaignReady (omitSystemicAxis axis) = false := by
  cases axis <;> decide

theorem every_systemic_axis_omission_reaches_exact_repair_route
    (axis : SystemicAxis) :
    PopulationReviewRouteFor (omitSystemicAxis axis) = repairRouteForAxis axis := by
  cases axis <;> decide

theorem campaign_readiness_requires_population_registry
    (record : PopulationRecord)
    (ready : PopulationCampaignReady record = true) :
    record.populationRegistered = true := by
  simp [PopulationCampaignReady] at ready
  exact ready.1

theorem campaign_readiness_requires_pairwise_validity
    (record : PopulationRecord)
    (ready : PopulationCampaignReady record = true) :
    PairwiseValid record = true := by
  simp [PopulationCampaignReady] at ready
  exact ready.2.1

theorem campaign_readiness_requires_effective_diversity
    (record : PopulationRecord)
    (ready : PopulationCampaignReady record = true) :
    EffectiveDiversityPresent record = true := by
  simp [PopulationCampaignReady] at ready
  exact ready.2.2.1

theorem campaign_readiness_requires_diversified_resource_control
    (record : PopulationRecord)
    (ready : PopulationCampaignReady record = true) :
    ResourceControlDiversified record = true := by
  simp [PopulationCampaignReady] at ready
  exact ready.2.2.2.1

theorem campaign_readiness_requires_human_stop
    (record : PopulationRecord)
    (ready : PopulationCampaignReady record = true) :
    HumanStopReachable record = true := by
  simp [PopulationCampaignReady] at ready
  exact ready.2.2.2.2.1

theorem campaign_readiness_requires_affected_party_coverage
    (record : PopulationRecord)
    (ready : PopulationCampaignReady record = true) :
    AffectedPartiesCovered record = true := by
  simp [PopulationCampaignReady] at ready
  exact ready.2.2.2.2.2.1

theorem campaign_readiness_requires_human_exit
    (record : PopulationRecord)
    (ready : PopulationCampaignReady record = true) :
    record.humanExitReachable = true := by
  simp [PopulationCampaignReady] at ready
  exact ready.2.2.2.2.2.2.1

theorem campaign_readiness_requires_recovery
    (record : PopulationRecord)
    (ready : PopulationCampaignReady record = true) :
    record.recoveryReachable = true := by
  simp [PopulationCampaignReady] at ready
  exact ready.2.2.2.2.2.2.2.1

theorem campaign_readiness_requires_residual_custody
    (record : PopulationRecord)
    (ready : PopulationCampaignReady record = true) :
    record.residualCustodyPresent = true := by
  simp [PopulationCampaignReady] at ready
  exact ready.2.2.2.2.2.2.2.2.1

theorem campaign_readiness_requires_non_claim_boundary
    (record : PopulationRecord)
    (ready : PopulationCampaignReady record = true) :
    record.nonClaimBoundaryPresent = true := by
  simp [PopulationCampaignReady] at ready
  exact ready.2.2.2.2.2.2.2.2.2

end AsiStackProofs.MultiAgentDynamics
