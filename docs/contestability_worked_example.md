# Contestability Worked Example

The Contestability Worked Example records one synthetic care-memory export
scenario for the Moral Uncertainty, Value Conflict, and Contestable Governance
chapter.

The scenario ID is `contestability://synthetic-care-memory-export-001`. It
models a request for audit, exit, fork, and redaction appeal when a memory
export touches privacy, safety, autonomy, and accountability. The validator
requires a value-conflict residual, scoped audit material, a scoped exit path,
a safety-limited fork boundary, a redaction appeal path, and replacement
preservation of conflict residuals and governance-right receipts.

Run:

```bash
python3 scripts/validate_contestability_worked_example.py
```

The local result record is:

```text
experiments/contestability_worked_example/results/2026-07-02-local.json
```

The validator also runs seven expected-invalid mutation controls: missing
residual uncertainty, exit without portable material, unsafe fork, redaction
without appeal, replacement that drops residuals, support-promotion overclaim,
and missing non-claim boundaries.

This fixture does not prove moral correctness, does not prove legal rights, does not prove reviewer independence, does not prove export usability, does not prove fork safety, and does not promote support state.
