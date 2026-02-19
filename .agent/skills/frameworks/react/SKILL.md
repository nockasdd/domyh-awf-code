---
name: react
detect: ["package.json:react", "*.jsx", "*.tsx", "vite.config.ts"]
version: "7.0.0"
category: frontend
tier: 1
---

# React Patterns — DOMYH Awesome Code

> **Version**: React 19.2+ (2025-2026)
> **Philosophy**: Server-first, compiler-optimized, hooks-based

---

## Decision Tree

```
Task → What React pattern?
  ├─ Component design
  │   ├─ List/forms → Server Components (RSC)
  │   ├─ Interactive → Client Component ('use client')
  │   └─ Layout → Composition pattern (children)
  ├─ State management
  │   ├─ Local → useState / useReducer
  │   ├─ Shared (small) → Context + useReducer
  │   ├─ Complex → Zustand (simple) / Jotai (atomic)
  │   └─ Server → TanStack Query / SWR
  ├─ Data fetching
  │   ├─ Server → use() + fetch in RSC
  │   ├─ Client → TanStack Query
  │   └─ Forms → Server Actions + useActionState
  └─ Rendering
      ├─ SEO needed → Next.js SSR/SSG
      ├─ SPA → Vite + React Router
      └─ Static → Astro + React islands
```

## 🎯 When to Use This Skill

Use for: React SPAs, component libraries, client-side apps.
**NOT for**: SSR (→ nextjs or Vite RSC plugin), mobile-first (→ flutter).

---

## 📦 Recommended Stack (2025-2026)

### Core

- **React 19** - UI library 🏆
- **TypeScript 5.5+** - Type safety
- **Vite 6** - Build tool 🏆

### UI Components

- **shadcn/ui** - Radix + Tailwind 🏆
- **Radix UI** - Headless primitives

### State Management

- **Zustand** - Simple client state 🏆
- **TanStack Query** - Server state 🏆

### Forms

- **React Hook Form** + **Zod** 🏆

---

## 🆕 React 19 Features

### React Compiler (Auto Memoization)

```tsx
// ✅ No need for useMemo/useCallback!
function ExpensiveList({ items }: { items: Item[] }) {
  const sorted = items.toSorted((a, b) => a.name.localeCompare(b.name));
  return (
    <ul>
      {sorted.map((item) => (
        <li key={item.id}>{item.name}</li>
      ))}
    </ul>
  );
}
```

### use() Hook

```tsx
import { use, Suspense } from "react";

function UserProfile({ userPromise }: { userPromise: Promise<User> }) {
  const user = use(userPromise);
  return <h1>{user.name}</h1>;
}

<Suspense fallback={<Loading />}>
  <UserProfile userPromise={fetchUser()} />
</Suspense>;
```

### useOptimistic Hook

```tsx
"use client";
import { useOptimistic } from "react";

function LikeButton({ likes }: { likes: number }) {
  const [optimisticLikes, addLike] = useOptimistic(likes, (s) => s + 1);

  async function handleLike() {
    addLike(null);
    await likePost();
  }

  return <button onClick={handleLike}>❤️ {optimisticLikes}</button>;
}
```

### useActionState

```tsx
// React 19: returns [state, action, isPending] triple
import { useActionState } from "react";

function Form() {
  const [state, action, isPending] = useActionState(async (prev, formData) => {
    const result = await submit(formData);
    return result.success ? null : result.error;
  }, null);

  return (
    <form action={action}>
      <input name="email" required />
      <button disabled={isPending}>{isPending ? "..." : "Submit"}</button>
      {state && <p className="text-red-500">{state}</p>}
    </form>
  );
}
```

---

## 🏗️ Component Patterns

```tsx
interface Props {
  user: User;
  onEdit?: (user: User) => void;
}

export function UserCard({ user, onEdit }: Props) {
  return (
    <div className="rounded-lg p-4 shadow">
      <h3>{user.name}</h3>
      {onEdit && <button onClick={() => onEdit(user)}>Edit</button>}
    </div>
  );
}
```

---

## 📊 State Management

### Zustand Store

```tsx
import { create } from "zustand";

interface AuthStore {
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

export const useAuth = create<AuthStore>((set) => ({
  user: null,
  login: async (email, password) => {
    const user = await authApi.login(email, password);
    set({ user });
  },
  logout: () => set({ user: null }),
}));
```

### TanStack Query

```tsx
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

export function useUser(id: string) {
  return useQuery({
    queryKey: ["user", id],
    queryFn: () => api.getUser(id),
    staleTime: 5 * 60 * 1000,
  });
}

export function useUpdateUser() {
  const client = useQueryClient();
  return useMutation({
    mutationFn: api.updateUser,
    onSuccess: () => client.invalidateQueries({ queryKey: ["user"] }),
  });
}
```

---

## 🎨 Form Handling

```tsx
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";

const schema = z.object({
  name: z.string().min(2),
  email: z.string().email(),
});

export function UserForm({
  onSubmit,
}: {
  onSubmit: (d: z.infer<typeof schema>) => void;
}) {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({
    resolver: zodResolver(schema),
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register("name")} />
      {errors.name && <span>{errors.name.message}</span>}
      <input {...register("email")} />
      {errors.email && <span>{errors.email.message}</span>}
      <button>Submit</button>
    </form>
  );
}
```

---

## ✅ Best Practices Checklist

- [ ] React 19 Compiler enabled
- [ ] TypeScript strict mode
- [ ] TanStack Query for server state
- [ ] Zustand for client state
- [ ] Suspense for loading states
- [ ] Proper accessibility (a11y)

---

## 📚 External References — Performance Rules

> **Source**: Vercel React Best Practices (57 rules)
> **Rules**: 57 detailed optimization rules across 8 categories

For advanced performance optimization, see [ADVANCED.md](./ADVANCED.md#vercel-performance-rules):

| Priority | Category                   | Impact   | Prefix         |
| -------- | -------------------------- | -------- | -------------- |
| 1        | Eliminating Waterfalls     | CRITICAL | `async-`       |
| 2        | Bundle Size Optimization   | CRITICAL | `bundle-`      |
| 3        | Server-Side Performance    | HIGH     | `server-`      |
| 4        | Client-Side Data Fetching  | HIGH     | `client-`      |
| 5        | Re-render Optimization     | MEDIUM   | `rerender-`    |
| 6        | Third-Party Optimization   | MEDIUM   | `third-party-` |
| 7        | Image & Media Optimization | MEDIUM   | `media-`       |
| 8        | Advanced Patterns          | LOW      | `advanced-`    |

---

_DOMYH Awesome Code • React 19_
