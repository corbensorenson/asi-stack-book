#!/usr/bin/env python3
"""Reject mutable, unregistered, or stale-reviewed CI dependencies."""

from __future__ import annotations

import copy
from datetime import date, datetime, timedelta, timezone
import json
import os
import re
import sys
from pathlib import Path

from build_canonical_public_status import validate_against_schema
from install_lean_runtime import binary_record


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_DIR = ROOT / ".github" / "workflows"
LOCAL_ACTION_DIR = ROOT / ".github" / "actions"
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
        return datetime.now(timezone.utc).date()
    if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", raw):
        raise ValueError("ASI_PIN_REVIEW_AS_OF must be YYYY-MM-DD")
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
    # Semantic consumers must not coerce or dereference rejected shapes.
    if errors:
        return errors
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
    try:
        binary_record(data)
    except (KeyError, TypeError, ValueError) as error:
        errors.append(f"governed Elan runtime binary is invalid: {error}")

    for row in pins:
        if not isinstance(row, dict):
            continue
        label = str(row.get("id", "unknown"))
        try:
            reviewed = date.fromisoformat(str(row.get("reviewed_on", "")))
            due = date.fromisoformat(str(row.get("review_due_on", "")))
            if reviewed.isoformat() != row["reviewed_on"] or due.isoformat() != row["review_due_on"]:
                raise ValueError("noncanonical review date")
        except ValueError:
            errors.append(f"{label}: reviewed_on and review_due_on must be YYYY-MM-DD ISO dates")
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
            if row.get("runtime_binary") is not None:
                errors.append(f"{label}: runtime binary belongs to the Elan installer owner")
        elif row.get("kind") == "commit_url_installer":
            if label != f"commit-url-installer:{row.get('repository')}":
                errors.append(f"{label}: installer ID must derive from repository")
            if f"/{pin}/" not in str(row.get("artifact_url", "")):
                errors.append(f"{label}: installer URL is not bound to its recorded commit")
            digest = str(row.get("artifact_sha256", ""))
            if not re.fullmatch(r"[0-9a-f]{64}", digest):
                errors.append(f"{label}: installer artifact SHA-256 is missing or malformed")
            try:
                observed = date.fromisoformat(row["runtime_binary"]["observed_on"])
                if observed.isoformat() != row["runtime_binary"]["observed_on"]:
                    raise ValueError("noncanonical binary observation date")
                if observed > as_of:
                    errors.append(f"{label}: runtime binary observation is in the future")
            except (KeyError, ValueError, TypeError):
                errors.append(f"{label}: runtime binary observation date is missing or invalid")
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
    if "elan-init.sh" in text or elan_refs or "/releases/latest/" in text:
        errors.append(f"{label}: moving Elan shell/binary installation is forbidden; use the governed archive helper")
    if "install_lean_runtime.py" in text:
        if 'python3 scripts/install_lean_runtime.py --install --elan-home "$HOME/.elan"' not in text:
            errors.append(f"{label}: Elan must use the governed helper with its explicit CI tool home")
        if not installer.get("runtime_binary"):
            errors.append(f"{label}: runtime helper lacks a governed archive inventory")
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
        f"`{installer.get('runtime_binary', {}).get('version', '')}`",
        "retained review context",
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
    first_action = next(
        REMOTE_ACTION_RE.fullmatch(target).group("action")
        for target in USES_RE.findall(publish_text)
        if REMOTE_ACTION_RE.fullmatch(target)
        and REMOTE_ACTION_RE.fullmatch(target).group("action") in action_pins
    )
    controls = {
        "moving action tag": publish_text.replace(
            f"{first_action}@{action_pins[first_action]}",
            f"{first_action}@v4",
            1,
        ),
        "moving binary installer": publish_text + '\nrun: curl https://github.com/leanprover/elan/releases/latest/download/elan.tar.gz\n',
        "uncontrolled runtime helper": publish_text.replace(' --install --elan-home "$HOME/.elan"', ' --install', 1),
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
    next(row for row in mismatched["pins"] if row["repository"] == first_action)["pin"] = "0" * 40
    bad_actions, bad_installer = inventory_values(mismatched)
    if not validate_workflow_text("negative control: mismatched inventory pin", publish_text, bad_actions, bad_installer):
        failures.append("negative control was incorrectly accepted: mismatched inventory pin")

    duplicate = copy.deepcopy(inventory)
    duplicate["pins"].append(copy.deepcopy(duplicate["pins"][0]))
    if not validate_inventory(duplicate, schema, as_of=as_of):
        failures.append("negative control was incorrectly accepted: duplicate inventory ID")
    for name, mutate in [
        ("missing runtime binary", lambda row: row.pop("runtime_binary")),
        ("mutable binary URL", lambda row: row["runtime_binary"]["artifacts"][0].update(url="https://github.com/leanprover/elan/releases/latest/download/elan.tar.gz")),
        ("erased binary digest", lambda row: row["runtime_binary"]["artifacts"][0].update(sha256="")),
        ("duplicate binary platform", lambda row: row["runtime_binary"]["artifacts"][1].update(target=row["runtime_binary"]["artifacts"][0]["target"])),
    ]:
        candidate = copy.deepcopy(inventory)
        mutate(next(row for row in candidate["pins"] if row["repository"] == "leanprover/elan"))
        if not validate_inventory(candidate, schema, as_of=as_of):
            failures.append(f"negative control was incorrectly accepted: {name}")
    return failures


def main() -> None:
    errors: list[str] = []
    workflows = sorted((*WORKFLOW_DIR.glob("*.yml"), *WORKFLOW_DIR.glob("*.yaml")))
    local_actions = sorted((*LOCAL_ACTION_DIR.rglob("action.yml"), *LOCAL_ACTION_DIR.rglob("action.yaml")))
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
        as_of = datetime.now(timezone.utc).date()
    inventory_errors = validate_inventory(inventory, schema, as_of=as_of)
    errors.extend(inventory_errors)
    if inventory_errors:
        print("CI supply-chain pin validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)
    action_pins, installer = inventory_values(inventory)

    workflow_texts: dict[str, str] = {}
    seen_actions: set[str] = set()
    for path in [*workflows, *local_actions]:
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

    installer_workflows = [text for text in workflow_texts.values() if "install_lean_runtime.py" in text]
    if len(installer_workflows) != 1:
        errors.append(f"expected exactly one CI definition owning the Elan installer, found {len(installer_workflows)}")
    else:
        if not errors:
            errors.extend(run_negative_controls(installer_workflows[0], inventory, schema, seen_actions, as_of=as_of))

    if errors:
        print("CI supply-chain pin validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    next_due = min(date.fromisoformat(str(row["review_due_on"])) for row in inventory["pins"])
    print(
        "CI supply-chain pin validation passed: "
        f"{len(workflows)} workflows, {len(local_actions)} local actions, {len(seen_actions)} governed actions, "
        f"1 versioned/digest-bound installer with retained source context, review current through {next_due}, "
        "and 11 rejecting negative controls; fresh Linux qualification remains pending."
    )


if __name__ == "__main__":
    main()
