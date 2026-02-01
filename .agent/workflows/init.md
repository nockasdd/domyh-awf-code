---
name: init
trigger: ["/init", "khởi tạo", "create project", "new project"]
persona: architect
description: "✨ Initialize project with intelligent scaffolding, P0-P6 phases, and progress tracking"
---

# ✨ /init — Project Initialization Pro v3.0

> Intelligent Project Scaffolding
> 📚 30+ Templates • P0-P6 Phases • Auto-Detection

---

## 🔄 INITIALIZATION FLOW

```
User: /init [stack] [type]
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 1: DETECT (Auto)                 │
│ ▸ Parse user intent                     │
│ ▸ Detect existing project               │
│ ▸ Infer stack from keywords             │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 2: CONFIGURE                      │
│ ▸ Select template                       │
│ ▸ Choose architecture                   │
│ ▸ Set project options                   │
│ ⛔ STOP → Confirm before scaffold       │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 3: SCAFFOLD                       │
│ ▸ Run init commands                     │
│ ▸ Create folder structure               │
│ ▸ Generate base files                   │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 4: CONFIGURE                      │
│ ▸ Setup linting & formatting            │
│ ▸ Configure git hooks                   │
│ ▸ Create .env.example                   │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 5: GENERATE PLAN                  │
│ ▸ Create P0-P6 implementation plan      │
│ ▸ Show next steps                       │
│ ▸ Offer to start coding                 │
└─────────────────────────────────────────┘
```

---

## 📋 TEMPLATE REGISTRY (30+ Templates)

### 🔧 Backend Languages

```yaml
# ═══════════════════════════════════════════════════════════════
# SYSTEMS LANGUAGES
# ═══════════════════════════════════════════════════════════════

go:
  architectures: [standard, clean, hexagonal, ddd]
  default: standard
  init: "go mod init {module}"
  tools: [golangci-lint, air, wire]
  templates:
    standard: |
      {project}/
      ├── cmd/
      │   └── {name}/main.go
      ├── internal/
      │   ├── config/
      │   ├── handler/
      │   ├── service/
      │   └── repository/
      ├── pkg/
      ├── go.mod
      └── Makefile

rust:
  architectures: [cargo, workspace, binary, library]
  default: cargo
  init: "cargo new {project}"
  tools: [clippy, rustfmt, cargo-watch]
  templates:
    cargo: |
      {project}/
      ├── src/
      │   ├── main.rs
      │   └── lib.rs
      ├── Cargo.toml
      └── README.md

cpp:
  architectures: [cmake, single, library, vcpkg]
  default: cmake
  init: "cmake -S . -B build"
  tools: [cmake, clang-format, cppcheck]

c:
  architectures: [make, cmake, single]
  default: make
  init: "make init"
  tools: [gcc, clang, valgrind]

# ═══════════════════════════════════════════════════════════════
# JVM LANGUAGES
# ═══════════════════════════════════════════════════════════════

java:
  architectures: [maven, gradle, spring, clean]
  default: maven
  init: "mvn archetype:generate"
  tools: [maven, gradle, spotless]
  templates:
    spring: "spring init --type=maven-project"

kotlin:
  architectures: [android, multiplatform, ktor, compose]
  default: android
  init: "gradle init --type kotlin-application"
  tools: [gradle, ktlint, detekt]
  templates:
    android: "Android Studio wizard"
    ktor: "ktor new {project}"

scala:
  architectures: [sbt, mill, akka]
  default: sbt
  init: "sbt new scala/scala-seed.g8"

# ═══════════════════════════════════════════════════════════════
# .NET LANGUAGES
# ═══════════════════════════════════════════════════════════════

csharp:
  architectures: [clean, mvvm, mvc, minimal, blazor]
  default: clean
  init: "dotnet new webapi -n {project}"
  tools: [dotnet-format, resharper]
  templates:
    clean: "dotnet new webapi --use-controllers"
    blazor: "dotnet new blazorwasm"
    maui: "dotnet new maui"

fsharp:
  architectures: [console, web, giraffe]
  default: console
  init: "dotnet new console -lang F#"

# ═══════════════════════════════════════════════════════════════
# SCRIPTING LANGUAGES
# ═══════════════════════════════════════════════════════════════

python:
  architectures: [src, flat, django, fastapi, flask]
  default: src
  init: "uv init {project}" # 2025 standard
  tools: [ruff, mypy, uv, poetry]
  templates:
    fastapi: "fastapi-template"
    django: "django-admin startproject"
    src: |
      {project}/
      ├── src/{name}/
      │   ├── __init__.py
      │   └── main.py
      ├── tests/
      ├── pyproject.toml
      └── README.md

ruby:
  architectures: [rails, sinatra, gem, cli]
  default: rails
  init: "rails new {project}"
  tools: [rubocop, bundler]

php:
  architectures: [laravel, symfony, psr4, wordpress]
  default: laravel
  init: "composer create-project laravel/laravel {project}"
  tools: [php-cs-fixer, phpstan]
  templates:
    laravel: "laravel new {project}"
    symfony: "symfony new {project}"

perl:
  architectures: [module, script, mojolicious]
  default: module
  init: "module-starter --module={project}"

lua:
  architectures: [standard, love2d, neovim]
  default: standard
  tools: [luacheck, stylua]
```

