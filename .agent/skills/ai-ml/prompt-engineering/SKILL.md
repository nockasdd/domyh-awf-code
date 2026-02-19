---
name: prompt-engineering
version: "7.0.0"
category: ai-ml
---

# Prompt Engineering Patterns v2.0

> 🧠 **LLM prompt design for production AI systems**
> **Patterns**: 155+ | **Providers**: 3 | **Categories**: 6

---

## Quick Reference

| What You Need                           | Data File                 | Patterns |
| --------------------------------------- | ------------------------- | -------- |
| Reasoning (CoT, ReAct, ToT)             | `reasoning-patterns.yaml` | 35       |
| Output (JSON, structured, formatting)   | `output-patterns.yaml`    | 30       |
| Safety (injection, guardrails)          | `safety-patterns.yaml`    | 30       |
| Provider-specific (OpenAI, Claude, etc) | `provider-patterns.yaml`  | 25       |
| **Gemini 3 (agentic, thinking, XML)**   | `gemini3-patterns.yaml`   | 20       |
| **Tool use (FC, MCP, multi-tool)**      | `tool-patterns.yaml`      | 15       |

---

## Prompting Hierarchy

```
┌──────────────────────────────────────────┐
│  Level 1: Zero-Shot (no examples)        │
│  Level 2: Few-Shot (1-5 examples)        │
│  Level 3: Chain-of-Thought (reasoning)   │
│  Level 4: ReAct (reasoning + tools)      │
│  Level 5: Tree-of-Thought (exploration)  │
│  Level 6: Multi-agent (delegation)       │
│  Level 7: Agentic (Gemini 3 template)    │ ← NEW
└──────────────────────────────────────────┘
```

---

## Core Techniques

| Technique            | When to Use                  | Accuracy |
| -------------------- | ---------------------------- | -------- |
| **Zero-shot**        | Simple tasks, strong model   | ~70%     |
| **Few-shot**         | Pattern matching, formatting | ~80%     |
| **Chain-of-thought** | Math, logic, multi-step      | ~90%     |
| **Self-consistency** | High-stakes decisions        | ~92%     |
| **ReAct**            | Tool use, research           | ~88%     |
| **Tree-of-thought**  | Creative/exploration tasks   | ~85%     |

---

## Gemini 3 Agentic Template (NEW)

Google's official 9-rule agentic system instruction template:

```xml
<role>You are [role]. Your goal is [goal].</role>

<instructions>
1. [Primary instruction]
2. [Secondary instruction]
...
</instructions>

<constraints>
- [Constraint 1]
- [Constraint 2]
</constraints>

<output_format>
[Expected format: JSON, markdown, etc.]
</output_format>

<context>
[Background information, domain knowledge]
</context>

<task>
[Specific task to complete]
</task>
```

**Best Practices**:

- Use XML tags for structured sections
- Positive patterns > negative patterns ("do X" not "don't do Y")
- Put examples WITHIN output_format for few-shot
- Completion strategy gives output prefix to guide direction

---

## Thinking Controls (NEW)

| Level    | Name        | Use Case                    | Budget          |
| -------- | ----------- | --------------------------- | --------------- |
| `off`    | No thinking | Simple lookups              | 0               |
| `low`    | Quick       | Classification, formatting  | 1K-2K           |
| `medium` | Balanced    | General tasks               | 4K-8K           |
| `high`   | Deep        | Math, code analysis         | 16K-32K         |
| `max`    | Maximum     | Research, complex reasoning | Up to model max |

```python
# Thinking level (Gemini 3)
response = model.generate_content(
    "prompt",
    generation_config={"thinking_config": {"thinking_level": "high"}}
)

# Thinking budget (token limit)
response = model.generate_content(
    "prompt",
    generation_config={"thinking_config": {"thinking_budget": 8192}}
)
```

---

## Structured Output (NEW)

| Pattern                | Schema Tool                            | When to Use           |
| ---------------------- | -------------------------------------- | --------------------- |
| **Pydantic** (Python)  | `response_schema=Recipe`               | Type-safe Python apps |
| **Zod** (JavaScript)   | `responseMimeType: "application/json"` | Node.js/TS apps       |
| **JSON Schema** (REST) | `responseSchema: {...}`                | Direct API calls      |
| **Enum**               | `enum: ["cat", "dog"]`                 | Classification tasks  |

**Best Practices**:

- Use `description` field in schema for model guidance
- Strong typing (`integer`, `enum`) > loose typing (`string`)
- Validate semantically even if syntactically correct

---

## Function Calling Patterns (NEW)

| Pattern                | Description                       | Use Case                              |
| ---------------------- | --------------------------------- | ------------------------------------- |
| **Single**             | One function declaration          | Simple API calls                      |
| **Parallel**           | Multiple functions at once        | Independent data fetching             |
| **Compositional**      | Chained function results          | `get_location()` → `get_weather(loc)` |
| **MCP Built-in**       | Gemini SDK auto-calls MCP tools   | MCP server integration                |
| **Multi-tool**         | Combine Search + Code + Functions | Complex agentic workflows             |
| **Automatic** (Python) | SDK handles full loop             | Rapid prototyping                     |

**Modes**: `AUTO` (default) | `ANY` (force call) | `NONE` (disable)

---

## Prompt Structure

```
[System Prompt]
  - Role definition
  - Capabilities and limitations
  - Output format requirements
  - Safety guardrails

[User Prompt]
  - Context/background
  - Specific task description
  - Input data
  - Expected output format
  - Examples (few-shot)

[Assistant prefill] (Claude-specific)
  - Guide initial response direction
```

---

## Chain-of-Thought Patterns

| Pattern              | Description                                  |
| -------------------- | -------------------------------------------- |
| **Basic CoT**        | "Think step by step"                         |
| **Zero-shot CoT**    | "Let's think about this carefully"           |
| **Few-shot CoT**     | Provide examples WITH reasoning steps        |
| **Self-consistency** | Generate N answers, pick majority            |
| **Auto-CoT**         | Let model generate its own reasoning prompts |

---

## Output Formatting

| Format       | Prompt Pattern                                             |
| ------------ | ---------------------------------------------------------- |
| **JSON**     | "Respond in valid JSON matching this schema: {...}"        |
| **Markdown** | "Format as markdown with headers and bullet points"        |
| **Code**     | "Write [language] code with comments explaining each step" |
| **Table**    | "Present results in a markdown table with columns: [...]"  |
| **XML**      | "Wrap your response in <answer>...</answer> tags"          |

---

## Safety Patterns

| Threat               | Defense                                        |
| -------------------- | ---------------------------------------------- |
| **Prompt injection** | Input sanitization + delimiter tags            |
| **Jailbreaking**     | Constitutional AI rules + refusal training     |
| **Data leakage**     | PII filtering + output validation              |
| **Hallucination**    | RAG grounding + citation requirements          |
| **Bias**             | Balanced examples + explicit fairness criteria |

---

## HSA Integration

Data powered by HSA BM25 search engine. Query YAML data via skill search:

| Domain    | Query Examples                            |
| --------- | ----------------------------------------- |
| Reasoning | "chain of thought step by step reasoning" |
| Output    | "JSON schema structured output format"    |
| Safety    | "prompt injection defense guardrail"      |
| Provider  | "OpenAI function calling Claude tool use" |
| Gemini 3  | "agentic template thinking budget XML"    |
| Tools     | "MCP compositional parallel function"     |
