---
name: tailwind
detect:
  [
    "tailwind.config.js",
    "tailwind.config.ts",
    "@tailwind",
    '@import "tailwindcss"',
  ]
version: "6.0.0"
category: styling
tier: 1
---

# Tailwind CSS Patterns — DOMYH Awesome Code v5.5

> **Version**: Tailwind CSS 4 (2025-2026)
> **Philosophy**: CSS-first configuration, utility-first styling

---

## 🎯 When to Use This Skill

Use for: Utility-first CSS, rapid UI development, design systems.
**NOT for**: CSS-in-JS (→ styled-components), traditional CSS.

---

## 📦 Recommended Stack (2025-2026)

### Core

| Tool               | Use Case            |
| ------------------ | ------------------- |
| **Tailwind CSS 4** | Utility-first 🏆    |
| **Vite plugin**    | Bundler integration |
| **PostCSS**        | Processing          |

### Components

| Library         | Use Case              |
| --------------- | --------------------- |
| **shadcn/ui**   | Radix + Tailwind 🏆   |
| **Headless UI** | Accessible primitives |
| **DaisyUI**     | Component library     |

### IDE Support

| IDE                        | Features                       |
| -------------------------- | ------------------------------ |
| **VS Code + IntelliSense** | Autocomplete, hover preview 🏆 |
| **WebStorm**               | Built-in Tailwind support      |

---

## 🆕 Tailwind CSS 4 Features

### CSS-First Configuration

```css
/* app.css - No more tailwind.config.js! */
@import "tailwindcss";

/* 🆕 Define theme in CSS */
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

### Custom Utilities

```css
/* 🆕 @utility replaces @layer utilities */
@utility scrollbar-hidden {
  scrollbar-width: none;
  &::-webkit-scrollbar {
    display: none;
  }
}

@utility text-balance {
  text-wrap: balance;
}

/* Usage: <p class="scrollbar-hidden text-balance">...</p> */
```

### New Utilities in v4

```html
<!-- Container Queries -->
<div class="@container">
  <div class="@lg:flex @md:grid">...</div>
</div>

<!-- Field Sizing -->
<textarea class="field-sizing-content"></textarea>

<!-- Color Scheme -->
<html class="color-scheme-dark">
  <!-- 3D Transforms -->
  <div class="rotate-x-12 rotate-y-6 perspective-500">
    <!-- Inert State -->
    <div class="inert:opacity-50 inert:pointer-events-none"></div>
  </div>
</html>
```

---

## 🔧 Core Patterns

### Component Styling

```html
<!-- ✅ Organized utility groups -->
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
  /* States */
  hover:bg-primary/90 focus:ring-2 focus:ring-primary/50
  /* Transitions */
  transition-all duration-200
  /* Disabled */
  disabled:opacity-50 disabled:cursor-not-allowed
"
>
  Click me
</button>
```

### Component Extraction (Sparingly)

```css
/* components.css */
@utility btn-primary {
  @apply inline-flex items-center justify-center gap-2
         px-4 py-2 min-w-32
         text-sm font-medium
         bg-primary text-white
         rounded-lg shadow-md
         hover:bg-primary/90 focus:ring-2 focus:ring-primary/50
         transition-all duration-200
         disabled:opacity-50 disabled:cursor-not-allowed;
}

/* ⚠️ Use sparingly - prefer utilities inline */
```

### Responsive Design

```html
<!-- Mobile-first approach -->
<div
  class="
  /* Mobile */
  flex flex-col gap-4 p-4
  /* Tablet */
  md:flex-row md:gap-6 md:p-6
  /* Desktop */
  lg:gap-8 lg:p-8
  /* Large */
  xl:max-w-7xl xl:mx-auto
"
></div>
```

### Dark Mode

```html
<!-- With OS preference -->
<html class="dark:bg-gray-900 dark:text-white">
  <!-- Toggle-based -->
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
  --radius-full: 9999px;
}
```

---

## ⚡ Performance Best Practices

```css
/* ✅ Limit theme scope */
@theme {
  /* Only define what you need */
  --color-*: initial; /* Remove unused color scales */
}

/* ✅ Content configuration for tree-shaking */
@source "./src/**/*.{html,js,ts,jsx,tsx,vue,svelte}";
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
- [ ] Minify for production
- [ ] Use JIT (default in v4)

### Design System

- [ ] Define semantic colors
- [ ] Create custom utilities sparingly
- [ ] Document design tokens
- [ ] Use CSS variables for theming

---

_DOMYH Awesome Code v6.0.0 • Tailwind CSS 4_
