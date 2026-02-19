---
name: gemini-tts
version: "7.0.0"
category: ai-ml
---

# Gemini Text-to-Speech

> 🎙️ **Prompt-steerable speech synthesis**
> **Models**: Flash / Lite / Pro | **Markup tags**: 4 modes | **Patterns**: 29+

---

## Quick Reference

| What You Need              | Data File                 | Patterns |
| -------------------------- | ------------------------- | -------- |
| Model comparison & configs | `models.yaml`             | 6        |
| Markup tags reference      | `markup-tags.yaml`        | 15       |
| Style prompting            | `prompting-patterns.yaml` | 8        |

---

## 3 Levers of Speech Control

```
┌──────────────────────────────────────┐
│  1. Prompt Style Instructions        │  ← Natural language direction
│  2. Markup Tags in Text              │  ← Fine-grained control
│  3. Model Selection                  │  ← Quality vs latency
└──────────────────────────────────────┘
```

---

## Model Comparison

| Feature           | Flash     | Lite           | Pro                 |
| ----------------- | --------- | -------------- | ------------------- |
| **Latency**       | ⚡ Lowest | ⚡ Low         | 🐢 Higher           |
| **Quality**       | Good      | Good           | **Best**            |
| **Cost**          | Low       | **Lowest**     | Higher              |
| **Streaming**     | ✅        | ✅             | ✅                  |
| **Multi-speaker** | ✅        | ✅             | ✅                  |
| **Best for**      | Real-time | Cost-effective | Audiobooks, premium |

---

## Markup Tags (4 Modes)

### Non-speech sounds

```
[laughing] I can't believe that happened!
[sigh] It's been a long day.
[gasp] Really?!
[clears throat] Let me start over.
```

### Speaking style

```
[whispering] This is a secret
[sarcasm] Oh, what a great idea
[cheerfully] Welcome to the show!
[sadly] I'm sorry to hear that
```

### Vocalized sounds

```
[singing] La la la...
[humming] Hmm hmm hmm
```

### Pacing & pronunciation

```
[extremely fast] Breaking news just in!
[slowly] Let me explain this carefully
[pause: 2s] ...and then it happened
```

---

## Multi-Speaker Setup

```python
config = {
    "speech_config": {
        "multi_speaker_voice_config": {
            "speaker_voice_configs": [
                {"speaker": "Alice", "voice_config": {"prebuilt_voice_config": {"voice_name": "Kore"}}},
                {"speaker": "Bob", "voice_config": {"prebuilt_voice_config": {"voice_name": "Puck"}}}
            ]
        }
    }
}
```

Format text with speaker tags:

```
Alice: Welcome to the podcast!
Bob: Thanks for having me.
Alice: [cheerfully] Let's get started!
```

---

## Output Formats

| Format          | MIME Type               | Use Case                 |
| --------------- | ----------------------- | ------------------------ |
| WAV (PCM 24kHz) | `audio/wav`             | High quality, editing    |
| OGG Opus        | `audio/ogg;codecs=opus` | Streaming, low bandwidth |
| MP3             | `audio/mp3`             | Universal compatibility  |
| FLAC            | `audio/flac`            | Lossless archival        |
| AAC             | `audio/aac`             | Mobile playback          |
| PCM Raw         | `audio/L16;rate=24000`  | Real-time processing     |

---

## HSA Integration

| Domain | Query Examples                           |
| ------ | ---------------------------------------- |
| Models | "TTS model comparison latency quality"   |
| Markup | "speech markup whispering laughing sigh" |
| Style  | "energetic narration podcast voiceover"  |
