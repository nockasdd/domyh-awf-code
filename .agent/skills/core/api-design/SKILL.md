---
name: api-design
version: "6.4.2"
category: core
---

# 🔗 API Design Patterns

> Comprehensive patterns for REST, GraphQL, and gRPC API design
> 🚀 HSA Dynamic Search Enabled | 📊 202 Patterns | 25 Test APIs

---

## 🎯 HSA Integration

Data powered by HSA BM25 search engine. Query YAML data via skill search:

| Domain     | Query Examples                   |
| ---------- | -------------------------------- |
| REST       | "versioning strategy URI header" |
| GraphQL    | "N+1 DataLoader schema"          |
| gRPC       | "streaming protobuf reliability" |
| Error      | "RFC 9457 error response format" |
| Rate Limit | "token bucket sliding window"    |

---

## 📊 Quick Reference

### REST Richardson Maturity Model

| Level | Name         | Characteristics                     |
| ----- | ------------ | ----------------------------------- |
| 0     | Swamp of POX | Single URI, single method (RPC)     |
| 1     | Resources    | Individual URIs per resource        |
| 2     | HTTP Verbs   | Proper GET/POST/PUT/DELETE          |
| 3     | HATEOAS      | Hypermedia controls, self-discovery |

### API Versioning Strategies (Real-World)

| Strategy   | Example                            | Used By                   |
| ---------- | ---------------------------------- | ------------------------- |
| URI        | `/v1/users`                        | Facebook, Twitter, PayPal |
| Header     | `X-API-Version: 1`                 | Microsoft Azure           |
| Date-Based | `2024-06-20`                       | **Stripe**, **GitHub**    |
| Semantic   | `2.1.0`                            | **Twilio** SDKs           |
| Calendar   | `X-GitHub-Api-Version: 2022-11-28` | GitHub REST               |

### Pagination Patterns

| Pattern | Use Case           | Trade-off        |
| ------- | ------------------ | ---------------- |
| Offset  | Small datasets     | Slow at scale    |
| Cursor  | Large/dynamic data | No random access |
| Keyset  | Ordered lists      | Sequential only  |

### Rate Limiting

```
┌─────────────────────────────────────────┐
│ Token Bucket: Handles bursts            │
│ - Tokens refill at fixed rate           │
│ - Burst up to bucket capacity           │
├─────────────────────────────────────────┤
│ Sliding Window: Smooth rate             │
│ - Rolling time window                   │
│ - More precise than fixed window        │
└─────────────────────────────────────────┘
```

### Error Response (RFC 9457)

```json
{
  "type": "https://api.example.com/errors/rate-limit",
  "title": "Rate Limit Exceeded",
  "status": 429,
  "detail": "You have exceeded 100 requests per minute",
  "instance": "/logs/abc123"
}
```

---

## 🧪 Test APIs for Learning

| API             | URL                          | Best For           |
| --------------- | ---------------------------- | ------------------ |
| JSONPlaceholder | jsonplaceholder.typicode.com | Prototyping, demos |
| httpbin         | httpbin.org                  | HTTP debugging     |
| Reqres          | reqres.in                    | Auth flows         |
| Random User     | randomuser.me/api            | UI testing         |
| FakeStore API   | fakestoreapi.com             | E-commerce         |
| Postman Echo    | postman-echo.com             | Request inspection |

> 💡 See `test-apis.yaml` for matching APIs by use case

---

## 📁 Data Files

| File                     | Patterns | Coverage                           |
| ------------------------ | -------- | ---------------------------------- |
| `rest-patterns.yaml`     | 30       | URI, methods, HATEOAS, caching     |
| `graphql-patterns.yaml`  | 25       | Schema, resolvers, N+1, DataLoader |
| `grpc-patterns.yaml`     | 25       | Protobuf, streaming, reliability   |
| `api-versioning.yaml`    | 25       | URI, header, Stripe/GitHub/Twilio  |
| `pagination.yaml`        | 15       | Offset, cursor, keyset             |
| `rate-limiting.yaml`     | 20       | Token bucket, sliding window       |
| `error-responses.yaml`   | 20       | RFC 9457, validation errors        |
| `http-status-codes.yaml` | 27       | 2xx, 4xx, 5xx reference            |
| `test-apis.yaml`         | 25       | Public APIs for testing            |

**Total: 202 patterns**

---

## 🔧 Common Patterns

### REST Best Practices

```yaml
URI Design:
  - Use plural nouns: /users, /products
  - Nest max 2-3 levels: /users/{id}/orders
  - Use hyphens: /order-items
  - Keep lowercase: /users not /Users
  - No verbs: GET /users not /getUsers

HTTP Methods:
  GET: Read (idempotent)
  POST: Create
  PUT: Replace entire resource
  PATCH: Partial update
  DELETE: Remove (idempotent)
```

### GraphQL N+1 Solution

```javascript
// Without DataLoader (N+1 problem)
users.map((user) => db.query(`SELECT * FROM orders WHERE userId = ${user.id}`));

// With DataLoader (1 batched query)
const orderLoader = new DataLoader((userIds) =>
  db.query(`SELECT * FROM orders WHERE userId IN (${userIds})`),
);
users.map((user) => orderLoader.load(user.id));
```

### gRPC Streaming

```protobuf
// Unary RPC
rpc GetUser(UserRequest) returns (User);

// Server streaming
rpc ListUsers(Empty) returns (stream User);

// Client streaming
rpc UploadData(stream Chunk) returns (Status);

// Bidirectional streaming
rpc Chat(stream Message) returns (stream Message);
```

---

_DOMYH Awesome Code • API Design Patterns • 202 patterns • HSA Enabled_
