namespace AsiStackProofs.GovernedRepositoryTrace

structure AuthorityHandoff where
  parentCeiling : Nat
  childCeiling : Nat
  requestedAuthority : Nat
deriving DecidableEq, Repr

def AuthorityMonotone (trace : List AuthorityHandoff) : Bool :=
  trace.all (fun handoff =>
    decide (handoff.childCeiling ≤ handoff.parentCeiling) &&
      decide (handoff.requestedAuthority ≤ handoff.childCeiling))

def governedAuthorityTrace : List AuthorityHandoff :=
  [ { parentCeiling := 2, childCeiling := 2, requestedAuthority := 1 },
    { parentCeiling := 2, childCeiling := 1, requestedAuthority := 1 },
    { parentCeiling := 2, childCeiling := 1, requestedAuthority := 1 } ]

def widenedAuthorityNegative : List AuthorityHandoff :=
  [ { parentCeiling := 2, childCeiling := 1, requestedAuthority := 3 } ]

theorem governed_fixture_authority_monotone :
    AuthorityMonotone governedAuthorityTrace = true := by
  decide

theorem authority_widening_negative_rejected :
    AuthorityMonotone widenedAuthorityNegative = false := by
  decide

structure TimedEffectAttempt where
  logicalTime : Nat
  revocationTime : Nat
  effectAllowed : Bool
  effectObserved : Bool
deriving DecidableEq, Repr

def RevocationBeforeEffect (trace : List TimedEffectAttempt) : Bool :=
  trace.all (fun attempt =>
    if decide (attempt.revocationTime ≤ attempt.logicalTime) then
      (attempt.effectAllowed == false) && (attempt.effectObserved == false)
    else true)

def governedEffectTrace : List TimedEffectAttempt :=
  [ { logicalTime := 3, revocationTime := 99,
      effectAllowed := true, effectObserved := true },
    { logicalTime := 5, revocationTime := 5,
      effectAllowed := false, effectObserved := false },
    { logicalTime := 7, revocationTime := 4,
      effectAllowed := false, effectObserved := false } ]

def revocationRaceNegative : List TimedEffectAttempt :=
  [ { logicalTime := 5, revocationTime := 5,
      effectAllowed := true, effectObserved := true } ]

theorem governed_fixture_revocation_before_effect :
    RevocationBeforeEffect governedEffectTrace = true := by
  decide

theorem effect_at_revocation_time_negative_rejected :
    RevocationBeforeEffect revocationRaceNegative = false := by
  decide

structure EvidenceEvent where
  supportBefore : Nat
  supportAfter : Nat
  transitionCreated : Bool
  acceptedReview : Bool
  artifactDigestMatches : Bool
  independentEffectObservation : Bool
  supportStateEffectNone : Bool
deriving DecidableEq, Repr

def EvidenceEventIntegrity (event : EvidenceEvent) : Bool :=
  if event.transitionCreated then
    decide (event.supportBefore ≠ event.supportAfter) &&
      event.acceptedReview &&
      event.artifactDigestMatches &&
      event.independentEffectObservation
  else
    decide (event.supportBefore = event.supportAfter) &&
      event.supportStateEffectNone

def EvidenceTraceIntegrity (trace : List EvidenceEvent) : Bool :=
  trace.all EvidenceEventIntegrity

def noChangeEvidenceEvent : EvidenceEvent where
  supportBefore := 1
  supportAfter := 1
  transitionCreated := false
  acceptedReview := false
  artifactDigestMatches := true
  independentEffectObservation := true
  supportStateEffectNone := true

def governedEvidenceTrace : List EvidenceEvent :=
  [ noChangeEvidenceEvent, noChangeEvidenceEvent, noChangeEvidenceEvent,
    noChangeEvidenceEvent, noChangeEvidenceEvent, noChangeEvidenceEvent,
    noChangeEvidenceEvent, noChangeEvidenceEvent, noChangeEvidenceEvent ]

def unrecordedPromotionNegative : List EvidenceEvent :=
  [ { noChangeEvidenceEvent with supportAfter := 4 } ]

theorem governed_fixture_evidence_integrity :
    EvidenceTraceIntegrity governedEvidenceTrace = true := by
  decide

theorem unrecorded_promotion_negative_rejected :
    EvidenceTraceIntegrity unrecordedPromotionNegative = false := by
  decide

structure ResidualDelta where
  created : Nat
  discovered : Nat
  discharged : Nat
deriving DecidableEq, Repr

def ResidualsCreated (trace : List ResidualDelta) : Nat :=
  (trace.map (fun delta => delta.created)).sum

def ResidualsDiscovered (trace : List ResidualDelta) : Nat :=
  (trace.map (fun delta => delta.discovered)).sum

def ResidualsDischarged (trace : List ResidualDelta) : Nat :=
  (trace.map (fun delta => delta.discharged)).sum

def ResidualConserved (trace : List ResidualDelta) (finalOpen : Nat) : Bool :=
  decide (ResidualsCreated trace = ResidualsDischarged trace + finalOpen) &&
    decide (ResidualsDiscovered trace = ResidualsCreated trace)

def governedResidualTrace : List ResidualDelta :=
  [ { created := 1, discovered := 1, discharged := 1 },
    { created := 1, discovered := 1, discharged := 0 } ]

theorem governed_fixture_residual_conserved :
    ResidualConserved governedResidualTrace 1 = true := by
  decide

theorem erased_open_residual_negative_rejected :
    ResidualConserved governedResidualTrace 0 = false := by
  decide

def GovernedRepositoryTraceValid : Prop :=
  AuthorityMonotone governedAuthorityTrace = true ∧
    RevocationBeforeEffect governedEffectTrace = true ∧
    EvidenceTraceIntegrity governedEvidenceTrace = true ∧
    ResidualConserved governedResidualTrace 1 = true

theorem governed_repository_trace_four_invariants :
    GovernedRepositoryTraceValid := by
  exact ⟨governed_fixture_authority_monotone,
    governed_fixture_revocation_before_effect,
    governed_fixture_evidence_integrity,
    governed_fixture_residual_conserved⟩

end AsiStackProofs.GovernedRepositoryTrace
