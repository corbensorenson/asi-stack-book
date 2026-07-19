# P4/M7 full-state update and unlearning campaign

Executed: 2026-07-16

This campaign asks a narrower and more useful question than “did the model
forget?” It tests whether one bounded local update system can keep behavioral
change, causal-influence evidence, membership-attack behavior, lineage
invalidation, legal assessment, storage erasure, backup erasure, and external
descendant closure as eight separate outcomes while tracking 24 declared state
surfaces and preserving exact rollback.

The terminal result is a **claim narrowing**, not a support promotion. It is
evidence about a frozen Qwen representation plus a small structured fusion
head. The Qwen weights never changed. Nothing here establishes language-model
unlearning, zero influence, privacy, complete erasure, legal compliance,
production behavior, transfer, or SOTA.

## Failure lineage

The first held-out attempt passed its original integrity checks but failed a
more basic validity question discovered during outcome review. Both deletion
cohorts contained only the rare `allow` class, their unique identifiers landed
at the final representation position, and every arm—including deletion-aware
retraining—scored 0% true-label accuracy. The observed behavior and distance
metrics therefore could not adjudicate unlearning. The entire corpus, raw run,
checkpoints, result, validator, and diagnosis remain preserved; the run is
terminal `instrument_inadequate_unlearning_target_not_learnable`, with no claim
outcome.

V2 balanced all three classes, moved identifiers away from the terminal
position, used attention-masked mean pooling, and added a deletion-like
preflight floor. It never opened the held-out denominator: the linear frozen-
representation head reached 43.33% general and 33.33% deletion-like accuracy
against 60% floors. That is a second instrument failure, not a claim attempt.

The terminal v3 instrument made the custody interface explicit. It concatenated
an L2-normalized, mean-pooled representation from the exact local
`Qwen/Qwen2.5-Coder-0.5B-Instruct` snapshot
`ea3f2471cf1b1f0db85067f1ef93848e38e88c25` with a deterministic one-hot vector
of the authority, provenance, contamination, deletion, and risk fields already
visible in each record. A 32-unit nonlinear head was the only trainable model
component. No label or held-out outcome entered that vector.

The sacrificial v3 ablation made the repair source visible:

| Preflight path | General accuracy | Deletion-like accuracy |
|---|---:|---:|
| Transformer-only linear | 0.7667 | 0.7000 |
| Structured-only nonlinear | 1.0000 | 1.0000 |
| Fused nonlinear | 1.0000 | 1.0000 |

The fused path passed the frozen 0.80 floors. This does not prove the structured
path is generally superior; it shows that this control task became learnable
when the declared custody fields were exposed rather than recovered implicitly
from one frozen embedding.

## Frozen terminal design

The confirmatory corpus has 870 authored public-safe natural-language custody
records. Both 30-record deletion cohorts and the 60 matched nonmembers contain
balanced `allow`, `quarantine`, and `deny` labels. Five seeds compare seven
arms:

1. no update;
2. standard update;
3. governed update with a validation-only retained floor, clipping, and
   regularization;
4. stronger regularized forgetting mitigation;
5. approximate unlearning with sequential A then B requests;
6. deletion-aware retraining without either deletion cohort; and
7. exact rollback to prospective base authority.

Best and final checkpoints are both retained. Authority selection uses only the
validation split, with earliest-epoch tie breaking. Each arm records model,
optimizer, scheduler, gradients, Python/NumPy/Torch RNG, sampler, data and
split, tokenizer, training configuration, code and environment, best/final/
released/shadow/rollback checkpoint, evaluator, inference and feature caches,
lineage, and local backup surfaces.

## Terminal results

Deletion-aware retraining achieved mean deletion true-label accuracy `0.9767`,
passing the frozen `0.80` target-adequacy floor. The retained and target tests
were saturated at `1.0000` for all arms; this simplicity is a ceiling on the
campaign, not evidence of general capability.

Approximate unlearning moved `0.01222040` closer in parameter distance to the
deletion-aware retraining comparator than standard update. Its direction-
invariant loss-threshold membership-attack advantage was `0.03700000`, a
`-0.02511111` change relative to standard update. These are small bounded
effects. Retraining remains only a comparator, and one internal membership
attack remains only a probe.

All 35 arm/seed transactions restored the 24 declared surface digests to the
prospective base digest. That is exact restoration of the declared local
representation, including simulated serialized non-model surfaces; it is not
production or open-system rollback.

Five late local descendants were invalidated and quarantined. The declared
operational feature shard and local backup were physically absent after the
request, with zero logical index references. The immutable research corpus,
feature packet, checkpoints, and raw evidence remain intentionally retained.
An unreachable simulated remote replica supplied no acknowledgement. Therefore
the storage result is partial, local, and derived-store-only; external
descendant and remote-backup closure remain unresolved.

The run took `111.174886` wall seconds, including `89.984342` seconds for shared
feature extraction. Marginal API cost was zero. Energy and operator time were
not measured, so they cannot be inferred from the receipt.

## Eight separate dispositions

| Claim axis | Terminal disposition |
|---|---|
| Behavioral cohort change | observed, bounded local |
| Causal influence reduction | small comparator-distance reduction; zero influence not established |
| Membership/privacy change | attack advantage reduced in one internal probe; privacy not established |
| Lineage invalidation | five local descendants invalidated and quarantined |
| Legal compliance | not evaluated |
| Storage erasure | declared operational shard only; retained research evidence remains |
| Backup erasure | local absence observed; remote unresolved |
| External descendant closure | unresolved |

The canonical claim outcome is `claim_narrowed_after_full_attempt`. Chapter-core
support remains `argument`. No result in this package authorizes a release,
deployment, publication, legal assertion, privacy assertion, language-model
unlearning assertion, SOTA comparison, AGI claim, or ASI claim.

## Reproduction

```bash
python3 scripts/validate_p4_m7_update_unlearning_design.py
python3 scripts/validate_p4_m7_update_unlearning.py
python3 scripts/validate_p4_m7_update_unlearning_failure_lineage.py
python3 scripts/validate_p4_m7_update_unlearning_v3_design.py
python3 scripts/validate_p4_m7_update_unlearning_v3.py
```

The first two validators preserve the misleading-but-byte-valid v1 result.
The failure-lineage validator treats v1 target invalidity and v2's unopened
failed preflight as expected historical outcomes, binds both exact diagnoses
into v3, and rejects six laundering mutations. The v3 validators require the
adequate terminal target, all eight claim axes, all 24 rollback surfaces,
retained storage residuals, and zero chapter-core promotion.
