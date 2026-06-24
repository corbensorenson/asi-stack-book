# Release Records

This directory contains public-safe records for rendered, validated live-book releases and future major-version edition releases.

Each `*.json` file is validated by:

```bash
python3 scripts/validate_protocol_examples.py
```

Records without `record_type: "edition_release"` use `schemas/living_book_release_record.schema.json`. Records with `record_type: "edition_release"` use `schemas/edition_release_record.schema.json`.

The validation checks record shape only. It does not prove manuscript quality, claim truth, source interpretation, benchmark validity, artifact render success, narration quality, or finality.
