---
name: monitor
trigger: ["/monitor", "observability", "logging", "giám sát"]
persona: developer
description: "📡 Setup observability: logging, tracing, metrics, and alerting configuration"
---

# 📡 /monitor — Observability Pro v3.0

> Complete Observability Stack Setup
> 📚 30+ Languages • OpenTelemetry • 3 Pillars

---

## 🔄 SETUP FLOW

```
User: /monitor [command]
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 1: DETECT (Auto)                 │
│ ▸ Detect project stack                  │
│ ▸ Check existing observability          │
│ ▸ Identify gaps                         │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 2: CONFIGURE                      │
│ ▸ Select tools per pillar               │
│ ▸ Setup OpenTelemetry                   │
│ ⛔ STOP → Confirm before install        │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 3: INSTRUMENT                     │
│ ▸ Add logging library                   │
│ ▸ Add tracing SDK                       │
│ ▸ Add metrics exporter                  │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 4: DEPLOY                         │
│ ▸ Start collectors                      │
│ ▸ Configure dashboards                  │
│ ▸ Setup alerting                        │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 5: VERIFY                         │
│ ▸ Send test telemetry                   │
│ ▸ Verify data in backends               │
│ ▸ Test alerts                           │
└─────────────────────────────────────────┘
```

---

## 🎯 COMMANDS

| Command              | Description      | Focus               |
| -------------------- | ---------------- | ------------------- |
| `/monitor`           | Full setup guide | All pillars         |
| `/monitor logs`      | Logging setup    | Structured logging  |
| `/monitor trace`     | Tracing setup    | Distributed tracing |
| `/monitor metrics`   | Metrics setup    | Prometheus/OTEL     |
| `/monitor alerts`    | Alerting setup   | Alert rules         |
| `/monitor dashboard` | Dashboard setup  | Grafana             |

---

## 📊 THREE PILLARS OF OBSERVABILITY

```
┌─────────────────────────────────────────────────────────────┐
│                    OBSERVABILITY                            │
├───────────────────┬───────────────────┬─────────────────────┤
│      LOGS         │     TRACES        │      METRICS        │
│   (What happened) │ (Request flow)    │  (System health)    │
├───────────────────┼───────────────────┼─────────────────────┤
│ • Structured JSON │ • Spans & Context │ • Time-series data  │
│ • Log levels      │ • Trace IDs       │ • Counters/Gauges   │
│ • Context-rich    │ • Service maps    │ • Histograms        │
└───────────────────┴───────────────────┴─────────────────────┘
                           │
                           ▼
              ┌─────────────────────────┐
              │    OpenTelemetry        │
              │   (Unified Standard)    │
              └─────────────────────────┘
```

---

## 📋 PHASE 1: DETECT

### Current State Report:

```
📡 OBSERVABILITY STATUS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Stack: Go + Gin + PostgreSQL

Pillar Analysis:
├── Logs: ⚠️ Basic (fmt.Println)
├── Traces: ❌ Not configured
├── Metrics: ❌ Not configured
└── Alerts: ❌ Not configured

Recommendations:
1. Replace fmt with structured logging (slog/zap)
2. Add OpenTelemetry SDK for tracing
3. Expose Prometheus metrics
4. Configure Grafana + AlertManager

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 📝 PILLAR 1: LOGGING

### Library by Language:

```yaml
# ═══════════════════════════════════════════════════════════════
# STRUCTURED LOGGING LIBRARIES (2025)
# ═══════════════════════════════════════════════════════════════

logging:
  go:
    recommended: slog # stdlib, Go 1.21+
    alternatives: [zap, zerolog]
    install: "# built-in"
    example: |
      logger := slog.New(slog.NewJSONHandler(os.Stdout, nil))
      logger.Info("request processed",
        slog.String("trace_id", traceID),
        slog.Int("status", 200),
      )

  typescript:
    recommended: pino
    alternatives: [winston, bunyan]
    install: "npm install pino pino-pretty"
    example: |
      import pino from 'pino';
      const logger = pino({ level: 'info' });
      logger.info({ traceId, userId }, 'request processed');

  python:
    recommended: structlog
    alternatives: [loguru, python-json-logger]
    install: "pip install structlog"
    example: |
      import structlog
      logger = structlog.get_logger()
      logger.info("request processed", trace_id=trace_id, status=200)

  java:
    recommended: logback + slf4j
    alternatives: [log4j2]
    install: "maven: ch.qos.logback:logback-classic"

  kotlin:
    recommended: kotlin-logging
    alternatives: [slf4j]
    install: "gradle: io.github.oshai:kotlin-logging"

  rust:
    recommended: tracing
    alternatives: [log, env_logger]
    install: "cargo add tracing tracing-subscriber"

  csharp:
    recommended: Serilog
    alternatives: [NLog, Microsoft.Extensions.Logging]
    install: "dotnet add package Serilog.AspNetCore"

  php:
    recommended: Monolog
    install: "composer require monolog/monolog"

  ruby:
    recommended: Semantic Logger
    alternatives: [rails logger, lograge]
