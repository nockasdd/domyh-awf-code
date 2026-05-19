---
library: vuejs
version: 3.x
latest: true
category: frontend
official_docs: https://vuejs.org
last_updated: 2026-03-20
last_checked: 2026-03-21
---

# Vue.js v3

> Vue.js — The Progressive JavaScript Framework.
> Current: v3.5+ | Previous: v2.x (EOL)
> Docs: https://vuejs.org

## Version Comparison

| Feature | v2 (EOL) | v3 |
|:--------|:---------|:---|
| API Style | Options API | Composition API + Options |
| Reactivity | Object.defineProperty | Proxy-based |
| TypeScript | Partial | First-class |
| Fragments | ❌ | ✅ Multi-root templates |
| Teleport | ❌ | ✅ |
| Suspense | ❌ | ✅ Experimental |
| Script Setup | ❌ | ✅ `<script setup>` |
| Tree-shaking | Limited | Full ESM |
| Performance | ~2x | Baseline (faster) |

## Installation

```bash
npm create vue@latest
# Options: TypeScript, JSX, Vue Router, Pinia, Vitest, ESLint, Prettier

# or manual
npm install vue@3
```

## Project Structure

```
src/
├── App.vue
├── main.ts
├── components/
│   ├── ui/           # Reusable UI components
│   └── layout/       # Layout components
├── views/            # Page-level components
├── composables/      # Custom hooks (use*.ts)
├── stores/           # Pinia stores
├── router/
│   └── index.ts
├── assets/
│   └── styles/
├── types/            # TypeScript types
└── utils/
```

## Composition API (Recommended)

### `<script setup>` (SFC)

```vue
<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'

// Reactive state
const count = ref(0)
const message = ref('Hello')

// Computed
const doubled = computed(() => count.value * 2)

// Methods
function increment() {
  count.value++
}

// Lifecycle
onMounted(() => {
  console.log('Component mounted')
})

// Watchers
watch(count, (newVal, oldVal) => {
  console.log(`Count changed: ${oldVal} → ${newVal}`)
})

// Watch multiple sources
watch([count, message], ([newCount, newMsg]) => {
  console.log(newCount, newMsg)
})

// Deep watch
watch(() => state.nested.value, (newVal) => {
  console.log('Deep change:', newVal)
}, { deep: true })

// Immediate watch
watchEffect(() => {
  // auto-tracks dependencies, runs immediately
  console.log(`Count is ${count.value}`)
})
</script>

<template>
  <button @click="increment">{{ count }} ({{ doubled }})</button>
  <input v-model="message" />
</template>
```

### Reactive State

```ts
import { ref, reactive, shallowRef, toRefs, toRef, readonly } from 'vue'

// ref — primitive values (access via .value)
const count = ref(0)
count.value++ // must use .value in script

// reactive — objects (no .value needed)
const state = reactive({ name: 'Vue', version: 3 })
state.name = 'Vue.js' // direct mutation

// shallowRef — only track .value reassignment (performance)
const data = shallowRef({ items: [] })
data.value = { items: [...newItems] } // triggers update

// toRefs — destructure reactive without losing reactivity
const { name, version } = toRefs(state)

// toRef — single property
const nameRef = toRef(state, 'name')

// readonly — prevent mutation
const readonlyState = readonly(state)
```

### Props & Emits

```vue
<script setup lang="ts">
// Props with defaults
const props = withDefaults(defineProps<{
  title: string
  count?: number
  items?: string[]
  variant?: 'primary' | 'secondary'
}>(), {
  count: 0,
  items: () => [],
  variant: 'primary',
})

// Emits with type validation
const emit = defineEmits<{
  (e: 'update', id: number): void
  (e: 'delete', id: number): void
  (e: 'submit', data: { name: string; email: string }): void
}>()

// v-model support (single)
const model = defineModel<string>()
// parent: <Child v-model="text" />

// Multiple v-models
const firstName = defineModel<string>('firstName')
const lastName = defineModel<string>('lastName')
// parent: <Child v-model:firstName="first" v-model:lastName="last" />

// Expose (limit what parent can access via ref)
defineExpose({ reset, validate })

// Slots type checking (3.3+)
defineSlots<{
  default(props: { item: Item }): any
  header(props: {}): any
}>()
</script>
```

### Composables (Custom Hooks)

