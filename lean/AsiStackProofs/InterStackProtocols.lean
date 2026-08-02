namespace AsiStackProofs.InterStackProtocols

inductive InterStackDispatchRoute where
  | retainAsExchangeDraft
  | requireIdentityRepair
  | requireAccountableReview
  | requireBudgetRepair
  | denyDispatch
  | releaseToLocalDispatch
deriving DecidableEq, Repr

structure InterStackExchangeRecord where
  protocolVersionRecorded : Bool
  endpointCapabilityRecorded : Bool
  senderIdentityRecorded : Bool
  receiverIdentityRecorded : Bool
  principalRecorded : Bool
  delegatedAuthorityRecorded : Bool
  audienceScopeBound : Bool
  requestExpiryCurrent : Bool
  credentialRequired : Bool
  credentialVerified : Bool
  credentialCurrent : Bool
  revocationPathRecorded : Bool
  valueBearingRequest : Bool
  budgetReserved : Bool
  expectedReceiptRecorded : Bool
  receiptDisputed : Bool
  residualOwnerRecorded : Bool
  dispatchRequested : Bool
deriving DecidableEq, Repr

def InterStackDispatchRouteFor (record : InterStackExchangeRecord) : InterStackDispatchRoute :=
  if record.protocolVersionRecorded = false then
    InterStackDispatchRoute.retainAsExchangeDraft
  else if record.endpointCapabilityRecorded = false then
    InterStackDispatchRoute.requireAccountableReview
  else if record.senderIdentityRecorded = false then
    InterStackDispatchRoute.requireIdentityRepair
  else if record.receiverIdentityRecorded = false then
    InterStackDispatchRoute.requireIdentityRepair
  else if record.principalRecorded = false then
    InterStackDispatchRoute.requireIdentityRepair
  else if record.delegatedAuthorityRecorded = false then
    InterStackDispatchRoute.requireAccountableReview
  else if record.audienceScopeBound = false then
    InterStackDispatchRoute.denyDispatch
  else if record.requestExpiryCurrent = false then
    InterStackDispatchRoute.denyDispatch
  else if record.credentialRequired = true && record.credentialVerified = false then
    InterStackDispatchRoute.denyDispatch
  else if record.credentialCurrent = false then
    InterStackDispatchRoute.denyDispatch
  else if record.revocationPathRecorded = false then
    InterStackDispatchRoute.requireAccountableReview
  else if record.valueBearingRequest = true && record.budgetReserved = false then
    InterStackDispatchRoute.requireBudgetRepair
  else if record.expectedReceiptRecorded = false then
    InterStackDispatchRoute.requireAccountableReview
  else if record.receiptDisputed = true then
    InterStackDispatchRoute.requireAccountableReview
  else if record.residualOwnerRecorded = false then
    InterStackDispatchRoute.requireAccountableReview
  else if record.dispatchRequested = true then
    InterStackDispatchRoute.releaseToLocalDispatch
  else
    InterStackDispatchRoute.retainAsExchangeDraft

theorem invalid_credential_blocks_dispatch
    {record : InterStackExchangeRecord} :
    record.protocolVersionRecorded = true ->
    record.endpointCapabilityRecorded = true ->
    record.senderIdentityRecorded = true ->
    record.receiverIdentityRecorded = true ->
    record.principalRecorded = true ->
    record.delegatedAuthorityRecorded = true ->
    record.audienceScopeBound = true ->
    record.requestExpiryCurrent = true ->
    record.credentialRequired = true ->
    record.credentialVerified = false ->
    InterStackDispatchRouteFor record = InterStackDispatchRoute.denyDispatch := by
  intro protocol endpoint sender receiver principal delegated audience expiry
    credentialRequired credentialInvalid
  unfold InterStackDispatchRouteFor
  simp [protocol, endpoint, sender, receiver, principal, delegated, audience,
    expiry, credentialRequired, credentialInvalid]

