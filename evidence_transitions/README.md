# Evidence Transitions

This directory stores reviewed evidence-transition records for the living book.

Each record must validate against `schemas/evidence_transition_record.schema.json` and must not promote a support state unless the corresponding evidence transition is accepted and the canonical claim matrix is updated. A no-change record is useful when review finds that a claim should stay at `argument`.

Generated fixtures under `tests/fixtures/protocol_records/` demonstrate schema shape only. Records here are project review records and belong in changelogged roadmap work.

