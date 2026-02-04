# 📊 Error Analysis Template

> Learn from mistakes (Reflexion Memory Pattern)

---

## Purpose

When an error occurs or the user corrects the agent, use this template to analyze what went wrong and prevent future occurrences. Store insights in `patterns/errors.json`.

---

## Error Analysis Framework

### 1. What Happened?

```yaml
error:
  timestamp: "[ISO8601]"
  task: "[What was being attempted]"
  symptom: "[What went wrong]"
  user_feedback: "[What the user said]"
```

### 2. Root Cause Analysis (5 Whys)

```
Why 1: [First level cause]
  ↓
Why 2: [Deeper cause]
  ↓
Why 3: [Even deeper]
  ↓
Why 4: [Getting to root]
  ↓
Why 5: [Root cause]
```

### 3. Error Classification

| Category                | Examples                      |
| ----------------------- | ----------------------------- |
| **Assumption Error**    | Assumed library X was used    |
| **Context Missing**     | Didn't have full requirements |
| **Hallucination**       | Generated non-existent API    |
| **Scope Creep**         | Did more than asked           |
| **Incomplete Analysis** | Missed edge case              |
| **Tool Misuse**         | Wrong tool for the job        |
| **Communication Gap**   | Misunderstood request         |

### 4. Impact Assessment

- **Severity:** P0/P1/P2/P3
- **User Trust Impact:** High/Medium/Low
- **Time Wasted:** Xh
- **Recoverable:** Yes/No

---

## Lesson Extraction

### Pattern to Avoid

```yaml
pattern:
  name: "[Short name for the pattern]"
  trigger: "[What situation triggers this error]"
  wrong_action: "[What was done incorrectly]"
  correct_action: "[What should be done instead]"
  detection: "[How to recognize this situation]"
```

### Prevention Strategy

1. **Before action:** [Check to add]
2. **During action:** [Verification step]
3. **After action:** [Validation step]

---

## Storage Format

Save to `patterns/errors.json`:

```json
{
  "patterns": [
    {
      "id": "ERR-001",
      "name": "assumed_library_without_verification",
      "created": "2026-02-03T15:00:00Z",
      "occurrences": 1,
      "trigger": "Suggesting code fixes for authentication",
      "wrong_action": "Assumed bcrypt was used without checking imports",
      "correct_action": "Grep for password hashing library before suggesting",
      "detection_rule": "Before suggesting crypto-related fixes, verify the actual library",
      "severity": "P2",
      "category": "assumption_error"
    }
  ]
}
```

---

## Integration with Future Tasks

When starting a new task:

1. **Load errors.json** → Check for relevant patterns
2. **Match context** → Does current task match any trigger?
3. **Apply prevention** → Follow the prevention strategy
4. **Verify** → Confirm the error pattern is avoided

---

## Example Analysis

```markdown
### Error Analysis: ERR-002

**What Happened:**

- Task: Implement user authentication
- Symptom: Suggested code that used deprecated API
- User Feedback: "This API was removed in v3.0"

**Root Cause (5 Whys):**

1. Why deprecated? → Used old documentation
2. Why old docs? → Searched web without checking date
3. Why no date check? → Online research rule not applied
4. Why not applied? → Rushed to provide answer
5. Why rushed? → Assumed simple task

**Classification:** Assumption Error + Context Missing

**Lesson:**

- Pattern: Using outdated APIs
- Trigger: Suggesting library-specific code
- Prevention: Always check library version and docs date

**Stored as:** ERR-002 in patterns/errors.json
```

---

# DOMYH Awesome Code v6.1.2 • Error Analysis Template