theorem missing_reserved_budget_blocks_economic_dispatch
    {record : InterStackExchangeRecord} :
    record.protocolVersionRecorded = true ->
    record.endpointCapabilityRecorded = true ->
    record.senderIdentityRecorded = true ->
    record.receiverIdentityRecorded = true ->
    record.principalRecorded = true ->
    record.delegatedAuthorityRecorded = true ->
    record.audienceScopeBound = true ->
    record.requestExpiryCurrent = true ->
    record.credentialRequired = false ->
    record.credentialCurrent = true ->
    record.revocationPathRecorded = true ->
    record.valueBearingRequest = true ->
    record.budgetReserved = false ->
    InterStackDispatchRouteFor record = InterStackDispatchRoute.requireBudgetRepair := by
  intro protocol endpoint sender receiver principal delegated audience expiry
    credentialNotRequired credentialCurrent revocationPath valueBearing budgetNotReserved
  unfold InterStackDispatchRouteFor
  simp [protocol, endpoint, sender, receiver, principal, delegated, audience,
    expiry, credentialNotRequired, credentialCurrent, revocationPath, valueBearing,
    budgetNotReserved]

theorem complete_exchange_reaches_local_dispatch
    {record : InterStackExchangeRecord} :
    record.protocolVersionRecorded = true ->
    record.endpointCapabilityRecorded = true ->
    record.senderIdentityRecorded = true ->
    record.receiverIdentityRecorded = true ->
    record.principalRecorded = true ->
    record.delegatedAuthorityRecorded = true ->
    record.audienceScopeBound = true ->
    record.requestExpiryCurrent = true ->
    record.credentialRequired = false ->
    record.credentialCurrent = true ->
    record.revocationPathRecorded = true ->
    record.valueBearingRequest = false ->
    record.expectedReceiptRecorded = true ->
    record.receiptDisputed = false ->
    record.residualOwnerRecorded = true ->
    record.dispatchRequested = true ->
    InterStackDispatchRouteFor record = InterStackDispatchRoute.releaseToLocalDispatch := by
  intro protocol endpoint sender receiver principal delegated audience expiry
    credentialNotRequired credentialCurrent revocationPath notValueBearing receipt
    notDisputed residual dispatch
  unfold InterStackDispatchRouteFor
  simp [protocol, endpoint, sender, receiver, principal, delegated, audience,
    expiry, credentialNotRequired, credentialCurrent, revocationPath,
    notValueBearing, receipt, notDisputed, residual, dispatch]

theorem missing_sender_requires_identity_repair
    {record : InterStackExchangeRecord} :
    record.protocolVersionRecorded = true ->
    record.endpointCapabilityRecorded = true ->
    record.senderIdentityRecorded = false ->
    InterStackDispatchRouteFor record = InterStackDispatchRoute.requireIdentityRepair := by
  intro protocol endpoint sender
  unfold InterStackDispatchRouteFor
  simp [protocol, endpoint, sender]

theorem audience_mismatch_denies_dispatch
    {record : InterStackExchangeRecord} :
    record.protocolVersionRecorded = true ->
    record.endpointCapabilityRecorded = true ->
    record.senderIdentityRecorded = true ->
    record.receiverIdentityRecorded = true ->
    record.principalRecorded = true ->
    record.delegatedAuthorityRecorded = true ->
    record.audienceScopeBound = false ->
    InterStackDispatchRouteFor record = InterStackDispatchRoute.denyDispatch := by
  intro protocol endpoint sender receiver principal delegated audience
  unfold InterStackDispatchRouteFor
  simp [protocol, endpoint, sender, receiver, principal, delegated, audience]

