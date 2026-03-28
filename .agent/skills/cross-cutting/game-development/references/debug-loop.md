# Debug Loop Protocol — Game Development

> Systematic debugging for game scripts via MCP bridge.  
> Max 5 iterations per debug session (rule GCS_006).

---

## Flow Diagram

```
START → Is Engine Open?
  ├─ NO  → STOP: "Please open Unity/UE Editor"
  └─ YES → Bridge Health Check
              ├─ FAIL  → STOP: "MCP bridge not responding"
              └─ PASS  →
                  ┌─────────────────────────────┐
                  │   ITERATION 1-5             │
                  │                             │
                  │  1. COMPILE                 │
                  │     Unity: compile_scripts  │
                  │     UE: ue_execute_python    │
                  │           ↓                 │
                  │  2. PARSE LOGS              │
                  │     Read error messages     │
                  │     Categorize (see below)  │
                  │           ↓                 │
                  │  3. MATCH GOTCHAS           │
                  │     Check gotchas.yaml      │
                  │     Apply known fix         │
                  │           ↓                 │
                  │  4. APPLY FIX               │
                  │     Edit script code        │
                  │     Or modify via bridge    │
                  │           ↓                 │
                  │  5. VERIFY                  │
                  │     Re-compile              │
                  │     Check runtime logs      │
                  │           ↓                 │
                  │  ✅ PASS → EXIT             │
                  │  ❌ FAIL → NEXT ITERATION   │
                  │  ⚠️ 5x FAIL → ESCALATE     │
                  └─────────────────────────────┘
```

---

## Error Categories

### Category 1: Compile Errors (Auto-fixable ✅)

| Error Pattern | Cause | Auto-Fix |
|:-------------|:------|:---------|
| `CS1002: ; expected` | Missing semicolon | Add `;` at line |
| `CS0246: type not found` | Missing using directive | Add `using UnityEngine;` etc. |
| `CS0103: name does not exist` | Typo or wrong variable name | Suggest correction |
| `CS1513: } expected` | Missing closing brace | Add `}` at scope end |
| `CS0029: Cannot convert` | Type mismatch | Cast or convert type |

### Category 2: Runtime Errors (Usually auto-fixable ⚠️)

| Error Pattern | Cause | Auto-Fix |
|:-------------|:------|:---------|
| `NullReferenceException` | Unassigned reference | Add null check + SerializeField |
| `MissingComponentException` | GetComponent returns null | Add [RequireComponent] or null check |
| `MissingReferenceException` | Destroyed object accessed | Check lifecycle, use pool |
| `IndexOutOfRangeException` | Array bounds exceeded | Add bounds check |

### Category 3: Logic Errors (Partial auto-fix ⚠️)

| Error Pattern | Cause | Auto-Fix |
|:-------------|:------|:---------|
| Object not moving | Wrong physics setup | Check Rigidbody, gravity, constraints |
| Score not updating | Event not connected | Check Singleton, event listeners |
| Game not ending | State not changing | Check GameManager.ChangeState calls |
| Enemy not spawning | Spawner timing wrong | Check spawn rate, pool size |

### Category 4: Visual Errors (Needs screenshot 📸)

| Error Pattern | Cause | Auto-Fix |
|:-------------|:------|:---------|
| Sprites invisible | Wrong sorting layer | Set Sorting Layer + Order |
| UI not showing | No Canvas or wrong mode | Add Canvas, set Overlay mode |
| Camera wrong angle | Offset misconfigured | Recalculate camera offset |
| Objects overlapping | Z-fighting | Adjust Z positions |

---

## Log Parsing Patterns

### Unity Console Log Format

```regex
# Error
^([\w\.]+Exception): (.+)$
^([\w\.]+)\((\d+),(\d+)\): error (CS\d+): (.+)$

# Warning
^([\w\.]+)\((\d+),(\d+)\): warning (CS\d+): (.+)$

# Runtime
^NullReferenceException: Object reference not set.*
  at (\w+)\.(\w+) \(.*\) \[.*\] in (.+):(\d+)$
```

### UE Python Error Format

```regex
# Python error
^LogPython: Error: (.+)$
^Traceback \(most recent call last\):$
^  File "(.+)", line (\d+), in (.+)$
^(\w+Error): (.+)$

# Remote Control error
^LogRemoteControl: Error: (.+)$
^HTTP (\d+): (.+)$
```

---

## Escalation Protocol

After 5 failed iterations, provide user with:

```markdown
## Debug Summary

### Errors Remaining
1. [Error type]: [Message] at [file:line]

### Fixes Attempted
1. Iteration 1: [What was tried] → [Result]
2. Iteration 2: [What was tried] → [Result]
...

### Root Cause Analysis
- [Best guess at root cause]
- [What additional info is needed]

### Recommended Next Steps
1. [Manual action for user]
2. [Alternative approach]
3. [External resource/documentation]
```

---
