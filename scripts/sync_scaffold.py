#!/usr/bin/env python3
"""Synchronize the Quarto living-book scaffold from inventory metadata.

This script intentionally does not ingest source documents or mark any tests as
passed. It only turns the handoff outline and source inventory into explicit
book structure.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TODAY = "2026-06-24"

SOURCE_INVENTORY = ROOT / "sources" / "source_inventory.json"


CHAPTERS = [
    {
        "num": "01",
        "file": "chapters/01_asi_is_a_stack.qmd",
        "title": "ASI Is a Stack, Not a Model",
        "problem": "The book needs a single architecture frame for AI systems that must plan, remember, verify, act, route work, and improve without collapsing into one opaque model.",
        "insufficient": "A larger model alone does not define authority boundaries, memory governance, evidence ledgers, tool permissions, or safe replacement rules.",
        "claim": "Efficient ASI should be modeled as a governed stack of cooperating layers rather than as a single undifferentiated model.",
        "mechanism": [
            "Name each layer of the stack and its responsibility.",
            "Treat boundaries, interfaces, and evidence states as first-class design objects.",
            "Use the rest of the book to refine each layer into testable mechanisms.",
        ],
        "interfaces": [
            "Alignment constrains admissible goals.",
            "Governance bounds authority and self-modification.",
            "Planning, memory, reasoning, execution, routing, compression, and evidence layers exchange typed artifacts.",
        ],
        "invariants": [
            "Layer boundaries remain explicit.",
            "Claims carry support states.",
            "Execution authority is not implied by reasoning ability.",
        ],
        "failure_modes": [
            "Anthology drift: source papers remain isolated instead of becoming one architecture.",
            "Monolith drift: layer responsibilities are folded back into model scale.",
            "Evidence drift: conceptual claims are presented as tested claims.",
        ],
        "minimal": "A diagrammed stack, chapter map, source crosswalk, and claim/evidence matrix that keep responsibilities separable.",
        "sources": ["viea", "beastbrain", "aletheia", "moecot", "talos"],
        "tests": [
            "Full-stack traceability review",
            "Layer-boundary audit",
            "Claim-support label audit",
        ],
    },
    {
        "num": "02",
        "file": "chapters/02_efficient_asi_hypothesis.qmd",
        "title": "The Efficient ASI Hypothesis",
        "problem": "The book needs a non-scale-only theory for why a governed ASI stack could become more capable without requiring every task to use maximal cognition.",
        "insufficient": "Parameter count does not by itself explain routing, context selectivity, procedural memory, compression, verification, or runtime targeting.",
        "claim": "Efficient ASI is a design hypothesis: capability improves when cognition is routed, compressed, reused, governed, and tested.",
        "mechanism": [
            "Route subtasks to the smallest adequate specialist.",
            "Preserve reusable work as artifacts, tools, and procedural memory.",
            "Track residual burden when compression or routing leaves unresolved work.",
        ],
        "interfaces": [
            "Planning requests minimum viable intelligence.",
            "Routing selects specialists and tools.",
            "Evidence layers decide whether efficiency claims are supported.",
        ],
        "invariants": [
            "Efficiency claims require measured task quality and cost.",
            "Compression must expose residuals instead of hiding them.",
            "Fallback paths remain available when lightweight routes fail.",
        ],
        "failure_modes": [
            "Treating cheap inference as sufficient evidence of intelligence.",
            "Compressing away critical context.",
            "Optimizing benchmark scores while increasing hidden residual burden.",
        ],
        "minimal": "A costed task-routing model with explicit fallback, residual accounting, and benchmark gates.",
        "sources": ["viea", "moecot", "rmi", "cgs", "rankfold_neuralfold", "bbvca_v9", "simulation_scaling"],
        "tests": [
            "Minimum viable intelligence routing test",
            "Residual burden accounting test",
            "Compression utility preservation test",
        ],
    },
    {
        "num": "03",
        "file": "chapters/03_failure_modes.qmd",
        "title": "Failure Modes of Ungoverned Intelligence",
        "problem": "The architecture needs an explicit failure model before it can claim governance, reliability, or safe improvement.",
        "insufficient": "High-level safety language misses earlier engineering failures such as goal misbinding, context corruption, authority creep, evaluator drift, and unverified claims.",
        "claim": "Ungoverned intelligence fails through stack-level breakdowns before any dramatic science-fiction failure mode is needed.",
        "mechanism": [
            "Classify failures by layer.",
            "Map each failure to an invariant and a planned falsification test.",
            "Use failures to constrain later architecture choices.",
        ],
        "interfaces": [
            "Governance limits authority creep.",
            "VCM limits context pollution.",
            "Verification limits false certainty.",
            "Execution layers limit side effects.",
        ],
        "invariants": [
            "Authority must be explicit and bounded.",
            "Evidence records must be auditable.",
            "Self-modification cannot bypass identity and evaluator checks.",
        ],
        "failure_modes": [
            "Evaluator capture or drift.",
            "Memory poisoning and context pollution.",
            "Tool/action overreach.",
            "Compression that hides residual complexity.",
        ],
        "minimal": "A failure taxonomy tied to chapter-specific invariants and planned tests.",
        "sources": ["scf", "vcm_public", "talos", "spinoza", "field_of_god", "viea"],
        "tests": [
            "Authority creep scenario",
            "Context pollution scenario",
            "Evaluator drift scenario",
            "Unverified-claim scenario",
        ],
    },
    {
        "num": "04",
        "file": "chapters/04_alignment_constitution.qmd",
        "title": "Alignment and Constitution",
        "problem": "A self-improving system needs a stable moral and interpretive substrate before planning and execution can be trusted.",
        "insufficient": "Reactive refusal rules do not define value continuity, corrigibility, moral uncertainty, anti-domination, or self-modification ethics.",
        "claim": "The alignment layer should act as a constitutional substrate that constrains goals, plans, and self-modification.",
        "mechanism": [
            "Represent constitutional commitments as constraints on planning and execution.",
            "Track unresolved moral uncertainty instead of hiding it.",
            "Keep philosophical claims engineering-compatible and explicitly labeled.",
        ],
        "interfaces": [
            "Planning receives admissible-goal constraints.",
            "Governance receives authority and dignity constraints.",
            "Verification checks whether claims exceed the constitutional evidence state.",
        ],
        "invariants": [
            "Human dignity and agency preservation remain visible requirements.",
            "Corrigibility cannot be optimized away by self-improvement.",
            "Speculative metaphysical material remains labeled as speculative.",
        ],
        "failure_modes": [
            "Power without care.",
            "Mystical framing replacing technical constraints.",
            "Self-modification that weakens constitutional commitments.",
        ],
        "minimal": "A compact constitution appendix, conflict taxonomy, and planned scenario tests.",
        "sources": ["alignment_field", "field_of_god", "ethica_mechanica", "eternal_code", "coherence_exchange"],
        "tests": [
            "Constitutional consistency test",
            "Value conflict classification test",
            "Self-modification ethics scenario",
            "Power-seeking and agency-dominance scenario",
        ],
    },
    {
        "num": "05",
        "file": "chapters/05_governance_and_scf.qmd",
        "title": "Governance and Stable Capability Fields",
        "problem": "The stack needs a way to improve components while preserving identity, bounded authority, route validity, and evaluator integrity.",
        "insufficient": "Ordinary plugin replacement does not define qualified implementation replacement, authority ceilings, mutation tests, or rollback.",
        "claim": "Governed self-improvement requires stable capability fields: stable semantic boundaries with replaceable implementations and bounded authority.",
        "mechanism": [
            "Define field identity separately from implementation.",
            "Require qualification evidence before replacement.",
            "Track route validity, authority ceilings, and rollback conditions.",
        ],
        "interfaces": [
            "Planning may request field capabilities.",
            "Execution may invoke only authorized routes.",
            "Evidence layers record qualification and regression results.",
        ],
        "invariants": [
            "Implementation replacement cannot expand authority by default.",
            "Evaluator integrity must be protected from the field being evaluated.",
            "Rollback remains available after failed mutation.",
        ],
        "failure_modes": [
            "Authority escalation during replacement.",
            "Evaluator capture.",
            "Field identity drift.",
        ],
        "minimal": "A field schema with qualification predicates, route validity checks, authority ceilings, and rollback metadata.",
        "sources": ["scf", "talos", "ladon_manhattan", "viea", "moecot"],
        "tests": [
            "Qualification predicate test",
            "Route validity test",
            "Authority non-escalation test",
            "Mutation test",
            "Rollback and recovery test",
        ],
    },
    {
        "num": "06",
        "file": "chapters/06_planning_and_control.qmd",
        "title": "Planning and Control",
        "problem": "Goals need to become governed task graphs with dependencies, budgets, risk limits, tool choices, and stopping conditions.",
        "insufficient": "Planning cannot be collapsed into memory, reasoning, or execution because each layer has different authority and failure modes.",
        "claim": "Planning is a separate control layer that converts goals into governed action without owning memory, reasoning, or side effects.",
        "mechanism": [
            "Compile goals into strategic and tactical plans.",
            "Represent dependencies, constraints, context requests, and runtime replanning triggers.",
            "Delegate execution through governed contracts.",
        ],
        "interfaces": [
            "Alignment filters goals.",
            "VCM supplies context packets.",
            "Routers select specialists.",
            "Talos-like execution systems run typed jobs.",
        ],
        "invariants": [
            "Plans expose constraints and stopping conditions.",
            "Runtime replanning preserves original authority limits.",
            "Tool selection is justified by task requirements.",
        ],
        "failure_modes": [
            "Scope creep.",
            "Planning without replanning.",
            "Tool selection that exceeds authority or budget.",
        ],
        "minimal": "A task graph format with dependencies, constraints, context requests, risk budgets, and stop conditions.",
        "sources": ["planforge", "planforge_compiler_arch", "cognitive_compilation", "viea", "software_magic_grimoire", "moecot"],
        "tests": [
            "Decomposition accuracy test",
            "Dependency ordering test",
            "Constraint preservation test",
            "Runtime replanning test",
            "Tool selection test",
            "Budget and risk allocation test",
            "Scope creep prevention test",
        ],
    },
    {
        "num": "07",
        "file": "chapters/07_virtual_context_memory.qmd",
        "title": "Virtual Context Memory",
        "problem": "Long-horizon agents need selected, governed, evidence-carrying context rather than a flat transcript.",
        "insufficient": "Long context windows and ordinary retrieval do not automatically preserve authority labels, source fidelity, adequacy, or planner-guided relevance.",
        "claim": "Virtual Context Memory should compile active context packets from durable memory using evidence, authority labels, and planner requests.",
        "mechanism": [
            "Separate durable memory from active context.",
            "Build context packets with summaries, handles, provenance, and adequacy status.",
            "Expose unsafe, unknown, or unsatisfied context states.",
        ],
        "interfaces": [
            "Planning requests context.",
            "Verification checks source and summary fidelity.",
            "Execution receives only context appropriate to its authority.",
        ],
        "invariants": [
            "Authority labels survive summarization.",
            "Context adequacy is distinct from context admission.",
            "Summaries carry provenance and open uncertainty.",
        ],
        "failure_modes": [
            "Context pollution.",
            "Summary overconfidence.",
            "Privacy or behavioral authority leakage.",
        ],
        "minimal": "A context packet schema with source handles, authority labels, summary proofs, adequacy status, and planned fidelity tests.",
        "sources": ["vcm_public", "vcm_editable", "context_engineer", "black_hole_context_manager", "verification_bandwidth", "moecot"],
        "tests": [
            "Context packet adequacy test",
            "Distractor resistance test",
            "Authority label preservation test",
            "Proof-carrying summary fidelity test",
            "Planner-guided prefetch accuracy test",
            "Privacy and behavioral authority check",
        ],
    },
    {
        "num": "08",
        "file": "chapters/08_labor_execution_os.qmd",
        "title": "Labor and Execution OS",
        "problem": "Reasoning must become typed work with artifacts, permissions, audit logs, and governed side effects.",
        "insufficient": "A generic agent loop does not provide typed job lifecycle, replay, artifact graph discipline, or human approval gates.",
        "claim": "The execution layer should convert plans into typed jobs and artifacts through a governed labor operating system.",
        "mechanism": [
            "Compile command contracts into jobs.",
            "Run jobs through adapters with permissions and audit logs.",
            "Promote repeated workflows into verified tools when evidence supports it.",
        ],
        "interfaces": [
            "Planning emits job contracts.",
            "Governance enforces authority and approvals.",
            "Evidence layers reconstruct audit trails and replay results.",
        ],
        "invariants": [
            "Side effects pass through explicit authorization.",
            "Artifacts are addressable and auditable.",
            "Human approval gates remain enforceable.",
        ],
        "failure_modes": [
            "Tool misuse.",
            "Unlogged side effects.",
            "Workflow-to-tool promotion without evidence.",
        ],
        "minimal": "A typed job schema, artifact graph, permission model, audit log, and replay protocol.",
        "sources": ["talos", "talos_md", "viea", "genesiscode", "software_magic_grimoire", "cognitive_loop_closure", "moecot"],
        "tests": [
            "Typed job lifecycle test",
            "Tool permission enforcement test",
            "Audit log reconstruction test",
            "Replay determinism test",
            "Human approval gate test",
            "Adversarial job injection test",
        ],
    },
    {
        "num": "09",
        "file": "chapters/09_reasoning_verification.qmd",
        "title": "Reasoning, Verification, and Epistemology",
        "problem": "The stack needs explicit claim states, belief revision, uncertainty, and verification loops rather than fluent generation alone.",
        "insufficient": "Generated text can be coherent without being grounded, checked, calibrated, or fit for high-risk action.",
        "claim": "Reasoning and verification should maintain claim records with evidence tiers, contradiction handling, and calibrated uncertainty.",
        "mechanism": [
            "Extract claims from plans, context, and outputs.",
            "Assign support states and evidence tiers.",
            "Revise beliefs when contradiction or stronger evidence appears.",
        ],
        "interfaces": [
            "VCM supplies provenance.",
            "Planning and execution request verification before high-risk steps.",
            "Evidence matrices expose support state to readers and systems.",
        ],
        "invariants": [
            "Unsupported claims remain labeled.",
            "Contradictions are tracked instead of silently overwritten.",
            "High-risk domains pay a verification tax.",
        ],
        "failure_modes": [
            "False verification.",
            "Silence failure when evidence is insufficient.",
            "Evaluator or citation drift.",
        ],
        "minimal": "A claim ledger with support states, source handles, uncertainty, contradiction links, and review status.",
        "sources": ["spinoza", "uat", "coherence_exchange", "verification_bandwidth", "treellm", "viea"],
        "tests": [
            "Claim extraction test",
            "Contradiction detection test",
            "Belief revision test",
            "Evidence tier assignment test",
            "Uncertainty calibration test",
            "Insufficient-evidence silence test",
        ],
    },
    {
        "num": "10",
        "file": "chapters/10_routing_modular_intelligence.qmd",
        "title": "Routing and Modular Intelligence",
        "problem": "The stack needs to assign work across bounded specialists while preserving permissions, readiness, and regression history.",
        "insufficient": "One undifferentiated system cannot cleanly express specialist capability, local memory, readiness gates, quarantine, or residual escrow.",
        "claim": "ASI scales by routing across bounded specialist modules with explicit readiness gates and benchmark-driven promotion.",
        "mechanism": [
            "Use lightweight routing heads to select specialist cores.",
            "Track residuals, benchmark frontiers, and regression suites.",
            "Split, merge, retire, or quarantine modules based on evidence.",
        ],
        "interfaces": [
            "Planning asks for capability.",
            "Governance bounds route authority.",
            "Evidence layers decide readiness and promotion.",
        ],
        "invariants": [
            "Specialist authority is local and explicit.",
            "Promotion requires benchmark and regression evidence.",
            "Residuals are recorded instead of hidden.",
        ],
        "failure_modes": [
            "Wrong specialist selection.",
            "Premature promotion.",
            "Regression loss after module replacement.",
        ],
        "minimal": "A router registry with capability metadata, readiness gates, residual escrow, and regression preservation hooks.",
        "sources": ["octopus_router", "rmi", "moecot", "beastbrain", "cognitive_loop_closure", "benchmaxxing"],
        "tests": [
            "Specialist routing accuracy test",
            "Readiness gate enforcement test",
            "Benchmark promotion test",
            "Quarantine behavior test",
            "Regression preservation test",
            "Residual escrow integrity test",
        ],
    },
    {
        "num": "11",
        "file": "chapters/11_compression_representation.qmd",
        "title": "Compression and Representation",
        "problem": "The architecture needs ways to preserve useful generative structure while reducing surface detail, cost, and memory burden.",
        "insufficient": "Compression can appear efficient while discarding critical semantics, increasing residual burden, or harming downstream utility.",
        "claim": "Compression is a first-class stack layer only when it exposes residual burden, fallback paths, and downstream utility tests.",
        "mechanism": [
            "Separate semantic, model, memory, artifact, and representation compression.",
            "Use generate-verify-repair loops where reconstruction matters.",
            "Route to fallback systems when probes show compression is inadequate.",
        ],
        "interfaces": [
            "VCM compresses context with evidence.",
            "Routing selects compressed or full specialists.",
            "Evidence tests reconstruction quality and utility.",
        ],
        "invariants": [
            "Lossy claims remain labeled.",
            "Residual burden is visible.",
            "Fallback is available when compressed representations fail.",
        ],
        "failure_modes": [
            "Hidden residual complexity.",
            "False lossless claims.",
            "Latency or utility regressions after compression.",
        ],
        "minimal": "A compression ledger with description cost, residual burden, reconstruction checks, and fallback criteria.",
        "sources": ["cgs", "rgs", "rankfold_neuralfold", "rankfold_compressor", "bbvca_v9", "bbvca_main", "bugbrain", "simulation_scaling"],
        "tests": [
            "Reconstruction quality test",
            "Residual burden test",
            "Probe-and-route fallback test",
            "Compression ratio test",
            "Latency cost test",
            "Downstream utility preservation test",
        ],
    },
    {
        "num": "12",
        "file": "chapters/12_mathematical_search_substrates.qmd",
        "title": "Mathematical and Search Substrates",
        "problem": "Exploratory representations may improve search, routing, or compression, but the book needs to keep these hypotheses falsifiable.",
        "insufficient": "Novel mathematical substrates can become overclaimed if they are not tied to tests, baselines, and failure criteria.",
        "claim": "Alternative substrates belong in the stack only as testable implementation hypotheses until evidence supports them.",
        "mechanism": [
            "Frame coil, calculus, and geometric representations as optional specialist substrates.",
            "Define what they would need to improve.",
            "Specify falsification tests before adoption into core architecture.",
        ],
        "interfaces": [
            "Routing can treat a substrate as a specialist core.",
            "Compression can test representation efficiency.",
            "Evidence layers compare against baselines.",
        ],
        "invariants": [
            "Exploratory claims stay exploratory.",
            "Performance claims require measured baselines.",
            "Failed hypotheses remain recorded.",
        ],
        "failure_modes": [
            "Overclaiming performance.",
            "Using opaque math as authority.",
            "Adopting a substrate without regression tests.",
        ],
        "minimal": "A technical appendix and experiment plan with baseline comparisons and adoption gates.",
        "sources": ["coilmoecot", "temporal_coil_research", "cognitive_compilation", "genesiscode", "viea"],
        "tests": [
            "Baseline search comparison",
            "Representation efficiency test",
            "GPU parallelization feasibility test",
            "Failure-case and falsification review",
        ],
    },
    {
        "num": "13",
        "file": "chapters/13_evidence_benchmarks.qmd",
        "title": "Evidence, Benchmarks, and Ratchets",
        "problem": "A living architecture needs a way to move claims from speculative to tested without Goodharting or losing regressions.",
        "insufficient": "Benchmarks alone can be saturated, gamed, or disconnected from source claims and real-world requirements.",
        "claim": "The book should maintain evidence ratchets that connect claims, tests, residuals, regressions, and release history.",
        "mechanism": [
            "Track benchmark frontiers and mastery thresholds.",
            "Create residual escrow when tests reveal incomplete capability.",
            "Preserve regressions and hidden checks to reduce Goodhart pressure.",
        ],
        "interfaces": [
            "Every chapter contributes claims.",
            "Experiments produce evidence records.",
            "Changelog entries record evidence-state movement.",
        ],
        "invariants": [
            "No test success is claimed without execution.",
            "Synthetic and empirical evidence remain distinct.",
            "Negative or inconclusive results remain visible.",
        ],
        "failure_modes": [
            "Benchmark overfitting.",
            "Regression deletion.",
            "Claim support inflation.",
        ],
        "minimal": "A claim/evidence matrix, test spec appendix, and release checklist.",
        "sources": ["benchmaxxing", "moecot", "rmi", "cognitive_loop_closure", "road_to_agi", "viea", "tokenmana"],
        "tests": [
            "Saturation detection test",
            "Hidden benchmark transfer test",
            "Regression generation test",
            "Anti-Goodhart check",
            "Residual backlog integrity test",
        ],
    },
    {
        "num": "14",
        "file": "chapters/14_integrated_reference_architecture.qmd",
        "title": "Integrated Reference Architecture",
        "problem": "Readers need to see the whole machine from user intent to governed action and evidence-updated self-improvement.",
        "insufficient": "Layer descriptions can still feel disconnected unless the book walks through the complete control flow.",
        "claim": "The stack can be specified as an integrated reference architecture with typed handoffs between layers.",
        "mechanism": [
            "Trace user intent through constitution, governance, planning, VCM, routing, verification, execution, evidence, and improvement gates.",
            "Show which artifact each layer emits.",
            "Identify where authority can stop or reroute the process.",
        ],
        "interfaces": [
            "All stack layers participate.",
            "Artifacts and evidence ledgers provide continuity.",
            "SCF-style gates control improvement.",
        ],
        "invariants": [
            "No layer silently bypasses governance.",
            "Artifacts remain traceable.",
            "Self-improvement follows evidence and authority gates.",
        ],
        "failure_modes": [
            "Untraceable handoffs.",
            "Planning/execution collapse.",
            "Self-improvement without evaluator integrity.",
        ],
        "minimal": "A reference flow diagram, interface table, and end-to-end trace example marked conceptual until implemented.",
        "sources": ["viea", "moecot", "scf", "vcm_public", "planforge", "talos", "spinoza", "alignment_field", "octopus_router", "rmi", "benchmaxxing"],
        "tests": [
            "End-to-end intent trace test",
            "Artifact continuity audit",
            "Authority stop-condition test",
            "Evidence-ledger update test",
        ],
    },
    {
        "num": "15",
        "file": "chapters/15_prototype_roadmap.qmd",
        "title": "Prototype Roadmap",
        "problem": "The architecture needs a build sequence that prevents self-improvement features from arriving before evaluator and governance integrity.",
        "insufficient": "A roadmap that jumps straight to autonomous improvement would skip artifact memory, tests, claim ledgers, and authority controls.",
        "claim": "The prototype should grow in staged increments from artifact graph to governed capability replacement.",
        "mechanism": [
            "Begin with source matrix, artifact graph, and claim ledger.",
            "Add planner, VCM, typed execution, verification, benchmark ratchets, and SCF gates in order.",
            "Delay recursive self-improvement until evaluator and governance checks are credible.",
        ],
        "interfaces": [
            "Each phase unlocks a later layer.",
            "Evidence gates decide promotion.",
            "Changelog and release tags document progress.",
        ],
        "invariants": [
            "Roadmap phases have acceptance criteria.",
            "Self-improvement is gated by evaluator integrity.",
            "Compression and procedural memory are optimized after correctness scaffolds exist.",
        ],
        "failure_modes": [
            "Building agency before auditability.",
            "Skipping verification because prototypes appear useful.",
            "Treating roadmap milestones as test results.",
        ],
        "minimal": "A phase table with deliverables, acceptance gates, and blocked dependencies.",
        "sources": ["moecot", "viea", "road_to_agi", "benchmaxxing", "scf", "vcm_public", "planforge", "beastbrain"],
        "tests": [
            "Phase acceptance checklist",
            "Dependency gate review",
            "Prototype evidence-state audit",
            "Rollback readiness review",
        ],
    },
    {
        "num": "16",
        "file": "chapters/16_living_book_methodology.qmd",
        "title": "Living Book Methodology",
        "problem": "The book itself must stay current while preserving source traceability, claim states, tests, release history, and reader orientation.",
        "insufficient": "A static anthology cannot show evidence movement, deprecations, source updates, or reproducible renders.",
        "claim": "The living book should model the ASI stack discipline through Quarto source, inventories, evidence matrices, tests, changelogs, and releases.",
        "mechanism": [
            "Use Quarto as the canonical source of truth.",
            "Use a public static site for rendered reading.",
            "Require every meaningful update to touch the relevant chapter, source matrix, evidence matrix, and changelog.",
        ],
        "interfaces": [
            "Source ingestion feeds source notes.",
            "Drafting feeds claim matrices.",
            "Tests feed evidence-state changes.",
            "Releases feed the public site and changelog.",
        ],
        "invariants": [
            "No fabricated source content.",
            "No fabricated test results.",
            "Deprecated claims remain visible with reasons.",
        ],
        "failure_modes": [
            "Public site diverges from Quarto source.",
            "Changelog omits evidence-state changes.",
            "Readers cannot tell which claims are speculative.",
        ],
        "minimal": "A Quarto repo, GitHub Pages workflow, source inventory, claim/evidence matrix, validation script, and release checklist.",
        "sources": ["road_to_agi", "benchmaxxing", "viea"],
        "tests": [
            "Quarto render check",
            "Validation script check",
            "Claim/evidence consistency check",
            "Changelog update check",
        ],
    },
]


GLOSSARY = [
    ("ASI stack", "A proposed governed cognitive architecture made of alignment, governance, planning, memory, reasoning, execution, routing, compression, evidence, and improvement layers."),
    ("Alignment and constitution", "The layer that constrains admissible goals, values, self-modification, and human-agency requirements."),
    ("Stable Capability Field", "A stable capability boundary with replaceable implementations, bounded authority, qualification evidence, and rollback rules."),
    ("PlanForge", "The planning/control framing for compiling goals into governed task graphs, dependencies, budgets, and replanning triggers."),
    ("Virtual Context Memory", "A governed memory/context layer that compiles evidence-carrying context packets from durable sources."),
    ("Talos", "The labor/execution OS framing for typed jobs, artifact graphs, tool permissions, audit logs, and replay."),
    ("Spinoza", "The reasoning and verification framing for claim extraction, evidence tiers, contradiction handling, and belief revision."),
    ("MoECOT", "A modular orchestration/prototype framing with specialist cores, readiness gates, ledgers, and replay."),
    ("Octopus Router", "A lightweight routing architecture for dynamically selecting bounded specialist arms or cores."),
    ("Ratcheting Modular Intelligence", "A capability-growth doctrine based on benchmark frontiers, residual escrow, regression preservation, and verified module promotion."),
    ("Compact Generative Systems", "A compression framing focused on the smallest adequate generative or governing structure without hiding residual complexity."),
    ("RankFold / NeuralFold", "A compression source family for low-rank residual coding, functional preprocessing, and fallback routing."),
    ("BBVCA", "A generate-verify-repair compression source family using seeded local laws, bounded search, and residual tracking."),
    ("Artifact graph", "A traceable graph of produced objects, source handles, jobs, claims, and evidence records."),
    ("Claim ledger", "A structured record of claims, support states, sources, uncertainty, contradiction links, and review status."),
    ("Context packet", "The active, compiled context supplied to an agent or job, including source handles, summaries, authority labels, and adequacy status."),
    ("Proof-carrying summary", "A summary that carries provenance and checks sufficient to audit its fidelity to source material."),
    ("Authority ceiling", "The maximum action authority a layer, field, tool, or implementation may exercise."),
    ("Readiness gate", "An evidence and regression checkpoint that must pass before a module or field can be promoted."),
    ("Residual escrow", "A visible backlog of unresolved failures, uncertainty, or residual complexity left by a route, compression, or benchmark result."),
    ("Benchmark ratchet", "A process that uses tests, regressions, hidden checks, and residuals to move capability claims without erasing failure cases."),
]


TEST_SPECS = {
    "Alignment": [
        "Constitutional consistency",
        "Value conflict classification",
        "Self-modification ethics scenario",
        "Power-seeking / agency-dominance scenario",
    ],
    "SCF": [
        "Qualification predicates",
        "Route validity",
        "Mutation",
        "Authority non-escalation",
        "Rollback and recovery",
    ],
    "Planning": [
        "Decomposition accuracy",
        "Dependency ordering",
        "Constraint preservation",
        "Runtime replanning",
        "Tool selection",
        "Budget and risk allocation",
        "Scope creep prevention",
    ],
    "VCM": [
        "Context packet adequacy",
        "Distractor resistance",
        "Authority label preservation",
        "Proof-carrying summary fidelity",
        "Planner-guided prefetch accuracy",
        "Privacy / behavioral authority checks",
    ],
    "Talos / execution": [
        "Typed job lifecycle",
        "Tool permission enforcement",
        "Audit log reconstruction",
        "Replay determinism",
        "Human approval gates",
        "Adversarial job injection",
    ],
    "Spinoza / verification": [
        "Claim extraction",
        "Contradiction detection",
        "Belief revision",
        "Evidence tier assignment",
        "Uncertainty calibration",
        "Refusal or silence when evidence is insufficient",
    ],
    "Routing / modularity": [
        "Specialist routing accuracy",
        "Readiness gate enforcement",
        "Benchmark promotion",
        "Quarantine",
        "Regression preservation",
        "Residual escrow",
    ],
    "Compression": [
        "Reconstruction quality",
        "Residual burden",
        "Probe-and-route fallback",
        "Compression ratio",
        "Latency cost",
        "Downstream utility preservation",
    ],
    "Benchmark ratchets": [
        "Saturation detection",
        "Hidden benchmark transfer",
        "Regression generation",
        "Anti-Goodhart checks",
        "Residual backlog integrity",
    ],
}


def read_inventory() -> list[dict]:
    with SOURCE_INVENTORY.open(encoding="utf-8") as f:
        records = json.load(f)
    if not isinstance(records, list):
        raise TypeError("sources/source_inventory.json must contain a list")
    return records


def inventory_by_id(records: list[dict]) -> dict[str, dict]:
    return {record["id"]: record for record in records}


def qmd_escape(value: object) -> str:
    text = "" if value is None else str(value)
    return text.replace("|", "\\|").replace("\n", " ")


def yaml_list(items: list[str]) -> str:
    if not items:
        return " []"
    return "\n" + "\n".join(f'  - "{item}"' for item in items)


def bullet_list(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def chapter_sources(chapter: dict, by_id: dict[str, dict]) -> list[str]:
    merged: list[str] = []
    for source_id in chapter["sources"]:
        if source_id in by_id and source_id not in merged:
            merged.append(source_id)
    for source_id, record in by_id.items():
        if chapter["num"] in [str(target).zfill(2) for target in record.get("chapter_targets", [])]:
            if source_id not in merged:
                merged.append(source_id)
    return merged


def write_chapters(records: list[dict]) -> None:
    by_id = inventory_by_id(records)
    for chapter in CHAPTERS:
        source_ids = chapter_sources(chapter, by_id)
        source_label = ", ".join(f"`{source_id}`" for source_id in source_ids) or "None assigned yet"
        gaps = [
            "Assigned source texts have not yet been ingested or summarized.",
            "No Codex tests have been implemented or run.",
            "Chapter prose is a scaffold, not a completed manuscript draft.",
        ]
        crosswalk_rows = []
        for source_id in source_ids:
            source = by_id[source_id]
            crosswalk_rows.append(
                f"| `{source_id}` | {qmd_escape(source['title'])} | Planned use from inventory/handoff: {qmd_escape(source.get('notes', ''))} |"
            )
        if not crosswalk_rows:
            crosswalk_rows.append("| TBD | TBD | No source assigned yet. |")

        test_rows = "\n".join(f"| {qmd_escape(test)} | Support or falsify this chapter's layer claim. | planned; not run |" for test in chapter["tests"])
        text = f"""---
