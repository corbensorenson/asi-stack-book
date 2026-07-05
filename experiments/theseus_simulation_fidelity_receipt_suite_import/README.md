# Theseus Simulation-Fidelity Receipt Suite Import

This experiment records a sanitized public-safe import of the Project Theseus
simulation-fidelity receipt suite.

The tracked fixture stores digest, count, scenario, and boundary facts only. It
does not copy the raw Project Theseus report, private payloads, private paths,
prompts, tests, candidate traces, score labels, checkpoints, or training rows
into this public repository.

Run:

```bash
python3 scripts/validate_theseus_simulation_fidelity_receipt_suite_import.py --write-result
python3 scripts/validate_theseus_simulation_fidelity_receipt_suite_import.py
```

Boundary: this import supports only the bounded non-core claim
`resource-economics.simulation_fidelity_receipt_suite_import`. It does not
prove simulator adequacy, physical feasibility, benchmark transfer, native KV
parity, deployment readiness, live Project Theseus replay, model quality,
economic outcome, learned generation, safety, ASI, or any chapter core claim.
