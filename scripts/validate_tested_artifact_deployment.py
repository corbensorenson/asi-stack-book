#!/usr/bin/env python3
"""Validate the tested-build to no-rebuild deployment workflow boundary."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / ".github" / "workflows" / "build-pages-artifact.yml"
DEPLOY = ROOT / ".github" / "workflows" / "publish.yml"

BUILD_REQUIRED = (
    "name: Build tested Pages artifact",
    "python3 scripts/run_validation_registry.py --tier deep",
    "cd lean && lake build",
    "quarto render --to html",
    "python3 scripts/build_tested_site_bundle.py --site _site --output build/pages-tested",
    'python3 scripts/validate_tested_site_bundle.py --bundle build/pages-tested --expected-commit "$GITHUB_SHA"',
    "name: pages-tested-${{ github.sha }}",
    "uses: actions/upload-artifact@",
)

DEPLOY_REQUIRED = (
    "workflow_run:",
    'workflows: ["Build tested Pages artifact"]',
    "github.event.workflow_run.conclusion == 'success'",
    "github.event.workflow_run.head_branch == 'main'",
    "ref: ${{ github.event.workflow_run.head_sha }}",
    "uses: actions/download-artifact@",
    "run-id: ${{ github.event.workflow_run.id }}",
    "name: pages-tested-${{ github.event.workflow_run.head_sha }}",
    'python3 scripts/validate_tested_site_bundle.py --bundle build/pages-tested --expected-commit "${{ github.event.workflow_run.head_sha }}"',
    "uses: actions/upload-pages-artifact@",
    "path: build/pages-tested/site",
    "uses: actions/deploy-pages@",
    "--url \"${{ needs.deploy.outputs.page_url }}\"",
)

DEPLOY_FORBIDDEN = (
    "quarto render",
    "lake build",
    "run_validation_registry.py",
    "build_tested_site_bundle.py",
    "sync_scaffold.py",
)


def validate_text(build: str, deploy: str) -> list[str]:
    errors: list[str] = []
    for fragment in BUILD_REQUIRED:
        if fragment not in build:
            errors.append(f"tested-build workflow missing: {fragment}")
    for fragment in DEPLOY_REQUIRED:
        if fragment not in deploy:
            errors.append(f"deployment workflow missing: {fragment}")
    for fragment in DEPLOY_FORBIDDEN:
        if fragment in deploy:
            errors.append(f"deployment workflow must not rebuild or revalidate source: {fragment}")
    if deploy.find("validate_tested_site_bundle.py") > deploy.find("upload-pages-artifact@"):
        errors.append("deployment must verify the downloaded bundle before Pages upload")
    return errors


def negative_controls(build: str, deploy: str) -> list[str]:
    failures: list[str] = []
    controls = {
        "deploy rebuild": (build, deploy + "\n      - run: quarto render\n"),
        "current-run artifact": (build, deploy.replace("run-id: ${{ github.event.workflow_run.id }}", "run-id: ${{ github.run_id }}", 1)),
        "unbound commit": (build, deploy.replace("--expected-commit \"${{ github.event.workflow_run.head_sha }}\"", "", 1)),
    }
    for label, (candidate_build, candidate_deploy) in controls.items():
        if not validate_text(candidate_build, candidate_deploy):
            failures.append(f"negative control was incorrectly accepted: {label}")
    return failures


def main() -> None:
    errors: list[str] = []
    for path in (BUILD, DEPLOY):
        if not path.exists():
            errors.append(f"missing {path.relative_to(ROOT)}")
    if errors:
        fail(errors)
    build = BUILD.read_text(encoding="utf-8", errors="ignore")
    deploy = DEPLOY.read_text(encoding="utf-8", errors="ignore")
    errors.extend(validate_text(build, deploy))
    errors.extend(negative_controls(build, deploy))
    fail(errors)
    print("Tested-artifact deployment validation passed: successful-run handoff, commit binding, no deploy rebuild, and 3 rejecting negative controls.")


def fail(errors: list[str]) -> None:
    if not errors:
        return
    print("Tested-artifact deployment validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


if __name__ == "__main__":
    main()
