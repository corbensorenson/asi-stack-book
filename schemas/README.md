# Schemas

Public JSON Schemas for book protocols and records.

These schemas are starting points for executable validation. They should track the protocol appendix and chapter claims.

Run:

```bash
python3 scripts/validate_schemas.py
python3 scripts/validate_protocol_examples.py
```

`validate_schemas.py` checks the schema files themselves. `validate_protocol_examples.py` checks valid example records under `tests/fixtures/protocol_records/` against their matching schemas.
