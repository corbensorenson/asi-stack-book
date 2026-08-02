import AsiStackProofs.ResourceEconomics

namespace AsiStackProofs.PhysicalComputeInfrastructureReview

/-!
A bounded review model for physical compute infrastructure. The model proves
finite workload accounting, capacity admission, impact attribution, scoped
receipts, and non-substitution properties over authored records. It does not
establish delivered performance, sustainability, resilience, community
acceptability, or deployment readiness.
-/

inductive EvidenceKind where
  | deviceCounter | facilityPue | annualRenewableContract | workloadEnergyEstimate
  | outageDrill
deriving DecidableEq, Repr

inductive ClaimClass where
  | boundedDeviceActivity | facilityOverheadRatio | contractualEnergyMatch
  | boundedWorkloadEstimate | drillExecution | deliveredUsefulCompute
  | temporalGridImpact | sustainability | resilience | communityAcceptability
deriving DecidableEq, Repr

def establishes : EvidenceKind -> ClaimClass -> Bool
  | .deviceCounter, .boundedDeviceActivity => true
  | .facilityPue, .facilityOverheadRatio => true
  | .annualRenewableContract, .contractualEnergyMatch => true
  | .workloadEnergyEstimate, .boundedWorkloadEstimate => true
  | .outageDrill, .drillExecution => true
  | _, _ => false

theorem device_counter_does_not_establish_delivered_useful_compute :
    establishes .deviceCounter .deliveredUsefulCompute = false := by rfl
theorem facility_pue_does_not_establish_sustainability :
    establishes .facilityPue .sustainability = false := by rfl
theorem renewable_contract_does_not_establish_temporal_grid_impact :
    establishes .annualRenewableContract .temporalGridImpact = false := by rfl
theorem workload_energy_estimate_does_not_establish_community_acceptability :
    establishes .workloadEnergyEstimate .communityAcceptability = false := by rfl
theorem outage_drill_does_not_establish_resilience :
    establishes .outageDrill .resilience = false := by rfl

structure DemandVector where
  compute : Nat
  memory : Nat
  network : Nat
  storage : Nat
  power : Nat
  cooling : Nat
deriving DecidableEq, Repr

def DemandVector.add (left right : DemandVector) : DemandVector :=
  { compute := left.compute + right.compute
    memory := left.memory + right.memory
    network := left.network + right.network
    storage := left.storage + right.storage
    power := left.power + right.power
    cooling := left.cooling + right.cooling }

structure WorkloadRequirement where
  workloadId : Nat
  demand : DemandVector
deriving DecidableEq, Repr

def aggregateDemand : List WorkloadRequirement -> DemandVector
  | [] => ⟨0, 0, 0, 0, 0, 0⟩
  | workload :: tail => workload.demand.add (aggregateDemand tail)

theorem aggregate_demand_append_composes
    (before after : List WorkloadRequirement) :
    aggregateDemand (before ++ after) =
      (aggregateDemand before).add (aggregateDemand after) := by
  induction before with
  | nil => simp [aggregateDemand, DemandVector.add]
  | cons head tail ih =>
      simp [aggregateDemand, DemandVector.add, ih, Nat.add_assoc]

theorem every_member_compute_demand_is_bounded_by_aggregate
    (workloads : List WorkloadRequirement) (workload : WorkloadRequirement)
    (member : workload ∈ workloads) :
    workload.demand.compute <= (aggregateDemand workloads).compute := by
  induction workloads with
  | nil => simp at member
  | cons head tail ih =>
      simp only [List.mem_cons] at member
      simp only [aggregateDemand, DemandVector.add]
      rcases member with same | rest
      · subst workload; omega
      · have bounded := ih rest; omega

structure CapacityEnvelope where
  compute : Nat
  memory : Nat
  network : Nat
  storage : Nat
  power : Nat
  cooling : Nat
deriving DecidableEq, Repr

def DemandWithinCapacity (d : DemandVector) (c : CapacityEnvelope) : Prop :=
  d.compute <= c.compute ∧ d.memory <= c.memory ∧ d.network <= c.network ∧
  d.storage <= c.storage ∧ d.power <= c.power ∧ d.cooling <= c.cooling

