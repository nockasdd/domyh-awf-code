---
description: "Use when writing tests, setting up test infrastructure, or reviewing test coverage."
applyTo: "**/*.test.ts,**/*.test.tsx,**/*.spec.ts,**/tests/**/*,**/__tests__/**/*"
---

# Testing Guidelines

## Test Structure (AAA)

- Arrange: Set up test data
- Act: Execute the operation
- Assert: Verify results

## Unit Tests

- Test one unit in isolation
- Mock external dependencies
- Fast (< 100ms each)

## Integration Tests

- Test component interactions
- Use test database/containers
- Clean state between tests

## Naming

- should_behavior_when_condition
- Clear and descriptive
