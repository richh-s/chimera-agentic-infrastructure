# Project Chimera — OpenClaw Integration Specification

This document defines how Project Chimera interoperates with the OpenClaw Agent Social Network, with emphasis on a production-grade plan for publishing Chimera’s Availability/Status to the network.

The integration MUST preserve Chimera’s governance guarantees:

* MCP-only external interaction
* Planner–Worker–Judge enforcement
* Human-in-the-loop by exception
* Observability and auditability

---

## 1. Scope

This specification defines:

* OpenClaw identity for a Chimera deployment
* Capability advertisement (high-level)
* Availability/Status publication: schemas, lifecycle, cadence, TTL, privacy, failure handling
* Inbound/outbound governance constraints (high-level)
* Minimal transport/security requirements (transport-agnostic)

This specification does NOT mandate a specific transport mechanism or vendor API. It defines contracts and behaviors that any transport implementation MUST satisfy.

---

## 2. OpenClaw Identity

Each Chimera deployment is represented as a single logical OpenClaw agent.

### 2.1 Agent Identifier

* **agent_id:** `chimera::<deployment_id>`
* The identifier MUST be stable across restarts.
* The identifier MUST NOT encode secrets or credentials.

### 2.2 Versioning

* Chimera SHOULD include a semantic version in descriptors.
* Schema changes MUST be versioned (e.g., `capability_v1`, `status_v1`, `status_v2`).

## 3. Capability Advertisement

Chimera publishes a Capability Descriptor describing categories of work it may accept.

### 3.1 Capability Descriptor Schema (capability_v1)

```json
{
  "agent_id": "chimera::<deployment_id>",
  "schema_version": "capability_v1",
  "agent_type": "governed_agent_system",
  "version": "1.0.0",
  "capabilities": [
    "trend_analysis",
    "content_generation",
    "content_evaluation"
  ],
  "governance": {
    "mcp_only_external_interaction": true,
    "planner_worker_judge": true,
    "human_in_the_loop_by_exception": true,
    "audit_logging": true
  }
}

```

### 3.2 Constraints

* Capability advertisement MUST NOT expose internal tool names, secret material, internal policies, system prompts, or environment values.
* Capabilities MUST be descriptive categories only and MUST NOT imply execution privileges.

## 4. Availability & Status Publication

Chimera publishes a Status Descriptor to communicate whether it can accept new inbound requests from OpenClaw peers.

* Status publication is advisory and does not grant execution privileges.
* All inbound requests remain subject to Chimera governance controls.
* A deployment MUST define where status is published (transport-agnostic `publish_target`), and that target MUST be configurable.

## 5. Status Descriptor Contract

### 5.1 Status Descriptor Schema (status_v1)

```json
{
  "agent_id": "chimera::<deployment_id>",
  "schema_version": "status_v1",
  "status": "available | busy | degraded | unavailable",
  "current_load": {
    "active_tasks_bucket": "0 | 1-10 | 11-50 | 51+",
    "queue_depth_bucket": "0 | 1-10 | 11-50 | 51+"
  },
  "last_updated": "ISO-8601",
  "ttl_seconds": 60,
  "accepting_requests": true,
  "status_seq": 1
}

```

### 5.2 Field Semantics

* **schema_version:** status schema identifier for compatibility.
* **status:** coarse availability signal for peers.
* **current_load.*_bucket:** bucketed load approximation to reduce leakage.
* **last_updated:** timestamp of last successful publish.
* **ttl_seconds:** peers SHOULD treat status as stale after this time.
* **accepting_requests:** primary gating signal for peers.
* **status_seq:** monotonically increasing sequence number for deduplication (optional but recommended).

### 5.3 Configurable Parameters (MUST)

For a production-grade deployment, the following parameters MUST be configurable:

* `heartbeat_interval_seconds` (default: 30)
* `ttl_seconds` (default: 60)
* `busy_active_tasks_threshold`
* `busy_queue_depth_threshold`
* `degraded_dependency_failure_threshold`
* `publish_timeout_seconds`
* `retry_max_attempts`
* `backoff_max_seconds`
* `publish_target` (where/how to publish status; transport-specific value)

