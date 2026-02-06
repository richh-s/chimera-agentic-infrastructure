# Skill: Memory Curator

## Skill ID
`skill_memory_curator`

## Version
`2.0.0`

---

## Purpose

The **Memory Curator** governs Chimera's **long-term learning system** by controlling what enters long-term memory. It transforms raw learning signals into **auditable, policy-compliant memory action plans** while preserving human oversight and governance guarantees.

This skill ensures Chimera learns effectively while maintaining strict boundaries between learning, memory, and action.

---

## Core Principle

> **Learning without autonomy.**  
Chimera may learn, but it may not decide what becomes memory without policy, confidence, and oversight.

Memory is **privilege, not right**. Every memory entry must earn its place through governance, validation, and audit.

---

## Responsibility Boundary

### This Skill DOES:
- **Evaluate** memory candidates against versioned memory policies
- **Normalize**, tag, and structure memory content for consistency
- **Detect** and redact sensitive information (PII, secrets, credentials)
- **Deduplicate** and merge overlapping or complementary knowledge
- **Apply** retention, expiration, and archival rules based on policy
- **Suggest** semantic relationships for knowledge graph enrichment
- **Propose** create/update/merge/deprecate/archive actions
- **Escalate** sensitive, uncertain, or policy-adjacent memories for human review
- **Generate** policy feedback, learning metrics, and quality insights
- **Produce** complete, immutable audit trails for all decisions

### This Skill DOES NOT:
- **Write**, delete, or directly mutate memory storage
- **Perform** external lookups, enrichment, or data augmentation
- **Store** PII, secrets, credentials, or sensitive personal data
- **Override** Judge, HITL, or governance team decisions
- **Trigger** planning, execution, or behavior changes
- **Make** autonomous decisions about what Chimera "knows"
- **Access** raw user data or external analytics platforms

---

## Memory Candidate Taxonomy

Memory candidates are categorized into governed semantic kinds with strict validation:

### **Strategy & Performance Learning**
| Kind | Purpose | Example | Auto-Approval Threshold |
|------|---------|---------|------------------------|
| `strategy_learning` | Campaign effectiveness patterns | "Question-based hooks outperform statements by 30%" | 0.85 |
| `performance_pattern` | Engagement pattern detection | "Friday afternoons show 15% lower CTR" | 0.8 |
| `timing_optimization` | Temporal performance insights | "Best posting time: 10AM local audience time" | 0.8 |

### **Platform & Persona Insights**
| Kind | Purpose | Example | Auto-Approval Threshold |
|------|---------|---------|------------------------|
| `platform_insight` | Platform-specific behavior | "LinkedIn prefers paragraph breaks over bullet points" | 0.85 |
| `persona_learning` | Persona performance metrics | "Tech_Leader persona engages best with data-driven posts" | 0.8 |
| `content_style` | Format and style effectiveness | "Short sentences (<15 words) increase readability by 40%" | 0.75 |
| `audience_insight` | Audience behavior patterns | "Developer audience prefers code examples over metaphors" | 0.8 |

### **System & Operations Learning**
| Kind | Purpose | Example | Auto-Approval Threshold |
|------|---------|---------|------------------------|
| `workflow_learning` | Process optimization | "Batch processing reduces execution time by 60%" | 0.85 |
| `cost_learning` | Resource efficiency insights | "Image compression reduces storage cost by 70% with minimal quality loss" | 0.8 |
| `system_behavior` | System performance patterns | "Memory usage spikes during video transcription" | 0.7 |
| `capability_discovery` | New skill or pattern detection | "Skill can now process 4K video with hardware acceleration" | 0.7 |

### **Risk & Compliance Governance**
| Kind | Purpose | Example | Auto-Approval Threshold |
|------|---------|---------|------------------------|
| `safety_learning` | Safety pattern recognition | "Posts mentioning 'guaranteed' trigger higher scrutiny" | 0.6 (always reviewed) |
| `compliance_learning` | Regulatory pattern detection | "Certain financial terms require disclaimers" | 0.6 (always reviewed) |
| `risk_pattern` | Risk factor identification | "Rapid posting frequency correlates with spam flags" | 0.7 |

### **Governance & Taxonomy**
| Kind | Purpose | Example | Auto-Approval Threshold |
|------|---------|---------|------------------------|
| `taxonomy_update` | Classification system improvements | "Add 'AI_Governance' as new topic category" | 0.5 (always escalated) |

### **Other & Uncategorized**
| Kind | Purpose | Example | Auto-Approval Threshold |
|------|---------|---------|------------------------|
| `other` | Uncategorized learning | Catch-all for unclassified insights | 0.0 (never auto-approved) |

