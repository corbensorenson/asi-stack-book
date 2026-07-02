# Cognitive Compilation Trace Harness

Command:

```bash
python3 scripts/validate_cognitive_compilation_traces.py
```

Result record:

- `experiments/cognitive_compilation_traces/results/2026-07-02-local.md`

Result summary:

- `Cognitive compilation trace harness passed: 2 valid fixture(s), 4 expected-invalid fixture(s).`

The harness checks synthetic Cognitive Compilation trace records for:

- source-plan requirement preservation into semantic atoms,
- represented lowering receipts for every lowered atom,
- receipt-level obligation preservation,
- target audit links across source plan, semantic atoms, receipts, assumptions, validators, residuals, and support-state effects,
- repair traces that remain inside the declared repair scope, and
- expected-invalid controls for missing receipts, dropped obligations, global regeneration repair, and syntactic validator passes without obligation-preservation audit.

Boundary:

The fixtures are hand-authored trace records. The harness does not parse arbitrary goals, run a cognitive compiler, lower to real code/prose/schemas, execute LLVM or MLIR tools, run translation validation, inspect a concrete generated target artifact, measure localized repair quality, compare against direct generation, or promote support state.

Non-claims:

- This harness does not prove compiler correctness.
- This harness does not prove target artifact quality.
- This harness does not prove local repair performance.
- This harness does not promote the Cognitive Compilation chapter core claim above `argument`.
