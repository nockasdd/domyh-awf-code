# NPM Package Publishing Guide

## Prerequisites

1. npm account with access to `@domyh` scope
2. Logged in: `npm login`
3. Build passed: `npm run build`

## Publishing Steps

### First-time Setup

```bash
# Create organization (if not exists)
npm org create domyh

# Add yourself as owner
npm org set domyh <your-npm-username> owner
```

### Publish

```bash
# 1. Bump version (if needed)
npm version patch  # or minor, major

# 2. Build
npm run build

# 3. Dry run (test publish)
npm pack

# 4. Publish
npm publish --access public

# 5. Verify
npm info @domyh/cli
```

### Version Strategy

- **Patch** (v5.5.x): Bug fixes, typo corrections
- **Minor** (5.x.0): New skills, new workflows, improvements
- **Major** (x.0.0): Breaking changes, architecture changes

## Package Contents

The published package includes:

```
@domyh/cli/
├── bin/cli.js          # CLI entry point
├── dist/               # Compiled TypeScript
├── skills/             # All 34 skills (Agent Skills format)
├── workflows/          # All 31 workflows (symlink to .agent/workflows)
├── templates/          # IDE config templates
├── core/               # Core configuration
├── package.json
└── README.md
```

## Post-Publish

1. Create GitHub release with tag `v5.5.0`
2. Update documentation
3. Announce on social media / Discord

## Unpublish (Emergency Only)

```bash
# Within 72 hours only
npm unpublish @domyh/cli@v5.5.0
```

---

_DOMYH Awesome Code v5.5 • Publishing Guide_