theorem expired_request_denies_dispatch
    {record : InterStackExchangeRecord} :
    record.protocolVersionRecorded = true ->
    record.endpointCapabilityRecorded = true ->
    record.senderIdentityRecorded = true ->
    record.receiverIdentityRecorded = true ->
    record.principalRecorded = true ->
    record.delegatedAuthorityRecorded = true ->
    record.audienceScopeBound = true ->
    record.requestExpiryCurrent = false ->
    InterStackDispatchRouteFor record = InterStackDispatchRoute.denyDispatch := by
  intro protocol endpoint sender receiver principal delegated audience expiry
  unfold InterStackDispatchRouteFor
  simp [protocol, endpoint, sender, receiver, principal, delegated, audience, expiry]

theorem revoked_credential_denies_dispatch
    {record : InterStackExchangeRecord} :
    record.protocolVersionRecorded = true ->
    record.endpointCapabilityRecorded = true ->
    record.senderIdentityRecorded = true ->
    record.receiverIdentityRecorded = true ->
    record.principalRecorded = true ->
    record.delegatedAuthorityRecorded = true ->
    record.audienceScopeBound = true ->
    record.requestExpiryCurrent = true ->
    record.credentialRequired = true ->
    record.credentialVerified = true ->
    record.credentialCurrent = false ->
    InterStackDispatchRouteFor record = InterStackDispatchRoute.denyDispatch := by
  intro protocol endpoint sender receiver principal delegated audience expiry
    credentialRequired credentialVerified credentialRevoked
  unfold InterStackDispatchRouteFor
  simp [protocol, endpoint, sender, receiver, principal, delegated, audience,
    expiry, credentialRequired, credentialVerified, credentialRevoked]

theorem disputed_receipt_requires_review
    {record : InterStackExchangeRecord} :
    record.protocolVersionRecorded = true ->
    record.endpointCapabilityRecorded = true ->
    record.senderIdentityRecorded = true ->
    record.receiverIdentityRecorded = true ->
    record.principalRecorded = true ->
    record.delegatedAuthorityRecorded = true ->
    record.audienceScopeBound = true ->
    record.requestExpiryCurrent = true ->
    record.credentialRequired = false ->
    record.credentialCurrent = true ->
    record.revocationPathRecorded = true ->
    record.valueBearingRequest = false ->
    record.expectedReceiptRecorded = true ->
    record.receiptDisputed = true ->
    InterStackDispatchRouteFor record = InterStackDispatchRoute.requireAccountableReview := by
  intro protocol endpoint sender receiver principal delegated audience expiry
    credentialNotRequired credentialCurrent revocationPath notValueBearing receipt disputed
  unfold InterStackDispatchRouteFor
  simp [protocol, endpoint, sender, receiver, principal, delegated, audience,
    expiry, credentialNotRequired, credentialCurrent, revocationPath,
    notValueBearing, receipt, disputed]

theorem missing_residual_owner_requires_review
    {record : InterStackExchangeRecord} :
    record.protocolVersionRecorded = true ->
    record.endpointCapabilityRecorded = true ->
    record.senderIdentityRecorded = true ->
    record.receiverIdentityRecorded = true ->
    record.principalRecorded = true ->
    record.delegatedAuthorityRecorded = true ->
    record.audienceScopeBound = true ->
    record.requestExpiryCurrent = true ->
    record.credentialRequired = false ->
    record.credentialCurrent = true ->
    record.revocationPathRecorded = true ->
    record.valueBearingRequest = false ->
    record.expectedReceiptRecorded = true ->
    record.receiptDisputed = false ->
    record.residualOwnerRecorded = false ->
    InterStackDispatchRouteFor record = InterStackDispatchRoute.requireAccountableReview := by
  intro protocol endpoint sender receiver principal delegated audience expiry
    credentialNotRequired credentialCurrent revocationPath notValueBearing receipt
    notDisputed residual
  unfold InterStackDispatchRouteFor
  simp [protocol, endpoint, sender, receiver, principal, delegated, audience,
    expiry, credentialNotRequired, credentialCurrent, revocationPath,
    notValueBearing, receipt, notDisputed, residual]

/-! A local handoff lifecycle. Authored fields are assumptions; no peer trust,
credential truth, settlement, payment, execution, or external effect is proved. -/

