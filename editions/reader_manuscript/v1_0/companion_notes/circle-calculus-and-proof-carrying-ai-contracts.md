# Circle Calculus Companion Note

Status: drafting companion note, not release reviewed.

Chapter: `circle-calculus-and-proof-carrying-ai-contracts`

Routing record: `editions/reader_manuscript/v1_0/companion_note_routing.json`

Primary reader source: `build/reader_edition/chapters/circle-calculus-and-proof-carrying-ai-contracts.qmd`

Evidence references: `docs/circle_external_receipt_slice.md`,
`docs/circle_public_replay_consumer_gate.md`,
`experiments/circle_public_replay/fixtures/valid/circle_rope_receipt.consumer.valid.json`,
`scripts/validate_circle_public_replay.py`, and
`AsiStackProofs.ProofCarryingContracts`.

This note helps e-reader and audio review for the Circle proof-contract chapter.
It does not replace the chapter prose. Meaning-critical limits must still stay
in the reader spine: proof authority is not model-quality authority, workload
evidence is still required before downstream promotion, and stale or unreplayed
proof references remain residual.

## Reader Promise

After reading or hearing this companion note, a human should be able to follow
the chapter's receipt vocabulary without mistaking a theorem-linked structural
receipt for evidence that an AI model became better, safer, faster, longer
context, or more deployable.

## Quick Glossary

| Term | Plain meaning | Boundary |
|---|---|---|
| Proof receipt | A record that carries a finite structural fact, theorem references, deterministic fields, validation commands, and non-claims. | It can carry a narrow structural boundary; it does not prove broad behavior. |
| Theorem-linked receipt | A receipt that names theorem IDs and proof-status scope. | The theorem reference must still resolve or remain residual. |
| Dictionary-bound | The finite model is tied to a recognized contract family or engineering object. | Naming the family does not prove the model is useful. |
| Fingerprinted | Content, request, pack, receipt, or contract fields have recorded hashes. | A fingerprint makes drift detectable; it does not prove quality. |
| Resolver-checked | A stated command has checked whether theorem references or receipt fields resolve. | Resolution is structural evidence only unless a downstream claim has its own evidence. |
| Consumer-gated | Allowed and blocked downstream uses are recorded before another layer consumes the receipt. | A receipt accepted for one consumer does not automatically transfer to another. |
| Workload-blocked | Workload, baseline, metric, or evidence artifacts are missing. | No model-quality, runtime, memory, context-length, transfer, safety, or ASI claim is allowed. |
| Retired or superseded | The receipt is stale, replaced, contradicted, or no longer current. | Historical context only unless a later review requalifies it. |
| Theorem laundering | Repeating a narrow formal result as if it proved a broader capability or deployment claim. | This is a failure mode, not a valid evidence move. |

## The Circle Fixture In One Page

The current public ASI-side Circle lane validates one pinned receipt fixture:
`circle.rope.CC-AI-CONTRACT-ROPE-001.public_consumer_gate`.

The fixture concerns the contract family `rope_position_distinguishability` and
the engineering object `CC-AI-CONTRACT-ROPE-001`. It records seven required
theorem IDs, deterministic fields such as `d19_proved_request_status=proved`,
and pinned fingerprints for contract, receipt, request, and contract-pack
content. The validator is `python3 scripts/validate_circle_public_replay.py`.

That validator checks the accepted fixture and rejects four mutation controls:
digest mismatch, missing required theorem ID, stale contract fingerprint status,
and unsupported transfer-claim use in the consumer gate.

The local Lean bridge models the same public consumer-gate boundary as a finite
fixture: one accepted receipt, four rejected mutation controls, seven required
theorem IDs, pinned digest fields, blocked support movement, no chapter-core
promotion, and no deployed-transport claim. It is a boundary proof over the ASI
Stack record shape, not a replay of the external Circle proof stack.

The allowed use is structural proof-contract receipt discussion and future
consumer-fixture design. The blocked uses include chapter-core claim promotion,
model-quality promotion, runtime promotion, context-length promotion,
deployment-readiness claims, transfer claims, and ASI claims.

## Audio Treatment

In an audio script, do not read every receipt field as a long list unless the
release reviewer explicitly wants an appendix-style narration. The spoken path
should say:

- the receipt names a finite structural fact;
- theorem IDs and fingerprints make the fact checkable and drift-visible;
- the consumer gate says where the receipt may and may not be used;
- workload-blocked means no capability promotion is allowed;
- the chapter remains at architectural-argument support for its core claim.

The detailed theorem IDs, fingerprints, and receipt fields can be routed to this
companion note while the main audio keeps the proof-versus-performance boundary
clear.

## Non-Claims

- This companion note is not a reader release record.
- This companion note is not an EPUB, PDF, DOCX, HTML, MP3, M4B, or
  audio-embedded EPUB artifact review.
- This companion note does not promote any chapter core claim above `argument`.
- This companion note does not claim local replay of external Circle proofs
  from this repository.
- This companion note does not claim that the local Lean bridge proves the
  external Circle contracts, resolves theorem IDs from local artifacts, vendors
  a public Circle pack, or validates deployed proof-contract transport.
- This companion note does not prove model quality, reasoning ability, context
  length, speed, memory scaling, deployment safety, transfer, or ASI.
- This companion note does not make curated reader prose equal authority beside
  the live AI/research book.
