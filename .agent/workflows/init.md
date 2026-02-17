---
description: "✨ Initialize project with intelligent scaffolding, P0-P6 phases, and progress tracking"
skills: { required: [], contextual: [auto] }
---

# ✨ /init — Init Pro

> Intelligent Project Scaffolding
> 📚 30+ Templates • P0-P6 Phases • Auto-Detection

---

## INITIALIZATION FLOW

1. **DETECT** (Auto) — Parse user intent, detect existing project via HSA (`hsa_detect_stack`), check installed tools (`hsa_detect_environment`), infer stack from keywords
2. **CONFIGURE** — Select template, choose architecture → ⛔ STOP: confirm before scaffold
3. **SCAFFOLD** — Run init commands, create folder structure, generate base files
4. **CONFIGURE** — Setup linting/formatting, git hooks, create .env.example
5. **SYNC** — `hsa_check_changes` to update index after project creation
6. **PLAN** — Generate P0-P6 implementation plan, show next steps, offer to start coding

---

## TEMPLATE REGISTRY

### Backend / Systems

```yaml
# lang: architectures (default*) | init command | tools
go: standard*, clean, hexagonal, ddd | go mod init {module} | golangci-lint, air, wire
rust: cargo*, workspace, binary, library | cargo new {project} | clippy, rustfmt
cpp: cmake*, single, library, vcpkg | cmake -S . -B build | cmake, clang-format
c: make*, cmake, single | make init | gcc, clang, valgrind
java: maven*, gradle, spring, clean | mvn archetype:generate | maven, gradle, spotless
kotlin: android*, multiplatform, ktor, compose | gradle init | gradle, ktlint, detekt
scala: sbt*, mill, akka | sbt new scala/scala-seed.g8
csharp: clean*, mvvm, mvc, minimal, blazor | dotnet new webapi -n {project} | dotnet-format
fsharp: console*, web, giraffe | dotnet new console -lang F#
python: src*, flat, django, fastapi, flask | uv init {project} | ruff, mypy, uv
ruby: rails*, sinatra, gem, cli | rails new {project} | rubocop, bundler
php: laravel*, symfony, psr4, wordpress | composer create-project laravel/laravel {project} | php-cs-fixer
perl: module*, script, mojolicious | module-starter --module={project}
lua: standard*, love2d, neovim | — | luacheck, stylua
```

### Frontend Frameworks

```yaml
react: vite*, remix | npm create vite@latest {project} -- --template react-ts | eslint, vitest
nextjs: app*, pages, fullstack | npx create-next-app@latest {project} | eslint, turbopack
remix: indie*, classic | npx create-remix@latest {project}
vue: vite*, nuxt, pinia | npm create vue@latest {project} | eslint, vitest
nuxt: default*, layers, minimal | npx nuxi@latest init {project}
svelte: sveltekit*, vite | npm create svelte@latest {project}
angular: standalone*, modules | ng new {project}
solid: vite*, start | npm create solid@latest {project}
astro: default*, blog, docs | npm create astro@latest {project}
```

### Mobile

```yaml
swift: swiftpm*, ios, mvvm, tca | swift package init | swiftformat, swiftlint
kotlin_android: compose*, xml, multiplatform | Android Studio wizard | ktlint, detekt
dart: flutter*, console, package | flutter create {project} | dart_format
react_native: expo*, bare | npx create-expo-app {project}
```

### Infrastructure

```yaml
docker: multistage*, single, compose
kubernetes: helm*, kustomize, manifest | helm create {project}
terraform: aws*, gcp, azure, multi | terraform init
aws: cdk*, sam, terraform, serverless | cdk init app --language typescript
github_actions: node*, go, python, docker → .github/workflows/ci.yml
```

### Monorepo

```yaml
turborepo: npx create-turbo@latest | ⭐ recommended | caching, parallel, remote-cache
nx: npx create-nx-workspace@latest | affected, graph, generators
pnpm: pnpm init | pnpm-workspace.yaml
```

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

## P0-P6 PLAN TEMPLATE

```
P0: Environment — .env.example, secrets validation, .gitignore
P1: Foundation — Init project, install deps, setup linting, git hooks, README
P2: Core — Define entities/models, setup DI, implement core logic
P3: Features — Feature 1, Feature 2, Feature 3
P4: Integration — API/routes, error handling, logging, tracing
P5: Testing — Unit tests (80%+), integration tests, E2E
P6: Production — Dockerfile, CI/CD, health checks, deploy config
```

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

| Command                        | Description               |
| ------------------------------ | ------------------------- |
| `/init [stack]`                | Initialize with stack     |
| `/init ai [description]`       | AI-powered scaffolding    |
| `/init from [template]`        | Use template              |
| `/init templates`              | List templates            |
| `/init --level [1\|2\|3]`      | Basic/Standard/Enterprise |
| `/init --monorepo [turbo\|nx]` | Create monorepo           |
---

## SESSION SAVE

After completing this workflow:
1. Update `memory/CONTEXT_SNAPSHOT.md` - what changed, current status
2. Append summary to `memory/session.md`
