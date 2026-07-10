# Source Note: Interledger Protocol V4

| Field | Value |
|---|---|
| Source ID | `ext_interledger_protocol_v4` |
| Source title | Interledger Protocol V4 |
| Ingestion date | 2026-07-10 |
| Source version / URL | IL-RFC-27, https://interledger.org/developers/rfcs/interledger-protocol/ |
| Citation label | Interledger (2026), Interledger Protocol V4 |
| Published / updated | Versioned RFC / inspected 2026-07-10 |
| Ingestion basis | Official protocol documentation inspected for packetized value transfer across independent ledgers, connector roles, account/balance obligations, neutrality, interoperability, and end-to-end boundary design. No ASI Stack payment, connector, account, settlement, or economic workflow ran. |

## Thesis

ILPv4 is a narrow interoperability protocol for routing packets of value across
independent ledgers through connectors. It is a useful model for separating
cross-network value movement from application-layer policy, but it does not
settle whether a transfer is authorized, fair, lawful, final, or beneficial.

## Mechanisms

- Route packets of value across ledgers that need not share a provider,
  currency, or implementation.
- Track obligations through bilateral accounts and balances between peers.
- Keep the core protocol narrow and place features not required by connectors at
  sender/receiver edges under the end-to-end principle.
- Permit higher-level protocols to add quoting, chunking, and other transfer
  behavior without making them an implicit property of the core route.

## Evidence

- The official documentation specifies the stated packet, connector, account,
  balance, and layered-boundary concepts.
- It does not establish payment settlement, a local economic exchange, legal
  transfer, fairness, delegated authority, or an ASI Stack resource result.
- This repository has not sent, received, routed, settled, or reconciled an ILP
  packet or account.

## Failure Modes

- Treating a routed packet or connector acknowledgement as settlement,
  authorization, correct accounting, or legitimate consideration.
- Allowing a remote agent to bind a local principal to value transfer without a
  separate consent, scope, budget, and approval record.
- Hiding fees, exchange assumptions, dispute paths, residual obligations, or
  failure outcomes behind an aggregate payment-success label.
- Treating protocol neutrality as a solution to policy, fairness, or safety.

## Book Chapters Supported

- `inter-stack-protocols-identity-and-economic-exchange` (Inter-Stack Protocols, Identity, and Economic Exchange)

## Claims To Add Or Update

- Use ILPv4 as a scoped comparator for packetized cross-network value exchange,
  connector obligations, and an end-to-end separation between transport and
  application policy.
- Require economic exchange records to retain principal, scope, budget,
  consideration, receipt, failure, dispute, residual, and revocation context.
- Do not claim local payment, accounting, settlement, delegated authority,
  fairness, legality, or safety.

## Open Questions

- What minimum public-safe exchange fixture can distinguish an authorized
  reserved budget from a settled, disputed, refunded, or failed transfer?
- Which ownership layer handles economic residuals that outlive a remote task or
  revoked delegation?