title: "{chapter['title']}"
status: "conceptual"
last_updated: "{TODAY}"
primary_sources:{yaml_list(source_ids)}
evidence_level: "argument"
open_evidence_gaps:{yaml_list(gaps)}
---

# {chapter['title']}

## Chapter status

| Field | Value |
|---|---|
| Status | conceptual |
| Last updated | {TODAY} |
| Primary source records | {source_label} |
| Evidence level | argument |
| Source ingestion state | Source records assigned; source texts not yet ingested. |
| Test state | Planned only; no tests have been run. |

## Drafting guardrail

This stub is derived from the handoff outline and source inventory only. It does not claim that the listed source documents have been ingested, summarized, or independently verified.

## Problem

{chapter['problem']}

## Why existing approaches are insufficient

{chapter['insufficient']}

## Core claim

[{chapter['num']}-core, support: argument] {chapter['claim']}

## Mechanism

{bullet_list(chapter['mechanism'])}

## Interfaces

{bullet_list(chapter['interfaces'])}

## Invariants

{bullet_list(chapter['invariants'])}

## Failure modes

{bullet_list(chapter['failure_modes'])}

## Minimal implementation

{chapter['minimal']}

## Codex test plan

| Test | Purpose | Status |
|---|---|---|
{test_rows}

## Source crosswalk

