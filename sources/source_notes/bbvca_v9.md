# Source Note: BBVCA v9

| Field | Value |
|---|---|
| Source ID | `bbvca_v9` |
| Source title | BBVCA_v9_final_public_release |
| Ingestion date | 2026-06-24 |
| Source version / URL | Google Docs source in inventory: https://docs.google.com/document/d/1dCcqTteePCyUb66H3qJ-50uYMNDdqHFG7-qQpHSvVaA |
| Ingestion basis | Local raw cache inspected at `sources/raw/google_docs/bbvca_v9.txt`; raw text is not published. |

## Thesis

BBVCA v9 defines generate-verify-repair compression under a contract-relative reconstruction discipline. A practical compressor should search for compact shared-law explanations, verify local generated structure, and pay exact repair costs for whatever the generator cannot honestly explain.

## Mechanisms

- Define a reconstruction contract specifying what must be reproduced, arithmetic semantics, and allowed liberties.
- Move repeatable explanatory burden into public law families when doing so reduces total description length.
- Exclude any claim that arbitrary larger data can be recovered from a strictly smaller private apex representation alone.
- Bound verification inside local interaction regions.
- Preserve exactness at each layer through retained detail, residuals, literals, repair streams, and fallback.
- Charge partition and interface boundaries as first-class rate costs.
- Use a bounded non-overlapping additive Prototype A search path.
- Separate search-time proxy-rate scoring from final entropy-coded serialization.
- Bootstrap and calibrate proxy tables, then refresh them when realized rate diverges.

## Evidence

- The source is a public research whitepaper and hardening pass.
- It provides mature conceptual rules, rate-accounting discipline, and implementation constraints.
- The repository has not implemented BBVCA Prototype A or reproduced compression ratios.
- Treat v9 as stronger than earlier BBVCA variants for book discussion because it explicitly handles proxy-rate honesty.

## Failure Modes

- Claiming universal compression without exact repair and rate accounting.
- Letting search-time proxies masquerade as final code length.
- Pruning promising branches with miscalibrated proxy rates.
- Ignoring boundary/interface costs.
- Allowing approximation drift across layers.
- Treating cosmological metaphor as physics or codec proof.

## Book Chapters Supported

- `the-efficient-asi-hypothesis` (The Efficient ASI Hypothesis)
- `generate-verify-repair-compression` (Generate-Verify-Repair Compression)
- `rankfold-neuralfold-and-artifact-compression` (RankFold, NeuralFold, and Artifact Compression)

## Claims To Add Or Update

- Use BBVCA v9 as the primary source for generate-verify-repair compression and proxy-rate discipline.
- Avoid earlier overbroad universality language unless it is bounded by v9's reconstruction contract and repair streams.

## Open Questions

- Should the book implement a toy generate-verify-repair codec fixture?
- Which BBVCA principles are suitable for Lean invariants versus empirical compression tests?
