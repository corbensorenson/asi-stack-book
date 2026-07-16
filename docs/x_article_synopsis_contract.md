# Maintained X Article Synopsis Contract

Status: binding future-derivative contract; artifacts pending P9

Owner: Corben Sorenson

Roadmap authority:
`docs/post_v2_3_claim_proof_and_sota_challenge_roadmap.md`, P9

## Purpose

Maintain one concise public synopsis of *The ASI Stack* for publication as an X
Article. It is a derivative of the evidence-reconciled living book, not an
independent manuscript or a marketing substitute for the book. It must help a
reader understand the architecture, the strongest results, the strongest
failures, what is formally versus empirically supported, and what remains open.

## Canonical future artifacts

- Article source: `editions/x_article/asi_stack_synopsis.md`
- Manifest and staleness record: `editions/x_article/manifest.json`
- Primary header: `editions/x_article/asi_stack_synopsis_header.png`
- Header provenance and alt text: `editions/x_article/header_provenance.json`
- Optional platform fallback: `editions/x_article/asi_stack_synopsis_header.jpg`
- Publication or ready-not-published record:
  `release_records/<date>-x-article-synopsis-disposition.json`

These paths are reserved now. Their absence means P9 is pending; this contract
does not authorize placeholder content, invented results, image generation, or
external publication before the evidence freeze.

## Hard article gates

1. The first visible body line after the X-native title is exactly
   `https://corbensorenson.github.io/asi-stack-book/`.
2. Title, visible body, headings, captions, and footnotes total no more than
   9,999 words. The drafting target is 7,500–9,250 words.
3. Every substantive claim maps to a stable chapter/claim atom, current support
   state, evidence lane, artifact, and book anchor.
4. The article does not strengthen scope, independence, transfer, causality,
   certainty, safety, implementation, or SOTA status beyond the book record.
5. Decisive negative, null, narrowed, refuted, and blocked results are included
   when they change how a reader should understand the stack.
6. Formal theorem, executable conformance, empirical measurement, causal
   intervention, reproduction/transfer, source synthesis, and normative
   argument remain visibly distinct.
7. Repeated definitions, roadmap mechanics, count theater, hype, and details
   that do not change understanding or action are removed.
8. The canonical Markdown source, not the X composer, remains the editable
   source of truth. Any platform formatting delta is recorded.

## Hard header gates

- Exact dimensions: 2000×800 pixels.
- Exact aspect ratio: 5:2.
- Primary format: RGB PNG; JPEG fallback only when the current composer needs
  it.
- Essential content remains in a centered safe region and survives real
  desktop and mobile X preview crops.
- The visual represents a governed, layered AI architecture without implying
  that ASI, universal safety, or beyond-SOTA performance has been achieved.
- Provenance records the design brief or prompt, source/generation tool and
  version, rights state, dimensions, color mode, byte size, SHA-256, alt text,
  preview results, and any platform derivative digest.
- Alt text uses natural sentence structure, describes the image, and does not
  merely repeat the article title.

## X compatibility gate

The current official X help page documents Articles as a Premium-tier feature
that supports links, images, media, headings, lists, formatting, header images,
editing through unpublish/republish, and audience controls. It does not state a
stable Article-body limit or a 5:2 pixel specification. Therefore execution
must re-check the official help and then test the live X composer for:

- account eligibility and selected audience;
- full-body acceptance and rendered word/character behavior;
- top-link visibility and destination;
- heading, list, emphasis, caption, and link preservation;
- PNG/JPEG upload, crop, compression, and desktop/mobile preview;
- alt-text entry and readback; and
- draft, edit/unpublish, and publication behavior that affects maintenance.

Official references checked 2026-07-14:

- `https://help.x.com/en/using-x/articles`
- `https://help.x.com/en/using-x/write-image-descriptions`

The repository's 9,999-word and exact 5:2 rules remain binding even if X later
permits a larger article or a different image shape.

## Maintenance and staleness

The manifest binds the article and header to digests or stable identities for:

- `book_structure.json` and the summarized chapter set;
- the claim-atom registry and core evidence-quality vectors;
- cited proof/result/source artifacts and their chapter anchors;
- the latest public release identity and canonical live-book URL;
- the article source, rendered word count, claim crosswalk, header, alt text,
  and provenance; and
- the X help-page check date and composer-preview receipt.

The derivative becomes stale when any summarized chapter or claim is added,
removed, renamed, promoted, narrowed, deprecated, or refuted; a decisive result
or source changes; the public release identity or live-book URL changes; the
header changes; or X changes relevant composer/media behavior. Each public book
release must refresh and revalidate it or record an exact `not_refreshed`
disposition. A stale article must not be represented as current.

## Publication authority

Repository readiness and external publication are separate decisions. No
automation may publish, edit, unpublish, or delete the X Article without
Corben's explicit authorization for that mutation. P9 may terminate as
`ready_not_published`. If publication is authorized, the release record must
bind the X URL, audience, timestamp, source/header digests, composer preview,
and exact live-book destination.

## Non-claims

This contract does not prove a book claim, promote a support state, establish
X compatibility before the live preflight, grant media rights, create a header
image, publish an Article, or authorize account access.
