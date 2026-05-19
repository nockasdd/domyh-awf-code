<!-- HSA Docs Template — Convention for local documentation files -->
<!-- Save as: docs/{library}@{version}.md or docs/{library}.md (latest) -->

---
library: {library-name}
version: {major-version}
latest: {true|false}
category: {frontend|backend|database|css|testing|api-tool|infra|other}
official_docs: {url}
last_updated: {YYYY-MM-DD}
---

# {Library} v{Version}

> {One-line description of this library version}
> ⚠️ This is LEGACY. For latest, use `{library}.md`.

## Version Comparison
<!-- MANDATORY — helps agent disambiguate versions instantly -->
| Feature | v{this} | v{latest} |
|:--------|:--------|:----------|
| Config  | ...     | ...       |

## Installation
<!-- MANDATORY — exact install commands with version pinning -->

```bash
npm install {library}@{version}
```

## Configuration
<!-- MANDATORY — complete config example, annotated -->

## Core API
<!-- MANDATORY — most-used APIs with params, types, return values -->

## Common Patterns
<!-- RECOMMENDED — real-world usage examples -->

## Gotchas & Breaking Changes
<!-- CRITICAL — things that trip up agents and humans -->
<!-- Use ⚠️ markers for version-specific warnings -->

## Migration
<!-- MANDATORY if not latest — checklist to upgrade to next version -->

<!--
BM25 DESIGN RULES:
- H1 = library name (root search anchor)
- H2 = feature category, add (vN) suffix for version matching
- Code:prose ratio ≥ 70:30
- Use ⚠️ diff notes for version disambiguation
- Keep 5-30KB per file, H2 sections ~50 lines each
-->
