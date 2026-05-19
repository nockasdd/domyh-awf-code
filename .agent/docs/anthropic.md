---
library: anthropic
version: latest
latest: true
category: ai-sdk
official_docs: https://docs.anthropic.com
last_updated: 2026-03-20
last_checked: 2026-03-21
---

# Anthropic Claude API

> Anthropic — Claude AI models. Messages API, tool use, extended thinking, prompt caching.
> Docs: https://docs.anthropic.com

## Installation

```bash
npm install @anthropic-ai/sdk
```

## Messages API

```ts
import Anthropic from '@anthropic-ai/sdk';

const anthropic = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });

// Basic completion
const message = await anthropic.messages.create({
  model: 'claude-sonnet-4-20250514',
  max_tokens: 1024,
  system: 'You are a helpful assistant.',
  messages: [
    { role: 'user', content: 'Explain REST APIs in one paragraph.' },
  ],
});

console.log(message.content[0].text);
// message.usage: { input_tokens, output_tokens }
// message.stop_reason: 'end_turn' | 'max_tokens' | 'stop_sequence' | 'tool_use'
```

### Streaming

```ts
// Event-based streaming
const stream = anthropic.messages.stream({
  model: 'claude-sonnet-4-20250514',
  max_tokens: 1024,
  messages: [{ role: 'user', content: 'Write a poem.' }],
});

stream.on('text', (text) => process.stdout.write(text));
const finalMessage = await stream.finalMessage();

// Async iterator
const stream2 = await anthropic.messages.create({
  model: 'claude-sonnet-4-20250514',
  max_tokens: 1024,
  messages: [{ role: 'user', content: 'Write a poem.' }],
  stream: true,
});

for await (const event of stream2) {
  if (event.type === 'content_block_delta' && event.delta.type === 'text_delta') {
    process.stdout.write(event.delta.text);
  }
}
```

### Multi-turn Conversation

```ts
const response = await anthropic.messages.create({
  model: 'claude-sonnet-4-20250514',
  max_tokens: 1024,
  system: 'You are a TypeScript expert.',
  messages: [
    { role: 'user', content: 'What is TypeScript?' },
    { role: 'assistant', content: 'TypeScript is a typed superset of JavaScript...' },
    { role: 'user', content: 'Show me a generic example.' },
  ],
});
```

### Vision (Image Input)

```ts
// Base64 image
const message = await anthropic.messages.create({
  model: 'claude-sonnet-4-20250514',
  max_tokens: 1024,
  messages: [{
    role: 'user',
    content: [
      {
        type: 'image',
        source: { type: 'base64', media_type: 'image/png', data: base64Data },
      },
      { type: 'text', text: 'What is in this image?' },
    ],
  }],
});

// URL image
const message2 = await anthropic.messages.create({
  model: 'claude-sonnet-4-20250514',
  max_tokens: 1024,
  messages: [{
    role: 'user',
    content: [
      { type: 'image', source: { type: 'url', url: 'https://example.com/image.jpg' } },
      { type: 'text', text: 'Describe this image in detail.' },
    ],
  }],
});

// Multiple images
const message3 = await anthropic.messages.create({
  model: 'claude-sonnet-4-20250514',
  max_tokens: 1024,
  messages: [{
    role: 'user',
    content: [
      { type: 'image', source: { type: 'url', url: 'https://example.com/before.jpg' } },
      { type: 'image', source: { type: 'url', url: 'https://example.com/after.jpg' } },
      { type: 'text', text: 'What changed between these two images?' },
    ],
  }],
});
```

## Tool Use (Function Calling)

### Client Tools (Custom)

