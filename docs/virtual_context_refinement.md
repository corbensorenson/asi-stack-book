# Virtual Context ABI reachable-refinement receipt

Recorded: 2026-07-15
Roadmap: `post-v2.3-claim-proof-and-sota-challenge-roadmap` P2/M3
Support-state effect: `none`

## Outcome

`lean/AsiStackProofs/VirtualContextRefinement.lean` replaces two assumption-projection declarations with an exact 39-theorem reachable request, resolver, certificate, materialization, mandatory-miss, denial, and terminal-state semantics. State carries exact abstract identities for request, address, version, snapshot, mount, source, and derived representation; an authority ceiling and approved authority; lease time; resolver, certificate, materialization, and typed-fault receipts; materialization emission; support and external-effect authority boundaries; stage; and logical time.

The four-event success witness binds one request, resolves an exact unexpired permitted hit, certifies its source-bound derived representation without authority widening or completeness overclaim, and materializes it with receipt custody. The two-event mandatory-miss witness produces a typed-fault receipt and no materialization. Lean proves arbitrary successful runs from a bound request preserve request identity, every successful run preserves the authority ceiling and support/external-effect authority, accepted runs expose valid traces and exact batch composition, materialization requires a fresh lease and complete receipts, mandatory misses preserve exact identity and fault/materialization exclusion, and materialized, typed-fault, and denied states are absorbing.

`python3 scripts/validate_virtual_context_refinement.py` independently reimplements the transition relation and recompiles the exact theorem surface. It rechecks all eleven prior resolver scenarios—two valid and nine expected-invalid—without trusting their decision digest, consumes the separate context-admission suite at its exact three-valid/five-invalid boundary, accepts both reachable witnesses, checks all eight prefix/suffix composition splits, and rejects 73 of 73 mutations across binding, authority, lease, source/certificate identity, omission, overclaim, taint, receipts, terminal reentry, fault/materialization exclusivity, support, external effect, and time.

## Exact boundary

This is finite structured-record evidence. Numeric identifiers establish equality only, not natural-language address truth, payload meaning, summary fidelity, or certificate truthfulness. The context-admission suite remains a distinct prior harness: admission validity is not resolver or materialization correctness. Authority, lease, mount permission, source hashes, certificate assertions, taint flags, and receipts remain trusted abstract inputs. The packet does not establish a deployed resolver, memory store, context compiler, transaction isolation, deletion enforcement, model-facing context quality, leak prevention, natural-workload usefulness, reproduction, transfer, safety, SOTA, AGI, ASI, or chapter-core support. It creates no effect, evidence transition, support transition, or release transition.
