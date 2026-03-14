---
description: "✨ Initialize project with intelligent scaffolding, P0-P6 phases, and progress tracking"
skills: { required: [coding-rules], contextual: [auto] }
success_criteria: "Project scaffolded, build passes, P0-P6 plan generated"
---

# ✨ /init — Init Pro

> Intelligent Project Scaffolding
> 📚 30+ Templates • P0-P6 Phases • Auto-Detection • Architecture Gate • Quality Standards

---

## INITIALIZATION FLOW

1. **DETECT + CLASSIFY** (Auto)
   - Parse user intent, detect existing project via HSA (`hsa_detect`), check installed tools (`hsa_detect`)
   - **Existing Project Guard**:
     - IF `hsa_detect` finds existing project (package.json, go.mod, Cargo.toml, etc.):
       → ⛔ WARN: "Dự án đã tồn tại tại thư mục này."
       → Offer: (1) Reinitialize (overwrite), (2) Switch to `/modify`, (3) Cancel
     - IF empty directory → proceed normally
   - Infer stack from keywords
   - **Complexity Scoring** — Evaluate via `complexity-scoring.yaml` (H1-H5):
     - Score < 5 → Developer persona, standard flow
     - Score 5-7 → Suggest orchestration to user
     - Score ≥ 8 (multi-stack/system) → Auto-activate Orchestrator persona
   - **Runtime Validation** — Verify minimum versions (Node ≥ 20, Go ≥ 1.22, Python ≥ 3.12, Rust ≥ 1.80, etc.)
   - **MCP**: `hsa_detect`, `hsa_detect`, `hsa_session("init project {name}")`

2. **ARCHITECTURE SELECTION** (Gate ⛔)
   - **Load architecture data**: `hsa_search("architecture patterns {stack}")`
   - **Present 2-3 options** with trade-offs (ADR format → Architect persona behavior):
     - Architecture name + description
     - Best for (use case match)
     - Testability + complexity rating
     - Full directory tree preview from `framework-directories.yaml`
   - **SOLID compliance** per language from `solid-principles.yaml`:
     - Show which SOLID principles the architecture enforces
     - Highlight DI mechanism for selected stack
   - **MCP**: `hsa_search("framework directories {stack}")`, `hsa_search("solid principles {language}")`
   - → ⛔ STOP: User confirms architecture + directory structure before scaffold

3. **SCAFFOLD** — Run init commands, create folder structure, generate base files
   - Apply architecture-specific structure from Step 2
   - Generate ADR-001: `docs/adr/001-architecture-decision.md` (chosen pattern + reasoning)
   - **MCP**: `hsa_session("scaffold completed")`

4. **SETUP** — Setup linting/formatting, git hooks, create .env.example
   - Load naming conventions: `hsa_search("naming conventions {language}")`
   - Setup language-specific linter + formatter from CROSS-CUTTING table
   - Setup DI tool matching architecture choice
   - **MCP**: `hsa_search("naming conventions {lang}")`

5. **SYNC** — `hsa_check_changes` to update index after project creation
   - **MCP**: `hsa_check_changes`, `hsa_feedback` on key files, `hsa_session("project: {name}, stack: {stack}, arch: {pattern}")`

6. **PLAN + UAT** — Generate P0-P6 implementation plan with acceptance criteria
   - Map each phase to workflow command (see LIFECYCLE HANDOFF)
   - Generate quality checklist (SOLID/DRY/KISS/YAGNI/12-Factor)
   - Show next recommended command
   - **MCP**: `hsa_session("P0-P6 plan generated")`

---

## TEMPLATE REGISTRY
> Read `workflows/data/init-frameworks.yaml` for framework mappings, supported architectures, and init commands.

---

## AUTO-DETECTION

| User Input    | → Stack          |
| ------------- | ---------------- |
| "go api"      | Go + standard    |
| "next app"    | Next.js + app    |
| "react app"   | React + vite     |
| "fastapi"     | Python + fastapi |
| "spring boot" | Java + spring    |
| "flutter app" | Dart + flutter   |
| "monorepo"    | Turborepo        |

| File Found     | → Stack |
| -------------- | ------- |
| go.mod         | Go      |
| package.json   | Node/TS |
| Cargo.toml     | Rust    |
| pyproject.toml | Python  |
| \*.csproj      | C#      |
| pubspec.yaml   | Dart    |

---

## P0-P6 PLAN TEMPLATE (with Acceptance Criteria)

