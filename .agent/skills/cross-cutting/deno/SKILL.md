---
name: deno
detect: ["deno.json", "deno.jsonc", "deno.lock", "mod.ts", "deps.ts"]
version: "6.1.2"
category: runtime
tier: 2
---

# Deno Patterns — DOMYH Awesome Code v6.1.2

> **Version**: Deno 2.0+ (2025-2026)
> **Framework**: Fresh, Hono
> **Philosophy**: Secure by default, TypeScript-first

---

## 🎯 When to Use This Skill

Use for: APIs, CLI tools, edge functions, TypeScript projects.
**NOT for**: Heavy npm ecosystem dependency (→ nodejs), speed-critical (→ bun).

---

## 📦 Why Deno 2?

| Feature     | Deno 2         | Node.js | Bun      |
| ----------- | -------------- | ------- | -------- |
| TS support  | Native 🏆      | Via tsc | Native   |
| Permissions | Built-in 🏆    | None    | None     |
| npm compat  | Full           | N/A     | Full     |
| Deploy      | Deno Deploy 🏆 | Vercel  | None     |
| Testing     | Built-in 🏆    | Jest    | Built-in |

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
    "lint": "deno lint"
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
// main.ts
import { Hono } from "hono";
import { cors } from "hono/cors";
import { logger } from "hono/logger";

const app = new Hono();

// Middleware
app.use("*", logger());
app.use("/api/*", cors());

// Routes
app.get("/", (c) => c.text("Hello Deno!"));

app.get("/api/users", async (c) => {
  const users = await getUsers();
  return c.json(users);
});

app.get("/api/users/:id", async (c) => {
  const id = c.req.param("id");
  const user = await getUser(id);
  if (!user) {
    return c.json({ error: "Not found" }, 404);
  }
  return c.json(user);
});

app.post("/api/users", async (c) => {
  const body = await c.req.json();
  const user = await createUser(body);
  return c.json(user, 201);
});

// Start server
Deno.serve({ port: 8000 }, app.fetch);
```

### Database with Deno KV

```typescript
// lib/db.ts
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
  const user: User = {
    id,
    ...data,
    createdAt: new Date(),
  };

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
    if (entry.key.length === 2) {
      users.push(entry.value);
    }
  }

  return users;
}

export async function deleteUser(id: string): Promise<boolean> {
  const user = await getUser(id);
  if (!user) return false;

  await kv
    .atomic()
    .delete(["users", id])
    .delete(["users_by_email", user.email])
    .commit();

  return true;
}
```

### Permissions Best Practices

```typescript
// ✅ Request only needed permissions
// deno run --allow-net=api.example.com --allow-read=./config main.ts

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

```typescript
// islands/Counter.tsx
import { useSignal } from "@preact/signals";

interface Props {
  start: number;
}

export default function Counter({ start }: Props) {
  const count = useSignal(start);

  return (
    <div class="flex gap-4 items-center">
      <button onClick={() => count.value--}>-</button>
      <span>{count}</span>
      <button onClick={() => count.value++}>+</button>
    </div>
  );
}
```

---

## 🧪 Testing

```typescript
// tests/api_test.ts
import { assertEquals, assertExists } from "@std/assert";
import { createUser, getUser, deleteUser } from "../lib/db.ts";

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

  await t.step("delete user", async () => {
    const deleted = await deleteUser(userId);
    assertEquals(deleted, true);

    const user = await getUser(userId);
    assertEquals(user, null);
  });
});

// HTTP tests
Deno.test("API endpoints", async () => {
  const res = await fetch("http://localhost:8000/api/users");
  assertEquals(res.status, 200);

  const users = await res.json();
  assertEquals(Array.isArray(users), true);
});
```

```bash
# Run tests
deno test --allow-all

# With coverage
deno test --allow-all --coverage=coverage
deno coverage coverage
```

---

## ✅ Production Checklist

### Security

- [ ] Minimal permissions specified
- [ ] No --allow-all in production
- [ ] Environment variables for secrets
- [ ] CORS configured properly

### Quality

- [ ] deno lint passing
- [ ] deno fmt consistent
- [ ] deno check for type errors
- [ ] Tests coverage > 80%

### Deploy

- [ ] deno.lock committed
- [ ] Deno Deploy or Docker
- [ ] Health check endpoint
- [ ] Structured logging

---

_DOMYH Awesome Code v6.1.2 • Deno 2.0+_
