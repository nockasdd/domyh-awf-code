---
description: "✍️ AI Prompt Generator: research, analyze, and create structured markdown prompts"
skills: { required: [prompt-engineering], contextual: [domyh-design] }
success_criteria: "Prompt generated, research cited, RCTO structure applied"
---

# ✍️ /prompt — Prompt Generator Pro

> Research → Analyze → Structure → Generate → Refine
> 📚 RCTO Framework • Online Research • Multi-format Output

---

## PROMPT FLOW

1. **ANALYZE** — Parse user request, detect prompt type (image/project/modify/system/general). If project-related: load context via HSA (`hsa_search`). Extract: purpose, target tool/model, language, constraints. Show: `[Step 1/5] Analyzing: "{request}" → Type: image`
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

> **Template Reference**: Read `templates/prompts/{type}.md` for the correct RCTO template structure.
> Available templates: `image.md`, `project.md`, `modify.md`, `system.md`.

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

## REFLECTION CHECKPOINT

⛔ **MANDATORY** — Execute before completing this workflow (SESSION_005):

1. **VERIFY** — Does output meet success_criteria (see YAML frontmatter)?
2. **PERSIST** (if HSA available — preferred, 1 tool call):
   - `hsa_session({action:'persist', task_summary:'[workflow] [summary]', files_touched:[...], auto_notify:true})`
   - If key decision → `hsa_session({action:'anchor', content:'[decision]', category:'decision'})`
3. **PERSIST** (if HSA unavailable — manual fallback):
   - Append task summary to `memory/session.md`
   - If last task → Update `memory/CONTEXT_SNAPSHOT.md`

