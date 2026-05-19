---
library: go
version: 1.25
latest: true
category: language
official_docs: https://go.dev/doc/
last_updated: 2026-03-21
last_checked: 2026-03-21
source: ai-enhanced from go.dev/doc/go1.25 + effective_go + web research
---

# Go v1.25

> Go — A statically typed, compiled language designed for simplicity, concurrency, and performance.
> Current: v1.25.7 (Feb 2026) | Previous: v1.24 (Feb 2025)
> Docs: https://go.dev/doc/

## Version Comparison

| Feature | v1.23 | v1.24 | v1.25 |
|:--------|:------|:------|:------|
| Range-over-func (iterators) | ✅ Stable | ✅ | ✅ |
| Generic type aliases | ❌ | ✅ | ✅ |
| Swiss Tables map impl | ❌ | ✅ Default | ✅ |
| Container-aware GOMAXPROCS | ❌ | ❌ | ✅ Auto cgroup |
| `testing/synctest` | ❌ | Experimental | ✅ Stable |
| `encoding/json/v2` | ❌ | ❌ | 🧪 Experimental |
| Trace FlightRecorder | ❌ | ❌ | ✅ |
| Experimental GC (greenteagc) | ❌ | ❌ | 🧪 10-40% less GC |
| DWARF5 debug info | ❌ | ❌ | ✅ Default |
| `os.Root` (dir-scoped FS) | ❌ | ✅ | ✅ |
| `runtime.AddCleanup` | ❌ | ✅ | ✅ |
| FIPS 140-3 crypto module | ❌ | ✅ | ✅ |
| Tool directives in go.mod | ❌ | ✅ | ✅ |
| PGO | Single-digit% | ✅ Stable | ✅ Stable |
| Min macOS | 11 | 11 | **12 Monterey+** |
| Min Linux kernel | 2.6.32 | 3.2+ | 3.2+ |

## Installation

```bash
# macOS / Linux
curl -fsSL https://go.dev/dl/go1.25.7.linux-amd64.tar.gz | sudo tar -C /usr/local -xzf -
export PATH=$PATH:/usr/local/go/bin

# macOS (Homebrew) — requires macOS 12 Monterey+
brew install go

# Windows (winget)
winget install GoLang.Go

# Verify
go version    # go1.25.7 linux/amd64
go env GOPATH # ~/go (default)
```

## Configuration

```bash
# Go module init
go mod init github.com/user/project

# go.mod — module file
module github.com/user/project

go 1.25

# v1.24+: tool directives replace tools.go
tool (
    golang.org/x/tools/cmd/stringer
    github.com/sqlc-dev/sqlc/cmd/sqlc
)

require (
    github.com/gin-gonic/gin v1.9.1
)

# Environment variables
GOPATH     # workspace path (default: ~/go)
GOBIN      # binary install path (default: $GOPATH/bin)
GOPROXY    # module proxy (default: https://proxy.golang.org,direct)
GOFLAGS    # default flags for go commands
GOFIPS140  # enable FIPS 140-3 mode (v1.24+)
CGO_ENABLED # 0=disable cgo, 1=enable

# Profile-guided optimization
go build -pgo=auto ./...  # uses default.pgo if present
```

## Core API

### Types & Variables

```go
// Basic types
var i int = 42
var f float64 = 3.14
var s string = "hello"
var b bool = true
var p *int = &i              // pointer

// Short declaration (inside functions only)
name := "Go"
count := 0

// Constants
const Pi = 3.14159
const (
    StatusOK    = 200
    StatusError = 500
)

// Arrays & Slices
arr := [3]int{1, 2, 3}       // fixed-size array
sl := []int{1, 2, 3}         // slice (dynamic)
sl = append(sl, 4, 5)        // append to slice
sl2 := make([]int, 0, 100)   // pre-allocate capacity

// Maps — ⚠️ MUST initialize before use (nil map panics!)
m := map[string]int{
    "one": 1,
    "two": 2,
}
m["three"] = 3
v, ok := m["four"]  // ok=false if key not found
delete(m, "one")

// Structs
type User struct {
    Name  string `json:"name"`
    Email string `json:"email"`
    Age   int    `json:"age,omitempty"`
}
u := User{Name: "Alice", Email: "alice@go.dev"}
```

### Functions & Error Handling

