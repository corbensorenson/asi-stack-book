# Living-Book Change-Packet Harness

Last updated: 2026-07-02

This harness checks synthetic records for the living-book change-packet concept
described in the Living Book Methodology chapter. A change packet is the
auditable unit of book progress: it names what changed, which surfaces moved,
which checks ran, what release or audience surface was affected, and what the
change does not imply.

## Record Shape

The schema is `schemas/living_book_change_packet.schema.json`.

Required fields include:

- `packet_id`
- `packet_type`
- `source_commit`
- `changed_chapters`
- `changed_sources`
- `changed_claims`
- `proof_tags`
- `schema_or_fixture_paths`
- `validation_commands`
- `validation_status`
- `render_result`
- `release_target`
- `audience_profiles`
- `derived_artifact_boundary`
- `support_state_effect`
- `evidence_transition_refs`
- `changelog_refs`
- `public_url`
- `residuals`
- `non_claims`

## Harness Checks

`python3 scripts/validate_living_book_change_packets.py` checks that:

- packet IDs use the `change-packet://` identity prefix;
- public-surface changes name changelog refs;
- passing packets name validation commands;
- render-pass packets name a render or live-view validation command;
- reader/audio derivative targets state a derived, non-equal-authority or
  non-approval boundary;
- promotion-eligible support effects name evidence-transition refs, and upward
  transitions name an accepted evidence-transition ref;
- blocked, partial, pending, or failed packets preserve residuals;
- every packet carries explicit non-claims.

## Current Local Result

The 2026-07-02 local run passed:

```text
Living-book change-packet harness passed: 3 valid fixture(s), 6 expected-invalid fixture(s).
```

The result record is
`experiments/living_book_change_packets/results/2026-07-02-local.md`.

## Boundary

This is a synthetic publication-governance fixture. It makes the change-packet
concept executable at the record level. It does not approve a release, reader
artifact, EPUB, PDF, DOCX, audio artifact, source interpretation, manuscript
quality, editorial quality, live-site availability, support-state promotion, or
future-agent correctness.
