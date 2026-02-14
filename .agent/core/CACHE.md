# Session Cache v6.2.7

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

```
Target: < 10,000 tokens peak
├── META.yaml baseline: 1,773 tokens
├── Active skills (3×): 4,500 tokens
├── Current workflow: 500 tokens
└── Buffer: 3,227 tokens
```

---

\_DOMYH Awesome Code
