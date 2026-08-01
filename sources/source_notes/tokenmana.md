# Source Note: TokenMana

| Field | Value |
|---|---|
| Source ID | `tokenmana` |
| Source title | TokenMana: Regenerative Capacity and Temporal Elasticity Papers |
| Ingestion date | 2026-06-24 |
| Full-fidelity review | 2026-07-31 |
| Source version / URL | Google Docs source in inventory: https://docs.google.com/document/d/1dGOlGPZi6byTwRUbHQt40OSErBnQ4j6G_BZvA-oJRM8 |
| Ingestion basis | Complete local raw cache inspected at `sources/raw/google_docs/tokenmana.txt` (1,269 lines; approximately 7,996 words). Raw text is not published. |
| Evidence role | Corben-authored mechanism-design and human-outcomes research lineage; no reproduced theorem, simulation, pricing experiment, or human study. |

## Thesis

TokenMana contains two linked proposals. The infrastructure proposal replaces
periodic all-at-once quota resets with a bounded capacity stock that regenerates
over time, permits limited bursts, and may interact with load-sensitive price
updates. The human proposal treats the temporal shape of access as choice
architecture: reset cliffs and deadlines may concentrate AI-assisted work,
shift it toward night hours, and externalize cost into fatigue, rework, or
sleep disruption. A responsible resource policy must therefore account for
load, task utility, quality, fairness, human time, health-sensitive privacy,
verification capacity, and displaced costs rather than optimizing token
throughput or provider margin alone.

These are testable hypotheses and mechanism candidates. The paper's theorem
labels do not contain full proofs, and the causal pathway from quota design to
sleep or productivity has not been measured.

## Version and correction lineage

The cache contains five tabs but two substantive paper families:

| Family | Draft progression | Controlling version |
|---|---|---|
| Regenerative Capacity Mechanisms for Load-Stable Token Pricing | Initial paper 1; revised paper 1 in tab 3; public release in tab 4 | Tab 4 v1.0, which acknowledges informal existence and variance proofs, reduced-form convex cost, remaining deadline peaks, no provider competition, and future empirical work. |
| Temporal Elasticity of API Access and Cognitive Efficiency | Initial paper 2; shorter revision in tab 3; public release in tab 5 | Tab 5 v1.0, which narrows universal causal language, cites sleep and staggered-adoption literature, defines observable proxies, and foregrounds privacy, selection, confounding, and measurement error. |

Repeated equations and claims across drafts are correction history, not
independent evidence.

## Mechanisms

### Regenerative capacity

- Give an account or workload a versioned capacity state with regeneration
  rate, maximum stock, bounded service or burst rate, permitted debt, expiry,
  priority, transfer rules, protected floors, and current balance.
- Make issuance and consumption auditable. A regenerated credit is permission
  to request a resource under current policy, not guaranteed compute, evidence,
  action authority, monetary value, or an exemption from safety and review.
- Compare periodic reset, ordinary token-bucket, pay-as-you-go, static rate
  limit, staggered quota, reservation, queue-based admission, and regenerative
  policies against the same arrival process and task-value distribution.
- Separate deterministic synchronization introduced by policy from external
  deadlines, correlated releases, outages, common price signals, retries,
  time zones, and strategic users. Removing one reset cliff does not eliminate
  peaks.
- If prices respond to load, bind observation window, estimator, delay,
  elasticity model, smoothing, caps, anti-oscillation policy, fairness,
  notification, appeal, and fallback. Load feedback can itself synchronize or
  exclude users.

### Temporal elasticity and human consequences

- Record the temporal access contract: renewal cadence, discontinuities,
  accrual, expiration, burst and concurrency rules, throttling, price changes,
  notification timing, predictability, and deadline interaction.
- Treat renewal clustering and nocturnal usage as behavioral observations, not
  proof of sleep loss or harm. Distinguish time zones, user-chosen schedules,
  caregiving, multiple jobs, incidents, product releases, and other deadlines.
- Measure useful task outcomes and repair burden rather than calling token
  volume productivity. Candidate friction measures include rework loops,
  repeated correction, build/test failures, delayed completion, reviewer load,
  and self-reported workload, each with construct-validity limitations.
- Study any sleep pathway with explicit consent, data minimization, purpose
  limitation, short retention, deletion/export, separation from employers and
  performance management, no medical inference, participant withdrawal, and
  independent ethics oversight where applicable.
- Prefer randomized or prospectively staggered plan changes when legitimate;
  otherwise preserve selection, interference, concurrent product changes,
  pre-trends, seasonality, differential attrition, time zones, and deadline
  confounding. Shared capacity and load-based prices create spillovers that can
  violate ordinary no-interference assumptions.

## Interfaces and invariants

`resource-economics-and-token-budgets` owns regenerative capacity, temporal
access contracts, protected floors, displaced costs, and joint accounting.
Human Factors owns reviewer fatigue and control capacity; Physical Compute owns
real infrastructure and environmental bottlenecks; Policy Optimization owns
feedback changes; Benchmark Ratchets owns evaluation; deployment and
distribution chapters own access fairness and institutional consequences.

