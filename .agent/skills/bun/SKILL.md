---
name: bun
detect: ["bun.lockb", "bunfig.toml"]
version: "6.0.0"
category: runtime
tier: 2
---

# Bun Patterns — DOMYH Awesome Code v5.5

> **Version**: Bun 1.1+ (2025-2026)
> **Framework**: Elysia, Hono
> **Philosophy**: Speed-first, all-in-one

---

## 🎯 When to Use This Skill

Use for: Fast APIs, bundling, scripts, Node.js replacement.
**NOT for**: Edge deploys (→ deno), strict security (→ deno).

---

## 📦 Why Bun?

| Feature     | Bun         | Node.js  | Deno     |
| ----------- | ----------- | -------- | -------- |
| Speed       | Fastest 🏆  | Baseline | Fast     |
| npm compat  | Full 🏆     | N/A      | Full     |
| Bundler     | Built-in 🏆 | webpack  | None     |
| Test runner | Built-in 🏆 | Jest     | Built-in |
| TS support  | Native      | Via tsc  | Native   |

---

## 🔧 Project Setup

```bash
# Create project
bun init

# Add dependencies
bun add elysia
bun add -d @types/bun

# Run
bun run index.ts

# Build
bun build ./index.ts --outdir ./dist
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
// index.ts
import { Elysia, t } from "elysia";
import { cors } from "@elysiajs/cors";

const app = new Elysia()
  .use(cors())
  .state("version", "1.0.0")

  // GET with validation
  .get("/", () => "Hello Bun!")

  .get("/users", async () => {
    const users = await getUsers();
    return users;
  })

  .get(
    "/users/:id",
    async ({ params: { id }, error }) => {
      const user = await getUser(id);
      if (!user) return error(404, "User not found");
      return user;
    },
    {
      params: t.Object({
        id: t.String(),
      }),
    },
  )

  // POST with body validation
  .post(
    "/users",
    async ({ body }) => {
      const user = await createUser(body);
      return user;
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

### File Operations

```typescript
// ✅ Fast file reading
const file = Bun.file("./data.json");
const data = await file.json();

// ✅ Fast file writing
await Bun.write("./output.json", JSON.stringify(data, null, 2));

// ✅ Streaming large files
const bigFile = Bun.file("./large.csv");
const stream = bigFile.stream();

for await (const chunk of stream) {
  process(chunk);
}

// ✅ Glob patterns
const glob = new Bun.Glob("**/*.ts");
for await (const file of glob.scan(".")) {
  console.log(file);
}
```

### SQLite (Built-in)

```typescript
import { Database } from "bun:sqlite";

const db = new Database("app.db");

// ✅ Create table
db.run(`
  CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
  )
`);

// ✅ Prepared statements (fast!)
const insertUser = db.prepare(`
  INSERT INTO users (name, email) VALUES ($name, $email)
`);

const getUser = db.prepare(`
  SELECT * FROM users WHERE id = ?
`);

const listUsers = db.prepare(`
  SELECT * FROM users ORDER BY created_at DESC LIMIT ?
`);

// Usage
insertUser.run({ $name: "John", $email: "john@example.com" });
const user = getUser.get(1);
const users = listUsers.all(10);

// ✅ Transactions
db.transaction(() => {
  insertUser.run({ $name: "Alice", $email: "alice@example.com" });
  insertUser.run({ $name: "Bob", $email: "bob@example.com" });
})();
```

### Password Hashing (Built-in)

```typescript
// ✅ Hash password
const hash = await Bun.password.hash("mypassword", {
  algorithm: "argon2id",
  memoryCost: 65536,
  timeCost: 3,
});

// ✅ Verify password
const isValid = await Bun.password.verify("mypassword", hash);
```

---

## 📦 Bundling

```typescript
// build.ts
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

console.log("Build complete!");
for (const output of result.outputs) {
  console.log(`  ${output.path} (${output.size} bytes)`);
}
```

---

## 🧪 Testing

```typescript
// user.test.ts
import { describe, expect, test, beforeAll, afterAll } from "bun:test";
import { app } from "./index";

describe("User API", () => {
  beforeAll(() => {
    // Setup
  });

  afterAll(() => {
    // Cleanup
  });

  test("GET / returns hello", async () => {
    const res = await app.handle(new Request("http://localhost/"));
    expect(res.status).toBe(200);
    expect(await res.text()).toBe("Hello Bun!");
  });

  test("POST /users creates user", async () => {
    const res = await app.handle(
      new Request("http://localhost/users", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: "Test User",
          email: "test@example.com",
        }),
      }),
    );

    expect(res.status).toBe(200);
    const user = await res.json();
    expect(user.name).toBe("Test User");
  });

  test("POST /users validates email", async () => {
    const res = await app.handle(
      new Request("http://localhost/users", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: "Test",
          email: "invalid",
        }),
      }),
    );

    expect(res.status).toBe(422);
  });
});
```

```bash
# Run tests
bun test

# Watch mode
bun test --watch

# Coverage
bun test --coverage
```

---

## ✅ Production Checklist

### Performance

- [ ] Using bun:sqlite for DB
- [ ] Prepared statements cached
- [ ] Bun.file for I/O
- [ ] Production build minified

### Quality

- [ ] TypeScript strict mode
- [ ] Tests passing
- [ ] No type errors

### Deploy

- [ ] Docker with oven/bun image
- [ ] bun.lockb committed
- [ ] Health check endpoint

---

_DOMYH Awesome Code v6.0.0 • Bun 1.1+_
