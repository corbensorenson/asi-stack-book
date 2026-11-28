# SciFact compact reading retest rubric

Score decision, determining citation, and scope as separate binary fields. A locator must identify the exact run, case, or protocol section that supports the facts. Retain a reason for each partial score and count unsupported numerical claims separately.

| ID | Required decision facts | Determining citation | Scope |
|---|---|---|---|
| SO1 | Holds rose 212 to 247, an increase of 35. Holds with annotated evidence rose 121 to 151, an increase of 30. | Reserved SciFact run's triage table | On the reserved split. Counts characterize routed cases, with review time or labor unmeasured. |
| SO2 | Document-only had 16 unsupported, 47 held, and 20,748 input tokens. Sentence-only had 17 unsupported, 45 held, and 19,725 input tokens. | Four rankings on fresh citation papers | Tokens record model input. Serving time or energy stays unmeasured. |
| SO3 | First arm 52/73 (about 71.2%). Three-paper arm 81/105 (about 77.1%). Held claims are outside the fractions. | Three-paper comparison table | Unsupported means failure under the finite benchmark's annotations and rule. It does not estimate real-world scientific error prevalence. |
| SO4 | 12 unjudged papers, one pooled rationale, two incomplete human citations. Judge the paper, obtain human highlight annotations, or improve sentence selection respectively. | Retrospective scoring-ceiling chapter passage | The catalog and annotations are incomplete, and the two-sentence rule can miss valid evidence. |
| SE1 | Train for development, labeled dev reserved. Exclude claim 3 and claims sharing its cited paper because the dataset card illustrates claim 3. | Pinned protocol's freeze and adjudicate section | This split and exclusion do not establish lack of pretraining exposure. |
| SE2 | Maximize the strongest nonneutral score minus the neutral score; ties by document rank. Use annotations only after selection. | Pinned three-paper protocol | Same candidate catalog/ranker or model shared across compared arms, or labels used only for assessment of the frozen comparison. |
| SE3 | Human paper 18064113, baseline 54468511, document-only 15432317. All four held. | Published claim 83 case or exact pinned result/annotation | One certifiable case. Eligible human evidence exists but the selected papers were unjudged; a hold does not settle scientific truth. |
| SE4 | Run `score.py select` and `score.py evaluate` from the pinned checkout using retained predictions; no new prediction-generation step needed. | Pinned protocol's reproduce section | Replay checks scoring and decisions on retained evidence. It does not independently verify inference, generalization, or data reconstruction. |
