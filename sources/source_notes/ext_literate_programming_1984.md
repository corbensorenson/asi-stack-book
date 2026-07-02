# Source Note: Literate Programming

| Field | Value |
|---|---|
| Source ID | `ext_literate_programming_1984` |
| Source title | Literate Programming |
| Ingestion date | 2026-07-01 |
| Source version / URL | Oxford Academic record, https://academic.oup.com/comjnl/article/27/2/97/343244 |
| Citation label | Knuth (1984), Literate Programming |
| Published / updated | 1984-01-01 / 1984-01-01 |
| DOI | 10.1093/comjnl/27.2.97 |
| Ingestion basis | Public publisher metadata inspected for the Living Book Methodology external-positioning queue; article text not vendored into this repository and no WEB/CWEB toolchain implemented. |

## Thesis

Literate programming is the external lineage source for treating a technical artifact as both executable structure and human-readable exposition. It helps position the ASI Stack living book as a governed source graph that renders prose, rather than as prose loosely accompanied by scripts.

## Mechanisms

- Organize explanation around human comprehension rather than only compiler order.
- Preserve a relationship between source, generated documentation, and executable artifacts.
- Treat documentation as part of the artifact, not as an afterthought.
- Make later maintenance easier by preserving design intent alongside code structure.

## Evidence

- The source provides historical and methodological grounding for literate programming.
- This repository has not implemented WEB/CWEB, reproduced the paper's tooling, or proved that this book satisfies literate-programming ideals.
- Use this source as lineage and comparator vocabulary, not as support-state promotion.

## Failure Modes

- Polished exposition can still hide weak evidence if claim states are absent.
- A generated document can be mistaken for a reviewed or correct artifact.
- Code/prose coupling can drift if generation and validation are not checked.

## Book Chapters Supported

- `living-book-methodology` (Living Book Methodology)

## Claims To Add Or Update

- Use literate programming to position the living book's prose/code/source coupling lineage.
- Keep the ASI Stack method distinct: it adds source queues, claim states, evidence transitions, release records, reader projections, and non-claims that ordinary literate-programming lineage does not by itself provide.
- Do not claim the repository implements WEB/CWEB or proves manuscript quality from literate-programming lineage.

## Open Questions

- Which living-book change packet fields are the closest analogues of weave/tangle outputs?
- Would future proof/test snippets benefit from a stricter executable-document pattern?
- What validator would catch prose/code drift before publication?
