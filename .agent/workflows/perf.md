---
name: perf
trigger: ["/perf", "performance", "profiling", "hiệu năng"]
persona: developer
description: "⚡ Performance profiling: CPU, memory, benchmarks, and optimization recommendations"
---

# ⚡ /perf — Perf Pro v3.1

> Complete Performance Analysis & Optimization
> 📚 30+ Languages • CPU/Memory • Load Testing

---

## 🔄 PROFILING FLOW

```
User: /perf [command]
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 1: IDENTIFY                       │
│ ▸ Detect tech stack                     │
│ ▸ Find performance targets              │
│ ▸ Establish baseline                    │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 2: MEASURE                        │
│ ▸ Run profilers                         │
│ ▸ Collect metrics                       │
│ ▸ Generate flamegraphs                  │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 3: ANALYZE                        │
│ ▸ Identify hotspots                     │
│ ▸ Detect memory leaks                   │
│ ▸ Find N+1 queries                      │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 4: OPTIMIZE                       │
│ ▸ Apply fixes                           │
│ ⛔ STOP → Confirm before changes        │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 5: VERIFY                         │
│ ▸ Re-run benchmarks                     │
│ ▸ Compare before/after                  │
│ ▸ Validate improvements                 │
└─────────────────────────────────────────┘
```

---

## 🎯 COMMANDS

| Command           | Description      | Focus       |
| ----------------- | ---------------- | ----------- |
| `/perf`           | Quick analysis   | Overview    |
| `/perf cpu`       | CPU profiling    | Hotspots    |
| `/perf memory`    | Memory analysis  | Leaks       |
| `/perf benchmark` | Run benchmarks   | Throughput  |
| `/perf load`      | Load testing     | Scalability |
| `/perf trace`     | Tracing analysis | Latency     |
| `/perf web`       | Web vitals       | Frontend    |

---

## 🔥 CPU PROFILING

### Tools by Language:

```yaml
# ═══════════════════════════════════════════════════════════════
# CPU PROFILING TOOLS
# ═══════════════════════════════════════════════════════════════

cpu_profiling:
  go:
    builtin: pprof
    commands:
      profile: "go tool pprof -http=:8080 cpu.prof"
      collect: "go test -cpuprofile=cpu.prof -bench=."
    visualization: "go tool pprof -svg cpu.prof > cpu.svg"

  typescript:
    tools: [clinic.js, 0x, node --prof]
    commands:
      clinic: "npx clinic doctor -- node app.js"
      flame: "npx 0x app.js"
    visualization: "clinic flame -- node app.js"

  python:
    tools: [cProfile, py-spy, scalene]
    commands:
      cprofile: "python -m cProfile -o output.prof script.py"
      pyspy: "py-spy record -o profile.svg -- python script.py"
      scalene: "scalene script.py"
    recommended: scalene # CPU + memory + GPU

  rust:
    tools: [perf, flamegraph, cargo-profiler]
    commands:
      flamegraph: "cargo flamegraph --bin myapp"
      perf: "perf record --call-graph=dwarf target/release/myapp"

  java:
    tools: [JProfiler, YourKit, async-profiler]
    commands:
      async: "java -agentpath:libasyncProfiler.so=start,file=profile.jfr -jar app.jar"

  csharp:
    tools: [dotTrace, Visual Studio Profiler]
    commands:
      dotnet: "dotnet-trace collect --process-id {pid}"

  ruby:
    tools: [rbspy, stackprof]
    commands:
      rbspy: "rbspy record -- ruby script.rb"

  php:
    tools: [Xdebug, Blackfire]
    commands:
      xdebug: "php -dxdebug.mode=profile script.php"
```

### Hotspot Analysis:

