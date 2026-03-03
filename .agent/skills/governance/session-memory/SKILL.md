---
name: "session-memory"
description: "Persistent memory pattern using hsa_session with structured shelves. Decisions, patterns, errors survive across sessions and context compaction."
triggers:
  - "When making architectural or design decisions"
  - "When discovering patterns or solutions worth remembering"
  - "When encountering errors that should not be repeated"
  - "At session start — recall prior decisions before re-debating"
  - "Before context compaction — emergency save"
---

# Session Memory (Persistent Brain Pattern)

## Problem

Without persistent memory, each session starts from zero. Agent re-debates decisions, re-discovers patterns, and repeats solved errors. Context compaction silently erases hours of accumulated knowledge.

## Solution: Structured Anchors as Memory Shelves

Use `hsa_session` with structured categories to create searchable, persistent memory that survives across sessions and compaction events.

### Memory Shelf Architecture

| Shelf | Category | When to Save | Example |
|-------|----------|-------------|---------|
| Architecture decisions | `decision` | Choosing framework, library, API design | "Chose JWT over session: stateless, scales horizontally" |
| Code patterns | `convention` | Recurring patterns, naming conventions | "API responses use `{ data, error, meta }` envelope" |
| Resolved errors | `context` | Error + root cause + fix | "Port 3000 conflict: kill process or use 3001" |
| Hard constraints | `constraint` | Port numbers, API limits, schema rules | "PostgreSQL max connections: 100, pool size: 20" |
| Stack info | `stack` | Tech stack, versions, dependencies | "Node 22 + TypeScript 5.7 + Vitest" |

## Structured Anchor Format

### Decision Anchor Template

```
hsa_session(
  content: "[DECISION] Chose {X} over {Y}. Reason: {why}. Trade-off: {what we lose}. Date: {today}",
  category: "decision"
)
```

**Example:**
```
hsa_session(
  content: "[DECISION] Chose Drizzle ORM over Prisma. Reason: lighter, SQL-first, better edge support. Trade-off: less mature ecosystem. 2026-02-20",
  category: "decision"
)
```

### Convention Anchor Template

```
hsa_session(
  content: "[CONVENTION] {pattern name}: {description}. Files: {where applied}",
  category: "convention"
)
```

**Example:**
```
hsa_session(
  content: "[CONVENTION] API Response Envelope: All endpoints return { data, error, meta }. Files: src/utils/response.ts",
  category: "convention"
)
```

### Error Anchor Template

```
hsa_session(
  content: "[ERROR] {symptom} → Root cause: {cause} → Fix: {solution}. Files: {affected}",
  category: "context"
)
```

### Constraint Anchor Template

```
hsa_session(
  content: "[CONSTRAINT] {what}: {limit}. Source: {where documented}",
  category: "constraint"
)
```

## Save Protocol

### When to Save (Triggers)

| Trigger | Action | Priority |
|---------|--------|----------|
| Chose X over Y | `save_anchor(category: "decision")` | 🔴 Immediate |
| Found reusable pattern | `save_anchor(category: "convention")` | 🟡 Soon |
| Fixed tricky bug | `save_anchor(category: "context")` with error + root cause | 🔴 Immediate |
| Discovered constraint | `save_anchor(category: "constraint")` | 🟡 Soon |
| Detected project stack | `save_anchor(category: "stack")` | 🟢 Once |
| Context feels heavy (many turns) | Emergency save key decisions | 🔴 Immediate |

### Save Cadence

- **Every significant decision** → save immediately
- **Every 5-8 turns** → review if anything unsaved
- **Before any "let me think about this"** → save current state first
- **Never wait for session end** → compaction may fire before end

## Recall Protocol (Session Start)

### Step 1: Retrieve Prior State

```
hsa_session(
  current_action: "Starting new session — retrieving prior anchors",
  include_anchors: true
)
```

### Step 2: Parse Anchors by Category

Read the drift report output. Look for:
- `[DECISION]` anchors → Don't re-debate these
- `[CONVENTION]` anchors → Follow these patterns
- `[CONSTRAINT]` anchors → Respect these limits
- `[ERROR]` anchors → Avoid these mistakes

### Step 3: Declare Intent Referencing Prior Work

```
hsa_session(
  focus: "Continuing: {summary from anchors}",
  mode: "plan_driven",
  goals: ["Goal from prior session anchors"]
)
```

## Compaction Survival Protocol

### Detect Compaction Risk

Signs that compaction is imminent:
- Very long conversation (50+ turns)
- Multiple topic shifts
- Large code blocks in context
- System mentions context limits

### Emergency Save Sequence

When compaction risk detected:

```
# 1. Save current progress
hsa_session(
  content: "[SESSION] Progress: {done list}. Pending: {todo list}. Key files: {files}",
  category: "context"
)

# 2. Save any unsaved decisions
hsa_session(
  content: "[DECISION] {any decision made but not yet saved}",
  category: "decision"
)

# 3. Update hierarchy
hsa_session(level: "action", label: "Emergency save before compaction", status: "completed")
```

## Memory Hygiene

### When Anchors Become Stale

| Signal | Action |
|--------|--------|
| Decision was reversed | Save new decision, reference old one |
| Convention changed | Save updated convention with "[UPDATED]" prefix |
| Error was a false lead | Don't delete — add "[SUPERSEDED]" note |
| Constraint removed | Save "[REMOVED] constraint: {reason}" |

### Don't Over-Save

- Skip trivial formatting decisions
- Skip temporary debugging notes
- Skip file paths that may change
- Focus on **WHY** not **WHAT** — the what is in code

## Red Flags

| Thought | Reality |
|---------|---------|
| "I'll save at the end" | Context may compact before end. Save NOW. |
| "This is obvious" | Obvious to you now, invisible to next session. |
| "I remember this" | After compaction you won't. After session switch you can't. |
| "I already saved something similar" | Check with drift — if not there, save again. |
| "This decision is temporary" | Temporary decisions have a habit of becoming permanent. Save it. |
