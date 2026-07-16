namespace AsiStackProofs.ClaimLedgerRefinement

/-!
A reachable append-only claim-ledger lifecycle.  The ledger can validate and
materialize an evidence-owner decision, but cannot create support authority,
establish truth, or commit an external effect.
-/

inductive RevisionAction where
  | noChange
  | narrow
  | split
  | merge
  | downgrade
  | deprecate
  | supersede
  | dispute
  | requestPromotion
deriving DecidableEq, Repr

inductive LifecycleEventKind where
  | propose
  | append
  | materialize
  | acknowledge
deriving DecidableEq, Repr

inductive LifecycleStage where
  | idle
  | proposed
  | appended
  | materialized
  | acknowledged
deriving DecidableEq, Repr

inductive RevisionRoute where
  | rejectWrongStage
  | rejectStaleBase
  | rejectEventSubstitution
  | rejectLedgerAuthorityLeak
  | blockOpenContradiction
  | handoffToEvidenceOwner
  | requestHistoryAndNonOverwrite
  | requestRevisionReason
  | requestResidualRecord
  | requestDependencyClosure
  | requestOntologyMigration
  | requestSurfacePlan
  | requestSurfaceAcknowledgment
  | acceptProposal
  | authorizeAppend
  | materializeView
  | acknowledgeSurfaces
deriving DecidableEq, Repr

structure LedgerState where
  claimId : Nat
  ledgerVersion : Nat
  headDigest : Nat
  semanticVersion : Nat
  ontologyVersion : Nat
  supportRank : Nat
  stage : LifecycleStage
  pendingEventDigest : Option Nat
  requiredSurfaceAcks : Nat
  observedSurfaceAcks : Nat
  materializedLedgerVersion : Nat
  appendCount : Nat
  externalEffects : Nat
deriving DecidableEq, Repr

structure RevisionEvent where
  kind : LifecycleEventKind
  action : RevisionAction
  eventDigest : Nat
  claimId : Nat
  baseLedgerVersion : Nat
  priorHeadDigest : Nat
  priorSemanticVersion : Nat
  nextSemanticVersion : Nat
  priorOntologyVersion : Nat
  nextOntologyVersion : Nat
  priorSupportRank : Nat
  nextSupportRank : Nat
  ledgerSelfApprovesSupport : Bool
  externalEffectRequested : Bool
  evidenceOwnerReceiptPresent : Bool
  openContradiction : Bool
  historyRefsPresent : Bool
  nonOverwriteAttestationPresent : Bool
  revisionReasonPresent : Bool
  residualRequired : Bool
  residualRefsPresent : Bool
  dependencyClosureComplete : Bool
  ontologyMigrationReceiptPresent : Bool
  surfacePlanComplete : Bool
  requiredSurfaceAcks : Nat
  observedSurfaceAcks : Nat
  surfaceAcknowledgmentReceiptPresent : Bool
deriving DecidableEq, Repr

def ExactBase (state : LedgerState) (event : RevisionEvent) : Bool :=
  decide (event.claimId = state.claimId) &&
    decide (event.baseLedgerVersion = state.ledgerVersion) &&
    decide (event.priorHeadDigest = state.headDigest) &&
    decide (event.priorSemanticVersion = state.semanticVersion) &&
    decide (event.priorOntologyVersion = state.ontologyVersion) &&
    decide (event.priorSupportRank = state.supportRank)

def SupportMovesUp (event : RevisionEvent) : Bool :=
  decide (event.priorSupportRank < event.nextSupportRank)

def OntologyChanges (event : RevisionEvent) : Bool :=
  decide (event.priorOntologyVersion != event.nextOntologyVersion)

