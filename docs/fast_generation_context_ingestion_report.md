# Fast Generation Context Ingestion Report

Date: 2026-06-24

Raw packet location: `sources/inbox/fast_generation_browser_note_2026-06-24/`

Public status: raw packet is local-only and ignored by git. This report is the public-safe synthesis.

## Ingestion Boundaries

- The browser-GPT packet was treated as author intent, chapter-scoping guidance, and external-literature queue context.
- No private conversation wording was copied verbatim into the public manuscript.
- No third-party speedup, benchmark, or quality claim was promoted from the packet.
- No claim was promoted to `source-derived`, `prototype-backed`, `synthetic-test-backed`, `empirical-test-backed`, or `external-literature-backed`.
- Primary papers named by the packet still require source records, source notes, and citation normalization before the book can rely on them.

## Added or Strengthened

| Area | Public update |
|---|---|
| Chapter structure | Added `Fast Generation Architectures` as a Part III chapter after Generate-Verify-Repair Compression. |
| Stack interface | Framed fast generation as PlanForge-selected generation mode routing through VCM, generator, verifier, Talos, Benchmaxxing, and SCF gates. |
| Evidence discipline | Added `effective_verified_tokens_per_second` and `useful_solution_per_second` as planned metrics rather than reported results. |
| Research direction | Preserved multi-seed diffusion and hybrid AR/MTP/diffusion systems as speculative research directions. |
| Test backlog | Added planned tests for AR baseline, speculative decoding, MTP, internal heads, diffusion, multi-seed diffusion, hybrid repair, planner-selected routing, risk-tiered decoding, and KV-cache accounting. |
| Record schema | Added a `generation_mode_record` schema and fixture to validate route metadata without reporting any unrun benchmark result. |
| Proof backlog | Added two planned proof targets for generation-mode records and raw-token-speed promotion blocking. |

## External Literature Queue

The packet suggested these external literature families for future source-note work:

| Area | Needed before use |
|---|---|
| Multi-token prediction and future-token heads | Add source records, read primary papers, create source notes, and map claims to exact mechanisms. |
| Speculative decoding and speculative sampling | Separate draft, verifier, accepted-token, rejected-token, and correctness claims. |
| Multi-head and feature-level drafting | Record whether the method proposes surface tokens, branches, or latent features. |
| Lookahead, trie retrieval, and branch verification | Separate retrieval/procedural-memory acceleration from generation-model architecture. |
| Diffusion language models and arbitrary-order generation | Distinguish sketching, denoising, span commitment, and final verification. |
| Early exit and self-speculative inference | Specify the layer boundary between cheap draft and later verifier/corrector. |
| State-space and recurrent alternatives | Separate sequence-processing efficiency from accepted-token-per-step acceleration. |
| KV-cache and serving-layer accelerators | Separate aggregate throughput, memory bandwidth, and single-request verified-output latency. |

## Remaining Missing or Blocked Items

| Item | Needed before claim promotion |
|---|---|
| Third-party bibliography | Add citation-normalized external records to `sources/source_inventory.json`. |
| External source notes | Read the primary sources and create source notes under `sources/source_notes/`. |
| Generation-mode implementation | The JSON Schema fixture and finite Lean predicates exist; executable route code, accepted-output accounting, and benchmark artifacts are still missing. |
| Benchmarks | Implement and run at least one baseline and one acceleration-mode test with accepted-output accounting. |
| Lean expansion | Extend `AsiStackProofs.FastGeneration` only after additional route semantics or benchmark records are concrete. |

## Validation Requirement

After this ingestion, the required validation loop is:

```bash
python3 scripts/sync_scaffold.py
python3 scripts/sync_proof_manifest.py --check
python3 scripts/validate_proof_readiness.py
python3 scripts/validate_publication.py
python3 scripts/validate_book.py
python3 scripts/validate_visual_coverage.py
python3 scripts/validate_schemas.py
python3 scripts/validate_protocol_examples.py
(cd lean && lake build)
LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 quarto render --to html
```
