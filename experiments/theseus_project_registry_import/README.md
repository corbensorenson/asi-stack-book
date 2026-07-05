# Theseus Project Registry Import

This experiment records one sanitized public-safe Project Theseus project-registry
health import from the local `Theseus-Hive` checkout at commit `1ad88a22`.

The fixture intentionally imports only summary counts, source digests, claim
boundaries, and non-claims. It does not copy the raw registry report, private
paths, prompts, tests, traces, candidate code, checkpoints, training rows, or
any private payload into this public repository.

Validate with:

```bash
python3 scripts/validate_theseus_project_registry_import.py
```