```go
// Multiple return values
func divide(a, b float64) (float64, error) {
    if b == 0 {
        return 0, fmt.Errorf("division by zero")
    }
    return a / b, nil
}

// Named return values
func swap(a, b int) (x, y int) {
    return b, a
}

// Variadic functions
func sum(nums ...int) int {
    total := 0
    for _, n := range nums {
        total += n
    }
    return total
}

// Error handling pattern (Go idiom)
result, err := divide(10, 0)
if err != nil {
    log.Fatal(err) // or return err
}

// errors.Is / errors.As (Go 1.13+)
if errors.Is(err, os.ErrNotExist) { /* ... */ }

var pathErr *os.PathError
if errors.As(err, &pathErr) {
    fmt.Println(pathErr.Path)
}

// Wrapping errors
return fmt.Errorf("failed to process %s: %w", name, err)
```

### Interfaces & Generics

```go
// Interface
type Reader interface {
    Read(p []byte) (n int, err error)
}

// Interface embedding
type ReadWriter interface {
    Reader
    Writer
}

// Empty interface (any = interface{})
func printAnything(v any) {
    fmt.Println(v)
}

// Generics (Go 1.18+)
func Map[T any, U any](s []T, f func(T) U) []U {
    result := make([]U, len(s))
    for i, v := range s {
        result[i] = f(v)
    }
    return result
}

// Type constraints
type Number interface {
    ~int | ~float64 | ~int64
}

func Sum[T Number](nums []T) T {
    var total T
    for _, n := range nums {
        total += n
    }
    return total
}

// v1.24: Generic type aliases
type Set[T comparable] = map[T]struct{}
```

### Concurrency

```go
// Goroutines
go func() {
    fmt.Println("running concurrently")
}()

// Channels
ch := make(chan int)        // unbuffered
ch := make(chan int, 10)    // buffered

go func() { ch <- 42 }()
val := <-ch

// Select (multiplexing)
select {
case msg := <-ch1:
    fmt.Println(msg)
case ch2 <- value:
    fmt.Println("sent")
case <-time.After(5 * time.Second):
    fmt.Println("timeout")
}

// WaitGroup
var wg sync.WaitGroup
for i := 0; i < 10; i++ {
    wg.Add(1)
    go func(id int) {
        defer wg.Done()
        process(id)
    }(i)  // ⚠️ Pass loop var as arg!
}
wg.Wait()

// Mutex
var mu sync.Mutex
mu.Lock()
defer mu.Unlock()
// critical section

// Context (cancellation + timeout)
ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
defer cancel()

select {
case result := <-doWork(ctx):
    fmt.Println(result)
case <-ctx.Done():
    fmt.Println("timeout:", ctx.Err())
}
```

### Iterators (v1.23+)

```go
// Range-over-func — custom iterators
import "iter"

// Seq[V] = func(yield func(V) bool)
func Fibonacci() iter.Seq[int] {
    return func(yield func(int) bool) {
        a, b := 0, 1
        for {
            if !yield(a) {
                return
            }
            a, b = b, a+b
        }
    }
}

// Usage
for n := range Fibonacci() {
    if n > 100 { break }
    fmt.Println(n)
}

// Seq2[K, V] for key-value pairs
func Enumerate[T any](s []T) iter.Seq2[int, T] {
    return func(yield func(int, T) bool) {
        for i, v := range s {
            if !yield(i, v) {
                return
            }
        }
    }
}

// slices/maps package iterator support
import "slices"
slices.All(mySlice)      // iter.Seq2[int, T]
slices.Values(mySlice)   // iter.Seq[T]
slices.Collect(seq)      // collect iterator to slice
```

### HTTP & Web

```go
// HTTP server (stdlib)
http.HandleFunc("/hello", func(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintf(w, "Hello, %s!", r.URL.Query().Get("name"))
})
log.Fatal(http.ListenAndServe(":8080", nil))

// HTTP server with mux patterns (Go 1.22+)
mux := http.NewServeMux()
mux.HandleFunc("GET /api/users/{id}", getUser)
mux.HandleFunc("POST /api/users", createUser)

// Path value extraction
func getUser(w http.ResponseWriter, r *http.Request) {
    id := r.PathValue("id")
    // ...
}

// HTTP client
client := &http.Client{Timeout: 10 * time.Second}
resp, err := client.Get("https://api.example.com/data")
if err != nil {
    log.Fatal(err)
}
defer resp.Body.Close()

body, _ := io.ReadAll(resp.Body)
```

### Testing

