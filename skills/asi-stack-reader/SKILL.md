---
name: asi-stack-reader
description: Consult The ASI Stack living book to locate a passage, check a saved decision against later evidence, and cite a result with its scope.
---

# Read The ASI Stack

Start at the [agent index](https://corbensorenson.github.io/asi-stack-book/agent-index.json) to identify the current book revision and the available routes. The routes work over ordinary HTTP.

1. For a known record ID, hash the exact UTF-8 ID with SHA-256. Substitute the first two lowercase hex characters into the shard template and select that ID from the shard's records. Compare the shard snapshot_id with the agent index. The bundled Python client offers the same lookup with --record ID.
2. For evidence questions, match all your clues in one read of the [short lookup catalog](https://corbensorenson.github.io/asi-stack-book/agent/lookup.json). Keep the matching section URLs and follow them directly. The bundled client accepts multiple clues in one invocation, for example python3 read_book.py --find "claim ledger" --find "capability replacement". Exact identifiers, aliases, and numbers help disambiguate a result. Use the [full discovery index](https://corbensorenson.github.io/asi-stack-book/agent/discovery.json) for alternate locators and specialized records, or the [AI dictionary](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/knowledge-graph/dictionary.json) for terms.
3. Open the result’s section_url. The primary export includes the passage, its evidence limits, and the available citation fields. A case export includes the evidence revision, result digest, and exact input pointers. Formal declarations include the Lean statement and pinned source line. Use the export’s canonical URL for the passage. Read another source if the export leaves a fact your question requires unresolved. The [section index](https://corbensorenson.github.io/asi-stack-book/agent/sections.json) gives a small export of each addressable chapter section with its canonical URL and footnotes. The section template also resolves a known volume ID and heading anchor directly. For a theorem, search declaration names and premises or open the [formal declarations](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/proof-declarations.html).
4. To independently verify a case, use case_sources to check the file digests and resolve the exact JSON Pointers. For a saved result, follow edges marked supersedes_decision and compare the revisions. The [citation history](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/citation-history.html) gives an interactive comparison.
5. Report the decision, decisive evidence, and scope. Give the canonical passage URL, record ID, and book revision. Include the evidence revision and result digest when citing a run. When a quantity was unmeasured, say so and cite the measurement boundary.

The [SciFact claim 7 example](https://corbensorenson.github.io/asi-stack-book/agent/scifact-claim-7.md) verifies both outcomes from the pinned readings. The Python client supports --scifact-example and --case-inputs ID. Use Python 3.10 or later.

The [graph manifest](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/knowledge-graph/manifest.json) describes the complete archive and paginated relationships for offline graph analysis.
