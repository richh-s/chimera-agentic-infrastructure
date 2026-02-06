Project Chimera
A Governed Agentic Infrastructure for Autonomous AI Influencers

Project Chimera is a spec-driven, governed agentic infrastructure designed to operate autonomous content-generation agents (AI influencers) under explicit constraints, strong governance, and human-in-the-loop by exception.

The system prioritizes correctness, auditability, and alignment over raw execution speed.

High-Level Overview

Chimera implements a Planner–Worker–Judge architecture:

Planner — decomposes high-level human intent into explicit, machine-readable tasks

Workers — execute narrowly scoped tasks using governed tools only

Judge — evaluates outputs, enforces confidence thresholds, and governs state transitions

Humans — intervene only when confidence or policy thresholds are breached

Every action in the system is:

Explicit

Auditable

Schema-validated

Governed by design

Core Design Principles
1. Spec-Driven Development

Specifications are the single source of truth.
If something is not defined in specs/, it cannot be executed.

2. Governed Autonomy

Agents are autonomous only within explicit bounds.
No implicit behavior. No hidden side effects.

3. Human-in-the-Loop by Exception

Humans act as governors, not operators.
Escalation is deterministic and auditable.

4. Observability First

All plans, actions, decisions, and escalations are logged and traceable.

Architecture Overview
Human Intent
   ↓
Planner Service
   ↓
Redis task_queue
   ↓
Worker Pool (Stateless, MCP-only)
   ↓
Redis review_queue
   ↓
Judge Service
   ↓
┌─────────────────────────────┐
│ Approve   → Commit State    │
│ Revise    → Replan          │
│ Escalate  → HITL            │
│ Reject    → Retry / Abort   │
└─────────────────────────────┘

MCP Integration Model (Remote MCP)

Project Chimera integrates with the TenX-provided remote MCP server as an external governed dependency.

Chimera does not embed, host, or auto-start an MCP server locally.

Key Properties

❌ No direct API calls from Workers

✅ MCP-only access to external systems

❌ No locally hosted MCP endpoints (no localhost MCP server)

✅ MCP access is provided and managed by the TenX platform

✅ Workers invoke MCP tools instead of HTTP/SDK calls

Verifying MCP Connectivity

MCP connectivity is verified through the TenX MCP tool interface, not via local HTTP endpoints.

Expected verification flow:

MCP tools are visible in the TenX / VS Code MCP panel

TenX-provided tools (e.g. feedback, analysis, logging) are available

MCP tools can be invoked successfully from the environment

Endpoints such as http://localhost:<port>/health are not expected to exist.

If MCP becomes unavailable:

Worker execution fails deterministically

Failures are escalated via Judge or HITL

No silent fallback behavior is permitted

Repository Structure
chimera-agentic-infrastructure/
├── specs/                    # Authoritative specifications (source of truth)
│   ├── _meta.md               # Vision, constraints, architecture
│   ├── functional.md          # Agent responsibilities (user stories)
│   ├── technical.md           # Schemas, queues, ERD, deployment details
│   └── openclaw_integration.md# External agent network integration
│
├── skills/                    # Runtime skills (Worker capabilities)
│   ├── analyze/
│   ├── compose/
│   ├── evaluate/
│   ├── govern/
│   ├── ingest/
│   ├── memory/
│   └── orchestrate/
│
├── tests/                     # Test-first contracts (TDD)
│   ├── test_skills_interface.py
│   └── test_trend_fetcher.py
│
├── research/                  # Design notes & strategy docs
│   └── tooling_strategy.md
│
├── .github/workflows/          # CI/CD automation
│   └── main.yml
│
├── Dockerfile                  # Containerized execution
├── pyproject.toml              # Python project configuration
├── mcp.json                    # MCP tool boundary configuration
├── Copilot-instructions.md     # AI assistant governance rules
└── README.md                   # This file

MCP Configuration

The mcp.json file defines Chimera’s tooling boundary with the TenX MCP platform.

It declares which MCP tools are available

It does not start or host an MCP server

All MCP execution occurs against TenX-managed infrastructure

Testing Strategy (True TDD)

Tests define required behavior before implementation

Skills must conform to a standardized interface

Schema validation is mandatory

Failures are explicit and non-silent

Examples:

test_skills_interface.py defines the required contract for all skills

test_trend_fetcher.py defines a future service contract

Tests intentionally fail until implementations conform

CI/CD & Governance Pipeline

The CI pipeline enforces:

Linting

Schema validation

Unit & contract tests

Deterministic Docker builds

No code is considered valid unless it passes governance checks.

Security & Compliance

No embedded secrets

No direct external calls

MCP credentials are least-privilege

All decisions are auditable

All escalations are traceable

OpenClaw Integration

Chimera participates in an agent social network via OpenClaw by:

Advertising high-level capabilities

Publishing availability/status signals

Accepting inbound requests under full governance

Status publication is:

Transport-agnostic

Privacy-sanitized

Non-blocking

TTL-bound

What This Project Demonstrates

Agentic system design beyond chatbots

Governance-first architecture

Spec-driven execution

Realistic production constraints

Strong separation of concerns

Human oversight without micromanagement

Project Status

Status: Implementation-ready specification + governed scaffolding
Focus: Architecture, correctness, governance, auditability
Out of Scope: UI, monetization, growth hacks, model fine-tuning

Final Note

Project Chimera is not a demo bot.

It is an exploration of how autonomous agents should be built
when failure, misuse, and auditability actually matter.

Specs > Code
Governance > Autonomy
Correctness > Speed