# Project Theseus Import Fixtures

This directory contains the public-safe Project Theseus report import lane used
by `scripts/validate_theseus_report.py`.

- `fixtures/valid/architecture_gate_public_report.valid.json` is the sanitized
  static import report.
- `fixtures/invalid/*.invalid.json` are mutation controls that must be rejected.
- `results/2026-06-29-local.json` records the validator's expected public
  digest, gate count, and non-claim boundary.

The lane verifies a pinned report digest and schema contract. It does not vendor
Project Theseus, rerun its local commands, promote a chapter core claim, or copy
private training data, checkpoints, traces, prompts, or benchmark payloads.
