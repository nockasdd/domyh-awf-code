---
name: audit-pro
description: "12-Expert Panel audit with SCoT reasoning, cross-expert critique, and smart skill loading. v2: 277 checkpoints, 16 per-expert files, 11 weight profiles."
detect: []
priority: 1
category: cross-cutting
tier: 1
---

# Audit Pro v2 — 12-Expert Panel System

> 🔬 **277 Checkpoints** | **12 Experts** | **16 Files** | **11 Weight Profiles**
> 🧠 **SCoT Reasoning** | **Cross-Expert Critique** | **Smart Skill Loading**

---

## Decision Tree

```
User requests audit
    │
    ├─ /ap → Full audit (auto-detect all experts)
    ├─ /ap quick → Security + Architecture only
    ├─ /ap [expert] → Single expert
    ├─ /ap desktop → Core 5 + Desktop supplement
    ├─ /ap cli → Core 5 + CLI supplement
    ├─ /ap library → Core 5 + Library supplement
    ├─ /ap mcp → Core 5 + MCP supplement
    │
    ▼
  1. DISCOVERY → detect stack, project type, auto-activate experts
    │
    ▼
  2. SMART LOAD → per-expert checklists + skill patterns (~3000 tok)
    │
    ▼
  3. SCOPE CONTRACT → ⛔ STOP (user selects 1-10)
    │
    ▼
  4. EXECUTE → SCoT 7-step per checkpoint
    │
    ▼
  5. CRITIQUE ROUND → cross-expert challenge (P0/P1 only)
    │
    ▼
  6. HOLISTIC SYNTHESIS → 5 project-level questions (beyond checklists)
    │
    ▼
  7. DEBATE ROUND → IF systemic issues found, experts discuss
    │
    ▼
  8. SELF-REVIEW → deduplicate, verify, resolve disputes
    │
    ▼
  9. REPORT → score, findings, holistic assessment, debate summary
    │
    ▼
  10. PERSIST → save to memory
```

---

## Expert × Skill Matrix

| Expert | Skills Loaded | Total Patterns | Focus |
|:-------|:-------------|:--------------|:------|
| Security | security + authentication | 660+ | OWASP/CWE, auth, supply chain |
| Architecture | coding-rules + api-design | 360+ | SOLID, patterns, structure |
| Performance | observability + web-perf | 400+ | OTel, metrics, profiling |
| Quality | testing + error-handling + coding-rules | 510+ | Tests, errors, naming |
| DevOps | logging + observability | 705 | Logs, alerting, CI/CD |
| UX | domyh-design + web-perf | varies | WCAG, design system |
| Data | database + sql | varies | Schema, migrations |
| AI Safety | security (AI subset) | 20+ | Prompt injection, guardrails |

---

## SCoT Protocol (Per Checkpoint)

```yaml
# 7-step Structured Chain-of-Thought
scot_protocol:
  1_locate: "hsa_search for relevant code → file:line refs"
  2_understand: "What does this code actually do? (1 sentence)"
  3_assess: "Does it meet the checkpoint standard?"
  4_evidence: "Quote exact code or file:line (max 200 chars)"
  5_impact: "If it fails, worst case? → P0-P3 severity"
  6_counter: "Devil's advocate — why might this be acceptable?"
  7_verdict: "PASS | FAIL | N/A (confidence 1-10)"
```

---

## Critique Round Protocol

```yaml
# Cross-expert challenge on P0/P1 findings only
critique_round:
  pairs:
    - Security ↔ Architecture: "Arch issues → security vulns?"
    - Architecture ↔ Security: "Security measures → over-engineered?"
    - Performance ↔ Quality: "Quality improvements → perf impact?"
    - Quality ↔ Performance: "Perf optimizations → maintainable?"
    - DevOps ↔ Security: "Deployment practices → secure? Secrets managed?"
  outcomes:
    - AGREE: "Confirmed, severity appropriate"
    - DISPUTE: "Disagree because [reason]"
    - ELEVATE: "More severe than reported"
    - LOWER: "Less severe, recommend downgrade"
  rules:
    - Each expert MUST use their counter_argument_guide
    - Counter-argument is MANDATORY for every FAIL verdict
    - N/A verdicts still require brief justification
```

---

## Data Files (16 Checklists + 1 Scoring)

### Expert Checklists (12 files)

| File | Expert | Items | Activation |
|:-----|:-------|:------|:-----------|
| `checklists/security.yaml` | Security | 28 | always |
| `checklists/architecture.yaml` | Architecture | 26 | always |
| `checklists/performance.yaml` | Performance | 24 | always |
| `checklists/quality.yaml` | Quality | 24 | always |
| `checklists/devops.yaml` | DevOps | 24 | always |
| `checklists/ux.yaml` | UX | 16 | has_ui |
| `checklists/data.yaml` | Data | 15 | has_database |
| `checklists/compliance.yaml` | Compliance | 15 | is_regulated |
| `checklists/product.yaml` | Product | 13 | scope_full |
| `checklists/reliability.yaml` | Reliability | 15 | is_production |
| `checklists/cloud.yaml` | Cloud | 12 | has_infra |
| `checklists/ai-safety.yaml` | AI Safety | 10 | has_ai |

### Supplementary Checklists (4 files, NEW)

| File | Type | Items | Detection |
|:-----|:-----|:------|:----------|
| `checklists/desktop.yaml` | Desktop App | 15 | electron/tauri deps |
| `checklists/cli.yaml` | CLI Tool | 12 | commander/yargs/clap deps |
| `checklists/library.yaml` | Library/SDK | 14 | publishConfig/exports |
| `checklists/mcp-plugin.yaml` | MCP Plugin | 14 | @modelcontextprotocol deps |

### Scoring
| File | Content |
|:-----|:--------|
| `scoring.yaml` | 11 profiles, 10 scopes, grades, priorities |

---

## Usage

```
# Full audit
/ap

# Desktop app audit
/ap desktop

# Single expert
/ap expert security

# Compare with previous
/ap --compare
```

---