```ts
const response = await anthropic.messages.create({
  model: 'claude-sonnet-4-20250514',
  max_tokens: 1024,
  tools: [{
    name: 'get_weather',
    description: 'Get current weather for a city. Returns temperature and conditions.',
    input_schema: {
      type: 'object',
      properties: {
        city: { type: 'string', description: 'City name, e.g. "San Francisco"' },
        unit: { type: 'string', enum: ['celsius', 'fahrenheit'], description: 'Temperature unit' },
      },
      required: ['city'],
    },
  },
  {
    name: 'search_database',
    description: 'Search the product database by query',
    input_schema: {
      type: 'object',
      properties: {
        query: { type: 'string' },
        limit: { type: 'number', description: 'Max results (default: 10)' },
      },
      required: ['query'],
    },
  }],
  messages: [{ role: 'user', content: 'What is the weather in Tokyo?' }],
});

// Handle tool use loop
if (response.stop_reason === 'tool_use') {
  const toolUse = response.content.find(block => block.type === 'tool_use');
  const result = await executeFunction(toolUse.name, toolUse.input);

  // Send tool result back
  const finalResponse = await anthropic.messages.create({
    model: 'claude-sonnet-4-20250514',
    max_tokens: 1024,
    tools: [/* same tools */],
    messages: [
      { role: 'user', content: 'What is the weather in Tokyo?' },
      { role: 'assistant', content: response.content },
      {
        role: 'user',
        content: [{
          type: 'tool_result',
          tool_use_id: toolUse.id,
          content: JSON.stringify(result),
          // is_error: true,  // set if tool execution failed
        }],
      },
    ],
  });
}
```

### Server Tools (web_search, web_fetch)

```ts
// Web Search — runs on Anthropic servers, no implementation needed
const response = await anthropic.messages.create({
  model: 'claude-sonnet-4-20250514',
  max_tokens: 1024,
  tools: [{
    type: 'web_search_20250305',
    name: 'web_search',
    max_uses: 5,  // limit searches per request
  }],
  messages: [{ role: 'user', content: 'Latest TypeScript release notes' }],
});

// Web Fetch — fetch and read web pages
const response2 = await anthropic.messages.create({
  model: 'claude-sonnet-4-20250514',
  max_tokens: 1024,
  tools: [{
    type: 'web_fetch_20250305',
    name: 'web_fetch',
  }],
  messages: [{ role: 'user', content: 'Read and summarize https://example.com/article' }],
});
```

### Tool Choice

```ts
// Force specific tool
tool_choice: { type: 'tool', name: 'get_weather' }

// Let Claude decide
tool_choice: { type: 'auto' }

// Force ANY tool (must use one)
tool_choice: { type: 'any' }
```

## Extended Thinking

```ts
const response = await anthropic.messages.create({
  model: 'claude-sonnet-4-20250514',
  max_tokens: 16000,
  thinking: {
    type: 'enabled',
    budget_tokens: 10000,  // tokens allocated for thinking
  },
  messages: [{ role: 'user', content: 'Solve this complex math problem step by step...' }],
});

// Response includes thinking blocks
for (const block of response.content) {
  if (block.type === 'thinking') {
    console.log('Thinking:', block.thinking);
  } else if (block.type === 'text') {
    console.log('Answer:', block.text);
  }
}
```

## Prompt Caching

```ts
// Cache system prompt (saves cost on repeated calls)
const response = await anthropic.messages.create({
  model: 'claude-sonnet-4-20250514',
  max_tokens: 1024,
  system: [
    {
      type: 'text',
      text: 'You are an expert on the following codebase...\n[large context here]',
      cache_control: { type: 'ephemeral' },  // cache this block
    },
  ],
  messages: [{ role: 'user', content: 'How does the auth module work?' }],
});

// Check cache performance
console.log(response.usage);
// { input_tokens, output_tokens, cache_creation_input_tokens, cache_read_input_tokens }

// Multi-turn with cached context
const messages = [
  {
    role: 'user',
    content: [{
      type: 'text',
      text: largeDocument,
      cache_control: { type: 'ephemeral' },  // cache user message
    }],
  },
  { role: 'assistant', content: 'I have read the document...' },
  { role: 'user', content: 'Summarize section 3.' },
];
```

### Caching Strategies

