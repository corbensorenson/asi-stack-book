#!/usr/bin/env python3
"""Build/check the source-only v2.1 reader amendment after P2 prose changes."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

import build_reader_edition


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "editions/reader_manuscript/v2_1"
STRUCTURE = ROOT / "book_structure.json"
PREDECESSOR = ROOT / "editions/reader_manuscript/v2_0/manifest.json"
ACCEPTED = {
    "ext_faithfulness_information_flow_2026",
    "ext_monitorbench_2026",
    "ext_v_jepa_2_2025",
    "ext_embedded_agency_2019",
}

READER_AMENDMENTS = {
    "artifact-graphs-audit-logs-and-replay": """
## Reasoning records are not authority records

A reasoning trace is one artifact class, not an authoritative receipt. The
reader must keep private reasoning, reported rationale, observable action,
action receipt, monitorability evidence, and authoritative effect separate.
`ext_faithfulness_information_flow_2026` adds the decisive boundary: a trace
may contain enough information to predict an answer without being causally
necessary for that answer. Trace perturbation, action perturbation,
hidden-computation controls, and evaluator identity therefore belong in the
record, while transcript plausibility never grants execution authority.
""",
    "integrated-reference-architecture": """
## Predictive state inside an embedded system

The reference trace can carry a latent world-model handoff without adding a
new layer. `ext_v_jepa_2_2025` motivates records for observation and encoder
identity, action-conditioned predictor, candidate sequence, horizon, search
budget, uncertainty, prediction error, replanning trigger, fallback, and
sim-to-real residual. Planning may propose an action from that packet; it does
not inherit authority to execute it.

