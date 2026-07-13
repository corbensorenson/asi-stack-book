"""QI-07: atlas migration compatibility, descendants, and exact rollback."""

from __future__ import annotations

from .canonical import ContractError, make_envelope


def migrate(source_epoch: str, target_epoch: str, rows: list[dict], inventory: dict[str, list[str]], *, shadow_passed: bool) -> dict:
    required_inventory = {"descendants", "caches", "backups", "receipts"}
    if set(inventory) != required_inventory:
        raise ContractError("migration inventory incomplete")
    compatibility = []
    failures = []
    merge_lineage = []
    split_lineage = []
    for row in rows:
        mode = row.get("mode", "same")
        if mode == "same":
            if row["old_soid"] != row["new_soid"]:
                raise ContractError("silent migration retarget forbidden")
            compatibility.append({**row, "status": "compatible"})
        elif mode == "fail":
            failures.append({**row, "status": "typed_failure"})
        elif mode == "merge":
            if not row.get("lineage_id"):
                raise ContractError("merge requires typed lineage")
            merge_lineage.append(row)
        elif mode == "split":
            if not row.get("lineage_id") or len(row.get("new_soids", [])) < 2:
                raise ContractError("split requires typed lineage and children")
            split_lineage.append(row)
        else:
            raise ContractError("unknown migration mode")
    rollback_identity = {
        "restored_epoch": source_epoch,
        "same_soid_rows": all(row["old_soid"] == row["new_soid"] for row in compatibility),
        "inventory_counts": {key: len(value) for key, value in inventory.items()},
        "complete": shadow_passed and all(inventory.values()),
    }
    return {
        "source_epoch": source_epoch,
        "target_epoch": target_epoch,
        "compatibility": compatibility,
        "typed_failures": failures,
        "merge_lineage": merge_lineage,
        "split_lineage": split_lineage,
        "shadow_results": {"passed": shadow_passed, "case_count": len(rows)},
        "descendants": inventory["descendants"],
        "caches": inventory["caches"],
        "backups": inventory["backups"],
        "receipts": inventory["receipts"],
        "rollback_identity": rollback_identity,
    }


def artifact(record: dict, input_digests: list[str]) -> dict:
    if not record["rollback_identity"]["complete"]:
        raise ContractError("rollback inventory or shadow result incomplete")
    return make_envelope(
        "QI-07", f"migration:{record['source_epoch']}:{record['target_epoch']}",
        ["data-engines-continual-learning-and-unlearning"], record,
        input_digests=input_digests,
        non_claim_boundary="Finite local migration and rollback fixture only; no model forgetting, privacy erasure, or storage erasure claim.",
    )
