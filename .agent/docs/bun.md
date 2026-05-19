---
library: bun
version: latest
latest: true
category: backend
official_docs: https://bun.sh/docs
last_updated: 2026-03-20
last_checked: 2026-03-21
source: bun.sh + curated
---

# Bun v1.3

> Bun — All-in-one JavaScript runtime. Fast bundler, test runner, package manager.
> Drop-in Node.js replacement. Built on JavaScriptCore. Acquired by Anthropic (2025).
> 3-4x faster HTTP, 10x faster cold starts, native TypeScript.
> Docs: https://bun.sh

## Installation

```bash
# macOS/Linux
curl -fsSL https://bun.sh/install | bash

# Windows
powershell -c "irm bun.sh/install.ps1 | iex"

# npm
npm install -g bun
```

## Runtime

```bash
bun run index.ts                   # run TypeScript directly (no config needed)
bun run index.jsx                  # JSX/TSX supported out of the box
bun --watch index.ts               # auto-restart on changes
bun --hot index.ts                 # hot reload (preserve state)
```

```ts
// Built-in APIs (Web Standard + Node.js compat)
const server = Bun.serve({
    port: 3000,
    fetch(req) {
        const url = new URL(req.url);
        if (url.pathname === '/') return new Response('Hello Bun!');
        if (url.pathname === '/json') return Response.json({ hello: 'world' });
        return new Response('Not Found', { status: 404 });
    },
});

console.log(`Listening on ${server.url}`);
```

## Package Manager

```bash
bun install                        # install all deps (10-100x faster than npm)
bun add express zod                # add dependency
bun add -d vitest                  # add dev dependency
bun remove lodash                  # remove
bun update                         # update all
bun pm ls                          # list installed packages
```

## Bundler

```ts
// bun build
await Bun.build({
    entrypoints: ['./src/index.ts'],
    outdir: './dist',
    target: 'bun',                   // or 'browser', 'node'
    minify: true,
    sourcemap: 'external',
});
```

```bash
bun build ./src/index.ts --outdir ./dist --minify
```

## Test Runner

```ts
// math.test.ts
import { describe, it, expect, mock, beforeEach } from 'bun:test';

describe('math', () => {
    it('adds numbers', () => {
        expect(1 + 2).toBe(3);
    });

    it('async', async () => {
        const result = await fetchData();
        expect(result).toEqual({ id: 1 });
    });
});

// Mocking
const mockFn = mock(() => 42);
mockFn();
expect(mockFn).toHaveBeenCalled();
```

```bash
bun test                           # run all tests
bun test --watch                   # watch mode
bun test --coverage                # with coverage
```

## File I/O (Bun APIs)

```ts
// Read/Write (fastest in any JS runtime)
const file = Bun.file('data.json');
const text = await file.text();
const json = await file.json();
const bytes = await file.bytes();

await Bun.write('output.txt', 'Hello');
await Bun.write('data.json', JSON.stringify({ key: 'value' }));

// Streaming
const writer = Bun.file('large.txt').writer();
writer.write('chunk 1\n');
writer.write('chunk 2\n');
writer.end();
```

## SQLite (Built-in)

```ts
import { Database } from 'bun:sqlite';

const db = new Database('mydb.sqlite');
db.run('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)');

const insert = db.prepare('INSERT INTO users (name, email) VALUES (?, ?)');
insert.run('Alice', 'alice@test.com');

const users = db.prepare('SELECT * FROM users WHERE name = ?').all('Alice');

const insertMany = db.transaction((users) => {
    for (const u of users) insert.run(u.name, u.email);
});
insertMany([{ name: 'Bob', email: 'bob@test.com' }]);
```

## Bun.SQL (v1.3 NEW — PostgreSQL/MySQL/SQLite)

```ts
// Native database clients — no npm packages needed
import { sql } from 'bun';

// PostgreSQL
const db = sql`postgres://user:pass@localhost/mydb`;
const users = await db`SELECT * FROM users WHERE age > ${18}`;

// MySQL
const mysql = sql`mysql://user:pass@localhost/mydb`;

// Tagged template — SQL injection safe
const name = 'Alice';
const result = await db`SELECT * FROM users WHERE name = ${name}`;
```

## Zero-Config Frontend (v1.3 NEW)

```bash
# Run HTML files directly — auto handles HMR, React Fast Refresh
bun index.html

# Compile to self-contained HTML
bun build --compile --target=browser ./src/index.ts
```

## Native REPL (v1.3 NEW)

```bash
bun repl                               # start native REPL (Zig-powered)
# Features: top-level await, ESM import & require, syntax highlighting,
#           persistent history, tab completion, multi-line input
```

## Gotchas

⚠️ **Node.js compat**: ~95% compatible. Some edge cases with native addons, `vm` module, `--require`.

⚠️ **Windows**: Full native support since v1.2+. No performance compromises.

⚠️ **`Bun.serve`**: Uses Web `Request`/`Response` API, NOT Express-style `req`/`res`.

⚠️ **Package manager**: Uses hardlinks. `node_modules` is shared across projects. Very fast but different structure.

⚠️ **TypeScript**: Transpiled, NOT type-checked. Use `tsc --noEmit` for type checking.

⚠️ **`bun:test`**: Jest-compatible API but some differences. `jest.fn()` → `mock()`.

⚠️ **`bun:sqlite`**: Built into runtime. No npm install needed. Fastest SQLite for JS.

⚠️ **`Bun.SQL`** (v1.3): Native PostgreSQL/MySQL/SQLite client. Tagged template = SQL injection safe.

⚠️ **Lockfile**: Uses `bun.lockb` (binary). Add to git. Not compatible with `package-lock.json`.

⚠️ **Anthropic**: Bun acquired by Anthropic (2025). Used in Claude Code. Production-ready.
