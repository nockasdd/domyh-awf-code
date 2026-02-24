---
name: event-driven
version: "6.4.3"
category: cross-cutting
---

# Event-Driven Architecture — Kafka • RabbitMQ • NATS

> Pub/Sub • Event Sourcing • CQRS • Saga Pattern  
> Dead Letter Queues • Idempotent Consumers • Schema Evolution

---

## Khi Nào Dùng

- Thiết kế async messaging giữa microservices
- Chọn message broker (Kafka vs RabbitMQ vs NATS)
- Implement event sourcing, CQRS, hoặc saga pattern
- Xử lý DLQ, idempotency, schema evolution

## Broker Selection Guide

| Feature         | Kafka                                 | RabbitMQ                    | NATS                             |
| --------------- | ------------------------------------- | --------------------------- | -------------------------------- |
| **Throughput**  | 1M+ msg/s                             | 50K-100K msg/s              | 200K-400K msg/s                  |
| **Latency**     | 10-50ms                               | 5-20ms                      | <1ms (core)                      |
| **Persistence** | Always                                | Configurable                | JetStream                        |
| **Delivery**    | At-least-once (exactly-once possible) | At-least-once               | At-most-once / Exactly-once (JS) |
| **Best For**    | Data streaming, event log             | Business workflows, routing | Real-time, IoT, cloud-native     |
| **Complexity**  | ⭐⭐⭐ High                           | ⭐⭐ Medium                 | ⭐ Low                           |

## Core Patterns

### Pub/Sub

```
Producer ──▶ Topic/Exchange ──▶ Consumer A
                            ──▶ Consumer B
                            ──▶ Consumer C
```

### Event Sourcing + CQRS

```
Command ──▶ Event Store ──▶ [OrderCreated, ItemAdded, OrderPaid]
                                          │
                      ┌───────────────────┤
                      ▼                   ▼
               Read Model A        Read Model B
              (Order Summary)     (Analytics)
```

### Saga Pattern

```
Orchestrator Saga:
  Orchestrator ──▶ Service A (Book Order)
                   ├── Success ──▶ Service B (Process Payment)
                   │                ├── Success ──▶ Service C (Ship)
                   │                └── Failure ──▶ Compensate A
                   └── Failure ──▶ Done

Choreography Saga:
  Service A ──event──▶ Service B ──event──▶ Service C
       ◀──compensate──      ◀──compensate──
```

## Production Patterns

### Dead Letter Queue (DLQ)

```typescript
// Consumer with DLQ fallback
async function consume(message: Message) {
  try {
    await process(message);
    await message.ack();
  } catch (err) {
    if (message.retryCount >= MAX_RETRIES) {
      await dlq.publish(message); // Send to DLQ
      await message.ack(); // Remove from main queue
    } else {
      await message.nack({ requeue: true, delay: backoff(message.retryCount) });
    }
  }
}
```

### Idempotent Consumer

```typescript
// Deduplication by event ID
async function handleEvent(event: Event) {
  const processed = await redis.setnx(`event:${event.id}`, "1", "EX", 86400);
  if (!processed) return; // Already handled
  await processEvent(event);
}
```

### Schema Evolution

| Strategy            | Compatibility       | Example                   |
| ------------------- | ------------------- | ------------------------- |
| **Add field**       | Backward compatible | New optional field        |
| **Deprecate field** | Forward compatible  | Mark as deprecated        |
| **Rename field**    | Breaking!           | Add alias, deprecate old  |
| **Remove field**    | Breaking!           | Schema registry + version |

## Common Traps

| Trap                    | Fix                                             |
| ----------------------- | ----------------------------------------------- |
| Message ordering        | Kafka: partition key; RabbitMQ: single consumer |
| Duplicate processing    | Idempotent consumers + dedup by event ID        |
| Consumer lag            | Monitor lag, auto-scale consumers               |
| Poison messages         | DLQ + max retry count                           |
| Schema breaking changes | Schema registry, versioned events               |
| Back-pressure           | Consumer rate limiting, buffering               |

## Monitoring Essentials

- Consumer lag (Kafka: `kafka-consumer-groups`, RabbitMQ: management UI)
- Message throughput (in/out per second)
- Error rate & DLQ depth
- End-to-end latency (publish → consume)

---

_DOMYH Awesome Code • Event-Driven Architecture Skill v1.0.0_
