# Component Versions

Per-workflow and per-skill version numbers. The system version lives in
`.agent/core/VERSION.yaml` → `system.version` — that is the only version the
CLI and the bump script read.

This table is reference material for humans. Nothing in the framework parses it,
so drift here does not break anything; the numbers document which generation of
each workflow the current release shipped.

## Workflows

| Workflow | Version | Notes |
|:---------|:--------|:------|
| `/ap` | 5.1 | Multi-expert consensus |
| `/code` | 3.2 | Auto test loop + security-first |
| `/debug` | 3.3 | Root cause tracing + defense-in-depth |
| `/plan` | 3.2 | Deep interview + auto phase generation |
| `/test` | 3.2 | TDD iron law + AI testing |
| `/modify` | 3.1 | AI-driven modernization |
| `/deploy` | 3.1 | GitOps + progressive delivery |
| `/refactor` | 3.1 | AI-assisted refactoring |
| `/review` | 3.1 | AI-assisted reviews |
| `/init` | 3.1 | AI scaffolding + 30+ templates |
| `/migrate` | 3.1 | Zero-downtime CDC |
| `/doc` | 3.1 | AI-optimized + auto API |
| `/generate` | 3.1 | Multi-modal + quality gates |
| `/perf` | 3.1 | Agent-aware profiling |
| `/upgrade` | 3.1 | Security-first updates |
| `/clean` | 2.2 | Dead code removal |
| `/monitor` | 3.1 | AI-powered observability |
| `/env` | 3.1 | Vault + multi-env sync |
| `/recap` | 3.2 | Session continuity |
| `/status` | 3.1 | Full health dashboard |
| `/help` | 2.1 | Context-aware + smart suggestions |
| `/suggest` | 3.1 | Git-aware suggestions |
| `/dev` | 3.1 | HMR 2025 + error overlay |
| `/revert` | 3.1 | Safe rollback + feature flags |
| `/orchestrate` | 3.1 | Fault-tolerant multi-agent |
| `/save` | 1.0 | Session persistence |
| `/lang` | 1.0 | i18n switching |
| `/search` | 1.1 | Semantic memory search |
| `/think` | 4.0 | 6 methods + 5 tiers + multi-mode |
| `/visualize` | 4.0 | Multi-platform + component mapping |

## Skills

| Skill | Version | Notes |
|:------|:--------|:------|
| `ui-ux-pro` | 5.0 | UI/UX Pro Max |
| `web-perf` | 5.0 | Web performance |

Unlisted workflows follow the framework default generation.
