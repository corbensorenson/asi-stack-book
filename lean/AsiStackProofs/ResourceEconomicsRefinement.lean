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
  receiptCount : Nat := 0
  resourceBillReceiptCount : Nat := 0
  reconciliationReceiptCount : Nat := 0
  supportAssigned : Bool := false
  externalEffectCommitted : Bool := false
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

def accepted : Route → Bool
  | .acceptBudgeting | .acceptReservation | .acceptSchedule | .acceptExecution
  | .acceptVerification | .acceptTransfer | .acceptReconciliation | .acceptClosure
  | .acceptClosed => true
  | _ => false

theorem authority_request_never_accepts
    (s : State) (kind : EventKind) (p : Packet)
    (h : p.supportPromotionRequested || p.externalEffectRequested = true) :
    accepted (route s kind p) = false := by
  by_cases h₁ : kind != expectedKind s.stage
  · simp [route, h₁, accepted]
  by_cases h₂ : p.requestDigest != s.requestDigest || p.consumerDigest != s.consumerDigest || p.taskDigest != s.taskDigest
  · simp [route, h₁, h₂, accepted]
  by_cases h₃ : p.policyDigest != s.policyDigest || p.rightsDigest != s.rightsDigest
  · simp [route, h₁, h₂, h₃, accepted]
  by_cases h₄ : p.resourceDigest != s.resourceDigest
  · simp [route, h₁, h₂, h₃, h₄, accepted]
  by_cases h₅ : p.evaluatorDigest != s.evaluatorDigest || p.simulationDigest != s.simulationDigest || p.resultDigest != s.resultDigest
  · simp [route, h₁, h₂, h₃, h₄, h₅, accepted]
  by_cases h₆ : p.eventDigest = s.lastEventDigest
  · simp [route, h₁, h₂, h₃, h₄, h₅, h₆, accepted]
  cases hs : p.supportPromotionRequested <;>
    cases he : p.externalEffectRequested <;>
    simp_all [route, accepted]

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

structure ResourceIdentity where
  requestDigest : Nat
  consumerDigest : Nat
  taskDigest : Nat
  policyDigest : Nat
  rightsDigest : Nat
  resourceDigest : Nat
  evaluatorDigest : Nat
  simulationDigest : Nat
  resultDigest : Nat
deriving DecidableEq, Repr

def resourceIdentity (state : State) : ResourceIdentity :=
  { requestDigest := state.requestDigest
    consumerDigest := state.consumerDigest
    taskDigest := state.taskDigest
    policyDigest := state.policyDigest
    rightsDigest := state.rightsDigest
    resourceDigest := state.resourceDigest
    evaluatorDigest := state.evaluatorDigest
    simulationDigest := state.simulationDigest
    resultDigest := state.resultDigest }

def advanceStage : Stage -> Stage
  | .requested => .budgeted
  | .budgeted => .reserved
  | .reserved => .scheduled
  | .scheduled => .executed
  | .executed => .verified
  | .verified => .transferred
  | .transferred => .reconciled
  | .reconciled => .closed
  | .closed => .closed

def applyEvent (state : State) (kind : EventKind) (packet : Packet) :
    State × Route :=
  let selectedRoute := route state kind packet
  if accepted selectedRoute then
    ({state with
      stage := advanceStage state.stage
      lastEventDigest := packet.eventDigest
      receiptCount := state.receiptCount + 1
      resourceBillReceiptCount := if selectedRoute == .acceptVerification then
        state.resourceBillReceiptCount + 1 else state.resourceBillReceiptCount
      reconciliationReceiptCount := if selectedRoute == .acceptClosure then
        state.reconciliationReceiptCount + 1 else state.reconciliationReceiptCount},
      selectedRoute)
  else (state, selectedRoute)

structure ResourceEvent where
  kind : EventKind
  packet : Packet
deriving DecidableEq, Repr

def ResourceStep (state : State) (event : ResourceEvent) : Option State :=
  if state.stage = .closed then none
  else if accepted (route state event.kind event.packet) then
    some (applyEvent state event.kind event.packet).1
  else none

def ResourceRun : State -> List ResourceEvent -> Option State
  | state, [] => some state
  | state, event :: tail =>
      match ResourceStep state event with
      | none => none
      | some next => ResourceRun next tail

def ResourceTraceAccepted : State -> List ResourceEvent -> Prop
  | _, [] => True
  | state, event :: tail =>
      accepted (route state event.kind event.packet) = true ∧
      ResourceTraceAccepted (applyEvent state event.kind event.packet).1 tail

theorem accepted_step_is_accepted
    {state next : State} {event : ResourceEvent}
    (stepped : ResourceStep state event = some next) :
    accepted (route state event.kind event.packet) = true := by
  unfold ResourceStep at stepped
  split at stepped
  · simp at stepped
  · split at stepped
    · assumption
    · simp at stepped

