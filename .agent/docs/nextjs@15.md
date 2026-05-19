---
library: nextjs
version: 15
latest: false
category: frontend
official_docs: https://nextjs.org/docs
last_updated: 2026-03-20
source: official docs + crawl4ai/trafilatura extraction
---

# Next.js v15

> Next.js v15 — The React Framework for full-stack web applications.
> ⚠️ This is LEGACY. For latest, use `nextjs.md` (Next.js v16).
> Docs: https://nextjs.org/docs

## Version Comparison

| Feature | v14 | v15 |
|:--------|:----|:----|
| React version | React 18 | React 19 |
| Caching | Aggressive (default ON) | Opt-in (default OFF) |
| `fetch()` caching | Cached by default | No cache by default |
| Route Handlers GET | Cached by default | Dynamic by default |
| Client Router Cache | 30s stale time | 0s stale time |
| Turbopack | Beta | Stable for dev |
| `next/form` | ❌ | ✅ Client-side nav form |
| Partial Prerendering | Experimental | Experimental (improved) |
| `after()` API | ❌ | ✅ Stable |
| `instrumentation.js` | ❌ | ✅ Stable |
| `next.config.ts` | ❌ | ✅ TypeScript config |

## Installation

```bash
npx create-next-app@latest my-app
# Options: TypeScript, ESLint, Tailwind CSS, src/ dir, App Router

# Manual
npm install next@latest react@latest react-dom@latest
```

```json
// package.json scripts
{
  "dev": "next dev --turbopack",
  "build": "next build",
  "start": "next start",
  "lint": "next lint"
}
```

## App Router Structure

```
app/
├── layout.tsx          # Root layout (required)
├── page.tsx            # Home page (/)
├── loading.tsx         # Loading UI (Suspense boundary)
├── error.tsx           # Error boundary
├── not-found.tsx       # 404 page
├── global-error.tsx    # Global error boundary
├── route.ts            # API Route Handler
├── template.tsx        # Re-rendered layout (no state persist)
│
├── blog/
│   ├── page.tsx        # /blog
│   └── [slug]/
│       ├── page.tsx    # /blog/:slug (dynamic)
│       └── opengraph-image.tsx  # OG image generation
│
├── (marketing)/        # Route group (no URL segment)
│   ├── layout.tsx      # Group-specific layout
│   └── about/page.tsx  # /about
│
├── @modal/             # Parallel route (named slot)
│   ├── default.tsx
│   └── login/page.tsx
│
├── api/
│   └── users/
│       └── route.ts    # API: /api/users
│
└── [...catchAll]/      # Catch-all segment
    └── page.tsx
```

## Core API

### Layouts & Pages

```tsx
// app/layout.tsx — Root Layout (required, wraps all pages)
import { Inter } from 'next/font/google';
const inter = Inter({ subsets: ['latin'] });

export const metadata = {
  title: { default: 'My App', template: '%s | My App' },
  description: 'Built with Next.js',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={inter.className}>
      <body>{children}</body>
    </html>
  );
}

// app/page.tsx — Server Component by default
export default async function Home() {
  const data = await fetch("https://api.example.com/data");
  return <main>{/* render data */}</main>;
}

// loading.tsx — automatic Suspense boundary
export default function Loading() {
  return <div className="skeleton">Loading...</div>;
}

// error.tsx — must be client component
"use client";
export default function Error({ error, reset }: { error: Error; reset: () => void }) {
  return (
    <div>
      <h2>Something went wrong!</h2>
      <p>{error.message}</p>
      <button onClick={reset}>Try again</button>
    </div>
  );
}
```

### Data Fetching

