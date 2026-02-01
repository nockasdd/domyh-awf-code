---
name: nextjs
detect:
  ["next.config.js", "next.config.mjs", "next.config.ts", "app/layout.tsx"]
version: "4.3.0"
category: frontend
tier: 1
---

# Next.js Patterns — DOMYH Awesome Code v4.3

> **Version**: Next.js 15/16 (2025-2026)
> **Runtime**: React meta-framework with App Router
> **Philosophy**: Server-first, zero-config, progressive enhancement

---

## 🎯 When to Use This Skill

Use for: React SSR/SSG apps, Server Components, App Router, API routes, Turbopack builds.
**NOT for**: Pure React SPA (→ react skill), Node.js backend only (→ nodejs skill).

---

## 📦 Recommended Stack (2025-2026)

### Core

| Library             | Use Case                  | Version  |
| ------------------- | ------------------------- | -------- |
| **Next.js 15/16**   | App Router 🏆             | ^15.0    |
| **React 19**        | Server Components         | ^19.0    |
| **TypeScript 5.5+** | Type safety               | ^5.5     |
| **Turbopack**       | Fast bundler (default 16) | Built-in |

### UI & Styling

| Library            | Use Case            | Install                  |
| ------------------ | ------------------- | ------------------------ |
| **shadcn/ui**      | Radix + Tailwind 🏆 | `npx shadcn@latest init` |
| **Tailwind CSS 4** | Utility CSS         | `npm i tailwindcss@next` |
| **Framer Motion**  | Animations          | `npm i framer-motion`    |

### Data & State

| Library            | Use Case        | Install                       |
| ------------------ | --------------- | ----------------------------- |
| **TanStack Query** | Server state 🏆 | `npm i @tanstack/react-query` |
| **Zustand**        | Client state    | `npm i zustand`               |
| **Prisma**         | Database ORM    | `npm i prisma @prisma/client` |
| **Drizzle**        | Lightweight ORM | `npm i drizzle-orm`           |

### Auth

| Library            | Use Case           | Install                |
| ------------------ | ------------------ | ---------------------- |
| **NextAuth.js v5** | Full-featured auth | `npm i next-auth@beta` |
| **Clerk**          | Auth-as-a-service  | `npm i @clerk/nextjs`  |

### IDE Support

| IDE          | Extension                         | Features                      |
| ------------ | --------------------------------- | ----------------------------- |
| **VS Code**  | ESLint, Tailwind CSS IntelliSense | Auto-format, class sorting 🏆 |
| **WebStorm** | Built-in                          | Full Next.js support          |

---

## 🏗️ Next.js 15/16 New Features

### Turbopack (Default in 16)

```bash
# ✅ 2-5x faster production builds
# ✅ 10x faster Fast Refresh
# No configuration needed in Next.js 16

# Enable FS cache for even faster builds (beta)
# next.config.ts
export default {
  experimental: {
    turbopack: {
      fileSystemCache: true,
    }
  }
}
```

### Async Request APIs (15+)

```tsx
// app/users/[id]/page.tsx
// ✅ params is now a Promise
export default async function UserPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const user = await fetchUser(id);
  return <UserProfile user={user} />;
}

// ✅ searchParams is also a Promise
export default async function SearchPage({
  searchParams,
}: {
  searchParams: Promise<{ q?: string }>;
}) {
  const { q } = await searchParams;
  const results = await search(q);
  return <SearchResults results={results} />;
}
```

---

## 📁 Project Structure

```
my-app/
├── app/
│   ├── layout.tsx          # Root layout
│   ├── page.tsx             # Home page
│   ├── loading.tsx          # Loading UI
│   ├── error.tsx            # Error boundary
│   ├── not-found.tsx        # 404 page
│   ├── (auth)/              # Route group (no URL segment)
│   │   ├── login/page.tsx
│   │   └── register/page.tsx
│   ├── dashboard/
│   │   ├── layout.tsx       # Nested layout
│   │   ├── page.tsx
│   │   └── settings/page.tsx
│   └── api/
│       └── users/route.ts   # API route
├── components/
│   ├── ui/                  # shadcn components
│   └── features/            # Feature components
├── lib/
│   ├── db.ts                # Database client
│   └── utils.ts             # Utilities
├── public/
├── next.config.ts
└── tailwind.config.ts
```

---

## 🔧 Server Components (Default)

### Data Fetching in Server Components

```tsx
// app/posts/page.tsx
// ✅ Server Component - default, no directive needed
import { db } from "@/lib/db";

export default async function PostsPage() {
  // Direct database access - no API needed
  const posts = await db.post.findMany({
    orderBy: { createdAt: "desc" },
    take: 10,
  });

  return (
    <div>
      {posts.map((post) => (
        <PostCard key={post.id} post={post} />
      ))}
    </div>
  );
}

// ✅ Static metadata
export const metadata = {
  title: "Posts",
  description: "All blog posts",
};

// ✅ Dynamic metadata
export async function generateMetadata({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const post = await getPost(id);
  return {
    title: post.title,
    openGraph: { images: [post.image] },
  };
}
```

### Caching Strategies

