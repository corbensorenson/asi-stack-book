# Reflexive Model-World Systems: When Representations Become Causes

- **Source ID:** `reflexive_model_world_systems`
- **Author:** Corben Sorenson
- **Date:** August 2026
- **Class:** Author research preprint with formal propositions and reproducible toy simulations
- **Exact manuscript:** `papers/source/reflexive_model_world_systems.md`
- **Archived package:** `sources/raw/corben_papers/reflexive_model_world_systems/reproducibility_package_v1_0/`
- **Exact Markdown SHA-256:** `6b30990f2d22d409b1f0e5823f7aef41b5de6040a5c63bb74b5ca6e39c7a95e9`
- **Exact Markdown bytes:** 99,480
- **Package contents reviewed:** Markdown, DOCX metadata, simulation and replot scripts, raw per-seed CSV outputs, summary CSV/JSON, run log, seven figures, requirements, README, and checksum file
- **Local reproduction status:** Not reproduced during intake. The first local rerun stopped before any simulation because `scikit-learn` was unavailable. The supplied result files and checksums remain source-reported package artifacts, not locally reproduced evidence.

## Thesis

A consequential model can alter the world, measurement process, preferences, institutions, and evidence streams from which its successors learn. The relevant object is then an evolving model-world loop rather than a model observing an exogenous world. A governed model lineage is reflexively closed over a horizon when one of its deployments causally changes evidence later used to update a successor in that lineage.

## Distinct contribution to the book

The existing world-model chapter governs imagination as a fallible prediction service and reconciles predictions against observations. RMWS exposes a deeper failure: the observation stream may itself be a descendant of prior model deployment. It therefore owns a distinct causal interface among deployment, world and regime state, evidence generation, model lineage, and successor update.

This warrants a dedicated technical chapter after `Governed World Models and Reality Grounding`. The Human Reader should deepen Unit 11 and connect the consequences to Units 21 and 25 rather than add a new unit.

## Mechanisms mined

1. **Lineage-relative reflexive closure.** Define model identity through governed succession, not weight similarity, and require an intervention difference in a future evidence channel used by a successor.
2. **Eight-channel audit signature.** Track state/features, outcomes/labels, exposure/sampling, measurement, preferences/utilities, ontologies/categories, institutions, and model ecology. The channels imply different estimands and controls and should not be collapsed into generic distribution shift.
3. **Model-descended evidence.** Classify evidence by causal ancestry rather than human-versus-synthetic origin. Human-origin data selected through model influence can be descended; synthetic data generated independently of the lineage can be an anchor.
4. **Query-relative descendancy.** Evidence can be descended for one question and effectively independent for another. Provenance must name lineage, horizon, admissible deployment class, target query, identification method, and uncertainty.
5. **Grounding reserve.** Protect informative evidence channels approximately invariant to admissible lineage interventions. Independence without information is useless; informative evidence without independence may identify only the deployed regime.
6. **Reflexive debt.** Record the widening set of baseline worlds compatible with available logs when deployment erases counterfactual variation, exposure history, measurement changes, or unaffected comparison groups.
7. **Epistemic capture.** A lineage can improve on-policy calibration while losing the ability to estimate pre-deployment or alternative-policy worlds.
8. **Self-inclusive state.** When model state changes the world's transition law, world state alone need not be Markov; the joint state must include the model and relevant regime.
9. **Loop stability.** Local stability depends on the spectral radius of the coupled world-model Jacobian. Stable convergence is not normative desirability.
10. **Counterfactual-label mismatch.** A successful intervention can make the observed outcome diverge from the no-intervention target, causing naive retraining to learn the wrong risk.
11. **Diversity contraction and model ecology.** Broad optimization toward a shared low-dimensional target contracts diversity in the stated toy model; multiple lineages can preserve niches or instead synchronize, race on proxies, dominate, or collapse a shared evidence commons.
12. **Institutional hysteresis.** Removing or rolling back a model does not restore categories, incentives, preferences, or institutions altered by deployment.
13. **Trajectory-level evaluation.** Separate baseline fidelity, on-policy fidelity, causal steering utility, and legitimacy. High accuracy on the world a model helped create is not independent validation.
14. **Reflexive alignment.** Govern acceptable model-world trajectories, including evidence, preferences, institutions, and successor systems, rather than only a frozen model or immediate action.

