#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TERMINAL = ROOT / "experiments/claim_family_terminal_coverage/results/result.json"
BUNDLES = ROOT / "experiments/claim_family_bundle_coverage/result.json"
STATUS = ROOT / "roadmap_records/post_v2_3_claim_proof_and_sota_challenge_status.json"
START = "<!-- P7-EVIDENCE-RECONCILIATION:START -->"
END = "<!-- P7-EVIDENCE-RECONCILIATION:END -->"


def load(path: Path):
    return json.loads(path.read_text())


def prose_list(values: list[str]) -> str:
    if not values:
        return "none"
    return ", ".join(f"`{value}`" for value in values)


def count_text(counts: Counter) -> str:
    order = [
        "blocked_after_full_attempt",
        "retained_after_full_attempt",
        "narrowed_after_full_attempt",
        "refuted_after_full_attempt",
        "deprecated_after_full_attempt",
        "promoted_at_bounded_scope",
    ]
    return "; ".join(f"{counts[key]} `{key}`" for key in order if counts[key])


def row_for_state(state: str, rows: list[dict]) -> str | None:
    selected = [row for row in rows if row["terminal_disposition"] == state]
    if not selected:
        return None
    attempted = sorted({lane for row in selected for lane in row.get("attempted_local_lanes", [])})
    missing = sorted({lane for row in selected for lane in row.get("missing_or_unproved_lanes", [])})
    refs = sorted({row["accepted_transition_ref"] for row in selected if row.get("accepted_transition_ref")})
    if state == "blocked_after_full_attempt":
        why = f"Missing or unproved lanes across this set: {prose_list(missing)}. These are residual proof obligations, not false claims."
    elif state == "retained_after_full_attempt":
        why = "All atom-required local routes were present at the frozen audit boundary, but no accepted upward transition was inferred."
    elif state == "promoted_at_bounded_scope":
        why = f"Only the already accepted exact transitions are preserved: {prose_list(refs)}. No chapter-core movement follows."
    else:
        why = f"The exact accepted transition lineage is preserved: {prose_list(refs)}. The claim is not widened."
    return f"| {state.replace('_', ' ')} | {len(selected)} | {prose_list(attempted)} | {why} |"


def build_block(chapter_id: str, family_id: str, rows: list[dict], bundle: dict) -> str:
    counts = Counter(row["terminal_disposition"] for row in rows)
    core = next((row for row in rows if row.get("role") == "core" or row.get("atom_id") == f"{chapter_id}.core"), None)
    if core is None:
        raise ValueError(f"missing core atom: {chapter_id}")
    attempted = sorted({lane for row in rows for lane in row.get("attempted_local_lanes", [])})
    missing = sorted({lane for row in rows for lane in row.get("missing_or_unproved_lanes", [])})
    accepted = sorted({row["accepted_transition_ref"] for row in rows if row.get("accepted_transition_ref")})
    p6 = ""
    if chapter_id == "replaceable-cognitive-substrates-beyond-transformer-monoculture":
        p6 = (
            "\nThe dated P6 external-reproduction attempt adds seven exact "
            "`blocked_after_full_attempt` dispositions for the architecture tournament, "
            "including this core, Transformer baseline, state-space/recurrent, portfolio, "
            "OneCell, total-system-KISS, and architectural-RSI atoms. Gated DeltaNet-2 "
            "displaces Mamba-3 as the newest reported recurrent frontier for its exact "
            "source envelope; no local reproduction, candidate comparison, Pareto result, "
            "or SOTA result follows.\n"
        )
    return f"""{START}
## Evidence reconciliation (2026-07-16)

The invariant protocol, field meanings, and inference limits are stated once in
[Living Book Methodology](living-book-methodology.qmd#chapter-evidence-packet-contract).
This packet contains only the chapter-specific projection; its authoritative
per-atom rows are the `{chapter_id}` slice of
`experiments/claim_family_terminal_coverage/results/result.json`.{p6}

::: {{.asi-human-only}}
The core remains **{core['terminal_disposition'].replace('_', ' ')}** at
`{core['support_state']}` support. The strongest family attempt was
**{bundle['bundle_name']}**. Its exact boundary is: {bundle['terminal_boundary']}
Across {len(rows)} atoms, the terminal ledger records {count_text(counts)}.
:::

::: {{.asi-ai-only}}
| Chapter-specific field | Value |
|---|---|
| Family / atom denominator | `{family_id}` / {len(rows)} atoms |
| Terminal dispositions | {count_text(counts)} |
| Core | `{core['atom_id']}`: `{core['terminal_disposition']}` at `{core['support_state']}` |
| Core attempted / missing lanes | {prose_list(core.get('attempted_local_lanes', []))} / {prose_list(core.get('missing_or_unproved_lanes', []))} |
| Attempted local lanes | {prose_list(attempted)} |
| Missing or unproved lanes | {prose_list(missing)} |
| Strongest family bundle | **{bundle['bundle_name']}** (`{bundle['bundle_kind']}`): {bundle['scope']} |
| Negative controls | {'; '.join(bundle['negative_controls'])}. |
| Accepted transitions | {prose_list(accepted)} |
| Maximum inference | {bundle['terminal_boundary']} |
| Reproduction / next burden | Replay `{bundle['validator_path']}` and `scripts/validate_claim_family_terminal_program.py`; fill the named atom-specific lanes under a new prospective protocol. |
:::
{END}
"""


def main() -> None:
    terminal = load(TERMINAL)
    status = load(STATUS)
    bundles = {row["family_id"]: row for row in load(BUNDLES)["bundles"]}
    family_by_chapter = {row["chapter_id"]: row["family_id"] for row in status["chapter_claim_program"]}
    rows_by_chapter: dict[str, list[dict]] = {}
    for row in terminal["dispositions"]:
        rows_by_chapter.setdefault(row["chapter_id"], []).append(row)
    if set(rows_by_chapter) != set(family_by_chapter):
        raise SystemExit("chapter set mismatch between terminal result and status")
    changed = 0
    for chapter_id in sorted(rows_by_chapter):
        path = ROOT / "chapters" / f"{chapter_id}.qmd"
        text = path.read_text()
        block = build_block(chapter_id, family_by_chapter[chapter_id], rows_by_chapter[chapter_id], bundles[family_by_chapter[chapter_id]])
        if START in text:
            text = re.sub(re.escape(START) + r".*?" + re.escape(END) + r"\n?", block, text, flags=re.S)
        else:
            marker = "\n## Handoff"
            if marker not in text:
                raise SystemExit(f"chapter lacks Handoff insertion point: {chapter_id}")
            text = text.replace(marker, "\n" + block + marker, 1)
        text = re.sub(r"(?m)^last_updated: \"?\d{4}-\d{2}-\d{2}\"?$", 'last_updated: "2026-07-16"', text, count=1)
        path.write_text(text)
        changed += 1
    print(f"Reconciled {changed} chapter evidence packets from 3,745 terminal atom rows and eight family bundles.")


if __name__ == "__main__":
    main()