```tsx
// Server Component — direct async/await
async function ProductPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const product = await db.product.findUnique({ where: { id } });
  return <div>{product.name}</div>;
}

// Parallel data fetching
async function Dashboard() {
  const [users, posts, analytics] = await Promise.all([
    fetchUsers(),
    fetchPosts(),
    fetchAnalytics(),
  ]);
  return <div>{/* render all */}</div>;
}

// Streaming with Suspense (progressive rendering)
export default async function Page() {
  return (
    <div>
      <h1>Dashboard</h1>
      {/* Fast data loads first */}
      <UserInfo />
      {/* Slow data streams in later */}
      <Suspense fallback={<Skeleton />}>
        <SlowAnalytics />
      </Suspense>
    </div>
  );
}
```

### Server Actions

```tsx
// app/actions.ts
"use server";

import { revalidatePath, revalidateTag } from "next/cache";
import { redirect } from "next/navigation";
import { z } from "zod";

const createPostSchema = z.object({
  title: z.string().min(1).max(200),
  content: z.string().min(1),
});

export async function createPost(prevState: any, formData: FormData) {
  const validatedFields = createPostSchema.safeParse({
    title: formData.get("title"),
    content: formData.get("content"),
  });

  if (!validatedFields.success) {
    return { errors: validatedFields.error.flatten().fieldErrors };
  }

  await db.post.create({ data: validatedFields.data });
  revalidatePath("/posts");
  redirect("/posts");
}

// Non-form Server Action
export async function toggleLike(postId: string) {
  await db.like.toggle({ where: { postId, userId: currentUser.id } });
  revalidateTag("post-likes");
}
```

### Route Handlers

```tsx
// app/api/users/route.ts
import { NextRequest, NextResponse } from "next/server";

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const query = searchParams.get("q");
  const page = parseInt(searchParams.get("page") ?? "1");

  const users = await db.user.findMany({
    where: query ? { name: { contains: query } } : undefined,
    skip: (page - 1) * 20,
    take: 20,
  });

  return NextResponse.json({ users, page });
}

export async function POST(request: NextRequest) {
  const body = await request.json();
  const user = await db.user.create({ data: body });
  return NextResponse.json(user, { status: 201 });
}

// Dynamic route handler
// app/api/users/[id]/route.ts
export async function GET(request: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const user = await db.user.findUnique({ where: { id } });
  if (!user) return NextResponse.json({ error: 'Not found' }, { status: 404 });
  return NextResponse.json(user);
}
```

### Middleware

```tsx
// middleware.ts (project root)
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  // Auth check
  const token = request.cookies.get("session")?.value;
  if (!token && request.nextUrl.pathname.startsWith("/dashboard")) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  // Add custom headers
  const response = NextResponse.next();
  response.headers.set("x-pathname", request.nextUrl.pathname);

  // Geolocation-based redirect
  const country = request.geo?.country;
  if (country === "DE" && !request.nextUrl.pathname.startsWith("/de")) {
    return NextResponse.redirect(new URL(`/de${request.nextUrl.pathname}`, request.url));
  }

  return response;
}

export const config = {
  matcher: [
    '/((?!_next/static|_next/image|favicon.ico|public).*)',
  ],
};
```

### Metadata & SEO

```tsx
// Static metadata
export const metadata = {
  title: "My App",
  description: "Built with Next.js",
  keywords: ["next.js", "react", "typescript"],
  authors: [{ name: "Author" }],
  openGraph: {
    title: "My App",
    description: "...",
    images: ["/og.png"],
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "My App",
  },
  robots: { index: true, follow: true },
};

// Dynamic metadata
export async function generateMetadata({ params }: {
  params: Promise<{ slug: string }>
}): Promise<Metadata> {
  const { slug } = await params;
  const post = await getPost(slug);
  return {
    title: post.title,
    description: post.excerpt,
    openGraph: { images: [post.coverImage] },
  };
}
```

### Caching & Revalidation (v15)