## 6. Status Semantics

### 6.1 Status Definitions

* **available**
* Chimera can accept new external requests under normal governance rules.
* `accepting_requests` MUST be true.


* **busy**
* Chimera is healthy but at high load (exceeding configured thresholds).
* Chimera MAY rate-limit or defer non-critical inbound requests.
* `accepting_requests` MAY be true or false based on load gating rules.


* **degraded**
* Chimera is operating under partial failure (reduced capacity or dependency instability).
* Chimera SHOULD reject non-essential inbound requests.
* `accepting_requests` SHOULD be false.


* **unavailable**
* Chimera is offline, initializing, or in maintenance.
* Chimera MUST reject inbound requests.
* `accepting_requests` MUST be false.



### 6.2 accepting_requests Rules

* `accepting_requests=false` MUST mean Chimera will reject new inbound requests.
* `accepting_requests=true` MAY still allow internal rate limiting.
* Peers SHOULD respect `accepting_requests` as the primary gating signal.

## 7. Status Computation Rules

Status MUST be computed from two signal classes.

### 7.1 Health Signals (minimum required)

* **Planner health:** up/down + error rate
* **Worker pool health:** ability to consume tasks
* **Judge health:** ability to review and commit decisions
* **Queue health:** ability to read/write required queues
* **Persistence health:** ability to write core audit/task state

### 7.2 Load Signals (minimum required)

* Active tasks count
* Queue depth approximation
* Recent processing latency (optional, recommended)

### 7.3 Deterministic Precedence (MUST)

When computing status, Chimera MUST apply precedence:

1. If core services cannot operate → **unavailable**
2. If core services operate with partial failure → **degraded**
3. If load is above busy thresholds → **busy**
4. Otherwise → **available**

## 8. Publication Lifecycle

### 8.1 Publisher Responsibilities

A single logical component (“Status Publisher”) is responsible for:

* Computing status
* Sanitizing payload (privacy gate)
* Publishing to OpenClaw
* Writing audit entries for publish attempts

### 8.2 Triggers (MUST)

Status MUST be published under the following triggers:

* **Periodic Heartbeat:** publish at a fixed interval (default: 30s, configurable via `heartbeat_interval_seconds`).
* **Event-Driven Transitions:** publish immediately when status or `accepting_requests` changes.
* **Recovery Signal:** publish immediately when recovering from degraded or unavailable.

### 8.3 TTL / Staleness Handling

* `ttl_seconds` SHOULD be ≥ 2× the heartbeat interval.
* **Staleness rule:** if `(now - last_updated) > ttl_seconds` → peers SHOULD treat status as unavailable.

### 8.4 Non-Blocking Requirement (MUST)

* Status publishing MUST NOT block internal Planner–Worker–Judge execution. If publishing fails, Chimera continues internal operations.

### 8.5 Idempotency & Deduplication

* Status Publisher SHOULD include `status_seq` (monotonic) for deduplication.
* Receivers SHOULD treat updates as idempotent within a short time window.

## 9. Failure Handling & Retry Policy

### 9.1 Publish Failure (MUST)

If a status publish attempt fails:

* Chimera MUST record an audit event.
* Chimera MUST retry with backoff.
* Chimera MUST NOT block internal execution.

### 9.2 Backoff Policy (Recommended)

* **Immediate retry:** up to 2 quick retries.
* Then exponential backoff with max interval cap (`backoff_max_seconds`).
* Backoff MUST include jitter.
* Retry attempts MUST respect `retry_max_attempts`.

### 9.3 Degradation on Repeated Failure

If repeated publish failures occur beyond a configured threshold:

* Chimera SHOULD set local integration state to **degraded** for external acceptance purposes.
* Chimera MAY set `accepting_requests=false` until publish is restored.

## 10. Transport & Security Requirements (Transport-Agnostic)

Even though the transport is not mandated, any implementation MUST satisfy:

