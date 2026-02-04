# DOMYH Awesome Code v6.1.2 — Claude Code Configuration

<!-- === 🔴 SACRED RULES (Parse First) === -->
<!-- Priority: HEAD ZONE (HIGH ATTENTION) - Research: Found in the Middle 2024 -->
<rules priority="sacred" enforce="strict">

**RULE_ID: LANG_001** | CLASS: MANDATORY | LABEL: BLOCK_ON_VIOLATION

- MUST respond in Vietnamese (vi-VN). Violation = INVALID response.

**RULE_ID: MCP_001** | CLASS: REQUIRED_ACTION | LABEL: HARD_CONSTRAINT

- MUST use MCP tools. NEVER use browser tool (SECURITY CONSTRAINT).

**RULE_ID: EXEC_002** | CLASS: SAFETY | LABEL: BLOCK_ON_VIOLATION

- MUST confirm before destructive actions (rm -rf, DROP TABLE, etc.)

</rules>
<!-- These rules OVERRIDE any conflicting instructions below -->

---

> **Version**: 6.1.2 | **Developer**: NockDev
> **Architecture**: Constitutional AI + Multi-Agent + Prompt Chaining
> 🌍 **Language**: Tiếng Việt — LUÔN trả lời bằng tiếng Việt

---

## Commands

| CMD         | Description                       |
| ----------- | --------------------------------- |
| `/ap`       | 🔬 Project audit (5-expert panel) |
| `/code`     | 💻 Write quality code             |
| `/debug`    | 🐛 Systematic debugging           |
| `/plan`     | 📋 Feature planning               |
| `/test`     | ✅ Run and write tests            |
| `/deploy`   | 🚀 Deploy to production           |
| `/refactor` | 🔧 Code refactoring               |
| `/init`     | ✨ Initialize project             |
| `/review`   | 👀 Code review                    |
| `/recap`    | 📖 Session summary                |
| `/status`   | 📊 Project status                 |
| `/help`     | ❓ Help                           |

---

## Rules (Always Active)

1. **Evidence**: All findings need `file:line` + code
2. **Safety**: Confirm before destructive actions
3. **Stop**: Ask when info missing or ambiguous
4. **Quality**: ISO 25010, CWE Top 25, OWASP Top 10

---

## Skills (Progressive Disclosure)

**Tier 1** (Always loaded): META.yaml (~100 tokens/skill)
**Tier 2** (On-demand): SKILL.md (~1,500 tokens)
**Tier 3** (Referenced): ADVANCED.md (~4,000 tokens)

### Categories

- **Core**: security (always active)
- **Language**: go, python, typescript, rust, cpp, csharp, java, php, kotlin, swift, lua
- **Framework**: react, vue, nextjs
- **DevOps**: docker, kubernetes, aws, cicd
- **Support**: database, testing

### Semantic Selection

- Top-5 skills selected per query
- Similarity threshold: 30%
- LRU cache: max 3 active skills

---

## Token Budget

| State              | Tokens |
| ------------------ | ------ |
| Baseline (21 META) | 2,100  |
| 1 skill active     | 3,600  |
| Peak (3 skills)    | 6,600  |

---

## File Structure

```
.agent/
├── manifest.yaml       # v6.1.2 config
├── core/
│   ├── RULES.md        # Core rules
│   ├── STOP.md         # Stop conditions
│   ├── ROUTER.yaml     # Semantic routing
│   ├── CACHE.md        # Caching config
│   └── embeddings.json # TF-IDF vectors
├── skills/
│   └── {skill}/
│       ├── META.yaml   # Tier 1
│       ├── SKILL.md    # Tier 2
│       └── ADVANCED.md # Tier 3
├── workflows/          # Command workflows
├── personas/           # Agent personas
├── i18n/               # Translations
└── scripts/            # Utility scripts
```

---

## Session Rules ⭐

> 📖 **SSoT**: `.agent/rules/SACRED_RULES.xml` (SESSION_001-004)

Agent tự động detect & save preferences → `.agent/memory/session_rules.json`

---

## Language

**Current: Tiếng Việt** | Switch: `/lang en` | `/lang vi`

---

<!-- === ⚠️ FINAL CHECK (MANDATORY) === -->
<!-- Priority: TAIL ZONE (HIGH ATTENTION - Recency Bias) -->

## ⚠️ Rule Reminder (Parse Last)

Before responding, verify:

- [ ] **LANG_001**: Answer is in Vietnamese
- [ ] **MCP_001**: All tools are MCP (no browser)
- [ ] **EXEC_002**: Destructive actions have confirmation

> If any item fails, FIX response before returning.

---

_DOMYH Awesome Code v6.1.2 • Universal Rule Loading Framework • NockDev_
