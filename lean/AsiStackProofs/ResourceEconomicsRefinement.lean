namespace AsiStackProofs.ResourceEconomicsRefinement

inductive Stage where
  | requested | budgeted | reserved | scheduled | executed | verified | transferred | reconciled | closed
deriving DecidableEq, Repr

inductive EventKind where
  | bindRequest | declareBudget | reserveCapacity | scheduleWork | recordExecution
  | verifyOutcome | transportClaim | reconcileSpend | close
deriving DecidableEq, Repr

inductive Route where
  | rejectWrongStage | rejectRequestSubstitution | rejectPolicySubstitution
  | rejectResourceSubstitution | rejectEvidenceSubstitution | rejectEventReplay | rejectAuthorityLeak
  | requestConsumer | requestTask | requestRisk | requestRights | requestHorizon | requestNonClaims | acceptBudgeting
  | requestResourceInventory | requestUnits | requestDirectCost | requestDisplacedCost
  | requestVerificationCost | requestUncertainty | requestProtectedFloors | acceptReservation
  | requestCapacity | requestReviewerCapacity | requestVerifierCapacity | requestProtectedOverhead
  | requestDebtExpiry | requestCapacityOwner | acceptSchedule
  | requestQueuePolicy | requestHighRiskPriority | requestTailPolicy | requestTenantIsolation
  | requestFallback | acceptExecution
  | requestActualSpend | requestFailureRetention | requestUnsafeReleaseAccounting
  | requestUsefulOutcome | requestResourceBill | blockRawProxyPromotion | acceptVerification
  | requestVerifierOutcome | requestEvaluatorBoundary | requestFalseDecisionAccounting
  | requestResiduals | requestRecovery | acceptTransfer
  | requestSimulationScope | requestSimulationFidelity | requestTemporalSemantics
  | requestSimulationResourceBill | requestSimulationOmissions | requestTransferDecision
  | blockFidelityOverclaim | acceptReconciliation
  | requestVariance | requestOpportunityCost | requestIncidents | requestDescendants
  | requestEvidenceTransition | acceptClosure
  | requestAcknowledgment | requestResultDigest | requestCleanup | acceptClosed
deriving DecidableEq, Repr

structure State where
  stage : Stage
  requestDigest : Nat
  consumerDigest : Nat
  taskDigest : Nat
  policyDigest : Nat
  rightsDigest : Nat
  resourceDigest : Nat
  evaluatorDigest : Nat
  simulationDigest : Nat
  resultDigest : Nat
  lastEventDigest : Nat
deriving DecidableEq, Repr

structure Packet where
  requestDigest : Nat := 6001
  consumerDigest : Nat := 6002
  taskDigest : Nat := 6003
  policyDigest : Nat := 6004
  rightsDigest : Nat := 6005
  resourceDigest : Nat := 6006
  evaluatorDigest : Nat := 6007
  simulationDigest : Nat := 6008
  resultDigest : Nat := 6009
  eventDigest : Nat := 111
  consumer : Bool := true
  task : Bool := true
  risk : Bool := true
  rights : Bool := true
  horizon : Bool := true
  nonClaims : Bool := true
  resourceInventory : Bool := true
  units : Bool := true
  directCost : Bool := true
  displacedCost : Bool := true
  verificationCost : Bool := true
  uncertainty : Bool := true
  protectedFloors : Bool := true
  capacity : Bool := true
  reviewerCapacity : Bool := true
  verifierCapacity : Bool := true
  protectedOverhead : Bool := true
  debtExpiry : Bool := true
  capacityOwner : Bool := true
  queuePolicy : Bool := true
  highRiskPriority : Bool := true
  tailPolicy : Bool := true
  tenantIsolation : Bool := true
  fallback : Bool := true
  actualSpend : Bool := true
  failureRetention : Bool := true
  unsafeReleaseAccounting : Bool := true
  usefulOutcome : Bool := true
  resourceBill : Bool := true
  rawProxyPromotion : Bool := false
  verifierOutcome : Bool := true
  evaluatorBoundary : Bool := true
  falseDecisionAccounting : Bool := true
  residuals : Bool := true
  recovery : Bool := true
  simulated : Bool := false
  simulationScope : Bool := true
  simulationFidelity : Bool := true
  temporalSemantics : Bool := true
  simulationResourceBill : Bool := true
  simulationOmissions : Bool := true
  transferDecision : Bool := true
  claimedSupportLevel : Nat := 1
  fidelitySupportLevel : Nat := 1
  variance : Bool := true
  opportunityCost : Bool := true
  incidents : Bool := true
  descendants : Bool := true
  evidenceTransition : Bool := true
  acknowledgment : Bool := true
  resultDigestBound : Bool := true
  cleanup : Bool := true
  supportPromotionRequested : Bool := false
  externalEffectRequested : Bool := false
