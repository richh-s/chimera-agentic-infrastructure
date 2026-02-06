# Skill: Engagement Evaluator

## Skill ID
`skill_engagement_evaluator`

## Version
`2.0.0`

---

## Purpose

The **Engagement Evaluator** measures how well persona-published content is
likely to perform — or has performed — in terms of **attention, interaction,
amplification, retention, conversion, and emotional resonance**.

It provides **learning signals, not control decisions**, closing Chimera's
learning loop while maintaining strict governance boundaries.

---

## Responsibility Boundary

### This Skill DOES:
- **Predict** engagement potential prior to publishing
- **Analyze** observed engagement post-publish with statistical rigor
- **Compare** performance against multi-dimensional baselines
- **Generate** evidence-backed insights and prioritized recommendations
- **Provide** confidence-scored evaluation with uncertainty metrics
- **Support** A/B testing analysis and iterative improvement
- **Feed** learning data back to model improvement systems

### This Skill DOES NOT:
- Modify content or publishing decisions directly
- Trigger re-publication or automatic retries
- Change persona definitions or platform rules
- Optimize spend, timing, or distribution automatically
- Access external analytics or scrape platform data
- Store personal data or inference results

---

## Evaluation Modes

### 1. **Predictive Mode** (Pre-Publish)
Used **before scheduling** to estimate engagement potential based on:
- Content structure, hooks, and clarity
- Persona alignment and voice consistency
- Platform-specific norms and constraints
- Temporal context and audience patterns
- Competitive landscape and novelty factors

**Output**: Confidence-scored predictions with risk assessment

### 2. **Observed Mode** (Post-Publish)
Used **after publishing** to evaluate actual performance:
- Multi-dimensional engagement metrics analysis
- Relative performance vs. historical/persona/platform baselines
- Statistical significance of observed outcomes
- Unexpected drop-offs, spikes, or anomalies
- Prediction accuracy assessment for model improvement

**Output**: Performance analysis with learning feedback

### 3. **Comparative Mode** (A/B Testing)
Used for **experimentation analysis**:
- Variant performance comparison
- Statistical significance testing
- Minimum detectable effect analysis
- Learning extraction from controlled experiments

**Output**: Test results with actionable insights

---

## Engagement Dimensions

| Dimension | Description | Key Metrics | Optimization Target |
|-----------|-------------|-------------|---------------------|
| **Attention** | Ability to stop scrolling and attract views | Impressions, Reach, Hook Effectiveness | Capture initial interest |
| **Interaction** | Direct user engagement and participation | Likes, Comments, Replies, Questions | Foster two-way communication |
| **Amplification** | Content sharing and virality potential | Shares, Retweets, Reposts, Saves | Encourage distribution |
| **Retention** | Sustained engagement over time | Watch Time, Dwell Time, Completion Rate | Maintain interest |
| **Conversion** | Desired action completion | Clicks, Follows, Saves, Profile Visits | Drive specific outcomes |
| **Emotional Resonance** | Emotional impact and memorability | Sentiment Analysis, Emotional Triggers | Create memorable experiences |

All scores are **normalized (0.0–1.0)** for cross-platform comparison and include **confidence intervals**.

---

## Confidence Framework

### Score Interpretation
| Confidence Range | Meaning | Usage Guidance | Judge Action |
|-----------------|---------|----------------|--------------|
| **≥ 0.8** | High confidence | Safe for planning and optimization | Accept for automated use |
| **0.7–0.79** | Good confidence | Use with minor caution | Review if critical decision |
| **0.6–0.69** | Moderate confidence | Manual review recommended | Always review before action |
| **< 0.6** | Low confidence | Escalate or disregard | Escalate to HITL |

### Confidence Components:
- **Model Confidence**: Prediction algorithm certainty
- **Data Quality**: Completeness and freshness of input data
- **Statistical Significance**: Reliability of comparisons
- **Platform Specificity**: Relevance to target platform
- **Temporal Relevance**: Timing context appropriateness

**Low-confidence evaluations MUST be flagged to the Judge** if used in any downstream decisions.

---

## Integration Flow