```ts
// composables/useFetch.ts
import { ref, watchEffect, type Ref } from 'vue'

export function useFetch<T>(url: string | Ref<string>) {
  const data = ref<T | null>(null)
  const error = ref<string | null>(null)
  const loading = ref(true)

  watchEffect(async () => {
    loading.value = true
    error.value = null
    try {
      const urlStr = typeof url === 'string' ? url : url.value
      const res = await fetch(urlStr)
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      data.value = await res.json()
    } catch (e) {
      error.value = (e as Error).message
    } finally {
      loading.value = false
    }
  })

  return { data, error, loading }
}

// composables/useDebounce.ts
import { ref, watch, type Ref } from 'vue'

export function useDebounce<T>(source: Ref<T>, delay = 300): Ref<T> {
  const debounced = ref(source.value) as Ref<T>
  let timeout: ReturnType<typeof setTimeout>

  watch(source, (newVal) => {
    clearTimeout(timeout)
    timeout = setTimeout(() => {
      debounced.value = newVal
    }, delay)
  })

  return debounced
}

// composables/useLocalStorage.ts
export function useLocalStorage<T>(key: string, defaultValue: T) {
  const stored = localStorage.getItem(key)
  const data = ref<T>(stored ? JSON.parse(stored) : defaultValue)

  watch(data, (newVal) => {
    localStorage.setItem(key, JSON.stringify(newVal))
  }, { deep: true })

  return data
}
```

### Provide / Inject

```vue
<!-- Parent.vue -->
<script setup>
import { provide, ref } from 'vue'
import type { InjectionKey } from 'vue'

// Type-safe injection key
export const ThemeKey: InjectionKey<Ref<'light' | 'dark'>> = Symbol('Theme')

const theme = ref<'light' | 'dark'>('dark')
provide(ThemeKey, theme) // type-safe
provide('config', { apiUrl: '/api' }) // string key
</script>

<!-- Grandchild.vue -->
<script setup>
import { inject } from 'vue'
import { ThemeKey } from '../Parent.vue'

const theme = inject(ThemeKey)!          // Ref<'light' | 'dark'>
const config = inject('config', { apiUrl: '' }) // with default
</script>
```

## Template Directives

```html
<!-- Conditionals -->
<div v-if="type === 'A'">A</div>
<div v-else-if="type === 'B'">B</div>
<div v-else>Other</div>
<div v-show="isVisible">Show/hide (CSS display)</div>

<!-- Lists -->
<li v-for="(item, index) in items" :key="item.id">
  {{ index }}: {{ item.name }}
</li>

<!-- Object iteration -->
<div v-for="(value, key, index) in object" :key="key">
  {{ key }}: {{ value }}
</div>

<!-- Events -->
<button @click="handleClick">Click</button>
<button @click.prevent="submit">Prevent default</button>
<button @click.stop="handler">Stop propagation</button>
<button @click.once="handler">Fire once</button>
<input @keyup.enter="search" />
<input @keyup.ctrl.s="save" />

<!-- Two-way binding -->
<input v-model="text" />
<input v-model.number="age" />
<input v-model.trim="name" />
<input v-model.lazy="query" />  <!-- sync on change, not input -->

<!-- Dynamic attributes -->
<a :href="url" :class="{ active: isActive, disabled: !isEnabled }">Link</a>
<div :class="['base', isActive ? 'active' : '']">Conditional class</div>
<div :style="{ color: textColor, fontSize: size + 'px' }">Styled</div>

<!-- Slots -->
<template #header>Header content</template>
<template #default="{ item }">{{ item.name }}</template>

<!-- Teleport -->
<Teleport to="body">
  <div class="modal-overlay">
    <div class="modal">Modal content</div>
  </div>
</Teleport>
```

## Pinia (State Management)

```ts
// stores/useUserStore.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

// Setup store (Composition API style — recommended)
export const useUserStore = defineStore('user', () => {
  // State
  const user = ref<User | null>(null)
  const loading = ref(false)

  // Getters
  const isAuthenticated = computed(() => !!user.value)
  const fullName = computed(() =>
    user.value ? `${user.value.firstName} ${user.value.lastName}` : ''
  )

  // Actions
  async function login(email: string, password: string) {
    loading.value = true
    try {
      const res = await fetch('/api/login', {
        method: 'POST',
        body: JSON.stringify({ email, password }),
      })
      user.value = await res.json()
    } finally {
      loading.value = false
    }
  }

  function logout() {
    user.value = null
  }

  // Persist (with plugin)
  return { user, loading, isAuthenticated, fullName, login, logout }
})

// Usage in component
<script setup>
import { useUserStore } from '@/stores/useUserStore'
const userStore = useUserStore()

// Direct access
userStore.login('email', 'pass')
console.log(userStore.isAuthenticated)
console.log(userStore.fullName)

// Destructure with storeToRefs (for reactivity)
import { storeToRefs } from 'pinia'
const { user, isAuthenticated } = storeToRefs(userStore)
const { login, logout } = userStore  // actions don't need storeToRefs
</script>
```

