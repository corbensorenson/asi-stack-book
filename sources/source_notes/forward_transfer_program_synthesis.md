# Source Note: From Compression to Forward Transfer

| Field | Value |
|---|---|
| Source ID | `forward_transfer_program_synthesis` |
| Source title | *From Compression to Forward Transfer: Evaluating Reusable Knowledge in Program Synthesis* |
| Author / date | Corben Sorenson; August 2026 |
| Ingestion date | 2026-08-14 |
| Canonical local text | `sources/raw/corben_papers/forward_transfer_program_synthesis/from_compression_to_forward_transfer.md`; SHA-256 `70c4e62eedad4883db9cc8a8740c71176b25f8a95ce61742fc559b9c9ab9e447`; 101,853 bytes |
| Supplied presentation copy | `sources/raw/corben_papers/forward_transfer_program_synthesis/from_compression_to_forward_transfer.docx`; SHA-256 `fb4840af26a764a5861e1ad826b14269510a9af9e66ab864c27d6c2abc0d26a4`; 89,004 bytes |
| Supplied bibliography | `sources/raw/corben_papers/forward_transfer_program_synthesis/from_compression_to_forward_transfer_references.bib`; SHA-256 `2a3f2eea0d9ec521cc6ba8b2d3e1f66a38bd1990582c88ec74d1a6947716cdff`; 10,607 bytes; 31 entries |
| Storage boundary | The complete supplied bundle is retained in the ignored local Corben-paper archive. The exact Markdown is copied into the tracked public paper library under the standing author-publication boundary. |
| Evidence boundary | The manuscript supplies definitions, finite counterexamples, experimental protocols, and a reporting schema. It reports no executed benchmark, measured forward-transfer effect, resource advantage, independent reproduction, or support transition. |

## Thesis

Reusable knowledge should be evaluated by what it changes on future work, not
only by how compactly it describes past work. The paper proposes a **verified
forward-transfer intervention**: freeze a task distribution, knowledge state,
search procedure, verifier, and budget; then compare future synthesis outcomes
under matched presence, absence, placebo, removal, and search-factorial
conditions. This separates four quantities that are often conflated:
retrospective compression, prospective compression, observed reuse, and
marginal forward transfer.

Its governing distinction is that compression proposes a reusable abstraction,
reuse supplies mechanism evidence, and an intervention on future outcomes
supplies causal evidence. A stored or invoked abstraction can remain valid even
when it is redundant, costly, search-obstructing, or transfer-negative.

## Mechanisms

1. **Four-value separation.** Retrospective compression, prospective
   compression, operational reuse, and marginal forward transfer receive
   separate measurements and cannot substitute for one another.
2. **Behavioral reuse ladder.** R0 through R7 distinguish stored, exposed,
   invoked, verified-solution, semantically contributory, operationally
   essential, positive-transfer, and cross-family-transfer states.
3. **Versioned evaluation rounds.** Grammar, knowledge state, search,
   verifier, task distribution, budgets, and analysis are frozen before the
   test set is exposed.
4. **Matched intervention controls.** Absence, irrelevant abstraction,
   duplicate, no-op, random-valid, expert, oracle, and removal conditions
   separate availability from necessity and utility.
5. **Library-search factorial.** A two-by-two design distinguishes a useful
   library from a better search procedure that happens to accompany it.
6. **Exact outcomes.** `verified`, `refuted`, `unknown`, `timeout`, and
   `invalid` remain distinct; a timeout is not a semantic refutation.
7. **Lifecycle separation.** Extraction, independent validation, development
   evaluation, freezing, test intervention, disposition, and admission to a
   later version occur as separate steps.
8. **Full cost accounting.** Mining, verification, indexing, documentation,
   storage, maintenance, retrieval, search, candidate verification, and
   compilation costs are compared under equal downstream and equal total
   budgets, with a declared break-even horizon.
9. **Verification levels.** Tested, exhaustive-bounded, solver-validated,
   certificate-checked, proof-assistant-checked, and artifact-validated claims
   remain separate.
10. **Concrete protocol families.** Depth-controlled sequence synthesis,
    comparator networks, bounded bit-vector synthesis, and an optional theorem
    library provide increasing implementation difficulty while preserving exact
    or independently checkable outcomes.

## Evidence

### Formal Observations And Limits

The manuscript gives finite constructions showing that retrospective
compression need not create forward transfer, invocation need not imply
marginal utility, a larger library can worsen bounded discoverability, unequal
compute cannot identify a library effect, verified source does not imply a
verified emitted artifact, same-round promotion confounds evaluation, and
transfer depends on the task distribution, search, verifier, and budget. These
are scoped arguments and counterexamples, not independently mechanized results
in this repository.

The paper does not claim library learning, future-oriented abstraction
selection, proof reuse, counterexample-guided synthesis, or algorithm discovery
as new. Its cited literature is a map for later source review; the bibliography
does not by itself authorize book claims about those works.

## Failure Modes

