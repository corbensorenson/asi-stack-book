# Proof lookup by application terms

The revised proof catalog returned all four clues from the earlier application reader’s first batch. The previous catalog returned a determining declaration for three clues and returned no match for the finite selector. The revised catalog contains all ten indexed declarations in 4,704 bytes. The exact minimum-cost packet now also quotes the Reader’s limits on cost calibration, measured efficiency and workload coverage. These checks concern the earlier observed miss. [Batch replay](batch-replay.json) · [Live verification](live-verification.json)

Two fresh readers, one per edition, each earned all 12 rubric points on four new application questions. The updated reader used seven opens instead of nine and 1.6% fewer deduplicated bytes. Each reader used one catalog open. Neither used a chapter directory, per-volume index, or full HTML page. [Frozen protocol](protocol.md) · [Scores](scores.json)

| Measure | First proof lookup | Proof lookup with application terms |
|---|---:|---:|
| Quality points | 12/12 | 12/12 |
| Unsupported numerical claims | 0 | 0 |
| Resource opens | 9 | 7 |
| Proof catalog opens | 1 | 1 |
| Separate chapter or Reader section opens | 2 | 0 |
| Deduplicated bytes | 307,190 | 302,221 |
| Displayed bytes | 29,573 | 24,903 |

The reader on the first edition opened the exact Unit 2 and Unit 8 sections. The updated reader cited those sections from the proof packet context. Both used the exact declaration exports. Only the finite selector packet gained a second application paragraph. The fresh pair showed no catalog retries in either edition. The replay of the earlier clues isolates the lookup change that addresses that session’s repeat-read trigger. [First edition journal](application-baseline-opens.json) · [Updated journal](application-candidate-opens.json)

The comparison used tested bundles for `9f84414d` and `c833ed9f`, and fresh Codex CLI 0.171.0-alpha.13 sessions with gpt-6.1-sol at high reasoning effort. One reviewer applied the frozen rubric with edition labels visible. Bytes count distinct uncompressed payloads per session. This single pair checks the new application questions. [First matched test](../proof-lookup-2026-11-28/results.md) · [Build identities](suite.json) · [Offline replay](replay-suite.json)