## Primary chapter routing

- `reflexive-model-world-systems` — primary owner of reflexive closure, the eight-channel audit, model-descended evidence, grounding reserves, reflexive debt, trajectory evaluation, and persistence-aware rollback.
- `governed-world-models-and-reality-grounding` — hands off model predictions and deployment effects; consumes self-inclusive state and distinguishes observation from lineage-independent grounding.
- `data-engines-continual-learning-and-unlearning` — records action exposure, evidence ancestry, target regime, and descendant propagation in training inputs.
- `artifact-graphs-audit-logs-and-replay` — extends ordinary transformation lineage with causal ancestry and deployment exposure.
- `benchmark-ratchets-and-anti-goodhart-evidence` — owns reflexive benchmarks, randomized probes, shadow policies, causal estimands, and anti-capture evaluation.
- `multi-agent-dynamics-collective-intelligence-and-systemic-risk` — consumes the reflexive evidence-commons and cross-lineage externality matrix.
- `human-ai-communication-persuasion-and-epistemic-security` and `governed-objective-formation-value-learning-and-goal-integrity` — consume preference formation, manipulation, ontology change, and the difference between learning preferences and causing them.
- `institutions-international-coordination-and-public-legitimacy` and `ai-deployment-transition-distribution-and-human-agency` — consume institutional persistence, legitimacy, adaptation burden, contestability, and socio-technical rollback.
- `recursive-self-improvement-boundaries` and `open-ended-improvement-engines` — consume lineage-bound evaluator independence, protected grounding, and the prohibition on widening authority from self-descended evidence alone.
- `regret_engine` consumers, especially `planning-as-a-control-layer` and `policy-optimization-and-learning-from-feedback`, should distinguish observed on-policy regret from counterfactual regret.
- `integrated-reference-architecture` — locates the reflexive-system audit around deployment, observation, evidence, retraining, and successor admission.

## Formal and experimental evidence

The paper states six propositions under explicit assumptions: augmented-state necessity, local linear stability, counterfactual-label mismatch, contraction under a common target, single-history non-identifiability, and institutional hysteresis. These should be treated as scoped mathematical arguments until independently mechanized or checked.

The package reports three deterministic toy campaigns:

- 60-seed norm/appearance coevolution with common-score contraction and a plural-model condition;
- 35-seed self-negating decision support comparing naive and causal-aware retraining; and
- 60-seed recursive evidence ancestry comparing independent real, independent synthetic, model-generated, model-selected human-origin, and replacement regimes.

The supplied data, code, figures, and checksums make those source-reported runs inspectable. Intake did not reproduce them because the local environment lacked `scikit-learn`; therefore the book may report them only as source-reported mechanistic demonstrations, not as locally reproduced or externally validated findings.

## Failure modes and strongest objections

- The framework may be a relabeling of performative prediction or cybernetics unless its decomposition changes estimands and controls.
- Descendancy may be unidentifiable without randomization, instruments, variation, or structural assumptions.
- Eight channels may be incomplete or too coarse.
- Local stability says little about global nonlinear regimes, rare transitions, or normative outcomes.
- Grounding reserves can remain independent while becoming stale or uninformative.
- Multiple models can synchronize or escalate a proxy arms race instead of preserving pluralism.
- The simulations are stylized and do not estimate real social, medical, institutional, or frontier-model effects.
- No technical formalism resolves the legitimacy of preference influence or distribution of performative power.

## Proof and implementation opportunities

- Lean: world state is insufficient when two equal external states with different model states yield different next-state distributions in a finite model.
- Lean: bounded common-target updates contract pairwise differences; model rollback alone does not imply restoration of a persistent institutional state.
- Project Theseus: implement a lineage manifest, time-unrolled causal graph, evidence-ancestry record, grounding-reserve contract, target-regime field, and persistence-aware rollback dossier.
- Test: rerun the three simulations in a pinned environment, verify exact summaries or explain drift, then add intervention and ablation controls.

## Support-state disposition

`argument` for the chapter architecture. The source-reported toy results may be described with explicit source attribution and limits, but no local synthetic-test-backed or empirical promotion is accepted during intake.
