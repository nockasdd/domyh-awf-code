---
name: logging
version: "6.3.9"
category: core
---

# 📝 Logging Best Practices Skill

> Comprehensive logging patterns for 12+ languages with HSA integration

---

## Overview

| Metric          | Value |
| --------------- | ----- |
| **Patterns**    | 300+  |
| **Languages**   | 12    |
| **Data Files**  | 13    |
| **HSA Domains** | 4     |

---

## Language Coverage

### Backend / Systems

| Language | Libraries              | Key Patterns                        |
| -------- | ---------------------- | ----------------------------------- |
| **Go**   | slog, zap, zerolog     | Structured logging, JSON handlers   |
| **Rust** | tracing, log           | Spans, events, subscribers          |
| **Java** | SLF4J, Log4j2, Logback | Facades, MDC, async appenders       |
| **C#**   | ILogger, Serilog, NLog | Sinks, enrichers, message templates |
| **C++**  | spdlog, glog           | High-performance, async logging     |

### Scripting / Dynamic

| Language       | Libraries                  | Key Patterns               |
| -------------- | -------------------------- | -------------------------- |
| **Python**     | logging, structlog, loguru | Processors, JSON, rotation |
| **TypeScript** | Winston, Pino              | Transports, child loggers  |
| **PHP**        | Monolog, PSR-3             | Handlers, formatters       |
| **Ruby**       | Logger, Semantic Logger    | Tagged logging             |

### Mobile

| Language   | Libraries              | Key Patterns             |
| ---------- | ---------------------- | ------------------------ |
| **Swift**  | OSLog, Logger          | Unified logging, privacy |
| **Kotlin** | kotlin-logging, Timber | Android logging, tags    |

### Functional

| Language   | Libraries         | Key Patterns       |
| ---------- | ----------------- | ------------------ |
| **Elixir** | Logger, Telemetry | Metadata, backends |

---

## Core Patterns

### Log Levels

```
TRACE → DEBUG → INFO → WARN → ERROR → FATAL
```

| Level | When to Use                               |
| ----- | ----------------------------------------- |
| TRACE | Very detailed debugging (loop iterations) |
| DEBUG | Debugging information (variable values)   |
| INFO  | General system events (startup, config)   |
| WARN  | Potential issues (deprecated, retries)    |
| ERROR | Errors that need attention                |
| FATAL | Critical failures, system shutdown        |

### Structured Logging

```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "INFO",
  "message": "User login successful",
  "user_id": "12345",
  "ip": "192.168.1.1",
  "duration_ms": 45,
  "trace_id": "abc123"
}
```

### Correlation IDs

```
trace_id: Links all logs for a request
span_id: Links logs within operation
request_id: HTTP request identifier
```

---

## HSA Integration

Data powered by HSA BM25 search engine. Example queries:

| Domain      | Query Examples                  |
| ----------- | ------------------------------- |
| Language    | "Go slog structured logging"    |
| Language    | "Python structlog processors"   |
| Aggregation | "ELK stack log pipeline"        |
| OTel        | "OpenTelemetry log correlation" |

---

## Data Files

| File                        | Patterns | Description                |
| --------------------------- | -------- | -------------------------- |
| `core-patterns.yaml`        | 30       | Fundamentals, log levels   |
| `language-go.yaml`          | 25       | slog, zap, zerolog         |
| `language-python.yaml`      | 25       | logging, structlog, loguru |
| `language-typescript.yaml`  | 25       | Winston, Pino              |
| `language-rust.yaml`        | 25       | tracing, subscribers       |
| `language-java.yaml`        | 25       | SLF4J, Log4j2, MDC         |
| `language-csharp.yaml`      | 25       | Serilog, NLog              |
| `language-swift.yaml`       | 20       | OSLog, unified logging     |
| `language-kotlin.yaml`      | 20       | kotlin-logging, Timber     |
| `language-others.yaml`      | 25       | PHP, Ruby, C++, Elixir     |
| `aggregation-patterns.yaml` | 25       | ELK, Loki, Splunk          |
| `otel-logging.yaml`         | 20       | OpenTelemetry logs         |
| `anti-patterns.yaml`        | 15       | Common mistakes            |

**Total: 305 patterns**

---

## Quick Reference

### Go (slog)

```go
logger := slog.New(slog.NewJSONHandler(os.Stdout, nil))
logger.Info("user login",
    slog.String("user_id", "123"),
    slog.Int("attempt", 1))
```

### Python (structlog)

```python
import structlog
log = structlog.get_logger()
log.info("user_login", user_id="123", attempt=1)
```

### TypeScript (Pino)

```typescript
import pino from "pino";
const logger = pino();
logger.info({ userId: "123", attempt: 1 }, "user login");
```

### Rust (tracing)

```rust
use tracing::{info, instrument};

#[instrument]
fn login(user_id: &str) {
    info!(user_id, "user login");
}
```

---

_DOMYH Awesome Code • Logging Skill v1.0 • 305 Patterns_
