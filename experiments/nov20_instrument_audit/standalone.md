# Replay the featured instrument audits

Extract the ZIP and use Python 3.10 or later from this directory.
Each command checks the bundled files, reruns one study, and compares
the full result with the pinned bytes. The matching CSV in the kit
lets you inspect individual study cases.

```sh
python3 replay.py verifier-floor-cache
python3 replay.py receiver-effect-audit
python3 replay.py transfer-scheduler-audit
```

- The verifier replay should match 66 prescribed decisions in each arm,
  with 75 document reads in each and 2,367 serialized handoff bytes in
  the retained arm.
- The receiver rescore should match 128 and 144 verified closures on
  the same 160 pairs. Seven effect controls exercise wrong and repeated
  effects separately from a hold.
- At the descriptive proposal cap, the scheduler replay should match
  the change from 28 to 8 verified cells for query-aware whole programs.
  Query-aware routines verify 20 under each scheduler.

Add `--vary` to examine an additional assumption. In the verifier check,
the request carries a trusted current revision while the index can
return an older one. In the receiver check, a current reply carries
an old failure and the caller compares its source revision. Both are
separate authored controls. The scheduler option compares different
budget and wording strata in the retained paired outcomes. It is a
reanalysis of those cases.

These packages support exact author-code replay and inspection of
retained results. The pinned protocols and study pages give the
workload, comparison and remaining uncertainty for each run.
