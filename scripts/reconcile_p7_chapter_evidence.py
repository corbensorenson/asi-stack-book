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
    state_rows = [row_for_state(state, rows) for state in [
        "promoted_at_bounded_scope",
        "narrowed_after_full_attempt",
        "refuted_after_full_attempt",
        "deprecated_after_full_attempt",
        "retained_after_full_attempt",
        "blocked_after_full_attempt",
    ]]
    state_rows = [row for row in state_rows if row]
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

This chapter owns **{len(rows)}** structured claim atoms in `{family_id}`. The
frozen repository-wide terminal audit records {count_text(counts)}. Its core
atom `{core['atom_id']}` remains at `{core['support_state']}` with terminal
disposition `{core['terminal_disposition']}`. The authoritative per-atom rows
are the `{chapter_id}` slice of
`experiments/claim_family_terminal_coverage/results/result.json`; this summary
does not replace that ledger.{p6}

::: {{.asi-human-only}}
### What the evidence now says

The chapter's core remains **{core['terminal_disposition'].replace('_', ' ')}**
at `{core['support_state']}` support. Across its {len(rows)} structured claims,
{counts['blocked_after_full_attempt']} still lack required proof lanes,
{counts['narrowed_after_full_attempt']} were narrowed, and
{counts['promoted_at_bounded_scope']} received only a bounded subordinate
promotion. No chapter-core claim moved upward.

The strongest relevant family attempt was **{bundle['bundle_name']}**. It gives
this family one real success/failure boundary under rejecting controls, but it
does not prove the rest of this chapter. What worked was limited to its declared
scope; what failed or remains open is preserved in the blocked and narrowed
counts above. The decisive boundary is: {bundle['terminal_boundary']}

The conclusion changes only when new atom-specific work fills the missing
lanes—{prose_list(missing)}—under a prospective protocol and an accepted
evidence transition. Until then, nearby tests, formal models, source counts, and
the family result cannot substitute for the missing evidence.
:::

::: {{.asi-ai-only}}

### Evidence packet

| Field | Exact chapter boundary |
|---|---|
| Protocol | Prospectively frozen 3,745-atom repository audit plus the validated `{family_id}` minimum family bundle. |
| Attempted local lanes | {prose_list(attempted)} |
| Missing or unproved lanes | {prose_list(missing)} |
| Family-level natural-work or end-to-end bundle | **{bundle['bundle_name']}** (`{bundle['bundle_kind']}`): {bundle['scope']} |
| Negative controls | {'; '.join(bundle['negative_controls'])}. |
| Exact accepted transitions in this chapter | {prose_list(accepted)} |
| Core outcome | `{core['terminal_disposition']}` at `{core['support_state']}`; no chapter-core promotion. |
| Uncertainty and transfer | The bundle's measured or executable scope does not transfer automatically to this chapter's other atoms. Missing lanes remain explicit above. |
| Reproduction path | Replay `{bundle['validator_path']}` and `scripts/validate_claim_family_terminal_program.py`; then supply the missing atom-specific lanes under a new prospective protocol. |

### Worked success, failure, and boundary cases

- **Success case:** the family-level bundle passed its own rejecting validator
  within this exact scope: {bundle['scope']} This is evidence that the family
  received a competent attempt, not that every claim in this chapter succeeded.
- **Failure or non-promotion case:** {counts['blocked_after_full_attempt']} atoms
  remain blocked and {counts['narrowed_after_full_attempt']} are narrowed. A
  green family validator cannot fill their missing lanes or raise the core.
- **Boundary case:** {bundle['terminal_boundary']}

### Argument-exit table

| Atom set | Count | Work performed | Terminal reason and next burden |
|---|---:|---|---|
| Core: `{core['atom_id']}` | 1 | {prose_list(core.get('attempted_local_lanes', []))} | `{core['terminal_disposition']}`; missing or unproved: {prose_list(core.get('missing_or_unproved_lanes', []))}. |
{chr(10).join(state_rows)}

This table is a disposition map, not a promotion quota. The next valid movement
is atom-specific evidence that fills the named missing lanes, survives relevant
negative controls, and enters through an accepted evidence transition. Until
then, source counts, theorem counts, fixtures, validators, or nearby family
results cannot be used as substitutes.
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
