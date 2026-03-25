---
name: graph-patterns
description: "Guide agent on when to use CodeGraph (hsa_trace_flow) vs BM25 (hsa_search) vs Vector search. Decision framework for retrieval strategy selection."
detect: "When agent needs to understand code relationships, call chains, or impact analysis"
category: core
tier: 2
---

# Graph Patterns — Retrieval Strategy Selection

## When to Use Each Strategy

| Signal | Strategy | Tool | Why |
|:-------|:---------|:-----|:----|
| "What calls function X?" | **CodeGraph** | `hsa_trace_flow(entry_point, direction='upstream')` | Structural query |
| "What does X depend on?" | **CodeGraph** | `hsa_trace_flow(entry_point, direction='downstream')` | Dependency chain |
| "Find code related to auth" | **BM25+Vector** | `hsa_search(query)` | Semantic search |
| "Files matching *.test.ts" | **File search** | `hsa_search(action='files', pattern)` | Glob pattern |
| "Impact of changing X" | **CodeGraph → BM25** | trace_flow first, then search affected | Combined |
| "How is X implemented?" | **BM25+Vector** | `hsa_search(query, output_mode='full')` | Content retrieval |
| "Reference architecture" | **Repo Map** | `hsa_explore(action='repo_map')` | PageRank overview |

## Decision Tree

```
Need to understand code?
├── Structural relationships?
│   ├── Call chain / dependency → hsa_trace_flow
│   ├── File ranking overview → hsa_explore(repo_map)
│   └── Symbol definition → hsa_trace_flow(direction='both')
├── Content/semantic search?
│   ├── Code patterns → hsa_search(output_mode='skeleton')
│   ├── Full implementation → hsa_search(output_mode='full')
│   └── File names only → hsa_search(action='files')
└── Impact analysis?
    └── trace_flow → collect affected files → hsa_search each
```

## CodeGraph Capabilities (HSA Engine)

| Feature | Tool | Parameters |
|:--------|:-----|:-----------|
| Symbol lookup | `hsa_trace_flow` | `entry_point='ClassName'` |
| Call chain (upstream) | `hsa_trace_flow` | `direction='upstream'` |
| Call chain (downstream) | `hsa_trace_flow` | `direction='downstream'` |
| Both directions | `hsa_trace_flow` | `direction='both'` |
| Max depth | `hsa_trace_flow` | `depth=5` (max) |
| PageRank ranking | `hsa_explore` | `action='repo_map'` |
| Focus files | `hsa_explore` | `focus_files=['path']` |

## Pre-Refactor Checklist

⛔ **MANDATORY** — Before changing any function signature or interface:

1. `hsa_trace_flow(entry_point='functionName', direction='upstream')` → Who calls this?
2. `hsa_trace_flow(entry_point='functionName', direction='downstream')` → What does it call?
3. `hsa_search(query='functionName', output_mode='references')` → All file references
4. Assess blast radius → if > 5 files affected, STOP and confirm with user

## Anti-Patterns

| ❌ Don't | ✅ Do Instead |
|:---------|:-------------|
| `grep` for function calls | `hsa_trace_flow` for call chains |
| Search "imports" as text | CodeGraph dependency edges |
| Read files one by one manually | `hsa_explore(repo_map)` for ranked overview |
| Skip graph check before refactor | Always trace_flow before changing signatures |
| Use `output_mode='full'` first | Start with `skeleton` or `references`, escalate |
