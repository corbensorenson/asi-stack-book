# v0.2 Manuscript Status

Last updated: 2026-06-24

This file records the current state of the first complete manuscript pass for **The ASI Stack**.

Current scale: 50 chapter files, 97,623 chapter words, averaging 1,952 words per chapter.

## Completed in v0.2

- All 50 manifest-driven chapters now have end-to-end manuscript prose.
- Every chapter retains the required contract: status, drafting guardrail, problem, insufficiency, core claim, mechanism, interfaces, invariants, failure modes, minimal implementation, Codex test plan, source crosswalk, and summary.
- Every chapter lists source loading state from the source notes, local raw cache, and connector/recovery records currently visible to the repo.
- Every chapter exposes formalization hooks from the existing proof targets.
- Chapter support states remain conservative; the drafting pass did not promote claims above their recorded evidence basis.
- The public landing page has a generated text-free hero image and an editable Mermaid reference-architecture diagram.
- Source notes now exist for all 59 source records currently assigned to chapters, including the original backbone notes, RMI, Benchmaxxing, CGS, Octopus Router, Cognitive Loop Closure, Project Theseus public-project records, Circle Calculus public-project records, the Field of God AI Constitution, GenesisCode, Verification Bandwidth, Cognitive Compilation, Simulation Scaling, UAT, Ladon/Manhattan, Ratcheting Generative Systems, TokenMana, BeastBrain, TreeLLM, BBVCA, RankFold/NeuralFold, Aletheia, Context Engineer, BugBrain, and the philosophical alignment lineage sources.
- The stack-boundary Lean proof targets are implemented in `AsiStackProofs.StackBoundaries`.
- The Project Theseus implementation-reference chapter and Circle proof-contract chapter now include Mermaid diagrams for their report and receipt boundaries.

## Still Missing for v1.0

- Most source-to-claim mappings still need explicit claim-level mapping from the new source notes before support states can be promoted.
- Source-note coverage is no longer the main blocker for assigned sources; source-to-claim mapping, direct chapter revision from those notes, and claim-level evidence promotion remain incomplete.
- Most Lean proof targets remain planned or triaged as schema/process/research targets.
- Codex tests are planned but not implemented or run.
- External literature remains queued rather than citation-normalized.
- The manuscript needs hand revision after deeper source mining so chapters can become less template-shaped and more source-specific without losing the stack contract.

## Regeneration

The baseline drafting pass is reproducible:

```bash
python3 scripts/draft_v02_from_manifest.py
```

This command rewrites all chapter files from `book_structure.json`. Use it intentionally, especially after source-specific prose has been added.

## Evidence Rule

The v0.2 draft is architecture prose. It is not a proof, benchmark report, or source-derived release unless the relevant claim support state says so and the artifact exists in the repository.

## Local Validation

Passed on 2026-06-24:

```bash
python3 scripts/source_readiness_report.py
python3 scripts/sync_scaffold.py
python3 scripts/sync_proof_manifest.py
python3 scripts/validate_publication.py
python3 scripts/validate_book.py
python3 scripts/validate_schemas.py
(cd lean && lake build)
quarto render --to html
```

Quarto rendered 60 inputs and wrote `_site/index.html`.
