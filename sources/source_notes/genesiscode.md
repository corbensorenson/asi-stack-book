# Source Note: GenesisCode

| Field | Value |
|---|---|
| Source ID | `genesiscode` |
| Source title | GenesisCode |
| Ingestion date | 2026-06-24 |
| Source version / URL | Google Docs source in inventory: https://docs.google.com/document/d/1w4gKcF9a7oV6hsUECsWeEafblvc78ZusxaxdUTfLR2M |
| Ingestion basis | Local raw cache inspected at `sources/raw/google_docs/genesiscode.txt`; raw text is not published. |

## Thesis

GenesisCode frames AI-assisted programming as an evidence-carrying software system rather than a trust relationship with generated code. Its core move is to put a tiny deterministic calculus, explicit effect boundaries, hardened protocol invariants, semantic patches, replayable logs, and obligation artifacts between AI proposals and executable software.

## Mechanisms

- Use a minimal pure functional kernel with immutable data, lexical closures, and a small trusted computing base.
- Represent code in a canonical intermediate form with stable provenance hashes so AI edits can be reviewed as semantic patches instead of free-form text mutations.
- Keep all nondeterminism, including I/O, time, randomness, networking, and model calls, behind capability boundaries.
- Record deterministic effect logs so executions can be replayed and audited.
- Require packages and extensions to carry obligations such as tests, property checks, proofs, resource budgets, determinism claims, capability policies, and compiler-equivalence checks.
- Treat optimizers, JITs, foreign-function bridges, and generated code as outside the trusted core unless translation validation or equivalent evidence is attached.
- Use unforgeable protocol seals to distinguish ordinary data from privileged control responses, errors, effect requests, and unhandled messages.

## Evidence

- The source is a technical specification for an AI-native programming system with a small kernel and a larger verification/provenance envelope.
- It provides concrete architectural roles, artifact types, trust-boundary distinctions, and validation obligations.
- It does not provide a local implementation, local proof artifact, benchmark result, or security audit in this repository.
- Claims derived from this note should therefore remain at `argument` or `source-derived` support unless a GenesisCode prototype, replay checker, or proof module is added and validated here.

## Failure Modes

- Treating AI-generated code as trusted because it is syntactically valid.
- Letting nondeterministic effects bypass capability checks or replay logs.
- Allowing optimizer or compiler output to escape without translation validation.
- Using text diffs where semantic patch artifacts are required for auditability.
- Growing the trusted computing base until the small-kernel argument no longer applies.
- Mistaking obligation metadata for discharged obligations.

## Book Chapters Supported

- `system-boundaries-and-authority` (System Boundaries and Authority)
- `intent-to-execution-contracts` (Command Contracts: From Intent to Executable Work; includes folded command-contract semantic-interface material)
- `cognitive-compilation-and-semantic-ir` (Cognitive Compilation and Semantic IR)
- `spinoza-verification-and-proof-carrying-claims` (Spinoza Verification and Proof-Carrying Claims)
- `labor-os-and-typed-jobs` (Labor OS and Typed Jobs)
- `artifact-graphs-audit-logs-and-replay` (Artifact Graphs, Audit Logs, and Replay)
- `runtime-adapters-tool-permissions-and-human-approval` (Runtime Adapters, Tool Permissions, and Human Approval)
- `mathematical-and-search-substrates` (Mathematical and Search Substrates)
- `executable-specifications-and-lean-proof-envelope` (Executable Specifications and Lean Proof Envelope)
- `open-research-agenda-and-bibliography-plan` (Open Research Agenda and Bibliography Plan)

## Claims To Add Or Update

- Use GenesisCode as a source for the book's distinction between proposal generation, capability-mediated execution, and evidence-carrying acceptance.
- Use it to support semantic patching, provenance hashes, effect logs, replay, obligations, and small-TCB discipline.
- Do not claim that GenesisCode is implemented, benchmarked, secure, or mechanically verified inside this repo unless those artifacts are later added and pass validation.

## Open Questions

- Should the book prototype a minimal semantic patch schema under `schemas/` before drafting stronger implementation language?
- Which GenesisCode obligations should map directly into Appendix C support states?
- Should a small Lean module formalize capability-mediated effect requests as a follow-on to the existing stack-boundary proofs?
