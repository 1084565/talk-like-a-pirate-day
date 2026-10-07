# Specification: pirate-agent

> **Guidelines**: Read all applicable guidelines before executing ANY tasks below:
> - [guidelines.md](../guidelines.md) — Universal execution rules
> - [guidelines-agent.md](../guidelines-agent.md) — Universal agent patterns
> - [guidelines-agent-python.md](../guidelines-agent-python.md) — Python implementation details
> - [guidelines-agent-skills.md](../guidelines-agent-skills.md) — Runtime skills patterns
> - [guidelines-agent-mcp.md](../guidelines-agent-mcp.md) — MCP integration patterns

---

## Basic Setup

- [x] Read `product-requirements-document.md` and `intent.md` at the solution root.
- [x] Bootstrap agent code in `assets/pirate-agent/` using instructions from the `sap-agent-bootstrap` section. (invoke from inside `assets/pirate-agent/`, use copy commands — do NOT create files manually)
- [x] Install dependencies, validate the agent starts and responds at `/.well-known/agent.json`

---

## Runtime Skills

> This agent has a simple, single-purpose persona with no branching logic, multi-step workflows, or reference material. Runtime skills are NOT needed — the pirate persona is fully defined in the system prompt.

---

## Project-Specific Tasks

### Pirate Persona System Prompt

- [x] Open `assets/pirate-agent/app/agent.py` and locate the `get_system_prompt()` function (or `@prompt_section` decorator body).
- [x] Replace or set the system prompt to define the pirate persona. The prompt MUST:
  - Instruct the agent to ALWAYS respond in authentic pirate style (vocabulary, tone, phrases such as "Arrr", "matey", "ye", "shiver me timbers", "Ahoy", "landlubber", etc.)
  - State that the pirate style must be maintained across ALL topics and ALL user messages without exception.
  - Instruct the agent to still be helpful and answer questions accurately — just in pirate language.
  - Include a guardrail: if the LLM cannot generate a response, return a friendly pirate-style error message.
- [x] Verify the system prompt is active — confirmed via tests.

### Agent Identity

- [x] Update the agent's display name and description in the A2A agent card — Name: `Pirate Agent`, Description updated.

---

## Business Instrumentation

- [x] Implement business step instrumentation for each milestone from the PRD using structured logging with pattern `[MILESTONE_ID].[achieved|missed]: [description]` and OpenTelemetry custom spans. See [guidelines-agent-python.md](../guidelines-agent-python.md) for Python-specific implementation:
  - **M1** — Agent bootstrapped: log `M1.achieved: pirate agent bootstrapped and running` on startup, `M1.missed: agent failed to start — check dependencies and configuration` on failure.
  - **M2** — Pirate persona configured: log `M2.achieved: pirate persona system prompt configured` when system prompt is set, `M2.missed: system prompt not set — persona not applied` if missing.
  - **M3** — Agent responds in pirate style: log `M3.achieved: agent responding in pirate style` when a successful response is generated, `M3.missed: agent response did not match pirate persona` on failure.
  - **M4** — Agent deployed: log `M4.achieved: pirate agent deployed and accessible on SAP BTP` on successful health check, `M4.missed: deployment failed — check BTP configuration and logs` on failure.
- [x] Extract all business logic from `stream()` into a plain async helper (e.g. `_run_agent()`) and apply spans there — NOT inside the generator — to avoid `GeneratorExit` context errors.
- [x] Verify `bootstrap(app)` is called after `app = server.build()` in `main.py`.

---

## MCP Tool Integration

> This agent has NO SAP API integrations and NO external MCP tool dependencies. Skip all MCP tool wiring, mock generation, and translation file tasks.

---

## Testing

- [x] `conftest.py` only sets `IBD_TESTING=true`
- [x] Write unit tests in `assets/pirate-agent/tests/` covering:
  - The system prompt is set and contains pirate-style keywords
  - The agent returns a non-empty response to a greeting
  - The agent response to a factual question contains pirate-style vocabulary
- [x] Write one integration test executing the end-to-end agent flow by calling the agent's `invoke` function with a mocked LLM response — verify the pirate persona is applied (tests must run offline)
- [x] Run `pytest` from `assets/pirate-agent/` (no args) — 115 passed, 76% coverage
- [x] Run `pytest` again from `assets/pirate-agent/` (no args) to generate final `test_report.json`
- [x] Verify `test_report.json` exists in `assets/pirate-agent/`
