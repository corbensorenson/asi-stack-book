# Source Note: Ladon & The Manhattan Protocol

| Field | Value |
|---|---|
| Source ID | `ladon_manhattan` |
| Source title | Ladon & The Manhattan Protocol |
| Ingestion date | 2026-06-24 |
| Full-fidelity review | 2026-07-31 |
| Source version / URL | Google Docs source in inventory: https://docs.google.com/document/d/1uT9iQ7Jb2TsU9DletvtVeLEej63aIQl3WS3jTsMgtSM |
| Ingestion basis | Complete local raw cache inspected at `sources/raw/google_docs/ladon_manhattan.txt` (129 lines; approximately 1,303 words). Raw text is not published. |
| Evidence role | Corben-authored security architecture and pseudocode lineage; no implementation or security result. |

## Thesis

The durable thesis is capability separation: an agent can be authorized to
request a narrowly scoped operation without receiving the credential bytes or
general authority behind that operation. Secret custody, caller identity,
purpose, parameters, destination, use count, time, approval, policy, and
response constraints belong to a trusted mediation path. Computations that
must touch sensitive material require a declared isolation and egress boundary,
and the resulting effect or derivative remains security-sensitive even when
the raw secret never appears in model context.

## Mechanisms

- Keep raw credentials outside the model-visible prompt, ordinary application
  heap, logs, and rendered UI where the platform permits. Use a hardened secret
  manager, OS facility, HSM, enclave, or remote signer appropriate to the
  threat model rather than treating all of those mechanisms as equivalent.
- Give the agent an opaque, unforgeable, short-lived capability reference. The
  token resolves only for a named principal, operation, target, parameter
  schema, purpose, destination, budget, time, nonce, and policy version.
- Collect secrets through a trusted input path whose provenance and actual
  platform isolation are independently observable. The AI-facing application
  receives only the authorized reference and minimum metadata.
- Perform late substitution or remote use at a complete mediation boundary.
  Recheck current lease, caller, scope, destination, payload, rate, approval,
  revocation, and policy on every use; do not merely replace a recognizable
  string in an arbitrary request.
- For computations requiring plaintext, create a compartment with a stated
  isolation grade and lifecycle: spawn, admit code/data, inject, execute,
  mediate effects and egress, declassify or refuse outputs, close handles,
  zeroize reachable buffers at the supported grade, destroy, revoke, audit,
  recover, and retain residuals.
- Treat returned signatures, transaction hashes, decrypted outputs, API
  responses, timing, error differences, and use/no-use behavior as derivatives
  and possible oracles. Secret non-disclosure is distinct from prevention of
  unauthorized use or harmful effects.

## Interfaces and invariants

`security-kernel-and-digital-scifs` is the canonical owner. Runtime Adapters
owns effect calls and approval; System Boundaries owns principal and authority;
Context Transactions owns taint, derived state, and deletion closure; Supply
Chain and Confidential Computation own trusted-component and protected-
execution assumptions. The source is related to those chapters as one author-
side lineage, not independent corroboration.

Key invariants are: a handle cannot authorize itself; possession and use are
different; every use is revalidated; parameter and destination scope cannot
expand through substitution; secret absence from context does not imply
authority safety; output sanitization and declassification are separate;
revocation reaches derived sessions, caches, and queued effects where possible;
and zeroization claims never exceed the measured platform boundary.

## Evidence

The paper contains architecture prose, a sequence diagram, an illustrative
Rust structure, an unsafe function sketch, and two named “theorems.” There is
no `ladon-rs` package, kernel module, build, hardware target, trusted UI,
capability service, remote signer, compartment, policy engine, test trace,
attack suite, formal proof, side-channel measurement, audit, or independent
reproduction in this repository. The book's synthetic Security Kernel fixtures
exercise record routing only and do not validate Ladon.

## Failure Modes

- The handle is a guessable string, bearer token, replay oracle, or metadata
  leak revealing account, environment, privilege, or asset identity.
- Credential secrecy is preserved while the agent can make arbitrary charges,
  signatures, messages, deployments, or queries with the credential.
- A substitution layer checks the handle but not caller, destination, payload,
  purpose, rate, time, approval, or current revocation.
- The trusted UI is spoofed, inaccessible, observed through the application,
  or unavailable on the claimed platform.
- Secrets or derivatives escape through formatted strings, stack and register
  copies, allocator behavior, kernel/network buffers, TLS libraries, logs,
  crash dumps, swap, snapshots, backups, accelerators, timing, caches, power,
  errors, or output oracles.
- A compartment has nominally no network or shared memory but can still affect
  the host, filesystem, scheduler, caller, or returned output.
- Random timing jitter or page coloring is treated as a general side-channel
  defense without threat-specific measurement.
- Revocation stops future lookup while active sessions, queued requests,
  cached tokens, downstream services, or completed irreversible effects remain.
- Concentrating keys and policy in one manager creates a high-value trusted-
  computing-base and availability bottleneck.

## Explicitly rejected or bounded claims

- Environment variables and `.env` files are not universally “catastrophic”;
  their risk depends on process, host, deployment, and threat boundaries.
