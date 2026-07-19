# P4/M8 Campaign 5 — Situated World-Model Acquisition and Memory Consolidation

Date closed: 2026-07-16  
Run ID: `p4-m8-finite-pomdp-world-model-001`  
Disposition: `bounded_non_core_promotion_accepted`  
New chapter: no

## Decision

Campaign 5 earns one narrow `synthetic-test-backed` non-core transition. In two
finite authored partially observable simulators, a governed Bayesian
count-table agent maintained persistent entity identity, separated observation
from belief, kept multiple hypotheses live, gathered information, used one
bounded diagnostic intervention, gated uncertain or shifted cases, preserved
episode and consolidation lineage, and supported exact serialized replacement
and rollback probes. Under the frozen comparison, it exceeded the reactive
baseline on hidden-state estimation in both environments, did not exceed the
ungoverned predictive baseline's unsafe-action rate, stayed within 0.10 task
success of the best baseline in both environments, and produced all six
prospectively directional aggregate ablation signatures.

This is not a chapter-core promotion and not evidence for a neural world model,
open-world causal understanding, developmental learning, general transfer,
deployment safety, simulator realism, SOTA, AGI, or ASI. It establishes only
the behavior of the recorded finite architecture and scoring contract.

## Frozen contract and lineage

The design was frozen before any episode or outcome. The builder prohibited a
rewrite once raw or result artifacts existed; the preregistration prohibited
outcome-aware retry and simulator repair after outcome. The runner and
independent evaluator refused code, design, environment, or result-schema hash
drift.

| Artifact | SHA-256 |
|---|---|
| `design.json` | `8054219e2aaa7b97a2146c8e216eacb4cf5dd8a018fe11c2d4991448a3e9e71a` |
| `environments.json` | `d762c6e530091e0103ea7ae250268cfe60da66a30d1a40beda683dfd89f1ea33` |
| `preregistration.json` | `b92608df9d9dd3cab83a9d1a179bd1307999339a046345a40fb8f0c6052ff69b` |
| `campaign_run.json` | `6350521526b2f58236367e62527c5b67df7c564635005afeb72c03ba62fafd1f` |
| `confirmatory_result.json` | `ba1039167a898b08607213aa007b268918a305af2cd0479ed66b4c6315deaa67` |
| result schema | `15e448b62dcc34720fbf6f0e75391f5c09e4b0c5819cef85f13d8fca4e443568` |

The frozen denominator was 11,250 episodes: two environments, five seeds, ten
arms, 105 curriculum episodes per seed/arm across the two environments, and
120 held-out episodes per seed/arm across the two environments. The held-out
denominator was 6,000 episodes. The raw trace is stored compactly because it
contains the full artifact record for every episode and would otherwise add
formatting bytes without evidence value.

## Environments and declared transfer boundary

`adaptive_workshop` modeled four persistent machine cells. Its probes were
vibration, thermal state, and alignment; its controlled intervention was a
reversible low-power diagnostic pulse; its terminal actions were continue,
recalibrate, or isolate-and-service. The shift changed the thermal sensor.

`service_mesh_transfer` modeled four persistent service artifacts. Its probes
were latency, trace shape, and cache state; its controlled intervention was a
disposable canary bypass; its terminal actions were keep-route,
refresh-local-state, or isolate-dependency. The shift changed the latency
sensor. Its transition matrix, sensor distributions, intervention response,
action vocabulary, and entity semantics differed from the workshop.

The only shared abstraction was the declared three-state interface:
`nominal`, `recoverable`, and `blocked`. Success in the second authored domain
therefore tests reuse of the governed interface, not zero-shot transfer of a
learned model or representation.

## Compared paths

The campaign compared:

1. reactive/no-world-model behavior;
2. transcript memory;
3. an ungoverned predictive count-table model;
4. the governed world-model path;
5. no active information gathering;
6. no controlled intervention;
7. no observation–belief separation;
8. no uncertainty gate;
9. no consolidation; and
10. no quiescent stabilization.

All arms used the same hidden trajectories per environment and seed and the
same declared ceilings: no more than three information actions, one bounded
intervention, and 1,000 compute-proxy units per episode. Reference state was
available only to the evaluator and post-effect learning.

## Held-out result

| Environment | Arm | Hidden-state accuracy | Task success | Unsafe action | Mean Brier |
|---|---|---:|---:|---:|---:|
| Workshop | reactive | 0.4500 | 0.4500 | 0.5500 | 0.6667 |
| Workshop | transcript | 0.7767 | 0.7767 | 0.2233 | 0.3465 |
| Workshop | ungoverned predictive | 0.7667 | 0.7667 | 0.2333 | 0.3457 |
| Workshop | governed | 0.7933 | 0.7433 | 0.1000 | 0.2689 |
| Service mesh | reactive | 0.4067 | 0.4067 | 0.5933 | 0.6667 |
| Service mesh | transcript | 0.6533 | 0.6533 | 0.3467 | 0.4300 |
| Service mesh | ungoverned predictive | 0.7267 | 0.7267 | 0.2733 | 0.4110 |
| Service mesh | governed | 0.7967 | 0.6967 | 0.1133 | 0.3229 |

