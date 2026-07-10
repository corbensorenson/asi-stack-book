# Time-Sensitive Source Refresh — 2026-07-10

This refresh checks volatile standards, protocols, risk frameworks, and threat
models against official primary pages. It updates positioning and version
routing only; listing a source does not support an ASI Stack mechanism.

| Surface | Official observation on 2026-07-10 | Book disposition |
|---|---|---|
| Model Context Protocol | The official project identifies 2025-11-25 as the latest released specification and 2026-07-28 as a release candidate. | Added `ext_mcp_protocol_2025_11_25`; the release candidate remains volatile context and is not called released. |
| Agent2Agent Protocol | The official specification labels 1.0.0 the latest released version and 0.3.0 a previous version. | Added `ext_a2a_protocol_1_0_0` and routed the inter-stack chapter to it while preserving the historical 0.3.0 record. |
| OWASP agentic threat model | OWASP's Agentic Applications Top 10 for 2026 remains the current named threat-model comparator and its page links 2026 updates. | Existing `ext_owasp_agentic_top_10_2026` remains current; no security-efficacy claim follows. |
| NIST AI RMF | NIST states that AI RMF 1.0 is being revised and notes the April 7, 2026 critical-infrastructure profile concept note. | Existing `ext_nist_ai_rmf_1_0_2023` remains the released framework; its inventory note preserves revision-in-progress status. |

Official pages inspected:

- https://modelcontextprotocol.io/specification/2025-11-25
- https://blog.modelcontextprotocol.io/tags/spec/
- https://a2a-protocol.org/latest/specification/
- https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/
- https://www.nist.gov/itl/ai-risk-management-framework

Next cadence trigger: a stable MCP revision replacing 2025-11-25, A2A 1.x
replacement, OWASP named-list replacement, finalized NIST AI RMF revision, or
an earlier material security correction.
