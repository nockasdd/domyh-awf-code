# Testing — Advanced Patterns

# DOMYH Awesome Code v4.3 — Tier 3 Reference

## Table of Contents

- [Test Architecture](#test-architecture)
- [Mocking Strategies](#mocking-strategies)
- [Property-Based Testing](#property-based-testing)
- [Performance Testing](#performance-testing)

---

## Test Architecture

### Test Pyramid Implementation

```typescript
// Unit Test (70% of tests)
describe("OrderService", () => {
  let service: OrderService;
  let mockRepo: jest.Mocked<OrderRepository>;

  beforeEach(() => {
    mockRepo = {
      findById: jest.fn(),
      save: jest.fn(),
    } as any;
    service = new OrderService(mockRepo);
  });

  it("calculates total with discount", () => {
    const order = { items: [{ price: 100, qty: 2 }], discount: 10 };
    expect(service.calculateTotal(order)).toBe(180);
  });
});

// Integration Test (20% of tests)
describe("OrderRepository", () => {
  let db: TestDatabase;
  let repo: OrderRepository;

  beforeAll(async () => {
    db = await TestDatabase.create();
    repo = new OrderRepository(db.connection);
  });

  afterAll(() => db.destroy());

  it("persists and retrieves order", async () => {
    const order = await repo.save(createOrder());
    const found = await repo.findById(order.id);
    expect(found).toEqual(order);
  });
});

// E2E Test (10% of tests)
describe("Order API", () => {
  it("creates order via API", async () => {
    const response = await request(app)
      .post("/orders")
      .send({ items: [{ productId: "1", qty: 2 }] })
      .expect(201);

    expect(response.body.id).toBeDefined();
  });
});
```

---

## Mocking Strategies

### Dependency Injection Mocks

```typescript
// Contract-based mock
interface PaymentGateway {
  charge(amount: number): Promise<PaymentResult>;
}

class MockPaymentGateway implements PaymentGateway {
  private responses: Map<number, PaymentResult> = new Map();
  public calls: number[] = [];

  respondWith(amount: number, result: PaymentResult) {
    this.responses.set(amount, result);
    return this;
  }

  async charge(amount: number): Promise<PaymentResult> {
    this.calls.push(amount);
    return this.responses.get(amount) ?? { success: true };
  }
}

// Usage
const gateway = new MockPaymentGateway().respondWith(100, {
  success: false,
  error: "Declined",
});

const service = new PaymentService(gateway);
await service.process(100);
expect(gateway.calls).toEqual([100]);
```

### Network Mocking

```typescript
import nock from "nock";

describe("ExternalAPI", () => {
  afterEach(() => nock.cleanAll());

  it("handles retry on 503", async () => {
    nock("https://api.example.com")
      .get("/data")
      .reply(503)
      .get("/data")
      .reply(200, { value: 42 });

    const result = await fetchWithRetry("/data");
    expect(result.value).toBe(42);
  });
});
```

---

## Property-Based Testing

### Hypothesis (Python)

```python
from hypothesis import given, strategies as st

@given(st.lists(st.integers()))
def test_sort_is_idempotent(xs):
    """Sorting twice equals sorting once"""
    assert sorted(sorted(xs)) == sorted(xs)

@given(st.lists(st.integers(), min_size=1))
def test_sort_preserves_elements(xs):
    """Sorting doesn't add or remove elements"""
    sorted_xs = sorted(xs)
    assert len(sorted_xs) == len(xs)
    assert set(sorted_xs) == set(xs)

@given(
    st.text(min_size=1),
    st.text(min_size=1)
)
def test_concat_length(a, b):
    """Concatenation length equals sum of lengths"""
    assert len(a + b) == len(a) + len(b)
```

### Fast-Check (TypeScript)

```typescript
import fc from "fast-check";

describe("Money", () => {
  it("add is commutative", () => {
    fc.assert(
      fc.property(
        fc.integer({ min: 0, max: 1000000 }),
        fc.integer({ min: 0, max: 1000000 }),
        (a, b) => Money.add(a, b) === Money.add(b, a),
      ),
    );
  });

  it("format and parse are inverse", () => {
    fc.assert(
      fc.property(
        fc.integer({ min: 0, max: 99999999 }),
        (cents) => Money.parse(Money.format(cents)) === cents,
      ),
    );
  });
});
```

---

## Performance Testing

### k6 Load Testing

```javascript
import http from "k6/http";
import { check, sleep } from "k6";

export const options = {
  stages: [
    { duration: "30s", target: 20 }, // Ramp up
    { duration: "1m", target: 20 }, // Steady
    { duration: "10s", target: 0 }, // Ramp down
  ],
  thresholds: {
    http_req_duration: ["p(95)<200"], // 95% under 200ms
    http_req_failed: ["rate<0.01"], // Error rate < 1%
  },
};

export default function () {
  const res = http.get("https://api.example.com/orders");

  check(res, {
    "status is 200": (r) => r.status === 200,
    "response time OK": (r) => r.timings.duration < 200,
  });

  sleep(1);
}
```

### Benchmark Tests

```go
func BenchmarkSerialize(b *testing.B) {
    data := generateLargeData()

    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        _ = json.Marshal(data)
    }
}

func BenchmarkSerializeParallel(b *testing.B) {
    data := generateLargeData()

    b.RunParallel(func(pb *testing.PB) {
        for pb.Next() {
            _ = json.Marshal(data)
        }
    })
}
```

---

_DOMYH Awesome Code v4.3 — Tier 3 Reference_