**Note:** Allowed kinds are strictly controlled by `memory_policy.allowed_kinds`. Unlisted kinds are automatically rejected.

---

## Governance Rules (Non-Negotiable)

### 1. **Sensitive Data Is Never Stored**
The curator must **reject or redact**:
- **PII**: Emails, phone numbers, physical addresses, government IDs
- **Credentials**: API keys, passwords, tokens, access codes
- **Financial Data**: Credit card numbers, account details, transaction data
- **Health Information**: Medical conditions, treatments, patient data
- **Competitive Secrets**: Unreleased features, pricing strategies, IP
- **Security Details**: System vulnerabilities, infrastructure maps

**Rule:** If uncertainty exists about sensitivity → **escalate**. Never store questionable content.

### 2. **Retention Is Mandatory & Bounded**
Every accepted memory must have:
- **Defined Retention**: Explicit `retention_days` (1-3650)
- **Expiration Category**: `ephemeral`, `short_term`, `medium_term`, `long_term`, or `permanent`
- **Auto-Review Schedule**: Periodic confidence decay and re-evaluation
- **Archival Path**: Clear transition to read-only or metadata-only storage

**Rule:** No permanent memory without explicit policy allowance. Memory has natural decay.

### 3. **Confidence-Driven Decision Hierarchy**

| Confidence Range | Policy Field | Outcome | Human Oversight |
|------------------|--------------|---------|-----------------|
| ≥ 0.85 | `min_auto_accept` | Auto-accept | None required |
| 0.7 - 0.84 | `min_accept` | Accept with review | Judge notification |
| 0.6 - 0.69 | `review_threshold` | Review required | Judge approval |
| 0.4 - 0.59 | `escalation_threshold` | Escalate | HITL or governance review |
| < 0.4 | - | Reject | Audit only |

**Rule:** Low-confidence learning is never silently persisted. Uncertainty must be surfaced.

### 4. **Human Approval Is First-Class Workflow**
Human approval is **required** for:
- **Confidential or Restricted Data**: Any memory with `data_classification: confidential` or higher
- **Safety Learning**: All `safety_learning` and `compliance_learning` candidates
- **Taxonomy Updates**: Any `taxonomy_update` proposal
- **Policy Contradictions**: Memories that contradict existing policy or knowledge
- **First-of-Kind**: First instance of any new memory kind
- **System Behavior Changes**: `system_behavior` or `capability_discovery` with high impact
- **High-Risk Patterns**: Anything marked with `sensitivity_hints: possible_*`

**Rule:** When in doubt, escalate. Human judgment cannot be automated away for critical decisions.

---

## Curation Pipeline

### **Phase 1: Intake & Validation** *(< 2 seconds)*
- **Schema Validation**: Verify all required fields and formats
- **Batch Constraints**: Enforce `max_candidates_per_batch` (100)
- **Policy Compatibility**: Check `policy_version` against supported versions
- **Content Limits**: Validate `max_content_length_chars` (10,000)
- **Rejection Criteria**: Malformed, oversized, or unsupported input

### **Phase 2: Sensitivity & Redaction** *(< 5 seconds)*
- **Pattern Scanning**: Apply `redaction_rules` for PII, secrets, etc.
- **Content Analysis**: Use `sensitivity_hints` and heuristic detection
- **Redaction Application**: Replace sensitive content with `[REDACTED]` markers
- **Audit Logging**: Record all redactions with patterns and confidence
- **Escalation**: Flag uncertain sensitivity for human review

### **Phase 3: Normalization & Deduplication** *(< 8 seconds)*
- **Tag Normalization**: Convert tags to lowercase, remove duplicates, enforce patterns
- **Content Hashing**: Generate SHA-256 `content_hash` for deduplication
- **Index Comparison**: Check against `existing_memory_index` for duplicates
- **Merge Detection**: Identify similar content for strengthening vs. new entry
- **Confidence Aggregation**: Combine confidence from multiple sources

### **Phase 4: Retention & Lifecycle Planning** *(< 3 seconds)*
- **Retention Assignment**: Apply `retention_policy` defaults and overrides
- **Expiration Categorization**: Assign `expiration_category` based on hints and policy
- **Auto-Review Scheduling**: Calculate next review date based on `auto_review_cycles`
- **Archival Planning**: Determine archival path and compression requirements
- **Priority Setting**: Assign `priority` based on impact and confidence

