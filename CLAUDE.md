# DOMYH Agent v4.3 — Claude Code Configuration

> **Version**: 4.3.0 | **Developer**: NockDev
> **Architecture**: Progressive Disclosure + Semantic Selection

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
├── manifest.yaml       # v4.0 config
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

## Language

Default: English | Switch: `/lang vi`

---

_DOMYH Agent v4.3 • Progressive Disclosure Architecture_
