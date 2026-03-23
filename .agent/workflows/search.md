---
description: "🔍 Semantic search across memory and audit history"
skills: { required: [], contextual: [] }
success_criteria: "Relevant results found, ranked by score, within token budget"
---

# 🔍 /search — Semantic Memory Search

> AI-powered semantic search across project memory
> 📚 Semantic + Keyword + Hybrid modes

---

## ⛔ RULES (Always Apply)

| # | Rule | Category |
|:--|:-----|:---------|
| R1 | Use `hsa_search` for codebase search — `/search` is for MEMORY only | Scope |
| R2 | Limit results to top_k=5, min_score=0.7 (70%) | Efficiency |
| R3 | Truncate results within token budget (2500 max) | Efficiency |

---

## SEARCH FLOW

1. **CHECK** — Verify semantic memory enabled. If disabled → fall back to keyword search.
2. **SEARCH** — Query relevant collections with filters. Rank by similarity score.
3. **FORMAT** — Present top results with relevance scores, source, and date.
4. **REFINE** — Suggest refinement: `/search {collection} {query}`

---

## COMMANDS

| Command | Description | Example |
|:--------|:------------|:--------|
| `/search {query}` | Search all collections | `/search authentication patterns` |
| `/search audits {query}` | Search audits only | `/search audits security issues` |
| `/search decisions {query}` | Search decisions | `/search decisions database` |
| `/search errors {query}` | Search error patterns | `/search errors timeout` |
| `/find-similar` | Find similar to current context | `/find-similar` |
| `/recall {topic}` | Recall past decisions | `/recall caching strategy` |

---

## SEARCHABLE COLLECTIONS

| Collection | Content | Fields Searched |
|:-----------|:--------|:----------------|
| `audits` | Audit reports | findings, recommendations |
| `decisions` | Architecture decisions | title, context, rationale |
| `code_reviews` | Code review findings | findings, suggestions |
| `error_patterns` | Error solutions | error_message, solution |

---

## SEARCH MODES

| Mode | Method | Best For |
|:-----|:-------|:---------|
| **Semantic** (default) | Vector similarity | Concepts, patterns, similar issues |
| **Keyword** (fallback) | Exact text matching | Specific terms, when semantic disabled |
| **Hybrid** | Semantic (0.7) + Keyword (0.3) via RRF | Specific terms + context |

---

## 💡 TIPS

1. **Be specific:** "authentication JWT refresh" > "auth issues"
2. **Use collection filters:** `/search audits P0 security`
3. **Use context:** `/find-similar` uses current file context
4. **Codebase search:** Use `hsa_search` instead — different purpose

---

## REFLECTION CHECKPOINT

⛔ **MANDATORY** — Execute before completing this workflow (SESSION_005):

1. **VERIFY** — Does output meet success_criteria (see YAML frontmatter)?
2. **PERSIST** (if HSA available):
   - `hsa_session({action:'persist', task_summary:'[workflow] [summary]', files_touched:[...]})`
3. **PERSIST** (if HSA unavailable):
   - Append task summary to `memory/session.md`
