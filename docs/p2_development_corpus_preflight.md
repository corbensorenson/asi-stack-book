# P2 Natural Development-Corpus Preflight

Date: 2026-07-17  
State: **qualified for development only; final denominator unselected and closed**

The P2 corpus now has a pinned natural-data candidate rather than an authored
fixture. SWE-rebench V2 revision
`475dd5e8703bb5fb22dd3c60b5d038b019eba1e0` contains 1,117 tasks created after
the pinned local Qwen3-8B snapshot, spanning 532 repositories and 20 languages.
The post-snapshot filter reduces one contamination route; it does not prove contamination absence.

Only compact metadata and content digests are retained. The 409 MiB source
parquet, problem statements, human solution patches, hidden test patches, and
source trees are not vendored. A 12-task **development-only** pool spans 12
public merged pull requests, 12 repositories, and seven languages. All twelve
use permissive licenses, have dataset quality code A with no B1–B6 flags,
separate solution and test paths, accessible GitHub receipts, and resolvable
`linux/amd64` image manifests.

Those screens do not pass the construct or resource gates. The paper itself
documents false-negative risks from setup failure, test coupling, implicit
naming, and external dependencies, while its diagnostic study covers only 300
tasks in five languages. The release also has known missing/mismatched image
reports. Every development task must therefore reproduce the human-gold
fail-to-pass/pass-to-pass transition locally, survive independent specification
review, reject candidate edits to test-patch paths, and expose ordinary and
adversarial governance opportunities. The local arm64 host must measure pull,
expanded disk, emulation, runtime, and cleanup costs.

The final denominator remains unselected and closed. No task text, patch, test,
or outcome from a future final pool is available for debugging. This preflight
creates no benchmark result, competence-qualified empirical transition,
support-state promotion, coding-capability result, governance benefit, safety,
transfer, reproduction, SOTA, release, AGI, or ASI claim.

The subsequent fixed-denominator gold run qualified seven tasks directly and
one more through an independently implemented AVA parser. Four tasks were
terminally classified N0 after bounded rescue exposed compile-label, runtime
external-resource, local-filesystem, or dynamic-dependency incompatibilities.
They cannot be dropped to improve the observed rate: four same-language
replacements must be drawn sequentially under the frozen deterministic policy,
after the resource ceiling is frozen. See
`docs/p2_gold_preflight_diagnosis.md` and
`docs/p2_task_qualification_and_replacement_policy.md`.

Machine records:

- `evidence_quality/p2_development_corpus_preflight.json`
- `experiments/p2_governed_repository_admission/corpus/post_snapshot_eligible_metadata.jsonl`
- `experiments/p2_governed_repository_admission/corpus/development_pool.json`
- `experiments/p2_governed_repository_admission/corpus/image_manifest_receipts.json`
