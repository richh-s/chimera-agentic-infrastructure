# Skill: Cost Guard

## Skill ID
`skill_cost_guard`

## Version
`1.1.0`

---

## Purpose

The **Cost Guard** enforces Chimera's **economic governance** by preventing
unbounded or irresponsible spending during autonomous execution.

It ensures agents remain **financially aligned** with campaign budgets,
daily limits, and risk tolerance.

---

## Responsibility Boundary

### This skill DOES:
- Evaluate projected and cumulative costs
- Enforce budget thresholds at multiple time scales
- Surface cost risks and overrun patterns
- Recommend optimization strategies
- Escalate budget violations to the Judge
- Generate cost efficiency metrics

### This skill DOES NOT:
- Execute or cancel tasks directly
- Modify budgets or spending limits
- Call external billing or payment systems
- Override Judge or Human decisions
- Access financial account information

---

## Cost Decision Semantics

| Decision | Confidence Threshold | Meaning                        | Default Action                      |
|----------|----------------------|--------------------------------|-------------------------------------|
| `allow`  | ≥ 0.8                | Cost within safe bounds        | Proceed with execution              |
| `warn`   | 0.6–0.79             | Approaching budget limits      | Proceed with warning alerts         |
| `block`  | < 0.6                | Budget exceeded or unsafe      | Halt & escalate to Judge            |

⚠️ **All decisions are advisory.**  
The Judge and Human Governor retain final authority over budget exceptions.

---

## Budget Threshold Framework

| Threshold Type        | Default Value       | Trigger Condition                        | Required Action                          |
|-----------------------|---------------------|------------------------------------------|------------------------------------------|
| **Warning Threshold** | 75% of budget       | Projected spend reaches threshold        | Emit warning, continue monitoring        |
| **Block Threshold**   | 90% of budget       | Actual spend reaches threshold           | Block new tasks, allow in-progress       |
| **Hard Stop**         | 100% of budget      | Budget fully exhausted                   | Immediate halt, escalate to HITL         |
| **Daily Burst Limit** | 50% of daily budget | Hourly spend exceeds limit               | Throttle execution, defer tasks          |
| **Task Cost Ceiling** | $10.00 per task     | Single task cost exceeds limit           | Block task, suggest alternatives         |

**Thresholds are adjustable** based on `risk_tolerance` input:
- `low`: More conservative (60% warning, 75% block)
- `medium`: Default values (75% warning, 90% block)
- `high`: More permissive (85% warning, 95% block)

---

## Evaluation Pipeline

### 1. Cost Aggregation & Estimation
- **Task Cost Calculation**: Compute based on skill chain complexity
- **Projection Analysis**: Forecast total spend including pending tasks
- **Budget Remaining**: Calculate available budget across all time scales
- **Efficiency Scoring**: Rate cost-effectiveness of proposed execution

### 2. Threshold & Pattern Analysis
- **Multi-scale Budget Checking**: Campaign, daily, hourly limits
- **Risk Tolerance Application**: Adjust thresholds based on input
- **Runaway Spend Detection**: Identify accelerating cost patterns
- **Priority Weighting**: Allow higher costs for critical tasks

### 3. Decision Generation & Optimization
- **Decision Recommendation**: Allow/Warn/Block based on analysis
- **Alert Generation**: Create actionable cost warnings
- **Optimization Suggestions**: Recommend cost-saving alternatives
- **Audit Trail Creation**: Record decision rationale and metadata

---

## Optimization Recommendation Categories

| Category       | Example Recommendations                        | Expected Savings   |
|----------------|------------------------------------------------|--------------------|
| **Skill-Level**   | Use `fast` instead of `accurate` mode          | 40–60%            |
| **Temporal**      | Defer to next budget window                    | 100% (deferred)   |
| **Architectural** | Cache results, reduce redundancy               | 20–30%            |
| **Scope**         | Reduce analysis depth or breadth               | 25–50%            |
| **Alternative**   | Use different skill combination                | 15–35%            |

### Example Recommendations:
- **Reduce analysis depth** from `deep` to `standard`
- **Switch to lower-cost model tier** for non-critical tasks
- **Defer non-urgent work** to next budget period
- **Cache or reuse prior results** from similar tasks
- **Split large workloads** across multiple budget windows
- **Use approximate methods** where high precision isn't required

---

## Cost Forecasting & Analytics

### Projection Metrics:
- **Time to Budget Exhaustion**: Estimated hours/days until budget depleted
- **Daily Spend Rate**: Current spending velocity
- **Cost Efficiency Score**: (0.0–1.0) How efficiently budget is being used
- **Burn Rate Alerting**: Notify when spending accelerates unexpectedly

### Anomaly Detection:
- **Unusually High Task Costs**: Flag tasks exceeding historical averages
- **Budget Acceleration**: Detect when daily spend rate increases >50%
- **Inefficient Skill Chains**: Identify suboptimal skill combinations
- **Redundant Processing**: Detect duplicate or overlapping work

---

## Failure Modes & Recovery

