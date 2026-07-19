# P2 Replacement Task Opening and Evaluator Calibration

Date: 2026-07-17  
State: **rank-one specs opened; independent evaluator calibrated; execution outcomes unopened**

After all four rank-one candidates passed provenance and image-resource gates,
their pinned dataset rows were opened. Every problem, solution patch, test
patch, command, base, image, license, and expected-test set matches its frozen
digest. Solution and test paths are disjoint. The four tasks bind 227 Rust,
6,209 Go, 60 Go, and 351 Java expected test identities.

The independent evaluator was implemented without importing the upstream parser.
It uses separate Cargo, Go, and Maven grammars and explicitly reports zero-exit
visible failure, nonzero-exit/no-status, and zero-exit/no-status conditions.
Calibration retained three failed attempts: a Maven counter-tuple defect, a
comma-boundary defect, and a `Running`-prefix slice defect. The corrected
evaluator then matched expected labels and the pinned upstream implementation
on all 12 authored controls and 20 historical raw logs (32/32 exact).

This calibration is necessary but not sufficient. Two parsers can share a
conceptual mistake, so candidate admission still requires exact expected-set
agreement, two paired repetitions, positive and negative controls, separated
dependency materialization, offline outcome execution, complete resource
monitoring, and raw-log custody. Candidate execution outcomes and the final
held-out pool remain unopened.

Machine records:

- `evidence_quality/p2_replacement_task_opening.json`
- `evidence_quality/p2_independent_test_log_evaluator_calibration.json`
- `evidence_quality/p2_independent_test_log_evaluator_calibration_attempt_001.json`
- `evidence_quality/p2_independent_test_log_evaluator_calibration_attempt_002_failed_30_of_32.json`
- `evidence_quality/p2_independent_test_log_evaluator_calibration_attempt_003_failed_31_of_32.json`
