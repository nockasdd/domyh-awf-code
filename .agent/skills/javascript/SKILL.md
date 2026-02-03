---
name: javascript
detect: ["*.js", "*.mjs", "*.cjs", ".eslintrc*", "package.json"]
version: "6.0.0"
category: web
tier: 1
---

# JavaScript Patterns — DOMYH Awesome Code v5.5

> ES2025/ES2026 • Node.js 22 LTS • Bun • Deno — 2025-2026

## 🔍 Language Detection

```yaml
javascript_indicators:  # JavaScript skill activates
  - "*.js, *.mjs, *.cjs files"
  - "package.json"
  - "require(), import/export"
  - "function, const, let"
  - "console.log()"
  - "!*.ts files" (TypeScript is separate)

not_javascript:
  - "*.ts, interface, type" → TypeScript
  - "*.jsx with types" → TypeScript
  - "pubspec.yaml" → Dart/Flutter
```

---

## 📊 JavaScript Versions (2025-2026)

| Standard   | Finalized | Key Features                               |
| ---------- | --------- | ------------------------------------------ |
| **ES2024** | 2024-06   | Grouping, Promise.withResolvers            |
| **ES2025** | 2025-06   | Promise.try, Set algebra, Iterator helpers |
| **ES2026** | 2026-06   | Temporal API, using keyword (preview)      |

### ES2025 Features

```javascript
// ✅ Promise.try - Handle sync/async uniformly
const result = await Promise.try(() => {
  if (Math.random() > 0.5) throw new Error("Random fail");
  return "success";
});

// ✅ Set algebra methods
const setA = new Set([1, 2, 3, 4]);
const setB = new Set([3, 4, 5, 6]);

setA.union(setB); // Set {1, 2, 3, 4, 5, 6}
setA.intersection(setB); // Set {3, 4}
setA.difference(setB); // Set {1, 2}
setA.symmetricDifference(setB); // Set {1, 2, 5, 6}

// ✅ Iterator helpers
const doubled = [1, 2, 3]
  .values()
  .map((x) => x * 2)
  .filter((x) => x > 2)
  .toArray(); // [4, 6]

// ✅ RegExp.escape
const userInput = "hello (world)";
const escaped = RegExp.escape(userInput); // 'hello \\(world\\)'
new RegExp(escaped);
```

### ES2026 Preview

```javascript
// ✅ Temporal API (replacing Date)
const now = Temporal.Now.instant();
const date = Temporal.PlainDate.from("2026-02-01");
const dateTime = Temporal.PlainDateTime.from("2026-02-01T12:00:00");

// Immutable, timezone-aware
const tokyo = Temporal.Now.zonedDateTimeISO("Asia/Tokyo");
const duration = Temporal.Duration.from({ hours: 2, minutes: 30 });

// ✅ using keyword (resource management)
{
  using file = await openFile("data.txt");
  // file automatically closed when block exits
}

// ✅ Array.fromAsync
const asyncItems = Array.fromAsync(asyncGenerator());

// ✅ Error.isError (reliable error detection)
Error.isError(new Error()); // true
Error.isError({ message: "fake" }); // false
```

---

## 🛠️ Runtimes & Toolchain

### Node.js 22 LTS (Recommended)

```yaml
version: 22.x (LTS)
key_features:
  - V8 12.4 engine with Maglev compiler
  - Native ESM support
  - Permission model (--permission flag)
  - Stable fs.cp and fs.mv
  - require() for ES modules (transition aid)
  - Improved diagnostics and heap snapshots
package_managers:
  - npm 10.x (default)
  - pnpm 9.x (faster, space-efficient)
  - yarn 4.x (Plug'n'Play)
```

### Bun (Alternative)

```yaml
version: 1.x
key_features:
  - 3-4x faster than Node.js
  - Built-in bundler, transpiler
  - Native TypeScript support
  - Drop-in Node.js replacement
  - bun.lockb binary lockfile
use_cases:
  - Fast development
  - Scripts and CLI tools
  - Performance-critical servers
caveats:
  - Some npm packages may need adjustment
  - Rapid development (check compatibility)
```

