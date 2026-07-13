# Source Note: in-toto: Providing farm-to-table guarantees for bits and bytes

| Field | Value |
|---|---|
| Source ID | `ext_in_toto_2019` |
| Source title | in-toto: Providing farm-to-table guarantees for bits and bytes |
| Ingestion date | 2026-07-10 |
| Source version / URL | USENIX Security 2019, https://www.usenix.org/conference/usenixsecurity19/presentation/torres-arias |
| Citation label | Torres-Arias et al. (2019), in-toto |
| Published / updated | 2019-08 / 2019-08 |
| Ingestion basis | Full primary USENIX paper reviewed for its signed layout, functionary/link metadata, material/product inspection, role and threshold model, partial key-compromise analysis, deployment cases, overhead evaluation, historical-incident comparison, and stated integration dependencies. No local in-toto layout, attestation, or verification run was performed. |

## Thesis

in-toto lets a project owner declare and sign the required software-supply-chain
layout, lets authorized functionaries sign link metadata describing the
materials and products of each step, and lets a client verify that the delivered
artifact followed the declared chain. Its security properties degrade according
to which keys and thresholds are compromised rather than following a universal
“one valid signature means safe” rule.

## Mechanisms

- A project owner signs the layout: expected steps, authorized functionaries,
  thresholds, artifact rules, and inspection commands.
- Functionaries record authenticated link metadata over step materials and
  products; human and automated functionaries are both supported.
- Clients match signed link metadata to the layout and delivered product rather
  than checking isolated signatures without the intended process.
- Delegation, role separation, and thresholds limit the consequences of some
  individual key compromises; the security result depends on the concrete
  layout and key assignment.
- TUF or another last-mile mechanism remains relevant for bootstrapping trust,
  freshness, rollback protection, and metadata distribution; in-toto does not
  silently absorb those properties.
- The paper evaluates three deployment styles and analyzes how their different
  layouts and threshold choices would respond to historical compromises.

## Evidence

- The paper reports a Datadog deployment evaluation in which in-toto metadata
  accounted for about 19% of the mirrored repository size under the described
  configuration, with possible reductions from different tracking/signature
  choices, and adds less than 0.6 seconds of verification time in its reported
  package cases.
- It analyzes 30 historical supply-chain incidents against three deployments;
  the paper reports that the concrete layouts would have addressed different
  fractions, with threshold and last-mile choices explaining much of the
  difference. This is retrospective configuration-specific analysis, not a
  universal prevention rate.
- The paper explicitly models partial degradation under key compromise and
  shows why the identity of the compromised role matters.
- Valid attestations still do not establish artifact correctness,
  uncompromised authorized actors, model safety, data fitness, confidentiality,
  or deployment merit. No model-weight custody or ASI Stack result is reported.

## Failure Modes

- Assuming signed authorized steps are complete or trustworthy in their surrounding environment.
- Treating supply-chain verification as a substitute for model evaluation or governance review.
- Omitting an artifact or transformation from the layout and then interpreting
  successful verification as coverage of the omitted path.
- Using weak threshold/key assignments that allow one compromised functionary
  to satisfy a security-critical step.
- Treating historical-incident counterfactual analysis as a live penetration
  test or proof against novel attacks.
- Ignoring trust-bootstrap, freshness, rollback, mix-and-match, and last-mile
  dependencies that the deployment supplies through other systems.

## Book Chapters Supported

- `model-weight-custody-and-hardware-roots-of-trust`
- `ai-supply-chain-integrity-and-lifecycle-provenance`
- `artifact-graphs-audit-logs-and-replay`

## Claims To Add Or Update

- Use as a comparator for project-owner layouts, functionary link metadata,
  material/product matching, role separation, thresholds, and consumer-side
  lifecycle verification.
- Preserve the distinction between authorized-step evidence and artifact
  correctness, confidentiality, model safety, custody authority, or release
  merit.
- For weight custody, use it to show that a signature is consumer-bound evidence
  about an artifact path, not a substitute for key-release policy, environment
  attestation, load observation, or irreversible-release authority.

## Open Questions

- How should the book distinguish an authorized lineage step from a verified-safe model or data artifact?
- Which model-training and packaging steps belong in a weight-specific layout,
  and which derivative artifacts remain outside a tractable closure?
- How should functionary-key compromise, threshold quality, freshness, and
  last-mile dependencies be represented in custody residuals?
