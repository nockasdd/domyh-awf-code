---
name: ai-agents
version: "6.4.0"
category: ai-ml
---

# AI Agent Orchestration — LangChain • CrewAI • AutoGen

> Multi-agent systems • LLM API integration • Agent rules  
> Tool use • Memory management • Production patterns

---

## Khi Nào Dùng

- Xây dựng AI agents (single/multi-agent)
- Integrate LLM APIs (OpenAI, Anthropic, Gemini)
- Thiết kế agent orchestration patterns
- Implement agent memory & tool use
- Cấu hình agent rules (Cursor, Cline, AGENTS.md)

## Orchestration Patterns

```
┌─────────────────────────────────────────────────────┐
│ SUPERVISOR (recommended for complex tasks)          │
│                                                     │
│  ┌──────────┐                                       │
│  │Supervisor│──┬──▶ Agent A (Research)               │
│  │(Router)  │  ├──▶ Agent B (Code)                   │
│  └──────────┘  └──▶ Agent C (Review)                 │
│                                                     │
│ SWARM (for collaborative tasks)                     │
│  Agent A ◄──▶ Agent B ◄──▶ Agent C                   │
│                                                     │
│ SEQUENTIAL (for pipeline tasks)                     │
│  Agent A ──▶ Agent B ──▶ Agent C                     │
└─────────────────────────────────────────────────────┘
```

| Pattern          | Use Case                   | Complexity         |
| ---------------- | -------------------------- | ------------------ |
| **Sequential**   | ETL, simple pipelines      | ⭐ Low             |
| **Supervisor**   | Complex tasks, routing     | ⭐⭐ Medium        |
| **Swarm**        | Collaborative, peer review | ⭐⭐⭐ High        |
| **Hierarchical** | Enterprise, delegation     | ⭐⭐⭐⭐ Very High |

## LLM API Integration

### Multi-Provider Pattern

```typescript
// Provider-agnostic interface
interface LLMProvider {
  chat(messages: Message[], options?: Options): Promise<Response>;
  stream(messages: Message[], options?: Options): AsyncGenerator<Chunk>;
}

// Structured output (all providers)
const result = await llm.chat(messages, {
  responseFormat: { type: "json_schema", schema: userSchema },
});
```

### Function Calling

```typescript
// Tool definition (OpenAI format, widely adopted)
const tools = [
  {
    type: "function",
    function: {
      name: "search_database",
      description: "Search the product database",
      parameters: {
        type: "object",
        properties: {
          query: { type: "string" },
          limit: { type: "number", default: 10 },
        },
        required: ["query"],
      },
    },
  },
];
```

### Streaming

```typescript
// SSE streaming pattern
for await (const chunk of llm.stream(messages)) {
  process.stdout.write(chunk.content); // real-time output
}
```

## Agent Rules Systems

| System     | Location              | Format                       | Scope            |
| ---------- | --------------------- | ---------------------------- | ---------------- |
| **Cursor** | `.cursor/rules/*.mdc` | MDC (frontmatter + markdown) | Dynamic per-file |
| **Cursor** | Settings → Rules      | Plain text                   | Global user      |
| **Cline**  | `.clinerules/`        | Markdown files               | Project          |
| **Codex**  | `AGENTS.md`           | Markdown                     | Project          |
| **DOMYH**  | `.agent/skills/`      | YAML + Markdown              | Hierarchical     |

### Best Practices

1. **Concise** — Under 500 lines per rule file
2. **Specific** — Show patterns, not just principles
3. **Scoped** — Use glob patterns for context-specific rules
4. **Layered** — Global → Project → File-specific

## Memory Patterns

| Type         | Duration   | Storage     | Use Case              |
| ------------ | ---------- | ----------- | --------------------- |
| **Buffer**   | Session    | In-memory   | Chat history          |
| **Summary**  | Session    | In-memory   | Long conversations    |
| **Vector**   | Persistent | Vector DB   | Recall past knowledge |
| **Episodic** | Persistent | DB + Vector | Event-based recall    |

## Production Checklist

- ✅ Rate limiting per provider API key
- ✅ Retry with exponential backoff
- ✅ Token usage tracking & cost alerts
- ✅ Async queue for long-running agents
- ✅ Human-in-the-loop for destructive actions
- ✅ Observability: traces, spans, token counts
- ✅ Fallback provider on rate limit

## Common Traps

| Trap                    | Fix                                            |
| ----------------------- | ---------------------------------------------- |
| Context window overflow | Summarize history, trim old messages           |
| Agent loops             | Max iterations limit, break conditions         |
| Hallucination in tools  | Validate tool outputs, constrained prompts     |
| High costs              | Cache responses, use smaller models for triage |
| Prompt injection        | Input sanitization, system prompt protection   |

---

_DOMYH Awesome Code • AI Agents Skill v1.0.0_