```mermaid
flowchart TD
    A[Persona Publisher<br/>Creates Content] --> B{Evaluation Mode?}
    
    B -->|Predictive| C[Engagement Evaluator<br/>Predict Performance]
    C --> D[Insights & Predictions]
    D --> E[Planner Feedback Loop<br/>Optimize Future Content]
    
    B -->|Observed| F[Engagement Evaluator<br/>Analyze Performance]
    F --> G[Performance Analysis<br/>+ Learning Data]
    G --> H[Model Improvement<br/>Continuous Learning]
    
    B -->|Comparative| I[Engagement Evaluator<br/>A/B Test Analysis]
    I --> J[Test Results<br/>Statistical Significance]
    J --> K[Content Strategy<br/>Data-Driven Decisions]
    
    D --> L[Analytics Dashboard<br/>Performance Reporting]
    G --> L
    J --> L
    
    style A fill:#e3f2fd
    style C fill:#e8f5e8
    style F fill:#fff3e0
    style I fill:#f3e5f5
    style L fill:#f5f5f5
Example Use Cases
Predictive Evaluation (Pre-Publish)
json
{
  "skill": "skill_engagement_evaluator",
  "inputs": {
    "content": "AI governance must balance innovation with accountability. Three frameworks leading the way...",
    "platform": "LinkedIn",
    "evaluation_mode": "predictive",
    "persona_context": {
      "persona_id": "persona_tech_thought_leader",
      "persona_version": "2.1.0"
    },
    "temporal_context": {
      "day_of_week": "wednesday",
      "hour_of_day": 10
    }
  }
}
Observed Performance Review (Post-Publish)
json
{
  "skill": "skill_engagement_evaluator",
  "inputs": {
    "content": "Exploring three principles of responsible AI deployment.",
    "platform": "X",
    "evaluation_mode": "observed",
    "observed_metrics": {
      "impressions": 12500,
      "reach": 8400,
      "likes": 540,
      "comments": 87,
      "shares": 42,
      "clicks": 310,
      "collection_duration_hours": 48,
      "metrics_timestamp": "2024-01-15T14:30:00Z"
    },
    "historical_baseline": {
      "avg_engagement_rate": 0.042,
      "sample_size": 45,
      "time_period": "30d"
    }
  }
}
A/B Test Analysis
json
{
  "skill": "skill_engagement_evaluator",
  "inputs": {
    "content": "New AI safety guidelines released today...",
    "platform": "LinkedIn",
    "evaluation_mode": "comparative",
    "testing_context": {
      "test_id": "test_headline_variants_0124",
      "variant_id": "variant_b",
      "control_metrics": {
        "engagement_score": 0.72,
        "sample_size": 1500
      },
      "test_objective": "engagement",
      "minimum_detectable_effect": 0.1
    }
  }
}
Failure Modes & Recovery
Error Category	Error Codes	Automatic Recovery	Escalation Required	Impact Level
Missing Metrics	METRICS_INCOMPLETE	✅ Degrade to predictive	⚠️ If confidence < 0.6	Medium
Baseline Unavailable	BASELINE_MISSING	✅ Skip comparison	❌ No	Low
Execution Timeout	EXECUTION_TIMEOUT	✅ Return partial results	✅ Yes	High
Data Inconsistency	DATA_INCONSISTENT	❌ No	✅ Immediate	Critical
Model Failure	MODEL_UNAVAILABLE	✅ Fallback to rule-based	✅ Yes	High
Platform Unsupported	PLATFORM_UNSUPPORTED	✅ Generic evaluation	⚠️ Flag for review	Medium
Graceful Degradation Levels:
Full Analysis: Complete evaluation with all features

Essential Analysis: Core scores without baselines/comparisons

Minimal Analysis: Basic engagement score only

Failure: Escalate to Judge with diagnostic information

Quality Gates & Validation
Input Validation:
✅ Content length within bounds (10-10,000 chars)

✅ Supported platform and evaluation mode

✅ Required metrics present for observed mode

✅ Temporal context validity

✅ Persona schema compliance

Output Validation:
✅ Confidence score ≥ 0.6 (or flagged)

✅ All required output fields populated

✅ Score ranges valid (0.0-1.0)

✅ Timestamps in ISO 8601 format

✅ Unique evaluation ID generated

Performance Targets:
P95 Processing Time: < 10 seconds

Cache Hit Ratio: > 60%

Prediction Accuracy: > 75% (observed mode validation)

Uptime: 99.5%

Governance & Safety
Data Privacy:
No personal data inference or storage

No external API calls or scraping

All evaluations logged with full audit trail

Data retention: 90 days (results), 365 days (learning data)

Security Controls:
Input validation and sanitization

Output sanitization before return

Rate limiting (30 requests/minute)

Encryption at rest and in transit

Access logging and monitoring

Compliance:
GDPR-compliant data handling

No PII storage or processing

Audit trail completeness

Change tracking for models and rules

Learning Loop Governance:
Model improvements require governance approval

A/B test results reviewed before strategy changes

Prediction accuracy monitored continuously

Confidence calibration checked regularly

Cost & Resource Considerations
Resource Allocation:
Memory: 512 MB maximum

CPU: 2 cores allocated

Storage: 100 MB temporary

Network: No external calls allowed

Optimization Strategies:
Caching: Identical evaluations cached (24h TTL)

Batch Processing: Multiple evaluations in single workflow

Progressive Enhancement: Start basic, enhance if confidence low

Model Selection: Choose appropriate model based on complexity

Cost Monitoring:
Execution time tracking

Cache efficiency metrics

Model inference costs

Resource utilization alerts

Integration Patterns
With Content Creation Pipeline:
text
Persona Publisher → Engagement Evaluator (predictive) → Scheduler → Publisher
With Learning Loop:
text
Publisher → Engagement Evaluator (observed) → Model Improvement → Persona Publisher
With Analytics & Reporting:
text
Engagement Evaluator → Analytics Dashboard → Performance Reports → Strategy Planning
With Governance Layer:
text
Engagement Evaluator → Judge Review → HITL Escalation → Governance Decisions
Summary
The Engagement Evaluator closes Chimera's learning loop while maintaining strict governance boundaries.

Autonomy ends where interpretation begins.

This skill embodies Chimera's core principles:

Insight without authority — Understanding performance without control

Measurement without mutation — Observing outcomes without changing them

Learning without risk — Improving through data without exposure

Prediction without presumption — Forecasting without certainty

Every evaluation is:

✅ Governed by confidence thresholds and quality gates

✅ Auditable with complete provenance and metadata

✅ Actionable with prioritized insights and recommendations

✅ Improving through continuous learning feedback

✅ Safe with graceful degradation and escalation paths

The Engagement Evaluator ensures Chimera learns from every interaction while remaining bounded, accountable, and aligned with human oversight