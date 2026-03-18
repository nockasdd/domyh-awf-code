---
name: vue
description: "Vue.js development patterns for Composition API and SFCs. Use when working with .vue files or Vue projects."
detect: ["*.vue", "package.json:vue", "vite.config.ts"]
category: frameworks
tier: 1
---

# Vue Patterns — DOMYH Awesome Code

> **Version**: Vue 3.5+/3.6 (2025-2026)
> **Philosophy**: Progressive, Composition API, reactive

---

## 🎯 When to Use This Skill

Use for: Web apps, SSR with Nuxt, progressive enhancement.
**NOT for**: Mobile (→ flutter), React apps (→ react).

---

## 📦 Recommended Stack (2025-2026)

### Core

| Library     | Use Case           |
| ----------- | ------------------ |
| **Vue 3.5** | Composition API 🏆 |
| **Nuxt 4**  | Full-stack SSR 🏆  |

### State

| Library    | Use Case          |
| ---------- | ----------------- |
| **Pinia**  | Official store 🏆 |
| **VueUse** | Composables 🏆    |

### UI

| Library       | Use Case            |
| ------------- | ------------------- |
| **Radix Vue** | Headless primitives |
| **PrimeVue**  | Enterprise          |
| **Vuetify 3** | Material Design     |
| **Naive UI**  | Customizable        |

### IDE Support

| IDE          | Features                    |
| ------------ | --------------------------- |
| **VS Code**  | Vue - Official extension 🏆 |
| **WebStorm** | Built-in Vue support        |

---

## 🆕 Vue 3.5 Features

### Reactive Props Destructure

```vue
<script setup lang="ts">
// ✅ Vue 3.5: Reactive destructure (stable)
const { user, loading = false } = defineProps<{
  user: User;
  loading?: boolean;
}>();

// Props are now reactive by default!
watchEffect(() => {
  console.log(user.name); // Reactive
});
</script>
```

### Improved Template Refs

```vue
<script setup lang="ts">
import { useTemplateRef } from "vue";

// ✅ Type-safe template refs
const inputRef = useTemplateRef<HTMLInputElement>("input");

function focus() {
  inputRef.value?.focus();
}
</script>

<template>
  <input ref="input" />
</template>
```

---

## 🔧 Composition API Patterns

### Component Structure

```vue
<script setup lang="ts">
import { ref, computed } from "vue";

interface Props {
  user: User;
}

interface Emits {
  (e: "update", user: User): void;
  (e: "delete", id: number): void;
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

// Reactive state
const isEditing = ref(false);

// Computed
const displayName = computed(() => `${props.user.name} <${props.user.email}>`);

// Methods
function handleUpdate(data: Partial<User>) {
  emit("update", { ...props.user, ...data });
}
</script>

<template>
  <div>
    <h2>{{ displayName }}</h2>
    <button @click="emit('delete', user.id)">Delete</button>
  </div>
</template>
```

### Custom Composables

```typescript
// composables/useUser.ts
import { ref, computed } from "vue";

export function useUser(id: Ref<number>) {
  const user = ref<User | null>(null);
  const loading = ref(false);
  const error = ref<Error | null>(null);

  async function fetch() {
    loading.value = true;
    error.value = null;
    try {
      user.value = await api.getUser(id.value);
    } catch (e) {
      error.value = e as Error;
    } finally {
      loading.value = false;
    }
  }

  // Auto-fetch when id changes
  watch(id, fetch, { immediate: true });

  return { user, loading, error, refetch: fetch };
}

// Usage
const userId = ref(1);
const { user, loading, error } = useUser(userId);
```

### useAsyncState Pattern

```typescript
// composables/useAsyncState.ts
export function useAsyncState<T>(fn: () => Promise<T>, initialState: T) {
  const state = ref<T>(initialState) as Ref<T>;
  const loading = ref(false);
  const error = ref<Error | null>(null);

  async function execute() {
    loading.value = true;
    error.value = null;
    try {
      state.value = await fn();
    } catch (e) {
      error.value = e as Error;
    } finally {
      loading.value = false;
    }
  }

  return { state, loading, error, execute };
}
```

---

## 📊 Pinia Stores

### Setup Store (Recommended)

```typescript
// stores/user.ts
import { defineStore } from "pinia";
import { ref, computed } from "vue";

export const useUserStore = defineStore(
  "user",
  () => {
    // State
    const user = ref<User | null>(null);
    const token = ref<string | null>(null);

    // Getters
    const isLoggedIn = computed(() => !!user.value);
    const fullName = computed(() => user.value?.name ?? "Guest");

    // Actions
    async function login(email: string, password: string) {
      const response = await authApi.login(email, password);
      user.value = response.user;
      token.value = response.token;
    }

    function logout() {
      user.value = null;
      token.value = null;
    }

    return { user, token, isLoggedIn, fullName, login, logout };
  },
  {
    persist: true, // pinia-plugin-persistedstate
  },
);
```

### Store Composition

```typescript
// stores/cart.ts
export const useCartStore = defineStore("cart", () => {
  const userStore = useUserStore();
  const items = ref<CartItem[]>([]);

  const total = computed(() =>
    items.value.reduce((sum, item) => sum + item.price * item.quantity, 0),
  );

  async function checkout() {
    if (!userStore.isLoggedIn) {
      throw new Error("Must be logged in");
    }
    return api.checkout(items.value);
  }

  return { items, total, checkout };
});
```

---

## 🚀 Nuxt 4 Patterns

### Data Fetching

```vue
<script setup lang="ts">
// ✅ Server-side data fetching
const {
  data: users,
  pending,
  error,
  refresh,
} = await useFetch("/api/users", {
  key: "users",
  default: () => [],
});

// ✅ With transform
const { data: user } = await useFetch(`/api/users/${route.params.id}`, {
  transform: (data) => normalizeUser(data),
});

// ✅ Lazy fetch
const { data, pending } = await useLazyFetch("/api/data");
</script>
```

### Server Routes

```typescript
// server/api/users/[id].get.ts
export default defineEventHandler(async (event) => {
  const id = getRouterParam(event, "id");

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
```

### Middleware

```typescript
// middleware/auth.ts
export default defineNuxtRouteMiddleware((to, from) => {
  const user = useSupabaseUser();

  if (!user.value && to.path !== "/login") {
    return navigateTo("/login");
  }
});

// Usage in page
definePageMeta({
  middleware: "auth",
});
```

---

## ✅ Best Practices Checklist

### Code Quality

- [ ] `<script setup>` syntax
- [ ] TypeScript with strict mode
- [ ] Props/emits typed
- [ ] Composables for logic reuse

### State

- [ ] Pinia for global state
- [ ] Computed for derived state
- [ ] VueUse utilities

### Performance

- [ ] `shallowRef` for large objects
- [ ] `v-once` for static content
- [ ] Lazy components
- [ ] `<Suspense>` for async

---
