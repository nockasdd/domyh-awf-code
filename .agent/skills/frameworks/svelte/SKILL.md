---
name: svelte
detect: ["svelte.config.js", "*.svelte", "+page.svelte", "+layout.svelte"]
version: "6.4.2"
category: frontend
tier: 1
---

# Svelte Patterns — DOMYH Awesome Code

> **Version**: Svelte 5.x / SvelteKit 2.x (Feb 2026)
> **Philosophy**: Compiled reactivity, runes, zero overhead

---

## 🎯 When to Use This Skill

Use for: High-performance web apps, minimal bundle, compile-time optimization.
**NOT for**: Large enterprise (→ angular), React teams (→ react).

---

## 📦 Recommended Stack (2025-2026)

### Core

| Tool            | Use Case        |
| --------------- | --------------- |
| **Svelte 5**    | UI framework 🏆 |
| **SvelteKit 2** | Full-stack      |
| **Vite**        | Bundler         |

### State

| Library            | Use Case               |
| ------------------ | ---------------------- |
| **Svelte Stores**  | Built-in               |
| **Runes ($state)** | Svelte 5 reactivity 🏆 |

### IDE Support

| IDE                            | Features         |
| ------------------------------ | ---------------- |
| **VS Code + Svelte extension** | Full support 🏆  |
| **WebStorm**                   | Built-in support |

---

## 🆕 Svelte 5 Runes

### $state - Reactive State

```svelte
<script>
  // 🆕 Svelte 5: $state replaces let
  let count = $state(0);
  let user = $state({ name: 'John', age: 30 });

  function increment() {
    count++;  // Reactive!
  }

  function updateName(name) {
    user.name = name;  // Deep reactivity
  }
</script>

<button onclick={increment}>
  Count: {count}
</button>
```

### $derived - Computed Values

```svelte
<script>
  let firstName = $state('John');
  let lastName = $state('Doe');

  // 🆕 $derived replaces $:
  let fullName = $derived(`${firstName} ${lastName}`);

  // Complex derived with function
  let initials = $derived(() => {
    return `${firstName[0]}${lastName[0]}`.toUpperCase();
  });
</script>

<p>{fullName} ({initials})</p>
```

### $effect - Side Effects

```svelte
<script>
  let count = $state(0);

  // 🆕 $effect replaces $: for side effects
  $effect(() => {
    console.log('Count changed:', count);

    // Return cleanup function
    return () => {
      console.log('Cleanup');
    };
  });

  // Run once after mount
  $effect(() => {
    const timer = setInterval(() => count++, 1000);
    return () => clearInterval(timer);
  });
</script>
```

### $props - Component Props

```svelte
<script>
  // 🆕 $props replaces export let
  let {
    name,
    age = 0,        // Default value
    onSave          // Event handler
  } = $props();
</script>

<div>
  <p>{name} is {age} years old</p>
  <button onclick={() => onSave?.({ name, age })}>
    Save
  </button>
</div>
```

### $bindable - Two-way Binding

```svelte
<script>
  // Parent can bind to this
  let { value = $bindable('') } = $props();
</script>

<input bind:value />

<!-- Usage in parent -->
<!-- <TextInput bind:value={searchQuery} /> -->
```

---

## 🔧 SvelteKit Patterns

### Page with Load Function

```svelte
<!-- +page.svelte -->
<script>
  let { data } = $props();
</script>

<h1>{data.user.name}</h1>
<ul>
  {#each data.posts as post}
    <li>{post.title}</li>
  {/each}
</ul>
```

```typescript
// +page.ts
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ params, fetch }) => {
  const user = await fetch(`/api/users/${params.id}`).then((r) => r.json());
  const posts = await fetch(`/api/users/${params.id}/posts`).then((r) =>
    r.json(),
  );

  return { user, posts };
};
```

### Server-only Load

```typescript
// +page.server.ts
import type { PageServerLoad } from "./$types";
import { db } from "$lib/server/db";
import { error } from "@sveltejs/kit";

export const load: PageServerLoad = async ({ params }) => {
  const user = await db.user.findUnique({
    where: { id: params.id },
  });

  if (!user) {
    throw error(404, "User not found");
  }

  return { user };
};
```

