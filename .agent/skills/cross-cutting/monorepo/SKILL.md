---
name: monorepo
version: "7.0.0"
category: cross-cutting
---

# 📦 Monorepo Management

> Patterns for multi-package repository management
> 📚 Nx • Turborepo • pnpm Workspaces • Changesets

---

## Quick Reference

| Tool                | Best For                  | Package Manager | Remote Cache |
| ------------------- | ------------------------- | --------------- | :----------: |
| **Nx**              | Large enterprise, plugins | Any             | ✅ Nx Cloud  |
| **Turborepo**       | Simple, fast builds       | Any             |  ✅ Vercel   |
| **pnpm workspaces** | Lightweight, npm-like     | pnpm            |      ❌      |
| **Lerna**           | Legacy, npm publishing    | npm/yarn        |      ❌      |

---

## Monorepo vs Polyrepo

| Aspect          | Monorepo                    | Polyrepo          |
| --------------- | --------------------------- | ----------------- |
| Code sharing    | ✅ Easy                     | ⚠️ Via packages   |
| Atomic changes  | ✅ Single commit            | ❌ Multi-repo PRs |
| CI complexity   | ⚠️ Needs affected detection | ✅ Simple         |
| Team autonomy   | ⚠️ Shared codebase          | ✅ Independent    |
| Dependency mgmt | ✅ Centralized              | ⚠️ Version matrix |

---

## Nx Workspace

```bash
# Create Nx workspace
npx create-nx-workspace@latest my-org --preset=ts

# Add apps
nx g @nx/next:app my-app
nx g @nx/node:app api

# Add libraries
nx g @nx/js:lib shared-types
nx g @nx/react:lib ui-components

# Run affected
nx affected --target=build
nx affected --target=test
```

---

## Turborepo

```json
// turbo.json
{
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**"]
    },
    "test": {
      "dependsOn": ["build"]
    },
    "lint": {}
  }
}
```

```bash
turbo run build --filter=@org/web
turbo run test --affected
```

---

## Directory Structure

```
monorepo/
├── apps/
│   ├── web/          # Next.js frontend
│   ├── api/          # Node.js backend
│   └── mobile/       # React Native
├── packages/
│   ├── ui/           # Shared UI components
│   ├── config/       # Shared configs (ESLint, TS)
│   └── utils/        # Shared utilities
├── nx.json / turbo.json
├── pnpm-workspace.yaml
└── package.json
```

---

## HSA Integration

| Query                              | Data File                 |
| ---------------------------------- | ------------------------- |
| `nx generators executors affected` | `nx-patterns.yaml`        |
| `turborepo pipeline cache`         | `turborepo-patterns.yaml` |
| `pnpm workspace npm yarn`          | `workspace-patterns.yaml` |
| `affected ci change detection`     | `ci-cd-strategies.yaml`   |
| `changesets conventional commits`  | `versioning.yaml`         |

---

_DOMYH Awesome Code • Monorepo Management_