```
🔥 CPU HOTSPOTS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Top CPU Consumers (sorted by self time):

| Function | Self % | Total % | Calls |
|----------|--------|---------|-------|
| json.Marshal | 32% | 35% | 50,000 |
| db.Query | 28% | 45% | 10,000 |
| regex.Match | 15% | 15% | 100,000 |
| http.Write | 10% | 12% | 50,000 |

Flamegraph: file://./cpu_profile.svg

Recommendations:
1. 🔴 Cache JSON encoding for repeated objects
2. 🔴 Add database query batching
3. 🟡 Pre-compile regex patterns
4. 🟢 Response streaming acceptable

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 🧠 MEMORY PROFILING

### Tools by Language:

```yaml
# ═══════════════════════════════════════════════════════════════
# MEMORY PROFILING TOOLS
# ═══════════════════════════════════════════════════════════════

memory_profiling:
  go:
    builtin: pprof
    commands:
      heap: "go tool pprof -http=:8080 mem.prof"
      collect: "go test -memprofile=mem.prof -bench=."
      allocs: "go tool pprof -alloc_space mem.prof"

  typescript:
    tools: [clinic.js, heapdump, memwatch]
    commands:
      heapsnapshot: "node --heapsnapshot-signal=SIGUSR2 app.js"
      clinic: "npx clinic heap -- node app.js"

  python:
    tools: [memory_profiler, pympler, tracemalloc]
    commands:
      tracemalloc: |
        import tracemalloc
        tracemalloc.start()
        # ... code ...
        snapshot = tracemalloc.take_snapshot()
      scalene: "scalene --memory script.py"

  rust:
    tools: [heaptrack, valgrind, dhat]
    commands:
      heaptrack: "heaptrack ./target/release/myapp"
      valgrind: "valgrind --tool=massif ./myapp"

  java:
    tools: [JProfiler, VisualVM, Eclipse MAT]
    commands:
      heap_dump: "jmap -dump:format=b,file=heap.hprof {pid}"

  csharp:
    tools: [dotMemory, Visual Studio Profiler]
    commands:
      dump: "dotnet-dump collect --process-id {pid}"
```

### Memory Leak Detection:

```
🧠 MEMORY ANALYSIS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Memory Usage:
├── Heap: 256 MB (limit: 512 MB)
├── Stack: 8 MB
├── RSS: 312 MB
└── GC Cycles: 45 (avg: 12ms)

Top Memory Consumers:
| Type | Count | Size | Growth |
|------|-------|------|--------|
| []byte | 50,000 | 128 MB | +5%/min ⚠️ |
| *User | 10,000 | 45 MB | stable |
| string | 25,000 | 32 MB | stable |
| map[string]any | 5,000 | 28 MB | +2%/min |

⚠️ POTENTIAL LEAK DETECTED:
└── []byte growing without bound
    └── Source: handler/upload.go:78
    └── Fix: Add buffer pool or limit

Recommendations:
1. 🔴 Implement sync.Pool for []byte buffers
2. 🔴 Add context timeout for uploads
3. 🟡 Consider streaming for large files

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 📊 BENCHMARKING

### Benchmark Tools by Language:

```yaml
# ═══════════════════════════════════════════════════════════════
# BENCHMARKING TOOLS
# ═══════════════════════════════════════════════════════════════

benchmarking:
  go:
    builtin: "go test -bench"
    commands:
      run: "go test -bench=. -benchmem ./..."
      compare: "benchstat old.txt new.txt"
    example: |
      func BenchmarkFoo(b *testing.B) {
        for i := 0; i < b.N; i++ {
          Foo()
        }
      }

  typescript:
    tools: [vitest bench, tinybench]
    commands:
      vitest: "npx vitest bench"
    example: |
      bench('foo', () => {
        foo();
      });

  python:
    tools: [pytest-benchmark, pyperf]
    commands:
      pytest: "pytest --benchmark-only"
    example: |
      def test_foo(benchmark):
        result = benchmark(foo)

  rust:
    tools: [criterion, divan]
    commands:
      criterion: "cargo bench"
    example: |
      #[bench]
      fn bench_foo(b: &mut Bencher) {
        b.iter(|| foo());
      }

  java:
    tool: JMH
    commands:
      run: "java -jar benchmarks.jar"
```

