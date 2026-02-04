---
name: modify
trigger:
  ["/modify", "/fix-project", "sửa project", "update project", "fix existing"]
persona: developer
description: "🔧 Fix existing project: detect stack → analyze issues → plan → execute → verify"
---

# 🔧 /modify — Modify Pro v3.1

> AI-Powered Legacy Modernization & Issue Resolution
> 📚 30+ Languages • Technical Debt • Automated Analysis

---

## 🔄 MODIFICATION FLOW

```
User: /modify [options]
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 1: DETECT (Auto)                 │
│ ▸ Detect project stack                  │
│ ▸ Identify architecture pattern         │
│ ▸ Map project structure                 │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 2: ANALYZE                        │
│ ▸ Scan for issues                       │
│ ▸ Detect technical debt                 │
│ ▸ Prioritize by severity                │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 3: PLAN                           │
│ ▸ Generate fix plan                     │
│ ▸ Estimate effort                       │
│ ⛔ STOP → Confirm scope                 │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 4: EXECUTE                        │
│ ▸ Apply fixes                           │
│ ▸ Document changes                      │
│ ▸ Update tests                          │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 5: VERIFY                         │
│ ▸ Run lint/type check                   │
│ ▸ Run tests                             │
│ ▸ Verify build                          │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 6: REPORT                         │
│ ▸ Summary of changes                    │
│ ▸ Technical debt score                  │
│ ▸ Suggested next steps                  │
└─────────────────────────────────────────┘
```

---

## 🎯 COMMANDS

| Command              | Description         | Focus                |
| -------------------- | ------------------- | -------------------- |
| `/modify`            | Full analysis & fix | All issues           |
| `/modify --security` | Security focus      | Vulnerabilities only |
| `/modify --deps`     | Dependencies        | Outdated/vulnerable  |
| `/modify --quality`  | Code quality        | Lint, types, smells  |
| `/modify --perf`     | Performance         | Bottlenecks, N+1     |
| `/modify --quick`    | P0 only, no confirm | Critical fixes       |
| `/modify ./src`      | Specific path       | Directory scope      |

---

## 📋 PHASE 1: DETECT

### Stack Detection (30+ Languages):

```yaml
# ═══════════════════════════════════════════════════════════════
# DETECTION SIGNALS
# ═══════════════════════════════════════════════════════════════

detection:
  go:
    files: [go.mod, go.sum, "*.go"]
    framework: [gin, echo, fiber, chi]

  rust:
    files: [Cargo.toml, Cargo.lock]
    framework: [actix, axum, rocket]

  python:
    files: [pyproject.toml, requirements.txt, setup.py]
    framework: [django, fastapi, flask]

  typescript:
    files: [tsconfig.json, package.json]
    framework: [express, nestjs, next, nuxt]

  javascript:
    files: [package.json, "*.js"]
    framework: [express, react, vue]

  java:
    files: [pom.xml, build.gradle, "*.java"]
    framework: [spring, quarkus, micronaut]

  kotlin:
    files: [build.gradle.kts, "*.kt"]
    framework: [spring, ktor]

  csharp:
    files: ["*.csproj", "*.sln"]
    framework: [aspnet, blazor, maui]

  php:
    files: [composer.json, "*.php"]
    framework: [laravel, symfony]

  ruby:
    files: [Gemfile, "*.rb"]
    framework: [rails, sinatra]

  swift:
    files: [Package.swift, "*.swift"]
    framework: [vapor, swiftui]

  dart:
    files: [pubspec.yaml, "*.dart"]
    framework: [flutter]
```

### Detection Output:

```
📦 PROJECT DETECTED

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Project: my-api
Stack: Go 1.22 + Gin
Architecture: Clean Architecture
Database: PostgreSQL + GORM

Structure:
├── cmd/ (entry points)
├── internal/
│   ├── handler/
│   ├── service/
│   └── repository/
├── pkg/
└── tests/

Stats:
├── Files: 127 (.go)
├── Lines: 15,847
├── Packages: 23
├── Dependencies: 45
└── Last Modified: 2 days ago

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 📋 PHASE 2: ANALYZE

### Issue Categories:

```yaml
analysis_categories:
  # ═══════════════════════════════════════════════════════════════
  # SECURITY (P0)
  # ═══════════════════════════════════════════════════════════════

  security:
    checks:
      - Hardcoded secrets
      - SQL injection
      - XSS vulnerabilities
      - Insecure dependencies
      - Missing authentication
      - Insufficient authorization
    tools:
      go: [gosec, staticcheck]
      python: [bandit, safety]
      javascript: [npm audit, snyk]
      java: [spotbugs, owasp-dependency-check]
      csharp: [security-code-scan]

  # ═══════════════════════════════════════════════════════════════
  # DEPENDENCIES (P0-P1)
  # ═══════════════════════════════════════════════════════════════

  dependencies:
    checks:
      - Outdated packages
      - Vulnerable versions
      - Unused dependencies
      - License compliance
    tools:
      go: [go mod tidy, govulncheck]
      python: [pip-audit, pipdeptree]
      javascript: [npm outdated, npx depcheck]
      java: [mvn versions:display-dependency-updates]
      rust: [cargo audit, cargo outdated]

  # ═══════════════════════════════════════════════════════════════
  # CODE QUALITY (P1-P2)
  # ═══════════════════════════════════════════════════════════════

  code_quality:
    checks:
      - Lint errors
      - Type errors
      - Dead code
      - Code smells
      - Complexity metrics
    tools:
      go: [golangci-lint]
      python: [ruff, mypy]
      javascript: [eslint, tsc]
      java: [checkstyle, pmd]
      csharp: [dotnet format]
      rust: [clippy]

  # ═══════════════════════════════════════════════════════════════
  # PERFORMANCE (P2)
  # ═══════════════════════════════════════════════════════════════

  performance:
    checks:
      - N+1 queries
      - Memory leaks
      - Slow operations
      - Missing indexes
      - Unbounded queries
    tools:
      go: [pprof]
      python: [py-spy]
      javascript: [clinic.js]

  # ═══════════════════════════════════════════════════════════════
  # TESTS (P2)
  # ═══════════════════════════════════════════════════════════════

  tests:
    checks:
      - Missing coverage
      - Failing tests
      - Flaky tests
      - Outdated mocks
    tools:
      go: [go test -cover]
      python: [pytest --cov]
      javascript: [jest --coverage]
      java: [jacoco]

  # ═══════════════════════════════════════════════════════════════
  # TECHNICAL DEBT (P2-P3)
  # ═══════════════════════════════════════════════════════════════

  technical_debt:
    checks:
      - TODO/FIXME comments
      - Deprecated APIs
      - Legacy patterns
      - Missing documentation
      - Inconsistent naming
```

### Analysis Output:

```
🔍 ANALYSIS RESULTS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| Category     | Issues | Priority | Status |
|--------------|--------|----------|--------|
| Security     | 3      | P0       | 🔴     |
| Dependencies | 12     | P1       | 🟠     |
| Code Quality | 8      | P2       | 🟡     |
| Performance  | 2      | P2       | 🟡     |
| Tests        | 5      | P2       | 🟡     |
| Tech Debt    | 15     | P3       | 🔵     |

Total Issues: 45
Critical (P0): 3
High (P1): 12

Technical Debt Score: 6.5/10
Estimated Fix Time: 4-6 hours

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 📋 PHASE 3: PLAN

### Priority Matrix:

| Priority | Description                | SLA          | Action       |
| -------- | -------------------------- | ------------ | ------------ |
| **P0**   | Critical security/breaking | Immediate    | Must fix now |
| **P1**   | High impact bugs           | This session | Should fix   |
| **P2**   | Medium quality issues      | This week    | Queue next   |
| **P3**   | Low improvements           | Optional     | Backlog      |

### Generated Plan:

