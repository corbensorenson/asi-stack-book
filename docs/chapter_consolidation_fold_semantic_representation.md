# Chapter Consolidation Fold Disposition: Semantic Representation

Status: fold-disposition ready; human/external review not completed.

This is a review artifact for the governed consolidation sequence. It does not
edit `book_structure.json`, merge chapters, fold chapters, change Appendix C
support states, create source/proof/test evidence, approve reader artifacts, or
promote any claim above `argument`.

This disposition does not edit `book_structure.json`.

## Candidate

| Field | Value |
|---|---|
| Fold candidate | `semantic-representation-and-tree-structured-models` |
| Candidate title | Semantic Representation and Tree-Structured Models |
| Proposed destination | `compact-generative-systems-and-residual-honesty`, if the compression/representation package is executed or revised to accept the fold. |
| Destination title | Compact Generative Systems: Generate, Verify, Repair, and Residual Honesty |
| Dependency | Do not execute this fold before the compression/representation package has an execute, revise, defer, or reject decision. |
| Proposed fold section | Semantic Representation Leasing |
| Current state | `fold_disposition_ready` |
| Required decision | Execute fold after destination-package review, revise fold disposition, defer for release, or reject and retain standalone. |

## Rationale

The fold recommendation is not that semantic representation is unimportant. The
recommendation is that the current standalone chapter is mostly a
representation-leasing facet of the broader compression and residual-honesty
control plane. Its strongest artifact is the `Semantic Node Record`: a bounded
meaning object with provenance, hierarchy, relation refs, tokenization
contract, grounding state, version, supersession, residual uncertainty,
permitted uses, and evaluation refs. That record answers the same governance
question as the compression package: when may a smaller or more structured
representation carry work without hiding loss?

The semantic chapter should not be folded into VCM or semantic-page
certificates by default. VCM owns context addressing, certificates, mounts,
transactions, adequacy, and materialization receipts. Semantic representation
owns the optional representation substrate: graph nodes, path-derived semantic
tokens, semantic leases, hierarchy migration, and consumer-specific adequacy.
Those are closer to compression, representation admission, and residual
honesty than to the memory ABI.

Because the destination compression package is itself review-ready but not
executed, this fold disposition is dependency-bound. If review rejects the
compression merge, or keeps RankFold/NeuralFold standalone in a way that changes
the representation spine, this semantic disposition should be revised before
any manifest edit.

The dependency chain runs through
`compact-generative-systems-and-residual-honesty`,
`generate-verify-repair-compression`, and
`rankfold-neuralfold-and-artifact-compression`. The adjacent context and
certificate surfaces `virtual-context-abi` and
`semantic-pages-context-cells-and-certificates` remain important consumers, but
they are not the default destination for this fold.

## Preservation Ledger

| Preserved item | Destination treatment |
|---|---|
| TreeLLM semantic graph and path-token proposal | Preserve as a source-bounded representation proposal, not a reproduced model-size or reasoning-gain result. |
| Semantic leasing discipline | Keep as a named Semantic Representation Leasing section inside the compression/representation destination if the fold executes. |
| `Semantic Node Record` | Preserve as the representation-lease record beside compact-generative, compression-receipt, and compressed-artifact records. |
| Provenance, grounding, permitted use, residual uncertainty, and supersession | Preserve as required fields before a semantic node can carry task authority. |
| Consumer policies for VCM, Spinoza, planning, cognitive compilation, compression, and human explanation | Preserve as interface rules, not as evidence that all consumers work. |
| Hierarchy-update and graph-migration risks | Preserve as failure modes and restoration tests. |
| Circle/Coil optional representation substrates | Preserve only as optional-substrate guardrails with baselines and negative controls, not as model-quality evidence. |
| Information Bottleneck and LoRA comparators | Preserve as external vocabulary for relevance-preserving compression and low-rank adaptation, not as local representation adequacy evidence. |
| Semantic restoration condition | Restore standalone only after public-safe semantic-graph evidence creates chapter-owning evidence. |

## Proposed Destination Outline

If executed, the compression/representation destination should keep one chapter
skeleton. Do not paste the full semantic-representation chapter after the
compression chapter. The fold should add or revise these named pieces:

1. In `Why existing approaches are insufficient`, add the warning that a clean
   semantic graph can hide uncertainty as easily as a smaller tensor can hide
   residual work.
2. In `Mechanism`, add **Semantic Representation Leasing** as a subsection that
   treats graph nodes, semantic tokens, and typed meaning structures as scoped
   representations whose use depends on provenance, grounding, adequacy,
   interoperability, consumer policy, and supersession.
