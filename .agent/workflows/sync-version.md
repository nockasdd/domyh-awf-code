---
description: 🔄 Sync version from VERSION.yaml SSoT across all files
---

# /sync-version — Version Sync from SSoT

## Purpose

Sync the system version from `.agent/core/VERSION.yaml` (Single Source of Truth) across all project files that reference it.

## Steps

### 1. Read Current Version

```
Read .agent/core/VERSION.yaml → extract system.version
Display: Current version = X.Y.Z
```

### 2. Determine Target Version

**If user provides a version or bump type:**
- `patch` → X.Y.(Z+1)
- `minor` → X.(Y+1).0
- `major` → (X+1).0.0
- `X.Y.Z` → exact version

**If no argument:** Show current version and ask.

### 3. Run bump-version Script

```bash
node scripts/bump-version.mjs <bump> --dry-run   # Preview first
node scripts/bump-version.mjs <bump>              # Apply
```

### 4. Verify

- Confirm VERSION.yaml updated
- Check README.md, configs, and other files updated
- Report: N files updated, M replacements

## Examples

```
/sync-version patch        → 6.4.12 → 6.4.13
/sync-version minor        → 6.4.12 → 6.5.0
/sync-version 7.0.0        → 6.4.12 → 7.0.0
/sync-version              → Show current + ask
```

## Notes

- VERSION.yaml changelog section is protected (historical versions preserved)
- `.agent/` directory is intentionally skipped by bump script (VERSION.yaml updated separately)
- Always run `--dry-run` first to preview changes
