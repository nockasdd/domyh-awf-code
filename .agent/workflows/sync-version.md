---
description: 🔄 Sync version from VERSION.yaml SSoT across all files
skills: { required: [], contextual: [] }
success_criteria: "Version synced across all files, validation passed"
---

# /sync-version — Version SSoT Sync

> Propagate the single source of truth version to all 60+ files.

## Prerequisites

- Node.js installed
- Working directory at project root

## Steps

1. **Preview changes** (dry run):

```bash
// turbo
node domyh-awf/.agent/scripts/sync-version.mjs --dry-run
```

2. **Execute sync**:

```bash
node domyh-awf/.agent/scripts/sync-version.mjs
```

3. **Validate** (check for drift — useful in CI):

```bash
// turbo
node domyh-awf/.agent/scripts/sync-version.mjs --validate
```

## How It Works

1. Reads `core/VERSION.yaml` → `system.version` (the SSoT)
2. Scans `.agent/` directory for YAML, JSON, XML, and MD files
3. Replaces version strings using format-aware patterns
4. Preserves each file's formatting style (quoted/unquoted, v-prefix)

## When to Use

- After bumping version in `core/VERSION.yaml`
- Before release/deployment
- In CI pipeline to detect version drift (`--validate`)

## Version Bump Workflow

```
1. Edit core/VERSION.yaml → system.version: "X.Y.Z"
2. Run: /sync-version
3. Commit all changes
```

---

## 💾 SESSION SAVE

After completing this workflow:
1. Update `memory/CONTEXT_SNAPSHOT.md` - what changed, current status
2. Append summary to `memory/session.md`
