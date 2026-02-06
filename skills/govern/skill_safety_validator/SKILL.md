# Skill: Safety Validator

## Skill ID
`skill_safety_validator`

## Version
`1.1.0`

---

## Purpose

The **Safety Validator** enforces Chimera's governance model by validating content
against **safety, compliance, platform policy, and ethical constraints**.

It is the **final automated gate** before any content may proceed to publishing
or scheduling.

---

## Responsibility Boundary

### This skill DOES:
- Evaluate content for safety and compliance risks
- Detect policy violations and ethical concerns
- Assign severity levels to violations
- Recommend remediation actions
- Surface uncertainty for Judge escalation
- Provide quantitative safety scores

### This skill DOES NOT:
- Modify or rewrite content
- Make publishing decisions
- Override the Judge or Human Governor
- Fetch external data or policies
- Store content beyond validation session

---

## Safety Domains Evaluated

| Domain | Examples | Risk Level |
|--------|----------|------------|
| Hate & Harassment | Slurs, dehumanization, targeted abuse | Critical |
| Misinformation | False claims, misleading advice, conspiracy theories | High |
| Violence | Threats, glorification, incitement | Critical |
| Sexual Content | Explicit or exploitative material | Medium-High |
| Self-Harm | Encouragement, instructions, normalization | Critical |
| Illegal Activity | Drugs, fraud, weapons promotion | High |
| Copyright | Unauthorized reproduction, plagiarism | Medium |
| Platform Policy | TOS violations, community guidelines | Medium |
| Ethical Risk | Manipulation, deception, psychological harm | High |
| Brand Safety | Reputational damage, inappropriate associations | Medium |
| Legal Compliance | Regulatory violations, disclosure requirements | High |

---

## Validation Pipeline

### 1. Content Analysis
- Text parsing and tokenization
- Contextual understanding
- Entity and relationship mapping

### 2. Rule Application
- Safety policy evaluation
- Platform-specific rule checking
- Risk profile weighting
- Ethical guideline assessment

### 3. Risk Scoring
- Quantitative safety scores (0.0-1.0)
- Severity classification
- Confidence calculation
- Remediation identification

### 4. Decision Generation
- Safety decision (pass/review/block)
- Violation reporting
- Recommendation generation
- Audit metadata collection

---

## Decision Semantics

| Decision | Confidence Threshold | Meaning | Default Action |
|----------|----------------------|---------|----------------|
| `pass` | ≥ 0.8 | No meaningful safety risk | Proceed to publishing |
| `review` | 0.6–0.79 | Ambiguous or medium risk | Escalate to Judge |
| `block` | < 0.6 | High or critical risk | Halt pipeline |

⚠️ **All decisions are advisory.**  
The Judge retains final authority and may override any decision.

---

## Violation Severity Framework

| Severity | Description | Required Action | Time to Escalation |
|----------|-------------|-----------------|-------------------|
| **Low** | Minor phrasing issues, tone concerns | Suggest edit | 24 hours |
| **Medium** | Policy-adjacent, potential violations | Review required | 2 hours |
| **High** | Clear violation, moderate harm risk | Block immediately | 30 minutes |
| **Critical** | Severe harm risk, illegal content | Immediate escalation | Instant HITL |

---

## Safety Scores Explained

### Quantitative Safety Metrics:
- **Overall Safety** (0.0-1.0): Comprehensive safety assessment
- **Toxicity Score** (0.0-1.0): Hate speech and harassment risk
- **Misinformation Risk** (0.0-1.0): Factual accuracy concerns
- **Platform Compliance** (0.0-1.0): Adherence to platform rules
- **Brand Safety** (0.0-1.0): Reputation and association risk

### Score Interpretation:
- 0.9-1.0: Exceptionally safe
- 0.7-0.89: Generally safe, minor concerns
- 0.5-0.69: Moderate risk, requires review
- 0.3-0.49: High risk, likely block
- <0.3: Critical risk, immediate block

