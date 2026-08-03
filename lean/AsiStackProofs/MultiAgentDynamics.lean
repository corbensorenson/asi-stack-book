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

structure AllocationState where
  totalUnits : Nat
  unallocatedUnits : Nat
  systemAUnits : Nat
  systemBUnits : Nat
  concentrationLimit : Nat
  receiptCount : Nat
  supportAssignmentCount : Nat
  externalEffectAuthorityCount : Nat
deriving DecidableEq, Repr

structure AllocationEvent where
  target : Agent
  units : Nat
  pairwiseAuthorized : Bool
  supportAssignmentRequested : Bool
  externalEffectAuthorityRequested : Bool
deriving DecidableEq, Repr

def AllocationConserved (state : AllocationState) : Prop :=
  state.unallocatedUnits + state.systemAUnits + state.systemBUnits =
    state.totalUnits

def AllocationEventValid
    (state : AllocationState) (event : AllocationEvent) : Prop :=
  AllocationConserved state ∧
    event.pairwiseAuthorized = true ∧
    0 < event.units ∧
    event.units ≤ 1 ∧
    event.units ≤ state.unallocatedUnits ∧
    event.target ≠ .human ∧
    event.supportAssignmentRequested = false ∧
    event.externalEffectAuthorityRequested = false

instance allocationEventValidDecidable
    (state : AllocationState) (event : AllocationEvent) :
    Decidable (AllocationEventValid state event) := by
  unfold AllocationEventValid AllocationConserved
  infer_instance

def applyAllocationEvent
    (state : AllocationState) (event : AllocationEvent) : AllocationState :=
  match event.target with
  | .human => state
  | .systemA =>
      { state with
        unallocatedUnits := state.unallocatedUnits - event.units
        systemAUnits := state.systemAUnits + event.units
        receiptCount := state.receiptCount + 1 }
  | .systemB =>
      { state with
        unallocatedUnits := state.unallocatedUnits - event.units
        systemBUnits := state.systemBUnits + event.units
        receiptCount := state.receiptCount + 1 }

def AllocationStep
    (state : AllocationState) (event : AllocationEvent) : Option AllocationState :=
  if AllocationEventValid state event then
    some (applyAllocationEvent state event)
  else none

def AllocationRun : AllocationState → List AllocationEvent → Option AllocationState
  | state, [] => some state
  | state, event :: tail =>
      match AllocationStep state event with
      | none => none
      | some next => AllocationRun next tail

def ProcessAllocationEvent
    (state : AllocationState) (event : AllocationEvent) : AllocationState × Bool :=
  match AllocationStep state event with
  | none => (state, false)
  | some next => (next, true)

theorem accepted_allocation_step_is_valid
    {state next : AllocationState} {event : AllocationEvent}
    (stepped : AllocationStep state event = some next) :
    AllocationEventValid state event := by
  unfold AllocationStep at stepped
  split at stepped
  · assumption
  · simp at stepped

theorem accepted_allocation_step_applies_event
    {state next : AllocationState} {event : AllocationEvent}
    (stepped : AllocationStep state event = some next) :
    next = applyAllocationEvent state event := by
  unfold AllocationStep at stepped
  split at stepped
  · exact Option.some.inj stepped |>.symm
  · simp at stepped

theorem accepted_allocation_step_preserves_conservation
    {state next : AllocationState} {event : AllocationEvent}
    (stepped : AllocationStep state event = some next) :
    AllocationConserved next := by
  have valid := accepted_allocation_step_is_valid stepped
  have applies := accepted_allocation_step_applies_event stepped
  rcases valid with ⟨conserved, _, positive, _, available, nonhuman, _, _⟩
  subst next
  cases target : event.target with
  | human => exact False.elim (nonhuman target)
  | systemA =>
      simp [applyAllocationEvent, target, AllocationConserved] at *
      omega
  | systemB =>
      simp [applyAllocationEvent, target, AllocationConserved] at *
      omega