- SGX, TrustZone, Apple Secure Enclave, HSMs, protected pages, remote signers,
  and kernel memory are not interchangeable generic secret-page mechanisms.
- `PROT_NONE` is an address-space permission, not proof of a kernel enclave,
  air gap, non-extractability, side-channel safety, or host-compromise safety.
- A hardware-composited overlay rendered “directly by the kernel's display
  driver” is a platform-specific proposal, not a demonstrated portable path.
- The illustrative Rust code is not an implementation: it uses an undefined
  socket buffer, constructs additional secret-bearing strings, leaves protocol
  framing and TLS unspecified, and does not establish cleanup of all copies.
- Rust memory safety does not make unsafe kernel/substitution code, policy,
  cryptography, side channels, or zeroization correct.
- The “Ignorance Theorem” is false as a theorem. A model can infer a secret,
  exploit its capability, query an oracle, induce disclosure elsewhere, or
  leak derivatives without holding the literal bit sequence in context.
- The “Ephemerality Theorem” is false as a theorem. A short intended lifetime
  does not make RAM-dump, register, cache, crash, concurrent, or remanence risk
  statistically negligible without measurements and a threat model.
- A signed result or transaction hash is not automatically non-sensitive or
  safe; it may embody an irreversible unauthorized effect.

## Section-family closure

| Section | Disposition |
|---|---|
| Agency Paradox and right-to-use versus knowledge-of-secret | Integrated as capability and authority separation, with harmful-use and effect boundaries added. |
| Vault, memory pages, and handle system | Integrated in Security Kernel as implementation-specific custody plus caller-bound leases; platform equivalence claims rejected. |
| Golden Interface | Retained as trusted-input-path design lineage and a research obligation; no portable implementation claim. |
| Syscall interception and late substitution | Integrated as complete mediation with exact caller, payload, target, destination, and policy binding rather than textual replacement. |
| Digital SCIF lifecycle | Integrated in the stronger authority-use and declassification transaction, including derivative outputs and recovery. |
| Cache partitioning and execution jitter | Retained as threat-specific candidate mitigations only; no side-channel claim. |
| Rust crate sketch | Retained as incomplete pseudocode and a useful negative implementation example. |
| Ignorance and Ephemerality “theorems” | Explicitly rejected as theorems and converted into narrower exposure-reduction hypotheses. |

## Book Chapters Supported

- `security-kernel-and-digital-scifs`
- `runtime-adapters-tool-permissions-and-human-approval`
- `system-boundaries-and-authority`
- `context-transactions-snapshots-mounts-and-taint`
- `confidential-and-verifiable-ai-computation`
- `ai-supply-chain-integrity-and-lifecycle-provenance`
- `moral-uncertainty-and-value-conflict`: capability use and protected-state handling must preserve affected-party and harm boundaries; secret non-disclosure does not decide moral permissibility.
- `stable-capability-fields`: opaque handles and caller-bound scope motivate capability identity and compatibility fields without proving equivalence or safe replacement.
- `personal-compute-hives-and-federated-edge-intelligence`: local compartments and remote-use handles supply bounded federation context; no device, enclave, or hive security result is established.

No new chapter or prose section is warranted. The Security Kernel chapter
already states the full corrected mechanism, including capabilities,
isolation grades, complete egress, declassification, revocation, side channels,
availability, recovery, and non-claims.

## Claims To Add Or Update

- Retain Ladon as the author-side origin of blind-handle and late-substitution
  pressure while keeping it below the canonical Security Kernel contract.
- Treat “model does not receive literal secret bytes” as one exposure control,
  not a security theorem or authorization result.
- Keep harmful use, derivative disclosure, output effects, revocation closure,
  and platform-specific isolation in every future implementation claim.

## Research obligations and falsifiers

1. Freeze a real threat model, platforms, secrets, principals, operations,
   effects, attackers, channels, trusted components, and recovery assumptions.
2. Compare ordinary secret managers plus scoped APIs, remote signing,
   application sandboxes, capability systems, protected execution, and the
   proposed full transaction under matched tasks and budgets.
3. Attack handle guessing, theft, replay, confused deputy, payload and
   destination substitution, prompt injection, tool injection, privilege
   composition, logs, errors, caches, timing, crash state, revocation races,
   output oracles, and irreversible harmful use.
4. Measure task success, unauthorized effect, literal and semantic disclosure,
   false denial, latency, throughput, availability, recovery, operator burden,
   trusted-core size, and residual reachability.
5. Falsify the design if ordinary scoped service APIs perform as well, if the
   mediation path is bypassable, or if secret hiding does not reduce total
   unauthorized disclosure and effect risk.

## Open Questions

- Which operations should use non-exportable keys or remote signers instead of
  ever materializing plaintext in a local compartment?
- How can a user verify that a credential-entry surface is trusted and bound to
  the intended operation and application?
- Which derived outputs require the same or a lower-but-still-protected label?
- How should revocation and compensation behave after a permitted capability
  has already caused an irreversible external effect?