| Source ID | Title | Planned use |
|---|---|---|
{chr(10).join(crosswalk_rows)}

## Summary

This chapter currently establishes the structural slot for this layer of the ASI stack. The next drafting pass should ingest the assigned sources, separate source-derived claims from design hypotheses, and update Appendix C when support states change.
"""
        (ROOT / chapter["file"]).write_text(text, encoding="utf-8")


def write_source_matrix(records: list[dict]) -> None:
    rows = []
    for record in records:
        targets = ", ".join(str(target).zfill(2) for target in record.get("chapter_targets", []))
        rows.append(
            "| `{id}` | {title} | `{priority}` | `{layer}` | {targets} | [source]({url}) | inventory-recorded; text not ingested | {notes} |".format(
                id=qmd_escape(record.get("id", "")),
                title=qmd_escape(record.get("title", "")),
                priority=qmd_escape(record.get("priority", "")),
                layer=qmd_escape(record.get("layer", "")),
                targets=qmd_escape(targets),
                url=qmd_escape(record.get("url", "")),
                notes=qmd_escape(record.get("notes", "")),
            )
        )
    text = f"""# Source Matrix

This matrix is generated from `sources/source_inventory.json`.

Source text status is deliberately conservative: the records are inventoried, but the source documents themselves have not yet been exported, ingested, summarized, or verified in this repository.

