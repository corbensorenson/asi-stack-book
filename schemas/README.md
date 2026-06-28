# Schemas

Public JSON Schemas for book protocols, records, and the manifest contract.

These schemas are starting points for executable validation. They should track the protocol appendix, chapter claims, and `book_structure.json` shape.

Run:

```bash
python3 scripts/validate_schemas.py
python3 scripts/validate_protocol_examples.py
python3 scripts/validate_book.py
```

`validate_schemas.py` checks the schema files themselves. `validate_protocol_examples.py` checks valid example records under `tests/fixtures/protocol_records/` against their matching schemas. `validate_book.py` checks `book_structure.json` against `schemas/book_structure.schema.json` before running the semantic book validators.