The trace is also inside the world it describes. `ext_embedded_agency_2019`
warns that the stack, its verifier, and its subsystems use bounded models and
can share blind spots or divergent objectives. Trust roots, recursion stops,
descendant identity, ontology changes, and outside-model residuals remain
visible; a complete-looking ledger is not a solution to embedded agency.
""",
}


def load(path: Path):
    return json.loads(path.read_text())


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest_bytes(parts: list[bytes]) -> str:
    return hashlib.sha256(b"".join(parts)).hexdigest()


def chapter_rows(structure: dict):
    return [chapter for part in structure["parts"] for chapter in part["chapters"]]


def build_into(target: Path) -> dict:
    structure = load(STRUCTURE)
    predecessor = load(PREDECESSOR)
    chapters = chapter_rows(structure)
    target.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="asi-reader-v2-1-") as td:
        generated = Path(td)
        summary = build_reader_edition.generate(generated, "reader_release", None)
        records = []
        for order, chapter in enumerate(chapters, 1):
            source = generated / chapter["file"]
            destination = target / "chapters" / f"{chapter['id']}.qmd"
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
            text = destination.read_text()
            amendment = READER_AMENDMENTS.get(chapter["id"])
            if amendment:
                marker = "\n## Summary\n"
                if marker not in text:
                    raise RuntimeError(f"reader amendment insertion marker missing: {chapter['id']}")
                text = text.replace(marker, "\n" + amendment.strip() + "\n" + marker, 1)
                destination.write_text(text)
            accepted = sorted(sid for sid in ACCEPTED if sid in text)
            records.append({
                "chapter_id": chapter["id"],
                "title": chapter["title"],
                "order": order,
                "live_source": chapter["file"],
                "live_source_sha256": sha(ROOT / chapter["file"]),
                "reader_source": f"editions/reader_manuscript/v2_1/chapters/{chapter['id']}.qmd",
                "reader_source_sha256": sha(destination),
                "p2_accepted_source_ids_in_prose": accepted,
                "claim_support_state": "argument",
                "reconciliation_status": "internally_reconciled",
                "meaning_effect": "external boundary or comparator strengthened; core claim meaning and support state unchanged",
            })
    source_tree = digest_bytes([STRUCTURE.read_bytes()] + [(ROOT / c["file"]).read_bytes() for c in chapters])
    reader_tree = digest_bytes([(target / "chapters" / f"{c['id']}.qmd").read_bytes() for c in chapters])
    manifest = {
        "schema_version": "asi_stack.curated_reader_source_amendment.v1",
        "edition_id": "asi-stack-curated-reader-v2.1",
        "version": "v2.1",
        "status": "reconciled_source_only",
        "chapter_count": len(chapters),
        "created": "2026-07-14",
        "predecessor": {
            "edition_id": predecessor["edition_id"],
            "path": "editions/reader_manuscript/v2_0/manifest.json",
            "manifest_sha256": sha(PREDECESSOR),
            "immutability": "read_only_historical_predecessor_not_modified",
        },
        "amendment_reason": "Post-v2.3 P2 passage-reviewed external anchoring for reasoning-trace faithfulness, monitorability, V-JEPA/world-model ownership, and embedded-agency limits.",
        "source_snapshot": {
            "parent_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
            "working_tree_boundary": "chapter bytes and source-tree digest are authoritative; parent commit predates this source-only amendment",
            "book_structure_sha256": sha(STRUCTURE),
            "source_tree_sha256": source_tree,
            "reader_tree_sha256": reader_tree,
        },
        "accepted_source_ids": sorted(ACCEPTED),
        "chapter_records": records,
        "format_status": {
            "html": "not_built_not_approved",
            "epub": "not_built_not_approved",
            "pdf": "not_built_not_approved",
            "docx": "not_built_not_approved",
            "audio": "deferred_not_authorized",
            "embedded_audio": "deferred_not_authorized",
        },
        "release_state": "not_released_source_only",
        "support_state_effect": "none",
        "release_effect": "none",
        "external_human_prepublication_required": False,
        "non_claims": [
            "This source amendment does not modify or supersede immutable v1.0 or v2.0 artifacts.",
            "No v2.1 format artifact is built, approved, published, tagged, archived, or deployed.",
            "Internal prose reconciliation is not independent external-human review.",
            "No chapter-core claim moves above argument.",
            "No model quality, monitorability, causal-world-model, corrigibility, safety, AGI, or ASI result is established.",
        ],
    }
    (target / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    (target / "README.md").write_text(
        "# ASI Stack Curated Reader v2.1 Source Amendment\n\n"
        "Status: `reconciled_source_only`; no format artifact or release.\n\n"
        "This directory carries the 54-chapter Human projection after the post-v2.3 P2 external-evidence reconciliation. It is a successor source edition because v2.0 is frozen and immutable. The amendment adds passage-reviewed reasoning-trace, monitorability, V-JEPA/world-model, and embedded-agency boundaries without changing any chapter-core support state.\n\n"
        "No HTML, EPUB, PDF, DOCX, audio, embedded-audio, publication, rights, safety, AGI, or ASI approval is implied. No independent external-human prepublication review is required or claimed.\n"
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.write == args.check:
        raise SystemExit("Choose exactly one of --write or --check")
    if args.write:
        manifest = build_into(OUT)
        print(f"Reader v2.1 wrote {manifest['chapter_count']} source chapters; no format artifact or release.")
        return
    with tempfile.TemporaryDirectory(prefix="asi-reader-v2-1-check-") as td:
        candidate = Path(td) / "v2_1"
        manifest = build_into(candidate)
        expected = sorted(p.relative_to(OUT).as_posix() for p in OUT.rglob("*") if p.is_file())
        actual = sorted(p.relative_to(candidate).as_posix() for p in candidate.rglob("*") if p.is_file())
        if expected != actual:
            raise SystemExit("Reader v2.1 file set drifted")
        for relative in expected:
            if (OUT / relative).read_bytes() != (candidate / relative).read_bytes():
                raise SystemExit(f"Reader v2.1 byte drift: {relative}")
        print(f"Reader v2.1 reproducibility check passed: {manifest['chapter_count']} source chapters byte-identical; no formats built.")


if __name__ == "__main__":
    main()