inductive ExchangeStage where
  | draft | identityBound | delegationBound | budgetBound | dispatched | receipted | closed
deriving DecidableEq, Repr

inductive ExchangeEventKind where
  | bindIdentity | bindDelegation | bindBudget | requestLocalDispatch | recordReceipt | closeExchange
deriving DecidableEq, Repr

inductive ExchangeRoute where
  | rejectWrongStage | rejectIdentitySubstitution | rejectReplay | rejectAuthorityLaundering
  | requestEndpoint | requestSender | requestReceiver | requestPrincipal
  | requestDelegation | rejectAudience | rejectExpiry | rejectCredential
  | requestRevocationPath | requestBudget | requestExpectedReceipt
  | requestObservedReceipt | requestDisputeDisposition | requestResidualOwner
  | acceptIdentity | acceptDelegation | acceptBudget | acceptDispatch | acceptReceipt | acceptClosure
deriving DecidableEq, Repr

structure ExchangeState where
  stage : ExchangeStage
  exchangeId : Nat
  protocolVersion : Nat
  senderId : Nat
  receiverId : Nat
  principalId : Nat
  requestDigest : Nat
  budgetDigest : Nat
  receiptDigest : Nat
  authorityCeiling : Nat
  lastEventDigest : Nat
  receiptCount : Nat
  localHandoffCount : Nat
  closureCount : Nat
  supportAssignmentCount : Nat
  externalEffectCount : Nat
  settlementCount : Nat
deriving DecidableEq, Repr

structure ExchangePacket where
  exchangeId : Nat
  protocolVersion : Nat
  senderId : Nat
  receiverId : Nat
  principalId : Nat
  requestDigest : Nat
  budgetDigest : Nat
  receiptDigest : Nat
  authorityCeiling : Nat
  eventDigest : Nat
  endpointCapabilityRecorded : Bool
  senderIdentityRecorded : Bool
  receiverIdentityRecorded : Bool
  principalRecorded : Bool
  delegationRecorded : Bool
  audienceBound : Bool
  expiryCurrent : Bool
  credentialRequired : Bool
  credentialVerified : Bool
  credentialCurrent : Bool
  revocationPathRecorded : Bool
  valueBearing : Bool
  budgetReserved : Bool
  expectedReceiptRecorded : Bool
  observedReceiptRecorded : Bool
  receiptDisputed : Bool
  disputeDispositionPresent : Bool
  residualOwnerRecorded : Bool
  supportAssignmentRequested : Bool
  externalEffectRequested : Bool
  settlementRequested : Bool
deriving DecidableEq, Repr

def expectedExchangeKind : ExchangeStage -> ExchangeEventKind
  | .draft => .bindIdentity
  | .identityBound => .bindDelegation
  | .delegationBound => .bindBudget
  | .budgetBound => .requestLocalDispatch
  | .dispatched => .recordReceipt
  | .receipted => .closeExchange
  | .closed => .bindIdentity

def exchangeIdentityMatches (state : ExchangeState) (packet : ExchangePacket) : Bool :=
  state.exchangeId = packet.exchangeId && state.protocolVersion = packet.protocolVersion &&
    state.senderId = packet.senderId && state.receiverId = packet.receiverId &&
    state.principalId = packet.principalId && state.requestDigest = packet.requestDigest &&
    state.budgetDigest = packet.budgetDigest && state.receiptDigest = packet.receiptDigest &&
    state.authorityCeiling = packet.authorityCeiling

