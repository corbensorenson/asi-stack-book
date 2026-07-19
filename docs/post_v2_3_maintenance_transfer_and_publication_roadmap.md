# Post-v2.3 Evidence Competence, Transfer, and Publication Roadmap

Status: **active canonical successor**  
Activated: 2026-07-16  
Substantively revised: 2026-07-17  
Authority: Corben Sorenson  
Machine status: `roadmap_records/post_v2_3_maintenance_transfer_and_publication_status.json`  
Experiment authority: `docs/claim_bearing_experiment_competence_standard.md`

## Purpose

This roadmap contains the unfinished and recurring work after the completed
Post-v2.3 Claim Proof, Causal Validation, and SOTA-Challenge Roadmap. Its first
obligation is now stronger than “write a falsifier before the run.” A negative
result is meaningful only when the tested implementation competently realizes
the intended mechanism, the task actually instantiates the claim, the
instrument could detect a practically important effect, and the idea received
a fair prospectively bounded opportunity to succeed.

Small or deliberately simple implementations remain useful for debugging.
They are not automatically valid tests of an architecture. A chance-level
system, broken evaluator, weak proxy, mismatched tuning budget, authored toy
corpus, or failed positive control must terminate as an implementation,
instrument, construct, or sensitivity problem—not as evidence that the idea is
false. The governing standard is **claim-commensurate competence**, because no
finite experiment can literally prove that every better implementation has
been exhausted.

The roadmap does not reopen completed repository bookkeeping merely to improve
counts. It does reopen the *interpretation* of historical negative and
no-change results where the new competence standard was not yet applied. Raw
outcomes remain immutable; overbroad negative inferences are quarantined until
they earn an N0–N5 classification.

The latest immutable public living-book release remains `v2.3.0`. The current
55-chapter working book, v2.2 reader evidence freeze, and X Article synopsis are
newer artifacts. The post-v2.3 evidence corpus was committed and pushed to
`main` at `882b2a82c` on 2026-07-18. That custody checkpoint is not a new
living-book or reader release, DOI/archive deposit, license grant, or public
post.

## Review adjudication and corrected baseline

The 2026-07-17 review contained several useful criticisms and several stale
counts. The roadmap adopts the criticisms with teeth while preserving the
current repository truth.

| Surface | Current audited state | Roadmap consequence |
|---|---:|---|
| Transition files | 117 | Preserve the full history; the tree did not collapse to six records. |
| Review-accepted transitions | 115 | Every accepted transition must resolve through the canonical claim-identity graph. |
| Direct atom/addendum matches | 25 | Direct identity is not the only valid relation, but implicit identity is forbidden. |
| Accepted claim IDs without a direct atom match | 90 at review; all 90 now indirectly resolved | P0 installed explicit bounded `subclaim_of` or `proxy_for` edges and a rejecting validator; zero accepted identities remain unmapped. |
| Accepted transition states | 87 argument/no-change, 14 synthetic, 10 prototype, 3 refuted, 1 empirical | The target is the first **competence-qualified natural, non-authored, independently evaluated transfer-aware** empirical transition—not the first empirical label ever. |
| Frozen structured denominator | 3,730 activation atoms + 15 reviewed addendum atoms | Campaign claims must not be silently promoted into the atom denominator or chapter cores. |
| Registry support movement | 2 of 3,730 activation atoms are above argument | Claim-ID reconciliation must report evidence truth without inflating core or atom support. |
| Formal snapshot | 298 targets, 98 modules, 1,300 theorem declarations; 894 derived/decomposed, 230 direct/projection, 176 unknown/mixed | The old 91/278 count is stale, but syntax classification is not semantic depth; P4 audits meaning, consumers, countermodels, and refinement. |
| Attested Git state | Review baseline: `cd98c0c4b` plus 380 dirty paths. Custody checkpoint: pushed `main` commit `882b2a82c`. | P0 now enforces post-commit evidence custody and requires the final remediation checkpoint to be re-attested after every campaign disposition. |

## Round 15 adjudication and required corrective

The 2026-07-18 Round 15 review had four criticisms with teeth. The repository
adopts them without adopting stale proof counts or pretending blocked work
completed.

