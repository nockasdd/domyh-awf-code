---
library: tailwindcss
version: 3
latest: false
category: css
official_docs: https://v3.tailwindcss.com/docs/
last_updated: 2026-03-20
---

# Tailwind CSS v3

> Tailwind CSS v3.x — JS-based configuration, PostCSS pipeline, JIT engine.
> ⚠️ This is the LEGACY version. For v4 (latest), use `tailwindcss.md`.
> Docs: https://v3.tailwindcss.com/docs/

## v3 vs v4: Key Differences

| Feature | v3 (this doc) | v4 (latest) |
|:--------|:-------------|:------------|
| Config | `tailwind.config.js` (JS) | `@theme {}` (CSS) |
| CSS Import | `@tailwind base/components/utilities` | `@import "tailwindcss"` |
| Plugins | `require('@tailwindcss/forms')` | `@plugin "@tailwindcss/forms"` |
| Custom variants | `addVariant()` in plugin | `@custom-variant` in CSS |
| Dark mode | `darkMode: 'class'` or `'selector'` | `@custom-variant dark (...)` |
| Content paths | `content: [...]` REQUIRED | Auto-detected |
| Colors | `theme.extend.colors` in JS | `--color-*` in `@theme` |
| Container queries | Plugin required | Built-in `@container` |
| Arbitrary values | `top-[117px]` | Same syntax |
| Build tool | PostCSS plugin / CLI | Vite plugin / PostCSS / CLI |

## Installation (v3)

### Tailwind CLI

```bash
npm install -D tailwindcss@3
npx tailwindcss init
```

### PostCSS Plugin

```bash
npm install -D tailwindcss@3 postcss autoprefixer
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

### CSS Setup

```css
/* main.css */
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### CLI Build

```bash
npx tailwindcss -i ./src/input.css -o ./src/output.css --watch
```

## Configuration: tailwind.config.js

### Basic Config

```js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{html,js,jsx,tsx}',
    './components/**/*.{html,js,jsx,tsx}',
    './src/**/*.{html,js,jsx,tsx}',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
```

### ESM Config (v3.3+)

```js
/** @type {import('tailwindcss').Config} */
export default {
  content: ["./src/**/*.{html,js}"],
  theme: { extend: {} },
  plugins: [],
};
```

### TypeScript Config

```ts
import type { Config } from 'tailwindcss';

export default {
  content: ["./src/**/*.{html,js,tsx}"],
  theme: { extend: {} },
  plugins: [],
} satisfies Config;
```

### Content Paths (MANDATORY)

Content paths are **required** in v3 — Tailwind scans these for class names:

```js
module.exports = {
  content: [
    './public/**/*.html',
    './src/**/*.{js,jsx,ts,tsx}',
    './src/**/*.vue',
    './content/**/*.md',
  ],
};
```

> ⚠️ v4 auto-detects content — no configuration needed.

### Theme Customization

#### Extending defaults (RECOMMENDED)

```js
module.exports = {
  theme: {
    extend: {
      colors: {
        brand: '#3b82f6',
        'brand-dark': '#1d4ed8',
      },
      spacing: { '128': '32rem', '144': '36rem' },
      borderRadius: { '4xl': '2rem' },
      fontFamily: { display: 'Oswald, ui-serif' },
      screens: { '3xl': '1600px' },
    },
  },
};
```

#### Overriding defaults entirely

```js
module.exports = {
  theme: {
    colors: {
      'blue': '#1fb6ff',
      'purple': '#7e5bef',
      'pink': '#ff49db',
      transparent: 'transparent',
      current: 'currentColor',
    },
    fontFamily: {
      sans: ['Graphik', 'sans-serif'],
      serif: ['Merriweather', 'serif'],
    },
    screens: {
      sm: '480px', md: '768px', lg: '976px', xl: '1440px',
    },
  },
};
```

> ⚠️ Overriding replaces ALL defaults. Use `extend` to keep them.

### Prefix

```js
module.exports = { prefix: 'tw-' };
// Usage: <div class="tw-bg-blue-500 tw-text-white">
```

### Important

```js
module.exports = { important: true };
// Or scope: module.exports = { important: '#app' };
```

### Presets

```js
// my-preset.js
module.exports = {
  theme: { colors: { blue: { 500: '#3b82f6' } } },
  plugins: [require('@tailwindcss/typography')],
};

// tailwind.config.js
module.exports = {
  presets: [require('./my-preset')],
  theme: { extend: {} },
};
```

## CSS Directives (v3)

### @tailwind

```css
@tailwind base;        /* Preflight reset + base styles */
@tailwind components;  /* Component classes */
@tailwind utilities;   /* Utility classes */
@tailwind variants;    /* Hover, focus, responsive variants (optional) */
```

### @layer

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  h1 { @apply text-2xl; }
  h2 { @apply text-xl; }
}

@layer components {
  .btn-blue {
    @apply bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded;
  }
  .card {
    background-color: theme('colors.white');
    border-radius: theme('borderRadius.lg');
    padding: theme('spacing.6');
    box-shadow: theme('boxShadow.xl');
  }
}

@layer utilities {
  .content-auto { content-visibility: auto; }
}
```

### @apply

```css
.select2-dropdown { @apply rounded-b-lg shadow-md; }
.select2-search { @apply border border-gray-300 rounded; }

/* With !important */
.btn { @apply font-bold py-2 px-4 rounded !important; }

