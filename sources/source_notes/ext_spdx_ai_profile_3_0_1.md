# Source Note: SPDX 3.0.1 AI Profile

| Field | Value |
|---|---|
| Source ID | `ext_spdx_ai_profile_3_0_1` |
| Source title | SPDX Specification 3.0.1 AI Profile |
| Ingestion date | 2026-07-10 |
| Source version / URL | SPDX 3.0.1 AI Profile, https://spdx.github.io/spdx-spec/v3.0.1/model/AI/AI/ |
| Citation label | SPDX (2024), Specification 3.0.1 AI Profile |
| Published / updated | 2024-12 / 2024-12 |
| Ingestion basis | Official SPDX specification and conformance material inspected for its AI/model, dataset, build, supplier, provenance, integrity, relationship, and lifecycle metadata scope. No ASI Stack AI BOM, SPDX document, inventory export, conformance check, or provenance audit ran. |

## Thesis

SPDX 3 provides an interoperable data model for Bills of Materials spanning
software, AI artifacts, datasets, builds, suppliers, provenance, integrity,
relationships, and lifecycle information. A BOM is a structured description and
exchange format; its presence or conformance does not prove completeness,
security, data fitness, model behavior, legal compliance, or deployment merit.

## Mechanisms

- Model AI packages, datasets, software components, build information, supplier
  identities, provenance, integrity methods, relationships, and lifecycle data
  as typed, interoperable elements.
- Exchange BOM information through defined serialization and profile-conformance
  points rather than relying only on unstructured vendor statements.
- Use relationships to express composition and dependency context across an AI
  system instead of reducing the system to one model file.
- Allow AI-profile information to interoperate with related build, dataset,
  security, licensing, and extension information without claiming that every
  profile or field is present.

## Evidence

- The official specification defines an AI profile and an extensible BOM model
  that covers the stated data categories and relationship structures.
- Profile conformance is a data-exchange condition, not evidence that an
  inventory is complete or that listed components are trustworthy.
- This repository has not produced, imported, validated, exchanged, or audited
  an SPDX AI document or an AI system Bill of Materials.

## Failure Modes

- BOM theater: a syntactically valid inventory omits important data, model,
  build, dependency, supplier, prompt, hardware, or derivative relationships.
- A listed component's identity or license is mistaken for security, fitness,
  safety, or legal clearance.
- A BOM is not refreshed after a dependency, dataset, signing, training, build,
  configuration, advisory, or distribution change.
- AI-profile interoperability is overstated as a local conformance, complete
  system inventory, artifact integrity, or deployment result.

## Book Chapters Supported

- `ai-supply-chain-integrity-and-lifecycle-provenance` (AI Supply-Chain Integrity and Lifecycle Provenance)

## Claims To Add Or Update

- Use this note for AI BOM, typed artifact, dataset/build/supplier relationship,
  provenance, integrity, lifecycle, and interoperability vocabulary.
- Keep BOM presence and profile conformance separate from inventory completeness,
  artifact security, data fitness, model safety, legal compliance, readiness,
  authority, and ASI.
- Do not claim a local AI BOM, SPDX conformance, complete supply-chain graph,
  component inventory, provenance audit, or deployment approval.

## Open Questions

- Which ASI Stack record fields map cleanly to interoperable BOM fields and
  which require a separate governance extension?
- How should a BOM record connect to revocation, residual ownership, affected
  releases, and re-review without becoming an unauthorized decision engine?
- What independent review would be needed to distinguish a complete enough
  inventory for one purpose from a merely well-formed document?
