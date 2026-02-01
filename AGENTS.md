# AGENTS.md — Multi-Agent Configuration

# DOMYH Awesome Code v4.3

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

## 20 Commands

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

_DOMYH Awesome Code v4.3 • Multi-Agent Ready_
