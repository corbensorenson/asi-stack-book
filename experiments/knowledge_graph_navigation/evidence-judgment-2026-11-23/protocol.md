# Shared-corpus evidence judgment pilot

The ten development tasks were frozen in commit `53c55447` before querying the first preview. Both interfaces returned empty results for every question under the initial lexical coverage rule. That capture is preserved. The questions now belong to development. A second set was frozen in commit `ee0c8440` after the matching revision was written and before querying it. Score its full questions and short reformulations as separate conditions. The November 23 live retrieval baseline remains a separate audit of three different indexes and its own 16 tasks.

Both arms use the same revision-bound evidence catalog and matching function. The ordinary arm selects Research evidence in the technical book, Human Reader or paper library, as assigned. The graph arm selects Citable evidence. Look at the top four primary results and follow the first two in rank order. Follow each directly to its rendered book anchor. The graph requires opening its record before following the citation, with at most four route actions per task. The ordinary arm uses up to two under the same rule. Use one query per task in each condition. Preserve primary excerpts, openable locators, the two exact fragments and the graph preview where applicable, with at most 1,400 UTF-8 bytes for any single excerpt. The capture deliberately compares shared-corpus behavior under the same fixed inspection policy. This does not isolate the effect of freely following relationships, or measure the default unfiltered search.

Score four quantities separately:

- **Retrieval.** The predeclared exact evidence target appears in the first four results.
- **Citation.** A followed route resolves to a visible, independently openable fragment that directly supports the answer. Score only from the captured excerpt and primary evidence summary.
- **Scope.** The response states the limiting condition in the rubric and the captured evidence warrants that condition.
- **Answer or justified abstention.** On answerable tasks, require the disposition and its decisive observation or comparison. On the two abstention tasks, require a cited measurement boundary. A blank packet or an unsupported refusal earns zero. Report justified abstentions separately across those two tasks.

This is a small, unblinded pilot. The same agent authored the tasks and adjudicated the recorded packets. The questions concern a known set of records, and the scores do not estimate general research performance. Use failures to prioritize separate work. If tuning from these results, hold out a new task set for the next evaluation.

Run from the repository root with the path to the tested HTML site and an output path. `NODE_PATH` points to the existing Playwright dependency. Set `PLAYWRIGHT_CHROMIUM_EXECUTABLE` when using a local Chrome install.

```sh
pilot=experiments/knowledge_graph_navigation/evidence-judgment-2026-11-23
export NODE_PATH="$PWD/ci/browser/node_modules"
node "$pilot/capture.cjs" _site /tmp/asi-evidence-full.json "$pilot/holdout.json"
node "$pilot/capture.cjs" _site /tmp/asi-evidence-short.json "$pilot/holdout.json" short
```
