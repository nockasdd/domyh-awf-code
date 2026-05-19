---
library: openai
version: latest
latest: true
category: ai-sdk
official_docs: https://developers.openai.com/docs
last_updated: 2026-03-20
last_checked: 2026-03-21
---

# OpenAI API

> OpenAI — GPT-5.4, reasoning models, image/video gen, audio, embeddings.
> SDK: `openai` (official Node.js)
> Docs: https://developers.openai.com/docs

## Installation

```bash
npm install openai
```

## Responses API (Recommended)

The Responses API is the recommended way to interact with OpenAI models. It's simpler than Chat Completions and supports built-in tools.

```ts
import OpenAI from 'openai';

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

// Basic text generation
const response = await openai.responses.create({
  model: 'gpt-5.4',
  input: 'Explain REST APIs in one paragraph.',
});
console.log(response.output_text);

// With instructions
const response2 = await openai.responses.create({
  model: 'gpt-5.4-mini',
  instructions: 'You are a senior TypeScript developer. Be concise.',
  input: 'Explain generics.',
});
```

### Built-in Tools

```ts
// Web Search
const response = await openai.responses.create({
  model: 'gpt-5.4',
  input: 'What are the latest TypeScript release notes?',
  tools: [{ type: 'web_search_preview' }],
});

// File Search (from vector store)
const response2 = await openai.responses.create({
  model: 'gpt-5.4',
  input: 'What does our refund policy say?',
  tools: [{ type: 'file_search', vector_store_ids: ['vs_xxx'] }],
});

// Code Interpreter
const response3 = await openai.responses.create({
  model: 'gpt-5.4',
  input: 'Calculate the standard deviation of [4, 8, 15, 16, 23, 42]',
  tools: [{ type: 'code_interpreter' }],
});

// Computer Use (preview)
const response4 = await openai.responses.create({
  model: 'computer-use-preview',
  input: 'Navigate to example.com and take a screenshot.',
  tools: [{
    type: 'computer_use_preview',
    display_width: 1024,
    display_height: 768,
    environment: 'browser',
  }],
});
```

### Conversation State

```ts
// Continue conversation with previous_response_id
const first = await openai.responses.create({
  model: 'gpt-5.4',
  input: 'My name is Alice.',
});

const second = await openai.responses.create({
  model: 'gpt-5.4',
  input: 'What is my name?',
  previous_response_id: first.id,
});
// "Your name is Alice."
```

## Chat Completions API (Legacy but widely used)

```ts
const completion = await openai.chat.completions.create({
  model: 'gpt-5.4',
  messages: [
    { role: 'system', content: 'You are a TypeScript expert.' },
    { role: 'user', content: 'Explain generics in one paragraph.' },
  ],
  temperature: 0.7,
  max_tokens: 1024,
});

console.log(completion.choices[0].message.content);
```

### Streaming

```ts
const stream = await openai.chat.completions.create({
  model: 'gpt-5.4-mini',
  messages: [{ role: 'user', content: 'Write a poem.' }],
  stream: true,
});

for await (const chunk of stream) {
  process.stdout.write(chunk.choices[0]?.delta?.content ?? '');
}

// Helper method
const runner = openai.chat.completions.stream({
  model: 'gpt-5.4-mini',
  messages: [{ role: 'user', content: 'Write a poem.' }],
});
runner.on('content', (delta) => process.stdout.write(delta));
const finalContent = await runner.finalContent();
```

### Vision

```ts
const response = await openai.chat.completions.create({
  model: 'gpt-5.4',
  messages: [{
    role: 'user',
    content: [
      { type: 'text', text: 'What is in this image?' },
      { type: 'image_url', image_url: { url: 'https://example.com/image.jpg' } },
    ],
  }],
});

// Base64 image
content: [
  { type: 'text', text: 'Describe this screenshot.' },
  { type: 'image_url', image_url: { url: `data:image/png;base64,${base64Data}` } },
]
```

### Structured Output

```ts
import { zodResponseFormat } from 'openai/helpers/zod';
import { z } from 'zod';

const CalendarEvent = z.object({
  name: z.string(),
  date: z.string(),
  participants: z.array(z.string()),
  location: z.string().optional(),
});

const completion = await openai.beta.chat.completions.parse({
  model: 'gpt-5.4',
  messages: [
    { role: 'system', content: 'Extract event info from user text.' },
    { role: 'user', content: 'Team standup tomorrow at 10am with Alice and Bob in Room 5.' },
  ],
  response_format: zodResponseFormat(CalendarEvent, 'calendar_event'),
});

const event = completion.choices[0].message.parsed;
// { name: 'Team standup', date: '...', participants: ['Alice', 'Bob'], location: 'Room 5' }
```

## Function Calling (Tool Use)

```ts
const response = await openai.chat.completions.create({
  model: 'gpt-5.4',
  messages: [{ role: 'user', content: 'What is the weather in San Francisco?' }],
  tools: [{
    type: 'function',
    function: {
      name: 'get_weather',
      description: 'Get the current weather for a city.',
      strict: true,
      parameters: {
        type: 'object',
        properties: {
          city: { type: 'string', description: 'City name' },
          unit: { type: 'string', enum: ['celsius', 'fahrenheit'] },
        },
        required: ['city'],
        additionalProperties: false,
      },
    },
  }],
  tool_choice: 'auto',  // 'auto' | 'none' | 'required' | { type: 'function', function: { name: '...' } }
});

// Handle tool calls
const toolCall = response.choices[0].message.tool_calls?.[0];
if (toolCall) {
  const args = JSON.parse(toolCall.function.arguments);
  const result = await getWeather(args.city, args.unit);

  // Send result back
  const finalResponse = await openai.chat.completions.create({
    model: 'gpt-5.4',
    messages: [
      { role: 'user', content: 'What is the weather in San Francisco?' },
      response.choices[0].message,
      { role: 'tool', tool_call_id: toolCall.id, content: JSON.stringify(result) },
    ],
  });
}
```