## Vue Router (v4)

```ts
// router/index.ts
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: () => import('../views/Home.vue'),
      meta: { title: 'Home' },
    },
    {
      path: '/users',
      component: () => import('../views/Users.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/user/:id',
      component: () => import('../views/UserDetail.vue'),
      props: true,  // pass route params as props
    },
    {
      path: '/admin',
      component: () => import('../layouts/AdminLayout.vue'),
      children: [
        { path: '', component: () => import('../views/admin/Dashboard.vue') },
        { path: 'settings', component: () => import('../views/admin/Settings.vue') },
      ],
    },
    { path: '/:pathMatch(.*)*', component: () => import('../views/NotFound.vue') },
  ],
})

// Navigation guard
router.beforeEach((to, from) => {
  if (to.meta.requiresAuth && !isAuthenticated()) {
    return { name: 'Login', query: { redirect: to.fullPath } }
  }
})

// Route-level guard
{
  path: '/admin',
  beforeEnter: (to, from) => {
    if (!isAdmin()) return { name: 'Home' }
  },
}

export default router
```

```vue
<!-- In component -->
<script setup>
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

// Read params
console.log(route.params.id)
console.log(route.query.search)

// Navigate
router.push('/users')
router.push({ name: 'User', params: { id: '123' } })
router.replace('/login')
router.go(-1)
</script>

<template>
  <nav>
    <RouterLink to="/" active-class="active">Home</RouterLink>
    <RouterLink :to="{ name: 'Users' }">Users</RouterLink>
  </nav>
  <RouterView />
</template>
```

## Transition & Animation

```vue
<template>
  <!-- Single element -->
  <Transition name="fade">
    <div v-if="show">Content</div>
  </Transition>

  <!-- List -->
  <TransitionGroup name="list" tag="ul">
    <li v-for="item in items" :key="item.id">{{ item.name }}</li>
  </TransitionGroup>
</template>

<style>
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

.list-enter-active, .list-leave-active { transition: all 0.4s ease; }
.list-enter-from, .list-leave-to { opacity: 0; transform: translateX(-30px); }
.list-move { transition: transform 0.4s ease; }
</style>
```

## Vapor Mode (Experimental)

```ts
// Vapor Mode — no Virtual DOM, compiles to direct DOM operations
// Opt-in per component for performance-critical sections

// vite.config.ts
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [
    vue({
      features: {
        vaporMode: true,  // enable vapor compilation
      },
    }),
  ],
});
```

## useTemplateRef (3.5+)

```vue
<script setup>
import { useTemplateRef, onMounted } from 'vue';

// Type-safe template ref (replaces ref('name') pattern)
const inputRef = useTemplateRef<HTMLInputElement>('myInput');

onMounted(() => {
  inputRef.value?.focus();
});
</script>

<template>
  <input ref="myInput" />
</template>
```

## Gotchas & Breaking Changes

⚠️ **ref vs reactive**: `ref` for primitives, `reactive` for objects. Don't reassign `reactive()` — loses reactivity.

⚠️ **`.value` trap**: Must use `.value` in `<script>`, auto-unwrapped in `<template>`.

⚠️ **Props destructuring**: In v3.5+, destructuring `defineProps()` is reactive. Before 3.5, use `toRefs(props)`.

⚠️ **v-if vs v-for**: Never use on same element. `v-if` has higher priority in v3 (opposite of v2).

⚠️ **Options API**: Still supported but Composition API is recommended for new projects.

⚠️ **Pinia**: Replaces Vuex. Use `storeToRefs()` when destructuring store state/getters.

⚠️ **`defineModel`** (3.4+): Replaces manual `modelValue` prop + `update:modelValue` emit.

⚠️ **`defineSlots`** (3.3+): Type-safe scoped slots for component libraries.

⚠️ **`useTemplateRef`** (3.5+): Type-safe template refs. Replaces `ref('name')` pattern.

⚠️ **Vapor Mode**: Experimental. No Virtual DOM — compiles to direct DOM operations for speed.