theorem accepted_step_applies_event
    {state next : State} {event : ResourceEvent}
    (stepped : ResourceStep state event = some next) :
    next = (applyEvent state event.kind event.packet).1 := by
  unfold ResourceStep at stepped
  split at stepped
  · simp at stepped
  · split at stepped
    · exact Option.some.inj stepped |>.symm
    · simp at stepped

theorem apply_event_preserves_full_identity (state : State)
    (event : ResourceEvent) :
    resourceIdentity (applyEvent state event.kind event.packet).1 =
      resourceIdentity state := by
  by_cases acceptedRoute : accepted (route state event.kind event.packet) = true <;>
    simp [applyEvent, acceptedRoute, resourceIdentity]

theorem rejected_apply_event_preserves_state (state : State)
    (event : ResourceEvent)
    (rejected : accepted (route state event.kind event.packet) = false) :
    (applyEvent state event.kind event.packet).1 = state := by
  simp [applyEvent, rejected]

theorem accepted_step_preserves_full_identity
    {state next : State} {event : ResourceEvent}
    (stepped : ResourceStep state event = some next) :
    resourceIdentity next = resourceIdentity state := by
  rw [accepted_step_applies_event stepped]
  exact apply_event_preserves_full_identity state event

theorem accepted_step_preserves_non_authority
    {state next : State} {event : ResourceEvent}
    (stepped : ResourceStep state event = some next) :
    next.supportAssigned = state.supportAssigned ∧
    next.externalEffectCommitted = state.externalEffectCommitted := by
  rw [accepted_step_applies_event stepped]
  simp [applyEvent, accepted_step_is_accepted stepped]

theorem accepted_step_adds_exactly_one_receipt
    {state next : State} {event : ResourceEvent}
    (stepped : ResourceStep state event = some next) :
    next.receiptCount = state.receiptCount + 1 := by
  rw [accepted_step_applies_event stepped]
  simp [applyEvent, accepted_step_is_accepted stepped]

theorem accepted_step_advances_stage
    {state next : State} {event : ResourceEvent}
    (stepped : ResourceStep state event = some next) :
    next.stage = advanceStage state.stage := by
  rw [accepted_step_applies_event stepped]
  simp [applyEvent, accepted_step_is_accepted stepped]

theorem apply_event_resource_bill_count_monotone (state : State)
    (event : ResourceEvent) :
    state.resourceBillReceiptCount <=
      (applyEvent state event.kind event.packet).1.resourceBillReceiptCount := by
  cases routed : route state event.kind event.packet <;>
    simp [applyEvent, routed, accepted]

theorem apply_event_reconciliation_count_monotone (state : State)
    (event : ResourceEvent) :
    state.reconciliationReceiptCount <=
      (applyEvent state event.kind event.packet).1.reconciliationReceiptCount := by
  cases routed : route state event.kind event.packet <;>
    simp [applyEvent, routed, accepted]

theorem accepted_run_preserves_full_identity
    {state final : State} {events : List ResourceEvent}
    (ran : ResourceRun state events = some final) :
    resourceIdentity final = resourceIdentity state := by
  induction events generalizing state with
  | nil => simp [ResourceRun] at ran; subst final; rfl
  | cons event tail ih =>
      cases stepped : ResourceStep state event with
      | none => simp [ResourceRun, stepped] at ran
      | some next =>
          have tailRan : ResourceRun next tail = some final := by
            simpa [ResourceRun, stepped] using ran
          exact (ih tailRan).trans (accepted_step_preserves_full_identity stepped)

theorem accepted_run_preserves_support
    {state final : State} {events : List ResourceEvent}
    (ran : ResourceRun state events = some final) :
    final.supportAssigned = state.supportAssigned := by
  induction events generalizing state with
  | nil => simp [ResourceRun] at ran; subst final; rfl
  | cons event tail ih =>
      cases stepped : ResourceStep state event with
      | none => simp [ResourceRun, stepped] at ran
      | some next =>
          have tailRan : ResourceRun next tail = some final := by
            simpa [ResourceRun, stepped] using ran
          exact (ih tailRan).trans (accepted_step_preserves_non_authority stepped).1

theorem accepted_run_preserves_external_effect
    {state final : State} {events : List ResourceEvent}
    (ran : ResourceRun state events = some final) :
    final.externalEffectCommitted = state.externalEffectCommitted := by
  induction events generalizing state with
  | nil => simp [ResourceRun] at ran; subst final; rfl
  | cons event tail ih =>
      cases stepped : ResourceStep state event with
      | none => simp [ResourceRun, stepped] at ran
      | some next =>
          have tailRan : ResourceRun next tail = some final := by
            simpa [ResourceRun, stepped] using ran
          exact (ih tailRan).trans (accepted_step_preserves_non_authority stepped).2

