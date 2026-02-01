---
name: status
trigger: ["/status", "health", "trạng thái"]
description: "📊 Project health: build, tests, coverage, lint metrics, and recent activity"
---

# 📊 /status — Project Health Pro v3.0

> Complete Project Health Dashboard
> 📚 Multi-stack • Auto-detect • Actionable

---

## 🔄 STATUS FLOW

```
User: /status
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 1: DETECT                         │
│ ▸ Identify project stack                │
│ ▸ Find config files                     │
│ ▸ Locate test/lint tools                │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 2: COLLECT                        │
│ ▸ Run build check                       │
│ ▸ Run tests                             │
│ ▸ Get coverage                          │
│ ▸ Run linter                            │
│ ▸ Check dependencies                    │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 3: REPORT                         │
│ ▸ Calculate health score                │
│ ▸ Identify issues                       │
│ ▸ Suggest improvements                  │
└─────────────────────────────────────────┘
```

---

## 🎯 COMMANDS

| Command         | Description         |
| --------------- | ------------------- |
| `/status`       | Full health report  |
| `/status quick` | Brief summary       |
| `/status build` | Build status only   |
| `/status tests` | Test status only    |
| `/status deps`  | Dependencies status |

---

## 📊 HEALTH REPORT

```markdown
📊 PROJECT HEALTH REPORT

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Project: my-api
Stack: Go + Gin + PostgreSQL
Last Updated: 2026-01-31 18:40:00

## Overall Health: 🟢 85/100 (Good)

## Metrics Dashboard

| Metric   | Value      | Target | Status |
| -------- | ---------- | ------ | ------ |
| Build    | ✅ Pass    | Pass   | 🟢     |
| Tests    | 142/145    | 100%   | 🟡     |
| Coverage | 78%        | 80%    | 🟡     |
| Lint     | 5 warnings | 0      | 🟡     |
| Deps     | 2 outdated | 0      | 🟡     |
| Security | 0 vulns    | 0      | 🟢     |

## Build Details
```

✅ Build successful
Time: 12.3s
Output: ./bin/api

```

## Test Results

| Suite | Pass | Fail | Skip |
|-------|------|------|------|
| Unit | 120 | 2 | 3 |
| Integration | 20 | 1 | 0 |
| E2E | 5 | 0 | 0 |

❌ Failed Tests:
1. `TestUserCreate` - timeout exceeded
2. `TestOrderValidation` - assertion failed
3. `TestPaymentWebhook` - nil pointer

## Coverage Breakdown

| Package | Coverage | Status |
|---------|----------|--------|
| handlers | 85% | 🟢 |
| services | 72% | 🟡 |
| repository | 68% | 🟡 |
| utils | 91% | 🟢 |

## Lint Issues

| Severity | Count | Top Issues |
|----------|-------|------------|
| Error | 0 | - |
| Warning | 5 | unused var (3), shadowed var (2) |
| Info | 12 | - |

## Dependency Status

| Type | Outdated | Vulnerable |
|------|----------|------------|
| Direct | 2 | 0 |
| Indirect | 5 | 1 |

Outdated:
- `gin-gonic/gin` 1.9.0 → 1.10.0 (minor)
- `lib/pq` 1.10.0 → 1.10.9 (patch)

## Recent Activity

| Event | Time |
|-------|------|
| Last commit | 2h ago |
| Last deploy | 1d ago |
| Last test run | 5m ago |

## Issues Summary

| Priority | Count | Description |
|----------|-------|-------------|
| 🔴 P0 | 0 | Critical |
| 🟠 P1 | 3 | Failing tests |
| 🟡 P2 | 2 | Low coverage |
| 🔵 P3 | 5 | Lint warnings |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 💡 Recommendations

1. 🔴 Fix 3 failing tests
2. 🟠 Increase services coverage to 80%
3. 🟡 Update 2 outdated dependencies
4. 🔵 Fix lint warnings

Next: `/test` to fix failing tests
```