| ID | Title | Priority | Layer | Chapter targets | URL | Current status | Notes |
|---|---|---|---|---|---|---|---|
{chr(10).join(rows)}
"""
    (ROOT / "appendices" / "A_source_matrix.qmd").write_text(text, encoding="utf-8")


def write_claim_matrix(records: list[dict]) -> None:
    by_id = inventory_by_id(records)
    rows = []
    for chapter in CHAPTERS:
        source_ids = chapter_sources(chapter, by_id)
        source_label = ", ".join(f"`{source_id}`" for source_id in source_ids) or "TBD"
        rows.append(
            f"| `{chapter['num']}-core` | {chapter['num']} | {qmd_escape(chapter['claim'])} | argument | {source_label} | Outline-level architecture claim only. | Ingest sources; define and run tests before raising support state. |"
        )
    text = f"""# Claim/Evidence Matrix

This initial matrix contains one core placeholder claim per chapter.

No claim is marked `source-derived`, `prototype-backed`, `synthetic-test-backed`, `empirical-test-backed`, or `external-literature-backed` yet. Those labels require source ingestion, prototype inspection, or actual test execution.

| Claim ID | Chapter | Claim | Current support state | Assigned sources | Current evidence | Open gap |
|---|---:|---|---|---|---|---|
{chr(10).join(rows)}

