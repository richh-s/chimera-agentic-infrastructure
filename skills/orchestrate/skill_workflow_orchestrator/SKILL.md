# Skill: Workflow Orchestrator

## Skill ID
`skill_workflow_orchestrator`

## Version
`3.0.0`

---

## Purpose

The **Workflow Orchestrator** is Chimera's **central nervous system for complex task execution**. It coordinates, sequences, and supervises multi-skill workflows under strict governance constraints, enabling sophisticated pipelines while maintaining auditable control and human oversight.

This skill transforms declarative workflow definitions into **managed, observable, and compliant execution** — orchestrating without autonomy, coordinating without control.

---

## Core Principle

> **Coordination without command.**  
The orchestrator manages *how* skills execute, not *what* they decide. It provides sequence, not substance; coordination, not content.

---

## Responsibility Boundary

### This Skill DOES:
- **Parse & Validate** workflow definitions against schema and policies
- **Schedule & Sequence** skill execution based on dependencies
- **Manage State** across distributed skill invocations
- **Handle Errors** with configurable retry and escalation policies
- **Track Resources** including time, cost, and compute allocation
- **Enforce Governance** through confidence thresholds and approval gates
- **Provide Observability** with comprehensive metrics and audit trails
- **Support Recovery** through checkpoints and state persistence
- **Coordinate Parallelism** with controlled concurrency limits
- **Generate Execution Plans** for validation and estimation

### This Skill DOES NOT:
- **Execute Business Logic** (delegates to individual skills)
- **Make Content Decisions** (follows predefined workflow logic)
- **Bypass Governance** (enforces all policies and thresholds)
- **Mutate Persistent Storage** (manages state, not storage)
- **Access External Systems** (except through authorized skills)
- **Override Human Decisions** (escalates when uncertain)
- **Learn Autonomous Behaviors** (follows explicit definitions)
- **Trigger Unauthorized Actions** (requires valid initiator)

---

## Workflow Definition Architecture

### **Workflow Types**
| Type | Pattern | Use Case | Max Concurrency |
|------|---------|----------|----------------|
| **Linear** | Sequential steps | Simple pipelines | 1 step at a time |
| **Parallel** | Independent branches | Batch processing | Configurable (default: 3) |
| **Conditional** | Branching logic | Decision-based flows | Dynamic based on conditions |
| **Looping** | Iterative execution | Retry/optimization loops | Limited iterations |
| **Hybrid** | Mixed patterns | Complex business logic | Optimized per segment |

### **Step Definition Components**