### ⚛️ Frontend Frameworks

```yaml
# ═══════════════════════════════════════════════════════════════
# REACT ECOSYSTEM (2025)
# ═══════════════════════════════════════════════════════════════

react:
  architectures: [vite, cra-deprecated, remix]
  default: vite # CRA deprecated in 2024
  init: "npm create vite@latest {project} -- --template react-ts"
  tools: [eslint, prettier, vitest]
  note: "⚠️ create-react-app is deprecated. Use Vite or Next.js"

nextjs:
  architectures: [app, pages, fullstack]
  default: app # App Router is default
  init: "npx create-next-app@latest {project}"
  tools: [eslint, prettier, turbopack]
  options:
    - "--typescript"
    - "--tailwind"
    - "--eslint"
    - "--app" # App Router (default)
    - "--src-dir"
  templates:
    app: |
      {project}/
      ├── src/
      │   ├── app/
      │   │   ├── layout.tsx
      │   │   ├── page.tsx
      │   │   └── globals.css
      │   ├── components/
      │   └── lib/
      ├── public/
      ├── next.config.js
      └── package.json

remix:
  architectures: [indie, classic]
  default: indie
  init: "npx create-remix@latest {project}"

# ═══════════════════════════════════════════════════════════════
# VUE ECOSYSTEM
# ═══════════════════════════════════════════════════════════════

vue:
  architectures: [vite, nuxt, pinia]
  default: vite
  init: "npm create vue@latest {project}"
  tools: [eslint, prettier, vitest]

nuxt:
  architectures: [default, layers, minimal]
  default: default
  init: "npx nuxi@latest init {project}"
  tools: [eslint, prettier]

# ═══════════════════════════════════════════════════════════════
# OTHER FRAMEWORKS
# ═══════════════════════════════════════════════════════════════

svelte:
  architectures: [vite, sveltekit]
  default: sveltekit
  init: "npm create svelte@latest {project}"

angular:
  architectures: [standalone, modules]
  default: standalone
  init: "ng new {project}"

solid:
  architectures: [vite, start]
  default: vite
  init: "npm create solid@latest {project}"

astro:
  architectures: [default, blog, docs]
  default: default
  init: "npm create astro@latest {project}"
```

### 📱 Mobile Development

```yaml
swift:
  architectures: [swiftpm, ios, mvvm, tca]
  default: swiftpm
  init: "swift package init"
  tools: [swiftformat, swiftlint]
  templates:
    ios: "Xcode → New Project → App"
    tca: "TCA template"

kotlin_android:
  architectures: [compose, xml, multiplatform]
  default: compose
  init: "Android Studio wizard"
  tools: [ktlint, detekt]

dart:
  architectures: [flutter, console, package]
  default: flutter
  init: "flutter create {project}"
  tools: [dart_format, flutter_analyze]
  templates:
    flutter: "flutter create --org com.{org} {project}"

react_native:
  architectures: [expo, bare]
  default: expo
  init: "npx create-expo-app {project}"
  tools: [eslint, prettier]
```

### 🏗️ Infrastructure