| Criticism | Adjudication | Corrective and terminal criterion |
|---|---|---|
| 380 dirty files put irreplaceable evidence at risk | **Accepted and corrected immediately.** | All existing work was committed and pushed to `main` at `882b2a82c`. The release-tier git-custody gate now rejects any modified, staged, or untracked path under `evidence_transitions/`, `evidence_quality/`, or `release_records/`. Every terminal campaign disposition ends in committed custody before it counts. |
| P2 burned ranks on infrastructure weather before an outcome existed | **Accepted.** | `docs/p2_infrastructure_materialization_and_content_freeze_amendment.md` makes bounded, receipt-complete setup retries legal only before protected task content opens; requires pool-wide infrastructure readiness; blocks rather than advances on setup exhaustion; keeps rank 4 irreversible; reinstates rank 5 as setup-pending; and keeps rank 6 closed. The current 60-GiB host constraint is a named blocker, not a fake slot-1 completion. |
| Four refinement modules remained silent stubs | **Underlying demand accepted; snapshot stale.** | `docs/round_15_proof_depth_disposition.md` retains the four non-stub finite models, adds quantified state-preservation/receipt or authority non-acceptance theorems, binds consumers and mutations, and keeps their inference ceilings explicit. Wider semantic-depth work remains open. |
| Repeated no-release records became an avoidance pattern | **Accepted.** | P7 must repair and fully re-render PDF/DOCX, validate EPUB/PDF/DOCX/HTML by exact format-specific gates, publish approved reader artifacts to the existing GitHub Release target, and record deployed/release identities. The X synopsis remains staged. A failed format may remain blocked only with a current exact defect receipt, not an inherited roadmap disposition. |

Appendix C already consumes the claim-identity graph. The canonical public
status object and generated `publication_readiness.md` block now consume its
115/115 resolution, 25 direct, 61 subclaim, 29 proxy, and zero-parent-movement
counts and bind the graph digest.

The KERC result is retained as the observation that its frozen configured
pipeline failed its preregistered gate on the authored 192-record corpus. Its
0.5 task score, missing adversarial-polarity training class, jointly authored
compiler/verifier, small linear cores, redundant residual storage, and
uncalibrated energy prevent that result from being cited as a refutation of
Kernel English, learned cognitive compilation, hierarchical residuals, or the
broader architecture unless a competence audit establishes a stronger N-level.

## Operating rules

1. **No false-negative laundering.** A failed implementation is evidence about
   that implementation's readiness, not automatically about its intended idea.
2. **A fair chance to succeed comes before a right to refute.** Claim-bearing
   work freezes mechanism activation, matched engineering and tuning budgets,
   favorable/oracle checks, positive controls, sensitivity, and a fair rescue
   ladder before final held-out opening.
3. **No metric theater.** Counts of claims, transitions, theorems, validators,
   sources, formats, or releases never substitute for semantic or empirical
   evidence.
4. **No support laundering.** Formal, executable, empirical, causal,
   reproduction, transfer, source-synthesis, and normative lanes remain
   separate.
5. **Historical evidence is immutable but interpretation is revisable.** Failed
   attempts, raw outcomes, instrument defects, inaccessible comparators, and
   platform limitations remain visible with exact lineage.
6. **No outcome-aware rescue.** Infrastructure setup may receive only the
   prospectively frozen bounded retries in the P2 amendment while protected
   task content remains unopened. The no-rerun rule becomes absolute at the
   first protected-content exposure. Rescue and tuning otherwise use
   development or sacrificial data; final held-out data is opened once only
   after every competence gate passes.
7. **No conversational dependency.** Routine work is local or reproducibly
   tooled. Hosted-chat interaction is never a completion gate.
8. **No external-human prepublication gate.** The roadmap does not require
   private reviewers. Independence needed for a scientific result must come
   from separately implemented evaluators, implementations, or reproductions;
   it does not require another person to read the unfinished book.
9. **Main-only repository continuity.** Work stays on `main`; no branch or pull
   request is required. Commit, push, tag, deploy, archive/DOI deposit, license
   change, and public posting remain owner-gated external mutations.
10. **One active successor.** Closure requires a new successor or an explicit
    continuing-maintenance authority in the same transaction.

## P0 — Public truth, claim identity, and attestation continuity

Build one canonical claim-identity graph covering the 3,730 activation atoms,
15-atom addendum, 55 chapter cores, campaign-local claims, transition IDs,
proof targets, experiment estimands, Appendix C rows, chapter evidence packets,
and synopsis claims. Each accepted transition must have exactly one primary
identity relation:

- `atom`: exact canonical atom identity;
- `subclaim_of`: a narrower proposition whose truth does not move the parent;
- `alias_of`: the same proposition under a retired or local name; or
- `proxy_for`: an instrument-specific measurement relation with an explicit
  construct-validity ceiling.

Every non-exact relation must state population, environment, model,
intervention, outcome, authority, time, artifact, maximum inference, and why it
does not promote its parent. The graph validator must reject unmapped accepted
transitions, cycles, multiple primary owners, dangling aliases, unsupported
parent promotion, scope widening, proxy-to-target laundering, and different
claims that merely share a name.

Keep the landing page, README, citation guidance, release records, roadmap
pointers, reader manifests, and X synopsis consistent with actual public and
local state. The public-truth validator must reject stale release identity,
obsolete active-roadmap claims, missing supersession records, and derivatives
whose bound chapter, claim, result, source, release, URL, header, or platform
inputs have changed.

The current named checkpoint attestation is stale because HEAD excludes the
working-tree state it is being asked to describe. Without rewriting history,
prepare one exact commit-bound reconciliation receipt containing source commit,
tree digest, changed-file inventory, generated-artifact boundaries, validation
results, release effect, and public-state effect. When Corben explicitly
authorizes commit and push, record the work on `main`, push `main`, then attest
the resulting immutable commit. A clean tree cannot be claimed before that
sequence succeeds.