```go
// file: math_test.go
func TestAdd(t *testing.T) {
    got := Add(2, 3)
    if got != 5 {
        t.Errorf("Add(2,3) = %d; want 5", got)
    }
}

// Table-driven tests (Go idiom)
func TestDivide(t *testing.T) {
    tests := []struct {
        name    string
        a, b    float64
        want    float64
        wantErr bool
    }{
        {"normal",   10, 2, 5, false},
        {"zero-div", 10, 0, 0, true},
    }
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got, err := Divide(tt.a, tt.b)
            if (err != nil) != tt.wantErr {
                t.Errorf("error = %v, wantErr %v", err, tt.wantErr)
            }
            if got != tt.want {
                t.Errorf("got %v, want %v", got, tt.want)
            }
        })
    }
}

// Benchmarks
func BenchmarkSort(b *testing.B) {
    for b.Loop() {  // v1.24: b.Loop() replaces b.N
        sort.Ints(data)
    }
}

// Fuzzing
func FuzzParse(f *testing.F) {
    f.Add("hello")
    f.Fuzz(func(t *testing.T, input string) {
        result, err := Parse(input)
        if err != nil { return }
        _ = result
    })
}

// Commands
// go test ./...
// go test -bench=. -benchmem
// go test -fuzz=FuzzParse
// go test -cover -coverprofile=cover.out
// go tool cover -html=cover.out
```

### Testing Concurrent Code (v1.25: `testing/synctest`)

```go
import "testing/synctest"

func TestConcurrentCache(t *testing.T) {
    // synctest.Test runs in isolated "bubble" with virtualized time
    synctest.Test(t, func(t *testing.T) {
        cache := NewCache(5 * time.Second) // TTL-based cache
        cache.Set("key", "value")

        // Time advances instantly — no real 5s wait!
        time.Sleep(6 * time.Second)

        _, ok := cache.Get("key")
        if ok {
            t.Error("expected cache entry to expire")
        }
    })
}

func TestWorkerPool(t *testing.T) {
    synctest.Test(t, func(t *testing.T) {
        ch := make(chan int)
        go func() { ch <- 42 }()

        // Wait blocks until all goroutines in bubble are blocked
        synctest.Wait()
        val := <-ch
        if val != 42 {
            t.Errorf("got %d, want 42", val)
        }
    })
}
```

### Trace FlightRecorder (v1.25)

```go
import "runtime/trace"

// Lightweight continuous tracing — capture last N seconds on demand
fr := trace.NewFlightRecorder()
fr.Start()

// ...application runs...

// When significant event occurs, snapshot trace:
if err := fr.WriteTo(os.Create("trace.out")); err != nil {
    log.Fatal(err)
}
// Analyze: go tool trace trace.out
```

## Common Patterns

```go
// 1. Functional options pattern
type Server struct {
    port    int
    timeout time.Duration
}

type Option func(*Server)

func WithPort(port int) Option {
    return func(s *Server) { s.port = port }
}

func WithTimeout(d time.Duration) Option {
    return func(s *Server) { s.timeout = d }
}

func NewServer(opts ...Option) *Server {
    s := &Server{port: 8080, timeout: 30 * time.Second}
    for _, opt := range opts {
        opt(s)
    }
    return s
}

srv := NewServer(WithPort(9090), WithTimeout(60*time.Second))

// 2. Worker pool
func workerPool(jobs <-chan Job, results chan<- Result, workers int) {
    var wg sync.WaitGroup
    for i := 0; i < workers; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for job := range jobs {
                results <- process(job)
            }
        }()
    }
    wg.Wait()
    close(results)
}

// 3. Graceful shutdown
ctx, stop := signal.NotifyContext(context.Background(),
    syscall.SIGINT, syscall.SIGTERM)
defer stop()

srv := &http.Server{Addr: ":8080"}
go func() { srv.ListenAndServe() }()

<-ctx.Done()
shutdownCtx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
defer cancel()
srv.Shutdown(shutdownCtx)

// 4. Dependency injection via interfaces
type UserStore interface {
    GetUser(ctx context.Context, id string) (*User, error)
}

type Service struct {
    store UserStore  // injected
}

func NewService(store UserStore) *Service {
    return &Service{store: store}
}

// 5. Middleware pattern (HTTP)
func Logger(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        start := time.Now()
        next.ServeHTTP(w, r)
        log.Printf("%s %s %v", r.Method, r.URL.Path, time.Since(start))
    })
}

mux := http.NewServeMux()
handler := Logger(Auth(mux))
```

## Gotchas & Breaking Changes

### General Gotchas

- ⚠️ **Nil map panic**: Writing to uninitialized map panics at runtime. Always `make(map[K]V)` or use literal.
  ```go
  var m map[string]int
  m["key"] = 1  // PANIC: assignment to entry in nil map
  // Fix: m = make(map[string]int)
  ```

- ⚠️ **Variable shadowing with `:=`**: Inner scope `:=` creates NEW variable, doesn't modify outer.
  ```go
  x := 1
  if true {
      x := 2  // shadows outer x!
      _ = x
  }
  fmt.Println(x)  // still 1!
  // Fix: use x = 2 (not :=)
  ```

