#!/usr/bin/env python3
"""Reject mutable, unregistered, or stale-reviewed CI dependencies."""

from __future__ import annotations

import copy
from datetime import date, timedelta
import json
import os
import re
import sys
from pathlib import Path

from build_canonical_public_status import validate_against_schema


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_DIR = ROOT / ".github" / "workflows"
LEDGER = ROOT / "docs" / "ci_supply_chain_pinning.md"
INVENTORY = ROOT / "ci" / "dependency_pin_inventory.json"
SCHEMA = ROOT / "schemas" / "ci_dependency_pin_inventory.schema.json"

USES_RE = re.compile(r"^\s*(?:-\s*)?uses:\s*([^\s#]+)", re.MULTILINE)
REMOTE_ACTION_RE = re.compile(r"^(?P<action>[^@]+)@(?P<ref>[^@]+)$")
FULL_COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
ELAN_URL_RE = re.compile(
    r"https://raw\.githubusercontent\.com/leanprover/elan/([^/]+)/elan-init\.sh"
)


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def audit_date() -> date:
    raw = os.environ.get("ASI_PIN_REVIEW_AS_OF")
    if not raw:
        return date.today()
    try:
        return date.fromisoformat(raw)
    except ValueError as exc:
        raise ValueError("ASI_PIN_REVIEW_AS_OF must be YYYY-MM-DD") from exc


def inventory_values(data: dict) -> tuple[dict[str, str], dict]:
    actions = {
        str(row["repository"]): str(row["pin"])
        for row in data.get("pins", [])
        if row.get("kind") == "github_action"
    }
    installers = [row for row in data.get("pins", []) if row.get("kind") == "commit_url_installer"]
    return actions, installers[0] if len(installers) == 1 else {}


def validate_inventory(data: dict, schema: dict, *, as_of: date) -> list[str]:
    errors = validate_against_schema(data, schema, str(INVENTORY.relative_to(ROOT)))
    policy = data.get("review_policy", {})
    max_age = int(policy.get("max_review_age_days", 0) or 0)
    warning_age = int(policy.get("warning_age_days", 0) or 0)
    if max_age <= 0 or warning_age <= 0 or warning_age >= max_age:
        errors.append("pin review policy requires 0 < warning_age_days < max_review_age_days")
    pins = data.get("pins", [])
    ids = [str(row.get("id", "")) for row in pins if isinstance(row, dict)]
    if len(ids) != len(set(ids)):
        errors.append("dependency pin inventory contains duplicate IDs")
    repositories = [str(row.get("repository", "")) for row in pins if isinstance(row, dict)]
    if len(repositories) != len(set(repositories)):
        errors.append("dependency pin inventory contains duplicate repositories")
    installers = [row for row in pins if isinstance(row, dict) and row.get("kind") == "commit_url_installer"]
    if len(installers) != 1:
        errors.append(f"dependency pin inventory must contain exactly one commit URL installer, found {len(installers)}")

    for row in pins:
        if not isinstance(row, dict):
            continue
        label = str(row.get("id", "unknown"))
        try:
            reviewed = date.fromisoformat(str(row.get("reviewed_on", "")))
            due = date.fromisoformat(str(row.get("review_due_on", "")))
        except ValueError:
            errors.append(f"{label}: reviewed_on and review_due_on must be ISO dates")
            continue
        if reviewed > as_of:
            errors.append(f"{label}: review date {reviewed} is in the future relative to {as_of}")
        expected_due = reviewed + timedelta(days=max_age)
        if due != expected_due:
            errors.append(f"{label}: review_due_on {due} must equal reviewed_on + {max_age} days ({expected_due})")
        if policy.get("fail_closed_after_due") is not True:
            errors.append("pin review policy must fail closed after the due date")
        if as_of > due:
            errors.append(f"{label}: dependency review expired on {due}; current audit date is {as_of}")
        pin = str(row.get("pin", ""))
        if not FULL_COMMIT_RE.fullmatch(pin):
            errors.append(f"{label}: pin is not a full lowercase commit SHA")
        if row.get("kind") == "github_action":
            if label != f"github-action:{row.get('repository')}":
                errors.append(f"{label}: GitHub action ID must derive from repository")
            if row.get("artifact_url") is not None or row.get("artifact_sha256") is not None:
                errors.append(f"{label}: GitHub action record must not carry installer artifact fields")
        elif row.get("kind") == "commit_url_installer":
            if label != f"commit-url-installer:{row.get('repository')}":
                errors.append(f"{label}: installer ID must derive from repository")
            if f"/{pin}/" not in str(row.get("artifact_url", "")):
                errors.append(f"{label}: installer URL is not bound to its recorded commit")
            digest = str(row.get("artifact_sha256", ""))
            if not re.fullmatch(r"[0-9a-f]{64}", digest):
                errors.append(f"{label}: installer artifact SHA-256 is missing or malformed")
    return errors


