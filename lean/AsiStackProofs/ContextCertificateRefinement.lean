namespace AsiStackProofs.ContextCertificateRefinement

/-!
Finite reachable certificate provenance and consumer-admission semantics.
Numeric identities, authority ranks, lifecycle epochs, policy decisions, and
receipts are trusted abstract inputs. The model does not establish source or
payload truth, transformation fidelity, verifier independence, or deployment.
-/

inductive CertificateStage where
  | raw | sourceBound | derived | certified | verified | admitted | revoked | quarantined
deriving DecidableEq, Repr

inductive CertificateEventKind where
  | bindSource | deriveCell | certifyCell | verifyCell | admitUse | revoke | quarantine
deriving DecidableEq, Repr

structure CertificateState where
  stage : CertificateStage
  certificateId : Nat
  sourceId : Nat
  sourceAuthority : Nat
  derivedId : Nat
  derivedAuthority : Nat
  lossContractId : Nat
  omissionLedgerId : Nat
  permittedUseId : Nat
  lifecycleEpoch : Nat
  sourceBindingReceipt : Bool
  certificateReceipt : Bool
  verificationReceipt : Bool
  deletionClosureRequired : Bool
  deletionClosureReceipt : Bool
  evidenceTransitionRequired : Bool
  evidenceTransitionReceipt : Bool
  revoked : Bool
  tainted : Bool
  admitted : Bool
  logicalTime : Nat
deriving DecidableEq, Repr

structure CertificateEvent where
  kind : CertificateEventKind
  fromStage : CertificateStage
  toStage : CertificateStage
  certificateId : Nat
  sourceId : Nat
  sourceAuthority : Nat
  derivedId : Nat
  derivedAuthority : Nat
  lossContractId : Nat
  omissionLedgerId : Nat
  permittedUseId : Nat
  requestedUseId : Nat
  lifecycleEpoch : Nat
  wellFormed : Bool
  derivedRepresentation : Bool
  sourceBindingsDeclared : Bool
  lossContractDeclared : Bool
  omissionsDeclared : Bool
  permittedUsesDeclared : Bool
  sourceBindingReceipt : Bool
  certificateReceipt : Bool
  verifierReferencesDeclared : Bool
  verificationPassed : Bool
  verificationReceipt : Bool
  deletionClosureRequired : Bool
  deletionClosureReceipt : Bool
  supportPromotionRequested : Bool
  evidenceTransitionReceipt : Bool
  revoked : Bool
  revocationReceipt : Bool
  tainted : Bool
  admitted : Bool
  logicalTime : Nat
deriving DecidableEq, Repr

def CertificateIdentityMatches (state : CertificateState) (event : CertificateEvent) : Bool :=
  decide (event.certificateId = state.certificateId) &&
    decide (event.sourceId = state.sourceId) &&
    decide (event.sourceAuthority = state.sourceAuthority)

def DerivedIdentityMatches (state : CertificateState) (event : CertificateEvent) : Bool :=
  CertificateIdentityMatches state event &&
    decide (event.derivedId = state.derivedId) &&
    decide (event.derivedAuthority = state.derivedAuthority)

def ContractIdentityMatches (state : CertificateState) (event : CertificateEvent) : Bool :=
  DerivedIdentityMatches state event &&
    decide (event.lossContractId = state.lossContractId) &&
    decide (event.omissionLedgerId = state.omissionLedgerId) &&
    decide (event.permittedUseId = state.permittedUseId) &&
    decide (event.lifecycleEpoch = state.lifecycleEpoch)