Across five seeds, governed hidden-state accuracy was 0.7933 (95% CI
0.7151–0.8716) in the workshop and 0.7967 (0.7495–0.8438) in the service mesh.
The governed path traded some task completion for escalation: versus the
ungoverned predictive arm, task success was lower by 0.0233 and 0.0300, while
unsafe action was lower by 0.1333 and 0.1600. This is a measured trade, not a
free improvement.

Shift detection remained weak: 0.1667 in the workshop and 0.2200 in the service
mesh, with false-shift-alarm rates of 0.1467 and 0.1600. Intervention-effect
prediction was 0.5999 and 0.6470. These values sharply limit any claim of robust
anomaly detection or causal understanding.

## Causal ablations

The preregistered promotion gate required at least four of six aggregate
directional signatures; all six passed under their frozen cross-environment
definitions.

| Removed mechanism | Workshop effect | Service-mesh effect | Frozen aggregate direction |
|---|---:|---:|---|
| Active information | governed accuracy minus ablation = -0.0067 | +0.0367 | positive mean; mixed by environment |
| Intervention | governed accuracy minus ablation = +0.0267 | +0.0700 | positive |
| Observation–belief separation | ablation minus governed Brier = +0.0969 | +0.1203 | positive |
| Uncertainty gate | ablation minus governed unsafe rate = +0.1033 | +0.0833 | positive |
| Consolidation | governed accuracy minus ablation = +0.0367 | +0.0700 | positive |
| Quiescence | ablation minus governed silent rewrites = +34 | +44 | positive |

The active-information signature is deliberately reported as mixed: it was
slightly harmful in the workshop and helpful in the service mesh. Passing the
predeclared mean-direction gate does not erase that heterogeneity.

## Memory and identity receipts

Every governed held-out row preserved exact entity binding between evaluator
reference, episode identity, and agent input. An entity-conditioned prior was
used on every governed held-out row. These checks establish identity plumbing,
not learned object permanence.

The governed path created a mean of six consolidation versions per workshop
run and four per service-mesh run. Every consolidation carried supporting and
contradicting episode references, a supersession edge after version one, and a
rollback snapshot. Across the ten governed runs:

- serialized replacement matched exactly in 10/10;
- rollback to the selected snapshot matched exactly in 10/10;
- detached abstractions: 0;
- missing contradiction fields: 0;
- lineage breaks: 0; and
- silent rewrites outside quiescent consolidation: 0.

Removing quiescence produced 34 and 44 silent rule rewrites across the five
seeds in the two environments. Removing consolidation reset predictive tables
at the frozen boundaries and reduced held-out accuracy in both environments.
These are finite implementation effects, not proof that this consolidation
policy is optimal for neural or open-ended systems.

## Promotion review and chapter ownership

The separate review accepts one bounded non-core transition:
`situated-world-model.finite-pomdp-governed-acquisition-and-consolidation` moves
from `argument` to `synthetic-test-backed`. The transition covers the exact
finite run, artifact separation, integrity gates, baseline comparisons, causal
ablation signatures, and replacement/rollback receipts.

The new-chapter gate does not pass. The observed interfaces are important but
already have clear owners:

- **Planning as a Control Layer** owns hidden-state belief, prediction,
  intervention, planning action, uncertainty escalation, and shift residuals.
- **Replaceable Cognitive Substrates Beyond Transformer Monoculture** owns the
  typed observation/world/belief/prediction interface and the requirement that
  different internals share the same governed operational shell.
- **Procedural Memory and Cognitive Loop Closure** owns quiescent consolidation,
  support and contradiction lineage, replacement, rollback, and retirement.
- **Benchmark Ratchets and Anti-Goodhart Evidence** owns matched baselines,
  ablations, multi-seed uncertainty, frozen gates, and heterogeneity reporting.

A separate developmental-world-model chapter would duplicate these owners and
invite anthropomorphic claims the evidence cannot support.

## Claim ceiling

This campaign does not establish neural representation learning, a learned
latent dynamics model, language-model improvement, natural-task usefulness,
open-world object permanence, human developmental equivalence, general causal
reasoning, counterfactual validity outside the authored tables, reliable shift
detection, simulator adequacy, sim-to-real transfer, embodied competence,
production safety, security, privacy, autonomous authority, SOTA, AGI, ASI,
publication readiness, release readiness, or any chapter-core claim.

The narrow positive lesson is architectural: in these two finite environments,
the governed interface was executable and causally legible. Observation,
belief, prediction, intervention, effect, and consolidation were separable;
uncertainty gating reduced unsafe action at a measurable task-success cost; and
quiescent, versioned consolidation avoided silent rewrites while retaining
exact replacement and rollback receipts.
