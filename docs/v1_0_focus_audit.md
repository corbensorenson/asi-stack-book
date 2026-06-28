# v1.0 Focus Audit

Last audited: 2026-06-28

This audit is a planning surface for the next ASI Stack work cycle. It answers two questions:

- What is already strong enough to rely on while writing and improving the book?
- Where should effort go next if the goal is a final-quality living book rather than a large but unproven draft?

It does not promote any claim support state, report any new source result, report any benchmark result, or claim that reader, ebook, document, or audio release artifacts have been reviewed or published.

## Audit Basis

The audit is based on the current repository state, the public-safe status documents, and these local checks:

```bash
python3 scripts/validate_v1_status_snapshot.py
python3 scripts/validate_source_evidence_audit.py
python3 scripts/validate_proof_artifact_audit.py
python3 scripts/validate_reader_spine.py --check
python3 scripts/validate_publication.py
python3 scripts/validate_visual_coverage.py
python3 scripts/validate_release_profiles.py
python3 scripts/validate_human_reading_paths.py
python3 scripts/validate_reader_evidence_boundaries.py --check
python3 scripts/sync_reader_overlay_asset.py --check
python3 scripts/validate_reader_overlays.py --check
python3 scripts/audit_reader_continuity.py --check
python3 scripts/validate_reader_manuscript_manifest.py
python3 scripts/validate_outline_consistency.py
python3 scripts/validate_implementation_horizons.py
python3 scripts/validate_repeated_prose.py
python3 scripts/validate_schemas.py
python3 scripts/validate_protocol_examples.py
python3 scripts/validate_support_state_transitions.py
python3 scripts/validate_authority_transitions.py
python3 scripts/validate_plan_execution_contracts.py
python3 scripts/validate_context_admission_adequacy.py
python3 scripts/validate_readiness_residual_gates.py
python3 scripts/validate_benchmark_antigoodhart.py
python3 scripts/validate_phase5_harness_registry.py
python3 scripts/render_reader_formats.py --check
python3 scripts/build_audio_script.py --check
python3 scripts/validate_book.py
python3 scripts/source_readiness_report.py
```

The checks passed in the audit run. The source-readiness command rewrote no tracked content. These checks are structural, traceability, render-readiness, or generated-workspace checks. They do not prove source interpretation, runtime behavior, benchmark quality, proof adequacy, reader-release review, or audiobook quality.

## Current Shape

| Surface | Current state | Interpretation |
|---|---:|---|
| Manifest parts | 4 | The book has a stable four-part architecture. |
| Manifest chapters | 54 | Coverage is broad enough that new chapters should be added only when a source or idea owns a genuinely new boundary. |
| Appendices | 11 | Source, claim, schema, test, proof, release, lineage, and implementation-horizon surfaces exist. |
| Chapter body words | 184,472 | The book is already full-length; the main risk is not shortness. |
| Raw chapter-file words | 192,061 | Live scaffolding adds useful AI/research overhead beyond the reader spine. |
| Source records | 122 | The corpus is substantial, with 59 Corben/local records and 63 external records by current appendices. |
| Assigned source/chapter pairs | 461 | Chapter-source coverage is dense and traceable. |
| Exact claim-source mappings | 461 | Every assigned pair is mapped at the claim-source layer. |
| Passage-reviewed mappings | 461 | Every assigned pair has a recorded passage-review mapping state. |
| Core claim support states | 54 at `argument` | The book is still conservative. This is correct until accepted evidence transitions exist. |
| Lean proof targets | 112 implemented finite-record targets | Traceability is complete; semantic adequacy remains unreviewed. |
| Protocol schemas | 71 | Record shapes are well-covered. |
| Protocol fixtures | 70 valid fixtures | Fixture validation is broad but not a substitute for runtime tests. |
| Test appendix rows | 228 | Appendix E now has 213 chapter-level rows plus 15 repository-level check rows. |
| Planned/unrun chapter test rows | 155 | The biggest technical evidence gap is still tests beyond shape validation, synthetic gate fixtures, and narrow finite-record proofs. |
| Implemented or partial test/proof/check rows in Appendix E | 73 | Appendix E now has 57 implemented chapter rows, 1 partial chapter row, and 15 repository-level checks. Existing rows mostly validate fixtures, synthetic transition gates, synthetic plan-execution consistency, synthetic context admission/adequacy consistency, synthetic readiness/residual gate consistency, synthetic benchmark anti-Goodhart consistency, the Phase 5 harness registry, the reader continuity audit, Lean build, or proof/source traceability mechanics. |
| Reader spine | 54 chapters, minimum 1957 words | The generated reader source is structurally substantial. |
| Reader continuity audit | 54 chapters, 0 high-priority and 3 medium-priority heuristic review rows | The audit gives Phase 2 a deterministic human-review queue without claiming manual review or release readiness. |
| Human Reading Path bridges | 54, minimum 170 words | Every chapter has a human-entry bridge. |
| Reader overlay operations | 33 active | The opening-chapter semantic overlay pilot, Efficient ASI table-to-prose pass, Human Intent table-to-prose pass, System Boundaries table-to-prose pass, Evidence States table-to-prose pass, Personal Compute Hives table/prose pass, Command Contracts table-to-prose pass, Planning table-to-prose pass, Verification Bandwidth table-to-prose pass, Runtime Adapters table-to-prose pass, Labor OS table-to-prose pass, Circle Contracts table/prose pass, Generate-Verify-Repair table-to-prose pass, Fast Generation table/code-to-prose pass, RankFold/NeuralFold table-to-prose pass, Mathematical and Search Substrates table-to-prose pass, Policy Optimization table-to-prose pass, Artifact Steward Agents table/prose pass, Executable Specifications prose pass, and Semantic Representation table-to-prose pass are active; broader reader continuity review and chapter-by-chapter overlays remain open. |
| Reader format readiness | HTML, EPUB, DOCX ready for attempts | The check confirms setup readiness, not produced reviewed artifacts. |
| Audio script readiness | 59 script files generated for review | The check confirms script generation, not audio existence or review. |
| GitHub Pages workflow | Latest checked runs passing | Public deployment mechanics are healthy. |

