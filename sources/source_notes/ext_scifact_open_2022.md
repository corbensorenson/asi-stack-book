# SciFact-Open: Towards open-domain scientific claim verification

| Field | Value |
|---|---|
| Source ID | `ext_scifact_open_2022` |
| Primary publication | Wadden et al. (2022). [Preprint used in the chapter](https://arxiv.org/abs/2210.13777) · [Findings of EMNLP publication and author metadata](https://aclanthology.org/2022.findings-emnlp.347/) |
| Reviewed | November 27, 2026. Sections 2–3 and 5, and the [authors’ annotation guide](https://github.com/dwadden/scifact-open/blob/main/doc/data.md). |

## Thesis

Pooling candidate documents from multiple systems can uncover evidence beyond the papers a claim originally cited.

## Mechanisms

The authors use claims from the original SciFact test set and annotate candidate abstracts from a 500,000-abstract corpus. The release identifies each document judgment as citation-derived or pooled. For a pooled document, sentence highlights come from retrieval systems.

## Evidence

The authors release 279 claims. The book uses a fixed subset of the released candidate corpus to compare four retrieval routes. Its fresh-paper rules and its full-human-highlight score are decisions of the local study.

## Failure Modes

Pooled highlights are model suggestions. Flattened citation-derived highlights can combine alternative human rationales. An unassessed paper may be relevant.

## Book Chapters Supported

- `verification-bandwidth-and-context-adequacy` — [Where the citation was lost](https://corbensorenson.github.io/asi-stack-book/chapters/verification-bandwidth-and-context-adequacy.html#fresh-citation-retrieval)

## Claims To Add Or Update

Score document verdicts separately from the evidence that certifies the proposed citation.

## Open Questions

How often would a separate annotator accept a shorter span or an unjudged retrieved abstract?
