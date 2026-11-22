# Evidence judgment with graph and book search

This pilot used eight authored questions, two entry points, and the same rendered candidate at `06960ed72764a2be62b7a0db198d915500d6a6ec`. The questions, fixed queries and scoring rubric were recorded in `18afea66` before packet collection. Each route could inspect four search results, follow four links and read up to 1,000 UTF-8 bytes per inspected record. The recorded packets include the search index digests and the graph snapshot identity. [Protocol](judgment_protocol.md) · [Questions](judgment_tasks.json) · [Frozen-query packets](judgment_artifacts/frozen-query-packets.json)

## Frozen queries

| Route | Answer | Citation | Scope |
| --- | ---: | ---: | ---: |
| Ordinary Quarto search | 1/8 | 1/8 | 1/8 |
| Knowledge graph | 5/8 | 5/8 | 5/8 |

The same agent authored the tasks and scored the evidence it could read in each packet. These are unblinded descriptive counts for fixed queries. The ordinary search returned no records on seven queries. The graph has a broader searchable corpus, including generated study runs, and uses a different ranking policy. The comparison measures those interfaces as delivered. It leaves the individual effects of graph structure, ranking, corpus coverage and query formulation unresolved.

| Task | Book search A/C/S | Graph A/C/S | Answer grounded in the available packets |
| --- | --- | --- | --- |
| J01. Deployment inference | 1/1/1 | 1/1/1 | The result supports a policy effect on 16 authored tasks in one local campaign. Certification on another deployment needs evidence from that deployment or independently justified transfer. The book packet supplied the Appendix C reconciliation. The graph packet supplied the selected local policy effect citation with the `proxy_for` boundary. |
| J02. Shared observation | 0/0/0 | 0/0/0 | Abstained. The graph returned general shared-dependency and verifier-capture statements. Its inspected excerpts did not reach the explicit discussion separating multiple receipts from separate effect observations. |
| J03. Scheduler and reuse | 0/0/0 | 1/1/1 | Retest the candidates at the actual expanded-work cap with the scheduler and cost denominator fixed across arms. The factorial run changes whole versus routine verification from 28 versus 20 under the proposal cap to 4 versus 16 under expanded work. The second scheduler also changes the proposal-cap ranking. These are dependent cells over 16 authored tasks. The graph packet supplied both named run routes. |
| J04. Matched receiver access | 0/0/0 | 1/1/1 | Both second-source routes verified 80 of 288 closures. The gateway saved 192 caller requests and added 54,168 status payload bytes. The graph packet supplied the matched-access run. Four authored tasks, supplied revisions and local processes leave active operator effort open. |
| J05. Delayed effect observation | 0/0/0 | 1/1/1 | Check commit against the grant in force at the write. The later observation finds an already authorized commit in the grant-to-effect regression. Grant revision, commit and observation are separate in four ordered schedules using a shared database and owner. The graph packet supplied the exact regression run. |
| J06. Circle proof boundary | 0/0/0 | 1/1/1 | The retained evidence covers one pinned rope target with command/result receipts and a finite consumer gate with four rejecting controls. General proof transport remains open. The graph packet supplied the exact selected claim route and proposition. |
| J07. Atlas baseline correction | 0/0/0 | 0/0/0 | Abstained. Neither packet supplied the correction's margin and corrected estimate. |
| J08. Deployed operator minutes | 0/0/0 | 0/0/0 | Abstained. Neither packet supplied the verifier study's explicit labor limit. This leaves the response unsupported under the rubric for a deliberately open question. |

A zero can mean the packet contained no applicable evidence or that its evidence did not meet that scoring criterion. The table preserves failures and omits claims of statistical significance. A future independent trial should allow measured query reformulation, hold out entire question lineages and give both arms access to a common corpus when the question is about navigation structure specifically.

## Short-query sensitivity

After inspecting the frozen packets, the author chose a shorter, familiar search term for each question. Both routes used the same alternative terms, candidate and budget. This post hoc check tests sensitivity to query choice on the same questions. [Alternate queries](judgment_short_queries.json) · [Short-query packets](judgment_artifacts/short-query-packets.json)

| Route | Answer | Citation | Scope |
| --- | ---: | ---: | ---: |
| Ordinary Quarto search | 4/8 | 3/8 | 3/8 |
| Knowledge graph | 4/8 | 4/8 | 3/8 |

| Task | Book search A/C/S | Graph A/C/S | Response and remaining gap |
| --- | --- | --- | --- |
| J01 | 1/1/1 | 1/1/1 | Both packets preserve the local-policy result and its transfer limit. |
| J02 | 1/1/1 | 0/0/0 | Unit 15's shipment discussion supports treating both reports as one reported event and seeking evidence tied to the effect. The graph returned no hits for the shorter term. |
| J03 | 0/0/0 | 1/1/1 | The graph still reaches the scheduler run. Keep both methods until the matched comparison uses the actual cap and scheduler. Ordinary search surfaced other scheduler studies. |
| J04 | 1/1/1 | 1/1/1 | Both packets reach the receiver study and preserve the equal closure, caller-call and transport comparison with its local scope. |
| J05 | 0/0/0 | 1/1/0 | The graph reaches Unit 3's `Revocation Is a Race` section. Order the grant and effect before judging authorization. The excerpt does not supply the specific local delayed-observation check needed for the scope point. |
| J06 | 1/0/0 | 0/0/0 | The book's Circle core passage supplies the applicable narrow inference. Its exact-case results appear as headings without enough evidence for the citation or scope points. The graph surfaced source and core records and missed the selected claim. |
| J07 | 0/0/0 | 0/0/0 | Both routes found the right paper or nearby chapters. The excerpts missed the corrected margin and its decision. |
| J08 | 0/0/0 | 0/0/0 | The graph found verifier runs and diagnostic cost measures. Neither packet supplied an explicit scope statement about active operator minutes. |

Use the graph for named runs and claim-to-artifact trails. Keep ordinary search available for locating narrative examples. The short-query check tied on answers and scope, and the graph supplied one more precise citation under this budget. The source and study excerpts missed the passages needed to decide the Atlas and operator-time questions in both conditions.

## Reproduce the packets

Build and finalize the candidate at the recorded manuscript revision. Use the browser executable recorded by the runner, or set `PLAYWRIGHT_CHROMIUM_EXECUTABLE` to a compatible Chromium binary. From the repository root run the two commands below. To reproduce the original runner bytes, use `compare.cjs` from `18afea66` for the first command. The second command uses the alternate-query mode introduced with this report.

```sh
node experiments/knowledge_graph_navigation/compare.cjs SITE packets.json judgment
node experiments/knowledge_graph_navigation/compare.cjs SITE alternate-packets.json judgment-short-queries
```

The raw packets record all inspected excerpts and their ordering. Re-score against the frozen rubric to challenge any individual judgment.
