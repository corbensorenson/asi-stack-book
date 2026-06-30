# Source Note: Dafny: An Automatic Program Verifier For Functional Correctness

| Field | Value |
|---|---|
| Source ID | `ext_dafny_2010` |
| Source title | Dafny: An Automatic Program Verifier For Functional Correctness |
| Ingestion date | 2026-06-28 |
| Source version / URL | Microsoft Research publication page, https://www.microsoft.com/en-us/research/publication/dafny-automatic-program-verifier-functional-correctness/ |
| Citation label | Leino (2010), Dafny |
| Published / updated | 2010-04 / not recorded |
| DOI | not recorded |
| Ingestion basis | Primary Microsoft Research publication page inspected for program-verification vocabulary; paper not vendored into this repository and no Dafny program or verifier run reproduced. |

## Thesis

Dafny belongs in the proof-envelope, command-contract, runtime-adapter, and prototype-roadmap chapters as an external reference for specification-oriented programming and automatic functional-correctness verification. It helps the ASI Stack separate a typed contract, a verifier, an SMT-backed proof obligation, and an actual runtime artifact.

## Mechanisms

- Express functional-correctness obligations near the program text.
- Use a language and verifier together so proof obligations are closer to the problem domain.
- Rely on an SMT solver to automate parts of verification.
- Treat specifications, implementations, verifier output, and runtime execution as distinct artifacts.

## Evidence

- The source records the Dafny publication context and method claims from Microsoft Research.
- This repository has not written Dafny specifications, run Dafny, translated ASI Stack schemas into Dafny, or checked functional-correctness obligations with Dafny.
- Use this source as external program-verification vocabulary, not as local evidence for contract correctness.

## Failure Modes

- Verification can prove the wrong specification if the contract omits a safety-relevant obligation.
- Automation can hide solver assumptions, model gaps, or unverified runtime integration.
- A verified program fragment does not prove the surrounding AI workflow, tool policy, or source interpretation.

## Book Chapters Supported

- `executable-specifications-and-lean-proof-envelope` (Executable Specifications and Lean Proof Envelope)
- `intent-to-execution-contracts` (Command Contracts: From Intent to Executable Work; includes folded command-contract semantic-interface material)
- `runtime-adapters-tool-permissions-and-human-approval` (Runtime Adapters, Tool Permissions, and Human Approval)
- `prototype-roadmap` (Prototype Roadmap)

## Claims To Add Or Update

- Use this note to compare ASI Stack schemas, command contracts, and proof envelopes against external program-verification practice.
- Do not claim Dafny compatibility, Dafny proof output, or functional-correctness verification in this repository.
- Keep support state at `argument` until a verifier fixture, translated contract, or accepted evidence transition exists.

## Open Questions

- Which command-contract obligations should become verifier-ready preconditions and postconditions?
- What is the smallest verifier-backed runtime-adapter example worth building?
- How should the roadmap distinguish schema validation from functional-correctness verification?