### P0 claim-identity implementation receipt

The identity tranche is complete. `evidence_quality/claim_identity_graph.json`
resolves all 115 accepted transitions: 25 exact atom identities, 61 bounded
subclaims, and 29 proxies. Every indirect edge preserves population,
environment, model, intervention, outcome, authority, time, artifact,
maximum-inference, and parent-nonpromotion boundaries; none moves its parent
support state. `docs/claim_identity_graph_reconciliation.md` exposes the full
crosswalk, and `scripts/validate_claim_identity_graph.py` rejects twelve
identity, scope, artifact, and support-laundering mutations.

The first P0 custody checkpoint is complete at pushed `main` commit
`882b2a82c`. P0 remains continuous: the Round 15 remediation itself requires a
new clean commit-bound attestation, and the custody gate prevents dirty evidence
from being counted or released.

## P1 — Negative-result rehabilitation and false-negative defense

Apply `docs/claim_bearing_experiment_competence_standard.md` retrospectively to
all 87 accepted no-change and three accepted refuted transitions, plus every
historical `narrowed`, `blocked_after_full_attempt`, or prose-level negative
claim used by a chapter. Assign exactly one N0–N5 level:

- N0 instrument failure: no claim inference;
- N1 implementation failure: the idea remains untested;
- N2 proxy or regime failure: retain the proxy result, not target refutation;
- N3 competent exact implementation-setting result;
- N4 mechanism-level counterevidence from multiple competent implementations;
- N5 broad refutation after natural diverse corpora, two transfer settings,
  adequate sensitivity, independent reproduction, and no surviving frozen
  rescue.

The retrospective audit must reconstruct, rather than assume, mechanism
activation, component competence, task validity, positive controls, baselines,
tuning parity, evaluator sensitivity, power, rescue history, held-out custody,
and scope. Missing evidence lowers the N-level. It never gets filled with a
plausible narrative after the fact.

For KERC, preserve the original transition and raw failure. Audit whether the
0.5 task score and known training/implementation defects make it N1 or N2. If a
serious learned compiler and native cores warrant a new test, create a new
claim identity, natural corpus, stronger baselines, independent evaluator, and
prospective protocol. Never reopen the old held-out denominator or overwrite
the historical record.

Chapter prose, Appendix C, the non-core ledger, evidence packets, synopsis, and
public status must use the rehabilitated bounded language. Until audit, a
historical negative result may report what happened but cannot support a broad
architecture or mechanism conclusion.

### P1 accepted-transition rehabilitation receipt

The first retrospective tranche is complete. All 90 accepted transitions with
historical `no_change` or `refuted` effects are digest-bound in
`evidence_quality/negative_result_rehabilitation.json` and assigned exactly one
maximum-negative-inference level: one N0 instrument failure, fifteen N1
implementation failures, seventy-four N2 proxy/regime failures, and zero N3,
N4, or N5 results. The three raw `refuted` labels remain immutable historical
observations; under the competence standard they do not establish an exact,
mechanism-level, architectural, parent-atom, or chapter-core refutation. KERC
is N1, and the two QCSA-labeled refutations are N2. The validator rejects twelve
history rewriting, competence invention, held-out reopening, scope widening,
and support-laundering mutations.

P1 is complete. `evidence_quality/negative_inference_surface_audit.json` binds
75 current reader-facing surfaces, including all 55 live chapters, and reports
zero forbidden overbroad phrases, zero missing named rehabilitation boundaries,
and zero chapters that use `blocked_after_full_attempt` without also stating
that the gaps are residual proof obligations rather than false claims. The X
synopsis source is refreshed; its older unpublished platform draft is honestly
marked stale and cannot be published without update and revalidation. Historical
transition files, completed roadmaps, frozen reader editions, and raw experiment
outputs remain immutable historical scope rather than being rewritten.

## P2 — Competence-qualified natural empirical frontier

Select the highest-value live claim for which a natural, non-authored corpus,
competent implementation, strong comparators, and an honest measurement are
available. Do not select the easiest atom merely to move a support-state count.
Write the canonical identity and causal/mechanistic prediction first, then
freeze the complete competence dossier required by the experiment contract.

The campaign must include:

- at least one strong current model or system suitable for the task, plus a
  matched comparator and mechanism ablations;
- component tests and traces proving the proposed mechanism activated;
- matched engineering, optimization, data, tool, and compute opportunity;
- an oracle or deliberately favorable upper bound where possible;
- natural non-authored data with provenance, contamination, licensing,
  sampling, preprocessing, and exclusion records;
- natural task difficulty spanning neither floor nor ceiling, along with
  positive, negative, trivial, and adversarial controls;
- an independently implemented evaluator calibrated through blinded known-
  effect injection and explicit false-accept/false-reject accounting;
- preregistered minimum effect, sensitivity/power, uncertainty, multiplicity,
  missing-data, stop, cost, and claim-ceiling rules;
