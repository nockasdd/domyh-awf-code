---
description: "🔬 DOMYH AUDIT  Kiểm tra chuyên sâu toàn bộ hệ thống"
---

# 🔬 /ap — DOMYH Audit Pro v5.0

> Comprehensive 5-Expert Panel Audit System
> 📚 Based on: ISO 25010, CWE Top 25, OWASP Top 10

---

## 🔄 AUDIT FLOW

```
User: /ap
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 1: DISCOVERY (Auto - 30s)        │
│ ▸ Detect tech stack                     │
│ ▸ Count files & estimate complexity     │
│ ▸ Load specialized skills               │
│ ▸ Check for existing audit history      │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 2: SCOPE CONTRACT                 │
│ ▸ Display 5 scope options               │
│ ⛔ STOP - WAIT FOR USER SELECTION       │
└─────────────────────────────────────────┘
    │ User selects scope (1-5)
    ▼
┌─────────────────────────────────────────┐
│ PHASE 3: EXECUTE (Per Scope Time)       │
│ ▸ Run 5 Expert Panels sequentially      │
│ ▸ Each expert has ~20 checkpoints       │
│ ▸ Collect findings with evidence        │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 4: REPORT                         │
│ ▸ Production Readiness Score (0-10)     │
│ ▸ Findings by P0/P1/P2/P3               │
│ ▸ Actionable next steps                 │
│ ▸ Save to .domyh/audit_YYYY-MM-DD.md    │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 5: MEMORY PERSIST (Auto)          │
│ ▸ Update memory/audit_summary.json      │
│ ▸ Log key decisions to decisions.md    │
│ ▸ Update memory/state.json scores       │
│ ▸ Append to session.md history          │
└─────────────────────────────────────────┘
```

---

## 🎯 SCOPE OPTIONS

| #   | Scope                | Est. | Coverage                        | When to Use                    |
| --- | -------------------- | ---- | ------------------------------- | ------------------------------ |
| 1   | 🔴 **FULL AUDIT**    | ~2h  | Backend + Frontend + Infra + DB | Pre-production, Major releases |
| 2   | 🟠 **BACKEND**       | ~1h  | Server, APIs, Database          | Backend changes, API updates   |
| 3   | 🟡 **FRONTEND**      | ~30m | UI, State, Performance          | UI changes, UX updates         |
| 4   | 🟢 **SECURITY ONLY** | ~1h  | Vulnerabilities, Auth, Secrets  | Security review, Compliance    |
| 5   | 🔵 **CUSTOM**        | ?    | User-defined modules            | Specific areas of concern      |

```
⛔ STOP after displaying this table
📝 Wait for user: "Enter number (1-5) or describe custom scope:"
```

---

## 👥 5 EXPERT PANELS (Enhanced v5.0)

### 👨‍💼 PANEL 1: Security Expert (Minh)

> Focus: Vulnerabilities, Authentication, Data Protection

#### Checklist (25 items):

**🔐 Authentication & Authorization**

- [ ] JWT token validation & expiration
- [ ] Session management security
- [ ] Password hashing (bcrypt/argon2)
- [ ] OAuth/SSO implementation
- [ ] Role-based access control (RBAC)
- [ ] API key management

**🛡️ CWE Top 25 (2024)**

- [ ] CWE-79: XSS vulnerabilities
- [ ] CWE-89: SQL Injection
- [ ] CWE-78: OS Command Injection
- [ ] CWE-22: Path Traversal
- [ ] CWE-352: CSRF protection
- [ ] CWE-287: Authentication bypass
- [ ] CWE-862: Missing authorization

**🌐 OWASP Top 10 (2021)**

- [ ] A01: Broken Access Control
- [ ] A02: Cryptographic Failures
- [ ] A03: Injection
- [ ] A05: Security Misconfiguration
- [ ] A07: Auth Failures
- [ ] A09: Logging Failures

**🔒 Secrets & Data**

- [ ] No hardcoded secrets
- [ ] .env files not in git
- [ ] Sensitive data encryption
- [ ] Audit logging for sensitive ops

**Tools Used:**

```bash
grep_search: "password|secret|api_key|token"
find_by_name: ".env*", "credentials.*", "*.key"
view_file: auth handlers, middleware
```

---

### 👩‍💻 PANEL 2: Architecture Expert (Linh)

> Focus: Design Patterns, Structure, Maintainability

#### Checklist (20 items):

