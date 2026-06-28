# Source Note: Proof-Carrying Code

| Field | Value |
|---|---|
| Source ID | `ext_proof_carrying_code_1997` |
| Source title | Proof-Carrying Code |
| Ingestion date | 2026-06-28 |
| Source version / URL | ACM DOI, https://dl.acm.org/doi/10.1145/263699.263712 |
| Citation label | Necula (1997), Proof-Carrying Code |
| Published / updated | 1997-01 / not recorded |
| DOI | 10.1145/263699.263712 |
| Ingestion basis | Primary ACM DOI record inspected for the formal-methods literature queue; paper not vendored into this repository and no PCC implementation imported. |

## Thesis

Proof-Carrying Code belongs in the proof-envelope and runtime-adapter chapters as the external ancestor of carrying machine-checkable evidence with an executable artifact. It clarifies the difference between a proof artifact, a consumer policy, and actual permission to execute.

## Mechanisms

- Pair code with a proof that it satisfies a host policy.
- Let the host validate the proof before executing untrusted code.
- Separate producer obligations from consumer-side proof checking.
- Treat proof validity as scoped to a declared safety policy.

## Evidence

- The source contributes formal-methods architecture and historical grounding.
- This repository has not implemented PCC, imported PCC proofs, or validated machine code against a host policy.
- Use it as external comparison for proof-carrying claims and artifact admission, not as evidence of local enforcement.

## Failure Modes

- A proof can be valid for the wrong policy.
- A proof consumer can over-read a narrow theorem.
- Runtime effects outside the proof boundary can still violate operational intent.

## Book Chapters Supported

- `executable-specifications-and-lean-proof-envelope` (Executable Specifications and Lean Proof Envelope)
- `spinoza-verification-and-proof-carrying-claims` (Spinoza Verification and Proof-Carrying Claims)
- `runtime-adapters-tool-permissions-and-human-approval` (Runtime Adapters, Tool Permissions, and Human Approval)
- `artifact-graphs-audit-logs-and-replay` (Artifact Graphs, Audit Logs, and Replay)

## Claims To Add Or Update

- Use this note to ground proof-carrying artifact vocabulary.
- Do not claim the ASI Stack implements PCC or proof-carrying runtime adapters.
- Keep support state at `argument` until an implemented artifact and consumer check exist.

## Open Questions

- Which proof target should first become a consumer-checked receipt?
- What policy boundary should a runtime adapter proof actually cover?
- How should invalid or stale proof receipts block artifact reuse?
