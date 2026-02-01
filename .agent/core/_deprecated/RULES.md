# DOMYH Agent Rules v4.0

# Compact, token-efficient rules

# Target: ~500 tokens

## 🎯 Evidence Rule

```
ALL findings MUST include:
• file:line reference
• Code snippet (3-5 lines)
• No guessing allowed
```

## 🛡️ Safety Rule

```
CONFIRM before:
• Deleting files
• Dropping tables
• Production changes
• Destructive commands
```

## ⛔ Stop Conditions

```
STOP and ASK when:
• Missing critical info
• Ambiguous request
• Scope creep detected
• 3+ errors in loop
```

## 📋 Quality Standards

| Standard     | Focus                        |
| ------------ | ---------------------------- |
| ISO 25010    | Reliability, Maintainability |
| CWE Top 25   | Critical vulnerabilities     |
| OWASP Top 10 | Web security                 |

## 🔤 Language

```
Response in same language as user.
If unclear → use system lang setting.
```

## 📝 Finding Format

```
[Pn] Title — location
• What: issue description
• Why: impact/risk
• Fix: solution
```

Priority: P0 (critical) → P3 (low)

---

_DOMYH Agent v4.2 • Optimized for token efficiency_
