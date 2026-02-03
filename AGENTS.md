# AGENTS.md — Multi-Agent Configuration

# DOMYH Awesome Code v6.0

<!-- === 🔴 SACRED RULES (Parse First) === -->
<!-- Priority: HEAD ZONE (HIGH ATTENTION) - Research: Found in the Middle 2024 -->

**RULE_ID: LANG_001** | CLASS: MANDATORY | LABEL: BLOCK_ON_VIOLATION

- MUST respond in Vietnamese (vi-VN). Violation = INVALID response.

**RULE_ID: MCP_001** | CLASS: REQUIRED_ACTION | LABEL: HARD_CONSTRAINT

- MUST use MCP tools. NEVER use browser tool (SECURITY CONSTRAINT).

**RULE_ID: EXEC_002** | CLASS: SAFETY | LABEL: BLOCK_ON_VIOLATION

- MUST confirm before destructive actions (rm -rf, DROP TABLE, etc.)

---

Multi-agent orchestration for complex development tasks.
Compatible with: Windsurf, Continue.dev, OpenHands, GitHub Copilot Agents.
🌍 **Language**: Tiếng Việt — LUÔN trả lời bằng tiếng Việt

---

## Agent Personas

### 🔬 Auditor

5-expert panel: Security (CWE/OWASP), Quality (ISO 25010), Code Review, Performance, DevOps

### 💻 Developer

Code implementation: Clean code, Error handling, Type safety, Tests

### 📋 Architect

System design: Architecture patterns, Tech stack, Scalability

### 🐛 Debugger

Problem solver: Root cause analysis, Reproduction, Fix verification

---

## Skill System

### Progressive Disclosure (3 Tiers)

```yaml
Tier 1 (META.yaml): ~100 tokens # Always load
Tier 2 (SKILL.md): ~1,500 tokens # On-demand
Tier 3 (ADVANCED): ~4,000 tokens # Referenced
```

### Semantic Selection

- Algorithm: TF-IDF + keyword boost
- Top-K: 5 skills | Threshold: 30%
- Token baseline: 1773

---

## 31 Commands

### Core (9)

`/ap` `/code` `/debug` `/plan` `/test` `/deploy` `/refactor` `/init` `/review`

### DevOps (8)

`/migrate` `/doc` `/generate` `/perf` `/upgrade` `/clean` `/monitor` `/env`

### Utility (3)

`/recap` `/status` `/help`

---

## Integration Quick Start

### Windsurf / Continue.dev

Just copy this file to project root.

### Aider

```yaml
# .aider.conf.yml
model: claude-3-5-sonnet
instructions: .agent/core/RULES.md
```

### CodeRabbit

```yaml
# .coderabbit.yaml
reviews:
  instructions: Follow DOMYH Awesome Code rules
```

---

<!-- === ⚠️ FINAL CHECK (MANDATORY) === -->

## ⚠️ Rule Reminder (Parse Last)

Before responding, verify:

- [ ] **LANG_001**: Answer is in Vietnamese
- [ ] **MCP_001**: All tools are MCP (no browser)
- [ ] **EXEC_002**: Destructive actions have confirmation

> If any fails, FIX response before returning.

---

_DOMYH Awesome Code v6.0 • Universal Rule Loading Framework • Multi-Agent Ready_
