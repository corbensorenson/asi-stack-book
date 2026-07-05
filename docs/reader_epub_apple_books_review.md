# Reader EPUB Apple Books Review

Generated validation command:

```bash
python3 scripts/validate_reader_epub_apple_books_review.py
```

Status: `passed_apple_books_epub_application_review`

Reviewed artifact: `build/curated_reader_edition/format_artifacts/epub/_reader_site/The-ASI-Stack.epub`

Reviewed artifact SHA-256: `0cde00ffdb070b12884ae1d7400c4e7dcc4321e0141956c5d9d89b434463fbda`

Application path: Apple Books (`com.apple.iBooksX`) on macOS.

## What Was Checked

- Apple Books imported or retained The ASI Stack in the local Books library and opened it into a reader window.
- Chapter 1 rendered without the earlier XML error banner.
- A page advance rendered the ASI Stack control-plane figure, caption, figure-boundary text, and the next section heading.
- The Apple Books table-of-contents popover opened and listed front matter, chapter 1, and chapter 1 section entries with page targets.
- The package-level EPUB audit records zero XML parse errors, zero bare class attributes, zero paragraph-wrapped figure tags, zero unresolved internal hrefs, and zero live-marker or raw core-claim marker leaks.
- The browser EPUB review records 104 page-view pairs with zero failed pairs.
- The key-figure EPUB layout review records 20 key-figure page-view pairs with zero failed pairs.

## Repair Notes

The first Apple Books attempt found a real EPUB/XHTML failure: a bare `class`
attribute on generated figure tags. After that was repaired, Apple Books found a
second XML failure: paragraph-wrapped figure tags such as `<p><figure></p>`.
The repair path now removes bare class attributes, unwraps paragraph-wrapped
figure tags, adds EPUB-only overflow and inline-code wrapping CSS, and the
content audit parses every XHTML entry as XML.

The current reviewed artifact has zero XML parse errors.

## Release Effect

This clears only `app_or_ereader_review_not_completed` for the current repaired
curated EPUB/e-reader application path. It does not approve the curated reader
edition, does not approve EPUB publication, does not publish or archive an
artifact, does not create an edition release record, does not approve audio, and
does not promote any claim support state.

Boundary phrase for validator stability: this review does not approve the curated reader edition.

## Residuals

- `reader_release_approval_not_created` remains active.
- `reader_release_record_not_created` remains active.
- DOCX application review or an explicit release decision remains open.
- Manual keyboard-only review, screen-reader review, and WCAG conformance review remain open unless scoped out by a later release decision.
- Audio narration, timecoding, files, and audio release records remain open.
