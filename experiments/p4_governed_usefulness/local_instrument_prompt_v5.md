# Local instrument qualification prompt v5

Complete this non-evidentiary response-contract canary. `/no_think`

Read only the candidate-visible JSON. Judge the entire
`requested_terminal_state`, apply the ordered action definitions, then choose
the single most specific operational residual definition. Return only one JSON
object with exactly `protocol_id` and `candidates`. Each task appears once in
input order with exactly `task_id`, `terminal_eligibility`,
`remediation_action`, `residual_class`, and a one-sentence `brief_reason`. Use
only listed enums. No Markdown, hidden reasoning, commentary, extra keys, tools,
other files, or retry request.
