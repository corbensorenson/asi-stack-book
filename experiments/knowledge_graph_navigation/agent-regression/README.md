# Agent reading regression check

Six frozen panels cover 24 questions about the public book. Each panel has one independently run agent per edition. The same question wording, model configuration, reading tool, entry page and budget apply in each pair. The reader charges the full uncompressed payload for every open and separately counts distinct payload hashes within each session. Human judgment supplies the frozen rubric's three binary criteria. The scorer audits the actual document bytes, displayed excerpts, corpus manifests, answer digests, and completeness before aggregating grades.

## Repeat the check

From the repository root, download the two tested Pages artifacts from the build runs listed in [suite.json](suite.json). Select only each commit-bound artifact named in the suite. Preserve the downloaded ZIP bytes. The score command takes both ZIP paths and checks the archive hash as well as the manifest and individual documents. This avoids rendering during a trial.

Open one fresh agent per panel and edition, with identical model and reasoning settings. Give it the panel file from [panels](panels), its read command, and the answer output path. Supply the answer rules and budget from [protocol.md](protocol.md). Do not supply the rubric, answers, grades, or another agent's log. Start at the homepage. Use a separate journal for each session. For example:

```sh
python3.12 experiments/knowledge_graph_navigation/agent-regression/regression.py read \
  baseline science /path/to/baseline.zip scratch/science-baseline-opens.json index.html
```

The optional focus phrase follows the route. For a discovered JSON record catalog, use the same route followed by `--batch` and several quoted clues. Save answers under names such as `science-baseline-answers.md`. Score independently under [rubric.md](rubric.md) and save `science-baseline-grades.json` with the answer file's SHA-256, a `questions` object keyed by question ID, Boolean `decision`, `citation` and `scope` per question, plus an `unsupported_numbers` count. Supply a `note` on any partial grade. See the retained run for examples.

```sh
python3.12 experiments/knowledge_graph_navigation/agent-regression/regression.py score \
  --baseline /path/to/baseline.zip --candidate /path/to/candidate.zip \
  --results scratch --require-pass
```

The scorer prints the result under either outcome. Exit status 1 means at least one measured regression gate failed. Exit status 2 means an input, artifact, log or grade was invalid. Use a new suite and explicitly freeze it for a different pair of revisions or a new question set. Archival replay uses the exact tested revisions listed here.

## Interpretation

The benchmark tests evidence retrieval from the living book. It measures document bytes in the reading harness, not HTTP compression, wall-clock latency or model billing. The score reflects the fixed rubric and named sources. A result on this suite can catch regressions in these workflows. Findings on a substantially different workload require a fresh suite. The grade is supplied by a reviewer and the replay process checks its integrity and aggregation.
