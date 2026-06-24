namespace AsiStackProofs.ContextCertificates

inductive AuthorityLevel where
  | publicUse
  | draftingUse
  | citationUse
  | executionUse
  | restrictedUse
deriving DecidableEq, Repr

def AuthorityLevel.rank : AuthorityLevel -> Nat
  | .publicUse => 0
  | .draftingUse => 1
  | .citationUse => 2
  | .executionUse => 3
  | .restrictedUse => 4

structure ContextCellCertificate where
  derived : Bool
  sourceBindingsDeclared : Bool
  lossContractDeclared : Bool
  permittedUsesDeclared : Bool
  authorityCeiling : AuthorityLevel
deriving DecidableEq, Repr

def CertificateComplete (certificate : ContextCellCertificate) : Prop :=
  certificate.sourceBindingsDeclared = true ∧
    certificate.lossContractDeclared = true ∧
    certificate.permittedUsesDeclared = true

def DerivedCellValid (certificate : ContextCellCertificate) : Prop :=
  certificate.derived = true ->
    CertificateComplete certificate

theorem derived_context_cell_carries_bindings_and_loss_use_contracts
    {certificate : ContextCellCertificate} :
    DerivedCellValid certificate ->
    certificate.derived = true ->
    certificate.sourceBindingsDeclared = true ∧
      certificate.lossContractDeclared = true ∧
      certificate.permittedUsesDeclared = true := by
  intro valid derived
  exact valid derived

structure SourceCell where
  authorityCeiling : AuthorityLevel
deriving DecidableEq, Repr

structure SummaryCell where
  authorityCeiling : AuthorityLevel
deriving DecidableEq, Repr

def SummaryRespectsSourceAuthority
    (summary : SummaryCell) (sources : List SourceCell) : Prop :=
  ∀ source, source ∈ sources ->
    summary.authorityCeiling.rank <= source.authorityCeiling.rank

def AuthorityEscalates
    (summary : SummaryCell) (source : SourceCell) : Prop :=
  source.authorityCeiling.rank < summary.authorityCeiling.rank

theorem summary_authority_cannot_exceed_source_ceiling
    {summary : SummaryCell} {sources : List SourceCell} {source : SourceCell} :
    SummaryRespectsSourceAuthority summary sources ->
    source ∈ sources ->
    summary.authorityCeiling.rank <= source.authorityCeiling.rank := by
  intro respects member
  exact respects source member

theorem authority_preservation_rejects_escalating_summary
    {summary : SummaryCell} {sources : List SourceCell} {source : SourceCell} :
    SummaryRespectsSourceAuthority summary sources ->
    source ∈ sources ->
    ¬ AuthorityEscalates summary source := by
  intro respects member escalates
  unfold AuthorityEscalates at escalates
  have bounded :
      summary.authorityCeiling.rank <= source.authorityCeiling.rank :=
    respects source member
  exact (Nat.not_lt_of_ge bounded) escalates

end AsiStackProofs.ContextCertificates
