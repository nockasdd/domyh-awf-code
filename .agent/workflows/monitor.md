---
description: "📡 Setup observability: logging, tracing, metrics, and alerting configuration"
skills: { required: [observability, logging], contextual: [auto] }
success_criteria: "logs/traces/metrics configured, data verified in backends, alerts set"
---

# 📡 /monitor — Monitor Pro

> 3-Pillar Observability: Logs, Traces, Metrics
> 📚 OpenTelemetry • Prometheus • Grafana • Multi-language

---

## MONITOR FLOW

1. **DETECT** (Auto) — `hsa_session("setup observability")`, detect stack via HSA (`hsa_detect`), load obs context (`hsa_search`), check existing observability, identify gaps
2. **PLAN** — Recommend libraries & backends, setup OpenTelemetry → ⛔ STOP: confirm before install
3. **EXECUTE** — Add logging, tracing (OpenTelemetry), metrics (Prometheus), configure alerts
4. **VERIFY** — Verify data in backends, test alerts
5. **SYNC** — `hsa_check_changes` to update index after observability config changes

---

## COMMANDS

| Command              | Description      | Focus         |
| -------------------- | ---------------- | ------------- |
| `/monitor`           | Full setup guide | All pillars   |
| `/monitor logs`      | Logging setup    | Pillar 1      |
| `/monitor traces`    | Tracing setup    | Pillar 2      |
| `/monitor metrics`   | Metrics setup    | Pillar 3      |
| `/monitor alerts`    | Alerting config  | Operations    |
| `/monitor dashboard` | Dashboard setup  | Visualization |

---

## 📊 3 PILLARS OF OBSERVABILITY

| Pillar         | Purpose       | Data Type              | Key Tools             |
| -------------- | ------------- | ---------------------- | --------------------- |
| 📝 **Logs**    | What happened | Structured JSON events | slog, zap, winston    |
| 🔍 **Traces**  | Request flow  | Spans & context        | OpenTelemetry, Jaeger |
| 📈 **Metrics** | System health | Time-series numbers    | Prometheus, Grafana   |

---

## 📝 PILLAR 1: STRUCTURED LOGGING

| Language   | Library               | Install                                 |
| ---------- | --------------------- | --------------------------------------- |
| Go         | `slog` (stdlib 1.21+) | built-in                                |
| Python     | `structlog`           | `pip install structlog`                 |
| TypeScript | `pino`                | `npm i pino`                            |
| Rust       | `tracing`             | `cargo add tracing tracing-subscriber`  |
| Java       | `SLF4J + Logback`     | Maven/Gradle                            |
| C#         | `Serilog`             | `dotnet add package Serilog.AspNetCore` |
| PHP        | `Monolog`             | `composer require monolog/monolog`      |
| Ruby       | `Semantic Logger`     | `gem install semantic_logger`           |

### Best Practices

| Category    | Guidelines                                                        |
| ----------- | ----------------------------------------------------------------- |
| Structure   | JSON format, consistent fields, correlation IDs                   |
| Levels      | `ERROR`: failures, `WARN`: degraded, `INFO`: events, `DEBUG`: dev |
| Security    | Mask PII (email, phone, SSN), no passwords                        |
| Performance | Async logging, sample repetitive, log rotation                    |

---

## 🔍 PILLAR 2: DISTRIBUTED TRACING

### OpenTelemetry Setup

| Language   | Install Command                                                   |
| ---------- | ----------------------------------------------------------------- |
| Go         | `go get go.opentelemetry.io/otel`                                 |
| Python     | `pip install opentelemetry-api opentelemetry-sdk`                 |
| Java       | `opentelemetry-javaagent.jar` (auto-instrument)                   |
| TypeScript | `npm i @opentelemetry/sdk-node`                                   |
| Rust       | `cargo add opentelemetry opentelemetry-otlp`                      |
| C#         | `dotnet add package OpenTelemetry.Exporter.OpenTelemetryProtocol` |

### Tracing Backends

| Backend    | Type           | Docker Quick Start                                                |
| ---------- | -------------- | ----------------------------------------------------------------- |
| **Jaeger** | All-in-one OSS | `docker run -p 16686:16686 -p 4317:4317 jaegertracing/all-in-one` |
| **Tempo**  | Grafana native | `docker-compose` with Grafana                                     |
| **Zipkin** | Lightweight    | `docker run -p 9411:9411 openzipkin/zipkin`                       |

> 💡 **Recommended**: Use **OpenTelemetry Collector** as a unified pipeline for logs, traces, and metrics. Supports batching, filtering, enrichment, and multi-backend routing.

---

## 📈 PILLAR 3: METRICS

### Prometheus Setup

| Language   | Library                    | Key Metrics                                    |
| ---------- | -------------------------- | ---------------------------------------------- |
| Go         | `prometheus/client_golang` | `http_requests_total`, `http_duration_seconds` |
| Python     | `prometheus_client`        | `requests_total`, `request_latency`            |
| TypeScript | `prom-client`              | `http_request_duration_seconds`                |
| Java       | `micrometer`               | Spring Boot auto-metrics                       |
| Rust       | `metrics-rs`               | Custom counters, histograms                    |
| C#         | `prometheus-net`           | ASP.NET Core metrics                           |

### RED + USE Methods

| Method  | Metrics                         | Use For        |
| ------- | ------------------------------- | -------------- |
| **RED** | Rate, Errors, Duration          | Services, APIs |
| **USE** | Utilization, Saturation, Errors | Infrastructure |

---

## 🚨 ALERTING

### Alert Priority

| Level | Response Time | Example                   |
| ----- | ------------- | ------------------------- |
| P1    | < 5 min       | Service down, data loss   |
| P2    | < 30 min      | High error rate, degraded |
| P3    | < 4 hours     | Performance degradation   |
| P4    | Next day      | Warning thresholds        |

### Recommended Thresholds

| Metric              | Warning | Critical |
| ------------------- | ------- | -------- |
| Error rate          | > 1%    | > 5%     |
| Response time (p95) | > 500ms | > 2s     |
| CPU usage           | > 70%   | > 90%    |
| Memory usage        | > 80%   | > 95%    |
| Disk usage          | > 75%   | > 90%    |
---

## REFLECTION CHECKPOINT

⛔ **MANDATORY** — Execute before completing this workflow (SESSION_005):

1. **VERIFY** — Does output meet success_criteria (see YAML frontmatter)?
2. **PERSIST** (if HSA available — preferred, 1 tool call):
   - `hsa_session({action:'persist', task_summary:'[workflow] [summary]', files_touched:[...]})`
   - If key decision → `hsa_session({action:'anchor', content:'[decision]', category:'decision'})`
3. **PERSIST** (if HSA unavailable — manual fallback):
   - Append task summary to `memory/session.md`
   - If last task → Update `memory/CONTEXT_SNAPSHOT.md`

