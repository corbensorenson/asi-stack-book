# Source Note: Ten Percent Challenge — Task-Scoped Compression and External Feedback

| Field | Value |
|---|---|
| Source ID | `ext_ten_percent_challenge_2026` |
| Review date | 2026-11-06 |
| Citation | Bobliuuu and contributors (2026), Ten Percent Challenge |
| Source type | Public software repository and source-reported experiment; not a peer-reviewed paper |
| Selected version | [Commit dc0475b06c3d7ed7fbae05fb709c19a98537b19e](https://github.com/Bobliuuu/ten-percent-challenge/tree/dc0475b06c3d7ed7fbae05fb709c19a98537b19e) |
| Storage | Public-safe authored synthesis; selected raw files cached only in ignored `build/` |
| Review scope | Selected task definition, decision, compression/packing and loader code, feedback mechanism, manifest, harness lock, two final receipts, and maintainer response; no model execution or full repository audit |

## Thesis

A narrow behavioral contract can admit an aggressively compressed checkpoint
without preserving the original model's general interface. The submitted
case also illustrates how a frozen backbone can acquire persistent behavioral
changes through an external estimator. Compression, learning, and challenge
acceptance require separate conclusions.

## Mechanisms

The selected pipeline combines Hadamard rotation, calibration-based
Hessian-aware quantization, entropy-coded indices/scales, and reduced stored
embedding/output structures. The task is five-option tool selection, not
generation of executable tool calls and arguments. Inspect
[`TASK_C.md`](https://github.com/Bobliuuu/ten-percent-challenge/blob/dc0475b06c3d7ed7fbae05fb709c19a98537b19e/v2/commercial/TASK_C.md),
[`push_c2.py`](https://github.com/Bobliuuu/ten-percent-challenge/blob/dc0475b06c3d7ed7fbae05fb709c19a98537b19e/v2/compress_C/push_c2.py),
and [`pack_artifact.py`](https://github.com/Bobliuuu/ten-percent-challenge/blob/dc0475b06c3d7ed7fbae05fb709c19a98537b19e/v2/compress_C/pack_artifact.py).
The packer losslessly codes quantizer symbols; quantization itself is lossy.
No task-loss gradient update to the backbone does not mean its numerical
weights survived compression unchanged.

The inspected loader rebuilds a bf16 `AutoModel` on the GPU, fills retained
embedding rows, decodes/dequantizes the body, and reverses the rotation.
Its byte size and SHA-256 match the loader entry in the source's artifact
manifest. This is a check of the inspected loader against a reported manifest,
not verification of the released weight files or peak runtime memory.

The feedback path projects option features to 64 dimensions and uses a fitted
discriminant head. `ingest_feats` changes per-tool prototype means and
true/predicted counts. `_scores`/`decide` gate the fixed head on nonempty memory.
These are learned external statistics even though backbone weights and prompt
tokens stay fixed. Source:
[`predict.py`](https://github.com/Bobliuuu/ten-percent-challenge/blob/dc0475b06c3d7ed7fbae05fb709c19a98537b19e/v2/c2_fb/artifact_code/predict.py),
`Head`, `Mem`, `_scores`, `decide`, and `ingest_feats`.

## Evidence

The source's final receipts report 2,000 C2 items. Stage 1 records a
1,432,412,701-byte artifact against a 15,231,233,024-byte bf16 reference,
76.75% base accuracy, and 79.90% candidate accuracy. Stage 2 adds an
852-byte memory and reports 80.20%. Both report a one-point-margin paired
non-inferiority pass; the statistical implementation and evaluation history
were not independently certified. Sources:
[`stage1.json`](https://github.com/Bobliuuu/ten-percent-challenge/blob/dc0475b06c3d7ed7fbae05fb709c19a98537b19e/v2/harness/receipts/REAL_final/stage1.json),
[`stage2.json`](https://github.com/Bobliuuu/ten-percent-challenge/blob/dc0475b06c3d7ed7fbae05fb709c19a98537b19e/v2/harness/receipts/REAL_final/stage2.json).

The first receipt records about 81 seconds for the base and 217 for the
candidate. The runner/worker timers include loading and differ in execution
path; these are neither matched steady-state latency nor proof of speedup.
The size boundary excludes Python runtime dependencies.

## Failure Modes

- Closed-choice accuracy does not establish open-ended generation, argument
  correctness, real tool execution, or general retention. Reported broader
  knowledge failures constrain this particular search, not a universal bit
  lower bound.
- `RESULTS.md` explicitly says part of the feedback gain comes from enabling
  the prefit head. Stage 2 is a composite intervention; its increment cannot
  be attributed wholly to six annotations.
- The proof describes five head rows, but the inspected builder selects
  letter rows A–N and the manifest-matching loader allocates fourteen logit
  slots, masking to the offered choices. The book states the five-choice task
  without repeating the five-row implementation claim.
- `CRITERION.md` retains earlier 14B/MMLU settings. C2 identity, denominator,
  budget, margin, and alpha are taken from `LOCK_HARNESS_C2.json` and final
  receipts. That documentation mismatch merits caution about replay.
- The base revision is null in the C2 lock. Public hashes and isolated
  candidate execution do not independently establish an unseen evaluation
  history or exact upstream model custody.

## Challenge Adjudication

In the [November 6 maintainer response](https://github.com/DeusExperiments/ten-percent-challenge/issues/2#issuecomment-6689471947),
tokenbender accepts steps 1–4 under relaxed criteria but rejects step 5 because
the feedback depends on a label-fitted classifier and external parameters.
The code's head gating supports that dependency. This is not a completed
challenge win or accepted demonstration of parameter-free learning. The
maintainer's judgment concerns challenge eligibility, not independent
reproduction of the numerical experiment.

## Claims To Add Or Update

Use the case to explain task-specific artifact admission and adaptation
outside backbone weights. Preserve source-reported status, excluded costs,
runtime reconstruction, composite feedback, and the adverse adjudication.
No book core claim or support state changes.

## Open Questions

What survives a broader input population, changed tool catalog, argument
generation, matched small-model baseline, head-only/memory-only ablations,
runtime-memory measurement, and independent evaluation? Those are unobserved
research questions, not work commissioned by source integration.

## Book Chapters Supported

- `rankfold-neuralfold-and-artifact-compression`
- `adjudicated-persistence-and-the-adaptive-commit-boundary`

## Chapter Decision

Update existing owners under
`research_backlog_records/ten_percent_challenge_2026_11_06.json` and
`new_paper_triage_scenarios/ten_percent_challenge_2026_11_06.json`.
The software experiment is a scoped comparator, not evidence for RankFold,
NeuralFold, an Adaptive Commit Boundary implementation, or general model
compression with preserved capability.