```tsx
// ⚠️ v15: fetch() is NOT cached by default (changed from v14)
// Opt-in to caching:
const data = await fetch(url, { cache: "force-cache" });

// Time-based revalidation
const data = await fetch(url, { next: { revalidate: 3600 } });

// Page-level revalidation
export const revalidate = 60; // revalidate every 60 seconds

// On-demand revalidation
import { revalidatePath, revalidateTag } from "next/cache";
revalidatePath("/posts");       // revalidate entire path
revalidatePath("/posts", "page"); // page only
revalidateTag("posts");         // revalidate by tag

// Tag data for revalidation
const data = await fetch(url, { next: { tags: ["posts"] } });

// unstable_cache for non-fetch data sources
import { unstable_cache } from "next/cache";
const getCachedPosts = unstable_cache(
  async () => db.post.findMany(),
  ["posts"],
  { revalidate: 3600, tags: ["posts"] }
);
```

## Common Patterns

### Dynamic Routes & Static Generation

```tsx
// app/blog/[slug]/page.tsx
export default async function BlogPost({ params }: {
  params: Promise<{ slug: string }>
}) {
  const { slug } = await params;
  const post = await getPost(slug);
  return <article>{post.content}</article>;
}

// Generate static params for SSG
export async function generateStaticParams() {
  const posts = await getAllPosts();
  return posts.map((post) => ({ slug: post.slug }));
}

// Dynamic segment config
export const dynamicParams = true;  // allow non-generated params
// export const dynamic = 'force-static';  // force SSG
// export const dynamic = 'force-dynamic'; // force SSR
```

### Image Optimization

```tsx
import Image from "next/image";

<Image
  src="/hero.jpg"
  alt="Hero"
  width={1200}
  height={600}
  priority        // LCP image — preload
  placeholder="blur"
  blurDataURL={blurHash}
  sizes="(max-width: 768px) 100vw, 50vw"
/>

// Remote images — configure in next.config
// next.config.ts
import type { NextConfig } from 'next';

const config: NextConfig = {
  images: {
    remotePatterns: [
      { protocol: 'https', hostname: '**.example.com' },
    ],
  },
};
```

### Environment Variables

```bash
# .env.local (git-ignored, local development)
DATABASE_URL="postgresql://..."
API_SECRET="secret"

# .env (shared, committed)
NEXT_PUBLIC_API_URL="https://api.example.com"

# ⚠️ NEXT_PUBLIC_ prefix = exposed to client bundle
# Without prefix = server-only (Server Components, Route Handlers, middleware)
```

### Client Component Patterns

```tsx
"use client";
import { useState, useTransition } from "react";
import { useRouter } from "next/navigation";
import { deletePost } from "./actions";

export function DeleteButton({ id }: { id: string }) {
  const [isPending, startTransition] = useTransition();
  const router = useRouter();

  return (
    <button
      disabled={isPending}
      onClick={() => startTransition(async () => {
        await deletePost(id);
        router.refresh(); // refresh server data
      })}
    >
      {isPending ? "Deleting..." : "Delete"}
    </button>
  );
}

// next/form — client-side navigation form
import Form from "next/form";

<Form action="/search">
  <input name="q" placeholder="Search..." />
  <button type="submit">Search</button>
</Form>
// Navigates to /search?q=... with client-side transition
```

### Parallel Routes & Intercepting Routes

```tsx
// Parallel routes: @slot directories
// app/layout.tsx
export default function Layout({
  children,
  modal,
}: {
  children: React.ReactNode;
  modal: React.ReactNode;
}) {
  return (
    <>
      {children}
      {modal}
    </>
  );
}

// app/@modal/login/page.tsx — shown alongside main content
// app/@modal/default.tsx — returns null when no modal

// Intercepting routes: (.)folder, (..)folder, (...)folder
// app/@modal/(.)photo/[id]/page.tsx — intercepts /photo/[id]
```

## Turbopack (Stable)

```bash
# Use Turbopack for faster dev server (stable in v15)
next dev --turbopack

# next.config.ts — no extra config needed
# Turbopack is drop-in replacement for webpack in dev
```

