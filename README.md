# The ASI Stack

**The ASI Stack: A Governed Systems Architecture for Advanced AI, with ASI as the Stress Case** is Corben Sorenson's living technical book about building advanced AI as an auditable system rather than an unconstrained model.

- [Read the living book](https://corbensorenson.github.io/asi-stack-book/)
- [Browse the public repository](https://github.com/corbensorenson/asi-stack-book)

This repository contains the canonical Quarto manuscript, its dynamic structure, public-safe source and evidence metadata, executable validation, and Lean proof workspace.

## Choose the product you need

| Product | Best for | Open |
|---|---|---|
| Narrative book | A human-oriented route through the architecture. | [Narrative route](https://corbensorenson.github.io/asi-stack-book/products/narrative-book/) |
| Architecture reference | Interfaces, invariants, protocols, tests, proofs, and implementation horizons. | [Architecture index](https://corbensorenson.github.io/asi-stack-book/products/architecture-reference/) |
| Evidence registry | Claims, support states, sources, tests, proofs, releases, and residuals. | [Evidence registry](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/) |

Projection boundaries are defined in [`docs/product_contracts.md`](docs/product_contracts.md).

The canonical current book is the live **84-chapter** site. Use its `AI view` for the complete research scaffold or `Human view` for the cleaner prose projection. Human view is a reading aid, not a reviewed reader-release manuscript.

## 60-Second Trust Surface

<!-- canonical-status:generated-begin -->
_Current canonical metrics (generated from machine records): **84 manifest chapters; 458 public-safe records; 84 chapter-core claims; 84/84 chapters externally positioned; 0 promoted core claims; 115/115 accepted transitions identity-resolved (25 direct, 61 subclaim, 29 proxy; 0 parent movements).**_
<!-- canonical-status:generated-end -->

**What this is:** a public living-book research program and evidence system for governed advanced-AI systems, using ASI as the extreme stress case.

**What this is not:** not a validated ASI implementation, not a deployed safety system, and not a benchmark-proven architecture.

The inventory has 458 public-safe records; 84/84 chapters are externally positioned with 0 explicit external-baseline exceptions. External positioning is not exhaustive literature synthesis. All 84 chapter core claims remain at `argument`; [the core-claim disposition ledger](docs/core_claim_disposition_ledger.md) records 84 per-chapter core-claim dispositions, 22 accepted no-change transition dispositions, 62 accepted no-promotion dispositions, and 0 promoted core claims. Twenty-five narrow non-core transitions are recorded in [the non-core evidence ledger](docs/non_core_evidence_ledger.md), alongside 61 accepted `blocks_promotion` decisions and no chapter-core promotion.

[Appendix C](appendices/C_claim_evidence_matrix.qmd) is the claim/support-state ledger. [Appendix G](appendices/G_corben_source_corpus.qmd) separates Corben-authored and local-project sources from [Appendix H](appendices/H_external_sources.qmd), which records external literature. [Novelty positioning](docs/contribution_novelty_ledger.md) is not proof of novelty. No independent external review is claimed; see [the review ledger](docs/external_review_status.md).

The compact public contract is checked by [`scripts/validate_trust_surface.py`](scripts/validate_trust_surface.py).

## Start Here

| Need | Canonical owner |
|---|---|
| Read the book | [Living book](https://corbensorenson.github.io/asi-stack-book/) |
| Change parts or chapter order | [`book_structure.json`](book_structure.json) |
| Draft chapters or plan proofs | [`docs/book_outline.md`](docs/book_outline.md) |
| Execute current work | [`docs/post_v2_3_maintenance_transfer_and_publication_roadmap.md`](docs/post_v2_3_maintenance_transfer_and_publication_roadmap.md) and its [machine status](roadmap_records/post_v2_3_maintenance_transfer_and_publication_status.json) |
| Audit claims and evidence | [Appendix C](appendices/C_claim_evidence_matrix.qmd) and [`proofs/proof_manifest.json`](proofs/proof_manifest.json) |
| Understand repository ownership | [`docs/repository_map.md`](docs/repository_map.md) |
| Ingest or update the book | [`docs/living_update_workflow.md`](docs/living_update_workflow.md) |

Earlier roadmaps, review packets, probes, and release receipts are historical records, not competing instructions.

## Work Locally

Prerequisites: Python 3, Quarto, Node.js for browser checks, and Lean/Lake for formal proofs.

```bash
python3 scripts/sync_scaffold.py
python3 scripts/sync_proof_manifest.py
python3 scripts/validate_book.py
quarto render --to html
```

`book_structure.json` is the only ordering authority. Add, move, merge, or remove chapters there, then regenerate the scaffold; chapter numbering and navigation update automatically. Do not hand-edit `_quarto.yml`.

Do not report a theorem as proven unless `lake build` passed, a test as passing unless it ran, or a source claim unless the source was actually reviewed. Proof artifacts, citations, and implementation code do not silently promote chapter-core support states.

## Artifact Discipline

The normal loop is HTML-first and content-first. EPUB, PDF, DOCX, and audio generation are major-version release work only, after the manuscript is approved for that gate. Audience and strip policy lives in [`editions/release_profiles.json`](editions/release_profiles.json).

Avoid disposable tracked files. Update the canonical owner for a fact or decision; use ignored `build/` or `/tmp` output for diagnostics; batch expensive validation; and remove regenerated local artifacts when their review is complete. A standalone report belongs in Git only when it is a durable evidence, governance, or release record with a named consumer.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the internal change gate and [the repository map](docs/repository_map.md) for storage classes.

## Rights

The manuscript is publicly visible but is not open source or an invitation for unsolicited contributions. See [LICENSE.md](LICENSE.md), [NOTICE.md](NOTICE.md), and [CONTRIBUTING.md](CONTRIBUTING.md).
