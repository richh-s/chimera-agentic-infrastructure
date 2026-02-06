# Skill: Trend Classifier

## Skill ID
`skill_trend_classifier`

## Version
`1.2.0`

---

## Purpose

The **Trend Classifier** evaluates semantic signals produced by upstream analysis
to determine whether content aligns with **emerging, stable, or declining trends**.

It connects **content understanding** to **strategic prioritization** without
making publishing or safety decisions.

---

## Responsibility Boundary

### This skill DOES:
- Classify content into trend categories
- Identify trend lifecycle stage
- Estimate trend momentum and relevance
- Provide confidence and supporting signals
- Recommend (non-binding) prioritization actions

### This skill DOES NOT:
- Discover trends from raw platform data
- Scrape or query external systems
- Modify or generate content
- Make publishing or safety decisions

---

## Inputs

Provided by upstream skills (validated via `contract.json`):

- **Topics** with confidence and relevance scores
- **Themes** with descriptive context
- **Entities** with frequency counts
- **Optional temporal context** (`real_time`, `recent`, `historical`)

---

## Trend Classification Model

### Trend Categories
- **Emerging** — Increasing relevance, early adoption
- **Stable** — Sustained interest, predictable performance
- **Declining** — Reduced relevance or saturation

### Trend Stages
1. **Early** — Initial discovery, niche interest
2. **Growth** — Accelerating adoption, expanding reach
3. **Peak** — Maximum visibility, mainstream attention
4. **Saturation** — Plateauing interest, competitive landscape
5. **Decline** — Decreasing relevance, legacy status

### Classification Criteria
Classification is based on weighted analysis of:
- Topic alignment strength (0.0–1.0)
- Theme consistency across samples
- Entity concentration and diversity
- Temporal weighting
- Novelty score
- Sentiment trend direction (−1.0 to +1.0)

---

## Quality & Confidence Thresholds

| Confidence | Action | Downstream Impact |
|-----------|--------|-------------------|
| < 0.4 | Reject, escalate to Judge | Block processing |
| 0.4–0.6 | Flag for HITL review | Proceed with caution |
| 0.6–0.8 | Accept with caution | Warning applied |
| > 0.8 | Accept for planning | Full confidence |

**Low-confidence classifications MUST be surfaced to the Judge.**

---

## Recommended Actions (Advisory Only)

| Recommendation | Criteria | Typical Use Case |
|----------------|----------|------------------|
| `prioritize` | High relevance + emerging/growth | Campaign focus |
| `monitor` | Moderate relevance + stable | Ongoing tracking |
| `deprioritize` | Low relevance + declining | Sunset planning |

⚠️ These are **recommendations only**.  
The Planner and Judge retain final authority.

---

## Pattern Library

### Emerging Patterns
- Novel topic with high novelty
- Accelerating mentions
- Diverse source adoption
- Early adopter focus

### Stable Patterns
- Consistent volume
- Established entities
- Predictable cycles
- Mainstream coverage

### Declining Patterns
- Decreasing velocity
- Saturation signals
- Negative sentiment shift
- Legacy dominance

---

## Failure Modes

| Error Code | Description | Recovery Strategy |
|------------|-------------|-------------------|
| `NO_SIGNALS` | Insufficient input | Return neutral, low confidence |
| `LOW_CONFIDENCE` | Below threshold | Flag for review |
| `CLASSIFICATION_ERROR` | Internal failure | Escalate to Judge |
| `INVALID_INPUT` | Malformed input | Reject immediately |

No automatic retries are attempted.

---

## Integration Flow

```mermaid
flowchart LR
    A[Content Analyzer] --> B[Trend Classifier]
    B --> C{Confidence > 0.6?}
    C -->|Yes| D[Safety Validator]
    C -->|No| E[Judge Review]
    E -->|Approved| D
    E -->|Rejected| F[Task Failed]
    
    style A fill:#e8f5e8
    style B fill:#fff3e0
    style D fill:#ffebee
    style E fill:#f3e5f5
Cost & Performance
Fixed compute cost — No external API calls

Stateless operation — No long-running state

Cache-friendly — Results cacheable by input hash

Performance Benchmarks
Average processing time: < 100ms

Throughput capacity: 30 requests/minute

Memory footprint: < 256MB

Compliance & Privacy
No personal data inference — Only analyzes content patterns

No external enrichment — All data from upstream skills

Inherited classification — Outputs inherit input data classification

Fully auditable — All decisions include confidence and signal scores

Data Retention
Trend results stored per Chimera policy

Supporting signals retained for 30 days

No persistent storage of raw inputs

Integration Examples
Basic Classification
json
{
  "skill": "skill_trend_classifier",
  "inputs": {
    "topics": [
      { "name": "AI Governance", "confidence": 0.85, "relevance_score": 0.72 }
    ],
    "themes": [
      {
        "theme": "Ethical Technology",
        "description": "Focus on responsible AI",
        "confidence": 0.78
      }
    ]
  }
}
With Historical Context
json
{
  "skill": "skill_trend_classifier",
  "inputs": {
    "topics": [...],
    "themes": [...],
    "entities": [...],
    "time_context": "recent",
    "historical_context": {
      "previous_trend_category": "emerging",
      "previous_velocity": 0.7,
      "days_since_last_observation": 7
    }
  }
}
Summary
The Trend Classifier turns semantic insight into strategic signal.

It helps Chimera focus attention where it matters,
while remaining governed, explainable, and non-authoritative.