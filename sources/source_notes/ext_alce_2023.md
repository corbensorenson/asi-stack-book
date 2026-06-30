# Source Note: Enabling Large Language Models to Generate Text with Citations

| Field | Value |
|---|---|
| Source ID | `ext_alce_2023` |
| Source title | Enabling Large Language Models to Generate Text with Citations |
| Ingestion date | 2026-06-28 |
| Source version / URL | arXiv:2305.14627, https://arxiv.org/abs/2305.14627 |
| Citation label | Gao et al. (2023), ALCE |
| Published / updated | 2023-05-24 / 2023-10-31 |
| DOI | 10.48550/arXiv.2305.14627 |
| Ingestion basis | Primary arXiv metadata and abstract inspected for the retrieval/citation literature queue; benchmark data, code, model outputs, and citation evaluations are not imported into this repository. |

## Thesis

ALCE belongs in the VCM, verification-bandwidth, claim-ledger, and benchmark chapters as an external reference for citation-backed generation. It helps the ASI Stack treat retrieved evidence and citation quality as measurable surfaces rather than assuming that a retrieved passage automatically supports a generated answer.

## Mechanisms

- Require end-to-end systems to retrieve supporting evidence and generate answers with citations.
- Evaluate generated answers across fluency, correctness, and citation quality.
- Use diverse questions and retrieval corpora so citation support can be compared across systems.
- Identify incomplete citation support even when generated answers look plausible.

## Evidence

- The source reports ALCE as a benchmark for automatic LLM citation evaluation and notes substantial remaining citation-support gaps in its evaluated systems.
- This repository has not run ALCE, imported its corpora, reproduced model scores, or audited generated citations.
- Use this source as external vocabulary for citation-quality and evidence-support evaluation, not as local VCM or claim-ledger evidence.

## Failure Modes

- Citation presence can be mistaken for citation support when the cited passage does not actually entail the generated claim.
- Fluency can hide correctness and citation-quality failures.
- Imported citation metrics can become benchmark gaming if evidence boundaries, held-out corpora, and evaluator behavior are not recorded.

## Book Chapters Supported

- `virtual-context-abi` (The Virtual Context ABI: Typed Pages, Cells, and Certificates)
- `verification-bandwidth-and-context-adequacy` (Verification Bandwidth and Context Adequacy)
- `claim-ledgers-and-belief-revision` (Claim Ledgers and Belief Revision)
- `benchmark-ratchets-and-anti-goodhart-evidence` (Benchmark Ratchets and Anti-Goodhart Evidence)

## Claims To Add Or Update

- Use this note to sharpen citation-quality and evidence-support vocabulary.
- Do not claim that VCM, claim ledgers, or reader-facing citations satisfy ALCE-style support without a local evaluation record.
- Keep support state at `argument` until citation-evaluation fixtures, benchmark runs, or accepted evidence transitions exist.

## Open Questions

- Which claim-ledger record should distinguish cited, entailed, contradicted, and unsupported spans?
- What VCM packet fields should preserve enough provenance for later citation-quality scoring?
- How should benchmark ratchets prevent citation metrics from rewarding shallow citation stuffing?
