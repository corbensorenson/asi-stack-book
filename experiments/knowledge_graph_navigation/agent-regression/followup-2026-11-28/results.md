# ByteFlow and SciFact retrieval follow-up

The first deployed revision, `db1df1da`, fixed the original ByteFlow miss and cut reading cost on the original science panel. All four gates passed on the six-panel rerun. The first fresh science panel exposed a remaining method-lookup cost despite full answer credit. The subsequent revision, `61fe4836`, puts each reviewed case's parent run method, scope, and compact export alongside the case. [Protocol](protocol.md) · [First live verification](live-verification.json)

## Frozen regression

Twelve new sessions answered the previously frozen 24 questions on the original direct-link edition `d5d8c2f7` and the first deployed revision `db1df1da`. Participants used the same inherited model configuration and allowance. One reviewer applied the frozen rubric with edition labels visible. [Frozen suite](frozen/suite.json) · [Scores](frozen/scores.json)

| Panel | Direct-link score | Deployed score | Direct-link deduplicated bytes | Deployed deduplicated bytes |
|---|---:|---:|---:|---:|
| Assurance | 12/12 | 12/12 | 692,999 | 1,321,074 |
| Authority | 12/12 | 12/12 | 1,530,679 | 345,530 |
| Formal scope | 12/12 | 12/12 | 997,419 | 334,145 |
| Generation | 9/12 | 11/12 | 2,966,644 | 1,096,977 |
| Scientific evidence | 12/12 | 12/12 | 1,628,146 | 306,302 |
| Forward transfer | 12/12 | 12/12 | 2,692,080 | 1,195,334 |
| **Total** | **69/72** | **71/72** | **10,507,967** | **4,599,362** |

The deployed agent found ByteFlow's two-position boundary example, the 0.6B and 50B-token Table 3 comparison, and the identifier-recovery caveat. The direct-link agent inferred the slot constraint and left the measured comparison unresolved. The deployed agent lost one scope point for BridgeKV. There were zero unsupported numerical claims in either edition. [Generation answers](frozen/generation-candidate-answers.md) · [Generation grades](frozen/generation-candidate-grades.json)

The rerun cut total deduplicated reading by 56.2%. Science fell 81.2% against the new direct-link session and 83.6% against the 1,870,436 bytes in the preceding candidate session. The latter is a historical comparison. The science agent opened the 5,899-byte topic catalog once and followed five compact passages. Assurance cost more in this pair. These routes are individual observations under the same allowance. [Science journal](frozen/science-candidate-opens.json) · [Previous candidate scores](../run-2026-11-28/scores.json)

One direct-link generation session lost a journal entry after two concurrent writes. It stopped before answering. A fresh session restarted that arm using sequential commands. The partial journal is retained outside the scored files. [Invalidated journal](frozen/generation-baseline-invalid-opens.json) · [Reader instructions](../README.md)

## First fresh test

Four separate sessions answered eight new questions on the preceding edition `552fb37f` and the first deployed revision `db1df1da`. Both earned full credit on every item. [Fresh questions](fresh-panels) · [Rubric](fresh-rubric.md) · [Fresh suite and scores](fresh/scores.json)

| Panel | Previous score | Deployed score | Previous deduplicated bytes | Deployed deduplicated bytes |
|---|---:|---:|---:|---:|
| Science | 12/12 | 12/12 | 415,701 | 580,376 |
| Segmentation | 12/12 | 12/12 | 1,743,317 | 402,553 |
| **Total** | **24/24** | **24/24** | **2,159,018** | **982,929** |

The segmentation session reached the ByteFlow section and its H-Net and JEPA neighbors using compact exports. Its deduplicated cost fell 76.9%. The new science session spent 39.6% more. It first reached the four compact passages and then opened the same 269,119-byte study page three times while checking the case and shared model rationale. Deduplication charged that page once. The parent-run context change addresses the extra navigation evidenced in this trace. [Segmentation journal](fresh/segmentation-candidate-opens.json) · [Science journal](fresh/science-candidate-opens.json)

## Science confirmation after adding case context

Two further sessions answered four newly frozen questions on `552fb37f` and the second live revision, `61fe4836`. Both earned 12 of 12 points and produced zero unsupported numerical claims. The candidate opened the parent run's compact export and also opened the full study page. Its trace included a 304,606-byte replay ZIP that the text reader could not display. The harness charges the full payload on such an open. Deduplicated cost rose from **884,501 to 938,310 bytes**, or **6.1%**, so the science cost gate failed. The public check confirmed the case-to-run links and the continued availability of the original ByteFlow export. [Confirmation questions](confirmation-panels) · [Scores](confirmation/scores.json) · [Candidate journal](confirmation/science-candidate-opens.json) · [Second live verification](confirmation-live-verification.json)

The 24-question regression confirms the targeted ByteFlow repair and the scientific reading improvement on its original panel. The two fresh science pairs retained answer quality and both cost more in the changed edition. The candidate's route choices included work beyond the compact lookup. These are individual agent paths with one session per edition on each panel. The costs measure payload bytes under the same reader allowance. Network compression, latency, and model billing remain unmeasured.

## Offline replay

The three runs retain their answer sheets, grades, read journals, verified site subsets, and original and replay suites. From the repository root, the same scorer audits each packet without the original build downloads. The replay reproduces the original metrics and gates. Use `--require-pass` when an observed cost or quality regression should produce a nonzero exit status.

```sh
dir=experiments/knowledge_graph_navigation/agent-regression
for trial in frozen fresh confirmation; do
  run="$dir/followup-2026-11-28/$trial"
  python3.12 "$dir/regression.py" score --suite "$run/replay-suite.json" \
    --baseline "$run/baseline-replay.zip" --candidate "$run/candidate-replay.zip" \
    --results "$run"
done
```