```yaml
# ═══════════════════════════════════════════════════════════════
# CONTAINERS & ORCHESTRATION
# ═══════════════════════════════════════════════════════════════

docker:
  architectures: [multistage, single, compose]
  default: multistage
  templates:
    multistage: |
      FROM node:20-alpine AS builder
      WORKDIR /app
      COPY package*.json ./
      RUN npm ci
      COPY . .
      RUN npm run build

      FROM node:20-alpine
      WORKDIR /app
      COPY --from=builder /app/dist ./dist
      CMD ["node", "dist/index.js"]

kubernetes:
  architectures: [helm, kustomize, manifest]
  default: helm
  init: "helm create {project}"

terraform:
  architectures: [aws, gcp, azure, multi]
  default: aws
  init: "terraform init"

# ═══════════════════════════════════════════════════════════════
# CLOUD PLATFORMS
# ═══════════════════════════════════════════════════════════════

aws:
  architectures: [cdk, sam, terraform, serverless]
  default: cdk
  init: "cdk init app --language typescript"

gcp:
  architectures: [terraform, pulumi, gcloud]
  default: terraform

azure:
  architectures: [bicep, terraform, arm]
  default: bicep

# ═══════════════════════════════════════════════════════════════
# CI/CD
# ═══════════════════════════════════════════════════════════════

github_actions:
  templates: [node, go, python, docker]
  default: node
  files:
    - .github/workflows/ci.yml
    - .github/workflows/deploy.yml

gitlab_ci:
  templates: [node, docker]
  files:
    - .gitlab-ci.yml
```

### 📦 Monorepo Tools

```yaml
turborepo:
  init: "npx create-turbo@latest"
  default: ⭐ Recommended
  features: [caching, parallel, remote-cache]

nx:
  init: "npx create-nx-workspace@latest"
  features: [affected, graph, generators]

pnpm_workspaces:
  init: "pnpm init"
  config: "pnpm-workspace.yaml"

lerna:
  init: "npx lerna init"
  note: "Consider Turborepo for new projects"
```

---

## 🎯 AUTO-DETECTION

### Keyword Mapping:

| User Input    | → Stack + Architecture |
| ------------- | ---------------------- |
| "go api"      | Go + standard          |
| "next app"    | Next.js + app          |
| "react app"   | React + vite           |
| "fastapi"     | Python + fastapi       |
| "spring boot" | Java + spring          |
| "flutter app" | Dart + flutter         |
| "monorepo"    | Turborepo              |
| "wpf"         | C# + mvvm              |
| "blazor"      | C# + blazor            |

### File Detection:

| File Found     | → Stack   |
| -------------- | --------- |
| go.mod         | Go        |
| package.json   | Node/TS   |
| Cargo.toml     | Rust      |
| pyproject.toml | Python    |
| \*.csproj      | C#        |
| pubspec.yaml   | Dart      |
| turbo.json     | Turborepo |

---

## 📋 P0-P6 IMPLEMENTATION PLAN

```markdown
# {Project} — Implementation Plan

## Info

Stack: {lang} | Arch: {pattern} | Type: {type}

## Structure

{generated_tree}

## Phases

### P0: Environment ⏱️

- [ ] Create .env.example with all vars
- [ ] Setup secrets validation (envalid/zod)
- [ ] Configure .gitignore

### P1: Foundation ⏱️

- [ ] Initialize project ({init_cmd})
- [ ] Install dependencies
- [ ] Setup linting ({lint_tool})
- [ ] Configure git hooks (husky/pre-commit)
- [ ] Create README.md

### P2: Core ⏱️

- [ ] Define entities/models
- [ ] Setup DI container ({di_tool})
- [ ] Implement core business logic

### P3: Features ⏱️

- [ ] Feature 1: {feature_1}
- [ ] Feature 2: {feature_2}
- [ ] Feature 3: {feature_3}

### P4: Integration ⏱️

- [ ] API/Routes setup
- [ ] Error handling
- [ ] Logging ({log_tool})
- [ ] Tracing (OpenTelemetry)

### P5: Testing ⏱️

- [ ] Unit tests (80%+ coverage)
- [ ] Integration tests
- [ ] E2E tests (if needed)

### P6: Production ⏱️

- [ ] Dockerfile (multistage)
- [ ] CI/CD pipeline ({ci_tool})
- [ ] Health checks
- [ ] Deploy config

## Commands

| Action | Command      |
| ------ | ------------ |
| Build  | {build_cmd}  |
| Dev    | {dev_cmd}    |
| Test   | {test_cmd}   |
| Lint   | {lint_cmd}   |
| Deploy | {deploy_cmd} |
```

---

## 🔧 CROSS-CUTTING PATTERNS

### Linting by Language:

| Language   | Linter        | Formatter          |
| ---------- | ------------- | ------------------ |
| Go         | golangci-lint | gofmt              |
| Rust       | clippy        | rustfmt            |
| Python     | ruff          | ruff format        |
| TypeScript | eslint        | prettier           |
| Java       | checkstyle    | google-java-format |
| C#         | dotnet-format | -                  |
| Ruby       | rubocop       | -                  |
| PHP        | php-cs-fixer  | -                  |

### Dependency Injection:

| Language   | Tool                |
| ---------- | ------------------- |
| Go         | wire, fx            |
| Python     | dependency-injector |
| TypeScript | tsyringe, inversify |
| Java       | Spring              |
| Kotlin     | Hilt, Koin          |
| C#         | Microsoft.DI        |

### Observability Stack:

| Category | Tools                   |
| -------- | ----------------------- |
| Logging  | slog, zap, pino, loguru |
| Tracing  | OpenTelemetry           |
| Metrics  | Prometheus              |
| APM      | Sentry, Datadog         |

---

## ⚙️ TOKEN OPTIMIZATION

```yaml
token_saving:
  # Auto-detect, minimal prompts
  - Infer stack from keywords
  - Use best defaults
  - Only ask truly unknown info

  # Efficient scaffolding
  - Run init commands directly
  - Generate structure once
  - Batch file creation
```

---

## 📋 BEHAVIOR RULES

| Input                      | Action                       |
| -------------------------- | ---------------------------- |
| `/init go api`             | ✅ PROCEED: Go + standard    |
| `/init nextjs`             | ✅ PROCEED: Next.js + app    |
| `/init monorepo`           | ✅ PROCEED: Turborepo        |
| `/init`                    | ❓ ASK: lang + purpose       |
| `create fastapi with auth` | ✅ PROCEED: Python + fastapi |

---

## 🤖 AI-POWERED SCAFFOLDING (v3.1)

```yaml
ai_scaffolding:
  description: "Natural language project creation"

  capabilities:
    analyze_description: "Parse natural language project request"
    suggest_stack: "Recommend optimal tech stack"
    generate_structure: "Create directory + boilerplate"
    configure_tools: "Setup linting, testing, CI"

  progressive_disclosure:
    level_1:
      name: "Basic"
      description: "Just the essentials"
      includes: ["src/", "README.md", "package.json"]

    level_2:
      name: "Standard"
      description: "Common addons"
      includes: ["tests/", "eslint", "prettier", ".env.example"]

    level_3:
      name: "Enterprise"
      description: "Full production setup"
      includes: ["CI/CD", "Docker", "docs/", "monitoring"]

  commands:
    ai_create: "/init ai [description]"
    example: "/init ai 'REST API for blog with user auth and posts'"

  workflow:
    1: "Parse natural language description"
    2: "Identify tech requirements"
    3: "Suggest stack (confirm with user)"
    4: "Generate structure based on level"
    5: "Configure development tools"
```

---

## 🔧 TEMPLATE ENGINE 2025 (v3.1)

```yaml
template_engine:
  description: "Modern template-based scaffolding"

  sources:
    local: "~/.agent/templates/"
    github: "GitHub template repos"
    organization: "Company-specific standards"
    registry: "DOMYH template registry"

  customization:
    prompts:
      interactive: "Ask during scaffold"
      config_file: "Read from .init.yaml"
      cli_args: "Pass via command line"

    variables:
      built_in: ["project_name", "author", "year", "license"]
      custom: "User-defined in template"

    hooks:
      pre_create: "Validate requirements"
      post_create: "Run setup scripts"

  monorepo_support:
    turborepo: "pnpm workspaces + Turbo"
    nx: "Nx workspace with plugins"
    lerna: "Lerna with npm/yarn"
    pnpm: "pnpm workspaces only"

  commands:
    from_template: "/init from [template_url]"
    list_templates: "/init templates"
    create_template: "/init template create"

  examples:
    - "/init from gh:company/api-template"
    - "/init from local:fastapi-clean"
    - "/init from https://github.com/org/template"
```

---

## 🔧 SUB-COMMANDS

| Command                        | Description              |
| ------------------------------ | ------------------------ |
| `/init [stack]`                | Initialize with stack    |
| `/init ai [description]`       | AI-powered scaffolding   |
| `/init from [template]`        | Use template             |
| `/init templates`              | List available templates |
| `/init --level [1\|2\|3]`      | Set disclosure level     |
| `/init --monorepo [turbo\|nx]` | Create monorepo          |

---

_DOMYH Awesome Code v4.3 • Init Pro v3.1 • AI Scaffolding + 30+ Templates_