def CertificateEventSpecificValid
    (authorityCeiling : Nat) (state : CertificateState) (event : CertificateEvent) : Bool :=
  match event.kind with
  | .bindSource =>
      decide (event.fromStage = .raw) && decide (event.toStage = .sourceBound) &&
        event.wellFormed && decide (0 < event.certificateId) &&
        decide (0 < event.sourceId) &&
        decide (event.sourceAuthority ≤ authorityCeiling) &&
        decide (0 < event.lifecycleEpoch) && !event.revoked && !event.tainted
  | .deriveCell =>
      decide (event.fromStage = .sourceBound) && decide (event.toStage = .derived) &&
        CertificateIdentityMatches state event && event.derivedRepresentation &&
        event.sourceBindingsDeclared && decide (0 < event.derivedId) &&
        decide (event.derivedAuthority ≤ state.sourceAuthority) &&
        event.sourceBindingReceipt && !event.revoked && !event.tainted
  | .certifyCell =>
      decide (event.fromStage = .derived) && decide (event.toStage = .certified) &&
        DerivedIdentityMatches state event && event.lossContractDeclared &&
        event.omissionsDeclared && event.permittedUsesDeclared &&
        decide (0 < event.lossContractId) && decide (0 < event.omissionLedgerId) &&
        decide (0 < event.permittedUseId) &&
        decide (event.lifecycleEpoch = state.lifecycleEpoch) &&
        event.certificateReceipt && !event.revoked && !event.tainted
  | .verifyCell =>
      decide (event.fromStage = .certified) && decide (event.toStage = .verified) &&
        ContractIdentityMatches state event && event.verifierReferencesDeclared &&
        event.verificationPassed && event.verificationReceipt &&
        decide (event.deletionClosureRequired = state.deletionClosureRequired) &&
        (!event.deletionClosureRequired || event.deletionClosureReceipt) &&
        !event.revoked && !event.tainted
  | .admitUse =>
      decide (event.fromStage = .verified) && decide (event.toStage = .admitted) &&
        ContractIdentityMatches state event &&
        decide (event.requestedUseId = state.permittedUseId) &&
        state.sourceBindingReceipt && state.certificateReceipt &&
        state.verificationReceipt &&
        (!state.deletionClosureRequired || state.deletionClosureReceipt) &&
        (!event.supportPromotionRequested || event.evidenceTransitionReceipt) &&
        !state.revoked && !state.tainted && event.admitted
  | .revoke =>
      decide (event.toStage = .revoked) &&
        decide (event.certificateId = state.certificateId) &&
        decide (state.lifecycleEpoch < event.lifecycleEpoch) &&
        event.revoked && event.revocationReceipt && !event.admitted
  | .quarantine =>
      decide (event.toStage = .quarantined) &&
        decide (event.certificateId = state.certificateId) &&
        event.tainted && !event.admitted

def CertificateEventValid
    (authorityCeiling : Nat) (state : CertificateState) (event : CertificateEvent) : Prop :=
  state.stage = event.fromStage ∧ state.logicalTime < event.logicalTime ∧
    CertificateEventSpecificValid authorityCeiling state event = true

instance certificateEventValidDecidable
    (authorityCeiling : Nat) (state : CertificateState) (event : CertificateEvent) :
    Decidable (CertificateEventValid authorityCeiling state event) := by
  unfold CertificateEventValid
  infer_instance

def ApplyCertificateEvent (state : CertificateState) (event : CertificateEvent) : CertificateState :=
  { state with
    stage := event.toStage
    certificateId := if event.kind = .bindSource then event.certificateId else state.certificateId
    sourceId := if event.kind = .bindSource then event.sourceId else state.sourceId
    sourceAuthority := if event.kind = .bindSource then event.sourceAuthority else state.sourceAuthority
    derivedId := if event.kind = .deriveCell then event.derivedId else state.derivedId
    derivedAuthority := if event.kind = .deriveCell then event.derivedAuthority else state.derivedAuthority
    lossContractId := if event.kind = .certifyCell then event.lossContractId else state.lossContractId
    omissionLedgerId := if event.kind = .certifyCell then event.omissionLedgerId else state.omissionLedgerId
    permittedUseId := if event.kind = .certifyCell then event.permittedUseId else state.permittedUseId
    lifecycleEpoch := if event.kind = .bindSource || event.kind = .revoke then event.lifecycleEpoch else state.lifecycleEpoch
    sourceBindingReceipt := state.sourceBindingReceipt || event.sourceBindingReceipt
    certificateReceipt := state.certificateReceipt || event.certificateReceipt
    verificationReceipt := state.verificationReceipt || event.verificationReceipt
    deletionClosureRequired := if event.kind = .certifyCell then event.deletionClosureRequired else state.deletionClosureRequired
    deletionClosureReceipt := state.deletionClosureReceipt || event.deletionClosureReceipt
    evidenceTransitionRequired := state.evidenceTransitionRequired || event.supportPromotionRequested
    evidenceTransitionReceipt := state.evidenceTransitionReceipt || event.evidenceTransitionReceipt
    revoked := state.revoked || event.revoked
    tainted := state.tainted || event.tainted
    admitted := state.admitted || event.admitted
    logicalTime := event.logicalTime }

def CertificateStep
    (authorityCeiling : Nat) (state : CertificateState) (event : CertificateEvent) :
    Option CertificateState :=
  if CertificateEventValid authorityCeiling state event then
    some (ApplyCertificateEvent state event)
  else none

def CertificateRun (authorityCeiling : Nat) :
    CertificateState → List CertificateEvent → Option CertificateState
  | state, [] => some state
  | state, event :: tail =>
      match CertificateStep authorityCeiling state event with
      | none => none
      | some next => CertificateRun authorityCeiling next tail

theorem accepted_step_is_valid
    {ceiling : Nat} {state next : CertificateState} {event : CertificateEvent}
    (accepted : CertificateStep ceiling state event = some next) :
    CertificateEventValid ceiling state event := by
  unfold CertificateStep at accepted
  split at accepted
  · assumption
  · simp at accepted

