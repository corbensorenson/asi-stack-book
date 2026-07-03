# Curated Reader Prose Pass: RankFold, NeuralFold, and Artifact Compression

Date: 2026-07-01

Evidence-boundary alignment: 2026-07-03

Follow-up: 2026-07-03

Status: reconciled for prose meaning on 2026-07-03.

Chapter: `rankfold-neuralfold-and-artifact-compression`

Reader manuscript file: `editions/reader_manuscript/v1_0/chapters/rankfold-neuralfold-and-artifact-compression.qmd`

Live source file: `chapters/rankfold-neuralfold-and-artifact-compression.qmd`

## Reader Promise

This pass should let a human reader understand artifact compression as a routing and evidence problem, not a storage trick.

The reader throughline is:

> a compressed artifact earns one use at a time.

## Curation Scope

- Added a second 2026-07-03 reconciliation pass that positions artifact
  compression after fast generation: the shortcut-accounting rule applies both
  to output over time and to stored artifacts that the stack wants to keep,
  move, and reuse.
- Reworked the generated reader opening into a stronger archive-facing premise.
- Centered the chapter stakes on the difference between cheaper artifact handling and quiet evidence substitution.
- Preserved the RankFold/NeuralFold, RankFold compressor, BBVCA, CGS, and resource-economics source boundaries.
- Preserved the compressed-artifact gate Mermaid diagram and its meaning.
- Preserved the minimum viable implementation and beyond-SOTA sections without implying that a compressor, deterministic decoder, corpus benchmark, utility probe, or artifact admission system already exists.
- Preserved the distinction among representation, reconstruction, compression-ratio, utility, latency, exact-replay, fallback-frequency, and decoder-drift claims.
- Aligned the reader MVI with the implemented RankFold public-safe replay probe and static artifact import: the replay records one RAW0 roundtrip and corrupt-archive rejection with no compression advantage, while the import records three existing `.rfa` archive observations over one 100,000,000-byte decoded digest and `NEURAL0` inspect metadata.

## Meaning-Preservation Checks

- The live core claim remains a design-rationale claim with `argument` support.
- No Appendix C, Appendix K, proof manifest, source note, or support-state promotion is changed by this reader pass.
- External compression work remains comparison vocabulary and credibility grounding, not evidence for local RankFold/NeuralFold performance.
- Source-reported RankFold/NeuralFold and BBVCA ideas remain architecture/design material unless the repository has a local run or proof.
- Current fixtures, the RankFold public-safe replay probe, and the static artifact import validate record shape, bounded local replay, recorded archive metadata consistency, and no-promotion boundaries only; they do not establish NeuralFold compression, codec correctness, benchmark performance, downstream utility, fallback execution, deployed compression behavior, or artifact readiness.
- The 2026-07-03 reconciliation connects speed accounting to artifact
  admission and artifact admission to full resource budgeting without changing
  any live-book claim, source boundary, proof/test status, implementation
  horizon, or release boundary.

## Non-Claims

- This pass does not claim a working RankFold/NeuralFold compressor.
- This pass does not claim measured compression ratios, utility improvements, deterministic replay, or corpus results.
- This pass does not claim that a compressed artifact can replace the preserved full artifact outside a declared use envelope.
- This pass does not promote the chapter core claim above `argument`; the existing RankFold replay and artifact-import records remain no-promotion evidence surfaces.

## Remaining Blockers

- Chapter-level prose meaning is reconciled for this pass, but reader release,
  format artifact review, and final curated-reconciliation approval remain
  blocked.
- Stronger evidence still needs a public toy corpus, baseline comparisons, deterministic decode checks, metadata/residual accounting, task probes, fallback-route fixtures, negative controls, and decoder-drift cases.
- Any future support-state promotion needs an accepted evidence-transition record.
