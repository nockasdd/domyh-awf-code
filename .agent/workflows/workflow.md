---
description: "🔄 Meta-command: workflow discovery, chaining, and aliasing"
skills: { required: [], contextual: [] }
---

# 🔄 /workflow — Workflow Meta

> Discover, Chain, and Manage Workflows
> 📚 Discovery • Chaining • Aliases • Context-Aware • DAG Execution

---

## COMMANDS

| Command                       | Description                              |
| ----------------------------- | ---------------------------------------- |
| `/workflow list`              | List all available workflows by category |
| `/workflow list [category]`   | List workflows in specific category      |
| `/workflow chain [a] [b] [c]` | Execute workflows in sequence            |
| `/workflow suggest`           | Suggest next workflow based on context   |
| `/workflow recent`            | Show recently used workflows             |
| `/workflow info [cmd]`        | Show detailed info about a workflow      |
| `/workflow dag [a] [b] [c]`   | Execute with dependency awareness        |

---

## 📋 WORKFLOW CATEGORIES

| Category    | Label                  | Commands                                             |
| ----------- | ---------------------- | ---------------------------------------------------- |
| core        | 💻 Core Development    | `/code`, `/debug`, `/fix`, `/test`                   |
| quality     | 🔍 Quality & Review    | `/ap`, `/review`, `/refactor`, `/security`           |
| planning    | 📋 Planning & Thinking | `/plan`, `/think`, `/visualize`                      |
| generation  | 🏗️ Generation          | `/init`, `/scaffold` (also `/generate`), `/doc`      |
| operations  | 🚀 Operations          | `/deploy`, `/env`, `/migrate`, `/monitor`, `/revert` |
| maintenance | 🔧 Maintenance         | `/upgrade`, `/perf`, `/git`                          |
| utility     | 📊 Utility             | `/status`, `/recap`, `/save`, `/suggest`, `/help`    |
| onboarding  | 📦 Onboarding          | `/onboard`                                           |
| meta        | 🔄 Meta                | `/workflow`, `/orchestrate`, `/lang`                 |

---

## 🗺️ MASTER FLOW MAP

```mermaid
graph LR
    subgraph planning["📋 Planning"]
        plan["/plan"]
        think["/think"]
        visualize["/visualize"]
    end

    subgraph generation["🏗️ Generation"]
        init["/init"]
        scaffold["/scaffold"]
        doc["/doc"]
    end

    subgraph core["💻 Core Development"]
        code["/code"]
        debug["/debug"]
        fix["/fix"]
        test["/test"]
    end

    subgraph quality["🔍 Quality & Review"]
        ap["/ap"]
        review["/review"]
        refactor["/refactor"]
        security["/security"]
    end

    subgraph operations["🚀 Operations"]
        deploy["/deploy"]
        env["/env"]
        migrate["/migrate"]
        monitor["/monitor"]
        revert["/revert"]
    end

    subgraph maintenance["🔧 Maintenance"]
        upgrade["/upgrade"]
        perf["/perf"]
        git["/git"]
    end

    %% Cross-group connections
    plan --> code
    plan --> scaffold
    init --> scaffold
    scaffold --> code
    code --> test
    code --> review
    debug --> fix
    fix --> test
    test -->|pass| deploy
    test -->|fail| fix
    review --> refactor
    refactor --> test
    ap --> refactor
    ap --> fix
    security --> fix
    deploy --> monitor
    migrate --> test
    upgrade --> test
```

---

## 🔄 CANONICAL FLOW PATTERNS

```mermaid
graph LR
    subgraph standard["Standard (5-step)"]
        S1["DETECT"] --> S2["PLAN"] --> S3["EXECUTE"] --> S4["VERIFY"] --> S5["SYNC"]
    end

    subgraph deep["Deep (6-step)"]
        D1["DETECT"] --> D2["ANALYZE"] --> D3["PLAN"] --> D4["EXECUTE"] --> D5["VERIFY"] --> D6["SYNC"]
    end

    subgraph quick["Quick (4-step)"]
        Q1["DETECT"] --> Q2["EXECUTE"] --> Q3["VERIFY"] --> Q4["SYNC"]
    end
```

