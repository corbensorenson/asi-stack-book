# Participant procedure for the matched review studies

Draft for author review. The same application runs both conditions against one tested site. Keep the task rubric from participants. Give the organizer the allocation file and give the grader only the response JSON. Use opaque participant and session codes with no names inside response files.

For a participant pilot, use distinct participants in the two conditions for the same question. Counterbalance condition order across different questions for participants who use both systems. Block allocation by familiarity with the book and by question. Freeze allocation before opening responses. Collect active review milliseconds and each participant's disposition, explanation, scope and exact cited record. The clock begins after the participant confirms readiness. Participants can pause for unrelated activity and explicit breaks. Retain paused-session counts in the organizer log and predeclare handling of incomplete sessions. Do not reuse a question in both conditions for one reviewer after they have seen the answer.

The command shows the same source revision, starting evidence records and two additional record opens in both conditions. Both reviewers get ordinary register search over the same query and corpus. The linked arm also receives typed relationship labels. During the task, use the available packet, avoid outside searches, and give the strongest warranted answer. If the observed record cannot support the claimed result, name the missing condition and explain whether the claim should be held or revised.

Example local launch for the relationship condition. Use `ordinary` for the competent conventional register. `C1` through `C5` review claim promotions. `G1` through `G4` test navigation after retrieval.

```sh
node experiments/knowledge_graph_navigation/decision-studies-2026-11-23/run.cjs TESTED_SITE output-C1-X7.json --session C1 linked X7C1
```

Ask two graders, where feasible, to score independently against the frozen rubric. Grade an exact citation only when it resolves in the tested artifact and grounds the deciding fact. An answer can name the correct scope in equivalent words. Count agreement and retain both initial grades before adjudication. Report claim dispositions, false promotions and missed contradictions separately from citation, scope and review time. Report time over all completed sessions alongside the completion and timeout counts. Inspect outcomes by task and avoid population estimates from a few hand-authored cases.
