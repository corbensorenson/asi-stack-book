# ASI Stack Post-v2 Evidence Roadmap

Roadmap ID: `asi-stack-post-v2-evidence-2026-07-10`

Authority: Corben Sorenson

Status: active canonical post-v2 execution roadmap; all empirical priorities
complete, reconciliation and release gate in progress

Predecessor: `docs/asi_stack_completion_roadmap.md`, completed for v2.0.0 and
retained as immutable release history

## Goal to point at

> Move The ASI Stack from a completed, internally coherent v2.0.0 research
> book to a stronger evidence-bearing program. Concentrate on a small number of
> matched, reproducible workloads that test governed cognition, record/reality
> reconciliation, routing and deliberation, and real learning/update causality.
> Preserve failed runs, governance cost, negative results, rollback failures,
> and transfer limits. Change chapter support states only through accepted
> evidence transitions. Keep the 54-chapter architecture stable unless a new
> source or result proves that a distinct interface, invariant, artifact, and
> failure family is genuinely unowned. Maintain the live book and its sources,
> but do not substitute more scaffolding, formats, or planning documents for
> empirical work.

This paragraph is the canonical long-running post-v2 goal.

## Why this is the next direction

The v2.0.0 roadmap is complete. The remaining weakness is not missing book
structure, source routing, schemas, proof hooks, validation machinery, or
release hygiene. It is the distance between a carefully specified
architecture and evidence from realistic work.

All 54 chapter-core claims honestly remain at `argument`. Their evidence
vectors show the same program-wide limits: independence is internal-only,
claim-scope coverage is unmeasured, validity is not independently assessed,
and transfer is not established. Thirty-five claims have no claim-specific
reproduction or adversarial result. The existing governed repository-change
slice is valuable but narrow: it uses a disposable local repository, no model
planning or code generation, deterministic accounting units, and no deployed
authorization, verifier, or rollback service.

The next cycle therefore optimizes for information gain, not claim count. A
well-instrumented negative result, no-change decision, demotion, or refutation
is a successful roadmap outcome.

## Scope decisions

- Keep the current 54-chapter manifest stable by default.
- Improve existing chapter owners before considering a new chapter.
- Select at most three active empirical programs at once.
- Do not attempt a 54-claim promotion sweep.
- Do not require external-human review or outreach.
- Do not regenerate EPUB, DOCX, PDF, audio, or a curated-reader release during
  ordinary evidence work. Those are optional future products, not current
  debt.
- Do not backfill v1.0.0 or rewrite v2.0.0 release history.
- Keep post-v2 drafting all-rights-reserved unless a later tagged release
  installs its own exact rights snapshot.

## Roadmap transition

The authority transition is complete: repository entry points identify this
document as the only active execution roadmap, while the v1, v1.x, historical-
project, remediation, and v2 completion roadmaps remain available as evidence.
It is recorded here for provenance and is not active work.

The three active programs are frozen before outcome runs in
`experiments/post_v2_evidence_program/preregistration.json` and summarized in
`docs/post_v2_evidence_preregistration.md`. The preregistration pins the local
model runtime, workloads, matched baselines, arms, metrics, controls, stop
rules, allowed dispositions, and conditional deferrals. Changing those fields
after an outcome is visible requires a versioned amendment that preserves the
original record.

## Execution status

| Priority | State | Accepted result | Core disposition |
|---|---|---|---|
| Realistic governed work | complete | `experiments/post_v2_governed_work_flagship/results/2026-07-10-local.json` | Three `no_change` decisions; zero core support movement. |
| Routing and deliberation | complete | `experiments/post_v2_routing_deliberation/results/2026-07-10-local.json` | Two independent `no_change` decisions; zero core support movement. |
| Real update causality | complete | `experiments/post_v2_update_causality/results/2026-07-10-local.json` | Four `no_change` decisions; zero core support movement. |

