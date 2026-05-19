---
library: hono
version: 4.x
latest: true
category: backend
official_docs: https://hono.dev
last_updated: 2026-03-20
last_checked: 2026-03-21
source: hono.dev + curated
---

# Hono v4

> Hono — Ultrafast web framework for the Edge. Built on Web Standards.
> Runs on: Cloudflare Workers, Deno, Bun, Node.js, AWS Lambda, Fastly.
> Docs: https://hono.dev

## Installation

```bash
# Bun
bun create hono my-app

# Node.js
npm create hono@latest my-app

# Deno
deno init --lib hono
```

## Basic

```ts
import { Hono } from 'hono';

const app = new Hono();

app.get('/', (c) => c.text('Hello Hono!'));
app.get('/json', (c) => c.json({ message: 'Hello' }));
app.get('/html', (c) => c.html('<h1>Hello</h1>'));

// Dynamic route
app.get('/users/:id', (c) => {
    const id = c.req.param('id');
    return c.json({ id });
});

// Query params
app.get('/search', (c) => {
    const q = c.req.query('q');
    const page = c.req.query('page') ?? '1';
    return c.json({ q, page });
});

// POST with body
app.post('/users', async (c) => {
    const body = await c.req.json();
    return c.json(body, 201);
});

// Methods
app.put('/users/:id', handler);
app.delete('/users/:id', handler);
app.patch('/users/:id', handler);

export default app;  // works with Bun/Deno/CF Workers
```

## Middleware

```ts
import { cors } from 'hono/cors';
import { logger } from 'hono/logger';
import { prettyJSON } from 'hono/pretty-json';
import { bearerAuth } from 'hono/bearer-auth';
import { compress } from 'hono/compress';
import { etag } from 'hono/etag';
import { secureHeaders } from 'hono/secure-headers';

// Built-in middleware
app.use('*', logger());
app.use('*', cors({ origin: 'http://localhost:3000' }));
app.use('*', secureHeaders());
app.use('*', compress());
app.use('*', etag());
app.use('/api/*', prettyJSON());
app.use('/api/*', bearerAuth({ token: 'my-secret-token' }));

// Custom middleware
app.use('*', async (c, next) => {
    const start = Date.now();
    await next();
    const ms = Date.now() - start;
    c.header('X-Response-Time', `${ms}ms`);
});
```

## Routing

```ts
// Route groups
const api = new Hono();
api.get('/users', listUsers);
api.post('/users', createUser);
api.get('/users/:id', getUser);
app.route('/api/v1', api);

// Chaining
app.get('/').get('/about').get('/contact');

// Wildcard
app.get('/files/*', (c) => {
    const path = c.req.path;
    return c.text(`File: ${path}`);
});

// Regex
app.get('/post/:id{[0-9]+}', handler);
```

## Validation (with Zod)

```ts
import { zValidator } from '@hono/zod-validator';
import { z } from 'zod';

const createUserSchema = z.object({
    name: z.string().min(1),
    email: z.string().email(),
});

app.post('/users',
    zValidator('json', createUserSchema),
    async (c) => {
        const data = c.req.valid('json');  // typed!
        return c.json(data, 201);
    }
);

// Validate query params
app.get('/search',
    zValidator('query', z.object({ q: z.string(), page: z.coerce.number().default(1) })),
    (c) => {
        const { q, page } = c.req.valid('query');
        return c.json({ q, page });
    }
);
```

## RPC (Type-safe Client)

```ts
// Server: Export type
const routes = app
    .get('/users', (c) => c.json([{ id: 1, name: 'Alice' }]))
    .post('/users', zValidator('json', schema), async (c) => {
        const data = c.req.valid('json');
        return c.json(data, 201);
    });

export type AppType = typeof routes;

// Client: Fully typed
import { hc } from 'hono/client';
import type { AppType } from './server';

const client = hc<AppType>('http://localhost:8787');
const res = await client.users.$get();           // typed response
const users = await res.json();                   // { id: number; name: string }[]
```

## JSX (Built-in)

```tsx
import { Hono } from 'hono';

const app = new Hono();

const Layout = ({ children }: { children: any }) => (
    <html><body>{children}</body></html>
);

app.get('/', (c) => c.html(
    <Layout>
        <h1>Hello Hono!</h1>
    </Layout>
));
```

## Node.js Adapter

```ts
import { serve } from '@hono/node-server';
import app from './app';

serve({ fetch: app.fetch, port: 3000 });
console.log('Server running on port 3000');
```

## Gotchas

⚠️ **Web Standards**: Uses `Request`/`Response` API, NOT Node.js `req`/`res`. Works everywhere.

⚠️ **`c.req.json()`**: Returns Promise. Must `await`. Body can only be read once.

⚠️ **Route order**: First match wins. Put specific routes before wildcards.

⚠️ **Middleware**: Must call `await next()` to pass to next handler. Otherwise request stops.

⚠️ **RPC client**: End-to-end type safety like tRPC but simpler. Use `hc<AppType>()`.

⚠️ **Bun/Deno**: Just `export default app`. Node.js needs `@hono/node-server` adapter.

⚠️ **Zod validator**: Install `@hono/zod-validator` separately. Validates `json`, `query`, `param`, `header`.

⚠️ **Performance**: ~4x faster than Express on Bun. Near-native speed on Cloudflare Workers.
