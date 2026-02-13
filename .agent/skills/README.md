# 📁 Skills — DOMYH Awesome Code

> Tech-specific patterns loaded via Progressive Disclosure

---

## Quick Reference

| Metric          | Value                 |
| --------------- | --------------------- |
| Total Skills    | 82                    |
| Total META Size | ~17KB                 |
| Avg per skill   | ~300 bytes (~100 tok) |
| Max detected    | 5 META.yaml           |
| Max active T2   | 3 SKILL.md            |

---

## Categories

| Category               | Skills                                                                                                | Priority   |
| ---------------------- | ----------------------------------------------------------------------------------------------------- | ---------- |
| **Core** (6)           | security, api-design, error-handling, logging, observability, authentication                          | 0 (always) |
| **Language** (28)      | go, python, typescript, javascript, rust, cpp, c, csharp, java, php, kotlin, swift, lua, asm, ...     | 1          |
| **Framework** (8)      | react, vue, nextjs, nuxt, angular, svelte, flutter, react-native                                      | 2          |
| **DevOps** (7)         | docker, kubernetes, aws, ci-cd, terraform, gcp, azure                                                 | 3          |
| **Cross-cutting** (21) | testing, database, sql, tailwind, electron, coding-rules, domyh-design, web-perf, playwright, ...     | 4          |
| **Tooling** (5)        | mcp, api-protocols, ide-extension, cli-dev, browser-agent                                             | 5          |
| **AI-ML** (7)          | ai-agents, prompt-engineering, rag-patterns, vector-search, gemini-media-gen, gemini-tts, gemini-live | 6          |

---

## 3-Tier Progressive Disclosure

| Tier | File        | Tokens | When       |
| ---- | ----------- | ------ | ---------- |
| T1   | META.yaml   | ~100   | Always     |
| T2   | SKILL.md    | ~1,500 | On-demand  |
| T3   | ADVANCED.md | ~4,000 | Referenced |

---

## META.yaml Schema (v6.2.5)

```yaml
name: skill-id          # lowercase, hyphen-separated
display: Display Name   # Human-readable
category: language      # core|language|framework|devops|cross-cutting|tooling|ai-ml
priority: 1             # 0-6 (lower = higher)
desc: "Short desc"      # Max 80 chars
keywords: [kw1, kw2]    # Max 5-7 keywords
detect: [*.ext, file]   # File patterns
caps: [cap1, cap2]      # Max 3 capabilities
```

**Target:** ≤400 bytes per META.yaml

---

## Skill Detection Flow

```
1. Scan project files
2. Match against detect patterns
3. Calculate TF-IDF similarity
4. Load Top-5 matching skills
5. Apply LRU cache (max 3)
```

---

_DOMYH Awesome Code _
