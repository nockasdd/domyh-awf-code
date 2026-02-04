# ✅ Success Analysis Template

> Reinforce good patterns (Positive Reflexion)

---

## Purpose

When a task succeeds or the user expresses satisfaction, analyze what worked well and store these patterns in `patterns/successes.json` for future reference.

---

## Success Detection Signals

Look for:

- User says "perfect", "exactly what I needed", "great"
- Task completed without revisions
- User immediately uses the output
- Follow-up questions indicate understanding
- No corrections needed

---

## Success Analysis Framework

### 1. What Worked?

```yaml
success:
  timestamp: "[ISO8601]"
  task: "[What was accomplished]"
  outcome: "[The result]"
  user_signal: "[How we know it succeeded]"
```

### 2. Key Patterns Identified

| Aspect            | What Worked                  |
| ----------------- | ---------------------------- |
| **Approach**      | [Method used]                |
| **Communication** | [How it was explained]       |
| **Evidence**      | [What evidence was provided] |
| **Structure**     | [How output was organized]   |
| **Tools**         | [Which tools were effective] |

### 3. Success Factors

Rate contribution to success:

| Factor             | Contribution | Evidence |
| ------------------ | ------------ | -------- |
| Clear requirements | High/Med/Low | [how]    |
| Thorough analysis  | High/Med/Low | [how]    |
| Good communication | High/Med/Low | [how]    |
| Appropriate tools  | High/Med/Low | [how]    |
| Self-critique      | High/Med/Low | [how]    |

---

## Pattern Extraction

### Generalizable Pattern

```yaml
pattern:
  name: "[Short descriptive name]"
  context: "[When this pattern applies]"
  approach: "[Step-by-step what to do]"
  key_elements:
    - "[Element 1]"
    - "[Element 2]"
  success_indicators: "[How to know it's working]"
```

### Replication Checklist

To replicate this success:

- [ ] [Step 1]
- [ ] [Step 2]
- [ ] [Step 3]

---

## Storage Format

Save to `patterns/successes.json`:

```json
{
  "patterns": [
    {
      "id": "SUC-001",
      "name": "thorough_api_documentation_review",
      "created": "2026-02-03T15:00:00Z",
      "uses": 1,
      "last_used": "2026-02-03T15:00:00Z",
      "context": "Implementing features with external APIs",
      "approach": [
        "1. Read official docs first",
        "2. Check for recent changes",
        "3. Test with simple example",
        "4. Implement incrementally"
      ],
      "key_elements": [
        "Always verify API version",
        "Include error handling examples",
        "Reference specific doc sections"
      ],
      "success_rate": 0.95,
      "category": "implementation"
    }
  ]
}
```

---

## Integration with Future Tasks

When starting a new task:

1. **Load successes.json** → Find relevant patterns
2. **Match context** → Does current task match any pattern?
3. **Apply approach** → Follow the successful approach
4. **Track** → Did it work again? Update `uses` count

---

## Example Analysis

```markdown
### Success Analysis: SUC-002

**What Worked:**

- Task: Debug authentication failure
- Outcome: Found and fixed root cause in 15 minutes
- User Signal: "That was exactly the issue, thanks!"

**Key Patterns:**

- Approach: Started with log analysis before code
- Communication: Showed evidence before suggesting fix
- Tools: Used grep to find all auth-related code first

**Generalizable Pattern:**

- Name: "Log-first debugging"
- Context: Any bug investigation
- Approach:
  1. Check logs/errors first
  2. Identify relevant code paths
  3. Form hypothesis
  4. Verify with evidence
  5. Fix with minimal change

**Stored as:** SUC-002 in patterns/successes.json
```

---

## Pattern Reinforcement

When a pattern is used successfully again:

1. **Increment uses** → `uses += 1`
2. **Update success rate** → `(old_rate * old_uses + 1) / new_uses`
3. **Promote if reliable** → Move to "proven patterns" if `uses > 5 && rate > 0.8`

---

# DOMYH Awesome Code v6.1.2 • Success Analysis Template
