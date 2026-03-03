---
description: "Use when writing backend API code, Go handlers, services, or repository patterns."
applyTo: "src/**/*.go,api/**/*,handlers/**/*,services/**/*,pkg/**/*"
---

# Backend API Guidelines

## Go Patterns

- Clean Architecture: handlers → services → repositories
- Interface-driven for testability
- Error wrapping: `fmt.Errorf("context: %w", err)`
- Context propagation for cancellation

## API Design

- RESTful conventions
- Consistent error responses
- Pagination for lists
- Rate limiting

## Security

- Input validation on all endpoints
- Parameterized queries (no SQL injection)
- Authentication middleware
- Audit logging
