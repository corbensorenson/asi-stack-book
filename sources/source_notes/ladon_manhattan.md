# Source Note: Ladon & The Manhattan Protocol

| Field | Value |
|---|---|
| Source ID | `ladon_manhattan` |
| Source title | Ladon & The Manhattan Protocol |
| Ingestion date | 2026-06-24 |
| Source version / URL | Google Docs source in inventory: https://docs.google.com/document/d/1uT9iQ7Jb2TsU9DletvtVeLEej63aIQl3WS3jTsMgtSM |
| Ingestion basis | Local raw cache inspected at `sources/raw/google_docs/ladon_manhattan.txt`; raw text is not published. |

## Thesis

Ladon and the Manhattan Protocol propose a kernel-level security architecture for high-agency AI systems: the AI may use a credential through a constrained handle, but it should not know or store the credential itself. The design moves sensitive authority out of prompts, model context, and application memory and into a secret-management layer.

## Mechanisms

- Store secrets in a hardened manager or vault outside the AI process.
- Give the AI opaque handles rather than credential bytes.
- Use a secure user interface path for credential entry so the AI-rendered interface cannot observe the secret.
- Intercept outbound calls or syscalls at a boundary where policy can authorize and inject the secret.
- Run sensitive computations inside ephemeral isolated containers or secure compartments.
- Zeroize sensitive memory after the computation and return only permitted outputs.
- Use side-channel defenses such as cache partitioning, execution jitter, and memory isolation as design considerations.
- Treat prompt injection as less powerful when the model has no credential bits to reveal.

## Evidence

- The source is a security architecture/specification with implementation sketches.
- It provides a concrete handle-based pattern, secret-injection boundary, and compartment lifecycle.
- The repository has not implemented Ladon, run kernel-level tests, verified side-channel defenses, or audited the design.
- Security claims must remain architectural unless a prototype and threat-model-specific validation are added.

## Failure Modes

- Treating a handle as safe while allowing unrestricted use of the authority it names.
- Leaking secrets through logs, traces, screenshots, rendered UI, or tool transcripts.
- Injecting secrets too early, before policy and destination checks.
- Failing to wipe ephemeral compartments or allowing network/shared-memory escape.
- Ignoring side channels and assuming memory isolation alone is sufficient.
- Overstating the defense as complete protection rather than reduced credential exposure.

## Book Chapters Supported

- `system-boundaries-and-authority` (System Boundaries and Authority)
- `governance-rights-fork-exit-and-audit` (Governance Rights: Fork, Exit, and Audit)
- `stable-capability-fields` (Stable Capability Fields)
- `security-kernel-and-digital-scifs` (Security Kernel and Digital SCIFs)
- `context-transactions-snapshots-mounts-and-taint` (Context Transactions, Snapshots, Mounts, and Taint)
- `runtime-adapters-tool-permissions-and-human-approval` (Runtime Adapters, Tool Permissions, and Human Approval)
- `personal-compute-hives-and-federated-edge-intelligence` (Personal Compute Hives and Federated Edge Intelligence)

## Claims To Add Or Update

- Use Ladon as the book's main source for blind credential handles and secret-use boundaries.
- Tie Digital SCIFs to execution authority, taint, audit logs, and runtime adapter design.
- Do not state that this design solves AI security; state that it reduces a specific class of credential-exfiltration failures under named assumptions.

## Open Questions

- Should `schemas/` include an authority-handle record separate from ordinary tool calls?
- What minimal local test can demonstrate handle-only traces without using real secrets?
- Which side-channel assumptions should the security-kernel chapter explicitly mark out of scope?
