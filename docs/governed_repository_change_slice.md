# Governed Repository-Change Vertical Slice

Last executed: 2026-07-10

This is the first ASI Stack experiment that executes a complete, bounded
repository change through a simpler baseline and a governed route. It creates
fresh temporary Git repositories, changes executable Python code, runs public
tests, invokes an independent verifier process, compares claimed and observed
artifact digests, commits accepted effects, performs rollback, and verifies the
post-rollback tree. It does not merely validate a prewritten record.

The requested change fixes a budget allocator so its output stays within
`[0, ceiling]`. The public smoke tests cover ordinary and over-ceiling inputs.
The independent observer also checks a negative input that distinguishes the
safe clamp from a cheaper `abs(...)` shortcut. The only authorized repository
path is `src/budget.py`.

Run the workload and refresh its tracked result with:

```bash
python3 scripts/run_governed_repository_change_slice.py --write-result
python3 scripts/validate_governed_repository_change_slice.py
```

## End-to-End Trace

The nominal governed path records intent acceptance, an authority ceiling, a
plan DAG, context admission, costed route candidates, a sandboxed repository
effect, a proposal receipt, independent effect observation, an evidence gate,
and a local release commit. Refused paths stop before effect or roll back to the
initial tree. An inexact rollback is quarantined rather than represented as a
successful refusal.

The eight named adversarial cases are:

1. retrieved-context prompt injection;
2. stale authorization;
3. revocation during execution;
4. a forged or mismatched receipt;
5. a correlated proposer and verifier;
6. hidden residual cost;
7. failed rollback; and
8. a cheaper route that violates a safety constraint.

The prompt-injection and cheap-route cases demonstrate mitigation rather than
automatic refusal: the injected out-of-scope instruction is quarantined, the
cheap ineligible route is rejected, and the authorized safe patch can still be
released. Stale or revoked authority and correlated review stop before the
first effect. Receipt mismatch and hidden residuals trigger exact rollback.
The failed-rollback case deliberately leaves an unauthorized tracked-file
mutation; the final tree digest exposes the incomplete reversal and routes the
repository to quarantine.

## Matched Comparison

Both routes receive the same requested change and begin from the same fixture
repository. Workload units and latency steps are deterministic accounting
units, not wall-clock production benchmarks. The observed local suite runtime
is recorded in the result for diagnostics but excluded from reproducibility
comparison.

| Metric | Simple baseline | Governed route | Difference |
|---|---:|---:|---:|
| Correct dispositions | 1 | 9 | +8 |
| False accepts | 8 | 0 | -8 |
| False rejects | 0 | 0 | 0 |
| Unsafe effects observed inside fixtures | 8 | 2 | -6 |
| Unsafe releases | 8 | 0 | -8 |
| Deterministic cost units | 27 | 66 | +39 |
| Deterministic latency steps | 27 | 89 | +62 |
| Operator-review steps | 0 | 9 | +9 |
| Rollback attempts | 0 | 3 | +3 |
| Exact rollbacks | 0 | 2 | +2 |
| Failed rollbacks quarantined | 0 | 1 | +1 |

The comparison therefore exposes the governance tax instead of hiding it: the
governed route consumes 39 additional deterministic cost units, 62 additional
trace steps, and nine review steps. In this deliberately adversarial workload,
that overhead reduces eight baseline false accepts and eight unsafe releases
to zero. This is a fixture result, not a general cost-effectiveness estimate.

## Record/Reality Controls

The proposer receipt carries the changed-file SHA-256. A separate process reads
the repository state, executes tests, directly probes program behavior,
enumerates tracked and untracked changed paths, and compares the claimed digest
with the observed bytes. Record shape alone cannot pass the release gate.

The result also preserves two uncomfortable facts. The governed route observes
two unsafe effects inside disposable fixtures: the undeclared cache artifact
and the unauthorized mutation used to test failed rollback. Neither is
released. One is removed by exact rollback; the other remains visible in a
quarantined temporary repository. Reporting only “zero unsafe releases” while
hiding those attempted effects would repeat the record/reality failure this
slice is meant to address.

## Evidence Boundary

This is an executed local repository workflow and is stronger than a static
record-shape fixture. Its boundary is still narrow: bounded local fixture
repository only; no language-model planning or code generation; no deployed
authorization, sandbox, verifier, or rollback service; deterministic workload
units are not production cost or latency measurements; no chapter-core
support-state promotion; and no safety, security, software-quality, or ASI
claim. The result creates no evidence-transition record and changes no chapter
core claim above `argument`.

## Artifacts

- Workload: `experiments/governed_repository_change_slice/input/workload.json`
- Result: `experiments/governed_repository_change_slice/results/2026-07-10-local.json`
- Runner: `scripts/run_governed_repository_change_slice.py`
- Independent observer: `scripts/governed_repository_independent_verifier.py`
- Validator: `scripts/validate_governed_repository_change_slice.py`
- Result schema: `schemas/governed_repository_change_result.schema.json`
