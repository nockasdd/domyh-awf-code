---
description: "🔒 Security scanning & remediation: SAST, SCA, secrets, containers, licenses"
skills: { required: [security], contextual: [auto] }
success_criteria: "Scan complete, findings documented with CWE references"
---

# 🔒 /security — Security Pro

> Active Security Scanning & Automated Remediation
> 📚 SAST • SCA • Secrets • Containers • Licenses • Auto-Fix
> ℹ️ For checklist-based audit, use `/ap security`. This workflow runs actual tools.

---

## SECURITY FLOW

1. **DETECT** — Identify stack via HSA (`hsa_detect`), discover available security tools, load security context (`hsa_search`). Show: `[Step 1/6] Detecting: Node.js + Go monorepo`
2. **SCAN** — Execute selected scan type(s), collect findings in structured format. Show: `[Step 2/6] Running SAST scan... 47 files analyzed`
3. **ANALYZE** — Deduplicate, correlate findings, assign severity (Critical/High/Medium/Low), filter false positives. Show: `[Step 3/6] Found: 2 critical, 5 high, 12 medium`
4. **REPORT** — Structured report with evidence, CWE/CVE references, fix suggestions. Show severity summary
5. **FIX** (Optional) — Auto-fix safe issues, suggest fixes for complex ones → ⛔ STOP: confirm before applying
6. **SYNC** — `hsa_check_changes` to update index after fixes

---

## COMMANDS

| Command                    | Description               | Scope                       |
| -------------------------- | ------------------------- | --------------------------- |
| `/security`                | Full scan (all types)     | Entire project              |
| `/security scan`           | Full scan (explicit)      | Entire project              |
| `/security sast`           | Static analysis           | Source code vulnerabilities |
| `/security deps`           | Dependency audit (SCA)    | Known CVEs in dependencies  |
| `/security secrets`        | Secret scanning           | Leaked credentials/keys     |
| `/security container`      | Container image scan      | Dockerfile/image vulns      |
| `/security license`        | License compliance        | OSS license risks           |
| `/security fix [id]`       | Auto-fix specific finding | Single vulnerability        |
| `/security --scope [path]` | Limit scan scope          | Specific directory/file     |
| `/security --ci`           | CI-friendly output        | JSON/SARIF for CI pipelines |

---

## 🛠️ TOOL REGISTRY

### SAST (Static Application Security Testing)

```yaml
sast_tools:
  javascript:
    primary: "npx semgrep --config auto --json"
    fallback: "npx eslint --plugin security --format json"
  python:
    primary: "bandit -r src/ -f json"
    fallback: "ruff check --select S --output-format json"
  go:
    primary: "gosec -fmt json ./..."
    fallback: "go vet ./..."
  java:
    primary: "semgrep --config auto --json"
  ruby:
    primary: "brakeman --format json"
  php:
    primary: "phpstan analyse --error-format json"
  general:
    primary: "semgrep --config auto --json"
```

### SCA (Software Composition Analysis)

```yaml
sca_tools:
  npm: "npm audit --json"
  yarn: "yarn audit --json"
  pnpm: "pnpm audit --json"
  pip: "pip-audit --format json"
  go: "govulncheck -json ./..."
  cargo: "cargo audit --json"
  maven: "mvn dependency-check:check"
  nuget: "dotnet list package --vulnerable --format json"
  composer: "composer audit --format json"
  bundler: "bundle audit check --format json"
```

### Secrets Scanning

```yaml
secret_patterns:
  high_confidence:
    - "AWS[_-]?(ACCESS|SECRET)[_-]?KEY"
    - "AKIA[0-9A-Z]{16}" # AWS Access Key
    - "ghp_[a-zA-Z0-9]{36}" # GitHub PAT
    - "sk-[a-zA-Z0-9]{48}" # OpenAI API Key
    - "xoxb-[0-9]{10,13}" # Slack Bot Token
    - "PRIVATE KEY-----" # Private keys
  checks:
    - ".env files not in .gitignore"
    - "Hardcoded passwords in config"
    - "API keys in source code"
    - "Tokens in commit history"
  tools:
    primary: "trufflehog filesystem --json ."
    fallback: "grep -rn patterns"
```

### Container Scanning

```yaml
container_tools:
  primary: "trivy image --format json"
  alternatives:
    - "docker scout cves --format json"
    - "grype image --output json"
  filesystem: "trivy fs --format json ."
```

### License Compliance

```yaml
license_tools:
  npm: "npx license-checker --json"
  pip: "pip-licenses --format json"
  go: "go-licenses csv ."
  cargo: "cargo license --json"

risk_levels:
  copyleft: ["GPL-2.0", "GPL-3.0", "AGPL-3.0"] # 🔴 High risk
  weak_copyleft: ["LGPL-2.1", "MPL-2.0"] # 🟡 Medium risk
  permissive: ["MIT", "Apache-2.0", "BSD-2", "ISC"] # 🟢 Low risk
```

---

## 📊 FINDING FORMAT

```
🔒 [CRITICAL] CWE-89: SQL Injection
📁 src/api/users.go:42
📝 Unsanitized user input in SQL query
🔍 Evidence: `db.Query("SELECT * FROM users WHERE id=" + userID)`
💡 Fix: Use parameterized query `db.Query("SELECT * FROM users WHERE id=$1", userID)`
📚 Ref: https://cwe.mitre.org/data/definitions/89.html
```

---

## 📋 REPORT FORMAT

```
🔒 SECURITY SCAN — [project] — [date]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Scan Types: SAST ✅ | SCA ✅ | Secrets ✅ | Container ⏭️ | License ✅

| Severity | Count | Auto-fixable |
| Critical |     2 |            1 |
| High     |     5 |            3 |
| Medium   |    12 |            8 |
| Low      |     7 |            7 |

⏱️ Duration: 45s | Files: 128 | Dependencies: 47
📁 Full: .domyh/security/scan_YYYY-MM-DD.json
```

---

## 🔄 vs `/ap security`

| Feature  | `/security`            | `/ap security`   |
| -------- | ---------------------- | ---------------- |
| Type     | **Active scanning**    | Checklist review |
| Tools    | SAST/SCA/Secrets/Trivy | AI analysis only |
| Speed    | ~2-5 min               | ~30 min          |
| Output   | Scan results + SARIF   | Audit findings   |
| Auto-fix | ✅ Yes                 | ❌ No            |
| When     | During development     | Pre-release gate |
| CI/CD    | ✅ `--ci` flag         | ❌ Interactive   |

> 💡 **Best practice**: Run `/security` during development, `/ap security` before release.

---

## ⛔ SAFETY

- Confirm with user before applying auto-fixes
- Never expose actual secret values in reports (mask to `sk-****...****`)
- Warn before scanning large directories (> 10,000 files)
- Skip scanning `node_modules/`, `vendor/`, `.git/` by default
- Output findings to `.domyh/security/` (gitignored) for sensitive content
---

## 🔄 CASCADE EVALUATION (Recommended — MCP)

⚠️ **Evaluate before EXECUTE step** — see `delegation-intelligence` skill for scoring.

For deep security analysis, delegate to specialized reasoning model via cascade:
```
hsa_delegate({action:'cascade', cascade_text:'[detailed prompt]', task_type:'review'})
→ wait 5s → hsa_delegate({action:'cascade_read', cascade_id:'...'})
→ repeat cascade_read (3-5s intervals, max 10 polls)
```
**Auto-cascade** (weighted score ≥6.5): OWASP Top 10, crypto vulnerability assessment
**Suggest cascade** (weighted score 4.0-6.5): Auth review, data handling patterns

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

