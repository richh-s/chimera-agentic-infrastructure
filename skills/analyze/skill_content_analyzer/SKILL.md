# Skill: Content Analyzer

## Skill ID
`skill_content_analyzer`

## Version
`1.1.0`

---

## Purpose

The **Content Analyzer** skill extracts **semantic meaning** from structured
text content (e.g., transcripts, captions, descriptions).

It transforms raw text into **governed, machine-readable signals** used for:
- Safety validation
- Cost gating
- Persona alignment
- Campaign planning

This skill provides **understanding**, not authority.

---

## Responsibility Boundary

### This skill DOES:
- Perform topic extraction, theme detection, entity recognition
- Produce fine-grained sentiment analysis
- Attach confidence and relevance scores
- Emit structured, auditable outputs
- Provide analysis metadata for deduplication and caching

### This skill DOES NOT:
- Download or ingest media
- Perform transcription
- Make safety or compliance decisions
- Rewrite or publish content
- Write to long-term memory directly

---

## Invoked By

- **Worker Agent**, via a Planner-issued Task

---

## Analysis Methods

### Topic Extraction
- Uses LDA-style topic modeling or equivalent
- Extracts 3–5 dominant topics
- Assigns confidence and relevance scores
- Normalized against Chimera taxonomy

### Theme Detection
- Identifies narrative and abstract themes
- Provides descriptive context
- Associates confidence with each theme

### Entity Recognition
- Named Entity Recognition (NER)
- Entity typing (PERSON, ORG, LOCATION, etc.)
- Frequency analysis to identify significance

### Sentiment Analysis
- Overall polarity classification
- Continuous sentiment score (-1.0 → +1.0)
- Breakdown across positive / neutral / negative
- Key emotional signals extracted

---

## Inputs

(Strictly validated — see `contract.json`)

- **`text`** *(required)*  
  Plain text to analyze.

- **`language`** *(optional)*  
  ISO-639-1 language code. Defaults to auto-detection.

- **`analysis_depth`** *(optional)*  
  One of `basic`, `standard`, `deep`.  
  Controls cost and fidelity.

---

## Execution Constraints

- Maximum execution time: **30 seconds**
- Maximum text length: **20,000 characters**
- Analysis depth determines compute cost
- No external write access

---

## Quality Metrics

### Confidence Thresholds

| Confidence Range | Judge Action |
|-----------------|-------------|
| 0.0 – 0.3 | Reject & escalate |
| 0.3 – 0.6 | Flag for HITL |
| 0.6 – 0.8 | Accept with caution |
| 0.8 – 1.0 | Accept |

Low-confidence outputs MUST be surfaced to the Judge.

---

## Cache Strategy

### Deduplication
- Input text hashed using SHA-256
- Identical text within TTL returns cached result

### Cache TTL

| Analysis Depth | TTL |
|---------------|-----|
| Basic | 48h |
| Standard | 24h |
| Deep | 12h |

Cache invalidated on:
- Model upgrades
- Method changes
- Governance override

---

## Cost Transparency

| Analysis Depth | Compute Cost | Typical Use |
|---------------|--------------|-------------|
| Basic | ~0.5 CPU-sec | Screening |
| Standard | ~2.0 CPU-sec | Default |
| Deep | ~8.0 CPU-sec | Planning |

Rules:
- Auto-select `basic` for text < 500 chars
- `deep` requires explicit Planner intent

---

## Failure Modes & Recovery

| Error Code | Category | Retry | Escalation |
|----------|----------|-------|------------|
| `TEXT_EMPTY` | Validation | No | No |
| `TEXT_LIMIT` | Validation | No | Yes |
| `LANG_UNSUPPORTED` | Policy | No | Yes |
| `LOW_CONFIDENCE` | Quality | No | Flag |
| `ANALYSIS_ERROR` | Execution | Yes (1×) | Yes |

### Graceful Degradation
If full analysis fails:
1. Attempt sentiment-only analysis
2. Fall back to keyword extraction
3. Return minimal metadata with low confidence

---

## Integration Examples

### Basic Invocation
```json
{
  "skill": "skill_content_analyzer",
  "inputs": {
    "text": "The AI revolution brings both opportunities and challenges.",
    "analysis_depth": "standard"
  }
}
Multilingual Example
{
  "skill": "skill_content_analyzer",
  "inputs": {
    "text": "La inteligencia artificial transformará nuestra sociedad.",
    "language": "es",
    "analysis_depth": "basic"
  }
}
Downstream Dependency
flowchart TD
    A[Content Analyzer] --> B{Confidence > 0.8?}
    B -->|Yes| C[Safety Validator]
    B -->|No| D[Judge Review]
    C --> E[Cost Guard]
    E --> F[Persona Publisher]
Compliance & Privacy
No user tracking

No persistent storage

Text processed in-memory

Outputs inherit input data classification

Summary
The Content Analyzer gives Chimera meaning with accountability.

It enables informed governance decisions while remaining
bounded, auditable, and cost-aware.