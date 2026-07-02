# RankFold Artifact Import

This note records a narrow public-safe import from existing local RankFold
output artifacts. It is useful because the RankFold chapter previously had
only source-reported compression architecture and schema/Lean record gates; it
did not surface concrete local archive observations.

## Recorded Facts

The import record is
`experiments/rankfold_artifact_import/results/2026-07-02-local.json`.

It records three existing `.rfa` archive observations for the same
100,000,000-byte decoded artifact digest:

| Artifact label | Archive bytes | Decoded bytes | Decoded SHA-256 consensus | Archive / decoded | Decoded / archive | `rfa verify` |
|---|---:|---:|---|---:|---:|---|
| `enwik8_out2_1771038259` | 36,169,618 | 100,000,000 | `2b49720ec4d78c3c9fabaee6e4179a5e997302b3a70029f30f2d582218c024a8` | 0.36169618 | 2.76475134 | 1 OK, 0 failed |
| `enwik8_out3_1771047103` | 36,155,111 | 100,000,000 | `2b49720ec4d78c3c9fabaee6e4179a5e997302b3a70029f30f2d582218c024a8` | 0.36155111 | 2.76586068 | 1 OK, 0 failed |
| `enwik8_out4_1771047630` | 36,148,844 | 100,000,000 | `2b49720ec4d78c3c9fabaee6e4179a5e997302b3a70029f30f2d582218c024a8` | 0.36148844 | 2.76634019 | 1 OK, 0 failed |

`rfa inspect` reported one unencrypted `__pack0__` stream, one page, one
entry, total original `95.37 MB`, and codec mix `NEURAL0: 1` for each recorded
archive. The `rfa` binary used for read-only inspection had SHA-256
`f03e3175742411b4310187cf48c5e735813c4a411a93dc53b68a3364ed75f438`.

## Boundary

This is a local artifact-import record, not a fresh benchmark. It validates
that the recorded metadata is internally consistent and that three existing
archives passed RankFold's read-only archive verifier. It does not copy dataset
bytes or archive bytes into this repository.

This record does not prove RankFold codec correctness, deterministic decoder
correctness beyond the recorded local decoded digest observations, compression
from source input, benchmark performance, downstream utility, fallback
execution, deployed compression behavior, or any support-state promotion. It
does not promote the RankFold chapter core claim.

## Validation

Run:

```bash
python3 scripts/validate_rankfold_artifact_import.py
```

The validator checks record math, digest consensus, archive-verification
summaries, codec metadata, non-claim boundaries, and that the RankFold chapter,
reader manuscript, outline, roadmap, and manifest expose the import without
promoting the chapter core claim above `argument`.
