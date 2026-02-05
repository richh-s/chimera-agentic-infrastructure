# Project Chimera — Developer Tooling Strategy (MCP)

> **Scope:** Developer Experience Only  
> **Applies To:** Humans and AI coding assistants during development  
> **Out of Scope:** Agent runtime execution (see `/skills`)

---

## 1. Purpose

This document defines the **developer tooling layer** for Project Chimera.

Project Chimera uses the **Model Context Protocol (MCP)** to provide a governed,
auditable interface between the AI coding assistant and the local development
environment.

The goal is to:
- Enable productive development
- Preserve traceability and auditability
- Prevent uncontrolled or implicit system access
- Enforce spec-driven workflows

---

## 2. Tooling Philosophy

Project Chimera follows the principle of **Isolation by Intent**.

- **Developer Tools** exist to help build and inspect the system.
- **Runtime Agents** never receive these tools.
- Access is granted based on role, not convenience.

This separation ensures that development power does not leak into runtime autonomy.

---

## 3. Configured MCP Servers (Developer Layer)

The following MCP servers are enabled in the developer’s IDE to support
Chimera development.

| MCP Server | Purpose | Capabilities |
|-----------|--------|-------------|
| **Filesystem MCP** | Governed file access | Read/write source files, specs, and documentation |
| **Git MCP** | Version control | View diffs, check status, create commits |
| **Sequential Thinking MCP** | Reasoning enforcement | Require structured planning before implementation |
| **Web Search MCP** | Technical research | Read-only access to external documentation |

---

## 4. Tool Responsibilities & Constraints

### 4.1 Filesystem MCP

**Purpose:**  
Enable controlled interaction with the Chimera repository.

**Allowed:**
- Read project files
- Modify source code and documentation
- Update specs with human approval

**Forbidden:**
- Access outside the repository root
- Access to system files, secrets, or environment configs

---

### 4.2 Git MCP

**Purpose:**  
Ensure all changes are traceable and auditable.

**Allowed:**
- Inspect repository state
- Generate diffs
- Create commits with descriptive messages

**Constraints:**
- No force pushes
- Commit history is treated as an audit log

---

### 4.3 Sequential Thinking MCP

**Purpose:**  
Prevent unplanned or speculative coding.

**Usage Rule:**
- Must be invoked for any non-trivial change
- Used to outline reasoning and implementation steps before code is written

This supports Chimera’s **Plan → Execute → Review** model.

---

### 4.4 Web Search MCP

**Purpose:**  
Support real-time research during development.

**Allowed:**
- Read-only queries for public technical documentation
- API reference lookup

**Forbidden:**
- Data scraping
- Credential harvesting
- Persistent storage of external content

---

## 5. Governance & Guardrails

The following rules apply to all developer tooling:

- Tools are **assistive**, not autonomous
- Tool usage must not bypass specifications
- All meaningful changes must be explainable and reviewable
- Specs remain the single source of truth

Tooling does not grant execution authority.

---

## 6. Explicit Non-Goals

This tooling layer does **not**:
- Execute runtime agent actions
- Publish content
- Make governance decisions
- Replace human review

Those responsibilities belong to the **runtime skill layer** and **Judge/HITL** processes.

---

## 7. Separation from Runtime Skills

Developer MCP tools:
- Have higher privilege
- Operate during development only
- Are never exposed to Worker agents

Runtime agents interact exclusively through **defined Skills**
documented under the `/skills` directory.

---

## 8. Summary

This tooling strategy enables safe, traceable development of Project Chimera
while preserving strict boundaries between:
- Human development workflows
- AI-assisted coding
- Autonomous agent execution

