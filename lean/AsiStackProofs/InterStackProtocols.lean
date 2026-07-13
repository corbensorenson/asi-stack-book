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

end AsiStackProofs.InterStackProtocols