def ExchangeRouteFor (state : ExchangeState) (kind : ExchangeEventKind)
    (packet : ExchangePacket) : ExchangeRoute :=
  if kind != expectedExchangeKind state.stage then .rejectWrongStage
  else if exchangeIdentityMatches state packet = false then .rejectIdentitySubstitution
  else if packet.eventDigest = state.lastEventDigest then .rejectReplay
  else if packet.supportAssignmentRequested || packet.externalEffectRequested ||
      packet.settlementRequested then .rejectAuthorityLaundering
  else match state.stage with
  | .draft | .closed =>
      if packet.endpointCapabilityRecorded = false then .requestEndpoint
      else if packet.senderIdentityRecorded = false then .requestSender
      else if packet.receiverIdentityRecorded = false then .requestReceiver
      else if packet.principalRecorded = false then .requestPrincipal
      else .acceptIdentity
  | .identityBound =>
      if packet.delegationRecorded = false then .requestDelegation
      else if packet.audienceBound = false then .rejectAudience
      else if packet.expiryCurrent = false then .rejectExpiry
      else if packet.credentialRequired &&
          (packet.credentialVerified = false || packet.credentialCurrent = false) then
        .rejectCredential
      else if packet.revocationPathRecorded = false then .requestRevocationPath
      else .acceptDelegation
  | .delegationBound =>
      if packet.valueBearing && packet.budgetReserved = false then .requestBudget
      else .acceptBudget
  | .budgetBound =>
      if packet.expectedReceiptRecorded = false then .requestExpectedReceipt
      else .acceptDispatch
  | .dispatched =>
      if packet.observedReceiptRecorded = false then .requestObservedReceipt
      else .acceptReceipt
  | .receipted =>
      if packet.receiptDisputed && packet.disputeDispositionPresent = false then
        .requestDisputeDisposition
      else if packet.residualOwnerRecorded = false then .requestResidualOwner
      else .acceptClosure

def exchangeAccepted : ExchangeRoute -> Bool
  | .acceptIdentity | .acceptDelegation | .acceptBudget | .acceptDispatch
  | .acceptReceipt | .acceptClosure => true
  | _ => false

def nextExchangeStage : ExchangeStage -> ExchangeStage
  | .draft | .closed => .identityBound
  | .identityBound => .delegationBound
  | .delegationBound => .budgetBound
  | .budgetBound => .dispatched
  | .dispatched => .receipted
  | .receipted => .closed

def applyExchange (state : ExchangeState) (kind : ExchangeEventKind)
    (packet : ExchangePacket) : ExchangeState :=
  let route := ExchangeRouteFor state kind packet
  if exchangeAccepted route then
    { state with
      stage := nextExchangeStage state.stage
      lastEventDigest := packet.eventDigest
      receiptCount := state.receiptCount + 1
      localHandoffCount := state.localHandoffCount +
        (if kind = .requestLocalDispatch then 1 else 0)
      closureCount := state.closureCount + (if kind = .closeExchange then 1 else 0) }
  else state

structure ExchangeEvent where
  kind : ExchangeEventKind
  packet : ExchangePacket
deriving DecidableEq, Repr

def runExchange : ExchangeState -> List ExchangeEvent -> ExchangeState
  | state, [] => state
  | state, event :: rest => runExchange (applyExchange state event.kind event.packet) rest

theorem rejected_exchange_event_preserves_exact_state
    (state : ExchangeState) (kind : ExchangeEventKind) (packet : ExchangePacket)
    (rejected : exchangeAccepted (ExchangeRouteFor state kind packet) = false) :
    applyExchange state kind packet = state := by simp [applyExchange, rejected]

theorem exchange_event_preserves_exact_identity
    (state : ExchangeState) (kind : ExchangeEventKind) (packet : ExchangePacket) :
    let next := applyExchange state kind packet
    next.exchangeId = state.exchangeId ∧ next.protocolVersion = state.protocolVersion ∧
      next.senderId = state.senderId ∧ next.receiverId = state.receiverId ∧
      next.principalId = state.principalId ∧ next.requestDigest = state.requestDigest ∧
      next.budgetDigest = state.budgetDigest ∧ next.receiptDigest = state.receiptDigest ∧
      next.authorityCeiling = state.authorityCeiling := by
  by_cases h : exchangeAccepted (ExchangeRouteFor state kind packet) = true <;>
    simp [applyExchange, h]

