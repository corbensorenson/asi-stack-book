# P2 Gold-Oracle Preflight Diagnosis

Date: 2026-07-17  
State: **all 12 original development tasks dispositioned; four replacements required; final pool closed**

The fixed-denominator run executed two baseline and two human-gold arms for all
12 natural development tasks. Only seven passed the pinned exact oracle. That
7/12 result is an instrument preflight, not a benchmark score and not a
negative result about governed admission.

The five apparent failures were investigated without dropping any denominator
member. One was a definite upstream parser false rejection: AVA visibly emitted
all 21 expected baseline failures, but the official JavaScript parser has no
grammar for `✘ [fail]:` and the command returned zero. An independent parser
recovered the exact expected baseline and human-gold sets in both retained
repetitions, qualifying that task and bringing the usable count to eight.

The other four official images fetched dependencies after tests began. A
recorded setup phase materialized dependencies, sealed a derived image, and
reran both arms offline. This exposed deeper task/environment problems rather
than mechanism failures:

- the Rust test patch fails compilation before any named tests run, although
  the dataset expects 480 named failures; human gold passes 481 tests, one more
  than the stored set;
- Compose-Go's target baseline panics before 59 stored failures can be observed,
  and an unrelated schema test requires `json-schema.org` at runtime;
- Gitleaks' target fix behaves, but two Git fixture tests fail in both arms on
  the local container filesystem with a cross-device rename error; and
- Java's Maven setup reveals dynamic test-provider dependencies only at test
  time. Generic offline materialization missed Surefire's provider; an explicit
  provider fetch then exposed another missing JUnit launcher. The bounded rescue
  stopped rather than chasing an open-ended dependency chain.

All four are N0 exclusions with no claim effect. They remain in the immutable
lineage and require same-language replacements under the frozen deterministic
policy: one Rust, two Go, and one Java task. The eight qualified tasks cannot be
used as a smaller favorable denominator.

Eight attempt records and 62 compressed arm logs are retained and digest-
verified. One interrupted rescue attempt is also retained: it was aborted
because it had hashes but not raw offline logs. That failure caused the runner
to version every subsequent attempt and preserve all raw output. The full
12-task run also exposed material resource costs: 1,634.6 seconds of image pull
time, a 1.20 GB largest expanded image, a 431.5-second longest arm, and a 21.46
GB host free-space reduction across the run despite per-image cleanup.

The resource gate is still open because all 12 qualified tasks have not yet
been measured under the frozen ceiling. The ceiling was frozen before the
metadata-only replacement queue was drawn; candidate task content and outcomes
remain unopened. Independent task/specification review, policy-arm
implementation, independent evaluator calibration, power/sensitivity, the fair
rescue ladder, and the final one-time held-out opening also remain pending.

Machine records:

- `evidence_quality/p2_gold_preflight_diagnosis.json`
- `evidence_quality/p2_task_qualification_and_replacement_policy.json`
- `experiments/p2_governed_repository_admission/gold_preflight/result.json`
- `experiments/p2_governed_repository_admission/gold_preflight_rescue/attempts/`

This diagnosis establishes no coding ability, governance benefit, safety,
transfer, SOTA, release, AGI, or ASI result. The final pool remains unselected
and unopened.
