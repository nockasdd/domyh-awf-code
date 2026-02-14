# Progressive Disclosure Patterns

## 3-Tier Loading System

```
Tier 1: META.yaml     (~100 tokens)  — Always loaded for routing
Tier 2: SKILL.md      (~1,500 tokens) — Loaded on-demand when skill activated
Tier 3: ADVANCED.md   (~4,000 tokens) — Referenced only when deep-dive needed
```

## When to Split

| Condition              | Action                                 |
| ---------------------- | -------------------------------------- |
| SKILL.md < 300 lines   | Keep as-is                             |
| SKILL.md 300-500 lines | Consider splitting heavy sections      |
| SKILL.md > 500 lines   | **Must split** into core + references/ |

## Split Strategy

1. **Keep in SKILL.md** (core, < 300 lines):
   - Decision tree
   - Quick start / most common workflow
   - Essential patterns overview
   - Production checklist
   - Data file references

2. **Move to references/** (on-demand):
   - Detailed code examples
   - Platform-specific content
   - Migration guides
   - Advanced patterns
   - API reference tables

3. **Keep in ADVANCED.md** (rare access):
   - Deep architectural patterns
   - Performance tuning guides
   - Edge cases and gotchas
   - Historical context

## Reference File Naming

```
references/
├── {topic}-patterns.md     # Pattern collections
├── {platform}-specific.md  # Platform guides
├── migration-guide.md      # Version migration
└── api-reference.md        # API documentation
```

## Linking Pattern

```markdown
## 📚 Deep-Dive References

- **Topic Name** — Brief description
  → See [references/topic-name.md](references/topic-name.md)
```
