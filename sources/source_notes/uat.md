# Source Note: Unified Adaptive Tribunal

| Field | Value |
|---|---|
| Source ID | `uat` |
| Source title | Unified Adaptive Tribunal |
| Ingestion date | 2026-06-24 |
| Source version / URL | Google Docs source in inventory: https://docs.google.com/document/d/1R7wKo2qg5waosEa-SwC-JKF77qoDiiEp1Df4Gbap0VE |
| Ingestion basis | Local raw cache inspected at `sources/raw/google_docs/uat.txt`; raw text is not published. |

## Thesis

The Unified Adaptive Tribunal is a protocol for turning multi-model drafting into constrained knowledge engineering. Its central claim is that high-stakes AI writing should shift the human role from unchecked prompt steering to adjudication of evidence-tiered propositions after retrieval, decomposition, adversarial review, and compression.

## Mechanisms

- Generate orthogonal priors: structural maps, retrieval dossiers, and anti-premise or dialectical critiques.
- Treat the retrieval dossier as the explicit verification boundary for the automated system.
- Decompose drafts into atomic propositions and assign proposition states such as verified, inferred, or unsupported.
- Retain directly supported propositions, flag inferred propositions for subject-matter-expert review, and remove unsupported propositions.
- Run a bounded adversarial siege in which red-team critique rotates through logic, citation, and omission checks.
- Prevent intent leakage in adversarial review by giving the red team only the dossier and draft, not the original user prompt.
- Stop revision with a double lock: syntactic stability, semantic stability, and a hard cycle cap.
- Compress the final draft while preserving verified proposition count.
- Preserve human checkpoints for adjudication and final sign-off.

## Evidence

- The source contains a reference architecture, implementation pseudocode, operational guidance, and explicit limitations.
- It provides concrete protocol states and termination criteria that can inform the ASI Stack evidence layer.
- It reports no locally reproduced benchmark, no implemented pipeline in this repository, and no independent validation of the suggested thresholds.
- Source-derived claims should distinguish protocol design from measured performance.

## Failure Modes

- Correlated hallucination when the retrieval corpus itself contains a widely repeated falsehood.
- Decomposition loss when nuanced claims fail atomic extraction and are deleted.
- Plateau trapping where critique and revision stabilize around a mediocre but defensible draft.
- Consensus bias against emerging or minority claims not present in indexed sources.
- Tool fragility when search or retrieval returns low-quality material.
- Excessive token and latency cost relative to task stakes.

## Book Chapters Supported

- `evidence-states-and-claim-discipline` (Evidence States and Claim Discipline)
- `moral-uncertainty-and-value-conflict` (Moral Uncertainty, Value Conflict, and Contestable Governance)
- `claim-ledgers-and-belief-revision` (Claim Ledgers and Belief Revision)
- `unified-adaptive-tribunal-and-adversarial-review` (Unified Adaptive Tribunal and Adversarial Review)
- `benchmark-ratchets-and-anti-goodhart-evidence` (Benchmark Ratchets and Anti-Goodhart Evidence)

## Claims To Add Or Update

- Use UAT as a protocol source for adversarial review, proposition-tiering, retrieval-bounded verification, and SME checkpoints.
- Connect UAT states to Appendix C support states while keeping them distinct from proof or empirical validation.
- Do not claim UAT can discover novel truth beyond its dossier; the source explicitly limits it to verification and compression of available evidence.

## Open Questions

- Should the book define a small JSON schema for proposition-level tribunal records?
- Which UAT thresholds should remain examples rather than normative architecture requirements?
- Can the book-writing pipeline itself use a lightweight UAT pass before a future v1.0 release candidate?
