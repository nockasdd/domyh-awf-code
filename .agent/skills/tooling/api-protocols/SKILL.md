---
name: api-protocols
description: "API protocol patterns for HTTP/2, gRPC, WebSocket, and GraphQL transport. Use when choosing or implementing API protocols."
category: tooling
---

# Modern API Protocols — GraphQL • tRPC • gRPC

> GraphQL federation & schema design • tRPC end-to-end TypeScript • gRPC high-performance polyglot  
> Complements `core/api-design` (REST patterns)

---

## Khi Nào Dùng

- Thiết kế GraphQL API (schema, federation, subscriptions)
- Dùng tRPC cho full-stack TypeScript monorepo
- Dùng gRPC cho service-to-service high-performance
- Chọn strategy: REST vs GraphQL vs tRPC vs gRPC

## Protocol Selection Guide

| Protocol    | Best For                 | Speed      | Type Safety     | Learning Curve |
| ----------- | ------------------------ | ---------- | --------------- | -------------- |
| **REST**    | Public APIs, CRUD        | ⭐⭐⭐     | Manual          | ⭐ Easy        |
| **GraphQL** | Flexible queries, mobile | ⭐⭐⭐     | Schema-based    | ⭐⭐ Medium    |
| **tRPC**    | TS monorepo, internal    | ⭐⭐⭐     | End-to-end auto | ⭐ Easy        |
| **gRPC**    | Microservices, streaming | ⭐⭐⭐⭐⭐ | Proto-based     | ⭐⭐⭐ Hard    |

## GraphQL Patterns

### Schema Design (Client-Centric)

```graphql
# ✅ GOOD: Client-driven, meaningful types
type User {
  id: ID!
  profile: UserProfile!
  posts(first: Int!, after: String): PostConnection!
}

# Relay-style cursor pagination
type PostConnection {
  edges: [PostEdge!]!
  pageInfo: PageInfo!
}
```

### Federation (Apollo)

```graphql
# Subgraph: Users
type User @key(fields: "id") {
  id: ID!
  name: String!
}

# Subgraph: Orders (extends User)
extend type User @key(fields: "id") {
  id: ID! @external
  orders: [Order!]!
}
```

### Security Checklist

- ✅ Query depth limiting (max 10-15)
- ✅ Persisted queries (whitelist, no arbitrary queries)
- ✅ Cost analysis (complexity scoring)
- ✅ Rate limiting per operation type
- ✅ Field-level authorization

### N+1 Prevention

```typescript
// ✅ Use DataLoader for batching
const userLoader = new DataLoader(async (ids) => {
  const users = await db.users.findMany({ where: { id: { in: ids } } });
  return ids.map((id) => users.find((u) => u.id === id));
});
```

## tRPC Patterns

### Router Setup

```typescript
// server: define once
const appRouter = router({
  user: router({
    getById: publicProcedure
      .input(z.object({ id: z.string() }))
      .query(({ input }) => db.user.findUnique({ where: { id: input.id } })),
    create: protectedProcedure
      .input(createUserSchema)
      .mutation(({ input }) => db.user.create({ data: input })),
  }),
});

// client: full type inference, zero codegen
const user = await trpc.user.getById.query({ id: "123" }); // fully typed!
```

### Best Practices

1. **Monorepo** — Share types between client/server (same TS codebase)
2. **Middleware** — Auth, logging, rate limiting via procedure middleware
3. **Split routers** — One router per domain (user, post, payment)
4. **React Query** — Automatic cache invalidation via `trpc.useUtils()`

## gRPC Patterns

### Proto Design

```protobuf
syntax = "proto3";
package user.v1;

service UserService {
  rpc GetUser(GetUserRequest) returns (User);
  rpc ListUsers(ListUsersRequest) returns (stream User); // server streaming
  rpc Chat(stream ChatMessage) returns (stream ChatMessage); // bidi
}

message User {
  string id = 1;
  string name = 2;
  google.protobuf.Timestamp created_at = 3;
}
```

### Performance Rules

1. **Reuse channels** — Don't create new channel per request
2. **Keep protos small** — Efficient serialization = faster
3. **TLS always** — Encrypt all gRPC traffic
4. **Load balancing** — Client-side or proxy-based (Envoy)

## Common Traps

| Trap            | Protocol | Fix                                                     |
| --------------- | -------- | ------------------------------------------------------- |
| N+1 queries     | GraphQL  | DataLoader batching                                     |
| Over-fetching   | GraphQL  | Persisted queries, field selection                      |
| Bundle size     | tRPC     | Split routers per API route                             |
| Browser compat  | gRPC     | Use gRPC-Web with Envoy proxy                           |
| Schema breaking | All      | Versioning (GraphQL deprecation, proto reserved fields) |

---
