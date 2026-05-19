---
library: turborepo
version: latest
latest: true
category: infra
official_docs: https://turborepo.dev/docs
last_updated: 2026-03-20
last_checked: 2026-03-21
source: turborepo.dev + curated
---

# Turborepo v2

> Turborepo — High-performance build system for JavaScript/TypeScript monorepos.
> Incremental builds, remote caching, task parallelization.
> Docs: https://turborepo.dev

## Installation

```bash
# New monorepo
npx create-turbo@latest my-monorepo

# Add to existing project
npm install -D turbo
```

## Project Structure

```
my-monorepo/
├── apps/
│   ├── web/          # Next.js app
│   └── api/          # Express/Hono API
├── packages/
│   ├── ui/           # Shared UI components
│   ├── config/       # Shared configs (eslint, tsconfig)
│   └── utils/        # Shared utilities
├── turbo.json
├── package.json
└── pnpm-workspace.yaml  (or npm workspaces)
```

## turbo.json

```jsonc
{
    "$schema": "https://turbo.build/schema.json",
    "tasks": {
        "build": {
            "dependsOn": ["^build"],       // run deps' build first
            "outputs": [".next/**", "dist/**"],
            "env": ["NODE_ENV"]
        },
        "dev": {
            "cache": false,                // don't cache dev server
            "persistent": true             // long-running process
        },
        "lint": {
            "dependsOn": ["^build"]
        },
        "test": {
            "dependsOn": ["build"],
            "outputs": ["coverage/**"]
        },
        "check-types": {
            "dependsOn": ["^build"]
        }
    }
}
```

## Commands

```bash
turbo build                        # build all packages
turbo dev                          # dev all packages
turbo build --filter=web           # build only 'web' app
turbo build --filter=web...        # build 'web' + its dependencies
turbo build --filter='./apps/*'    # build all apps
turbo lint test --parallel         # run lint and test in parallel
turbo build --dry-run              # show what would run
turbo build --graph                # visualize task graph
turbo build --summarize            # performance summary
```

## Remote Caching

```bash
# Vercel (built-in)
npx turbo login
npx turbo link

# Self-hosted
turbo build --api="https://cache.example.com" --token="xxx"
```

## Package Configuration

```json
// apps/web/package.json
{
    "name": "web",
    "dependencies": {
        "ui": "workspace:*",
        "utils": "workspace:*"
    }
}
```

```yaml
# pnpm-workspace.yaml
packages:
  - "apps/*"
  - "packages/*"
```

## Gotchas

⚠️ **`^` prefix**: `"dependsOn": ["^build"]` means "build my deps first". Without `^` = same package.

⚠️ **`outputs`**: Must list build outputs for caching. Miss an output = stale cache.

⚠️ **`persistent: true`**: Required for `dev`, `start`, watch-mode tasks.

⚠️ **`cache: false`**: Use for non-deterministic tasks (dev servers, deploys).

⚠️ **env vars**: List in `env` to invalidate cache when env changes.

⚠️ **Filter syntax**: `--filter=web` (exact), `--filter=web...` (with deps), `--filter=...web` (with dependents).

⚠️ **Vercel integration**: Automatic remote caching on Vercel. Free tier includes it.