```yaml
step_download_video:
  step_id: "step_download_video"
  step_name: "Download Source Video"
  skill: "skill_media_harvester"
  skill_version_constraint: "^2.0.0"
  inputs:
    url: "https://youtube.com/watch?v=example"
    media_type: "video"
    quality: "high"
  input_templates:
    audio_path: "{{step_download_video.output.local_path}}"
  depends_on: []
  timeout_seconds: 180
  retry_policy:
    max_retries: 3
    retry_on: ["timeout", "execution_error"]
    backoff_strategy: "exponential"
    backoff_base_seconds: 2
  failure_behavior: "escalate"
  resource_requirements:
    memory_mb: 512
    cpu_cores: 1
    network_access: true
  confidence_threshold: 0.7
  approval_required: false
Template Resolution System
The orchestrator supports dynamic input resolution using mustache-style templates:

json
{
  "audio_path": "{{step_download_video.output.local_path}}",
  "analysis_type": "{{step_config.output.preferred_analysis}}",
  "platform": "{{workflow_context.target_platform}}"
}
Resolution Order:

Previous step outputs (by step_id.output.field)

Workflow context variables

Static input values

Default values from skill contracts

Execution Modes
1. Execute Mode (Default)
Purpose: Full workflow execution

Behavior: Invokes all skills, manages state, produces outputs

Use Case: Production task execution

Outputs: Complete results with metadata

2. Validate Only Mode
Purpose: Definition validation without execution

Behavior: Validates schema, dependencies, skill availability

Use Case: CI/CD pipeline testing

Outputs: Validation report with warnings

3. Dry Run Mode
Purpose: Simulation with cost/time estimation

Behavior: Simulates execution without skill invocation

Use Case: Planning and budgeting

Outputs: Execution plan with estimates

4. Estimate Only Mode
Purpose: Quick resource estimation

Behavior: Analyzes requirements without deep validation

Use Case: Quick feasibility checks

Outputs: High-level cost/time estimates

State Management & Recovery
Checkpoint System
yaml
checkpoints:
  enabled: true
  interval_steps: 5
  max_checkpoints: 10
  retention_days: 7
  encryption: true
Checkpoint Contents:

Completed step IDs and outputs

Accumulated cost and time

Pending step dependencies

Workflow execution context

State hash for integrity verification

Recovery Scenarios
Scenario	Detection	Recovery Strategy	Data Loss Risk
Skill Timeout	Execution timeout	Retry with backoff	None (idempotent)
System Failure	Process termination	Resume from last checkpoint	Since last checkpoint
Resource Exhaustion	Memory/CPU limits	Degrade and continue	Current step output
Network Partition	Skill unavailable	Pause and retry later	None
Policy Violation	Confidence threshold	Escalate for approval	None (blocked)
Error Handling & Escalation Matrix
Error Classification
Severity	Error Types	Auto-Retry	Escalation Path	Timeout
Transient	Timeout, rate limit	✅ Yes (3x)	None	5 minutes
Recoverable	Skill error, validation	✅ Conditional	Judge	15 minutes
Systemic	Resource exhaustion	❌ No	HITL + Operations	Immediate
Critical	Policy violation, security	❌ No	Security + Governance	Immediate
Escalation Workflows
text
Low Severity → Judge Review (24h SLA)
Medium Severity → Judge → HITL (12h SLA)
High Severity → Judge → HITL → Governance (4h SLA)
Critical Severity → Security → Operations → Executive (1h SLA)
Failure Propagation Rules
Fail-Fast: Critical errors stop entire workflow

Continue-on-Error: Non-critical errors allow continuation

Conditional Continuation: Continue based on step importance

Pause-and-Escalate: Stop execution, await human decision

Resource Governance
Cost Management
yaml
cost_governance:
  budget_usd: 50.0
  warning_threshold_percent: 80
  stop_threshold_percent: 95
  cost_tracking_granularity: "per_step"
  cost_breakdown:
    - compute
    - external_apis
    - storage
    - network
Time Budgeting
Total Time Budget: Configurable per workflow (1s - 24h)

Step Timeouts: Individual step limits (1s - 1h)

Critical Path Analysis: Identifies time-sensitive steps

Overrun Prevention: Automatic escalation at thresholds

Compute Resource Allocation
yaml
resource_pools:
  default:
    memory_mb: 1024
    cpu_cores: 2
    concurrent_steps: 3
  high_performance:
    memory_mb: 4096
    cpu_cores: 4
    concurrent_steps: 10
    gpu_required: true
Confidence & Quality Gates
Confidence Thresholds
Threshold	Value	Action	Required Approval
Auto-Success	≥ 0.85	Proceed immediately	None
Acceptable	0.70 - 0.84	Proceed with logging	Judge notification
Review Required	0.60 - 0.69	Pause for review	Judge approval
Escalation	0.40 - 0.59	Escalate for decision	HITL review
Rejection	< 0.40	Reject step	Governance review
Quality Metrics
Step Success Rate: Target > 95%

Average Confidence: Target > 0.80

Retry Rate: Target < 20%

Escalation Rate: Target < 10%

Cost Efficiency: Actual vs. estimated cost ratio

Time Efficiency: Actual vs. estimated time ratio

Performance SLAs
Metric	Target	Warning	Critical
Execution Time	P95 < 300s	> 400s	> 600s
Success Rate	> 95%	90-95%	< 90%
Cost Accuracy	±10%	±20%	±30%
Escalation Response	< 60m	60-120m	> 120m
Security & Compliance
Authentication & Authorization
JWT-based Authentication: Required for all executions

Role-Based Access Control:

planner: Can initiate workflows

judge: Can approve/review steps

hitl: Can override decisions

governance: Can modify policies

auditor: Read-only access to all data

Tenant Isolation: Multi-tenant data separation

Execution Context Validation: Verifies initiator permissions

Data Protection
Encryption: AES-256 for data at rest and in transit

PII Handling: Automatic detection and redaction

Secrets Management: Never stored in workflow state

Audit Trail: Immutable logs of all decisions

Data Minimization: Only necessary data persisted

Compliance Features
GDPR Compliance: Right to erasure support

Audit Requirements: 180-day retention minimum

Access Logging: All operations logged

Change Tracking: Versioned workflow definitions

Integrity Checks: SHA-256 hashing for state validation

Monitoring & Observability
Key Metrics
prometheus
# Throughput
workflow_executions_total{status="completed"}
workflow_steps_executed_total

# Performance
workflow_execution_duration_seconds
step_execution_duration_seconds_bucket

# Quality
workflow_success_rate
step_confidence_score

# Resource Usage
workflow_cost_usd
resource_utilization_percent

# Errors
workflow_failures_total
step_retries_total
escalations_total
Alerting Rules
Alert	Condition	Severity	Action
High Failure Rate	Success rate < 90% for 15m	Critical	Page on-call
Cost Overrun	Actual cost > 120% estimate	High	Notify budget owner
Time Overrun	Execution time > 200% estimate	Medium	Investigate bottlenecks
High Escalation Rate	> 30% steps escalated	High	Review governance
Resource Exhaustion	Memory > 90% for 5m	Critical	Scale or throttle
Dashboard Components
Execution Overview: Throughput, success rate, average duration

Cost Analysis: Per-workflow and per-step cost breakdown

Quality Metrics: Confidence scores, escalation rates

Resource Utilization: CPU, memory, concurrent executions

Error Analysis: Failure patterns, retry statistics

SLA Compliance: Performance against targets

Integration Patterns
Content Pipeline Example
flowchart TD
    A[Planner<br/>Creates Task] --> B{Complex Task?}
    B -->|Yes| C[Workflow Orchestrator<br/>Coordinates Pipeline]
    B -->|No| D[Single Skill<br/>Direct Execution]
    
    C --> E[Step 1: Media Harvest<br/>Download source content]
    E --> F[Step 2: Vocal Analysis<br/>Transcribe audio]
    F --> G[Step 3: Content Analysis<br/>Extract topics/themes]
    G --> H[Step 4: Safety Validation<br/>Check compliance]
    H --> I{Confidence ≥ 0.8?}
    I -->|Yes| J[Step 5: Persona Publishing<br/>Format for platform]
    I -->|No| K[Judge Review<br/>Manual assessment]
    J --> L[Final Output<br/>Ready for publishing]
    K -->|Approved| J
    K -->|Rejected| M[Workflow Failed<br/>Escalate to HITL]
    
    style C fill:#e3f2fd
    style H fill:#fff3e0
    style I fill:#e8f5e8
    style K fill:#fce4ec
    style M fill:#ffebee
Batch Processing Pattern
json
{
  "workflow_type": "parallel",
  "max_concurrent_steps": 10,
  "steps": [
    {
      "step_id": "process_item_1",
      "skill": "skill_content_analyzer",
      "inputs": {"text": "Content 1..."},
      "depends_on": []
    },
    {
      "step_id": "process_item_2",
      "skill": "skill_content_analyzer", 
      "inputs": {"text": "Content 2..."},
      "depends_on": []
    }
    // ... up to 10 parallel items
  ]
}
Conditional Execution Pattern
yaml
steps:
  - step_id: "analyze_content"
    skill: "skill_content_analyzer"
    # ... analysis step
  
  - step_id: "check_safety"
    skill: "skill_safety_validator"
    depends_on: ["analyze_content"]
    condition:
      type: "if"
      expression: "{{analyze_content.output.sentiment.overall}} == 'negative'"
    # Only executes if content is negative sentiment
  
  - step_id: "publish_content"
    skill: "skill_persona_publisher"
    depends_on: ["analyze_content", "check_safety"]
    condition:
      type: "unless"
      expression: "{{check_safety.output.is_approved}} == false"
    # Skips if safety check failed
Failure Scenarios & Mitigations
Scenario 1: Skill Unavailability
Symptoms: Skill timeout or "service unavailable" errors
Detection: Connection failures or timeouts
Mitigation:

Retry with exponential backoff (up to 3 attempts)

If unavailable, escalate to Judge for alternative path

Update skill registry health status

Route future workflows to healthy instances

Scenario 2: Cost Overrun
Symptoms: Accumulated cost exceeds budget threshold
Detection: Real-time cost tracking
Mitigation:

Pause workflow at next checkpoint

Notify budget owner and Judge

Offer options: continue with override, reduce scope, or cancel

Log decision for audit trail

Scenario 3: Infinite Loop
Symptoms: Step retries exceeding maximum, circular dependencies
Detection: Cycle detection in dependency graph
Mitigation:

Detect and break cycles in validation phase

Enforce maximum retry limits per step

Implement timeout for entire workflow

Escalate to operations for manual intervention

Scenario 4: Data Corruption
Symptoms: State hash mismatch, invalid step outputs
Detection: Integrity checks at checkpoint load
Mitigation:

Reject corrupted state, revert to previous checkpoint

Escalate to security team if malicious pattern detected

Isolate affected workflow instance

Conduct forensic analysis on audit trail

Operational Guidelines
Capacity Planning
Metric	Development	Staging	Production
Concurrent Workflows	1	3	10
Steps per Workflow	10	50	100
State Size Limit	10 MB	50 MB	100 MB
Retention Period	7 days	30 days	180 days
Cost Budget	$10	$100	$1000
Deployment Checklist
Skill registry populated with required versions

Memory policy configured and validated

Authentication tokens issued to authorized components

Monitoring and alerting configured

Backup and recovery procedures documented

SLA targets agreed with stakeholders

Cost tracking integrated with billing system

Audit trail destination configured

Escalation contacts registered

Runbook for common failures created

Maintenance Schedule
Daily: Review escalation queue, check system health

Weekly: Analyze performance metrics, optimize slow steps

Monthly: Review cost efficiency, update skill versions

Quarterly: Security audit, policy review, capacity planning

Annually: Comprehensive review, architecture assessment

Summary
The Workflow Orchestrator is Chimera's execution engine — transforming complex intentions into managed, observable, and governed skill executions.

Key Architectural Principles:
Declarative over Imperative: Workflows define what not how

Managed over Autonomous: Every execution is supervised and auditable

Resilient over Fragile: Built-in recovery and state persistence

Observable over Opaque: Complete visibility into execution details

Governed over Unchecked: Policy enforcement at every step

The Orchestrator Ensures:
✅ Sequence without ambiguity — Clear dependency resolution

✅ Progress without risk — Checkpoints and recovery paths

✅ Scale without chaos — Controlled parallelism

✅ Complexity without confusion — Comprehensive observability

✅ Efficiency without compromise — Resource and cost governance

This skill embodies Chimera's core promise: sophisticated capability with accountable control. It enables complex multi-skill workflows while maintaining the governance boundaries that make autonomous systems safe, auditable, and aligned with human values.