def FleetFits (workloads : List WorkloadRequirement) (capacity : CapacityEnvelope) : Prop :=
  DemandWithinCapacity (aggregateDemand workloads) capacity

theorem aggregate_compute_overrun_rejects_fleet_fit
    (workloads : List WorkloadRequirement) (capacity : CapacityEnvelope)
    (overrun : capacity.compute < (aggregateDemand workloads).compute) :
    Not (FleetFits workloads capacity) := by
  intro fits
  exact (Nat.not_lt_of_ge fits.1) overrun

structure ImpactEntry where
  workloadId : Nat
  operationalEnergy : Nat
  facilityOverhead : Nat
  backupEnergy : Nat
  coolingEnergy : Nat
  reportedTotal : Nat
deriving DecidableEq, Repr

def attributedEnergy (entry : ImpactEntry) : Nat :=
  entry.operationalEnergy + entry.facilityOverhead + entry.backupEnergy + entry.coolingEnergy

def impactEntryAccounted (entry : ImpactEntry) : Prop :=
  entry.reportedTotal = attributedEnergy entry

def totalAttributedEnergy : List ImpactEntry -> Nat
  | [] => 0
  | entry :: tail => attributedEnergy entry + totalAttributedEnergy tail

theorem attributed_energy_append_composes (before after : List ImpactEntry) :
    totalAttributedEnergy (before ++ after) =
      totalAttributedEnergy before + totalAttributedEnergy after := by
  induction before with
  | nil => simp [totalAttributedEnergy]
  | cons head tail ih => simp [totalAttributedEnergy, ih, Nat.add_assoc]

theorem hidden_backup_energy_breaks_exact_accounting
    (entry : ImpactEntry) (present : 0 < entry.backupEnergy) :
    Not (impactEntryAccounted
      { entry with reportedTotal :=
          entry.operationalEnergy + entry.facilityOverhead + entry.coolingEnergy }) := by
  intro accounted
  simp [impactEntryAccounted, attributedEnergy] at accounted
  omega

structure InfrastructureDossier where
  workloadIdentityBound : Bool := true
  siteIdentityBound : Bool := true
  intervalBound : Bool := true
  hardwareConfigBound : Bool := true
  topologyBound : Bool := true
  workloadVersionBound : Bool := true
  meterVersionBound : Bool := true
  requestedComputeSeparated : Bool := true
  nameplateComputeSeparated : Bool := true
  availableComputeSeparated : Bool := true
  deliveredComputeSeparated : Bool := true
  usefulWorkSeparated : Bool := true
  computeCapacityBound : Bool := true
  memoryCapacityBound : Bool := true
  networkCapacityBound : Bool := true
  storageCapacityBound : Bool := true
  powerCapacityBound : Bool := true
  thermalCapacityBound : Bool := true
  operationalEnergyBound : Bool := true
  facilityOverheadBound : Bool := true
  temporalGridBound : Bool := true
  backupEnergyBound : Bool := true
  coolingBound : Bool := true
  waterBound : Bool := true
  embodiedMaterialsBound : Bool := true
  landCommunityBound : Bool := true
  uncertaintyBound : Bool := true
  allocationMethodBound : Bool := true
  interruptionBudgetBound : Bool := true
  degradationPlanBound : Bool := true
  failoverPlanBound : Bool := true
  concentrationBound : Bool := true
  maintenanceBound : Bool := true
  demandResponseBound : Bool := true
  retirementBound : Bool := true
  dataDestructionBound : Bool := true
  reboundObservationBound : Bool := true
  residualOwnerBound : Bool := true
  currentTick : Nat := 10
  expiresAt : Nat := 20
  availabilityClaimed : Bool := false
  sustainabilityClaimed : Bool := false
  resilienceClaimed : Bool := false
  communityAcceptabilityClaimed : Bool := false
  supportOrReleaseRequested : Bool := false
deriving DecidableEq, Repr

def Current (d : InfrastructureDossier) : Prop := d.currentTick <= d.expiresAt
instance currentDecidable (d : InfrastructureDossier) : Decidable (Current d) := by
  unfold Current; infer_instance

