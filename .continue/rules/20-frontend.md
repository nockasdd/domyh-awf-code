---
name: Frontend Skills
alwaysApply: false
globs: ["src/**/*.tsx", "src/**/*.jsx"]
---

# Frontend Development Skills

## React Patterns

- Prefer functional components with hooks
- Use React.memo for expensive renders
- Extract custom hooks for reusable logic

## Component Structure

- Hooks first, Effects second, Handlers third, Render last
- Keep components focused and small
- Use composition over prop drilling

## State Management

- Local state: useState/useReducer
- Shared: Context for small, Zustand/Redux for complex
- Server state: TanStack Query/SWR
