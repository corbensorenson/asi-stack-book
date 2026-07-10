# Landing Visual Review — 2026-07-10

Review state: local rendered-page inspection, not an independent editorial or
accessibility review.

The landing page was inspected from a clean 67-page Quarto render at a
1280×720 browser viewport after the canonical-status and release-channel build.
The document and viewport widths both measured 1280 pixels, so the page had no
horizontal overflow. The title/subtitle, author, reading-mode control,
generated status block, introductory sentence, hero, sidebar, and table of
contents were readable with stable spacing and contrast.

The inspection identified one information-architecture issue: the product
selector began about 1,257 pixels from the document top, below the hero and
status dashboard. It was moved directly after the one-sentence introduction
and before the hero so narrative, architecture-reference, and evidence-registry
routes are available in the first reading sequence. Dense transition IDs,
theorem IDs, hashes, and fixture detail remain in their owning ledgers rather
than on the landing surface.

After the clean re-render, DOM geometry placed the selector heading at 497 px
and the hero at 875 px while document and viewport widths still agreed at
1280 px. The selector is therefore present within the first 720 px viewport
instead of beginning below the second screen.

The page still carries a long research-book sidebar because the live book is
one of the three products. Human view hides research scaffolding inside
chapters; it does not turn the live navigation into a reviewed standalone
reader artifact. The external systems/editorial packet and reader-release
gates remain open.

This review does not establish mobile, screen-reader, keyboard, contrast,
reader-release, publication, or independent editorial approval beyond the
separate automated and tracked records.
