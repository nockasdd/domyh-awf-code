---
description: "🔧 Fix existing project: detect stack → analyze issues → plan → execute → verify"
skills: { required: [coding-rules], contextual: [auto] }
success_criteria: "issues fixed, lint/type/test pass, debt score improved"
---

# 🔧 /modify — Project Modification Pro v3.0

> AI-Powered Legacy Modernization & Issue Resolution
> 📚 30+ Languages • Technical Debt • Automated Analysis

---

## 🔄 MODIFICATION FLOW

1. **PHASE 1: DETECT (Auto)** — `hsa_session`, `hsa_detect`, identify architecture pattern and map structure.
2. **PHASE 2: ANALYZE** — Scan for issues, detect technical debt, prioritize by severity.
3. **PHASE 3: PLAN** — Generate fix plan, estimate effort. ⛔ **STOP** → Confirm scope with user.
4. **PHASE 4: EXECUTE** — Apply fixes, document changes, update tests.
5. **PHASE 5: VERIFY** — Run lint/type check, tests, verify build.
6. **PHASE 6: REPORT** — Summary of changes, technical debt score, suggested next steps. `hsa_check_changes` to update index.

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

### Stack Detection

> Detect stack automatically using `hsa_detect` or `_router.yaml` patterns.
> Agent selects fix strategy based on detected language and framework.

### Detection Output

```text
📦 PROJECT DETECTED: my-api | Go 1.22 + Gin | Clean Architecture
   Files: 127 (.go) | Lines: 15,847 | Packages: 23 | Deps: 45
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

### Analysis Output

```text
🔍 ANALYSIS: 45 issues (3 P0, 12 P1, 15 P2, 15 P3) | Debt: 6.5/10 | ETA: 4-6h
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

### Generated Plan

Group issues by priority (P0→P3), each with `file:line` references:

```text
📋 FIX PLAN — P0: 3 (30min) | P1: 12 (2h) | P2: 5 (3h) | P3: 15 (optional)
⛔ SELECT SCOPE: 1️⃣ Fix ALL | 2️⃣ P0+P1 only | 3️⃣ P0 only | 4️⃣ Interactive
```

---

## 📋 PHASE 4: EXECUTE

### Fix Application

For each fix, show: Issue → File:Line → Before/After diff → Reason.
Track progress: `🔧 FIX #N/M | P0: x/y ✅ | P1: x/y | Files: N modified`

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
```

### Verification Output

```text
✅ VERIFY: Lint ✅ | Types ✅ | Tests 127/127 ✅ | Build ✅ (2.3s) | Coverage: 82%
```

---

## 📋 PHASE 6: REPORT

### Final Summary

```text
📊 REPORT: 15/20 fixed | 12 files | +234/-156 lines | Debt: 6.5→8.2 (+26%)
   P0: 3/3 ✅ | P1: 8/12 | P2: 4/5 | Remaining → /test, /doc, /deploy, /ap
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
| Detect  | `perf-001`                    |
| Analyze | `stop-conditions`             |
| Plan    | `stop-conditions`             |
| Execute | `edit-verification`, `safety` |
| Verify  | `exec-001`                    |
| Report  | `exec-001`                    |

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

