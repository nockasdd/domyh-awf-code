---
description: "✍️ AI Prompt Generator: research, analyze, and create structured markdown prompts"
skills: { required: [prompt-engineering], contextual: [domyh-design] }
---

# ✍️ /prompt — Prompt Generator Pro

> Research → Analyze → Structure → Generate → Refine
> 📚 RCTO Framework • Online Research • Multi-format Output

---

## PROMPT FLOW

1. **ANALYZE** — Parse user request, detect prompt type (image/project/modify/system/general). Extract: mục đích, target tool/model, ngôn ngữ, constraints. Show: `[Step 1/5] Analyzing: "{request}" → Type: image`
2. **RESEARCH** — Online research về domain, best practices, reference examples. Tìm kiếm: cấu trúc prompt tối ưu cho target tool, industry standards, trending patterns. Show: `[Step 2/5] Researching: "midjourney v6 architecture prompts"...`
3. **STRUCTURE** — Apply RCTO Framework (Role-Context-Task-Output). Map research → sections phù hợp. Choose template theo prompt type. Show: `[Step 3/5] Structuring prompt with 6 sections...`
4. **GENERATE** — Tạo structured markdown prompt. Viết bằng ngôn ngữ người dùng yêu cầu. Apply prompt-engineering patterns (CoT, few-shot, role-play). Show: `[Step 4/5] Generating prompt...`
5. **REFINE** — Present output → ⛔ **STOP — user review**. Iterate nếu cần: thêm chi tiết, đổi style, adjust parameters.

---

## COMMANDS

| Command                  | Loại        | Mô tả                     | Output              |
| ------------------------ | ----------- | ------------------------- | ------------------- |
| `/prompt [anything]`     | auto-detect | Tự phân tích và chọn loại | Markdown prompt     |
| `/prompt image [desc]`   | image       | Prompt tạo ảnh AI         | Image gen prompt    |
| `/prompt project [desc]` | project     | Prompt tạo dự án mới      | Project spec prompt |
| `/prompt modify [desc]`  | modify      | Prompt chỉnh sửa dự án    | Modification prompt |
| `/prompt system [desc]`  | system      | System prompt cho AI      | System prompt       |

### Flags

| Flag                                      | Mô tả                                    |
| ----------------------------------------- | ---------------------------------------- |
| `--lang vi/en`                            | Ngôn ngữ output (default: ngôn ngữ user) |
| `--tool midjourney/dalle/flux/claude/gpt` | Target AI tool                           |
| `--detail minimal/standard/detailed`      | Mức chi tiết (default: detailed)         |
| `--format markdown/yaml/json`             | Output format (default: markdown)        |

---

## RCTO FRAMEWORK

Mọi prompt đều follow cấu trúc RCTO:

```
┌─────────────────────────────────────────┐
│  R — ROLE                               │
│  Ai sẽ thực hiện? Persona, expertise    │
├─────────────────────────────────────────┤
│  C — CONTEXT                            │
│  Background, constraints, domain info   │
├─────────────────────────────────────────┤
│  T — TASK                               │
│  Yêu cầu cụ thể, step-by-step          │
├─────────────────────────────────────────┤
│  O — OUTPUT                             │
│  Format, structure, quality criteria    │
└─────────────────────────────────────────┘
```

---

## PROMPT TYPE TEMPLATES

### 1. Image Prompt Template

```markdown
# 🖼️ [Title]

## Target

- **Model**: [Midjourney v6 / DALL-E 3 / Flux Pro / Stable Diffusion XL]
- **Aspect Ratio**: [16:9 / 1:1 / 9:16 / 3:2]
- **Quality**: [Standard / HD / Ultra]

## Main Prompt

[Subject] in [style]. [Composition] with [lighting].
[Color palette]. [Atmosphere/mood]. [Details and textures].
[Camera angle/lens if photographic].

## Style References

- Art style: [e.g., digital art, oil painting, cinematic]
- Influences: [e.g., Studio Ghibli, Wes Anderson, cyberpunk]

## Negative Prompt

[Elements to avoid — blurry, deformed, text artifacts, etc.]

## Variations

1. **[Variant A]** — [Different style/mood/angle]
2. **[Variant B]** — [Different color/lighting/composition]
3. **[Variant C]** — [Different detail level/abstraction]

## Parameters

[Tool-specific parameters: --ar, --v, --s, --q, etc.]
```

### 2. Project Prompt Template

```markdown
# 🏗️ [Project Name]

## Context

- **Mục đích**: [Why this project exists]
- **Target users**: [Who will use it]
- **Domain**: [Industry/area]

## Requirements

### Functional (P0 — Must Have)

1. [Feature — detailed description, acceptance criteria]
2. [Feature — detailed description, acceptance criteria]

### Functional (P1 — Should Have)

1. [Feature — description]

### Non-Functional

- **Performance**: [Response time, throughput targets]
- **Security**: [Auth, data protection requirements]
- **Scalability**: [Expected load, growth projections]
- **Accessibility**: [WCAG level, platforms]

## Recommended Tech Stack

| Layer    | Technology | Reasoning |
| -------- | ---------- | --------- |
| Frontend | [choice]   | [why]     |
| Backend  | [choice]   | [why]     |
| Database | [choice]   | [why]     |

## Architecture Overview

[High-level architecture description / diagram]

## Implementation Phases

1. **Phase 1** (MVP): [scope, timeline estimate]
2. **Phase 2** (v1.0): [scope, timeline estimate]
3. **Phase 3** (v2.0): [scope, timeline estimate]
```

