---
description: "🔍 Semantic search across memory and audit history"
skills: { required: [], contextual: [] }
success_criteria: "Relevant results found, ranked by score, within token budget"
---

# 🔍 /search — Semantic Memory Search v1.0

> AI-powered semantic search across your project memory
> 📚 Requires: Semantic Memory enabled

---

## 🔄 SEARCH FLOW

```
User: /search {query}
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 1: CHECK AVAILABILITY             │
│ ▸ Check if semantic memory enabled      │
│ ▸ If disabled → Fall back to keyword    │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 2: GENERATE EMBEDDING             │
│ ▸ Create query embedding                │
│ ▸ OpenAI or local fallback              │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 3: SEARCH COLLECTIONS             │
│ ▸ Search relevant collections           │
│ ▸ Apply filters if specified            │
│ ▸ Rank by similarity score              │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 4: FORMAT RESULTS                 │
│ ▸ Limit to top_k results                │
│ ▸ Truncate for token budget             │
│ ▸ Display with relevance scores         │
└─────────────────────────────────────────┘
```

---

## 🎯 COMMANDS

| Command                     | Description                     | Example                           |
| --------------------------- | ------------------------------- | --------------------------------- |
| `/search {query}`           | Search all collections          | `/search authentication patterns` |
| `/search audits {query}`    | Search audits only              | `/search audits security issues`  |
| `/search decisions {query}` | Search decisions                | `/search decisions database`      |
| `/search errors {query}`    | Search error patterns           | `/search errors timeout`          |
| `/find-similar`             | Find similar to current context | `/find-similar`                   |
| `/recall {topic}`           | Recall past decisions           | `/recall caching strategy`        |

---

## 📊 OUTPUT FORMAT

```markdown
🔍 SEARCH RESULTS: "{query}"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Found {count} results in {time}ms

### 1. {title} (Relevance: {score}%)

**Source**: {collection} | **Date**: {date}

{summary}

---

### 2. {title} (Relevance: {score}%)

**Source**: {collection} | **Date**: {date}

{summary}

---

### 3. {title} (Relevance: {score}%)

**Source**: {collection} | **Date**: {date}

{summary}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 Refine search with: `/search {collection} {query}`
```

---

## 🔍 SEARCH TYPES

### Semantic Search (Default)

- Uses vector similarity
- Understands meaning, not just keywords
- Best for: concepts, patterns, similar issues

### Keyword Fallback

- Used when semantic disabled
- Exact text matching
- Searches: session.md, decisions.md, audits

### Hybrid Search

- Combines semantic + keyword
- Best for: specific terms + context

---

## 📁 SEARCHABLE COLLECTIONS

| Collection       | Content                | Fields Searched           |
| ---------------- | ---------------------- | ------------------------- |
| `audits`         | Audit reports          | findings, recommendations |
| `decisions`      | Architecture decisions | title, context, rationale |
| `code_reviews`   | Code review findings   | findings, suggestions     |
| `error_patterns` | Error solutions        | error_message, solution   |

---

## ⚙️ CONFIGURATION

```yaml
# In SEMANTIC_ENGINE.yaml
queries:
  defaults:
    top_k: 5 # Max results
    min_score: 0.7 # Minimum relevance (70%)
    include_metadata: true

# Token budget
tokens:
  max_results: 2500 # Total token limit
  per_result: 500 # Per result limit
```

---

## 🔀 HYBRID SEARCH MODE

```yaml
hybrid_search:
  description: "Combine semantic + keyword for best results"

  strategy:
    1_semantic:
      action: "Vector similarity search"
      weight: 0.7
    2_keyword:
      action: "Exact phrase matching"
      weight: 0.3
    3_merge:
      action: "Reciprocal Rank Fusion (RRF)"

  commands:
    - "/search hybrid [query]"
    - "/search --mode=hybrid [query]"

  example:
    query: "JWT authentication error handling"
    semantic: "Find conceptually similar auth patterns"
    keyword: "Find exact 'JWT' and 'error' matches"
    result: "Combined ranked results"
```

---

## 📍 CONTEXT-AWARE SEARCH

```yaml
context_search:
  description: "Auto-inject context from current file/task"

  commands:
    - "/search context" # Search based on active file
    - "/find-related" # Find related patterns

  auto_context:
    from_file: "Extract keywords from open file"
    from_error: "Extract error message patterns"
    from_task: "Extract from current task context"
```

---

## 🚫 FALLBACK BEHAVIOR

When semantic memory is **disabled**:

```
🔍 KEYWORD SEARCH RESULTS: "{query}"

Searching:
• memory/session.md
• memory/decisions.md
• memory/audit_summary.json

{keyword_matches}
```

---

## 💡 TIPS

1. **Be specific**: "authentication JWT refresh" > "auth issues"
2. **Use collection filters**: `/search audits P0 security`
3. **Combine with context**: `/find-similar` uses current context
4. **Check enabled**: `/mem status` shows if semantic is on

---

## 📦 REQUIREMENTS

```yaml
# Semantic memory (optional)
dependencies:
  - lancedb # pip install lancedb
  - openai # For embeddings (or use local)

# Local fallback (no API needed)
local_dependencies:
  - sentence-transformers # pip install sentence-transformers
```

---

---

## REFLECTION CHECKPOINT

⛔ **MANDATORY** — Execute before completing this workflow (SESSION_005):

1. **VERIFY** — Does output meet success_criteria (see YAML frontmatter)?
2. **PERSIST** (if HSA available — preferred, 1 tool call):
   - `hsa_session({action:'persist', task_summary:'[workflow] [summary]', files_touched:[...], auto_notify:true})`
   - If key decision → `hsa_session({action:'anchor', content:'[decision]', category:'decision'})`
3. **PERSIST** (if HSA unavailable — manual fallback):
   - Append task summary to `memory/session.md`
   - If last task → Update `memory/CONTEXT_SNAPSHOT.md`

