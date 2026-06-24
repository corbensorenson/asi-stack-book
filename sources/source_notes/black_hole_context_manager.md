# Source Note: Black Hole Context Manager

| Field | Value |
|---|---|
| Source ID | `black_hole_context_manager` |
| Source title | Black Hole Context Manager |
| Ingestion date | 2026-06-24 |
| Source version / URL | Google Docs source in inventory: https://docs.google.com/document/d/14KPQT5d86HaFZzQdUr_Sn5p7-8cscSqIZm5zxkijl-I |
| Ingestion basis | Local raw cache inspected at `sources/raw/google_docs/black_hole_context_manager.txt`; raw text is not published. |

## Thesis

Black Hole Context Manager is a production-style context-management specification that ranks, freezes, evicts, and routes chunks by relevance, entropy, mass, drift, security, and context budget. Its book value is as a concrete context-transaction and memory-budget design.

## Mechanisms

- Represent chunks with content, embeddings, entropy, mass, timestamps, and cached scores.
- Recompute mass lazily when the goal vector drifts.
- Combine normalized entropy and goal similarity through a multiplicative score.
- Rate-limit and sanitize inputs.
- Protect critical context through cryptographic or multi-turn confirmation paths.
- Cluster active chunks, freeze irrelevant clusters, and serialize them to colder storage.
- Manage context budgets by evicting low-mass chunks while preserving high-priority state.

## Evidence

- The source is a code/specification document for a context manager.
- It includes implementation-oriented details but no local test run, package, or benchmark in this repository.
- Treat it as a design source for context management patterns.

## Failure Modes

- Preserving high-entropy text that is irrelevant to the current goal.
- Dropping low-mass chunks that are legally or evidentially critical.
- Letting goal drift change memory priority without audit.
- Freezing clusters too aggressively and losing recoverable context.
- Treating rate limiting and HMAC attestation as complete poisoning defense.

## Book Chapters Supported

- `context-transactions-snapshots-mounts-and-taint` (Context Transactions, Snapshots, Mounts, and Taint)

## Claims To Add Or Update

- Use this source for context-budget algorithms, chunk mass, freezing, eviction, and goal-drift handling.
- Do not claim production readiness without executable code and tests in this repo.

## Open Questions

- Should the VCM/context transaction schema include entropy, goal similarity, and criticality fields?
- What small fixture can test freeze/evict behavior without private data?
