# JavaScript — Advanced Patterns

> DOMYH Agent v4.3 — Tier 3 Reference

## Table of Contents

- [ES2025/ES2026 Deep Dive](#es20252026-deep-dive)
- [Node.js 22 Advanced Patterns](#nodejs-22-advanced-patterns)
- [Bun vs Deno Comparison](#bun-vs-deno-comparison)
- [Error Handling Patterns](#error-handling-patterns)
- [Testing Patterns](#testing-patterns)

---

## ES2025/ES2026 Deep Dive

### Temporal API (ES2026)

```javascript
// ✅ Temporal replaces the broken Date API
// Immutable, timezone-aware, correct

// Current instant (absolute time)
const now = Temporal.Now.instant();
console.log(now.toString()); // 2026-02-01T05:43:00.000Z

// Current date in specific timezone
const tokyo = Temporal.Now.zonedDateTimeISO("Asia/Tokyo");
const newYork = Temporal.Now.zonedDateTimeISO("America/New_York");

// Plain date (no time)
const birthday = Temporal.PlainDate.from("1990-05-15");

// Plain time (no date)
const meeting = Temporal.PlainTime.from("14:30");

// DateTime (no timezone)
const appointment = Temporal.PlainDateTime.from("2026-02-01T14:30:00");

// ZonedDateTime (full context)
const flight = Temporal.ZonedDateTime.from({
  year: 2026,
  month: 2,
  day: 1,
  hour: 14,
  minute: 30,
  timeZone: "America/Los_Angeles",
});

// ✅ Duration and arithmetic
const duration = Temporal.Duration.from({ hours: 2, minutes: 30 });
const later = appointment.add(duration);

// ✅ Comparison
const isAfter = flight.toInstant().epochMilliseconds > now.epochMilliseconds;

// ✅ Formatting
const formatted = birthday.toLocaleString("en-US", {
  weekday: "long",
  year: "numeric",
  month: "long",
  day: "numeric",
}); // "Tuesday, May 15, 1990"
```

### using Keyword (Resource Management)

```javascript
// ✅ Automatic resource cleanup (like Python's with, C#'s using)
class DatabaseConnection {
  constructor(url) {
    this.url = url;
    console.log("Connecting to", url);
  }

  query(sql) {
    return { rows: [] };
  }

  // Symbol.dispose for sync cleanup
  [Symbol.dispose]() {
    console.log("Closing connection");
  }
}

// ✅ Automatic cleanup when block exits
function processData() {
  using conn = new DatabaseConnection("postgres://...");
  const result = conn.query("SELECT * FROM users");
  // conn is automatically closed here
  return result;
}

// ✅ async using for async cleanup
class AsyncFile {
  static async open(path) {
    const file = new AsyncFile();
    await file._open(path);
    return file;
  }

  async read() {
    /* ... */
  }

  // Symbol.asyncDispose for async cleanup
  async [Symbol.asyncDispose]() {
    await this._close();
    console.log("File closed");
  }
}

async function readFile() {
  await using file = await AsyncFile.open("data.txt");
  const content = await file.read();
  // file is automatically closed
  return content;
}
```

### Iterator Helpers

```javascript
// ✅ Chain operations on iterators without creating intermediate arrays
function* generateNumbers(max) {
  for (let i = 1; i <= max; i++) {
    yield i;
  }
}

const result = generateNumbers(1000)
  .filter((n) => n % 2 === 0) // Only even
  .map((n) => n * 2) // Double
  .take(5) // First 5
  .toArray(); // [4, 8, 12, 16, 20]

// ✅ Works with any iterable
const filtered = new Set([1, 2, 3, 4, 5])
  .values()
  .filter((n) => n > 2)
  .toArray(); // [3, 4, 5]

// ✅ Available methods
// .map(), .filter(), .take(), .drop(), .flatMap()
// .forEach(), .some(), .every(), .find(), .reduce()
// .toArray()
```

---

## Node.js 22 Advanced Patterns

### Permission Model

```bash
# ✅ Run with limited permissions
node --permission --allow-fs-read=/app/data --allow-fs-write=/tmp \
     --allow-net=api.example.com \
     app.js

# Permission flags:
# --allow-fs-read=<path>   Allow reading specific paths
# --allow-fs-write=<path>  Allow writing specific paths
# --allow-net=<host>       Allow network access to specific hosts
# --allow-child-process    Allow spawning child processes
```

```javascript
// ✅ Check permissions at runtime
import { permission } from "node:process";

if (permission.has("fs.read", "/app/config")) {
  const config = await fs.readFile("/app/config/settings.json");
}
```

### Native Test Runner

```javascript
// ✅ Built-in test runner (no Jest needed for simple cases)
import { test, describe, beforeEach, mock } from "node:test";
import assert from "node:assert";

describe("UserService", () => {
  let service;

  beforeEach(() => {
    service = new UserService();
  });

  test("creates user successfully", async () => {
    const user = await service.create({ email: "test@example.com" });
    assert.strictEqual(user.email, "test@example.com");
  });

  test("throws on invalid email", async () => {
    await assert.rejects(() => service.create({ email: "invalid" }), {
      message: "Invalid email format",
    });
  });

  test("with mocked dependency", async () => {
    const mockDb = mock.fn(() => ({ id: 1, email: "test@example.com" }));
    service.db = { insert: mockDb };

    await service.create({ email: "test@example.com" });

    assert.strictEqual(mockDb.mock.callCount(), 1);
  });
});

// Run: node --test
```

### Worker Threads for CPU-bound Tasks

```javascript
import {
  Worker,
  isMainThread,
  parentPort,
  workerData,
} from "node:worker_threads";

if (isMainThread) {
  // Main thread: dispatch work to workers
  async function processInParallel(data) {
    const chunks = splitIntoChunks(data, 4);
    const workers = chunks.map((chunk) => {
      return new Promise((resolve, reject) => {
        const worker = new Worker(import.meta.filename, {
          workerData: chunk,
        });
        worker.on("message", resolve);
        worker.on("error", reject);
      });
    });

    const results = await Promise.all(workers);
    return results.flat();
  }
} else {
  // Worker thread: process chunk
  const result = processChunk(workerData);
  parentPort.postMessage(result);
}
```

---

## Bun vs Deno Comparison

### Bun Patterns

```javascript
// ✅ Bun: Built-in SQLite
import { Database } from "bun:sqlite";

const db = new Database("mydb.sqlite");
db.run("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)");
db.run("INSERT INTO users (name) VALUES (?)", ["Alice"]);
const users = db.query("SELECT * FROM users").all();

// ✅ Bun: Native Fetch server
Bun.serve({
  port: 3000,

  async fetch(req) {
    const url = new URL(req.url);

    if (url.pathname === "/api/users" && req.method === "GET") {
      return Response.json(await getUsers());
    }

    return new Response("Not Found", { status: 404 });
  },

  // WebSocket support built-in
  websocket: {
    open(ws) {
      console.log("Connected");
    },
    message(ws, message) {
      ws.send(`Echo: ${message}`);
    },
    close(ws) {
      console.log("Disconnected");
    },
  },
});

// ✅ Bun: File operations
const file = Bun.file("data.json");
const content = await file.json();
await Bun.write("output.txt", "Hello World");
```

### Deno Patterns

```typescript
// ✅ Deno: Permission-based security
const file = await Deno.readTextFile("./config.json");
// Requires: deno run --allow-read=./config.json script.ts

// ✅ Deno: Built-in TypeScript
interface User {
  id: number;
  name: string;
}

const users: User[] = [];

// ✅ Deno: URL imports (no package.json)
import { serve } from "https://deno.land/std@0.220.0/http/server.ts";

serve((req) => new Response("Hello"));

// ✅ Deno: Top-level await
const data = await Deno.readTextFile("data.json");
console.log(JSON.parse(data));

// ✅ Deno: Permissions API
const status = await Deno.permissions.query({ name: "read", path: "/etc" });
if (status.state === "granted") {
  // Safe to read
}
```

---

## Error Handling Patterns

### Result Pattern (Avoiding Exceptions)

```javascript
// ✅ Result type for explicit error handling
class Result {
  constructor(value, error) {
    this.value = value;
    this.error = error;
    this.isSuccess = !error;
  }

  static ok(value) {
    return new Result(value, null);
  }

  static err(error) {
    return new Result(null, error);
  }

  map(fn) {
    if (this.isSuccess) {
      return Result.ok(fn(this.value));
    }
    return this;
  }

  flatMap(fn) {
    if (this.isSuccess) {
      return fn(this.value);
    }
    return this;
  }

  unwrap() {
    if (this.isSuccess) return this.value;
    throw this.error;
  }

  unwrapOr(defaultValue) {
    return this.isSuccess ? this.value : defaultValue;
  }
}

// ✅ Usage
async function fetchUser(id) {
  try {
    const response = await fetch(`/api/users/${id}`);
    if (!response.ok) {
      return Result.err(new Error(`HTTP ${response.status}`));
    }
    return Result.ok(await response.json());
  } catch (error) {
    return Result.err(error);
  }
}

const result = await fetchUser(1);
if (result.isSuccess) {
  console.log(result.value.name);
} else {
  console.error("Failed:", result.error.message);
}
```

### Comprehensive Error Types

```javascript
// ✅ Custom error hierarchy
class AppError extends Error {
  constructor(message, code, details = {}) {
    super(message);
    this.name = "AppError";
    this.code = code;
    this.details = details;
    this.timestamp = new Date().toISOString();
  }

  toJSON() {
    return {
      name: this.name,
      message: this.message,
      code: this.code,
      details: this.details,
      timestamp: this.timestamp,
    };
  }
}

class ValidationError extends AppError {
  constructor(message, fields) {
    super(message, "VALIDATION_ERROR", { fields });
    this.name = "ValidationError";
  }
}

class NotFoundError extends AppError {
  constructor(resource, id) {
    super(`${resource} not found: ${id}`, "NOT_FOUND", { resource, id });
    this.name = "NotFoundError";
  }
}

// ✅ Error handler middleware
function errorHandler(err, req, res, next) {
  if (err instanceof ValidationError) {
    return res.status(400).json(err.toJSON());
  }
  if (err instanceof NotFoundError) {
    return res.status(404).json(err.toJSON());
  }

  // Unknown error - log and return generic
  console.error("Unhandled error:", err);
  res.status(500).json({
    name: "InternalError",
    message: "An unexpected error occurred",
    code: "INTERNAL_ERROR",
  });
}
```

---

## Testing Patterns

### Vitest (Recommended)

```javascript
// ✅ Vitest: Fast, Vite-native testing
import { describe, it, expect, vi, beforeEach } from "vitest";

describe("UserService", () => {
  let service;
  let mockDb;

  beforeEach(() => {
    mockDb = {
      query: vi.fn(),
      insert: vi.fn(),
    };
    service = new UserService(mockDb);
  });

  it("returns user by id", async () => {
    mockDb.query.mockResolvedValue([{ id: 1, name: "Alice" }]);

    const user = await service.getById(1);

    expect(user).toEqual({ id: 1, name: "Alice" });
    expect(mockDb.query).toHaveBeenCalledWith(
      expect.stringContaining("SELECT"),
      [1],
    );
  });

  it("throws when user not found", async () => {
    mockDb.query.mockResolvedValue([]);

    await expect(service.getById(999)).rejects.toThrow("User not found");
  });
});
```

### End-to-End with Playwright

```javascript
import { test, expect } from "@playwright/test";

test.describe("Login Flow", () => {
  test("successful login redirects to dashboard", async ({ page }) => {
    await page.goto("/login");

    await page.fill('[name="email"]', "test@example.com");
    await page.fill('[name="password"]', "password123");
    await page.click('button[type="submit"]');

    await expect(page).toHaveURL("/dashboard");
    await expect(page.locator("h1")).toContainText("Welcome");
  });

  test("invalid credentials shows error", async ({ page }) => {
    await page.goto("/login");

    await page.fill('[name="email"]', "wrong@example.com");
    await page.fill('[name="password"]', "wrongpass");
    await page.click('button[type="submit"]');

    await expect(page.locator(".error-message")).toBeVisible();
    await expect(page.locator(".error-message")).toContainText(
      "Invalid credentials",
    );
  });
});
```

---

_DOMYH Agent v4.3 — JavaScript Advanced Patterns — 2025-2026_
