# Frontend Development Guidelines

## React Patterns

- Prefer functional components with hooks
- Use React.memo for expensive renders
- Extract custom hooks for reusable logic

## Component Structure

- Hooks first, Effects second, Handlers third, Render last
- Keep components focused and small

## State Management

- Local: useState/useReducer
- Shared: Context or Zustand
- Server: TanStack Query/SWR