- A shorter library description is advertised as future utility without an
  intervention.
- Invocation counts are treated as benefit even when the abstraction is
  redundant or harmful.
- The library and search procedure change together, making attribution
  impossible.
- Test tasks influence the library version that is evaluated on them.
- Timeouts are counted as refutations or omitted from the denominator.
- Construction and maintenance costs are excluded from the comparison.
- Source-level verification is allowed to cover an unverified compiler,
  lowering, or emitted artifact.
- Cross-family or open-ended improvement is inferred from one bounded task
  distribution.

## Chapter Decision

Do not add a paper-shaped chapter. `procedural-memory-and-cognitive-loop-closure`
is the primary owner because it governs the promotion of traces and candidate
abstractions into reusable procedures. Evaluation, economics, formal
verification, compression, persistence, recursive improvement, and learning
theory each receive only the consequence they own. This keeps causal admission
distinct from the mechanisms that propose, store, verify, price, or reuse an
artifact.

## Book Chapters Supported

| Chapter | Distinct contribution | Source locus | Boundary |
|---|---|---|---|
| `procedural-memory-and-cognitive-loop-closure` | The forward-transfer intervention, R0-R7 ladder, frozen candidate lifecycle, and distinction between valid, reused, necessary, and beneficial procedures. | Sections 4-6, 10-13; Appendices A-B | No procedure or transfer effect was implemented or measured. |
| `benchmark-ratchets-and-anti-goodhart-evidence` | Matched placebo/removal controls, library-search factorial, exact outcome taxonomy, frozen rounds, and complete denominators. | Sections 5-6, 10-13 | Proposed evaluation design only. |
| `resource-economics-and-token-budgets` | Full construction and operating cost, equal-downstream versus equal-total comparison, and break-even horizon. | Section 7 | No measured cost advantage or optimum. |
| `executable-specifications-and-lean-proof-envelope` | Separate semantic-contract, source-proof, lowering, emitted-artifact, and transfer claims. | Sections 3.4-3.5, 8-9 | No proof or artifact validation was run here. |
| `rankfold-neuralfold-and-artifact-compression` | Compression as candidate generation rather than causal evidence; vocabulary growth can obstruct bounded search. | Sections 4, 7.5-7.6, 9 | No codec or transfer result. |
| `adjudicated-persistence-and-the-adaptive-commit-boundary` | A later-version admission boundary after independent validation and frozen evaluation; valid-but-transfer-negative artifacts remain distinguishable. | Sections 6.2, 6.8-6.9; Appendix B | No admission service or benchmark run. |
| `recursive-self-improvement-boundaries` | Library growth is not recursive improvement; improvements to search and knowledge require separate interventions. | Sections 6.9, 15.6, 16.8 | No open-ended or compounding improvement result. |
| `learning-theory-generalization-and-scaling-science` | Transfer claims are relative to task lineage, distribution, search, verifier, and budget. | Sections 4.5, 9.7, 11, 13.2, 14.5 | No universal generalization or scaling claim. |

## Claims To Add Or Update

- Require future-task interventions before calling a reusable abstraction
  beneficial.
- Preserve the full R0-R7 ladder rather than collapsing storage, invocation,
  necessity, transfer, and cross-family transfer into one reuse label.
- Freeze knowledge and evaluator state before test exposure, and admit accepted
  candidates only to a later version.
- Use matched placebos, removal tests, and a library-search factorial to identify
  the mechanism responsible for any measured gain.
- Report exact verifier outcomes and complete task-lineage denominators.
- Compare equal downstream and equal total budgets, including lifecycle costs
  and break-even horizon.
- Validate source semantics, emitted artifacts, and transfer as separate claims.
- Keep every conclusion relative to its task distribution, search procedure,
  verifier, and resource budget.

## Proof Or Test Candidates

- Mechanize a finite positive-retrospective-compression, zero-forward-transfer
  counterexample after checking for duplication with current compression proofs.
- Mechanize invocation without marginal utility and same-round promotion
  confounding in a finite lifecycle model.
- Encode a finite grammar-growth witness where adding a valid abstraction
  worsens bounded discoverability.
- Add source-to-artifact validation obligations to an existing formal-artifact
  consumer rather than creating an unowned theorem family.
- Implement one Tier-1 comparator-network or bounded bit-vector intervention
  with frozen rounds, exact verification, placebos, removal, and equal-total
  accounting before making any empirical transfer claim.

## Open Questions

- Which task lineages make semantic contribution and operational necessity
  identifiable without prohibitive intervention cost?
- How should interacting abstractions be tested when bounded set interventions
  are still combinatorial?
- What matched irrelevant abstraction is strong enough to control for grammar
  growth and retrieval exposure without becoming useful itself?
- How should negative knowledge, dispatch policies, and learned search control
  appear on the same reuse ladder as positive reusable programs?
- Which of the paper's 31 external references survive full-paper review and are
  the right anchors for individual chapter claims?
