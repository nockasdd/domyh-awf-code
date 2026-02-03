# DOMYH Code Review Style Guide v5.5

## Code Quality

### Naming

- Use descriptive, meaningful names
- Follow language conventions (camelCase, snake_case, PascalCase)
- Avoid abbreviations unless universally known

### Functions

- Keep functions focused (single responsibility)
- Maximum 50 lines per function
- Maximum 3 levels of nesting

### Error Handling

- Handle all error cases explicitly
- Use structured error types
- Log errors with context

## Security

### Input Validation

- Validate all user input
- Sanitize before use
- Type coercion checks

### SQL

- Use parameterized queries
- Never concatenate user input

## Testing

- Write tests for new features
- Cover edge cases
- Use meaningful test names

## Documentation

- Add JSDoc/docstrings for public APIs
- Comment "why" not "what"
- Keep README up to date
