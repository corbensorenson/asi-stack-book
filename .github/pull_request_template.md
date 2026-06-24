## Scope

Briefly describe the change.

## Checklist

- [ ] I preserved `book_structure.json` as the structure source of truth.
- [ ] I ran `python3 scripts/sync_scaffold.py` after structure or generated appendix changes.
- [ ] I ran `python3 scripts/sync_proof_manifest.py` after proof-tag changes.
- [ ] I did not publish raw/private source exports.
- [ ] I did not fabricate source content, citations, proof results, benchmark results, or test results.
- [ ] I updated `appendices/F_changelog.qmd` for meaningful changes.
- [ ] I ran `python3 scripts/validate_publication.py`.
- [ ] I ran `python3 scripts/validate_book.py`.
- [ ] I ran `python3 scripts/validate_schemas.py`.
- [ ] I ran `quarto render --to html`.
- [ ] I ran `lake build` if Lean files changed.