```

### Log Best Practices:

```yaml
best_practices:
  # ═══════════════════════════════════════════════════════════════
  # STRUCTURE
  # ═══════════════════════════════════════════════════════════════

  format:
    - Use JSON format (machine-readable)
    - Include timestamp (ISO 8601)
    - Include log level (DEBUG/INFO/WARN/ERROR)
    - Include trace_id for correlation

  context:
    - request_id
    - user_id
    - service_name
    - version
    - environment

  # ═══════════════════════════════════════════════════════════════
  # SECURITY
  # ═══════════════════════════════════════════════════════════════

  sensitive_data:
    never_log:
      - passwords
      - tokens
      - credit_cards
      - PII
    mask_fields: [email, phone, ssn]

  # ═══════════════════════════════════════════════════════════════
  # PERFORMANCE
  # ═══════════════════════════════════════════════════════════════

  performance:
    - Use async logging
    - Sample repetitive logs
    - Set appropriate log levels
    - Implement log rotation
```

---

## 🔍 PILLAR 2: DISTRIBUTED TRACING

### OpenTelemetry Setup by Language:

```yaml
# ═══════════════════════════════════════════════════════════════
# OPENTELEMETRY SDK SETUP
# ═══════════════════════════════════════════════════════════════

tracing:
  go:
    install: |
      go get go.opentelemetry.io/otel
      go get go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc
    setup: |
      exporter, _ := otlptracegrpc.New(ctx)
      tp := trace.NewTracerProvider(
        trace.WithBatcher(exporter),
        trace.WithResource(resource.NewWithAttributes(
          semconv.ServiceNameKey.String("my-service"),
        )),
      )
      otel.SetTracerProvider(tp)

  typescript:
    install: |
      npm install @opentelemetry/sdk-node @opentelemetry/auto-instrumentations-node
    setup: |
      const sdk = new NodeSDK({
        serviceName: 'my-service',
        traceExporter: new OTLPTraceExporter(),
        instrumentations: [getNodeAutoInstrumentations()],
      });
      sdk.start();

  python:
    install: |
      pip install opentelemetry-sdk opentelemetry-exporter-otlp
    setup: |
      from opentelemetry import trace
      from opentelemetry.sdk.trace import TracerProvider
      from opentelemetry.sdk.trace.export import BatchSpanProcessor
      from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

      provider = TracerProvider()
      provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
      trace.set_tracer_provider(provider)

  java:
    install: "opentelemetry-javaagent.jar"
    setup: |
      java -javaagent:opentelemetry-javaagent.jar \
        -Dotel.service.name=my-service \
        -Dotel.exporter.otlp.endpoint=http://localhost:4317 \
        -jar myapp.jar

  rust:
    install: |
      cargo add opentelemetry opentelemetry-otlp tracing-opentelemetry

  csharp:
    install: "dotnet add package OpenTelemetry.Exporter.OpenTelemetryProtocol"
```

### Tracing Backends:

```yaml
backends:
  jaeger:
    description: "Open source, all-in-one"
    setup: "docker run -p 16686:16686 -p 4317:4317 jaegertracing/all-in-one"
    ui: "http://localhost:16686"

  tempo:
    description: "Grafana's tracing backend"
    setup: "docker run -p 3200:3200 -p 4317:4317 grafana/tempo"

  zipkin:
    description: "Twitter's tracing system"
    setup: "docker run -p 9411:9411 openzipkin/zipkin"

  honeycomb:
    description: "SaaS observability platform"

  datadog:
    description: "APM + infrastructure"

  newrelic:
    description: "Full observability platform"
```

---

## 📈 PILLAR 3: METRICS

### Prometheus/OTEL Metrics by Language:

```yaml
# ═══════════════════════════════════════════════════════════════
# METRICS INSTRUMENTATION
# ═══════════════════════════════════════════════════════════════

