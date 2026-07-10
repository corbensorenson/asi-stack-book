# Source Note: NIST Cybersecurity Supply Chain Risk Management

| Field | Value |
|---|---|
| Source ID | `ext_nist_cscrm_2022` |
| Source title | Cybersecurity Supply Chain Risk Management Practices for Systems and Organizations |
| Ingestion date | 2026-07-10 |
| Source version / URL | NIST SP 800-161r1-upd1, May 2022, https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-161r1-upd1.pdf |
| Citation label | NIST (2022), SP 800-161r1 |
| Published / updated | 2022-05 / 2022-05 |
| Ingestion basis | Primary NIST standard inspected for its supply-chain definition, risk framing, lifecycle scope, supplier/component inventory, assessment, response, monitoring, incident communication, and tailoring limits. No ASI Stack supply-chain program, supplier review, artifact inventory, incident exercise, or control assessment ran. |

## Thesis

Cybersecurity supply-chain risk management is a lifecycle-wide, context-tailored
process for identifying, assessing, responding to, and monitoring risk arising
from suppliers, components, products, services, and their linked processes. It
requires explicit governance and risk decisions; it is not a guarantee that a
supply chain or its artifacts are safe.

## Mechanisms

- Maintain supply-chain and component/supplier information across research,
  design, acquisition, delivery, integration, operations, and disposal.
- Integrate risk framing, assessment, response, and monitoring with accountable
  organizational decision processes rather than treating procurement as a
  one-time security event.
- Keep incident and stakeholder communication paths available for risk that
  appears after an artifact has been acquired or deployed.
- Tailor controls to the operational context, criticality, threat, vulnerability,
  policy, and risk-tolerance assumptions that make a risk decision meaningful.

## Evidence

- The standard defines supply-chain scope as linked resources and processes
  spanning a product or service life cycle and provides C-SCRM practices at its
  stated scope.
- It is not AI-specific implementation evidence and does not prescribe a
  complete ASI model/data/code lineage graph.
- This repository has not performed a supplier assessment, supply-chain risk
  assessment, incident exercise, vulnerability review, component inventory, or
  lifecycle control evaluation.

## Failure Modes

- Treating a supplier name, inventory, or policy document as evidence that a
  component is secure or suitable.
- Leaving upstream advisories, changes, and incidents disconnected from
  downstream artifact or release decisions.
- Applying a generic control list without a scoped threat, criticality, owner,
  risk response, or monitoring plan.
- Confusing cybersecurity supply-chain process with model safety, data fitness,
  legal compliance, deployment authorization, or ASI.

## Book Chapters Supported

- `ai-supply-chain-integrity-and-lifecycle-provenance` (AI Supply-Chain Integrity and Lifecycle Provenance)

## Claims To Add Or Update

- Use this note for lifecycle, risk-framing, supplier/component, assessment,
  response, monitoring, incident, and disposal vocabulary.
- Keep supply-chain status separate from artifact correctness, absence of
  compromise, data quality, model safety, readiness, authority, and ASI.
- Do not claim local C-SCRM conformance, supplier trustworthiness, inventory
  completeness, incident-response effectiveness, or artifact integrity.

## Open Questions

- Which AI-specific artifact, data, training, build, deployment, and derivative
  relationships must be included in a public-safe supply-chain record?
- How should a downstream model's affected scope and re-review route be updated
  when a dependency, dataset, signer, supplier, or advisory changes?
- What independent evidence would be needed before a narrow supply-chain
  integrity claim could move beyond architecture rationale?