```ts
// 1-hour extended cache (for long-running sessions)
cache_control: { type: 'ephemeral', ttl: 3600 }

// What can be cached: system prompt, tools, messages with images/documents
// What CANNOT: response tokens, thinking blocks
// Minimum cacheable: 1024 tokens (Sonnet/Opus), 2048 tokens (Haiku)
// Cache invalidation: ANY change to cached content invalidates it
```

## Batches API

```ts
// Create batch of requests (50% cost discount)
const batch = await anthropic.batches.create({
  requests: items.map((item, i) => ({
    custom_id: `request-${i}`,
    params: {
      model: 'claude-sonnet-4-20250514',
      max_tokens: 1024,
      messages: [{ role: 'user', content: item.prompt }],
    },
  })),
});

// Poll for completion
let result = await anthropic.batches.retrieve(batch.id);
while (result.processing_status === 'in_progress') {
  await new Promise(resolve => setTimeout(resolve, 10000));
  result = await anthropic.batches.retrieve(batch.id);
}

// Results available at result.results_url
```

## Models Reference

| Model | API Name | Context | Best For | Cost |
|:------|:---------|:--------|:---------|:-----|
| Claude Opus 4 | `claude-opus-4-20250514` | 200K | Most capable, complex tasks | $$$$ |
| Claude Sonnet 4 | `claude-sonnet-4-20250514` | 200K | Best balance, coding | $$$ |
| Claude Haiku 3.5 | `claude-3-5-haiku-20241022` | 200K | Fast + cheap, classification | $ |

## Common Patterns

### System Prompt Best Practices

```ts
// Structured system prompt
const systemPrompt = `You are a senior TypeScript developer assistant.

## Rules
- Always provide TypeScript examples with proper types.
- Use modern patterns: async/await, const assertions, discriminated unions.
- Explain your reasoning before showing code.

## Context
- Project uses: Next.js 15 App Router, Prisma, TanStack Query
- Style: functional components, Zod for validation
- Node.js 22 LTS`;
```

### Agentic Loop

```ts
async function agentLoop(userMessage: string) {
  let messages: Anthropic.MessageParam[] = [{ role: 'user', content: userMessage }];

  while (true) {
    const response = await anthropic.messages.create({
      model: 'claude-sonnet-4-20250514',
      max_tokens: 4096,
      tools: tools,
      messages,
    });

    // Append assistant response
    messages.push({ role: 'assistant', content: response.content });

    if (response.stop_reason === 'end_turn') {
      return response.content.filter(b => b.type === 'text').map(b => b.text).join('');
    }

    if (response.stop_reason === 'tool_use') {
      const toolResults = [];
      for (const block of response.content) {
        if (block.type === 'tool_use') {
          const result = await executeFunction(block.name, block.input);
          toolResults.push({
            type: 'tool_result' as const,
            tool_use_id: block.id,
            content: JSON.stringify(result),
          });
        }
      }
      messages.push({ role: 'user', content: toolResults });
    }
  }
}
```

## Gotchas & Breaking Changes

⚠️ **`stop_reason: 'tool_use'`**: Must check — Claude stops when it wants to call a tool.

⚠️ **Content blocks**: `message.content` is an array of blocks `{type: 'text'|'tool_use'|'thinking'}`, not a string.

⚠️ **`max_tokens` required**: Mandatory param — unlike OpenAI where it's optional.

⚠️ **System prompt**: Separate `system` param — NOT inside `messages` array.

⚠️ **Tool schemas**: Use `input_schema` (JSON Schema format), NOT `parameters` like OpenAI.

⚠️ **Streaming events**: `content_block_delta` → `text_delta` for text, `input_json_delta` for tool args.

⚠️ **Prompt caching**: Minimum 1024 tokens to cache. Cache invalidated on ANY content change.

⚠️ **Server tools**: `web_search_20250305` — versioned type names, no client implementation needed.

⚠️ **Extended thinking**: `budget_tokens` controls how long Claude thinks. Higher = better reasoning, more cost.

⚠️ **Batches**: 50% cost discount but async — results in hours, not seconds.

