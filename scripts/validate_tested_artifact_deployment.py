#!/usr/bin/env python3
"""Validate the tested-build to no-rebuild deployment workflow boundary."""

from __future__ import annotations

import sys
import shlex
from pathlib import Path
import yaml


ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / ".github" / "workflows" / "build-pages-artifact.yml"
DEPLOY = ROOT / ".github" / "workflows" / "publish.yml"

BUILD_REQUIRED = (
    "name: Build tested Pages artifact",
    "python3 scripts/run_validation_registry.py --tier deep",
    "cd lean && lake build",
    "python3 scripts/admission_guard.py --run quarto render --to html",
    "python3 scripts/admission_guard.py --run quarto render papers --to html",
    "python3 scripts/validate_paper_library.py --site _site",
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
    errors.extend(workflow_selection_errors(build, deploy))
    return errors


def workflow_selection_errors(build: str, deploy: str) -> list[str]:
    """Inspect executable step ownership; a matching comment cannot be a gate."""
    errors = []
    try:
        build_value, deploy_value = yaml.safe_load(build), yaml.safe_load(deploy)
        steps = deploy_value["jobs"]["deploy"]["steps"]
        build_steps = build_value["jobs"]["build"]["steps"]
        by_id = {step.get("id"): (index, step) for index, step in enumerate(steps) if step.get("id")}
        selection = by_id["selection"]
        final_selection = by_id["final-selection"]
        deployment = by_id["deployment"]
    except (yaml.YAMLError, KeyError, TypeError, AttributeError) as error:
        return [f"deployment selection structure is invalid: {error}"]
    if deploy_value.get("concurrency", {}).get("cancel-in-progress") is not False:
        errors.append("a late older completion must not cancel an active current deployment")
    for _, step in (selection, final_selection):
        command = step.get("run", "")
        if not command.startswith("python3 scripts/select_tested_site_deployment.py ") or '--candidate "${{ github.event.workflow_run.head_sha }}"' not in command or '--github-output "$GITHUB_OUTPUT"' not in command:
            errors.append("selection must invoke the exact candidate/main selector and publish its decision")
    if not selection[0] < final_selection[0] < deployment[0]:
        errors.append("candidate selection and final selection must precede deployment")
    if final_selection[1].get("if") != "steps.selection.outputs.eligible == 'true'":
        errors.append("final selection must be conditioned on initial eligibility")
    if deployment[1].get("if") != "steps.final-selection.outputs.eligible == 'true'":
        errors.append("deployment must consume the final eligibility decision")
    preparation = [index for index, step in enumerate(steps) if
                   any(action in step.get("uses", "") for action in ("download-artifact@", "upload-pages-artifact@"))
                   or "validate_tested_site_bundle.py" in step.get("run", "")]
    if len(preparation) != 3 or any(not selection[0] < index < final_selection[0] or steps[index].get("if") != "steps.selection.outputs.eligible == 'true'" for index in preparation):
        errors.append("download, verification and upload must all occur between eligibility checks")
    if deploy_value["jobs"].get("attest", {}).get("if") != "needs.deploy.outputs.page_url != ''":
        errors.append("a skipped deployment must not imply an attestation")
    render_steps = [step for step in build_steps if step.get("name") == "Render clean HTML"]
    guarded_renders = [
        ["python3", "scripts/admission_guard.py", "--run", "quarto", "render", "--to", "html"],
        ["python3", "scripts/admission_guard.py", "--run", "quarto", "render", "editions/reader_manuscript/current", "--to", "html"],
        ["python3", "scripts/admission_guard.py", "--run", "quarto", "render", "papers", "--to", "html"],
    ]
    try:
        lines = [shlex.split(line) for line in render_steps[0].get("run", "").splitlines() if line.strip()] if len(render_steps) == 1 else []
        actual = [line for line in lines if "quarto" in line and "render" in line]
    except ValueError:
        actual = []
    if (actual != guarded_renders or not render_steps or "if" in render_steps[0]
            or render_steps[0].get("continue-on-error", False)):
        errors.append("canonical renders must hold the source read lease and require failures")
    browser_steps = [step for step in build_steps if "validate_live_human_view_browser.js" in step.get("run", "")]
    expected_browser = [
        ["node", "scripts/validate_live_human_view_browser.js", "--strict", "--all-chapters", "--all-viewports"],
        ["python3", "scripts/validate_live_human_view_browser_report.py", "--site", "_site"],
    ]
    try:
        commands = [shlex.split(line) for line in browser_steps[0]["run"].splitlines() if line.strip()] if len(browser_steps) == 1 else []
    except ValueError:
        commands = []
    if (commands != expected_browser or browser_steps[0].get("continue-on-error", False)
            or "if" in browser_steps[0]):
        errors.append("publication must require the strict complete browser producer then its current-report consumer")
    elif any(index <= build_steps.index(browser_steps[0]) for index, step in enumerate(build_steps)
             if "build_tested_site_bundle.py" in step.get("run", "") or "upload-artifact@" in step.get("uses", "")
             and step.get("if") != "always()"):
        errors.append("browser report acceptance must precede bundling and artifact upload")
    return errors


def negative_controls(build: str, deploy: str) -> list[str]:
    failures: list[str] = []
    controls = {
        "deploy rebuild": (build, deploy + "\n      - run: quarto render\n"),
        "missing paper-library render": (build.replace("          python3 scripts/admission_guard.py --run quarto render papers --to html\n", "", 1), deploy),
        "unguarded canonical render": (build.replace("python3 scripts/admission_guard.py --run quarto render --to html", "quarto render --to html", 1), deploy),
        "decorative canonical render guard": (build.replace("python3 scripts/admission_guard.py --run quarto render --to html", "echo python3 scripts/admission_guard.py --run quarto render --to html", 1), deploy),
        "missing rendered paper validation": (build.replace("          python3 scripts/validate_paper_library.py --site _site\n", "", 1), deploy),
        "current-run artifact": (build, deploy.replace("run-id: ${{ github.event.workflow_run.id }}", "run-id: ${{ github.run_id }}", 1)),
        "unbound commit": (build, deploy.replace("--expected-commit \"${{ github.event.workflow_run.head_sha }}\"", "", 1)),
        "late-run cancellation": (build, deploy.replace("cancel-in-progress: false", "cancel-in-progress: true")),
        "ignored eligibility": (build, deploy.replace("if: steps.final-selection.outputs.eligible == 'true'", "if: always()")),
        "decorative selection": (build, deploy.replace("run: python3 scripts/select_tested_site_deployment.py", "run: echo python3 scripts/select_tested_site_deployment.py")),
        "optional browser": (build.replace("--strict --all-chapters --all-viewports", "--all-chapters --all-viewports"), deploy),
        "missing browser report": (build.replace("          python3 scripts/validate_live_human_view_browser_report.py --site _site\n", ""), deploy),
        "decorative browser report": (build.replace("          python3 scripts/validate_live_human_view_browser_report.py", "          echo python3 scripts/validate_live_human_view_browser_report.py"), deploy),
        "consumer before producer": (build.replace("          node scripts/validate_live_human_view_browser.js --strict --all-chapters --all-viewports\n          python3 scripts/validate_live_human_view_browser_report.py --site _site",
                                                      "          python3 scripts/validate_live_human_view_browser_report.py --site _site\n          node scripts/validate_live_human_view_browser.js --strict --all-chapters --all-viewports"), deploy),
        "conditional browser": (build.replace("      - name: Browser-smoke live Human view\n", "      - name: Browser-smoke live Human view\n        if: 'false'\n"), deploy),
        "ignored browser report failure": (build.replace("      - name: Browser-smoke live Human view\n", "      - name: Browser-smoke live Human view\n        continue-on-error: true\n"), deploy),
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
    print("Tested-artifact deployment validation passed: successful-run handoff, exact-main selection, guarded renders, strict browser/report gates, commit binding, no deploy rebuild, and 16 rejecting negative controls.")


def fail(errors: list[str]) -> None:
    if not errors:
        return
    print("Tested-artifact deployment validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


if __name__ == "__main__":
    main()
