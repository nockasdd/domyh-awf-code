# Stop Conditions v4.0

# Compact rules for halting execution

## ⛔ MUST STOP

### P0: Safety (Immediate)

```
• rm -rf, DROP TABLE
• Production environment
• Secrets exposure risk
→ CONFIRM with user
```

### P1: Missing Info

```
• No file/folder path provided
• Unclear error message
• Missing credentials/config
→ ASK for specifics
```

### P2: Ambiguity

```
• Multiple interpretations
• Conflicting requirements
• Scope unclear
→ CLARIFY before proceed
```

### P2: Error Loop

```
• Same error 3+ times
• Different approach failed
→ PAUSE, explain situation
```

## ✅ MAY CONTINUE

- Clear, unambiguous request
- Safe, reversible actions
- Development environment
- User explicitly approved

## 🚀 MUST CONTINUE (No Questions)

```
When workflow provides explicit flow:
• Follow steps in order
• Don't stop to confirm obvious actions
• Only ask for TRULY unknown info
• Use defaults when available

Example: "/init go api"
→ PROCEED with Go + Standard arch
→ DON'T ask: "Do you want Go?"
```

---

_DOMYH Agent v4.2_
