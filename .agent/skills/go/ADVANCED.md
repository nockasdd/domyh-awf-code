# Go — Advanced Patterns

# DOMYH Agent v4.2 — Tier 3 Reference

# Load only when explicitly referenced

## Table of Contents

- [Advanced Error Handling](#advanced-error-handling)
- [Concurrency Patterns](#concurrency-patterns)
- [Performance Optimization](#performance-optimization)
- [Testing Strategies](#testing-strategies)

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

_DOMYH Agent v4.2 — Tier 3 Reference_
