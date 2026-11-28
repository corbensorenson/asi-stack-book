# Book-wide compact reading retest

The live edition provides a 43,285-byte directory for all 89 technical chapters and 26 Reader units. Each volume has its own section index. Parent excerpts give their own text and direct links to subsections. The previous complete section list is 695,701 bytes and remains available. The tested build had 3,597 section destinations and 507 smaller parent exports. We matched 192 public payloads to their tested bytes, including all 115 volume indexes, 23 study-run exports, ten proof exports, and 11 replay kits. The study pages still carry their verification and replay materials. [Live verification](live-verification.json)

## Matched results

Six new sessions answered 12 questions in three matched panels on the preceding live edition `a2e05e10` and the new edition `235a908a`. The same prompt, inherited model configuration, and reading allowance applied throughout. One reviewer graded the frozen rubric with edition labels visible. All four aggregate regression gates passed. [Protocol](protocol.md) · [Questions](panels) · [Rubric](rubric.md) · [Audited scores](scores.json)

| Panel | Previous score | Compact score | Previous deduplicated bytes | Compact deduplicated bytes |
|---|---:|---:|---:|---:|
| Technical chapters | 6/12 | 11/12 | 1,155,344 | 473,851 |
| Studies and proof | 12/12 | 12/12 | 357,947 | 878,889 |
| Reader and missing case | 11/12 | 12/12 | 834,712 | 429,040 |
| **Total** | **29/36** | **35/36** | **2,348,003** | **1,781,780** |

The new edition used **24.1% fewer deduplicated bytes** across the three panels. It found all twelve deciding citations, compared with nine in the preceding edition. Both editions gave zero unsupported numerical assertions. Counting distinct full-page payloads per session gave three for the new edition and seven for the preceding edition. Neither edition downloaded a replay. The comparison charges the full bytes of any fetched document even when the reader displays an excerpt.

- **Technical chapters.** The new session used 59.0% fewer bytes and opened no full HTML page after the homepage. It located the two answers the preceding session had left unresolved. It still left the break-even study's measurement scope unresolved. The final section was truncated by the remaining display allowance. [Candidate answers](chapters-candidate-answers.md) · [Candidate journal](chapters-candidate-opens.json)
- **Studies and proof.** Both sessions earned full credit. The new session used 145.5% more bytes. It reached compact evidence and pinned protocols first, then reopened two full study pages six times in total while checking what a receiver rerun would observe and which claim-review case was missed. Those two pages contributed 530,207 deduplicated bytes. [Candidate journal](evidence-candidate-opens.json) · [Previous journal](evidence-baseline-opens.json)
- **Reader and missing case.** The new session used 48.6% fewer bytes. It read the Reader excerpts, then loaded the full verification study for the unexported `1-tick-15` row and used the pinned protocol for the cutoff rule. It gave the exact case and denominator. [Candidate answers](reader-candidate-answers.md#br4) · [Candidate journal](reader-candidate-opens.json)

One matched pair per panel gives a local observation about route choice under the stated allowance. Raw payload bytes include the homepage. The comparison leaves network compression, latency, model billing and cross-model variation unmeasured.

## Replay

The offline replay matched the original metrics and gates exactly. The run retains the responses, grades, read journals, verified site subset, and both suite manifests. From the repository root:

```sh
dir=experiments/knowledge_graph_navigation/agent-regression
run="$dir/book-compact-2026-11-28"
python3.12 "$dir/regression.py" score --suite "$run/replay-suite.json" \
  --baseline "$run/baseline-replay.zip" --candidate "$run/candidate-replay.zip" \
  --results "$run" --require-pass
```
