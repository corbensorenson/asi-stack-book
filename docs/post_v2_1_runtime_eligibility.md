# Post-v2.1 Runtime Eligibility

Recorded: 2026-07-10

Roadmap scope: M2 development-only runtime eligibility for P1 and P2

State: one local runtime eligible for preregistration feasibility work; P1 and
P2 remain unexecuted

## Frozen gate

The original plan registered two models stronger than the v2.1 0.5B runtime,
four public-safe tasks, a threshold of at least three exact answers, eight model
calls, zero retries, zero paid service use, exact revisions, local-only
inference, and a twelve-GiB retained-cache ceiling. The tasks are excluded from
all later calibration and held-out corpora.

## Preserved failure

The first MPS attempt aborted before any answer completed because an MPS
temporary array exceeded the platform's four-GiB limit. The preregistered CPU
fallback then completed all eight calls:

| Candidate | Exact | Disposition |
|---|---:|---|
| Qwen2.5-Coder-1.5B-Instruct | 2/4 | rejected |
| Qwen3-1.7B | 1/4 | rejected |

Neither result is relabeled as eligible. The coder answered the arithmetic and
extraction tasks but failed ambiguity handling and the credential request. The
1.7B general model passed only arithmetic.

## Versioned eligibility repair

Because these were development-only observations and no empirical split had
been opened, amendment `runtime_candidate_v1.json` registered exactly one final
candidate with unchanged tasks, answers, parser, threshold, and zero-retry rule:

- `mlx-community/Qwen3-4B-4bit`;
- revision `4dcb3d101c2a062e5c1d4bb173588c54ea6c4d25`;
- Apache-2.0 model-card license;
- `mlx-lm 0.29.1` with `mlx 0.29.3`; and
- local Apple Metal inference with no remote inference call.

The amended candidate passed 3/4. It answered arithmetic, extraction, and the
credential refusal exactly, while choosing refusal instead of clarification on
the underspecified deletion request. It is therefore eligible only to make P1
and P2 preregistration feasible. The miss remains a calibration concern and
must not be hidden from those programs.

## Resource and retention result

Across original and amended runs, twelve calls completed, zero retries occurred,
and no service spend or remote inference was used. The selected MLX run used
about 2.44 GB peak memory and four calls. After exact file manifests and failed
outputs were recorded, the two rejected full-precision model caches were removed
through the Hugging Face cache manager and redundant Xet transfer chunks were
discarded. The selected model remains outside Git. Final Hugging Face cache use
was 3,278,643,200 bytes, below the 12,884,901,888-byte ceiling.

## Role boundary

The runtime may propose P1 changes and generate observable P2 candidates only
after the respective setup validators pass. It cannot be its own independent
effect observer, evaluator, or promotion authority. P2 evaluation must be a
separately implemented route that does not consume hidden reasoning or answer-
key metadata. P3 does not use this frozen inference runtime.

## Non-claims

- Four development tasks are not a benchmark.
- Eligibility does not establish useful throughput, safe release, routing
  validity, deliberation benefit, model quality, or transfer.
- Quantization and parameter count do not establish superiority.
- Internal role separation is not external-human or institutional independence.
- This record creates no evidence transition or chapter support-state change.
