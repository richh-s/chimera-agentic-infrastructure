# Skill: Vocal Analyzer

## Skill ID
`skill_vocal_analyzer`

## Version
`1.2.0`

---

## Purpose

The **Vocal Analyzer** skill converts audio content into **structured textual and vocal signals**.

It performs:
- Audio preprocessing and normalization
- Speech-to-text transcription
- Speaker diarization
- Vocal feature extraction
- Quality and confidence assessment

This skill is the **mandatory bridge** between media ingestion and semantic analysis.

---

## Responsibility Boundary

### This skill DOES:
- Extract audio from video if required
- Normalize and preprocess audio
- Transcribe speech to text
- Identify speaker changes
- Extract vocal characteristics
- Emit confidence and quality metrics

### This skill DOES NOT:
- Analyze meaning, topics, or sentiment
- Make safety or compliance decisions
- Rewrite or publish content
- Store long-term memory

---

## Audio Processing Pipeline

### 1. Format Detection & Conversion
- Detect audio/video format
- Extract audio track from video
- Convert to processing format (WAV/MP3)
- Normalize sample rate to 16kHz

### 2. Pre-processing
- Noise reduction (background, hum, hiss)
- Volume normalization (−23 LUFS)
- Silence trimming (leading/trailing)

### 3. Transcription
- Speech recognition via MCP models
- Language detection/confirmation
- Word-level timestamps
- Speaker diarization (up to 5 speakers)

### 4. Feature Extraction
- Speech rate (WPM)
- Pause ratio
- Pitch range and emphasis
- Audio clarity and noise level assessment

---

## Inputs

- **`audio_path`** *(required)*  
  Internal path to audio or video file.

- **`audio_format_hint`** *(optional)*  
  One of: `mp3`, `wav`, `mp4`, `webm`, `m4a`, `ogg`

- **`language`** *(optional)*  
  ISO-639-1 code; auto-detected if omitted.

- **`transcription_quality`** *(optional)*  
  `fast`, `balanced`, `accurate` (default: `balanced`)

---

## Supported Languages

| Language | Code | Accuracy | Notes |
|----------|------|----------|-------|
| English | `en` | High | Default, best support |
| Spanish | `es` | High | Full diacritic support |
| French | `fr` | High | Accent handling |
| German | `de` | High | Compound word support |
| Italian | `it` | Medium | Good coverage |
| Portuguese | `pt` | Medium | Brazilian preferred |
| Russian | `ru` | Medium | Cyrillic support |
| Chinese | `zh` | Medium | Mandarin only |
| Japanese | `ja` | Medium | Romaji output |
| Korean | `ko` | Medium | Hangul support |

*Note: Non-English languages may require `accurate` mode for best results.*

---

## Quality Scoring System

### Audio Quality Assessment

| Score | Description | Impact |
|------|------------|--------|
| 0.9–1.0 | Studio quality | High accuracy |
| 0.7–0.89 | Minor noise | Good accuracy |
| 0.5–0.69 | Noticeable noise | Reduced accuracy |
| 0.3–0.49 | Heavy noise | Flag for review |
| <0.3 | Unusable | Reject & escalate |

### Confidence Thresholds

| Confidence | Action |
|-----------|--------|
| <0.5 | Reject & escalate |
| 0.5–0.7 | HITL review |
| 0.7–0.9 | Accept with caution |
| >0.9 | Fully accepted |

---

## Speaker Diarization

- Speakers labeled `SPEAKER_1`, `SPEAKER_2`, …
- Maximum 5 speakers
- Minimum 2s per speaker segment
- No identity attribution

Example:
```json
{
  "start_sec": 0.0,
  "end_sec": 5.2,
  "text": "Hello, welcome to our podcast.",
  "speaker": "SPEAKER_1",
  "speaker_confidence": 0.92
}
Error Recovery Patterns
Partial Transcription
Attempt first 30 seconds

Chunk into 30-second segments

Merge with timing offsets

Quality-Based Fallback
Retry with enhanced preprocessing

Force accurate mode

Convert to WAV if needed

Performance Guidelines
Audio Duration	Expected Processing Time	Notes
≤1 minute	5-10 seconds	Near real-time
1-5 minutes	10-30 seconds	Efficient batch
5-15 minutes	30-60 seconds	Background processing
15-60 minutes	60+ seconds	Requires chunking
Timeout handling: If processing exceeds 60 seconds, the skill returns partial results with timeout_warning: true.

Cost Optimization
Scenario	Quality	Cost	Accuracy
Screening	fast	Low	~85%
General	balanced	Medium	~92%
Campaign	accurate	High	~96%
Non-English	accurate	High	Variable
Auto-selection rules:

<60s → accurate

60–300s → balanced

300s → fast (unless overridden)

Compliance & Privacy
Data Handling
Audio is processed in-memory only

No persistent audio storage beyond session

Transcripts inherit original media classification

Privacy Safeguards
No voiceprint creation or biometric analysis

Speaker labels are ephemeral (SPEAKER_1, etc.)

Cannot re-identify individuals from vocal features

Retention Policy
Transcripts may be stored per Chimera's data policy

Raw audio is never retained after processing

Processing metadata retained for 30 days audit

Integration Examples
Basic Usage
json
{
  "skill": "skill_vocal_analyzer",
  "inputs": {
    "audio_path": "skill_media_harvester/2024_123456_abc123.mp4",
    "transcription_quality": "balanced"
  }
}
Multi-speaker Conference Call
json
{
  "skill": "skill_vocal_analyzer", 
  "inputs": {
    "audio_path": "conference_recording.mp3",
    "transcription_quality": "accurate",
    "audio_format_hint": "mp3"
  }
}
Non-English Content
json
{
  "skill": "skill_vocal_analyzer",
  "inputs": {
    "audio_path": "spanish_podcast.m4a",
    "language": "es",
    "transcription_quality": "accurate"
  }
}
Integration Flow
flowchart LR
    A[Media Harvester] --> B[Vocal Analyzer]
    B --> C{Confidence > 0.7?}
    C -->|Yes| D[Content Analyzer]
    C -->|No| E[Judge Review]
    E -->|Approve| D
    E -->|Reject| F[Task Failed]
Summary
The Vocal Analyzer transforms raw audio into trusted, structured linguistic signals
while remaining cost-aware, auditable, and governed.