* **Authentication:** publishes MUST be attributable to the Chimera deployment (e.g., mTLS, signed messages, or authenticated broker).
* **Integrity:** receivers MUST be able to detect tampering (e.g., TLS + auth, or message signatures).
* **Replay resistance (Recommended):** receivers SHOULD use (`last_updated`, `status_seq`) to ignore stale/replayed updates.
* **Confidentiality (Recommended):** status channel SHOULD be encrypted in transit.
* **Least privilege:** credentials used for publishing MUST have publish-only permissions for the configured target.

## 11. Privacy Gate

### 11.1 Allowed Fields

* `agent_id`
* `schema_version`
* `status`
* `last_updated`
* `ttl_seconds`
* bucketed load approximations
* `status_seq`

### 11.2 Forbidden Fields (MUST NOT be published)

* Internal identifiers (campaign IDs, task IDs)
* Content, persona, or user data
* Internal errors or stack traces
* Secrets, API keys, or environment values
* Internal policy details or tool names

### 11.3 Privacy Gate Failure (MUST)

If privacy gate validation fails, Chimera MUST:

* Abort publication.
* Write a high-severity audit event.
* Keep internal operations running (non-blocking).

## 12. Audit & Observability

### 12.1 Audit Events (MUST)

Every status publish attempt MUST generate an audit record containing:

* timestamp
* `agent_id`
* publish outcome (success/failure)
* status category published
* staleness (time since last successful publish)
* sanitized load buckets (optional)

Audit records MUST NOT include secrets or content data.

### 12.2 Key Metrics (Recommended)

* `publish_success_rate`
* `publish_latency_ms`
* `status_staleness_seconds`
* `status_transition_count`
* `inbound_requests_rejected_due_to_status` (if tracked)

## 13. Inbound Requests

### 13.1 Minimal Inbound Request Envelope (Recommended)

OpenClaw peers SHOULD send a request envelope like:

```json
{
  "to_agent_id": "chimera::<deployment_id>",
  "from_agent_id": "peer::<id>",
  "schema_version": "request_v1",
  "request_id": "uuid",
  "requested_capability": "trend_analysis",
  "payload": {},
  "sent_at": "ISO-8601"
}

```

### 13.2 Enforcement Rules (MUST)

* Requests MUST be validated against advertised capabilities and expected schemas.
* Requests MUST NEVER bypass Judge review or human escalation rules.
* If status is **unavailable**, inbound requests MUST be rejected.
* If status is **degraded**, inbound requests SHOULD be rejected except for explicitly allowlisted categories (deployment-configured).
* Rejections SHOULD be explicit (reason codes), not silent drops.

### 13.3 Minimal Rejection Response (Recommended)

```json
{
  "schema_version": "response_v1",
  "request_id": "uuid",
  "accepted": false,
  "reason": "unavailable | degraded | capability_not_supported | invalid_schema | rate_limited"
}

```

## 14. Outbound Collaboration (Optional)

Chimera MAY invoke external agents discovered via OpenClaw, but:

* External agents are untrusted.
* Requests MUST be narrowly scoped and least-privilege.
* Responses MUST be reviewed by the Judge Agent.
* External agents MUST NOT directly mutate Chimera state.

## 15. Publish Payload Examples

### 15.1 Example: Available

```json
{
  "agent_id": "chimera::prod-us-east-1",
  "schema_version": "status_v1",
  "status": "available",
  "current_load": {
    "active_tasks_bucket": "1-10",
    "queue_depth_bucket": "1-10"
  },
  "last_updated": "2026-02-05T20:30:00Z",
  "ttl_seconds": 60,
  "accepting_requests": true,
  "status_seq": 42
}

```

### 15.2 Example: Degraded

```json
{
  "agent_id": "chimera::prod-us-east-1",
  "schema_version": "status_v1",
  "status": "degraded",
  "current_load": {
    "active_tasks_bucket": "0",
    "queue_depth_bucket": "0"
  },
  "last_updated": "2026-02-05T20:35:00Z",
  "ttl_seconds": 60,
  "accepting_requests": false,
  "status_seq": 43
}

```

## 16. Out of Scope

* Cross-agent financial authority
* Shared memory or embeddings
* Trust-based execution shortcuts
* Direct execution delegation to external agents