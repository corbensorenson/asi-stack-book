# Model-adequacy dossier: Hive lifecycle refinement

## Decision

Adequate for one finite authored policy-to-closure Hive lifecycle and its typed failure routes. Inadequate for distributed execution, partition tolerance, authority-service correctness, useful work, or transfer.

## Reachable model

Seven reachable stages preserve exact job, principal, contract, registry, candidate-set, selected-node, policy, authority, lease, evaluator, consumer, and residual identity. Forty-seven routes cover policy, denominator, least-authority, locality, budget, energy, dropout, federation, sandbox, approval, partition, receipt, useful-outcome, residual, recovery, revocation, descendant, acknowledgment, replay, and authority-leak failures.

## Countermodels and consumer

Seventeen refinement declarations include identity/effect invariants, thirteen concrete countermodels, and one closed witness. The independent consumer rejects 53/53 mutations and reruns the two inherited suites exactly.

## Assumptions, exclusions, and adequacy verdict

The model trusts all authored policy, authority, lease, partition, denial, receipt, outcome, recovery, revocation, and acknowledgment fields. It does not prove node identity, attestation, policy correctness, network behavior, sandbox enforcement, no-mutation truth, effect truth, useful work, energy accounting, recovery efficacy, privacy, security, availability, or transfer. Support-state effect: exactly `none`.
