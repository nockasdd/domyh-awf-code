# Session Cache v6.4.2

## Caching Strategy

### Workflow Cache

```yaml
enabled: true
scope: session
ttl: 3600
max_entries: 10
```

### Skill Cache

```yaml
enabled: true
max_active: 3
eviction: lru
preload_meta: true
```

### Query Cache

```yaml
enabled: true
cache_embeddings: true
cache_selections: true
ttl: 1800
```

## Cache Layers

| Layer     | TTL     | Strategy             |
| --------- | ------- | -------------------- |
| META.yaml | Session | Always loaded        |
| SKILL.md  | 1 hour  | On-demand, LRU       |
| Workflow  | 1 hour  | Per-command          |
| Query     | 30 min  | Embedding similarity |

## Eviction Rules

1. When `max_active` reached → evict LRU skill
2. When cache full → evict oldest entries
3. On command change → clear irrelevant cache

## Memory Budget

> **Note**: This is the **agent-side skill/workflow cache** budget, NOT the HSA engine
> context retrieval budget (which defaults to 8,000 tokens — see `hsa-engine-ts/config/constants.ts`).
> IDE adapters may define their own `max_peak` in `.agent/ide/{ide}.json`.

```
Target: < 10,000 tokens peak (agent-side, 3 active skills)
├── META.yaml baseline: 2,200 tokens
├── Active skills (3×): 4,500 tokens
├── Current workflow: 500 tokens
└── Buffer: 2,800 tokens
```

---

\_DOMYH Awesome Code