deriving DecidableEq, Repr

def expectedKind : Stage → EventKind
  | .requested => .bindRequest | .budgeted => .declareBudget | .reserved => .reserveCapacity
  | .scheduled => .scheduleWork | .executed => .recordExecution | .verified => .verifyOutcome
  | .transferred => .transportClaim | .reconciled => .reconcileSpend | .closed => .close

def route (s : State) (kind : EventKind) (p : Packet) : Route :=
  if kind != expectedKind s.stage then .rejectWrongStage
  else if p.requestDigest != s.requestDigest || p.consumerDigest != s.consumerDigest || p.taskDigest != s.taskDigest then .rejectRequestSubstitution
  else if p.policyDigest != s.policyDigest || p.rightsDigest != s.rightsDigest then .rejectPolicySubstitution
  else if p.resourceDigest != s.resourceDigest then .rejectResourceSubstitution
  else if p.evaluatorDigest != s.evaluatorDigest || p.simulationDigest != s.simulationDigest || p.resultDigest != s.resultDigest then .rejectEvidenceSubstitution
  else if p.eventDigest = s.lastEventDigest then .rejectEventReplay
  else if p.supportPromotionRequested || p.externalEffectRequested then .rejectAuthorityLeak
  else match s.stage with
  | .requested =>
      if !p.consumer then .requestConsumer else if !p.task then .requestTask else if !p.risk then .requestRisk
      else if !p.rights then .requestRights else if !p.horizon then .requestHorizon else if !p.nonClaims then .requestNonClaims else .acceptBudgeting
  | .budgeted =>
      if !p.resourceInventory then .requestResourceInventory else if !p.units then .requestUnits
      else if !p.directCost then .requestDirectCost else if !p.displacedCost then .requestDisplacedCost
      else if !p.verificationCost then .requestVerificationCost else if !p.uncertainty then .requestUncertainty
      else if !p.protectedFloors then .requestProtectedFloors else .acceptReservation
  | .reserved =>
      if !p.capacity then .requestCapacity else if !p.reviewerCapacity then .requestReviewerCapacity
      else if !p.verifierCapacity then .requestVerifierCapacity else if !p.protectedOverhead then .requestProtectedOverhead
      else if !p.debtExpiry then .requestDebtExpiry else if !p.capacityOwner then .requestCapacityOwner else .acceptSchedule
  | .scheduled =>
      if !p.queuePolicy then .requestQueuePolicy else if !p.highRiskPriority then .requestHighRiskPriority
      else if !p.tailPolicy then .requestTailPolicy else if !p.tenantIsolation then .requestTenantIsolation
      else if !p.fallback then .requestFallback else .acceptExecution
  | .executed =>
      if !p.actualSpend then .requestActualSpend else if !p.failureRetention then .requestFailureRetention
      else if !p.unsafeReleaseAccounting then .requestUnsafeReleaseAccounting else if !p.usefulOutcome then .requestUsefulOutcome
      else if !p.resourceBill then .requestResourceBill else if p.rawProxyPromotion then .blockRawProxyPromotion else .acceptVerification
  | .verified =>
      if !p.verifierOutcome then .requestVerifierOutcome else if !p.evaluatorBoundary then .requestEvaluatorBoundary
      else if !p.falseDecisionAccounting then .requestFalseDecisionAccounting else if !p.residuals then .requestResiduals
      else if !p.recovery then .requestRecovery else .acceptTransfer
  | .transferred =>
      if p.simulated && !p.simulationScope then .requestSimulationScope
      else if p.simulated && !p.simulationFidelity then .requestSimulationFidelity
      else if p.simulated && !p.temporalSemantics then .requestTemporalSemantics
      else if p.simulated && !p.simulationResourceBill then .requestSimulationResourceBill
      else if p.simulated && !p.simulationOmissions then .requestSimulationOmissions
      else if p.simulated && !p.transferDecision then .requestTransferDecision
      else if p.simulated && p.fidelitySupportLevel < p.claimedSupportLevel then .blockFidelityOverclaim
      else .acceptReconciliation
  | .reconciled =>
      if !p.variance then .requestVariance else if !p.opportunityCost then .requestOpportunityCost
      else if !p.incidents then .requestIncidents else if !p.descendants then .requestDescendants
      else if !p.evidenceTransition then .requestEvidenceTransition else .acceptClosure
  | .closed =>
      if !p.acknowledgment then .requestAcknowledgment else if !p.resultDigestBound then .requestResultDigest
      else if !p.cleanup then .requestCleanup else .acceptClosed