- the frozen fair rescue ladder on development data; and
- a final held-out denominator opened exactly once after every gate passes.

Measure usefulness, unsafe release, latency, compute, total lifecycle cost,
governance cost, failure modes, abstention, and residual debt together. Success
may support only the canonical bounded claim. Failure may move a claim only to
the N-level actually earned. An underpowered, chance-level, non-activated, or
positive-control-failing run terminates as an instrument or implementation
result and triggers no negative inference.

### P2 frontier-selection receipt

Selection is complete and the final denominator remains closed. Five candidates
were compared prospectively under weighted scientific value, canonical
relevance, natural-data access, implementation competence, evaluator
independence, sensitivity, and local-resource feasibility. The selected claim
is `p2.governed_natural_repository_change_admission_joint_frontier`, a bounded
`subclaim_of` `integrated-reference-architecture.invariant.015`. It asks whether
full governed admission improves the joint useful-safe-release and false-
blocking frontier on natural non-authored repository changes relative to
matched test-only and record-only baselines while preserving latency, compute,
evaluator work, rollback failure, and residual cost.

The exact selection and custody plan is
`evidence_quality/p2_frontier_selection.json`. Seven competence gates remain
pending: implementation, construct, comparators, evaluator, sensitivity,
development-only rescue, and resources. The held-out gate remains closed. KERC,
QCSA, routing/deliberation, and unlearning were not discarded; each is deferred
because its current implementation or evaluator state would repeat an N1/N2
attempt rather than give the claim a fair prospect of success.

### P2 natural development-corpus receipt

SWE-rebench V2 revision
`475dd5e8703bb5fb22dd3c60b5d038b019eba1e0` is now the pinned natural-task
candidate. A metadata-only post-snapshot screen found 1,117 tasks across 532
repositories and 20 languages. Twelve development-only tasks span twelve public
merged pull requests, twelve repositories, and seven languages; all have
permissive licenses, clean dataset diagnostic flags, separate solution/test
paths, public source receipts, and resolvable `linux/amd64` image manifests.

This advances corpus acquisition, not construct competence. The task release
uses automated setup and LLM annotations, its paper's diagnostic study covers
only 300 tasks in five languages, and its issue tracker documents missing or
mismatched images. All twelve development tasks must reproduce their human-gold
test transition, pass independent specification review and a test-path
collision guard, and fit measured pull/run/emulation/cleanup ceilings before
construct or resource gates can pass. The final pool remains unselected and
closed. Exact receipts are in
`evidence_quality/p2_development_corpus_preflight.json` and
`docs/p2_development_corpus_preflight.md`.

### P2 gold-oracle and dependency-isolation rehabilitation

Natural-task provenance is not enough if the official harness can manufacture
false negatives. Before corpus qualification, execute every development task in
paired test-patch-only and human-gold-plus-test-patch arms with at least two
repetitions. Preserve raw logs even for aborted attempts. Separate dependency
materialization from evaluation: obtain dependencies only in a recorded setup
phase, bind their resolved content into a sealed environment, and run both arms
offline from that same environment. Unrestricted setup egress is diagnostic
only; a claim-bearing run requires a hermetic snapshot or a prospectively
allowlisted, content-digest-verified dependency path with supply-chain and
failure receipts.

Score every consequential task with both the pinned upstream parser and a
materially independent parser/oracle. Calibrate the independent path on
passing, named failing, compile-failing, malformed, missing, and parser-
disagreement logs. A zero exit code cannot erase visibly reported failures, and
a compile-stage failure cannot be treated as hundreds of observed named test
failures. Exact expected-set drift, omitted new tests, setup failure, parser
silence, architecture/emulation divergence, and nonzero parser disagreement
all close the construct gate until diagnosed.

Freeze the task exclusion and replacement policy before drawing any replacement
or final task. A development task whose human-gold transition cannot be scored
without changing the oracle becomes an immutable N0 construct/evaluator
pathology; it is not retroactively rescued by weakening acceptance. Apply the
same exclusion rule to the eligible universe, draw a replacement without
outcome cherry-picking, retain the original denominator and failure lineage,
and rerun the complete qualification. The final pool may be selected and
digest-sealed only after this procedure, and its labels/outcomes may be opened
once only through a blinded evaluator after every implementation, comparator,
evaluator, sensitivity, rescue, and resource gate passes.

The first full fixed-denominator execution and bounded rescue are now
terminally diagnosed. Seven tasks passed the pinned exact oracle. An
independent parser recovered one definite AVA false rejection, producing eight
qualified development tasks across five languages. Four tasks remain N0 and
require same-language replacements: one Rust task has unobservable compile-
failure labels and an extra human-gold test; one Go task combines a target panic
with an unrelated runtime schema fetch; a second Go task depends on filesystem
rename semantics absent from the local container path; and the Java task
reveals an open-ended dynamic Maven provider chain. None has claim effect.

