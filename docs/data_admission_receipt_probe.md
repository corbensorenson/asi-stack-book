# Data-Admission Receipt Probe

Command: `python3 scripts/validate_data_admission_receipt_probe.py`

Result: `experiments/data_admission_receipt_probe/results/2026-07-10-local.json`

This deterministic, public-safe probe exercises four finite scenarios:
missing provenance routes to `block`, a missing contamination record routes to
`quarantine`, a missing deletion scope remains `experimental_only`, and a
complete record becomes receipt-eligible. It also rejects four expected-invalid controls:
treating missing provenance or contamination as eligible, treating a
missing deletion scope as ordinary eligibility, and using the record as a
support-state promotion.

The probe checks receipt-field routing only. It does not load or evaluate a
dataset; it does not train, update, or evaluate a model; it does not verify
semantic contamination absence; and it does not verify deletion from
checkpoints, adapters, caches, retrieval stores, or published artifacts.
Receipt eligibility therefore remains distinct from data quality, privacy,
continual-learning utility, verified unlearning, or the Data Engines chapter
core claim. The existing Lean theorems in `AsiStackProofs.DataEngines` provide
the same finite block, quarantine, and eligibility boundaries; neither layer
proves an open-world lifecycle result.
