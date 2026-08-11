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
| Original paper library | Corben's digest-bound papers and architecture sources, with links to the chapters they informed. | [Read the original papers](https://corbensorenson.github.io/asi-stack-book/papers/) |

Projection boundaries are defined in [`docs/product_contracts.md`](docs/product_contracts.md).

The canonical current book is the live **87-chapter** site. Use its `AI view` for the complete research scaffold or `Human view` for the cleaner prose projection. Human view is a reading aid, not a reviewed reader-release manuscript.

The mutable root site and `/latest/` are the canonical current publication
surfaces and contain all 87 manifest chapters. Versioned tags and GitHub Release assets are immutable historical snapshots. `v2.3.0` remains the latest
completed immutable HTML release. The
[`Post-v2.3 Evidence Competence, Transfer, and Publication Roadmap`](docs/post_v2_3_maintenance_transfer_and_publication_roadmap.md)
is the sole active roadmap, with machine authority in
[`roadmap_records/post_v2_3_maintenance_transfer_and_publication_status.json`](roadmap_records/post_v2_3_maintenance_transfer_and_publication_status.json).
All 87 live chapter-core claims remain at `argument`.

## 60-Second Trust Surface

<!-- canonical-status:generated-begin -->
_Current canonical metrics (generated from machine records): **87 manifest chapters; 487 public-safe records; 87 chapter-core claims; 87/87 chapters externally positioned; 0 promoted core claims; 115/115 accepted transitions identity-resolved (25 direct, 61 subclaim, 29 proxy; 0 parent movements).**_
<!-- canonical-status:generated-end -->

**What this is:** a public living-book research program and evidence system for governed advanced-AI systems, using ASI as the extreme stress case.

**What this is not:** not a validated ASI implementation, not a deployed safety system, and not a benchmark-proven architecture.

The inventory has 487 public-safe records; 87/87 chapters are externally positioned with 0 explicit external-baseline exceptions. External positioning is not exhaustive literature synthesis. All 87 chapter core claims remain at `argument`; [the core-claim disposition ledger](docs/core_claim_disposition_ledger.md) records 87 per-chapter core-claim dispositions, 22 accepted no-change transition dispositions, 65 accepted no-promotion dispositions, and 0 promoted core claims. The 25 accepted non-core upward evidence transitions are recorded in [the non-core evidence ledger](docs/non_core_evidence_ledger.md), alongside 61 accepted `blocks_promotion` decisions and no chapter-core promotion.

[Appendix C](appendices/C_claim_evidence_matrix.qmd) is the claim/support-state ledger. [Appendix G](appendices/G_corben_source_corpus.qmd) separates Corben-authored and local-project sources from [Appendix H](appendices/H_external_sources.qmd), which records external literature. The [Corben paper library](papers/index.qmd) publishes 50 exact, digest-bound original manuscripts as HTML reading pages and links each one to its current chapter assignments; publication exposes lineage but does not validate or promote the papers' claims. [docs/chapter_external_grounding_status.md](docs/chapter_external_grounding_status.md) reports current per-chapter coverage. [Novelty positioning](docs/contribution_novelty_ledger.md) is not proof of novelty. No independent external review is claimed; see [the review ledger](docs/external_review_status.md).

Contribution-level prior-art positioning is recorded in
[docs/defended_contribution_prior_art_positioning.md](docs/defended_contribution_prior_art_positioning.md)
and checked by
[`scripts/validate_defended_contribution_prior_art.py`](scripts/validate_defended_contribution_prior_art.py);
positioning is not proof of novelty.

Evidence-laundering failure cases and their non-promotion boundaries are
recorded in
[docs/evidence_laundering_prevention_case_studies.md](docs/evidence_laundering_prevention_case_studies.md)
and checked by
[`scripts/validate_evidence_laundering_case_studies.py`](scripts/validate_evidence_laundering_case_studies.py).

Historical chapter merges, redirects, and retained URL lineage are summarized
in [docs/chapter_consolidation_sequence.md](docs/chapter_consolidation_sequence.md)
and [docs/chapter_consolidation_url_history_policy.md](docs/chapter_consolidation_url_history_policy.md);
the full history is checked by
[`scripts/validate_chapter_consolidation_sequence.py`](scripts/validate_chapter_consolidation_sequence.py).

The compact public contract is checked by [`scripts/validate_trust_surface.py`](scripts/validate_trust_surface.py).

## Start Here

| Need | Canonical owner |
|---|---|
| Read the book | [Living book](https://corbensorenson.github.io/asi-stack-book/) |
| Change parts or chapter order | [`book_structure.json`](book_structure.json) |
| Draft chapters or plan proofs | [`docs/book_outline.md`](docs/book_outline.md) |
| Execute current work | [`docs/post_v2_3_maintenance_transfer_and_publication_roadmap.md`](docs/post_v2_3_maintenance_transfer_and_publication_roadmap.md) and its [machine status](roadmap_records/post_v2_3_maintenance_transfer_and_publication_status.json) |
| Audit claims and evidence | [Appendix C](appendices/C_claim_evidence_matrix.qmd) and [`proofs/proof_manifest.json`](proofs/proof_manifest.json) |
| Read Corben's original papers | [`papers/index.qmd`](papers/index.qmd) and the paper links in Appendix G |
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
quarto render papers --to html
```

`book_structure.json` is the only ordering authority. Add, move, merge, or remove chapters there, then regenerate the scaffold; chapter numbering and navigation update automatically. Do not hand-edit `_quarto.yml`.

Do not report a theorem as proven unless `lake build` passed, a test as passing unless it ran, or a source claim unless the source was actually reviewed. Proof artifacts, citations, and implementation code do not silently promote chapter-core support states.

The registered Phase 5 harness set is defined in
[`experiments/phase5_harness_registry.json`](experiments/phase5_harness_registry.json),
summarized in
[`docs/test_harness_status_ledger.md`](docs/test_harness_status_ledger.md),
checked by
[`scripts/validate_phase5_harness_registry.py`](scripts/validate_phase5_harness_registry.py),
and executed through
[`scripts/run_phase5_harnesses.py`](scripts/run_phase5_harnesses.py).

## Artifact Discipline

The normal loop is HTML-first and content-first. EPUB, PDF, DOCX, and audio generation are major-version release work only, after the manuscript is approved for that gate. Audience and strip policy lives in [`editions/release_profiles.json`](editions/release_profiles.json).

Avoid disposable tracked files. Update the canonical owner for a fact or decision; use ignored `build/` or `/tmp` output for diagnostics; batch expensive validation; and remove regenerated local artifacts when their review is complete. A standalone report belongs in Git only when it is a durable evidence, governance, or release record with a named consumer.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the internal change gate and [the repository map](docs/repository_map.md) for storage classes.

## Rights

At exact tag `v2.3.0`, rights are routed per file: cleared author-owned prose
and figures are CC BY 4.0, cleared software-like artifacts are Apache 2.0, and
excluded paths receive no grant. Later drafting states remain all-rights-reserved
unless another exact release ledger says otherwise. The manuscript is not an
invitation for unsolicited contributions. See [LICENSE.md](LICENSE.md),
[NOTICE.md](NOTICE.md), and [CONTRIBUTING.md](CONTRIBUTING.md).