Eight original attempt records and 62 compressed arm logs remain in the
lineage, including the raw-log-custody abort that caused subsequent attempt
versioning. The initial image-size field was later found to be Docker Engine
content-store bytes rather than expanded size. A four-image calibration now
separates the exact Engine-content measurement from a conservative upper bound
derived from Docker's rounded virtual-size display. The prospectively repaired
ceiling is 300 seconds for pull and dependency setup, 1.5 GB Engine content,
7 GB conservative virtual size, 600-second accepted arms, 6 GiB peak memory,
six CPUs, 1,024 PIDs, 50 GiB minimum free space, stable zero-Docker cleanup,
and bounded task/campaign residuals.

The deterministic replacement ladder is active and every terminal failure is
retained as N0 without denominator reduction or claim effect. Rank-one task
specifications for all four slots are digest-bound; the independent Cargo/Go/
Maven evaluator agrees on all 32 calibration cases. In the Rust slot, rank 1
reproduced two checksum-identical Cargo snapshots but its own `make test`
attempts a networked `rustup` prerequisite before emitting tests; rank 2
exceeded the frozen Engine-content ceiling; rank 3 lacked the required verified
commit signature; rank 4 reproduced 331 registry archives and 57 exact-commit
Git-source files twice, but a resource-monitor timeout during its first
baseline arm invalidated the attempt; and rank 5 exceeded the frozen pull-time
ceiling before image measurement. The monitor now records sampling errors and
fails them closed, partial-layer cleanup is explicit, rank 4 is not rerun after
partial outcome exposure, and rank 6 is next. Candidate outcomes remain closed
for the other three slots; the final pool is still unselected and unopened.
This remains the frozen deterministic sequential replacement rule; no later
diagnosis may reorder candidates or weaken a gate.

The resource and construct gates remain pending four qualified replacements
and remeasurement of the complete twelve-task denominator. Do not reduce the
denominator from twelve to eight. Exact receipts begin with
`evidence_quality/p2_gold_preflight_diagnosis.json` and
`evidence_quality/p2_task_qualification_and_replacement_policy.json`; the
resource contract is `evidence_quality/p2_resource_ceiling.json`, and the
sequential rank diagnoses are under `evidence_quality/p2_slot1_rank*`.

## P3 — Independent reproduction, transfer, and SOTA challenge

Reattempt the seven historically blocked P6 atoms only when the candidate,
exact strong comparator, required hardware, dataset rights, and executable
protocol are simultaneously available. A weaker proxy may be useful for
instrument work but cannot silently become a SOTA comparison.

Any claim seeking reproduction support needs a materially separate
implementation or operator path and an independently implemented evaluator.
Any claim seeking broad or mechanism-level support needs at least two
materially different transfer settings selected before outcomes: for example a
different corpus/domain and a different model family, architecture, scale, or
deployment topology. Report per-setting results and failure envelopes rather
than only aggregates.

Freeze model/checkpoint identity, source code, environment, hardware, seeds,
training and tuning budget, evaluator access, cost accounting, defeat criteria,
and downgrade triggers. SOTA/Pareto language additionally requires a dated
frontier search, exact comparator receipts, matched resources, uncertainty, and
survival under the joint usefulness/safety/latency/cost/governance frontier.
Inaccessible or irreproducible comparators remain exact blockers, not losses or
wins.

## P4 — Semantically meaningful formal evidence

Audit the 298 proof targets and 98 Lean modules for semantic adequacy, not proof
shape alone. The 894 `derived/decomposed` classifications are syntax-level
signals; `native_decide`, case splits, arithmetic, or induction do not by
themselves establish that the model captures the book's claim.

Prioritize `DataEngineLifecycleRefinement`,
`OpenEndedImprovementRefinement`, `PolicyOptimizationRefinement`, and
`ResourceEconomicsRefinement`, then every module named by a consequential
safety, evidence, rollback, or self-improvement claim. For each retained
theorem cluster require:

- a plain-language proposition and exact canonical claim consumer;
- explicit modeled state, environment, authority, assumptions, and omitted
  semantics;
- at least one nontrivial countermodel or mutation that the final theorem
  rejects;
- composition, induction, arithmetic, refinement, reachability, or
  noninterference content that is not merely a copied predicate projection;
- an executable/runtime consumer when the theorem purports to constrain
  implementation; and
- chapter prose that states the maximum semantic inference.

Delete, merge, or reclassify stubs that add no semantic leverage. Do not set a
theorem-count quota. A smaller proof surface with meaningful models and real
consumers is better than a large decidable mirror of authored records. Formal
success remains formal evidence; it cannot establish empirical competence,
evaluator truth, deployed enforcement, safety, or transfer.

## P5 — Effect-complete governed reference system

Evolve the integrated local slice into a real multi-process reference system
with durable identity, scoped credentials, revocation, concurrent ledgers,
observed external and internal effects, exact rollback where possible,
compensation and quarantine where not, and descendant-aware deletion. Track
model, optimizer, scheduler, RNG, cache, backup, derived artifacts, and
descendant state. Choose checkpoint authority prospectively.

