# SciFact compact reading retest

The deployed edition stayed on compact evidence for the ordinary science questions. It earned the same full score and used 48.7% fewer deduplicated bytes. On the escalation panel it fetched pinned plain-text methods and one distinct full study page for an unexported case. The two sessions in each panel used the same reading allowance and public entry route. [Frozen protocol](protocol.md) · [Questions](panels) · [Rubric](rubric.md) · [Live verification](live-verification.json)

## Results

Four new sessions answered eight questions using the previous live case-context edition `61fe4836` and the compact-reading edition `a2e05e10`. One reviewer applied the frozen rubric with edition labels visible. All four aggregate gates passed. Each edition got all eight decisions, determining citations, and scope judgments and gave no unsupported numerical assertions. [Suite](suite.json) · [Audited scores](scores.json)

| Panel | Previous score | Compact score | Previous deduplicated bytes | Compact deduplicated bytes |
|---|---:|---:|---:|---:|
| Ordinary citation | 12/12 | 12/12 | 638,767 | 327,392 |
| Protocol and case escalation | 12/12 | 12/12 | 772,275 | 574,231 |
| **Total** | **24/24** | **24/24** | **1,411,042** | **901,623** |

The ordinary candidate used ten opens and no full study page or replay archive. It consulted one 4,413-byte pinned protocol while answering the ranking comparison. The previous edition used 15 opens and opened the same full study page four times at different anchors. The full payload was counted once in the deduplicated total. [Previous ordinary journal](ordinary-baseline-opens.json) · [Compact ordinary journal](ordinary-candidate-opens.json)

The escalation candidate opened two pinned protocols for details about the split, selector, and retained prediction replay. It opened the full study page twice for claim 83, first to locate the case and then at its exact published anchor. That was one distinct full-page payload. The previous edition also reached claim 83 and read the paired CSV and raw case file along the way. Neither session downloaded a replay archive. Deduplicated bytes fell 25.6% on this panel and 36.1% overall. [Previous escalation journal](escalation-baseline-opens.json) · [Compact escalation journal](escalation-candidate-opens.json) · [Claim 83 response](escalation-candidate-answers.md#se3)

## Publication and scope

The tested deployment exposed the compact catalog, run and case exports, and pinning information used in the retest. Each SciFact run export now carries a direct plain-text protocol route. The full study pages contain the verification details and downloads. The public byte check matched all three replay ZIPs and their presence on the canonical pages to the tested artifact. [Live verification and payload sizes](live-verification.json)

There was one matched pair per panel. Earlier fresh science panels and these panels used different questions, so their outcomes remain separate. The byte counts include the starting homepage and charge full payloads even when only an excerpt is shown. They do not measure network compression, latency, or billing. The offline replay reproduced the full-bundle scores exactly.

```sh
dir=experiments/knowledge_graph_navigation/agent-regression
run="$dir/scifact-compact-2026-11-28"
python3.12 "$dir/regression.py" score --suite "$run/replay-suite.json" \
  --baseline "$run/baseline-replay.zip" --candidate "$run/candidate-replay.zip" \
  --results "$run" --require-pass
```