## Agent SDK

```ts
// TypeScript Agent SDK — multi-step autonomous agents
import { Agent, run } from '@anthropic-ai/agent-sdk';

const agent = new Agent({
  name: 'code-assistant',
  model: 'claude-sonnet-4-20250514',
  instructions: 'You are a senior TypeScript developer.',
  tools: [/* custom tools, MCP servers */],
});

const result = await run(agent, 'Fix the bug in auth.ts');
```

```python
# Python Agent SDK
from anthropic_agent_sdk import Agent, run

agent = Agent(
    name="code-assistant",
    model="claude-sonnet-4-20250514",
    instructions="You are a senior TypeScript developer.",
)

result = run(agent, "Fix the bug in auth.ts")
```

Features: Custom tools, MCP integration, structured outputs, user approvals/input, permissions, Skills

## Agent Skills

```ts
// Installable skills for agents — pre-built capabilities
// Available at: platform.claude.com/docs/en/agents-and-tools/agent-skills

// API quickstart for skills
const response = await anthropic.messages.create({
  model: 'claude-sonnet-4-20250514',
  max_tokens: 1024,
  // Skills provide structured tool definitions
  tools: agentSkills,
  messages: [{ role: 'user', content: 'Deploy the app' }],
});
```

## Code Execution Tool

```ts
// Sandboxed code execution — runs Python on Anthropic servers
const response = await anthropic.messages.create({
  model: 'claude-sonnet-4-20250514',
  max_tokens: 4096,
  tools: [{ type: 'code_execution_20250522', name: 'code_execution' }],
  messages: [{ role: 'user', content: 'Calculate fibonacci(30) and plot it' }],
});
```

## Files API

```ts
// Upload files for processing across multiple conversations
const file = await anthropic.files.upload({
  file: fs.createReadStream('large-document.pdf'),
  purpose: 'user_message',
});

const response = await anthropic.messages.create({
  model: 'claude-sonnet-4-20250514',
  max_tokens: 1024,
  messages: [{
    role: 'user',
    content: [
      { type: 'file', file_id: file.id },
      { type: 'text', text: 'Summarize this document' },
    ],
  }],
});
```

## Fast Mode (Beta)

```ts
// Research preview — faster responses for simpler tasks
const response = await anthropic.messages.create({
  model: 'claude-sonnet-4-20250514',
  max_tokens: 1024,
  // Fast mode automatically simplifies processing
  messages: [{ role: 'user', content: 'What is 2 + 2?' }],
});
```

## Context & Compaction

```ts
// Compaction — automatically summarize long conversations
// Useful for multi-turn agents hitting context limits

// Context editing — modify previous messages in conversation
// Context windows: 200K tokens for all Claude models

// Effort control — adjust response detail level
const response = await anthropic.messages.create({
  model: 'claude-sonnet-4-20250514',
  max_tokens: 1024,
  // effort: 'low' | 'medium' | 'high' — controls response thoroughness
  messages: [{ role: 'user', content: 'Quick answer: capital of France?' }],
});
```

## Additional Gotchas

⚠️ **Agent SDK**: Available in Python and TypeScript. Supports multi-step agents with tool use + MCP.

⚠️ **Code execution tool**: Sandboxed Python execution. Type: `code_execution_20250522`.

⚠️ **Files API**: Upload once, use across conversations. Supported: PDF, images, text files.

⚠️ **Fast mode**: Beta/research preview. Faster but may reduce quality for complex tasks.

⚠️ **Compaction**: Use for long multi-turn agents to stay within context window.

⚠️ **Context editing**: Can modify previous messages — useful for correcting conversation flow.

⚠️ **Computer use tool**: Type `computer_20241022` — lets Claude control mouse/keyboard in sandbox.

⚠️ **Bash tool**: Type `bash_20241022` — lets Claude execute shell commands in sandbox.

⚠️ **Data residency**: Available for enterprise — choose US or EU data processing region.

⚠️ **Admin API**: Manage organization, workspaces, API keys programmatically.
