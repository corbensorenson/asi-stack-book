# Source Note: Simulation Scaling Law

| Field | Value |
|---|---|
| Source ID | `simulation_scaling` |
| Source title | The Simulation Scaling Law: Resource Constraints on Scope, Clockspeed, and Effective Fidelity in Nested Physical Simulations |
| Ingestion date | 2026-06-24 |
| Full-fidelity review | 2026-07-31 |
| Source version / URL | Google Docs source in inventory: https://docs.google.com/document/d/1rt0lnpwZ9X6M_ejLC7PYHQSXsvajYICGo4ETS-ndUFA |
| Ingestion basis | Complete local raw cache inspected at `sources/raw/google_docs/simulation_scaling.txt` (1,383 lines; approximately 17,309 words). Raw text is not published. |
| Evidence role | Corben-authored theoretical synthesis and correction lineage; no reproduced physical bound, simulator, benchmark, feasibility result, or independent literature audit. |

## Thesis

The paper's durable thesis is that simulation feasibility is relative to a
declared contract. “Simulate this system” is not a determinate engineering
request until the target, observables, fidelity and error tolerances, temporal
semantics, boundary conditions, and permitted approximations are fixed. A
candidate simulator must then satisfy every operative resource constraint—not
only a compute estimate—and a synthetic result may support only the real-world
claim allowed by that contract.

The manuscript proposes the scalar heuristic
`D = scope * clockspeed / effective_efficiency <= capacity`. That expression
is useful as a mnemonic or visualization only under strong separability and
common-scaling assumptions. It is not established as a physical law. The book
therefore retains the simulation contract and tradeoff intuition while
replacing the universal scalar with a typed resource-demand vector, explicit
coupling constraints, and a claim-transport boundary.

## Version and correction lineage

The cache contains six tabs representing repeated drafting rather than six
independent sources:

| Version family | Material change | Disposition |
|---|---|---|
| Earliest prose draft | Presents the scope–speed–efficiency equation as exact or universal, treats the self-identical universe as the sole 1:1 exception, and makes aggressive claims about reversible computation and feasibility. | Superseded. Its strongest physical and metaphysical claims are explicitly rejected below. |
| Early formal draft | Introduces a simulation contract, naïve reference implementation, bottleneck capacity ratios, efficiency decomposition, physical-computation references, Vazza calibration, and Wolpert interface. | Mechanisms retained; claimed derivation and universal corollary narrowed. |
| LaTeX/final-draft revisions | Adds communication, states first-order and contract-relative limitations, and clarifies that reversible logic shifts rather than erases bottlenecks. | Best intermediate correction, but still uses one efficiency factor for heterogeneous resources and still overstates the 1:1 exclusion. |
| Public-release-style final tab | Supplies the clearest seven-step application recipe and limitations/future-work section. | Controlling prose version for audit, subject to the mathematical and evidentiary corrections in this note. |

Repeated abstracts, equations, Vazza figures, conclusions, and references across
tabs are lineage, not replication.

## Mechanisms

### Simulation contract

- Declare target system and boundary, required outputs or observables, fidelity
  and error metric, temporal semantics, initial conditions, boundary
  conditions, intervention/query rights, stochastic treatment, and success
  horizon.
- Declare what may be omitted, deferred, cached, reconstructed, coarse-grained,
  conditionally evaluated, approximated, or replaced by a surrogate. Changing
  one of these fields changes the contract; it is not an implementation-only
  speedup.
- Bind the contract to the exact candidate and reference implementations, model
  and hardware identities, resource meters, environment, and consumer claim.

### Per-bottleneck feasibility

- Estimate a typed demand vector for compute or state-transition rate, working
  and persistent state, communication and synchronization, latency or
  sequential depth, energy, irreversible erasure, heat rejection, error
  correction, sensing/I/O, and any task-specific scarce resource.
- Estimate a compatible capacity vector using the same units, scope, time
  interval, geometry, environment, reliability, and architecture. Universal
  physical bounds are ceilings, not descriptions of attainable hardware.
- Require every component constraint and every coupling constraint to pass.
  The minimum normalized margin may summarize an already completed vector
  audit, but cannot replace it.