def IdentityComplete (d : InfrastructureDossier) : Prop :=
  d.workloadIdentityBound = true ∧ d.siteIdentityBound = true ∧
  d.intervalBound = true ∧ d.hardwareConfigBound = true ∧ d.topologyBound = true ∧
  d.workloadVersionBound = true ∧ d.meterVersionBound = true

def CapacityComplete (d : InfrastructureDossier) : Prop :=
  d.requestedComputeSeparated = true ∧ d.nameplateComputeSeparated = true ∧
  d.availableComputeSeparated = true ∧ d.deliveredComputeSeparated = true ∧
  d.usefulWorkSeparated = true ∧ d.computeCapacityBound = true ∧
  d.memoryCapacityBound = true ∧ d.networkCapacityBound = true ∧
  d.storageCapacityBound = true ∧ d.powerCapacityBound = true ∧
  d.thermalCapacityBound = true

def ImpactComplete (d : InfrastructureDossier) : Prop :=
  d.operationalEnergyBound = true ∧ d.facilityOverheadBound = true ∧
  d.temporalGridBound = true ∧ d.backupEnergyBound = true ∧ d.coolingBound = true ∧
  d.waterBound = true ∧ d.embodiedMaterialsBound = true ∧
  d.landCommunityBound = true ∧ d.uncertaintyBound = true ∧
  d.allocationMethodBound = true

def ResilienceComplete (d : InfrastructureDossier) : Prop :=
  d.interruptionBudgetBound = true ∧ d.degradationPlanBound = true ∧
  d.failoverPlanBound = true ∧ d.concentrationBound = true ∧
  d.maintenanceBound = true ∧ d.demandResponseBound = true ∧
  d.retirementBound = true ∧ d.dataDestructionBound = true ∧
  d.reboundObservationBound = true ∧ d.residualOwnerBound = true ∧ Current d

def BoundaryComplete (d : InfrastructureDossier) : Prop :=
  d.availabilityClaimed = false ∧ d.sustainabilityClaimed = false ∧
  d.resilienceClaimed = false ∧ d.communityAcceptabilityClaimed = false ∧
  d.supportOrReleaseRequested = false

instance identityDecidable (d : InfrastructureDossier) : Decidable (IdentityComplete d) := by
  unfold IdentityComplete; infer_instance
instance capacityDecidable (d : InfrastructureDossier) : Decidable (CapacityComplete d) := by
  unfold CapacityComplete; infer_instance
instance impactDecidable (d : InfrastructureDossier) : Decidable (ImpactComplete d) := by
  unfold ImpactComplete; infer_instance
instance resilienceDecidable (d : InfrastructureDossier) : Decidable (ResilienceComplete d) := by
  unfold ResilienceComplete Current; infer_instance
instance boundaryDecidable (d : InfrastructureDossier) : Decidable (BoundaryComplete d) := by
  unfold BoundaryComplete; infer_instance

def DossierAdmissible (d : InfrastructureDossier) : Prop :=
  IdentityComplete d ∧ CapacityComplete d ∧ ImpactComplete d ∧
  ResilienceComplete d ∧ BoundaryComplete d
instance admissibleDecidable (d : InfrastructureDossier) : Decidable (DossierAdmissible d) := by
  unfold DossierAdmissible IdentityComplete CapacityComplete ImpactComplete
    ResilienceComplete Current BoundaryComplete
  infer_instance
def DossierReady (d : InfrastructureDossier) : Bool := decide (DossierAdmissible d)

inductive ReviewState where
  | proposed | identityReviewed | capacityReviewed | impactReviewed | resilienceReviewed
  | boundaryReviewed | repairRequired | eligibleForTheseusWorkloadCapacityCampaign
deriving DecidableEq, Repr

def ReviewStepFor (d : InfrastructureDossier) : ReviewState -> ReviewState
  | .proposed => if decide (IdentityComplete d) then .identityReviewed else .repairRequired
  | .identityReviewed => if decide (CapacityComplete d) then .capacityReviewed else .repairRequired
  | .capacityReviewed => if decide (ImpactComplete d) then .impactReviewed else .repairRequired
  | .impactReviewed => if decide (ResilienceComplete d) then .resilienceReviewed else .repairRequired
  | .resilienceReviewed => if decide (BoundaryComplete d) then .boundaryReviewed else .repairRequired
  | .boundaryReviewed => .eligibleForTheseusWorkloadCapacityCampaign
  | state => state

