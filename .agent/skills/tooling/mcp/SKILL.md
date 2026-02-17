---
name: mcp
version: "6.3.1"
category: tooling
---

# MCP — Model Context Protocol Server Development

> Skill cho phát triển MCP servers & clients  
> JSON-RPC 2.0 • Tool/Resource/Prompt primitives • OAuth 2.1

---

## Khi Nào Dùng

- Xây dựng MCP server kết nối AI agents với tools/data
- Phát triển custom tools, resources, prompts cho Claude/Gemini/ChatGPT
- Thiết kế transport layer (stdio local, Streamable HTTP production)
- Implement OAuth 2.1 cho MCP servers remote

## Architecture

```
┌─────────────────────────────────────────┐
│           HOST APPLICATION              │
│  (Claude Desktop, VS Code, IDE...)      │
│                                         │
│  ┌──────────┐  ┌──────────┐             │
│  │ Client A │  │ Client B │  ← 1:1 map  │
│  └────┬─────┘  └────┬─────┘             │
└───────│──────────────│──────────────────┘
        │              │
  ┌─────▼─────┐  ┌─────▼─────┐
  │ Server A  │  │ Server B  │  ← Bounded context
  │ (Files)   │  │ (GitHub)  │  ← Single responsibility
  └───────────┘  └───────────┘
```

## Core Patterns

### Transport Selection

| Transport           | Use Case                           | Auth               |
| ------------------- | ---------------------------------- | ------------------ |
| **stdio**           | Local dev, CLI tools, same-machine | Not required       |
| **Streamable HTTP** | Remote, production, multi-user     | OAuth 2.1 required |

### Tool Design (CRITICAL)

```typescript
// ✅ GOOD: Stateless, idempotent, bounded
server.tool(
  "search_files",
  {
    query: z.string(),
    maxResults: z.number().default(10),
  },
  async ({ query, maxResults }) => {
    const results = await search(query, maxResults);
    return { content: [{ type: "text", text: JSON.stringify(results) }] };
  },
);

// ❌ BAD: Stateful, unbounded results
server.tool("get_all_data", {}, async () => {
  return { content: [{ type: "text", text: entireDatabase }] }; // OOM!
});
```

### Tool Rules

1. **Stateless** — No side effects between calls
2. **Idempotent** — Same input → same output
3. **Bounded** — Use `maxResults` + pagination tokens
4. **Validated** — JSON Schema cho tất cả inputs
5. **Documented** — Clear description cho AI model

### Resource Design

```typescript
// Static resource
server.resource("config", "config://app", async () => ({
  contents: [{ uri: "config://app", text: configData }],
}));

// Dynamic resource template
server.resourceTemplate("user/{id}", async (uri) => ({
  contents: [{ uri, text: await getUser(uri.params.id) }],
}));
```

## Security Checklist

- ✅ OAuth 2.1 cho HTTP transport
- ✅ Input validation (JSON Schema)
- ✅ Response size limits
- ✅ Rate limiting per client
- ✅ No secrets in tool outputs
- ✅ Sanitize file paths (prevent traversal)

## Common Traps

| Trap                 | Giải pháp                                    |
| -------------------- | -------------------------------------------- |
| Response quá lớn     | Pagination tokens, `maxResults`              |
| Timeout              | Set timeout per tool, return partial results |
| Error classification | Use JSON-RPC error codes (-32600 to -32603)  |
| Concurrent requests  | Stateless design, no shared mutable state    |
| Transport mismatch   | stdio=dev only, HTTP=prod with OAuth         |

## SDK Quick Reference

| Language   | Package                     | Docs                    |
| ---------- | --------------------------- | ----------------------- |
| TypeScript | `@modelcontextprotocol/sdk` | modelcontextprotocol.io |
| Python     | `mcp`                       | modelcontextprotocol.io |

---

_DOMYH Awesome Code • MCP Skill v1.0.0_