def validate_inventory_coverage(data: dict, seen_actions: set[str]) -> list[str]:
    action_pins, installer = inventory_values(data)
    errors: list[str] = []
    missing = sorted(seen_actions - set(action_pins))
    unused = sorted(set(action_pins) - seen_actions)
    for action in missing:
        errors.append(f"workflow action is not governed by the dependency inventory: {action}")
    for action in unused:
        errors.append(f"governed action pin is no longer exercised by a workflow: {action}")
    if not installer:
        errors.append("dependency inventory does not resolve exactly one installer record")
    return errors


def validate_workflow_text(
    label: str,
    text: str,
    action_pins: dict[str, str],
    installer: dict,
) -> list[str]:
    """Validate one workflow body without trusting YAML execution semantics."""
    errors: list[str] = []
    for target in USES_RE.findall(text):
        if target.startswith("./"):
            continue
        if target.startswith("docker://"):
            if "@sha256:" not in target:
                errors.append(f"{label}: Docker action is not digest-pinned: {target}")
            continue
        match = REMOTE_ACTION_RE.fullmatch(target)
        if not match or not FULL_COMMIT_RE.fullmatch(match.group("ref")):
            errors.append(f"{label}: remote action is not pinned to a full commit SHA: {target}")
            continue
        expected = action_pins.get(match.group("action"))
        if expected is None:
            errors.append(f"{label}: remote action is absent from the governed inventory: {match.group('action')}")
        elif match.group("ref") != expected:
            errors.append(
                f"{label}: {match.group('action')} uses unreviewed commit "
                f"{match.group('ref')}; update the machine inventory and prose ledger together"
            )

    installer_pin = str(installer.get("pin", ""))
    installer_digest = str(installer.get("artifact_sha256", ""))
    installer_url = str(installer.get("artifact_url", ""))
    elan_refs = ELAN_URL_RE.findall(text)
    if "elan-init.sh" in text:
        if elan_refs != [installer_pin] or installer_url not in text:
            errors.append(f"{label}: Elan installer must use exactly the governed commit URL")
        checksum_command = f'echo "{installer_digest}  /tmp/elan-init.sh" | sha256sum -c -'
        if checksum_command not in text:
            errors.append(f"{label}: Elan installer is not verified with the governed SHA-256 digest")
        if text.find(checksum_command) > text.find("sh /tmp/elan-init.sh"):
            errors.append(f"{label}: Elan checksum verification must precede installer execution")
    return errors


def validate_ledger(text: str, action_pins: dict[str, str], installer: dict) -> list[str]:
    errors: list[str] = []
    normalized = " ".join(text.split())
    for action, commit in action_pins.items():
        if f"`{action}`" not in text or f"`{commit}`" not in text:
            errors.append(f"pin ledger does not record {action} at {commit}")
    for fragment in (
        f"`{installer.get('pin', '')}`",
        f"`{installer.get('artifact_sha256', '')}`",
        "`ci/dependency_pin_inventory.json`",
        "90 days",
        "## Update procedure",
        "full commit SHA",
        "runner image and transitive network/tool dependencies remain outside",
        "does not prove an action or installer is benign",
    ):
        if fragment not in normalized:
            errors.append(f"pin ledger is missing governed text: {fragment}")
    return errors