- Identify the active bottleneck and test whether an optimization merely moves
  demand into another component. Compression can increase decompression work;
  reversibility can increase memory, latency, and error-management cost;
  distribution can exchange local memory for bandwidth and synchronization.

### Scope, clockspeed, and implementation efficiencies

- Scope and simulated-time rate are useful design levers, but their demand need
  not be linear or separable. Long-range coupling, adaptivity, event sparsity,
  stiffness, parallelism, sequential depth, boundary communication, quantum
  state representation, and error correction can create different laws for
  different resource components.
- Keep representation, conditional evaluation, algorithm, reversible-
  computation, hardware, and communication changes separate. Their gains can
  overlap, conflict, or apply to only one resource.
- Distinguish implementation improvement under a fixed contract from contract
  weakening. Reduced resolution, fewer observables, smaller scope, delayed
  answers, or observer-conditioned rendering are different tasks when the
  original contract required the discarded behavior.

### Claim transport

- Separate logical definability, computability, physical upper-bound
  consistency, engineering feasibility, simulator adequacy, benchmark result,
  and real-world transfer.
- Record omissions, instrumentation effects, uncertain assumptions, residuals,
  and the exact supported claim before a synthetic result enters an evidence
  ledger.
- A failed transfer remains useful as a narrower test, counterexample, or
  residual. It cannot be promoted because the simulator was expensive or
  detailed.

## Interfaces and invariants

`resource-economics-and-token-budgets` owns the Simulation Contract Record,
typed demand/capacity accounting, and claim-transport gate. Governed World
Models owns representational adequacy and reality grounding; Benchmark
Ratchets owns comparative evaluation; Physical Compute owns attainable
hardware, energy, cooling, networking, and environmental constraints; Evidence
and Claim Ledgers own support transitions; the Research Agenda owns independent
physics review and executable feasibility work.

Invariants are: the contract is prospective and versioned; unlike units are
not collapsed before their constraints are checked; a changed contract is not
credited as an implementation efficiency; an upper physical bound is not
attainable capacity; a minimum margin is a summary, not a proof; simulator
success grants no unlisted transfer; and metaphysical possibility grants no
capability, safety, or deployment evidence.

## Evidence

The source supplies a conceptual contract, normalized reference accounting,
first-order equations, a bottleneck recipe, physical-limit references, a
worked reinterpretation of figures reported by Vazza, a discussion of Wolpert,
and an explicit limitations section. It supplies no new theorem proof,
dimensional or sensitivity analysis, simulation implementation, physical
device, capacity measurement, benchmark, uncertainty interval, robustness
test, independent replication, or evidence that the component efficiencies
multiply without overlap. The Vazza numbers and interpretations are
source-reported secondary uses until each primary passage and assumption is
independently reviewed.

## Mathematical and physical audit

- `D = sigma * rho / epsilon <= eta(m)` follows only after assuming that every
  relevant resource scales by the same `sigma * rho` factor and benefits from
  the same `epsilon`. Those assumptions are not derived and are false for many
  simulators: stored state need not scale with clockspeed, communication may
  grow superlinearly, event-driven work can be sparse, and sequential depth can
  bind independently of operation count.
- A safer statement is a family of inequalities `d_j(C, I) <= c_j(A, m)` for
  contract `C`, implementation `I`, resource `j`, architecture/environment `A`,
  and allocation `m`, plus coupling constraints. `min_j(c_j/d_j)` is meaningful
  only after positive, commensurate component demands and definitions are
  fixed.
- One multiplicative efficiency product can double-count correlated gains and
  hide tradeoffs. Coarse-graining may alter the contract; compression adds
  decode work; reversible computation may exchange erasure for time, space,
  control, and error-correction burdens.
- Defining scope as contracted degrees of freedom “actually instantiated”
  while permitting them to be omitted or fidelity-reduced is internally
  unstable. If the contract requires those degrees of freedom, omission fails
  it; if it does not, the reference scope was misdefined.
- Capacity is not generally a function of mass fraction alone. Energy above
  ground, volume or area, geometry, temperature, cooling surface, free-energy
  flux, causal structure, bandwidth, material, reliability, duration, and
  architecture matter.
