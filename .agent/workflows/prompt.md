---
description: "✍️ AI Prompt Generator Pro: detect, interview, lazy-load, generate optimized prompts for 10+ content types"
skills: { required: [prompt-engineering], contextual: [domyh-design, gemini-media-gen] }
success_criteria: "Prompt generated, framework applied, model-optimized, ready for copy-paste"
---

# ✍️ /prompt — Prompt Generator Pro

> DETECT → INTERVIEW → LOAD → GENERATE → REFINE
> 📚 5 Frameworks • 10 Types • Lazy Loading • Token Optimized

---

## PROMPT FLOW (5 Steps)

1. **DETECT** — Parse request → auto-detect type (see AUTO-DETECT below). Auto-recommend model from `ai-models-catalog.yaml` → auto_selection. Show: `[1/5] Type: IMAGE/anime_avatar → Model: Midjourney v7`
2. **INTERVIEW** — Ask 2-3 Qs from INTERVIEW MAP below. **Skip if user already provided** (model, style, platform in desc/flags). Show: `[2/5] Quick questions...`
3. **LOAD** — Lazy load ONLY needed data per LAZY LOAD MAP below. **Never load all files.** Show: `[3/5] Loading image-types-personal...`
4. **GENERATE** — Apply framework template from loaded data. Write prompt in user's language. If `--variants` → generate N variants with different angles (see VARIANT ANGLES). If complex/niche → online research. Show: `[4/5] Generating with SVCLMA framework...`
5. **REFINE** — Present prompt → ⛔ **STOP for user review**. Iterate if needed. Optional: save to `.domyh/prompts/prompt_YYYY-MM-DD_{type}.md`

---

## COMMANDS

| Command                    | Type        | Framework  |
| -------------------------- | ----------- | ---------- |
| `/prompt [anything]`       | auto-detect | Auto       |
| `/prompt image [desc]`     | image       | RCTO+PRISM |
| `/prompt video [desc]`     | video       | SVCLMA     |
| `/prompt marketing [desc]` | marketing   | CO-STAR    |
| `/prompt email [desc]`     | email       | AIDA       |
| `/prompt social [desc]`    | social      | CO-STAR    |
| `/prompt audio [desc]`     | audio       | RCTO+Audio |
| `/prompt data [desc]`      | data        | RCTO       |
| `/prompt project [desc]`   | project     | RCTO       |
| `/prompt modify [desc]`    | modify      | RCTO       |
| `/prompt system [desc]`    | system      | RCTO       |

### Flags

| Flag | Description |
| ---- | ----------- |
| `--lang vi/en` | Output language |
| `--tool midjourney/dalle/flux/ideogram` | Image model |
| `--model sora/veo/runway/kling/hailuo` | Video model |
| `--platform instagram/youtube/linkedin/twitter/google-ads` | Platform |
| `--variants N` | N variants (default: 1) |
| `--detail minimal/standard/detailed` | Detail level |

---

## AUTO-DETECT LOGIC

```
User Input → Keyword Match:
├─ video/clip/animation/sora/veo/runway/cinematic/trailer  → VIDEO   → SVCLMA
├─ ad/campaign/copy/headline/slogan/CTA/tagline            → MARKETING → CO-STAR
├─ email/newsletter/outreach/cold email/drip/subject        → EMAIL   → AIDA
├─ tweet/post/linkedin/instagram/tiktok/thread/hashtag      → SOCIAL  → CO-STAR
├─ voice/narration/podcast/music/tts/suno/udio              → AUDIO   → RCTO+Audio
├─ analyze/chart/report/dashboard/SQL/metrics/KPI           → DATA    → RCTO
├─ image/photo/avatar/logo/banner/poster/wallpaper/midjourney → IMAGE → RCTO+PRISM
├─ project/build/website/application/startup/SaaS           → PROJECT → RCTO
├─ modify/fix/add/refactor/improve/upgrade/migrate          → MODIFY  → RCTO
├─ system prompt/persona/bot/agent/assistant/chatbot        → SYSTEM  → RCTO
└─ Default                                                  → GENERAL → RCTO
```

---

## INTERVIEW MAP (inline — flow control)

Ask 2-3 Qs per type. **Skip entirely if user provided all info.**

| Type | always_ask | ask_if_missing | skip_if |
|------|-----------|----------------|---------|
| **image** | Loại ảnh? (avatar/logo/banner/poster...) • Aspect ratio? | Model? • Style? (photorealistic/anime/minimalist) | type+style in desc, `--tool` |
| **video** | Target model? (Sora/Veo/Runway/Kling/Hailuo) • Duration? | Audio needed? • Camera movement? | `--model`, duration in desc |
| **marketing** | Platform? (Google Ads/Facebook/Instagram...) • Target audience? | Tone? • Multiple variants? | `--platform`, audience in desc |
| **email** | Type? (cold/newsletter/launch/follow-up/drip) • CTA? | Tone? | type in desc |
| **social** | Platform? (Twitter/IG/LinkedIn/TikTok) | Hashtag research? • Tone? | `--platform` |
| **audio** | Type? (music/voiceover/podcast/SFX) • Model? | Genre/mood/BPM? or Voice details? | type+model in desc |
| **data** | Analysis type? (report/dashboard/chart/SQL) • Data source? | Audience? | — |
| **system** | Agent purpose? (chatbot/assistant/analyst) • Constraints? | Tool calling? • Thinking level? | — |
| **project** | Tech stack? • Scope? (MVP/full/prototype) | — | — |
| **modify** | What to change? (feature/bugfix/refactor) • Breaking OK? | — | — |

