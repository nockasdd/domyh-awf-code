# ⚙️ DOMYH Awesome Code Core v6.2.4

Core system files (always loaded).

## Files (44 total)

### Engine Files

| File                      | Purpose               | Tokens |
| ------------------------- | --------------------- | ------ |
| ROUTER.yaml               | Semantic routing      | ~350   |
| FLOW_ENGINE.yaml          | Workflow chaining     | ~500   |
| MEMORY_ENGINE.yaml        | 4-layer memory system | ~600   |
| SEMANTIC_ENGINE.yaml      | Vector DB (optional)  | ~600   |
| TOKEN_LOADING.yaml        | Lazy loading strategy | ~350   |
| TOKEN_BUDGETS.yaml        | SSoT for token limits | ~400   |
| CONTEXT_LOADER.yaml       | JIT context loading   | ~450   |
| CONTEXT_INJECTOR.yaml     | Smart injection       | ~600   |
| CONTEXT_PRIORITY.yaml     | Priority scoring      | ~600   |
| ACTIVE_MEMORY.yaml        | Self-directing memory | ~650   |
| MEMORY_CONSOLIDATION.yaml | Auto-consolidation    | ~600   |

### Registry Files

| File                  | Purpose                 | Tokens |
| --------------------- | ----------------------- | ------ |
| ARCH_REGISTRY.yaml    | Architecture patterns   | ~1,900 |
| LIBRARY_REGISTRY.yaml | Library recommendations | ~650   |
| INTENT_DETECTION.yaml | Intent classification   | ~700   |
| CODING_STYLES.yaml    | Language conventions    | ~650   |
| PATTERNS.yaml         | Workflow patterns       | ~550   |
| SKILLS_FLOW.yaml      | Skill loading rules     | ~900   |
| SKILL_SCHEMA.yaml     | Skill structure         | ~400   |

### Documentation Files

| File            | Purpose              | Tokens |
| --------------- | -------------------- | ------ |
| README.md       | This file            | ~200   |
| CACHE.md        | Caching strategy     | ~250   |
| COMMANDS.md     | Command registry     | ~500   |
| CUSTOMIZE.md    | Skill customization  | ~600   |
| DATA_SAFETY.md  | Sensitive data rules | ~300   |
| PERMISSIONS.md  | Access control tiers | ~350   |
| AUDIT_POLICY.md | Audit configuration  | ~250   |
| TEMPLATES.yaml  | Output templates     | ~300   |

### Utilities

| File                      | Purpose             | Tokens |
| ------------------------- | ------------------- | ------ |
| MEMORY_PATHS.yaml         | SSoT for paths      | ~200   |
| MEMORY_UTILS.yaml         | Memory helpers      | ~400   |
| SCORING_FORMULA.yaml      | Priority algorithm  | ~300   |
| SUMMARIZATION_ENGINE.yaml | Content compression | ~450   |
| CLEANUP_ENGINE.yaml       | Context cleanup     | ~550   |
| TOKEN_SUMMARY.yaml        | Token analytics     | ~350   |
| embeddings.json           | TF-IDF vectors      | N/A    |
| session_cache.json        | LRU session state   | N/A    |

## Architecture

### Progressive Disclosure

```
Tier 1: META.yaml   (~100 tokens)  → Always loaded
Tier 2: SKILL.md    (~1,500 tokens) → On-demand
Tier 3: ADVANCED.md (~4,000 tokens) → Referenced only
```

### Semantic Selection

- Algorithm: TF-IDF with keyword boost
- Top-K: 5 skills per query
- Threshold: 30% similarity
- Cache: LRU (max 3 active skills)

## Token Budget

| State            | Tokens | Reference              |
| ---------------- | ------ | ---------------------- |
| Idle baseline    | ~2,100 | 21 × META.yaml         |
| 1 skill active   | ~3,600 | +1,500 SKILL.md        |
| Peak (3 skills)  | ~6,600 | 3 × SKILL.md           |
| + Semantic layer | +2,500 | TOKEN_BUDGETS.yaml:119 |

> **Note**: Semantic layer is disabled by default. Enable in `MEMORY_ENGINE.yaml`.

---

_DOMYH Awesome Code • Core System_
