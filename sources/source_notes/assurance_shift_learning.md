# Source Note: When Success Stops Teaching

| Field | Value |
|---|---|
| Source ID | `assurance_shift_learning` |
| Source title | *When Success Stops Teaching: Assurance-Shift Learning and Governed Residual Boundary Learning for Mature AI Systems* |
| Author / date | Corben Sorenson; version 1.0; August 11, 2026 |
| Ingestion date | 2026-08-11 |
| Canonical local text | `sources/raw/corben_papers/assurance_shift_learning/package_v1_0/When_Success_Stops_Teaching_Corben_Sorenson.md`; SHA-256 `611787d91fb3035ff6948fd54b5391880da38f2008a85a6c8f89bb11da9fac40`; 128,784 bytes |
| Supplied presentation copy | `sources/raw/corben_papers/assurance_shift_learning/package_v1_0/When_Success_Stops_Teaching_Corben_Sorenson.docx`; SHA-256 `bb77dad821ff76fc075ff2173d6318d7fda88ea6b3a4522e7ab7f0ca5c5c4004` |
| Supporting resources | `references.bib`, `CITATION.cff`, four PNG figures, package README, and `MANIFEST.sha256` in the same local package |
| Package integrity | All nine entries in the supplied manifest matched their recorded SHA-256 values on ingestion. This establishes package-byte integrity only. |
| Storage boundary | The complete supplied package is retained in the ignored local Corben-paper archive. The exact Markdown and referenced figures may be copied into the tracked public paper library under the standing author-publication boundary in `papers/paper_library.json`. |
| Evidence boundary | The paper is a conceptual systems architecture, formal proposal, benchmark specification, and research program. It reports no completed GRBL implementation, SaturationShiftBench run, empirical crossover, independently checked theorem, safety result, or support transition. |

## Thesis

The paper proposes a competence-dependent change in learning emphasis. In a
local operating region where positive behavior is already broad, stable, and
well supported, another ordinary success may carry less marginal information
than a well-characterized exception. The resulting **Assurance-Shift
Hypothesis** is not that negative examples are universally superior. It is
that the marginal allocation of learning effort may rationally move from
ordinary positive acquisition toward boundary discovery, evaluator
improvement, diagnosis, least-invasive repair, monitoring, and recovery.

The paper calls its governed lifecycle **Governed Residual Boundary Learning
(GRBL)**. GRBL distributes responsibility across operation, evidence,
discovery, adjudication, repair, and assurance planes. It should therefore be
integrated through existing book owners rather than converted into a
paper-shaped chapter or a super-layer with authority over all six planes.

## Mechanisms

1. **Qualified Competence Envelope.** Record competence as a scoped,
   versioned, distribution-relative, time-relative, and evaluator-relative
   evidence claim rather than a declaration that the capability is solved.
2. **Frontier modes.** Distinguish acquisition, selection, robustness,
   evaluation, assurance, and recovery. A local controller allocates effort
   among them under coverage, observability, and resource constraints.
3. **Selection gap.** Compare the best supported candidate with the top-
   selected candidate. A small gap can signal saturated selection; a large gap
   can expose a ranking, routing, or evaluator problem even when aggregate
   success is high.
4. **Informative exceptions.** Preserve rarity, severity, surprise,
   recurrence, transfer, evaluator confidence, causal uncertainty, and repair
   value separately. Neither a rare event nor a severe event is automatically
   learning-eligible.
5. **Outcome-process orthogonality.** Keep lucky success and bad-luck failure
   visible. Outcome labels alone do not identify the process defect or repair
   target.
6. **Boundary Evidence Bundle.** Bind a decision capsule, observed defect,
   evaluator verdict, preserved successful prefix, candidate correction,
   protected positive behavior, counterexample to the repair, causal
   uncertainty, recovery record, and scope/lifecycle metadata.
7. **Evaluator-first rule.** When observation channels cannot distinguish
   relevant states, additional policy optimization cannot recover the missing
   information. Improve the evaluator or instrument before increasing update
   pressure.
8. **Least-invasive repair.** Consider evidence, data, memory, tests, guards,
   procedures, tools, recovery, adapters, modules, weights, architecture, and
   specification as distinct repair surfaces. Apply the narrowest qualified
   intervention rather than defaulting to weight updates.
9. **Repair compatibility.** Track interactions among local repairs as a
   compatibility hypergraph. Independently useful patches can conflict when
   composed and may require re-synthesis.
