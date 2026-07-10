# Source Note: Verification Bandwidth in Bounded Contexts

| Field | Value |
|---|---|
| Source ID | `verification_bandwidth` |
| Source title | Verification Bandwidth in Bounded Contexts |
| Ingestion date | 2026-06-24 |
| Source version / URL | Google Docs source in inventory: https://docs.google.com/document/d/1T34n1Ya6_joaAD8ZxygOpiEuNzEVj3G8_nf0xZuFL2U |
| Ingestion basis | Local raw cache inspected at `sources/raw/google_docs/verification_bandwidth.txt`; raw text is not published. |

## Thesis

Verification Bandwidth argues that long context should not be confused with long-range reasoning. A model may generate across a large context while still being unable to jointly verify all relevant constraints when the active verification workspace is smaller than the combined objects that must be compared.

## Mechanisms

- Distinguish total context length from effective verification workspace.
- Define semantic units as the pieces of content whose mutual consistency must be checked.
- Model coherence as constraint satisfaction rather than continuity of generated prose.
- Treat pairwise grinding as the act of jointly attending to two semantic units in enough detail to verify consistency.
- Identify a two-body verification limit: rigorous comparison becomes unavailable when the joint size of the compared units exceeds the effective workspace.
- Show how a dominant large unit can monopolize verification capacity and suppress checking against other units.
- Explain transitive decay: local consistency through intermediates does not guarantee global consistency.
- Frame hierarchical summaries as a scale/fidelity tradeoff, not a free solution.
- Propose a constraint-satisfaction test that compares linear generation with a final explicit grinding step and measures contradiction reduction.

## Evidence

- The source is a conceptual and theoretical framework with falsifiable test suggestions.
- It provides definitions, proposed theorems, and an empirical test design centered on logical contradiction rate.
- The book repository has not run the proposed constraint-satisfaction test.
- Theorems in this source should be treated as source-proposed arguments unless mechanized or empirically tested later.

## Failure Modes

- Equating a larger context window with verified use of all included evidence.
- Letting one large document or summary crowd out critical cross-checks.
- Assuming adjacent coherence implies non-adjacent coherence.
- Using RAG as if retrieval alone solves verification.
- Compressing evidence into summaries without recording what fidelity was lost.
- Measuring output fluency instead of contradiction rate, residual claims, and evidence coverage.

## Book Chapters Supported

- `evidence-states-and-claim-discipline` (Evidence States and Claim Discipline)
- `virtual-context-abi` (The Virtual Context ABI: Typed Pages, Cells, and Certificates)
- `verification-bandwidth-and-context-adequacy` (Verification Bandwidth and Context Adequacy)
- `spinoza-verification-and-proof-carrying-claims` (Proof-Carrying Claims and Adversarial Review)
- `fast-generation-architectures` (Fast Generation Architectures)
- `policy-optimization-and-learning-from-feedback` (Policy Optimization and Learning from Feedback)
- `compact-generative-systems-and-residual-honesty` (Compact Generative Systems: Generate, Verify, Repair, and Residual Honesty)
- `open-research-agenda-and-bibliography-plan` (Open Research Agenda and Bibliography Plan)
- `governed-deliberation-and-test-time-scaling` (Governed Deliberation and Test-Time Scaling)

## Claims To Add Or Update

- Use this source to justify a separate context-adequacy layer in the architecture.
- Use this source to prevent fast-generation speed claims from bypassing verification bandwidth: faster draft production is not faster verified cognition if contradiction checks become the bottleneck.
- Use this source to bound context-policy and reasoning-budget rewards: longer context or shorter reasoning is not a valid reward unless verification adequacy and contradiction pressure are measured.
- Treat verification capacity as a scarce resource that must be budgeted, measured, and surfaced in claim ledgers.
- Require summaries, context cells, and semantic pages to expose coverage and compression loss rather than pretending to preserve all source constraints.
- Treat deliberation time as a verification-limited budget: additional branches,
  revisions, or tokens cannot substitute for an adequate independent check.

## Open Questions

- What minimal synthetic benchmark should the repo add for contradiction-rate testing?
- Can the two-body verification limit be formalized as a finite resource invariant in Lean?
- How should the book distinguish context retrieval, context packing, and context verification in diagrams and schemas?
