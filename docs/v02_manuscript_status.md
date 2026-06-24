# v0.2 Manuscript Status

Last updated: 2026-06-24

This file records the current state of the first complete manuscript pass for **The ASI Stack**.

Current scale: 50 chapter files, 78,012 chapter words, averaging 1,560 words per chapter.

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
- Four central mechanism chapters now have source-specific hand revisions and Mermaid diagrams for verification bandwidth, cognitive compilation, generate-verify-repair compression, and Digital SCIF authority flow.
- The first Part II control-spine chapters now distinguish command-contract, intent-trace, plan-graph, PlanForge-DAG, and semantic-atom fixture validation from unimplemented behavioral execution, scheduler, compiler, and benchmark claims.
- The VCM/context-substrate chapters now distinguish context ABI, semantic page certificate, context transaction, and context adequacy fixture validation from unimplemented resolvers, context compilers, transactional stores, summary-fidelity tests, and contradiction-rate benchmarks.
- The reasoning/review chapters now distinguish claim records, belief revisions, proof-carrying claim envelopes, and tribunal review fixtures from unimplemented claim extractors, contradiction detectors, proof verifiers, formalization-mismatch checks, and multi-reviewer tribunal runs.
- The execution-substrate chapters now distinguish typed-job, artifact-graph, runtime-adapter, and procedural-tool fixture validation from unimplemented lifecycle checkers, replay/audit harnesses, tool-effect enforcement, approval gates, loop detectors, and regression suites.
- The routing/readiness/MoECOT chapters now distinguish specialist registry, routing decision, readiness gate, and orchestration fixture validation from unimplemented routing benchmarks, lifecycle-transition enforcement, quarantine routing, imported MoECOT artifacts, replay records, and reproduced runtime benchmarks.
- The compactness/compression/semantic-resource chapters now distinguish compact generative records, compression receipts, compressed artifact records, semantic node records, and resource budget fixtures from unimplemented codecs, utility probes, grounding benchmarks, load simulations, scheduler runs, and Lean proofs.
- Executable schema drafts now cover context ABI records, context adequacy records, context transaction records, layer boundary records, semantic atoms, semantic node records, semantic page certificates, compact generative records, compression receipts, compressed artifact records, authority-use receipts, costed route records, resource budget records, simulation contract records, substrate adoption records, cyclic memory contracts, cyclic mixer evaluation records, specialist registry records, routing decision records, readiness gate records, benchmark ratchet records, MoECOT orchestration records, authority transition records, failure boundary maps, intent contracts, command contracts, intent-to-execution traces, plan graphs, PlanForge DAGs, typed jobs, artifact graph records, runtime adapter invocations, procedural tool records, proof target records, prototype phase records, research backlog records, claim records, evidence transition records, belief revision records, proof-carrying claims, tribunal reviews, constitutional predicates, agency rights checklists, value conflict records, governance rights records, stable capability fields, replacement transactions, and self-improvement transitions, with valid example fixtures checked by `scripts/validate_protocol_examples.py`.

## Still Missing for v1.0

- Most source-to-claim mappings still need explicit claim-level mapping from the new source notes before support states can be promoted.
- Source-note coverage is no longer the main blocker for assigned sources; source-to-claim mapping, direct chapter revision from those notes, and claim-level evidence promotion remain incomplete.
- Most Lean proof targets remain planned or triaged as schema/process/research targets.
- Most chapter-level Codex tests are planned but not implemented or run; protocol schema fixture validation is implemented and remains limited to schema/example consistency.
- External literature remains queued rather than citation-normalized.
- The manuscript still needs hand revision after deeper source mining for remaining chapters so they can become less template-shaped and more source-specific without losing the stack contract.

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
python3 scripts/validate_protocol_examples.py
(cd lean && lake build)
quarto render --to html
```

Quarto rendered 60 inputs and wrote `_site/index.html`.
