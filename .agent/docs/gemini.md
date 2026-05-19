---
library: gemini
version: latest
latest: true
category: ai-sdk
official_docs: https://ai.google.dev
last_updated: 2026-03-20
last_checked: 2026-03-21
source: official docs + crawl4ai/trafilatura extraction
---

# Google Gemini API

> Gemini — Google's multimodal AI models. Text, vision, code, and more.
> SDK: `@google/genai` (recommended) | Legacy: `@google/generative-ai`
> Docs: https://ai.google.dev

## Installation

```bash
npm install @google/genai
```

## Text Generation

```ts
import { GoogleGenAI } from '@google/genai';

const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });

// Basic generation
const response = await ai.models.generateContent({
  model: 'gemini-2.5-flash',
  contents: 'Explain REST APIs in one paragraph.',
});
console.log(response.text);

// With system instruction and config
const response2 = await ai.models.generateContent({
  model: 'gemini-2.5-flash',
  contents: 'Write a TypeScript interface for a User.',
  config: {
    systemInstruction: 'You are a senior TypeScript developer.',
    temperature: 0.7,
    topP: 0.9,
    topK: 40,
    maxOutputTokens: 2048,
    stopSequences: ['---'],
  },
});
```

### Streaming

```ts
const response = await ai.models.generateContentStream({
  model: 'gemini-2.5-flash',
  contents: 'Write a comprehensive guide to Svelte 5.',
});

for await (const chunk of response) {
  process.stdout.write(chunk.text ?? '');
}

// Get final aggregated response
const result = await response;
console.log(result.text);
console.log(result.usageMetadata);
```

### Multi-turn Chat

```ts
const chat = ai.chats.create({
  model: 'gemini-2.5-flash',
  config: {
    systemInstruction: 'You are a helpful coding assistant.',
  },
  history: [
    { role: 'user', parts: [{ text: 'What is TypeScript?' }] },
    { role: 'model', parts: [{ text: 'TypeScript is a typed superset...' }] },
  ],
});

const response = await chat.sendMessage('Show me a generics example.');
console.log(response.text);

// Streaming chat
const streamResponse = await chat.sendMessageStream('Explain more about utility types.');
for await (const chunk of streamResponse) {
  process.stdout.write(chunk.text ?? '');
}
```

## Vision (Image/Video)

```ts
import { createPartFromUri, createPartFromBase64 } from '@google/genai';
import * as fs from 'fs';

// From file path
const imageData = fs.readFileSync('photo.jpg');
const base64Image = imageData.toString('base64');

const response = await ai.models.generateContent({
  model: 'gemini-2.5-flash',
  contents: [
    createPartFromBase64(base64Image, 'image/jpeg'),
    { text: 'Describe what you see in this image.' },
  ],
});

// From URL
const response2 = await ai.models.generateContent({
  model: 'gemini-2.5-flash',
  contents: [
    { text: 'What is in this image?' },
    { fileData: { fileUri: 'https://example.com/image.jpg', mimeType: 'image/jpeg' } },
  ],
});

// Multiple images (comparison)
const response3 = await ai.models.generateContent({
  model: 'gemini-2.5-flash',
  contents: [
    createPartFromBase64(before, 'image/png'),
    createPartFromBase64(after, 'image/png'),
    { text: 'What changed between these two images?' },
  ],
});
```

## Structured Output (JSON)

```ts
import { Type } from '@google/genai';

const response = await ai.models.generateContent({
  model: 'gemini-2.5-flash',
  contents: 'List 3 programming languages with their use cases.',
  config: {
    responseMimeType: 'application/json',
    responseSchema: {
      type: Type.ARRAY,
      items: {
        type: Type.OBJECT,
        properties: {
          name: { type: Type.STRING, description: 'Language name' },
          useCases: {
            type: Type.ARRAY,
            items: { type: Type.STRING },
            description: 'Primary use cases',
          },
          popularity: {
            type: Type.STRING,
            enum: ['high', 'medium', 'low'],
          },
        },
        required: ['name', 'useCases', 'popularity'],
      },
    },
  },
});

const languages = JSON.parse(response.text);
```

