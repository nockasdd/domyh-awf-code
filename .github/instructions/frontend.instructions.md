---
applyTo: "src/**/*.tsx,src/**/*.jsx,components/**/*.tsx,components/**/*.jsx"
excludeAgent: ""
---

# Frontend Component Guidelines

## React Patterns

- Prefer functional components with hooks
- Use React.memo for expensive renders
- Extract custom hooks for reusable logic
- Error boundaries for graceful failures

## Component Structure

1. Hooks first (useState, useRef, custom)
2. Effects second (useEffect)
3. Handlers third
4. Render last

## State Management

- Local: useState/useReducer
- Shared: Context or Zustand
- Server: TanStack Query/SWR

## Testing

- React Testing Library for behavior
- Vitest for unit tests
