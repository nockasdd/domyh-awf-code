---
library: vercel-ai
version: latest
latest: true
category: ai-sdk
official_docs: https://ai-sdk.dev
last_updated: 2026-03-20
last_checked: 2026-03-21
---

# Vercel AI SDK v4

> AI SDK — The TypeScript toolkit for building AI-powered applications.
> Supports: OpenAI, Anthropic, Google, Mistral, and more.
> Docs: https://ai-sdk.dev

## Installation

```bash
npm install ai @ai-sdk/openai         # OpenAI provider
npm install ai @ai-sdk/anthropic      # Anthropic provider
npm install ai @ai-sdk/google         # Google provider
```

## Core Functions

### generateText

```ts
import { generateText } from 'ai';
import { openai } from '@ai-sdk/openai';

const { text, usage } = await generateText({
  model: openai('gpt-4o'),
  prompt: 'Explain quantum computing in one paragraph.',
  maxTokens: 500,
  temperature: 0.7,
});
```

### streamText

```ts
import { streamText } from 'ai';
import { anthropic } from '@ai-sdk/anthropic';

const result = streamText({
  model: anthropic('claude-sonnet-4-20250514'),
  messages: [
    { role: 'system', content: 'You are a helpful assistant.' },
    { role: 'user', content: 'Write a poem about coding.' },
  ],
});

for await (const chunk of result.textStream) {
  process.stdout.write(chunk);
}
```

### generateObject (Structured Output)

```ts
import { generateObject } from 'ai';
import { openai } from '@ai-sdk/openai';
import { z } from 'zod';

const { object } = await generateObject({
  model: openai('gpt-4o'),
  schema: z.object({
    recipe: z.object({
      name: z.string(),
      ingredients: z.array(z.object({
        name: z.string(),
        amount: z.string(),
      })),
      steps: z.array(z.string()),
    }),
  }),
  prompt: 'Generate a recipe for chocolate cake.',
});
// object.recipe.name, object.recipe.ingredients, etc.
```

### Tool Calling

```ts
import { generateText, tool } from 'ai';
import { z } from 'zod';

const result = await generateText({
  model: openai('gpt-4o'),
  tools: {
    weather: tool({
      description: 'Get the weather for a location',
      parameters: z.object({
        location: z.string().describe('City name'),
      }),
      execute: async ({ location }) => {
        return { temperature: 72, condition: 'sunny' };
      },
    }),
  },
  prompt: 'What is the weather in San Francisco?',
});
```

## Next.js Integration

### Route Handler (Streaming)

```ts
// app/api/chat/route.ts
import { streamText } from 'ai';
import { openai } from '@ai-sdk/openai';

export async function POST(req: Request) {
  const { messages } = await req.json();

  const result = streamText({
    model: openai('gpt-4o'),
    messages,
  });

  return result.toDataStreamResponse();
}
```

### Client Hook

```tsx
'use client';
import { useChat } from 'ai/react';

export function Chat() {
  const { messages, input, handleInputChange, handleSubmit, isLoading } = useChat();

  return (
    <div>
      {messages.map(m => (
        <div key={m.id}>{m.role}: {m.content}</div>
      ))}
      <form onSubmit={handleSubmit}>
        <input value={input} onChange={handleInputChange} />
        <button disabled={isLoading}>Send</button>
      </form>
    </div>
  );
}
```

## Embeddings

```ts
import { embed, embedMany } from 'ai';
import { openai } from '@ai-sdk/openai';

// Single embedding
const { embedding } = await embed({
  model: openai.embedding('text-embedding-3-small'),
  value: 'What is the meaning of life?',
});

// Batch embeddings
const { embeddings } = await embedMany({
  model: openai.embedding('text-embedding-3-small'),
  values: ['Hello', 'World', 'AI SDK'],
});
```

## Multi-Provider

```ts
import { openai } from '@ai-sdk/openai';
import { anthropic } from '@ai-sdk/anthropic';
import { google } from '@ai-sdk/google';

// Same API — swap models freely
const result1 = await generateText({ model: openai('gpt-4o'), prompt: '...' });
const result2 = await generateText({ model: anthropic('claude-sonnet-4-20250514'), prompt: '...' });
const result3 = await generateText({ model: google('gemini-2.0-flash'), prompt: '...' });
```

## streamObject (Structured Streaming)

```ts
import { streamObject } from 'ai';
import { z } from 'zod';

const result = streamObject({
  model: openai('gpt-4o'),
  schema: z.object({
    recipes: z.array(z.object({
      name: z.string(),
      ingredients: z.array(z.string()),
    })),
  }),
  prompt: 'Generate 3 recipes.',
});

for await (const partialObject of result.partialObjectStream) {
  console.log(partialObject);  // progressively typed partial object
}
```

