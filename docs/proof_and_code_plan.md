# Proof and Code Plan

The book should include lean proofs, executable specs, or tests where doing so clarifies the architecture.

## Source of Truth

`docs/book_outline.md` is the source of truth for Lean proof scope. Each chapter has a `Lean proof targets` table with stable `lean:*` tags, intended Lean modules, formal targets, and status.

Run this after changing outline proof tags:

```bash
python3 scripts/sync_proof_manifest.py
```

The generated machine-readable manifest is `proofs/proof_manifest.json`.

The proof triage file is `proofs/proof_triage.json`. It classifies each outline target as a near-term formal invariant, schema contract, process contract, or research-agenda item. Use it to avoid turning every chapter's conceptual claim into ceremonial Lean.

## What Belongs in Proofs

Good proof candidates:

- authority non-escalation invariants,
- route validity predicates,
- stable capability field replacement conditions,
- monotonic evidence-state transitions,
- rollback preconditions,
- claim support-state constraints,
- typed job lifecycle invariants,
- context packet admission vs adequacy separation.

Avoid formalizing vague philosophical claims before they are translated into operational predicates.

Targets marked `schema-contract`, `process-contract`, or `research-agenda` should not be marked implemented merely because prose exists. They need an executable schema, policy model, test harness, or better formal statement first.

## What Belongs in Code

Good code candidates:

- source ingestion and cache tools,
- claim/evidence matrix validators,
- schema validators for context packets, typed jobs, SCF records, context adequacy records, semantic atoms, compression receipts, and authority-use receipts,
- toy tests for routing, residual escrow, and benchmark ratchets,
- small synthetic experiments for VCM, planning, Talos, Spinoza, compression, and RMI.

## Directory Roles

| Path | Role |
|---|---|
| `proofs/` | Proof notes and formalization plans. |
| `lean/` | Lean 4 project when formal proofs are executable. |
| `experiments/` | Runnable synthetic tests and benchmark harnesses. |
| `schemas/` | JSON Schemas for protocols and records. |
| `test_results/` | Public-safe result summaries. |

## Result Discipline

Do not say a theorem is proven unless the proof checker passes.

Do not say an experiment supports a claim unless the test was implemented, run, and recorded.