---

## LAZY LOAD MAP (inline — flow control)

Load ONLY what's needed. `?` = optional. Data path: `prompt-engineering/data/`

| Type | Load (required) | Load (optional) | Skip |
|------|----------------|-----------------|------|
| **image** | `image-types-{sub}.yaml` | `ai-models-catalog.yaml` | prompt-frameworks |
| **video** | `ai-models-catalog.yaml` | `prompt-frameworks.yaml` | image-types |
| **marketing** | `prompt-frameworks.yaml` | — | image-types, ai-models |
| **email** | `prompt-frameworks.yaml` | — | image-types, ai-models |
| **social** | `prompt-frameworks.yaml` | — | image-types, ai-models |
| **audio** | `ai-models-catalog.yaml` | — | image-types, prompt-frameworks |
| **data** | — | `reasoning-patterns.yaml` | image-types, ai-models |
| **system** | `gemini3-patterns.yaml` | `safety-patterns.yaml` | image-types, ai-models |
| **project** | — | `reasoning-patterns.yaml` | all data files |
| **modify** | — | `reasoning-patterns.yaml` | all data files |

### Image Sub-file Routing

```
avatar/pet/wallpaper/sticker/emoji/meme/profile  → image-types-personal.yaml
logo/banner/poster/mockup/thumbnail/card/slides   → image-types-business.yaml
concept/illustration/pattern/album/game/book       → image-types-creative.yaml
ad/hero/email-header/social-post/testimonial       → image-types-marketing.yaml
food/architecture/fashion/landscape/street/macro   → image-types-photography.yaml
```

---

## VARIANT ANGLES

When `--variants N`, use distinct angles:

| Angle | Strategy |
|-------|----------|
| **Direct** | Clear, benefit-focused, no metaphor |
| **Emotional** | Story-driven, pain/aspiration hook |
| **Data-driven** | Statistics, social proof, numbers |
| **Urgency** | Scarcity, time-limit, FOMO |
| **Curiosity** | Question hook, cliffhanger |

---

## FRAMEWORK SELECTION

| Framework | Best For | Loaded From |
|-----------|----------|-------------|
| **RCTO** | System, project, modify, code, general | `prompt-frameworks.yaml` |
| **CO-STAR** | Marketing, social, copywriting | `prompt-frameworks.yaml` |
| **SVCLMA** | Video generation | `prompt-frameworks.yaml` |
| **AIDA** | Email, sales copy | `prompt-frameworks.yaml` |
| **PAS** | Ads, landing pages | `prompt-frameworks.yaml` |

---

## RESEARCH RULES

```yaml
always_research: "Model syntax updates, niche domains (medical/legal), platform policy changes"
skip_research:   "Simple image prompts, standard marketing copy, common system prompts"
conditional:     "Video/audio → only if specific model or niche technique"
```

---

## QUALITY CRITERIA

| Criteria | Description |
| -------- | ----------- |
| **Specific** | No ambiguity, concrete details |
| **Structured** | Framework sections clearly separated |
| **Actionable** | Copy-paste ready for target tool |
| **Complete** | All context present, no [PLACEHOLDER] |
| **Optimized** | Model-specific syntax (--ar, --no, etc.) |

---

## ANTI-PATTERNS

| Don't | Do Instead |
| ----- | ---------- |
| Load all data files upfront | Lazy load per LAZY LOAD MAP |
| Skip interview | Ask Qs if info missing |
| Same variant, different words | Each variant: distinct angle |
| Mix camera directions in 1 shot | One camera per video segment |
| Ignore platform char limits | Check platform_constraints |
| Always force online research | Skip for simple types |
| Generic model recommendation | Use auto_selection from catalog |

---

## INTEGRATION

### Data Files (in `prompt-engineering/data/`)
- `ai-models-catalog.yaml` → 14 models, camera vocab, auto-selection, negative prompts
- `image-types-{personal,business,creative,marketing,photography}.yaml` → 5 sub-catalogs
- `prompt-frameworks.yaml` → 5 framework templates + 8 platform constraints

### Contextual Skills
- `domyh-design` → style/color data for image/UI prompts
- `gemini-media-gen` → Gemini-specific patterns
- `gemini3-patterns.yaml` → agentic templates for system prompts

---

## REFLECTION CHECKPOINT

⛔ **MANDATORY** — Execute before completing (SESSION_005):

1. **VERIFY** — Output meets success_criteria?
2. **PERSIST** (HSA):
   - `hsa_session({action:'persist', task_summary:'[workflow] [summary]', files_touched:[...]})`
   - If key decision → `hsa_session({action:'anchor', content:'[decision]', category:'decision'})`
3. **PERSIST** (manual fallback):
   - Append to `memory/session.md` → Update `memory/CONTEXT_SNAPSHOT.md`
