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

inductive ClaimLedgerRevisionRoute where
  | rejectMissingClaimIdentity
  | requestSupportStateRecord
  | requestEvidenceTransition
  | blockOpenContradictionPromotion
  | requestContradictionHandling
  | preserveRevisionHistory
  | preserveNonOverwriteAttestation
  | requestSurfaceSynchronization
  | preserveSplitHistory
  | requestDowngradeReason
  | requestResidualRecord
  | preserveNonClaimBoundary
  | acceptLedgerRevision
deriving DecidableEq, Repr

structure ClaimLedgerRevisionReview where
  revisionRequested : Bool
  claimIdentityPresent : Bool
  priorSupportStateRecorded : Bool
  newSupportStateRecorded : Bool
  promotionRequested : Bool
  evidenceTransitionPresent : Bool
  evidenceRefsPresent : Bool
  supportStateIncreased : Bool
  contradictionState : ContradictionState
  historyRefsPresent : Bool
  nonOverwriteAttestationPresent : Bool
  changedSurfaceRefsComplete : Bool
  splitRequested : Bool
  childClaimsCarryHistory : Bool
  downgradeRequested : Bool
  downgradeReasonPresent : Bool
  residualRequired : Bool
  residualRefsPresent : Bool
  nonClaimBoundaryPresent : Bool
deriving DecidableEq, Repr

def ClaimLedgerRevisionRouteFor
    (review : ClaimLedgerRevisionReview) :
    ClaimLedgerRevisionRoute :=
  if review.revisionRequested = false then
    ClaimLedgerRevisionRoute.acceptLedgerRevision
  else if review.claimIdentityPresent = false then
    ClaimLedgerRevisionRoute.rejectMissingClaimIdentity
  else if
      review.priorSupportStateRecorded = false ||
        review.newSupportStateRecorded = false then
    ClaimLedgerRevisionRoute.requestSupportStateRecord
  else if
      review.promotionRequested = true &&
        (review.evidenceTransitionPresent = false ||
          review.evidenceRefsPresent = false ||
          review.supportStateIncreased = false) then
    ClaimLedgerRevisionRoute.requestEvidenceTransition
  else if
      review.promotionRequested = true &&
        review.contradictionState = ContradictionState.open then
    ClaimLedgerRevisionRoute.blockOpenContradictionPromotion
  else if review.contradictionState = ContradictionState.open then
    ClaimLedgerRevisionRoute.requestContradictionHandling
  else if review.historyRefsPresent = false then
    ClaimLedgerRevisionRoute.preserveRevisionHistory
  else if review.nonOverwriteAttestationPresent = false then
    ClaimLedgerRevisionRoute.preserveNonOverwriteAttestation
  else if review.changedSurfaceRefsComplete = false then
    ClaimLedgerRevisionRoute.requestSurfaceSynchronization
  else if
      review.splitRequested = true &&
        review.childClaimsCarryHistory = false then
    ClaimLedgerRevisionRoute.preserveSplitHistory
  else if
      review.downgradeRequested = true &&
        review.downgradeReasonPresent = false then
    ClaimLedgerRevisionRoute.requestDowngradeReason
  else if
      review.residualRequired = true &&
        review.residualRefsPresent = false then
    ClaimLedgerRevisionRoute.requestResidualRecord
  else if review.nonClaimBoundaryPresent = false then
    ClaimLedgerRevisionRoute.preserveNonClaimBoundary
  else
    ClaimLedgerRevisionRoute.acceptLedgerRevision

def completeClaimLedgerRevisionReview : ClaimLedgerRevisionReview where
  revisionRequested := true
  claimIdentityPresent := true
  priorSupportStateRecorded := true
  newSupportStateRecorded := true
  promotionRequested := false
  evidenceTransitionPresent := true
  evidenceRefsPresent := true
  supportStateIncreased := false
  contradictionState := ContradictionState.none
  historyRefsPresent := true
  nonOverwriteAttestationPresent := true
  changedSurfaceRefsComplete := true
  splitRequested := false
  childClaimsCarryHistory := true
  downgradeRequested := false
  downgradeReasonPresent := true
  residualRequired := false
  residualRefsPresent := true
  nonClaimBoundaryPresent := true

theorem revision_request_missing_claim_identity_rejected :
    ClaimLedgerRevisionRouteFor
        { completeClaimLedgerRevisionReview with
          claimIdentityPresent := false } =
      ClaimLedgerRevisionRoute.rejectMissingClaimIdentity := by
  simp [ClaimLedgerRevisionRouteFor, completeClaimLedgerRevisionReview]

theorem missing_support_state_record_requests_support_state_record :
    ClaimLedgerRevisionRouteFor
        { completeClaimLedgerRevisionReview with
          newSupportStateRecorded := false } =
      ClaimLedgerRevisionRoute.requestSupportStateRecord := by
  simp [ClaimLedgerRevisionRouteFor, completeClaimLedgerRevisionReview]

