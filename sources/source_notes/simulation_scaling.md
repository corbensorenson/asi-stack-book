# Source Note: Simulation Scaling Law

| Field | Value |
|---|---|
| Source ID | `simulation_scaling` |
| Source title | Simulation Scaling Law |
| Ingestion date | 2026-06-24 |
| Source version / URL | Google Docs source in inventory: https://docs.google.com/document/d/1rt0lnpwZ9X6M_ejLC7PYHQSXsvajYICGo4ETS-ndUFA |
| Ingestion basis | Local raw cache inspected at `sources/raw/google_docs/simulation_scaling.txt`; raw text is not published. |

## Thesis

Simulation Scaling Law treats simulation feasibility as contract-relative. A simulation is not simply possible or impossible in the abstract; its feasibility depends on the requested scope, clockspeed, fidelity, efficiency, and available physical capacity under bottlenecks such as compute, memory, thermodynamics, and communication.

## Mechanisms

- Define a simulation contract with target degrees of freedom, required outputs, fidelity standard, and temporal semantics.
- Normalize demand as a function of scope, clockspeed ratio, and effective efficiency.
- Compare demand against the minimum available capacity across relevant bottlenecks.
- Use scope, clockspeed, fidelity, resource fraction, and efficiency as explicit tradeoff levers.
- Separate computability or definability from physical feasibility.
- Explain why real-time, high-fidelity, same-physics simulations face stronger constraints than reduced-scope or offline simulations.
- Use the framework to reason about nested simulations, ASI resource allocation, and benchmark environments.

## Evidence

- The source is a theoretical synthesis and scaling framework.
- It connects contract-relative simulation demand to known physical-computation constraints as reported by the source.
- No physical experiment, simulation benchmark, or independent literature audit was run in this repository.
- External references named by the source should be checked before the book cites them directly.

## Failure Modes

- Discussing simulation without specifying scope, fidelity, and temporal contract.
- Treating theoretical computability as if it guarantees feasible execution.
- Ignoring memory, heat, bandwidth, and latency bottlenecks.
- Smuggling in a different parent physics model without saying so.
- Using vague simulation arguments to support ASI capability claims without resource accounting.
- Treating first-order scaling as a complete physical model.

## Book Chapters Supported

- `the-efficient-asi-hypothesis` (The Efficient ASI Hypothesis)
- `failure-modes-of-ungoverned-intelligence` (Failure Modes of Ungoverned Intelligence)
- `compact-generative-systems-and-residual-honesty` (Compact Generative Systems and Residual Honesty)
- `resource-economics-and-token-budgets` (Resource Economics and Token Budgets)
- `simulation-fidelity-and-physical-constraints` (Simulation Fidelity and Physical Constraints)
- `mathematical-and-search-substrates` (Mathematical and Search Substrates)
- `open-research-agenda-and-bibliography-plan` (Open Research Agenda and Bibliography Plan)

## Claims To Add Or Update

- Use this source to make resource contracts explicit when the book discusses simulation, world models, sandboxing, or synthetic evaluation.
- Treat simulation fidelity as an engineering budget tied to a stated contract.
- Avoid using simulation arguments as evidence for capabilities unless demand, capacity, and bottleneck assumptions are named.

## Open Questions

- Should the book include a small calculator or schema for simulation contracts?
- Which external physics/computation references need direct bibliography entries?
- Can a test fixture demonstrate contract-relative feasibility on toy simulations without overclaiming?
