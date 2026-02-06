# Skill: Media Harvester

## Skill ID
`skill_media_harvester`

## Version
`1.1.0`

---

## Purpose

The **Media Harvester** skill is responsible for **securely ingesting external media assets**
(video, image, or audio) into Project Chimera’s controlled runtime environment.

This skill performs **download, validation, integrity verification, and metadata extraction only**.

It does **not** analyze semantic content, make safety judgments, or publish media.

---

## Responsibility Boundary

### This skill DOES:
- Download media from **HTTPS-only** public URLs
- Enforce media-type, size, duration, and format constraints
- Verify file integrity using checksums and platform signals
- Extract technical metadata (format, duration, dimensions, codec, bitrate)
- Store assets in isolated, temporary storage
- Produce deterministic, auditable outputs

### This skill DOES NOT:
- Perform transcription or semantic analysis
- Rewrite or transform content
- Make safety, policy, or cost decisions
- Persist long-term memory
- Trigger publication or scheduling

---

## Invoked By

- **Worker Agent**, acting on a Planner-issued Task

---

## Inputs

The skill accepts the following inputs (see `contract.json` for strict validation rules):

- **`url`** *(required)*  
  Publicly accessible **HTTPS** media URL.

- **`media_type`** *(required)*  
  One of: `video`, `image`, `audio`

- **`quality`** *(optional)*  
  One of: `low`, `medium`, `high`  
  Defaults to `medium` when omitted.

---

## Execution Constraints

The Media Harvester enforces the following constraints at runtime:

- **Maximum execution time:** 60 seconds  
- **Rate limit:** 10 requests per minute  
- **Maximum file size:** 500 MB  
- **Maximum duration (video/audio):** 3600 seconds  
- **Allowed formats:**
  - Video: `mp4`, `webm`, `mov`
  - Image: `jpg`, `jpeg`, `png`, `gif`, `webp`
  - Audio: `mp3`, `wav`, `ogg`, `m4a`

Resource limits:
- Memory: 256 MB
- CPU: 1 core
- Temporary disk usage: 1024 MB

---

## External Interaction

- All external access occurs **exclusively via MCP Action Tools**
- Direct HTTP requests, SDK calls, or shell access are forbidden
- Redirects are followed up to a safe maximum
- Robots.txt and platform terms are respected

---

## Outputs

On success, the skill produces structured outputs including:

- **`local_path`** — internal path to the downloaded media  
- **`size_mb`** — file size in megabytes  
- **`checksum`** — SHA-256 integrity checksum  
- **`metadata`** — extracted technical properties:
  - format
  - duration (seconds)
  - dimensions (if applicable)
  - codec
  - bitrate
- **`download_status`** — verification result:
  - verification flag
  - verification method
  - verification timestamp (ISO-8601)

All outputs are deterministic and auditable.

---

## Storage Strategy

### Temporary Storage
- Assets are stored in an isolated temporary directory
- Automatic cleanup occurs after 24 hours
- No persistence across sessions unless promoted downstream

### Naming Convention
skill_media_harvester/{timestamp}_{checksum_short}.{ext}


### Access Control
- Read-only for downstream skills
- No public URLs generated
- Encrypted at rest where supported

---

## Failure Modes & Escalation

| Category | Error Code | Retry | Escalation |
|--------|-----------|-------|------------|
| Network timeout | `NETWORK_TIMEOUT` | Yes (2×) | No |
| Invalid URL | `URL_INVALID` | No | No |
| File too large | `SIZE_LIMIT` | No | Yes |
| Unsupported format | `FORMAT_UNSUPPORTED` | No | Yes |
| Virus detected | `SECURITY_THREAT` | No | 🚨 Immediate HITL |
| Rate limit exceeded | `RATE_LIMIT` | No | Yes |

**Immediate HITL escalation occurs for:**
- Malware or prohibited content detection
- Repeated failures indicating systemic issues
- Security or compliance violations

---

## Cost Considerations

- Bandwidth usage is monitored per domain
- Quality may be downgraded automatically if cost thresholds are approached
- Frequent assets may be cached for up to 24 hours

---

## Compliance & Privacy

- HTTPS enforced for all downloads
- Virus scanning and content filtering enabled
- No user tracking or analytics
- Source URLs and checksums logged for audit
- No redistribution of downloaded content

---

## Integration Example

```json
{
  "skill": "skill_media_harvester",
  "inputs": {
    "url": "https://example.com/video.mp4",
    "media_type": "video",
    "quality": "high"
  }
}
Summary
The Media Harvester is Chimera’s secure ingestion gateway.

It ensures that all external media enters the system in a controlled,
validated, auditable, and policy-compliant manner—forming the foundation
for all downstream analysis and publishing workflows.