metrics:
  go:
    library: prometheus/client_golang
    install: "go get github.com/prometheus/client_golang/prometheus"
    expose: |
      import "github.com/prometheus/client_golang/prometheus/promhttp"
      http.Handle("/metrics", promhttp.Handler())

  typescript:
    library: prom-client
    install: "npm install prom-client"
    expose: |
      import { collectDefaultMetrics, register } from 'prom-client';
      collectDefaultMetrics();
      app.get('/metrics', async (req, res) => {
        res.set('Content-Type', register.contentType);
        res.end(await register.metrics());
      });

  python:
    library: prometheus-client
    install: "pip install prometheus-client"
    expose: |
      from prometheus_client import start_http_server, Counter
      REQUEST_COUNT = Counter('requests_total', 'Total requests')
      start_http_server(8000)

  java:
    library: micrometer
    install: "micrometer-registry-prometheus"
    expose: "Spring Actuator /actuator/prometheus"

  rust:
    library: prometheus
    install: "cargo add prometheus"
```

### Key Metrics to Track:

```yaml
essential_metrics:
  # ═══════════════════════════════════════════════════════════════
  # RED METRICS (Request-based)
  # ═══════════════════════════════════════════════════════════════

  red:
    rate: "http_requests_total"
    errors: "http_requests_errors_total"
    duration: "http_request_duration_seconds"

  # ═══════════════════════════════════════════════════════════════
  # USE METRICS (Resource-based)
  # ═══════════════════════════════════════════════════════════════

  use:
    utilization: "cpu_usage_percent"
    saturation: "queue_length"
    errors: "disk_errors_total"

  # ═══════════════════════════════════════════════════════════════
  # BUSINESS METRICS
  # ═══════════════════════════════════════════════════════════════

  business:
    - orders_created_total
    - revenue_total
    - active_users
    - conversion_rate
```

---

## 🚨 ALERTING

### Alert Configuration:

```yaml
# ═══════════════════════════════════════════════════════════════
# ALERTMANAGER RULES
# ═══════════════════════════════════════════════════════════════

alerting:
  rules:
    high_error_rate:
      expr: |
        sum(rate(http_requests_errors_total[5m])) 
        / sum(rate(http_requests_total[5m])) > 0.05
      for: 5m
      severity: critical
      summary: "Error rate above 5%"

    high_latency:
      expr: |
        histogram_quantile(0.95, 
          sum(rate(http_request_duration_seconds_bucket[5m])) by (le)
        ) > 1
      for: 10m
      severity: warning
      summary: "P95 latency above 1s"

    service_down:
      expr: up == 0
      for: 1m
      severity: critical
      summary: "Service unreachable"

  channels:
    slack:
      webhook_url: "${SLACK_WEBHOOK_URL}"
    pagerduty:
      service_key: "${PAGERDUTY_KEY}"
    email:
      to: "oncall@company.com"
```

### Alert Best Practices:

```yaml
best_practices:
  - Avoid alert fatigue (prioritize critical)
  - Use severity labels (critical/warning/info)
  - Include runbook links
  - Group related alerts
  - Set appropriate thresholds
  - Use SLO-based alerts
```

---

## 📊 DASHBOARDS

### Grafana Dashboard Templates:

```yaml
dashboards:
  service_overview:
    panels:
      - Request rate (RPS)
      - Error rate (%)
      - P50/P95/P99 latency
      - Active connections

  infrastructure:
    panels:
      - CPU/Memory usage
      - Disk I/O
      - Network traffic
      - Container health

  business:
    panels:
      - Orders per minute
      - Revenue tracking
      - User activity
      - Conversion funnel
```

---

## 🐳 INFRASTRUCTURE SETUP

### Docker Compose Stack:

```yaml
# docker-compose.observability.yml
version: "3.8"