The nine decisions are consolidated in
`claim_decisions/post_v2_empirical_dispositions.json`. Three accepted non-core
`blocks_promotion` transition records preserve the bounded evidence and its
negative results without laundering it into chapter-core support. The
hardware-custody, federation, and Circle/Coil model-quality lanes remain
deferred because their activation conditions are still absent.

## Priority 1 — Realistic governed-work flagship

Outcome: test the book's strongest cross-stack contribution on realistic work,
not only record fixtures.

Build a preregistered task corpus of real but disposable repository changes.
The same tasks must run through a simple baseline and a governed route. When an
authorized model runtime is available, include actual model planning and code
generation; otherwise the run remains a prepared candidate and cannot close
this priority.

The governed route must bind intent, authority, context provenance, plan,
route, sandbox, independent effect observation, evidence decision, residuals,
rollback or quarantine, and final release/refusal. It must preserve the eight
existing attack families and add natural task failures rather than relying
only on hand-authored adversarial fixtures.

Measure together:

- task success and verified correctness;
- false accepts and false rejects;
- unsafe effects and unsafe releases;
- first-effect and final-effect identity;
- rollback attempts, exact rollbacks, and quarantines;
- discovered and unresolved residuals;
- model/tool cost, wall-clock latency, and operator interventions; and
- result sensitivity across task families and repeated runs.

Minimum closure evidence:

- public-safe task and attack corpus with contamination controls;
- matched baseline and governed configurations;
- content-addressed run bundles and environment record;
- independent effect observer separated from the proposer;
- rerun and mutation controls;
- explicit residual and evidence-transition decisions; and
- chapter updates in the governed-cognition, record/reality, and governance-
  economics owners, whether the result supports, narrows, or contradicts them.

This priority does not require a favorable result or a chapter-core promotion.

## Priority 2 — Routing and deliberation comparisons

Outcome: close the two highest-leverage deferred historical-project packets
with one shared matched-compute program.

### Routing lane

Compare oracle routing, a learned or adaptive router, a rule router, one
specialist, and fallback/abstention under the same held-out workload and compute
budget. Preserve request-feature provenance, persistent budget ownership,
route receipts, interference counterfactuals, fallback calibration, and failed
specialist families.

### Deliberation lane

Compare adaptive deliberation with fixed-step and no-deliberation references
under matched latency/compute budgets. Record first-hit, last-correct, stop
reason, branch credit, dissent, verifier behavior, answer changes, and cases
where extra computation makes the result worse.

Minimum closure evidence:

- preregistered held-out split and leakage controls;
- matched compute and latency accounting;
- multiple seeds or repeated trials;
- usefulness and safety/failure metrics reported together;
- negative controls for oracle leakage, proxy reward, retry inflation,
  fallback erasure, and selective reporting; and
- separate no-change/promote/narrow/demote/refute decisions for Routing Heads
  and Governed Deliberation.

## Priority 3 — Real update-causality campaign

Outcome: determine whether the stack's learning and improvement records remain
truthful when state actually changes.

Use a small, disposable, reproducible model or policy workload. It must include
real parameter or policy mutation, content pins, seeds, independent train/
validation/test splits, a matched no-update baseline, fixed probes, checkpoint
identity, runtime-output causality, forgetting measurement, rollback, and
descendant invalidation.

Run a bounded champion/challenger campaign with single-axis changes, fixed
budgets, best-versus-final checkpoint authority, preserved failed families,
and stop rules. Include one deletion or unlearning request and verify what was
and was not removed.

This single program owns the next evidence opportunity for:

- Data Engines, Continual Learning, and Unlearning;
- Policy Optimization and Learning from Feedback;
- Open-Ended Improvement Engines; and
- Recursive Self-Improvement Boundaries, only at the transaction boundary.

Minimum closure evidence:

- reproducible mutation and no-update runs;
- parameter/checkpoint/output lineage;
- changed-decision ablations and evaluator separation;
- forgetting, rollback, and invalidation results;
- negative-knowledge archive and stop decision; and
- one explicit disposition per affected core claim without bundled promotion.

