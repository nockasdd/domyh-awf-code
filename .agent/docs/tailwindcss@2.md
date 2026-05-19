---
library: tailwindcss
version: 2
latest: false
category: css
official_docs: https://v2.tailwindcss.com/docs/
last_updated: 2026-03-20
---

# Tailwind CSS v2

> Tailwind CSS v2.x — JS config with purge, variants config, PostCSS 7/8.
> ⚠️ This is a LEGACY version. For v3, use `tailwindcss@3.md`. For v4 (latest), use `tailwindcss.md`.
> Docs: https://v2.tailwindcss.com/docs/

## v2 vs v3 vs v4: Key Differences

| Feature | v2 (this doc) | v3 | v4 (latest) |
|:--------|:-------------|:---|:------------|
| Config key | `purge` | `content` | Auto-detected |
| Dark mode | `darkMode: false` (disabled default) | `darkMode: 'class'` | `@custom-variant dark` |
| Variants | `variants: { extend: {} }` | Auto-enabled all | Auto-enabled all |
| JIT mode | Opt-in (`mode: 'jit'`) | Default | Default |
| CSS setup | `@tailwind base/components/utilities` | Same | `@import "tailwindcss"` |
| Config format | JS only (`module.exports`) | JS (+ESM v3.3) | CSS (`@theme {}`) |
| Plugins | `require()` | `require()` | `@plugin` |
| PostCSS | Requires PostCSS 8 (or v7 compat) | PostCSS 8 | PostCSS / Vite |

## Installation (v2)

### PostCSS Plugin

```bash
npm install -D tailwindcss@^2 postcss@latest autoprefixer@latest
npx tailwindcss init
```

```js
// postcss.config.js
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};
```

### PostCSS 7 Compatibility Build

For tools using older PostCSS versions:

```bash
npm install -D tailwindcss@npm:@tailwindcss/postcss7-compat postcss@^7 autoprefixer@^9
```

### CSS Setup

```css
/* main.css */
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### Tailwind CLI

```bash
npx tailwindcss -i ./src/input.css -o ./dist/output.css --watch
```

### CDN (development only)

```html
<link href="https://unpkg.com/tailwindcss@^2/dist/tailwind.min.css" rel="stylesheet">
```

## Configuration: tailwind.config.js

### Default Config Structure

```js
// tailwind.config.js
module.exports = {
  purge: [],
  darkMode: false,   // or 'media' or 'class'
  theme: {
    extend: {},
  },
  variants: {
    extend: {},
  },
  plugins: [],
};
```

> ⚠️ v2 uses `purge` instead of v3's `content`. v2 uses `darkMode: false` by default (disabled).

### Purge Configuration (v2-specific)

```js
module.exports = {
  purge: [
    './src/**/*.html',
    './src/**/*.vue',
    './src/**/*.jsx',
  ],
  // ...
};
```

> ⚠️ v3 renamed `purge` → `content`. v4 auto-detects.

### JIT Mode (v2.1+)

```js
module.exports = {
  mode: 'jit',
  purge: ['./src/**/*.{html,js}'],
  // ...
};
```

> ⚠️ v3+ JIT is default — no need for `mode: 'jit'`.

### Theme Customization

```js
module.exports = {
  theme: {
    colors: {
      gray: require('tailwindcss/colors').coolGray,
      blue: require('tailwindcss/colors').lightBlue,
      red: require('tailwindcss/colors').rose,
      pink: require('tailwindcss/colors').fuchsia,
    },
    fontFamily: {
      sans: ['Graphik', 'sans-serif'],
      serif: ['Merriweather', 'serif'],
    },
    extend: {
      spacing: { '128': '32rem', '144': '36rem' },
      borderRadius: { '4xl': '2rem' },
    },
  },
};
```

### Variants Configuration (v2-specific)

v2 requires explicitly enabling variants per utility:

```js
module.exports = {
  variants: {
    fill: [],       // Disable all variants for fill
    extend: {
      borderColor: ['focus-visible'],
      opacity: ['disabled'],
    },
  },
};
```

> ⚠️ v3+ auto-enables ALL variants — no `variants` config needed.

### Plugins

```js
module.exports = {
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
    require('@tailwindcss/aspect-ratio'),
  ],
};
```

### Prefix

```js
module.exports = { prefix: 'tw-' };
// <div class="tw-bg-blue-500 tw-text-white">
```

### Important

```js
// All utilities !important
module.exports = { important: true };

// Scoped to selector
module.exports = { important: '#app' };
```

### Presets

```js
module.exports = {
  presets: [require('@acmecorp/base-tailwind-config')],
  theme: { /* project-specific */ },
};
```

## Dark Mode (v2)

### Disabled by default

```js
module.exports = {
  darkMode: false,  // Dark mode disabled (v2 default)
};
```

### Media strategy (auto)

```js
module.exports = {
  darkMode: 'media',  // Uses prefers-color-scheme
};
```

### Class strategy (manual toggle)

```js
module.exports = {
  darkMode: 'class',
};
```

```html
<html class="dark">
  <div class="bg-white dark:bg-black">
    <h1 class="text-gray-900 dark:text-white">Title</h1>
  </div>
</html>
```

### Toggle with JavaScript

```js
// In <head> to avoid FOUC
if (localStorage.theme === 'dark' || (
  !('theme' in localStorage) &&
  window.matchMedia('(prefers-color-scheme: dark)').matches
)) {
  document.documentElement.classList.add('dark');
} else {
  document.documentElement.classList.remove('dark');
}

// Manual toggle
localStorage.theme = 'light';
localStorage.theme = 'dark';
localStorage.removeItem('theme'); // Respect OS
```

### Enabling dark variants (v2-specific)

v2 may require enabling dark variants per utility:

```js
module.exports = {
  darkMode: 'class',
  variants: {
    extend: {
      backgroundColor: ['dark'],
      textColor: ['dark'],
      borderColor: ['dark'],
    },
  },
};
```

> ⚠️ v3+ auto-enables dark variant for all utilities.

## Responsive Design (v2)

### Default Breakpoints

| Prefix | Min width |
|:-------|:----------|
| `sm:` | 640px |
| `md:` | 768px |
| `lg:` | 1024px |
| `xl:` | 1280px |
| `2xl:` | 1536px |

### Usage

```html
<div class="w-full md:w-1/2 lg:w-1/3">Responsive</div>
<div class="flex flex-col md:flex-row">Stacked → Row</div>
```

### Custom Breakpoints

```js
module.exports = {
  theme: {
    screens: {
      tablet: '640px', laptop: '1024px', desktop: '1280px',
    },
  },
};
```

## Extracting Components (v2)

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer components {
  .btn-primary {
    @apply py-2 px-4 bg-blue-500 text-white font-semibold rounded-lg
           shadow-md hover:bg-blue-700 focus:outline-none;
  }
}
```

## v2 → v3 Migration Checklist

1. **Rename `purge` → `content`** in tailwind.config.js
2. **Remove `mode: 'jit'`** — JIT is default in v3
3. **Remove `darkMode: false`** → dark mode uses `media` by default
4. **Remove `variants` section** — all variants auto-enabled
5. **Update deprecated colors** → `coolGray` → `gray`, `lightBlue` → `sky`
6. **Update PostCSS 7 compat** → Use PostCSS 8 directly
7. **Update `@tailwindcss/forms`** → Needs v3-compatible version
8. **Check `important` selector** → v3 uses `:is()` nesting

## v2 → v4 Migration Checklist

1. Complete v2 → v3 migration first (above)
2. Then follow v3 → v4 migration in `tailwindcss@3.md`
