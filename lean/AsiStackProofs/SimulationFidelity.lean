namespace AsiStackProofs.SimulationFidelity

structure SimulationClaimRecord where
  claimUsedAsEvidence : Bool
  scopeDeclared : Bool
  fidelityDeclared : Bool
  resourceBoundsDeclared : Bool
deriving DecidableEq, Repr

def SimulationClaimFieldsComplete (record : SimulationClaimRecord) : Prop :=
  record.scopeDeclared = true ∧
    record.fidelityDeclared = true ∧
      record.resourceBoundsDeclared = true

def SimulationClaimUseValid (record : SimulationClaimRecord) : Prop :=
  record.claimUsedAsEvidence = true -> SimulationClaimFieldsComplete record

theorem simulation_claim_used_as_evidence_includes_scope_fidelity_and_bounds
    {record : SimulationClaimRecord} :
    SimulationClaimUseValid record ->
    record.claimUsedAsEvidence = true ->
    record.scopeDeclared = true ∧
      record.fidelityDeclared = true ∧
        record.resourceBoundsDeclared = true := by
  intro valid used
  exact valid used

theorem evidence_use_without_scope_declaration_rejected
    {record : SimulationClaimRecord} :
    record.claimUsedAsEvidence = true ->
    record.scopeDeclared = false ->
    ¬ SimulationClaimUseValid record := by
  intro used missingScope valid
  have fields := valid used
  unfold SimulationClaimFieldsComplete at fields
  rw [missingScope] at fields
  cases fields.1

structure ExperimentResultRecord where
  promoted : Bool
  declaredFidelitySupportLevel : Nat
  claimedResultLevel : Nat
deriving DecidableEq, Repr

def ResultWithinDeclaredFidelity (record : ExperimentResultRecord) : Prop :=
  record.claimedResultLevel <= record.declaredFidelitySupportLevel

def ExperimentResultPromotionValid (record : ExperimentResultRecord) : Prop :=
  record.promoted = true -> ResultWithinDeclaredFidelity record

theorem promoted_experiment_result_cannot_exceed_declared_fidelity_support
    {record : ExperimentResultRecord} :
    ExperimentResultPromotionValid record ->
    record.promoted = true ->
    record.claimedResultLevel <= record.declaredFidelitySupportLevel := by
  intro valid promoted
  exact valid promoted

theorem promoted_result_above_declared_fidelity_rejected
    {record : ExperimentResultRecord} :
    record.promoted = true ->
    record.declaredFidelitySupportLevel < record.claimedResultLevel ->
    ¬ ExperimentResultPromotionValid record := by
  intro promoted exceeds valid
  have within := valid promoted
  exact Nat.not_lt_of_ge within exceeds

structure TheseusSimulationFidelityReceiptSuiteSummary where
  passedFixtureCount : Nat
  requiredScenarioCount : Nat
  simulationContractRecordCount : Nat
  fidelityRecordCount : Nat
  worldAdapterReceiptCount : Nat
  evidenceTransitionRecordCount : Nat
  failureBoundaryRecordCount : Nat
  blockedTransferCount : Nat
  downgradedClaimCount : Nat
  scenarioOnlyCount : Nat
  planningAdapterNodeCount : Nat
  planningAdapterEdgeCount : Nat
  planningAdapterPassed : Bool
  publicTrainingRowsWritten : Nat
  externalInferenceCalls : Nat
  fallbackReturnCount : Nat
  rawReportCopied : Bool
  privatePayloadCopied : Bool
  chapterCorePromotionClaimed : Bool
  physicalFeasibilityClaimed : Bool
  benchmarkTransferClaimed : Bool
  nativeKvParityClaimed : Bool
  deploymentClaimed : Bool
  liveSimulatorClaimed : Bool
  learnedGenerationClaimed : Bool
  modelQualityClaimed : Bool
  economicOutcomeClaimed : Bool
  cleanLiveTheseusReplayClaimed : Bool
deriving DecidableEq, Repr