## Support States

| State | Meaning |
|---|---|
| unsupported | Not yet supported; likely remove or mark as speculative. |
| argument | Supported by reasoning only. |
| source-derived | Derived from supplied source papers. |
| prototype-backed | Implemented in a prototype but not robustly tested. |
| synthetic-test-backed | Supported by controlled synthetic tests. |
| empirical-test-backed | Supported by external or realistic tests. |
| external-literature-backed | Supported by third-party literature. |
"""
    (ROOT / "appendices" / "C_claim_evidence_matrix.qmd").write_text(text, encoding="utf-8")


def write_glossary() -> None:
    rows = "\n".join(f"| {qmd_escape(term)} | {qmd_escape(definition)} | initial; refine after source ingestion |" for term, definition in GLOSSARY)
    text = f"""# Glossary

These are initial working definitions derived from the handoff packet. They are not final source-derived definitions.

| Term | Working definition | Status |
|---|---|---|
{rows}
"""
    (ROOT / "appendices" / "B_glossary.qmd").write_text(text, encoding="utf-8")


def write_protocol_schemas() -> None:
    text = """# Protocol Schemas

These are draft schema placeholders for later source-derived protocol work. They are intentionally minimal and should not be treated as final API contracts.

## Command Contract

```yaml
command_contract:
  intent: string
  requester: string
  authority_ceiling: string
  constraints: []
  expected_artifacts: []
  required_approvals: []
  stop_conditions: []
```

