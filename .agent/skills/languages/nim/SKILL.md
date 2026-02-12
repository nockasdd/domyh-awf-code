---
name: nim
detect: ["*.nim", "*.nimble", "nim.cfg"]
version: "6.2.1"
category: systems
tier: 3
---

# Nim Patterns — DOMYH Awesome Code

> **Version**: Nim 2.0+ (2025-2026)
> **Focus**: Python-like syntax, C-like performance
> **Philosophy**: Efficient, expressive, elegant

---

## 🎯 When to Use

Use for: Systems programming, game dev, CLI tools, scripting with performance.
**NOT for**: Large team projects (smaller ecosystem), web backends (→ go).

---

## 🔧 Project Setup

```bash
nimble init myproject
cd myproject
nim c -r src/myproject.nim
```

---

## 🔄 Core Patterns

### Types and Procedures

```nim
type
  User = object
    id: int
    name: string
    email: string
    active: bool

  UserError = object of CatchableError

proc createUser(name, email: string): User =
  if name.len == 0:
    raise newException(UserError, "Name required")
  result = User(id: 1, name: name, email: email, active: true)

proc greet(user: User): string =
  "Hello, " & user.name & "!"

# Usage
let user = createUser("John", "john@example.com")
echo user.greet()
```

### Templates and Macros

```nim
# Template (compile-time substitution)
template time(body: untyped): float =
  let start = cpuTime()
  body
  cpuTime() - start

# Usage
let elapsed = time:
  for i in 0..<1_000_000:
    discard i * 2
echo "Elapsed: ", elapsed

# Macro (AST manipulation)
import macros

macro debug(n: varargs[typed]): untyped =
  result = newNimNode(nnkStmtList)
  for i in n:
    result.add quote do:
      echo astToStr(`i`), " = ", `i`

debug x, y, z  # Prints: x = 1, y = 2, z = 3
```

### Async/Await

```nim
import asyncdispatch, httpclient

proc fetchUrl(url: string): Future[string] {.async.} =
  let client = newAsyncHttpClient()
  defer: client.close()
  result = await client.getContent(url)

proc main() {.async.} =
  let content = await fetchUrl("https://example.com")
  echo content.len, " bytes"

waitFor main()
```

---

## ✅ Production Checklist

- [ ] `nim check` passing
- [ ] Tests with `testament` or `unittest`
- [ ] `--gc:arc` or `--gc:orc` for memory
- [ ] Cross-compile for targets

---

_DOMYH Awesome Code • Nim 2.0+_