- ⚠️ **Range loop + goroutine closure**: Loop variable reused across iterations.
  ```go
  for _, v := range items {
      go func() {
          process(v)  // ⚠️ All goroutines see LAST value!
      }()
  }
  // Fix: pass as argument
  go func(v Item) { process(v) }(v)
  // Or (Go 1.22+): loop var is per-iteration (fixed)
  ```

- ⚠️ **Send to closed channel panics**: Always only close from sender side.
  ```go
  close(ch)
  ch <- data  // PANIC: send on closed channel
  ```

- ⚠️ **Slice append may or may not allocate**: `append` returns new slice — always reassign.
  ```go
  s2 := append(s1, 4)  // s2 may share underlying array with s1!
  // Fix: use slices.Clone(s1) before appending to avoid aliasing
  ```

- ⚠️ **defer evaluates args immediately**:
  ```go
  x := 1
  defer fmt.Println(x)  // prints 1, not 2
  x = 2
  // Fix: use closure: defer func() { fmt.Println(x) }()
  ```

### v1.25 Breaking Changes

- ⚠️ **macOS 12 Monterey required**: macOS 11 Big Sur no longer supported.
- ⚠️ **Windows/ARM 32-bit deprecated**: Final version with Win/ARM32 — removed in Go 1.26.
- ⚠️ **FMA floating-point (amd64 v3+)**: `GOAMD64=v3` uses fused multiply-add — may slightly change float results.
- ⚠️ **Container-aware GOMAXPROCS**: Default behavior changed — respects cgroup CPU limits. Disable: `GODEBUG=containermaxprocs=0`.
- ⚠️ **`encoding/json/v2` error text**: If using `GOEXPERIMENT=jsonv2`, error messages may differ from v1.
- ⚠️ **Stricter module checksums**: Corrupted/mismatched module data fails faster.
- ⚠️ **New `go vet` analyzers**: `waitgroup` (misused `WaitGroup.Add`) + `hostport` (IPv6 address format) may surface new warnings.

### v1.24 Breaking Changes

- ⚠️ **Swiss Tables map**: New map implementation changes memory layout. If regression, set `GOEXPERIMENT=noswissmap`.
- ⚠️ **`runtime.GOROOT` deprecated**: Use `GOROOT` env var instead.
- ⚠️ **Min Linux kernel 3.2+**: Older kernels no longer supported.
- ⚠️ **`runtime.SetFinalizer` → `runtime.AddCleanup`**: Prefer `AddCleanup` — `SetFinalizer` is error-prone and deprecated pattern.
- ⚠️ **New `go vet` warnings**: May flag existing test code — fix, don't suppress.
- ⚠️ **Deprecated crypto functions**: `NewOFB`, `NewCFBEncrypter`, `NewCFBDecrypter` deprecated.

### v1.23 Breaking Changes

- ⚠️ **Timer/Ticker channel now unbuffered**: Code relying on `len(timer.C)` or buffered behavior BREAKS. Use non-blocking receive instead.
  ```go
  // Old (broken in 1.23): if len(t.C) > 0 { <-t.C }
  // New: select { case <-t.C: default: }
  ```
- ⚠️ **`go:linkname` restricted**: Can no longer reference unexported symbols in other packages.

## Migration

### From Go 1.24 → 1.25
1. Update `go 1.25` in `go.mod`
2. Update macOS CI images to macOS 12+
3. Replace `sync.WaitGroup` misuses flagged by new vet analyzer
4. Fix IPv6 hostport issues flagged by `hostport` analyzer
5. Test with `GOEXPERIMENT=greenteagc` for GC improvements (10-40% less overhead)
6. Test with `GOEXPERIMENT=jsonv2` for faster JSON decoding
7. Adopt `testing/synctest` for concurrent test code
8. Use `trace.FlightRecorder` for lightweight production tracing
9. Run `go vet ./...` — 2 new analyzers

### From Go 1.23 → 1.24
1. Update `go 1.24` in `go.mod`
2. Replace `tools.go` with `tool` directives in `go.mod`
3. Replace `runtime.SetFinalizer` → `runtime.AddCleanup`
4. Test with Swiss Tables map — set `GOEXPERIMENT=noswissmap` if issues
5. Update Linux CI images to kernel 3.2+
6. Adopt `os.Root` for directory-scoped filesystem access
7. Run `go vet ./...` — new test analyzers

<!--
BM25 DESIGN RULES:
- H1 = library name (root search anchor)
- H2 = feature category, add (vN) suffix for version matching
- Code:prose ratio ≥ 70:30
- Use ⚠️ diff notes for version disambiguation
- Keep 5-30KB per file, H2 sections ~50 lines each
-->