theorem accepted_derivation_preserves_source_and_authority
    {ceiling : Nat} {state next : CertificateState} {event : CertificateEvent}
    (kind : event.kind = .deriveCell)
    (accepted : CertificateStep ceiling state event = some next) :
    event.certificateId = state.certificateId ∧
      event.sourceId = state.sourceId ∧
      event.sourceAuthority = state.sourceAuthority ∧
      event.derivedAuthority ≤ state.sourceAuthority ∧
      event.sourceBindingReceipt = true := by
  rcases accepted_step_is_valid accepted with ⟨_, _, specific⟩
  simp [CertificateEventSpecificValid, kind, CertificateIdentityMatches, and_assoc] at specific
  have fields :
      event.fromStage = .sourceBound ∧ event.toStage = .derived ∧
        event.certificateId = state.certificateId ∧ event.sourceId = state.sourceId ∧
        event.sourceAuthority = state.sourceAuthority ∧ event.derivedRepresentation = true ∧
        event.sourceBindingsDeclared = true ∧ 0 < event.derivedId ∧
        event.derivedAuthority ≤ state.sourceAuthority ∧
        event.sourceBindingReceipt = true ∧ event.revoked = false ∧
        event.tainted = false := by
    simpa [and_assoc] using specific
  rcases fields with ⟨_, _, cert, source, sourceAuth, _, _, _, derivedAuth, receipt, _, _⟩
  exact ⟨cert, source, sourceAuth, derivedAuth, receipt⟩

theorem accepted_admission_preserves_provenance_contracts_and_authority
    {ceiling : Nat} {state next : CertificateState} {event : CertificateEvent}
    (kind : event.kind = .admitUse)
    (accepted : CertificateStep ceiling state event = some next) :
    event.certificateId = state.certificateId ∧
      event.sourceId = state.sourceId ∧ event.sourceAuthority = state.sourceAuthority ∧
      event.derivedId = state.derivedId ∧ event.derivedAuthority = state.derivedAuthority ∧
      event.lossContractId = state.lossContractId ∧
      event.omissionLedgerId = state.omissionLedgerId ∧
      event.permittedUseId = state.permittedUseId ∧
      event.requestedUseId = state.permittedUseId ∧
      state.sourceBindingReceipt = true ∧ state.certificateReceipt = true ∧
      state.verificationReceipt = true := by
  rcases accepted_step_is_valid accepted with ⟨_, _, specific⟩
  simp [CertificateEventSpecificValid, kind, ContractIdentityMatches,
    DerivedIdentityMatches, CertificateIdentityMatches, and_assoc] at specific
  have fields :
      event.fromStage = .verified ∧ event.toStage = .admitted ∧
        event.certificateId = state.certificateId ∧ event.sourceId = state.sourceId ∧
        event.sourceAuthority = state.sourceAuthority ∧ event.derivedId = state.derivedId ∧
        event.derivedAuthority = state.derivedAuthority ∧
        event.lossContractId = state.lossContractId ∧
        event.omissionLedgerId = state.omissionLedgerId ∧
        event.permittedUseId = state.permittedUseId ∧
        event.lifecycleEpoch = state.lifecycleEpoch ∧
        event.requestedUseId = state.permittedUseId ∧
        state.sourceBindingReceipt = true ∧ state.certificateReceipt = true ∧
        state.verificationReceipt = true ∧
        (!state.deletionClosureRequired || state.deletionClosureReceipt) = true ∧
        (!event.supportPromotionRequested || event.evidenceTransitionReceipt) = true ∧
        state.revoked = false ∧ state.tainted = false ∧ event.admitted = true := by
    simpa [and_assoc] using specific
  rcases fields with ⟨_, _, cert, source, sourceAuth, derived, derivedAuth, loss,
    omissions, use, _, requested, bindReceipt, certReceipt, verifyReceipt, _, _, _, _, _⟩
  exact ⟨cert, source, sourceAuth, derived, derivedAuth, loss, omissions, use,
    requested, bindReceipt, certReceipt, verifyReceipt⟩

def initialState : CertificateState where
  stage := .raw
  certificateId := 0
  sourceId := 0
  sourceAuthority := 0
  derivedId := 0
  derivedAuthority := 0
  lossContractId := 0
  omissionLedgerId := 0
  permittedUseId := 0
  lifecycleEpoch := 0
  sourceBindingReceipt := false
  certificateReceipt := false
  verificationReceipt := false
  deletionClosureRequired := false
  deletionClosureReceipt := false
  evidenceTransitionRequired := false
  evidenceTransitionReceipt := false
  revoked := false
  tainted := false
  admitted := false
  logicalTime := 0