- Margolus–Levitin/Lloyd bounds constrain idealized distinguishable-state
  evolution under stated energy assumptions. “Elementary operation” is not an
  architecture-independent useful-operation budget.
- Bekenstein and holographic bounds are upper ceilings under particular
  physical assumptions, not achievable memory specifications. Area-scaling
  equality cannot be assigned to arbitrary ordinary devices.
- Landauer concerns logically irreversible erasure, not every logical
  operation. Reversible computing does not make effective efficiency infinite:
  noise, control, ancillae, uncomputation, latency, reliability, and heat
  rejection remain.
- The claimed straight-line phase frontier follows algebraically from the
  chosen scalar model. It is not empirical evidence that real simulator
  frontiers have slope minus one.
- The proper-subsystem 1:1 exclusion is not proved by asserting `eta(m) < 1`.
  Exact microstate reproduction, prediction, emulation, behavioral equivalence,
  analog evolution, self-simulation, and compressed-law/state simulation are
  different contracts. A rigorous impossibility needs definitions and a
  theorem whose premises exclude compression, delay, external inputs, and
  trivial identity cases.
- Self-identical physical evolution is a boundary comparator, not an
  informative simulator architecture or evidence that nested simulations are
  feasible.
- Wolpert-style logical self-simulation and undecidability results do not imply
  physical resource equality, testability, or that simulation layers have any
  particular metaphysical status.

## Failure Modes

- A compact scalar hides the binding resource, incompatible units, or a demand
  moved into bandwidth, latency, cooling, error correction, or human work.
- A baseline is intentionally naïve, making ordinary engineering look like an
  enormous universal efficiency gain.
- Approximation or reduced scope is called efficiency even though it changes
  what must be reproduced.
- Ideal physical ceilings are treated as realizable capacity, omitting
  architecture and reliability losses.
- State size is multiplied by a universal timestep and operations per bit
  without exploiting dynamics, locality, sparsity, event structure, or
  validated numerical methods.
- A simulator passes its internal checks while its omitted variable decides the
  external outcome.
- Simulation-hypothesis rhetoric distracts from the bounded engineering claim
  or converts formal possibility into unwarranted confidence.

## Explicitly rejected or bounded claims

- The scalar expression is not established as an exact, universal, novel, or
  natural physical “Simulation Scaling Law.”
- The source does not prove that full-scope real-time simulation by every
  proper subsystem is impossible, or that self-identity is the only exception.
- It does not show that `eta(m) < 1` for every proper subsystem, that resource
  ratios scale with allocated mass, or that all simulator demands share one
  linear factor.
- It does not show that efficiency factors are independent or multiplicative,
  that reversible logic permits unbounded efficiency, or that physical upper
  bounds are achievable.
- The quoted Vazza quantities, neutrino timestep inference, per-bit update
  assumption, and power estimates are not reproduced or independently audited
  here; they cannot establish a general Earth- or universe-simulation result.
- The source does not establish that ancestor simulations are probable or
  impossible, that we are or are not simulated, that parent physics differs,
  or that the simulation hypothesis is experimentally decidable.
- No simulation feasibility, model capability, benchmark transfer, safety,
  deployment, or ASI conclusion follows from this source alone.

## Section-family closure

| Section family | Disposition |
|---|---|
| Six-tab draft and correction lineage | De-duplicated; final public-style tab controls wording while earlier overclaims are retained as superseded boundaries. |
| Simulation contract and reference implementation | Integrated and strengthened in Resource Economics with target, observables, errors, boundaries, queries, stochastic treatment, implementation identity, and transfer fields. |
| Scope, clockspeed, and efficiency levers | Retained as design intuition; linearity, separability, and common-efficiency assumptions are explicit rather than treated as law. |
| Normalized capacity and minimum bottleneck | Replaced by typed demand/capacity inequalities plus coupling constraints; scalar margin allowed only as a post-audit summary. |
| Efficiency decomposition | Retained as separate resource-specific mechanisms with overlap, contract-change, and bottleneck-shifting warnings. |
| Physical computation foundations | Routed to independent primary-source review; upper bounds are not promoted as attainable engineering capacity. |
| Vazza calibration | Retained as a source-reported worked example and research obligation, not reproduced evidence. |
| Wolpert interface | Retained only for logical-possibility versus physical-feasibility separation; metaphysical conclusions rejected. |
| Tradeoff frontier and 1:1 corollary | The scalar plot is labeled model-conditional; the universal exclusion claim is converted into a formalization obligation. |
| Simulation-hypothesis implications | Kept as boundary context, not used as ASI evidence. |
| Limitations and future work | Integrated into explicit nonlinear, distributed, quantum, gravitational, contract, and nested-layer obligations. |

