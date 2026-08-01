# Source Note: ORCP–MoECOT

| Field | Value |
|---|---|
| Source ID | `orcp_moecot` |
| Source title | ORCP–MoECOT: A Governed Oscillating Rail Cascade Codec |
| Ingestion date | 2026-07-31 |
| Source version / URL | Technical specification, 2026-03-03; https://drive.google.com/file/d/1J5sd32zKhp4pBjWTRyrpjNM-8_DpHpsY |
| Ingestion basis | Full authenticated connector text section-audited; raw private text is not published. |

## Thesis

ORCP–MoECOT specifies a deterministic lossless codec whose strongest transferable lesson is the decoder-boring principle: all search and adaptive refinement belong on the encoder side, while the archive transmits enough explicit plan, state, transform, and update information for a bounded decoder to reproduce exactly. Compression is judged by complete archive rate against baselines, not by model cleverness or hidden shared state.

## Mechanisms

- One shared codec core with separate encoder and decoder wrappers prevents implementation drift while preserving role asymmetry.
- A framed container binds header and block identities, semantic digests, compiler-contract digest, and CRC checks.
- Reversible transforms feed a fixed-point bitwise range coder.
- A hierarchical tree-gated mixture predictor combines local, match, and structural rails.
- A bounded MCO32 block planner searches encoder choices while active-frontier pruning keeps compute per bit bounded.
- Regime-specific meta-profiles and optional prime-lag features are transmitted or identified explicitly.
- Anti-experts contribute penalty/inhibition signals rather than negative probability mixture weights.
- Encoder-only refinement is accepted only when its bit savings exceed the transmitted update-packet overhead.
- Random or encrypted input may approach `p=.5`; universal input acceptance means correct bounded fallback, not universal compression.

## Evidence

- The complete technical specification was reviewed for format, transforms, entropy coder, predictor, planner, profiles, anti-experts, online refinement, boundedness, and fallback.
- The source supplies algorithms and invariants but no inspected implementation, released corpus, round-trip artifact, compression table, runtime measurement, or independent decoder result.
- The design is therefore a detailed comparator and implementation obligation, not codec evidence.

## Failure Modes

- Hiding encoder search, plan metadata, model state, update packets, or shared libraries outside the rate denominator.
- Letting decoder-side search or floating-point ambiguity break deterministic reconstruction.
- Calling “accepts arbitrary bytes” universal compression.
- Applying learned updates whose signaling cost exceeds their savings.
- Using anti-experts as negative mixture weights that invalidate probability semantics.
- Reporting CRC or digest integrity as proof of semantic or compression quality.

## Book Chapters Supported

- `compact-generative-systems-and-residual-honesty` — Compact Generative Systems: Generate, Verify, Repair, and Residual Honesty

## Claims To Add Or Update

- Add decoder symmetry and explicit plan transmission to the book's exact-reconstruction contract.
- Count refinement packets, model/profile identity, compiler contract, and all framing in final rate.
- Separate universal acceptance, exact round trip, and useful compression as three different claims.
- Require an independently implemented decoder and incompressible controls before any codec promotion.

## Open Questions

- Can the proposed predictor beat standard strong codecs after complete archive and compute accounting?
- Are the fixed-point and update rules sufficiently specified for cross-implementation bit identity?
- Do optional prime-lag features survive matched ablations and signaling cost?

## Section-Family Closure Ledger

| Family | Disposition | Book effect |
|---|---|---|
| Container, framing, digests, CRC | integrated | Exact-reconstruction contract includes archive identity and integrity boundaries. |
| Reversible transforms and range coder | integrated as codec specification | No implementation result inferred. |
| Rail mixture predictor and planner | integrated as candidate mechanism | Full compute and signaling costs remain charged. |
| Anti-experts and refinement packets | integrated | Probability and rate-accounting boundaries added. |
| Random/encrypted fallback | integrated | Universal acceptance is separated from useful compression. |
| Compression performance | research obligation | Requires implementation, baselines, independent decode, and transfer. |

## Non-Claims

This source does not establish a working ORCP codec, exact cross-implementation decoding, compression advantage, bounded real-world performance, semantic understanding, production readiness, or ASI. A technical specification is not a benchmark result.