## Function Calling (Tool Use)

```ts
// Define tools
const tools = [{
  functionDeclarations: [{
    name: 'get_weather',
    description: 'Get current weather for a location',
    parameters: {
      type: Type.OBJECT,
      properties: {
        city: { type: Type.STRING, description: 'City name' },
        unit: { type: Type.STRING, enum: ['celsius', 'fahrenheit'] },
      },
      required: ['city'],
    },
  }, {
    name: 'search_products',
    description: 'Search products in the catalog',
    parameters: {
      type: Type.OBJECT,
      properties: {
        query: { type: Type.STRING },
        maxResults: { type: Type.NUMBER },
      },
      required: ['query'],
    },
  }],
}];

const response = await ai.models.generateContent({
  model: 'gemini-2.5-flash',
  contents: 'What is the weather in Tokyo?',
  config: { tools },
});

// Handle function call
const functionCall = response.candidates?.[0]?.content?.parts?.find(p => p.functionCall);
if (functionCall) {
  const { name, args } = functionCall.functionCall;
  const result = await executeFunction(name, args);

  // Send result back
  const finalResponse = await ai.models.generateContent({
    model: 'gemini-2.5-flash',
    contents: [
      { role: 'user', parts: [{ text: 'What is the weather in Tokyo?' }] },
      { role: 'model', parts: [functionCall] },
      { role: 'user', parts: [{ functionResponse: { name, response: result } }] },
    ],
    config: { tools },
  });
}

// Auto function calling (SDK handles the loop)
const response2 = await ai.models.generateContent({
  model: 'gemini-2.5-flash',
  contents: 'Weather in Paris and London',
  config: {
    tools,
    toolConfig: { functionCallingConfig: { mode: 'AUTO' } },
  },
});
```

## Grounding with Google Search

```ts
const response = await ai.models.generateContent({
  model: 'gemini-2.5-flash',
  contents: 'What are the latest TypeScript release notes?',
  config: {
    tools: [{ googleSearch: {} }],
  },
});

// Access grounding metadata
const groundingMetadata = response.candidates?.[0]?.groundingMetadata;
console.log(groundingMetadata?.searchEntryPoint?.renderedContent); // search widget
console.log(groundingMetadata?.groundingChunks);  // source URLs
```

## Embeddings

```ts
const result = await ai.models.embedContent({
  model: 'text-embedding-004',
  contents: 'What is machine learning?',
  config: {
    taskType: 'RETRIEVAL_DOCUMENT',  // or RETRIEVAL_QUERY, SEMANTIC_SIMILARITY, CLASSIFICATION
    dimensions: 768,  // optional: reduce dimensions
  },
});

const embedding = result.embedding.values;  // float[]

// Batch embeddings
const batchResult = await ai.models.batchEmbedContents({
  model: 'text-embedding-004',
  requests: texts.map(text => ({
    content: { parts: [{ text }] },
    taskType: 'RETRIEVAL_DOCUMENT',
  })),
});
```

## Safety Settings

```ts
import { HarmCategory, HarmBlockThreshold } from '@google/genai';

const response = await ai.models.generateContent({
  model: 'gemini-2.5-flash',
  contents: prompt,
  config: {
    safetySettings: [
      { category: HarmCategory.HARM_CATEGORY_HARASSMENT, threshold: HarmBlockThreshold.BLOCK_ONLY_HIGH },
      { category: HarmCategory.HARM_CATEGORY_HATE_SPEECH, threshold: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE },
      { category: HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT, threshold: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE },
      { category: HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, threshold: HarmBlockThreshold.BLOCK_NONE },
    ],
  },
});

// Check if blocked
if (response.promptFeedback?.blockReason) {
  console.log('Blocked:', response.promptFeedback.blockReason);
}
```

## Thinking (Extended Reasoning)

