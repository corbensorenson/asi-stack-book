# Source Note: TreeLLM

| Field | Value |
|---|---|
| Source ID | `treellm` |
| Source title | TreeLLM |
| Ingestion date | 2026-06-24 |
| Source version / URL | Google Docs source in inventory: https://docs.google.com/document/d/17C98P4WhU4srqrT83xXpopRvwHO19zRFJ_ov0MWhgHE |
| Ingestion basis | Local raw cache inspected at `sources/raw/google_docs/treellm.txt`; raw text is not published. |

## Thesis

TreeLLM proposes replacing opaque memorized knowledge with an explicit, traversable semantic graph and compact tokens derived from paths through that graph. The model becomes a navigator over an external semantic operating system rather than the sole container of world knowledge.

## Mechanisms

- Represent concepts, questions, and relations as a probabilistic multi-entry directed acyclic graph.
- Encode concepts as fixed-size semantic tokens built from traversal paths and residual attributes.
- Make tokens self-referential by tokenizing the vocabulary used in questions.
- Support similarity, analogy, interpolation, and counterfactual operations through path and residual operations.
- Bootstrap the graph through high-information-gain questions and iterative self-tokenization.
- Separate factual updates from model retraining by editing graph nodes, edges, and tokenized articles.
- Share one semantic graph across many lightweight agents.

## Evidence

- The source is a whitepaper/specification with several evolving variants in the cache.
- It provides a concrete semantic representation proposal and training/update strategy.
- It does not provide a local TreeLLM implementation, measured compression ratios, benchmarked reasoning gains, or verified token format in this repository.

## Failure Modes

- Assuming a curated semantic graph can cover open-world ambiguity without residual uncertainty.
- Confusing fixed token size with lossless semantic adequacy.
- Overclaiming explainability when traversal paths may still be incomplete or biased.
- Treating graph updates as cheap without accounting for consistency, versioning, and downstream retokenization.
- Allowing a canonical DAG to become an unreviewed authority source.

## Book Chapters Supported

- `cognitive-compilation-and-semantic-ir` (Cognitive Compilation and Semantic IR)
- `verification-bandwidth-and-context-adequacy` (Verification Bandwidth and Context Adequacy)
- `spinoza-verification-and-proof-carrying-claims` (Proof-Carrying Claims and Adversarial Review)
- `semantic-representation-and-tree-structured-models` (Semantic Representation and Tree-Structured Models)
- `mathematical-and-search-substrates` (Mathematical and Search Substrates)

## Claims To Add Or Update

- Use TreeLLM to motivate explicit semantic substrates, graph-traversal explanations, and updateable representation layers.
- Do not claim TreeLLM achieves its stated model-size or reasoning advantages without a prototype or benchmark.

## Open Questions

- Should semantic pages in the book expose TreeLLM-like path traces?
- What validation would show that a semantic token preserves enough information for a target task?
