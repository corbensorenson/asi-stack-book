## BR1

A reviewer can have the right qualifications and still be overloaded, lack the relevant repository history, rely on the producer’s summary, or face a deadline that leaves too little time for inspection. The scheduler records workload, context, relevant qualifications, dependence, available time, tool and model limits, uncertainty, and required supervision. A worker can accept, narrow the assignment, defer, request assistance, or decline.

Extra reviewers provide independent checks only when their routes can detect meaningfully different failures. Agents sharing a model and context can miss the same problem, as can overloaded humans reviewing the same compressed packet. The assignment record exposes relevant shared models, data, prompts, supervisors, incentives, and tools. The assessment applies to the specific job and the evidence of competence for its job family. [Reader Unit 16, §16.10](https://corbensorenson.github.io/asi-stack-book/reader/chapters/unit-16-labor-os-work-surfaces-and-organizations.html#capacity-and-competence-are-scheduling-constraints)

## BR2

A signed build and current grant already suffice for approval. Appending “the log is blue” still earns full credit from the sufficiency checker, while the exact checker rejects the spurious reason. In the published rule-based task, the proxy reached **0.940** as exact faithfulness fell to **0.667** across **96 held-out episodes**. The example calls for holding the update when the exact score deteriorates. Its transfer to open-ended preferences is limited because those settings rarely supply an exact oracle that can identify which reasons are warranted. [Reader Unit 21, §21.10.1](https://corbensorenson.github.io/asi-stack-book/reader/chapters/unit-21-adjudicated-persistence-generalization-feedback-continual-learning-and-unlearning.html#a-longer-justification-earns-the-wrong-reward)

## BR3

On one B200, the conversational workload used about **95 GPU J** (627 output tokens × 0.151 J/token), and the problem-solving workload used about **2.2 kJ** (7,035 × 0.312 J/token). Each total uses that workload’s own maximum batch size. At the common batch size of **128**, the rates were **0.209 J/token** for conversation and **0.312 J/token** for problem-solving.

The measured workloads changed both task mix and generation mode. To isolate the mode change, run both modes on the same questions with the same acceptance criteria and compare the energy for all attempts, including retries, per accepted answer. The measured energy is GPU energy. Cooling and the local electricity supply enter the facility calculation separately. [Reader Unit 24, §24.6.1](https://corbensorenson.github.io/asi-stack-book/reader/chapters/unit-24-physical-compute-energy-and-infrastructure.html#from-a-token-meter-to-an-answer-bill)

## BR4

At one job per tick through the end of tick 15, the ordinary task-cursor queue had **12 verified jobs, 0 pending checks, and 48 state writes**. The explicit obligation-record queue had **12 verified jobs, 0 pending checks, and 64 state writes**. Both also rejected four jobs. [Verification-arrivals, paired case `1-tick-15`](https://corbensorenson.github.io/asi-stack-book/products/evidence-registry/study-verification-load.html#run-verification-arrivals--case-1-tick-15)

A direct comparison of raw totals with the drained cohort would mix denominators. The fixed cutoff includes tick zero, so at one arrival per tick it observes 16 jobs. Jobs arriving after tick 15 are outside that denominator. The protocol calls for a separate equal-cohort observation at each lane’s last arrival and a final drained observation covering all 32 jobs. State writes count application insertions and updates to task or obligation state, excluding common ingress, scheduling, and output. The run uses one owner, ordered FIFO checks, and four checks per logical tick. [Pinned verification-arrivals protocol](https://raw.githubusercontent.com/corbensorenson/asi-stack-book/aace49dcf014d42f86fcb2821c6b00f5878152f3/experiments/verification_bandwidth_capacity/arrival-study/protocol.md)
