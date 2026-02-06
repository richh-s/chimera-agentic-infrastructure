# Skill: Persona Publisher

## Skill ID
`skill_persona_publisher`

## Version
`2.0.0`

---

## Purpose

The **Persona Publisher** transforms validated content into **persona-aligned, platform-specific publishable output**.

It is the **final creative step** before scheduling or publication, but it does **not** publish content itself. This skill ensures Chimera speaks with a consistent, intentional voice while respecting platform constraints and governance boundaries.

---

## Responsibility Boundary

### This Skill DOES:
- Rewrite content to match persona voice and tone
- Apply platform-specific formatting constraints
- Enforce stylistic and structural rules
- Generate alternative content variants for A/B testing
- Emit confidence scores and formatting metadata
- Surface non-blocking warnings for Judge awareness
- Maintain full audit trail of transformations

### This Skill DOES NOT:
- Decide *what* content should be published
- Perform safety or cost validation
- Publish or schedule content
- Learn or mutate persona definitions
- Make publication timing decisions
- Bypass downstream governance checks

---

## Persona Model

A persona defines **how** Chimera speaks, not **what** it says. Personas are **immutable during execution** and must be versioned.

### Persona Components:
- **Voice**: Overall personality (e.g., analytical, authoritative, conversational)
- **Tone**: Emotional register (formal, casual, playful, provocative)
- **Style Guidelines**: Explicit rules (sentence length, emoji usage, jargon policy)
- **Boundaries**: Topics allowed/forbidden, content limitations
- **Target Audience**: Who the persona addresses (general, technical, business)

### Persona Governance:
- Versioned using semantic versioning
- Changes require governance approval
- No runtime modification allowed
- Audit trail of all persona applications

---

## Platform Formatting Rules

| Platform | Key Constraints | Optimal Strategy |
|----------|-----------------|------------------|
| **X (Twitter)** | 280 characters, 4 media slots | Punchy phrasing, 1-2 hashtags, thread-ready |
| **LinkedIn** | 3000 characters, professional tone | Paragraph breaks, data-driven insights, minimal hashtags |
| **Instagram** | 2200 characters, 30 hashtags max | Visual storytelling, emoji usage, hashtag clusters |
| **TikTok** | 150 characters for captions | Hook-first, casual tone, trending audio context |
| **YouTube** | 5000 characters for descriptions | SEO-optimized, timestamped, keyword-rich |
| **Bluesky** | 300 characters, custom feeds | Community-aligned, concise, feed-aware |
| **Mastodon** | 500 characters, instance norms | Federated-aware, community guidelines respected |

Platform rules are **applied deterministically** with version tracking.

---

## Generation Pipeline

### 1. **Input Validation & Provenance Check**
- Validate persona schema and version
- Verify platform compatibility
- Check hard limits (length, forbidden phrases)
- Confirm content provenance (source, analysis references)

### 2. **Persona Alignment**
- Rewrite content to match persona voice characteristics
- Apply tone and emotional register
- Enforce stylistic rules and boundaries
- Preserve core semantic meaning and intent

### 3. **Platform Adaptation**
- Apply platform-specific formatting
- Enforce character limits and structure
- Insert required hashtags, mentions, or CTAs
- Optimize for platform engagement patterns

### 4. **Quality Assurance & Variant Generation**
- Generate 1-3 alternative formulations
- Measure tone alignment and persona adherence
- Check constraint compliance
- Calculate readability scores
- Emit confidence score and structured warnings

### 5. **Audit & Compliance Logging**
- Record all transformation steps
- Log persona and platform versions
- Generate unique generation ID
- Prepare compliance validation report

---

## Confidence Thresholds & Quality Gates

| Confidence Range | Action Required | Downstream Impact |
|-----------------|-----------------|-------------------|
| **≥ 0.8** | Accept output | Ready for immediate publication review |
| **0.7–0.79** | Accept with warnings | Requires Judge acknowledgment of warnings |
| **0.6–0.69** | Escalate to Judge | Manual review before proceeding |
| **< 0.6** | Reject and escalate | Cannot proceed; requires HITL intervention |

### Additional Quality Gates:
- **Persona Adherence**: Minimum 0.8 score required
- **Platform Optimization**: Minimum 0.7 score required
- **Readability**: Flesch score between 40-100
- **Warning Count**: Maximum 3 non-blocking warnings
- **Compliance**: All required checks must pass

Low-confidence outputs **MUST** be escalated. No silent failures allowed.

---

## Failure Modes & Recovery

