# ByteFlow: Language Modeling through Adaptive Byte Compression without a Tokenizer

Chunyuan Deng, Sanket Lokegaonkar, Colin Lockard, Besnik Fetahu, Nasser Zalmout, Xian Li. [Primary paper, arXiv 2603.03583v1](https://arxiv.org/html/2603.03583v1).

## Mechanism and evidence

Use local coding-rate scores to select top-K boundary positions inside a fixed computation shape.

Table 3 compares chunking rules inside the same 0.6B architecture trained on the reported 50B-token scale and averages three runs.

## Reviewed passage and limits

Section 4.4, Table 3. Bits per byte and downstream scores describe those configurations. A boundary score does not certify semantic fidelity on a new language or task.

## Book Chapters Supported

- `replaceable-cognitive-substrates-beyond-transformer-monoculture`