### **Phase 5: Knowledge Graph Integration** *(< 7 seconds)*
- **Entity Extraction**: Identify `related_entities` from content and tags
- **Relationship Suggestion**: Propose semantic links using `relationship_types`
- **Strength Calculation**: Weight relationships by evidence and confidence
- **Contradiction Detection**: Flag conflicting knowledge with explicit `contradicts` edges
- **Graph Updates**: Generate `knowledge_graph_updates` for downstream processing

### **Phase 6: Decision & Audit** *(< 5 seconds)*
- **Confidence Assessment**: Calculate overall `confidence_score` for batch
- **Policy Compliance**: Check against all `forbidden_content_rules`
- **Escalation Routing**: Route items to appropriate approval workflows
- **Audit Generation**: Create complete `curation_metadata` with all decisions
- **Feedback Generation**: Produce `policy_feedback` and `learning_metrics`

---

## Decision Outcomes & Escalation Paths

| Decision | Meaning | Required Actions | Timeline | Escalation Path |
|----------|---------|-----------------|----------|-----------------|
| **`pass`** | All candidates safe to proceed | Write accepted items to memory store | Immediate | None |
| **`partial_pass`** | Some accepted, some rejected | Write accepted; log rejections with reasons | Immediate | Judge notification |
| **`review_required`** | Human approval needed for some items | Hold batch; route to Judge queue | 24 hours | Judge → HITL if no response |
| **`escalated`** | High-risk or sensitive content | Hold batch; route to governance team | 48 hours | Governance → Security if needed |
| **`blocked`** | Policy violation or unsafe batch | No writes; high-priority alert | Immediate | Security + Governance + HITL |

### **Approval Workflow Chains:**
Low Risk: Judge → (auto-approve if confidence > 0.8)
Medium Risk: Judge → HITL → (approve/reject)
High Risk: Judge → Governance Team → Security Review → HITL
Critical: Immediate HITL → Security → Executive Review

text

---

## Knowledge Graph Governance

### **Relationship Types & Semantics:**
| Relationship | Meaning | Use Case | Confidence Threshold |
|--------------|---------|----------|---------------------|
| **`supports`** | Evidence supports claim | "Data shows X works on LinkedIn" → supports "LinkedIn strategy" | 0.8 |
| **`contradicts`** | Evidence contradicts claim | "New data contradicts previous timing insight" | 0.85 |
| **`extends`** | Builds upon existing knowledge | "Advanced technique extends basic method" | 0.75 |
| **`deprecates`** | New insight replaces old | "Updated algorithm deprecates v1 approach" | 0.9 |
| **`similar_to`** | Semantic similarity | "Twitter insight similar to Bluesky pattern" | 0.7 |
| **`prerequisite_for`** | Required knowledge | "Understanding A required for B" | 0.8 |
| **`alternative_to`** | Different approach to same goal | "Method B alternative to Method A" | 0.75 |

### **Governance Rules:**
- Relationships are **suggestions only** → no automatic graph mutation
- All edges include confidence, justification, and version context
- Contradictory knowledge is preserved with explicit `contradicts` links
- Circular relationships are detected and flagged for review
- Relationship strength decays with memory confidence over time

---

## Failure Modes & Recovery

| Failure Category | Detection | Automatic Recovery | Escalation Required | Impact Level |
|------------------|-----------|-------------------|-------------------|--------------|
| **Validation Error** | Schema mismatch, missing fields | ❌ Reject batch | ✅ Immediate | High |
| **Policy Conflict** | Rule contradiction, version mismatch | ❌ No | ✅ Governance review | Critical |
| **Model Uncertainty** | Low confidence scores, ambiguous content | ✅ Degrade analysis | ⚠️ If confidence < 0.6 | Medium |
| **Execution Timeout** | Processing exceeds 30s | ✅ Return partial results | ✅ Yes | High |
| **Resource Exhaustion** | Memory/CPU limits exceeded | ✅ Simplify analysis | ⚠️ If repeated | Medium |
| **Data Corruption** | Invalid hashes, malformed content | ❌ Reject affected items | ✅ Security review | Critical |
| **Network Failure** | Cache/index unavailable | ✅ Use local fallback | ⚠️ If persistence needed | Low |

### **Graceful Degradation Levels:**
1. **Full Analysis**: Complete pipeline with all features (requires all resources)
2. **Essential Analysis**: Core validation + redaction + basic decisions (requires model + policy)
3. **Minimal Analysis**: Schema validation only (requires policy)
4. **Fail-Closed**: Reject all with detailed error (safety default)

**Golden Rule:** Safety always wins. Better to reject good memory than accept bad memory.

---

## Integration & Data Flow