## What Is Strong

### Architecture And Dynamic Structure

The project now has the right control plane. `book_structure.json` controls parts, chapter IDs, chapter order, source assignments, implementation horizons, and appendices. Quarto numbering is generated at render time. Chapter filenames are stable slugs. `scripts/add_chapter.py`, `scripts/add_part.py`, `scripts/chapter_adjacency_report.py`, `scripts/sync_scaffold.py`, and `scripts/validate_chapter_handoffs.py` make insertion, movement, and deletion feasible without manual renumbering.

The outline is also doing real work. `docs/book_outline.md` matches the manifest order, titles, core claims, assigned sources, and Lean proof targets. That makes it a usable source of truth for future "write the whole book" goals.

### Three-Audience Design

The book has a credible audience model:

- AI/writing-agent view: full live scaffold, source queues, proof hooks, validation commands, support states, and guardrails.
- Human researcher view: complete live book with matrices, sources, proof/test status, and residuals.
- Interested human view: on-site Human view and future reader/audio releases derived from the same source.

The `AI view` / `Human view` toggle is no longer just a visual idea. It has static validation, rendered HTML validation, and browser validation that can exercise every chapter across desktop and mobile. The generated reader source and live Human view share the reader-strip policy and overlay payload path.

### Evidence Boundaries

The source/evidence layer is disciplined. Appendix C records one core claim per manifest chapter, all core claims stay at `argument`, and exact claim-source mappings are present for assigned source/chapter pairs. Appendix G and Appendix H now separate Corben/local sources from external sources by other authors, which avoids confusing authorial lineage with third-party corroboration.

The strongest thing about the current evidence system is what it refuses to claim. It does not treat source notes, local raw caches, connector-readable documents, Lean finite-record predicates, or protocol fixtures as proof of broad ASI behavior.

### Validation Surface

The project has a serious local and CI validation loop:

- Manifest/scaffold sync.
- Outline/manifest consistency.
- Chapter definition-of-done checks.
- Handoff continuity.
- Human Reading Path coverage.
- Reader-spine and reader evidence-boundary checks.
- Reader-overlay checks.
- Source appendix ownership checks.
- Source/evidence audit.
- Proof artifact audit.
- Schema and protocol fixture validation.
- Repeated-prose ratchets.
- Visual coverage and diagram-walkthrough checks.
- Live Human view validation.
- Lean build.
- Quarto render.

This is exactly the right substrate for a living book. Future work should extend this loop into semantic review, tests, and release records instead of adding redundant scaffold checks.

## What Is Not Yet Established

The current repository does not yet establish the following:

- Any ASI capability, model-quality gain, deployment readiness, safety theorem, benchmark result, simulation result, or runtime behavior.
- That source interpretation is semantically adequate for support-state promotion.
- That all 112 finite-record Lean predicates are the best formalization of the intended chapter boundaries.
- That protocol fixtures validate behavior beyond schema shape.
- That MoECOT, Theseus, Circle, Talos, VCM, PlanForge, compression, routing, policy-optimization, benchmark, or simulation claims have been reproduced here.
- That a reviewed reader-release manuscript exists.
- That EPUB, PDF, DOCX, AZW3, MOBI, MP3, M4B, or audio-embedded EPUB artifacts exist.
- That the Human view has been fully read as a polished book, even though its mechanics validate.
- That diagrams are all optimal explanatory diagrams, even though every chapter has substantive diagram coverage and reading notes.

