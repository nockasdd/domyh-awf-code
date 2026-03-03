---
name: gemini-live
description: "Gemini Live API patterns for real-time multimodal AI. Use when implementing live audio/video AI interactions."
category: ai-ml
---

# Gemini Live & Advanced APIs

> 🔴 **Real-time streaming + Advanced Gemini capabilities**
> **APIs**: Live API + Context Caching + Code Execution + Grounding | **Patterns**: 28+

---

## Quick Reference

| What You Need                  | Data File              | Patterns |
| ------------------------------ | ---------------------- | -------- |
| Live API (WebSocket streaming) | `live-api.yaml`        | 8        |
| Context Caching                | `context-caching.yaml` | 6        |
| Code Execution (sandbox)       | `code-execution.yaml`  | 8        |
| Grounding with Google Search   | `grounding.yaml`       | 6        |

---

## Live API Overview

```

> Client (Audio/Video/Text)
> ↓ WebSocket
> Gemini Live API
> ↓ Real-time processing
> Response (Audio/Text)
> + Voice Activity Detection
> + Tool calling
> + Session management
```

### Implementation Approaches

| Approach             | Description                  | Use Case                      |
| -------------------- | ---------------------------- | ----------------------------- |
| **Server-to-server** | Backend connects to Live API | Secure, full control          |
| **Client-to-server** | Frontend connects directly   | Low latency, ephemeral tokens |

### Partner Integrations

| Partner                        | Description                       |
| ------------------------------ | --------------------------------- |
| **Pipecat** (Daily)            | Real-time AI chatbot framework    |
| **LiveKit**                    | Agents with Gemini Live           |
| **Fishjam** (Software Mansion) | Live video/audio streaming        |
| **ADK** (Google)               | Agent Development Kit             |
| **Vision Agents** (Stream)     | Real-time voice/video AI          |
| **Voximplant**                 | Inbound/outbound call integration |

---

## Context Caching

| Type         | Description                   | Cost                |
| ------------ | ----------------------------- | ------------------- |
| **Implicit** | Auto-enabled, no code changes | Free (auto savings) |
| **Explicit** | Manual cache with TTL control | Reduced input cost  |

### When to Use Explicit Caching

- Chatbots with extensive system instructions
- Repetitive analysis of lengthy video files
- Recurring queries against large document sets
- Frequent code repository analysis

### Implicit Caching Tips

- Put large, common content at beginning of prompt
- Send similar-prefix requests close together in time
- Check `usage_metadata.cached_content_token_count`

---

## Code Execution

**Python sandbox with 30+ libraries** — model writes, runs, and iterates on code.

### Key Libraries Available

| Category          | Libraries                                   |
| ----------------- | ------------------------------------------- |
| **Data Science**  | numpy, pandas, scipy, scikit-learn          |
| **Visualization** | matplotlib, seaborn                         |
| **Image**         | pillow, opencv-python, imageio              |
| **Documents**     | PyPDF2, python-docx, python-pptx, reportlab |
| **ML**            | tensorflow                                  |
| **Math**          | sympy, mpmath                               |

### Gemini 3 — Code Execution with Images

New in Gemini 3: model can manipulate and inspect images via code:

- **Zoom and inspect**: Auto-crops to examine small details
- **Visual math**: Multi-step calculations from image data
- **Image annotation**: Draws arrows and labels on images

### Billing

- No extra charge for code execution
- Billed at standard input/output token rates
- Generated code + results count as output tokens

---

## Grounding with Google Search

```
User Prompt → Model → Google Search → Synthesized Response + Citations
```

### Response Structure

```json
{
  "groundingMetadata": {
    "webSearchQueries": ["search terms used"],
    "groundingChunks": [{ "web": { "uri": "...", "title": "..." } }],
    "groundingSupports": [
      { "segment": { "text": "claim..." }, "groundingChunkIndices": [0, 1] }
    ]
  }
}
```

### Building Citations

- `groundingChunks` → source URLs and titles
- `groundingSupports` → maps text segments to sources
- `searchEntryPoint` → HTML/CSS for search widget (required by ToS)

---

## Multi-Tool Combinations

| Combo              | Use Case                        |
| ------------------ | ------------------------------- |
| Search + Functions | Real-time data + custom actions |
| Code + Functions   | Compute + external data         |
| Search + Code      | Research + data analysis        |
| All + MCP          | Complex agentic workflows       |

Live API supports ALL tool combinations simultaneously.

---

## HSA Integration

| Domain | Query Examples                               |
| ------ | -------------------------------------------- |
| Live   | "WebSocket streaming real-time audio VAD"    |
| Cache  | "context caching TTL cost savings implicit"  |
| Code   | "sandbox Python execution tensorflow pandas" |
| Ground | "Google Search grounding citations metadata" |