```mermaid
flowchart TD
    subgraph "Learning Sources"
        A[Engagement Evaluator<br/>Performance Insights]
        B[Trend Classifier<br/>Pattern Detection]
        C[Safety Validator<br/>Risk Learning]
        D[Content Analyzer<br/>Semantic Patterns]
        E[Workflow Orchestrator<br/>Process Optimization]
    end
    
    A --> F[Memory Curator<br/>Batch Processing]
    B --> F
    C --> F
    D --> F
    E --> F
    
    F --> G{Confidence & Policy Check}
    
    G -->|≥ 0.85 + No Red Flags| H[Auto-Accept<br/>Write to Memory Store]
    G -->|0.7-0.84 or Minor Flags| I[Judge Review Queue<br/>24h SLA]
    G -->|< 0.7 or Major Flags| J[Governance Escalation<br/>48h SLA]
    G -->|Policy Violation| K[Immediate Block<br/>Security Alert]
    
    H --> L[Knowledge Graph<br/>Relationship Updates]
    I -->|Approved| H
    I -->|Rejected| M[Rejection Audit Log]
    J -->|Approved with Conditions| H
    J -->|Rejected| N[High-Risk Audit Trail]
    
    L --> O[Memory Index<br/>Real-time Search]
    O --> P[Planner<br/>Strategy Optimization]
    O --> Q[Persona Publisher<br/>Content Improvement]
    
    F --> R[Policy Feedback Loop<br/>Continuous Improvement]
    R --> S[Governance Team<br/>Policy Updates]
    S --> T[Memory Policy<br/>Version 2.1.1]
    T -.-> F
    
    style F fill:#e3f2fd
    style G fill:#fff3e0
    style H fill:#e8f5e8
    style I fill:#fff3e0
    style J fill:#fce4ec
    style K fill:#ffebee
    style R fill:#f3e5f5
Quality Gates & Performance Targets
Input Quality Gates:
✅ Batch size: 1-100 candidates

✅ Content length: 5-10,000 characters

✅ Policy version: Compatible with current system

✅ Required fields: All present and valid

✅ Sensitive content: Flagged for review/redaction

Processing Performance:
P95 Processing Time: < 25 seconds

Memory Usage: < 1 GB per batch

CPU Utilization: < 2 cores sustained

Cache Hit Ratio: > 60% for relationship lookups

Throughput: 15 batches/minute maximum

Output Quality Targets:
Decision Consistency: > 85% for identical inputs

False Positive Rate: < 10% (accepting bad memory)

False Negative Rate: < 15% (rejecting good memory)

Policy Compliance: > 90% across all decisions

Audit Completeness: 100% of decisions logged

Monitoring & Alerts:
🚨 Critical: Policy violation, security breach, data leak

⚠️ High: High rejection rate (>40%), low confidence batches (<0.6)

🔔 Medium: Processing time >30s, cache miss rate >50%

ℹ️ Low: Policy feedback generated, relationship suggestions made

Compliance & Audit Requirements
Mandatory Audit Fields:
curation_id: Unique identifier for each curation batch

timestamp: ISO 8601 timestamp of decision

policy_version: Exact policy version applied

confidence_score: Overall batch confidence

decision: Final curation decision

accepted_count/rejected_count/escalation_count: Outcome statistics

redaction_details: All redactions applied with patterns

escalation_reasons: Why items required human review

Data Retention:
Curation Results: 180 days minimum

Rejection Logs: 90 days minimum

Audit Trails: 365 days minimum

Learning Data: 730 days for model improvement

Policy Versions: Permanent (immutable storage)

Security Controls:
Encryption: AES-256 at rest and in transit

Access Control: RBAC with strict separation of duties

Integrity Checks: SHA-256 hashing for all content

Change Tracking: Immutable logs for all policy and model changes

Compliance: GDPR, CCPA, HIPAA (where applicable), internal governance

Human Oversight Requirements:
Weekly: Review escalation patterns and policy effectiveness

Monthly: Audit random sample of auto-approved memories

Quarterly: Comprehensive policy review and update

Annually: Security audit and compliance certification

Summary
The Memory Curator is Chimera's conscience for learning — ensuring that every memory earned through experience meets strict governance standards before being allowed to influence future behavior.

Key Principles in Practice:

Memory is earned, not given → Every memory candidate must prove its value and safety

Uncertainty is surfaced, not hidden → Low confidence triggers review, not silence

Human judgment is irreplaceable → Critical decisions always involve human oversight

Audit is non-negotiable → Every decision is logged, traceable, and explainable

Safety always wins → Better to forget than to remember dangerously

This skill ensures Chimera grows wiser without growing reckless — learning from experience while remaining bounded by policy, oversight, and its core design principle: power without unchecked authority