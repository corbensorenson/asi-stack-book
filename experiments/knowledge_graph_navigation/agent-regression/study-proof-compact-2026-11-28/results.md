# Compact study and proof retest

The new edition gave the study agent enough information to cite the claim-review case and explain the receiver rerun scope from compact exports. In the matched retest it used no full study pages and retained full answer credit. The proof session also preserved full credit and used fewer deduplicated bytes. [Protocol](protocol.md) · [Fresh questions](panels) · [Rubric](rubric.md) · [Live verification](live-verification.json)

## Publication

The focused catalog is 22,660 bytes and lists 54 study, case and proof records. The general catalog is 41,413 bytes. Run exports link the pinned protocol, recorded result, paired-case table, and reviewed case exports. The receiver exports state that the command takes a new network observation. The earlier observation remains available at its recorded revision and digest. Case C3 exposes the actual one-versus-two opens and citation judgments. The public check matched 103 site files, including the study and proof exports, case tables, and 11 replay kits, and verified both pinned receiver results. [Focused catalog](https://corbensorenson.github.io/asi-stack-book/agent/topics/studies-and-proofs.json) · [Case C3](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-claim-review.html#run-claim-review-matched--case-c3)

## Matched results

Four fresh sessions answered eight questions using the preceding book-wide edition `235a908a` and the deployed edition `da9bd7cd`. The same startup page, reading tool, allowance and inherited model settings applied in both editions. One reviewer scored with edition labels visible. Both editions earned full credit on all decisions, determining citations and scope statements, with zero unsupported numerical claims. All four aggregate regression gates passed. [Frozen suite](suite.json) · [Scores](scores.json)

| Panel | Previous score | New score | Previous deduplicated bytes | New deduplicated bytes |
|---|---:|---:|---:|---:|
| Studies | 12/12 | 12/12 | 876,717 | 334,785 |
| Proofs | 12/12 | 12/12 | 391,165 | 372,957 |
| **Total** | **24/24** | **24/24** | **1,267,882** | **707,742** |

Study reading cost fell 61.8%. The previous session opened the claim-review and receiver study pages five times, accounting for two distinct payloads. The new session opened neither full page. It read the exact C3 export and used the receiver run's rerun scope and pinned result link. [Previous study journal](studies-baseline-opens.json) · [New study journal](studies-candidate-opens.json) · [New study answers](studies-candidate-answers.md)

Proof reading cost fell 4.7%. Both sessions reached exact declaration exports and used compact chapter evidence for real-world scope. The new session made 12 opens versus 10. The smaller catalog kept its deduplicated byte cost lower. Neither session loaded a full proof page or module. The combined saving was 44.2%, and neither edition downloaded any replay kit in the retest. [Previous proof journal](proofs-baseline-opens.json) · [New proof journal](proofs-candidate-opens.json)

One matched pair per panel provides a local result for these questions and this model configuration. Deduplicated cost counts distinct payload bytes per session, including the homepage. It leaves latency, network compression and model billing unmeasured. The offline audit reproduced the original metrics and gates.

```sh
dir=experiments/knowledge_graph_navigation/agent-regression
run="$dir/study-proof-compact-2026-11-28"
python3.12 "$dir/regression.py" score --suite "$run/replay-suite.json" \
  --baseline "$run/baseline-replay.zip" --candidate "$run/candidate-replay.zip" \
  --results "$run" --require-pass
```