## Gotchas

⚠️ **Provider packages**: Each AI provider needs its own `@ai-sdk/*` package.

⚠️ **`useChat` vs `useCompletion`**: `useChat` for multi-turn, `useCompletion` for single-turn.

⚠️ **Structured output**: Use `generateObject` with Zod schema — not manual JSON parsing.

⚠️ **Streaming**: `streamText` returns async iterable. Use `.toDataStreamResponse()` for Next.js.

⚠️ **Embeddings**: Use `openai.embedding('text-embedding-3-small')` — note `.embedding()` method, not `openai()`.

⚠️ **Multi-provider**: Same `generateText`/`streamText` API works across all providers — swap model only.

## Multi-Step Agents

```ts
import { generateText, tool } from 'ai';
import { openai } from '@ai-sdk/openai';
import { z } from 'zod';

const result = await generateText({
  model: openai('gpt-4o'),
  maxSteps: 10, // allow up to 10 tool call → result cycles
  tools: {
    search: tool({
      description: 'Search the knowledge base',
      parameters: z.object({ query: z.string() }),
      execute: async ({ query }) => searchDB(query),
    }),
    calculate: tool({
      description: 'Perform math calculations',
      parameters: z.object({ expression: z.string() }),
      execute: async ({ expression }) => eval(expression),
    }),
  },
  system: 'You are a helpful assistant. Use tools when needed.',
  prompt: 'What is the total revenue from Q4 2024?',
  onStepFinish({ text, toolCalls, toolResults }) {
    console.log('Step:', { text, toolCalls, toolResults });
  },
});
// result.steps — array of all intermediate steps
// result.text — final answer after all tool rounds
```

## Agentic Tool Ecosystem

```ts
// Community tools — add with one import
import { executeCode } from 'ai-sdk-tool-code-execution';    // Vercel Sandbox
import { webSearch } from '@exalabs/ai-sdk';                  // Exa web search
import { tavilySearch } from '@tavily/ai-sdk';                // Tavily search
import { scrapeTool } from 'firecrawl-aisdk';                 // Web scraping
import { perplexitySearch } from '@perplexity-ai/ai-sdk';     // Perplexity

const { text } = await generateText({
  model: openai('gpt-4o'),
  tools: {
    executeCode: executeCode(),
    webSearch: webSearch(),
    scrape: scrapeTool,
  },
  maxSteps: 5,
  prompt: 'Search the web for Node.js 22 features, then write code to demo one.',
});
```

## Middleware & Custom Providers

```ts
import { wrapLanguageModel } from 'ai';

// Add logging/caching/rate-limiting as middleware
const wrappedModel = wrapLanguageModel({
  model: openai('gpt-4o'),
  middleware: {
    transformParams: async ({ params }) => {
      console.log('Request:', JSON.stringify(params.prompt));
      return params;
    },
    wrapGenerate: async ({ doGenerate }) => {
      const startTime = Date.now();
      const result = await doGenerate();
      console.log(`Latency: ${Date.now() - startTime}ms`);
      return result;
    },
  },
});

// Custom provider registry
import { createProviderRegistry } from 'ai';
const registry = createProviderRegistry({
  openai, anthropic, google,
});
const model = registry.languageModel('openai:gpt-4o');
```

## MCP Integration

```ts
import { experimental_createMCPClient as createMCPClient } from 'ai';

const mcpClient = await createMCPClient({
  transport: {
    type: 'sse',
    url: 'https://my-mcp-server.com/sse',
  },
});

const tools = await mcpClient.tools(); // auto-discovers tools
const result = await generateText({
  model: openai('gpt-4o'),
  tools,
  maxSteps: 5,
  prompt: 'Use the MCP tools to complete this task.',
});

await mcpClient.close();
```

## RAG Pattern

```ts
import { embed, embedMany, generateText, tool } from 'ai';
import { openai } from '@ai-sdk/openai';
import { z } from 'zod';

// 1. Embed & store documents
const chunks = document.split('.').filter(Boolean);
const { embeddings } = await embedMany({
  model: openai.embedding('text-embedding-3-small'),
  values: chunks,
});
// Store embeddings + chunks in pgvector / Supabase

// 2. Retrieve & generate
const result = await generateText({
  model: openai('gpt-4o'),
  tools: {
    searchKnowledge: tool({
      description: 'Search knowledge base for relevant info',
      parameters: z.object({ query: z.string() }),
      execute: async ({ query }) => {
        const { embedding } = await embed({
          model: openai.embedding('text-embedding-3-small'),
          value: query,
        });
        return findSimilarChunks(embedding); // cosine similarity
      },
    }),
  },
  maxSteps: 3,
  prompt: userQuestion,
});
```
