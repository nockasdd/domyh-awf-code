---
name: context-compaction
description: "Detect context window saturation and trigger compaction. Includes signals, thresholds, and techniques for maintaining context quality during long sessions."
detect: "When context utilization exceeds 40% or session exceeds 50 tool calls"
category: governance
tier: 2
---

# Context Compaction — Window Management

> HSA Engine has 4 built-in compaction strategies. This skill guides WHEN to trigger them.

## Compaction Signals (Act When ANY Triggers)

| Signal | Threshold | Detection |
|:-------|:----------|:----------|
| Token usage | > 40% of budget | Check conversation length |
| Tool call count | > 50 calls | Count in session |
| Conversation turns | > 30 turns | Count user+agent messages |
| File outputs | > 3 large results (>2000 tok each) | Monitor tool output size |
| Session time | > 45 min | Check elapsed time |

## Action: Compaction Workflow

```
Signal detected?
├── YES → Step 1: Persist current state
│   └── hsa_session(action='persist', task_summary='...')
├── Step 2: Summarize key findings
│   └── Write to CONTEXT_SNAPSHOT.md
├── Step 3: Release unused skill slots
│   └── Stop referencing inactive T2 skills
└── Step 4: Switch to compact output modes
    └── Use output_mode='skeleton' or 'references'
```

## HSA Engine Strategy Mapping

| When | HSA Strategy | What Happens |
|:-----|:-------------|:-------------|
| Code blocks too large | `trim-code` | Removes fenced code blocks, keeps signatures |
| LLM available | `llm-summarize` | Batches items, LLM produces concise summaries |
| Many same-dir files | `summarize` | Groups by directory, merges into summaries |
| Critical budget | `aggressive` | File names + one-line descriptions only |

> HSA applies these automatically via `context-compactor.ts`. The agent role is to:
> 1. **Recognize** when compaction is needed (signals above)
> 2. **Persist** important state before compaction
> 3. **Reduce** unnecessary context proactively

## Proactive Techniques (Agent-Side)

| Technique | How |
|:----------|:----|
| History summarization | `hsa_session(action='persist')` → fresh context |
| Output truncation | Save large outputs to file, keep summary in context |
| Skill slot release | If 3 T2 loaded and one unused → stop referencing it |
| Reference compaction | Replace inline file content with `file:///path#L123` refs |
| Progressive disclosure | Start with `references` → `skeleton` → `full` only if needed |

## Anti-Patterns

| ❌ Don't | ✅ Do Instead |
|:---------|:-------------|
| Keep growing context indefinitely | Compact at 40% threshold |
| Re-read entire files repeatedly | Use `skeleton`/`references` mode first |
| Load all skills simultaneously | Max 3 T2 slots, release when done |
| Ignore large tool outputs | Extract key info, reference original |
| Wait until context is full | Proactively persist at 50 tool calls |
