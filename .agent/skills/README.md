# 📁 Skills — DOMYH Awesome Code v4.3

> Tech-specific patterns loaded via Progressive Disclosure

---

## Quick Reference

| Metric          | Value                  |
| --------------- | ---------------------- |
| Total Skills    | 22                     |
| Total META Size | 7.2KB                  |
| Avg per skill   | 329 bytes (~82 tokens) |
| Max active      | 3 skills               |

---

## Categories

| Category      | Skills                                                                        | Priority   |
| ------------- | ----------------------------------------------------------------------------- | ---------- |
| **Core**      | security                                                                      | 0 (always) |
| **Language**  | go, python, typescript, rust, cpp, csharp, java, php, kotlin, swift, lua, asm | 1          |
| **Framework** | react, vue, nextjs                                                            | 2          |
| **DevOps**    | docker, kubernetes, aws, ci-cd                                                | 3          |
| **Support**   | database, testing                                                             | 2          |

---

## 3-Tier Progressive Disclosure

| Tier | File        | Tokens | When       |
| ---- | ----------- | ------ | ---------- |
| T1   | META.yaml   | ~100   | Always     |
| T2   | SKILL.md    | ~1,500 | On-demand  |
| T3   | ADVANCED.md | ~4,000 | Referenced |

---

## META.yaml Schema (v4.0)

```yaml
name: skill-id          # lowercase, hyphen-separated
display: Display Name   # Human-readable
category: language      # core|language|framework|devops|support
priority: 1             # 0-5 (lower = higher)
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

_DOMYH Awesome Code v4.3_