def baseEvent (kind : CertificateEventKind) (fromStage toStage : CertificateStage)
    (time : Nat) : CertificateEvent where
  kind := kind
  fromStage := fromStage
  toStage := toStage
  certificateId := 101
  sourceId := 201
  sourceAuthority := 3
  derivedId := 301
  derivedAuthority := 2
  lossContractId := 401
  omissionLedgerId := 501
  permittedUseId := 601
  requestedUseId := 601
  lifecycleEpoch := 1
  wellFormed := true
  derivedRepresentation := true
  sourceBindingsDeclared := true
  lossContractDeclared := true
  omissionsDeclared := true
  permittedUsesDeclared := true
  sourceBindingReceipt := false
  certificateReceipt := false
  verifierReferencesDeclared := true
  verificationPassed := true
  verificationReceipt := false
  deletionClosureRequired := true
  deletionClosureReceipt := false
  supportPromotionRequested := false
  evidenceTransitionReceipt := false
  revoked := false
  revocationReceipt := false
  tainted := false
  admitted := false
  logicalTime := time

def bindEvent := baseEvent .bindSource .raw .sourceBound 1
def deriveEvent := { baseEvent .deriveCell .sourceBound .derived 2 with sourceBindingReceipt := true }
def certifyEvent := { baseEvent .certifyCell .derived .certified 3 with certificateReceipt := true }
def verifyEvent := { baseEvent .verifyCell .certified .verified 4 with
  verificationReceipt := true, deletionClosureReceipt := true }
def admitEvent := { baseEvent .admitUse .verified .admitted 5 with admitted := true }
def successTrace := [bindEvent, deriveEvent, certifyEvent, verifyEvent, admitEvent]

theorem exact_certificate_trace_admits :
    (CertificateRun 4 initialState successTrace).map (fun state =>
      (state.stage, state.admitted, state.sourceBindingReceipt,
        state.certificateReceipt, state.verificationReceipt)) =
      some (.admitted, true, true, true, true) := by
  native_decide

def spliceRun (before : List CertificateEvent) (event : CertificateEvent)
    (after : List CertificateEvent) :=
  CertificateRun 4 initialState (before ++ event :: after)

theorem source_substitution_rejected :
    spliceRun [bindEvent] { deriveEvent with sourceId := 999 } [certifyEvent, verifyEvent, admitEvent] = none := by native_decide
theorem authority_escalation_rejected :
    spliceRun [bindEvent] { deriveEvent with derivedAuthority := 4 } [certifyEvent, verifyEvent, admitEvent] = none := by native_decide
theorem missing_source_binding_receipt_rejected :
    spliceRun [bindEvent] { deriveEvent with sourceBindingReceipt := false } [certifyEvent, verifyEvent, admitEvent] = none := by native_decide
theorem missing_loss_contract_rejected :
    spliceRun [bindEvent, deriveEvent] { certifyEvent with lossContractDeclared := false } [verifyEvent, admitEvent] = none := by native_decide
theorem missing_omission_ledger_rejected :
    spliceRun [bindEvent, deriveEvent] { certifyEvent with omissionsDeclared := false } [verifyEvent, admitEvent] = none := by native_decide
theorem missing_permitted_use_rejected :
    spliceRun [bindEvent, deriveEvent] { certifyEvent with permittedUsesDeclared := false } [verifyEvent, admitEvent] = none := by native_decide
theorem stale_certificate_epoch_rejected :
    spliceRun [bindEvent, deriveEvent, certifyEvent] { verifyEvent with lifecycleEpoch := 2 } [admitEvent] = none := by native_decide
theorem missing_verification_receipt_rejected :
    spliceRun [bindEvent, deriveEvent, certifyEvent] { verifyEvent with verificationReceipt := false } [admitEvent] = none := by native_decide
theorem missing_deletion_closure_rejected :
    spliceRun [bindEvent, deriveEvent, certifyEvent] { verifyEvent with deletionClosureReceipt := false } [admitEvent] = none := by native_decide
theorem unpermitted_consumer_use_rejected :
    spliceRun [bindEvent, deriveEvent, certifyEvent, verifyEvent] { admitEvent with requestedUseId := 999 } [] = none := by native_decide
theorem support_promotion_without_transition_rejected :
    spliceRun [bindEvent, deriveEvent, certifyEvent, verifyEvent]
      { admitEvent with supportPromotionRequested := true } [] = none := by native_decide
theorem tainted_verification_rejected :
    spliceRun [bindEvent, deriveEvent, certifyEvent] { verifyEvent with tainted := true } [admitEvent] = none := by native_decide
theorem revoked_verification_rejected :
    spliceRun [bindEvent, deriveEvent, certifyEvent] { verifyEvent with revoked := true } [admitEvent] = none := by native_decide

end AsiStackProofs.ContextCertificateRefinement
