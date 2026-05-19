---
library: tanstack
version: latest
latest: true
category: frontend
official_docs: https://tanstack.com
last_updated: 2026-03-20
last_checked: 2026-03-21
source: official docs + crawl4ai/trafilatura extraction
---

# TanStack Query v5

> TanStack Query — Powerful async state management for React, Vue, Svelte, Angular.
> Also: TanStack Router, Table, Form.
> Docs: https://tanstack.com

## Installation

```bash
npm install @tanstack/react-query
npm install -D @tanstack/eslint-plugin-query  # optional
```

## Setup

```tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60 * 1000,         // 1 minute
      gcTime: 5 * 60 * 1000,        // 5 minutes (was cacheTime)
      retry: 3,
      refetchOnWindowFocus: false,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router />
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}
```

## Core API

### useQuery

```tsx
import { useQuery } from '@tanstack/react-query';

function UserProfile({ userId }: { userId: string }) {
  const { data, isPending, isError, error } = useQuery({
    queryKey: ['user', userId],
    queryFn: () => fetch(`/api/users/${userId}`).then(r => r.json()),
    staleTime: 5 * 60 * 1000,
    enabled: !!userId,   // conditional query
  });

  if (isPending) return <Spinner />;
  if (isError) return <Error message={error.message} />;
  return <div>{data.name}</div>;
}
```

### useMutation

```tsx
import { useMutation, useQueryClient } from '@tanstack/react-query';

function CreatePost() {
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: (newPost: { title: string }) =>
      fetch('/api/posts', { method: 'POST', body: JSON.stringify(newPost) }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['posts'] });
    },
    onError: (error) => {
      console.error('Failed:', error);
    },
  });

  return (
    <button
      onClick={() => mutation.mutate({ title: 'New Post' })}
      disabled={mutation.isPending}
    >
      {mutation.isPending ? 'Creating...' : 'Create Post'}
    </button>
  );
}
```

### useInfiniteQuery

```tsx
const { data, fetchNextPage, hasNextPage, isFetchingNextPage } = useInfiniteQuery({
  queryKey: ['posts'],
  queryFn: ({ pageParam }) => fetchPosts({ cursor: pageParam }),
  initialPageParam: 0,
  getNextPageParam: (lastPage) => lastPage.nextCursor,
});

const allPosts = data?.pages.flatMap(page => page.items) ?? [];
```

### Optimistic Updates

```tsx
useMutation({
  mutationFn: updateTodo,
  onMutate: async (newTodo) => {
    await queryClient.cancelQueries({ queryKey: ['todos'] });
    const previous = queryClient.getQueryData(['todos']);
    queryClient.setQueryData(['todos'], (old) => [...old, newTodo]);
    return { previous };
  },
  onError: (err, newTodo, context) => {
    queryClient.setQueryData(['todos'], context.previous);
  },
  onSettled: () => {
    queryClient.invalidateQueries({ queryKey: ['todos'] });
  },
});
```

## TanStack Ecosystem (16 Libraries)

| Category | Libraries |
|:---------|:----------|
| **Data & State** | Query, DB, Store, AI |
| **UI & UX** | Table, Form, Hotkeys |
| **Performance** | Virtual, Pacer |
| **Full-Stack** | Start, Router |
| **Tooling** | DevTools, Config, CLI, Intent, MCP |

## TanStack Router

```bash
npm install @tanstack/react-router
```

```tsx
import { createFileRoute } from '@tanstack/react-router';

// Type-safe file-based routing
export const Route = createFileRoute('/posts/$postId')({
  // Type-safe params
  parseParams: (params) => ({ postId: Number(params.postId) }),
  // Loader for data fetching
  loader: async ({ params }) => {
    return fetchPost(params.postId);
  },
  component: PostComponent,
});

function PostComponent() {
  const post = Route.useLoaderData();
  const { postId } = Route.useParams();
  return <div>{post.title}</div>;
}

// Type-safe search params
export const Route = createFileRoute('/posts')({
  validateSearch: (search) => ({
    page: Number(search.page ?? 1),
    filter: (search.filter as string) ?? '',
  }),
});
```

## TanStack Table

```bash
npm install @tanstack/react-table
```