Invariants are: resource credits create no authority; protected safety,
verification, rights, and review floors survive scarcity; utilization smoothing
does not prove useful work; cost reduction does not prove welfare or fairness;
human time and health-sensitive data are not free telemetry; no employer or
platform may infer individual impairment from a pricing experiment; failed,
deferred, shifted, or abandoned work stays in the denominator; and rollout
effects cannot exceed the identification design.

## Evidence

The source provides equations, informal proof roadmaps, comparative predictions,
an implementation mapping, an empirical design, operational measures, and
ethics language. It supplies no technical proof appendix, mechanized theorem,
simulation code, synthetic run, billing trace, production load data, pricing
experiment, queue model, customer behavior, sleep record, wearable data,
human-subjects protocol approval, productivity labels, or independent
replication. Its later external references are leads for separate primary-
source review and do not automatically validate the paper's model.

## Mathematical and causal audit

- The continuous stock equation requires explicit behavior at the upper bound
  (spill, reflection, or stopped regeneration). Without it, positive
  regeneration can violate `M <= P`.
- A usage rate bounded directly by a stock has a units problem unless time is
  normalized or the withdrawal constraint is defined over an interval. A
  service-rate cap and nonnegative stock trajectory should be separate.
- Compact controls and continuous payoffs are not, by themselves, a complete
  stationary Markov perfect equilibrium proof for a hybrid continuous-time,
  discrete-price, continuum-user game. State transitions, correspondence,
  measurability, discount horizon, boundary behavior, and provider strategy
  need precise conditions.
- Continuous stock dynamics and bounded controls exclude Dirac-like unlimited
  impulses, but they do not automatically make every optimal control path
  absolutely continuous or eliminate jumps.
- Strict variance dominance does not follow from removing reset discontinuity
  alone. Quota users need not concentrate usage, while common deadlines,
  prices, notifications, identical accrual, coordinated jobs, or burst caps can
  synchronize RCM users. Variance needs an exact process, horizon, stationarity,
  and comparator policy.
- The local stability expression is an illustrative linearization, not a full
  stability theorem. Delay, saturation, estimation noise, price floors/caps,
  strategic response, and multi-step feedback can change the dynamics.
- Conditional on equal mean load and a quadratic convex cost, lower variance
  lowers expected cost. “Profit dominance” additionally requires revenue,
  demand, price, churn, service quality, and implementation cost; it does not
  follow from cost variance alone.
- The sleep pathway is plausible but not identified by the structural model.
  Renewal timing, deadlines, work intensity, nocturnal share, sleep, and
  friction can be jointly caused or selected.
- A staggered rollout with shared infrastructure or load-sensitive prices may
  violate no-interference assumptions. A renewal-boundary discontinuity may
  also mix time trends and strategic timing. Causal claims require design-
  specific identification and robustness.
- Near-duplicate prompts, test failures, and corrections are noisy workflow
  measures, not direct cognitive or medical outcomes.

## Failure Modes

- Regenerative credits become an addictive progress mechanic, artificial
  scarcity, dark pattern, or inducement to remain online.
- A common accrual rate, price signal, notification, or expiry creates a new
  synchronized boundary.
- Burst debt accumulates, rolls over, transfers, or compounds into hidden
  future exclusion.
- Large tenants capture capacity, while small, low-income, high-latency,
  disabled, caregiving, or time-zone-constrained users receive worse access.
- The provider smooths its load by displacing work and risk into user time,
  unpaid waiting, sleep, local compute, or human review.
- Token accounting mismeasures multimodal, cached, tool, reasoning, memory,
  verification, and human work.
- Dynamic pricing is unpredictable, discriminatory, manipulable, or itself
  destabilizing.
- “Wellness” telemetry becomes worker surveillance, health inference, ranking,
  insurance/employment data, or coercive personalization.
- Better infrastructure variance coexists with worse task quality, false
  refusal, deadline failure, user welfare, access, or total environmental cost.

## Explicitly rejected or bounded claims

- The source does not establish stationary MPE existence, absolute continuity
  of all optimal usage, strict variance reduction, heavy-tail robustness,
  pricing stability, or profit dominance as proved results.
- The reported 20–35% variance reduction, 3–8% profit increase, and stability
  threshold near 0.42 are unsupported illustrations.
- Hard quota resets do not necessarily induce impulse demand, and regenerative
  capacity does not necessarily desynchronize all users or eliminate peaks.
- Regenerative access is not inherently distinct from or superior to carefully
  configured token-bucket, staggered quota, reservation, or queue mechanisms.
- Equal mean load and lower convex cost do not establish provider profit,
  consumer surplus, social welfare, fairness, or sustainability.
- Pricing architecture is not shown to reduce sleep, improve circadian
  stability, raise cognitive productivity, or reduce cognitive friction.
