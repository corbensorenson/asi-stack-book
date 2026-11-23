# November 23 live search baseline

This baseline captures the public ASI Stack at source revision
`83c0cd568b30bcc1b1b912a98190c0d8885a8d87`. Its graph snapshot was
`b40ecf4c68d8a09228e444574773ddaa629553154b967fe0fd80ad4e7948d9f3`.

The sixteen authored tasks each had a short phrase, a research question,
and preselected exact evidence destinations. Chromium captured the first
five results from the technical book, Human Reader, and graph. The
paper-library Atlas checks bring the total to 98. Each book entry point was
first warmed with a known-good query. The audit cleared the previous query,
waited for results or an empty state, and allowed the panel to settle.

| Search entry point | Exact target, short phrase | Exact target, full question |
| --- | ---: | ---: |
| Technical book | 1/16 | 0/16 |
| Human Reader | 4/16 | 1/16 |
| Knowledge graph | 7/16 | 3/16 |

An exact target score measures landing at one of the recorded evidence
routes. Related parent sections and source-title hits are visible in the
raw rows. The interfaces searched different corpora. Use this record as
the observed user-facing baseline. A comparison of graph navigation with
ordinary search on a common corpus requires a separate evaluation.

- [Task definitions](tasks.json)
- [Scored browser captures](scored.json)
- [Published index census](census.json)
- [Additional known-answer and timing controls](controls.json)
