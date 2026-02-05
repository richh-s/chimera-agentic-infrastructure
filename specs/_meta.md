# Project Chimera — Master Specification (_meta)

## 1. Vision

Project Chimera is a **governed, agentic infrastructure** designed for operating autonomous content-generation agents (AI influencers) under explicit, hard-coded constraints.

The system is designed to:

* Translate high-level human intent into executable agent plans.
* Operate agents as first-class actors with specific roles, rather than linear scripts.
* Enforce governance, observability, and human oversight by default.
* Prevent uncontrolled autonomy or opaque decision-making.

**Chimera prioritizes correctness, auditability, and alignment over raw execution speed.**

---

## 2. What Chimera Is

* A **Planner–Worker–Judge** agent system.
* A spec-driven execution environment where every action is pre-validated.
* A controlled publisher of AI-generated media.
* A participant in an agent social network (e.g., OpenClaw Integration).

---

## 3. What Chimera Is NOT

* **Not a chatbot:** It is a goal-oriented execution engine, not a conversational interface.
* **Not a monolith:** It is a decoupled micro-agent architecture.
* **Not fully autonomous:** Agents cannot bypass human review for sensitive or low-confidence actions.
* **Not a traditional "Bot":** It does not use hard-coded scraping; it uses governed tools (MCP).

---

## 4. Core Design Principles

### 4.1 Spec-Driven Development

Specifications are the **sole source of truth**. Agents must never act based on implicit assumptions. If a task is not defined in the schema, it cannot be executed.

### 4.2 Governed Autonomy

Agents operate autonomously **only within explicitly defined bounds**. Every action must be explainable, attributable, and reversible where possible.

### 4.3 Human-in-the-Loop (HITL) by Exception

Humans do not micromanage agents. Humans intervene only when confidence thresholds are breached, policies are violated, or a "Blocked" state is reached. The human role is **governance, not execution**.

### 4.4 Observability First

Every agent decision, plan, and action must be:

* **Loggable:** Persistent record in the Audit Log.
* **Inspectable:** Viewable via the Trace ID.
* **Attributable:** Linked to a specific Agent ID and Human Intent.

---

## 5. High-Level Architecture Pattern

Chimera follows the **Planner–Worker–Judge** triad to ensure a separation of powers:

* **Planner Agent:** Decomposes high-level goals into a directed acyclic graph (DAG) of tasks.
* **Worker Agents:** Execute narrowly scoped tasks using MCP tools. They have no "sight" of the overall goal, only their specific task.
* **Judge Agent:** Evaluates outputs against acceptance criteria. It acts as the final gatekeeper before any state commit or external publication.

---

## 6. Constraints & Non-Negotiables

* **MCP Enforcement:** All external interactions (Social APIs, Web Search, Databases) MUST occur via Model Context Protocol (MCP). Direct `fetch` or `curl` calls from agent logic are forbidden.
* **Schema Strictness:** All inter-agent communication (Queues) must conform to the JSON schemas defined in `technical.md`.
* **Fail-Safe Publication:** No content is published to external platforms without a "Pass" decision from the Judge or a Human Governor.
* **Stateless Workers:** Workers must not retain internal state; they must rely on the context provided in the Task object.

---

## 7. Success Criteria

The system is considered successful if:

1. Agents can complete a full "Trend-to-Post" cycle without human intervention in 80% of cases.
2. 100% of "Low Confidence" errors are successfully caught by the Judge and escalated.
3. A full audit trail exists for every post, showing which tool retrieved the trend and which model generated the caption.
4. The system automatically throttles or stops if a budget or rate limit is reached.

---

## 8. Document Cross-Reference

To understand the full implementation of Project Chimera, this document must be read alongside:

* **`specs/functional.md`**: For agent user stories and acceptance criteria.
* **`specs/technical.md`**: For JSON schemas, ERD, and infrastructure scaling.
* **`specs/openclaw.md`**: For protocols regarding external agent communication.

---

## 9. Open Questions (To Be Resolved)

* **Cost Gating:** Determining the maximum "Compute + API" budget per campaign before an automatic "Hard Stop" is triggered.
* **Identity Sovereignty:** Whether Agent private keys (for signing posts) are stored in a centralized vault or handled per-deployment.
* **Long-term Memory:** The policy for how much "Campaign History" is injected into the Planner's context window versus retrieved via Vector Search.

---