| Error Code              | Description                              | Automatic Behavior              | Recovery Strategy             |
|-------------------------|------------------------------------------|----------------------------------|-------------------------------|
| `MISSING_BUDGET_CONTEXT` | No budget data provided                 | Block execution                 | Require budget context        |
| `INVALID_COST_ESTIMATE`  | Cost estimate malformed or unrealistic  | Block execution                 | Request validated estimate    |
| `CALCULATION_ERROR`      | Internal computation failure            | Escalate to Judge               | System restart needed         |
| `TIMEOUT`                | Evaluation exceeds 15 seconds           | Block for safety                | Use cached decision if available |
| `BUDGET_CORRUPTION`      | Inconsistent budget data detected       | Block & escalate immediately    | Human audit required          |

**Fail-closed by default** — any uncertainty results in blocking to prevent unbounded spend.

---

## Integration Flow

```mermaid
flowchart LR
    A[Planner<br/>creates task] --> B[Cost Guard<br/>evaluates cost]
    B --> C{Cost Decision}
    C -->|Allow ≥0.8| D[Worker<br/>executes task]
    C -->|Warn 0.6-0.79| E[Worker executes<br/>with warnings]
    C -->|Block <0.6| F[Judge Review<br/>budget exception]
    E --> G[Monitor cost alerts]
    F -->|Override Approved| D
    F -->|Budget Exception Denied| H[Task Cancelled]
    
    style B fill:#fff3e0
    style C fill:#e8f5e8
    style F fill:#ffebee
    style H fill:#fce4ec
Cost & Performance

No external billing calls — All calculations internal
Deterministic runtime — Predictable performance under load
Average latency: < 50ms per evaluation
Throughput: 30 evaluations per minute
Stateless operation — No persistent budget state
Cache-friendly — Results cacheable by input hash (5-minute TTL)

Resource Requirements:

Memory: 128MB RAM
CPU: 1 core
Storage: 50MB for pricing model cache
Network: None required (fully self-contained)

Compliance & Auditability
Audit Requirements:

All decisions logged with full input/output context
Budget evaluations auditable for 90+ days
Pricing model versioned and change-tracked
Threshold adjustments documented and justified

Financial Controls:

No external billing system access — prevents accidental charges
Budget integrity checks — detect tampering or corruption
Cost data encryption — protect financial information
Retroactive cost analysis — support post-mortem reviews

Governance:

Regular pricing model reviews — ensure accuracy
Budget exception reporting — track all overrides
Cost efficiency reporting — identify optimization opportunities
Compliance attestations — regular financial governance checks

Integration Examples
Basic Cost Evaluation:
JSON{
  "skill": "skill_cost_guard",
  "inputs": {
    "task_context": {
      "task_id": "task_video_analysis_20240315_001",
      "campaign_id": "campaign_q2_social_2024",
      "skill_chain": [
        "skill_media_harvester",
        "skill_vocal_analyzer", 
        "skill_content_analyzer"
      ],
      "priority": "normal"
    },
    "cost_estimate": {
      "compute_units": 12.5,
      "api_calls": 3,
      "estimated_usd": 1.75,
      "cost_breakdown": {
        "compute_cost": 1.25,
        "api_cost": 0.30,
        "storage_cost": 0.20
      }
    },
    "budget_context": {
      "campaign_budget_usd": 50.0,
      "spent_to_date_usd": 38.0,
      "daily_budget_usd": 10.0,
      "daily_spent_usd": 4.5,
      "hard_stop": true,
      "budget_period": "campaign"
    },
    "risk_tolerance": "medium"
  }
}
With Budget Warning:
JSON{
  "skill": "skill_cost_guard",
  "inputs": {
    "task_context": { ... },
    "cost_estimate": { "estimated_usd": 8.0, ... },
    "budget_context": {
      "campaign_budget_usd": 50.0,
      "spent_to_date_usd": 42.0,  // 84% spent - warning threshold
      "daily_budget_usd": 10.0,
      "daily_spent_usd": 9.8,     // 98% daily - near block
      "hard_stop": true
    }
  }
}
// Returns: {"cost_decision": "warn", "alerts": [...]}
Priority-Based Exception:
JSON{
  "skill": "skill_cost_guard",
  "inputs": {
    "task_context": {
      "task_id": "urgent_crisis_response",
      "priority": "critical",  // High priority allows budget exception
      ...
    },
    "cost_estimate": { "estimated_usd": 15.0, ... },
    "budget_context": {
      "campaign_budget_usd": 100.0,
      "spent_to_date_usd": 95.0,  // Normally would block
      "hard_stop": false  // Allow override for critical tasks
    }
  }
}
// May return "warn" instead of "block" for critical priority
Summary
The Cost Guard prevents Chimera from becoming economically reckless.
It ensures autonomy remains:

Bounded — within defined financial constraints
Predictable — with clear cost projections and alerts
Financially Responsible — optimizing spend without compromising outcomes

No surprises. No runaway spend. No silent failures.
The guardian of your budget, ensuring every dollar spent delivers maximum value.