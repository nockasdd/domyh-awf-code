# 🧠 DOMYH Awesome Code Memory System

> Version 6.3.9 — 5-Layer Hierarchical Memory Architecture

---

## Overview

This directory contains the persistent memory system for DOMYH Awesome Code, enabling:

- **Cross-session context** — Remember work across conversations
- **Low token footprint** — Only ~5,500 tokens total (~4.3% of limit)
- **Human-readable files** — Easy to review and edit
- **Structured data** — Fast JSON lookups

---

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│ Layer 1: WORKING MEMORY (in-context)        ~500 tokens      │
│ └── Managed automatically by agent                           │
├──────────────────────────────────────────────────────────────┤
│ Layer 2: SESSION NOTES (file-based)         ~2,000 tokens    │
│ └── session.md — Current session context                     │
├──────────────────────────────────────────────────────────────┤
│ Layer 3: PROJECT STATE (JSON)               ~500 tokens      │
│ ├── state.json — Project info, preferences                   │
│ ├── audit_summary.json — Compact audit results               │
│ └── decisions.md — Architectural decisions log               │
├──────────────────────────────────────────────────────────────┤
│ Layer 4: SEMANTIC MEMORY (optional)         ~2,500 tokens    │
│ └── vectors/ — LanceDB (when enabled)                        │
├──────────────────────────────────────────────────────────────┤
│ Layer 5: SESSION GOVERNANCE (v7.0)          ~200 tokens      │
│ └── .agent/hsa/session-state.json — Intent, hierarchy,        │
│     anchors, drift metrics (managed by HSA MCP tools)        │
└──────────────────────────────────────────────────────────────┘
```

---

## Files

| File                 | Purpose                        | Format   | Max Tokens |
| -------------------- | ------------------------------ | -------- | ---------- |
| `session.md`         | Current session notes, history | Markdown | 2,000      |
| `decisions.md`       | Architectural decisions log    | Markdown | 500        |
| `state.json`         | Project state, preferences     | JSON     | 500        |
| `audit_summary.json` | Compact audit results          | JSON     | 200        |
| `vectors/`           | Semantic memory (optional)     | LanceDB  | 2,500      |

---

## Auto-Save Triggers

The memory system automatically saves when:

| Trigger               | Files Updated                              |
| --------------------- | ------------------------------------------ |
| Workflow completes    | `session.md`, `state.json`                 |
| Decision made         | `decisions.md`, `state.json`               |
| Audit completes       | `audit_summary.json`, `state.json`         |
| Error resolved        | `session.md`                               |
| Every 10 interactions | `session.md`                               |
| Intent declared       | `.agent/hsa/session-state.json`            |
| Progress tracked      | `.agent/hsa/session-state.json`            |
| Anchor saved          | `.agent/hsa/session-state.json`            |
| Session ends          | All files                                  |

---

## Auto-Load Triggers

Memory is loaded when:

| Event            | Layers Loaded         |
| ---------------- | --------------------- |
| Session starts   | State, Session notes  |
| `/recap` command | All layers            |
| Context request  | State only            |
| Semantic search  | Semantic (if enabled) |

---

## Configuration

Memory engine configuration: `core/archive/MEMORY_ENGINE.yaml` _(archived design spec)_

Key settings:

```yaml
# Token budgets per layer
layer_budgets:
  working: 500
  session: 2000
  state: 500
  semantic: 2500 # Only if enabled

# Auto-save interval
auto_save_interval_ms: 300000 # 5 minutes

# Cleanup threshold
auto_cleanup_threshold_tokens: 10000
```

---

## Usage

### View Current Memory

```
/recap
```

### Clear Session Memory

```
/clear session
```

### Force Save

```
/save memory
```

### Enable Semantic Memory

Edit `core/MEMORY_ENGINE.yaml`:

```yaml
semantic:
  enabled: true
```

---

## Human Editing

All markdown files are safe to edit manually:

- `session.md` — Add notes, correct info
- `decisions.md` — Update rationale, add context

JSON files should maintain schema:

- `state.json` — Use valid JSON
- `audit_summary.json` — Keep structure intact

---

_DOMYH Awesome Code — Memory System_