def RevisionRouteFor (state : LedgerState) (event : RevisionEvent) : RevisionRoute :=
  match event.kind with
  | .propose =>
      if state.stage != LifecycleStage.idle then
        .rejectWrongStage
      else if ExactBase state event = false || event.nextSemanticVersion != state.semanticVersion + 1 then
        .rejectStaleBase
      else if event.ledgerSelfApprovesSupport || event.externalEffectRequested then
        .rejectLedgerAuthorityLeak
      else if SupportMovesUp event && event.openContradiction then
        .blockOpenContradiction
      else if SupportMovesUp event && !event.evidenceOwnerReceiptPresent then
        .handoffToEvidenceOwner
      else if !event.historyRefsPresent || !event.nonOverwriteAttestationPresent then
        .requestHistoryAndNonOverwrite
      else if !event.revisionReasonPresent then
        .requestRevisionReason
      else if event.residualRequired && !event.residualRefsPresent then
        .requestResidualRecord
      else if !event.dependencyClosureComplete then
        .requestDependencyClosure
      else if OntologyChanges event && !event.ontologyMigrationReceiptPresent then
        .requestOntologyMigration
      else if !event.surfacePlanComplete || event.requiredSurfaceAcks = 0 then
        .requestSurfacePlan
      else
        .acceptProposal
  | .append =>
      if state.stage != LifecycleStage.proposed then
        .rejectWrongStage
      else if state.pendingEventDigest != some event.eventDigest then
        .rejectEventSubstitution
      else if ExactBase state event = false then
        .rejectStaleBase
      else
        .authorizeAppend
  | .materialize =>
      if state.stage != LifecycleStage.appended then
        .rejectWrongStage
      else if state.headDigest != event.eventDigest || state.ledgerVersion != event.baseLedgerVersion + 1 then
        .rejectEventSubstitution
      else
        .materializeView
  | .acknowledge =>
      if state.stage != LifecycleStage.materialized then
        .rejectWrongStage
      else if state.headDigest != event.eventDigest || state.materializedLedgerVersion != state.ledgerVersion then
        .rejectEventSubstitution
      else if
          !event.surfaceAcknowledgmentReceiptPresent ||
            event.observedSurfaceAcks != state.requiredSurfaceAcks then
        .requestSurfaceAcknowledgment
      else
        .acknowledgeSurfaces

def ApplyEvent (state : LedgerState) (event : RevisionEvent) : LedgerState :=
  match event.kind with
  | .propose =>
      { state with
        stage := .proposed
        pendingEventDigest := some event.eventDigest
        requiredSurfaceAcks := event.requiredSurfaceAcks
        observedSurfaceAcks := 0 }
  | .append =>
      { state with
        ledgerVersion := state.ledgerVersion + 1
        headDigest := event.eventDigest
        semanticVersion := event.nextSemanticVersion
        ontologyVersion := event.nextOntologyVersion
        supportRank := event.nextSupportRank
        stage := .appended
        pendingEventDigest := none
        appendCount := state.appendCount + 1 }
  | .materialize =>
      { state with
        stage := .materialized
        materializedLedgerVersion := state.ledgerVersion }
  | .acknowledge =>
      { state with
        stage := .acknowledged
        observedSurfaceAcks := event.observedSurfaceAcks }

def Step (state : LedgerState) (event : RevisionEvent) : Option LedgerState :=
  match RevisionRouteFor state event with
  | .acceptProposal
  | .authorizeAppend
  | .materializeView
  | .acknowledgeSurfaces => some (ApplyEvent state event)
  | _ => none

def Run : LedgerState -> List RevisionEvent -> Option LedgerState
  | state, [] => some state
  | state, event :: tail =>
      match Step state event with
      | none => none
      | some next => Run next tail

theorem apply_event_preserves_claim_identity (state : LedgerState) (event : RevisionEvent) :
    (ApplyEvent state event).claimId = state.claimId := by
  unfold ApplyEvent
  split <;> rfl

theorem apply_event_preserves_external_effects (state : LedgerState) (event : RevisionEvent) :
    (ApplyEvent state event).externalEffects = state.externalEffects := by
  unfold ApplyEvent
  split <;> rfl

theorem accepted_step_preserves_claim_identity
    {state next : LedgerState} {event : RevisionEvent}
    (accepted : Step state event = some next) :
    next.claimId = state.claimId := by
  unfold Step at accepted
  split at accepted <;> try contradiction
  all_goals cases accepted; exact apply_event_preserves_claim_identity state event

theorem accepted_step_cannot_commit_external_effect
    {state next : LedgerState} {event : RevisionEvent}
    (accepted : Step state event = some next) :
    next.externalEffects = state.externalEffects := by
  unfold Step at accepted
  split at accepted <;> try contradiction
  all_goals cases accepted; exact apply_event_preserves_external_effects state event