theorem accepted_allocation_step_preserves_non_authority
    {state next : AllocationState} {event : AllocationEvent}
  (stepped : AllocationStep state event = some next) :
    next.supportAssignmentCount = state.supportAssignmentCount ∧
      next.externalEffectAuthorityCount = state.externalEffectAuthorityCount := by
  rw [accepted_allocation_step_applies_event stepped]
  cases target : event.target <;> simp [applyAllocationEvent, target]

theorem rejected_allocation_step_preserves_exact_state
    (state : AllocationState) (event : AllocationEvent)
    (rejected : AllocationStep state event = none) :
    ProcessAllocationEvent state event = (state, false) := by
  simp [ProcessAllocationEvent, rejected]

theorem successful_allocation_run_preserves_conservation
    {state final : AllocationState} {events : List AllocationEvent}
    (initial : AllocationConserved state)
    (ran : AllocationRun state events = some final) :
    AllocationConserved final := by
  induction events generalizing state with
  | nil =>
      simp [AllocationRun] at ran
      subst final
      exact initial
  | cons event tail ih =>
      cases stepped : AllocationStep state event with
      | none => simp [AllocationRun, stepped] at ran
      | some next =>
          have tailRan : AllocationRun next tail = some final := by
            simpa [AllocationRun, stepped] using ran
          exact ih (accepted_allocation_step_preserves_conservation stepped) tailRan

theorem successful_allocation_run_preserves_non_authority
    {state final : AllocationState} {events : List AllocationEvent}
    (ran : AllocationRun state events = some final) :
    final.supportAssignmentCount = state.supportAssignmentCount ∧
      final.externalEffectAuthorityCount = state.externalEffectAuthorityCount := by
  induction events generalizing state with
  | nil =>
      simp [AllocationRun] at ran
      subst final
      exact ⟨rfl, rfl⟩
  | cons event tail ih =>
      cases stepped : AllocationStep state event with
      | none => simp [AllocationRun, stepped] at ran
      | some next =>
          have tailRan : AllocationRun next tail = some final := by
            simpa [AllocationRun, stepped] using ran
          have rest := ih tailRan
          have head := accepted_allocation_step_preserves_non_authority stepped
          exact ⟨rest.1.trans head.1, rest.2.trans head.2⟩

theorem successful_allocation_run_accounts_receipts
    {state final : AllocationState} {events : List AllocationEvent}
    (ran : AllocationRun state events = some final) :
    final.receiptCount = state.receiptCount + events.length := by
  induction events generalizing state with
  | nil =>
      simp [AllocationRun] at ran
      subst final
      simp
  | cons event tail ih =>
      cases stepped : AllocationStep state event with
      | none => simp [AllocationRun, stepped] at ran
      | some next =>
          have tailRan : AllocationRun next tail = some final := by
            simpa [AllocationRun, stepped] using ran
          have applies := accepted_allocation_step_applies_event stepped
          have valid := accepted_allocation_step_is_valid stepped
          rcases valid with ⟨_, _, _, _, _, nonhuman, _, _⟩
          have head : next.receiptCount = state.receiptCount + 1 := by
            rw [applies]
            cases target : event.target with
            | human => exact False.elim (nonhuman target)
            | systemA => simp [applyAllocationEvent, target]
            | systemB => simp [applyAllocationEvent, target]
          calc
            final.receiptCount = next.receiptCount + tail.length := ih tailRan
            _ = (state.receiptCount + 1) + tail.length := by rw [head]
            _ = state.receiptCount + (event :: tail).length := by
              simp [Nat.add_comm, Nat.add_left_comm]

theorem allocation_runs_compose
    {state middle final : AllocationState}
    {front back : List AllocationEvent}
    (first : AllocationRun state front = some middle)
    (second : AllocationRun middle back = some final) :
    AllocationRun state (front ++ back) = some final := by
  induction front generalizing state middle with
  | nil =>
      simp [AllocationRun] at first
      subst middle
      exact second
  | cons event tail ih =>
      cases stepped : AllocationStep state event with
      | none => simp [AllocationRun, stepped] at first
      | some next =>
          have tailFirst : AllocationRun next tail = some middle := by
            simpa [AllocationRun, stepped] using first
          simpa [AllocationRun, stepped] using ih tailFirst second