theorem exchange_event_cannot_assign_support_effect_or_settlement
    (state : ExchangeState) (kind : ExchangeEventKind) (packet : ExchangePacket) :
    let next := applyExchange state kind packet
    next.supportAssignmentCount = state.supportAssignmentCount ∧
      next.externalEffectCount = state.externalEffectCount ∧
      next.settlementCount = state.settlementCount := by
  by_cases h : exchangeAccepted (ExchangeRouteFor state kind packet) = true <;>
    simp [applyExchange, h]

theorem run_exchange_preserves_identity (state : ExchangeState) (events : List ExchangeEvent) :
    let final := runExchange state events
    final.exchangeId = state.exchangeId ∧ final.protocolVersion = state.protocolVersion ∧
      final.senderId = state.senderId ∧ final.receiverId = state.receiverId ∧
      final.principalId = state.principalId ∧ final.requestDigest = state.requestDigest ∧
      final.budgetDigest = state.budgetDigest ∧ final.receiptDigest = state.receiptDigest ∧
      final.authorityCeiling = state.authorityCeiling := by
  induction events generalizing state with
  | nil => simp [runExchange]
  | cons event rest ih =>
      have head := exchange_event_preserves_exact_identity state event.kind event.packet
      have tail := ih (applyExchange state event.kind event.packet)
      simp only at head tail ⊢
      exact ⟨tail.1.trans head.1, tail.2.1.trans head.2.1,
        tail.2.2.1.trans head.2.2.1, tail.2.2.2.1.trans head.2.2.2.1,
        tail.2.2.2.2.1.trans head.2.2.2.2.1,
        tail.2.2.2.2.2.1.trans head.2.2.2.2.2.1,
        tail.2.2.2.2.2.2.1.trans head.2.2.2.2.2.2.1,
        tail.2.2.2.2.2.2.2.1.trans head.2.2.2.2.2.2.2.1,
        tail.2.2.2.2.2.2.2.2.trans head.2.2.2.2.2.2.2.2⟩

theorem run_exchange_preserves_non_authority (state : ExchangeState)
    (events : List ExchangeEvent) :
    let final := runExchange state events
    final.supportAssignmentCount = state.supportAssignmentCount ∧
      final.externalEffectCount = state.externalEffectCount ∧
      final.settlementCount = state.settlementCount := by
  induction events generalizing state with
  | nil => simp [runExchange]
  | cons event rest ih =>
      have head := exchange_event_cannot_assign_support_effect_or_settlement
        state event.kind event.packet
      have tail := ih (applyExchange state event.kind event.packet)
      simp only at head tail ⊢
      exact ⟨tail.1.trans head.1, tail.2.1.trans head.2.1,
        tail.2.2.trans head.2.2⟩

theorem run_exchange_composes (state : ExchangeState)
    (left right : List ExchangeEvent) :
    runExchange state (left ++ right) = runExchange (runExchange state left) right := by
  induction left generalizing state with
  | nil => simp [runExchange]
  | cons event rest ih => simp [runExchange, ih]

def canonicalExchangeState : ExchangeState :=
  { stage := .draft, exchangeId := 801, protocolVersion := 4, senderId := 802,
    receiverId := 803, principalId := 804, requestDigest := 805, budgetDigest := 806,
    receiptDigest := 807, authorityCeiling := 2, lastEventDigest := 0,
    receiptCount := 0, localHandoffCount := 0, closureCount := 0,
    supportAssignmentCount := 0, externalEffectCount := 0, settlementCount := 0 }

