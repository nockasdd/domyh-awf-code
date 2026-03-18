# Go — Advanced Patterns


# Load only when explicitly referenced

## Table of Contents

- [Advanced Error Handling](#advanced-error-handling)
- [Concurrency Patterns](#concurrency-patterns)
- [Performance Optimization](#performance-optimization)
- [Testing Strategies](#testing-strategies)
- [Generics Patterns](#generics-patterns)
- [Context & Middleware](#context--middleware)
- [gRPC & Protobuf](#grpc--protobuf)
- [CGo Interop](#cgo-interop)
- [Build Tags & Modules](#build-tags--modules)
- [Wire Dependency Injection](#wire-dependency-injection)

---

## Advanced Error Handling

### Custom Error Types

```go
// Domain error with stack trace
type DomainError struct {
    Op      string  // Operation that failed
    Kind    Kind    // Category of error
    Err     error   // Wrapped error
    Stack   []byte  // Stack trace
}

func (e *DomainError) Error() string {
    return fmt.Sprintf("%s: %s: %v", e.Op, e.Kind, e.Err)
}

func (e *DomainError) Unwrap() error { return e.Err }

// Error kinds
type Kind int

const (
    KindNotFound Kind = iota
    KindValidation
    KindPermission
    KindInternal
)
```

### Error Wrapping Chain

```go
// Preserve context through call stack
func (s *Service) Process(ctx context.Context, id string) error {
    data, err := s.repo.Get(ctx, id)
    if err != nil {
        return &DomainError{
            Op:   "Service.Process",
            Kind: KindNotFound,
            Err:  err,
        }
    }
    return nil
}
```

---

## Concurrency Patterns

### Worker Pool

```go
func WorkerPool(ctx context.Context, jobs <-chan Job, workers int) <-chan Result {
    results := make(chan Result, workers)

    var wg sync.WaitGroup
    for i := 0; i < workers; i++ {
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
                    results <- process(job)
                }
            }
        }()
    }

    go func() {
        wg.Wait()
        close(results)
    }()

    return results
}
```

### Fan-Out/Fan-In

```go
func FanOut(ctx context.Context, input <-chan int, n int) []<-chan int {
    outputs := make([]<-chan int, n)
    for i := 0; i < n; i++ {
        outputs[i] = worker(ctx, input)
    }
    return outputs
}

func FanIn(ctx context.Context, inputs ...<-chan int) <-chan int {
    var wg sync.WaitGroup
    output := make(chan int)

    for _, in := range inputs {
        wg.Add(1)
        go func(ch <-chan int) {
            defer wg.Done()
            for v := range ch {
                select {
                case output <- v:
                case <-ctx.Done():
                    return
                }
            }
        }(in)
    }

    go func() {
        wg.Wait()
        close(output)
    }()

    return output
}
```

### Rate Limiter

```go
func NewRateLimiter(rate int, burst int) *rate.Limiter {
    return rate.NewLimiter(rate.Limit(rate), burst)
}

func (s *Service) RateLimitedCall(ctx context.Context) error {
    if err := s.limiter.Wait(ctx); err != nil {
        return err
    }
    return s.doCall(ctx)
}
```

---

## Performance Optimization

### Sync.Pool for Object Reuse

```go
var bufferPool = sync.Pool{
    New: func() interface{} {
        return new(bytes.Buffer)
    },
}

func Process(data []byte) []byte {
    buf := bufferPool.Get().(*bytes.Buffer)
    defer func() {
        buf.Reset()
        bufferPool.Put(buf)
    }()

    // Use buffer...
    return buf.Bytes()
}
```

### Efficient String Building

```go
// ❌ Slow: O(n²)
func slowConcat(strs []string) string {
    result := ""
    for _, s := range strs {
        result += s
    }
    return result
}

// ✅ Fast: O(n)
func fastConcat(strs []string) string {
    var sb strings.Builder
    for _, s := range strs {
        sb.WriteString(s)
    }
    return sb.String()
}
```

---

## Testing Strategies

### Table-Driven Tests

```go
func TestParser(t *testing.T) {
    tests := []struct {
        name    string
        input   string
        want    Result
        wantErr bool
    }{
        {"empty", "", Result{}, true},
        {"valid", "data", Result{Value: "data"}, false},
        {"special", "a b c", Result{Value: "a b c"}, false},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got, err := Parse(tt.input)
            if (err != nil) != tt.wantErr {
                t.Errorf("error = %v, wantErr %v", err, tt.wantErr)
                return
            }
            if !reflect.DeepEqual(got, tt.want) {
                t.Errorf("got = %v, want %v", got, tt.want)
            }
        })
    }
}
```

### Testing with Context

```go
func TestWithTimeout(t *testing.T) {
    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    defer cancel()

    result := make(chan int)
    go func() {
        result <- slowOperation()
    }()

    select {
    case <-ctx.Done():
        t.Fatal("test timed out")
    case r := <-result:
        if r != expected {
            t.Errorf("got %d, want %d", r, expected)
        }
    }
}
```

---

## Generics Patterns

### Type Constraints

```go
// Custom constraint combining interfaces
type Number interface {
    ~int | ~int32 | ~int64 | ~float32 | ~float64
}

type Ordered interface {
    Number | ~string
}

// Generic function with constraint
func Min[T Ordered](a, b T) T {
    if a < b {
        return a
    }
    return b
}

// Generic Map/Filter/Reduce
func Map[T, U any](slice []T, fn func(T) U) []U {
    result := make([]U, len(slice))
    for i, v := range slice {
        result[i] = fn(v)
    }
    return result
}

func Filter[T any](slice []T, fn func(T) bool) []T {
    var result []T
    for _, v := range slice {
        if fn(v) {
            result = append(result, v)
        }
    }
    return result
}
```

### Generic Data Structures

```go
// Thread-safe generic cache
type Cache[K comparable, V any] struct {
    mu    sync.RWMutex
    items map[K]V
    ttl   time.Duration
}

func NewCache[K comparable, V any](ttl time.Duration) *Cache[K, V] {
    return &Cache[K, V]{
        items: make(map[K]V),
        ttl:   ttl,
    }
}

func (c *Cache[K, V]) Get(key K) (V, bool) {
    c.mu.RLock()
    defer c.mu.RUnlock()
    v, ok := c.items[key]
    return v, ok
}

func (c *Cache[K, V]) Set(key K, value V) {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.items[key] = value
}
```

---

## Context & Middleware

### Context Value Pattern

```go
// Type-safe context keys (avoid collisions)
type ctxKey string

const (
    ctxUserID    ctxKey = "user_id"
    ctxRequestID ctxKey = "request_id"
    ctxTraceID   ctxKey = "trace_id"
)

func WithUserID(ctx context.Context, id string) context.Context {
    return context.WithValue(ctx, ctxUserID, id)
}

func UserIDFrom(ctx context.Context) (string, bool) {
    id, ok := ctx.Value(ctxUserID).(string)
    return id, ok
}
```

### HTTP Middleware Chain

```go
type Middleware func(http.Handler) http.Handler

// Chain middlewares in order
func Chain(middlewares ...Middleware) Middleware {
    return func(next http.Handler) http.Handler {
        for i := len(middlewares) - 1; i >= 0; i-- {
            next = middlewares[i](next)
        }
        return next
    }
}

// Request ID middleware
func RequestID() Middleware {
    return func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            id := r.Header.Get("X-Request-ID")
            if id == "" {
                id = uuid.NewString()
            }
            ctx := context.WithValue(r.Context(), ctxRequestID, id)
            w.Header().Set("X-Request-ID", id)
            next.ServeHTTP(w, r.WithContext(ctx))
        })
    }
}

// Usage
handler := Chain(RequestID(), Logger(), Auth())(router)
```

---

## gRPC & Protobuf

### Service Definition

```protobuf
// proto/user/v1/user.proto
syntax = "proto3";
package user.v1;
option go_package = "github.com/example/gen/user/v1";

service UserService {
  rpc GetUser(GetUserRequest) returns (GetUserResponse);
  rpc ListUsers(ListUsersRequest) returns (stream User);  // Server streaming
}

message GetUserRequest { string id = 1; }
message GetUserResponse { User user = 1; }
message User {
  string id = 1;
  string email = 2;
  string name = 3;
}
```

### Server Implementation

```go
type userServer struct {
    pb.UnimplementedUserServiceServer
    repo UserRepository
}

func (s *userServer) GetUser(ctx context.Context, req *pb.GetUserRequest) (*pb.GetUserResponse, error) {
    user, err := s.repo.FindByID(ctx, req.GetId())
    if err != nil {
        return nil, status.Errorf(codes.NotFound, "user %s not found", req.GetId())
    }
    return &pb.GetUserResponse{User: toProto(user)}, nil
}

// Unary interceptor (middleware)
func LoggingInterceptor(ctx context.Context, req any, info *grpc.UnaryServerInfo,
    handler grpc.UnaryHandler) (any, error) {
    start := time.Now()
    resp, err := handler(ctx, req)
    slog.Info("gRPC", "method", info.FullMethod, "duration", time.Since(start), "err", err)
    return resp, err
}
```

---

## CGo Interop

### Calling C from Go

```go
package main

/*
#include <stdlib.h>
#include <string.h>

typedef struct {
    int width;
    int height;
    unsigned char* data;
} Image;

Image* create_image(int w, int h) {
    Image* img = (Image*)malloc(sizeof(Image));
    img->width = w;
    img->height = h;
    img->data = (unsigned char*)calloc(w * h * 4, 1);
    return img;
}

void free_image(Image* img) {
    free(img->data);
    free(img);
}
*/
import "C"
import "unsafe"

func ProcessImage(width, height int) {
    img := C.create_image(C.int(width), C.int(height))
    defer C.free_image(img)

    // Access C struct fields
    data := C.GoBytes(unsafe.Pointer(img.data), C.int(img.width*img.height*4))
    _ = data // process...
}
```

### CGo Best Practices

```yaml
rules:
  - "ALWAYS defer C.free() for C-allocated memory"
  - "Use C.CString/C.GoString for string conversion"
  - "CGo calls have ~100ns overhead vs Go calls (~2ns)"
  - "Avoid CGo in hot loops — batch operations instead"
  - "Use //go:nosplit for performance-critical CGo bridges"
  - "Set CGO_ENABLED=0 for pure Go builds (no C deps)"
```

---

## Build Tags & Modules

### Conditional Compilation

```go
//go:build linux && amd64
// +build linux,amd64

package platform

// This file only compiles on linux/amd64
func optimizedSIMD(data []float64) float64 {
    // Use SIMD instructions via assembly
    return simdSum(data)
}
```

```go
//go:build !production

package config

// Debug helpers only in dev builds
func DumpConfig() {
    fmt.Printf("%+v\n", globalConfig)
}
```

### Go Workspace (Multi-Module)

```
// go.work
go 1.22

use (
    ./api
    ./pkg/shared
    ./internal/core
)
```

### Private Modules

```bash
# GOPRIVATE for private repos
export GOPRIVATE=github.com/myorg/*
export GONOSUMCHECK=github.com/myorg/*

# .netrc for auth
machine github.com login oauth2 password ${GITHUB_TOKEN}
```

---

## Wire Dependency Injection

### Provider Sets

```go
// wire.go
//go:build wireinject

package main

import "github.com/google/wire"

func InitializeApp(cfg Config) (*App, error) {
    wire.Build(
        NewDatabase,
        NewUserRepo,
        NewUserService,
        NewServer,
        wire.Struct(new(App), "*"),
    )
    return nil, nil
}

// Provider functions
func NewDatabase(cfg Config) (*sql.DB, func(), error) {
    db, err := sql.Open("postgres", cfg.DatabaseURL)
    if err != nil {
        return nil, nil, err
    }
    cleanup := func() { db.Close() }
    return db, cleanup, nil
}

func NewUserRepo(db *sql.DB) *UserRepo {
    return &UserRepo{db: db}
}
```

```bash
# Generate wire_gen.go
go install github.com/google/wire/cmd/wire@latest
wire ./...
```

---