## Partial Prerendering (PPR)

```tsx
// Combine static shell with dynamic content in same route
// Static parts prerendered at build, dynamic streamed at request

// next.config.ts
const config = { experimental: { ppr: 'incremental' } };

// app/page.tsx
export const experimental_ppr = true;

export default function Page() {
  return (
    <div>
      <h1>Static Header</h1>  {/* Prerendered */}
      <Suspense fallback={<Skeleton />}>
        <DynamicContent />     {/* Streamed at request */}
      </Suspense>
    </div>
  );
}
```

## Instrumentation

```ts
// instrumentation.ts (root) — runs once on server startup
export async function register() {
  if (process.env.NEXT_RUNTIME === 'nodejs') {
    // Init monitoring, DB connections, etc.
    await initMonitoring();
  }
}
```

## next.config.ts

```ts
import type { NextConfig } from 'next';

const config: NextConfig = {
  // Images
  images: {
    remotePatterns: [
      { protocol: 'https', hostname: '**.example.com' },
    ],
  },
  // Redirects
  async redirects() {
    return [
      { source: '/old-path', destination: '/new-path', permanent: true },
    ];
  },
  // Rewrites
  async rewrites() {
    return [
      { source: '/api/:path*', destination: 'https://backend.example.com/:path*' },
    ];
  },
  // Headers
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          { key: 'X-Frame-Options', value: 'DENY' },
        ],
      },
    ];
  },
  // Experimental
  experimental: {
    ppr: 'incremental',  // Partial Prerendering
  },
};
export default config;
```

## after() API (v15)

```tsx
import { after } from 'next/server';

export async function POST(request: NextRequest) {
  const data = await request.json();
  await db.save(data);

  // Run after response is sent — doesn't block user
  after(async () => {
    await analytics.track('data_saved', { id: data.id });
    await sendNotification(data);
  });

  return NextResponse.json({ ok: true });
}
```

## Navigation

```tsx
import Link from 'next/link';
import { useRouter, usePathname, useSearchParams } from 'next/navigation';

// Link — client-side navigation with prefetching
<Link href="/about">About</Link>
<Link href={`/blog/${post.slug}`} prefetch={false}>Read More</Link>
<Link href={{ pathname: '/search', query: { q: 'nextjs' } }}>Search</Link>

// useRouter — programmatic navigation
const router = useRouter();
router.push('/dashboard');
router.replace('/login');
router.back();
router.refresh();  // refresh server data without full reload

// usePathname
const pathname = usePathname();  // '/blog/hello'

// useSearchParams (client component only)
const searchParams = useSearchParams();
const q = searchParams.get('q');  // 'nextjs'
```

## Gotchas & Breaking Changes

⚠️ **v15**: `params` and `searchParams` are now **Promises** — must `await`.

⚠️ **v15**: `fetch()` default changed from `force-cache` to `no-store`.

⚠️ **v15**: Route Handlers `GET` are dynamic by default (not cached).

⚠️ **v15**: Client Router Cache `staleTime` changed from 30s to 0.

⚠️ **Server vs Client**: Cannot import Server Component into Client Component. Pass as `children`.

⚠️ **`"use server"`**: Only marks functions as Server Actions, NOT Server Components (Server is default).

⚠️ **`NEXT_PUBLIC_`**: Only variables with this prefix are exposed to client-side code.

⚠️ **`next.config.ts`** (v15): TypeScript config supported — use `NextConfig` type.

⚠️ **`after()` API**: Runs code after response is sent (logging, analytics) without blocking.

⚠️ **Middleware**: Runs on Edge Runtime — limited Node.js APIs. Cannot use `fs`, heavy npm packages.

⚠️ **Turbopack**: Use `next dev --turbopack` for faster dev builds. Stable in v15.

⚠️ **PPR**: `experimental_ppr = true` — static shell + dynamic streaming in same route.