def ReviewRun (d : InfrastructureDossier) : Nat -> ReviewState
  | 0 => .proposed
  | n + 1 => ReviewStepFor d (ReviewRun d n)

def StageInvariant (d : InfrastructureDossier) : ReviewState -> Prop
  | .proposed => True
  | .identityReviewed => IdentityComplete d
  | .capacityReviewed => IdentityComplete d ∧ CapacityComplete d
  | .impactReviewed => IdentityComplete d ∧ CapacityComplete d ∧ ImpactComplete d
  | .resilienceReviewed =>
      IdentityComplete d ∧ CapacityComplete d ∧ ImpactComplete d ∧ ResilienceComplete d
  | .boundaryReviewed | .eligibleForTheseusWorkloadCapacityCampaign => DossierAdmissible d
  | .repairRequired => True

theorem review_step_preserves_stage_invariant
    (d : InfrastructureDossier) (state : ReviewState) (h : StageInvariant d state) :
    StageInvariant d (ReviewStepFor d state) := by
  cases state <;> simp only [ReviewStepFor]
  case proposed => split <;> simp_all [StageInvariant]
  case identityReviewed => split <;> simp_all [StageInvariant]
  case capacityReviewed => split <;> simp_all [StageInvariant]
  case impactReviewed => split <;> simp_all [StageInvariant]
  case resilienceReviewed => split <;> simp_all [StageInvariant, DossierAdmissible]
  all_goals simp_all [StageInvariant]

theorem review_run_preserves_stage_invariant (d : InfrastructureDossier) (n : Nat) :
    StageInvariant d (ReviewRun d n) := by
  induction n with
  | zero => simp [ReviewRun, StageInvariant]
  | succ n ih => simpa [ReviewRun] using review_step_preserves_stage_invariant d _ ih

theorem campaign_eligibility_requires_admissible_dossier
    (d : InfrastructureDossier) (n : Nat)
    (h : ReviewRun d n = .eligibleForTheseusWorkloadCapacityCampaign) :
    DossierAdmissible d := by
  have invariant := review_run_preserves_stage_invariant d n
  simpa [h, StageInvariant] using invariant

def completeDossier : InfrastructureDossier := {}
theorem complete_dossier_is_ready : DossierReady completeDossier = true := by decide
theorem complete_dossier_reaches_only_theseus_workload_capacity_campaign :
    ReviewRun completeDossier 6 = .eligibleForTheseusWorkloadCapacityCampaign := by decide

inductive AdmissionAxis where
  | workloadIdentity | siteIdentity | interval | hardwareConfig | topology
  | workloadVersion | meterVersion | requestedCompute | nameplateCompute | availableCompute
  | deliveredCompute | usefulWork | computeCapacity | memoryCapacity | networkCapacity
  | storageCapacity | powerCapacity | thermalCapacity | operationalEnergy
  | facilityOverhead | temporalGrid | backupEnergy | cooling | water | embodiedMaterials
  | landCommunity | uncertainty | allocationMethod | interruptionBudget | degradationPlan
  | failoverPlan | concentration | maintenance | demandResponse | retirement
  | dataDestruction | reboundObservation | residualOwner | expiry | availabilityClaim
  | sustainabilityClaim | resilienceClaim | communityAcceptabilityClaim | supportOrRelease
deriving DecidableEq, Repr