## Context Packet

```yaml
context_packet:
  task_id: string
  source_handles: []
  summaries: []
  authority_labels: []
  adequacy_state: unknown
  open_uncertainties: []
```

## Stable Capability Field

```yaml
stable_capability_field:
  field_id: string
  semantic_boundary: string
  authority_ceiling: string
  implementations: []
  qualification_predicates: []
  regression_suite: []
  rollback_plan: string
```

## Typed Job

```yaml
typed_job:
  job_id: string
  contract_id: string
  runtime_adapter: string
  inputs: []
  outputs: []
  permissions: []
  audit_events: []
  replay_status: not_run
```

## Claim Record

```yaml
claim_record:
  claim_id: string
  text: string
  support_state: argument
  source_handles: []
  tests: []
  contradictions: []
  review_status: open
```
"""
    (ROOT / "appendices" / "D_protocol_schemas.qmd").write_text(text, encoding="utf-8")


def write_test_specs() -> None:
    rows = []
    for layer, tests in TEST_SPECS.items():
        for test in tests:
            rows.append(f"| {qmd_escape(layer)} | {qmd_escape(test)} | planned | not run |")
    text = f"""# Codex Test Specs

This appendix initializes the test backlog from the handoff evidence plan.

No result is recorded here unless a test has actually been implemented and run.