### Form Actions

```svelte
<!-- +page.svelte -->
<script>
  import { enhance } from '$app/forms';
</script>

<form method="POST" action="?/create" use:enhance>
  <input name="title" required />
  <button>Create</button>
</form>
```

```typescript
// +page.server.ts
import type { Actions } from "./$types";
import { fail, redirect } from "@sveltejs/kit";

export const actions: Actions = {
  create: async ({ request }) => {
    const data = await request.formData();
    const title = data.get("title");

    if (!title) {
      return fail(400, { title, missing: true });
    }

    const post = await db.post.create({ data: { title } });
    throw redirect(303, `/posts/${post.id}`);
  },
};
```

### Layouts

```svelte
<!-- +layout.svelte -->
<script>
  let { data, children } = $props();
</script>

<nav>
  <a href="/">Home</a>
  <a href="/about">About</a>
  {#if data.user}
    <span>{data.user.name}</span>
  {/if}
</nav>

<main>
  {@render children()}
</main>
```

---

## 🎨 Snippets (Svelte 5)

```svelte
<script>
  // 🆕 Snippets replace slots
  let { header, children } = $props();
</script>

{#snippet defaultHeader()}
  <h1>Default Header</h1>
{/snippet}

<header>
  {@render header?.() ?? defaultHeader()}
</header>

<main>
  {@render children()}
</main>

<!-- Usage -->
<!--
<Card>
  {#snippet header()}
    <h2>Custom Header</h2>
  {/snippet}

  <p>Content here</p>
</Card>
-->
```

---

## ✅ Best Practices Checklist

### Svelte 5 Migration

- [ ] Use $state instead of let
- [ ] Use $derived instead of $:
- [ ] Use $props instead of export let
- [ ] Use snippets instead of slots

### Performance

- [ ] Minimal component splitting
- [ ] Use $effect.pre for sync updates
- [ ] Lazy load routes
- [ ] SSR for initial load
- [ ] Enable async SSR for streaming

### SvelteKit

- [ ] Use server load for sensitive data
- [ ] Implement form actions
- [ ] Handle errors properly
- [ ] Use enhance for progressive enhancement
- [ ] Configure CSP hydration

---

## 🆕 Svelte 5.x Feb 2026 Features

### $inspect (Development Mode)

```svelte
<script>
  let count = $state(0);
  let user = $state({ name: 'Alice', age: 25 });

  // ✅ $inspect - reactive console.log for development
  $inspect(count);           // Logs whenever count changes
  $inspect(user).with(fn);   // Custom handler

  // ✅ Chainable with custom handlers
  $inspect(user).with((type, newVal, oldVal) => {
    console.log(`${type}: ${oldVal} → ${newVal}`);
  });
</script>
```

### Async SSR (Experimental)

```javascript
// ✅ SvelteKit 2.x: Async server-side rendering
// svelte.config.js
export default {
  kit: {
    experimental: {
      asyncSSR: true, // ✅ Enable async SSR
    },
  },
};
```

### CSP Hydration

```javascript
// ✅ Content Security Policy support for hydration
// svelte.config.js
export default {
  kit: {
    csp: {
      mode: "hash", // 'hash' | 'nonce' | 'auto'
      directives: {
        "script-src": ["self"],
        "style-src": ["self", "unsafe-inline"],
      },
    },
  },
};
```

### Deep Reactivity

```svelte
<script>
  // ✅ Svelte 5: Automatic deep reactivity for objects/arrays
  let items = $state([{ name: 'Item 1', done: false }]);

  function toggle(index) {
    // ✅ This triggers reactive update automatically
    items[index].done = !items[index].done;
  }

  // ✅ Nested objects work too
  let user = $state({
    profile: { settings: { theme: 'dark' } }
  });

  user.profile.settings.theme = 'light'; // ✅ Reactive!
</script>
```

---

_DOMYH Awesome Code • Svelte 5.x / SvelteKit 2.x • Feb 2026_
