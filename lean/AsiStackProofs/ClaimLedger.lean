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

end AsiStackProofs.ClaimLedger