### Benchmark Results:

```
📊 BENCHMARK RESULTS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Benchmark: CreateUser

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| ops/sec | 5,000 | 12,000 | +140% ✅ |
| avg latency | 200μs | 83μs | -58% ✅ |
| p99 latency | 850μs | 150μs | -82% ✅ |
| allocs/op | 45 | 12 | -73% ✅ |
| B/op | 4,096 | 512 | -87% ✅ |

Comparison:
├── Baseline: commit abc123
├── Current: commit def456
└── Improvement: SIGNIFICANT

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 🏋️ LOAD TESTING

### Tools:

```yaml
# ═══════════════════════════════════════════════════════════════
# LOAD TESTING TOOLS
# ═══════════════════════════════════════════════════════════════

load_testing:
  k6:
    description: "Modern, developer-centric"
    install: "brew install k6"
    example: |
      import http from 'k6/http';
      export const options = {
        vus: 100,
        duration: '30s',
      };
      export default function () {
        http.get('http://localhost:3000/api/users');
      }
    run: "k6 run script.js"

  locust:
    description: "Python-based, distributed"
    install: "pip install locust"
    example: |
      from locust import HttpUser, task
      class WebUser(HttpUser):
        @task
        def get_users(self):
          self.client.get("/api/users")
    run: "locust -f locustfile.py"

  autocannon:
    description: "Node.js, fast"
    install: "npm install -g autocannon"
    run: "autocannon -c 100 -d 30 http://localhost:3000"

  wrk:
    description: "C-based, very fast"
    run: "wrk -t12 -c400 -d30s http://localhost:3000"

  vegeta:
    description: "Go-based, constant rate"
    run: "echo 'GET http://localhost:3000' | vegeta attack -rate=100 -duration=30s | vegeta report"

  artillery:
    description: "YAML config, cloud scaling"
    run: "artillery run scenario.yml --output report.json"
```

### Load Test Results:

```
🏋️ LOAD TEST RESULTS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Test: API Load Test
Duration: 5 minutes
VUs: 100 → 500 (ramp up)

Throughput:
├── Requests: 245,000
├── RPS (avg): 816/s
├── RPS (max): 1,250/s
└── RPS (min): 420/s

Latency:
├── avg: 45ms
├── p50: 32ms
├── p95: 120ms
├── p99: 350ms
└── max: 2,100ms

Errors:
├── Total: 245 (0.1%)
├── 5xx: 120
├── Timeout: 125
└── Connection: 0

Resource Usage (peak):
├── CPU: 78%
├── Memory: 456 MB
├── Connections: 500
└── DB Connections: 25/50

Bottlenecks Identified:
1. 🔴 DB connection pool saturated at 450 VUs
2. 🟡 p99 latency spikes above 200ms
3. 🟡 Memory grows linearly with VUs

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 🌐 WEB PERFORMANCE

### Frontend Metrics:

```yaml
# ═══════════════════════════════════════════════════════════════
# CORE WEB VITALS (2025)
# ═══════════════════════════════════════════════════════════════

web_vitals:
  lcp:
    name: "Largest Contentful Paint"
    target: "< 2.5s"
    tools: [Lighthouse, WebPageTest]

  inp:
    name: "Interaction to Next Paint"
    target: "< 200ms"
    note: "Replaced FID in 2024"

  cls:
    name: "Cumulative Layout Shift"
    target: "< 0.1"

  ttfb:
    name: "Time to First Byte"
    target: "< 800ms"

tools:
  lighthouse:
    run: "npx lighthouse https://example.com --output=json"

  pagespeed:
    url: "https://pagespeed.web.dev/"

  webpagetest:
    url: "https://www.webpagetest.org/"
```

