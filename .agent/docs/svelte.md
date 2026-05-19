---
library: svelte
version: 5.x
latest: true
category: frontend
official_docs: https://svelte.dev
last_updated: 2026-03-20
last_checked: 2026-03-21
---

# Svelte v5

> Svelte — Cybernetically enhanced web apps. Compiler-first framework.
> Current: v5 (Runes) | Previous: v4
> Docs: https://svelte.dev

## Version Comparison

| Feature | v4 | v5 |
|:--------|:---|:---|
| Reactivity | `$:` syntax, `let` | Runes (`$state`, `$derived`) |
| Props | `export let` | `$props()` |
| Events | `createEventDispatcher` | Callback props |
| Effects | `$:` blocks | `$effect()` |
| Snippets | ❌ (slots) | ✅ `{#snippet}` |
| Component type | `.svelte` | `.svelte` + `.svelte.ts` |
| Kit version | SvelteKit 1 | SvelteKit 2 |

## Installation

```bash
npx sv create my-app
# Options: SvelteKit, TypeScript, ESLint, Prettier, Playwright, Vitest

# Vite + Svelte (no Kit)
npm create vite@latest my-app -- --template svelte-ts
```

## Runes Reactivity (v5)

### $state

```svelte
<script lang="ts">
  // Reactive state
  let count = $state(0);
  let name = $state('World');

  // Deep reactive objects
  let todos = $state<Todo[]>([
    { id: 1, text: 'Learn Svelte', done: false },
  ]);

  // $state.raw — non-deep (performance)
  let data = $state.raw<BigData[]>([]);

  // $state.snapshot — get non-reactive copy
  function save() {
    const snapshot = $state.snapshot(todos);
    localStorage.setItem('todos', JSON.stringify(snapshot));
  }
</script>

<button onclick={() => count++}>
  Count: {count}
</button>
<input bind:value={name} />
```

### $derived

```svelte
<script lang="ts">
  let items = $state([1, 2, 3, 4, 5]);
  let filter = $state<'all' | 'even' | 'odd'>('all');

  // Simple derived
  let total = $derived(items.length);

  // Complex derived
  let filtered = $derived.by(() => {
    switch (filter) {
      case 'even': return items.filter(i => i % 2 === 0);
      case 'odd': return items.filter(i => i % 2 !== 0);
      default: return items;
    }
  });
</script>
```

### $effect

```svelte
<script lang="ts">
  let count = $state(0);

  // Runs when dependencies change (auto-tracked)
  $effect(() => {
    console.log(`count is ${count}`);

    // Cleanup (returned function)
    return () => {
      console.log('cleanup');
    };
  });

  // Pre-effect (runs before DOM update)
  $effect.pre(() => {
    // scroll position, etc.
  });

  // Root effect (not tied to component lifecycle)
  const cleanup = $effect.root(() => {
    $effect(() => { /* ... */ });
    return () => { /* cleanup */ };
  });
</script>
```

### $props

```svelte
<script lang="ts">
  // Props with types and defaults
  interface Props {
    title: string;
    count?: number;
    variant?: 'primary' | 'secondary';
    children: import('svelte').Snippet;
    onclick?: (e: MouseEvent) => void;
  }

  let { title, count = 0, variant = 'primary', children, onclick }: Props = $props();

  // Rest props
  let { class: className, ...rest }: { class?: string; [key: string]: any } = $props();
</script>

<button class={variant} {onclick} {...rest}>
  {title} ({count})
</button>
{@render children()}
```

### $bindable

```svelte
<script lang="ts">
  // Two-way binding (replaces bind:value on custom components)
  let { value = $bindable('') }: { value: string } = $props();
</script>

<input bind:value />

<!-- Parent: <MyInput bind:value={text} /> -->
```

### $inspect

```svelte
<script lang="ts">
  let count = $state(0);
  let name = $state('World');

  // Logs when dependencies change (dev-only, stripped in production)
  $inspect(count);          // logs: "init" 0, then "update" 1, 2...
  $inspect(count, name);    // multiple values

  // Custom handler
  $inspect(count).with((type, ...values) => {
    if (type === 'update') console.log('count changed:', ...values);
  });

  // $inspect.trace() — log call stack on change (dev-only)
  $effect(() => {
    $inspect.trace('effect triggered');
    console.log(count);
  });
</script>
```

## Snippets (v5)

```svelte
<!-- Replaces <slot> from v4 -->
{#snippet row(item: Item)}
  <tr>
    <td>{item.name}</td>
    <td>{item.price}</td>
  </tr>
{/snippet}

<table>
  {#each items as item}
    {@render row(item)}
  {/each}
</table>

<!-- Passing snippets as props (replaces named slots) -->
{#snippet header()}
  <h1>My Header</h1>
{/snippet}

<Layout {header}>
  <p>Main content</p>
</Layout>
```

