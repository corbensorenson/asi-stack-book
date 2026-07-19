# P4/M8 Campaign 6 — KERC Canonical Language and Hierarchical Residual Runtime

## Terminal outcome

The campaign was frozen before outcomes with 192 authored bilingual records,
128 training records, 32 ordinary held-out records, 32 adversarial held-out
records, five seeds, eight baseline families, thirteen mechanism ablations, and
twenty state/authority attacks. It implemented all three planned slices: exact
object handles and shared terminology; semantic, faithful, and lossless packet
paths; and a small Kernel-native linear core compared with surface-unigram,
byte, dynamic-chunk, and simple-handle cores.

The broad efficiency claim is **refuted on this campaign**. Kernel, surface,
and simple-handle cores all achieved `0.500000` mean held-out intent-plus-
polarity accuracy because the adversarial polarity class was absent from the
training partition. The complete Kernel packet averaged `714.0` bytes versus
`73.25` bytes for the best simple total-description representation. The
32.625-byte Kernel string therefore cannot be reported as a system saving:
packet, objects, residuals, hashes, and migration metadata dominate it. Energy
was not calibrated, so there is no energy result.

Two narrower finite findings survive. Protected-object recall and lossless
byte recovery were both `1.000000` over 64 held-out records, while removing
protected-span capture reduced object recall to zero. A deliberately simple
shared-glossary byte calculation crossed its isolated byte break-even at two
turns. That calculation excludes semantic failures, privacy, migration,
monitoring, governance, and model costs; it is not an end-to-end efficiency
result.

The security boundary is negative. The rule-owned policy handled 19 of 20
finite attack cases, but allowed the quote/object escape string. The compiler
and verifier were authored together, the language coverage was templated
English and Spanish, several residual layers duplicated top-level object data,
and removing sense compilation was masked by intent words embedded in exact
URLs. These are retained instrument and construct-validity weaknesses, not
post-hoc repair invitations.

## Claim and chapter disposition

- `kerc.broad_matched_total_system_efficiency` is `refuted` for this exact
  implementation and corpus.
- `kerc.protected_exact_handle_preservation` and
  `kerc.interaction_shared_glossary_break_even` are accepted only as bounded
  `synthetic-test-backed` non-core findings.
- Security, multilingual transfer, independent semantic validity, model
  transfer, production efficiency, and energy remain blocked.
- No chapter core moves above `argument`, and the new-chapter gate fails. The
  observed interfaces remain owned by Cognitive Compilation, Compact
  Generative Systems, Virtual Context, Context Transactions, Verification
  Bandwidth, Fast Generation, Replaceable Cognitive Substrates, Resource
  Economics, Security Kernel, Procedural Memory, Benchmark Ratchets, and the
  Integrated Reference Architecture.

Canonical records are
`experiments/p4_kerc_runtime/design.json`,
`experiments/p4_kerc_runtime/preregistration.json`,
`experiments/p4_kerc_runtime/raw/campaign_run.json`, and
`experiments/p4_kerc_runtime/results/confirmatory_result.json`. The validating
command is `python3 scripts/validate_p4_m8_kerc_campaign.py`.

This local campaign does not establish general semantic preservation,
independent verifier validity, security, multilingual fairness, model or domain
transfer, production or energy efficiency, SOTA, AGI, ASI, deployment
readiness, publication authority, release authority, or chapter-core support.
