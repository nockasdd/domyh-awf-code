---
name: tailwind
detect:
  [
    "tailwind.config.js",
    "tailwind.config.ts",
    "@tailwind",
    '@import "tailwindcss"',
  ]
version: "6.4.5"
category: styling
tier: 1
---

# Tailwind CSS Patterns — DOMYH Awesome Code

> **Version**: Tailwind CSS 4.1 (2025-2026)
> **Philosophy**: CSS-first configuration, utility-first styling

---

## 🎯 When to Use This Skill

Use for: Utility-first CSS, rapid UI development, design systems.
**NOT for**: CSS-in-JS (→ styled-components), traditional CSS.

---

## 📦 What's New in Tailwind CSS 4.1 (2025)

| Feature                   | Description           |
| ------------------------- | --------------------- |
| **text-shadow-\***        | Text shadow utilities |
| **mask-\***               | Image/gradient masks  |
| **pointer-\***            | Input device queries  |
| **drop-shadow-\<color\>** | Colored drop shadows  |
| **noscript variant**      | No-JS styling         |
| **@source not**           | Ignore directories    |

---

## 📦 Recommended Stack

| Tool                 | Use Case              |
| -------------------- | --------------------- |
| **Tailwind CSS 4.1** | Utility-first 🏆      |
| **Vite plugin**      | Bundler integration   |
| **shadcn/ui**        | Radix + Tailwind 🏆   |
| **Headless UI**      | Accessible primitives |

---

## 🆕 CSS-First Configuration (v4+)

```css
/* app.css - No more tailwind.config.js! */
@import "tailwindcss";

@theme {
  /* Colors */
  --color-primary: #3b82f6;
  --color-secondary: #8b5cf6;
  --color-accent: #06b6d4;

  /* Typography */
  --font-sans: "Inter", sans-serif;
  --font-mono: "JetBrains Mono", monospace;

  /* Spacing */
  --spacing-18: 4.5rem;
  --spacing-22: 5.5rem;

  /* Animation */
  --animate-slide-in: slide-in 0.3s ease-out;
}

@keyframes slide-in {
  from {
    transform: translateX(-100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}
```

---

## 🆕 Text Shadow Utilities (v4.1)

```html
<!-- Text shadows with size variants -->
<h1 class="text-shadow-sm">Subtle shadow</h1>
<h1 class="text-shadow-md">Medium shadow</h1>
<h1 class="text-shadow-lg">Large shadow</h1>

<!-- Colored text shadows -->
<h1 class="text-shadow-lg text-shadow-blue-500/50">Blue glow effect</h1>

<!-- Dark mode compatible -->
<h1 class="text-shadow-lg dark:text-shadow-white/20">Adaptive shadow</h1>
```

---

## 🆕 Mask Utilities (v4.1)

```html
<!-- Gradient masks -->
<div class="mask-linear-to-b">Fades to transparent at bottom</div>

<div class="mask-radial">Circular fade from center</div>

<!-- Image masks -->
<div class="mask-[url('/mask.svg')]">Custom shape mask</div>

<!-- Combine with gradients -->
<img src="/photo.jpg" class="mask-linear-to-r from-black to-transparent" />
```

---

## 🆕 Pointer Media Queries (v4.1)

```html
<!-- Target touch devices -->
<button
  class="
  p-2 pointer-fine:p-1
  pointer-coarse:p-4 pointer-coarse:text-lg
"
>
  Touch-friendly button
</button>

<!-- Hover only on pointer devices -->
<div
  class="
  any-pointer-fine:hover:scale-105
  any-pointer-coarse:active:scale-95
"
>
  Adaptive interaction
</div>
```

---

## 🆕 Colored Drop Shadows (v4.1)

```html
<!-- Colored drop shadows -->
<div class="drop-shadow-lg drop-shadow-blue-500/50">Blue shadow</div>

<!-- Multiple shadows -->
<div
  class="
  drop-shadow-md drop-shadow-red-500/30
  hover:drop-shadow-lg hover:drop-shadow-red-500/50
"
>
  Hover glow effect
</div>
```

