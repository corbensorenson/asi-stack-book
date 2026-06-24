namespace AsiStackProofs.ProofCarryingContracts

structure ProofContractReceipt where
  theoremRefsPresent : Bool
  deterministicFieldsPresent : Bool
  nonClaimBoundaryPresent : Bool
deriving DecidableEq, Repr

def ReceiptBoundaryComplete (receipt : ProofContractReceipt) : Prop :=
  receipt.theoremRefsPresent = true ∧
    receipt.deterministicFieldsPresent = true ∧
      receipt.nonClaimBoundaryPresent = true

def ReadyForDownstreamUse (receipt : ProofContractReceipt) : Prop :=
  ReceiptBoundaryComplete receipt

theorem downstream_ready_receipt_exposes_boundary_fields
    {receipt : ProofContractReceipt} :
    ReadyForDownstreamUse receipt ->
      receipt.theoremRefsPresent = true ∧
        receipt.deterministicFieldsPresent = true ∧
          receipt.nonClaimBoundaryPresent = true := by
  intro ready
  exact ready

structure DownstreamPromotionReview where
  contractReady : Bool
  workloadPresent : Bool
  baselinePresent : Bool
  metricPresent : Bool
  evidenceArtifactPresent : Bool
  promoted : Bool
deriving DecidableEq, Repr

def PromotionEvidenceComplete (review : DownstreamPromotionReview) : Prop :=
  review.workloadPresent = true ∧
    review.baselinePresent = true ∧
      review.metricPresent = true ∧
        review.evidenceArtifactPresent = true

def ConsumerGateValid (review : DownstreamPromotionReview) : Prop :=
  review.promoted = true ->
    review.contractReady = true ∧ PromotionEvidenceComplete review

theorem contract_readiness_alone_cannot_promote_downstream_claim
    {review : DownstreamPromotionReview} :
    ConsumerGateValid review ->
    review.contractReady = true ->
    (review.workloadPresent = false ∨
      review.baselinePresent = false ∨
        review.metricPresent = false ∨
          review.evidenceArtifactPresent = false) ->
    review.promoted = false := by
  intro valid _ready missing
  cases promoted : review.promoted with
  | false => rfl
  | true =>
      have complete := (valid promoted).2
      unfold PromotionEvidenceComplete at complete
      cases missing with
      | inl noWorkload =>
          rw [noWorkload] at complete
          cases complete.1
      | inr rest =>
          cases rest with
          | inl noBaseline =>
              rw [noBaseline] at complete
              cases complete.2.1
          | inr rest =>
              cases rest with
              | inl noMetric =>
                  rw [noMetric] at complete
                  cases complete.2.2.1
              | inr noEvidence =>
                  rw [noEvidence] at complete
                  cases complete.2.2.2

end AsiStackProofs.ProofCarryingContracts
