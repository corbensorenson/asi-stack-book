# v0.2 Manuscript Status

Last updated: 2026-06-27

This file records the current state of the first complete manuscript pass for **The ASI Stack**.

Current v1.0 candidate readiness is tracked in `docs/v1_0_candidate_status.md`. This file remains a historical status document for the v0.2 baseline and early improvement pass.

Current repository scale after the v1.0 candidate improvement pass: 54 chapter files, 174,706 chapter words excluding YAML front matter, and 183,272 raw chapter-file words including metadata and live scaffolding.

## Completed in v0.2

- All 54 manifest-driven chapters now have end-to-end manuscript prose.
- Every chapter retains the required contract: status, drafting guardrail, problem, insufficiency, core claim, mechanism, interfaces, invariants, failure modes, minimum viable implementation, beyond-state-of-the-art end state, Codex test plan, source crosswalk, and summary.
- Every chapter lists source loading state from the source notes, local raw cache, and connector/recovery records currently visible to the repo.
- Every chapter exposes formalization hooks from the existing proof targets.
- Chapter support states remain conservative; the drafting pass did not promote claims above their recorded evidence basis.
- The public landing page has a generated text-free hero image and an editable Mermaid reference-architecture diagram.
- Source notes now exist for all 101 public-safe source records currently used by the book, including the original backbone notes, internal Google Docs sources, public/local Project Theseus records, Circle Calculus records, Field of God constitution records, external literature records, and official documentation records. The `sources/source_notes/` directory also contains a README and template that are not source records.
- The stack-boundary Lean proof targets are implemented in `AsiStackProofs.StackBoundaries`.
- The efficiency/minimum-viable-route Lean proof targets are implemented in `AsiStackProofs.Efficiency` as narrow finite-record predicates for listed lower-cost route exclusion and residual-record requirements.
- The authority-ceiling Lean proof targets are implemented in `AsiStackProofs.Authority` as narrow finite-record predicates for no-grant ceiling preservation and missing-grant denial.
- The failure-mode Lean proof targets are implemented in `AsiStackProofs.FailureModes` as narrow finite-record predicates for failed-invariant promotion blocking and unbounded-authority failure detection.
- The intent-contract Lean proof targets are implemented in `AsiStackProofs.IntentContracts` as narrow finite-record predicates for declared constraint/stop-condition preservation and missing-authority executable-job blocking.
- The constitutional-alignment Lean proof targets are implemented in `AsiStackProofs.Alignment` as narrow finite-record predicates for active-predicate satisfaction and protected-predicate weakening rejection.
- The agency/corrigibility Lean proof targets are implemented in `AsiStackProofs.Corrigibility` as narrow finite-record predicates for protected agency-right preservation and required correction-pathway rejection.
- The value-conflict Lean proof targets are implemented in `AsiStackProofs.ValueConflict` as narrow finite-record predicates for unresolved-conflict residual records and high-stakes review blocking.
- The governance-rights Lean proof targets are implemented in `AsiStackProofs.GovernanceRights` as narrow finite-record predicates for required audit/exit preservation and protected-right removal invalidation.
- The stable-capability-field Lean proof targets are implemented in `AsiStackProofs.StableCapabilityFields` as narrow finite-record predicates for qualification-required replacement, no-grant authority expansion rejection, and finite lifecycle routing away from default use when identity, evidence, lease, evaluator, authority, incident, rollback, or regression conditions fail.
- The replacement-transaction Lean proof targets are implemented in `AsiStackProofs.Replacement` as narrow finite-record predicates for qualification/rollback prerequisites, failed-regression promotion blocking, and finite transaction routing away from default promotion when artifacts, authority, evaluator, regression, rollback, or monitor conditions fail.
- The Digital SCIF/security-kernel authorization, clearance, and finite authority-use route predicates are implemented in `AsiStackProofs.SecurityKernel` as narrow finite-record proofs.
- The recursive-self-improvement Lean proof targets are implemented in `AsiStackProofs.SelfImprovement` as narrow finite-record predicates for protected-invariant preservation, sole-self-evaluation promotion blocking, lifecycle routing, and finite transition routing across evidence, evaluator, boundary-delta, rollback, stale-gate, residual, canary, and promotion outcomes.
- The planning-control Lean proof targets are implemented in `AsiStackProofs.Planning` as narrow finite-record predicates for authority inheritance and unsatisfied-constraint dispatch blocking.
- The PlanForge DAG Lean proof targets are implemented in `AsiStackProofs.PlanForge` as narrow finite-record predicates for indexed dependency ordering and failed-quality fallback to escalation or residual.
- The intent-to-execution Lean proof targets are implemented in `AsiStackProofs.IntentToExecution` as narrow finite-record predicates for parent-constraint preservation and missing-approval running blocks.
- The command-contract Lean proof targets are implemented in `AsiStackProofs.CommandContracts` as narrow finite-record predicates for required interface fields and explicit-constraint precedence.
- The cognitive-compilation Lean proof targets are implemented in `AsiStackProofs.CognitiveCompilation` as narrow finite-record predicates for IR-obligation preservation, repair-ledger update requirements, and finite semantic-lowering routing across source-plan, atom, obligation, dependency, authority, validator, receipt, residual, and acceptance states.
- The Virtual Context ABI Lean proof targets are implemented in `AsiStackProofs.VirtualContextABI` as narrow finite-record predicates for snapshot-bound resolution, mandatory-miss typed faults, and finite context-admission routing across malformed request, address, authority, mandatory/optional absence, certificate, taint, adequacy, residual, and materialization states.
- The context-certificate Lean proof targets are implemented in `AsiStackProofs.ContextCertificates` as narrow finite-record predicates for derived-cell certificate completeness and source-authority non-escalation.
- The context-transaction Lean proof targets are implemented in `AsiStackProofs.ContextTransactions` as narrow finite-record predicates for committed-event snapshot reads, taint propagation without declassification, and materialization blocking when open deletion obligations lack closure or declassification records.
- The verification-bandwidth Lean proof targets are implemented in `AsiStackProofs.VerificationBandwidth` as narrow finite-record predicates for adequacy/admission separation, inadequate-context support blocking, and finite verification-adequacy routing across missing-claim, unadmitted-context, high-risk inadequacy, pairwise-check, artifact, negative-evidence, contradiction, residual, draft-support, and verified-support states.
- The claim-ledger Lean proof targets are implemented in `AsiStackProofs.ClaimLedger` as narrow finite-record predicates for prior evidence/history preservation and open-contradiction promotion blocking.
- The typed-job Lean proof targets are implemented in `AsiStackProofs.TypedJobs` as narrow finite-record predicates for declared lifecycle transitions, approval-required execution blocking, and finite job-execution routing across missing job, contract, lifecycle, approval, permission, failure, residual, adjudication, evidence-ready delivery, scheduler-slot, dispatch, and retirement states.
- The artifact-graph Lean proof targets are implemented in `AsiStackProofs.ArtifactGraph` as narrow finite-record predicates for produced-artifact provenance references and missing-provenance promotion blocking.
- The runtime-adapter Lean proof targets are implemented in `AsiStackProofs.RuntimeAdapters` as narrow finite-record predicates for permission inclusion and high-impact approval rejection.
- The routing-specialist Lean proof targets are implemented in `AsiStackProofs.Routing` as narrow finite-record predicates for authority/readiness-bounded selection and failed-readiness fallback or residual routing.
- The readiness-gate Lean proof targets are implemented in `AsiStackProofs.ReadinessGates` as narrow finite-record predicates for all-gates-pass promotion, quarantine ordinary-route blocking, failed promoted-gate rejection, stronger-transition completeness, quarantine-route fallback, and stale-gate rerun or residual boundaries.
- The personal-compute-hive Lean proof targets are implemented in `AsiStackProofs.PersonalComputeHives` as narrow finite-record predicates for policy-before-optimization admission and faster-forbidden-node rejection.
- The Compact Generative Systems Lean proof targets are implemented in `AsiStackProofs.CompactGenerativeSystems` as narrow finite-record predicates for unresolved-obligation residuals and lossy-exactness blocking without verification evidence.
- The generate-verify-repair Lean proof targets are implemented in `AsiStackProofs.GenerateVerifyRepair` as narrow finite-record predicates for exact reconstruction equality and failed-verification exactness blocking.
- The Fast Generation Architectures Lean proof targets are implemented in `AsiStackProofs.FastGeneration` as narrow finite-record predicates for required route-promotion fields, raw-token-speed promotion blocking, and generation-mode admission lifecycle routing while preserving `argument` support.
- The artifact-compression Lean proof targets are implemented in `AsiStackProofs.ArtifactCompression` as narrow finite-record predicates for task-probe-or-fallback routing and residual/fallback metadata completeness.
- The semantic-representation Lean proof targets are implemented in `AsiStackProofs.SemanticRepresentation` as narrow finite-record predicates for grounded-node provenance and hierarchy-update supersession accounting.
- The resource-economics Lean proof targets are implemented in `AsiStackProofs.ResourceEconomics` as narrow finite-record predicates for required-gate preservation and high-risk insufficient-verification routing.
- The simulation-fidelity Lean proof targets are implemented in `AsiStackProofs.SimulationFidelity` as narrow finite-record predicates for simulation-claim field completeness and declared-fidelity support limits.
- The proof-carrying contract Lean proof targets are implemented in `AsiStackProofs.ProofCarryingContracts` as narrow finite-record predicates for receipt-boundary completeness, downstream consumer-gate evidence, stale/unsupported consumer rejection, and replay-artifact gates.
- The proof-envelope Lean proof targets are implemented in `AsiStackProofs.ProofEnvelope` as narrow finite-record predicates for implemented-target build/module requirements, non-operational target routing, proof-lane authority, support-promotion boundaries, and external-theorem reference boundaries.
- The coil-attention/cyclic-memory Lean proof targets are implemented in `AsiStackProofs.CoilAttentionMemory` as narrow finite-record predicates for alias-boundary, retrieval-quality promotion, recurrence-admission, and stale-read residual gates.
- The cyclic-mixer Lean proof targets are implemented in `AsiStackProofs.CyclicMixers` as narrow finite-record predicates for structural-claim separation, baseline/tradeoff promotion, alias diagnostics, adoption tradeoff packets, and hardware-refusal gates.
- The integrated-reference-architecture Lean proof targets are implemented in `AsiStackProofs.ReferenceArchitecture` as narrow finite-record predicates for handoff-artifact presence and missing-governance-gate rejection.
- The living-book-methodology Lean proof targets are implemented in `AsiStackProofs.LivingBook` as narrow finite-record predicates for manifest/drafting-artifact gates, structural-update sync gates, release-readiness boundaries, and derived-artifact boundaries.
- The bibliography-plan Lean proof targets are implemented in `AsiStackProofs.BibliographyPlan` as narrow finite-record predicates for source-ingestion and source-assignment gates.
- The proof-carrying-claim, tribunal, procedural-memory, MoECOT-runtime, benchmark-ratchet, and Theseus-reference Lean proof targets are implemented in `AsiStackProofs.ProofCarryingClaims`, `AsiStackProofs.Tribunal`, `AsiStackProofs.ProceduralMemory`, `AsiStackProofs.MoECOTRuntime`, `AsiStackProofs.BenchmarkRatchets`, and `AsiStackProofs.TheseusReference` as narrow finite-record predicates for process artifact, promotion, report-bundle, replay-readiness, and publication-boundary gates.
- The policy-optimization Lean proof targets are implemented in `AsiStackProofs.PolicyOptimization` as narrow finite-record predicates for governed policy-update records, unverified-reward/missing-governance promotion blocking, and route-level promotion failures for inadmissible feedback, target-evaluation gaps, reward-probe gaps, governance/authority gaps, rollback gaps, and regression/residual gaps.
- The artifact-steward Lean proof targets are implemented in `AsiStackProofs.ArtifactStewardAgents` as narrow finite-record predicates for dispatched work-contract boundaries and protected-action approval blocking.
- The prototype-roadmap Lean proof targets are implemented in `AsiStackProofs.PrototypeRoadmap` as narrow finite-record predicates for phase-unlock acceptance gates and evidence-required claim-promotion blocking.
- `Policy Optimization and Learning from Feedback` is a manifest-driven Part IV chapter after Benchmark Ratchets, with a public-safe browser-note ingestion report, method-family taxonomy, stack-policy target map, source-noted external-literature records for the initial policy/RL queue, policy-update schema, fixture, diagram, test backlog, and explicit no-training-run/non-claim boundary.
- Primary arXiv citation metadata is recorded for the current fast-generation external literature set and the initial policy-optimization/RL set; no external result has been reproduced or promoted to a stronger support state.
- The Project Theseus implementation-reference chapter and Circle proof-contract chapter now include Mermaid diagrams for their report and receipt boundaries.
- Every chapter now includes at least one Mermaid interface, lifecycle, state, or evidence-flow diagram.
- `scripts/validate_visual_coverage.py` checks that chapter diagram coverage and the landing-page hero asset remain present.
- The landing page and Preface are unnumbered front matter, so the Part I chapters begin the numbered book sequence.
- The landing-page hero image is constrained responsively so desktop and mobile first viewports show the path into current status without horizontal overflow.
- Four central mechanism chapters now have source-specific hand revisions and Mermaid diagrams for verification bandwidth, cognitive compilation, generate-verify-repair compression, and Digital SCIF authority flow.
- The first Part II control-spine chapters now distinguish command-contract, intent-trace, plan-graph, PlanForge-DAG, and semantic-atom fixture validation from unimplemented behavioral execution, scheduler, compiler, and benchmark claims.
- The VCM/context-substrate chapters now distinguish context ABI, semantic page certificate, context transaction, and context adequacy fixture validation from unimplemented resolvers, context compilers, transactional stores, summary-fidelity tests, and contradiction-rate benchmarks.
- The reasoning/review chapters now distinguish claim records, belief revisions, proof-carrying claim envelopes, and tribunal review fixtures from unimplemented claim extractors, contradiction detectors, proof verifiers, formalization-mismatch checks, and multi-reviewer tribunal runs.
- The execution-substrate chapters now distinguish typed-job, artifact-graph, runtime-adapter, and procedural-tool fixture validation plus the synthetic artifact-graph replay and procedural-memory loop harnesses from unimplemented lifecycle checkers, deployed replay/audit services, tool-effect enforcement, approval gates, deployed loop detectors, tool synthesizers, route monitors, retirement automation, and regression-quality suites.
- The routing/readiness/MoECOT chapters now distinguish specialist registry, routing decision, routing decision lease, readiness gate, and orchestration fixture validation from unimplemented routing benchmarks, learned-router quality tests, deployed authority enforcement, lifecycle-transition enforcement, quarantine routing, imported MoECOT artifacts, replay records, and reproduced runtime benchmarks.
- The compactness/compression/semantic-resource chapters now distinguish compact generative records, compression receipts, compressed artifact records, semantic node records, and resource budget fixtures from unimplemented codecs, utility probes, grounding benchmarks, load simulations, scheduler runs, and non-record-level Lean obligations.
- The simulation/search/cyclic-substrate chapters now distinguish simulation contracts, simulation-transfer boundary fixtures, substrate adoption records, proof target records, cyclic memory contracts, the synthetic cyclic-memory contract harness, and cyclic mixer evaluation fixtures from unimplemented feasibility calculators, A/B runs, theorem-resolution and receipt-replay checks, KV-cache certifiers, learned-memory workloads, long-context tests, RoPE/cyclic-mixer benchmarks, hardware tests, model-quality evaluations, physical-transfer evidence, and non-record-level simulation proof claims.
- The Part IV implementation/living-book chapters now distinguish proof target records, benchmark ratchet records, reference trace records, Theseus report crosswalk records, prototype phase records, living-book release records, and research backlog fixtures from unimplemented artifact-by-artifact proof audits, benchmark runs, integrated trace harnesses, imported Theseus reports, phase completion evidence, editorial quality review, and new-paper triage rehearsals.
- Appendix E now publishes a generated proof-target coverage summary from `proofs/proof_triage.json`: 129 proof targets are covered by triage, with all 129 implemented as finite-record Lean candidates after adding the Efficiency claim-admission lifecycle route, Fast Generation admission-lifecycle route, Artifact Compression admission-lifecycle route, EvidenceStates transition-lifecycle route envelope, ClaimLedger revision-lifecycle route envelope, Policy Optimization promotion-route envelope, Proof Envelope artifact-authority envelope, Readiness Gates lifecycle-boundary envelope, Labor OS job-execution route envelope, Verification Bandwidth adequacy route envelope, Virtual Context ABI context-admission route envelope, Cognitive Compilation semantic-lowering route envelope, Command Contracts execution dispatch route envelope, Self-Improvement transition route envelope, Security Kernel authority-use route envelope, Capability Replacement transaction route envelope, Stable Capability Fields lifecycle route envelope, Human Intent resolution route envelope, and prior Personal Compute Hives approval/federation and Artifact Steward Agents release/sunset predicates.
- `docs/proof_artifact_audit.md` now records a proof artifact traceability audit for all 129 targets, checking manifest, triage, Lean module, root import, chapter hook, limitation prose, and Appendix E wiring without claiming semantic proof adequacy or broad system behavior.
- Appendix C now includes a generated source-note chapter-mapping column for the claim/evidence matrix. All 461 assigned source/chapter pairs have source notes and are explicitly listed by stable chapter ID or exact chapter title in the corresponding source notes.
- Appendix C now includes a generated claim-source mapping column with exact source-note maps for all 54 core claims; the claims remain at `argument` support until accepted evidence transitions, passage reviews, or executed test/proof artifacts justify promotion.
- `docs/source_evidence_audit.md` now records the public-safe source evidence audit: all 461 assigned source/chapter pairs have source notes, chapter listings, exact claim-source mappings, and passage-reviewed mapping records.
- All chapter metadata now uses the current source-note/source-mapping boundary rather than the earlier v0.2 source-note-backlog wording, and the old generic planned-test/proof/crosswalk marker scan is clean.
- The remaining generic chapter test-plan purposes have been replaced with concrete acceptance targets, and `scripts/validate_book.py` now rejects stale generated manuscript phrases in chapters and chapter-generation scripts.
- The exact repeated long-paragraph scan is clean after replacing the last repeated invariant paragraph with chapter-specific prose, and `scripts/validate_repeated_prose.py` now keeps that regression out of `validate_book.py`.
- Executable schema drafts now cover context ABI records, context adequacy records, context transaction records, layer boundary records, semantic atoms, semantic node records, semantic page certificates, compact generative records, compression receipts, compressed artifact records, authority-use receipts, costed route records, resource budget records, generation-mode records, simulation contract records, substrate adoption records, cyclic memory contracts, cyclic mixer evaluation records, specialist registry records, routing decision records, readiness gate records, device resource cards, hive job contracts, hive scheduling decisions, benchmark ratchet records, policy optimization records, MoECOT orchestration records, authority transition records, failure boundary maps, intent contracts, command contracts, intent-to-execution traces, plan graphs, PlanForge DAGs, typed jobs, artifact graph records, runtime adapter invocations, procedural tool records, proof target records, reference trace records, Theseus report crosswalk records, artifact steward charters, project work contracts, contribution ledger entries, steward action decisions, sunset review records, prototype phase records, living-book release records, research backlog records, claim records, evidence transition records, belief revision records, proof-carrying claims, tribunal reviews, constitutional predicates, agency rights checklists, value conflict records, governance rights records, stable capability fields, replacement transactions, and self-improvement transitions, with valid example fixtures checked by `scripts/validate_protocol_examples.py`.