## Template Syntax

```svelte
<!-- Conditionals -->
{#if condition}
  <p>True</p>
{:else if other}
  <p>Other</p>
{:else}
  <p>False</p>
{/if}

<!-- Loops -->
{#each items as item, index (item.id)}
  <li>{index}: {item.name}</li>
{:else}
  <p>No items</p>
{/each}

<!-- Await -->
{#await promise}
  <p>Loading...</p>
{:then data}
  <p>{data}</p>
{:catch error}
  <p>Error: {error.message}</p>
{/await}

<!-- Key block (destroy and recreate) -->
{#key selectedId}
  <UserProfile {selectedId} />
{/key}

<!-- HTML (careful — XSS) -->
{@html rawHtml}

<!-- Events -->
<button onclick={handler}>Click</button>
<button onclick={(e) => console.log(e)}>Click</button>
<button onclick={handler} onmouseenter={hover}>Hover + Click</button>

<!-- Bindings -->
<input bind:value={text} />
<input type="checkbox" bind:checked={done} />
<select bind:value={selected}>
  <option value="a">A</option>
</select>
<div bind:clientWidth={w} bind:clientHeight={h}></div>

<!-- Transitions -->
<div transition:fade>Fade in/out</div>
<div in:fly={{ y: -20 }} out:fade>Fly in, fade out</div>

<!-- Class shorthand -->
<div class:active={isActive}>Active class</div>
<div class:active>Uses `active` variable</div>

<!-- {@const} — local constants in template blocks -->
{#each items as item}
  {@const total = item.price * item.quantity}
  <p>{item.name}: ${total}</p>
{/each}

<!-- {@attach} — v5 attachments (runs when element is mounted) -->
{@attach (node) => {
  // Runs when node is mounted
  node.focus();
  return () => {
    // Cleanup when unmounted
  };
}}

<!-- {@debug} — breakpoint in dev tools -->
{@debug count, name}
```

## Special Elements

```svelte
<!-- Error boundary (v5) -->
<svelte:boundary onerror={(error, reset) => console.error(error)}>
  <RiskyComponent />
  {#snippet failed(error, reset)}
    <p>Error: {error.message}</p>
    <button onclick={reset}>Try again</button>
  {/snippet}
</svelte:boundary>

<!-- Window events and bindings -->
<svelte:window
  onkeydown={handleKeydown}
  onscroll={handleScroll}
  bind:innerWidth={width}
  bind:scrollY={y}
/>

<!-- Document -->
<svelte:document onvisibilitychange={handleVisibility} />

<!-- Body -->
<svelte:body onmouseenter={handleMouseEnter} />

<!-- Head (SEO, meta) -->
<svelte:head>
  <title>{pageTitle}</title>
  <meta name="description" content={description} />
</svelte:head>

<!-- Dynamic element -->
<svelte:element this={tag} onclick={handler}>
  Dynamic {tag} element
</svelte:element>
```

## Context API

```svelte
<!-- Parent.svelte -->
<script lang="ts">
  import { setContext } from 'svelte';

  const theme = $state({ color: 'blue', dark: false });
  setContext('theme', () => theme);  // pass getter for reactivity
</script>

<!-- Child.svelte (any depth) -->
<script lang="ts">
  import { getContext } from 'svelte';

  const getTheme = getContext<() => { color: string; dark: boolean }>('theme');
  const theme = $derived(getTheme());  // reactive!
</script>

<p style:color={theme.color}>{theme.dark ? 'Dark' : 'Light'} mode</p>
```

## Lifecycle Hooks

```svelte
<script lang="ts">
  import { onMount, onDestroy, tick } from 'svelte';

  // onMount — runs after component is first rendered
  onMount(() => {
    const interval = setInterval(() => count++, 1000);
    return () => clearInterval(interval);  // cleanup on destroy
  });

  // onDestroy — cleanup when component is removed
  onDestroy(() => {
    console.log('Component destroyed');
  });

  // tick — wait for DOM update to complete
  async function handleClick() {
    count++;
    await tick();  // DOM is now updated
    input.focus();
  }
</script>
```

## SvelteKit

### Project Structure