| Layer | Test spec | Implementation status | Result status |
|---|---|---|---|
{chr(10).join(rows)}
"""
    (ROOT / "appendices" / "E_codex_test_specs.qmd").write_text(text, encoding="utf-8")


def write_changelog() -> None:
    text = f"""# Changelog

## {TODAY} - v0.1 scaffold seed

- Created the canonical Quarto living-book scaffold at the repository root.
- Populated Appendix A from `sources/source_inventory.json` with {len(read_inventory())} source records.
- Created chapter stubs for all 16 outline chapters with explicit source-ingestion and test-status guardrails.
- Initialized Appendix C with one `argument`-level claim placeholder per chapter.
- Initialized glossary, protocol-schema, and Codex test-spec appendices.
- Added local validation and GitHub Pages publishing scaffolding.

## v0.0

- Handoff packet created.
"""
    (ROOT / "appendices" / "F_changelog.qmd").write_text(text, encoding="utf-8")


def write_index_and_preface() -> None:
    index = """# The ASI Stack

A living technical book by Corben Sorenson.

## Core thesis

Efficient ASI should be treated as a governed cognitive stack rather than a monolithic model.

The proposed stack has ten cooperating concerns:

1. Alignment and constitution
2. Governance and stable capability fields
3. Planning and control
4. Virtual context memory
5. Reasoning and verification
6. Labor and execution
7. Routing and modular intelligence
8. Compression and representation
9. Evidence and benchmark ratchets
10. Recursive self-improvement