theorem accepted_append_is_exactly_one_new_version
    {state next : LedgerState} {event : RevisionEvent}
    (appendEvent : event.kind = LifecycleEventKind.append)
    (accepted : Step state event = some next) :
    next.ledgerVersion = state.ledgerVersion + 1 /\
      next.appendCount = state.appendCount + 1 /\
        next.headDigest = event.eventDigest := by
  unfold Step at accepted
  split at accepted <;> try contradiction
  all_goals
    cases accepted
    simp [ApplyEvent, appendEvent]

def initialState : LedgerState where
  claimId := 101
  ledgerVersion := 7
  headDigest := 7001
  semanticVersion := 3
  ontologyVersion := 2
  supportRank := 1
  stage := .idle
  pendingEventDigest := none
  requiredSurfaceAcks := 0
  observedSurfaceAcks := 0
  materializedLedgerVersion := 7
  appendCount := 7
  externalEffects := 0

def referenceRevision : RevisionEvent where
  kind := .propose
  action := .requestPromotion
  eventDigest := 8001
  claimId := 101
  baseLedgerVersion := 7
  priorHeadDigest := 7001
  priorSemanticVersion := 3
  nextSemanticVersion := 4
  priorOntologyVersion := 2
  nextOntologyVersion := 3
  priorSupportRank := 1
  nextSupportRank := 2
  ledgerSelfApprovesSupport := false
  externalEffectRequested := false
  evidenceOwnerReceiptPresent := true
  openContradiction := false
  historyRefsPresent := true
  nonOverwriteAttestationPresent := true
  revisionReasonPresent := true
  residualRequired := false
  residualRefsPresent := true
  dependencyClosureComplete := true
  ontologyMigrationReceiptPresent := true
  surfacePlanComplete := true
  requiredSurfaceAcks := 3
  observedSurfaceAcks := 0
  surfaceAcknowledgmentReceiptPresent := false

def appendRevision : RevisionEvent := { referenceRevision with kind := .append }
def materializeRevision : RevisionEvent := { referenceRevision with kind := .materialize }
def acknowledgeRevision : RevisionEvent :=
  { referenceRevision with
    kind := .acknowledge
    observedSurfaceAcks := 3
    surfaceAcknowledgmentReceiptPresent := true }

theorem stale_base_is_rejected :
    RevisionRouteFor initialState { referenceRevision with baseLedgerVersion := 6 } =
      RevisionRoute.rejectStaleBase := by native_decide

theorem ledger_self_approval_is_rejected :
    RevisionRouteFor initialState { referenceRevision with ledgerSelfApprovesSupport := true } =
      RevisionRoute.rejectLedgerAuthorityLeak := by native_decide

theorem upward_revision_with_open_contradiction_is_blocked :
    RevisionRouteFor initialState { referenceRevision with openContradiction := true } =
      RevisionRoute.blockOpenContradiction := by native_decide

theorem upward_revision_without_owner_receipt_is_handed_off :
    RevisionRouteFor initialState { referenceRevision with evidenceOwnerReceiptPresent := false } =
      RevisionRoute.handoffToEvidenceOwner := by native_decide

theorem ontology_change_without_migration_receipt_is_rejected :
    RevisionRouteFor initialState { referenceRevision with ontologyMigrationReceiptPresent := false } =
      RevisionRoute.requestOntologyMigration := by native_decide

theorem full_revision_lifecycle_reaches_exact_acknowledgment :
    Run initialState [referenceRevision, appendRevision, materializeRevision, acknowledgeRevision] =
      some {
        claimId := 101
        ledgerVersion := 8
        headDigest := 8001
        semanticVersion := 4
        ontologyVersion := 3
        supportRank := 2
        stage := .acknowledged
        pendingEventDigest := none
        requiredSurfaceAcks := 3
        observedSurfaceAcks := 3
        materializedLedgerVersion := 8
        appendCount := 8
        externalEffects := 0 } := by native_decide

theorem acknowledgment_before_materialization_is_rejected :
    RevisionRouteFor initialState acknowledgeRevision = RevisionRoute.rejectWrongStage := by
  native_decide

end AsiStackProofs.ClaimLedgerRefinement