---

## 🔧 Core Patterns

### Component Styling

```html
<button
  class="
  /* Layout */
  inline-flex items-center justify-center gap-2
  /* Sizing */
  px-4 py-2 min-w-32
  /* Typography */
  text-sm font-medium
  /* Colors */
  bg-primary text-white
  /* Effects */
  rounded-lg shadow-md
  /* 🆕 Text shadow */
  text-shadow-sm
  /* States */
  hover:bg-primary/90 focus:ring-2 focus:ring-primary/50
  /* Transition */
  transition-all duration-200
  /* Disabled */
  disabled:opacity-50 disabled:cursor-not-allowed
"
>
  Click me
</button>
```

### Responsive Design

```html
<!-- Mobile-first approach -->
<div
  class="
  flex flex-col gap-4 p-4
  md:flex-row md:gap-6 md:p-6
  lg:gap-8 lg:p-8
  xl:max-w-7xl xl:mx-auto
"
></div>
```

### Container Queries

```html
<div class="@container">
  <div class="@lg:flex @md:grid @sm:block">Adapts to container size</div>
</div>
```

### Dark Mode

```html
<html class="dark:bg-gray-900 dark:text-white">
  <button
    class="bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
    onclick="document.documentElement.classList.toggle('dark')"
  >
    Toggle Theme
  </button>
</html>
```

---

## 🎨 Design Tokens

```css
@theme {
  /* Color Scales */
  --color-gray-50: #f9fafb;
  --color-gray-100: #f3f4f6;
  --color-gray-900: #111827;

  /* Semantic Colors */
  --color-success: #10b981;
  --color-warning: #f59e0b;
  --color-error: #ef4444;

  /* Shadows */
  --shadow-sm: 0 1px 2px rgb(0 0 0 / 0.05);
  --shadow-lg: 0 10px 15px rgb(0 0 0 / 0.1);

  /* Border Radius */
  --radius-sm: 0.25rem;
  --radius-md: 0.375rem;
  --radius-lg: 0.5rem;
}
```

---

## 🆕 New Variants (v4.1)

```html
<!-- noscript variant -->
<div class="hidden noscript:block">JavaScript is disabled</div>

<!-- user-valid/user-invalid -->
<input
  class="
  border-gray-300
  user-valid:border-green-500
  user-invalid:border-red-500
"
/>

<!-- inverted-colors -->
<div class="inverted-colors:invert">Respects OS accessibility setting</div>
```

---

## ⚡ Build Optimization

```css
/* Limit theme scope */
@theme {
  --color-*: initial; /* Remove unused colors */
}

/* Content configuration */
@source "./src/**/*.{html,js,ts,jsx,tsx,vue,svelte}";

/* Ignore directories */
@source not "./src/legacy/*";
```

---

## ✅ Best Practices Checklist

### Code Quality

- [ ] Mobile-first responsive design
- [ ] Organized utility groups
- [ ] Minimal @apply usage
- [ ] Consistent spacing scale

### Performance

- [ ] Configure content sources
- [ ] Remove unused color scales
- [ ] Use JIT (default in v4)
- [ ] @source not for unused paths

### Design System

- [ ] Define semantic colors in @theme
- [ ] Use CSS variables for theming
- [ ] Document design tokens

---

## 🔌 HSA Integration

Data files available in `data/` directory (indexed by HSA engine):

| File              | Content                            |
| ----------------- | ---------------------------------- |
| `config.yaml`     | CSS-first @theme configuration     |
| `utilities.yaml`  | Utility class patterns             |
| `variants.yaml`   | New v4 variants (not-\*, starting) |
| `responsive.yaml` | Breakpoints, container queries     |
| `states.yaml`     | Hover, focus, active patterns      |
| `theme.yaml`      | Design token structure             |
| `build.yaml`      | Build optimization, @source        |
| `migration.yaml`  | v3 → v4 migration guide            |

Agent reads these YAML files directly for pattern lookup.

---

_DOMYH Awesome Code • Tailwind CSS 4.1 • 2026_
