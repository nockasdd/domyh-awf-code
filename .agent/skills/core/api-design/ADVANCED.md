# API Design — Advanced Patterns

## Table of Contents

- [REST Advanced](#rest-advanced)
- [GraphQL Patterns](#graphql-patterns)
- [gRPC Patterns](#grpc-patterns)
- [API Versioning](#api-versioning)
- [Rate Limiting & Throttling](#rate-limiting--throttling)
- [API Security](#api-security)

---

## REST Advanced

### HATEOAS Pattern

```json
{
  "id": "123",
  "name": "John Doe",
  "email": "john@example.com",
  "_links": {
    "self": { "href": "/api/v1/users/123" },
    "posts": { "href": "/api/v1/users/123/posts" },
    "avatar": { "href": "/api/v1/users/123/avatar" },
    "update": { "href": "/api/v1/users/123", "method": "PUT" },
    "delete": { "href": "/api/v1/users/123", "method": "DELETE" }
  }
}
```

### Pagination Strategies

```yaml
strategies:
  cursor_based:  # ✅ Recommended for real-time data
    request: "GET /api/posts?cursor=eyJpZCI6MTB9&limit=20"
    response:
      data: [...]
      pagination:
        next_cursor: "eyJpZCI6MzB9"
        has_more: true
    pros: ["Consistent with inserts/deletes", "O(1) seek"]
    cons: ["Can't jump to page N"]

  offset_based:  # For simple cases
    request: "GET /api/posts?page=2&per_page=20"
    response:
      data: [...]
      pagination: { page: 2, per_page: 20, total: 156, total_pages: 8 }
    pros: ["Jump to any page"]
    cons: ["Inconsistent with concurrent writes", "O(n) seek"]

  keyset:  # For sorted data
    request: "GET /api/posts?after_id=100&limit=20&sort=created_desc"
    pros: ["Fast with index", "Consistent"]
```

### Error Response Standard (RFC 7807)

```json
{
  "type": "https://api.example.com/errors/validation",
  "title": "Validation Error",
  "status": 422,
  "detail": "The request body contains invalid fields",
  "instance": "/api/v1/users",
  "errors": [
    { "field": "email", "message": "Invalid email format" },
    { "field": "age", "message": "Must be >= 18" }
  ],
  "trace_id": "abc-123-xyz"
}
```

---

## GraphQL Patterns

### Schema Design

```graphql
# Relay-style connection for pagination
type Query {
  users(first: Int, after: String, filter: UserFilter): UserConnection!
}

type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type UserEdge {
  node: User!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

# Input types for mutations
input CreateUserInput {
  name: String!
  email: String!
  role: UserRole = USER
}

type Mutation {
  createUser(input: CreateUserInput!): CreateUserPayload!
}

type CreateUserPayload {
  user: User
  errors: [UserError!]
}
```

### N+1 Prevention (DataLoader)

```typescript
const userLoader = new DataLoader<string, User>(async (ids) => {
  const users = await db.user.findMany({ where: { id: { in: [...ids] } } })
  const userMap = new Map(users.map(u => [u.id, u]))
  return ids.map(id => userMap.get(id) ?? new Error(`User ${id} not found`))
})

// Resolver
const resolvers = {
  Post: {
    author: (post) => userLoader.load(post.authorId),
  },
}
```

---

## gRPC Patterns

### Streaming

```protobuf
service ChatService {
  rpc SendMessage(ChatMessage) returns (Ack);                    // Unary
  rpc Subscribe(SubscribeRequest) returns (stream ChatMessage);  // Server stream
  rpc Upload(stream Chunk) returns (UploadResponse);             // Client stream
  rpc Chat(stream ChatMessage) returns (stream ChatMessage);     // Bidirectional
}
```

### Error Handling

```yaml
grpc_status_mapping:
  400_Bad_Request: INVALID_ARGUMENT
  401_Unauthorized: UNAUTHENTICATED
  403_Forbidden: PERMISSION_DENIED
  404_Not_Found: NOT_FOUND
  409_Conflict: ALREADY_EXISTS
  429_Too_Many: RESOURCE_EXHAUSTED
  500_Internal: INTERNAL
  503_Unavailable: UNAVAILABLE
  504_Timeout: DEADLINE_EXCEEDED
```

---

## API Versioning

```yaml
strategies:
  url_path:     # ✅ Most common
    example: "/api/v1/users, /api/v2/users"
    pros: ["Clear", "Cache-friendly"]

  header:       # For internal APIs
    example: "Accept: application/vnd.api+json;version=2"
    pros: ["Clean URLs"]

  query_param:  # Simple
    example: "/api/users?version=2"

best_practices:
  - "Support N-1 versions minimum"
  - "Deprecation header: Sunset: Sat, 01 Jan 2026"
  - "Migration guide in changelog"
  - "Feature flags over version bumps for minor changes"
```

---

## Rate Limiting & Throttling

### Token Bucket Implementation

```yaml
headers:
  X-RateLimit-Limit: 100        # Max requests per window
  X-RateLimit-Remaining: 42     # Remaining in window
  X-RateLimit-Reset: 1640000000 # Unix timestamp when window resets
  Retry-After: 30               # Seconds (when 429)

tiers:
  free:    { rpm: 60,   rpd: 1000  }
  pro:     { rpm: 600,  rpd: 10000 }
  enterprise: { rpm: 6000, rpd: 100000 }
```

---

## API Security

```yaml
checklist:
  authentication:
    - "OAuth 2.0 + PKCE for public clients"
    - "API keys for server-to-server (rotate every 90 days)"
    - "JWT with short expiry (15min access + refresh token)"
  authorization:
    - "RBAC or ABAC per endpoint"
    - "Scope-based access for OAuth"
  transport:
    - "TLS 1.3 minimum"
    - "HSTS header with preload"
  input:
    - "Validate Content-Type header"
    - "Request body size limits"
    - "Parameterized queries (never string concat)"
  output:
    - "Remove internal headers (X-Powered-By)"
    - "CORS whitelist (never *)"
    - "Response filtering (no internal IDs/fields)"
```

---