### Deno

```yaml
version: 2.x
key_features:
  - Secure by default (permissions)
  - Native TypeScript
  - No node_modules (URL imports)
  - Built-in formatter and linter
  - Fresh framework for web apps
use_cases:
  - Security-focused apps
  - Edge/serverless
  - TypeScript-first projects
```

---

## 🛠️ IDE Support

### VS Code (Recommended)

```yaml
extensions:
  - "ESLint" (dbaeumer.vscode-eslint)
  - "Prettier" (esbenp.prettier-vscode)
  - "JavaScript (ES6) code snippets"
  - "Path Intellisense"
  - "Live Server"
  - "Debugger for Chrome/Edge"
features:
  - IntelliSense
  - Integrated debugging
  - Terminal integration
  - Git integration
settings:
  editor.formatOnSave: true
  editor.defaultFormatter: "esbenp.prettier-vscode"
```

### WebStorm

```yaml
version: 2025.x
features:
  - Deep JavaScript understanding
  - Smart refactoring
  - Built-in debugger (no source maps needed)
  - Framework-specific intelligence
  - Code analysis and suggestions
use_cases:
  - Large JavaScript projects
  - Angular/React/Vue development
notes:
  - Paid IDE
  - Most comprehensive JS tooling
```

---

## 📦 Recommended Libraries

### Runtime & Build

| Tool               | Use Case             |
| ------------------ | -------------------- |
| **Node.js 22 LTS** | Production runtime   |
| **Bun**            | Fast dev, scripts    |
| **Vite**           | Dev server & bundler |
| **esbuild**        | Ultra-fast bundler   |
| **Rollup**         | Library bundling     |

### Backend Frameworks

| Framework   | Use Case           | Performance |
| ----------- | ------------------ | ----------- |
| **Express** | Minimal, mature    | Good        |
| **Fastify** | Fast, JSON-focused | Excellent   |
| **Hono**    | Edge-first         | Excellent   |
| **Koa**     | Middleware-focused | Good        |
| **NestJS**  | Enterprise, DI     | Good        |

### Frontend Frameworks

| Framework    | Use Case                |
| ------------ | ----------------------- |
| **React 19** | UI components           |
| **Vue 3**    | Progressive framework   |
| **Svelte 5** | Compiled, lightweight   |
| **Solid**    | Fine-grained reactivity |

### Utilities

| Library       | Use Case              |
| ------------- | --------------------- |
| **lodash-es** | Utility functions     |
| **date-fns**  | Date manipulation     |
| **zod**       | Runtime validation    |
| **axios**     | HTTP client           |
| **dotenv**    | Environment variables |

---

## ✨ Modern Patterns (ES2024+)

### Async/Await Best Practices

```javascript
// ✅ Proper async/await with error handling
async function fetchUser(id) {
  try {
    const response = await fetch(`/api/users/${id}`);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error("Fetch failed:", error);
    throw error;
  }
}

// ✅ Parallel execution with Promise.all
const [user, orders] = await Promise.all([fetchUser(id), fetchOrders(id)]);

// ✅ Promise.allSettled for partial failures
const results = await Promise.allSettled([
  fetchUser(1),
  fetchUser(2),
  fetchUser(3),
]);

results.forEach((result, i) => {
  if (result.status === "fulfilled") {
    console.log(`User ${i}: ${result.value.name}`);
  } else {
    console.error(`User ${i} failed: ${result.reason}`);
  }
});

// ✅ AbortController for cancellation
const controller = new AbortController();
const timeout = setTimeout(() => controller.abort(), 5000);

try {
  const response = await fetch(url, { signal: controller.signal });
  clearTimeout(timeout);
  return await response.json();
} catch (error) {
  if (error.name === "AbortError") {
    console.log("Request timed out");
  }
  throw error;
}
```

### Destructuring & Spread

