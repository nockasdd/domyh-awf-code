---
name: typescript
detect: ["tsconfig.json", "*.ts", "*.tsx", "*.mts", "*.cts"]
version: "4.3.0"
category: frontend
tier: 1
---

# TypeScript Patterns — DOMYH Agent v4.3

> **Version**: TypeScript 5.5/5.6 (2025-2026)
> **Philosophy**: Type-safe, inference-first, ESM-native

---

## 🎯 When to Use This Skill

Use for: Web apps, Node.js, type-safe JavaScript, React/Vue/Angular.
**NOT for**: Backend-heavy (→ go/rust), ML (→ python).

---

## 📦 Recommended Stack (2025-2026)

### Runtimes

| Runtime        | Use Case        |
| -------------- | --------------- |
| **Node.js 22** | Server, tooling |
| **Bun**        | Fast runtime 🏆 |
| **Deno 2**     | Secure runtime  |

### Build Tools

| Tool        | Use Case            |
| ----------- | ------------------- |
| **Vite**    | Frontend bundler 🏆 |
| **esbuild** | Fast bundling       |
| **tsup**    | Library bundling    |
| **tsx**     | TS execution        |

### Validation

| Library           | Use Case                |
| ----------------- | ----------------------- |
| **Zod**           | Schema validation 🏆    |
| **Valibot**       | Lightweight alternative |
| **Effect Schema** | Effect ecosystem        |

### IDE Support

| IDE          | Features                             |
| ------------ | ------------------------------------ |
| **VS Code**  | Built-in TS support, IntelliSense 🏆 |
| **WebStorm** | Advanced refactoring                 |

---

## 🆕 TypeScript 5.5/5.6 Features

### Inferred Type Predicates (5.5)

```typescript
// ✅ TypeScript 5.5 auto-infers predicates
const users = [null, { name: "John" }, undefined, { name: "Jane" }];

// TypeScript infers: (x): x is { name: string }
const validUsers = users.filter((x) => x !== null && x !== undefined);
// Type: { name: string }[]
```

### Regular Expression Syntax Checking (5.5)

```typescript
// ✅ Compile-time regex validation
const pattern = /(?<year>\d{4})-(?<month>\d{2})-(?<day>\d{2})/;

// ❌ Error at compile time
// const bad = /[/;  // Unterminated character class
```

### Disallowed Nullish/Truthy Checks (5.6)

```typescript
// ✅ 5.6 warns about always-true/false conditions
function process(value: string) {
  // ⚠️ Warning: always truthy (string is never null here)
  if (value !== null) {
    console.log(value);
  }
}
```

### Iterator Helpers (5.6)

```typescript
// ✅ New iterator methods
function* numbers() {
  yield 1;
  yield 2;
  yield 3;
  yield 4;
  yield 5;
}

// No intermediate arrays created
const doubled = numbers()
  .map((n) => n * 2)
  .filter((n) => n > 4)
  .take(2)
  .toArray();
// [6, 8]
```

---

## 🔧 Type Patterns

### Utility Types

```typescript
// ✅ Built-in utilities
interface User {
  id: number;
  name: string;
  email: string;
  createdAt: Date;
}

type CreateUser = Omit<User, "id" | "createdAt">;
type UpdateUser = Partial<Pick<User, "name" | "email">>;
type UserKeys = keyof User; // "id" | "name" | "email" | "createdAt"
```

### Discriminated Unions

```typescript
// ✅ Type-safe state handling
type AsyncState<T> =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; data: T }
  | { status: "error"; error: Error };

function renderState<T>(state: AsyncState<T>) {
  switch (state.status) {
    case "idle":
      return "Ready";
    case "loading":
      return "Loading...";
    case "success":
      return `Data: ${state.data}`; // data is available
    case "error":
      return `Error: ${state.error.message}`; // error is available
  }
}
```

### Branded Types

```typescript
// ✅ Prevent type confusion
declare const Brand: unique symbol;
type Brand<T, B> = T & { [Brand]: B };

type UserId = Brand<number, "UserId">;
type PostId = Brand<number, "PostId">;

function getUser(id: UserId): User { ... }
function getPost(id: PostId): Post { ... }

const userId = 1 as UserId;
const postId = 2 as PostId;

getUser(userId);  // ✅ OK
getUser(postId);  // ❌ Error: PostId not assignable to UserId
```

### Const Assertions

```typescript
// ✅ Literal types with as const
const ROLES = ["admin", "user", "guest"] as const;
type Role = (typeof ROLES)[number]; // "admin" | "user" | "guest"

const CONFIG = {
  api: "https://api.example.com",
  timeout: 5000,
} as const;
// Readonly with literal types
```

### Template Literal Types

```typescript
// ✅ Type-safe string patterns
type HttpMethod = "GET" | "POST" | "PUT" | "DELETE";
type ApiRoute = `/api/${string}`;
type Endpoint = `${HttpMethod} ${ApiRoute}`;

const endpoint: Endpoint = "GET /api/users"; // ✅
// const bad: Endpoint = "PATCH /api/users"; // ❌
```

---

## 🔄 Async Patterns

### Promise Utilities

```typescript
// ✅ Proper async handling
async function fetchWithTimeout<T>(url: string, timeout: number): Promise<T> {
  const controller = new AbortController();
  const id = setTimeout(() => controller.abort(), timeout);

  try {
    const response = await fetch(url, { signal: controller.signal });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return response.json();
  } finally {
    clearTimeout(id);
  }
}

// ✅ Parallel with error handling
async function fetchAll<T>(urls: string[]): Promise<PromiseSettledResult<T>[]> {
  return Promise.allSettled(
    urls.map((url) => fetch(url).then((r) => r.json())),
  );
}
```

### Result Pattern

```typescript
// ✅ Explicit error handling
type Result<T, E = Error> =
  | { success: true; data: T }
  | { success: false; error: E };

async function tryCatch<T>(fn: () => Promise<T>): Promise<Result<T>> {
  try {
    return { success: true, data: await fn() };
  } catch (error) {
    return { success: false, error: error as Error };
  }
}

// Usage
const result = await tryCatch(() => fetchUser(1));
if (result.success) {
  console.log(result.data);
} else {
  console.error(result.error);
}
```

---

## 🧪 Testing Types

```typescript
// ✅ Type testing with @ts-expect-error
type Assert<T extends true> = T;
type Equal<X, Y> =
  (<T>() => T extends X ? 1 : 2) extends <T>() => T extends Y ? 1 : 2
    ? true
    : false;

// Test that types work correctly
type TestUserKeys = Assert<
  Equal<keyof User, "id" | "name" | "email" | "createdAt">
>;

// @ts-expect-error - should fail
const invalidUser: User = { id: "string" };
```

---

## ✅ Best Practices Checklist

### Config

- [ ] `strict: true` enabled
- [ ] `noUncheckedIndexedAccess: true`
- [ ] `exactOptionalPropertyTypes: true`
- [ ] ESM with `"type": "module"`

### Code Quality

- [ ] No `any` types
- [ ] `unknown` over `any`
- [ ] Discriminated unions for state
- [ ] Explicit return types on exports

### Performance

- [ ] `skipLibCheck: true`
- [ ] Project references for monorepos
- [ ] Incremental builds enabled

---

_DOMYH Agent v4.3 • TypeScript 5.5/5.6_
