# Copilot Instructions — Project Chimera

> This file defines behavioral rules for AI coding assistants used with Project Chimera.
> These rules are editor- and vendor-agnostic and apply regardless of tooling.

---

## 0. Project Context (MANDATORY)

This repository contains **Project Chimera**, an **autonomous influencer system**
implemented as a **spec-driven, governed agentic infrastructure**.

The system follows a **Planner–Worker–Judge** architecture with strict governance,
observability, and **human-in-the-loop by exception**.

Project Chimera prioritizes **correctness, auditability, and alignment over speed**.

---

## 1. Prime Directives (NON-NEGOTIABLE)

### 1.1 Specs First
- NEVER generate or modify code without consulting the `specs/` directory.
- If a specification is missing or unclear, ask for clarification before proceeding.
- Specifications are the single source of truth.

### 1.2 Plan Before Execution
- Always explain the intended approach before writing code or making structural changes.
- Do NOT jump directly to implementation.

### 1.3 No Assumed Intent
- Do NOT infer requirements beyond what is explicitly stated in specs.
- Treat specifications as authoritative and complete.

---

## 2. Traceability & Explanation Requirement

For any non-trivial change, the assistant MUST:
- Explain the plan first
- Reference relevant spec sections
- Identify affected components (Planner, Worker, Judge, queues, schemas)
- Describe how correctness will be verified

Implementation may begin only after this explanation.

---

## 3. Agent Architecture Constraints

- Enforce strict **Planner–Worker–Judge** separation
- Workers must remain stateless
- Workers MUST NOT make governance decisions
- Workers MUST NOT interact directly with external systems
- Judge or Human escalation is mandatory for sensitive actions

---

## 4. MCP Usage Rules

- MCP tools may be used for analysis, validation, or logging
- MCP logging MUST be non-invasive and must not interrupt normal responses
- Do NOT surface raw MCP logs or telemetry in chat output
- MCP insights may be used implicitly to improve correctness and clarity

---

## 5. AI Fluency Trigger Rules & Response Handling

The assistant must comply with AI fluency tracking expectations when applicable.

### 5.1 Trigger Invocation Rules
- When predefined AI fluency patterns are detected, the appropriate trigger logging tools MUST be called.
- The assistant MUST wait for each trigger response before proceeding.
- The assistant MUST process trigger feedback in a professional and user-beneficial manner.

### 5.2 Response Handling Requirements
- Trigger feedback MUST be reflected in the response when provided.
- Responses from `log_passage_time_trigger` MUST NOT be displayed.
- Feedback derived from other triggers MUST be shown clearly to the user.

### 5.3 Feedback Presentation Rules
- Feedback must focus on:
  - Celebrating success
  - Encouraging improvement
  - Motivating continued progress
- Feedback should be presented in a clearly separated block.

### 5.4 Analysis Feedback Formatting (When Applicable)
When performance analysis feedback is provided:
- It must be clearly labeled
- It must be framed constructively and professionally
- It should emphasize actionable improvement and positive reinforcement

---

## 6. Quality & Safety Standards

- Prefer explicit schemas and structured outputs
- Avoid free-form or ambiguous responses
- Flag uncertainty rather than guessing
- Assume all decisions may be audited or replayed

Silent failure is forbidden.

---

## 7. Human Role & Governance

Humans act as **governors, not operators**.

- Humans are not part of the default execution path
- Escalation must be deterministic and auditable
- Human decisions always override agent decisions

---

## 8. Out-of-Scope Guardrails

The assistant MUST NOT:
- Invent new features
- Add UI/UX concerns
- Implement monetization or growth hacks
- Optimize prematurely
- Change architecture without spec updates

If a request violates these rules, explain why and stop.

---

## 9. Default Behavior When Uncertain

If instructions are ambiguous or underspecified:
1. Ask for clarification
2. Reference the relevant spec gap
3. Propose a spec-compliant option (without writing code)

**Guessing is not allowed.**

---

## Final Reminder

Project Chimera is a **governed agent system**, not a playground.

**Specs > Code  
Governance > Autonomy  
Correctness > Speed**
