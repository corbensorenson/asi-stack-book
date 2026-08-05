# Source Note: The Regret Engine

| Field | Value |
|---|---|
| Source ID | `regret_engine` |
| Source title | The Regret Engine: Governed Counterfactual Learning Signals for Continual Adaptation, Prospective Risk Control, and Self-Correction in Artificial Agents |
| Author / date | Corben Sorenson; August 4, 2026; standalone conceptual paper v1.0 |
| Ingestion date | 2026-08-04 |
| Canonical local text | `sources/raw/corben_papers/regret_engine/regret_engine.md`; SHA-256 `6d609442cdbd2725e0109544f000e5255ff6850ce766efa87800fa63a74d1623` |
| Supplied presentation copy | `sources/raw/corben_papers/regret_engine/regret_engine.docx`; SHA-256 `49223721c40de97c22736c760a7672409bb6790d80261739eb075cfb5aa07640` |
| Bundle comparison | Pandoc extraction confirms the same named section sequence in both supplied forms. The DOCX also contains a generated table of contents and embedded equation/figure images, so it is not text-identical to the Markdown. |
| Storage boundary | Both supplied files are retained in the ignored local Corben-paper archive. This tracked note is public-safe; ingestion does not itself publish the raw paper. |
| Missing companions | The Markdown cites `references.bib` and files under `figures/`, but neither companion path was supplied. The DOCX embeds its visual material. Citation keys remain unresolved until the bibliography is supplied or reconstructed from primary sources. |
| Evidence boundary | This is a conceptual architecture, formal proposal, and research program. It does not report an implemented Regret Engine, completed experiment, reproduced baseline, validated causal estimator, deployed control, or formal proof. |

## Thesis

Adaptive agents need a protected path that asks not only what happened, but
which materially better outcome was available under the information,
authority, resources, and uncertainty that existed when the decision was made.
The paper calls the resulting object **Governed Counterfactual Regret (GCR)**.
It is not a self-authored scalar reward. It is an externally adjudicated,
uncertainty-bearing comparison between an executed continuation policy and one
or more admissible comparators.

The proposed subsystem joins retrospective diagnosis, prospective planning,
continual learning, procedural compilation, recovery, and update governance:

```text
decision-time capsule
-> admissible comparator contract
-> counterfactual evidence ensemble
-> typed regret tensor
-> root-cause and learning-eligibility adjudication
-> append-only Regret Packet and Ledger
-> planning, replay, repair, or incident consumer
-> bounded update lease
-> independent promotion, rollback, quarantine, or retirement
```

The book-level contribution is this lifecycle and its ownership boundaries.
The paper should not be imported as a freestanding chapter because Planning,
Policy Optimization, Data Engines, Procedural Memory, Artifact Graphs,
Readiness, Operations, and the Integrated Reference Architecture already own
the relevant decisions and artifacts.

## Mechanisms

1. **Decision Capsule.** Before action, freeze observable information,
   objectives, authority, feasible alternatives, forecasts, uncertainty,
   resources, checks, model/tool/evaluator versions, and provenance. Later
   evidence may revise outcome estimates but may not create hindsight-only
   obligations.
2. **Comparator contract.** Alternatives are admitted only when availability,
   authority, information, resources, continuation semantics, causal
   feasibility, and menu stability are comparable. Rejected and unresolved
   comparators remain visible.
3. **Regret distinctions.** Keep absolute loss, hard violations, surprise,
   risk, attribution, avoidability, learning priority, ex-ante policy regret,
   ex-post event regret, process regret, epistemic regret, opportunity regret,
   recovery regret, and counterfactual surplus separate.
4. **Sparse Regret Tensor.** Preserve stakeholder or objective, horizon,
   comparator, causal contribution, foreseeability, feasibility,
   reversibility, recurrence, evidence, uncertainty, and provenance in native
   units. Consumer-specific scalar projections remain protected, versioned,
   and explicitly lossy.
5. **Counterfactual evidence ladder.** Route from exact replay through paired
   simulation, structural causal models, off-policy estimators, process
   verification, independent critics, and human review. Emit distributions or
   identified intervals when event-level regret is not identifiable.
6. **Prospective regret control.** Compare candidate policies on regret
   distributions, hard boundaries, opportunity closure, recovery burden, and
   uncertainty; search mitigations such as information gathering, bounded
   probes, narrower scope, verification, checkpoints, delegation, rollback,
   or scheduled abstention.
7. **Protected feedback modes.** Use regret first for diagnosis, replay
   priority, or an auxiliary prediction target. More direct objective shaping
   requires stronger anti-tampering, calibration, double-counting, and
   constraint controls.
8. **Regret-aware memory.** Separate catastrophic/hard-boundary, recurrent
   avoidable-defect, unresolved novelty, competence/surplus, and
   retired/superseded lanes. Preserve contrastive repair pairs when a reliable
   better trajectory exists.
9. **Regret-to-rule compilation.** Cluster recurring failures, identify the
   minimal causal difference, synthesize the least invasive test, monitor,
   checklist, guard, route, skill, policy patch, or architecture repair, and
   qualify it against held-out, mutation, adversarial, transfer, and protected
   counterexamples.
