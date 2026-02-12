---
name: deno
detect: ["deno.json", "deno.jsonc", "deno.lock", "mod.ts", "deps.ts"]
version: "6.2.1"
category: runtime
tier: 2
---

# Deno Patterns — DOMYH Awesome Code

> **Version**: Deno 2.6.8 (2025-2026)
> **Framework**: Fresh, Hono
> **Philosophy**: Secure by default, TypeScript-first

---

## 🎯 When to Use This Skill

Use for: APIs, CLI tools, edge functions, TypeScript projects.
**NOT for**: Heavy npm ecosystem (→ nodejs), speed-critical (→ bun).

---

## 📦 What's New in Deno 2.x (2025-2026)

| Version | Key Features                                        |
| ------- | --------------------------------------------------- |
| **2.2** | node:sqlite, TypeScript 5.7, lint plugins           |
| **2.4** | deno bundle return, bytes/text imports              |
| **2.5** | WebSocket headers, setTimeout unstable              |
| **2.6** | **dx** command, **deno audit**, tsgo fast typecheck |

---

## 🔧 Project Setup

### deno.json

```json
{
  "tasks": {
    "dev": "deno run --watch --allow-net --allow-read main.ts",
    "start": "deno run --allow-net --allow-read main.ts",
    "test": "deno test --allow-all",
    "check": "deno check *.ts",
    "fmt": "deno fmt",
    "lint": "deno lint",
    "audit": "deno audit"
  },
  "imports": {
    "@std/": "jsr:@std/",
    "hono": "jsr:@hono/hono@^4",
    "@oak/oak": "jsr:@oak/oak@^17"
  },
  "compilerOptions": {
    "strict": true
  }
}
```

### Project Structure

```
project/
├── deno.json         # Config & imports
├── deno.lock         # Lock file
├── main.ts           # Entry point
├── routes/
│   ├── api/
│   │   └── users.ts
│   └── index.ts
├── lib/
│   └── db.ts
└── tests/
    └── api_test.ts
```

---

## 🔄 Core Patterns

### HTTP Server with Hono

```typescript
import { Hono } from "hono";
import { cors } from "hono/cors";
import { logger } from "hono/logger";

const app = new Hono();

app.use("*", logger());
app.use("/api/*", cors());

app.get("/", (c) => c.text("Hello Deno 2.6!"));

app.get("/api/users", async (c) => {
  const users = await listUsers();
  return c.json(users);
});

app.get("/api/users/:id", async (c) => {
  const id = c.req.param("id");
  const user = await getUser(id);
  if (!user) return c.json({ error: "Not found" }, 404);
  return c.json(user);
});

Deno.serve({ port: 8000 }, app.fetch);
```

### Database with Deno KV

```typescript
const kv = await Deno.openKv();

interface User {
  id: string;
  name: string;
  email: string;
  createdAt: Date;
}

export async function createUser(
  data: Omit<User, "id" | "createdAt">,
): Promise<User> {
  const id = crypto.randomUUID();
  const user: User = { id, ...data, createdAt: new Date() };

  await kv.set(["users", id], user);
  await kv.set(["users_by_email", data.email], id);

  return user;
}

export async function getUser(id: string): Promise<User | null> {
  const result = await kv.get<User>(["users", id]);
  return result.value;
}

export async function listUsers(): Promise<User[]> {
  const users: User[] = [];
  const iter = kv.list<User>({ prefix: ["users"] });

  for await (const entry of iter) {
    if (entry.key.length === 2) users.push(entry.value);
  }
  return users;
}
```

### 🆕 node:sqlite (Deno 2.2+)

```typescript
import { DatabaseSync } from "node:sqlite";

const db = new DatabaseSync("app.db");

db.exec(`
  CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE
  )
`);

const stmt = db.prepare("INSERT INTO users (name, email) VALUES (?, ?)");
stmt.run("Alice", "alice@example.com");

const users = db.prepare("SELECT * FROM users").all();
```

---

## 🆕 CLI Commands (2.6+)

### dx — Package Binary Runner

```bash
# Run npm package binaries directly
dx prettier --write .
dx eslint src/
dx tsx script.ts

# Same as npx but for Deno
```

### deno audit — Security Scan

```bash
# Scan dependencies for vulnerabilities
deno audit

# Output:
# ✓ No vulnerabilities found
# - or -
# ⚠ Found 2 vulnerabilities in dependencies
```

### Granular Permissions

```bash
# Specific host only
deno run --allow-net=api.example.com main.ts

# Specific path only
deno run --allow-read=./config,./data main.ts

# Fine-grained env access
deno run --allow-env=DATABASE_URL,API_KEY main.ts
```

---

## 🔒 Permissions Best Practices

```typescript
// ✅ Check permissions at runtime
const netPermission = await Deno.permissions.query({ name: "net" });
if (netPermission.state !== "granted") {
  console.error("Network permission required");
  Deno.exit(1);
}

// ✅ Request permission dynamically
const status = await Deno.permissions.request({
  name: "read",
  path: "./config",
});

if (status.state === "granted") {
  const config = await Deno.readTextFile("./config/app.json");
}
```

---

## 🌐 Fresh Framework (Full-stack)

```typescript
// routes/index.tsx
import { Handlers, PageProps } from "$fresh/server.ts";
import Counter from "../islands/Counter.tsx";

interface Data {
  message: string;
}

export const handler: Handlers<Data> = {
  GET(req, ctx) {
    return ctx.render({ message: "Welcome to Fresh!" });
  },
};

export default function Home({ data }: PageProps<Data>) {
  return (
    <div class="p-4 mx-auto max-w-screen-md">
      <h1 class="text-4xl font-bold">{data.message}</h1>
      <Counter start={0} />
    </div>
  );
}
```

---

## 🧪 Testing

```typescript
import { assertEquals, assertExists } from "@std/assert";
import { createUser, getUser } from "../lib/db.ts";

Deno.test("User CRUD operations", async (t) => {
  let userId: string;

  await t.step("create user", async () => {
    const user = await createUser({
      name: "Test User",
      email: "test@example.com",
    });
    assertExists(user.id);
    assertEquals(user.name, "Test User");
    userId = user.id;
  });

  await t.step("get user", async () => {
    const user = await getUser(userId);
    assertExists(user);
    assertEquals(user.email, "test@example.com");
  });
});
```

```bash
deno test --allow-all           # Run tests
deno test --allow-all --coverage=coverage  # With coverage
deno coverage coverage          # View coverage
```

---

## ✅ Production Checklist

### Security

- [ ] Minimal permissions specified
- [ ] No --allow-all in production
- [ ] Environment variables for secrets
- [ ] CORS configured properly
- [ ] `deno audit` passing

### Quality

- [ ] deno lint passing
- [ ] deno fmt consistent
- [ ] deno check for type errors
- [ ] Tests coverage > 80%

### Deploy

- [ ] deno.lock committed
- [ ] Deno Deploy or Docker
- [ ] Health check endpoint

---

## 🔌 HSA Integration

Data powered by HSA BM25 search engine:

| Domain      | Query Examples                |
| ----------- | ----------------------------- |
| Runtime     | "Deno KV database operations" |
| Permissions | "allow-net granular security" |
| Framework   | "Fresh island component SSR"  |
| CLI         | "dx deno audit security scan" |

---

_DOMYH Awesome Code • Deno 2.6.8 • 2026_
