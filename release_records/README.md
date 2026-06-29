# Release Records

This directory contains public-safe records for rendered, validated live-book releases and future major-version edition releases.

Each `*.json` file is validated by:

```bash
python3 scripts/validate_protocol_examples.py
```

Records without `record_type: "edition_release"` use `schemas/living_book_release_record.schema.json`. Records with `record_type: "edition_release"` use `schemas/edition_release_record.schema.json`.

The validation checks record shape only. It does not prove manuscript quality, claim truth, source interpretation, benchmark validity, artifact render success, narration quality, or finality.

Major-version living-book release records may be committed after the tagged
source state they describe. In that case, `source_commit` names the exact
validated tag commit, while the record commit is a post-tag control update that
publishes the release facts, residuals, and non-claims.
