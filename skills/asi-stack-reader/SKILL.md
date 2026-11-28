---
name: asi-stack-reader
description: Consult The ASI Stack living book to locate a passage, check a saved decision against later evidence, and cite a result with its scope.
---

# Read The ASI Stack

Start at the [agent index](https://corbensorenson.github.io/asi-stack-book/agent-index.json) to identify the current book revision and the available routes. The routes work over ordinary HTTP.

1. For a known record ID, hash the exact UTF-8 ID with SHA-256. Substitute the first two lowercase hex characters into the shard template and select that ID from the shard's records. Compare the shard snapshot_id with the agent index. The bundled Python client offers the same lookup with --record ID.
2. For a question, search the [small evidence discovery index](https://corbensorenson.github.io/asi-stack-book/agent/discovery.json) by title, question, or alias. For a headword or acronym, start with the [AI dictionary](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/knowledge-graph/dictionary.json) and inspect its worked examples and measurements.
3. Open the result’s section_url for the determining passage. Alternate locators also carry a section_url. Use the export’s canonical URL in your answer and retain its comparison, denominator, and scope. The [section index](https://corbensorenson.github.io/asi-stack-book/agent/sections.json) gives a small export of each addressable chapter section with its canonical URL and footnotes. The section template also resolves a known volume ID and heading anchor directly. For a theorem, search declaration names and premises or open the [formal declarations](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/proof-declarations.html).
4. For a case, use the graph record's case_sources to check the file digests and resolve the exact JSON Pointers. For a saved result, follow edges marked supersedes_decision and compare the revisions. The [citation history](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/citation-history.html) gives an interactive comparison.
5. Report the decision, decisive evidence, and scope. Give the canonical passage URL, record ID, and book revision. Include the evidence revision and result digest when citing a run. When a quantity was unmeasured, say so and cite the measurement boundary.

The [SciFact claim 7 example](https://corbensorenson.github.io/asi-stack-book/agent/scifact-claim-7.md) verifies both outcomes from the pinned readings. The Python client supports --scifact-example and --case-inputs ID. Use Python 3.10 or later.

The [graph manifest](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/knowledge-graph/manifest.json) describes the complete archive and paginated relationships for offline graph analysis.