## Still Missing for v1.0

- No core claim is missing an exact source-note mapping or passage-reviewed mapping record, but source-derived support still requires claim-to-mechanism reconciliation and accepted evidence transitions.
- Source-note coverage, chapter-listing coverage, and core claim mapping are no longer the main blockers for assigned sources; direct chapter revision from those notes and claim-level evidence promotion remain incomplete.
- Semantic proof adequacy audits for the implemented proof targets still need to confirm that each finite-record predicate is the right formalization of its intended operational boundary. The current traceability audit checks wiring and limitation coverage only.
- Most chapter-level Codex tests are planned but not implemented or run; protocol schema fixture and release-record validation are implemented and remain limited to schema/example consistency.
- External literature remains incomplete outside the source-noted fast-generation and initial policy-optimization/RL sets; alignment, governance/evals, planning, memory/RAG, formal methods, modular routing, compression, benchmark science, broader process-reward work, RLOO/REINFORCE++ variants, and evaluator-gaming work still need citation-normalized records and source notes.
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
python3 scripts/sync_proof_manifest.py --check
python3 scripts/validate_proof_readiness.py
python3 scripts/validate_proof_artifact_audit.py
python3 scripts/validate_source_evidence_audit.py
python3 scripts/validate_publication.py
python3 scripts/validate_book.py
python3 scripts/validate_visual_coverage.py
python3 scripts/validate_schemas.py
python3 scripts/validate_protocol_examples.py
python3 scripts/validate_repeated_prose.py
git diff --check
(cd lean && lake build)
LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 quarto render --to html
```

Quarto rendered 62 inputs and wrote `_site/index.html`.
