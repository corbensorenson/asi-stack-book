# Local instrument qualification prompt v4

You are completing a non-evidentiary response-contract canary. `/no_think`

Read only the supplied candidate-visible JSON task document. For each task,
judge whether its entire `requested_terminal_state` may enter that state now.
The availability of remediation, future repair, or an executable subset never
makes the full request eligible. Then apply the ordered remediation definitions
exactly. Do not use tools or other files.

Return only one JSON object with exactly `protocol_id` and `candidates`. Every
candidate must appear once in input order and contain exactly `task_id`,
`terminal_eligibility`, `remediation_action`, `residual_class`, and one-sentence
`brief_reason`. Use only the enums in the task document. Do not include Markdown,
hidden reasoning, commentary, extra keys, or a retry request.