## Conditional backlog — Infrastructure-dependent lanes

These are real unfinished research opportunities but are not active until the
required infrastructure exists. Their deferral is not roadmap failure.

| Lane | Activation condition | Required result |
|---|---|---|
| Model-weight custody and hardware roots of trust | A non-secret disposable hardware/attestation environment is available. | Real measured boot or equivalent attestation, device binding, rotation, revocation, relocation, anti-rollback, and recovery controls. |
| Personal compute hives and federated edge intelligence | A disposable multi-node environment with distinct principals is available. | Signed untrusted payloads, round identity, participant and contribution identity, leases, replay attacks, revocation, partition/rejoin behavior, and aggregate residual accounting. |
| Circle/Coil model-quality lane | A trainable implementation and matched baseline are available. | Capability or efficiency comparison that keeps generated, frozen, trainable, updated, and runtime-reachable state separate. |

If an activation condition is absent, keep the existing exact deferred or
superseded disposition. Do not replace it with another fixture.

## Continuous lane — Living-source and build maintenance

Maintenance protects the book but cannot become the main research output.

- Refresh volatile protocols, standards, laws, threat taxonomies, model/agent
  evaluation frameworks, and major primary research before each public content
  release.
- Perform the governed CI dependency and action-pin review by 2026-10-08.
- Re-run source-to-chapter and terminology ownership checks when a new source
  changes a claim, interface, or comparison.
- Keep the public site, `/latest/`, version index, release records, and status
  object mutually consistent.
- Treat a passing maintenance cycle as release hygiene, not evidence for a
  chapter claim.

## Optional products, not active obligations

The following are intentionally outside the active roadmap:

- an edited 15-chapter narrative/reader edition;
- EPUB, DOCX, PDF, audiobook, or audio-embedded EPUB;
- a DOI or external archive identifier;
- external-human review or outreach; and
- additional chapters.

Any may be opened by a later author decision, but none should compete with the
three empirical priorities above. If an edition is opened, it needs its own
scope, artifact checks, rights snapshot, release record, and version; it cannot
silently become unfinished v2.0.0 work.

## Evidence-cycle rules

For every active program:

1. preregister the claim, simpler baseline, workload, metrics, stopping rule,
   threats, and failure interpretation before the result run;
2. preserve raw public-safe outputs, environment identity, code, seeds, and
   hashes;
3. report benefit and governance tax together;
4. separate proposer, observer, evaluator, and promotion authority in the
   record even when one author operates multiple roles;
5. retain failed attempts and negative knowledge;
6. update the evidence-quality vector before considering support-state change;
7. accept no-change, narrowing, demotion, and refutation as first-class
   outcomes; and
8. update existing chapters before proposing new ones.

## Release rule

Do not choose a v2.1, v3.0, or edition release number in advance of results.
Declare the next release only after at least one active program closes with a
reproducible public-safe artifact and all affected claim dispositions are
recorded. A release may truthfully contain only no-change, narrowing, or
negative results.

The release gate requires one clean commit to pass the validation registry,
Lean build, HTML render, browser checks, tested-bundle handoff, deployment,
public attestation, citation/version reconciliation, rights routing, and exact
artifact checks appropriate to the selected formats.

## Definition of done

This roadmap cycle is complete when:

- the realistic governed-work flagship is executed and dispositioned;
- the routing and deliberation program is executed and dispositioned;
- the real update-causality campaign is executed and dispositioned;
- every affected chapter, evidence vector, proof/test hook, residual, and
  source crosswalk agrees with the results;
- conditional lanes remain either honestly deferred or are completed after
  their activation conditions arise;
- no new chapter or format exists without its own passed gate;
- maintenance requirements due during the cycle are satisfied; and
- the resulting public release, if any, is built, deployed, attested, and
  archived from one clean tested state.

The cycle does not require positive results, blanket claim promotion, external
human review, expensive hardware acquisition, or a new edition format.
