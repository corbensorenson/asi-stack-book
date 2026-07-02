# RankFold Artifact Import

This directory records public-safe metadata from existing local RankFold output
artifacts. It does not contain source dataset bytes, archive bytes, private
paths, or unpublished implementation content.

The current result records three `.rfa` archive observations for the same
100,000,000-byte decoded artifact digest, their archive sizes and hashes, and
read-only `rfa verify` / `rfa inspect` summaries. The validator checks the
record math and non-claim boundaries only.

This is not a fresh benchmark run, not a deployed compressor result, not a
codec-correctness proof, not a downstream utility test, and not a chapter-core
support-state promotion.
