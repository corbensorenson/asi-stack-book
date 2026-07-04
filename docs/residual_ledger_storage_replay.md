# Residual Ledger Storage Replay

Command:

```bash
python3 scripts/validate_residual_ledger_storage_replay.py
```

Result:

```text
experiments/residual_ledger_storage_replay/results/2026-07-04-local.json
```

This is a bounded local storage/replay fixture for residual honesty. It uses an
append-only residual ledger event log, not another cross-artifact scrape, to
check whether residual records preserve sequence continuity, owner handoff,
discharge review, workload context, invalid-control rejection, and non-claim
boundaries.

Validated surfaces:

| Replay surface | What is checked | Boundary |
|---|---|---|
| Append-only chain | The validator computes a digest chain over four ordered entries and records the final chain digest. | Local deterministic fixture only; no deployed storage, distributed ledger, or tamper-proof runtime claim. |
| Owner handoff | A deferred residual moves from Resource review to Compact repair review only when the prior owner and accepted handoff review match. | No deployed workflow, reviewer correctness, or organization-process claim. |
| Discharge review | A discharged repair residual must carry an accepted discharge review and receipt. | No proof that every residual can be found, measured, discharged, or verified in the open world. |
| Workload context | Every replayed entry keeps a concrete workload context reference. | Context refs are repository artifacts, not live workload telemetry. |
| Invalid controls | The fixture rejects handoff-owner mismatch, missing discharge receipt/review, sequence gap, missing workload context, and support promotion from replay shape. | No support-state promotion or chapter-core promotion. |

Lean bridge:

- `residual_ledger_storage_replay_bridge` in
  `lean/AsiStackProofs/CompactGenerativeSystems.lean` mirrors the bounded
  replay summary: append-only digest chain computed, sequence continuity
  checked, owner handoff preserved, discharge review required, workload context
  preserved, invalid controls rejected, support-state effect `none`, non-claim
  boundary preserved, live storage unclaimed, and deployed ledger unclaimed.

No-promotion decision:

- `evidence_transitions/v1_x_measured/residual_ledger_storage_replay_no_change.json`
  records this lane as a reviewed `blocks_promotion` no-change decision.

Non-claims:

- This does not prove deployed residual-ledger storage.
- This is not a deployed residual ledger.
- This does not prove live residual detection.
- This does not prove safety.
- This does not promote any chapter core claim.
- This does not prove model quality or benchmark performance.
