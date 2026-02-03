# 🔍 DOMYH Awesome Code — Semantic Memory

> Vector-based semantic search using LanceDB
> **Status**: Optional (Disabled by default)

---

## Overview

This directory contains the LanceDB vector database for semantic memory.
When enabled, it provides:

- **Semantic search** across audit history
- **Similar decision** lookup
- **Error pattern** matching
- **Code review** insights

---

## Enabling Semantic Memory

### Option 1: Edit Configuration

Edit `.agent/core/SEMANTIC_ENGINE.yaml`:

```yaml
config:
  enabled: true # Change from false
```

### Option 2: Use Command (Future)

```
/mem enable-semantic
```

---

## Requirements

### LanceDB (Embedded)

```bash
# Python
pip install lancedb

# Node.js
npm install @lancedb/lancedb
```

### Embeddings (Choose one)

**OpenAI (Recommended)**:

```bash
export OPENAI_API_KEY=your_key
```

**Local Fallback (No API needed)**:

```bash
pip install sentence-transformers
```

---

## Collections

| Collection       | Content                 | Index Trigger      |
| ---------------- | ----------------------- | ------------------ |
| `audits`         | Full audit reports      | `/ap` complete     |
| `decisions`      | Architectural decisions | Decision made      |
| `code_reviews`   | Review findings         | `/review` complete |
| `error_patterns` | Error solutions         | Error resolved     |

---

## Search Commands

| Command         | Description           | Example                    |
| --------------- | --------------------- | -------------------------- |
| `/search`       | Semantic search all   | `/search authentication`   |
| `/find-similar` | Find similar content  | `/find-similar this error` |
| `/recall`       | Recall past decisions | `/recall database choice`  |

---

## Token Budget

| Setting           | Value     |
| ----------------- | --------- |
| Max results       | 5         |
| Tokens per result | 500       |
| **Total budget**  | **2,500** |

---

## Directory Structure

```
vectors/
├── README.md           # This file
├── domyh_memory.lance/ # LanceDB database (when created)
└── .gitignore          # Ignore database files
```

---

## Data Retention

| Collection | Max Age  | Minimum Keep |
| ---------- | -------- | ------------ |
| Audits     | 1 year   | 10 entries   |
| Decisions  | 2 years  | 50 entries   |
| Errors     | 6 months | 20 entries   |

---

## Fallback Behavior

When semantic search is disabled or unavailable:

- Falls back to **keyword search**
- Uses **file-based memory** (session.md, decisions.md)
- No warning shown to user

---

_DOMYH Awesome Code v5.5 • Semantic Memory (Optional)_