10. **Two adaptation clocks.** Fast containment can narrow, stop, fall back,
    preserve evidence, or recover. Slow consolidation can alter procedures,
    modules, weights, evaluators, or specifications only through its own gate.
11. **Memory strata and negative half-life.** Retain unresolved, active,
    regression, competence-preserving, and retired material separately.
    Negative priority decays relative to the learner and repair state, not by
    wall-clock age alone.
12. **SaturationShiftBench.** Compare twelve proposed learning conditions under
    equal total cost, with capability and attack ladders, explicit hypotheses,
    ablations, integrity measures, and decisive falsifiers.

## Evidence

The paper supplies definitions, equations, six propositions, four
conjectures, five algorithms in pseudocode, thirty-two system invariants, a
six-plane service architecture, extensive red-team failure modes, thirteen
metric families, a preregistration template, a twelve-condition benchmark
design, and a phased implementation roadmap. These are useful specifications
and falsification assets, not observed results.

The supplied bibliography makes the paper's external comparison surface
recoverable. Four especially recent citations were checked at primary arXiv
metadata and abstract level during intake: *When AI Benchmarks Plateau*,
*Hardening Agent Benchmarks with Adversarial Hacker-Fixer Loops*,
*Generalization Hacking*, and *AgentAbstain*. Their full papers have not yet
received book source notes, so their results are not inherited as evidence for
the manuscript.

## Failure Modes

- Benchmark saturation can be mistaken for capability maturity.
- Coverage or observability can collapse while aggregate success rises.
- Bad outcomes can punish sound processes, while lucky outcomes hide defects.
- False negatives, unrealistic probes, evaluator capture, and probe-generator
  monoculture can manufacture a misleading boundary.
- Whole-trajectory punishment, probability-mass displacement, excessive
  repulsion, and catastrophic fixation can suppress useful behavior.
- Local patches can conflict, accumulate into patch soup, or repair symptoms
  while leaving the causal defect intact.
- Memory can be poisoned, flooded, selectively forgotten, fossilized, or used
  to launder unsupported origins.
- Refusal can become a trivial local optimum if useful coverage is not a
  protected objective.
- Fast containment can be mistaken for learning; recovery can be used to erase
  incident history; assurance work can become unaudited bureaucracy.
- Strategic systems can manipulate saturation signals, probes, evaluators,
  or the allocation controller itself.

## Book Chapters Supported

| Chapter | Distinct contribution | Source locus | Boundary |
|---|---|---|---|
| `learning-compute-topology-and-adaptive-process-architecture` | Competence-dependent regime allocation and assurance-dominance as a learning-topology hypothesis. | Sections 2.2, 4.4-4.8, 5.10, 7.1, 10.13, 13.3 | No crossover or resource advantage has been measured. |
| `policy-optimization-and-learning-from-feedback` | Positive-support prerequisite, outcome/process separation, bounded negative pressure, and no direct observed-to-train edge. | Sections 2, 4.6-4.8, 6.3-6.5, 8, 9.3-9.4 | No policy improvement or anti-tampering effect. |
| `data-engines-continual-learning-and-unlearning` | Informative-exception strata, learner-relative negative half-life, natural/probe separation, and protected positives. | Sections 4.6-4.9, 5.6, 6.8, 7.4, 9.5 | Inhibition, replay, and retention are not unlearning or deletion. |
| `adversarial-evaluation-sandbagging-and-training-time-deception` | Evaluator observational ceiling, evaluator-first repair, probe ecology, and train-deployment divergence. | Sections 5.3, 6.2-6.4, 6.9, 9.1-9.3, 10.8-10.10 | No evaluator is shown adequate or independent. |
| `benchmark-ratchets-and-anti-goodhart-evidence` | Selection-gap diagnosis, saturation-versus-wall distinction, equal-cost SaturationShiftBench, attack injections, and decisive falsifiers. | Sections 5.2, 9.1, 10, 11, Appendix C | Proposed benchmark only; no condition has run. |
| `stable-capability-fields` | Boundary Evidence Bundles as qualification inputs, least-invasive repair placement, repair compatibility, and exact invalidation scope. | Sections 4.7, 5.7-5.8, 6.5, 6.10, 7.3, 13.4 | No field repair, compatibility result, or qualified transition. |
| `readiness-gates-residual-escrow-and-quarantine` | Qualified Competence Envelope and the separation of learning eligibility from readiness. | Sections 4.4, 6.4-6.6, 7.5, 8, 12.3 | No calibrated readiness threshold or deployment permission. |
| `procedural-memory-and-cognitive-loop-closure` | Compile mature exception families into tests, guards, procedures, and tools while preserving evidence and reactivation triggers. | Sections 6.5, 6.8, 7.3-7.4, 12.1-12.4 | No safe compiler or measured recurrence reduction. |
| `governed-operations-incident-command-and-graceful-degradation` | Fast containment versus slow consolidation, recovery as a coequal objective, and no incident-to-gradient shortcut. | Sections 6.7, 8, 9.6, 10.12, 12.3, 13.5 | No deployed containment or recovery result. |
| `integrated-reference-architecture` | Joined GRBL lifecycle across six existing planes without creating a super-owner. | Sections 6, 12.1-12.3, 13.5 | No end-to-end GRBL service has been built. |
| `evidence-states-and-claim-discipline` | The Qualified Competence Envelope as a bounded evidence claim rather than competence truth. | Sections 4.4, 7.5, 15.2 | Does not move a claim's support state. |
| `artifact-graphs-audit-logs-and-replay` | Bundle lineage, append-only lifecycle, supersession, repair descendants, and replay provenance. | Sections 4.7, 6.2, 6.8, 8, Appendix A | Record shape does not establish receipt faithfulness. |
| `resource-economics-and-token-budgets` | Assurance-share and equal-total-cost accounting, including evaluator, probe, repair, governance, and recovery cost. | Sections 7.6, 10.13, 11.8, 12.10 | No measured optimum or net lifecycle saving. |
| `adjudicated-persistence-and-the-adaptive-commit-boundary` | Supplies competence-relative evidence, protected positives, recovery obligations, and qualification boundaries for deciding whether an observed lesson may persist and how strongly. | Sections 4.4-4.9, 6.4-6.8, 7.3-7.6, 12.1-12.4 | Does not identify an optimal persistence locus or establish that any durable update is beneficial. |