**🏗️ SOLID Principles**

- [ ] Single Responsibility (1 class = 1 job)
- [ ] Open/Closed (extensible, not modifiable)
- [ ] Liskov Substitution (subtypes replaceable)
- [ ] Interface Segregation (small interfaces)
- [ ] Dependency Inversion (abstractions)

**📐 Design Patterns**

- [ ] Repository pattern for data access
- [ ] Factory pattern usage
- [ ] Strategy pattern for algorithms
- [ ] Observer for events
- [ ] Dependency Injection setup

**🔗 Coupling & Cohesion**

- [ ] Low coupling between modules
- [ ] High cohesion within modules
- [ ] Clear module boundaries
- [ ] Circular dependency detection

**📁 Project Structure**

- [ ] Follows domain-driven design
- [ ] Clear separation of concerns
- [ ] Consistent file/folder naming
- [ ] Proper layering (handlers → services → repos)

**📋 API Design**

- [ ] RESTful conventions
- [ ] Consistent error responses
- [ ] Proper HTTP status codes
- [ ] API versioning strategy

**Tools Used:**

```bash
view_file_outline: main packages
list_dir: project structure
grep_search: import patterns
```

---

### 👨‍🔧 PANEL 3: Performance Expert (Khoa)

> Focus: Speed, Resources, Scalability

#### Checklist (20 items):

**🗃️ Database Performance**

- [ ] N+1 query detection
- [ ] Index usage verification
- [ ] Connection pooling
- [ ] Query optimization
- [ ] Proper pagination

**💾 Memory Management**

- [ ] Memory leak patterns
- [ ] Large object handling
- [ ] Buffer management
- [ ] Garbage collection friendly

**⚡ Caching Strategy**

- [ ] Cache layer exists
- [ ] Cache invalidation logic
- [ ] Redis/Memcached usage
- [ ] HTTP caching headers

**🔄 Async Patterns**

- [ ] Proper goroutine/worker usage
- [ ] Context cancellation
- [ ] Rate limiting
- [ ] Queue implementation

**📊 Monitoring Ready**

- [ ] Response time tracking
- [ ] Resource usage metrics
- [ ] Error rate monitoring
- [ ] Performance baselines

**Tools Used:**

```bash
grep_search: "SELECT", "db.Query", "gorm"
view_file: database layer, repositories
analyze: query patterns
```

---

### 👩‍🔬 PANEL 4: Quality Expert (Hương)

> Focus: Testing, Documentation, Standards

#### Checklist (20 items):

**🧪 Test Coverage**

- [ ] Unit test existence (>70%)
- [ ] Integration tests (critical paths)
- [ ] E2E tests (core flows)
- [ ] Test naming conventions
- [ ] Mock/stub usage

**❌ Error Handling**

- [ ] Consistent error types
- [ ] Error wrapping with context
- [ ] No silent failures
- [ ] User-friendly messages
- [ ] Error recovery patterns

**📝 Documentation**

- [ ] README completeness
- [ ] API documentation
- [ ] Code comments (why, not what)
- [ ] Architecture decision records
- [ ] Setup/deployment guides

**🔧 Code Quality**

- [ ] No code duplication (DRY)
- [ ] Consistent formatting
- [ ] Linter compliance
- [ ] Type safety
- [ ] Naming conventions

**Tools Used:**

```bash
find_by_name: "*_test.go", "*.test.ts"
run_command: "go test -cover", "npm test"
view_file: README.md, docs/
```

---

### 👨‍🏫 PANEL 5: DevOps Expert (Đức)

> Focus: Deployment, Monitoring, Operations

#### Checklist (20 items):

**🚀 CI/CD Pipeline**

- [ ] Automated testing in CI
- [ ] Linting/formatting checks
- [ ] Build verification
- [ ] Deployment automation
- [ ] Rollback capability

**📊 Logging & Monitoring**

- [ ] Structured logging
- [ ] Log levels (debug/info/error)
- [ ] Centralized log collection
- [ ] Alerting configuration
- [ ] Dashboard existence

**🐳 Containerization**

- [ ] Dockerfile optimization
- [ ] Multi-stage builds
- [ ] .dockerignore completeness
- [ ] Docker Compose for dev
- [ ] Security scanning

**⚙️ Configuration**

- [ ] Environment separation
- [ ] Secrets management
- [ ] Feature flags
- [ ] Health check endpoints
- [ ] Graceful shutdown

**Tools Used:**

