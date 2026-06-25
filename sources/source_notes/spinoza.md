# Source Note: Proof of Belief / The Spinoza Architecture

| Field | Value |
|---|---|
| Source ID | `spinoza` |
| Source title | Proof of Belief / The Spinoza Architecture |
| Ingestion date | 2026-06-24 |
| Source version / URL | Multiple February 2026 drafts through later release-candidate material; https://docs.google.com/document/d/1Y90DBgxsOJImMXi4aOrwxtbyjlkVZpCzu1YJy_SFatk |
| Ingestion basis | Local raw cache inspected at `sources/raw/google_docs/spinoza.txt`; raw text is not published. |

## Thesis

Spinoza proposes a bounded neurosymbolic reasoning architecture: neural systems propose hypotheses or proof sketches, while symbolic verification, evidence graphs, belief revision, and tiered support states determine whether a claim can be committed.

## Mechanisms

- Separation between neural proposer and symbolic verifier.
- Proof/citation/procedure-carrying claim graph with tiers for certified, heuristic, probabilistic, speculative, or unknown claims.
- Belief revision through contradiction detection, dependency tracing, entrenchment, defeaters, and downgrade/block behavior.
- Explicit non-assumption that open-domain natural-language-to-logic translation is solved.
- Protected axioms, compartments, and threat model for self-rewriting or constitutional changes.

## Evidence

- The source contains multiple versions, including earlier high-level drafts and later de-risked formulations.
- It is a reasoning and verification architecture source, not proof that natural language can always be formalized.
- Later versions explicitly acknowledge undecidability, verifier timeouts, and downgrade paths.

## Failure Modes

- Marketing-heavy claims that overstate theorem proving or self-rewriting.
- Treating failed or timed-out verification as success.
- Letting the same component generate, verify, and authorize its own protected axioms.
- Assuming open-domain autoformalization is solved.

## Book Chapters Supported

- Claim Ledgers and Belief Revision
- Semantic Pages, Context Cells, and Certificates
- Verification Bandwidth and Context Adequacy
- Spinoza Verification and Proof-Carrying Claims
- Unified Adaptive Tribunal and Adversarial Review
- Failure Modes of Ungoverned Intelligence
- Constitutional Alignment Substrate
- Moral Uncertainty and Value Conflict
- Governance Rights: Fork, Exit, and Audit
- Fast Generation Architectures
- Semantic Representation and Tree-Structured Models
- Policy Optimization and Learning from Feedback
- Artifact Steward Agents and Living Project Governance
- Evidence States and Claim Discipline
- Executable Specifications and Lean Proof Envelope
- Integrated Reference Architecture
- Open Research Agenda and Bibliography Plan

## Claims To Add Or Update

- Use Spinoza for the proof-carrying claim and downgrade discipline.
- Use Spinoza to identify failure modes around unsupported claims, failed verification, contradiction handling, protected axioms, and self-authorizing changes.
- Use Spinoza to route semantic/context representation claims through explicit provenance, justification artifacts, contradiction handling, and verifier-scope limits.
- Use Spinoza to keep fast-generation acceptance predicates separate from truth, proof, and source support; accepted drafts still need claim-tier evidence.
- Use Spinoza to keep reward signals, verifier outputs, and preference labels separate from proof, evidence, and admissible belief updates.
- Treat all proof-carrying claims as bounded by formalization scope and verifier result.
- Connect Spinoza tiers to Appendix C support states without equating them automatically.

## Open Questions

- Which Spinoza version should be canonical for final terminology?
- Which belief-revision records should become schemas?
- Which Spinoza claim can be mechanized first in Lean or executable tests?
