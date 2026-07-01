# Project Theseus Generation Mode Import Fixtures

This directory contains the public-safe Project Theseus generation-mode gate
import lane used by `scripts/validate_theseus_generation_mode_import.py`.

- `fixtures/valid/generation_mode_gate_public_summary.valid.json` is the
  sanitized static import summary.
- `fixtures/invalid/*.invalid.json` are mutation controls that must be rejected.
- `results/2026-07-01-local.json` records the validator's expected public
  digest, generation-mode counts, negative comparison counts, and non-claim
  boundary.

The lane verifies a pinned report digest and summary contract. It does not
vendor Project Theseus, rerun the local generation-mode command, copy task
payloads or candidate outputs, promote a chapter core claim, or prove a
generation speed or quality result.