---

## 📈 PERFORMANCE TARGETS

```yaml
targets:
  api:
    response_time:
      p50: "< 50ms"
      p95: "< 200ms"
      p99: "< 500ms"
    throughput: "> 1000 RPS"
    error_rate: "< 0.1%"

  web:
    lcp: "< 2.5s"
    inp: "< 200ms"
    cls: "< 0.1"
    bundle_size: "< 200KB gzip"

  resources:
    cpu: "< 70%"
    memory: "< 80%"
    db_connections: "< 80% pool"
```

---

## 📊 PERFORMANCE REPORT

```
⚡ PERFORMANCE REPORT

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Project: my-api
Stack: Go + Gin + PostgreSQL
Date: 2026-01-31

Overall Score: 7.5/10 (Good)

| Category | Score | Status |
|----------|-------|--------|
| Throughput | 8/10 | ✅ |
| Latency | 7/10 | ⚠️ |
| Memory | 6/10 | ⚠️ |
| CPU | 9/10 | ✅ |

Top Issues:
1. 🔴 Memory growing under load (potential leak)
2. 🟡 P99 latency above target
3. 🟡 N+1 query in GetUserOrders

Recommendations:
- [ ] Implement connection pooling
- [ ] Add database query caching
- [ ] Profile memory allocation
- [ ] Add response compression

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 NEXT STEPS:
1️⃣ Fix memory leak
2️⃣ Optimize N+1 queries
3️⃣ Re-run benchmarks
4️⃣ Deploy improvements
```

---

## 🤖 AGENT PERFORMANCE KPIS

```yaml
agent_kpis:
  description: "Metrics specific to AI agents"

  core_metrics:
    accuracy: "Task completion correctness %"
    latency_p50: "Median response time"
    latency_p99: "99th percentile response"
    throughput: "Tasks completed per hour"
    token_efficiency: "Quality per token spent"
    context_usage: "Context window utilization %"

  thresholds:
    accuracy: ">= 95%"
    latency_p99: "< 5s for simple, < 30s for complex"
    context_usage: "< 80% (leave headroom)"

  command: "/perf agent [session_id]"
```

---

## 🧠 MEMORY OPTIMIZATION

```yaml
memory_optimization:
  strategies:
    dynamic_allocation:
      description: "Adjust based on task complexity"
      trigger: "Task type detection"

    strategic_forgetting:
      description: "Prune irrelevant context"
      method: "Score memories by relevance"
      threshold: "Remove if score < 0.3"

    smart_filtering:
      description: "Prioritize what to keep"
      focus: ["Recent", "Referenced", "Decision-critical"]

    vector_offload:
      description: "Store in external memory"
      use_case: "Long-term project context"

  commands:
    analyze: "/perf memory analyze"
    optimize: "/perf memory optimize"
    stats: "/perf memory stats"
```

---

## ⚡ CPU-AWARE SCHEDULING

```yaml
cpu_optimization:
  patterns:
    micro_batching:
      name: "CGAM - CPU/GPU Aware Micro-batching"
      benefit: "Up to 2.1x latency improvement"

    concurrency_limit:
      default: 3
      max: 5
      reason: "Avoid rate limits, diminishing returns"

    cache_aggressive:
      description: "Deduplicate retrieval calls"
      benefit: "Reduce redundant API calls"

  anti_patterns:
    - "Unbounded parallelism"
    - "Sync operations in hot path"
    - "Core over-subscription"
    - "No timeout boundaries"
```

---

## ⚙️ TOKEN OPTIMIZATION

```yaml
token_saving:
  # Quick analysis first
  - Run only essential profilers
  - Focus on top 3 hotspots

  # Batch recommendations
  - Group similar issues
  - Single optimization pass
```

---

_DOMYH Awesome Code v6.1.2 • Perf Pro v3.1 • Agent-Aware Profiling_
