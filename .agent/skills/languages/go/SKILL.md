---
name: go
detect: ["go.mod", "go.sum", "*.go", "go.work"]
version: "6.4.0"
category: backend
tier: 1
---

# Go Patterns — DOMYH Awesome Code

> **Version**: Go 1.22/1.23/1.24 (2025-2026)
> **Philosophy**: Simplicity, explicit error handling, powerful concurrency

---

## 🎯 When to Use This Skill

Use for: Backend services, microservices, CLI tools, cloud-native apps.
**NOT for**: Frontend (→ react/vue), mobile (→ swift/kotlin).

---

## 📦 Recommended Stack (2025-2026)

### Web Frameworks

| Library      | Use Case             | Performance        |
| ------------ | -------------------- | ------------------ |
| **Gin**      | REST APIs 🏆         | Very fast          |
| **Echo**     | Feature-rich         | Fast               |
| **Fiber**    | Express-style        | Fastest (fasthttp) |
| **Chi**      | Lightweight, modular | Fast               |
| **net/http** | Standard library     | Fast               |

### Database

| Library    | Use Case          |
| ---------- | ----------------- |
| **sqlc**   | Type-safe SQL 🏆  |
| **pgx/v5** | PostgreSQL driver |
| **GORM**   | Full ORM          |
| **sqlx**   | SQL extensions    |
| **ent**    | Graph-based ORM   |

### Utilities

| Library     | Use Case                       |
| ----------- | ------------------------------ |
| **slog**    | Structured logging (stdlib) 🏆 |
| **cobra**   | CLI apps                       |
| **viper**   | Configuration                  |
| **wire**    | Dependency injection           |
| **testify** | Testing assertions             |

### IDE Support

| IDE         | Market Share | Features                         |
| ----------- | ------------ | -------------------------------- |
| **VS Code** | 37% 🏆       | gopls, Go extension, Delve debug |
| **GoLand**  | 28%          | Full IDE, refactoring, analysis  |
| **Neovim**  | Growing      | gopls, LSP integration           |

---

## 🆕 Go 1.22/1.23/1.24 Features

### Range Over Int (Go 1.22)

```go
// ✅ Go 1.22: Range over integers
for i := range 10 {
    fmt.Println(i)  // 0, 1, 2, ..., 9
}

// ✅ Replaces traditional for loop
for i := 0; i < n; i++ {
    // old way
}
```

### Enhanced ServeMux (Go 1.22)

```go
// ✅ Method-based routing
mux := http.NewServeMux()

// Method patterns
mux.HandleFunc("GET /users", listUsers)
mux.HandleFunc("POST /users", createUser)
mux.HandleFunc("GET /users/{id}", getUser)
mux.HandleFunc("PUT /users/{id}", updateUser)
mux.HandleFunc("DELETE /users/{id}", deleteUser)

// ✅ Path wildcards with {param}
mux.HandleFunc("GET /files/{path...}", serveFiles)

func getUser(w http.ResponseWriter, r *http.Request) {
    // ✅ Get path value
    id := r.PathValue("id")
    // ...
}
```

### Iterators / Range Over Func (Go 1.23)

```go
import "iter"

// ✅ Custom iterator function
func FilterUsers(users []User, predicate func(User) bool) iter.Seq[User] {
    return func(yield func(User) bool) {
        for _, u := range users {
            if predicate(u) {
                if !yield(u) {
                    return  // Early termination
                }
            }
        }
    }
}

// ✅ Usage with range
activeUsers := FilterUsers(users, func(u User) bool {
    return u.Active
})

for user := range activeUsers {
    fmt.Println(user.Name)
}

// ✅ Collect to slice
import "slices"
result := slices.Collect(activeUsers)
```

### Generics Best Practices

```go
// ✅ Generic function with constraints
func Map[T, U any](items []T, f func(T) U) []U {
    result := make([]U, len(items))
    for i, item := range items {
        result[i] = f(item)
    }
    return result
}

// ✅ Generic type with constraints
type Set[T comparable] struct {
    items map[T]struct{}
}

func NewSet[T comparable]() *Set[T] {
    return &Set[T]{items: make(map[T]struct{})}
}

func (s *Set[T]) Add(item T) {
    s.items[item] = struct{}{}
}

func (s *Set[T]) Contains(item T) bool {
    _, ok := s.items[item]
    return ok
}

// ✅ Type inference - no need to specify types
names := Map(users, func(u User) string { return u.Name })
```

---

## 📝 Structured Logging (slog)

```go
import "log/slog"

// ✅ Create structured logger
logger := slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
    Level: slog.LevelInfo,
}))

// ✅ Log with attributes
logger.Info("user created",
    slog.String("user_id", user.ID),
    slog.String("email", user.Email),
    slog.Duration("duration", time.Since(start)),
)

// ✅ Child logger with default attributes
reqLogger := logger.With(
    slog.String("request_id", requestID),
    slog.String("user_id", userID),
)

reqLogger.Info("processing request")
reqLogger.Error("operation failed", slog.Any("error", err))

// ✅ Context-aware logging
logger.InfoContext(ctx, "database query",
    slog.String("query", query),
    slog.Int("rows", rowCount),
)
```

---

## 🛡️ Error Handling Patterns