These are not failures. They are the correct next frontier after a strong scaffold.

## Highest-Leverage Focus Areas

| Priority | Focus area | Current strength | Main gap | Best next artifact |
|---|---|---|---|---|
| P0 | Human-reader continuity review | Generated reader spine is substantial and mechanically clean; `docs/reader_continuity_audit.md` now gives the review pass a deterministic queue. | No reviewed human-reader manuscript exists. | Continue through the 3 medium-priority heuristic rows, then record chapter-level overlay operations, canonical prose edits, companion-note treatment, or no-action decisions for real problems found. |
| P0 | Claim-to-mechanism support review | 461 mappings are exact and passage-reviewed. | No accepted evidence transitions have promoted claims above `argument`. | Evidence transition records for a small number of narrow claims, or explicit decisions to keep them at `argument`. |
| P0 | Test/prototype execution | 71 schemas and 70 fixtures validate record shape, with six synthetic behavior-gate harnesses now wired into validation and registry-checked. | 155 Appendix E chapter rows remain planned/not run. | Next executable test harnesses should move toward replayable empirical slices or imported prototype traces with command, environment, result, and non-claim boundaries. |
| P0 | Proof adequacy review | 112 Lean targets build and trace. | All are finite-record predicates; adequacy has not been reviewed. | `docs/proof_adequacy_review.md` or an equivalent audit classifying each target as adequate, too narrow, too broad, or needing a stronger model. |
| P1 | External literature normalization | Fast-generation, policy-optimization, hives, and artifact-steward external records exist. | Alignment, governance/evals, planning, memory/RAG, formal methods, routing/MoE, compression, and benchmark science remain queued. | Add citation-normalized source records and source notes only after reading the sources. |
| P1 | Reader release dry run | Reader generation and HTML/EPUB/DOCX setup checks pass. | No actual reviewed reader artifact is recorded. | Render reader HTML/EPUB/DOCX, record actual local outcomes, inspect representative chapters, then create an edition release record only if review passes. |
| P1 | Visual and diagram quality | Every chapter has a Mermaid diagram and walkthrough note. | Validation proves coverage, not explanatory excellence or e-reader legibility. | Manual diagram audit with fixes for overloaded, redundant, or poorly scaled diagrams. |
| P1 | Public-site UX/accessibility | Pages deploy and Human view validates. | Site quality beyond mechanics needs human inspection. | Browser screenshots and manual notes for landing page, nav, mobile reading, table overflow, toggle clarity, and diagram legibility. |
| P2 | Citation and bibliography polish | Source ownership is clear. | 59 Corben/local records still use stable source IDs rather than normalized citation metadata. | Citation-normalization pass where metadata is actually known, preserving unknowns honestly. |
| P2 | Manifest schema hardening | Generators infer default claim labels and support states safely. | Many chapter manifest records rely on defaults instead of explicit `claim_label`. | Add a `book_structure` schema or explicit claim-label normalization after deciding the field contract. |
| P2 | Audio release path | Audio script generation check passes. | No reviewed audio script or audio artifacts exist. | Only begin after reader manuscript review; produce reviewed spoken-treatment notes before audio generation. |

## Recommended Work Packages

### 1. Reader Manuscript Review

Generate the reader edition, refresh `docs/reader_continuity_audit.md`, then read it like a book rather than like a validation target. The goal is not more word count. The goal is continuity, pacing, lack of duplicated scaffolding, readable transitions, and confidence that the ordinary prose carries all meaning-critical caveats after live-only sections are stripped.

Use the reader-overlay system only for human-reader presentation deltas that should not alter the canonical AI/research source. If the improvement also belongs in AI view, edit the chapter source instead.

Suggested review order:

1. Front matter, Part I, and Part II continuity.
2. Dense technical Part III chapters, especially routing, MoECOT, hives, fast generation, resource economics, simulations, mathematical substrates, Circle, coil memory, and cyclic mixers.
3. Part IV evidence and implementation chapters, especially proof envelope, benchmark ratchets, policy optimization, artifact steward agents, integrated reference architecture, prototype roadmap, and living-book methodology.
4. Appendices selected for reader release: glossary, Corben/local sources, external sources, release editions, and implementation horizons.