Bind P4 models to executable state with checked refinements rather than copied
summaries. Qualification requires adversarial boundary tests, crash recovery,
replay, concurrency, stale-cache and revocation tests, supply-chain provenance,
model-weight custody, incident records, effect injection, and an honest
residual register. Distinguish behavioral cohort removal from influence,
privacy, and storage erasure. A deployed claim is forbidden until the deployed
system and its exact commit-bound attestation exist.

Use the P2 competence standard for any performance or safety conclusion drawn
from the reference system. Schema conformance and clean traces are necessary
mechanism evidence, not proof of usefulness or real-world governance efficacy.

## P6 — Evidence, instrument, and source renewal

Run a dated primary-source and official-comparator sweep at least quarterly and
whenever a major architecture, evaluation, governance, learning, unlearning,
memory, AI-control, or evidence-method result appears. Map accepted sources to
chapters and canonical claims; preserve source-reported, locally reproduced,
and independently reproduced states. Prefer sources that can refute, narrow,
or change a live claim or protocol over bibliography growth.

Before reusing an evaluator or harness with materially different models,
domains, languages, scales, or tasks, renew its construct and sensitivity
evidence. Calibration must include known-effect injection, positive-control
behavior, adversarial evaluator cases, independence/leakage review, uncertainty,
and cost. Instrument drift closes the claim denominator; it does not create a
null result.

Maintain a failure-mode library for false negatives: non-activation, weak
training, optimizer mismatch, insufficient capacity, task floor/ceiling,
dataset artifacts, distribution mismatch, baseline under-tuning, evaluator
blind spots, leakage, underpower, seed instability, hidden lifecycle costs,
and outcome-aware rescue. Every new campaign states which of these it excludes,
measures, or retains.

### P6.1 — Deterministic Capability Compilation argument-exit lane

The July 2026 `deterministic_capability_compilation` source is integrated as
design rationale across twenty-two existing chapter owners; it creates no new chapter
and no support transition. Its next evidence-bearing unit is a bounded
capability-foundry vertical slice, not a toy imitation task. Freeze a capability
charter and semantic obligation mass-balance ledger; implement one executable
scaffold, at least two semantically closed learned fields, an NCO package and
four-layer ABI, a sparse linker, pass/fail/unknown translation validation, an
independently implemented evaluator, residual escrow, one reification proposal,
and effect-complete recovery.

The campaign must give the architecture a fair chance to succeed. Compare
against strong adapter, routed-expert, dense-distillation, merge, imitation,
and scratch-learning baselines under matched training, tuning, inference,
verification, fallback, rollback, and maintenance budgets. Test shared-state
interference, learner-induced states, verifier capture, shield bypass, residual
dominance, specification defects, reward exploitation, false reification, and
irreversible effects. A failed weak learner or inactive linker is N0/N1, not
evidence against capability compilation. Broad preservation claims require
independent reproduction and transfer beyond the development domain.

### P6.2 — Platonic World Model semantic-continuity lane

The July 2026 `platonic_world_model` source is integrated as design rationale
across nineteen existing owners; it creates no new chapter and no support
transition. Build profiles incrementally: stable family/version identity;
proposition, attestation, commitment, and proof separation; semantic diff and
governance; branch-protected grounding and dynamics; then packet compilation
and federation. Each profile must earn measured value before the next expands
the trusted and maintenance surface.

Both lanes are bound to
`docs/july_2026_two_paper_mining_completeness_audit.md`. A future source update
must refresh the relevant coverage row, chapter assignments, source note, and
research residuals; inventory or citation presence alone cannot preserve a
`fully mined` disposition.

The frozen evaluation must be longitudinal and adversarial. Compare against
well-tuned retrieval, vector-memory, property/RDF graph, ontology/provenance,
context-aware graph, latent/object-centric world-model, and concept-model
baselines. Induce lexical, intensional, extensional, grounding, relational,
dynamic, context, normative, and dependency drift; model replacement; policy
change; branch escape; evidence laundering; mapping abuse; authority escalation;
and dependency-index evasion. Measure historical replay, silent equivocation,
migration accuracy, context leakage, actuality contamination, grounding and
planning value, blast-radius recall, packet sufficiency, information-flow
leakage, latency, storage, review burden, and maintenance cost. Reject any PWM
component that simpler systems match at materially lower total cost.

## P7 — Reader remediation and owner-authorized publication

Repair the confirmed PDF page-48 clipping and page-50 right-edge overflow, then
rerun full raster and application inspection. Repair the DOCX page-6 figure
break and inspect the exact artifact in Microsoft Word before any Word-quality
claim. Expand EPUB review beyond the bounded Apple Books sample to complete
navigation, chapter coverage, and relevant device or assistive-technology
checks. Preserve exact before/after evidence and the approved local HTML
history.

Continue browser, keyboard, accessibility-tree, contrast, link, and responsive
checks over every page. The X Article header retains canonical local alt text;
recheck whether X exposes a header-description control before publication.
Claim-identity, negative-result, or material source changes trigger synopsis and
reader-derivative reconciliation.

