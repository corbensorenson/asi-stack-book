#!/usr/bin/env python3
"""Validate headline counts in docs/v1_0_candidate_status.md.

The v1.0 status page is a public-safe readiness surface. This script checks
that its snapshot counts still match the current repository artifacts; it does
not assert that the book is a v1.0 evidence release.
"""

from __future__ import annotations

from collections import Counter
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "docs" / "v1_0_candidate_status.md"
FRONT_MATTER_RE = re.compile(r"\A---\n.*?\n---\n?", re.DOTALL)
WORD_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9'_-]*")
HUMAN_BLOCK_RE = re.compile(r"::: \{\.asi-human-only\}\n## Human Reading Path\n\n(.*?)\n:::", re.DOTALL)
TEMPLATE_BRIDGE_PHRASES = (
    "The useful",
    "The practical",
    "The point is",
    "useful only when",
    "The mature test",
    "The mature version is",
    "the book",
    "this book",
    "Part I",
    "Part II",
    "Part III",
    "Part IV",
    "previous chapter",
    "previous chapters",
    "previous layers",
    "first two chapters",
    "first half",
    "closing move",
    "begins by",
    "ended by",
)


def fail(errors: list[str]) -> None:
    print("v1.0 status snapshot validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def flatten_chapters(structure: dict) -> list[dict]:
    return [chapter for part in structure.get("parts", []) for chapter in part.get("chapters", [])]


def chapter_word_counts() -> tuple[int, int, int]:
    chapter_files = sorted((ROOT / "chapters").glob("*.qmd"))
    body_words = 0
    raw_words = 0
    for path in chapter_files:
        text = path.read_text(encoding="utf-8")
        raw_words += len(WORD_RE.findall(text))
        body_words += len(WORD_RE.findall(FRONT_MATTER_RE.sub("", text, count=1)))
    return len(chapter_files), body_words, raw_words


def summary_metric(path: Path, metric: str) -> str | None:
    text = path.read_text(encoding="utf-8", errors="ignore")
    match = re.search(rf"^\|\s*{re.escape(metric)}\s*\|\s*(.*?)\s*\|$", text, re.MULTILINE)
    return match.group(1).strip() if match else None


def human_bridge_metrics(chapters: list[dict]) -> tuple[int, int, int, int]:
    values: list[int] = []
    opening_values: list[int] = []
    closing_values: list[int] = []
    template_phrase_hits = 0
    for chapter in chapters:
        path = ROOT / str(chapter.get("file", ""))
        text = path.read_text(encoding="utf-8", errors="ignore")
        match = HUMAN_BLOCK_RE.search(text)
        if not match:
            continue
        bridge_text = re.sub(r"\s+", " ", match.group(1).strip())
        normalized_bridge = bridge_text.lower()
        template_phrase_hits += sum(normalized_bridge.count(phrase.lower()) for phrase in TEMPLATE_BRIDGE_PHRASES)
        values.append(len(WORD_RE.findall(bridge_text)))
        sentences = [sentence.strip() for sentence in re.split(r"(?<=[.!?])\s+", bridge_text) if sentence.strip()]
        if sentences:
            opening_values.append(len(WORD_RE.findall(sentences[0])))
            closing_values.append(len(WORD_RE.findall(sentences[-1])))
    return (
        min(values) if values else 0,
        min(opening_values) if opening_values else 0,
        min(closing_values) if closing_values else 0,
        template_phrase_hits,
    )


def main() -> None:
    errors: list[str] = []
    status_text = STATUS.read_text(encoding="utf-8")
    structure = load_json(ROOT / "book_structure.json")
    if not isinstance(structure, dict):
        fail(["book_structure.json must contain an object."])
    chapters = flatten_chapters(structure)
    appendices = structure.get("appendices", [])
    front_matter = structure.get("front_matter", [])
    book_page_count = len(front_matter) + len(chapters) + len(appendices)
    source_records = load_json(ROOT / "sources" / "source_inventory.json")
    proof_manifest = load_json(ROOT / "proofs" / "proof_manifest.json")
    if not isinstance(source_records, list):
        fail(["sources/source_inventory.json must contain a list."])
    if not isinstance(proof_manifest, dict):
        fail(["proofs/proof_manifest.json must contain an object."])

    chapter_file_count, body_words, raw_words = chapter_word_counts()
    source_note_ids = {
        path.stem
        for path in (ROOT / "sources" / "source_notes").glob("*.md")
        if path.name not in {"README.md", "_template.md"}
    }
    source_ids = {str(record.get("id", "")) for record in source_records}
    missing_notes = sorted(source_ids - source_note_ids)
    evidence_counts = Counter(str(chapter.get("evidence_level", "")) for chapter in chapters)
    claim_label_counts = Counter(str(chapter.get("claim_label", "")) for chapter in chapters)
    schema_count = len(list((ROOT / "schemas").glob("*.schema.json")))
    fixture_count = len(list((ROOT / "tests" / "fixtures" / "protocol_records").glob("*.json")))
    release_count = len(list((ROOT / "release_records").glob("*.json")))
    (
        human_min_words,
        human_min_opening_words,
        human_min_closing_words,
        human_template_phrase_hits,
    ) = human_bridge_metrics(chapters)

    assigned_pairs = summary_metric(ROOT / "docs" / "source_evidence_audit.md", "Assigned source/chapter pairs")
    exact_mappings = summary_metric(ROOT / "docs" / "source_evidence_audit.md", "Exact claim-source mappings")
    passage_reviewed = summary_metric(ROOT / "docs" / "source_evidence_audit.md", "Passage-reviewed mappings recorded")
    proof_targets = str(proof_manifest.get("proof_target_count", ""))

    expected_fragments = [
        f"| Book structure | {len(structure.get('parts', []))} parts, {len(chapters)} manifest-driven chapters, {len(appendices)} appendices |",
        f"| Manifest claim contract | {len(chapters)} chapters explicitly declare `claim_label` and `evidence_level`; current distribution is {claim_label_counts.get('Design rationale', 0)} `Design rationale` labels and {evidence_counts.get('argument', 0)} `argument` support states; missing or invalid values fail validation |",
        f"| Manuscript scale | {chapter_file_count} chapter files; {body_words:,} chapter words excluding YAML front matter; {raw_words:,} raw chapter-file words including metadata and live scaffolding |",
        f"| Source inventory | {len(source_records)} public-safe source records, each with a matching public source note;",
        "| Source appendix ownership | Appendix G (`Corben's Own Sources, Papers, and Local Projects`) and Appendix H (`External Sources by Other Authors`) are independent top-level appendices with explicit source-ownership boundary blocks, ownership-rule rows, and appendix-local identity rows: G contains Corben's own papers, Corben-supplied materials, recovered project records, and local project records; H contains external records and third-party literature marked `external_literature`; neither appendix renders the other source class as a second ownership row |",
        f"| Claim/source traceability | {assigned_pairs} assigned source/chapter pairs, {exact_mappings} exact claim-source mappings, {passage_reviewed} passage-reviewed mappings |",
        f"| Support states | {evidence_counts.get('argument', 0)} chapter core claims at `argument`; the v1.0 evidence-transition pilot records eight accepted no-change decisions and no support-state promotion |",
        "`python3 scripts/validate_evidence_transitions.py`",
        "| Test harnesses | Seven synthetic harnesses are wired into book validation and the Phase 5 registry: the support-state transition harness checks 2 valid and 2 expected-invalid evidence-transition fixtures for no-change conservatism, upward-transition review gates, required evidence refs, and failed-verification blockers; the authority transition harness checks 3 valid and 3 expected-invalid authority-transition fixtures for non-escalation, permission separation, denial receipts, approval escalation, and confused-deputy shortcuts; the plan-execution contract harness checks 2 valid and 5 expected-invalid command-contract, plan-graph, DAG, semantic-atom, and typed-job fixtures for cross-record consistency, acyclic dependency order, dispatch receipts, requirement preservation, artifact traceability, and approval gating; the runtime adapter permission harness checks 2 valid and 5 expected-invalid typed-job, runtime-adapter-invocation, and authority-use-receipt fixtures for permission coverage, high-impact approval gating, approval expiry markers, effect receipts, rollback handles, irreversible residuals, and authority receipt alignment; the context admission/adequacy harness checks 3 valid and 5 expected-invalid context ABI, packet, certificate, transaction, and adequacy fixtures for admission/adequacy separation, conflict blocking, stale certificate rejection, deletion closure, escalation, and mode-confusion gates; the readiness/residual gate harness checks 4 valid and 5 expected-invalid costed-route, readiness-gate, and replacement-transaction fixtures for promotion gates, residual escrow custody, quarantine, authority bounds, expired-evidence reruns, fallback, and rollback readiness; the benchmark anti-Goodhart harness checks 2 valid and 5 expected-invalid benchmark-ratchet, policy-optimization, and steward-action fixtures for holdout/contamination/mutation or transfer checks, saturated-benchmark regression floors, blocked-ratchet policy promotion, reward-as-truth confusion, and release approval evidence. The registry guard checks commands, docs, fixture counts, result records, Appendix E rows, public status references, primary chapter mappings, non-claim boundaries, and main-validation wiring. None of these harnesses promotes live claims |",
        "`docs/support_state_transition_harness.md`",
        "`python3 scripts/validate_support_state_transitions.py`",
        "`docs/authority_transition_harness.md`",
        "`python3 scripts/validate_authority_transitions.py`",
        "`docs/plan_execution_contract_harness.md`",
        "`python3 scripts/validate_plan_execution_contracts.py`",
        "`docs/runtime_adapter_permission_harness.md`",
        "`python3 scripts/validate_runtime_adapter_permissions.py`",
        "`docs/context_admission_adequacy_harness.md`",
        "`python3 scripts/validate_context_admission_adequacy.py`",
        "`docs/readiness_residual_harness.md`",
        "`python3 scripts/validate_readiness_residual_gates.py`",
        "`docs/benchmark_antigoodhart_harness.md`",
        "`python3 scripts/validate_benchmark_antigoodhart.py`",
        "`experiments/phase5_harness_registry.json`",
        "`docs/phase5_harness_registry.md`",
        "`python3 scripts/validate_phase5_harness_registry.py`",
        f"| Proof envelope | {proof_targets} proof targets, all implemented as narrow finite-record Lean predicates; current proof adequacy review classifies 8 targets as adequate only for narrow finite-record claims, 28 useful-but-too-narrow, 20 needing richer state or review semantics, 40 needing executable tests first, 10 needing empirical or baseline tests first, and 6 remaining research-agenda until artifact import; follow-through increments add a record-aware allow/deny/escalate authority decision envelope, a record-aware planning control envelope, and a synthetic runtime adapter permission harness without promoting System Boundaries, Planning, or Runtime Adapters above `argument` |",
        "`docs/proof_adequacy_review.md`",
        f"| Schemas and fixtures | {schema_count} JSON Schemas, {fixture_count} valid protocol fixtures, {release_count} public release record |",
        f"| Implementation horizons | {len(chapters)} generated chapter build horizons with manifest-sourced minimum viable implementation and beyond-state-of-the-art endpoint fields |",
        "browser Human-view gate checks rendered Mermaid SVG visibility; dense Mermaid diagrams keep mobile labels readable through contained diagram-block scrolling without page-level horizontal overflow",
        "| Chapter handoffs | All 54 manifest chapters now end with reader-facing `Handoff` sections: non-final chapters name the next manifest chapter title and avoid numbered chapter references, while the final chapter closes the book-level arc; generated reader chapters must preserve the same single Handoff continuity after live-only stripping |",
        "the reader release has a tracked semantic overlay manifest as the editable delta source, generated reader delta report path as review output with a zero-active-operation note or operation digests and before/after excerpts, embedded live Human-view overlay payload for major-version human-edition deltas, and a generated reader-continuity audit with 0 high-priority and 3 medium-priority heuristic review rows",
        "`docs/reader_opening_full_review_pass.md` records the first full generated-reader chapter-text review for the opening three chapters; `docs/reader_boundary_full_review_pass.md` records the second full generated-reader chapter-text review for the failure/evidence/intent boundary sequence; `docs/reader_continuity_review.md` records first manual decisions for the three medium-priority reader-audit rows; `docs/reader_part_i_review_pass.md` records eight first-pass Part I decisions including one canonical prose cleanup; `docs/reader_part_ii_review_pass.md` records eleven first-pass Part II decisions including three canonical prose cleanups; `docs/reader_part_iii_review_pass.md` records eight first-pass Part III decisions including three canonical prose cleanups; and `docs/reader_part_iv_review_pass.md` records five first-pass Part IV decisions plus one reader-generator capitalization cleanup, without treating those notes as release approval.",
        "The synced chapter review matrix records 54 reader-review rows with 6 `reviewed`, 48 `spot_checked`, 0 `not_started`, 20 active-overlay chapters, 40 no-immediate-action decisions, 3 companion-note candidates, 1 curated-manuscript candidate, and release blockers on every row until reader release records and artifact review exist; the remaining 48 spot-checked rows also retain full-chapter-review blockers.",
        "The current v1.0 reader-overlay set carries 33 active operations: 2 opening-chapter operations, 1 Efficient ASI table-to-prose operation, 1 Human Intent table-to-prose operation, 1 System Boundaries table-to-prose operation, 1 Evidence States table-to-prose operation, 6 Personal Compute Hives table/prose operations, 2 Command Contracts table-to-prose operations, 1 Planning table-to-prose operation, 1 Verification Bandwidth table-to-prose operation, 1 Runtime Adapters table-to-prose operation, 1 Labor OS table-to-prose operation, 2 Circle Contracts table/prose operations, 1 Generate-Verify-Repair table-to-prose operation, 2 Fast Generation table/code-to-prose operations, 1 RankFold/NeuralFold table-to-prose operation, 1 Mathematical and Search Substrates table-to-prose operation, 2 Policy Optimization table-to-prose operations, 3 Artifact Steward Agents table/prose operations, 1 Executable Specifications prose operation, and 2 Semantic Representation table-to-prose operations for Human view and generated reader editions only",
        "The curated reader-manuscript manifest exists with `not_graduated` status so the future human-prose source can diverge only as a subordinate narrative derivative, and its dormant reconciliation-report template exists for future chapter-by-chapter divergence review.",
        "`editions/reader_overlays/v1_0/manifest.json`",
        "`editions/reader_manuscript/v1_0/manifest.json`",
        "`editions/reader_manuscript/v1_0/chapter_review_matrix.json`",
        "`editions/reader_manuscript/v1_0/reconciliation_report.md`",
        "`docs/reader_chapter_review_matrix.md`",
        "`docs/reader_opening_full_review_pass.md`",
        "`docs/reader_boundary_full_review_pass.md`",
        "`docs/reader_part_i_review_pass.md`",
        "`docs/reader_part_ii_review_pass.md`",
        "`docs/reader_part_iii_review_pass.md`",
        "`docs/reader_part_iv_review_pass.md`",
        "`docs/reader_continuity_audit.md`",
        "`assets/reader-overlays.html`",
        "`python3 scripts/sync_reader_overlay_asset.py --check`",
        "`python3 scripts/validate_reader_overlays.py --check`",
        "`python3 scripts/audit_reader_continuity.py --check`",
        "`python3 scripts/validate_reader_manuscript_manifest.py`",
        "`python3 scripts/sync_reader_chapter_review_matrix.py --check`",
        "`The book needs a place`",
        "`The book needs`",
        "`The stack needs`",
        "`The ASI Stack needs`",
        "`The problem is`",
        "`The insufficiency is`",
        "`The stack should`",
        "`The record should`",
        "`The response is`",
        "`The minimum should`",
        "`Operating mechanism:`",
        "`Failure closure:`",
        "`detect and route failure modes such as`",
        "`This is a target architecture, not a current-result claim`",
        "`remains a target architecture, not a current-result claim`",
        "`It remains beyond the chapter's present support state`",
        "`The interface is the`",
        "`The interface is a`",
        "`The interface is an`",
        "`The public schema now records`",
        "`The interface should`",
        "`The interface should also record`",
        "`The interface should distinguish`",
        "`The interface should expose`",
        "`The interface should carry`",
        "`The interface should also`",
        "`The contract should also`",
        "`None of those passages show`",
        "`The reviewed passages sharpen the`",
        "`The evidence map is narrower now`",
        "`The Lean coverage stays at`",
        "`The support state remains argument`",
        "`The passage-reviewed mappings support discussion`",
        "`The practical point is`",
        "`The practical test is`",
        "`The practical rule is`",
        "`The practical purpose is`",
        "`The practical problem is`",
        "`The subtle failure is`",
        "`The subtle failure mode is`",
        "`Another failure is`",
        "`Each failure should`",
        "`The fixture validates`",
        "`The fixture is not`",
        "`The fixture is only`",
        "`The result is`",
        "`This is why`",
        "`This matters because`",
        "`Another invariant is`",
        "`A second invariant is`",
        "`The strongest invariant is`",
        "`The key invariant is`",
        "`The invariant is`",
        "The repeated-prose guard now rejects `This is why`, so causal transitions must name the specific layer, record, authority change, or consequence directly.",
        "The repeated-prose guard now rejects `This matters because`, so causal explanations must be integrated into chapter-specific prose rather than attached as reusable explanatory scaffolding.",
        "The repeated-prose guard now rejects `The result is`, so summaries and transitions must name the actual bridge, discipline, lifecycle, or artifact path directly.",
        "The repeated-prose guard now rejects `Operating mechanism:`, the exact `remains a target architecture, not a current-result claim` disclaimer, and the reusable `keeps ... honest` cadence",
        f"All {book_page_count} rendered book pages carry the persistent and shareable `AI view` / `Human view` switch",
        "generated reader chapters strip raw live core-claim markers and repeated support boilerplate while preserving claim text and compact inline plain-language support-state boundaries",
        "all rendered pages embed the current reader-overlay payload before the reading-mode toggle and expose runtime overlay operation-count attributes after processing",
        "reader-overlay payload availability and runtime operation-count processing",
        "zero-active-operation note or operation digests and before/after excerpts",
        "generated reader chapter prose rejects `this chapter`, `the chapter`, and repeated evidence-boundary paragraph openers after live-only stripping",
        "while attaching the compact evidence boundary to the visible claim text",
        "raw marker and support-boilerplate hiding/restoration",
        "generated reader chapters preserve one chapter-specific Handoff after `Summary` and now must clear section-level word-count and substantial prose-paragraph floors after stripping",
        "browser smoke validation can exercise every manifest chapter across desktop and mobile viewports with `--all-chapters --all-viewports`, including reading-mode control visibility, reader-overlay payload availability and runtime operation-count processing, raw marker and support-boilerplate hiding/restoration, and horizontal-overflow checks, when Playwright/Chrome is available",
        f"bridge prose is guarded against meta-reader and meta-book scaffolding and must be at least 170 words excluding the source-only heading, must open with at least 11 words, must close with at least 11 words, must avoid known repeated bridge formulas, with the current bridge minimum at {human_min_words} words, opening-sentence minimum at {human_min_opening_words} words, closing-sentence minimum at {human_min_closing_words} words, and targeted template-phrase count at {human_template_phrase_hits}",
    ]

    if len(chapters) != chapter_file_count:
        errors.append(f"Manifest has {len(chapters)} chapters but chapters/ has {chapter_file_count} .qmd files.")
    if missing_notes:
        errors.append(f"Source inventory records missing source notes: {missing_notes}")
    if assigned_pairs is None or exact_mappings is None or passage_reviewed is None:
        errors.append("docs/source_evidence_audit.md is missing required summary metrics.")
    if not proof_targets:
        errors.append("proofs/proof_manifest.json is missing proof_target_count.")
    if human_min_words < 170:
        errors.append(f"Human Reading Path prose minimum is {human_min_words}, below 170.")
    if human_min_opening_words < 11:
        errors.append(f"Human Reading Path opening-sentence minimum is {human_min_opening_words}, below 11.")
    if human_min_closing_words < 11:
        errors.append(f"Human Reading Path closing-sentence minimum is {human_min_closing_words}, below 11.")
    if human_template_phrase_hits != 0:
        errors.append(f"Human Reading Path targeted template-phrase count is {human_template_phrase_hits}, expected 0.")

    for fragment in expected_fragments:
        if fragment not in status_text:
            errors.append(f"docs/v1_0_candidate_status.md is missing current fragment: {fragment}")

    if errors:
        fail(errors)

    print(
        "v1.0 status snapshot validation passed: "
        f"{len(chapters)} chapters, {body_words:,} body words, "
        f"{len(source_records)} sources, {proof_targets} proof targets."
    )


if __name__ == "__main__":
    main()
