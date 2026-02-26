# TypeScript — Advanced Patterns


# Load only when explicitly referenced

## Table of Contents

- [Advanced Type System](#advanced-type-system)
- [Utility Type Patterns](#utility-type-patterns)
- [Generic Patterns](#generic-patterns)
- [Module Patterns](#module-patterns)

---

## Advanced Type System

### Conditional Types

```typescript
// Extract return type based on input
type ApiResponse<T> = T extends "user"
  ? { id: string; name: string }
  : T extends "post"
    ? { id: string; title: string }
    : never;

// Usage
const userResponse: ApiResponse<"user"> = { id: "1", name: "John" };
```

### Template Literal Types

```typescript
// Dynamic string types
type HttpMethod = "GET" | "POST" | "PUT" | "DELETE";
type Endpoint = "/users" | "/posts" | "/comments";
type Route = `${HttpMethod} ${Endpoint}`;

// Route becomes: 'GET /users' | 'POST /users' | ...

// Extract parts
type ExtractPath<T> = T extends `${HttpMethod} ${infer P}` ? P : never;
```

### Discriminated Unions

```typescript
type Result<T, E> = { success: true; data: T } | { success: false; error: E };

function handleResult<T, E>(result: Result<T, E>) {
  if (result.success) {
    // TypeScript knows: result.data exists
    console.log(result.data);
  } else {
    // TypeScript knows: result.error exists
    console.error(result.error);
  }
}
```

---

## Utility Type Patterns

### Deep Partial

```typescript
type DeepPartial<T> = T extends object
  ? { [P in keyof T]?: DeepPartial<T[P]> }
  : T;

// Makes all nested properties optional
interface Config {
  server: { host: string; port: number };
  db: { url: string };
}
type PartialConfig = DeepPartial<Config>;
```

### Builder Pattern Types

```typescript
type Builder<T, Built = {}> = {
  [K in keyof T]-?: (value: T[K]) => Builder<Omit<T, K>, Built & Pick<T, K>>;
} & { build: Built extends T ? () => T : never };

// Ensures all required fields set before build()
```

### Branded Types

```typescript
// Prevent type confusion
type Brand<T, B> = T & { __brand: B };

type UserId = Brand<string, "UserId">;
type PostId = Brand<string, "PostId">;

function getUser(id: UserId): User {
  /* ... */
}

const userId = "abc" as UserId;
const postId = "def" as PostId;

getUser(userId); // ✅ OK
getUser(postId); // ❌ Error: PostId not assignable to UserId
```

---

## Generic Patterns

### Constrained Generics

```typescript
// Only allow objects with 'id' property
function findById<T extends { id: string }>(
  items: T[],
  id: string,
): T | undefined {
  return items.find((item) => item.id === id);
}

// Mapped type with filter
type FilterByType<T, U> = {
  [K in keyof T as T[K] extends U ? K : never]: T[K];
};

interface Mixed {
  name: string;
  age: number;
  active: boolean;
}
type StringFields = FilterByType<Mixed, string>; // { name: string }
```

### Higher-Kinded Types Simulation

```typescript
// Kind simulation using interfaces
interface Functor<F> {
  map<A, B>(fa: F, f: (a: A) => B): F;
}

// Array as Functor
const arrayFunctor: Functor<unknown[]> = {
  map: (fa, f) => fa.map(f),
};
```

---

## Module Patterns

### Barrel Exports

```typescript
// index.ts - Barrel file
export * from "./user";
export * from "./post";
export type { Config } from "./config";
```

### Dependency Injection Types

```typescript
// Container types
interface Container {
  resolve<T>(token: Token<T>): T;
  register<T>(token: Token<T>, factory: () => T): void;
}

class Token<T> {
  constructor(public readonly name: string) {}
}

// Usage
const UserService = new Token<IUserService>("UserService");
container.register(UserService, () => new UserServiceImpl());
```

---