| Error Category | Error Code | Automatic Recovery | Escalation Required |
|----------------|------------|-------------------|-------------------|
| **Invalid Persona** | `PERSONA_INVALID` | ❌ No | ✅ Immediate |
| **Constraint Conflict** | `CONSTRAINT_CONFLICT` | ❌ No | ✅ Yes |
| **Generation Failure** | `GENERATION_FAILED` | ✅ Fallback strategy | ⚠️ If fallback fails |
| **Timeout** | `EXECUTION_TIMEOUT` | ✅ Return partial | ✅ Yes |
| **Platform Unsupported** | `PLATFORM_UNSUPPORTED` | ✅ Generic fallback | ✅ Yes |
| **Quality Threshold** | `QUALITY_BELOW_THRESHOLD` | ❌ No | ✅ Yes |

### Fallback Strategies (in order):
1. Simplify style (remove complex formatting)
2. Remove optional constraints
3. Switch to persona variant
4. Platform fallback to "Generic"
5. Return unformatted content with explanation

**Fail-safe by default** — never publish questionable content.

---

## Integration Flow

```mermaid
flowchart TD
    A[Safety Validator<br/>✅ Approved] --> B[Cost Guard<br/>✅ Budget OK]
    B --> C[Persona Publisher<br/>Transform Content]
    C --> D{Confidence ≥ 0.7?}
    D -->|Yes| E[Output: Formatted Content<br/>+ Metadata + Variants]
    E --> F[Scheduler / Publisher<br/>Timing & Execution]
    D -->|No| G[Judge Review<br/>Manual Assessment]
    G -->|Override| F
    G -->|Reject| H[Task Failed<br/>Escalate to HITL]
    
    style A fill:#e8f5e8
    style B fill:#fff3e0
    style C fill:#e3f2fd
    style G fill:#fce4ec
    style H fill:#ffebee
Integration Examples
Basic LinkedIn Post
json
{
  "skill": "skill_persona_publisher",
  "inputs": {
    "content": "AI governance frameworks must balance innovation with ethical safeguards.",
    "persona": {
      "persona_id": "persona_ai_thought_leader",
      "voice": "authoritative",
      "tone": "professional",
      "target_audience": "business",
      "style_guidelines": [
        "Concise sentences under 25 words",
        "No emojis",
        "Data-driven insights",
        "Active voice preferred"
      ],
      "persona_boundaries": {
        "topics_allowed": ["AI ethics", "policy", "innovation"],
        "max_hashtags": 3,
        "emoji_usage": "none"
      },
      "persona_version": "2.1.0"
    },
    "platform": "LinkedIn",
    "platform_specific_rules": {
      "hashtag_strategy": "trailing",
      "line_break_style": "double"
    },
    "content_type": "social_post",
    "constraints": {
      "max_length": 280,
      "required_hashtags": ["#AI", "#Governance", "#Ethics"],
      "content_structure": "paragraph"
    },
    "content_provenance": {
      "source_skill": "skill_content_analyzer",
      "analysis_references": {
        "topics": ["AI Governance", "Ethical Frameworks"],
        "sentiment": "neutral",
        "confidence_score": 0.88
      }
    }
  }
}
X (Twitter) Thread Variant
json
{
  "skill": "skill_persona_publisher",
  "inputs": {
    "content": "Exploring three key principles for responsible AI deployment...",
    "persona": {
      "persona_id": "persona_tech_commentator",
      "voice": "conversational",
      "tone": "provocative",
      "style_guidelines": ["Thread-friendly", "Punchy openings", "Engagement questions"]
    },
    "platform": "X",
    "content_type": "thread",
    "constraints": {
      "max_length": 260,
      "required_mentions": ["@AI_Research"],
      "call_to_action": "What principles would you add? 👇"
    }
  }
}
Cost & Performance Considerations
Resource Usage:
Execution Time: < 20 seconds (95th percentile)

Memory: 512 MB maximum

CPU: 2 cores allocated

Cache Hit Ratio: Target > 60%

Cost Optimization:
Cache identical inputs (content + persona + platform hash)

Reuse generation for similar content patterns

Batch processing for thread generation

Progressive enhancement based on confidence

Compliance & Audit Requirements
Mandatory Audit Fields:
Generation ID (unique per transformation)

Timestamp (ISO 8601)

Persona ID and version

Platform and content type

Confidence score and compliance checks

Input content hash (SHA-256)

Retention Policy:
Audit logs retained for 90 days minimum

Generation metadata stored for 30 days

Compliance reports archived for 1 year

Security Controls:
No external API calls during generation

Input sanitization against injection attacks

Output validation before returning

Rate limiting (20 requests/minute)

Summary
The Persona Publisher ensures Chimera speaks with a consistent, intentional voice while respecting platform constraints and governance boundaries.

It shapes expression — it does not grant autonomy.

Every transformation is:

✅ Governed by versioned personas

✅ Constrained by platform rules

✅ Measured by quality metrics

✅ Audited for compliance

✅ Reversible through provenance tracking

This skill completes the content preparation pipeline while maintaining Chimera's core principle: power without unchecked authority.