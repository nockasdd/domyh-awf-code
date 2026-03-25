---
name: context-engineering
description: Context window management, token budget optimization, and compaction strategies
detect: []
category: core
tier: 1
---

# Context Engineering

> Context Engineering ⊃ Prompt Engineering
> "What the model KNOWS when you talk to it" — not just what you say.

## Context = Everything in the Window

```
System Rules → Memory → Retrieved Docs → Tool Schemas → History → Current Task
```

### Layered Context Taxonomy

| Layer | Content | Priority | Budget |
|:------|:--------|:---------|:-------|
| **System Rules** | SACRED_RULES, constitutional hierarchy | Always | ~500 tok |
| **Memory** | CONTEXT_SNAPSHOT, session.md, anchors | Cold start | ~500 tok |
| **Retrieved Docs** | RAG results, skill data, file contents | On-demand | ~2,000 tok |
| **Tool Schemas** | MCP tools, function signatures | Always | ~800 tok |
| **Conversation History** | Previous turns, summaries | Rolling | ~3,000 tok |
| **Current Task** | User query, active workflow, persona | Always | ~500 tok |

## Position Engineering (U-Shape Attention)

LLMs attend most to **head** and **tail** of context window ("Lost in the Middle" effect):

```
┌─────────────────────────────────────────────────┐
│ HEAD (HIGH attention)                           │
│ → SACRED_RULES, token budgets, core constraints │
├─────────────────────────────────────────────────┤
│ MIDDLE (LOW attention)                          │
│ → General context, old history, tool results    │
├─────────────────────────────────────────────────┤
│ TAIL (HIGH attention)                           │
│ → Current task, active persona, user query      │
└─────────────────────────────────────────────────┘
```

**Rule**: Place critical rules + budgets in HEAD. Place current task + persona in TAIL.

## 9 Context Engineering Techniques

| # | Technique | Status in DOMYH |
|:--|:----------|:----------------|
| 1 | **Layered Context** — structured taxonomy | ✅ Implemented |
| 2 | **Progressive Disclosure** — 3-tier skill loading | ✅ Implemented |
| 3 | **RAG Pipeline** — BM25+Vector hybrid retrieval | ✅ via HSA |
| 4 | **Context Compression** — signal-based compaction | ✅ Implemented |
| 5 | **Sub-agent Delegation** — fork context isolation | ✅ via hsa_delegate |
| 6 | **Tool Management** — curated via manifest | ✅ Implemented |
| 7 | **Agentic Memory** — multi-layer persistence | ✅ CONTEXT_SNAPSHOT + KI |
| 8 | **Position Engineering** — U-shape attention | ✅ Implemented |
| 9 | **Routing** — intent→workflow classification | ⚠️ Keyword (not LLM-powered) |

## When to Compact

| Signal | Action |
|--------|--------|
| Context >70% of window | Summarize old history |
| >10 consecutive tool results | Keep latest, compress old |
| Research phase → Execution phase | Summarize findings, clear raw data |
| Repetitive patterns accumulating | Extract pattern, remove duplicates |
| Context rot detected | Re-read source files, discard stale cache |

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
- 101 skills × ~86 tokens = ~8,700 tokens (vs 101 × 3,000 = 303,000 if all loaded)

### Memory Strategy
| Type | Storage | Tokens | Lifetime |
|------|---------|:------:|----------|
| **Anchors** | `hsa_session` | ~50 each | Permanent |
| **Session** | `CONTEXT_SNAPSHOT.md` | ~500 | Cross-session |
| **Working** | Context window | Dynamic | Current session |
| **Knowledge** | Knowledge Items | ~200 ref | Persistent |

### Tool Results
- **Keep**: Latest result, error messages, test output
- **Compress**: Old file contents, repeated search results
- **Discard**: Verbose build logs, large file listings

## HSA Tools for Context Management

| Tool | Context Role |
|------|-------------|
| `hsa_search` | Retrieve with token budget (max_tokens param) |
| `hsa_search(skills)` | Find relevant skills without loading all |
| `hsa_session(anchor)` | Persist facts outside context window |
| `hsa_session(persist)` | Save snapshot for next session |
| `hsa_session(drift)` | Detect context misalignment |
| `hsa_prefetch` | Pre-load files for faster access |
| `hsa_explore` | Compact codebase overview (vs reading all files) |
| `hsa_delegate` | Isolate sub-task context |

## Anti-Patterns

❌ Loading all skills at once
❌ Keeping full file contents after reading
❌ Not summarizing after research phase
❌ Dumping entire error logs into context
❌ Re-reading files already in context
❌ Ignoring position engineering (placing critical info in middle)
❌ Context rot — using stale cached data without re-validation
❌ "Lost in the Middle" — burying important instructions in center
