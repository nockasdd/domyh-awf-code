# 🔍 Critic Template

> Self-critique before output (Reflexion Pattern)

---

## Purpose

This template guides the agent to critically evaluate its own output before delivering it to the user. Based on the **Reflexion** paper and Anthropic's self-critique patterns.

---

## Pre-Output Checklist

Before finalizing your response, evaluate against these criteria:

### 1. Task Alignment

- [ ] Does this output directly address the user's request?
- [ ] Have I answered what was actually asked (not what I assumed)?
- [ ] Is the scope appropriate (not too narrow or too broad)?

### 2. Accuracy & Evidence

- [ ] Is all information accurate and verifiable?
- [ ] Have I provided evidence (file:line, sources) for claims?
- [ ] Are there any statements that need verification?

### 3. Completeness

- [ ] Are there missing edge cases?
- [ ] Have I addressed all parts of the question?
- [ ] Is there important context I should mention?

### 4. Safety & Side Effects

- [ ] Could this output cause unintended harm?
- [ ] Are there any security implications?
- [ ] Does this respect the user's constraints?

### 5. Clarity & Usefulness

- [ ] Is the output clear and well-organized?
- [ ] Can the user immediately act on this?
- [ ] Have I explained the "why" not just the "what"?

---

## Critique Questions

Ask yourself:

1. **"If I were the user, would this answer satisfy me?"**
   - If no → Identify what's missing

2. **"What's the weakest part of my response?"**
   - Strengthen or acknowledge it

3. **"Am I 100% confident in this?"**
   - If no → Add uncertainty markers

4. **"Could an expert find fault with this?"**
   - If yes → Revise or add caveats

---

## Confidence Scoring

Rate your output:

| Score              | Meaning                  | Action                    |
| ------------------ | ------------------------ | ------------------------- |
| 🟢 High (>90%)     | Very confident, verified | Proceed                   |
| 🟡 Medium (60-90%) | Mostly confident         | Add caveats               |
| 🔴 Low (<60%)      | Uncertain                | Research more or ask user |

---

## Revision Protocol

If critique reveals issues:

```
1. IDENTIFY → What specifically is wrong?
2. CLASSIFY → Is it accuracy, completeness, or clarity?
3. REVISE → Make specific corrections
4. RE-EVALUATE → Does the revision fix the issue?
5. DOCUMENT → Note what was changed and why
```

---

## Example Critique

```markdown
### Self-Critique

**Task Alignment:** ✅ Addresses the user's request to fix the login bug
**Accuracy:** ⚠️ I assumed bcrypt is used - should verify
**Completeness:** ✅ Covered main case and 2 edge cases
**Safety:** ✅ No security implications from the fix
**Clarity:** ✅ Code is commented and explained

**Confidence:** 🟡 Medium (85%)
**Revision needed:** Verify the password hashing library before suggesting changes
```

---

# DOMYH Awesome Code • Reflection Template