theorem promotion_without_evidence_transition_requests_evidence_transition :
    ClaimLedgerRevisionRouteFor
        { completeClaimLedgerRevisionReview with
          promotionRequested := true
          evidenceTransitionPresent := false
          supportStateIncreased := true } =
      ClaimLedgerRevisionRoute.requestEvidenceTransition := by
  simp [ClaimLedgerRevisionRouteFor, completeClaimLedgerRevisionReview]

theorem promotion_without_evidence_refs_requests_evidence_transition :
    ClaimLedgerRevisionRouteFor
        { completeClaimLedgerRevisionReview with
          promotionRequested := true
          evidenceRefsPresent := false
          supportStateIncreased := true } =
      ClaimLedgerRevisionRoute.requestEvidenceTransition := by
  simp [ClaimLedgerRevisionRouteFor, completeClaimLedgerRevisionReview]

theorem open_contradiction_promotion_is_blocked :
    ClaimLedgerRevisionRouteFor
        { completeClaimLedgerRevisionReview with
          promotionRequested := true
          supportStateIncreased := true
          contradictionState := ContradictionState.open } =
      ClaimLedgerRevisionRoute.blockOpenContradictionPromotion := by
  simp [ClaimLedgerRevisionRouteFor, completeClaimLedgerRevisionReview]

theorem open_contradiction_without_promotion_requests_handling :
    ClaimLedgerRevisionRouteFor
        { completeClaimLedgerRevisionReview with
          contradictionState := ContradictionState.open } =
      ClaimLedgerRevisionRoute.requestContradictionHandling := by
  simp [ClaimLedgerRevisionRouteFor, completeClaimLedgerRevisionReview]

theorem revision_without_history_refs_preserves_history :
    ClaimLedgerRevisionRouteFor
        { completeClaimLedgerRevisionReview with
          historyRefsPresent := false } =
      ClaimLedgerRevisionRoute.preserveRevisionHistory := by
  simp [ClaimLedgerRevisionRouteFor, completeClaimLedgerRevisionReview]

theorem revision_without_non_overwrite_attestation_preserves_attestation :
    ClaimLedgerRevisionRouteFor
        { completeClaimLedgerRevisionReview with
          nonOverwriteAttestationPresent := false } =
      ClaimLedgerRevisionRoute.preserveNonOverwriteAttestation := by
  simp [ClaimLedgerRevisionRouteFor, completeClaimLedgerRevisionReview]

theorem incomplete_surface_sync_requests_synchronization :
    ClaimLedgerRevisionRouteFor
        { completeClaimLedgerRevisionReview with
          changedSurfaceRefsComplete := false } =
      ClaimLedgerRevisionRoute.requestSurfaceSynchronization := by
  simp [ClaimLedgerRevisionRouteFor, completeClaimLedgerRevisionReview]

theorem split_without_child_history_preserves_split_history :
    ClaimLedgerRevisionRouteFor
        { completeClaimLedgerRevisionReview with
          splitRequested := true
          childClaimsCarryHistory := false } =
      ClaimLedgerRevisionRoute.preserveSplitHistory := by
  simp [ClaimLedgerRevisionRouteFor, completeClaimLedgerRevisionReview]

theorem downgrade_without_reason_requests_downgrade_reason :
    ClaimLedgerRevisionRouteFor
        { completeClaimLedgerRevisionReview with
          downgradeRequested := true
          downgradeReasonPresent := false } =
      ClaimLedgerRevisionRoute.requestDowngradeReason := by
  simp [ClaimLedgerRevisionRouteFor, completeClaimLedgerRevisionReview]

theorem required_residual_without_refs_requests_residual_record :
    ClaimLedgerRevisionRouteFor
        { completeClaimLedgerRevisionReview with
          residualRequired := true
          residualRefsPresent := false } =
      ClaimLedgerRevisionRoute.requestResidualRecord := by
  simp [ClaimLedgerRevisionRouteFor, completeClaimLedgerRevisionReview]

theorem revision_without_non_claim_boundary_preserves_boundary :
    ClaimLedgerRevisionRouteFor
        { completeClaimLedgerRevisionReview with
          nonClaimBoundaryPresent := false } =
      ClaimLedgerRevisionRoute.preserveNonClaimBoundary := by
  simp [ClaimLedgerRevisionRouteFor, completeClaimLedgerRevisionReview]

theorem complete_claim_ledger_revision_accepts :
    ClaimLedgerRevisionRouteFor completeClaimLedgerRevisionReview =
      ClaimLedgerRevisionRoute.acceptLedgerRevision := by
  simp [ClaimLedgerRevisionRouteFor, completeClaimLedgerRevisionReview]

end AsiStackProofs.ClaimLedger
