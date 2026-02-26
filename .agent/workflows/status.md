---
description: "📊 Project health: build, tests, coverage, lint metrics, and recent activity"
skills: { required: [], contextual: [auto] }
success_criteria: "Health score calculated, actionable recommendations shown"
---

# 📊 /status — Status Pro

> Project Health Dashboard
> 📚 Multi-stack • Auto-detect • Actionable • Trend Tracking

---

## STATUS FLOW

1. **DETECT** — Identify project stack via HSA (`hsa_detect_stack`), config files. Show: `[Step 1/3] Detected: Go + TypeScript monorepo`
2. **COLLECT** — Run build, tests, coverage, lint, dep check, `hsa_status` (engine health). Show: `[Step 2/3] Running 6 checks...`
3. **REPORT** — Calculate health score, identify issues, compare with previous. Use `hsa_export` for structured data. Save snapshot to `.domyh/status/health_YYYY-MM-DD.md`

---

## COMMANDS

| Command         | Description         |
| --------------- | ------------------- |
| `/status`       | Full health report  |
| `/status quick` | Brief summary       |
| `/status build` | Build status only   |
| `/status tests` | Test status only    |
| `/status deps`  | Dependencies status |
| `/status trend` | Compare history     |

---

## 🔧 COMMANDS BY STACK

| Language   | Build                  | Test               | Coverage                | Lint                   | Deps                                      |
| ---------- | ---------------------- | ------------------ | ----------------------- | ---------------------- | ----------------------------------------- |
| Go         | `go build ./...`       | `go test -v ./...` | `go test -cover`        | `golangci-lint run`    | `go list -m -u all`                       |
| TypeScript | `npm run build`        | `npm test`         | `npm run test:coverage` | `npm run lint`         | `npm outdated`                            |
| Python     | `python -m py_compile` | `pytest -v`        | `pytest --cov`          | `ruff check .`         | `pip list --outdated`                     |
| Rust       | `cargo build`          | `cargo test`       | `cargo tarpaulin`       | `cargo clippy`         | `cargo outdated`                          |
| Java       | `mvn compile`          | `mvn test`         | `mvn jacoco:report`     | `mvn checkstyle:check` | `mvn versions:display-dependency-updates` |
| C#         | `dotnet build`         | `dotnet test`      | `coverlet`              | `dotnet format`        | `dotnet list package --outdated`          |

---

## 📋 HEALTH THRESHOLDS

| Metric   | 🟢 Good    | 🟡 Warning    | 🔴 Critical   |
| -------- | ---------- | ------------- | ------------- |
| Build    | Pass       | Warnings      | Fail          |
| Tests    | 100% pass  | > 95%         | < 95%         |
| Coverage | > 80%      | 60-80%        | < 60%         |
| Lint     | 0 issues   | < 10 warnings | Errors        |
| Security | 0 vulns    | Low/medium    | High/critical |
| Deps     | Up to date | Patch/minor   | Major behind  |

---

## 📊 HEALTH SCORE

| Component | Weight |
| --------- | ------ |
| Build     | 20%    |
| Tests     | 20%    |
| Coverage  | 15%    |
| Lint      | 10%    |
| Security  | 15%    |
| CI/CD     | 10%    |
| Git       | 10%    |

### Report Format

```
📊 Project Health: 87/100 (🟢 Good)

Build    🟢 Pass        Tests    🟢 42/42 (100%)
Coverage 🟡 72%          Lint     🟢 0 issues
Security 🟢 0 vulns      Deps     🟡 3 outdated
CI/CD    🟢 Last pass    Git      🟢 Clean

⚡ Quick wins: Coverage +8% → run `/test write utils`
```

---

## 🚀 CI/CD STATUS

| Command                 | Description         |
| ----------------------- | ------------------- |
| `gh run list --limit 5` | GitHub Actions runs |
| `gh run view {id}`      | Run details         |

---

## 🔀 GIT STATUS

| Command                                  | Info                |
| ---------------------------------------- | ------------------- |
| `git branch --show-current`              | Current branch      |
| `git status --porcelain`                 | Uncommitted changes |
| `git rev-list --count HEAD ^origin/main` | Ahead of remote     |
| `git stash list`                         | Stashed changes     |