def omitAxis : AdmissionAxis -> InfrastructureDossier
  | .workloadIdentity => { completeDossier with workloadIdentityBound := false }
  | .siteIdentity => { completeDossier with siteIdentityBound := false }
  | .interval => { completeDossier with intervalBound := false }
  | .hardwareConfig => { completeDossier with hardwareConfigBound := false }
  | .topology => { completeDossier with topologyBound := false }
  | .workloadVersion => { completeDossier with workloadVersionBound := false }
  | .meterVersion => { completeDossier with meterVersionBound := false }
  | .requestedCompute => { completeDossier with requestedComputeSeparated := false }
  | .nameplateCompute => { completeDossier with nameplateComputeSeparated := false }
  | .availableCompute => { completeDossier with availableComputeSeparated := false }
  | .deliveredCompute => { completeDossier with deliveredComputeSeparated := false }
  | .usefulWork => { completeDossier with usefulWorkSeparated := false }
  | .computeCapacity => { completeDossier with computeCapacityBound := false }
  | .memoryCapacity => { completeDossier with memoryCapacityBound := false }
  | .networkCapacity => { completeDossier with networkCapacityBound := false }
  | .storageCapacity => { completeDossier with storageCapacityBound := false }
  | .powerCapacity => { completeDossier with powerCapacityBound := false }
  | .thermalCapacity => { completeDossier with thermalCapacityBound := false }
  | .operationalEnergy => { completeDossier with operationalEnergyBound := false }
  | .facilityOverhead => { completeDossier with facilityOverheadBound := false }
  | .temporalGrid => { completeDossier with temporalGridBound := false }
  | .backupEnergy => { completeDossier with backupEnergyBound := false }
  | .cooling => { completeDossier with coolingBound := false }
  | .water => { completeDossier with waterBound := false }
  | .embodiedMaterials => { completeDossier with embodiedMaterialsBound := false }
  | .landCommunity => { completeDossier with landCommunityBound := false }
  | .uncertainty => { completeDossier with uncertaintyBound := false }
  | .allocationMethod => { completeDossier with allocationMethodBound := false }
  | .interruptionBudget => { completeDossier with interruptionBudgetBound := false }
  | .degradationPlan => { completeDossier with degradationPlanBound := false }
  | .failoverPlan => { completeDossier with failoverPlanBound := false }
  | .concentration => { completeDossier with concentrationBound := false }
  | .maintenance => { completeDossier with maintenanceBound := false }
  | .demandResponse => { completeDossier with demandResponseBound := false }
  | .retirement => { completeDossier with retirementBound := false }
  | .dataDestruction => { completeDossier with dataDestructionBound := false }
  | .reboundObservation => { completeDossier with reboundObservationBound := false }
  | .residualOwner => { completeDossier with residualOwnerBound := false }
  | .expiry => { completeDossier with currentTick := 21 }
  | .availabilityClaim => { completeDossier with availabilityClaimed := true }
  | .sustainabilityClaim => { completeDossier with sustainabilityClaimed := true }
  | .resilienceClaim => { completeDossier with resilienceClaimed := true }
  | .communityAcceptabilityClaim => { completeDossier with communityAcceptabilityClaimed := true }
  | .supportOrRelease => { completeDossier with supportOrReleaseRequested := true }

inductive RepairDisposition where
  | bindWorkloadIdentity | bindSiteIdentity | bindInterval | bindHardwareConfig | bindTopology
  | bindWorkloadVersion | bindMeterVersion | separateRequestedCompute
  | separateNameplateCompute | separateAvailableCompute | separateDeliveredCompute
  | separateUsefulWork | bindComputeCapacity | bindMemoryCapacity | bindNetworkCapacity
  | bindStorageCapacity | bindPowerCapacity | bindThermalCapacity | bindOperationalEnergy
  | bindFacilityOverhead | bindTemporalGrid | bindBackupEnergy | bindCooling | bindWater
  | bindEmbodiedMaterials | bindLandCommunity | bindUncertainty | bindAllocationMethod
  | bindInterruptionBudget | addDegradationPlan | addFailoverPlan | bindConcentration
  | bindMaintenance | bindDemandResponse | bindRetirement | bindDataDestruction
  | observeRebound | assignResidualOwner | renewExpiry | rejectAvailabilityClaim
  | rejectSustainabilityClaim | rejectResilienceClaim | rejectCommunityAcceptabilityClaim
  | refuseSupportOrRelease | eligibleForTheseusWorkloadCapacityCampaign
deriving DecidableEq, Repr