## Book Chapters Supported

- `resource-economics-and-token-budgets`
- `governed-world-models-and-reality-grounding`
- `physical-compute-infrastructure-energy-and-environmental-constraints`
- `benchmark-ratchets-and-anti-goodhart-evidence`
- `claim-ledgers-and-belief-revision`
- `open-research-agenda-and-bibliography-plan`
- `the-efficient-asi-hypothesis`: scope, time, and typed resource tradeoffs discipline efficiency claims; the scalar heuristic is not evidence of efficient ASI.
- `failure-modes-of-ungoverned-intelligence`: omitted contracts, hidden bottlenecks, ideal-bound laundering, and simulator-to-world overtransfer are explicit failure modes.
- `learning-theory-generalization-and-scaling-science`: first-order scaling assumptions require empirical law fitting, uncertainty, regime-change, and falsification rather than “law” naming.
- `compact-generative-systems-and-residual-honesty`: compression and conditional evaluation count only under a fixed contract with omissions and residual cost visible.
- `mathematical-and-search-substrates`: physical and computational upper bounds constrain candidate substrates without proving attainable capacity or useful search.

No new chapter is warranted. Simulation Fidelity and Claim Transport already
has the correct owner in Resource Economics; the missing per-bottleneck
correction is now written there.

## Claims To Add Or Update

- Add the typed feasibility vector and explain that a scalar scope–speed–
  efficiency score is a conditional projection, not a universal law.
- Distinguish fixed-contract implementation gains from a weakened contract.
- Treat physical limits as ceilings requiring an attainable-architecture
  bridge and uncertainty analysis.
- Preserve logical possibility, physical consistency, engineering feasibility,
  simulator adequacy, and external transfer as separate evidence states.

## Research obligations and falsifiers

1. Specify one executable simulation contract, reference implementation,
   candidate implementation, demand vector, capacity vector, coupling
   constraints, meters, uncertainty model, and transfer claim prospectively.
2. Compare the scalar heuristic against measured per-resource demand across
   dense, sparse/event-driven, communication-bound, memory-bound, stiff,
   distributed, and surrogate implementations. Report where common linear
   scaling fails.
3. Audit Margolus–Levitin/Lloyd, Bekenstein, holographic, Landauer/Bennett,
   Vazza, and Wolpert claims at passage level with subject-matter review before
   using them for quantitative conclusions.
4. Test strong numerical, reduced-order, conditional, learned-surrogate,
   reversible, distributed, and deliberately simple baselines under the same
   contract. Attribute gains separately and measure interactions.
5. Run approximation and omission ablations, adversarial boundary cases,
   error propagation, sensitivity, uncertainty, and out-of-distribution
   transfer tests. A result is falsified if an omitted component controls the
   claimed outcome or if a cheaper strong baseline matches it.
6. Attempt a rigorous 1:1 impossibility statement only after defining target,
   containment, exactness, prediction delay, interaction, initialization,
   compression, stochasticity, self-reference, and identity. Publish a
   countermodel if the intended theorem is false.

## Open Questions

- Which resource vectors and coupling constraints are minimally sufficient for
  ordinary AI simulators, embodied world models, and scientific digital twins?
- How should uncertainty in both demand and attainable capacity propagate into
  a release decision?
- When does an implementation optimization preserve the contract, and when is
  it actually a change in fidelity or observable scope?
- Can a useful scalar summary remain legible without encouraging readers to
  forget the vector audit that makes it meaningful?
- Which executable artifact would justify restoring Simulation Fidelity and
  Physical Constraints as a standalone chapter?