/* Sass/SCSS workaround */
.btn { @apply font-bold py-2 px-4 rounded #{!important}; }
```

> ⚠️ Per-component `@apply` (Vue/Svelte `<style>`) cannot reference classes defined in global CSS. Use plugin system instead.

### theme() Function

```css
.content-area { height: calc(100vh - theme(spacing.12)); }
.sidebar { width: theme(spacing[2.5]); }
.btn-blue { background-color: theme(colors.blue.500); }
.overlay { background-color: theme(colors.blue.500 / 75%); }
```

### screen() Function

```css
@media screen(sm) { /* Resolves to @media (min-width: 640px) */ }
```

## Dark Mode (v3)

### Media strategy (default)

```js
module.exports = { darkMode: 'media' };
// Uses prefers-color-scheme automatically
```

### Class strategy

```js
module.exports = { darkMode: 'class' };
```

### Selector strategy (v3.4.1+)

```js
module.exports = { darkMode: 'selector' };
// Replaced 'class' strategy in v3.4.1
```

### HTML Usage

```html
<html class="dark">
  <body>
    <div class="bg-white dark:bg-gray-800">
      <h1 class="text-gray-900 dark:text-white">Title</h1>
    </div>
  </body>
</html>
```

### JS Toggle

```js
// Support light, dark, and system preference
if (localStorage.theme === 'dark' || (
  !('theme' in localStorage) &&
  window.matchMedia('(prefers-color-scheme: dark)').matches
)) {
  document.documentElement.classList.add('dark');
} else {
  document.documentElement.classList.remove('dark');
}

localStorage.theme = 'light';  // Force light
localStorage.theme = 'dark';   // Force dark
localStorage.removeItem('theme'); // Respect OS
```

> ⚠️ v4: Use `@custom-variant dark (&:where(.dark, .dark *))` — no JS config.

## Responsive Design (v3)

### Default Breakpoints

| Prefix | Min width | CSS |
|:-------|:----------|:----|
| `sm:` | 640px | `@media (min-width: 640px)` |
| `md:` | 768px | `@media (min-width: 768px)` |
| `lg:` | 1024px | `@media (min-width: 1024px)` |
| `xl:` | 1280px | `@media (min-width: 1280px)` |
| `2xl:` | 1536px | `@media (min-width: 1536px)` |

### Mobile-First

```html
<img class="w-16 md:w-32 lg:w-48" src="..." />
<div class="flex flex-col md:flex-row">
  <div class="md:w-1/3">Sidebar</div>
  <div class="md:w-2/3">Content</div>
</div>
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

### Arbitrary Breakpoints

```html
<div class="min-[320px]:text-center max-[600px]:bg-sky-300">...</div>
```

## Arbitrary Values (v3)

```html
<div class="top-[117px] lg:top-[344px]">Positioning</div>
<div class="bg-[#bada55] text-[22px]">Colors & sizing</div>
<div class="before:content-['Hello']">Pseudo-elements</div>
<div class="grid grid-cols-[fit-content(theme(spacing.32))]">Grid</div>
<div class="bg-[--my-color]">CSS variables (no var() needed)</div>

<!-- Arbitrary properties -->
<div class="[mask-type:luminance]">Any CSS property</div>
<!-- Arbitrary variants -->
<div class="[&:nth-child(3)]:underline">Custom selectors</div>
```

## Plugins (v3)

### Official Plugins

```js
module.exports = {
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
    require('@tailwindcss/aspect-ratio'),
    require('@tailwindcss/container-queries'),
  ],
};
```

> ⚠️ v4: `@plugin "@tailwindcss/forms"` in CSS.

### Writing Custom Plugins

```js
const plugin = require('tailwindcss/plugin');

module.exports = {
  plugins: [
    plugin(function({ addUtilities, addComponents, addVariant, theme }) {
      // Add utilities
      addUtilities({
        '.content-auto': { 'content-visibility': 'auto' },
      });

      // Add components
      addComponents({
        '.card': {
          backgroundColor: theme('colors.white'),
          borderRadius: theme('borderRadius.lg'),
          padding: theme('spacing.6'),
          boxShadow: theme('boxShadow.xl'),
        },
      });

      // Add variants
      addVariant('hocus', ['&:hover', '&:focus']);
      addVariant('supports-grid', '@supports (display: grid)');
    }),
  ],
};
```

> ⚠️ v4: `@custom-variant hocus (&:hover, &:focus)` in CSS.

### Exposing Plugin Options

```js
const plugin = require('tailwindcss/plugin');

module.exports = plugin.withOptions(
  function(options = {}) {
    return function({ addComponents }) {
      addComponents({
        '.btn': {
          padding: options.padding ?? '.5rem 1rem',
        },
      });
    };
  },
  function(options = {}) {
    return { theme: { extend: {} } };
  }
);
```

## Custom Colors (v3)

```js
const colors = require('tailwindcss/colors');

module.exports = {
  theme: {
    colors: {
      transparent: 'transparent',
      current: 'currentColor',
      black: colors.black,
      white: colors.white,
      gray: colors.gray,
      brand: {
        50: '#eff6ff', 100: '#dbeafe',
        500: '#3b82f6', 700: '#1d4ed8', 900: '#1e3a5f',
      },
    },
  },
};
```

> ⚠️ v4: `--color-brand-500: #3b82f6` in `@theme {}`.

## v3 → v4 Migration Checklist

1. **Remove `tailwind.config.js`** → Move to `@theme {}` in CSS
2. **Replace `@tailwind` directives** → `@import "tailwindcss"`
3. **Replace `require()` plugins** → `@plugin "name"`
4. **Remove `content: [...]`** → Auto-detected in v4
5. **Update `darkMode: 'class'`** → `@custom-variant dark (...)`
6. **Move `theme.extend.colors`** → `--color-*` in `@theme`
7. **Move `theme.screens`** → `--breakpoint-*` in `@theme`
8. **Replace `addVariant()` plugins** → `@custom-variant` in CSS
9. **Replace `theme()` function** → `var(--spacing-*)` CSS variables
10. **Update Sass/SCSS `@apply`** → Check v4 @apply compatibility
