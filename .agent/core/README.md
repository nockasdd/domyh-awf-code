# ⚙️ DOMYH Awesome Code Core

Core system files — always loaded or on-demand reference.

## Active Files

### System Config

| File                | Purpose                    |
| ------------------- | -------------------------- |
| VERSION.yaml        | SSoT for all versions      |
| MEMORY_PATHS.yaml   | SSoT for memory file paths |
| session_cache.json  | LRU session state          |

### Documentation (always loaded)

| File            | Purpose              | Lines |
| --------------- | -------------------- | ----- |
| AGENT_BEHAVIOR  | Agent execution guide | ~86   |
| AUDIT_POLICY    | Audit configuration  | ~68   |
| CACHE           | Caching strategy     | ~59   |
| COMMANDS        | Command registry     | ~106  |
| CUSTOMIZE       | Skill customization  | ~196  |
| DATA_SAFETY     | Sensitive data rules | ~92   |
| PERMISSIONS     | Access control tiers | ~100  |

### Reference (on-demand)

> ⚠️ Reference files moved to `docs/reference/`. Listed here for context only.

| File                  | Purpose                 |
| --------------------- | ----------------------- |
| ARCH_REGISTRY.yaml    | Architecture patterns   |
| BRANDING.yaml         | Project identity SSoT   |
| CODING_STYLES.yaml    | Language conventions    |
| HSA.yaml              | HSA master config       |
| LIBRARY_REGISTRY.yaml | Library recommendations |
| MCP_TOOLS.yaml        | MCP tool definitions    |
| PATTERNS.yaml         | Shared workflow patterns|
| SKILL_SCHEMA.yaml     | Skill structure schema  |
| TEMPLATES.yaml        | Template registry       |

## Archive

> Moved to `docs/archived-specs/`. Contains 25 legacy engine files (ROUTER, TOKEN_BUDGETS, etc.), consolidated into `AGENT_BEHAVIOR.md`.

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

---