def repairForAxis : AdmissionAxis -> RepairDisposition
  | .workloadIdentity => .bindWorkloadIdentity | .siteIdentity => .bindSiteIdentity
  | .interval => .bindInterval | .hardwareConfig => .bindHardwareConfig
  | .topology => .bindTopology | .workloadVersion => .bindWorkloadVersion
  | .meterVersion => .bindMeterVersion | .requestedCompute => .separateRequestedCompute
  | .nameplateCompute => .separateNameplateCompute
  | .availableCompute => .separateAvailableCompute
  | .deliveredCompute => .separateDeliveredCompute | .usefulWork => .separateUsefulWork
  | .computeCapacity => .bindComputeCapacity | .memoryCapacity => .bindMemoryCapacity
  | .networkCapacity => .bindNetworkCapacity | .storageCapacity => .bindStorageCapacity
  | .powerCapacity => .bindPowerCapacity | .thermalCapacity => .bindThermalCapacity
  | .operationalEnergy => .bindOperationalEnergy | .facilityOverhead => .bindFacilityOverhead
  | .temporalGrid => .bindTemporalGrid | .backupEnergy => .bindBackupEnergy
  | .cooling => .bindCooling | .water => .bindWater
  | .embodiedMaterials => .bindEmbodiedMaterials | .landCommunity => .bindLandCommunity
  | .uncertainty => .bindUncertainty | .allocationMethod => .bindAllocationMethod
  | .interruptionBudget => .bindInterruptionBudget | .degradationPlan => .addDegradationPlan
  | .failoverPlan => .addFailoverPlan | .concentration => .bindConcentration
  | .maintenance => .bindMaintenance | .demandResponse => .bindDemandResponse
  | .retirement => .bindRetirement | .dataDestruction => .bindDataDestruction
  | .reboundObservation => .observeRebound | .residualOwner => .assignResidualOwner
  | .expiry => .renewExpiry | .availabilityClaim => .rejectAvailabilityClaim
  | .sustainabilityClaim => .rejectSustainabilityClaim
  | .resilienceClaim => .rejectResilienceClaim
  | .communityAcceptabilityClaim => .rejectCommunityAcceptabilityClaim
  | .supportOrRelease => .refuseSupportOrRelease

def ExactRepairFor (d : InfrastructureDossier) : RepairDisposition :=
  if !d.workloadIdentityBound then .bindWorkloadIdentity
  else if !d.siteIdentityBound then .bindSiteIdentity
  else if !d.intervalBound then .bindInterval
  else if !d.hardwareConfigBound then .bindHardwareConfig
  else if !d.topologyBound then .bindTopology
  else if !d.workloadVersionBound then .bindWorkloadVersion
  else if !d.meterVersionBound then .bindMeterVersion
  else if !d.requestedComputeSeparated then .separateRequestedCompute
  else if !d.nameplateComputeSeparated then .separateNameplateCompute
  else if !d.availableComputeSeparated then .separateAvailableCompute
  else if !d.deliveredComputeSeparated then .separateDeliveredCompute
  else if !d.usefulWorkSeparated then .separateUsefulWork
  else if !d.computeCapacityBound then .bindComputeCapacity
  else if !d.memoryCapacityBound then .bindMemoryCapacity
  else if !d.networkCapacityBound then .bindNetworkCapacity
  else if !d.storageCapacityBound then .bindStorageCapacity
  else if !d.powerCapacityBound then .bindPowerCapacity
  else if !d.thermalCapacityBound then .bindThermalCapacity
  else if !d.operationalEnergyBound then .bindOperationalEnergy
  else if !d.facilityOverheadBound then .bindFacilityOverhead
  else if !d.temporalGridBound then .bindTemporalGrid
  else if !d.backupEnergyBound then .bindBackupEnergy
  else if !d.coolingBound then .bindCooling
  else if !d.waterBound then .bindWater
  else if !d.embodiedMaterialsBound then .bindEmbodiedMaterials
  else if !d.landCommunityBound then .bindLandCommunity
  else if !d.uncertaintyBound then .bindUncertainty
  else if !d.allocationMethodBound then .bindAllocationMethod
  else if !d.interruptionBudgetBound then .bindInterruptionBudget
  else if !d.degradationPlanBound then .addDegradationPlan
  else if !d.failoverPlanBound then .addFailoverPlan
  else if !d.concentrationBound then .bindConcentration
  else if !d.maintenanceBound then .bindMaintenance
  else if !d.demandResponseBound then .bindDemandResponse
  else if !d.retirementBound then .bindRetirement
  else if !d.dataDestructionBound then .bindDataDestruction
  else if !d.reboundObservationBound then .observeRebound
  else if !d.residualOwnerBound then .assignResidualOwner
  else if !decide (Current d) then .renewExpiry
  else if d.availabilityClaimed then .rejectAvailabilityClaim
  else if d.sustainabilityClaimed then .rejectSustainabilityClaim
  else if d.resilienceClaimed then .rejectResilienceClaim
  else if d.communityAcceptabilityClaimed then .rejectCommunityAcceptabilityClaim
  else if d.supportOrReleaseRequested then .refuseSupportOrRelease
  else .eligibleForTheseusWorkloadCapacityCampaign

