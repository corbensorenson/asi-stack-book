---
name: asi-stack-reader
description: Consult The ASI Stack living book to locate a passage, check a saved decision against later evidence, and cite a result with its scope.
---

# Read The ASI Stack

Start at the [agent index](https://corbensorenson.github.io/asi-stack-book/agent-index.json) to identify the current book revision and the available routes. The routes work over ordinary HTTP.

1. For a known record ID, hash the exact UTF-8 ID with SHA-256. Substitute the first two lowercase hex characters into the shard template and select that ID from the shard's records. Compare the shard snapshot_id with the agent index. The bundled Python client offers the same lookup with --record ID.
2. Match all your clues in one read of the [study and proof catalog](https://corbensorenson.github.io/asi-stack-book/agent/topics/studies-and-proofs.json) for runs, cases and Lean declarations. Use the [SciFact catalog](https://corbensorenson.github.io/asi-stack-book/agent/topics/scifact.json) for scientific citation or the [general evidence lookup](https://corbensorenson.github.io/asi-stack-book/agent/lookup.json) for other evidence. Keep the matching section URLs and follow them directly. The bundled client searches the general catalog with several clues in one invocation, for example python3 read_book.py --find "claim ledger" --find "capability replacement". Use the [full discovery index](https://corbensorenson.github.io/asi-stack-book/agent/discovery.json) for alternate locators or the [AI dictionary](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/knowledge-graph/dictionary.json) for terms.
3. For chapter or Reader questions, use the [chapter directory](https://corbensorenson.github.io/asi-stack-book/agent/chapters.json), the matching chapter's section index, and then the relevant section_url. A parent section gives its own text and links to subsections. The [complete section list](https://corbensorenson.github.io/asi-stack-book/agent/sections.json) is available for bulk use.
4. Cite the export’s url directly and stop when you have the facts and scope. A run’s reading fields lead to its pinned protocol, recorded result, exact case exports and paired-case table. Check rerun_scope when it is present to see whether the command makes a new observation. Use the canonical page for context absent from these routes, and reuse an already opened page for further inspection. The proof export gives the exact Lean statement, premises, conclusion and pinned source line. Open a proof body or replay kit when the question requires checking it.
5. To independently verify a case, use case_sources to check the file digests and resolve the exact JSON Pointers. For a saved result, follow edges marked supersedes_decision and compare the revisions. The [citation history](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/citation-history.html) gives an interactive comparison.
6. Report the decision, decisive evidence, and scope. Give the canonical passage URL, record ID, and book revision. Include the evidence revision and result digest when citing a run. When a quantity was unmeasured, say so and cite the measurement boundary.

The [SciFact claim 7 example](https://corbensorenson.github.io/asi-stack-book/agent/scifact-claim-7.md) verifies both outcomes from the pinned readings. The Python client supports --scifact-example and --case-inputs ID. Use Python 3.10 or later.

The [graph manifest](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/knowledge-graph/manifest.json) describes the complete archive and paginated relationships for offline graph analysis.
