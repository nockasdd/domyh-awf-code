---
description: "✍️ AI Prompt Generator: research, analyze, and create structured markdown prompts"
skills: { required: [prompt-engineering], contextual: [domyh-design] }
---

# ✍️ /prompt — Prompt Generator Pro

> Research → Analyze → Structure → Generate → Refine
> 📚 RCTO Framework • Online Research • Multi-format Output

---

## PROMPT FLOW

1. **ANALYZE** — Parse user request, detect prompt type (image/project/modify/system/general). If project-related: load context via HSA (`hsa_get_context`). Extract: purpose, target tool/model, language, constraints. Show: `[Step 1/5] Analyzing: "{request}" → Type: image`
2. **RESEARCH** — Online research on domain, best practices, reference examples. Search: optimal prompt structure for target tool, industry standards, trending patterns. Show: `[Step 2/5] Researching: "midjourney v6 architecture prompts"...`
3. **STRUCTURE** — Apply RCTO Framework (Role-Context-Task-Output). Map research → appropriate sections. Choose template by prompt type. Show: `[Step 3/5] Structuring prompt with 6 sections...`
4. **GENERATE** — Create structured markdown prompt. Write in the language requested by user. Apply prompt-engineering patterns (CoT, few-shot, role-play). Show: `[Step 4/5] Generating prompt...`
5. **REFINE** — Present output → ⛔ **STOP — user review**. Iterate if needed: add details, change style, adjust parameters.
6. **SAVE** (Optional) — If user confirms, save to `.domyh/prompts/prompt_YYYY-MM-DD_{type}.md`

---

## COMMANDS

| Command                  | Type        | Description                      | Output              |
| ------------------------ | ----------- | -------------------------------- | ------------------- |
| `/prompt [anything]`     | auto-detect | Auto-analyze and select type     | Markdown prompt     |
| `/prompt image [desc]`   | image       | AI image generation prompt       | Image gen prompt    |
| `/prompt project [desc]` | project     | New project specification prompt | Project spec prompt |
| `/prompt modify [desc]`  | modify      | Project modification prompt      | Modification prompt |
| `/prompt system [desc]`  | system      | System prompt for AI             | System prompt       |

### Flags

| Flag                                      | Description                         |
| ----------------------------------------- | ----------------------------------- |
| `--lang vi/en`                            | Output language (default: user lang)|
| `--tool midjourney/dalle/flux/claude/gpt` | Target AI tool                      |
| `--detail minimal/standard/detailed`      | Detail level (default: detailed)    |
| `--format markdown/yaml/json`             | Output format (default: markdown)   |

---

## RCTO FRAMEWORK

All prompts follow the RCTO structure:

```
┌─────────────────────────────────────────┐
│  R — ROLE                               │
│  Who will execute? Persona, expertise   │
├─────────────────────────────────────────┤
│  C — CONTEXT                            │
│  Background, constraints, domain info   │
├─────────────────────────────────────────┤
│  T — TASK                               │
│  Specific requirements, step-by-step    │
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

- **Purpose**: [Why this project exists]
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
├─ Contains: "image", "photo", "illustration",
│  "midjourney", "dall-e", "flux", "wallpaper", "poster"
│  → Type: IMAGE
│
├─ Contains: "project", "build", "website",
│  "application", "startup", "SaaS", "platform"
│  → Type: PROJECT
│
├─ Contains: "modify", "fix", "add", "change",
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

Before generating a prompt, agent MUST research online:

| Prompt Type | Research Targets                                                  |
| ----------- | ----------------------------------------------------------------- |
| Image       | Tool-specific syntax, trending styles, composition techniques     |
| Project     | Industry best practices, similar projects, tech stack comparisons |
| Modify      | Framework docs, migration guides, breaking changes                |
| System      | Latest prompting patterns, model capabilities, safety guidelines  |

### Research Quality Gates

- ✅ At least 2-3 trustworthy sources
- ✅ Cross-reference information across sources
- ✅ Prioritize official docs and recent articles (< 6 months)
- ✅ Include citations in the "References" section of output

---

## QUALITY CRITERIA

All generated prompts must meet:

| Criteria       | Description                                     |
| -------------- | ----------------------------------------------- |
| **Specific**   | No ambiguity, includes concrete details         |
| **Structured** | Clear sections, good hierarchy                  |
| **Actionable** | Can be copy-pasted directly into the target tool|
| **Complete**   | Sufficient context, no missing critical info    |
| **Tested**     | Format validated for target tool                |

---

## INTEGRATION

### With prompt-engineering skill

- Load reasoning patterns from `reasoning-patterns.yaml`
- Apply output formatting from `output-patterns.yaml`
- Check safety guardrails from `safety-patterns.yaml`

### With domyh-design skill (contextual)

- Load style/color data for image prompts
- Apply typography/layout knowledge for UI prompts
- Use image-gen-prompts.yaml templates when relevant

---

## ⚠️ ANTI-PATTERNS

| Don't                               | Do Instead                                |
| ----------------------------------- | ----------------------------------------- |
| Prompt too short, missing context   | Always include all RCTO sections          |
| Copy-paste template without custom  | Customize every section for the use case  |
| Skip research                       | Always research before generating         |
| Mixed languages                     | Keep consistent 1 language throughout     |
| Too much jargon                     | Write clearly for target audience         |
---

## SESSION SAVE

After completing this workflow:
1. Update `memory/CONTEXT_SNAPSHOT.md` - what changed, current status
2. Append summary to `memory/session.md`
