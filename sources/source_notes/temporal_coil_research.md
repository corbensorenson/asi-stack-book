# Source Note: Temporal Coil Research

| Field | Value |
|---|---|
| Source ID | `temporal_coil_research` |
| Source title | Temporal Coil Research |
| Ingestion date | 2026-06-24 |
| Source version / URL | Google Drive file in inventory: https://drive.google.com/file/d/1ITM42_XOcJwClSQC7CcBUj1IcU9z67rU |
| Ingestion basis | Local raw cache inspected at `sources/raw/google_docs/temporal_coil_research.bin`; raw text is not published. |

## Thesis

Temporal Coil Research is an experiment-tracking note for temporal-coil integration in round-robin training. Its strongest contribution is the insistence on manifest-driven A/B testing with component variants, placement variants, progressive modes, and multiseed readouts before claiming that coil mechanisms help.

## Mechanisms

- Wire temporal-coil settings through a canonical training manifest.
- Control features such as window primes, stride sets, CLF, PCTM, ACT, anti-coil, progressive stage promotion, and replication modes.
- Integrate coil signals at explicit points: prompt sampling, prompt hints, adversary hints, reward shaping, and collapse-candidate scoring.
- Run canonical A/B variants including coil off, component-only, full, progressive, FFT-backed, adaptive, and placement-restricted variants.
- Score variants by promotion metrics and multiseed readouts.
- Maintain an update log and next experimental pass rather than relying on one run.

## Evidence

- The source is an experiment process note with wired commands and hypotheses.
- The repo has not run the temporal coil A/B experiments or imported result artifacts.
- Treat this as process evidence for how to test cyclic mechanisms, not as evidence that temporal coils improve training.

## Failure Modes

- Claiming improvement from a single seed or unisolated intervention.
- Mixing coil mechanisms so the winning component cannot be identified.
- Letting prompt hints, reward shaping, and collapse scoring confound one another.
- Promoting stages by round count instead of metrics.
- Treating FFT acceleration as a separate architecture rather than a blend mode.

## Book Chapters Supported

- `mathematical-and-search-substrates` (Mathematical and Search Substrates)

## Claims To Add Or Update

- Use this source to describe the experimental discipline required for coil/cyclic mechanisms.
- Do not claim temporal-coil benefit until the A/B outputs are available and validated.

## Open Questions

- Should the Circle/coil chapters include a small A/B manifest schema?
- Which temporal-coil metrics would be publication-worthy for this book?