```tsx
// ✅ Static (cached indefinitely)
const data = await fetch(url);

// ✅ Revalidate every 60 seconds (ISR)
const data = await fetch(url, {
  next: { revalidate: 60 },
});

// ✅ No cache (always fresh)
const data = await fetch(url, {
  cache: "no-store",
});

// ✅ Cached function with unstable_cache
import { unstable_cache } from "next/cache";

const getCachedUser = unstable_cache(
  async (id: string) => db.user.findUnique({ where: { id } }),
  ["user"],
  { revalidate: 3600, tags: ["users"] },
);

// ✅ Revalidate on demand
import { revalidatePath, revalidateTag } from "next/cache";

export async function updateUser(id: string, data: UserData) {
  await db.user.update({ where: { id }, data });
  revalidatePath(`/users/${id}`);
  revalidateTag("users");
}
```

---

## 🎨 Client Components

```tsx
"use client";

import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

// ✅ Mark with "use client" for interactivity
export function UserForm({ userId }: { userId: string }) {
  const queryClient = useQueryClient();

  const { data: user, isLoading } = useQuery({
    queryKey: ["user", userId],
    queryFn: () => fetch(`/api/users/${userId}`).then((r) => r.json()),
  });

  const mutation = useMutation({
    mutationFn: (data: FormData) =>
      fetch(`/api/users/${userId}`, {
        method: "PATCH",
        body: data,
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["user", userId] });
    },
  });

  if (isLoading) return <Skeleton />;

  return (
    <form action={mutation.mutate}>
      <input name="name" defaultValue={user.name} />
      <button type="submit" disabled={mutation.isPending}>
        {mutation.isPending ? "Saving..." : "Save"}
      </button>
    </form>
  );
}
```

---

## ⚡ Server Actions

```tsx
// app/actions.ts
"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { z } from "zod";

const UserSchema = z.object({
  name: z.string().min(2),
  email: z.string().email(),
});

export async function createUser(formData: FormData) {
  // ✅ Validate input
  const validated = UserSchema.parse({
    name: formData.get("name"),
    email: formData.get("email"),
  });

  // ✅ Database operation
  const user = await db.user.create({
    data: validated,
  });

  // ✅ Revalidate cache
  revalidatePath("/users");

  // ✅ Redirect
  redirect(`/users/${user.id}`);
}

// ✅ useOptimistic for instant UI feedback (React 19)
("use client");
import { useOptimistic } from "react";

export function LikeButton({ likes }: { likes: number }) {
  const [optimisticLikes, addOptimisticLike] = useOptimistic(
    likes,
    (state) => state + 1,
  );

  async function handleLike() {
    addOptimisticLike(null); // Instant UI update
    await likePost(); // Server action
  }

  return <button onClick={handleLike}>❤️ {optimisticLikes}</button>;
}
```

---

## 🛡️ Middleware

```tsx
// middleware.ts
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // ✅ Auth check
  const token = request.cookies.get("token");
  if (pathname.startsWith("/dashboard") && !token) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  // ✅ Add headers
  const response = NextResponse.next();
  response.headers.set("x-pathname", pathname);

  return response;
}

export const config = {
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico).*)"],
};
```

---

## 🔌 API Routes

```tsx
// app/api/users/route.ts
import { NextRequest, NextResponse } from "next/server";

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const page = parseInt(searchParams.get("page") || "1");

  const users = await db.user.findMany({
    skip: (page - 1) * 10,
    take: 10,
  });

  return NextResponse.json(users);
}

export async function POST(request: NextRequest) {
  const body = await request.json();

  const user = await db.user.create({ data: body });

  return NextResponse.json(user, { status: 201 });
}

// app/api/users/[id]/route.ts
export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> },
) {
  const { id } = await params;
  const user = await db.user.findUnique({ where: { id } });

  if (!user) {
    return NextResponse.json({ error: "Not found" }, { status: 404 });
  }

  return NextResponse.json(user);
}
```

---

## 📊 Loading & Error States

```tsx
// app/dashboard/loading.tsx
export default function Loading() {
  return (
    <div className="animate-pulse">
      <div className="h-8 bg-gray-200 rounded w-1/4 mb-4" />
      <div className="h-4 bg-gray-200 rounded w-full mb-2" />
      <div className="h-4 bg-gray-200 rounded w-3/4" />
    </div>
  );
}

// app/dashboard/error.tsx
("use client");

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <div className="p-4 bg-red-50 rounded-lg">
      <h2 className="text-red-800 font-bold">Something went wrong!</h2>
      <p className="text-red-600">{error.message}</p>
      <button
        onClick={reset}
        className="mt-4 px-4 py-2 bg-red-600 text-white rounded"
      >
        Try again
      </button>
    </div>
  );
}
```

---

## ✅ Best Practices Checklist

### Architecture

- [ ] Server Components by default
- [ ] Client Components only for interactivity
- [ ] Feature-based file organization
- [ ] Parallel data fetching with Promise.all

### Performance

- [ ] Image optimization with next/image
- [ ] Font optimization with next/font
- [ ] Route prefetching enabled
- [ ] Suspense boundaries for streaming

### Security

- [ ] Environment variables for secrets
- [ ] Input validation with Zod
- [ ] CSRF protection in Server Actions
- [ ] Middleware for auth

### SEO

- [ ] Metadata configured per page
- [ ] OpenGraph images
- [ ] Sitemap generated
- [ ] robots.txt configured

---

_DOMYH Awesome Code v4.3 • Next.js 15/16_