“Ready, not published” is an honest terminal public-state disposition when
external authority is absent; it is not a reason to block evidence work. At
each checkpoint, record whether each prepared product remains current, has gone
stale, or is explicitly authorized for release. When Corben authorizes an
external action, reconcile the exact `main` commit, source tree, rights route,
citation, archive contents, built artifact, deployed bytes, URL, and
attestation. Publishing one product never forces the others.

For the prepared X Article, reopen draft `2077875347220041728`, reconcile it
against canonical Markdown and its manifest, recheck the top link, 2000×800
header crop, platform alt-description behavior, visible word count, formatting,
and audience, then publish only with explicit action-time authorization.

## P8 — Closure, residual ownership, and successor continuity

At every checkpoint, adjudicate each opened item as completed, narrowed,
refuted at an earned N-level, deprecated, superseded, instrument-inadequate,
implementation-inadequate, construct-invalid, underpowered,
`blocked_after_full_attempt`, or still owned with an exact trigger and next
check date. “More research needed” without an owner, prerequisite, and trigger
is invalid.

Close this roadmap only when all opened campaigns have terminal dispositions,
all accepted transition identities resolve, all negative inferences have an
auditable N-level, public truth is reconciled, evidence lanes remain separate,
local reader work is terminally dispositioned, external mutations have exact
authority and receipts, and the next successor or continuing-maintenance
authority activates in the same transaction.

## Execution order and decision rules

P0 begins immediately and remains continuous. Claim identity and stale
attestation must be made truthful before new headline metrics or release
claims. P1 then audits the historical negative frontier; its quarantine applies
immediately even before every retrospective dossier is complete. P2 may design
in parallel but cannot open final held-out data until its identity and
competence dossier pass. P3 opens only when exact access predicates are true.
P4 and P5 may proceed without P2, but neither can promote an empirical or broad
claim. P6 continuously renews the inputs to P1–P5. P7 local remediation may
proceed at any time; its external actions stay dormant until explicitly
authorized. P8 closes every checkpoint.

Every outcome-bearing item begins with an owner, stable claim identity, exact
scope, mechanism, falsifier, prerequisites, evidence lane, competence gates,
fair rescue ladder, held-out custody, stop rule, cost ceiling, artifact
destinations, negative-inference ceiling, and support ceiling. The held-out set
is not a debugging interface.

| Proposed movement | Minimum admissible evidence | Automatic rejection condition |
|---|---|---|
| Formal claim | Semantically adequate model, explicit assumptions, checked result, countermodel search, named claim/runtime consumer | Theorem count, `native_decide` alone, copied projection, vacuous antecedent, or no semantic consumer |
| Executable mechanism | Versioned competent implementation, activation trace, adversarial controls, observed effects, replay/recovery, residual accounting | Schema-only pass, inactive mechanism, mocked effect presented as real, or omitted failure/descendant state |
| Positive empirical/causal claim | Canonical identity, competence dossier, natural held-out outcome, calibrated independent evaluator, uncertainty, cost, controls | Leakage, failed positive control, floor/ceiling task, underpower, unmatched budget, or outcome-aware retry |
| Negative exact claim | All empirical gates plus a passed fair rescue ladder and N3 competence | Chance-level system, failed activation, implementation defect, bad proxy, evaluator blindness, or scope wider than exact setting |
| Mechanism counterevidence | N4: multiple competent implementations, valid tasks, mechanism controls, strong baselines, adequate sensitivity | One implementation, one proxy, missing favorable regime, shared defect, or jointly blind evaluator |
| Broad refutation | N5: N4 plus natural diverse corpora, two transfer settings, independent reproduction, and no surviving frozen rescue | Authored corpus only, single model/domain, no reproduction, or universal language beyond sampled envelope |
| Reproduction | Materially separate implementation/operator and evaluator, exact comparator, frozen environment/checkpoint, reproducible receipt | Same implementation relabeled independent, inaccessible comparator, or weaker proxy substitution |
| SOTA/Pareto | Current strong comparator, preregistered defeat criterion, matched resources, uncertainty, dated scope, joint frontier | Missing code/checkpoint/hardware, incomparable budget, marketing summary, or hidden negative setting |
| Publication readiness | Exact `main` commit, validated derivative, rights state, accessibility boundary, owner authority, deployed-byte receipt | Dirty/stale attestation, local build mistaken for publication, stale release identity, or implied license |

## Initial owned queue

1. **Completed locally:** the canonical claim-identity graph maps all 115
   accepted transitions, including the 90 non-direct claim IDs, without
   promoting parent atoms or cores; twelve rejecting identity mutations pass.
2. **Completed locally:** the accepted-transition rehabilitation ledger binds
   all 90 historical no-change/refuted records as 1 N0, 15 N1, 74 N2, and zero
   N3–N5; no broad or chapter-core negative inference survives.