---

## 📋 HEALTH THRESHOLDS

```yaml
thresholds:
  build:
    green: "Pass"
    yellow: "Pass with warnings"
    red: "Fail"

  tests:
    green: "100% pass"
    yellow: "> 95% pass"
    red: "< 95% pass"

  coverage:
    green: "> 80%"
    yellow: "60-80%"
    red: "< 60%"

  lint:
    green: "0 errors/warnings"
    yellow: "< 10 warnings"
    red: "> 10 warnings or errors"

  security:
    green: "0 vulnerabilities"
    yellow: "Low/medium vulns"
    red: "High/critical vulns"

  deps:
    green: "All up to date"
    yellow: "Patch/minor outdated"
    red: "Major version behind or vulns"
```

---

## 🔧 COMMANDS BY STACK

````yaml
commands:
  go:
    build: "go build ./..."
    test: "go test -v ./..."
    coverage: "go test -cover ./..."
    lint: "golangci-lint run"
    deps: "go list -m -u all"

  typescript:
    build: "npm run build"
    test: "npm test"
    coverage: "npm run test:coverage"
    lint: "npm run lint"
    deps: "npm outdated"

  python:
    build: "python -m py_compile"
    test: "pytest -v"
    coverage: "pytest --cov"
    lint: "ruff check ."
    deps: "pip list --outdated"

  rust:
    build: "cargo build"
    test: "cargo test"
    coverage: "cargo tarpaulin"
    lint: "cargo clippy"
    deps: "cargo outdated"

  java:
    build: "mvn compile"
    test: "mvn test"
    coverage: "mvn jacoco:report"
    lint: "mvn checkstyle:check"
    deps: "mvn versions:display-dependency-updates"
---

## 🚀 CI/CD PIPELINE STATUS

```yaml
ci_cd_status:
  github_actions:
    check: "gh run list --limit 5"
    output:
      - workflow_name
      - status (pass/fail/running)
      - duration
      - commit

  display: |
    ## CI/CD Status

    | Workflow | Status | Duration | Commit |
    |----------|--------|----------|--------|
    | CI Tests | ✅ Pass | 3m 42s | abc1234 |
    | Deploy   | ⏳ Running | 2m 10s | abc1234 |
    | Lint     | ✅ Pass | 45s | abc1234 |

  integration:
    gitlab: "gitlab-ci status"
    jenkins: "jenkins-cli build status"
    circleci: "circleci project"
````

---

## 🔀 GIT STATUS INTEGRATION

```yaml
git_status:
  check:
    - current_branch
    - uncommitted_changes
    - ahead_behind_remote
    - last_commit

  display: |
    ## Git Status

    | Info | Value |
    |------|-------|
    | Branch | main |
    | Status | 3 uncommitted files |
    | Remote | 2 ahead, 0 behind |
    | Last commit | 2h ago (feat: add auth) |

  commands:
    branch: "git branch --show-current"
    status: "git status --porcelain"
    remote: "git rev-list --count HEAD ^origin/main"
```

---

## 📊 SCORE CALCULATION

```yaml
health_score:
  weights:
    build: 20%
    tests: 20%
    coverage: 15%
    lint: 10%
    security: 15%
    ci_cd: 10% # NEW
    git: 10% # NEW

  calculation:
    build_pass: +20
    tests_pass: +20 * (pass_rate)
    coverage: +15 * (coverage_percent / target)
    lint_clean: +10 * (1 - issues/threshold)
    security_clean: +15
    ci_cd_green: +10
    git_clean: +10
```

---

## ⚙️ TOKEN OPTIMIZATION

```yaml
token_saving:
  - Run quick checks first
  - Cache results for session
  - Only show issues, not all metrics
  - Parallel git + CI checks
```

---

_DOMYH Agent v4.3 • Status Pro v3.1 • Full Health Dashboard_
