#!/usr/bin/env python3
"""Validate the maintained independent 26-unit Human Reader manuscript."""

from __future__ import annotations

import copy
import json
from pathlib import Path

from build_human_reader_current import (
    CROSSWALK,
    EDITION,
    MANIFEST,
    ROOT,
    STRUCTURE,
    build,
)

STATUS = ROOT / "roadmap_records/post_v2_3_maintenance_transfer_and_publication_status.json"
PAGES_WORKFLOW = ROOT / ".github/workflows/build-pages-artifact.yml"


UNIT_01_REQUIRED = [
    "## The Change That Worked",
    "## The Wrong Unit of Analysis",
    "## Why Greater Capability Makes Boundaries More Important",
    "## What the Stack Separates",
    "## The Law of Noninheritance",
    "## One Request, Many Commitments",
    "## When Does a Responsibility Deserve a Layer?",
    "## Interfaces Make Failure Addressable",
    "## Logical Layers, Not a Service Tax",
    "## The Stack Is Inside the World",
    "## One Architecture, Several Views",
    "## The Monolith Can Be the Right Baseline",
    "## Failure Modes of the Stack Thesis",
    "## What the Current Work Establishes",
    "## From Minimum Stack to Mature Architecture",
    "## Evidence That Would Change the Conclusion",
    "## What This Establishes",
    "Capability does not confer authority",
    "The live research chapter remains at `argument` support",
    "It does not establish authentic approvals or receipts",
    "does not promote the chapter core",
]
UNIT_02_REQUIRED = [
    "## The Expensive Answer That Looked Cheap",
    "## Accepted Useful Work",
    "## Freeze Quality Before Comparing Cost",
    "## The Complete Bill",
    "## Cost Moves Through Time and Organizations",
    "## Three Policies Compete",
    "## Governance Rent",
    "## A Route Ledger",
    "## Reuse Is the Main Long-Term Bet",
    "## Specialist Routes and Conditional Compute",
    "## Compression Moves Burden",
    "## Selective Deliberation",
    "## Scaling Is a Variable, Not a Destiny",
    "## One Repository Campaign",
    "## Failure Modes",
    "## The Strongest Objection",
    "## What the Current Work Establishes",
    "## From Minimum Ledger to Governed Route Economy",
    "## Evidence That Would Change the Conclusion",
    "## What This Establishes",
    "The live research chapter remains at `argument` support",
    "These artifacts establish finite accounting and transition discipline",
    "They do\nnot establish complete candidate search, accurate costs, calibrated quality",
]
UNIT_03_REQUIRED = [
    "## The Planner Does Not Hold the Key",
    "## Proposal, Approval, Effect, and Release",
    "## The Authority Tuple",
    "## Authority Is Checked at the Effect",
    "## Technical Authority and Legitimate Authority",
    "## Delegation Attenuates",
    "## Revocation Is a Race",
    "## Failure Is a Broken Responsibility",
    "## Incidents, Recurrence, and Remedy",
    "## Ungoverned Does Not Mean Unstructured",
    "## Dangerous Capability Is an Uplift Question",
    "## A Public-Safe Uplift Dossier",
    "## Misuse Authority Is Not Research Authority",
    "## Military AI Is a Command-and-Interaction System",
    "## Meaningful Human Judgment",
    "## Strategic Stability Is Relational",
    "## Safe Posture and Off-Ramps",
    "## Assurance Under Secrecy",
    "## One Request Across Four Risk Levels",
    "## Failure Modes",
    "## The Strongest Simpler Baseline",
    "## What the Current Work Establishes",
    "## From Minimum Authority to Governed Institutions",
    "## Evidence That Would Change the Conclusion",
    "## What This Establishes",
    "All four routed chapter cores remain at `argument` support",
    "They do not establish authentic identity or\nreceipts, deployed permission enforcement",
    "No hazardous-domain evaluation, public-safe strategic simulation",
    "No support or release state\nmoved",
]
UNIT_23_REQUIRED = [
    "## The Complete Bill",
    "## Speed Is a Qualified Route",
    "## Deliberation Has a Failure Surface",
    "## Compression Moves Burden",
    "## One Allocation Decision",
    "## The Allocation Lease",
    "## A Worked Budget",
    "## Failure Cases",
    "## Evidence and Experiments",
    "## Human Time and Organizational Cost",
    "## From Minimum Implementation to Mature System",
    "## What This Establishes",
    "evidentiary authority are separate claims",
    "does not establish that the proposed controller is economically optimal",
]
UNIT_04_REQUIRED = [
    "## A Change Can Be Correct and Still Be Unsafe",
    "## The Smallest Powerful Kernel",
    "## The Model Is Part of the Attack Surface",
    "## Privacy Is About Use, Not Merely Secrecy",
    "## Protected Computation Is Evidence, Not Permission",
    "## Model Weights Are a Custody Graph",
    "## The Supply Chain Is a Living Dependency Graph",
    "## Release Changes the Kind of Control",
    "## One End-to-End Custody Decision",
    "## Failure Cases",
    "## What the Current Evidence Can Establish",
    "## From Minimum Implementation to a Mature Security Fabric",
    "## The Strongest Objection",
    "## What This Establishes",
    "A successful local load is not release authority",
    "The conclusion should change if simpler systems prove equally effective",
]
UNIT_05_REQUIRED = [
    "## A Passing Test Is Not a General Verdict",
    "## Claims Need Stable Identities",
    "## Support States Are Not a Confidence Score",
    "## An Evidence Transition Is a Bounded Argument",
    "## Oversight Begins Where the Evaluator Is Weaker",
    "## Independence Is a Dependency Graph",
    "## White-Box Evidence Starts a New Challenge",
    "## One Patch, Three Evidence Paths",
    "## Failure Cases",
    "## The Strongest Simpler Baseline",
    "## What the Current Evidence Can Establish",
    "## From Minimum Implementation to a Mature Evidence System",
    "## The Strongest Objection",
    "## Evidence That Would Change the Conclusion",
    "## What This Establishes",
    "A passing test is not a method verdict",
    "This Human Reader synthesis does not combine those narrower\nresults into a stronger conclusion",
]
UNIT_06_REQUIRED = [
    "## The User Did Not Ask for That",
    "## Intent Is an Interpretation, Not a String",
    "## Outcomes and Means Must Stay Separate",
    "## Authority Is Not Context",
    "## A Contract Should Preserve Uncertainty",
    "## Meaningful Control Is a Resource Condition",
    "## The Approver Is an Epistemic Target",
    "## One Proposal, Four Decisions",
    "## Revocation and Re-Contracting",
    "## Failure Cases",
    "## The Strongest Simpler Baseline",
    "## What the Current Work Can Establish",
    "## From a Minimum Boundary to a Mature Control System",
    "## The Strongest Objection",
    "## Evidence That Would Change the Conclusion",
    "## What This Establishes",
    "Alignment concerns the relation between result and mandate",
    "the approver is also an epistemic target",
]
UNIT_07_REQUIRED = [
    "## The Patch Passes Every Test",
    "## A Constraint Is Not an Objective",
    "## Values Do Not Become One Number",
    "## Objective Formation Is a Lease",
    "## Behavior Is Not Objective Integrity",
    "## Separating Interventions",
    "## Who May Amend the Goal?",
    "## Dissent, Appeal, and Rights",
    "## One Proposal, Four Governance Objects",
    "## Revocation and Descendant Retirement",
    "## Failure Cases",
    "## The Strongest Simpler Baseline",
    "## What the Current Work Can Establish",
    "## From a Minimum Registry to a Mature Objective Service",
    "## The Strongest Objection",
    "## Evidence That Would Change the Conclusion",
    "## What This Establishes",
    "an optimizer\ncannot ratify its own purpose",
    "This Human Reader synthesis does not combine those bounded results into a\nstronger theorem",
]
UNIT_08_REQUIRED = [
    "## The Patch Leaves the Repository",
    "## Capability Is Not Mandate",
    "## The Affected Public Is Part of the System",
    "## Participation Is Not Representation",
    "## Jurisdiction Is a Routing Constraint",
    "## Coordination Must Survive Partial Participation",
    "## Resilience Has Four Different Verbs",
    "## One Shared Service, Many Authorities",
    "## Remedy Must Reach the Harmed Party",
    "## Concentration and Gradual Loss of Human Influence",
    "## Failure Cases",
    "## The Strongest Simpler Baseline",
    "## What the Current Work Can Establish",
    "## From a Minimum Packet to a Mature Governance Fabric",
    "## The Strongest Objection",
    "## Evidence That Would Change the Conclusion",
    "## What This Establishes",
    "Capability does not\ncreate mandate",
    "This Human Reader synthesis does not combine the two finite reviews into a\nstronger theorem",
]
UNIT_09_REQUIRED = [
    "## The Name That Survives the Upgrade",
    "## A Field Is a Promise, Not a Label",
    "## Compatibility Is Not Qualification",
    "## The Patch Verifier Replacement",
    "## Replacement Is a Transaction",
    "## Rollback Is Not Time Travel",
    "## Authority Must Not Ride Along",
    "## The Proof Boundary",
    "## Failure Cases",
    "## The Strongest Simpler Baseline",
    "## From a Minimum Record to a Replacement Fabric",
    "## The Strongest Objection",
    "## Evidence That Would Change the Conclusion",
    "## What This Establishes",
    "The field holds the\npromise. The implementation is one defeasible attempt to keep it",
    "No finite proof, schema, fixture, or clean local rollback can answer that\nquestion alone",
]
UNIT_10_REQUIRED = [
    "## Four Reports About One Patch",
    "## A Report Is Not the World",
    "## Observation Is Task-Relative",
    "## Agreement Is Not Independence",
    "## Calibration and Missingness Travel With the Result",
    "## Disagreement Is a Routing Signal",
    "## Freshness Is Part of Meaning",
    "## From Observation to Physical Effect",
    "## Simulation Is an Instrument, Not a World",
    "## Effect Observation and Recovery",
    "## Failure Cases",
    "## The Strongest Simpler Baseline",
    "## What the Current Work Establishes",
    "## From a Minimum Contract to an Observation Fabric",
    "## The Strongest Objection",
    "## Evidence That Would Change the Conclusion",
    "## What This Establishes",
    "The test runner and reviewer both read artifacts produced from the same stale\nbuild cache",
    "The models establish neither environmental truth, calibration, causal\nindependence, useful fusion, physical safety, recovery, nor deployment\nreadiness",
]
UNIT_11_REQUIRED = [
    "## The Branch That Passed",
    "## Five Kinds of State",
    "## Freeze the Forecast Before the Intervention",
    "## Prediction Is Not Intervention",
    "## Horizon Changes the Claim",
    "## Keep More Than One Possible World",
    "## Optimization Finds Favorable Mistakes",
    "## The Trial and the Receipt",
    "## Learning Without Rewriting History",
    "## Failure Cases",
    "## The Strongest Simpler Baseline",
    "## What the Current Work Establishes",
    "## From a Minimum Contract to a Reality-Grounded Model Service",
    "## The Strongest Objection",
    "## Evidence That Would Change the Conclusion",
    "## What This Establishes",
    "The model's\nown predicted state cannot serve as that effect observation",
    "The claim-bearing empirical lane is prospectively specified but has not run",
]
UNIT_12_REQUIRED = [
    "## A Plan That Survives Contact",
    "## Six Objects That Should Not Collapse",
    "## The Plan Begins With a Frozen Contract",
    "## Obligations, Not To-Do Items",
    "## Dependencies Have Types",
    "## Unknown Is a Planning State",
    "## Alternatives Need a Denominator",
    "## Reachability Is Not Permission",
    "## Scheduling the Whole Cost",
    "## Replanning Is a New Version",
    "## Branch Joins Are Semantic Decisions",
    "## Stop, Fallback, and Recovery Are Work",
    "## Failure Cases",
    "## The Strongest Simpler Baseline",
    "## What the Current Work Establishes",
    "## From a Minimum Planner to a Governed Control Service",
    "## The Strongest Objection",
    "## Evidence That Would Change the Conclusion",
    "## What This Establishes",
    "Reachability is not permission",
    "They do not establish decomposition quality, dependency truth or completeness",
]
UNIT_13_REQUIRED = [
    "## The Artifact That Followed the Plan",
    "## A Plan Node Is Not Yet an Artifact",
    "## Stable Semantic Identity",
    "## Ambiguity Is Compiler Debt",
    "## Relations Need Roles",
    "## Dimensions Are Types, Not Decoration",
    "## Equivalence Is Relative to a Consumer",
    "## Search Is a Candidate Generator",
    "## A New Substrate Must Earn Its Boundary",
    "## Progressive Lowering",
    "## Validate the Actual Target",
    "## Repair by Identity and Observed Change",
    "## Reverse Compilation Is Not Mind Reading",
    "## Failure Cases",
    "## The Strongest Simpler Baseline",
    "## What the Current Work Establishes",
    "## From a Minimum Compiler to a Cognitive Toolchain",
    "## The Strongest Objection",
    "## Evidence That Would Change the Conclusion",
    "## What This Establishes",
    "None of these results transfers support to the other owners",
    "selected full route tied its baseline at 1.000 task accuracy while\nusing 1.913386 times the operations",
]
UNIT_14_REQUIRED = [
    "## The Patch That Remembered Too Much",
    "## Five States, Not One Memory",
    "## Context Is a Typed Mount",
    "## Pages, Cells, and Certificates",
    "## Addresses Are Not Meaning",
    "## Snapshots Freeze a View, Not the World",
    "## Context Changes Are Transactions",
    "## Branches Need Context Isolation",
    "## Taint Is a Dependency Property",
    "## Durable Memory Begins With Events",
    "## Knowledge Is a Lattice of Qualified Relations",
    "## Contradiction Is Not a Cache Miss",
    "## Retrieval Produces Candidates",
    "## Forgetting Has Several Targets",
    "## Migration Must Preserve the Repair Path",
    "## Failure Cases",
    "## The Strongest Simpler Baseline",
    "## What the Current Work Establishes",
    "## From a Minimum Context Service to Durable Memory",
    "## The Strongest Objection",
    "## Evidence That Would Change the Conclusion",
    "## What This Establishes",
    "Storage does not\ngrant context admission. Context admission does not establish belief",
    "None of these results transfers support among the owners",
]
UNIT_15_REQUIRED = [
    "## The Claim Everyone Approved",
    "## Verification Starts With Obligations",
    "## Verification Bandwidth Is Qualified Capacity",
    "## Verification Is a Portfolio Decision",
    "## Context Adequacy Is Claim-Relative",
    "## A Claim Needs an Identity Before a Score",
    "## The Ledger Is Append-Only Belief History",
    "## Evidence Events Do Not Promote Themselves",
    "## Defeaters and Maximum Inference Travel With the Claim",
    "## Formality Has Several Lanes",
    "## Executable Specifications Make Disagreement Concrete",
    "## Lean Proves the Encoded Proposition",
    "## Proof-Carrying Claims Bind Interpretation",
    "## Proof Contracts Travel Without Promotion",
    "## Adversarial Review Is a Bounded Tribunal",
    "## Disagreement Is an Output, Not a Defect",
    "## Runtime Truth Is a Separate Bridge",
    "## Downgrades Must Reach Every Known Consumer",
    "## Failure Cases",
    "## The Strongest Simpler Baseline",
    "## What the Current Work Establishes",
    "## From a Minimum Ledger to an Evidence Fabric",
    "## The Strongest Objection",
    "## Evidence That Would Change the Conclusion",
    "## What This Establishes",
    "A passing test, theorem, source, benchmark, review, or runtime observation is\nan evidence artifact. It does not automatically move the parent claim",
    "Silence after notification is not counted as\nsuccessful repair",
]
UNIT_16_REQUIRED = [
    "## Every Worker Reports Success",
    "## Work Needs One Identity",
    "## Typed Jobs Are Executable Contracts",
    "## Acknowledgments Close Different Questions",
    "## Results Are Not Outcomes",
    "## Work Surfaces Absorb Abstraction Layers",
    "## A Harness Is Not an Employer or an Institution",
    "## Delegation Preserves Residual Duty",
    "## Accountability Cannot Be Summarized Away",
    "## Capacity and Competence Are Scheduling Constraints",
    "## Coordination Across Agents Needs Market and Command Limits",
    "## Assistance, Dependence, and Cognitive Sovereignty",
    "## Organizational Absorption Is a Feedback Loop",
    "## Transition Governance Starts Before Deployment",
    "## Human Agency After Role Redesign",
    "## One Repository Change, One Accountable Route",
    "## Failure Cases",
    "## The Strongest Simpler Baseline",
    "## What the Current Work Establishes",
    "## From a Minimum Job Contract to a Mature Labor Fabric",
    "## The Strongest Objection",
    "## Evidence That Would Change the Conclusion",
    "## What This Establishes",
    "Their combination in\nthis chapter does not promote any core claim",
    "A harness can\ncoordinate tools; it cannot create legitimacy",
]
UNIT_17_REQUIRED = [
    "## The Release That Succeeded Twice",
    "## Artifacts Form a Graph, Not a Folder",
    "## Provenance Has Completeness Boundaries",
    "## Audit Logs Are Event Claims",
    "## Replay Has Grades",
    "## Runtime Adapters Are Effect Boundaries",
    "## Approval Is a Scoped Input",
    "## Effect Leases Bound Action in Time",
    "## Expected Effect and Actual Effect Are Different Records",
    "## Observation Has a Budget and a Failure Policy",
    "## Rollback Is an Effect Claim",
    "## Change Control Joins Artifact and Authority",
    "## Incidents Begin With Divergence",
    "## Graceful Degradation Preserves the Important Contract",
    "## Recovery, Compensation, and Closure",
    "## Operations Must Survive the Governance Plane",
    "## Unknown External Effects Remain Open",
    "## One End-to-End Operational Route",
    "## Failure Cases",
    "## The Strongest Simpler Baseline",
    "## What the Current Work Establishes",
    "## From a Minimum Effect Route to a Mature Operations Fabric",
    "## The Strongest Objection",
    "## Evidence That Would Change the Conclusion",
    "## What This Establishes",
    "None makes\nlogs identical to reality",
    "Combining them here does not create deployment evidence or promote a core\nclaim",
]
UNIT_18_REQUIRED = [
    "## The Workflow That Escaped Its Lesson",
    "## Traces Are Episodes, Not Skills",
    "## Promotion Is a Governed Transition",
    "## Discovery Must Preserve the Denominator",
    "## Procedure Identity Includes Its Boundary",
    "## Execution Produces New Evidence, Not Automatic Reinforcement",
    "## Retirement Is Part of Memory",
    "## A Procedure Can Cross a Stack Boundary",
    "## Delegation Does Not Become Transitive by Transport",
    "## Protocol Versions Are Capability Negotiations",
    "## Receipts Are Disputable Claims",
    "## Economic Exchange Needs Its Own Ledger",
    "## Adversarial Peers Change the Default",
    "## Local Validity Is Not Population Safety",
    "## Coordination and Collective Intelligence Are Qualified Outcomes",
    "## Competition, Collusion, and Emergence",
    "## Concentration Can Grow Through Valid Choices",
    "## Systemic Interventions Need Counterfactuals",
    "## Bystanders and Public Institutions Are Participants",
    "## Gradual Disempowerment Has No Single Incident",
    "## One Procedure, One Exchange, One Population",
    "## Failure Cases",
    "## The Strongest Simpler Baseline",
    "## What the Current Work Establishes",
    "## From a Minimum Procedure to a Governed Agent Ecology",
    "## The Strongest Objection",
    "## Evidence That Would Change the Conclusion",
    "## What This Establishes",
    "Passing every local gate is one input, never the\nverdict",
    "It shows exact\nplaces where local evidence must stop",
]
UNIT_19_REQUIRED = [
    "## The Best Model for the Wrong Job",
    "## Capability Identity Is Not Model Identity",
    "## Routing Is a Governed Decision",
    "## Route Correctness and Answer Correctness Are Separate",
    "## Clarification, Abstention, and Fallback Are Routes",
    "## Calibration Belongs to the Route and the Answer",
    "## Specialists Need Lifecycle Governance",
    "## Composition Needs an Owner",
    "## Load and Scarcity Change the Best Route",
    "## Replaceability Requires an ABI",
    "## Checkpoints Must Preserve More Than Weights",
    "## Stateful Substrates Need Isolation and Concurrency Rules",
    "## Architecture Tournaments Need Full Costs",
    "## Adoption Is a Reversible Governance Transaction",
    "## Transformer Monoculture Is a Risk, Not a Refutation",
    "## Recurrence Changes the State Contract",
    "## Cyclic Memory Needs Residue and History",
    "## Coil and CoilRA Are Candidate Contracts",
    "## Non-Digital Substrates Still Need the Contract",
    "## Security and Rights Constrain Substrate Choice",
    "## One Task, Five Qualified Routes",
    "## Failure Cases",
    "## The Strongest Simpler Baseline",
    "## What the Current Work Establishes",
    "## From a Minimum Router to a Substrate Market",
    "## The Strongest Objection",
    "## Evidence That Would Change the Conclusion",
    "## What This Establishes",
    "Structural certification is not model quality",
    "The joined chapter does not combine these bounded results into a claim",
]
UNIT_20_REQUIRED = [
    "## The Checkpoint That Loaded Perfectly",
    "## A Training Run Is an Experimental Transaction",
    "## Data Order Is Part of the Mechanism",
    "## Optimizers Carry State and Policy",
    "## Randomness and Numerics Are Named Inputs",
    "## Distributed Execution Is Not Learning Topology",
    "## Four Topologies Must Stay Separate",
    "## Adaptive Identity Is Persistent Causal State",
    "## Learning Relations Need Types",
    "## LCT-IR Makes the Process Explicit",
    "## Learning Causal Normal Form Is a Comparison Tool",
    "## The Semantic Compiler Needs a Firewall",
    "## Realization Leakage Is a Measured Residual",
    "## Checkpoints Are Full-State Commits",
    "## Resume Equivalence Is Prospective",
    "## Checkpoint Selection Is Not Qualification",
    "## Scaling Is a Family of Interventions",
    "## Topology Claims Need Causal Experiments",
    "## Learning Extends Beyond Parameters",
    "## Adaptive Branch–Validate–Integrate",
    "## One Repository Learner, One Governed Run",
    "## Training Authority Expires",
    "## Failure Cases",
    "## The Strongest Simpler Baseline",
    "## What the Current Work Establishes",
    "## From a Minimum Run Record to Adaptive Infrastructure",
    "## The Strongest Objection",
    "## Evidence That Would Change the Conclusion",
    "## What This Establishes",
    "It does not train\na model or establish resume equivalence",
    "The joined chapter therefore establishes a precise training and topology\ncontract",
]
UNIT_21_REQUIRED = [
    "## The Same Green Patch, Two Different Lessons",
    "## An Outcome Is Not a Lesson",
    "## Candidate Lessons Need Identity",
    "## The Adaptive Commit Boundary",
    "## Eight Places a Lesson Can Live",
    "## Locus Is Part of the Claim",
    "## Minimum Sufficient Persistence",
    "## Generalization Is a Prospective Claim",
    "## Feedback Is Evidence, Not an Objective",
    "## Policy Updates Are Leased Candidates",
    "## Continual Learning Is State Management",
    "## Multiple Update Clocks",
    "## Data Engines Carry Learning Obligations",
    "## Unlearning Is Not One Claim",
    "## Scientific Discovery Is Governed Revision",
    "## Adjudicating the Two Patches",
    "## Deoptimization and Retirement",
    "## Failure Modes",
    "## The Strongest Simpler Baseline",
    "## What the Current Work Establishes",
    "## From Minimum Persistence to a Mature Learning System",
    "## The Strongest Objection",
    "## Evidence That Would Change the Conclusion",
    "## What This Establishes",
    "The central Adjudicated Persistence architecture is presently an argument and\nresearch program",
    "they do not\nestablish deletion, forgetting, influence removal, privacy, rights compliance,\nor external erasure",
    "It does not yet implement or validate the integrated\nadjudicator",
]
UNIT_22_REQUIRED = [
    "## The Candidate That Passed Yesterday's Test",
    "## Evaluation Is an Adversarial Measurement Process",
    "## Evidence Has a Denominator",
    "## Calibration, Abstention, and Coverage",
    "## Benchmarks Need Ratchets",
    "## Anti-Goodhart Evaluation",
    "## The Candidate May Know It Is Being Tested",
    "## Training-Time Deception",
    "## Capability Thresholds Trigger Commitments",
    "## Readiness Is a State Transition",
    "## Readiness Is Workload and Authority Relative",
    "## Residual Escrow",
    "## A Safety Case Compiles the Argument",
    "## Hazards Come Before Evidence Shopping",
    "## Assurance Must Be Incremental and Revocable",
    "## Evidence Needs Authenticity Without a Truth Oracle",
    "## Repairing the Candidate's Assurance Path",
    "## Failure Modes",
    "## The Strongest Simpler Baseline",
    "## What the Current Work Establishes",
    "## From Minimum Evaluation to an Assurance System",
    "## The Strongest Objection",
    "## Evidence That Would Change the Conclusion",
    "## What This Establishes",
    "No real capability assessment, safeguard\nexercise, bypass or rollback test",
    "No model, detector, mitigation, monitor, reward process, evaluator\nensemble, natural cross-context workload, deception finding, or deployment ran",
    "All six chapter cores remain at argument support",
]
UNIT_24_REQUIRED = [
    "## Where the Repository Task Actually Runs",
    "## From Cognitive Demand to Physical Demand",
    "## Memory Movement Can Dominate",
    "## Hardware Profiles Are Versioned Decisions",
    "## Measure Use Before Modeling Impact",
    "## Useful Output Is the Denominator",
    "## Energy Is Capacity, Timing, and Reliability",
    "## Water, Land, Materials, and Hardware Life",
    "## Concentration Changes the Architecture",
    "## Infrastructure Is a Governance Surface",
    "## Personal Compute Hives",
    "## Locality Is More Than Latency",
    "## Federation Adds a Principal Boundary",
    "## Partitions Are Authority Events",
    "## Resilience Requires Diverse Failure Domains",
    "## Maintenance Is Part of Capacity",
    "## Beyond Digital Accelerators",
    "## One Workflow, Three Placements",
    "## Failure Modes",
    "## The Strongest Simpler Baseline",
    "## What the Current Work Establishes",
    "## From Minimum Measurement to Governed Infrastructure",
    "## The Strongest Objection",
    "## Evidence That Would Change the Conclusion",
    "## What This Establishes",
    "No live scheduler, registry, portal,\nauthority service, network overlay, sandbox, federation, partition experiment",
    "It does not measure a natural workload or\nestablish performance, environmental impact, resilience, community outcome",
    "Both chapter cores remain at argument support",
]
UNIT_25_REQUIRED = [
    "## When the Verifier Proposes Its Successor",
    "## What Makes Improvement Recursive",
    "## Proposal Is Not Permission",
    "## Choose the Smallest Improvement Locus",
    "## Freeze the Improvement Contract",
    "## Open-Ended Search Without Open Authority",
    "## Evaluators Are Part of the Attack Surface",
    "## Strategic Candidates Need Adversarial Evaluation",
    "## Full-State Identity Before Replacement",
    "## Evidence Does Not Compound Automatically",
    "## The Improvement Governor",
    "## Govern the Improvement Portfolio",
    "## Admitting the Better Verifier",
    "## Descendants Inherit History, Not Authority",
    "## Replication Is a Distinct Capability",
    "## Replication Leases",
    "## Containment Is Continued Control",
    "## When Containment Fails",
    "## Revocation and Finite Retirement",
    "## Bounded Liveness",
    "## Improvement Velocity Has a Control Limit",
    "## Recursive Depth and Protected Boundaries",
    "## Failure Modes",
    "## The Strongest Simpler Baseline",
    "## What the Current Work Establishes",
    "## From One Replacement to a Governed Improvement Program",
    "## The Strongest Objection",
    "## Evidence That Would Change the Conclusion",
    "## What This Establishes",
    "No live candidate-authored proposal, natural useful improvement",
    "no task generator, adaptive\ncandidate search, evolving archive",
    "All three chapter cores remain at argument support",
]
UNIT_26_REQUIRED = [
    "## One Change Through the Whole Stack",
    "## The Reference Path",
    "## Following the Repository Change",
    "## A Minimal Trusted Kernel",
    "## Stable Identities, Replaceable Implementations",
    "## Canonical State and Projections",
    "## Effects Are the Architectural Center",
    "## Evidence Is a Transition System",
    "## Contracts Between Layers",
    "## Scaling the Architecture Without Scaling Ceremony",
    "## Project Theseus",
    "## Report-First Is Not Report-Only",
    "## What Theseus Currently Establishes",
    "## From Demonstrator to Research System",
    "## The Prototype Roadmap",
    "## What the Prototype Controls Establish",
    "## Artifact Stewardship",
    "## The Living Book",
    "## What the Living-Book Controls Establish",
    "## The Research Frontier",
    "## One Research Loop",
    "## A Fresh-Checkout Test",
    "## Current Integrated Evidence",
    "## The Strongest Simpler Baseline",
    "## What Would Change the Architecture",
    "## What This Establishes",
    "not a completed reference implementation of the book",
    "It establishes finite proposal discipline, not project governance",
    "does not establish citation accuracy",
    "do not include\nlanguage-model planning or generation in the integrated slice",
    "It does not\nestablish a complete deployed ASI Stack, whole-system safety",
]


