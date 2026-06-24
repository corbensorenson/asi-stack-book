# External Literature Queue

This book currently treats Corben Sorenson's AI papers, local projects, and conversation-mined architecture context as the primary research program being unified. That is a valid starting point, but it is not the same thing as third-party corroboration.

## Stance

- `source-derived` means derived from the supplied ASI Stack source corpus unless a claim explicitly cites third-party literature.
- `external-literature-backed` is reserved for claims backed by recorded third-party sources with bibliographic metadata.
- Self-authored sources can explain the architecture, motivate design choices, and preserve lineage, but they should not be presented as external validation.
- Third-party references discovered inside source papers still need to be recorded in this repo before the book relies on them.

## Priority Areas

| Area | Why it matters | Initial action |
|---|---|---|
| AI alignment and corrigibility | Ground constitutional alignment, corrigibility, agency, and power-seeking claims. | Add canonical survey/key-paper candidates before drafting Part I claims as literature-backed. |
| AI governance and evaluations | Ground readiness gates, audits, deployment policy, evals, and incident response. | Create citation-normalized source records for governance/evals references. |
| Agent planning and task decomposition | Compare PlanForge to HTN, behavior trees, GOAP, TAMP, and modern agent orchestration. | Use `planforge` references as candidates, then record final bibliography entries. |
| Memory, RAG, and context engineering | Compare VCM to long-context, RAG, MemGPT-style memory, ClawVM/RAMPART-like context compilation, and benchmark literature. | Mine `vcm_editable` references into a public-safe queue. |
| Formal methods and proof assistants | Ground Lean, proof-carrying claims, runtime assurance, and contract verification. | Add sources for Lean/proof assistant methods and runtime assurance. |
| Modular systems and routing | Compare MoECOT, Octopus, RMI, and specialist routing to MoE/routing/modular-agent literature. | Add external records before claiming novelty beyond this research program. |
| Compression and representation learning | Ground CGS, RankFold/NeuralFold, BBVCA, semantic trees, and residual accounting. | Distinguish mathematical analogy, prototype claim, and benchmarked compression. |
| Fast generation and decoding substrates | Ground MTP, speculative decoding, multi-head drafting, diffusion LLMs, early exit, state-space alternatives, KV-cache serving, and useful-solution-per-second metrics. | Create citation-normalized source records and source notes before promoting any speed-quality claim. |
| Benchmarks and anti-Goodhart methods | Ground benchmark ratchets, hidden tests, saturation, residual preservation, and eval gaming. | Add references before raising evidence claims in benchmark chapters. |

## Import Rule

When a third-party source is actually used, add it to `sources/source_inventory.json` with a stable source ID, create a source note after reading it, and update `book_structure.json` only for chapters that will mine it directly. Do not cite a paper from memory or from another source's bibliography without reading it.