10. **Regret debt.** Prioritize unresolved known patterns by recurrence,
    expected preventable burden, uncovered mitigation, and transfer. This is an
    engineering backlog, not an actor reward.
11. **Append-only Regret Ledger.** A packet binds the capsule, actual outcome,
    comparators, model-conditioned estimates, tensor cells, root cause,
    learning eligibility, recovery, repairs, appeals, supersession, and
    retirement. History is monotone while conclusions remain defeasible.
12. **Three update clocks.** Immediate reaction may stop, contain, roll back,
    or preserve evidence; medium adaptation may replay, repair, or compile;
    slow constitutional review may change objectives, rights, comparator
    policy, evaluators, or authority. Faster clocks cannot enact slower-clock
    changes.
13. **Root-cause tribunal.** Route policy, model, process, memory,
    implementation, specification, evaluator, novelty, stochastic,
    adversarial, exploitation, valid-optimization, and unresolved causes to
    different owners. Severity, causal contribution, and learning eligibility
    remain distinct.
14. **Bounded update broker.** Freeze target packet clusters, update surface,
    objective and scalarization versions, data and replay policy, protected
    capabilities, resource/drift limits, monitoring, rollback, promotion
    authority, and expiry before training.
15. **Operational modes.** Move a capability through observe-only, shadow,
    advisory, constrained, residual, canary, qualified, fallback, or quarantine
    states according to evidence and authority rather than score alone.

## Evidence

The paper supplies definitions, equations, three proof sketches, five
algorithms in pseudocode, a service decomposition, a reference packet schema,
worked examples, eight proposed experiments, baseline and ablation lists,
acceptance criteria, twenty failure modes, and a phased research sequence.
These are design and falsification assets, not observed results.

The strongest testable propositions are:

- exact event-level regret is generally non-identifiable without additional
  assumptions or experimental information;
- one scalar cannot preserve both typed repair routing and lexicographic hard
  constraints unless the missing distinctions exist outside the scalar;
- if the actor can lower measured regret without lowering the protected
  underlying deficit, sufficiently strong optimization creates a tampering
  incentive.

The Markdown contains citation keys but not their bibliography entries. Those
citations are therefore leads for external-source intake, not support imported
through this authored source.

## Assumptions And Limitations

- The comparator set, objective snapshot, stakeholder mapping, authority
  boundary, causal model, and evaluator policy are assumed to be governable but
  are not shown to be correct.
- Event-level counterfactuals may be non-identifiable, off-support, or dependent
  on unverifiable coupling assumptions.
- Causal attribution and multi-agent contribution allocation can be expensive,
  unstable, or misleading under model misspecification.
- Sparse tensors still require normalization and protected consumer
  projections; the architecture does not solve value aggregation.
- More conservative regret bounds can induce paralysis, while aggressive
  shaping can induce tampering, fixation, or proxy inversion.
- An append-only ledger conflicts with unrestricted retention; deletion,
  cryptographic erasure, tombstones, and downstream unlearning remain open
  implementation and governance problems.
- The actor/tribunal separation can fail through shared models, shared data,
  collusion, monoculture, credential compromise, or hidden common causes.
- The system has not been built, benchmarked, independently reviewed, or
  formally verified.

## Failure Modes

- Evidence suppression, log deletion, comparator poisoning, and hindsight
  leakage.
- World-model self-confirmation, evaluator capture, and false precision.
- Regret or specification laundering through actor-controlled objectives,
  weights, or adjudication.
- Excessive caution, opportunity paralysis, catastrophic fixation, and
  adversarial regret flooding.
- Double counting, proxy inversion, debt transfer, and recovery theater.
- Selective forgetting, memory poisoning, and repair overgeneralization.
- Nonstationary objectives or environments and collusive multi-agent
  attribution.

## Book Chapters Supported