```javascript
// ✅ Destructuring with defaults
const { name = "Guest", age = 0 } = user ?? {};

// ✅ Optional chaining + nullish coalescing
const city = user?.address?.city ?? "Unknown";

// ✅ Spread for immutable updates
const updatedUser = { ...user, name: "Alice" };
const extendedArray = [...array, newItem];

// ✅ Rest parameters
function sum(...numbers) {
  return numbers.reduce((a, b) => a + b, 0);
}
```

### Object.groupBy (ES2024)

```javascript
// ✅ Grouping items
const users = [
  { name: "Alice", age: 25 },
  { name: "Bob", age: 30 },
  { name: "Charlie", age: 25 },
];

const byAge = Object.groupBy(users, (user) => user.age);
// { 25: [Alice, Charlie], 30: [Bob] }
```

---

## ⚠️ Common Pitfalls

```javascript
// ❌ AVOID: == comparison (type coercion)
if (value == null) {}  // Matches both null and undefined

// ✅ USE: === strict equality
if (value === null || value === undefined) {}
// Or shorthand for null/undefined only:
if (value == null) {}  // This one case is acceptable

// ❌ AVOID: var (function-scoped, hoisted)
var x = 1;

// ✅ USE: const (immutable binding) / let (mutable)
const x = 1;
let y = 2;

// ❌ AVOID: for...in for arrays
for (const i in array) {}  // Iterates string keys, not efficient

// ✅ USE: for...of or array methods
for (const item of array) {}
array.forEach(item => {});

// ❌ AVOID: callback hell
fetch(url, (err, data) => {
  process(data, (err, result) => { ... });
});

// ✅ USE: async/await
const data = await fetch(url);
const result = await process(data);

// ❌ AVOID: floating promises
doSomethingAsync();  // No await, no catch

// ✅ USE: always handle promises
await doSomethingAsync();
// Or: doSomethingAsync().catch(handleError);

// ❌ AVOID: modifying function parameters
function update(user) {
  user.name = 'New Name';  // Mutation!
}

// ✅ USE: return new object
function update(user) {
  return { ...user, name: 'New Name' };
}
```

---

## 📂 Project Structure

```
src/
├── index.js              # Entry point
├── config/
│   └── index.js          # Configuration
├── routes/
│   ├── index.js          # Route registration
│   └── users.js          # User routes
├── controllers/
│   └── userController.js
├── services/
│   └── userService.js
├── repositories/
│   └── userRepository.js
├── models/
│   └── User.js
├── middleware/
│   ├── auth.js
│   └── errorHandler.js
└── utils/
    └── helpers.js
```

---

## 🎨 Naming Conventions (Airbnb Style)

| Element          | Convention    | Example                 |
| ---------------- | ------------- | ----------------------- |
| Variables        | camelCase     | `userName`, `isActive`  |
| Functions        | camelCase     | `getUserData()`         |
| Classes          | PascalCase    | `UserService`           |
| Constants        | UPPER_SNAKE   | `MAX_RETRIES`           |
| Files            | kebab-case    | `user-service.js`       |
| React Components | PascalCase    | `UserProfile.jsx`       |
| Private          | \_camelCase   | `_internalValue`        |
| Boolean vars     | is/has prefix | `isLoading`, `hasError` |

---

## ✅ Production Checklist

### Code Quality

- [ ] ESLint + Prettier configured
- [ ] No `var`, only `const`/`let`
- [ ] async/await used (no callback hell)
- [ ] Strict equality (`===`) used
- [ ] No console.log in production

### Error Handling

- [ ] All promises handled
- [ ] Global error handler configured
- [ ] Meaningful error messages

### Security

- [ ] Input validation with Zod/Joi
- [ ] Environment variables for secrets
- [ ] Rate limiting implemented
- [ ] CORS properly configured

### Performance

- [ ] Bundle size optimized
- [ ] Lazy loading where applicable
- [ ] Caching strategy implemented

---

_DOMYH Awesome Code v6.0.0 • JavaScript Development • 2025-2026_