theorem every_admission_axis_mutation_blocks_readiness (axis : AdmissionAxis) :
    DossierReady (omitAxis axis) = false := by cases axis <;> decide
theorem every_admission_axis_mutation_has_exact_repair (axis : AdmissionAxis) :
    ExactRepairFor (omitAxis axis) = repairForAxis axis := by cases axis <;> decide
theorem every_admission_axis_mutation_reaches_repair (axis : AdmissionAxis) :
    ReviewRun (omitAxis axis) 6 = .repairRequired := by cases axis <;> decide

theorem readiness_requires_identity (d : InfrastructureDossier) (h : DossierReady d = true) :
    IdentityComplete d := by exact (of_decide_eq_true h).1
theorem readiness_requires_capacity (d : InfrastructureDossier) (h : DossierReady d = true) :
    CapacityComplete d := by exact (of_decide_eq_true h).2.1
theorem readiness_requires_impact (d : InfrastructureDossier) (h : DossierReady d = true) :
    ImpactComplete d := by exact (of_decide_eq_true h).2.2.1
theorem readiness_requires_resilience (d : InfrastructureDossier) (h : DossierReady d = true) :
    ResilienceComplete d := by exact (of_decide_eq_true h).2.2.2.1
theorem readiness_requires_boundary (d : InfrastructureDossier) (h : DossierReady d = true) :
    BoundaryComplete d := by exact (of_decide_eq_true h).2.2.2.2

theorem expired_capacity_contract_remains_expired_when_time_advances
    (d : InfrastructureDossier) (later : Nat) (expired : d.expiresAt < d.currentTick)
    (advances : d.currentTick <= later) : Not (Current { d with currentTick := later }) := by
  intro current; unfold Current at current; change later <= d.expiresAt at current; omega

theorem demand_increase_past_capacity_rejects_fit
    (demand capacity increase : Nat) (_fits : demand <= capacity)
    (overrun : capacity < demand + increase) : Not (demand + increase <= capacity) := by
  omega

theorem capacity_loss_preserves_existing_overrun
    (demand oldCapacity newCapacity : Nat) (overrun : oldCapacity < demand)
    (loss : newCapacity <= oldCapacity) : Not (demand <= newCapacity) := by
  omega

structure ReceiptScope where
  workloadId : Nat
  siteId : Nat
  intervalId : Nat
  hardwareDigest : Nat
  meterVersion : Nat
deriving DecidableEq, Repr

def ReceiptUseAllowed
    (s : ReceiptScope) (workload site interval hardware meter : Nat) : Prop :=
  workload = s.workloadId ∧ site = s.siteId ∧ interval = s.intervalId ∧
  hardware = s.hardwareDigest ∧ meter = s.meterVersion

theorem workload_change_invalidates_capacity_receipt
    (s : ReceiptScope) (v : Nat) (h : Not (v = s.workloadId)) :
    Not (ReceiptUseAllowed s v s.siteId s.intervalId s.hardwareDigest s.meterVersion) := by
  intro x; exact h x.1
theorem site_change_invalidates_capacity_receipt
    (s : ReceiptScope) (v : Nat) (h : Not (v = s.siteId)) :
    Not (ReceiptUseAllowed s s.workloadId v s.intervalId s.hardwareDigest s.meterVersion) := by
  intro x; exact h x.2.1
theorem interval_change_invalidates_capacity_receipt
    (s : ReceiptScope) (v : Nat) (h : Not (v = s.intervalId)) :
    Not (ReceiptUseAllowed s s.workloadId s.siteId v s.hardwareDigest s.meterVersion) := by
  intro x; exact h x.2.2.1
