---
library: design-patterns
version: classic
latest: true
category: architecture
official_docs: https://refactoring.guru/design-patterns
last_updated: 2026-03-21
last_checked: 2026-03-21
source: ai-enhanced from refactoring.guru + Gang of Four + web research
---

# Design Patterns Reference

> Design Patterns — Proven solutions to recurring software design problems.
> Source: Gang of Four (GoF) + Modern adaptations
> Docs: https://refactoring.guru/design-patterns

## Creational Patterns

### Singleton

```typescript
// Modern TypeScript singleton — module-scoped (preferred)
class Database {
  private static instance: Database;
  private constructor(private url: string) {}

  static getInstance(): Database {
    if (!Database.instance) {
      Database.instance = new Database(process.env.DB_URL!);
    }
    return Database.instance;
  }

  query(sql: string) { /* ... */ }
}

// ⚠️ Gotcha: singletons make testing hard. Prefer dependency injection.
```

```python
# Python: module-level singleton (Pythonic)
# db.py — importing this module always returns same instance
class _Database:
    def __init__(self):
        self.connection = create_connection()

db = _Database()  # created once on import
```

### Factory Method

```typescript
// Factory — create objects without specifying exact class
interface Logger {
  log(message: string): void;
}

class ConsoleLogger implements Logger {
  log(message: string) { console.log(message); }
}

class FileLogger implements Logger {
  log(message: string) { fs.appendFileSync('app.log', message + '\n'); }
}

function createLogger(type: 'console' | 'file'): Logger {
  switch (type) {
    case 'console': return new ConsoleLogger();
    case 'file':    return new FileLogger();
  }
}

// Usage
const logger = createLogger(process.env.LOG_TARGET as any);
```

### Builder

```typescript
// Builder — construct complex objects step by step
class QueryBuilder {
  private table = '';
  private conditions: string[] = [];
  private ordering = '';
  private limitVal?: number;

  from(table: string)  { this.table = table; return this; }
  where(cond: string)  { this.conditions.push(cond); return this; }
  orderBy(col: string) { this.ordering = col; return this; }
  limit(n: number)     { this.limitVal = n; return this; }

  build(): string {
    let sql = `SELECT * FROM ${this.table}`;
    if (this.conditions.length) sql += ` WHERE ${this.conditions.join(' AND ')}`;
    if (this.ordering) sql += ` ORDER BY ${this.ordering}`;
    if (this.limitVal) sql += ` LIMIT ${this.limitVal}`;
    return sql;
  }
}

// Usage (fluent API)
const query = new QueryBuilder()
  .from('users')
  .where('active = true')
  .where('age > 18')
  .orderBy('name')
  .limit(10)
  .build();
```

## Structural Patterns

### Adapter

```typescript
// Adapter — make incompatible interfaces work together
interface ModernPayment {
  processPayment(amount: number, currency: string): Promise<boolean>;
}

// Legacy system with different interface
class LegacyPaymentGateway {
  makePayment(amountCents: number): boolean {
    // old implementation
    return true;
  }
}

class PaymentAdapter implements ModernPayment {
  constructor(private legacy: LegacyPaymentGateway) {}

  async processPayment(amount: number, currency: string): Promise<boolean> {
    const cents = Math.round(amount * 100);
    return this.legacy.makePayment(cents);
  }
}
```

### Decorator

```typescript
// Decorator — add behavior dynamically without subclassing
interface HttpClient {
  fetch(url: string): Promise<Response>;
}

class BaseClient implements HttpClient {
  async fetch(url: string) { return fetch(url); }
}

// Add logging
class LoggingClient implements HttpClient {
  constructor(private inner: HttpClient) {}

  async fetch(url: string) {
    console.log(`→ GET ${url}`);
    const start = Date.now();
    const res = await this.inner.fetch(url);
    console.log(`← ${res.status} (${Date.now() - start}ms)`);
    return res;
  }
}

// Add retry
class RetryClient implements HttpClient {
  constructor(private inner: HttpClient, private retries = 3) {}

  async fetch(url: string) {
    for (let i = 0; i < this.retries; i++) {
      try { return await this.inner.fetch(url); }
      catch (e) { if (i === this.retries - 1) throw e; }
    }
    throw new Error('unreachable');
  }
}

// Compose decorators
const client = new RetryClient(new LoggingClient(new BaseClient()));
```

### Repository

