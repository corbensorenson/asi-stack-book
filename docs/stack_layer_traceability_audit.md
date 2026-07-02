# Stack Layer Traceability Audit

Command:

```bash
python3 scripts/validate_stack_layer_traceability.py
```

Result record:

- `experiments/stack_layer_traceability/results/2026-07-02-local.md`

Result summary:

- `Stack layer traceability validation passed: 1 layer-boundary fixture, 6 mapped source(s), 44 claim row(s).`

The audit checks the opening chapter's layer-boundary and claim-discipline surfaces:

- the public `layer_boundary_record.valid.json` fixture still validates against `schemas/layer_boundary_record.schema.json`;
- the layer-boundary fixture uses existing chapter refs, source refs, and contract refs;
- `asi-is-a-stack-not-a-model` keeps exact claim-source mappings for all six assigned sources;
- each assigned source mapping is passage-reviewed and bounded by an explicit limit;
- Appendix A visibly maps assigned sources back to the opener;
- Appendix C has one core claim row per manifest chapter, and the opener keeps `Design rationale` plus `argument`;
- the opener's chapter text and outline keep the stack-boundary, source-to-layer, claim-support, and no-promotion markers visible.

Boundary:

This is a repository traceability audit. It does not execute an ASI Stack runtime, prove layer enforcement, measure model capability, validate source interpretation beyond the recorded source-note mappings, or promote any chapter core claim.

Non-claims:

- This audit does not prove the ASI Stack works as a deployed system.
- This audit does not prove whole-system safety or efficiency.
- This audit does not promote any chapter core claim support state.
