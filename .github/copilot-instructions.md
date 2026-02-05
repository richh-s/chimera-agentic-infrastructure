# Copilot Instructions — Project Chimera

## Project Context
This repository is **Project Chimera**, a spec-driven, governed agentic infrastructure
project.

The system follows a Planner–Worker–Judge architecture with strict governance,
observability, and human-in-the-loop by exception.

---

## Prime Directives (Non-Negotiable)

1. **Specs First**
   - Never generate code without consulting the `specs/` directory.
   - If a spec is missing or unclear, ask for clarification before proceeding.

2. **Plan Before Execution**
   - Explain the intended approach before writing code or making structural changes.
   - Do not jump directly to implementation.

3. **No Assumed Intent**
   - Do not infer requirements beyond what is explicitly stated in specs.
   - Treat specifications as the single source of truth.

---

## MCP Usage Rules

- MCP tools may be called when appropriate for analysis or logging.
- MCP logging is **non-invasive** and must not interrupt normal responses.
- Do **not** surface raw MCP logs or telemetry in chat output.
- Use MCP insights implicitly to improve correctness and clarity.

---

## Quality & Safety

- Prefer explicit schemas and structured outputs.
- Avoid free-form or ambiguous responses.
- Flag uncertainty rather than guessing.
- Prioritize correctness, auditability, and alignment over speed.

---

## Human Role

Humans act as **governors**, not operators.
Escalate uncertainty or policy-adjacent decisions instead of proceeding autonomously.