```typescript
// Repository — abstract data access layer
interface Repository<T> {
  findById(id: string): Promise<T | null>;
  findAll(filter?: Partial<T>): Promise<T[]>;
  create(entity: Omit<T, 'id'>): Promise<T>;
  update(id: string, data: Partial<T>): Promise<T>;
  delete(id: string): Promise<void>;
}

class UserRepository implements Repository<User> {
  constructor(private db: Database) {}

  async findById(id: string) {
    return this.db.query('SELECT * FROM users WHERE id = $1', [id]);
  }

  async findAll(filter?: Partial<User>) {
    const where = Object.entries(filter ?? {})
      .map(([k, v], i) => `${k} = $${i + 1}`).join(' AND ');
    return this.db.query(`SELECT * FROM users ${where ? 'WHERE ' + where : ''}`);
  }

  // ... create, update, delete
}

// Usage — easily swap implementations (SQL, MongoDB, in-memory)
const repo: Repository<User> = new UserRepository(db);
// In tests: new InMemoryUserRepository()
```

## Behavioral Patterns

### Observer / Event Emitter

```typescript
// Observer — pub/sub for decoupled communication
type EventHandler<T = any> = (data: T) => void;

class EventBus {
  private handlers = new Map<string, Set<EventHandler>>();

  on<T>(event: string, handler: EventHandler<T>) {
    if (!this.handlers.has(event)) this.handlers.set(event, new Set());
    this.handlers.get(event)!.add(handler);
    return () => this.handlers.get(event)?.delete(handler); // unsubscribe
  }

  emit<T>(event: string, data: T) {
    this.handlers.get(event)?.forEach(handler => handler(data));
  }
}

// Usage
const bus = new EventBus();
const unsub = bus.on<User>('user:created', user => sendWelcomeEmail(user));
bus.emit('user:created', newUser);
unsub(); // cleanup
```

### Strategy

```typescript
// Strategy — select algorithm at runtime
interface SortStrategy<T> {
  sort(data: T[]): T[];
}

class QuickSort<T> implements SortStrategy<T> {
  sort(data: T[]) { return [...data].sort(); }
}

class MergeSort<T> implements SortStrategy<T> {
  sort(data: T[]) { /* merge sort impl */ return data; }
}

class Sorter<T> {
  constructor(private strategy: SortStrategy<T>) {}

  setStrategy(strategy: SortStrategy<T>) { this.strategy = strategy; }
  sort(data: T[]) { return this.strategy.sort(data); }
}

// Usage — swap strategy based on data size
const sorter = new Sorter(data.length > 10000 ? new MergeSort() : new QuickSort());
```

### Middleware / Chain of Responsibility

```typescript
// Middleware — processing pipeline (Express/Hono pattern)
type Middleware = (ctx: Context, next: () => Promise<void>) => Promise<void>;

const logger: Middleware = async (ctx, next) => {
  const start = Date.now();
  await next();
  console.log(`${ctx.method} ${ctx.path} ${Date.now() - start}ms`);
};

const auth: Middleware = async (ctx, next) => {
  const token = ctx.headers.get('Authorization');
  if (!token) throw new HttpError(401, 'Unauthorized');
  ctx.user = verifyToken(token);
  await next();
};

const rateLimiter: Middleware = async (ctx, next) => {
  if (isRateLimited(ctx.ip)) throw new HttpError(429, 'Too many requests');
  await next();
};

// Compose: logger → auth → rateLimiter → handler
app.use(logger, auth, rateLimiter);
```

## Gotchas & Best Practices

- ⚠️ **Over-engineering**: Don't apply patterns prematurely. Start simple, refactor when needed.
- ⚠️ **Singleton testing**: Singletons create hidden dependencies. Prefer DI containers.
- ⚠️ **Observer memory leaks**: Always unsubscribe event handlers to prevent memory leaks.
- ⚠️ **God objects**: Repository pattern can become a "god class" — split by aggregate root.
- ⚠️ **Strategy vs if/else**: Only use Strategy when algorithms are complex or swappable. Simple conditionals don't need a pattern.
- ⚠️ **Builder without validation**: Builders can produce invalid objects. Add `build()` validation.
- ⚠️ **Decorator ordering matters**: `RetryClient(LoggingClient(base))` retries log each attempt. `LoggingClient(RetryClient(base))` logs only final result.
- ⚠️ **Abstract Factory overkill**: In modern languages with generics + DI, abstract factories are rarely needed.

### When to Use

| Pattern | Use When | Don't Use When |
|---------|----------|----------------|
| Singleton | Shared resource (DB pool, config) | Testable code needed |
| Factory | Object creation varies by context | Only 1-2 concrete types |
| Builder | 4+ constructor params, optional fields | Simple objects |
| Adapter | Integrating legacy/3rd-party code | Designing new system |
| Decorator | Adding behavior without subclass | Core behavior changes |
| Repository | Data access abstraction | Simple CRUD with ORM |
| Observer | Decoupled event-driven comm | Synchronous workflows |
| Strategy | Swappable algorithms | Fixed algorithm |
| Middleware | Request/response pipelines | Non-pipeline flows |

<!--
BM25 DESIGN RULES:
- H1 = library name (root search anchor)
- H2 = pattern category
- Code:prose ratio ≥ 70:30
- Multi-language examples (TS + Python)
- Keep 5-30KB per file
-->