def validate(manifest: dict, expected: dict, crosswalk: dict, expected_crosswalk: dict) -> list[str]:
    errors: list[str] = []
    if manifest != expected:
        errors.append("manifest differs from its canonical graph/outline/manuscript derivation")
    if crosswalk != expected_crosswalk:
        errors.append("conclusion/claim crosswalk differs from its canonical graph/outline/manuscript derivation")
    if manifest.get("unit_count") != 26 or manifest.get("owner_route_count") != 87:
        errors.append("Human Reader denominator drift")
    units = manifest.get("units", [])
    owner_ids = [owner_id for unit in units for owner_id in unit.get("owner_ids", [])]
    if len(owner_ids) != len(set(owner_ids)):
        errors.append("a technical owner routes to more than one Human Reader unit")
    structure = json.loads(STRUCTURE.read_text(encoding="utf-8"))
    canonical_ids = {
        chapter["id"] for part in structure["parts"] for chapter in part["chapters"]
    }
    if set(owner_ids) != canonical_ids:
        errors.append("Human Reader routes omit or invent a canonical owner")
    crosswalk_owners = [owner for unit in crosswalk.get("units", []) for owner in unit.get("owners", [])]
    crosswalk_ids = [owner.get("chapter_id") for owner in crosswalk_owners]
    if crosswalk.get("unit_count") != 26 or crosswalk.get("owner_route_count") != 87:
        errors.append("conclusion/claim crosswalk denominator drift")
    if len(crosswalk_ids) != len(set(crosswalk_ids)) or set(crosswalk_ids) != canonical_ids:
        errors.append("conclusion/claim crosswalk does not preserve every technical owner exactly once")
    if crosswalk.get("support_state_effect") != "none" or crosswalk.get("release_effect") != "none":
        errors.append("conclusion/claim crosswalk changed support or release state")
    workflow = PAGES_WORKFLOW.read_text(encoding="utf-8")
    for fragment in (
        "quarto render editions/reader_manuscript/current --to html",
        "python3 scripts/build_human_reader_public_site.py --site _site",
    ):
        if fragment not in workflow:
            errors.append(f"Pages workflow does not publish the Human Reader: {fragment}")
    for unit in crosswalk.get("units", []):
        if unit.get("owner_count") != len(unit.get("owners", [])):
            errors.append(f"{unit.get('unit_id')}: crosswalk owner count drift")
        source_path = EDITION / unit.get("human_reader_source_file", "")
        if not source_path.is_file():
            errors.append(f"{unit.get('unit_id')}: crosswalk Human Reader source is missing")
        for owner in unit.get("owners", []):
            if owner.get("human_reader_unit_id") != unit.get("unit_id"):
                errors.append(f"{owner.get('chapter_id')}: crosswalk unit binding drift")
            if owner.get("core_claim_id") != f"{owner.get('chapter_id')}.core":
                errors.append(f"{owner.get('chapter_id')}: crosswalk core-claim identity drift")
            technical_path = ROOT / owner.get("technical_source_file", "")
            if not technical_path.is_file():
                errors.append(f"{owner.get('chapter_id')}: crosswalk technical source is missing")
            for artifact in owner.get("artifact_refs", []):
                artifact_path = ROOT / artifact.get("path", "")
                if not artifact_path.is_file():
                    errors.append(f"{owner.get('chapter_id')}: crosswalk artifact reference is missing")
    for unit in units:
        path = EDITION / unit["source_file"]
        state = unit.get("state")
        if state == "not_started":
            if path.exists():
                errors.append(f"{unit['unit_id']}: existing source marked not started")
            continue
        if not path.is_file():
            errors.append(f"{unit['unit_id']}: started source is missing")
            continue
        text = path.read_text(encoding="utf-8")
        expected_panel_include = f"{{{{< include ../generated/{unit['unit_id']}-status.qmd >}}}}"
        if expected_panel_include not in text:
            errors.append(f"{unit['unit_id']}: source does not include its generated research-status panel")
        if "chapters/" in text and "{{< include" in text and "../generated/" not in text:
            errors.append(f"{unit['unit_id']}: source appears to include a live technical chapter")
        if state == "target_length_reached_internal_review_pending" and not (
            unit["target_min_words"] <= unit["visible_word_count"] <= unit["target_max_words"]
        ):
            errors.append(f"{unit['unit_id']}: false target-length completion")
        if unit.get("owner_support_states") != ["argument"]:
            errors.append(f"{unit['unit_id']}: routed owner support changed or was combined")
        panel_path = EDITION / "generated" / f"{unit['unit_id']}-status.qmd"
        if panel_path.is_file():
            panel = panel_path.read_text(encoding="utf-8")
            for owner_id in unit["owner_ids"]:
                owner_url = f"https://corbensorenson.github.io/asi-stack-book/chapters/{owner_id}.html"
                if owner_url not in panel:
                    errors.append(f"{unit['unit_id']}: missing discoverable owner route {owner_id}")
    unit_01 = next((unit for unit in units if unit.get("unit_id") == "unit-01"), None)
    if unit_01 is None or unit_01.get("state") != "target_length_reached_internal_review_pending":
        errors.append("Unit 1 has not reached its drafting target")
    else:
        text = (EDITION / unit_01["source_file"]).read_text(encoding="utf-8")
        for fragment in UNIT_01_REQUIRED:
            if fragment not in text:
                errors.append(f"Unit 1 missing required argument boundary: {fragment!r}")
    unit_02 = next((unit for unit in units if unit.get("unit_id") == "unit-02"), None)
    if unit_02 is None or unit_02.get("state") != "target_length_reached_internal_review_pending":
        errors.append("Unit 2 has not reached its drafting target")
    else:
        text = (EDITION / unit_02["source_file"]).read_text(encoding="utf-8")
        for fragment in UNIT_02_REQUIRED:
            if fragment not in text:
                errors.append(f"Unit 2 missing required argument boundary: {fragment!r}")
    unit_03 = next((unit for unit in units if unit.get("unit_id") == "unit-03"), None)
    if unit_03 is None or unit_03.get("state") != "target_length_reached_internal_review_pending":
        errors.append("Unit 3 has not reached its drafting target")
    else:
        text = (EDITION / unit_03["source_file"]).read_text(encoding="utf-8")
        for fragment in UNIT_03_REQUIRED:
            if fragment not in text:
                errors.append(f"Unit 3 missing required argument boundary: {fragment!r}")
    unit_04 = next((unit for unit in units if unit.get("unit_id") == "unit-04"), None)
    if unit_04 is None or unit_04.get("state") != "target_length_reached_internal_review_pending":
        errors.append("Unit 4 has not reached its drafting target")
    else:
        text = (EDITION / unit_04["source_file"]).read_text(encoding="utf-8")
        for fragment in UNIT_04_REQUIRED:
            if fragment not in text:
                errors.append(f"Unit 4 missing required argument boundary: {fragment!r}")
    unit_23 = next((unit for unit in units if unit.get("unit_id") == "unit-23"), None)
    if unit_23 is None or unit_23.get("state") != "target_length_reached_internal_review_pending":
        errors.append("Unit 23 has not reached its drafting target")
    else:
        text = (EDITION / unit_23["source_file"]).read_text(encoding="utf-8")
        for fragment in UNIT_23_REQUIRED:
            if fragment not in text:
                errors.append(f"Unit 23 missing required argument boundary: {fragment!r}")
    unit_05 = next((unit for unit in units if unit.get("unit_id") == "unit-05"), None)
    if unit_05 is None or unit_05.get("state") != "target_length_reached_internal_review_pending":
        errors.append("Unit 5 has not reached its drafting target")
    else:
        text = (EDITION / unit_05["source_file"]).read_text(encoding="utf-8")
        for fragment in UNIT_05_REQUIRED:
            if fragment not in text:
                errors.append(f"Unit 5 missing required argument boundary: {fragment!r}")
    unit_06 = next((unit for unit in units if unit.get("unit_id") == "unit-06"), None)
    if unit_06 is None or unit_06.get("state") != "target_length_reached_internal_review_pending":
        errors.append("Unit 6 has not reached its drafting target")
    else:
        text = (EDITION / unit_06["source_file"]).read_text(encoding="utf-8")
        for fragment in UNIT_06_REQUIRED:
            if fragment not in text:
                errors.append(f"Unit 6 missing required argument boundary: {fragment!r}")
    unit_07 = next((unit for unit in units if unit.get("unit_id") == "unit-07"), None)
    if unit_07 is None or unit_07.get("state") != "target_length_reached_internal_review_pending":
        errors.append("Unit 7 has not reached its drafting target")
    else:
        text = (EDITION / unit_07["source_file"]).read_text(encoding="utf-8")
        for fragment in UNIT_07_REQUIRED:
            if fragment not in text:
                errors.append(f"Unit 7 missing required argument boundary: {fragment!r}")
    unit_08 = next((unit for unit in units if unit.get("unit_id") == "unit-08"), None)
    if unit_08 is None or unit_08.get("state") != "target_length_reached_internal_review_pending":
        errors.append("Unit 8 has not reached its drafting target")
    else:
        text = (EDITION / unit_08["source_file"]).read_text(encoding="utf-8")
        for fragment in UNIT_08_REQUIRED:
            if fragment not in text:
                errors.append(f"Unit 8 missing required argument boundary: {fragment!r}")
    unit_09 = next((unit for unit in units if unit.get("unit_id") == "unit-09"), None)
    if unit_09 is None or unit_09.get("state") != "target_length_reached_internal_review_pending":
        errors.append("Unit 9 has not reached its drafting target")
    else:
        text = (EDITION / unit_09["source_file"]).read_text(encoding="utf-8")
        for fragment in UNIT_09_REQUIRED:
            if fragment not in text:
                errors.append(f"Unit 9 missing required argument boundary: {fragment!r}")
    unit_10 = next((unit for unit in units if unit.get("unit_id") == "unit-10"), None)
    if unit_10 is None or unit_10.get("state") != "target_length_reached_internal_review_pending":
        errors.append("Unit 10 has not reached its drafting target")
    else:
        text = (EDITION / unit_10["source_file"]).read_text(encoding="utf-8")
        for fragment in UNIT_10_REQUIRED:
            if fragment not in text:
                errors.append(f"Unit 10 missing required argument boundary: {fragment!r}")
    unit_11 = next((unit for unit in units if unit.get("unit_id") == "unit-11"), None)
    if unit_11 is None or unit_11.get("state") != "target_length_reached_internal_review_pending":
        errors.append("Unit 11 has not reached its drafting target")
    else:
        text = (EDITION / unit_11["source_file"]).read_text(encoding="utf-8")
        for fragment in UNIT_11_REQUIRED:
            if fragment not in text:
                errors.append(f"Unit 11 missing required argument boundary: {fragment!r}")
    unit_12 = next((unit for unit in units if unit.get("unit_id") == "unit-12"), None)
    if unit_12 is None or unit_12.get("state") != "target_length_reached_internal_review_pending":
        errors.append("Unit 12 has not reached its drafting target")
    else:
        text = (EDITION / unit_12["source_file"]).read_text(encoding="utf-8")
        for fragment in UNIT_12_REQUIRED:
            if fragment not in text:
                errors.append(f"Unit 12 missing required argument boundary: {fragment!r}")
    unit_13 = next((unit for unit in units if unit.get("unit_id") == "unit-13"), None)
    if unit_13 is None or unit_13.get("state") != "target_length_reached_internal_review_pending":
        errors.append("Unit 13 has not reached its drafting target")
    else:
        text = (EDITION / unit_13["source_file"]).read_text(encoding="utf-8")
        for fragment in UNIT_13_REQUIRED:
            if fragment not in text:
                errors.append(f"Unit 13 missing required argument boundary: {fragment!r}")
    unit_14 = next((unit for unit in units if unit.get("unit_id") == "unit-14"), None)
    if unit_14 is None or unit_14.get("state") != "target_length_reached_internal_review_pending":
        errors.append("Unit 14 has not reached its drafting target")
    else:
        text = (EDITION / unit_14["source_file"]).read_text(encoding="utf-8")
        for fragment in UNIT_14_REQUIRED:
            if fragment not in text:
                errors.append(f"Unit 14 missing required argument boundary: {fragment!r}")
    unit_15 = next((unit for unit in units if unit.get("unit_id") == "unit-15"), None)
    if unit_15 is None or unit_15.get("state") != "target_length_reached_internal_review_pending":
        errors.append("Unit 15 has not reached its drafting target")
    else:
        text = (EDITION / unit_15["source_file"]).read_text(encoding="utf-8")
        for fragment in UNIT_15_REQUIRED:
            if fragment not in text:
                errors.append(f"Unit 15 missing required argument boundary: {fragment!r}")
    unit_16 = next((unit for unit in units if unit.get("unit_id") == "unit-16"), None)
    if unit_16 is None or unit_16.get("state") != "target_length_reached_internal_review_pending":
        errors.append("Unit 16 has not reached its drafting target")
    else:
        text = (EDITION / unit_16["source_file"]).read_text(encoding="utf-8")
        for fragment in UNIT_16_REQUIRED:
            if fragment not in text:
                errors.append(f"Unit 16 missing required argument boundary: {fragment!r}")
    unit_17 = next((unit for unit in units if unit.get("unit_id") == "unit-17"), None)
    if unit_17 is None or unit_17.get("state") != "target_length_reached_internal_review_pending":
        errors.append("Unit 17 has not reached its drafting target")
    else:
        text = (EDITION / unit_17["source_file"]).read_text(encoding="utf-8")
        for fragment in UNIT_17_REQUIRED:
            if fragment not in text:
                errors.append(f"Unit 17 missing required argument boundary: {fragment!r}")
    unit_18 = next((unit for unit in units if unit.get("unit_id") == "unit-18"), None)
    if unit_18 is None or unit_18.get("state") != "target_length_reached_internal_review_pending":
        errors.append("Unit 18 has not reached its drafting target")
    else:
        text = (EDITION / unit_18["source_file"]).read_text(encoding="utf-8")
        for fragment in UNIT_18_REQUIRED:
            if fragment not in text:
                errors.append(f"Unit 18 missing required argument boundary: {fragment!r}")
    unit_19 = next((unit for unit in units if unit.get("unit_id") == "unit-19"), None)
    if unit_19 is None or unit_19.get("state") != "target_length_reached_internal_review_pending":
        errors.append("Unit 19 has not reached its drafting target")
    else:
        text = (EDITION / unit_19["source_file"]).read_text(encoding="utf-8")
        for fragment in UNIT_19_REQUIRED:
            if fragment not in text:
                errors.append(f"Unit 19 missing required argument boundary: {fragment!r}")
    unit_20 = next((unit for unit in units if unit.get("unit_id") == "unit-20"), None)
    if unit_20 is None or unit_20.get("state") != "target_length_reached_internal_review_pending":
        errors.append("Unit 20 has not reached its drafting target")
    else:
        text = (EDITION / unit_20["source_file"]).read_text(encoding="utf-8")
        for fragment in UNIT_20_REQUIRED:
            if fragment not in text:
                errors.append(f"Unit 20 missing required argument boundary: {fragment!r}")
    unit_21 = next((unit for unit in units if unit.get("unit_id") == "unit-21"), None)
    if unit_21 is None or unit_21.get("state") != "target_length_reached_internal_review_pending":
        errors.append("Unit 21 has not reached its drafting target")
    else:
        text = (EDITION / unit_21["source_file"]).read_text(encoding="utf-8")
        for fragment in UNIT_21_REQUIRED:
            if fragment not in text:
                errors.append(f"Unit 21 missing required argument boundary: {fragment!r}")
    unit_22 = next((unit for unit in units if unit.get("unit_id") == "unit-22"), None)
    if unit_22 is None or unit_22.get("state") != "target_length_reached_internal_review_pending":
        errors.append("Unit 22 has not reached its drafting target")
    else:
        text = (EDITION / unit_22["source_file"]).read_text(encoding="utf-8")
        for fragment in UNIT_22_REQUIRED:
            if fragment not in text:
                errors.append(f"Unit 22 missing required argument boundary: {fragment!r}")
    unit_24 = next((unit for unit in units if unit.get("unit_id") == "unit-24"), None)
    if unit_24 is None or unit_24.get("state") != "target_length_reached_internal_review_pending":
        errors.append("Unit 24 has not reached its drafting target")
    else:
        text = (EDITION / unit_24["source_file"]).read_text(encoding="utf-8")
        for fragment in UNIT_24_REQUIRED:
            if fragment not in text:
                errors.append(f"Unit 24 missing required argument boundary: {fragment!r}")
    unit_25 = next((unit for unit in units if unit.get("unit_id") == "unit-25"), None)
    if unit_25 is None or unit_25.get("state") != "target_length_reached_internal_review_pending":
        errors.append("Unit 25 has not reached its drafting target")
    else:
        text = (EDITION / unit_25["source_file"]).read_text(encoding="utf-8")
        for fragment in UNIT_25_REQUIRED:
            if fragment not in text:
                errors.append(f"Unit 25 missing required argument boundary: {fragment!r}")
    unit_26 = next((unit for unit in units if unit.get("unit_id") == "unit-26"), None)
    if unit_26 is None or unit_26.get("state") != "target_length_reached_internal_review_pending":
        errors.append("Unit 26 has not reached its drafting target")
    else:
        text = (EDITION / unit_26["source_file"]).read_text(encoding="utf-8")
        for fragment in UNIT_26_REQUIRED:
            if fragment not in text:
                errors.append(f"Unit 26 missing required argument boundary: {fragment!r}")
    if manifest.get("support_state_effect") != "none" or manifest.get("release_effect") != "none":
        errors.append("Human Reader drafting changed support or release state")
    status = json.loads(STATUS.read_text(encoding="utf-8"))["editorial_product_migration"]
    expected_status = {
        "human_reader_current_manifest_path": "editions/reader_manuscript/current/manifest.json",
        "human_reader_started_unit_count": manifest.get("started_unit_count"),
        "human_reader_target_length_unit_count": manifest.get("target_length_unit_count"),
        "human_reader_visible_word_count": manifest.get("visible_word_count"),
    }
    for field, value in expected_status.items():
        if status.get(field) != value:
            errors.append(f"roadmap Human Reader status drift: {field}")
    return errors


