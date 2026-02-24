---
name: microservices
version: "6.4.3"
category: cross-cutting
---

# 🏗️ Microservices Patterns

> Architecture patterns for distributed systems
> 📚 Saga • CQRS • Event Sourcing • Service Mesh • Resilience

---

## Quick Reference

| Pattern             | When to Use                                  | Complexity |
| ------------------- | -------------------------------------------- | ---------- |
| **Saga**            | Multi-service transactions                   | High       |
| **CQRS**            | Read/write asymmetry                         | Medium     |
| **Event Sourcing**  | Audit trail, temporal queries                | High       |
| **Service Mesh**    | Cross-cutting concerns (mTLS, observability) | High       |
| **Circuit Breaker** | Prevent cascade failures                     | Low        |
| **API Gateway**     | Single entry point, routing                  | Medium     |

---

## Saga Pattern

### Orchestration vs Choreography

| Aspect    | Orchestration           | Choreography             |
| --------- | ----------------------- | ------------------------ |
| Control   | Central orchestrator    | Event-driven, no central |
| Coupling  | Services → orchestrator | Event chain              |
| Debugging | Easier (single flow)    | Harder (distributed)     |
| Best for  | Complex workflows       | Simple 2-3 service flows |

### Compensating Transactions

```
Order → Payment → Inventory → Shipping
  ↓ (if Shipping fails)
  Refund ← Restock ← Cancel
```

---

## CQRS

```
┌─────────────────────────────────────────────┐
│  Command Side        │  Query Side          │
│  ────────────        │  ──────────          │
│  Write Model         │  Read Model          │
│  Domain Events       │  Projections         │
│  Event Store         │  Materialized Views  │
│  Optimized for       │  Optimized for       │
│  consistency         │  performance         │
└─────────────────────────────────────────────┘
```

---

## Communication Patterns

| Type  | Protocol  | Use Case                         |
| ----- | --------- | -------------------------------- |
| Sync  | REST/HTTP | Simple request-response          |
| Sync  | gRPC      | High-perf, typed contracts       |
| Async | Kafka     | Event streaming, high throughput |
| Async | RabbitMQ  | Task queues, routing             |
| Async | NATS      | Lightweight pub/sub              |

---

## Resilience Patterns

| Pattern             | Purpose                  | Library                      |
| ------------------- | ------------------------ | ---------------------------- |
| **Circuit Breaker** | Stop cascade failures    | Hystrix, Resilience4j, Polly |
| **Bulkhead**        | Isolate failures         | Thread pools, semaphores     |
| **Retry**           | Transient error recovery | Exponential backoff          |
| **Timeout**         | Prevent hanging          | Per-service config           |
| **Fallback**        | Graceful degradation     | Cache, default values        |

---

## Service Mesh

| Feature        | Istio       | Linkerd  |
| -------------- | ----------- | -------- |
| mTLS           | ✅ Auto     | ✅ Auto  |
| Traffic mgmt   | ✅ Advanced | ⚠️ Basic |
| Observability  | ✅ Full     | ✅ Good  |
| Complexity     | High        | Low      |
| Resource usage | Heavy       | Light    |

---

## Deployment Strategies

| Strategy        | Zero-Downtime | Rollback |   Risk   |
| --------------- | :-----------: | :------: | :------: |
| **Blue-Green**  |      ✅       | Instant  |   Low    |
| **Canary**      |      ✅       | Gradual  | Very Low |
| **Rolling**     |      ✅       |   Slow   |  Medium  |
| **A/B Testing** |      ✅       | Instant  |   Low    |

---

## HSA Integration

| Query                               | Data File             |
| ----------------------------------- | --------------------- |
| `saga orchestration compensation`   | `saga-patterns.yaml`  |
| `cqrs event store projection`       | `cqrs-patterns.yaml`  |
| `event sourcing snapshot replay`    | `event-sourcing.yaml` |
| `istio linkerd sidecar`             | `service-mesh.yaml`   |
| `grpc kafka rabbitmq nats`          | `communication.yaml`  |
| `circuit breaker bulkhead retry`    | `resilience.yaml`     |
| `distributed tracing opentelemetry` | `observability.yaml`  |
| `blue-green canary rolling`         | `deployment.yaml`     |

---

_DOMYH Awesome Code • Microservices Patterns_