```yaml
P0_environment:
  status: "(Partially completed during /init Step 4 — verify with ACs below)"
  tasks: [".env.example", ".gitignore", "secrets validation"]
  acceptance_criteria:
    - "AC-P0-01: Setup runs on clean machine in < 5 minutes"
    - "AC-P0-02: All required env vars documented in .env.example"
    - "AC-P0-03: .gitignore covers language-specific ignores"
  next_workflow: "/env"

P1_foundation:
  status: "(Completed during /init Steps 3-4 — verify with ACs below)"
  tasks: ["init project", "install deps", "linting", "git hooks", "README"]
  acceptance_criteria:
    - "AC-P1-01: `build` succeeds with zero errors"
    - "AC-P1-02: Linter passes with zero warnings"
    - "AC-P1-03: Directory follows selected architecture pattern"
    - "AC-P1-04: README has setup + run instructions"
  next_workflow: "/dev"

P2_core:
  tasks: ["entities/models", "DI container", "core logic"]
  acceptance_criteria:
    - "AC-P2-01: Core entities have unit tests (80%+ coverage)"
    - "AC-P2-02: SOLID principles verified (no god classes)"
    - "AC-P2-03: Functions under 50 lines, classes under 300 lines"
  next_workflow: "/code [core-logic]"

P3_features:
  tasks: ["Feature 1", "Feature 2", "Feature 3"]
  acceptance_criteria:
    - "AC-P3-01: Each feature has acceptance criteria matching user story"
    - "AC-P3-02: Each feature has unit + integration tests"
    - "AC-P3-03: No feature introduces circular dependencies"
  next_workflow: "/feature [name]"

P4_integration:
  tasks: ["API/routes", "error handling", "logging", "tracing"]
  acceptance_criteria:
    - "AC-P4-01: All API endpoints documented (OpenAPI/Swagger)"
    - "AC-P4-02: Error responses follow RFC 7807 format"
    - "AC-P4-03: Structured logging with correlation IDs"
  next_workflow: "/code add [integration]"

P5_testing:
  tasks: ["unit tests (80%+)", "integration tests", "E2E"]
  acceptance_criteria:
    - "AC-P5-01: Unit test coverage ≥ 80%"
    - "AC-P5-02: Integration tests for all external dependencies"
    - "AC-P5-03: E2E tests cover critical user flows"
  next_workflow: "/test then /e2e"

P6_production:
  tasks: ["Dockerfile", "CI/CD", "health checks", "deploy config"]
  acceptance_criteria:
    - "AC-P6-01: Docker builds in < 5 min, image < 500MB"
    - "AC-P6-02: CI pipeline: lint → test → build → deploy"
    - "AC-P6-03: Health check endpoint responds within 2s"
  next_workflow: "/deploy"
```

---

## QUALITY STANDARDS

### SOLID Compliance (per language — from `coding-rules/data/solid-principles.yaml`)

| Principle | Description | Agent Check |
|-----------|-------------|-------------|
| **S** — Single Responsibility | Each file/module has one purpose | Architecture pattern enforces |
| **O** — Open/Closed | Extensible via interfaces/traits, not modification | DI + plugin system |
| **L** — Liskov Substitution | Subtypes honor base contracts | Interface compliance review |
| **I** — Interface Segregation | Small, focused interfaces (not fat APIs) | Code review check |
| **D** — Dependency Inversion | High-level depends on abstractions | DI container setup |

### Additional Principles

| Principle | Description | Enforcement |
|-----------|-------------|-------------|
| **DRY** | No duplicated logic | `hsa_search` to find existing code first |
| **KISS** | Simple over clever | Architecture complexity ≤ project needs |
| **YAGNI** | No premature features | P0-P6 scope gate |
| **12-Factor** | Cloud-native config, deps, processes | .env + Dockerfile + CI |
| **Clean Code** | Naming, functions < 50L, no magic numbers | Linter + quality.yaml |

---

## CROSS-CUTTING

| Language | Linter        | Formatter          | DI Tool             |
| -------- | ------------- | ------------------ | ------------------- |
| Go       | golangci-lint | gofmt              | wire, fx            |
| Rust     | clippy        | rustfmt            | —                   |
| Python   | ruff          | ruff format        | dependency-injector |
| TS       | eslint        | prettier           | tsyringe, inversify |
| Java     | checkstyle    | google-java-format | Spring              |
| C#       | dotnet-format | —                  | Microsoft.DI        |

---

## SUB-COMMANDS

| Command                        | Description                  |
| ------------------------------ | ---------------------------- |
| `/init [stack]`                | Initialize with stack        |
| `/init ai [description]`       | AI-powered scaffolding       |
| `/init from [template]`        | Use template                 |
| `/init templates`              | List templates               |
| `/init --level [1\|2\|3]`      | Basic/Standard/Enterprise    |
| `/init --monorepo [turbo\|nx]` | Create monorepo              |
| `/init system [desc]`          | Multi-service system (→ Orchestrator) |
| `/init fullstack`              | Backend + Frontend (default arch)     |

---

## PROJECT LIFECYCLE — WORKFLOW HANDOFF

After `/init` completes, suggest the next workflow based on the P0-P6 plan:

| Phase | Workflow | Command | When |
|-------|----------|---------|------|
| P0 | /env | `/env` | Environment & secrets |
| P1 | /dev | `/dev` | Validate build + deps |
| P2 | /code or /scaffold | `/code [core-logic]` or `/scaffold module [name]` | Core implementation |
| P3 | /feature | `/feature [name]` | Feature-by-feature |
| P4 | /code | `/code add [integration]` | API routes, error handling |
| P5 | /test + /e2e | `/test` then `/e2e` | Test coverage |
| P6 | /deploy | `/deploy` | Production readiness |

### Multi-Project (Monorepo)

If user requests multiple stacks (e.g., "Go backend + Next.js frontend"):
1. → Auto-activate **Orchestrator** persona (complexity ≥ 8)
2. → Create monorepo structure (turborepo/nx/pnpm)
3. → Run `/init` for each package sequentially
4. → Wire shared configs (tsconfig, eslint, docker-compose)
5. → Show unified P0-P6 plan across all packages

---

## RELATED WORKFLOWS

| Before /init | After /init |
|-------------|-------------|
| — (fresh project) | `/env` → `/dev` → `/scaffold` → `/code` → `/feature` → `/test` → `/deploy` |

---

## REFLECTION CHECKPOINT

⛔ **MANDATORY** — Execute before completing this workflow (SESSION_005):

1. **VERIFY** — Does output meet success_criteria (see YAML frontmatter)?
2. **PERSIST** (if HSA available — preferred, 1 tool call):
   - `hsa_session({action:'persist', task_summary:'[workflow] [summary]', files_touched:[...]})`
   - If key decision → `hsa_session({action:'anchor', content:'[decision]', category:'decision'})`
3. **PERSIST** (if HSA unavailable — manual fallback):
   - Append task summary to `memory/session.md`
   - If last task → Update `memory/CONTEXT_SNAPSHOT.md`

