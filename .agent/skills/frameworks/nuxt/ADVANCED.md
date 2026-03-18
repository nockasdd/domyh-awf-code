# Nuxt — Advanced Patterns

## Table of Contents

- [Nitro Server Engine](#nitro-server-engine)
- [Server Routes API](#server-routes-api)
- [Advanced Rendering](#advanced-rendering)
- [SEO & Meta](#seo--meta)
- [Middleware Patterns](#middleware-patterns)
- [Module Development](#module-development)
- [Performance](#performance)

---

## Nitro Server Engine

### Event Handlers

```typescript
// server/api/users/[id].get.ts
export default defineEventHandler(async (event) => {
  const id = getRouterParam(event, 'id')
  const query = getQuery(event) // ?fields=name,email

  const user = await useStorage('db').getItem(`user:${id}`)
  if (!user) {
    throw createError({ statusCode: 404, message: 'User not found' })
  }

  return user
})

// server/api/users.post.ts
export default defineEventHandler(async (event) => {
  const body = await readValidatedBody(event, (data) => {
    // Validate with zod
    return userSchema.parse(data)
  })

  const user = await createUser(body)
  setResponseStatus(event, 201)
  return user
})
```

### Nitro Storage (KV)

```typescript
// server/utils/cache.ts
export async function getCachedData<T>(key: string, fetcher: () => Promise<T>, ttl = 3600) {
  const storage = useStorage('cache')
  const cached = await storage.getItem<T>(key)

  if (cached) return cached

  const data = await fetcher()
  await storage.setItem(key, data, { ttl })
  return data
}

// nitro.config — multi-driver storage
export default defineNitroConfig({
  storage: {
    cache: { driver: 'redis', base: 'cache:', url: process.env.REDIS_URL },
    db: { driver: 'fs', base: '.data/db' },
  },
})
```

### Nitro Tasks (Background Jobs)

```typescript
// server/tasks/cleanup.ts
export default defineTask({
  meta: { name: 'db:cleanup', description: 'Clean expired sessions' },
  run({ payload }) {
    const deleted = await deleteExpiredSessions()
    return { result: { deleted } }
  },
})

// Trigger from API
export default defineEventHandler(async (event) => {
  await runTask('db:cleanup', { payload: {} })
  return { status: 'ok' }
})
```

---

## Server Routes API

### REST API with Validation

```typescript
// server/api/posts/index.get.ts
export default defineEventHandler(async (event) => {
  const query = getValidatedQuery(event, (q) =>
    z.object({
      page: z.coerce.number().default(1),
      limit: z.coerce.number().max(100).default(20),
      sort: z.enum(['created', 'updated']).default('created'),
    }).parse(q)
  )

  const { page, limit, sort } = query
  const offset = (page - 1) * limit

  return await db.select().from(posts)
    .orderBy(desc(posts[sort]))
    .limit(limit)
    .offset(offset)
})
```

### Error Handling

```typescript
// server/utils/errors.ts
export class AppError extends Error {
  statusCode: number
  constructor(message: string, statusCode = 400) {
    super(message)
    this.statusCode = statusCode
  }
}

// server/middleware/error.ts
export default defineEventHandler((event) => {
  event.context.onError = (error: Error) => {
    if (error instanceof AppError) {
      setResponseStatus(event, error.statusCode)
      return { error: error.message }
    }
    setResponseStatus(event, 500)
    return { error: 'Internal server error' }
  }
})
```

---

## Advanced Rendering

### Hybrid Rendering (Route Rules)

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  routeRules: {
    '/':           { prerender: true },                // SSG at build time
    '/blog/**':    { isr: 3600 },                      // ISR: revalidate every hour
    '/api/**':     { cors: true, headers: { 'X-API': 'v1' } },
    '/admin/**':   { ssr: false },                     // SPA only
    '/old-page':   { redirect: '/new-page' },          // 301 redirect
    '/dashboard':  { swr: 600 },                       // Stale-while-revalidate
  },
})
```

### Island Components (Selective Hydration)

```vue
<!-- components/HeavyChart.server.vue -->
<script setup lang="ts">
// Only runs on server — zero JS shipped to client
const data = await $fetch('/api/analytics')
</script>

<template>
  <NuxtIsland name="HeavyChart" :props="{ data }" />
</template>
```

---

## SEO & Meta

### Composable Pattern

```typescript
// composables/useSEO.ts
export function useSEO(options: {
  title: string
  description: string
  image?: string
  type?: string
}) {
  useHead({
    title: options.title,
    meta: [
      { name: 'description', content: options.description },
      { property: 'og:title', content: options.title },
      { property: 'og:description', content: options.description },
      { property: 'og:image', content: options.image || '/og-default.png' },
      { property: 'og:type', content: options.type || 'website' },
      { name: 'twitter:card', content: 'summary_large_image' },
    ],
    link: [
      { rel: 'canonical', href: `https://example.com${useRoute().path}` },
    ],
  })
}

// Usage in page
useSEO({
  title: 'My Page',
  description: 'Page description for search engines',
  image: '/images/page-og.png',
})
```

### Structured Data (JSON-LD)

```typescript
useHead({
  script: [{
    type: 'application/ld+json',
    innerHTML: JSON.stringify({
      '@context': 'https://schema.org',
      '@type': 'Article',
      headline: article.title,
      datePublished: article.createdAt,
      author: { '@type': 'Person', name: article.author },
    }),
  }],
})
```

---

## Middleware Patterns

### Auth Middleware

```typescript
// middleware/auth.ts
export default defineNuxtRouteMiddleware(async (to) => {
  const { loggedIn, user } = useUserSession()

  if (!loggedIn.value) {
    return navigateTo('/login', { redirectCode: 301 })
  }

  // Role-based access
  if (to.meta.requiredRole && user.value?.role !== to.meta.requiredRole) {
    return abortNavigation(createError({ statusCode: 403 }))
  }
})

// pages/admin.vue — apply middleware
definePageMeta({
  middleware: 'auth',
  requiredRole: 'admin',
})
```

### Server Middleware (Global)

```typescript
// server/middleware/01.cors.ts
export default defineEventHandler((event) => {
  setResponseHeaders(event, {
    'Access-Control-Allow-Origin': process.env.ALLOWED_ORIGIN || '*',
    'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
  })

  if (getMethod(event) === 'OPTIONS') {
    setResponseStatus(event, 204)
    return ''
  }
})
```

---

## Module Development

### Custom Module

```typescript
// modules/analytics/index.ts
import { defineNuxtModule, addPlugin, createResolver } from '@nuxt/kit'

export default defineNuxtModule({
  meta: { name: 'analytics', configKey: 'analytics' },
  defaults: { trackingId: '', debug: false },

  setup(options, nuxt) {
    const { resolve } = createResolver(import.meta.url)

    // Add runtime plugin
    addPlugin(resolve('./runtime/plugin'))

    // Add composables
    addImportsDir(resolve('./runtime/composables'))

    // Add server routes
    addServerHandler({
      route: '/api/_analytics',
      handler: resolve('./runtime/server/api/collect'),
    })

    // Hook into build
    nuxt.hook('build:before', () => {
      console.log(`Analytics: ${options.trackingId}`)
    })
  },
})
```

---

## Performance

### Payload Optimization

```typescript
// Reduce payload size with pick()
const { data } = await useFetch('/api/users', {
  pick: ['id', 'name', 'avatar'],  // Only serialize these fields
  transform: (users) => users.slice(0, 10),  // Limit on client
})

// Lazy loading heavy components
const HeavyEditor = defineAsyncComponent(() =>
  import('~/components/HeavyEditor.vue')
)
```

### Data Fetching Best Practices

```typescript
// ✅ Parallel fetching (faster)
const [{ data: users }, { data: posts }] = await Promise.all([
  useFetch('/api/users'),
  useFetch('/api/posts'),
])

// ✅ Cached fetching with key
const { data, refresh } = await useFetch('/api/data', {
  key: 'my-data',
  getCachedData: (key, nuxtApp) =>
    nuxtApp.payload.data[key] || nuxtApp.static.data[key],
})
```

---