3. In `Interfaces`, preserve the `Semantic Node Record` as a companion record
   that can be consumed by VCM pages, Spinoza claim graphs, cognitive
   compilation atoms, compact-generation records, and human explanation
   surfaces only within declared permitted uses.
4. In `Invariants`, preserve the rules that grounded semantic nodes need
   provenance and hierarchy updates must preserve references or record
   supersession.
5. In `Failure modes`, keep false explainability, canonical graph capture,
   hierarchy drift, semantic laundering, stale consumer mappings, lossy
   fixed-size semantic tokens, and cyclic-substrate overclaim.
6. In `Minimum Viable Implementation`, keep
   `schemas/semantic_node_record.schema.json` and
   `tests/fixtures/protocol_records/semantic_node_record.valid.json` as
   record-shape fixtures only.
7. In `Beyond the State of the Art`, preserve semantic leasing as an endpoint:
   graph structure is task-scoped, provenance-bearing, supersession-aware, and
   consumer-policy bound before it can replace source context, proof objects,
   full artifacts, or human explanation.

## Source Union

If the fold executes after the compression/representation package is accepted,
the destination chapter's source queue should union the current compression and
semantic-representation sources:

- `cgs`
- `rgs`
- `bugbrain`
- `simulation_scaling`
- `rmi`
- `project_theseus_whitepaper`
- `bbvca_v9`
- `bbvca_main`
- `rankfold_neuralfold`
- `rankfold_compressor`
- `treellm`
- `spinoza`
- `verification_bandwidth`
- `cognitive_compilation`
- `circle_ai_architectures`
- `coilra_multicoil_rope`

`treellm` remains the central Corben-authored source for semantic graph and
path-token proposals, but it is still a whitepaper/specification here. It does
not supply a local TreeLLM implementation, measured compression ratio,
semantic-token benchmark, graph-grounding evaluation, or model-quality result.

If the compression review chooses the Conservative option and keeps
`rankfold-neuralfold-and-artifact-compression` standalone, this source union
must be revised before any semantic fold executes.

## External-Source Union

The destination should preserve the external comparators used by the
compression and semantic-representation chapters:

- `ext_deep_compression_2015`
- `ext_dreamcoder_2020`
- `ext_information_bottleneck_2000`
- `ext_knowledge_distillation_2015`
- `ext_mdl_tutorial_2004`
- `ext_codebleu_2020`
- `ext_gptq_2022`
- `ext_lora_2021`
- `ext_qlora_2023`

`ext_information_bottleneck_2000` positions semantic representation as
relevance-preserving compression rather than size-only compression.
`ext_lora_2021` positions low-rank structure as an external representation and
adaptation comparator. The compression comparators preserve pruning,
distillation, quantization, description-length, reusable-abstraction, and
artifact-quality vocabulary. None of these sources proves local TreeLLM,
semantic-node adequacy, graph grounding, model-quality improvement, or
deployment behavior.

## Appendix C Row Plan

If executed, `compact-generative-systems-and-residual-honesty.core` remains the
destination core claim, or the revised compression destination's accepted core
claim replaces it. The current semantic-representation core claim should become
a section-level subclaim inside the compression/representation destination:

> Semantic representations are task-scoped leases: graph nodes and semantic
> tokens may carry work only when provenance, grounding, utility,
> interoperability, permitted use, residual uncertainty, and supersession are
> explicit.

Support remains `argument`. The fold does not create source-derived,
prototype-backed, synthetic-test-backed, empirical-test-backed, mechanized, or
external-literature-backed support for the destination core claim.

No support-state movement is authorized by this disposition.

## Lean Module And Proof-Manifest Treatment

Preserve the compression package Lean modules and the semantic-representation
module. Semantic-specific proof tags:

- `AsiStackProofs.SemanticRepresentation`
- `lean:representation.semantic_tree.operational_invariant`
- `lean:representation.semantic_tree.failure_blocks_promotion`

If this fold executes, these tags should stay attached to the destination
chapter in `docs/book_outline.md` and the generated proof manifest. Do not
retire semantic-representation proof tags merely because the chapter is folded;
the grounded-provenance and hierarchy-supersession gates become more important
after folding.

The destination should also preserve the compression package proof tags already
listed in `docs/chapter_consolidation_dry_run_compression.md` and
`docs/chapter_consolidation_destination_draft_compression.md`.

## Schemas, Fixtures, And Harnesses