def main() -> None:
    expected, outputs = build()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    crosswalk = json.loads(CROSSWALK.read_text(encoding="utf-8"))
    expected_crosswalk = json.loads(outputs[CROSSWALK])
    errors = validate(manifest, expected, crosswalk, expected_crosswalk)
    stale = [
        path.relative_to(ROOT).as_posix()
        for path, text in outputs.items()
        if not path.is_file() or path.read_text(encoding="utf-8") != text
    ]
    if stale:
        errors.append("stale generated Human Reader derivatives: " + ", ".join(stale))

    altered = copy.deepcopy(manifest)
    altered["units"][0]["owner_ids"] = []
    if not validate(altered, expected, crosswalk, expected_crosswalk):
        errors.append("negative control accepted: owner-route loss")
    altered = copy.deepcopy(manifest)
    altered["units"][22]["visible_word_count"] = 1
    if not validate(altered, expected, crosswalk, expected_crosswalk):
        errors.append("negative control accepted: false length completion")
    altered = copy.deepcopy(manifest)
    altered["support_state_effect"] = "promoted"
    if not validate(altered, expected, crosswalk, expected_crosswalk):
        errors.append("negative control accepted: support laundering")
    altered_crosswalk = copy.deepcopy(crosswalk)
    altered_crosswalk["units"][0]["owners"] = []
    if not validate(manifest, expected, altered_crosswalk, expected_crosswalk):
        errors.append("negative control accepted: crosswalk owner-edge loss")

    if errors:
        raise SystemExit("Human Reader current validation failed:\n - " + "\n - ".join(errors))
    print(
        f"Human Reader current validation passed: {manifest['started_unit_count']}/26 units started, "
        f"{manifest['target_length_unit_count']} at target length, 87 owners routed once, "
        f"{manifest['visible_word_count']} visible words, and 4 rejecting controls."
    )


if __name__ == "__main__":
    main()
