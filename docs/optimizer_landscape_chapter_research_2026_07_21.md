# Optimizer landscape chapter research — 2026-07-21

## Decision

The book has the correct owner but not yet the required optimizer depth.
`chapters/governed-model-training-distributed-optimization-and-scaling.qmd`
already owns the optimizer, scheduler, numerical policy, full training state,
distributed topology, checkpoint family, and qualified handoff as one governed
run transaction. It currently names none of AdamW, Muon, Shampoo, SOAP,
Adafactor, Lion, Sophia, schedule-free optimization, LARS, or LAMB, and its
seven-source packet concerns distributed execution, checkpointing, and
time-to-quality rather than optimizer mechanisms.

Add an optimizer-landscape section and evidence packet to that chapter. Do not
create a separate optimizer chapter. A separate owner would split an optimizer
algorithm from the run conditions that determine its meaning and would
duplicate the training chapter's existing contract.

This is a research and implementation plan. The sources below are proposed
intake records, not yet passage-reviewed inventory entries, and they support no
book claim until their notes, mappings, and non-authorities pass the normal
source-ingestion workflow.

## Question the section must answer

How should a governed training system choose, configure, compare, checkpoint,
resume, and replace an optimizer when optimizer behavior depends jointly on
model architecture, parametrization, objective, data order, batch regime,
schedule, precision, clipping, regularization, topology, communication, and
tuning budget?

The section must teach both the mechanisms and the decision discipline. It
must not reduce the subject to a catalog or declare a universal winner.

## Required taxonomy

| Family | Representative methods | Mechanism the chapter must explain | Governing tradeoff |
|---|---|---|---|
| Classical first order | SGD, momentum, Nesterov | Raw gradient descent, velocity, and look-ahead acceleration | Low state and simple semantics versus conditioning and tuning burden |
| Coordinate-wise adaptive | AdaGrad, RMSProp, Adam, AMSGrad, AdamW | Per-coordinate moment estimates, bias correction, denominator stabilization, and decoupled weight decay | Robustness and convenience versus state memory, scale behavior, and coupled hyperparameters |
| Memory- and layer-scaled | Adafactor, LARS, LAMB | Factored moments or layer-wise trust ratios | Reduced state or large-batch scaling versus approximation and layer-rule sensitivity |
| Tensor and matrix preconditioning | Shampoo, SOAP | Structure-aware preconditioners and Adam-like updates in a changing eigenbasis | Better conditioning versus inverse-root cost, state, approximation, and communication |
| Sign and discovered rules | Lion | Momentum-sign updates discovered through symbolic search | Low optimizer state and simple updates versus method-specific learning-rate and decay behavior |
| Curvature-aware | Sophia and representative diagonal or low-rank second-order methods | Periodic curvature estimation and clipped preconditioned updates | Fewer steps in some regimes versus estimator cost, stability, and approximation validity |
| Orthogonalized matrix updates | Muon and qualified variants | Momentum followed by approximate matrix orthogonalization, commonly with Newton–Schulz iterations | Matrix-aware update geometry versus parameter eligibility, approximation precision, distributed communication, and scaling rules |
| Schedule and averaging alternatives | Schedule-free methods | Coupling online iterates, averaging, and momentum without a stopping-time schedule | Less schedule dependence versus altered evaluation and checkpoint semantics |
| Architecture- and scale-aware theory | maximal-update parametrization, modular norm/Scion, natural-gradient, K-FAC, mirror/proximal and trust-region families | Width/depth transfer, module-specific geometry, invariant metrics, or constrained steps | Principled transfer or geometry versus assumptions, implementation complexity, and open-world validity |

Policy-gradient and preference-optimization families such as PPO, DPO, and
GRPO remain owned by `Policy Optimization and Learning from Feedback`. They
specify feedback objectives and policy-update procedures; they are not a
substitute for explaining the parameter optimizer that executes an update.

## Primary-source intake queue

The first pass should favor original papers and official implementations. Every
record needs passage-level notes, exact admissible claims, explicit
non-authorities, freshness metadata, and mappings to the training chapter and
any secondary consumer before chapter prose cites it.