Preserve the semantic record shapes and interface fixtures:

- `schemas/semantic_node_record.schema.json`
- `schemas/semantic_atom.schema.json`
- `schemas/semantic_page_certificate.schema.json`
- `tests/fixtures/protocol_records/semantic_node_record.valid.json`
- `tests/fixtures/protocol_records/semantic_atom.valid.json`
- `tests/fixtures/protocol_records/semantic_page_certificate.valid.json`
- `python3 scripts/validate_schemas.py`
- `python3 scripts/validate_protocol_examples.py`

The semantic-node fixture remains a public record-shape validator only. It is
not a TreeLLM implementation, semantic-token benchmark, graph-grounding
evaluation, hierarchy-revision harness, cyclic-substrate experiment,
representation-utility benchmark, or support-state promotion.

## Reader Path And Handoff Repairs

If executed:

- The compression/representation destination's Human Reading Path should absorb
  semantic representation as the rule that a tidy meaning structure has to carry
  provenance, uncertainty, and permitted-use limits before it can replace fuller
  context.
- The folded semantic-representation chapter should not remain in the reader
  spine as a second full chapter skeleton.
- The predecessor Handoff before the folded chapter and the Handoff in the
  destination chapter must be repaired with
  `python3 scripts/chapter_adjacency_report.py --if-removing semantic-representation-and-tree-structured-models`
  and
  `python3 scripts/chapter_adjacency_report.py --chapter compact-generative-systems-and-residual-honesty`.
- If the compression package executes before this fold, rerun adjacency reports
  against the actual post-merge manifest before editing anything.
- Reader overlays, curated-reader records, companion-note routing, and review
  matrix rows that refer to the standalone semantic-representation chapter must
  either point to the new section or record a release deferral.

## URL, Redirect, And History Policy

Before any manifest edit, choose one public-history policy:

- keep `chapters/semantic-representation-and-tree-structured-models.qmd` as an
  archival source file excluded from the manifest with a clear historical note;
- add a public redirect or link note from the old chapter path to the
  compression/representation section; or
- defer the fold until the site has a durable folded-chapter URL policy.

Do not silently remove a public chapter path.

## Restoration Conditions

Semantic representation should be restored as a standalone chapter if one or
more of these public-safe artifacts becomes available and source-reviewed:

- a TreeLLM or semantic-graph prototype with command, environment, fixtures,
  baseline, negative control, and result-boundary records;
- a grounded-node evaluation on a bounded source domain;
- a hierarchy-revision harness that proves downstream consumers notice
  supersession, stale nodes, and provenance loss;
- a representation-utility benchmark comparing semantic-node use against
  plain-text, neural-only, retrieval-only, or full-context baselines;
- a graph-interoperability trace across VCM, Spinoza, cognitive compilation,
  compression, and human explanation surfaces;
- cyclic-substrate experiments with ordinary baselines, wrong-period controls,
  scalar controls, and negative results;
- independent external literature review finding that semantic representation
  owns a distinct evidence lane not representable inside the compression
  package;
- external review finding that semantic representation is central enough to the
  ASI Stack that burying it as a representation section weakens the book.

## Review Decision Surface

Reviewers should choose one:

- **Execute fold after destination review:** Semantic Representation and
  Tree-Structured Models becomes a named Semantic Representation Leasing section
  inside the accepted compression/representation destination, while all source,
  proof, schema, reader, and restoration boundaries are preserved.
- **Revise fold disposition:** Keep the candidate unexecuted and revise the
  destination, dependency, subclaim, source, proof, reader, or restoration
  treatment.
- **Defer for release:** Keep both chapters unchanged for the current release
  and pause curated-reader graduation for the standalone chapter until the
  consolidation decision is made.
- **Reject and retain standalone:** Keep Semantic Representation and
  Tree-Structured Models as a standalone chapter because review finds distinct
  artifact, proof, evidence, or reader ownership.

## Non-Claims

- This disposition does not merge or fold chapters.
- This disposition does not change `book_structure.json`.
- This disposition does not change Appendix C support states.
- This disposition does not create source-derived, external-literature-backed,
  proof-derived, prototype-backed, synthetic-test-backed, or empirical support.
- This disposition does not approve reader, ebook, PDF, DOCX, audio, DOI,
  archive, or release artifacts.
- This disposition does not prove semantic graph adequacy, TreeLLM behavior,
  grounding quality, hierarchy migration, cyclic-substrate advantage,
  representation utility, model-quality improvement, or deployment behavior.
