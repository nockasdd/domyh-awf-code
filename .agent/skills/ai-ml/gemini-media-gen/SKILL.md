---
name: gemini-media-gen
version: "6.3.1"
category: ai-ml
---

# Gemini Media Generation

> 🎨 **Native image + video generation via Gemini API**
> **Models**: Nano Banana (Flash/Pro) + Veo 3.1 | **Patterns**: 36+

---

## Quick Reference

| What You Need                | Data File               | Patterns |
| ---------------------------- | ----------------------- | -------- |
| Model selection & configs    | `image-models.yaml`     | 8        |
| Image prompt optimization    | `image-prompts.yaml`    | 12       |
| Video generation & prompting | `video-generation.yaml` | 10       |
| Files API management         | `files-api.yaml`        | 6        |

---

## Model Selection Guide

| Feature              | Nano Banana Flash                           | Nano Banana Pro                           |
| -------------------- | ------------------------------------------- | ----------------------------------------- |
| **Speed**            | ⚡ Fast                                     | 🐢 Slower                                 |
| **Max resolution**   | 1024×1024                                   | **4K (4096×4096)**                        |
| **Reference images** | Up to 5                                     | **Up to 14**                              |
| **Thinking**         | ❌                                          | ✅                                        |
| **Search grounding** | ❌                                          | ✅                                        |
| **Text rendering**   | Basic                                       | **Enhanced**                              |
| **SynthID**          | ✅ (watermark)                              | ✅                                        |
| **Model ID**         | `gemini-2.0-flash-preview-image-generation` | `gemini-2.5-pro-preview-image-generation` |

**Decision**: Use Flash for speed/prototyping, Pro for quality/production.

---

## Image Generation Rules

1. **Describe the scene** — Don't list keywords
   - ✅ "A golden retriever playing fetch on a sandy beach at sunset, waves crashing in the background"
   - ❌ "golden retriever, beach, sunset, waves, fetch, sand"

2. **Aspect Ratios**: `1:1` (default), `16:9` (landscape), `9:16` (portrait), `4:3`, `3:4`

3. **Safety**: All images include invisible SynthID watermark. Safety filters block harmful/CSAM content.

4. **Text in images**: Wrap desired text in quotes — `'Sale 50% Off'`

5. **Vietnamese support**: Gemini supports Vietnamese text in prompts natively

---

## Reference Image Strategies

| Strategy                  | Max Refs          | Use Case                                        |
| ------------------------- | ----------------- | ----------------------------------------------- |
| **Style transfer**        | 1-3               | Apply reference art style to new content        |
| **Subject reference**     | 1                 | Keep consistent character/product across images |
| **Multi-ref composition** | Up to 14 (Pro)    | Combine elements from multiple references       |
| **Inpainting**            | 1 (mask required) | Edit specific regions of existing image         |

---

## Veo 3.1 Video Generation

| Parameter           | Option          | Description                           |
| ------------------- | --------------- | ------------------------------------- |
| **Duration**        | 5-8 seconds     | Fixed short clips                     |
| **Resolution**      | 720p, 1080p, 4K | Output quality                        |
| **Audio**           | Native          | AI-generated sound effects & dialogue |
| **Input**           | Text or Image   | Text-to-video or image-to-video       |
| **Negative prompt** | Yes             | "Don't include X in the video"        |

### Video Prompt Elements

```
Subject: [who/what is in the scene]
Action: [what is happening]
Style: [cinematic, documentary, anime, etc.]
Camera: [pan left, zoom in, tracking shot, etc.]
Audio: [ambient sounds, dialogue, music style]
Lighting: [golden hour, neon, soft diffused, etc.]
```

### Video Extension

Feed last frame of generated video to extend the scene for another 5-8 seconds.

### Frame Control

Use reference image as first/last frame to control video composition.

---

## Files API Quick Reference

| Feature             | Value                            |
| ------------------- | -------------------------------- |
| **Storage**         | 20GB per project                 |
| **Per-file max**    | 2GB                              |
| **Retention**       | 48 hours                         |
| **Cost**            | Free                             |
| **Supported types** | Images, video, audio, PDFs, text |

```python
# Upload
file = client.files.upload(file="large_video.mp4")

# Check status (for video processing)
while file.state == "PROCESSING":
    file = client.files.get(name=file.name)

# Use in generation
response = model.generate_content([file, "Describe this video"])

# Delete
client.files.delete(name=file.name)
```

---

## HSA Integration

| Domain | Query Examples                          |
| ------ | --------------------------------------- |
| Image  | "nano banana 4K pro reference images"   |
| Video  | "veo 3.1 camera movement prompt"        |
| Files  | "files API upload video processing"     |
| Prompt | "image generation describe scene style" |
