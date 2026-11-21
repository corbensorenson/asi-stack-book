# Knowledge graph navigation evaluation

## Question

Does the graph help a reader or agent locate the right book passage or
evidence record under the same retrieval budget as the existing site
search? The comparison measures retrieval and evidence grounding on the
frozen task set.

## Comparison

Use the same rendered local snapshot for both routes. Record the source
commit and working-tree status, the exact input hashes for the graph, the
hash of the site's search index, and the task-file hash before scoring.

Give both routes the same query and at most four primary records. For
technical and reader starts, the baseline uses the corresponding edition's
actual Quarto search, including the technical edition's exact source and
core-claim index entries. For study starts, it uses the existing Evidence
Registry's study links ranked by query overlap. The graph uses the browser
companion's actual search for all starts.

Allow one further hop to a combined total of up to four unique destinations
from the primary documents. Both routes rank eligible links using the same
phrase and token overlap rule. Cross-edition tasks give links to the
requested edition priority in both routes. Baseline links come from the main content.
Graph links come from the selected record and its relation previews. Primary
and followed records each contribute up to 1,000 UTF-8 bytes of excerpts.
The runner preserves missing matches, truncation and browser errors in its
per-task output. No indexing or relevance changes use the scored outcomes.
Development checks exposed error handling and baseline issues before the
final comparison. The recorded run waits for the standard Reader link,
logs 404 responses, counts distinct primary destinations, and treats the
requested edition as a retrieval hint in both routes. The dry-run results
are exploratory. The same task wording, destinations, and budgets were
used throughout, with no tuning of either search index.

## Cases and scoring

Include named lookups, questions that cross the technical and reader
editions, and questions that need a particular run, proof scope, or
evidence limit. Keep exploratory demonstrations such as the e-means and
verifier-rollout smoke routes out of the scored set. Freeze the expected
current record, relevant section or run, and applicable scope before running
either method over the task set. A chapter about the right topic may earn
owner coverage without earning the exact passage or result match.

Report exact-record and owner recall separately. Award exact credit for a
stable graph ID or its canonical document and fragment. Document-level
targets can match at any fragment of the correct document. The five study
cases require the stated limit in the excerpt of the same run. Preserve the
rank of the first exact match and every retrieved excerpt. Report text and
returned record counts by interface and compare paired outcomes by task type.

`tasks.json` holds the twenty fixed tasks. `compare.cjs` runs against a
complete candidate with finalized reading routes and installed products.

```bash
node experiments/knowledge_graph_navigation/compare.cjs _site build/graph-navigation.json
```

This is an authored local evaluation. Measure independent reader or agent
use separately before generalizing task success, time savings, or answer
quality. Graph coverage and schema validity leave the book's support states
unchanged.
