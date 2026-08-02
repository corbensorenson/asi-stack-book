# Claim Dossier: System Boundaries and Authority

Chapter ID: `system-boundaries-and-authority`

Status: P1 semantic review pending

Core support state: `argument`

This dossier is generated from the manifest and review overlay. Inclusion is not proof or promotion.

| Atom | Role | Type | Review | Proposition |
|---|---|---|---|---|
| `system-boundaries-and-authority.core` | `core` | `normative` | `semantically_reviewed` | External-effect authority should be represented as a versioned, revocable tuple binding principal, execution domain, operation, target, permission class, scope, ceiling, grant state, delegation, expiry or revocation epoch, and receipt obligations; capability, context access, route quality, or ambient process power alone confers none of it. |
| `system-boundaries-and-authority.problem.001` | `problem` | `normative` | `semantically_reviewed` | To test whether cross-layer effects are authorized, the stack needs explicit identities for the principal, execution domain, operation, target, permission class, ceiling, grant lifecycle, delegation, and receipt. |
| `system-boundaries-and-authority.insufficiency.001` | `insufficiency` | `source-synthesis` | `semantically_reviewed` | Role labels, prompts, and ambient process identity do not by themselves distinguish read, transform, disclose, write, execute, and approve authority or enforce delegation, expiry, revocation, and cross-domain approval. |
| `system-boundaries-and-authority.minimum.001` | `minimum` | `executable` | `semantically_reviewed` | The smallest honest implementation boundary for System Boundaries and Authority is: An authority-transition schema plus a unified authority-tuple lifecycle that binds execution-domain ownership, scope, budget, trace, replay, grant, revocation, cross-domain approval, receipts, and protocol-versus-hardware-root boundaries. |
| `system-boundaries-and-authority.beyond_sota.001` | `beyond_sota` | `composite` | `semantically_reviewed` | System authority needs a type system for the stack. Every model, tool, memory cell, field, artifact, human, project, and runtime route would carry explicit capability bounds so the architecture can distinguish what a component can do from what it may do. In the mature authority architecture, authority becomes typed, bounded, revocable, and attached to concrete principals, layers, fields, tools, artifacts, and routes. |
| `system-boundaries-and-authority.mechanism.001` | `mechanism` | `normative` | `semantically_reviewed` | Define principals, authorities, ceilings, grants, revocations, and handoff contracts. |
| `system-boundaries-and-authority.mechanism.002` | `mechanism` | `formal` | `semantically_reviewed` | Separate knowledge access from action authority. |
| `system-boundaries-and-authority.mechanism.003` | `mechanism` | `executable` | `semantically_reviewed` | Represent missing authority as a detectable failure rather than implicit permission. |
| `system-boundaries-and-authority.mechanism.004` | `mechanism` | `executable` | `semantically_reviewed` | Bind principal, execution domain, operation, target, permission class, scope, budget account, trace, replay identity, grant, policy version, revocation epoch, and expiry in one authority tuple. |
| `system-boundaries-and-authority.mechanism.005` | `mechanism` | `normative` | `semantically_reviewed` | Name execution-domain, budget, trace, and revocation owners and require target-owner approval for cross-domain handoffs. |
| `system-boundaries-and-authority.mechanism.006` | `mechanism` | `source-synthesis` | `semantically_reviewed` | Keep protocol-security controls separate from hardware-root evidence and claims. |
| `system-boundaries-and-authority.mechanism.007` | `mechanism` | `formal` | `semantically_reviewed` | Classify every requested permission as read, transform, disclose, write, execute, or approve and reject implicit promotion between classes. |
| `system-boundaries-and-authority.interface.001` | `interface` | `executable` | `semantically_reviewed` | Governance issues versioned ceilings and grants with explicit issuer, scope, expiry, and revocation authority. |
| `system-boundaries-and-authority.interface.002` | `interface` | `executable` | `semantically_reviewed` | Execution consumes the bound authority tuple before an effect and emits an effect or denial receipt afterward. |
| `system-boundaries-and-authority.interface.003` | `interface` | `executable` | `semantically_reviewed` | Evidence consumes authority receipts and records missing, inconsistent, expired, revoked, over-ceiling, or cross-domain failures. |
| `system-boundaries-and-authority.invariant.001` | `invariant` | `formal` | `semantically_reviewed` | Authority never expands silently. |
| `system-boundaries-and-authority.invariant.002` | `invariant` | `formal` | `semantically_reviewed` | Read permission is not write permission. |
| `system-boundaries-and-authority.invariant.003` | `invariant` | `formal` | `semantically_reviewed` | Tool execution requires an explicit grant. |
| `system-boundaries-and-authority.invariant.004` | `invariant` | `formal` | `semantically_reviewed` | Delegated authority preserves grant, budget, trace, replay, and revocation identity while narrowing scope. |
| `system-boundaries-and-authority.invariant.005` | `invariant` | `formal` | `semantically_reviewed` | Cross-domain authority requires target-domain owner approval. |
| `system-boundaries-and-authority.invariant.006` | `invariant` | `formal` | `semantically_reviewed` | Protocol security does not establish a hardware root of trust. |
| `system-boundaries-and-authority.invariant.007` | `invariant` | `formal` | `semantically_reviewed` | Approval authority remains separate from execution authority and cannot be self-issued by the executor. |
| `system-boundaries-and-authority.invariant.008` | `invariant` | `executable` | `semantically_reviewed` | Grant expiry, revocation, delegation depth, and denied escalation remain visible to every downstream authority consumer. |
| `system-boundaries-and-authority.failure_mode.001` | `failure_mode` | `causal` | `semantically_reviewed` | Repeated unrecorded widening, permissive defaults, or exception accumulation can make active authority exceed the reviewed ceiling. |
| `system-boundaries-and-authority.failure_mode.002` | `failure_mode` | `causal` | `semantically_reviewed` | A higher-authority tool can launder ambient power for a lower-authority requester when the operation is not bound to the requester's ceiling and grant. |
| `system-boundaries-and-authority.failure_mode.003` | `failure_mode` | `causal` | `semantically_reviewed` | Treating memory or source access as disclosure, execution, or approval authority can convert available context into unauthorized effects. |
| `system-boundaries-and-authority.failure_mode.004` | `failure_mode` | `causal` | `semantically_reviewed` | Forking grant, budget, trace, replay, or revocation identity can let subsystems accept locally valid records that no longer describe one authorized effect. |
| `system-boundaries-and-authority.failure_mode.005` | `failure_mode` | `causal` | `semantically_reviewed` | A source-domain grant or historical receipt can be laundered into target-domain or current-epoch authority when target approval and revocation epoch are not rebound. |
| `system-boundaries-and-authority.failure_mode.006` | `failure_mode` | `causal` | `semantically_reviewed` | Presenting protocol authentication, encryption, signatures, replay windows, or device-derived keys as hardware-root evidence overstates the trust boundary. |
| `system-boundaries-and-authority.failure_mode.007` | `failure_mode` | `causal` | `semantically_reviewed` | Delayed or missing lifecycle propagation can leave expired or revoked grants usable in downstream or delegated contexts. |
| `system-boundaries-and-authority.failure_mode.008` | `failure_mode` | `causal` | `semantically_reviewed` | A replacement implementation can inherit authority handles qualified only for its predecessor, bypassing requalification and changing the effective authority subject. |
| `system-boundaries-and-authority.formal.authority-ceiling-operational-invariant` | `formal_target` | `formal` | `semantically_reviewed` | Every successful finite run preserves observation/effect accounting, live-grant ceiling/epoch/revocation safety, exact approval/dispatch custody, and a valid transition trace; accepted issuance, dispatch, and effect remain exactly grant-bound. |
| `system-boundaries-and-authority.formal.authority-ceiling-failure-blocks-promotion` | `formal_target` | `formal` | `semantically_reviewed` | Revoked grant IDs persist and cannot approve, dispatch, or commit an effect in any successful suffix; the independent consumer recompiles the exact surface and checks one-use, two-use, and revocation traces, every prefix and batch split, and 50 state-noninterfering mutations. |
| `system-boundaries-and-authority.formal.authority-lifecycle-admission-route` | `formal_target` | `formal` | `semantically_reviewed` | The exact thirty-one-theorem grant-to-effect refinement and independent consumer preserve six authority-decision fixtures, arbitrary-run state invariants, valid traces, batch composition, exact grant binding, and explicit denial, rollback, and revocation routes. |
| `system-boundaries-and-authority.formal.authority-revocation-trace-surface-bridge` | `formal_target` | `formal` | `semantically_reviewed` | Revoked grant IDs persist through every successful suffix, which excludes approval, dispatch, or effect under the revoked ID; rejected events return no successor, while the independent consumer preserves the five-entry cross-artifact revocation trace and zero support effect. |

## Argument-exit state

No promotion-or-refutation campaign is frozen yet. P1 must first replace every machine candidate with a semantic review and adjudicate every prose-only candidate.

## Non-claims

- This dossier does not establish semantic adequacy, implementation behavior, empirical benefit, transfer, safety, or SOTA status.
- All support movement requires a separate accepted evidence-transition record.