theorem hardware_change_invalidates_capacity_receipt
    (s : ReceiptScope) (v : Nat) (h : Not (v = s.hardwareDigest)) :
    Not (ReceiptUseAllowed s s.workloadId s.siteId s.intervalId v s.meterVersion) := by
  intro x; exact h x.2.2.2.1
theorem meter_change_invalidates_capacity_receipt
    (s : ReceiptScope) (v : Nat) (h : Not (v = s.meterVersion)) :
    Not (ReceiptUseAllowed s s.workloadId s.siteId s.intervalId s.hardwareDigest v) := by
  intro x; exact h x.2.2.2.2

structure HeadlineSignals where
  averagePower : Nat
  annualEnergy : Nat
deriving DecidableEq, Repr
structure UsefulComputeCase where
  signals : HeadlineSignals
  usefulOutputDelivered : Bool
deriving DecidableEq, Repr
def sharedHeadlineSignals : HeadlineSignals := ⟨40, 900⟩
def usefulDeliveryCase : UsefulComputeCase := ⟨sharedHeadlineSignals, true⟩
def stalledDeliveryCase : UsefulComputeCase := ⟨sharedHeadlineSignals, false⟩
def DeliveredUsefulCompute (c : UsefulComputeCase) : Bool := c.usefulOutputDelivered

theorem identical_energy_headlines_can_hide_opposite_useful_delivery :
    usefulDeliveryCase.signals = stalledDeliveryCase.signals ∧
    DeliveredUsefulCompute usefulDeliveryCase = true ∧
    DeliveredUsefulCompute stalledDeliveryCase = false := by decide

theorem energy_headlines_cannot_recover_useful_delivery (classify : HeadlineSignals -> Bool) :
    Not (forall c : UsefulComputeCase, classify c.signals = DeliveredUsefulCompute c) := by
  intro exact
  have a := exact usefulDeliveryCase
  have b := exact stalledDeliveryCase
  simp [usefulDeliveryCase, stalledDeliveryCase, sharedHeadlineSignals, DeliveredUsefulCompute] at a b
  rw [a] at b
  contradiction

structure EfficiencySignals where
  energyPerUsefulUnit : Nat
  unitCost : Nat
deriving DecidableEq, Repr
structure ReboundCase where
  signals : EfficiencySignals
  totalImpactReduced : Bool
deriving DecidableEq, Repr
def sharedEfficiencySignals : EfficiencySignals := ⟨7, 4⟩
def boundedDemandCase : ReboundCase := ⟨sharedEfficiencySignals, true⟩
def reboundDemandCase : ReboundCase := ⟨sharedEfficiencySignals, false⟩
def TotalImpactReduced (c : ReboundCase) : Bool := c.totalImpactReduced

theorem identical_unit_efficiency_can_hide_opposite_total_impact :
    boundedDemandCase.signals = reboundDemandCase.signals ∧
    TotalImpactReduced boundedDemandCase = true ∧
    TotalImpactReduced reboundDemandCase = false := by decide

theorem unit_efficiency_cannot_recover_total_impact (classify : EfficiencySignals -> Bool) :
    Not (forall c : ReboundCase, classify c.signals = TotalImpactReduced c) := by
  intro exact
  have a := exact boundedDemandCase
  have b := exact reboundDemandCase
  simp [boundedDemandCase, reboundDemandCase, sharedEfficiencySignals, TotalImpactReduced] at a b
  rw [a] at b
  contradiction

def physicalCapacityBudgetGate (withinCapacity : Bool) : ResourceEconomics.BudgetGateReview :=
  { requiredSafetyGate := true
    requiredVerificationGate := true
    safetyGateDisabled := !withinCapacity
    verificationGateDisabled := false }

theorem physical_capacity_failure_rejects_resource_budget_gate
    (withinCapacity : Bool) (failed : withinCapacity = false) :
    Not (ResourceEconomics.RequiredGatesPreserved
      (physicalCapacityBudgetGate withinCapacity)) := by
  apply ResourceEconomics.required_safety_gate_disabled_rejects_budget_gate_preservation
  · rfl
  · simp [physicalCapacityBudgetGate, failed]

end AsiStackProofs.PhysicalComputeInfrastructureReview
