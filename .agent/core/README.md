# DOMYH Awesome Code Core v4.3

Core system files (always loaded).

## Files

| File               | Purpose                  | Tokens |
| ------------------ | ------------------------ | ------ |
| RULES.md           | Core rules and standards | ~200   |
| STOP.md            | Stop conditions          | ~200   |
| ROUTER.yaml        | Semantic routing config  | ~350   |
| CACHE.md           | Caching strategy         | ~250   |
| COMMANDS.md        | Command registry         | ~500   |
| CUSTOMIZE.md       | Skill customization      | ~600   |
| ARCH_REGISTRY.yaml | Architecture patterns    | ~1,900 |
| embeddings.json    | TF-IDF skill vectors     | N/A    |
| session_cache.json | LRU session state        | N/A    |

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

| State                   | Tokens |
| ----------------------- | ------ |
| Baseline (33 META.yaml) | 3,300  |
| 1 skill active          | 4,800  |
| Peak (3 skills)         | 7,800  |
| + Semantic (if enabled) | +2,500 |

> **Note**: Semantic layer is disabled by default. Enable in `MEMORY_ENGINE.yaml`.

---

_DOMYH Awesome Code v4.3_
