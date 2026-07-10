# Source Note: AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents

| Field | Value |
|---|---|
| Source ID | `ext_agentdojo_2024` |
| Source title | AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents |
| Ingestion date | 2026-07-10 |
| Source version / URL | NeurIPS 2024, https://proceedings.neurips.cc/paper_files/paper/2024/hash/97091a5177d8dc64b1da8bf3e1f6fb54-Abstract-Datasets_and_Benchmarks_Track.html |
| Citation label | Debenedetti et al. (2024), AgentDojo |
| Published / updated | 2024 / 2024 |
| Ingestion basis | Metadata-first intake from the public conference record and repository inventory; no benchmark task or defense has been locally executed. |

## Thesis

AgentDojo is a benchmark comparator for tool-using agents operating over untrusted data, with security tasks, prompt-injection attacks, and defenses.

## Mechanisms

- The inventory identifies realistic tasks, tool use, security test cases, attacks, and defenses.
- It is routed to security, runtime adapters, benchmark ratchets, and adversarial evaluation.

## Evidence

- This note does not import benchmark scores or claim local reproduction.
- Benchmark results do not establish complete attack coverage, deployed robustness, safe authority handling, or system safety.

## Failure Modes

- Treating a benchmark defense as universal prompt-injection resistance.
- Ignoring tool authority, distribution shift, and evaluator limitations.

## Book Chapters Supported

- `security-kernel-and-digital-scifs`
- `runtime-adapters-tool-permissions-and-human-approval`
- `benchmark-ratchets-and-anti-goodhart-evidence`
- `adversarial-evaluation-sandbagging-and-training-time-deception`

## Claims To Add Or Update

- Use as a comparator for adversarial tool-use evaluation while requiring explicit local fixtures and residuals.

## Open Questions

- Which threat classes can a public-safe local fixture cover without implying benchmark completeness?
