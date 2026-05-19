---
library: nuxt
version: 3
latest: false
category: frontend
official_docs: https://nuxt.com/docs/3.x
last_updated: 2026-03-20
---

# Nuxt v3

> Nuxt 3 — The Intuitive Vue Framework, built on Vue 3 + Nitro.
> Current: v3.15+ | Next: v4.x
> Docs: https://nuxt.com/docs/3.x

## Installation

```bash
npx nuxi@3 init my-app
cd my-app
npm install
npm run dev
```

## Directory Structure (v3)

```
my-app/
├── pages/                # ← at root (NOT app/pages/ like v4)
│   ├── index.vue
│   ├── about.vue
│   └── posts/
│       └── [id].vue
├── components/           # Auto-imported
├── composables/          # Auto-imported
├── layouts/              # Layout components
├── middleware/            # Route middleware
├── plugins/              # Nuxt plugins
├── assets/               # Processed by Vite
├── server/
│   ├── api/              # API routes
│   ├── routes/           # Server routes
│   ├── middleware/        # Server middleware
│   └── utils/            # Server utilities
├── public/               # Static files
├── app.vue               # ← at root (NOT app/app.vue like v4)
├── nuxt.config.ts
└── app.config.ts
```

## Configuration

```ts
// nuxt.config.ts
export default defineNuxtConfig({
  runtimeConfig: {
    apiSecret: '',
    public: {
      apiBase: '/api',
    },
  },

  modules: [
    '@pinia/nuxt',
    '@nuxtjs/tailwindcss',
  ],

  app: {
    head: {
      title: 'My Nuxt 3 App',
      meta: [
        { name: 'description', content: 'My Nuxt 3 app' },
      ],
    },
  },

  typescript: {
    strict: true,
  },

  // No $production/$development overrides in v3
  // Use environment variables instead
});
```

## Routing (Same as v4 but root pages/)

```vue
<!-- pages/index.vue → / -->
<template>
  <div>
    <NuxtLink to="/about">About</NuxtLink>
  </div>
</template>

<!-- pages/posts/[id].vue → /posts/:id -->
<script setup lang="ts">
const route = useRoute();
const id = route.params.id;
</script>
```

### Route Middleware

```ts
// middleware/auth.ts
export default defineNuxtRouteMiddleware((to, from) => {
  const { authenticated } = storeToRefs(useAuthStore());
  if (!authenticated.value) {
    return navigateTo('/login');
  }
});
```

## Data Fetching

```vue
<script setup lang="ts">
// useFetch — SSR-safe
const { data, pending, error, refresh } = await useFetch('/api/posts');
// Note: v3 uses `pending` (v4 renamed to `status`)

// useAsyncData
const { data: user } = await useAsyncData('user', () => {
  return $fetch(`/api/users/${route.params.id}`);
});

// useLazyFetch — non-blocking
const { data, pending } = useLazyFetch('/api/posts');
// No await — doesn't block navigation
</script>

<template>
  <div v-if="pending">Loading...</div>
  <div v-else-if="error">Error: {{ error.message }}</div>
  <div v-else>{{ data }}</div>
</template>
```

## Server (Nitro — Same as v4)

```ts
// server/api/hello.ts
export default defineEventHandler((event) => {
  return { message: 'Hello!' };
});

// server/api/posts.post.ts
export default defineEventHandler(async (event) => {
  const body = await readBody(event);
  return { created: body };
});
```

## State Management

```vue
<script setup lang="ts">
// useState — SSR-friendly reactive state
const counter = useState('counter', () => 0);
</script>
```

## SEO & Meta

```vue
<script setup lang="ts">
useHead({
  title: 'My Page',
  meta: [{ name: 'description', content: 'Description' }],
});

// useSeoMeta (v3.12+)
useSeoMeta({
  title: 'My Page',
  ogTitle: 'My Page',
  description: 'Page description',
  ogImage: 'https://example.com/og.png',
});
</script>
```

## Key Differences: v3 → v4

| Aspect | v3 | v4 |
|:-------|:---|:---|
| Directory | `pages/` at root | `app/pages/` |
| Root component | `app.vue` at root | `app/app.vue` |
| Return values | `pending` (boolean) | `status` ('idle'\|'pending'\|'success'\|'error') |
| Env overrides | Not supported | `$production`, `$development`, `$env` |
| Vue minimum | Vue 3.3+ | Vue 3.5+ |
| Config flag | N/A | `compatibilityVersion: 4` |
| `useLazyFetch` | ✅ Separate function | ✅ Use `lazy: true` option |

## Gotchas

⚠️ **v3 → v4 migration**: Move `pages/`, `components/`, `composables/` into `app/` directory.

⚠️ **`pending` vs `status`**: v3 uses `pending: boolean`, v4 uses `status: string` for data fetching.

⚠️ **`useLazyFetch`**: Still works in v3 as separate composable. In v4, use `useFetch({ lazy: true })`.

⚠️ **No env overrides**: v3 doesn't support `$production`/`$development` in nuxt.config.

⚠️ **Auto-import**: Same as v4 — components, composables, utils auto-imported.

⚠️ **Nitro server**: Same as v4 — `server/api/` for API routes, `defineEventHandler`.