| Proposed source ID | Primary source | Role | Mandatory non-authority |
|---|---|---|---|
| `ext_sgd_1951` | Robbins and Monro, *A Stochastic Approximation Method* | Historical stochastic-approximation foundation | Does not establish modern deep-network optimizer superiority |
| `ext_nesterov_acceleration_1983` | Nesterov, *A method of solving a convex programming problem with convergence rate O(1/k^2)* | Acceleration and look-ahead foundation | Convex rates do not transfer automatically to nonconvex foundation-model training |
| `ext_adagrad_2011` | Duchi, Hazan, and Singer, *Adaptive Subgradient Methods for Online Learning and Stochastic Optimization* | Coordinate-wise adaptation foundation | Regret and convex results are not open-world LLM guarantees |
| `ext_adam_2015` | Kingma and Ba, [Adam: A Method for Stochastic Optimization](https://arxiv.org/abs/1412.6980) | First- and second-moment adaptive baseline | Original experiments and analysis do not make Adam universally best |
| `ext_amsgrad_2018` | Reddi, Kale, and Kumar, [On the Convergence of Adam and Beyond](https://openreview.net/forum?id=ryQu7f-RZ) | Adam failure construction and AMSGrad remedy | A convergence counterexample does not imply every practical Adam run fails |
| `ext_adamw_2019` | Loshchilov and Hutter, [Decoupled Weight Decay Regularization](https://openreview.net/forum?id=Bkg6RiCqY7) | Separates adaptive gradient updates from weight decay | Reported generalization gains are setting-bound and do not prove universal superiority |
| `ext_adafactor_2018` | Shazeer and Stern, [Adafactor: Adaptive Learning Rates with Sublinear Memory Cost](https://arxiv.org/abs/1804.04235) | Factored second moments, update clipping, and state-memory reduction | Factorization is an approximation and is not equally applicable to every parameter shape |
| `ext_lars_2017` | You, Gitman, and Ginsburg, [Large Batch Training of Convolutional Networks](https://arxiv.org/abs/1708.03888) | Layer-wise scaling for large-batch training | ImageNet/CNN evidence is not direct LLM evidence |
| `ext_lamb_2020` | You et al., [Large Batch Optimization for Deep Learning: Training BERT in 76 minutes](https://openreview.net/forum?id=Syx4wnEtvH) | Layer-wise adaptive moments and large-batch scaling | Time-to-target is hardware-, batch-, model-, and tuning-bound |
| `ext_shampoo_2018` | Gupta, Koren, and Singer, [Shampoo: Preconditioned Stochastic Tensor Optimization](https://proceedings.mlr.press/v80/gupta18a.html) | Tensor-structured preconditioning | Convex theory and reported experiments do not settle modern distributed cost-benefit |
| `ext_lion_2023` | Chen et al., [Symbolic Discovery of Optimization Algorithms](https://arxiv.org/abs/2302.06675) | Lion, optimizer search, and sign-momentum updates | Source-reported gains and search transfer are task- and budget-bound |
| `ext_sophia_2023` | Liu et al., [Sophia: A Scalable Stochastic Second-order Optimizer for Language Model Pre-training](https://arxiv.org/abs/2305.14342) | Diagonal curvature estimation and clipped second-order updates | Reported language-model speedups require matched reproduction before generalization |
| `ext_soap_2024` | Vyas et al., [SOAP: Improving and Stabilizing Shampoo using Adam](https://arxiv.org/abs/2409.11321) | Adam in Shampoo's evolving eigenbasis | Reported pretraining gains do not erase preconditioner overhead or tuning dependence |
| `ext_schedule_free_2024` | Defazio et al., [The Road Less Scheduled](https://arxiv.org/abs/2405.15682) | Schedule-free optimization and iterate averaging | Removing a stopping-time schedule does not remove all learning-rate or evaluation choices |
| `ext_mup_2022` | Yang et al., [Tensor Programs V: Tuning Large Neural Networks via Zero-Shot Hyperparameter Transfer](https://arxiv.org/abs/2203.03466) | Maximal-update parametrization and widthwise hyperparameter transfer | Transfer depends on the prescribed parametrization and does not establish arbitrary architecture transfer |
| `ext_modular_norm_2024` | Large et al., [Scalable Optimization in the Modular Norm](https://arxiv.org/abs/2405.14813) | Modular geometry and width/depth learning-rate transfer | Theoretical and experimental scope does not establish universal optimizer choice |
| `ext_muon_scalable_2025` | Liu et al., [Muon is Scalable for LLM Training](https://arxiv.org/abs/2502.16982) | Large-scale Muon, weight decay, per-parameter update scaling, and distributed implementation | The reported compute-efficiency result is source-reported and configuration-bound |
| `ext_muon_spectral_norm_2026` | Bernstein and Newhouse, [Muon Optimizes Under Spectral Norm Constraints](https://openreview.net/forum?id=Blz4hjxLwU) | Accepted theoretical interpretation of Muon with decoupled decay | An implicit-regularization account does not prove task-level superiority or safety |
| `ext_muon_inexact_2026` | *Beyond the Ideal: Analyzing the Inexact Muon Update* | Newton–Schulz approximation precision and optimizer hyperparameter coupling | Analysis of inexact updates does not identify a universally adequate iteration count |
| `ext_muon_block_periodic_2026` | [MuonBP: Faster Muon via Block-Periodic Orthogonalization](https://openreview.net/forum?id=mHouLSUQP5) | Communication-aware approximate orthogonalization | A variant's reported scale result does not transfer to arbitrary topology or model |

The source packet should also include one primary treatment of natural gradient
and one of K-FAC, plus current official framework implementations for the exact
semantics used in any executable comparison. Recent workshop or under-review
papers may be used as freshness and challenge sources but must be labeled by
review state and cannot outrank stable primary foundations.

## Chapter section design

1. **Optimizer choice is a run-policy choice.** Extend the Training Run
   Contract so optimizer family, implementation/version, parameter eligibility
   and groups, state dtype, epsilon, decay semantics, clipping, schedule,
   warmup, batch arithmetic, accumulation, loss scaling, and approximation
   settings are identity-bearing fields.
2. **Mechanism map.** Explain the taxonomy using common notation and compare
   state, update geometry, invariances, eligible tensor shapes, compute,
   communication, and failure modes. Avoid an encyclopedic list with no
   decision consequences.
3. **AdamW as the modern reference baseline.** Explain moments, bias
   correction, decoupled decay, parameter exclusions, state memory, and why an
   implementation called AdamW is not fully specified by its name.
4. **Structure-aware alternatives.** Compare Adafactor, Shampoo, SOAP, Sophia,
   and Muon by what structure they approximate and what extra state or
   computation they require. Explicitly describe Muon's matrix eligibility,
   orthogonalization approximation, common fallback optimizer for embeddings
   and scalar/vector parameters, and distributed communication implications.
5. **Scaling and transfer.** Relate LARS/LAMB, maximal-update
   parametrization, and modular-norm methods to batch, width, depth, module,
   and architecture transfer. Separate optimizer transfer from parametrization
   transfer.
6. **Scheduling is part of the optimizer policy.** Compare warmup and decay,
   constant and cosine schedules, schedule-free methods, early stopping, and
   checkpoint evaluation semantics.
7. **Governed selection protocol.** Specify the matched design, competence
   gates, rescue ladder, reporting matrix, and inference ceilings below.
8. **RSI and substrate abstraction.** The stack may admit new optimizer
   families through the same contract, but self-modification must create a new
   versioned run policy and earn qualification. Architectural self-improvement
   does not permit silent optimizer substitution.

## Competent comparison and argument-exit protocol

An optimizer result is admissible only after a prospective comparison freezes:

- model graph, initialization and parametrization; data identities and order;
  token/example budget; objective; precision; batch and accumulation; hardware
  and distributed topology; stopping rule; evaluation cadence; and fault
  policy;
- a defensible implementation for every arm, including correct parameter
  groups and method-specific settings, with unit tests against a trusted
  reference where one exists;
- equal or explicitly accounted tuning budgets, a prospectively frozen search
  space, at least three independent seeds, and a fair method-specific rescue
  ladder before a negative classification;
- strong baselines: at minimum tuned AdamW and tuned SGD/momentum where
  applicable, plus the simplest plausible schedule or parametrization
  alternative that could explain the gain;
- unopened final evaluation, independent evaluator implementation, raw traces,
  attempted-run denominator, failed and diverged runs, full checkpoint state,
  and exact environment and source identities; and
- tests at more than one meaningful scale or a narrow claim explicitly bounded
  to the single tested regime.

Report the joint outcome rather than a single best validation loss:

| Dimension | Required measurement |
|---|---|
| Progress | tokens, examples, optimizer steps, wall time, and energy to prospectively frozen quality thresholds |
| Final result | loss, task quality, calibration, robustness, downstream transfer, and retained capabilities |
| Resources | peak accelerator memory, optimizer-state bytes, FLOPs or measured compute, communication volume/time, and storage |
| Stability | divergence, overflow/underflow, gradient/update norms, sensitivity, seed variance, and failed-run denominator |
| Tuning | number and cost of trials, search space, selected configuration, and sensitivity around it |
| Scaling | batch-, width-, depth-, architecture-, duration-, and topology-transfer behavior where claimed |
| Recovery | complete state inventory and uninterrupted-versus-resumed equivalence under the declared equivalence class |
| Governance | instrumentation, checkpoint, evaluator, operator, rollback, and lifecycle cost |

## Claim and negative-inference ceilings

- A source-reported speedup is evidence about that source's configuration, not
  proof that the optimizer is globally faster or better.
- A convergence theorem establishes its stated assumptions and consequence; it
  does not establish open-world foundation-model quality, robustness, safety,
  or cost.
- A lower training loss, fewer steps, or a successful checkpoint load alone
  does not establish better downstream behavior or faithful resume.
- Failure of a naive, under-tuned, incorrectly grouped, or resource-starved arm
  is N0–N2 evidence about that attempt, not a refutation of the optimizer.
- A win at one model size, architecture, dataset, batch regime, or topology
  cannot support a scale- or substrate-general claim.
- Muon approximation precision, matrix eligibility, fallback rules, update
  scaling, and communication are part of the optimizer identity, not removable
  implementation details.
- Optimizer selection creates no automatic safety, governance, readiness,
  release, RSI, or ASI claim.

## Ownership and handoffs

| Consumer | Receives | Does not receive |
|---|---|---|
| Resource Economics | End-to-end compute, memory, communication, energy, tuning, recovery, and operator costs | Authority to choose a lower-cost optimizer regardless of quality or safety |
| Replaceable Cognitive Substrates | Architecture- and module-specific optimizer eligibility and transfer evidence | A claim that one optimizer spans all substrates |
| Policy Optimization and Learning from Feedback | Exact parameter optimizer and state used to execute a governed policy update | Ownership of base-training optimizer mechanisms |
| Data Engines and Privacy/Data Rights | Data-order, sampling, clipping, and privacy-mechanism interactions such as DP-SGD | Permission to infer privacy from ordinary gradient clipping |
| Benchmark Ratchets | Frozen qualification tasks, independent evaluation, and anti-Goodhart controls | Permission for validation data to select checkpoints or optimizer settings |
| Artifact/Weight Custody | Complete optimizer/checkpoint family and derivation identity | Proof that a loadable artifact faithfully resumes or deserves release |

## Terminal artifacts

This optimizer-depth amendment is terminal only when all of the following agree:

1. passage-reviewed source inventory entries and source notes;
2. a chapter mechanism matrix, decision protocol, failure modes, handoffs, and
   explicit non-claims;
3. claim atoms with falsifiers, acceptance criteria, promotion ceilings, and
   evidence-plan routes;
4. a versioned optimizer-policy schema or extension to the governed training
   run contract, with valid fixtures and negative mutations;
5. a preregistered matched-comparison protocol and executable implementation
   self-tests; execution may remain resource-gated and cannot be replaced by a
   toy result;
6. reader projection, glossary/source-appendix reconciliation, registered
   validation, and local render checks; and
7. an exact receipt stating support and release effects. Planning, citation,
   formal records, fixtures, or protocol readiness alone have effect `none`.
