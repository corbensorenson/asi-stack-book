# Procedural Memory Loop Harness

Last updated: 2026-06-30

Command:

```bash
python3 scripts/validate_procedural_memory_loop.py
```

Result record: `experiments/procedural_memory_loop/results/2026-06-30-local.md`

Result summary: Procedural memory loop harness passed: 3 valid fixture(s), 6 expected-invalid fixture(s).

## What It Checks

The harness validates synthetic procedural-memory qualification packets around
the existing `procedural_tool_record` schema. Each scenario includes a
procedural tool, candidate traces, negative examples, near misses, abstraction
fields, a regression review, expected route, and non-claims.

The validator checks that routable tools cite at least three comparable success
traces, preserve a near miss or failure, preserve negative examples, expose
parameters/preconditions/postconditions, match the abstraction invariant, pass
regression checks, keep the SCF target active, and avoid active retirement
triggers. Failed regressions route to quarantine or retirement, retired tools
must actually carry a retired route, and source traces cannot omit the failure
or near-miss traces that define the procedure boundary.

## Boundary

This is synthetic record-gate evidence. Passing it proves only that the
fixtures obey the loop-qualification rules checked by the script. It does not
prove deployed loop detection, tool synthesis, generated-tool correctness,
regression quality, route quality, monitoring automation, retirement automation,
source interpretation, benchmark quality, model quality, safety, or ASI
capability. It does not promote any Appendix C or chapter core support state.

