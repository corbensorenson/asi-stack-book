# Source Note: TokenMana

| Field | Value |
|---|---|
| Source ID | `tokenmana` |
| Source title | TokenMana |
| Ingestion date | 2026-06-24 |
| Source version / URL | Google Docs source in inventory: https://docs.google.com/document/d/1dGOlGPZi6byTwRUbHQt40OSErBnQ4j6G_BZvA-oJRM8 |
| Ingestion basis | Local raw cache inspected at `sources/raw/google_docs/tokenmana.txt`; raw text is not published. |

## Thesis

TokenMana proposes regenerative capacity mechanisms for AI usage pricing and resource governance. Instead of hard quota resets that synchronize bursts, users accumulate bounded usage capacity continuously, with pricing and burst controls shaped to reduce load variance and cognitive friction.

## Mechanisms

- Model each user as holding a regenerating capacity stock with a bounded pool.
- Allow bounded burst or compression multipliers while preventing unbounded demand spikes.
- Adjust prices or access conditions from aggregate load signals.
- Compare regenerative capacity with hard quota systems under convex infrastructure costs.
- Measure system outcomes with load variance, renewal clustering, nocturnal usage, and token-normalized cognitive friction.
- Use staggered rollout, renewal-boundary discontinuity, and opt-in sleep or productivity measures as proposed empirical strategies.
- Include privacy, opt-in, separation from employer, deletion, and export as study constraints.

## Evidence

- The source includes an economic model, formal claims as reported by the source, numerical or empirical design ideas, and a human-centered study protocol.
- The repository has not reproduced the formal results, run simulations, or collected empirical data.
- Treat the mechanism as a resource-governance design and research plan, not as verified pricing performance.

## Failure Modes

- Replacing hard resets with a regenerative scheme but still allowing synchronized external deadlines to dominate load.
- Optimizing infrastructure load while ignoring user sleep, friction, or task quality.
- Using burst multipliers that recreate quota cliffs.
- Overclaiming welfare or productivity benefits without controlled studies.
- Mishandling privacy when measuring usage, sleep, or cognitive-friction signals.
- Treating token spend as the only scarce resource.

## Book Chapters Supported

- `planning-as-a-control-layer` (Planning as a Control Layer: DAGs and Intelligence Arbitrage)
- `fast-generation-architectures` (Fast Generation Architectures)
- `resource-economics-and-token-budgets` (Resource Economics and Token Budgets)
- `resource-economics-and-token-budgets` (Resource Economics and Token Budgets; includes Simulation Fidelity and Claim Transport)
- `inter-stack-protocols-identity-and-economic-exchange` (Inter-Stack Protocols, Identity, and Economic Exchange)
- `benchmark-ratchets-and-anti-goodhart-evidence` (Benchmark Ratchets and Anti-Goodhart Evidence)
- `policy-optimization-and-learning-from-feedback` (Policy Optimization and Learning from Feedback)
- `personal-compute-hives-and-federated-edge-intelligence` (Personal Compute Hives and Federated Edge Intelligence)
- `artifact-steward-agents-and-living-project-governance` (Artifact Steward Agents and Living Project Governance)

## Claims To Add Or Update

- Use TokenMana to motivate regenerative budgets for models, humans, tools, and review capacity.
- Use TokenMana to keep fast-generation claims tied to latency, compute, memory, load variance, human friction, and quality constraints rather than raw token throughput.
- Use TokenMana to bound latency, cost, load, and capacity rewards so efficiency pressure cannot erase quality, sleep/cognitive-friction, or verification constraints.
- Tie resource economics to load variance, latency, sleep/cognitive cost, and quality rather than tokens alone.
- Keep claims about equilibrium, profit dominance, and human outcomes at source-proposed status until reproduced.

## Open Questions

- Should the book include a regenerative-budget schema for PlanForge schedulers?
- Which TokenMana claims are suitable for Lean-like formalization versus simulation?
- What toy load simulator would be sufficient to support a prototype-backed discussion?
