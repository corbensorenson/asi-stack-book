# Proof and Code Plan

The book should include lean proofs, executable specs, or tests where doing so clarifies the architecture.

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

## What Belongs in Code

Good code candidates:

- source ingestion and cache tools,
- claim/evidence matrix validators,
- schema validators for context packets, typed jobs, and SCF records,
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
