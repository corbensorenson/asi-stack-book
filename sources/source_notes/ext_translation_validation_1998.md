# Source Note: Translation Validation

| Field | Value |
|---|---|
| Source ID | `ext_translation_validation_1998` |
| Source title | Translation Validation |
| Ingestion date | 2026-07-02 |
| Source version / URL | Weizmann record, https://weizmann.esploro.exlibrisgroup.com/esploro/outputs/conferenceProceeding/Translation-validation/993262143603596 |
| Citation label | Pnueli, Siegel, and Singerman (1998), Translation Validation |
| Published / updated | 1998 / 1998 |
| Ingestion basis | Public bibliographic record and abstract inspected for the Cognitive Compilation external literature queue; paper not vendored, and no translation validator, semantic framework, refinement checker, or simulation proof was run from this repository. |

## Thesis

Translation validation is the direct comparator for the Cognitive Compilation chapter's lowering receipts. It shifts attention from proving a compiler correct once to checking each translation run after it happens. That maps cleanly onto the ASI Stack boundary: every lowered cognitive artifact should carry enough source, target, obligation, assumption, validator, and residual information for the translation to be checked before the artifact is treated as accepted.

## Mechanisms

- Validate each individual compiler or code-generator run after translation.
- Use a common semantic framework for source and target representations.
- Formalize correct implementation as a refinement relation.
- Use a simulation-based proof method to verify that produced target code implements source code.
- Treat validation as a post-translation acceptance phase rather than an assumption about all compiler runs.

## Evidence

- The public record describes translation validation as an alternative to verifying translators in advance.
- The abstract names source/target semantic frameworks, refinement, and simulation-based proof as ingredients.
- This repository has not implemented a translation validator, semantic framework, refinement checker, simulation proof, or source-to-target artifact comparison.
- Use this source for lowering-validation lineage only.

## Failure Modes

- A lowering receipt without a source/target relation can become a build log rather than a validation artifact.
- A validator can check syntax or schema conformance while missing semantic obligations.
- Per-translation validation can still fail if the source semantics omit the user intent, authority boundary, or evidence requirement.

## Book Chapters Supported

- `cognitive-compilation-and-semantic-ir` (Cognitive Compilation and Semantic IR)
- `executable-specifications-and-lean-proof-envelope` (Executable Specifications and Lean Proof Envelope)

## Claims To Add Or Update

- Use translation validation to explain why semantic lowering receipts must compare source obligations and target artifacts instead of merely recording that a generation pass occurred.
- Do not claim a translation validator, refinement proof, semantic-equivalence checker, compiler-correctness result, or target-artifact proof.

## Open Questions

- What is the smallest semantic-atom lowering receipt that can support a source/target preservation check?
- Should future chapter-section compilation include negative controls where target prose is fluent but drops an obligation?
- Which Lean or Python fixture can bridge semantic-atom records to a concrete lowering-validation decision?