```ts
// Enable thinking for complex tasks
const response = await ai.models.generateContent({
  model: 'gemini-2.5-flash',
  contents: 'Solve: What is the optimal algorithm for finding the longest common subsequence?',
  config: {
    thinkingConfig: {
      thinkingBudget: 1024,  // token budget for reasoning
      // thinkingBudget: 0    → disable thinking
      // thinkingBudget: -1   → dynamic (auto-adjust)
    },
  },
});

// Access thought process
for (const part of response.candidates?.[0]?.content?.parts ?? []) {
  if (part.thought) {
    console.log('Thinking:', part.text);  // reasoning steps
  } else {
    console.log('Answer:', part.text);    // final answer
  }
}
```

## Context Caching

```ts
// Cache large context (e.g., codebase, long docs) to reduce cost
const cache = await ai.caches.create({
  model: 'gemini-2.5-flash',
  config: {
    displayName: 'project-codebase',
    contents: [
      { role: 'user', parts: [{ text: largeCodebaseContent }] },
    ],
    systemInstruction: 'You are a code reviewer for this project.',
    ttl: '3600s',  // 1 hour TTL
  },
});

// Use cached context (cheaper — no re-processing)
const response = await ai.models.generateContent({
  model: 'gemini-2.5-flash',
  contents: 'Find potential bugs in the authentication module.',
  config: {
    cachedContent: cache.name,
  },
});

// List/delete caches
const caches = await ai.caches.list();
await ai.caches.delete({ name: cache.name });
```

## Document Understanding

```ts
// Process PDF documents (up to 1000 pages)
const pdfBuffer = fs.readFileSync('report.pdf');
const base64Pdf = pdfBuffer.toString('base64');

const response = await ai.models.generateContent({
  model: 'gemini-2.5-flash',
  contents: [
    { inlineData: { data: base64Pdf, mimeType: 'application/pdf' } },
    { text: 'Summarize the key findings in this report.' },
  ],
});
```

## Models Reference

| Model | API Name | Context | Best For |
|:------|:---------|:--------|:---------|
| Gemini 3 Flash | `gemini-3-flash-preview` | 1M | Latest, thinking, multimodal |
| Gemini 2.5 Pro | `gemini-2.5-pro-preview-06-05` | 1M | Most capable, complex reasoning |
| Gemini 2.5 Flash | `gemini-2.5-flash` | 1M | Best balance speed/quality |
| Gemini 2.5 Flash Image | `gemini-2.5-flash-preview-native-audio-dialog` | 1M | Native image generation |
| Gemini 2.0 Flash | `gemini-2.0-flash` | 1M | Fast, multimodal, agents |
| Text Embedding | `text-embedding-004` | 2K | Embeddings, search, RAG |

## Gotchas

⚠️ **`@google/genai`**: New SDK. Old `@google/generative-ai` still works but deprecated.

⚠️ **`response.text`**: Convenience getter. For function calls, check `response.candidates[0].content.parts`.

⚠️ **Structured output**: Must set `responseMimeType: 'application/json'` AND provide `responseSchema`.

⚠️ **1M context**: Gemini supports 1M tokens — far larger than most models. Great for large codebases.

⚠️ **Function calling**: Use `Type.OBJECT` from SDK, NOT raw JSON Schema `"type": "object"`.

⚠️ **Grounding**: `googleSearch` tool returns source URLs in `groundingMetadata`.

⚠️ **Safety filters**: Can block content unexpectedly. Set appropriate thresholds per use case.

⚠️ **Embeddings `taskType`**: Use `RETRIEVAL_QUERY` for search queries, `RETRIEVAL_DOCUMENT` for documents.

⚠️ **Thinking**: Use `thinkingBudget` to control reasoning depth. Set to `-1` for auto, `0` to disable.

⚠️ **Context caching**: Great for repeated queries against same large context. Cache has TTL — plan accordingly.

⚠️ **`gemini-3-flash-preview`**: Latest model with built-in thinking. Preview — may change.
