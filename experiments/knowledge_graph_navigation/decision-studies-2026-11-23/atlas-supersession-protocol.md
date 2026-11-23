# Supplemental navigation check for decision supersession

Freeze G5 before running it on the candidate with the historical Atlas record.
Both owner-side instruments start at the same six-comparator Atlas decision.
Give them the same register query, evidence corpus and two additional record
opens from the original [protocol](protocol.md). The linked instrument may
follow the directional decision supersession edge. Score whether each reaches
the corrected result, opens the exact citation, and retrieves the adaptation
limit. Record the number of opens until the first target for each arm.

This is a targeted check of a single supersession path. The earlier verifier
task measured how to find a follow-up. Here the later decision controls
interpretation of the earlier result, with the original artifact preserved.
Retain all nine earlier tasks and their capture. The new case adds a concrete
navigation test and does not contribute to the timed human-review denominator.

```sh
pilot=experiments/knowledge_graph_navigation/decision-studies-2026-11-23
node "$pilot/run.cjs" TESTED_SITE atlas-supersession-capture.json --tasks "$pilot/tasks-atlas-supersession.json"
```
