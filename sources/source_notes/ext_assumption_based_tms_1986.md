# Source Note: An Assumption-Based TMS

| Field | Value |
|---|---|
| Source ID | `ext_assumption_based_tms_1986` |
| Source title | An Assumption-Based TMS |
| Ingestion date | 2026-07-01 |
| Source version / URL | DOI metadata, https://doi.org/10.1016/0004-3702(86)90080-9 |
| Citation label | de Kleer (1986), An Assumption-Based TMS |
| Published / updated | 1986 / 1986 |
| DOI | 10.1016/0004-3702(86)90080-9 |
| Ingestion basis | DOI and public bibliographic metadata inspected for the assumption-based truth-maintenance literature queue; the full algorithm, code, and problem-solving demonstrations are not imported into this repository. |

## Thesis

This source belongs in `claim-ledgers-and-belief-revision` as an assumption-based truth-maintenance comparator. It helps the chapter distinguish a publication claim ledger from richer ATMS-style reasoning over assumption sets, inconsistent information, and context switching.

## Mechanisms

- Maintain assumption sets rather than only individual justifications.
- Track how conclusions depend on assumptions so multiple contexts can be considered.
- Support work with inconsistent information without immediately collapsing the reasoning process.
- Reduce some forms of backtracking by preserving dependency structure.

## Evidence

- The source is a journal article in Artificial Intelligence, 28(2):127-162, with DOI `10.1016/0004-3702(86)90080-9`.
- This repository has not implemented ATMS labels, reproduced de Kleer's algorithms, or tested multi-context assumption-set reasoning.
- Use this source as external lineage for assumption-set truth maintenance, not as evidence for a deployed ASI belief-revision engine.

## Failure Modes

- Treating ASI claim-ledger residuals as if they are complete ATMS environments.
- Inferring inconsistency-tolerant reasoning from a schema that only records contradiction state.
- Confusing cross-surface claim synchronization with assumption-set search or context switching.

## Book Chapters Supported

- `claim-ledgers-and-belief-revision` (Claim Ledgers and Belief Revision)

## Claims To Add Or Update

- Use this note to show that assumption-aware truth maintenance is prior art and that ASI claim ledgers occupy a narrower engineering role today.
- State that future claim-ledger work could learn from ATMS-style dependency and context machinery, but the current repository only has finite record discipline and synthetic fixtures.
- Keep chapter support at `argument` until local assumption-set, contradiction-quality, and context-switching evidence exists.

## Open Questions

- Should future ledger records separate assumptions, evidence, defeaters, and residuals more explicitly?
- What minimum fixture would test claim revision under two incompatible assumption contexts?
- Can a future Lean/Python bridge check assumption-set preservation without pretending to solve open-domain belief revision?