def completeState (selectedStage : Stage) : State where
  stage := selectedStage
  requestDigest := 6001
  consumerDigest := 6002
  taskDigest := 6003
  policyDigest := 6004
  rightsDigest := 6005
  resourceDigest := 6006
  evaluatorDigest := 6007
  simulationDigest := 6008
  resultDigest := 6009
  lastEventDigest := 0

def completePacket : Packet := {}

theorem missing_protected_floor_blocks_reservation :
    route (completeState .budgeted) .declareBudget
      { completePacket with protectedFloors := false } = .requestProtectedFloors := by native_decide

theorem missing_reviewer_capacity_blocks_schedule :
    route (completeState .reserved) .reserveCapacity
      { completePacket with reviewerCapacity := false } = .requestReviewerCapacity := by native_decide

theorem raw_proxy_cannot_promote_executed_work :
    route (completeState .executed) .recordExecution
      { completePacket with rawProxyPromotion := true } = .blockRawProxyPromotion := by native_decide

theorem simulated_claim_without_fidelity_blocks_transfer :
    route (completeState .transferred) .transportClaim
      { completePacket with simulated := true, simulationFidelity := false } = .requestSimulationFidelity := by native_decide

theorem simulated_claim_above_fidelity_blocks_transfer :
    route (completeState .transferred) .transportClaim
      { completePacket with simulated := true, fidelitySupportLevel := 1, claimedSupportLevel := 2 } = .blockFidelityOverclaim := by native_decide

theorem missing_failure_retention_blocks_verification :
    route (completeState .executed) .recordExecution
      { completePacket with failureRetention := false } = .requestFailureRetention := by native_decide

theorem complete_resource_lifecycle_reaches_closed_without_support_or_effect_authority :
    route (completeState .requested) .bindRequest completePacket = .acceptBudgeting ∧
    route (completeState .budgeted) .declareBudget completePacket = .acceptReservation ∧
    route (completeState .reserved) .reserveCapacity completePacket = .acceptSchedule ∧
    route (completeState .scheduled) .scheduleWork completePacket = .acceptExecution ∧
    route (completeState .executed) .recordExecution completePacket = .acceptVerification ∧
    route (completeState .verified) .verifyOutcome completePacket = .acceptTransfer ∧
    route (completeState .transferred) .transportClaim completePacket = .acceptReconciliation ∧
    route (completeState .reconciled) .reconcileSpend completePacket = .acceptClosure ∧
    route (completeState .closed) .close completePacket = .acceptClosed ∧
    completePacket.supportPromotionRequested = false ∧ completePacket.externalEffectRequested = false := by native_decide

theorem complete_simulation_transport_reaches_reconciliation_without_promotion :
    route (completeState .transferred) .transportClaim
      { completePacket with simulated := true } = .acceptReconciliation ∧
    completePacket.supportPromotionRequested = false := by native_decide

end AsiStackProofs.ResourceEconomicsRefinement