## Reading status

This v0.1 scaffold is structural. Source records are inventoried, but the source texts have not yet been ingested into this repository. Chapter claims are labeled `argument` until source ingestion, prototype inspection, or actual tests justify a stronger support state.
"""
    preface = """# Preface

This book is a unification pass across AI architecture papers and prototypes. It is not intended to be a pasted anthology. The goal is to treat the papers as fragments of one proposed architecture for governed, efficient, self-improving AI.

## What this book is

It is a living technical book organized around stack layers: alignment, governance, planning, memory, reasoning, execution, routing, compression, evidence, and recursive improvement.

## What this book is not

It is not a claim that the architecture is complete, proven, or safe in every domain. It is not a benchmark report unless tests are explicitly recorded as run. It is not a replacement for source documents.

## Claim labels

Claims use explicit support states: `unsupported`, `argument`, `source-derived`, `prototype-backed`, `synthetic-test-backed`, `empirical-test-backed`, and `external-literature-backed`.

## Why Codex tests matter

The living format is meant to support evidence ratchets. Codex test specs identify what would support or falsify claims, but no test result should be recorded until the test has actually run.
"""
    (ROOT / "index.qmd").write_text(index, encoding="utf-8")
    (ROOT / "preface.qmd").write_text(preface, encoding="utf-8")


def main() -> None:
    records = read_inventory()
    write_index_and_preface()
    write_chapters(records)
    write_source_matrix(records)
    write_claim_matrix(records)
    write_glossary()
    write_protocol_schemas()
    write_test_specs()
    write_changelog()
    print(f"Synchronized scaffold from {len(records)} source records.")


if __name__ == "__main__":
    main()
