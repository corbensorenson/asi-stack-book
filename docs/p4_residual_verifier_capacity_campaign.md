# P4 Campaign 4 — Residual Honesty and Verifier Capacity

Status: terminal instrument-limited full attempt; no held-out claim attempt and
no support promotion.

## Question

Can one local model distinguish clean evidence from material residuals under
neutral, time, token, reward, and evaluator-disagreement pressure, while a
structured ledger, independent verifier, and capacity-aware gate jointly
preserve useful decisions and prevent false reassurance?

The test was designed around five matched policy views: unconstrained decision,
self-report, structured residual ledger, structured plus independent verifier,
and capacity-aware governance. It tracked schema admission, defect discovery,
residual completeness, terminal eligibility, false reassurance, clean-release
retention, verification burden, latency, token proxy, and useful decisions per
second. The exact local generator was `mlx-community/Qwen3-8B-4bit` snapshot
`545dc4251c05440727734bcd94334791f6ab0192`, with thinking disabled, no retries,
no network inference, and no external spend.

## Preserved predecessor

The 2026-07-13 six-scenario predecessor exposed every residual identifier in
capped reasoning but produced 0/24 usable final structured decisions. That
result remains `no_change` and motivated an explicit final-answer contract.

## Three sacrificial versions

### v1 — exact-route and clean-control failure

V1 used five sacrificial tasks and two calls per task. Both lanes were
schema-admissible on 5/5 tasks, and the structured lane recovered every required
residual. It nevertheless emitted `block` on all five tasks. Exact route accuracy
was 1/5 and the clean release was rejected. The route labels also conflated the
shared terminal consequence of `block`, `reopen`, and `escalate`. Heldout stayed
sealed.

### v2 — label-bearing exemplar failure

V2 made release eligibility primary and used six fresh tasks with three clean
controls. The unconstrained decision lane achieved 6/6 eligibility decisions and
3/3 clean releases. The governed output contract, however, contained the
concrete exemplar `release_eligible: false` and one open residual row. The model
copied that pessimistic exemplar: it retained all required defect residuals but
blocked all three clean controls. Heldout again stayed sealed.

### v3 — terminal extraction-contract failure

V3 separated the already-qualified decision call from a label-free residual
extractor and removed concrete output exemplars. On six new tasks the decision
lane achieved 6/6 eligibility accuracy; structured extraction recovered every
required residual; all three clean controls produced exactly empty ledgers and
were released; the capacity-aware derived policy had zero false reassurance.

The preregistered interface gate still failed. Only 3/6 extractor objects were
schema-admissible: each defect case used the undeclared route `retain`, and its
requested-check list was empty. The frozen gate required at least 5/6. V3 also
forbade another instrument repair, so the fifteen authored held-out tasks and
hidden labels were never opened to generation or scored as a claim attempt.

## Honest disposition

Campaign 4 ends `terminal_instrument_inadequate_extraction_contract`. Across the
three versions, eighteen sacrificial tasks and 36 local model calls were given a
proper, versioned attempt. The apparently favorable v3 sacrificial values remain
diagnostic only. They do not establish general residual honesty, verifier
competence, safety, useful-throughput improvement, pressure robustness, or
transfer.

The useful engineering lesson is narrower: terminal eligibility and residual
identification can succeed while the action/check interface needed to consume
those residuals still fails. A residual ledger is not operational merely because
it names the defects.

## Reproduction

```bash
python3 scripts/validate_p4_m8_residual_verifier_terminal.py
```

The validator binds all three preregistrations, raw preflights, results, and
qualification records; requires every held-out path to remain absent; preserves
the v3 interface failure and diagnostic values; rejects six laundering
mutations; and requires zero chapter-core promotion.

## Claim ceiling

No held-out result exists. No chapter-core claim moves above `argument`. No
general honesty, interpretability, verifier quality, safety, transfer,
deployment, SOTA, AGI, ASI, publication, or release conclusion follows.