structure TheseusSimulationFidelityReceiptSuiteValid
    (summary : TheseusSimulationFidelityReceiptSuiteSummary) : Prop where
  countInvariant :
    summary.passedFixtureCount = 5 ∧
      summary.requiredScenarioCount = 5 ∧
        summary.simulationContractRecordCount = 6 ∧
          summary.fidelityRecordCount = 6 ∧
            summary.worldAdapterReceiptCount = 6 ∧
              summary.evidenceTransitionRecordCount = 6 ∧
                summary.failureBoundaryRecordCount = 6 ∧
                  summary.blockedTransferCount = 1 ∧
                    summary.downgradedClaimCount = 1 ∧
                      summary.scenarioOnlyCount = 1 ∧
                        summary.planningAdapterNodeCount = 4 ∧
                          summary.planningAdapterEdgeCount = 3 ∧
                            summary.planningAdapterPassed = true
  publicSafety :
    summary.publicTrainingRowsWritten = 0 ∧
      summary.externalInferenceCalls = 0 ∧
        summary.fallbackReturnCount = 0 ∧
          summary.rawReportCopied = false ∧
            summary.privatePayloadCopied = false
  noCorePromotion : summary.chapterCorePromotionClaimed = false
  noPhysicalFeasibilityClaim : summary.physicalFeasibilityClaimed = false
  noBenchmarkTransferClaim : summary.benchmarkTransferClaimed = false
  noNativeKvParityClaim : summary.nativeKvParityClaimed = false
  noDeploymentClaim : summary.deploymentClaimed = false
  noLiveSimulatorClaim : summary.liveSimulatorClaimed = false
  noLearnedGenerationClaim : summary.learnedGenerationClaimed = false
  noModelQualityClaim : summary.modelQualityClaimed = false
  noEconomicOutcomeClaim : summary.economicOutcomeClaimed = false
  noCleanLiveTheseusReplayClaim : summary.cleanLiveTheseusReplayClaimed = false

def theseusSimulationFidelityReceiptSuiteImportFixture :
    TheseusSimulationFidelityReceiptSuiteSummary :=
  {
    passedFixtureCount := 5,
    requiredScenarioCount := 5,
    simulationContractRecordCount := 6,
    fidelityRecordCount := 6,
    worldAdapterReceiptCount := 6,
    evidenceTransitionRecordCount := 6,
    failureBoundaryRecordCount := 6,
    blockedTransferCount := 1,
    downgradedClaimCount := 1,
    scenarioOnlyCount := 1,
    planningAdapterNodeCount := 4,
    planningAdapterEdgeCount := 3,
    planningAdapterPassed := true,
    publicTrainingRowsWritten := 0,
    externalInferenceCalls := 0,
    fallbackReturnCount := 0,
    rawReportCopied := false,
    privatePayloadCopied := false,
    chapterCorePromotionClaimed := false,
    physicalFeasibilityClaimed := false,
    benchmarkTransferClaimed := false,
    nativeKvParityClaimed := false,
    deploymentClaimed := false,
    liveSimulatorClaimed := false,
    learnedGenerationClaimed := false,
    modelQualityClaimed := false,
    economicOutcomeClaimed := false,
    cleanLiveTheseusReplayClaimed := false
  }

theorem theseus_simulation_fidelity_receipt_suite_import_fixture_valid :
    TheseusSimulationFidelityReceiptSuiteValid
      theseusSimulationFidelityReceiptSuiteImportFixture := by
  exact {
    countInvariant := by decide,
    publicSafety := by decide,
    noCorePromotion := by decide,
    noPhysicalFeasibilityClaim := by decide,
    noBenchmarkTransferClaim := by decide,
    noNativeKvParityClaim := by decide,
    noDeploymentClaim := by decide,
    noLiveSimulatorClaim := by decide,
    noLearnedGenerationClaim := by decide,
    noModelQualityClaim := by decide,
    noEconomicOutcomeClaim := by decide,
    noCleanLiveTheseusReplayClaim := by decide
  }

theorem theseus_simulation_fidelity_receipt_suite_import_core_promotion_rejected
    {summary : TheseusSimulationFidelityReceiptSuiteSummary} :
    summary.chapterCorePromotionClaimed = true ->
    ¬ TheseusSimulationFidelityReceiptSuiteValid summary := by
  intro claimed valid
  have notClaimed := valid.noCorePromotion
  rw [claimed] at notClaimed
  cases notClaimed

theorem theseus_simulation_fidelity_receipt_suite_import_physical_feasibility_overclaim_rejected
    {summary : TheseusSimulationFidelityReceiptSuiteSummary} :
    summary.physicalFeasibilityClaimed = true ->
    ¬ TheseusSimulationFidelityReceiptSuiteValid summary := by
  intro claimed valid
  have notClaimed := valid.noPhysicalFeasibilityClaim
  rw [claimed] at notClaimed
  cases notClaimed

theorem theseus_simulation_fidelity_receipt_suite_import_benchmark_transfer_overclaim_rejected
    {summary : TheseusSimulationFidelityReceiptSuiteSummary} :
    summary.benchmarkTransferClaimed = true ->
    ¬ TheseusSimulationFidelityReceiptSuiteValid summary := by
  intro claimed valid
  have notClaimed := valid.noBenchmarkTransferClaim
  rw [claimed] at notClaimed
  cases notClaimed

theorem theseus_simulation_fidelity_receipt_suite_import_native_kv_parity_overclaim_rejected
    {summary : TheseusSimulationFidelityReceiptSuiteSummary} :
    summary.nativeKvParityClaimed = true ->
    ¬ TheseusSimulationFidelityReceiptSuiteValid summary := by
  intro claimed valid
  have notClaimed := valid.noNativeKvParityClaim
  rw [claimed] at notClaimed
  cases notClaimed

end AsiStackProofs.SimulationFidelity