| Chapter | Distinct contribution | Source locus | Boundary |
|---|---|---|---|
| `planning-as-a-control-layer` | Decision Capsule, comparator admissibility, prospective regret distributions, bounded probes, inaction symmetry, and recommendation stability. | Sections 5, 8-9, 17.2, 20.5 | No planner, counterfactual model, calibration, or decision-quality result. |
| `policy-optimization-and-learning-from-feedback` | Protected Regret Packet projections, feedback modes, root-cause routing, anti-tampering separation, update leases, and non-self-promotion. | Sections 10, 14-18 | No reward-quality, policy-improvement, or anti-tampering result. |
| `procedural-memory-and-cognitive-loop-closure` | Contrastive repair pairs, regret debt, regret-to-rule compilation, durable ratchets, protected counterexamples, and retirement. | Sections 11-12, 17.3-17.4 | No autonomous repair discovery, transfer, or recurrence reduction. |
| `data-engines-continual-learning-and-unlearning` | Five replay strata, recurrence/transfer priority, competence preservation, importance correction, and deletion-aware packet custody. | Sections 11, 13.4, 17.3 | No forgetting, unlearning, privacy, or learning advantage. |
| `artifact-graphs-audit-logs-and-replay` | Decision Capsule and Regret Packet event family, signatures, content addressing, supersession, appeals, and replayable transformations. | Sections 5.2, 13, 19.2-19.4 | Record completeness and receipt faithfulness remain untested. |
| `claim-ledgers-and-belief-revision` | Explicit boundary between incident-learning records and belief claims; monotone evidence history with defeasible conclusions. | Sections 13, 18.13 | A Regret Packet does not establish the truth of its counterfactual or root-cause conclusion. |
| `readiness-gates-residual-escrow-and-quarantine` | Learning-eligibility matrix, unresolved escrow, operational modes, bounded promotion, rollback, and quarantine. | Sections 14.5, 16.3, 17.5, 19.9 | No readiness thresholds or promotion efficacy are calibrated. |
| `governed-operations-incident-command-and-graceful-degradation` | Recovery regret, reaction/adaptation/constitutional clocks, evidence preservation, recovery non-erasure, and incident-to-learning handoff. | Sections 6.8, 15, 18.10, 20 | No deployed incident, containment, or recovery result. |
| `benchmark-ratchets-and-anti-goodhart-evidence` | Luck-versus-quality, paralysis, delayed-harm, coding-agent, continual-stream, tampering, multi-agent, and identifiability experiments with ablations and acceptance criteria. | Sections 21-23 | Proposed experiment program only; cited baselines remain unresolved until bibliography recovery. |
| `integrated-reference-architecture` | Four-plane service composition and the capsule-to-ledger-to-broker cross-layer join. | Sections 14, 17, 19 | No end-to-end Regret Engine or ASI Stack integration exists. |

## Chapter Decision

Update the ten existing owners above. Do not add a standalone Regret Engine
chapter now. The paper proposes an assurance and learning subsystem that
crosses already explicit layer boundaries; making it a new chapter would
duplicate planning, feedback, memory, evidence, readiness, and operations.
Reconsider only if an implementation produces a durable tribunal or
counterfactual-evaluation service whose lifecycle cannot be owned cleanly by
the existing chapters.

## Claims To Add Or Update

- Add decision-time fairness: later evidence may update outcome estimates but
  cannot make an unavailable or unauthorized comparator retroactively
  admissible.
- Add the Decision Capsule as the committed pre-action record required for
  retrospective policy-quality analysis.
- Add a typed Regret Packet as one governed feedback artifact, explicitly not a
  reward, evidence transition, or authority grant.
- Keep severity, causal contribution, foreseeability, feasibility, and learning
  eligibility separate so incidents route to the right repair owner.
- Add counterfactual surplus and competence-preservation examples so a repair
  program cannot improve its ledger by forgetting useful exploration.
- Add regret debt as a recurrence-weighted repair backlog, not a scalar actor
  objective.
- Add recovery non-erasure and the three-clock rule to incident learning.
- Add missingness monotonicity, comparator poisoning, and regret tampering to
  the anti-Goodhart test program.

## Proof And Test Backlog

- Mechanize a finite comparator-admission model covering decision-time
  information, authority, resources, causal feasibility, and no-hindsight.
- Prove finite authority non-expansion and non-self-adjudication across a
  capsule-to-packet-to-update transaction.
- Prove recovery non-erasure for append-only incident history while allowing
  defeasible conclusions and packet retirement.
- Encode a finite counterexample showing why one scalar cannot recover both
  hard-constraint precedence and root-cause routing.
- Build the proposed coding-agent pilot with isolated worktrees, exact replay,
  omitted-test comparators, hidden holdouts, and independent packet
  adjudication.
- Compare outcome-only, process-reward, uniform replay, scalar-regret, and full
  typed-packet conditions under matched opportunity and complete costs.
- Attack actor write access, comparator selection, scalar weights, evidence
  visibility, evaluator monoculture, and packet deletion separately.
- Measure false blame, false absolution, interval coverage, repeated-defect
  rate, protected-capability regression, paralysis, recovery time, tampering,
  and full compute/human burden.

These candidates should be rationalized against existing Lean targets before
adding new public proof tags; source intake alone does not justify expanding the
proof manifest.

## Open Questions

- Which comparator contracts remain tractable in partially observed,
  open-ended, multi-agent environments?
- How should the system preserve normative disagreement without creating an
  unusable tensor or laundering it through a scalar projection?
- Which evaluator-independence tests detect shared-model and shared-data common
  causes rather than merely distinct service names?
- Can regret-aware replay improve recurrence without inducing catastrophic
  fixation or reducing useful exploration?
- What evidence is sufficient to compile a recurring pattern into a rule rather
  than retain it as uncertain memory?
- How should privacy deletion alter packet reproducibility, derived rules,
  descendants, and support ceilings?
- Which parts of the three propositions belong in Lean, which require causal
  identifiability analysis, and which require empirical adversarial testing?
- Are the paper's novelty comparisons accurate after its unresolved citation
  keys are mapped to complete primary-source records?