theorem accepted_run_accounts_exact_receipts
    {state final : State} {events : List ResourceEvent}
    (ran : ResourceRun state events = some final) :
    final.receiptCount = state.receiptCount + events.length := by
  induction events generalizing state with
  | nil => simp [ResourceRun] at ran; subst final; simp
  | cons event tail ih =>
      cases stepped : ResourceStep state event with
      | none => simp [ResourceRun, stepped] at ran
      | some next =>
          have tailRan : ResourceRun next tail = some final := by
            simpa [ResourceRun, stepped] using ran
          calc
            final.receiptCount = next.receiptCount + tail.length := ih tailRan
            _ = (state.receiptCount + 1) + tail.length := by
              rw [accepted_step_adds_exactly_one_receipt stepped]
            _ = state.receiptCount + (event :: tail).length := by
              simp only [List.length_cons]
              omega

theorem accepted_run_resource_bill_count_monotone
    {state final : State} {events : List ResourceEvent}
    (ran : ResourceRun state events = some final) :
    state.resourceBillReceiptCount <= final.resourceBillReceiptCount := by
  induction events generalizing state with
  | nil => simp [ResourceRun] at ran; subst final; exact Nat.le_refl _
  | cons event tail ih =>
      cases stepped : ResourceStep state event with
      | none => simp [ResourceRun, stepped] at ran
      | some next =>
          have tailRan : ResourceRun next tail = some final := by
            simpa [ResourceRun, stepped] using ran
          have stepMonotone : state.resourceBillReceiptCount <=
              next.resourceBillReceiptCount := by
            rw [accepted_step_applies_event stepped]
            exact apply_event_resource_bill_count_monotone state event
          exact Nat.le_trans stepMonotone (ih tailRan)

theorem accepted_run_reconciliation_count_monotone
    {state final : State} {events : List ResourceEvent}
    (ran : ResourceRun state events = some final) :
    state.reconciliationReceiptCount <= final.reconciliationReceiptCount := by
  induction events generalizing state with
  | nil => simp [ResourceRun] at ran; subst final; exact Nat.le_refl _
  | cons event tail ih =>
      cases stepped : ResourceStep state event with
      | none => simp [ResourceRun, stepped] at ran
      | some next =>
          have tailRan : ResourceRun next tail = some final := by
            simpa [ResourceRun, stepped] using ran
          have stepMonotone : state.reconciliationReceiptCount <=
              next.reconciliationReceiptCount := by
            rw [accepted_step_applies_event stepped]
            exact apply_event_reconciliation_count_monotone state event
          exact Nat.le_trans stepMonotone (ih tailRan)

theorem accepted_run_has_accepted_trace
    {state final : State} {events : List ResourceEvent}
    (ran : ResourceRun state events = some final) :
    ResourceTraceAccepted state events := by
  induction events generalizing state with
  | nil => trivial
  | cons event tail ih =>
      cases stepped : ResourceStep state event with
      | none => simp [ResourceRun, stepped] at ran
      | some next =>
          have tailRan : ResourceRun next tail = some final := by
            simpa [ResourceRun, stepped] using ran
          exact ⟨accepted_step_is_accepted stepped, by
            rw [← accepted_step_applies_event stepped]
            exact ih tailRan⟩

theorem resource_run_append (state : State)
    (first second : List ResourceEvent) :
    ResourceRun state (first ++ second) =
      (ResourceRun state first).bind fun intermediate =>
        ResourceRun intermediate second := by
  induction first generalizing state with
  | nil => simp [ResourceRun]
  | cons event tail ih =>
      simp only [List.cons_append, ResourceRun]
      cases ResourceStep state event <;> simp [ih]

theorem closed_state_accepts_no_event (state : State) (event : ResourceEvent)
    (closed : state.stage = .closed) :
    ResourceStep state event = none := by
  simp [ResourceStep, closed]

def initialResourceState : State := completeState .requested

def resourceEventAt (kind : EventKind) (digest : Nat) : ResourceEvent :=
  { kind := kind, packet := { eventDigest := digest } }

def completeResourceEvents : List ResourceEvent :=
  [ resourceEventAt .bindRequest 1
  , resourceEventAt .declareBudget 2
  , resourceEventAt .reserveCapacity 3
  , resourceEventAt .scheduleWork 4
  , resourceEventAt .recordExecution 5
  , resourceEventAt .verifyOutcome 6
  , resourceEventAt .transportClaim 7
  , resourceEventAt .reconcileSpend 8 ]

def completeResourceFinal : State :=
  { initialResourceState with
    stage := .closed
    lastEventDigest := 8
    receiptCount := 8
    resourceBillReceiptCount := 1
    reconciliationReceiptCount := 1 }

theorem complete_resource_run_reaches_closed_with_exact_receipts :
    ResourceRun initialResourceState completeResourceEvents =
      some completeResourceFinal := by
  decide

end AsiStackProofs.ResourceEconomicsRefinement
