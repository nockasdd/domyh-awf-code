---
name: observability
version: "6.4.2"
category: core
---

# 🔭 Observability Skill v1.0

> **400+ Patterns** | **12 Languages** | **OpenTelemetry Standard**

---

## Quick Stats

| Metric      | Value                |
| ----------- | -------------------- |
| Patterns    | 400+                 |
| Languages   | 12                   |
| Categories  | 8                    |
| HSA Adapter | ✅ BM25 skill search |

---

## Three Pillars + Profiling

| Pillar        | Purpose                      | Tools                          |
| ------------- | ---------------------------- | ------------------------------ |
| **Metrics**   | Numerical trends, alerts     | Prometheus, Micrometer, StatsD |
| **Tracing**   | Request flow                 | OpenTelemetry, Jaeger, Zipkin  |
| **Logs**      | Events (see `logging` skill) | -                              |
| **Profiling** | CPU/Memory hotspots          | pprof, Valgrind, Tracy         |

---

## Language Coverage

| Language   | Libraries                         | Patterns |
| ---------- | --------------------------------- | -------- |
| Go         | otel-go, pprof, prometheus-go     | 25       |
| Python     | otel-python, prometheus_client    | 25       |
| TypeScript | otel-js, prom-client, dd-trace    | 25       |
| Rust       | tracing, opentelemetry-rust       | 25       |
| Java       | Micrometer, Spring Actuator       | 25       |
| C#         | DiagnosticSource, AppInsights     | 25       |
| C++        | prometheus-cpp, Tracy, Valgrind   | 25       |
| Swift      | MetricKit, otel-swift             | 15       |
| Kotlin     | Firebase Performance, otel-kotlin | 15       |
| Others     | PHP, Ruby, Elixir                 | 15       |

---

## Core Patterns

### OpenTelemetry

```yaml
otel-core:
  - SDK initialization
  - TracerProvider setup
  - MeterProvider setup
  - OTLP exporter configuration
  - Context propagation
  - Semantic conventions
  - Auto-instrumentation
  - Manual instrumentation
```

### Metrics (RED/USE Methods)

```yaml
metrics-patterns:
  RED: # Request-oriented
    - Rate (requests/sec)
    - Errors (rate)
    - Duration (latency)
  USE: # Resource-oriented
    - Utilization (%)
    - Saturation (queue depth)
    - Errors (count)
```

### Tracing

```yaml
tracing-patterns:
  - Span creation
  - Context propagation
  - Sampling strategies (head/tail)
  - Baggage items
  - Error recording
  - Span links
```

### Alerting

```yaml
alerting-patterns:
  - SLO-based alerts
  - Multi-window burn rate
  - Error budget policies
  - On-call best practices
  - Alert fatigue prevention
```

---

## HSA Integration

Data powered by HSA BM25 search engine:

| Domain    | Query Examples                           |
| --------- | ---------------------------------------- |
| Metrics   | "prometheus go RED method"               |
| Tracing   | "OpenTelemetry span context propagation" |
| Core      | "otel SDK initialization exporter"       |
| Profiling | "pprof CPU memory Go"                    |
| Alerting  | "SLO burn rate multi-window"             |

---

## Data Files (16 YAMLs)

| Category  | File                    | Patterns |
| --------- | ----------------------- | -------- |
| Core      | core-patterns.yaml      | 30       |
| Core      | otel-core.yaml          | 30       |
| Metrics   | metrics-prometheus.yaml | 25       |
| Metrics   | metrics-patterns.yaml   | 20       |
| Tracing   | tracing-patterns.yaml   | 25       |
| Tracing   | tracing-tools.yaml      | 20       |
| Profiling | profiling-patterns.yaml | 20       |
| Alerting  | alerting-patterns.yaml  | 25       |
| Languages | language-\*.yaml        | 220      |
| Anti      | anti-patterns.yaml      | 15       |
| **Total** | -                       | **~400** |

---

## Anti-Patterns

| Anti-Pattern            | Why Bad          | Fix                    |
| ----------------------- | ---------------- | ---------------------- |
| High cardinality labels | Memory explosion | Bound label values     |
| Too many dashboards     | Alert fatigue    | SLO-focused dashboards |
| Metrics without alerts  | Invisible issues | Define thresholds      |
| Traces without context  | Hard debugging   | Add correlation IDs    |

---

_DOMYH Awesome Code • Observability • OpenTelemetry Standard_