theorem exhausted_allocation_state_rejects_every_event
    (state : AllocationState) (event : AllocationEvent)
    (exhausted : state.unallocatedUnits = 0) :
    ¬ AllocationEventValid state event := by
  intro valid
  rcases valid with ⟨_, _, positive, _, available, _, _, _⟩
  omega

theorem exhausted_allocation_state_has_no_nonempty_run
    (state : AllocationState) (event : AllocationEvent)
    (tail : List AllocationEvent) (exhausted : state.unallocatedUnits = 0) :
    AllocationRun state (event :: tail) = none := by
  have rejected := exhausted_allocation_state_rejects_every_event
    state event exhausted
  simp [AllocationRun, AllocationStep, rejected]

def allocationInitialState : AllocationState :=
  { totalUnits := 3
    unallocatedUnits := 3
    systemAUnits := 0
    systemBUnits := 0
    concentrationLimit := 2
    receiptCount := 0
    supportAssignmentCount := 0
    externalEffectAuthorityCount := 0 }

def allocationEvent (target : Agent) : AllocationEvent :=
  { target := target
    units := 1
    pairwiseAuthorized := true
    supportAssignmentRequested := false
    externalEffectAuthorityRequested := false }

def concentratedAllocationEvents : List AllocationEvent :=
  [allocationEvent .systemA, allocationEvent .systemA,
    allocationEvent .systemA]

def diversifiedAllocationEvents : List AllocationEvent :=
  [allocationEvent .systemA, allocationEvent .systemB,
    allocationEvent .systemB]

def concentratedAllocationFinal : AllocationState :=
  { allocationInitialState with
    unallocatedUnits := 0
    systemAUnits := 3
    receiptCount := 3 }

def diversifiedAllocationFinal : AllocationState :=
  { allocationInitialState with
    unallocatedUnits := 0
    systemAUnits := 1
    systemBUnits := 2
    receiptCount := 3 }

def LocalAuthorizationSummary (events : List AllocationEvent) : List Bool :=
  events.map (fun event => event.pairwiseAuthorized)

def AllocationOutcome (events : List AllocationEvent) : Bool :=
  match AllocationRun allocationInitialState events with
  | none => false
  | some final => decide (
      final.systemAUnits ≤ final.concentrationLimit ∧
        final.systemBUnits ≤ final.concentrationLimit)

theorem concentrated_local_steps_reach_exact_resource_concentration :
    AllocationRun allocationInitialState concentratedAllocationEvents =
      some concentratedAllocationFinal := by
  native_decide

theorem diversified_local_steps_reach_exact_bounded_allocation :
    AllocationRun allocationInitialState diversifiedAllocationEvents =
      some diversifiedAllocationFinal := by
  native_decide

theorem local_authorization_summaries_collide_across_systemic_outcomes :
    LocalAuthorizationSummary concentratedAllocationEvents =
        LocalAuthorizationSummary diversifiedAllocationEvents ∧
      concentratedAllocationEvents ≠ diversifiedAllocationEvents := by
  decide

theorem exact_allocation_state_separates_local_authorization_collision :
    AllocationOutcome concentratedAllocationEvents = false ∧
      AllocationOutcome diversifiedAllocationEvents = true := by
  native_decide

theorem no_exact_systemic_allocation_classifier_from_local_authorization_only :
    ¬ ∃ classify : List Bool → Bool,
      ∀ events : List AllocationEvent,
        classify (LocalAuthorizationSummary events) = AllocationOutcome events := by
  intro ⟨classify, exact⟩
  have concentrated := exact concentratedAllocationEvents
  have diversified := exact diversifiedAllocationEvents
  have collision := local_authorization_summaries_collide_across_systemic_outcomes
  have separated := exact_allocation_state_separates_local_authorization_collision
  rw [separated.1] at concentrated
  rw [separated.2] at diversified
  rw [collision.1] at concentrated
  simp_all

end AsiStackProofs.MultiAgentDynamics
