namespace AsiStackProofs.WhiteBoxEvidence

/-!
A finite admission and governance-routing model for model-internal evidence.
The Boolean fields are declared records, not scientific truth. The model can
constrain how a packet is consumed; it cannot establish that a feature, label,
circuit, intervention, evaluator, or coverage estimate is faithful.
-/

inductive InternalEvidenceState where
  | observational
  | predictive
  | causalBounded
  | unsupported
deriving DecidableEq, Repr

inductive RequestedAuthority where
  | preserve
  | restrict
  | widen
deriving DecidableEq, Repr

inductive GovernanceRoute where
  | reject
  | expire
  | preserve
  | restrict
  | escalate
  | grantWidening
deriving DecidableEq, Repr

structure InternalEvidencePacket where
  exactIdentity : Bool
  lineageFresh : Bool
  methodAssumptionsPresent : Bool
  negativeControlsPassed : Bool
  behavioralCrossCheck : Bool
  causalInterventionPassed : Bool
  separateEvaluator : Bool
  stabilityRecorded : Bool
  coverageResidualRecorded : Bool
  sideEffectsResolved : Bool
  materialChangeObserved : Bool
  releaseRequested : Bool
  evidenceState : InternalEvidenceState
  requestedAuthority : RequestedAuthority
deriving DecidableEq, Repr

def ScientificallyAdmissible (packet : InternalEvidencePacket) : Bool :=
  packet.exactIdentity &&
  packet.lineageFresh &&
  packet.methodAssumptionsPresent &&
  packet.negativeControlsPassed &&
  packet.stabilityRecorded &&
  packet.coverageResidualRecorded &&
  match packet.evidenceState with
  | .observational => true
  | .predictive => packet.behavioralCrossCheck
  | .causalBounded =>
      packet.behavioralCrossCheck &&
      packet.causalInterventionPassed &&
      packet.separateEvaluator
  | .unsupported => false

def WhiteBoxRouteFor (packet : InternalEvidencePacket) : GovernanceRoute :=
  if ScientificallyAdmissible packet = false then
    .reject
  else if packet.materialChangeObserved = true then
    .expire
  else if packet.requestedAuthority = .widen ∨ packet.releaseRequested = true then
    .escalate
  else if packet.sideEffectsResolved = false then
    .restrict
  else
    match packet.requestedAuthority with
    | .preserve => .preserve
    | .restrict => .restrict
    | .widen => .escalate

theorem evidence_never_grants_authority
    (packet : InternalEvidencePacket) :
    WhiteBoxRouteFor packet ≠ GovernanceRoute.grantWidening := by
  unfold WhiteBoxRouteFor
  split <;> simp_all
  split <;> simp_all
  split <;> simp_all
  split <;> simp_all
  cases packet.requestedAuthority <;> simp

theorem invalid_packet_rejected
    (packet : InternalEvidencePacket)
    (invalid :
      packet.exactIdentity = false ∨
      packet.lineageFresh = false ∨
      packet.methodAssumptionsPresent = false ∨
      packet.negativeControlsPassed = false ∨
      packet.stabilityRecorded = false ∨
      packet.coverageResidualRecorded = false ∨
      packet.evidenceState = .unsupported) :
    WhiteBoxRouteFor packet = .reject := by
  unfold WhiteBoxRouteFor
  have inadmissible : ScientificallyAdmissible packet = false := by
    rcases invalid with exactIdentity | lineage | assumptions | controls |
      stability | residual | unsupported
    · simp [ScientificallyAdmissible, exactIdentity]
    · simp [ScientificallyAdmissible, lineage]
    · simp [ScientificallyAdmissible, assumptions]
    · simp [ScientificallyAdmissible, controls]
    · simp [ScientificallyAdmissible, stability]
    · simp [ScientificallyAdmissible, residual]
    · simp [ScientificallyAdmissible, unsupported]
  simp [inadmissible]

theorem admitted_causal_packet_records_crosscheck_intervention_and_evaluator
    (packet : InternalEvidencePacket)
    (causal : packet.evidenceState = .causalBounded)
    (admitted : ScientificallyAdmissible packet = true) :
    packet.behavioralCrossCheck = true ∧
      packet.causalInterventionPassed = true ∧
      packet.separateEvaluator = true := by
  simp [ScientificallyAdmissible, causal] at admitted
  exact ⟨admitted.2.1.1, admitted.2.1.2, admitted.2.2⟩

theorem material_change_expires_admissible_packet
    (packet : InternalEvidencePacket)
    (admitted : ScientificallyAdmissible packet = true)
    (changed : packet.materialChangeObserved = true) :
    WhiteBoxRouteFor packet = .expire := by
  simp [WhiteBoxRouteFor, admitted, changed]

def boundedCausalPacket : InternalEvidencePacket where
  exactIdentity := true
  lineageFresh := true
  methodAssumptionsPresent := true
  negativeControlsPassed := true
  behavioralCrossCheck := true
  causalInterventionPassed := true
  separateEvaluator := true
  stabilityRecorded := true
  coverageResidualRecorded := true
  sideEffectsResolved := true
  materialChangeObserved := false
  releaseRequested := false
  evidenceState := .causalBounded
  requestedAuthority := .preserve

def stalePacket : InternalEvidencePacket :=
  { boundedCausalPacket with lineageFresh := false }

def authorityWideningPacket : InternalEvidencePacket :=
  { boundedCausalPacket with requestedAuthority := .widen }

def changedPacket : InternalEvidencePacket :=
  { boundedCausalPacket with materialChangeObserved := true }

theorem bounded_causal_fixture_preserves_authority :
    WhiteBoxRouteFor boundedCausalPacket = .preserve := by native_decide

theorem stale_fixture_is_rejected :
    WhiteBoxRouteFor stalePacket = .reject := by native_decide

theorem widening_fixture_escalates_without_grant :
    WhiteBoxRouteFor authorityWideningPacket = .escalate := by native_decide

theorem changed_fixture_expires :
    WhiteBoxRouteFor changedPacket = .expire := by native_decide

end AsiStackProofs.WhiteBoxEvidence