def canonicalExchangePacket (digest : Nat) : ExchangePacket :=
  { exchangeId := 801, protocolVersion := 4, senderId := 802, receiverId := 803,
    principalId := 804, requestDigest := 805, budgetDigest := 806, receiptDigest := 807,
    authorityCeiling := 2, eventDigest := digest, endpointCapabilityRecorded := true,
    senderIdentityRecorded := true, receiverIdentityRecorded := true, principalRecorded := true,
    delegationRecorded := true, audienceBound := true, expiryCurrent := true,
    credentialRequired := true, credentialVerified := true, credentialCurrent := true,
    revocationPathRecorded := true, valueBearing := true, budgetReserved := true,
    expectedReceiptRecorded := true, observedReceiptRecorded := true, receiptDisputed := false,
    disputeDispositionPresent := true, residualOwnerRecorded := true,
    supportAssignmentRequested := false, externalEffectRequested := false,
    settlementRequested := false }

def exchangeEvent (kind : ExchangeEventKind) (digest : Nat) : ExchangeEvent :=
  { kind := kind, packet := canonicalExchangePacket digest }

def completeExchangeTrace : List ExchangeEvent :=
  [exchangeEvent .bindIdentity 1, exchangeEvent .bindDelegation 2,
   exchangeEvent .bindBudget 3, exchangeEvent .requestLocalDispatch 4,
   exchangeEvent .recordReceipt 5, exchangeEvent .closeExchange 6]

theorem complete_exchange_lifecycle_closes_without_authority :
    runExchange canonicalExchangeState completeExchangeTrace =
      { canonicalExchangeState with
        stage := .closed
        lastEventDigest := 6
        receiptCount := 6
        localHandoffCount := 1
        closureCount := 1 } := by native_decide

theorem lifecycle_missing_sender_blocks_identity :
    ExchangeRouteFor canonicalExchangeState .bindIdentity
      { canonicalExchangePacket 1 with senderIdentityRecorded := false } = .requestSender := by native_decide

theorem lifecycle_expired_delegation_blocks_exchange :
    ExchangeRouteFor { canonicalExchangeState with stage := .identityBound } .bindDelegation
      { canonicalExchangePacket 2 with expiryCurrent := false } = .rejectExpiry := by native_decide

theorem lifecycle_invalid_credential_blocks_exchange :
    ExchangeRouteFor { canonicalExchangeState with stage := .identityBound } .bindDelegation
      { canonicalExchangePacket 2 with credentialVerified := false } = .rejectCredential := by native_decide

theorem lifecycle_authority_laundering_blocks_exchange :
    ExchangeRouteFor { canonicalExchangeState with stage := .budgetBound } .requestLocalDispatch
      { canonicalExchangePacket 4 with settlementRequested := true } =
        .rejectAuthorityLaundering := by native_decide

theorem lifecycle_missing_budget_blocks_value_exchange :
    ExchangeRouteFor { canonicalExchangeState with stage := .delegationBound } .bindBudget
      { canonicalExchangePacket 3 with budgetReserved := false } = .requestBudget := by native_decide

theorem lifecycle_missing_expected_receipt_blocks_dispatch :
    ExchangeRouteFor { canonicalExchangeState with stage := .budgetBound } .requestLocalDispatch
      { canonicalExchangePacket 4 with expectedReceiptRecorded := false } =
        .requestExpectedReceipt := by native_decide

theorem lifecycle_missing_observed_receipt_blocks_receipt :
    ExchangeRouteFor { canonicalExchangeState with stage := .dispatched } .recordReceipt
      { canonicalExchangePacket 5 with observedReceiptRecorded := false } =
        .requestObservedReceipt := by native_decide

theorem lifecycle_undispositioned_dispute_blocks_closure :
    ExchangeRouteFor { canonicalExchangeState with stage := .receipted } .closeExchange
      { { canonicalExchangePacket 6 with receiptDisputed := true } with
        disputeDispositionPresent := false } = .requestDisputeDisposition := by native_decide

theorem lifecycle_missing_residual_owner_blocks_closure :
    ExchangeRouteFor { canonicalExchangeState with stage := .receipted } .closeExchange
      { canonicalExchangePacket 6 with residualOwnerRecorded := false } =
        .requestResidualOwner := by native_decide

end AsiStackProofs.InterStackProtocols
