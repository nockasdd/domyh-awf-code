---
description: "⚡ Performance profiling: CPU, memory, benchmarks, and optimization recommendations"
skills: { required: [], contextual: [auto] }
---

# ⚡ /perf — Perf Pro

> 4-Pillar Performance: CPU, Memory, Benchmarks, Load Testing
> 📚 Multi-language • Flamegraphs • Web Vitals

---

## PERF FLOW

1. **BASELINE** — Detect stack via HSA (`hsa_detect_stack`), load perf context (`hsa_get_context`), collect current metrics
2. **PROFILE** — CPU/memory profiling, flamegraphs
3. **ANALYZE** — Identify hotspots, bottlenecks
4. **OPTIMIZE** — Apply fixes, verify improvement
5. **REPORT** — Before/after comparison

---

## COMMANDS

| Command        | Description      | Focus       |
| -------------- | ---------------- | ----------- |
| `/perf`        | Quick analysis   | Overview    |
| `/perf cpu`    | CPU profiling    | Hotspots    |
| `/perf memory` | Memory profiling | Leaks       |
| `/perf bench`  | Benchmarking     | Throughput  |
| `/perf load`   | Load testing     | Scalability |
| `/perf web`    | Web performance  | Core Vitals |

---

## 🔥 CPU PROFILING TOOLS

| Language   | Tool                    | Profile Command                            | Visualize                            |
| ---------- | ----------------------- | ------------------------------------------ | ------------------------------------ |
| Go         | pprof (stdlib)          | `go test -cpuprofile=cpu.prof -bench=.`    | `go tool pprof -http=:8080 cpu.prof` |
| TypeScript | Chrome DevTools         | `node --prof app.js`                       | DevTools → Performance               |
| Python     | cProfile                | `python -m cProfile -o cpu.prof script.py` | `snakeviz cpu.prof`                  |
| Rust       | perf/flamegraph         | `cargo flamegraph`                         | SVG output                           |
| Java       | async-profiler          | `profiler.sh -d 30 -f cpu.html PID`        | HTML flamegraph                      |
| C#         | dotTrace / dotnet-trace | `dotnet-trace collect -p PID`              | `speedscope`                         |
| Ruby       | rbspy                   | `rbspy record -- ruby script.rb`           | SVG flamegraph                       |
| PHP        | Xdebug / Blackfire      | `php -dxdebug.mode=profile script.php`     | Blackfire UI                         |

---

## 🧠 MEMORY PROFILING TOOLS

| Language   | Tool        | Heap Command                                  | Leak Detection                        |
| ---------- | ----------- | --------------------------------------------- | ------------------------------------- |
| Go         | pprof       | `go test -memprofile=mem.prof -bench=.`       | `go tool pprof -alloc_space mem.prof` |
| TypeScript | heapdump    | `node --inspect` → Chrome DevTools            | Heap snapshots comparison             |
| Python     | tracemalloc | `tracemalloc.start()` in code                 | `tracemalloc.get_traced_memory()`     |
| Rust       | valgrind    | `valgrind --tool=massif ./target/release/app` | `ms_print massif.out`                 |
| Java       | VisualVM    | `jmap -heap PID`                              | MAT analyzer                          |
| C#         | dotMemory   | `dotnet-dump collect -p PID`                  | `dotnet-dump analyze`                 |

---

## 📊 BENCHMARKING TOOLS

| Language   | Tool             | Run Command                                  | Compare                     |
| ---------- | ---------------- | -------------------------------------------- | --------------------------- |
| Go         | go test -bench   | `go test -bench=. -benchmem ./...`           | `benchstat old.txt new.txt` |
| TypeScript | Vitest bench     | `vitest bench` or Benchmark.js               | Manual comparison           |
| Python     | pytest-benchmark | `pytest --benchmark-only`                    | `pytest-benchmark compare`  |
| Rust       | criterion        | `cargo bench`                                | Built-in comparison         |
| Java       | JMH              | `mvn exec:java -Dexec.mainClass="benchmark"` | JMH output                  |

---

## 🏋️ LOAD TESTING

| Tool          | Type             | Quick Start                |
| ------------- | ---------------- | -------------------------- |
| **k6**        | Modern, scripted | `k6 run script.js`         |
| **wrk**       | HTTP benchmark   | `wrk -t12 -c400 -d30s URL` |
| **Artillery** | YAML config      | `artillery run config.yml` |
| **Locust**    | Python-based     | `locust -f locustfile.py`  |

---

## 🌐 WEB PERFORMANCE (Core Web Vitals 2025)

| Metric                              | Target  | Tools                   |
| ----------------------------------- | ------- | ----------------------- |
| **LCP** (Largest Contentful Paint)  | < 2.5s  | Lighthouse, WebPageTest |
| **INP** (Interaction to Next Paint) | < 200ms | Chrome DevTools         |
| **CLS** (Cumulative Layout Shift)   | < 0.1   | Lighthouse              |
| **TTFB** (Time to First Byte)       | < 800ms | WebPageTest             |
| **FCP** (First Contentful Paint)    | < 1.8s  | Lighthouse              |

### Optimization Checklist

| Category | Technique                           |
| -------- | ----------------------------------- |
| Images   | WebP/AVIF, responsive, lazy load    |
| JS       | Code splitting, tree shaking, defer |
| CSS      | Critical CSS inline, purge unused   |
| Fonts    | `font-display: swap`, preload       |
| Caching  | CDN, `Cache-Control`, ETags         |
| Network  | HTTP/3, preconnect, resource hints  |