services:
  # ═══════════════════════════════════════════════════════════════
  # OTEL COLLECTOR
  # ═══════════════════════════════════════════════════════════════

  otel-collector:
    image: otel/opentelemetry-collector-contrib:latest
    command: ["--config=/etc/otel-collector-config.yaml"]
    volumes:
      - ./otel-collector-config.yaml:/etc/otel-collector-config.yaml
    ports:
      - "4317:4317" # OTLP gRPC
      - "4318:4318" # OTLP HTTP

  # ═══════════════════════════════════════════════════════════════
  # TRACING
  # ═══════════════════════════════════════════════════════════════

  jaeger:
    image: jaegertracing/all-in-one:latest
    ports:
      - "16686:16686" # UI
      - "14268:14268" # HTTP collector
    environment:
      - COLLECTOR_OTLP_ENABLED=true

  # ═══════════════════════════════════════════════════════════════
  # METRICS
  # ═══════════════════════════════════════════════════════════════

  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"

  # ═══════════════════════════════════════════════════════════════
  # VISUALIZATION
  # ═══════════════════════════════════════════════════════════════

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana-data:/var/lib/grafana

  # ═══════════════════════════════════════════════════════════════
  # ALERTING
  # ═══════════════════════════════════════════════════════════════

  alertmanager:
    image: prom/alertmanager:latest
    ports:
      - "9093:9093"
    volumes:
      - ./alertmanager.yml:/etc/alertmanager/alertmanager.yml

  # ═══════════════════════════════════════════════════════════════
  # LOGGING
  # ═══════════════════════════════════════════════════════════════

  loki:
    image: grafana/loki:latest
    ports:
      - "3100:3100"

volumes:
  grafana-data:
```

### OTEL Collector Config:

```yaml
# otel-collector-config.yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors:
  batch:
    timeout: 1s
    send_batch_size: 1024

exporters:
  jaeger:
    endpoint: jaeger:14250
    tls:
      insecure: true
  prometheus:
    endpoint: "0.0.0.0:8889"
  loki:
    endpoint: http://loki:3100/loki/api/v1/push

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [jaeger]
    metrics:
      receivers: [otlp]
      processors: [batch]
      exporters: [prometheus]
    logs:
      receivers: [otlp]
      processors: [batch]
      exporters: [loki]
```

---

## 📡 OTEL 2025 STANDARDS

```yaml
otel_2025:
  semantic_conventions:
    http_spans: "Stable"
    database: "Stabilizing mid-2025"
    messaging: "Stabilizing mid-2025"
    genai: "Experimental → Stable"

  profiling:
    status: "GA Expected mid-2025"
    use_case: "Code efficiency, bottleneck detection"

  best_practices:
    - "Embrace semantic conventions"
    - "Strategic sampling in high-traffic"
    - "Contextual enrichment (user/order IDs)"
    - "Correlate traces, metrics, logs"

  command: "/monitor otel [setup|verify]"
```

---

## 🤖 GENAI OBSERVABILITY

```yaml
genai_observability:
  description: "Monitor AI/LLM workloads"

  metrics:
    - prompt_tokens
    - completion_tokens
    - latency_per_request
    - model_version
    - error_rate
    - cost_per_request

  traces:
    - prompt_content (opt-in)
    - response_content (opt-in)
    - tool_calls
    - reasoning_steps

  alerts:
    cost_spike: "> 200% baseline"
    error_rate: "> 5%"
    latency_p99: "> 10s"
    token_budget: "> 90% limit"

  command: "/monitor genai [setup|dashboard]"
```

---

## 🔮 PREDICTIVE ALERTING

```yaml
predictive_alerting:
  description: "AI detects issues before impact"

  capabilities:
    anomaly_detection:
      method: "Learn normal patterns"
      action: "Flag deviations"

    trend_prediction:
      method: "Forecast bottlenecks"
      action: "Proactive scaling"

    root_cause:
      method: "Correlate telemetry"
      action: "Suggest probable causes"

  anti_fatigue:
    correlation: "Group related alerts"
    prioritization: "Critical first"
    noise_reduction: "Filter low-impact"

  command: "/monitor alert [configure|analyze]"
```

---

## ⚙️ TOKEN OPTIMIZATION

```yaml
token_saving:
  # Quick stack detection
  - Infer observability gaps
  - Use recommended defaults

  # Batch setup
  - Single docker-compose file
  - Template configurations

  # Minimal prompts
  - Only confirm tool selection
  - Auto-configure everything else
```

---

## 📜 RULES APPLIED

| Phase      | Rules                |
| ---------- | -------------------- |
| Detect     | `context-management` |
| Configure  | `stop-conditions`    |
| Instrument | `edit-verification`  |
| Deploy     | `safety`             |
| Verify     | `evidence`           |

---

_DOMYH Agent v4.3 • Monitor Pro v3.1 • AI-Powered Observability_