```go
// ✅ Error wrapping with context
func GetUser(id string) (*User, error) {
    user, err := db.FindUser(id)
    if err != nil {
        return nil, fmt.Errorf("GetUser(%s): %w", id, err)
    }
    return user, nil
}

// ✅ Sentinel errors
var (
    ErrNotFound     = errors.New("not found")
    ErrUnauthorized = errors.New("unauthorized")
    ErrValidation   = errors.New("validation error")
)

// ✅ Check with errors.Is
if errors.Is(err, ErrNotFound) {
    http.Error(w, "Not Found", http.StatusNotFound)
    return
}

// ✅ Custom error types
type ValidationError struct {
    Field   string
    Message string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("%s: %s", e.Field, e.Message)
}

// ✅ Extract with errors.As
var validErr *ValidationError
if errors.As(err, &validErr) {
    // Handle validation error
    log.Printf("Validation failed: %s", validErr.Field)
}
```

---

## ⚡ Concurrency Patterns

```go
// ✅ Context-aware goroutine
func ProcessItems(ctx context.Context, items []Item) error {
    g, ctx := errgroup.WithContext(ctx)

    for _, item := range items {
        item := item  // Go 1.22+ not needed
        g.Go(func() error {
            return processItem(ctx, item)
        })
    }

    return g.Wait()
}

// ✅ Worker pool pattern
func WorkerPool(ctx context.Context, jobs <-chan Job, numWorkers int) {
    var wg sync.WaitGroup

    for range numWorkers {  // Go 1.22+
        wg.Add(1)
        go func() {
            defer wg.Done()
            for {
                select {
                case <-ctx.Done():
                    return
                case job, ok := <-jobs:
                    if !ok {
                        return
                    }
                    process(job)
                }
            }
        }()
    }

    wg.Wait()
}

// ✅ Fan-out, fan-in
func FanOutFanIn[T, R any](ctx context.Context, items []T, workers int, process func(T) R) []R {
    jobs := make(chan T, len(items))
    results := make(chan R, len(items))

    // Start workers
    var wg sync.WaitGroup
    for range workers {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for item := range jobs {
                results <- process(item)
            }
        }()
    }

    // Send jobs
    for _, item := range items {
        jobs <- item
    }
    close(jobs)

    // Collect results
    go func() {
        wg.Wait()
        close(results)
    }()

    var output []R
    for r := range results {
        output = append(output, r)
    }
    return output
}
```

---

## 🔧 HTTP Middleware Pattern

```go
// ✅ Middleware signature
type Middleware func(http.Handler) http.Handler

// ✅ Logging middleware
func LoggingMiddleware(logger *slog.Logger) Middleware {
    return func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            start := time.Now()

            // Wrap response writer
            wrapped := &responseWriter{ResponseWriter: w, statusCode: 200}

            next.ServeHTTP(wrapped, r)

            logger.Info("HTTP request",
                slog.String("method", r.Method),
                slog.String("path", r.URL.Path),
                slog.Int("status", wrapped.statusCode),
                slog.Duration("duration", time.Since(start)),
            )
        })
    }
}

// ✅ Chain middleware
func Chain(h http.Handler, middlewares ...Middleware) http.Handler {
    for i := len(middlewares) - 1; i >= 0; i-- {
        h = middlewares[i](h)
    }
    return h
}

// Usage
handler := Chain(mux,
    LoggingMiddleware(logger),
    RecoveryMiddleware(),
    AuthMiddleware(authService),
)
```

---

## 🧪 Testing Patterns

```go
// ✅ Table-driven tests
func TestParseID(t *testing.T) {
    tests := []struct {
        name    string
        input   string
        want    int
        wantErr bool
    }{
        {"valid", "123", 123, false},
        {"invalid", "abc", 0, true},
        {"empty", "", 0, true},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got, err := ParseID(tt.input)
            if (err != nil) != tt.wantErr {
                t.Errorf("error = %v, wantErr %v", err, tt.wantErr)
                return
            }
            if got != tt.want {
                t.Errorf("got %d, want %d", got, tt.want)
            }
        })
    }
}

// ✅ Go 1.24: T.Context()
func TestWithContext(t *testing.T) {
    ctx := t.Context()  // Auto-canceled when test ends

    result, err := FetchData(ctx)
    if err != nil {
        t.Fatalf("FetchData: %v", err)
    }
    // ...
}

// ✅ Mocking with interfaces
type UserRepository interface {
    Get(ctx context.Context, id string) (*User, error)
}

type MockUserRepo struct {
    GetFunc func(ctx context.Context, id string) (*User, error)
}

func (m *MockUserRepo) Get(ctx context.Context, id string) (*User, error) {
    return m.GetFunc(ctx, id)
}
```

---

## 📁 Project Structure

```
myapp/
├── cmd/
│   └── server/
│       └── main.go         # Entry point
├── internal/
│   ├── handlers/           # HTTP handlers
│   ├── services/           # Business logic
│   ├── repository/         # Data access
│   ├── models/            # Domain types
│   └── middleware/        # HTTP middleware
├── pkg/                   # Public packages
├── migrations/            # Database migrations
├── go.mod
├── go.sum
└── Makefile
```

---

## ✅ Best Practices Checklist

### Code Quality

- [ ] `gofmt` and `goimports` applied
- [ ] `go vet` passes
- [ ] `staticcheck` passes
- [ ] Race detection: `go test -race`

### Error Handling

- [ ] All errors checked
- [ ] Errors wrapped with `%w`
- [ ] Sentinel errors for expected cases
- [ ] `errors.Is`/`errors.As` used

### Concurrency

- [ ] Context propagated
- [ ] No goroutine leaks
- [ ] Channels closed properly
- [ ] `sync.WaitGroup` used correctly

### Performance

- [ ] Avoid unnecessary allocations
- [ ] Use `sync.Pool` for hot paths
- [ ] Profile with `pprof`
- [ ] Benchmark critical paths

---

_DOMYH Awesome Code • Go 1.22/1.23/1.24_