```markdown
📋 FIX PLAN

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## P0 — Critical (Must Fix Now)

- [ ] 🔴 Hardcoded API key → `config/config.go:45`
- [ ] 🔴 SQL injection in query → `repository/user.go:78`
- [ ] 🔴 Missing auth middleware → `handler/admin.go:12`

## P1 — High Priority (This Session)

- [ ] 🟠 Vulnerable dependency: gin v1.7.0 → upgrade to v1.9.1
- [ ] 🟠 Deprecated API usage → `service/payment.go:156`
- [ ] 🟠 N+1 query in GetUsers → `repository/user.go:34`

## P2 — Medium Priority (Queue)

- [ ] 🟡 Missing error handling → 8 locations
- [ ] 🟡 Test coverage 45% → target 80%
- [ ] 🟡 Dead code in utils → `pkg/utils/legacy.go`

## P3 — Optional (Backlog)

- [ ] 🔵 TODO comments: 15
- [ ] 🔵 Inconsistent naming: 12 files
- [ ] 🔵 Missing documentation: 5 packages

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Estimated Time:
├── P0: 30 min
├── P1: 2 hours
├── P2: 3 hours
└── P3: Optional

⛔ SELECT SCOPE:
1️⃣ Fix ALL (P0 + P1 + P2 + P3) — ~6 hours
2️⃣ Fix CRITICAL only (P0 + P1) — ~2.5 hours
3️⃣ Fix P0 ONLY — ~30 min
4️⃣ Fix ONE by ONE — Interactive
5️⃣ Cancel

Enter number:
```

---

## 📋 PHASE 4: EXECUTE

### Fix Application:

````
🔧 APPLYING FIX #1/3

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Issue: Hardcoded API key
File: `config/config.go:45`
Type: Security (P0)

Before:
```go
const apiKey = "sk-prod-abc123xyz"
````

After:

```go
apiKey := os.Getenv("API_KEY")
if apiKey == "" {
    return errors.New("API_KEY is required")
}
```

Reason: Hardcoded secrets in code can be exposed
via version control or decompilation.

Additional Changes:
├── Added API_KEY to .env.example
└── Updated README with env var docs

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```

### Batch Progress:

```

✅ FIXES APPLIED

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Progress: ████████████░░░░░░░░ 12/20

Applied:
├── P0: 3/3 ✅
├── P1: 8/12 (4 in progress)
└── P2: 1/5

Files Modified:
├── config/config.go — 2 changes
├── repository/user.go — 3 changes
├── handler/admin.go — 1 change
├── service/payment.go — 1 change
└── go.mod — 5 dependency updates

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

````

---

## 📋 PHASE 5: VERIFY

### Stack-Specific Commands:

```yaml
verification:
  go:
    lint: "golangci-lint run ./..."
    test: "go test ./... -v"
    build: "go build ./..."

  typescript:
    lint: "npm run lint"
    type: "npx tsc --noEmit"
    test: "npm test"
    build: "npm run build"

  python:
    lint: "ruff check ."
    type: "mypy ."
    test: "pytest -v"

  rust:
    lint: "cargo clippy -- -D warnings"
    test: "cargo test"
    build: "cargo build --release"

  java:
    lint: "mvn checkstyle:check"
    test: "mvn test"
    build: "mvn package"

  csharp:
    lint: "dotnet format --verify-no-changes"
    test: "dotnet test"
    build: "dotnet build"

  php:
    lint: "vendor/bin/phpcs"
    test: "vendor/bin/phpunit"

  ruby:
    lint: "rubocop"
    test: "rspec"
````

### Verification Output:

```
✅ VERIFICATION RESULTS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| Check  | Status | Details          |
|--------|--------|------------------|
| Lint   | ✅     | 0 errors         |
| Types  | ✅     | 0 errors         |
| Tests  | ✅     | 127/127 passed   |
| Build  | ✅     | Success (2.3s)   |

Coverage: 82% (+7% from baseline)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Overall: ✅ PASS
```

---

## 📋 PHASE 6: REPORT

### Final Summary:

```
📊 MODIFICATION REPORT

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Session Summary:
├── Duration: 45 minutes
├── Issues Fixed: 15/20
├── Files Modified: 12
├── Lines Changed: +234 / -156

By Priority:
├── P0 (Critical): 3/3 ✅
├── P1 (High): 8/12 (67%)
├── P2 (Medium): 4/5 (80%)
└── P3 (Low): 0/15 (deferred)

Technical Debt Score:
├── Before: 6.5/10
├── After: 8.2/10
└── Improvement: +26%

Security:
├── Vulnerabilities Fixed: 3
├── Dependencies Updated: 5
└── Remaining: 0 critical

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 REMAINING ISSUES (Backlog):

1. Test coverage: 82% → target 90%
2. TODO comments: 15 pending
3. Documentation gaps: 5 packages

📋 SUGGESTED NEXT STEPS:
1️⃣ `/test` — Increase test coverage
2️⃣ `/doc` — Generate documentation
3️⃣ `/deploy` — Deploy changes
4️⃣ `/ap` — Full audit

Enter number:
```