### 3. Modification Prompt Template

```markdown
# 🔧 [Modification Title]

## Current State

- **Project**: [name, tech stack]
- **What exists**: [current functionality]
- **Problem**: [why modification is needed]

## Desired Changes

1. [Change 1 — specific, measurable]
2. [Change 2 — specific, measurable]

## Constraints

- **Must preserve**: [existing functionality not to break]
- **Compatibility**: [versions, APIs, integrations]
- **Timeline**: [urgency level]

## Implementation Guide

### Files to Modify

- `[file]` — [what to change, why]

### New Files

- `[file]` — [purpose, contents]

### Testing Requirements

- [ ] [Test case 1]
- [ ] [Test case 2]

## Rollback Plan

[How to revert if something goes wrong]
```

### 4. System Prompt Template

```markdown
# 🤖 [System Name] — System Prompt

## Identity

- **Role**: [Specific persona with expertise]
- **Name**: [Optional persona name]
- **Tone**: [Professional / Friendly / Expert / etc.]

## Core Instructions

1. [Primary behavior rule]
2. [Response format rule]
3. [Knowledge boundary rule]

## Capabilities

- ✅ [Can do 1]
- ✅ [Can do 2]
- ❌ [Cannot/should not do 1]
- ❌ [Cannot/should not do 2]

## Response Format

[Structured output requirements — JSON schema, markdown sections, etc.]

## Examples

### User Input

> [example input]

### Expected Output

> [example output with correct format]

## Safety Rules

- [Guardrail 1 — what to refuse]
- [Guardrail 2 — what to escalate]
```

---

## AUTO-DETECT LOGIC

```
User Input → Keyword Analysis:
│
├─ Contains: "ảnh", "image", "hình", "photo", "illustration",
│  "midjourney", "dall-e", "flux", "wallpaper", "poster"
│  → Type: IMAGE
│
├─ Contains: "dự án", "project", "tạo app", "build", "website",
│  "application", "startup", "SaaS", "platform"
│  → Type: PROJECT
│
├─ Contains: "sửa", "modify", "fix", "thêm", "add", "change",
│  "refactor", "improve", "upgrade", "migrate"
│  → Type: MODIFY
│
├─ Contains: "system prompt", "persona", "bot", "agent",
│  "assistant", "chatbot", "instruction"
│  → Type: SYSTEM
│
└─ Default → Type: GENERAL (apply RCTO)
```

---

## RESEARCH STRATEGY

Trước khi tạo prompt, agent PHẢI research online:

| Prompt Type | Research Targets                                                  |
| ----------- | ----------------------------------------------------------------- |
| Image       | Tool-specific syntax, trending styles, composition techniques     |
| Project     | Industry best practices, similar projects, tech stack comparisons |
| Modify      | Framework docs, migration guides, breaking changes                |
| System      | Latest prompting patterns, model capabilities, safety guidelines  |

### Research Quality Gates

- ✅ Ít nhất 2-3 sources đáng tin cậy
- ✅ Cross-reference thông tin giữa sources
- ✅ Ưu tiên official docs và recent articles (< 6 tháng)
- ✅ Ghi citation vào phần "References" của output

---

## QUALITY CRITERIA

Mọi prompt generated phải đạt:

| Criteria       | Description                                |
| -------------- | ------------------------------------------ |
| **Specific**   | Không mơ hồ, có chi tiết cụ thể            |
| **Structured** | Sections rõ ràng, hierarchy tốt            |
| **Actionable** | Có thể copy-paste trực tiếp vào tool       |
| **Complete**   | Đủ context, không thiếu thông tin critical |
| **Tested**     | Format đúng cho target tool                |

---

## INTEGRATION

### Với prompt-engineering skill

- Load reasoning patterns từ `reasoning-patterns.yaml`
- Apply output formatting từ `output-patterns.yaml`
- Check safety guardrails từ `safety-patterns.yaml`

### Với domyh-design skill (contextual)

- Load style/color data cho image prompts
- Apply typography/layout knowledge cho UI prompts
- Use image-gen-prompts.yaml templates khi relevant

---

## ⚠️ ANTI-PATTERNS

| Don't                               | Do Instead                                |
| ----------------------------------- | ----------------------------------------- |
| Prompt quá ngắn, thiếu context      | Luôn include đủ RCTO sections             |
| Copy-paste template không customize | Customize mọi section cho use case cụ thể |
| Skip research                       | Luôn research trước khi generate          |
| Ngôn ngữ lẫn lộn                    | Giữ consistent 1 ngôn ngữ throughout      |
| Quá nhiều jargon                    | Viết clear cho target audience            |
