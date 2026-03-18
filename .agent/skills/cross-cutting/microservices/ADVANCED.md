# Microservices — Advanced Patterns

## Table of Contents

- [Saga Pattern](#saga-pattern)
- [CQRS & Event Sourcing](#cqrs--event-sourcing)
- [Circuit Breaker](#circuit-breaker)
- [Service Mesh](#service-mesh)
- [Observability](#observability)

---

## Saga Pattern

### Orchestration Saga

```typescript
class OrderSaga {
  async execute(order: Order): Promise<SagaResult> {
    const steps: SagaStep[] = [
      { execute: () => this.reserveInventory(order), compensate: () => this.releaseInventory(order) },
      { execute: () => this.processPayment(order),   compensate: () => this.refundPayment(order) },
      { execute: () => this.shipOrder(order),         compensate: () => this.cancelShipment(order) },
    ]

    const completed: SagaStep[] = []

    for (const step of steps) {
      try {
        await step.execute()
        completed.push(step)
      } catch (error) {
        // Compensate in reverse order
        for (const s of completed.reverse()) {
          await s.compensate()
        }
        return { success: false, error }
      }
    }

    return { success: true }
  }
}
```

### Choreography Saga

```yaml
flow:
  OrderService:
    publishes: OrderCreated
    subscribes: [PaymentCompleted, PaymentFailed]

  PaymentService:
    subscribes: OrderCreated
    publishes: [PaymentCompleted, PaymentFailed]

  InventoryService:
    subscribes: PaymentCompleted
    publishes: [InventoryReserved, InventoryFailed]

  ShippingService:
    subscribes: InventoryReserved
    publishes: [ShipmentCreated, ShipmentFailed]

compensation:
  ShipmentFailed: "Release inventory → Refund payment → Cancel order"
  InventoryFailed: "Refund payment → Cancel order"
  PaymentFailed: "Cancel order"
```

---

## CQRS & Event Sourcing

```typescript
// Command side
class OrderCommandHandler {
  async handle(cmd: CreateOrderCommand): Promise<void> {
    const order = Order.create(cmd.userId, cmd.items)
    await this.eventStore.append(order.id, order.uncommittedEvents)
    await this.eventBus.publish(order.uncommittedEvents)
  }
}

// Event store
interface EventStore {
  append(aggregateId: string, events: DomainEvent[]): Promise<void>
  getEvents(aggregateId: string): Promise<DomainEvent[]>
}

// Read side (projection)
class OrderProjection {
  async handle(event: OrderCreated): Promise<void> {
    await this.readDb.orders.upsert({
      id: event.orderId,
      userId: event.userId,
      status: 'created',
      total: event.total,
      updatedAt: event.timestamp,
    })
  }
}
```

---

## Circuit Breaker

```typescript
class CircuitBreaker {
  private state: 'closed' | 'open' | 'half-open' = 'closed'
  private failures = 0
  private lastFailure = 0

  constructor(
    private threshold = 5,
    private timeout = 30000,  // 30s
    private halfOpenMax = 3,
  ) {}

  async call<T>(fn: () => Promise<T>): Promise<T> {
    if (this.state === 'open') {
      if (Date.now() - this.lastFailure > this.timeout) {
        this.state = 'half-open'
      } else {
        throw new CircuitOpenError()
      }
    }

    try {
      const result = await fn()
      this.onSuccess()
      return result
    } catch (error) {
      this.onFailure()
      throw error
    }
  }

  private onSuccess() {
    this.failures = 0
    this.state = 'closed'
  }

  private onFailure() {
    this.failures++
    this.lastFailure = Date.now()
    if (this.failures >= this.threshold) {
      this.state = 'open'
    }
  }
}
```

---

## Service Mesh

```yaml
patterns:
  sidecar_proxy:
    tools: ["Istio (Envoy)", "Linkerd"]
    features: ["mTLS", "Traffic splitting", "Retry", "Circuit breaking"]

  traffic_management: |
    # Istio VirtualService — Canary
    apiVersion: networking.istio.io/v1
    kind: VirtualService
    spec:
      hosts: [api]
      http:
        - route:
            - destination: { host: api, subset: stable }
              weight: 90
            - destination: { host: api, subset: canary }
              weight: 10
```

---

## Observability

```yaml
three_pillars:
  logs:
    format: "Structured JSON"
    fields: [timestamp, level, service, trace_id, span_id, message]
    tools: ["ELK Stack", "Loki + Grafana"]

  metrics:
    types: ["Counter", "Gauge", "Histogram", "Summary"]
    golden_signals: ["Latency", "Traffic", "Errors", "Saturation"]
    tools: ["Prometheus + Grafana", "Datadog"]

  traces:
    standard: "OpenTelemetry"
    propagation: "W3C Trace Context"
    tools: ["Jaeger", "Tempo", "Zipkin"]

alerting_rules:
  - "Error rate > 1% for 5 minutes → P1"
  - "p99 latency > 2s for 5 minutes → P2"
  - "CPU > 80% for 10 minutes → P3"
```

---