- Seven-to-eight hours is not a universal individual optimum, and the simple
  quadratic sleep penalty is an illustrative model, not medical science.
- An opt-in study is not automatically non-coercive, private, or ethically
  adequate, especially when providers or employers control access.
- The proposed 200–500 users, 6–10 weeks, and detectable-effects statement is
  not a power analysis.

## Section-family closure

| Section family | Disposition |
|---|---|
| Initial and revised RCM models | Integrated as a candidate regenerative budget contract; mathematical gaps and repeated drafts are retained in this note. |
| Equilibrium, continuity, variance, heavy-tail, stability, and profit results | Converted from “established theorems” to proof obligations and empirical hypotheses. |
| Product-plan mapping | Integrated with units, spill/debt, protected floors, fairness, feedback, and appeal fields added. |
| Initial and public temporal-elasticity models | Added to Resource Economics as the temporal access contract and human-schedule externality boundary. |
| Renewal clustering, nocturnal share, sleep, and friction measures | Retained as separate observations/proxies with no causal or medical inference. |
| DiD, boundary discontinuity, mediation, and minimum study | Retained as research candidates with interference, selection, confounding, power, attrition, and ethics duties. |
| Privacy and scope discipline | Integrated and strengthened to forbid employer/performance use and individual impairment inference. |
| Repeated draft/public versions and minimal references | De-duplicated; external citations remain separate review obligations. |

## Book Chapters Supported

- `resource-economics-and-token-budgets`
- `human-factors-and-meaningful-control-in-oversight`
- `physical-compute-infrastructure-energy-and-environmental-constraints`
- `benchmark-ratchets-and-anti-goodhart-evidence`
- `policy-optimization-and-learning-from-feedback`
- `ai-deployment-transition-distribution-and-human-agency`
- `planning-as-a-control-layer`: capacity, deadlines, priority, deferral, and fallback constrain scheduling but do not choose task value or grant dispatch authority.
- `inter-stack-protocols-identity-and-economic-exchange`: regenerative credits and dynamic price signals require identity, units, expiry, fairness, dispute, and non-authority boundaries.
- `personal-compute-hives-and-federated-edge-intelligence`: local and shared capacity pools need owner-aware regeneration, burst, interference, and protected-floor accounting.
- `fast-generation-architectures`: cheap or bursty generation remains subordinate to useful-output, verification, and human-cost accounting.
- `artifact-steward-agents-and-living-project-governance`: project compute, reviewer capacity, and treasury-like credits require bounded issuance, custody, and displaced-work records.

No new chapter is warranted. The missing human temporal-access mechanism is
now written in Resource Economics; other chapter assignments remain bounded
interfaces rather than duplicated prose.

## Claims To Add Or Update

- Add a temporal access contract to resource budgeting and state that quotas,
  renewals, accrual, expiry, bursts, prices, and notifications shape human
  schedules as well as infrastructure load.
- Keep renewal clustering, nocturnal work, sleep, and friction as separate
  observations and causal stages.
- Correct theorem and profit language into formal and empirical obligations.
- Forbid health-sensitive telemetry from becoming access, employment,
  performance, insurance, or individualized impairment scoring.

## Research obligations and falsifiers

1. Specify a dimensionally consistent capacity model with boundary behavior,
   provider strategy, exact quota comparator, demand process, queue/cost model,
   and formal theorem statements before claiming equilibrium or dominance.
2. Implement strong reset, staggered-reset, token-bucket, reservation,
   pay-as-you-go, static-rate, and regenerative policies under matched natural
   or validated synthetic demand.
3. Measure mean, variance, tails, queueing, service quality, failures, churn,
   price/revenue, implementation cost, fairness, gaming, carbon/energy where
   available, and useful completed work—not load smoothness alone.
4. Preregister any human study, treatment, estimand, spillover model, sampling,
   power, attrition, privacy, deletion, adverse-event, and non-employment-use
   plan. Prefer cluster or interference-aware designs when prices/load are
   shared.
5. Test each causal link separately: regime to clustering, clustering to night
   work, night work to sleep, sleep to task outcomes. Retain null, adverse,
   heterogeneous, and subgroup results.
6. Falsify the win-win claim if smoothing merely shifts cost, if strong simple
   baselines match RCM, if access becomes less fair or predictable, or if human
   outcomes do not improve.

## Open Questions

- Can a regenerative plan remain legible to users while responding to real
  capacity without becoming dynamic-pricing manipulation?
- What units fairly cover text, multimodal input, cached computation, tool use,
  long reasoning, storage, verification, and human review?
- How should essential or high-impact tasks receive protected capacity without
  encouraging risk-label gaming or starving ordinary users?
- Which study design handles platform-wide pricing spillovers and deadlines
  without exposing sensitive work and sleep patterns?
- Does temporal flexibility reduce pressure, or does continuous visible
  accrual create a stronger compulsion to consume?
