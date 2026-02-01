# GEMINI.md — DOMYH Awesome Code v4.3

> 🎯 **Purpose**: AI-powered development assistant
> 👨‍💻 **Developer**: NockDev
> 🏗️ **Architecture**: Progressive Disclosure + Semantic Selection
> 🌍 **Language**: Tiếng Việt (Vietnamese) — LUÔN trả lời bằng tiếng Việt

---

## Commands

| Command     | Description                            |
| ----------- | -------------------------------------- |
| `/ap`       | 🔬 Full project audit (5-expert panel) |
| `/code`     | 💻 Write quality code                  |
| `/debug`    | 🐛 Systematic debugging                |
| `/plan`     | 📋 Feature planning                    |
| `/test`     | ✅ Run and write tests                 |
| `/deploy`   | 🚀 Deploy to production                |
| `/refactor` | 🔧 Code refactoring                    |
| `/init`     | ✨ Initialize project                  |
| `/review`   | 👀 Code review                         |
| `/recap`    | 📖 Session summary                     |
| `/save`     | 💾 Save session to memory files        |
| `/status`   | 📊 Project status                      |
| `/help`     | ❓ Help                                |

---

## Rules

1. **Evidence** — All findings need `file:line` + code snippet
2. **Safety** — No destructive actions without confirmation
3. **Stop** — Ask when info missing or ambiguous

---

## Skills (Progressive Disclosure)

| Tier | File        | Tokens | When            |
| ---- | ----------- | ------ | --------------- |
| T1   | META.yaml   | ~100   | Always loaded   |
| T2   | SKILL.md    | ~1,500 | On-demand       |
| T3   | ADVANCED.md | ~4,000 | Referenced only |

**Semantic Selection**: Top-5 skills per query, 30% similarity threshold

---

## Token Budget

- **Baseline**: 2,100 tokens (21 × META.yaml)
- **Single skill**: +1,500 tokens
- **Peak (3 skills)**: 6,600 tokens total

---

## Language

**Current: Tiếng Việt** | Switch: `/lang en` | `/lang vi`

> Configuration: `.agent/memory/state.json` → `preferences.language`

---

_DOMYH Awesome Code v4.3 • NockDev_
