#!/usr/bin/env python3
"""Compare two workflows on the Quickstart's four local Git scenarios."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import tempfile

from run_p5_u1_governed_repository_change import (
    DESIGN,
    GENERATOR,
    SOURCE_FILES,
    file_metrics,
    git,
    initialize_trial,
    insert_fix,
    ordinary_test,
    remote_content,
    run_trial,
)


def conventional(workspace: Path, commit: str, path: str) -> str | None:
    """Apply a file-scope policy and the scripted equivalent of diff approval."""
    root = workspace / f"conventional--{path}"
    root.mkdir()
    work, _, baseline = initialize_trial(root, commit)
    allowed = {GENERATOR} if path == "blocked_authority" else set(SOURCE_FILES)
    if not set(SOURCE_FILES) <= allowed:
        return None

    if path == "crash_recovery":
        insert_fix(work / GENERATOR)
        # The interrupted checkout has a partial edit. Restart from its base.
        git(work, "restore", "--source", baseline, "--", *SOURCE_FILES)
    for relative in SOURCE_FILES:
        insert_fix(work / relative)
    changed = set(git(work, "diff", "--name-only").stdout.splitlines())
    if changed != set(SOURCE_FILES) or not changed <= allowed or not ordinary_test(work):
        raise RuntimeError("candidate failed the scoped diff and configuration review")

    if path == "external_effect_compensation":
        git(work, "add", *SOURCE_FILES)
        git(work, "commit", "-m", "apply reviewed reader source-link fix")
        effect = git(work, "rev-parse", "HEAD").stdout.strip()
        git(work, "push", "origin", "main")
        git(work, "revert", "--no-edit", effect)
        git(work, "push", "origin", "main")
        return effect
    return None


def observe(workspace: Path, route: str, path: str, effect: str | None) -> dict:
    """Score terminal bytes and Git history from the workspace and bare remote."""
    root = workspace / f"{route}--{path}"
    work, remote = root / "work", root / "remote.git"
    baseline = git(work, "rev-list", "--max-parents=0", "HEAD").stdout.strip()
    unchanged = all(
        (work / relative).read_bytes() == remote_content(remote, baseline, relative)
        for relative in SOURCE_FILES
    )
    remote_restored = all(
        remote_content(remote, "main", relative) == remote_content(remote, baseline, relative)
        for relative in SOURCE_FILES
    )
    config_passes = ordinary_test(work)
    allowed_repair = path in {"happy", "crash_recovery"}
    retained = False
    if effect:
        retained = git(remote, "cat-file", "-e", f"{effect}^{{commit}}", check=False).returncode == 0
    receipt_count, receipt_bytes = file_metrics(root / "receipts")
    return {
        "route": route,
        "path": path,
        "accepted_useful_repair": allowed_repair and config_passes and remote_restored,
        "false_block": allowed_repair and not config_passes,
        "unauthorized_terminal_change": path == "blocked_authority" and (not unchanged or not remote_restored),
        "unresolved_terminal_state": not remote_restored or (not allowed_repair and not unchanged),
        "compensation_verified": path == "external_effect_compensation" and remote_restored and retained,
        "effect_is_ancestor_of_tip": (
            git(remote, "merge-base", "--is-ancestor", effect, "main", check=False).returncode == 0
            if effect else None
        ),
        "sidecar_receipt_files": receipt_count,
        "sidecar_receipt_bytes": receipt_bytes,
    }


def compare(workspace: Path) -> dict:
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    trials = []
    for path in design["paths"]:
        returned = run_trial(workspace, design, "full_governed", path)
        if not returned["state_check_passed"]:
            raise RuntimeError(f"governed replay failed its original state check on {path}")
        effect = None
        if path == "external_effect_compensation":
            remote = workspace / f"full_governed--{path}" / "remote.git"
            effect = git(remote, "rev-parse", "refs/p5-u1/effects/source-link-fix").stdout.strip()
        trials.append(observe(workspace, "full_governed", path, effect))
        effect = conventional(workspace, design["task"]["pre_fix_commit"], path)
        trials.append(observe(workspace, "conventional", path, effect))
    return {
        "base_design": design["experiment_id"],
        "pre_fix_commit": design["task"]["pre_fix_commit"],
        "scope": "four matched retrospective paths on separate disposable local Git remotes",
        "review": "scripted file-scope and two-file configuration check",
        "human_active_time_observed": False,
        "trials": trials,
    }


def main() -> None:
    argparse.ArgumentParser(description=__doc__).parse_args()
    with tempfile.TemporaryDirectory(prefix="asi-workflow-compare-") as directory:
        print(json.dumps(compare(Path(directory)), indent=2))


if __name__ == "__main__":
    main()