```
src/
├── routes/
│   ├── +page.svelte        # / (homepage)
│   ├── +page.ts             # client load function
│   ├── +page.server.ts      # server load function
│   ├── +layout.svelte       # root layout
│   ├── +layout.ts           # layout load
│   ├── +error.svelte        # error page
│   ├── blog/
│   │   ├── +page.svelte     # /blog
│   │   └── [slug]/
│   │       ├── +page.svelte     # /blog/:slug
│   │       └── +page.server.ts  # server data
│   └── api/
│       └── users/
│           └── +server.ts   # API endpoint
├── lib/
│   ├── components/
│   ├── server/              # server-only code ($lib/server)
│   └── utils.ts
├── app.html                 # HTML template
├── hooks.server.ts          # server hooks
└── hooks.client.ts          # client hooks
```

### Load Functions

```ts
// +page.server.ts — server-side data loading
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ params, locals, fetch, depends }) => {
  depends('app:posts');  // for invalidation

  const post = await db.post.findUnique({ where: { slug: params.slug } });
  if (!post) throw error(404, 'Post not found');

  return {
    post,
    comments: await db.comment.findMany({ where: { postId: post.id } }),
  };
};

// +page.ts — universal load (runs on server + client)
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch, params }) => {
  const res = await fetch(`/api/posts/${params.slug}`);
  const post = await res.json();
  return { post };
};

// +page.svelte — consume loaded data
<script lang="ts">
  import type { PageData } from './$types';
  let { data }: { data: PageData } = $props();
</script>

<h1>{data.post.title}</h1>
{#each data.comments as comment}
  <p>{comment.text}</p>
{/each}
```

### Form Actions

```ts
// +page.server.ts
import type { Actions } from './$types';
import { fail, redirect } from '@sveltejs/kit';

export const actions: Actions = {
  create: async ({ request, locals }) => {
    const data = await request.formData();
    const title = data.get('title') as string;

    if (!title) return fail(400, { title, missing: true });

    await db.post.create({ data: { title, authorId: locals.user.id } });
    throw redirect(303, '/posts');
  },
  delete: async ({ request }) => {
    const data = await request.formData();
    const id = data.get('id') as string;
    await db.post.delete({ where: { id } });
  },
};
```

```svelte
<!-- +page.svelte -->
<script lang="ts">
  import { enhance } from '$app/forms';
  import type { ActionData } from './$types';

  let { form }: { form: ActionData } = $props();
</script>

<form method="POST" action="?/create" use:enhance>
  <input name="title" value={form?.title ?? ''} />
  {#if form?.missing}<p class="error">Title is required</p>{/if}
  <button>Create Post</button>
</form>
```

### API Routes

```ts
// routes/api/users/+server.ts
import { json, error } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

export const GET: RequestHandler = async ({ url }) => {
  const query = url.searchParams.get('q');
  const users = await db.user.findMany({
    where: query ? { name: { contains: query } } : undefined,
  });
  return json(users);
};

export const POST: RequestHandler = async ({ request }) => {
  const body = await request.json();
  const user = await db.user.create({ data: body });
  return json(user, { status: 201 });
};
```

### Hooks

```ts
// hooks.server.ts — runs on every request
import type { Handle } from '@sveltejs/kit';

export const handle: Handle = async ({ event, resolve }) => {
  // Auth
  const session = event.cookies.get('session');
  if (session) {
    event.locals.user = await validateSession(session);
  }

  // Protect routes
  if (event.url.pathname.startsWith('/admin') && !event.locals.user?.isAdmin) {
    throw redirect(303, '/login');
  }

  return resolve(event);
};
```

## Stores (Legacy — still works in v5)

```ts
import { writable, readable, derived, get } from 'svelte/store';

const count = writable(0);
count.set(5);
count.update(n => n + 1);

// Subscribe
const unsubscribe = count.subscribe(value => console.log(value));

// In template: auto-subscribe with $
// <p>{$count}</p>
```

## Gotchas & Breaking Changes

⚠️ **v5 Runes**: `$state`, `$derived`, `$effect` replace `let`, `$:` reactivity.

⚠️ **v5 Props**: `$props()` replaces `export let`. No more `createEventDispatcher`.

⚠️ **v5 Snippets**: `{#snippet}` + `{@render}` replace `<slot>`.

⚠️ **v5 Events**: Use callback props (`onclick`) instead of `on:click`.

⚠️ **`$effect`**: Don't set state inside effects without careful thought — can cause infinite loops.

⚠️ **SvelteKit `load`**: Returns data must be serializable (no functions, class instances).

⚠️ **Form actions**: Use `use:enhance` for progressive enhancement without full page reloads.

⚠️ **`$lib`**: Import from `$lib/` alias for `src/lib/` directory.

⚠️ **SvelteKit 2**: Requires Vite 5+. `path.base` now empty string by default (not `/`).

⚠️ **Universal vs Server load**: `+page.ts` (universal) runs on both server+client. `+page.server.ts` runs server-only.