def run_negative_controls(
    publish_text: str,
    inventory: dict,
    schema: dict,
    seen_actions: set[str],
    *,
    as_of: date,
) -> list[str]:
    """Prove the checker rejects workflow and review-inventory regressions."""
    failures: list[str] = []
    action_pins, installer = inventory_values(inventory)
    first_action = next(iter(action_pins))
    controls = {
        "moving action tag": publish_text.replace(
            f"{first_action}@{action_pins[first_action]}",
            f"{first_action}@v4",
            1,
        ),
        "mutable installer URL": publish_text.replace(
            str(installer["artifact_url"]),
            str(installer["artifact_url"]).replace(str(installer["pin"]), "master"),
            1,
        ),
        "missing installer checksum": publish_text.replace(
            f'echo "{installer["artifact_sha256"]}  /tmp/elan-init.sh" | sha256sum -c -',
            "true # checksum removed by negative control",
            1,
        ),
    }
    for name, mutated in controls.items():
        if not validate_workflow_text(f"negative control: {name}", mutated, action_pins, installer):
            failures.append(f"negative control was incorrectly accepted: {name}")

    stale = copy.deepcopy(inventory)
    stale["pins"][0]["reviewed_on"] = "2025-01-01"
    stale["pins"][0]["review_due_on"] = "2025-04-01"
    if not validate_inventory(stale, schema, as_of=as_of):
        failures.append("negative control was incorrectly accepted: stale review")

    missing = copy.deepcopy(inventory)
    missing["pins"] = missing["pins"][1:]
    if not validate_inventory_coverage(missing, seen_actions):
        failures.append("negative control was incorrectly accepted: missing inventory action")

    mismatched = copy.deepcopy(inventory)
    mismatched["pins"][0]["pin"] = "0" * 40
    bad_actions, bad_installer = inventory_values(mismatched)
    if not validate_workflow_text("negative control: mismatched inventory pin", publish_text, bad_actions, bad_installer):
        failures.append("negative control was incorrectly accepted: mismatched inventory pin")

    duplicate = copy.deepcopy(inventory)
    duplicate["pins"].append(copy.deepcopy(duplicate["pins"][0]))
    if not validate_inventory(duplicate, schema, as_of=as_of):
        failures.append("negative control was incorrectly accepted: duplicate inventory ID")
    return failures


def main() -> None:
    errors: list[str] = []
    workflows = sorted((*WORKFLOW_DIR.glob("*.yml"), *WORKFLOW_DIR.glob("*.yaml")))
    if not workflows:
        errors.append("no GitHub Actions workflows found")
    if not INVENTORY.exists() or not SCHEMA.exists():
        errors.append("missing CI dependency pin inventory or schema")
        inventory: dict = {"pins": [], "review_policy": {}}
        schema: dict = {}
    else:
        inventory = load_json(INVENTORY)
        schema = load_json(SCHEMA)
    try:
        as_of = audit_date()
    except ValueError as exc:
        errors.append(str(exc))
        as_of = date.today()
    errors.extend(validate_inventory(inventory, schema, as_of=as_of))
    action_pins, installer = inventory_values(inventory)

    workflow_texts: dict[str, str] = {}
    seen_actions: set[str] = set()
    for path in workflows:
        text = path.read_text(encoding="utf-8", errors="ignore")
        label = str(path.relative_to(ROOT))
        workflow_texts[label] = text
        errors.extend(validate_workflow_text(label, text, action_pins, installer))
        for target in USES_RE.findall(text):
            match = REMOTE_ACTION_RE.fullmatch(target)
            if match:
                seen_actions.add(match.group("action"))
    errors.extend(validate_inventory_coverage(inventory, seen_actions))

    if not LEDGER.exists():
        errors.append(f"missing {LEDGER.relative_to(ROOT)}")
    else:
        errors.extend(validate_ledger(LEDGER.read_text(encoding="utf-8", errors="ignore"), action_pins, installer))

    installer_workflows = [text for text in workflow_texts.values() if "elan-init.sh" in text]
    if len(installer_workflows) != 1:
        errors.append(f"expected exactly one workflow owning the Elan installer, found {len(installer_workflows)}")
    else:
        errors.extend(run_negative_controls(installer_workflows[0], inventory, schema, seen_actions, as_of=as_of))

    if errors:
        print("CI supply-chain pin validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    next_due = min(date.fromisoformat(str(row["review_due_on"])) for row in inventory["pins"])
    print(
        "CI supply-chain pin validation passed: "
        f"{len(workflows)} workflows, {len(seen_actions)} governed actions, "
        f"1 commit-specific installer, review current through {next_due}, "
        "and 7 rejecting negative controls."
    )


if __name__ == "__main__":
    main()