```tsx
import { useReactTable, getCoreRowModel, getSortedRowModel,
         getFilteredRowModel, getPaginationRowModel, flexRender } from '@tanstack/react-table';

const columns = [
  { accessorKey: 'name', header: 'Name' },
  { accessorKey: 'email', header: 'Email' },
  { accessorKey: 'role', header: 'Role',
    cell: (info) => <Badge>{info.getValue()}</Badge> },
];

function DataTable({ data }) {
  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
  });

  return (
    <table>
      <thead>
        {table.getHeaderGroups().map(hg => (
          <tr key={hg.id}>
            {hg.headers.map(h => (
              <th key={h.id} onClick={h.column.getToggleSortingHandler()}>
                {flexRender(h.column.columnDef.header, h.getContext())}
              </th>
            ))}
          </tr>
        ))}
      </thead>
      <tbody>
        {table.getRowModel().rows.map(row => (
          <tr key={row.id}>
            {row.getVisibleCells().map(cell => (
              <td key={cell.id}>{flexRender(cell.column.columnDef.cell, cell.getContext())}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}
```

## TanStack Form

```bash
npm install @tanstack/react-form
```

```tsx
import { useForm } from '@tanstack/react-form';

function ContactForm() {
  const form = useForm({
    defaultValues: { name: '', email: '' },
    onSubmit: async ({ value }) => {
      await submitForm(value);
    },
  });

  return (
    <form onSubmit={(e) => { e.preventDefault(); form.handleSubmit(); }}>
      <form.Field name="name"
        validators={{ onChange: ({ value }) => !value ? 'Required' : undefined }}
        children={(field) => (
          <div>
            <input value={field.state.value} onChange={(e) => field.handleChange(e.target.value)} />
            {field.state.meta.errors.map(err => <span key={err}>{err}</span>)}
          </div>
        )}
      />
      <button type="submit">Submit</button>
    </form>
  );
}
```

## TanStack Virtual

```bash
npm install @tanstack/react-virtual
```

```tsx
import { useVirtualizer } from '@tanstack/react-virtual';

function VirtualList({ items }) {
  const parentRef = useRef<HTMLDivElement>(null);

  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 50,  // estimated row height
    overscan: 5,
  });

  return (
    <div ref={parentRef} style={{ height: '400px', overflow: 'auto' }}>
      <div style={{ height: `${virtualizer.getTotalSize()}px`, position: 'relative' }}>
        {virtualizer.getVirtualItems().map(vi => (
          <div key={vi.key} style={{
            position: 'absolute', top: 0,
            transform: `translateY(${vi.start}px)`,
            height: `${vi.size}px`,
          }}>
            {items[vi.index].name}
          </div>
        ))}
      </div>
    </div>
  );
}
```

## TanStack Start (RC)

Full-stack React framework powered by TanStack Router + Vite:
- Full-document SSR + Streaming
- Server Functions (RPC-like)
- File-based routing via TanStack Router
- Deploy to any hosting/runtime

```bash
npm install @tanstack/react-start @tanstack/react-router
```

## prefetchQuery (SSR/Loader)

```ts
const queryClient = useQueryClient();

await queryClient.prefetchQuery({
  queryKey: ['posts'],
  queryFn: () => fetchPosts(),
});

// useSuspenseQuery — throws promise for Suspense boundaries
import { useSuspenseQuery } from '@tanstack/react-query';
const { data } = useSuspenseQuery({ queryKey: ['posts'], queryFn: fetchPosts });
```

## Gotchas

⚠️ **v5**: `cacheTime` renamed to `gcTime`. `isLoading` replaced by `isPending`.

⚠️ **Query keys**: Must be arrays `['user', id]` — objects serialized deterministically.

⚠️ **`staleTime: 0`** (default): Data is immediately stale, refetched on mount.

⚠️ **`enabled: false`**: Query won't run until enabled becomes true.

⚠️ **TanStack Start**: RC stage — full-stack React framework (SSR, streaming, server functions).

⚠️ **TanStack Router**: Type-safe file-based routing with `createFileRoute`, search params validation.

⚠️ **TanStack Table**: Headless — no UI included. Use `flexRender` with your own components.

⚠️ **TanStack Form**: Field-level validation via `validators.onChange`. No schema lib required.

⚠️ **TanStack Virtual**: Use `estimateSize` for row height. `overscan` controls pre-rendered items.
