namespace AsiStackProofs.ClaimLedger

structure ClaimUpdate where
  priorEvidenceRefsPresent : Bool
  priorHistoryRefsPresent : Bool
  nextCarriesPriorEvidence : Bool
  nextCarriesPriorHistory : Bool
deriving DecidableEq, Repr

def ClaimUpdatePreservesPrior (update : ClaimUpdate) : Prop :=
  (update.priorEvidenceRefsPresent = true ->
    update.nextCarriesPriorEvidence = true) ∧
    (update.priorHistoryRefsPresent = true ->
      update.nextCarriesPriorHistory = true)

theorem claim_update_preserves_prior_evidence_and_revision_history
    {update : ClaimUpdate} :
    ClaimUpdatePreservesPrior update ->
    update.priorEvidenceRefsPresent = true ->
    update.priorHistoryRefsPresent = true ->
    update.nextCarriesPriorEvidence = true ∧
      update.nextCarriesPriorHistory = true := by
  intro preserves evidencePresent historyPresent
  exact And.intro
    (preserves.1 evidencePresent)
    (preserves.2 historyPresent)

inductive ContradictionState where
  | none
  | open
  | resolved
  | bounded
  | residual
deriving DecidableEq, Repr

def ContradictionHandled : ContradictionState -> Prop
  | .none => True
  | .open => False
  | .resolved => True
  | .bounded => True
  | .residual => True

structure PromotionReview where
  evidenceReady : Bool
  contradictionState : ContradictionState
deriving DecidableEq, Repr

def PromotionAllowed (review : PromotionReview) : Prop :=
  review.evidenceReady = true ∧
    ContradictionHandled review.contradictionState

theorem open_contradiction_blocks_claim_promotion
    {review : PromotionReview} :
    review.contradictionState = ContradictionState.open ->
    ¬ PromotionAllowed review := by
  intro openContradiction promoted
  unfold PromotionAllowed at promoted
  rw [openContradiction] at promoted
  exact promoted.2

inductive LedgerEffect where
  | noChange
  | promoted
  | downgraded
  | split
  | merged
  | deprecated
  | retired
  | blocked
deriving DecidableEq, Repr

structure BeliefRevisionRecord where
  claimIdentityPresent : Bool
  priorSupportStateRecorded : Bool
  newSupportStateRecorded : Bool
  evidenceRefsPresent : Bool
  revisionReasonPresent : Bool
  historyRefsPresent : Bool
  contradictionState : ContradictionState
  promotionAccepted : Bool
  supportStateIncreased : Bool
  ledgerEffect : LedgerEffect
  nonClaimBoundaryPresent : Bool
deriving DecidableEq, Repr

def BeliefRevisionRecordValid (record : BeliefRevisionRecord) : Prop :=
  record.claimIdentityPresent = true ∧
    record.priorSupportStateRecorded = true ∧
      record.newSupportStateRecorded = true ∧
        record.revisionReasonPresent = true ∧
          record.historyRefsPresent = true ∧
            record.nonClaimBoundaryPresent = true ∧
              (record.promotionAccepted = true ->
                record.evidenceRefsPresent = true ∧
                  ContradictionHandled record.contradictionState ∧
                    record.supportStateIncreased = true) ∧
                (record.contradictionState = ContradictionState.open ->
                  record.promotionAccepted = false ∧
                    record.ledgerEffect = LedgerEffect.blocked)

theorem valid_belief_revision_record_preserves_identity_history_and_boundary
    {record : BeliefRevisionRecord} :
    BeliefRevisionRecordValid record ->
    record.claimIdentityPresent = true ∧
      record.priorSupportStateRecorded = true ∧
        record.newSupportStateRecorded = true ∧
          record.revisionReasonPresent = true ∧
            record.historyRefsPresent = true ∧
              record.nonClaimBoundaryPresent = true := by
  intro valid
  exact And.intro valid.1
    (And.intro valid.2.1
      (And.intro valid.2.2.1
        (And.intro valid.2.2.2.1
          (And.intro valid.2.2.2.2.1 valid.2.2.2.2.2.1))))

theorem accepted_belief_revision_promotion_requires_evidence_handled_contradiction_and_increase
    {record : BeliefRevisionRecord} :
    BeliefRevisionRecordValid record ->
    record.promotionAccepted = true ->
    record.evidenceRefsPresent = true ∧
      ContradictionHandled record.contradictionState ∧
        record.supportStateIncreased = true := by
  intro valid promoted
  exact valid.2.2.2.2.2.2.1 promoted

theorem open_contradiction_blocks_belief_revision_promotion
    {record : BeliefRevisionRecord} :
    BeliefRevisionRecordValid record ->
    record.contradictionState = ContradictionState.open ->
    record.promotionAccepted = false ∧
      record.ledgerEffect = LedgerEffect.blocked := by
  intro valid openContradiction
  exact valid.2.2.2.2.2.2.2 openContradiction

end AsiStackProofs.ClaimLedger
