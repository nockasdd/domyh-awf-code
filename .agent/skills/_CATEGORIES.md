# 📂 Skill Category Taxonomy

> Two-level classification convention

## Filesystem Categories (8 directories)

Physical grouping in `.agent/skills/`:

| Directory | Count | Purpose |
|---|---|---|
| `core/` | 6 | Security, API design, auth, error handling, logging, observability |
| `languages/` | 28 | Programming language skills |
| `frameworks/` | 9 | React, Vue, Next.js, Angular, Nuxt, Svelte, Flutter, React Native, Streamlit |
| `devops/` | 7 | Docker, K8s, AWS, CI/CD, Terraform, Azure, GCP |
| `cross-cutting/` | 22 | Database, testing, Tailwind, Electron, Bun, Deno, etc. |
| `tooling/` | 5 | MCP, IDE extension, CLI dev, API protocols, Browser agent |
| `ai-ml/` | 8 | AI agents, vector search, prompt engineering, RAG, Gemini, ML pipelines |
| `governance/` | 8 | Drift prevention, session governance, context integrity, progressive escalation |

## META.yaml `category:` (Semantic Sub-tags)

Each `META.yaml` has a `category:` field that provides **semantic sub-classification** within
its filesystem parent. This is **by design** and does NOT need to match the directory name.

Example: `cross-cutting/tailwind/META.yaml` has `category: styling` — because "styling"
is more useful for semantic routing than the broad "cross-cutting" directory name.

### Common Sub-tags

| Sub-tag | Used by | Parent dir |
|---|---|---|
| `styling` | tailwind, domyh-design | cross-cutting |
| `runtime` | bun, deno | cross-cutting |
| `testing` | testing, tdd-workflow, playwright | cross-cutting |
| `data` | database, sql | cross-cutting |
| `messaging` | real-time, event-driven | cross-cutting |
| `security` | security | core |

> The `category:` field is used by the semantic engine for finer-grained skill matching.
> The filesystem directory is used for organizational structure and manifest registration.

---

_DOMYH Awesome Code • Skill Category Taxonomy_