Output should be either canonical prose edits or tracked reader overlay operations, plus a reviewed residual list. Do not claim a reader release until a release record names actual rendered artifacts and review status.

The current automated audit identifies 0 high-priority and 3 medium-priority heuristic rows after the table-to-prose and medium-density overlay pass. Continue with those medium-priority rows because they are dense, long, or otherwise likely to need human pacing decisions. The audit itself is not a manual review and should not be treated as release approval.

### 2. Evidence Transition Pilot

Do not attempt to promote all 54 core claims at once. Pick a small pilot set where the support boundary is narrow and the source basis is strongest.

Good first candidates:

- `evidence-states-and-claim-discipline`: the claim discipline is about the repository's own method and has strong internal artifacts.
- `living-book-methodology`: the repository itself demonstrates manifest-driven Quarto, source queues, claim/evidence matrices, proof manifests, tests, changelogs, and releases, but the claim must stay scoped to this project.
- `executable-specifications-and-lean-proof-envelope`: proof traceability is strong, while semantic proof adequacy still blocks broad promotion.
- `source appendices and implementation horizons`: these are generated public surfaces and can support narrow claims about book mechanics, not AI behavior.

For each pilot claim, record:

- Exact claim text.
- Proposed narrower support-state movement, if any.
- Source passages or repository artifacts used.
- Counterevidence or limitation.
- Command outputs, if commands matter.
- Evidence transition record.
- Appendix C update only after the transition is accepted.

Most claims may still remain at `argument`. A recorded non-promotion decision is useful evidence discipline.

### 3. First Executable Test Harnesses

The current test backlog is much larger than the implemented test surface. The first synthetic harness set is now implemented and registry-validated; the next test work should prioritize replayable empirical slices, imported prototype traces, or richer deterministic harnesses that strengthen multiple chapters without overstating evidence.

Initial harness set:

| Harness | Chapters helped | Why first |
|---|---|---|
| Support-state transition checker | Evidence states, claim ledgers, benchmark ratchets, living-book methodology | Directly supports the book's central evidence discipline. |
| Authority non-escalation / permission receipt tests | System boundaries, security kernel, runtime adapters, labor OS | Turns authority vocabulary into reject/accept behavior. |
| Plan graph and execution-contract tests | Intent contracts, command contracts, planning, PlanForge, cognitive compilation | Makes the planning/execution boundary executable. |
| Context admission vs adequacy tests | Virtual Context ABI, semantic pages, context transactions, verification bandwidth | Tests a core memory/reasoning interface. |
| Readiness gate and residual escrow tests | Routing, readiness gates, MoECOT, prototype roadmap, recursive self-improvement | Converts promotion-blocking language into synthetic cross-record gate behavior. |
| Benchmark ratchet anti-Goodhart tests | Benchmark ratchets, policy optimization, artifact steward agents | Keeps benchmark, policy-update, and steward-release handoffs from treating proxy scores as authority. |

The set is registered in `experiments/phase5_harness_registry.json`, documented in `docs/phase5_harness_registry.md`, and checked by `python3 scripts/validate_phase5_harness_registry.py`. The registry guard verifies command scripts, docs, fixture counts, result records, Appendix E rows, public status references, primary chapter mappings, non-claim boundaries, and `scripts/validate_book.py` wiring.

Each future harness should write public-safe results under a tracked result or report location only after it actually runs. If a test is negative, failed, or inconclusive, keep that result visible. The current harnesses remain synthetic record and cross-record gates only; they do not prove routing accuracy, deployed authorization, planner quality, memory correctness, benchmark quality, policy-training quality, steward-agent behavior, runtime safety, or support-state promotion.

### 4. Proof Adequacy Review

The Lean workspace is valuable because it makes local invariants executable and checkable. The risk is that a finite-record predicate can look stronger than it is.

The next proof work should classify each proof target:

- Adequate finite-record invariant for the chapter's current claim boundary.
- Useful but too narrow to affect support state.
- Needs richer state-machine semantics.
- Needs executable test or schema before Lean is meaningful.
- Should stay as research agenda rather than Lean.

The current `proofs/proof_triage.json` routes all 112 targets as `formal-invariant` and `lean-candidate`. That is coherent for the current proof envelope, but a mature v1.0 evidence release should be more discriminating.

### 5. External Literature Backfill

The external-source appendix already covers important fast-generation, policy-optimization, personal-compute-hive, and artifact-steward context. It does not yet cover all areas where a serious public technical book will be judged against outside literature.

Prioritize these queues:

1. Alignment, corrigibility, and power-seeking literature for Part I.
2. AI governance, evaluations, deployment policy, incident response, and model evals for readiness and governance chapters.
3. Planning, task decomposition, HTN/behavior trees/GOAP/TAMP, and agent orchestration for PlanForge and planning chapters.
4. RAG, memory systems, context engineering, long-context evaluation, and context-compilation work for VCM chapters.
5. Formal methods, proof assistants, proof-carrying code, runtime assurance, and contract verification for proof chapters.
6. Mixture-of-experts, model routing, modular agents, and systems routing for MoECOT/RMI/routing chapters.
7. Compression, representation learning, program synthesis, and residual/error accounting for CGS, RankFold/NeuralFold, BBVCA, and semantic representation chapters.
8. Benchmark science, contamination, saturation, hidden tests, and eval gaming for benchmark ratchets.

Do not cite a source from memory. Add a source record, read it, create a source note, assign only relevant chapters, then update mappings.

### 6. Release Artifact Dry Run

The release system is ready for a dry run after the reader manuscript review begins. The correct sequence is:

1. Generate the reader source.
2. Review the generated reader manuscript and delta report.
3. Render reader HTML, EPUB, and DOCX if local dependencies support them.
4. Attempt PDF only when dependencies support it.
5. Inspect produced artifacts for navigation, figures, tables, diagrams, wrapping, and bibliography behavior.
6. Record exact produced artifacts only if they exist.

The audiobook path should wait. Audio scripts are useful review workspaces, but audio should not start until the reader manuscript is reviewed.

### 7. Visual Quality Review

Mermaid coverage is now present across every chapter. The next visual pass should ask harder questions:

- Does the diagram explain the main boundary of the chapter, or only restate section names?
- Is it legible on mobile and e-reader-sized surfaces?
- Does it preserve evidence boundaries, or could it imply implementation/proof status?
- Should a dense diagram be split into a lifecycle diagram plus a record schema diagram?
- Does the diagram walkthrough actually help a reader understand the state transition?

Only add generated bitmap images where they carry meaning. Avoid decorative image work until diagrams and reader figures are clear.

### 8. Public-Site Inspection

The live site works mechanically. A human public-site pass should inspect:

- Landing page first impression and status honesty.
- Human view toggle placement, labeling, and persistence.
- Mobile and desktop navigation.
- Table overflow in source and claim appendices.
- Mermaid sizing and contrast.
- Reader flow when opened directly with `?view=human`.
- Whether the site makes the living/evidence-release distinction obvious.

The browser validator is necessary but not sufficient. It catches broken mechanics, not taste, pacing, or trust.

## Do Not Spend Much Effort Here Yet

- Adding many new chapters without a genuinely new boundary.
- Promoting support states because the prose sounds good.
- Producing audio before a reviewed reader manuscript.
- Treating source notes as external validation.
- Expanding Lean proofs without adequacy review.
- Adding decorative images before diagram and reader-legibility review.
- Polishing marketing copy while evidence transitions, tests, and reader review remain open.

## Suggested Focus Order

The best next sequence is:

1. Reader manuscript review and overlay/canonical prose corrections.
2. Evidence transition pilot on a small set of narrow repository-method claims.
3. First executable test harnesses for support transitions, authority, context adequacy, planning, readiness gates, and benchmark ratchets.
4. Proof adequacy review across all 112 Lean targets.
5. External literature backfill for alignment/governance/planning/memory/formal-methods/routing/compression/benchmark areas.
6. Reader release dry run with actual HTML/EPUB/DOCX render attempts and artifact inspection.
7. Visual and public-site quality review.
8. Audio script review and eventual audio artifact generation only after the reviewed reader release exists.

## Current Blocking Conditions

The project is not blocked from further writing or improvement. It is blocked from calling itself a v1.0 evidence release until these conditions are handled:

- Accepted evidence transitions exist for any claim moved above `argument`.
- Semantic proof adequacy review is recorded.
- At least the intended first wave of chapter-level tests is implemented, run, and recorded, or explicitly deferred.
- External literature queues are normalized where the book relies on outside comparison.
- Reader manuscript review is recorded before reader artifacts are called published.
- Actual format renders and release records exist before EPUB, PDF, DOCX, or other artifacts are claimed.
- Audio script review, generated audio, spot checks, and release records exist before any audiobook or audio-embedded EPUB is claimed.

## Bottom Line

The repo is no longer in scaffold-building mode. It is in evidence-release and reader-quality mode.

The highest-value work is to review the generated human manuscript, run a narrow evidence-transition pilot, implement the first real tests, review the semantic adequacy of the Lean proofs, and backfill third-party literature where outside grounding matters. That work will improve the book more than adding raw volume.
