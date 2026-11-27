# ByteFlow: Language Modeling through Adaptive Byte Compression without a Tokenizer

| Field | Value |
|---|---|
| Source ID | `ext_byteflow_2026` |

Chunyuan Deng, Sanket Lokegaonkar, Colin Lockard, Besnik Fetahu, Nasser Zalmout, Xian Li. [Primary paper, arXiv 2603.03583v1](https://arxiv.org/html/2603.03583v1).

## Thesis

Byte-level models can learn variable boundaries inside a fixed compute budget.

## Mechanisms

Use local coding-rate scores to select top-K boundary positions inside a fixed computation shape.

## Evidence

Table 3 compares chunking rules inside the same 0.6B architecture trained on the reported 50B-token scale and averages three runs.

## Failure Modes

Section 4.4, Table 3. Bits per byte and downstream scores describe those configurations. A boundary score does not certify semantic fidelity on a new language or task.

## Book Chapters Supported

- `replaceable-cognitive-substrates-beyond-transformer-monoculture` — [A fixed budget for learned byte boundaries](https://corbensorenson.github.io/asi-stack-book/chapters/replaceable-cognitive-substrates-beyond-transformer-monoculture.html#a-fixed-budget-for-learned-byte-boundaries)

## Claims To Add Or Update

Compare boundary policies inside the same model before attributing an improvement to adaptive coding.

## Open Questions

Do the selected boundaries preserve a rare identifier when the input mix changes?