## Chapter Decision

Update the ten primary chapter owners and add source mappings to the three
cross-cutting evidence, artifact, and resource owners. Do not add a standalone
chapter. The paper's six planes already have explicit owners in the stack, and
a new umbrella chapter would duplicate those responsibilities immediately.
Reconsider only if an implementation exposes a durable lifecycle that no
existing owner can govern without violating separation of authority.

## Claims To Add Or Update

- Treat competence as a qualified envelope indexed by version, operating
  region, distribution, time, evaluator set, and evidence rather than a scalar
  state.
- Treat assurance-dominance as a local allocation hypothesis with explicit
  preconditions and falsifiers, not a universal law favoring negative data.
- Require coverage and observability floors before interpreting high success as
  positive-support saturation.
- Separate natural-distribution evidence from probe-distribution evidence.
- Keep outcome, process, severity, causal attribution, learning eligibility,
  and readiness distinct.
- Route boundary bundles through independent adjudication before replay,
  procedural compilation, policy update, or promotion.
- Prefer the least invasive qualified repair and test repair composition before
  deployment.
- Preserve fast containment and slow consolidation as distinct clocks.
- Account for assurance cost explicitly and compare learning conditions under
  equal total cost.

## Proof Or Test Candidates

- Mechanize finite subtractive insufficiency: forbidden-behavior exclusion
  alone cannot guarantee all modeled positive obligations.
- Mechanize the evaluator observational ceiling for a finite
  indistinguishability witness.
- Prove that a useful-coverage floor rejects the trivial always-abstain policy
  in a bounded model.
- Encode a finite repair non-compositionality counterexample.
- Prove finite Boundary Evidence Bundle admission and non-self-adjudication.
- Rationalize these candidates against existing Lean owners before adding
  proof-manifest targets.
- Implement a Tier-1 exact-verifier SaturationShiftBench slice with equal total
  cost, selection-gap diagnostics, bundle ablations, protected positives, and
  explicit falsification criteria.

## Open Questions

- Which measurements distinguish positive-support saturation from benchmark
  exhaustion, evaluator blindness, or hidden scaffolding?
- Where does assurance-dominance begin, and does the crossover transfer across
  tasks, versions, and evaluator families?
- How should a learner-relative negative half-life respond to partial repairs,
  changed models, and rediscovered recurrence?
- Which repair interactions require pairwise testing, and which require
  higher-order compatibility checks?
- How much assurance work can be amortized before its monitoring assumptions
  expire?
- How can strategic systems be prevented from gaming their own regime
  allocator, probes, or evaluator ecology?
- Which external novelty comparisons survive full-paper review rather than
  abstract-level comparison?
