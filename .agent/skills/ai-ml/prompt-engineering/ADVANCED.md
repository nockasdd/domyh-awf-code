# Prompt Engineering — Advanced Patterns

## Table of Contents

- [Chain-of-Thought Prompting](#chain-of-thought-prompting)
- [Few-Shot Patterns](#few-shot-patterns)
- [System Prompt Architecture](#system-prompt-architecture)
- [Structured Output](#structured-output)
- [Advanced Techniques](#advanced-techniques)

---

## Chain-of-Thought Prompting

### Step-by-Step Reasoning

```yaml
pattern: |
  Think through this step by step:
  1. First, identify the core problem
  2. List all constraints and requirements
  3. Consider 2-3 possible approaches
  4. Evaluate trade-offs of each
  5. Select the best approach and explain why
  6. Implement the solution

example:
  task: "Design a rate limiter for an API"
  prompt: |
    Design a rate limiter for our API. Think step by step:
    1. What algorithm fits best? (Token bucket, Sliding window, Fixed window)
    2. What are the constraints? (Distributed, low latency, configurable)
    3. How to store state? (Redis, in-memory, database)
    4. How to handle edge cases? (Burst, multiple keys, graceful degradation)
    Show your reasoning before the implementation.
```

### Tree-of-Thought

```yaml
pattern: |
  Consider multiple approaches to solve this problem.
  For each approach:
  - Describe the approach in 1-2 sentences
  - Rate feasibility (1-5)
  - Rate quality (1-5)
  - List key risks

  Then select the best approach and implement it.
```

---

## Few-Shot Patterns

### Classification with Examples

```yaml
prompt: |
  Classify the following code review comment:

  Categories: bug, style, performance, security, suggestion

  Examples:
  - "This loop has O(n²) complexity" → performance
  - "Missing null check on line 15" → bug
  - "Consider using const instead of let" → style
  - "SQL injection risk in query builder" → security
  - "Could extract this into a helper function" → suggestion

  Classify: "The password is stored in plaintext"
  Answer:
```

### Code Generation Pattern

```yaml
prompt: |
  Generate a function following this pattern:

  // Input:
  function validateEmail(email: string): ValidationResult {
    if (!email) return { valid: false, error: 'Email required' }
    if (!email.includes('@')) return { valid: false, error: 'Invalid format' }
    return { valid: true }
  }

  // Now generate for:
  function validatePassword(password: string): ValidationResult
  // Rules: min 8 chars, 1 uppercase, 1 number, 1 special char
```

---

## System Prompt Architecture

### Layered System Prompt

```yaml
layers:
  identity: |
    You are a senior software engineer specializing in {stack}.
    You write production-quality code with error handling and tests.

  constraints: |
    Rules:
    - Always use TypeScript strict mode
    - Never use `any` type
    - Handle all error paths
    - Include JSDoc for public APIs
    - Follow {project} conventions

  context: |
    Project: {name}
    Stack: {tech_stack}
    Style guide: {link}
    Current task: {description}

  output_format: |
    Respond with:
    1. Brief analysis (2-3 sentences)
    2. Implementation (code blocks)
    3. Tests (if applicable)
    4. Edge cases considered

best_practices:
  - "Put most important instructions FIRST and LAST (primacy/recency)"
  - "Use XML tags for structure: <rules>, <context>, <output>"
  - "Be specific: 'max 200 words' not 'be brief'"
  - "Include negative examples: 'Do NOT use any type'"
  - "Test system prompt with adversarial inputs"
```

---

## Structured Output

### JSON Mode

```yaml
prompt: |
  Analyze the following code and return a JSON object:

  ```json
  {
    "complexity": "low|medium|high",
    "issues": [
      {
        "type": "bug|security|performance",
        "severity": "critical|high|medium|low",
        "line": number,
        "description": "string",
        "fix": "string"
      }
    ],
    "score": number (0-100),
    "summary": "string"
  }
  ```

  Code to analyze:
  {code}
```

---

## Advanced Techniques

```yaml
techniques:
  self_consistency:
    description: "Generate N responses, pick majority answer"
    use_when: "Reasoning tasks where accuracy matters"

  reflection:
    description: "Ask model to critique its own output"
    prompt: "Review your answer. What could be wrong? Correct any issues."

  meta_prompting:
    description: "Use LLM to generate prompts"
    prompt: "Generate the best prompt to solve: {task}"

  constitutional_ai:
    description: "Add principles to guide output"
    example: |
      Principles:
      1. Prefer simple solutions over clever ones
      2. Security is non-negotiable
      3. Readability > conciseness

anti_patterns:
  - "❌ Vague: 'Make it better'"
  - "❌ Too long: >2000 word system prompts"
  - "❌ Contradictory rules"
  - "❌ No examples for ambiguous tasks"
  - "❌ Assuming model knows project context"
```

---
