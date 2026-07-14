#!/usr/bin/env python3
"""Validate the prospectively frozen flagship before or after outcomes."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "experiments/post_v2_3_evidence_protocol_renewal/flagship"
PREREG = BASE / "preregistration.json"; TASKS = BASE / "tasks.json"; LABELS = BASE / "evaluator_labels.json"; RESULT = BASE / "results/program_result.json"; ADJUDICATION = BASE / "results/adjudication.json"


def sha(path: Path) -> str: return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    prereg = json.loads(PREREG.read_text()); tasks = json.loads(TASKS.read_text()); labels = json.loads(LABELS.read_text()); errors = []
    actual_families = len({row["family"] for row in tasks.get("tasks", [])})
    actual_attacks = len({row["attack_tag"] for row in tasks.get("tasks", []) if row.get("attack_tag") != "none"})
    if prereg.get("state") != "frozen_before_outcomes_opened": errors.append("flagship state drifted")
    if tasks.get("task_count") != 16 or tasks.get("family_count") != 8 or tasks.get("attack_count") != 8: errors.append("task/family/attack denominator drifted")
    if labels.get("label_count") != 16 or labels.get("visibility") != "evaluator_only_never_passed_to_generator": errors.append("evaluator-label isolation drifted")
    if prereg.get("corpus", {}).get("tasks_sha256") != hashlib.sha256(json.dumps(tasks, sort_keys=True, separators=(",", ":")).encode()).hexdigest(): errors.append("task canonical binding drifted")
    if prereg.get("corpus", {}).get("labels_sha256") != hashlib.sha256(json.dumps(labels, sort_keys=True, separators=(",", ":")).encode()).hexdigest(): errors.append("label canonical binding drifted")
    if prereg.get("budget", {}).get("model_calls") != 64 or prereg.get("budget", {}).get("candidate_outputs") != 32: errors.append("budget denominator drifted")
    if len(prereg.get("rollback", {}).get("surfaces", [])) != 9 or prereg.get("routes", {}).get("matched_authority") is not True: errors.append("rollback or authority freeze drifted")
    if prereg.get("support_state_effect") != "none_before_results": errors.append("freeze launders support")
    if RESULT.exists():
        result = json.loads(RESULT.read_text())
        if result.get("preregistration_sha256") != sha(PREREG) or result.get("tasks_sha256") != sha(TASKS) or result.get("labels_sha256") != sha(LABELS): errors.append("outcome lost exact frozen-file binding")
        if result.get("planned_candidate_outputs") != 32 or result.get("model_calls", 0) > 64: errors.append("outcome denominator/budget violation")
        if (actual_families, actual_attacks) != (9, 9): errors.append("exact post-outcome family/attack count drifted")
        if not ADJUDICATION.exists(): errors.append("frozen family/attack metadata mismatch lacks adjudication erratum")
        else:
            erratum = json.loads(ADJUDICATION.read_text()).get("frozen_metadata_erratum", {})
            if erratum.get("actual_families") != 9 or erratum.get("actual_attacked_tasks") != 9 or erratum.get("task_or_label_mutation") is not False:
                errors.append("frozen metadata erratum drifted")
    if errors: raise SystemExit("Governance-tax flagship freeze failed:\n - " + "\n - ".join(errors))
    print(f"Governance-tax flagship freeze passed: 16 tasks, declared 8/8 and exact-file {actual_families}/{actual_attacks} family/attack counts with required erratum after outcomes, 2 seeds, 64-call ceiling, evaluator-label isolation, 9 rollback surfaces, outcomes={'present' if RESULT.exists() else 'unopened'}.")


if __name__ == "__main__": main()
