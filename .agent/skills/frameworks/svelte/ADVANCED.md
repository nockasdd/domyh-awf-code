# Svelte — Advanced Patterns

## Table of Contents

- [Runes (Svelte 5)](#runes-svelte-5)
- [SvelteKit Advanced](#sveltekit-advanced)
- [Form Actions](#form-actions)
- [Stores Advanced](#stores-advanced)
- [Performance](#performance)

---

## Runes (Svelte 5)

### State & Derived

```svelte
<script>
  // Reactive state
  let count = $state(0)
  let items = $state([])

  // Derived (auto-computed)
  let doubled = $derived(count * 2)
  let total = $derived(items.reduce((sum, i) => sum + i.price, 0))

  // Deep reactive objects
  let form = $state({
    name: '',
    email: '',
    errors: {}
  })

  // Effect (side effects)
  $effect(() => {
    console.log(`Count changed to ${count}`)
    // Auto-cleanup on destroy
  })

  // Pre-effect (before DOM update)
  $effect.pre(() => {
    // Runs before DOM paint
  })
</script>

<button onclick={() => count++}>
  {count} (doubled: {doubled})
</button>
```

### Snippets (Reusable Templates)

```svelte
{#snippet row(item)}
  <tr>
    <td>{item.name}</td>
    <td>{item.price}</td>
    <td>
      <button onclick={() => remove(item.id)}>Delete</button>
    </td>
  </tr>
{/snippet}

<table>
  <tbody>
    {#each items as item (item.id)}
      {@render row(item)}
    {/each}
  </tbody>
</table>
```

### Props with Runes

```svelte
<script>
  // Type-safe props with defaults
  let {
    title,
    count = 0,
    onchange,
    children
  }: {
    title: string
    count?: number
    onchange?: (value: number) => void
    children?: import('svelte').Snippet
  } = $props()

  // Bindable props (two-way)
  let { value = $bindable() } = $props()
</script>
```

---

## SvelteKit Advanced

### Advanced Load Functions

```typescript
// +page.server.ts — parallel data loading
export const load: PageServerLoad = async ({ params, locals, depends }) => {
  depends('app:data')  // Invalidation key

  const [user, posts, stats] = await Promise.all([
    locals.db.user.findUnique({ where: { id: params.id } }),
    locals.db.post.findMany({ where: { authorId: params.id }, take: 20 }),
    locals.db.stats.get(params.id),
  ])

  if (!user) error(404, 'User not found')

  return { user, posts, stats }
}

// +page.ts — Universal load (runs on server + client)
export const load: PageLoad = async ({ data, fetch }) => {
  const enriched = await fetch(`/api/enrich/${data.user.id}`)
  return { ...data, enriched: await enriched.json() }
}
```

### Hooks

```typescript
// src/hooks.server.ts
export const handle: Handle = async ({ event, resolve }) => {
  // Auth check
  const session = event.cookies.get('session')
  if (session) {
    event.locals.user = await verifySession(session)
  }

  // Protected routes
  if (event.url.pathname.startsWith('/admin') && !event.locals.user?.isAdmin) {
    redirect(303, '/login')
  }

  return resolve(event, {
    transformPageChunk: ({ html }) =>
      html.replace('%lang%', event.locals.lang || 'en'),
  })
}

export const handleError: HandleServerError = ({ error, event }) => {
  console.error(error)
  return { message: 'Something went wrong', code: 'UNEXPECTED' }
}
```

---

## Form Actions

### Progressive Enhancement

```typescript
// +page.server.ts
export const actions = {
  create: async ({ request, locals }) => {
    const data = await request.formData()
    const title = data.get('title')

    if (!title || typeof title !== 'string') {
      return fail(400, { title, missing: true })
    }

    try {
      await locals.db.post.create({ data: { title, authorId: locals.user.id } })
    } catch (e) {
      return fail(500, { title, error: 'Failed to create' })
    }

    redirect(303, '/posts')
  },

  delete: async ({ request, locals }) => {
    const data = await request.formData()
    const id = data.get('id') as string
    await locals.db.post.delete({ where: { id } })
    return { success: true }
  },
} satisfies Actions
```

```svelte
<!-- +page.svelte -->
<script>
  import { enhance } from '$app/forms'
  let { form } = $props()
</script>

<form method="POST" action="?/create" use:enhance>
  <input name="title" value={form?.title ?? ''} />
  {#if form?.missing}<p class="error">Title required</p>{/if}
  <button>Create</button>
</form>
```

---

## Stores Advanced

### Custom Store Pattern

```typescript
function createTodoStore() {
  const { subscribe, set, update } = writable<Todo[]>([])

  return {
    subscribe,
    add: (text: string) => update(todos => [...todos, { id: crypto.randomUUID(), text, done: false }]),
    toggle: (id: string) => update(todos =>
      todos.map(t => t.id === id ? { ...t, done: !t.done } : t)
    ),
    remove: (id: string) => update(todos => todos.filter(t => t.id !== id)),
    clear: () => set([]),
  }
}

export const todos = createTodoStore()
```

---

## Performance

```yaml
performance:
  - "Use $state.raw() for large arrays (skip deep reactivity)"
  - "Lazy load components: const C = await import('./Heavy.svelte')"
  - "Stream data with SvelteKit: return { streamed: { data: promise } }"
  - "Prerender static pages: export const prerender = true"
  - "Use $effect.tracking() to avoid unnecessary effects"
  - "Image optimization: @sveltejs/enhanced-img"
```

---