---

## 🔧 MODERNIZATION PATTERNS

### Legacy Code Patterns:

```yaml
modernization:
  # ═══════════════════════════════════════════════════════════════
  # COMMON REFACTORING PATTERNS
  # ═══════════════════════════════════════════════════════════════

  patterns:
    extract_method:
      description: "Break down large functions"
      trigger: "Function > 50 lines"

    replace_conditional:
      description: "Replace complex conditionals"
      trigger: "Nested if/else > 3 levels"

    introduce_parameter_object:
      description: "Group related parameters"
      trigger: "Function > 4 parameters"

    extract_class:
      description: "Split large classes"
      trigger: "Class > 500 lines"

    remove_dead_code:
      description: "Delete unused code"
      trigger: "Unreachable code detected"

  # ═══════════════════════════════════════════════════════════════
  # API MODERNIZATION
  # ═══════════════════════════════════════════════════════════════

  api_updates:
    - "Replace deprecated API calls"
    - "Update to async/await patterns"
    - "Convert callbacks to promises"
    - "Modernize error handling"
```

---

## 🤖 AI CODE ANALYSIS

```yaml
ai_code_analysis:
  capabilities:
    scan: "Identify bottlenecks, vulnerabilities"
    suggest: "Propose improvements"
    auto_fix: "Apply safe changes automatically"
    doc_gen: "Generate missing documentation"
    test_gen: "Create characterization tests"

  tools:
    - Byteable (Java legacy)
    - Moderne (OpenRewrite recipes)
    - Qodo (test generation)
    - Refact.ai (auto refactor)

  workflow: 1. "AI scans codebase"
    2. "Prioritize by severity"
    3. "Propose fixes"
    4. "Human validates"
    5. "Apply incrementally"

  command: "/modify analyze [path]"
```

---

## 📊 TECHNICAL DEBT SCORING

```yaml
tech_debt_score:
  formula: |
    code_complexity * 0.3 +
    test_coverage_gap * 0.2 +
    dependency_age * 0.2 +
    security_findings * 0.3

  levels:
    healthy: "< 20 - Minimal debt"
    manageable: "20-50 - Regular maintenance"
    concerning: "50-80 - Prioritize remediation"
    critical: "> 80 - Modernize now"

  tracking:
    - "Track over time"
    - "Set reduction targets"
    - "Celebrate improvements"

  commands:
    score: "/modify debt score"
    report: "/modify debt report"
    trend: "/modify debt trend"
```

---

## ⚡ AUTONOMOUS MODERNIZATION

```yaml
auto_modernization:
  description: "AI-driven continuous improvement"

  workflow: 1. "AI scans legacy code"
    2. "Identifies patterns to update"
    3. "Generates modernized equivalent"
    4. "Creates characterization tests"
    5. "PRs for human review"

  safe_patterns:
    auto_apply:
      - "Deprecated API replacement"
      - "Syntax modernization"
      - "Import organization"
      - "Formatting fixes"

  requires_review:
    human_check:
      - "Logic changes"
      - "Architecture updates"
      - "Dependency upgrades"
      - "Breaking changes"

  benefits:
    - "40% faster modernization"
    - "Up to 40% cost reduction"
    - "Continuous hygiene"
```

---

## ⚙️ TOKEN OPTIMIZATION

```yaml
token_saving:
  # Quick detection
  - Infer stack from key files
  - Skip obvious non-issues

  # Batch operations
  - Group similar fixes
  - Apply patterns in bulk
  - Single verification run

  # Focused analysis
  - Priority filter first
  - Deep analysis on request
```

---

## 📜 RULES APPLIED

| Phase   | Rules                         |
| ------- | ----------------------------- |
| Detect  | `context-management`          |
| Analyze | `stop-conditions`             |
| Plan    | `stop-conditions`             |
| Execute | `edit-verification`, `safety` |
| Verify  | `evidence`                    |
| Report  | `evidence`                    |

---

_DOMYH Awesome Code v6.1.2 • Modify Pro v3.1 • AI-Driven Modernization_