| Variant      | Workflows                                                                                                      |
| ------------ | -------------------------------------------------------------------------------------------------------------- |
| **Standard** | `/code`, `/refactor`, `/scaffold`, `/env`, `/migrate`, `/monitor`, `/revert`, `/upgrade`, `/visualize`, `/doc` |
| **Deep**     | `/ap`, `/debug`, `/plan`, `/deploy`, `/test`, `/perf`, `/review`                                               |
| **Quick**    | `/fix`, `/dev`, `/git`, `/status`, `/recap`, `/help`                                                           |
| **Unique**   | `/think` (decision), `/orchestrate` (multi-agent), `/init` (interview)                                         |

---

## 🔗 WORKFLOW CHAINS

Run multiple workflows in sequence with data passing between them.

| Chain          | Flow                                                    | Usage                                                                                         |
| -------------- | ------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| Full Feature   | `/plan → /code → /test → /deploy`                       | `/workflow chain plan code test deploy`                                                       |
| Bug Fix        | `/debug → /fix → /test`                                 | `/workflow chain debug fix test`                                                              |
| Code Review    | `/review → /refactor → /test`                           | `/workflow chain review refactor test`                                                        |
| Quick Ship     | `/fix → /test → /git commit → /deploy`                  | `/workflow chain fix test git deploy`                                                         |
| New Feature    | `/scaffold → /code → /test`                             | `/workflow chain scaffold code test`                                                          |
| Quality Sweep  | `/ap → /refactor → /clean → /test`                      | `/workflow chain ap refactor clean test`                                                      |
| Security Gate  | `/security → /fix → /test → /deploy`                    | `/workflow chain security fix test deploy`                                                    |
| Release        | `/test → /status → /deploy → /monitor`                  | `/workflow chain test status deploy monitor`                                                  |
| Enterprise     | Full 8-stage SDLC chain                                 | `/workflow chain plan-specify code review test test-uat deploy-staging deploy deploy-signoff` |
| 🆕 Kickstart   | `/init → /env → /dev → /plan`                           | `/workflow chain init env dev plan` — New project from scratch                                |
| 🆕 Discovery   | `/status → /ap quick → /doc readme → /suggest`          | `/workflow chain status ap doc suggest` — Onboard existing project                            |
| 🆕 UI Flow     | `/think → /visualize → /scaffold → /code → /test`       | `/workflow chain think visualize scaffold code test` — Design → Code                          |
| 🆕 UI Refactor | `/visualize compare → /refactor ui → /test → /review`   | `/workflow chain visualize refactor test review` — Modernize UI                               |
| 🆕 Mobile App  | `/init → /visualize mobile → /scaffold → /code → /test` | `/workflow chain init visualize scaffold code test` — Mobile app                              |

---

## 💡 SMART SUGGESTIONS

| After                | Suggest Next                    |
| -------------------- | ------------------------------- |
| `/init`              | → `/env`, `/dev`, `/scaffold`   |
| `/code`              | → `/test`, `/review`            |
| `/debug`             | → `/fix`, `/test`               |
| `/fix`               | → `/test`, `/git commit`        |
| `/test` pass         | → `/git commit`, `/deploy`      |
| `/test` fail         | → `/fix`, `/debug`              |
| `/review`            | → `/refactor`, `/code fix`      |
| `/refactor`          | → `/test`                       |
| `/deploy`            | → `/monitor`, `/status`         |
| `/plan`              | → `/code`, `/scaffold`          |
| `/scaffold`          | → `/code`                       |
| `/ap`                | → `/refactor`, `/fix`           |
| `/ap` score < 7      | → `/fix`, `/refactor`           |
| `/migrate`           | → `/test`, `/deploy`            |
| `/security`          | → `/fix`, `/ap`                 |
| `/security` pass     | → `/deploy`                     |
| `/onboard`           | → `/plan`, `/code`, `/suggest`  |
| `/visualize`         | → `/scaffold`, `/code`          |
| CSS/UI files changed | → `/visualize responsive`       |
| `--dark-mode` flag   | → `/visualize dark-mode`        |
| New project opened   | → `discovery` chain             |
| `/refactor ui`       | → `/test`, `/visualize compare` |

---

## 🔄 CHAIN BEHAVIOR

| Feature        | Description                               |
| -------------- | ----------------------------------------- |
| Data passing   | Output of step N → input of step N+1      |
| Error handling | Stop chain on failure, show at which step |
| Skip logic     | Skip steps if preconditions already met   |
| Progress       | Show: `[Chain 2/4] Running /test...`      |
| Rollback       | Option to undo on chain failure           |
