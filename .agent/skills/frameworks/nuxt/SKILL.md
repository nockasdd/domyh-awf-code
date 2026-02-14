---
name: nuxt
detect: ["nuxt.config.ts", "nuxt.config.js", ".nuxtrc", "app.vue"]
version: "6.2.7"
category: frontend
tier: 1
---

# Nuxt Patterns — DOMYH Awesome Code

> **Version**: Nuxt 4.x (4.0 Jul 2025, latest 4.3.1)
> **Philosophy**: Full-stack Vue, hybrid rendering, DX-first

---

## 🎯 When to Use This Skill

Use for: Full-stack Vue apps, SSR, SSG, hybrid rendering.
**NOT for**: Static sites only (→ vue), non-Vue (→ nextjs).

---

## 📦 Recommended Stack (2025-2026)

### Core

| Tool       | Use Case          |
| ---------- | ----------------- |
| **Nuxt 4** | Full-stack Vue 🏆 |
| **Nitro**  | Server engine     |
| **Vite**   | Dev bundler       |

### State & Data

| Library                 | Use Case            |
| ----------------------- | ------------------- |
| **Pinia**               | State management 🏆 |
| **VueUse**              | Composables         |
| **@tanstack/vue-query** | Server state        |

### IDE Support

| IDE                 | Features                   |
| ------------------- | -------------------------- |
| **VS Code + Volar** | Full TypeScript support 🏆 |
| **Nuxtr extension** | Nuxt-specific tooling      |
| **WebStorm**        | Built-in Nuxt support      |

---

## 🆕 Nuxt 4 Features (2025)

### New Directory Structure

```
my-app/
├── app/                    # 🆕 Main app code
│   ├── components/
│   ├── composables/
│   ├── layouts/
│   ├── pages/
│   ├── plugins/
│   └── app.vue
├── server/                 # Server code
│   ├── api/
│   ├── middleware/
│   └── routes/
├── shared/                 # 🆕 Shared across client/server
├── public/
├── nuxt.config.ts
└── package.json
```

### Enhanced Data Fetching

```typescript
// ✅ Nuxt 4: Improved useFetch with auto-sharing
const {
  data: users,
  pending,
  error,
  refresh,
} = await useFetch("/api/users", {
  key: "users", // Auto-deduplication
  default: () => [], // Default value
  getCachedData: (key) => {
    // Custom cache
    return nuxtApp.payload.data[key];
  },
});

// ✅ Reactive keys - auto-refetch when params change
const userId = ref(1);
const { data: user } = await useFetch(() => `/api/users/${userId.value}`);

// ✅ useAsyncData for computed fetch logic
const { data } = await useAsyncData("user-profile", async () => {
  const user = await $fetch("/api/me");
  const posts = await $fetch(`/api/users/${user.id}/posts`);
  return { user, posts };
});
```

### Server Routes

```typescript
// server/api/users/[id].get.ts
export default defineEventHandler(async (event) => {
  const id = getRouterParam(event, "id");

  // Validate
  if (!id || isNaN(Number(id))) {
    throw createError({
      statusCode: 400,
      message: "Invalid user ID",
    });
  }

  const user = await db.user.findUnique({
    where: { id: Number(id) },
  });

  if (!user) {
    throw createError({
      statusCode: 404,
      message: "User not found",
    });
  }

  return user;
});

// ✅ Cached event handler for expensive operations
export default cachedEventHandler(
  async (event) => {
    return await expensiveComputation();
  },
  {
    maxAge: 60 * 60, // 1 hour
    swr: true, // Stale-while-revalidate
  },
);
```

---

## 🔧 Core Patterns

### Page Component

```vue
<!-- pages/users/[id].vue -->
<script setup lang="ts">
definePageMeta({
  middleware: "auth",
  layout: "dashboard",
});

const route = useRoute();
const {
  data: user,
  pending,
  error,
} = await useFetch(`/api/users/${route.params.id}`);

// SEO
useSeoMeta({
  title: () => user.value?.name ?? "User",
  description: () => `Profile for ${user.value?.name}`,
});
</script>

<template>
  <div v-if="pending">Loading...</div>
  <div v-else-if="error">{{ error.message }}</div>
  <UserProfile v-else :user="user!" />
</template>
```

### Middleware

```typescript
// middleware/auth.ts
export default defineNuxtRouteMiddleware((to, from) => {
  const user = useSupabaseUser(); // or your auth composable

  // ⚠️ Always use to/from, NOT useRoute()
  if (!user.value && to.path !== "/login") {
    return navigateTo("/login", {
      redirectCode: 302,
    });
  }
});

// middleware/admin.ts
export default defineNuxtRouteMiddleware(async (to) => {
  const { data } = await useFetch("/api/me");

  if (data.value?.role !== "admin") {
    throw createError({
      statusCode: 403,
      message: "Admin access required",
    });
  }
});
```

### Server Components (Islands)

```vue
<!-- components/HeavySyntaxHighlighter.server.vue -->
<script setup lang="ts">
// 🆕 Server-only component - no client JS
import { highlight } from "shikiji";

const props = defineProps<{
  code: string;
  lang: string;
}>();

const html = await highlight(props.code, {
  lang: props.lang,
  theme: "github-dark",
});
</script>

<template>
  <div v-html="html" />
</template>
```

---

## 🚀 Hybrid Rendering

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  routeRules: {
    // Static generation
    "/": { prerender: true },
    "/blog/**": { swr: 3600 }, // ISR: 1 hour

    // Client-side only
    "/dashboard/**": { ssr: false },

    // Server-side
    "/api/**": { cors: true },

    // Cache headers
    "/assets/**": { headers: { "cache-control": "max-age=31536000" } },
  },
});
```

---

## ✅ Best Practices Checklist

### Data Fetching

- [ ] Use `useFetch` over `$fetch` in components
- [ ] Provide `key` for deduplication
- [ ] Set `default` values
- [ ] Handle `pending` and `error` states

### Performance

- [ ] Use server components for static content
- [ ] Configure proper routeRules
- [ ] Cache expensive API handlers
- [ ] Lazy load heavy components

### Security

- [ ] Validate all route params
- [ ] Use `createError` for proper errors
- [ ] Implement proper middleware
- [ ] Never trust client data

---

_DOMYH Awesome Code • Nuxt 4_
