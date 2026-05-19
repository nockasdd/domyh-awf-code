---
library: trpc
version: 11.x
latest: true
category: backend
official_docs: https://trpc.io/docs
last_updated: 2026-03-20
last_checked: 2026-03-21
source: trpc.io + curated
---

# tRPC v11

> tRPC — End-to-end typesafe APIs. No schemas, no codegen.
> Uses TypeScript inference. Works with React, Next.js, Nuxt.
> Docs: https://trpc.io/docs

## Installation

```bash
npm install @trpc/server @trpc/client
# React integration
npm install @trpc/react-query @tanstack/react-query
# Next.js
npm install @trpc/next
```

## Server Setup

```ts
// server/trpc.ts — initialization
import { initTRPC, TRPCError } from '@trpc/server';
import { z } from 'zod';

const t = initTRPC.context<{ userId?: string }>().create();

export const router = t.router;
export const publicProcedure = t.procedure;
export const protectedProcedure = t.procedure.use(async ({ ctx, next }) => {
    if (!ctx.userId) {
        throw new TRPCError({ code: 'UNAUTHORIZED' });
    }
    return next({ ctx: { ...ctx, userId: ctx.userId } });
});
```

```ts
// server/router.ts — define procedures
import { router, publicProcedure, protectedProcedure } from './trpc';

export const appRouter = router({
    // Query — read data
    hello: publicProcedure
        .input(z.object({ name: z.string() }))
        .query(({ input }) => {
            return { greeting: `Hello ${input.name}!` };
        }),

    // Query with database
    user: router({
        getById: publicProcedure
            .input(z.object({ id: z.string() }))
            .query(async ({ input }) => {
                return await db.user.findUnique({ where: { id: input.id } });
            }),

        list: publicProcedure
            .input(z.object({ limit: z.number().default(10) }))
            .query(async ({ input }) => {
                return await db.user.findMany({ take: input.limit });
            }),
    }),

    // Mutation — write data
    createPost: protectedProcedure
        .input(z.object({
            title: z.string().min(1),
            content: z.string().min(1),
        }))
        .mutation(async ({ input, ctx }) => {
            return await db.post.create({
                data: { ...input, authorId: ctx.userId },
            });
        }),
});

export type AppRouter = typeof appRouter;
```

## React Client

```tsx
// utils/trpc.ts
import { createTRPCReact } from '@trpc/react-query';
import type { AppRouter } from '../server/router';

export const trpc = createTRPCReact<AppRouter>();
```

```tsx
// app/providers.tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { httpBatchLink } from '@trpc/client';
import { trpc } from './utils/trpc';

const queryClient = new QueryClient();
const trpcClient = trpc.createClient({
    links: [httpBatchLink({ url: '/api/trpc' })],
});

export function Providers({ children }: { children: React.ReactNode }) {
    return (
        <trpc.Provider client={trpcClient} queryClient={queryClient}>
            <QueryClientProvider client={queryClient}>
                {children}
            </QueryClientProvider>
        </trpc.Provider>
    );
}
```

```tsx
// components/UserProfile.tsx — usage
import { trpc } from '../utils/trpc';

function UserProfile({ id }: { id: string }) {
    // Fully typed — input AND output
    const { data, isPending, error } = trpc.user.getById.useQuery({ id });
    
    const createPost = trpc.createPost.useMutation({
        onSuccess: () => {
            // Invalidate related queries
            utils.user.list.invalidate();
        },
    });

    if (isPending) return <Spinner />;
    return <div>{data?.name}</div>;
}
```

## Next.js App Router

```ts
// app/api/trpc/[trpc]/route.ts
import { fetchRequestHandler } from '@trpc/server/adapters/fetch';
import { appRouter } from '../../../../server/router';

const handler = (req: Request) =>
    fetchRequestHandler({
        endpoint: '/api/trpc',
        req,
        router: appRouter,
        createContext: () => ({ userId: getUserId() }),
    });

export { handler as GET, handler as POST };
```

## Subscriptions (WebSocket)

```ts
// Server
import { observable } from '@trpc/server/observable';

const appRouter = router({
    onMessage: publicProcedure.subscription(() => {
        return observable<{ text: string }>((emit) => {
            const listener = (msg: string) => emit.next({ text: msg });
            ee.on('message', listener);
            return () => ee.off('message', listener);
        });
    }),
});

// Client
const { data } = trpc.onMessage.useSubscription(undefined, {
    onData: (msg) => console.log('New message:', msg.text),
});
```

## Gotchas

⚠️ **TypeScript required**: tRPC uses TS inference — no runtime schemas sent over wire.

⚠️ **Zod for input**: Use `z.object()` for input validation. Output types inferred from return.

⚠️ **Batch by default**: `httpBatchLink` batches multiple calls into single HTTP request.

⚠️ **Context**: Created per-request. Pass auth/db connection through `createContext`.

⚠️ **Error handling**: Use `TRPCError` with codes: `UNAUTHORIZED`, `NOT_FOUND`, `BAD_REQUEST`, `INTERNAL_SERVER_ERROR`.

⚠️ **React Query**: tRPC wraps TanStack Query — same `useQuery`/`useMutation` patterns.

⚠️ **Type export**: Export `type AppRouter` (type-only) — no runtime code shipped to client.

⚠️ **Monorepo ideal**: Best when server and client share same TypeScript project/monorepo.
