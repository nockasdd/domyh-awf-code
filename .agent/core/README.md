# ⚙️ DOMYH Awesome Code Core v6.4.3

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

| File                  | Purpose                 | Tokens |
| --------------------- | ----------------------- | ------ |
| ARCH_REGISTRY.yaml    | Architecture patterns   | ~1,900 |
| BRANDING.yaml         | Project identity SSoT   | ~600   |
| CODING_STYLES.yaml    | Language conventions ⚠️ | ~650   |
| HSA.yaml              | HSA master config       | ~1,100 |
| LIBRARY_REGISTRY.yaml | Library recommendations | ~650   |
| MCP_TOOLS.yaml        | MCP tool definitions    | ~1,100 |
| PATTERNS.yaml         | Shared workflow patterns| ~550   |
| SKILL_SCHEMA.yaml     | Skill structure schema  | ~400   |
| TEMPLATES.yaml        | Template registry       | ~300   |

> ⚠️ CODING_STYLES.yaml is deprecated — kept for reference. SSoT is `/code` workflow.

## Archive

`archive/` contains 25 legacy engine files (ROUTER, TOKEN_BUDGETS, CONTEXT_LOADER, SKILLS_FLOW, MEMORY_ENGINE, etc.). These were consolidated into `AGENT_BEHAVIOR.md` and are kept for historical reference only.

See `archive/README.md` for details.

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

_DOMYH Awesome Code • Core System v6.3.9_