---

## Failure Modes & Recovery

| Error Code | Description | Automatic Behavior | Recovery Strategy |
|------------|-------------|-------------------|-------------------|
| `UNCERTAIN_CLASSIFICATION` | Model uncertainty > 40% | Block decision | Escalate to Judge |
| `POLICY_CONFLICT` | Conflicting rule interpretations | Escalate immediately | Human review required |
| `INVALID_INPUT` | Malformed or unprocessable content | Reject with error | Fix input format |
| `INTERNAL_ERROR` | Processing failure | Block with error | System restart needed |
| `TIMEOUT` | Validation exceeded 25 seconds | Block for safety | Retry with simpler model |

**Fail-closed by default** — any uncertainty results in blocking.

---

## Integration Flow

```mermaid
flowchart LR
    A[Content Analyzer] --> B[Trend Classifier]
    B --> C[Safety Validator]
    C --> D{Decision & Confidence}
    D -->|Pass ≥0.8| E[Persona Publisher]
    D -->|Review 0.6-0.79| F[Judge Review]
    D -->|Block <0.6| G[Task Halted]
    F -->|Override Pass| E
    F -->|Confirm Block| G
    
    style C fill:#ffebee
    style F fill:#fff3e0
    style G fill:#fce4ec
Cost & Performance
No external API calls — Self-contained validation

Deterministic runtime — Predictable performance

Average latency: < 100ms per validation

Throughput: 20 validations per minute

Stateless operation — No session persistence

Cache-friendly — Results cacheable by content hash

Resource Requirements:
Memory: 512MB RAM

CPU: 1 core

Storage: 200MB for model cache

Network: None required

Compliance & Privacy
Data Protection:
No personal profiling or biometric inference

No external data enrichment or lookups

Ephemeral content handling (no persistence)

Encrypted processing where available

Audit Requirements:
Full audit logging enabled for all decisions

90-day retention of validation metadata

Tamper-evident decision records

Regular compliance attestations

Governance:
Model version tracking and rollback capability

Rule signature verification

Policy bundle integrity checks

Regular safety audits and updates

Platform-Specific Considerations
X (Twitter):
Character limit awareness

Hashtag and mention analysis

Trending topic sensitivity

YouTube:
Video description context

Community guideline focus

Copyright claim prevention

LinkedIn:
Professional tone requirements

Business context sensitivity

Industry-specific compliance

TikTok:
Short-form content optimization

Music and sound copyright

Youth safety protections

Instagram:
Visual context considerations

Hashtag and location analysis

Community guideline alignment

Integration Examples
Basic Validation:
json
{
  "skill": "skill_safety_validator",
  "inputs": {
    "content": "AI systems must be governed responsibly to ensure ethical outcomes.",
    "analysis_context": {
      "topics": [{"name": "AI Governance", "confidence": 0.85}],
      "themes": [{"theme": "Ethical Technology", "confidence": 0.78}],
      "sentiment": {"overall": "positive", "score": 0.65}
    },
    "platform": "LinkedIn",
    "risk_profile": "medium",
    "content_type": "social_post"
  }
}
With Violations Detected:
json
{
  "skill": "skill_safety_validator",
  "inputs": {
    "content": "This unapproved supplement cures all diseases instantly!",
    "analysis_context": {...},
    "platform": "X",
    "risk_profile": "low"
  }
}
// Returns violations: [{"category": "misinformation", "severity": "high", ...}]
Platform-Specific Validation:
json
{
  "skill": "skill_safety_validator",
  "inputs": {
    "content": "Check out our new product launch! #innovation #tech",
    "analysis_context": {...},
    "platform": "Instagram",
    "content_type": "ad_copy",
    "risk_profile": "high"
  }
}
Summary
The Safety Validator ensures Chimera remains aligned, defensible, and safe at scale.

It does not decide what to publish —
it ensures Chimera never publishes what it should not.

Fail-safe, auditable, and governed — the guardian at the gate