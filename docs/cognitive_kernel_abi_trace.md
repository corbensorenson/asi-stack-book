# Cognitive Kernel ABI finite trace receipt

Status: validated local finite transition-and-consumer trace; no chapter-core
support transition.

## What ran

`AsiStackProofs.ReplaceableCognitiveSubstrates` defines one substrate-neutral
control-plane transition relation over proposal, commit, migration, and
revocation events. Kernel family is data rather than control authority. The
model preserves the authority ceiling and exact checkpoint schema/digest across
every accepted step and arbitrary accepted finite traces. It separates proposal
events from receipt-bearing material-effect commits, rejects revoked actors and
targets, rejects incompatible migration, and retains fallback, evaluator,
assistance, lifecycle-cost, evidence-transition, residual-owner, and rollback
custody.

The same Lean module now models an authored six-field heterogeneous continuation
state. It proves that projecting this state to only a common schema and digest
is non-injective, that no decoder from that projection recovers every modeled
state, and that the declared full encoding round-trips and is injective.

The independently encoded Python consumer does not parse or invoke Lean. It
replays `experiments/cognitive_kernel_abi/corpus/2026-07-15.json` and checks:

- one accepted nine-event route through Transformer, selective state space,
  KAN, revocation, and selective-state-space fallback;
- fifteen expected-invalid cases;
- exactly two receipt-bound committed effects and zero proposal effects; and
- twelve event mutations, all rejected;
- four independently reconstructed omitted-state collisions under the common
  checkpoint projection; and
- mutations to all six declared full-checkpoint fields, all rejected.

The stored result is
`experiments/cognitive_kernel_abi/results/2026-07-15-local.json`. Its corpus
SHA-256 is
`32f541e8ef5c06ed8efeaeadde3f0e3b7690ccdf2388d973b04f56946b2aec9e` and
its Lean-model SHA-256 is
`74ee4204a79acaeb030fb704fa5ff0f664b76d13810b1e94b330a558ce89bcf8`.

Run:

```bash
lake -d lean build
python3 scripts/validate_cognitive_kernel_abi_trace.py
```

## Adjudication

This closes the chapter's post-activation formal target at a finite ABI-record
scope. It is useful because the same governed control plane admits a mixed
family route without granting a kernel direct effect or promotion authority.
It does not show that any listed architecture is capable, competitive, safe,
or even executable through a real shared ABI. The full encoding is complete
only by definition over the six fields modeled here; it does not establish a
causally complete state inventory for any implementation.

The support-state effect is exactly `none`.

## Non-claims

- No Transformer, Mamba, KAN, recurrent model, or program synthesizer was run.
- No model, optimizer, scheduler, RNG, cache, backup, adapter, online-memory,
  or descendant state was translated or restored.
- No evaluator-independence, rollback-efficacy, benchmark, architecture-quality,
  deployment, transfer, architectural-RSI, AGI, or ASI claim follows.
