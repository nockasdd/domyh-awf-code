---
name: context-engineering
description: Context window management, token budget optimization, and compaction strategies
---

# Context Engineering

> Context Engineering ⊃ Prompt Engineering
> "What the model KNOWS when you talk to it" — not just what you say.

## Context = Everything in the Window

```
System Prompt + Rules + Skills + Memory + Tool Results + History = Context
```

## When to Compact

| Signal | Action |
|--------|--------|
| Context >70% of window | Summarize old history |
| >10 consecutive tool results | Keep latest, compress old |
| Research phase → Execution phase | Summarize findings, clear raw data |
| Repetitive patterns accumulating | Extract pattern, remove duplicates |

## When to Fork (Sub-Agent)

| Signal | Action |
|--------|--------|
| Independent sub-task identified | Fork with minimal context |
| Sub-task needs different tool set | Use `hsa_delegate` |
| Current context irrelevant to sub-task | Isolate via `hsa_delegate` |
| Multiple research paths needed | Parallelize with sub-agents |

## Token Budget Rules

### Skills (Lazy-Loading)
- Metadata only at startup: **~50-100 tokens/skill**
- Full skill loaded on-demand: **~2,000-5,000 tokens**
- 85+ skills × 50 tokens = 4,250 tokens (vs 85 × 3,000 = 255,000 if all loaded)

### Memory Strategy
| Type | Storage | Tokens | Lifetime |
|------|---------|:------:|----------|
| **Anchors** | `hsa_session` | ~50 each | Permanent |
| **Session** | `CONTEXT_SNAPSHOT.md` | ~500 | Cross-session |
| **Working** | Context window | Dynamic | Current session |

### Tool Results
- **Keep**: Latest result, error messages, test output
- **Compress**: Old file contents, repeated search results
- **Discard**: Verbose build logs, large file listings

## HSA Tools for Context Management

| Tool | Context Role |
|------|-------------|
| `hsa_search` | Retrieve with token budget (max_tokens param) |
| `hsa_search` | Find relevant skills without loading all |
| `hsa_session` | Persist facts outside context window |
| `hsa_session` | Save snapshot for next session |
| `hsa_prefetch` | Pre-load files for faster access |
| `hsa_explore` | Compact codebase overview (vs reading all files) |

## Anti-Patterns

❌ Loading all skills at once
❌ Keeping full file contents after reading
❌ Not summarizing after research phase
❌ Dumping entire error logs into context
❌ Re-reading files already in context