```bash
view_file: Dockerfile, docker-compose.yml
view_file: .github/workflows/*.yml
grep_search: "log.Info", "logger"
```

---

## 📊 FINDING FORMAT

### Template:

```markdown
**[P0]** 🔒 Security `file:line`

**Issue:** Brief description of the problem
**Evidence:**
\`\`\`go
// actual code showing the issue
\`\`\`
**Impact:** What could go wrong
**Fix:**
\`\`\`go
// suggested fix
\`\`\`
```

### Priority Levels:

| Priority | Icon | Meaning                            | SLA               |
| -------- | ---- | ---------------------------------- | ----------------- |
| **P0**   | 🔴   | Critical - Security/Data loss risk | Fix immediately   |
| **P1**   | 🟠   | High - Affects core functionality  | Fix before deploy |
| **P2**   | 🟡   | Medium - Should fix soon           | Fix this sprint   |
| **P3**   | 🟢   | Low - Nice to have                 | Backlog           |

---

## 📋 FINAL REPORT FORMAT

```
📊 DOMYH AUDIT REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Project: [name]
Date: [YYYY-MM-DD]
Scope: [selected scope]
Duration: [time taken]

┌─────────────────────────────────┐
│  Production Readiness: X.X/10  │
└─────────────────────────────────┘

| Expert | Score | Issues |
|--------|-------|--------|
| Security | 8/10 | 2 P2 |
| Architecture | 7/10 | 1 P1, 3 P3 |
| Performance | 9/10 | 1 P3 |
| Quality | 6/10 | 2 P1, 4 P2 |
| DevOps | 8/10 | 1 P2 |

SUMMARY:
- P0 Critical: 0
- P1 High: 3
- P2 Medium: 5
- P3 Low: 8

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📁 Full report: .domyh/audit_YYYY-MM-DD.md
```

---

## 🔄 NEXT STEPS MENU

After audit completes:

```
📋 NEXT STEPS

1️⃣ /debug P0-001 → Fix critical issues first
2️⃣ /code → Implement P1 fixes
3️⃣ /test → Verify fixes
4️⃣ /ap → Re-audit after fixes
5️⃣ /deploy → Deploy when ready

Enter number or describe:
```

---

## 📜 RULES APPLIED

| Phase     | Rules                                           |
| --------- | ----------------------------------------------- |
| Discovery | `context-management`, `terminal-safety`         |
| Scope     | `stop-conditions`                               |
| Execute   | `evidence`, `quality`, `prompt-injection-guard` |
| Report    | `safety` (mask secrets), `edit-verification`    |

---

## 👥 MULTI-EXPERT CONSENSUS (v5.1)

```yaml
expert_panel:
  description: "5 specialized experts with consensus mechanism"

  experts:
    architect:
      focus: "System design, scalability, patterns"
      standards: ["Clean Architecture", "SOLID", "DDD"]

    security:
      focus: "Vulnerabilities, attack vectors"
      standards: ["OWASP Top 10", "CWE Top 25"]

    performance:
      focus: "Bottlenecks, optimization"
      standards: ["Core Web Vitals", "N+1 detection"]

    quality:
      focus: "Code smells, maintainability"
      standards: ["ISO 25010", "Cognitive complexity"]

    infrastructure:
      focus: "DevOps, reliability"
      standards: ["SRE principles", "12-factor app"]

  consensus:
    mechanism:
      voting: "Weighted average by severity"
      conflicts: "Highlight disagreements"
      final: "Human arbitration for P0"

    confidence:
      high: "> 80% agreement"
      medium: "60-80% agreement"
      low: "< 60% → flag for review"

  output:
    individual_scores: true
    combined_score: true
    disagreements: true
    citations: true

  commands:
    full: "/ap full"
    quick: "/ap quick"
    security: "/ap security"
    expert: "/ap expert [name]"
```

---

## 🔧 SUB-COMMANDS (Updated)

| Command              | Description             |
| -------------------- | ----------------------- |
| `/ap`                | Full 5-expert audit     |
| `/ap quick`          | Quick audit (2 experts) |
| `/ap security`       | Security focus only     |
| `/ap performance`    | Performance focus only  |
| `/ap expert [name]`  | Single expert audit     |
| `/ap --scope [path]` | Limit scope             |

---

_DOMYH Awesome Code v4.3 • Audit Pro v5.1 • Multi-Expert Consensus + 105 Checkpoints_