3. **Completed locally:** current chapter prose, Appendix C, evidence packets,
   synopsis/public surfaces, and `blocked_after_full_attempt` language are
   reconciled across 75 surfaces. KERC is N1, QCSA's two historical refutation
   labels are N2, and no broad or chapter-core negative inference survives.
4. **Blocked honestly:** P2 frontier selection, natural corpus acquisition, the
   fixed-denominator gold diagnosis, replacement policy, evaluator calibration,
   and historical ranks 1–5 are preserved. Do not continue at rank 6. Execute
   the pool-wide infrastructure materialization amendment first; rank 5 is
   setup-retry-pending because no protected content opened. Only after 30/30
   exact infrastructure receipts and monitor soak pass may still-unopened
   content activate. Then qualify all slots, rerun the final twelve twice, and
   complete independent task review, mechanism activation, strong-model,
   baseline, sensitivity, and rescue preflights before freezing the final
   denominator.
5. **Specific Round 15 proof audit completed:** the four named refinement
   modules are retained with quantified semantic theorems, route-complete
   consumers, failed-prefix controls, and explicit non-claims. Continue the
   wider module-by-module semantic audit; do not use theorem counts as closure.
6. Design the P5 reference slice around durable identity,
   authority-to-observed-effect linkage, effect-complete rollback, concurrent
   ledgers, revocation, crash recovery, full learning state, and descendant-
   aware deletion before choosing implementation volume.
7. Open the next source/instrument renewal sweep around false-negative
   prevention, alternative cognitive substrates, evaluator science, transfer,
   governed update/unlearning, the bounded Deterministic Capability Compilation
   foundry lane, and the incremental Platonic World Model semantic-continuity
   lane. Do not allow either new source to inherit evidence from its prose.
8. Repair PDF pages 48 and 50, then DOCX page 6, before broad format polish.
   Preserve failing images, compare exact rebuilt artifacts, visually inspect
   every PDF/DOCX page, validate EPUB structure and navigation, and publish only
   the formats that pass their own release gate.
9. Complete a new commit-bound `main` reconciliation and attestation packet for
   this remediation. Push `main`, observe CI/Pages, bind the reader Release
   assets and deployed URLs, and leave no dirty protected evidence surface.

## Checkpoint receipt

Each checkpoint records the public release identity; exact `main` commit and
tree state; working chapter, atom, and transition counts; claim-ID mapping
coverage; N0–N5 rehabilitation counts; competence dossiers and failed gates;
claim movements; semantic proof additions, reclassifications, and deletions;
executed or blocked experiments; implementation, comparator, corpus, model,
checkpoint, evaluator, and transfer identities; effect sizes and uncertainty;
costs; reader and derivative freshness; rights/publication authority;
failures; residuals; and the next owned trigger. It links public-safe raw
artifacts and includes negative mutations for its most consequential possible
lies.

## Milestones

| Milestone | State | Completion condition |
|---|---|---|
| M0 — Truth and identity control | in progress | Identity is complete and the first custody checkpoint is pushed; close only after this remediation has a clean commit-bound attestation and the new custody gate passes. |
| M1 — Negative-result rehabilitation | completed | All 90 accepted negative/no-change transitions are classified (1 N0, 15 N1, 74 N2, zero N3–N5), and 75 current surfaces including all 55 chapters preserve the resulting ceilings. |
| M2 — Competent natural empirical result | in progress | A high-value natural, non-authored campaign passes every competence gate and ends with a bounded positive, negative, or inconclusive disposition. |
| M3 — Reproduction and transfer | pending | Any broadened result has independent reproduction and two prospectively selected materially different transfer settings. |
| M4 — Semantic formal depth | in progress | The four Round 15 modules are explicitly retained and strengthened; close after every consequential cluster has an adequate model, countermodels, consumers, and honest inference ceiling, with empty stubs removed or reclassified. |
| M5 — Effect-complete reference | pending | Multi-process authority-to-effect, rollback/residual, full-state, and deletion behavior passes adversarial and recovery tests. |
| M6 — Renewal discipline | pending | Dated primary-source, comparator, evaluator, and false-negative instrument renewal is current and mapped to claims. |
| M7 — Reader/publication disposition | in progress | Repair and visually validate the reader formats, publish each approved artifact to the existing target with exact receipts, and retain any rejected format only with a current defect-bound disposition. |
| M8 — Successor continuity | pending | Every open item has a terminal disposition and the next exact authority is active. |

## Definition of done

This roadmap is complete only when the project can distinguish “the idea was
competently tested and failed” from “our implementation or test was not good
enough,” and its book, ledgers, proofs, experiments, derivatives, and public
surfaces all preserve that distinction. Completion requires resolved claim
identity, claim-commensurate competence, immutable raw evidence, N0–N5 negative
scope, semantic rather than count-based formal depth, independent transfer for
broad claims, effect-complete implementation boundaries, current sources and
instruments, exact `main` attestation, terminal reader/publication dispositions,
and uninterrupted successor ownership.
