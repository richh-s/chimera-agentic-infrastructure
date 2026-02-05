# Project Chimera — Agent Skills (Runtime Layer)

This directory defines the **runtime Skills** available to Project Chimera agents.

A **Skill** is a governed, single-purpose capability that a **Worker Agent**
may invoke during execution. Skills provide *power*, but not *authority*.

Authority remains with the **Planner**, **Judge**, and **Human-in-the-Loop (HITL)**.

---

##  Quick Overview

| Layer | Purpose | Example Skills | Status |
|-------|---------|----------------|--------|
| Ingest | Content acquisition | `skill_media_harvester` | ✅ Active |
| Analyze | Signal extraction | `skill_content_analyzer` | ✅ Active |
| Govern | Safety & compliance | `skill_safety_validator` | ✅ Active |
| Compose | Content transformation | `skill_persona_publisher` | ✅ Active |
| Orchestrate | Workflow coordination | `skill_workflow_orchestrator` | ✅ Active |
| Evaluate | Performance analysis | `skill_engagement_evaluator` | ⏳ Planned |
| Memory | Long-term learning control | `skill_memory_curator` | ⏳ Planned |

---

## What a Skill Is

A Skill:
- Performs exactly one well-defined action
- Has explicit, machine-validated input/output contracts
- May interact with external systems **only via approved MCP Action Tools**
- Produces outputs that are always reviewed before state changes or publication
- Is fully traceable and auditable

---

## What a Skill Is NOT

A Skill does **not**:
- Make planning or orchestration decisions
- Maintain long-term memory
- Publish content autonomously
- Bypass safety, cost, or governance checks
- Write directly to system memory or source code

---

## Skill Invocation Rules

- Skills are invoked **only** by Worker Agents
- Each invocation must be tied to a Planner-issued Task
- Outputs are evaluated by the Judge before proceeding
- Low-confidence or policy-adjacent outputs trigger escalation

---

## Directory Structure & Responsibility Layers

Skills are organized by **intent-based layers** to prevent role leakage
and enforce clean reasoning boundaries.

###  Ingest — Content Acquisition
`ingest/`
- `skill_media_harvester`

###  Analyze — Signal Extraction & Understanding
`analyze/`
- `skill_vocal_analyzer`
- `skill_content_analyzer`
- `skill_trend_classifier`

###  Govern — Safety, Compliance & Economics
`govern/`
- `skill_safety_validator`
- `skill_cost_guard`

###  Compose — Content Transformation
`compose/`
- `skill_persona_publisher`

### Orchestrate — Workflow Coordination
`orchestrate/`
- `skill_workflow_orchestrator`

###  Evaluate — Feedback & Performance
`evaluate/`
- `skill_engagement_evaluator`

###  Memory — Learning & Retention Control
`memory/`
- `skill_memory_curator`

---

## Contract Specification Requirements

Every Skill **MUST** include a `contract.json` defining strict I/O guarantees.

### Required Contract Schema

```json
{
  "skill_name": "string",
  "version": "semver",
  "description": "string",
  "inputs": {
    "param": {
      "type": "string|number|boolean|array|object",
      "required": true,
      "validation": "regex|enum|range",
      "example": "example value"
    }
  },
  "outputs": {
    "result": {
      "type": "string|number|boolean|array|object",
      "description": "output description"
    }
  },
  "constraints": {
    "max_execution_time": "seconds",
    "rate_limit": "requests/time",
    "resource_limits": "memory/cpu"
  },
  "security": {
    "requires_auth": true,
    "allowed_domains": ["array"],
    "data_classification": "public|internal|confidential"
  }
}
Execution Flow
flowchart TD
    P[Planner] -->|Task + Context| W[Worker]
    W -->|Validate Inputs| S[Skill]
    S -->|Execute| E[External System via MCP]
    E -->|Results| J[Judge]
    J -->|Approve| C[Continue]
    J -->|Reject| F[Fail]
    J -->|Escalate| H[HITL Review]
Error Handling Standards
All Skills must return structured errors.

Error Categories
Validation Errors (400) — malformed inputs

Execution Errors (500) — tool/API failures

Policy Errors (403) — safety or cost violations

Error Response Format
json
{
  "error": true,
  "error_type": "validation|execution|policy",
  "message": "Human-readable description",
  "code": "ERROR_CODE",
  "details": {
    "parameter": "field",
    "constraint": "violation"
  },
  "suggestion": "next step"
}
Testing Requirements
Each Skill should include:

text
skill_example/
├── tests/
├── fixtures/
└── mocks/
Required Coverage
Contract validation

Error cases

MCP integration

Performance within constraints

Versioning & Deployment
Skill Versioning
Semantic Versioning (MAJOR.MINOR.PATCH)

Deployment States
State	Description	Judge Behavior
development	In testing	HITL required
staging	Pre-prod	Enhanced scrutiny
production	Live	Normal review
deprecated	Phasing out	Warning
retired	Disabled	Blocked
Security Audit Checklist
Before enabling any Skill:

Input validation enforced

Output sanitization applied

Rate limits defined

No hardcoded secrets

External dependencies pinned

Timeouts enforced

Resource limits defined

Audit logs enabled

Contribution Workflow
Propose via RFC

Define contract & SKILL.md

Security & governance review

Implement with tests

Stage deployment

Production release

Glossary
Term	Definition
Skill	Governed runtime capability
Contract	Machine-readable I/O spec
MCP	Model Context Protocol
Planner	Task creation component
Worker	Skill execution component
Judge	Output evaluation authority
HITL	Human-in-the-loop escalation
Layer	Intent-based skill grouping
Summary
Skills define what Chimera agents can do, not what they decide.