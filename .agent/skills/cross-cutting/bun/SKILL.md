---
name: bun
detect: ["bun.lockb", "bunfig.toml", "bun.lock"]
version: "6.4.5"
category: runtime
tier: 2
---

# Bun Patterns — DOMYH Awesome Code

> **Version**: Bun 1.3.7 (2025-2026)
> **Framework**: Elysia, Hono
> **Philosophy**: Speed-first, all-in-one

---

## 🎯 When to Use This Skill

Use for: Fast APIs, bundling, scripts, Node.js replacement.
**NOT for**: Edge deploys (→ deno), strict security (→ deno).

---

## 📦 What's New in Bun 1.3 (2026)

| Feature               | Description                |
| --------------------- | -------------------------- |
| **Bun.sql**           | Built-in PostgreSQL client |
| **Bun.S3**            | Native S3 object storage   |
| **HTML Imports**      | Zero-config frontend dev   |
| **Bun.Archive**       | Tarball create/extract     |
| **Bun.JSON5/JSONL**   | Extended JSON parsing      |
| **50% faster Buffer** | Performance boost          |

---

## 🔧 Project Setup

```bash
# Create project
bun init

# Add dependencies
bun add elysia
bun add -d @types/bun

# Run (with hot reload)
bun --watch run index.ts

# Build
bun build ./index.ts --outdir ./dist --minify
```

### package.json

```json
{
  "name": "my-bun-app",
  "version": "1.0.0",
  "scripts": {
    "dev": "bun --watch run index.ts",
    "start": "bun run index.ts",
    "build": "bun build ./index.ts --outdir ./dist --minify",
    "test": "bun test"
  },
  "dependencies": {
    "elysia": "^1.0"
  },
  "devDependencies": {
    "@types/bun": "latest"
  }
}
```

---

## 🔄 Core Patterns

### HTTP Server with Elysia

```typescript
import { Elysia, t } from "elysia";
import { cors } from "@elysiajs/cors";

const app = new Elysia()
  .use(cors())
  .state("version", "1.0.0")

  .get("/", () => "Hello Bun 1.3!")

  .get(
    "/users/:id",
    async ({ params: { id }, error }) => {
      const user = await getUser(id);
      if (!user) return error(404, "User not found");
      return user;
    },
    {
      params: t.Object({ id: t.String() }),
    },
  )

  .post(
    "/users",
    async ({ body }) => {
      return await createUser(body);
    },
    {
      body: t.Object({
        name: t.String({ minLength: 2 }),
        email: t.String({ format: "email" }),
      }),
    },
  )

  .listen(3000);

console.log(`🦊 Elysia running at ${app.server?.url}`);
```

### 🆕 Bun.sql (PostgreSQL)

```typescript
// ✅ Built-in PostgreSQL client (Bun 1.2+)
const db = Bun.sql`postgresql://user:pass@localhost/mydb`;

// Query with tagged template
const users = await db`SELECT * FROM users WHERE active = true`;

// Parameterized queries (safe from SQL injection)
const userId = 123;
const user = await db`SELECT * FROM users WHERE id = ${userId}`;

// Transactions
await db.transaction(async (tx) => {
  await tx`INSERT INTO users (name) VALUES ('Alice')`;
  await tx`INSERT INTO logs (action) VALUES ('user_created')`;
});
```

### 🆕 Bun.S3 (Object Storage)

```typescript
// ✅ Native S3 support (Bun 1.2+)
const bucket = Bun.s3("my-bucket");

// Read file
const file = bucket.file("data.json");
const data = await file.json();

// Write file
await bucket.write("output.json", JSON.stringify(data));

// Stream large files
const stream = bucket.file("large.csv").stream();
for await (const chunk of stream) {
  process(chunk);
}

// List files
const files = await bucket.list({ prefix: "uploads/" });
```

### 🆕 HTML Imports (Zero-Config Frontend)

```bash
# Run HTML directly - Bun handles JS/CSS/React transpilation
bun ./index.html

# With hot reload
bun --hot ./index.html
```

```html
<!-- index.html -->
<!DOCTYPE html>
<html>
  <head>
    <script type="module" src="./app.tsx"></script>
  </head>
  <body>
    <div id="root"></div>
  </body>
</html>
```

### SQLite (Built-in)

```typescript
import { Database } from "bun:sqlite";

const db = new Database("app.db");

// Create table
db.run(`
  CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
  )
`);

// Prepared statements (fast!)
const insertUser = db.prepare(`
  INSERT INTO users (name, email) VALUES ($name, $email)
`);

insertUser.run({ $name: "John", $email: "john@example.com" });

// Transactions
db.transaction(() => {
  insertUser.run({ $name: "Alice", $email: "alice@example.com" });
  insertUser.run({ $name: "Bob", $email: "bob@example.com" });
})();
```

### 🆕 Archive API

```typescript
// ✅ Create tarball (Bun 1.3.6+)
const archive = await Bun.Archive.create("dist.tar.gz", {
  files: ["./dist"],
  compression: "gzip",
});

// Extract tarball
await Bun.Archive.extract("dist.tar.gz", "./output");
```

### 🆕 Extended JSON

```typescript
// JSON5 (comments, trailing commas)
const config = Bun.JSON5.parse(`{
  // This is a comment
  "name": "app",
  "debug": true,
}`);

// JSONL (line-delimited)
const lines = Bun.JSONL.parse(await Bun.file("logs.jsonl").text());
```

---

## 📦 Bundling

```typescript
const result = await Bun.build({
  entrypoints: ["./src/index.ts"],
  outdir: "./dist",
  minify: true,
  sourcemap: "external",
  target: "browser", // or "bun", "node"
  splitting: true,
  define: {
    "process.env.NODE_ENV": JSON.stringify("production"),
  },
});

if (!result.success) {
  console.error("Build failed:", result.logs);
  process.exit(1);
}
```

---

## 🧪 Testing

```typescript
import { describe, expect, test, beforeAll } from "bun:test";

describe("User API", () => {
  test("GET / returns hello", async () => {
    const res = await app.handle(new Request("http://localhost/"));
    expect(res.status).toBe(200);
    expect(await res.text()).toBe("Hello Bun 1.3!");
  });

  test("POST /users creates user", async () => {
    const res = await app.handle(
      new Request("http://localhost/users", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: "Test", email: "test@example.com" }),
      }),
    );
    expect(res.status).toBe(200);
  });
});
```

```bash
bun test              # Run tests
bun test --watch      # Watch mode
bun test --coverage   # Coverage report
```

---

## 🔧 CLI Commands (1.3+)

```bash
# Interactive dependency update
bun update --interactive

# Explain dependency chain
bun why lodash

# Security scan
bun x socket scan
```

---

## ✅ Production Checklist

### Performance

- [ ] Using Bun.sql for PostgreSQL
- [ ] Prepared statements cached
- [ ] Bun.file for I/O
- [ ] Production build minified

### Quality

- [ ] TypeScript strict mode
- [ ] Tests passing (bun test)
- [ ] No type errors

### Deploy

- [ ] Docker with oven/bun:1.3 image
- [ ] bun.lock committed (text-based)
- [ ] Health check endpoint

---

## 🔌 HSA Integration

Data powered by HSA BM25 search engine:

| Domain  | Query Examples                       |
| ------- | ------------------------------------ |
| API     | "Bun.sql PostgreSQL tagged template" |
| Storage | "Bun.S3 upload stream"               |
| Build   | "Bun.build minify splitting target"  |
| Runtime | "Elysia HTTP server validation"      |

---

_DOMYH Awesome Code • Bun 1.3.7 • 2026_