## Reasoning Models

```ts
// GPT-5.4 supports built-in reasoning
const response = await openai.responses.create({
  model: 'gpt-5.4',
  input: 'Solve this step by step: If a car travels at 60mph for 2.5 hours, then 80mph for 1.5 hours, what is the total distance?',
  reasoning: {
    effort: 'high',  // 'low' | 'medium' | 'high'
  },
});

// Access reasoning summary
console.log(response.output_text);
```

## Embeddings

```ts
const response = await openai.embeddings.create({
  model: 'text-embedding-3-small',  // or text-embedding-3-large
  input: 'What is machine learning?',
  dimensions: 512,  // optional: reduce dimensions (trade quality for speed)
});

const embedding = response.data[0].embedding;  // number[]

// Batch embeddings
const batch = await openai.embeddings.create({
  model: 'text-embedding-3-small',
  input: ['Text 1', 'Text 2', 'Text 3'],
});
```

## Image Generation

```ts
// gpt-image-1
const image = await openai.images.generate({
  model: 'gpt-image-1',
  prompt: 'A modern minimalist logo for a tech startup',
  quality: 'high',
  size: '1536x1024',
});
console.log(image.data[0].url);

// DALL-E 3
const image2 = await openai.images.generate({
  model: 'dall-e-3',
  prompt: 'A watercolor painting of a sunset',
  n: 1,
  size: '1024x1024',
  quality: 'hd',
  style: 'natural',  // 'vivid' | 'natural'
});
```

## Audio (Speech & Transcription)

```ts
// Speech-to-text (Whisper)
const transcription = await openai.audio.transcriptions.create({
  model: 'whisper-1',
  file: fs.createReadStream('audio.mp3'),
  language: 'en',
});
console.log(transcription.text);

// Text-to-speech
const speech = await openai.audio.speech.create({
  model: 'tts-1',  // or tts-1-hd
  voice: 'alloy',  // alloy, echo, fable, onyx, nova, shimmer
  input: 'Hello, welcome to our application!',
  response_format: 'mp3',
});

const buffer = Buffer.from(await speech.arrayBuffer());
fs.writeFileSync('speech.mp3', buffer);
```

## Agents SDK

```ts
// OpenAI Agents SDK — build multi-agent workflows
// npm install @openai/agents

import { Agent, run } from '@openai/agents';

const agent = new Agent({
  name: 'research-agent',
  model: 'gpt-5.4-mini',
  instructions: 'You are a research assistant. Use web search to find information.',
  tools: [{ type: 'web_search_preview' }],
});

const result = await run(agent, 'What are the latest trends in AI?');
console.log(result.finalOutput);
```

## Models Reference

| Model | API Name | Best For |
|:------|:---------|:---------|
| GPT-5.4 | `gpt-5.4` | Flagship — complex reasoning, agentic, coding |
| GPT-5.4 Mini | `gpt-5.4-mini` | Strong mini — coding, computer use, sub-agents |
| GPT-5.4 Nano | `gpt-5.4-nano` | Cheapest GPT-5.4-class — high-volume simple tasks |
| GPT-4o | `gpt-4o` | Previous gen — still capable, multimodal |
| GPT-4o Mini | `gpt-4o-mini` | Previous gen mini — fast, cheap |
| gpt-image-1 | `gpt-image-1` | Image generation |
| DALL-E 3 | `dall-e-3` | Image generation (legacy) |
| Embedding Small | `text-embedding-3-small` | Embeddings (fast) |
| Embedding Large | `text-embedding-3-large` | Embeddings (high quality) |
| Whisper-1 | `whisper-1` | Speech-to-text |
| TTS-1 / TTS-1 HD | `tts-1` | Text-to-speech |

## Prompt Caching

```ts
// Prompt caching automatically caches repeated prompt prefixes
// No code changes needed — just reuse the same system prompt
// Reduces latency and cost for repeated prefixes

// Check cache usage in response
const response = await openai.chat.completions.create({
  model: 'gpt-5.4',
  messages: [
    { role: 'system', content: longSystemPrompt },  // cached after first call
    { role: 'user', content: userQuery },
  ],
});
// response.usage.prompt_tokens_details.cached_tokens
```

## Gotchas

⚠️ **GPT-5.4**: Flagship model (replaces GPT-4o for complex tasks). Use `gpt-5.4-mini` for cost optimization.

⚠️ **Responses API vs Chat Completions**: Responses API is recommended — simpler, has built-in tools (web search, file search, code interpreter). Chat Completions is more mature/widely used.

⚠️ **`tool_calls`** (not `function_call`): Modern API uses `tools` array and `tool_calls` in response.

⚠️ **`strict: true`**: Enable strict mode in function definitions for guaranteed JSON Schema compliance.

⚠️ **Structured output**: Use `zodResponseFormat` from `openai/helpers/zod` for type-safe parsing.

⚠️ **Prompt caching**: Automatic for repeated prefixes. Keep system prompts consistent for cache hits.

⚠️ **Embeddings dimensions**: `text-embedding-3-*` supports `dimensions` param — smaller = faster.

⚠️ **Rate limits**: Use exponential backoff. Check `x-ratelimit-remaining` headers.

⚠️ **`previous_response_id`**: In Responses API, maintains conversation without managing message arrays.

⚠️ **Agents SDK**: Install separately with `@openai/agents`. Supports multi-agent orchestration.
