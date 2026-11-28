# Agent reading regression check

Six frozen panels cover 24 questions about the public book. Each panel has one independently run agent per edition. The same question wording, model configuration, reading tool, entry page and budget apply in each pair. The reader charges the full uncompressed payload for every open and separately counts distinct payload hashes within each session. A reviewer applies the frozen rubric's three binary criteria. The scorer audits the actual document bytes, displayed excerpts, corpus manifests, answer digests, and completeness before aggregating grades. [First run](run-2026-11-28/results.md) · [ByteFlow and SciFact follow-up](followup-2026-11-28/results.md) · [Compact SciFact retest](scifact-compact-2026-11-28/results.md) · [Book-wide compact retest](book-compact-2026-11-28/results.md) · [Study and proof retest](study-proof-compact-2026-11-28/results.md) · [Focused proof lookup](proof-lookup-2026-11-28/results.md) · [Proof application confirmation](proof-lookup-aliases-2026-11-28/results.md)

## Repeat the check

Use a full Git checkout so the reader can resolve commit-pinned source citations locally. From the repository root, download the two tested Pages artifacts from the build runs listed in [suite.json](suite.json). Save each artifact as the original ZIP. GitHub CLI can fetch the ZIP with `gh api repos/corbensorenson/asi-stack-book/actions/artifacts/ARTIFACT_ID/zip > edition.zip`. The score command takes both ZIP paths and checks the archive hash as well as the manifest and individual documents. This avoids rendering during a trial.

Open one fresh agent per panel and edition, with identical model and reasoning settings. Give it the panel file from [panels](panels), its read command, and the answer output path. Supply the answer rules and budget from [protocol.md](protocol.md). Do not supply the rubric, answers, grades, or another agent's log. Start at the homepage. Use a separate journal for each session and run calls against a given journal sequentially. For example:

```sh
python3.12 experiments/knowledge_graph_navigation/agent-regression/regression.py read \
  baseline science /path/to/baseline.zip scratch/science-baseline-opens.json index.html
```

Use the same participant prompt in both editions. Substitute the absolute checkout path, the panel path, the complete `read` command, and the answer path.

> You are a fresh participant in a matched reading comparison. Work in `{checkout}`. Read only the four questions in `{panel path}`. Use only this command for evidence and run each call sequentially because they share a journal: `{read command} ROUTE [FIND]`. Open `index.html` first. For a discovered JSON catalog of evidence records you may use `ROUTE --batch 'clue one' 'clue two'` to match multiple clues in one open. Follow publicly discoverable routes, compute addresses from published instructions, and cite the exact location. Limit 18 opens, 52000 displayed bytes total, 5500 per open. Use no other sources and avoid inspecting other sessions, rubric, or artifacts. Save answers headed by the four question IDs in `{answer path}`. Include decision, exact citation and scope, or say what remains unresolved. Report only completion.

The optional focus phrase follows the route. For a discovered JSON record catalog, use the same route followed by `--batch` and several quoted clues. Save answers under names such as `science-baseline-answers.md`. Score independently under [rubric.md](rubric.md) and save `science-baseline-grades.json` with the answer file's SHA-256, a `questions` object keyed by question ID, Boolean `decision`, `citation` and `scope` per question, plus an `unsupported_numbers` count. Supply a `note` on any partial grade. See the retained run for examples.

```sh
python3.12 experiments/knowledge_graph_navigation/agent-regression/regression.py score \
  --baseline /path/to/baseline.zip --candidate /path/to/candidate.zip \
  --results scratch --require-pass
```

The scorer prints the result under either outcome. Exit status 1 means at least one measured regression gate failed. Exit status 2 means an input, artifact, log or grade was invalid.

### Compare new revisions

Use full Pages archives for another generative trial. Freeze their identities before dispatch. Pass `--suite scratch/suite.json` immediately after `read` and `score` in the commands above. Add `--panels` and `--rubric` to `freeze` to use a new set in separate repository paths. Keep those files and the suite with the results.

```sh
python3.12 experiments/knowledge_graph_navigation/agent-regression/manage_suite.py freeze \
  --baseline baseline.zip --candidate candidate.zip --output scratch/suite.json
```

### Audit a retained run

The build artifacts expire. The checked-in replay ZIPs contain the tested bundle manifests and exactly the site assets needed to audit the recorded reads. Pinned repository citations replay from Git. Score with the replay suite to verify the retained grades and metrics offline. Its suite digest identifies the replay packet. The original scores retain the full comparison suite digest. Full editions are required for new agent sessions.

```sh
run=experiments/knowledge_graph_navigation/agent-regression/run-2026-11-28
python3.12 experiments/knowledge_graph_navigation/agent-regression/regression.py score \
  --suite "$run/replay-suite.json" --baseline "$run/baseline-replay.zip" \
  --candidate "$run/candidate-replay.zip" --results "$run" --require-pass
```

## Interpretation

The benchmark tests evidence retrieval from the living book. It measures document bytes in the reading harness, not HTTP compression, wall-clock latency or model billing. The score reflects the fixed rubric and named sources. A result on this suite can catch regressions in these workflows. Findings on a substantially different workload require a fresh suite. The grade is supplied by a reviewer and the replay process checks its integrity and aggregation.
