#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "docs/historical_project_p2_p3_dispositions.json"
DOC = ROOT / "docs/historical_project_p2_p3_dispositions.md"
ROADMAP = ROOT / "docs/historical_project_incorporation_roadmap.md"
EXPECTED = {
    "routing-heads-and-specialist-cores",
    "governed-deliberation-and-test-time-scaling",
    "coil-attention-cyclic-memory-and-recurrence-contracts",
    "resource-economics-and-token-budgets",
    "data-engines-continual-learning-and-unlearning",
    "policy-optimization-and-learning-from-feedback",
    "open-ended-improvement-engines",
    "recursive-self-improvement-boundaries",
    "artifact-steward-agents-and-living-project-governance",
    "model-weight-custody-and-hardware-roots-of-trust",
    "personal-compute-hives-and-federated-edge-intelligence",
    "prototype-roadmap",
    "open-research-agenda-and-bibliography-plan",
}
ALLOWED = {"completed", "deferred", "superseded"}


def main() -> None:
    value = json.loads(DATA.read_text(encoding="utf-8"))
    packets = value.get("packets", [])
    errors: list[str] = []
    ids = [packet.get("chapter_id") for packet in packets]
    if set(ids) != EXPECTED or len(ids) != len(EXPECTED):
        errors.append("disposition ledger must cover the thirteen P2/P3 packet IDs exactly once")
    roadmap = ROADMAP.read_text(encoding="utf-8")
    prose = DOC.read_text(encoding="utf-8")
    for packet in packets:
        chapter_id = packet.get("chapter_id", "")
        if packet.get("priority") not in {"P2", "P3"}:
            errors.append(f"{chapter_id}: priority must be P2 or P3")
        if packet.get("disposition") not in ALLOWED:
            errors.append(f"{chapter_id}: invalid disposition")
        if packet.get("owner") != chapter_id:
            errors.append(f"{chapter_id}: owning chapter must remain explicit")
        for field in ("reason", "reopen_condition", "evidence_route"):
            if not isinstance(packet.get(field), str) or len(packet[field].split()) < 3:
                errors.append(f"{chapter_id}: {field} must name a concrete decision or blocker")
        if packet.get("support_state_effect") != "none":
            errors.append(f"{chapter_id}: disposition cannot promote support")
        if chapter_id not in roadmap:
            errors.append(f"{chapter_id}: missing from incorporation roadmap")
    if value.get("support_state_effect") != "none":
        errors.append("ledger-level support_state_effect must remain none")
    if "does not" not in " ".join(value.get("non_claims", [])).lower() and "not that" not in " ".join(value.get("non_claims", [])).lower():
        errors.append("ledger must preserve explicit non-claims")
    for word in ("Completed", "Superseded", "Deferred"):
        if word.lower() not in prose.lower():
            errors.append(f"readable ledger must define {word.lower()}")
    if "reject a separate chapter for the current" not in roadmap:
        errors.append("durable semantic memory chapter decision is not explicit")
    if errors:
        raise SystemExit("Historical-project disposition validation failed:\n - " + "\n - ".join(errors))
    counts = {status: sum(packet["disposition"] == status for packet in packets) for status in sorted(ALLOWED)}
    print(f"Historical-project dispositions passed: 13 packets, {counts}, no support-state effect.")


if __name__ == "__main__":
    main()
