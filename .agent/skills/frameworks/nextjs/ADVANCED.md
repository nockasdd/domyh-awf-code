# Next.js — Advanced Patterns


## Table of Contents

- [Server Components](#server-components)
- [Data Fetching](#data-fetching)
- [Caching & Revalidation](#caching--revalidation)
- [Middleware & Edge](#middleware--edge)

---

## Server Components

### Server Functions

```tsx
// actions.ts
"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";

export async function createOrder(formData: FormData) {
  const product = formData.get("product") as string;
  const quantity = Number(formData.get("quantity"));

  // Direct database access - runs on server only
  const order = await db.order.create({
    data: { product, quantity },
  });

  revalidatePath("/orders");
  redirect(`/orders/${order.id}`);
}

// Component using action
export default function OrderForm() {
  return (
    <form action={createOrder}>
      <input name="product" required />
      <input name="quantity" type="number" required />
      <button type="submit">Create Order</button>
    </form>
  );
}
```

### Streaming & Suspense

```tsx
import { Suspense } from "react";

export default async function Page() {
  return (
    <main>
      <h1>Dashboard</h1>

      {/* Fast component renders immediately */}
      <QuickStats />

      {/* Slow components stream in */}
      <Suspense fallback={<ChartSkeleton />}>
        <SlowChart />
      </Suspense>

      <Suspense fallback={<TableSkeleton />}>
        <SlowDataTable />
      </Suspense>
    </main>
  );
}

// loading.tsx - Automatic Suspense boundary
export default function Loading() {
  return <DashboardSkeleton />;
}
```

---

## Data Fetching

### Parallel Data Fetching

```tsx
async function Page({ params }: { params: { id: string } }) {
  // Parallel fetching - don't await sequentially
  const userPromise = fetchUser(params.id);
  const postsPromise = fetchPosts(params.id);
  const statsPromise = fetchStats(params.id);

  const [user, posts, stats] = await Promise.all([
    userPromise,
    postsPromise,
    statsPromise,
  ]);

  return <Profile user={user} posts={posts} stats={stats} />;
}
```

### Data Preloading

```tsx
// preload pattern for waterfalls
import { preload } from "react-dom";

export function preloadUserData(id: string) {
  preloadUser(id);
  preloadPosts(id);
}

// In parent component
export default function Layout({ children }) {
  const id = useParams().id;
  preloadUserData(id); // Start fetching before children render
  return children;
}
```

---

## Caching & Revalidation

### Cache Strategies

```tsx
// Time-based revalidation
async function getProducts() {
  const res = await fetch("https://api.example.com/products", {
    next: { revalidate: 3600 }, // Revalidate every hour
  });
  return res.json();
}

// On-demand revalidation
// In Server Function or Route Handler
import { revalidatePath, revalidateTag } from "next/cache";

export async function updateProduct(id: string, data: ProductData) {
  await db.product.update({ where: { id }, data });

  // Revalidate specific path
  revalidatePath(`/products/${id}`);

  // Or by tag
  revalidateTag("products");
}

// Tagged fetch
async function getProduct(id: string) {
  const res = await fetch(`/api/products/${id}`, {
    next: { tags: ["products", `product-${id}`] },
  });
  return res.json();
}
```

### Unstable Cache

```tsx
import { unstable_cache } from "next/cache";

const getCachedUser = unstable_cache(
  async (id: string) => {
    return await db.user.findUnique({ where: { id } });
  },
  ["user"],
  { revalidate: 300, tags: ["users"] },
);
```

---

## Middleware & Edge

### Middleware

```tsx
// middleware.ts
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  const token = request.cookies.get("token")?.value;

  // Auth check
  if (!token && request.nextUrl.pathname.startsWith("/dashboard")) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  // Add headers
  const response = NextResponse.next();
  response.headers.set("x-request-id", crypto.randomUUID());

  return response;
}

export const config = {
  matcher: ["/dashboard/:path*", "/api/:path*"],
};
```

### Edge Runtime

```tsx
// app/api/geo/route.ts
export const runtime = "edge";

export async function GET(request: Request) {
  const { geo } = request;

  return Response.json({
    country: geo?.country,
    city: geo?.city,
    region: geo?.region,
  });
}
```

---
