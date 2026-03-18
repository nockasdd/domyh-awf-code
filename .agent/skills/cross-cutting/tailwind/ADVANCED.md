# Tailwind CSS — Advanced Patterns

## Table of Contents

- [Plugin Development](#plugin-development)
- [Custom Design System](#custom-design-system)
- [Component Patterns](#component-patterns)
- [Animation System](#animation-system)
- [Dark Mode Advanced](#dark-mode-advanced)
- [Responsive Strategies](#responsive-strategies)

---

## Plugin Development

### Custom Utilities Plugin

```javascript
// tailwind.config.js (v4: CSS-based, v3: JS-based)
import plugin from 'tailwindcss/plugin'

export default {
  plugins: [
    plugin(function ({ addUtilities, matchUtilities, theme }) {
      // Static utilities
      addUtilities({
        '.text-balance': { 'text-wrap': 'balance' },
        '.text-pretty': { 'text-wrap': 'pretty' },
        '.scrollbar-hide': {
          '-ms-overflow-style': 'none',
          'scrollbar-width': 'none',
          '&::-webkit-scrollbar': { display: 'none' },
        },
      })

      // Dynamic utilities: glass-10, glass-20, glass-50
      matchUtilities(
        {
          glass: (value) => ({
            background: `rgba(255, 255, 255, ${value})`,
            'backdrop-filter': `blur(${parseFloat(value) * 40}px)`,
            border: '1px solid rgba(255, 255, 255, 0.2)',
          }),
        },
        { values: { 10: '0.1', 20: '0.2', 50: '0.5', 80: '0.8' } }
      )
    }),
  ],
}
```

### Component Plugin

```javascript
plugin(function ({ addComponents, theme }) {
  addComponents({
    '.btn': {
      padding: `${theme('spacing.2')} ${theme('spacing.4')}`,
      borderRadius: theme('borderRadius.lg'),
      fontWeight: theme('fontWeight.semibold'),
      fontSize: theme('fontSize.sm'),
      transition: 'all 150ms ease',
      cursor: 'pointer',
      '&:focus-visible': {
        outline: `2px solid ${theme('colors.blue.500')}`,
        outlineOffset: '2px',
      },
    },
    '.btn-primary': {
      backgroundColor: theme('colors.blue.600'),
      color: theme('colors.white'),
      '&:hover': { backgroundColor: theme('colors.blue.700') },
    },
  })
})
```

---

## Custom Design System

### CSS-First Tokens (v4+)

```css
/* app.css — Tailwind v4 CSS-first config */
@import "tailwindcss";

@theme {
  /* Color System */
  --color-brand-50: oklch(0.97 0.01 250);
  --color-brand-500: oklch(0.55 0.15 250);
  --color-brand-900: oklch(0.25 0.08 250);

  /* Spacing Scale */
  --spacing-4xs: 0.125rem;
  --spacing-3xs: 0.25rem;
  --spacing-2xs: 0.375rem;

  /* Typography */
  --font-sans: 'Inter Variable', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;

  /* Radius */
  --radius-card: 0.75rem;
  --radius-button: 0.5rem;
  --radius-input: 0.375rem;

  /* Shadows */
  --shadow-card: 0 1px 3px oklch(0 0 0 / 0.08), 0 1px 2px oklch(0 0 0 / 0.04);
  --shadow-elevated: 0 10px 25px oklch(0 0 0 / 0.1);

  /* Animation durations */
  --duration-fast: 150ms;
  --duration-normal: 300ms;
  --duration-slow: 500ms;
}
```

### Semantic Token Layer

```css
@layer base {
  :root {
    --surface-primary: var(--color-white);
    --surface-secondary: var(--color-gray-50);
    --text-primary: var(--color-gray-900);
    --text-secondary: var(--color-gray-600);
    --border-default: var(--color-gray-200);
  }

  .dark {
    --surface-primary: var(--color-gray-900);
    --surface-secondary: var(--color-gray-800);
    --text-primary: var(--color-gray-50);
    --text-secondary: var(--color-gray-400);
    --border-default: var(--color-gray-700);
  }
}
```

---

## Component Patterns

### Card Pattern (No @apply)

```html
<!-- ✅ Utility-first approach (recommended over @apply) -->
<div class="group rounded-card bg-[var(--surface-primary)] border border-[var(--border-default)]
            shadow-card hover:shadow-elevated transition-shadow duration-normal">
  <div class="p-6">
    <h3 class="text-lg font-semibold text-[var(--text-primary)]
               group-hover:text-brand-500 transition-colors">
      {{ title }}
    </h3>
    <p class="mt-2 text-sm text-[var(--text-secondary)] line-clamp-3">
      {{ description }}
    </p>
  </div>
</div>
```

### Form Components

```html
<!-- Input with states -->
<label class="block text-sm font-medium text-[var(--text-primary)]">
  Email
  <input
    type="email"
    class="mt-1 block w-full rounded-input border border-[var(--border-default)]
           bg-[var(--surface-primary)] px-3 py-2 text-sm
           placeholder:text-[var(--text-secondary)]
           focus:outline-none focus:ring-2 focus:ring-brand-500/50 focus:border-brand-500
           disabled:opacity-50 disabled:cursor-not-allowed
           invalid:border-red-500 invalid:ring-red-500/50"
    placeholder="you@example.com"
  />
</label>
```

---

## Animation System

### Custom Keyframes

```css
@theme {
  --animate-fade-in: fade-in var(--duration-normal) ease-out;
  --animate-slide-up: slide-up var(--duration-normal) ease-out;
  --animate-scale-in: scale-in var(--duration-fast) ease-out;
}

@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slide-up {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes scale-in {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}
```

### Transition Groups (Vue/Nuxt)

```css
/* Staggered list animation */
.list-enter-active {
  transition: all var(--duration-normal) ease-out;
}
.list-enter-from {
  opacity: 0;
  transform: translateX(-20px);
}
.list-move {
  transition: transform var(--duration-normal) ease;
}
```

---

## Dark Mode Advanced

### Multi-Theme System

```css
/* Beyond light/dark — custom themes */
[data-theme="ocean"] {
  --color-brand-500: oklch(0.6 0.15 230);
  --surface-primary: oklch(0.15 0.02 230);
  --text-primary: oklch(0.9 0.01 230);
}

[data-theme="forest"] {
  --color-brand-500: oklch(0.55 0.12 145);
  --surface-primary: oklch(0.15 0.02 145);
  --text-primary: oklch(0.9 0.01 145);
}
```

```typescript
// composables/useTheme.ts
export function useTheme() {
  const theme = useState('theme', () => 'system')

  const applyTheme = (t: string) => {
    document.documentElement.setAttribute('data-theme', t)
    if (t === 'dark' || (t === 'system' && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }

  return { theme, applyTheme }
}
```

---

## Responsive Strategies

### Container Queries

```css
@theme {
  /* Container query breakpoints */
  --container-sm: 24rem;
  --container-md: 32rem;
  --container-lg: 48rem;
}
```

```html
<!-- Container queries with @container -->
<div class="@container">
  <div class="grid grid-cols-1 @sm:grid-cols-2 @lg:grid-cols-3 gap-4">
    <!-- Cards adapt to container, not viewport -->
  </div>
</div>
```

### Fluid Typography

```css
@theme {
  /* Fluid type scale: min at 375px, max at 1440px */
  --text-fluid-sm: clamp(0.875rem, 0.8rem + 0.2vw, 1rem);
  --text-fluid-base: clamp(1rem, 0.9rem + 0.3vw, 1.125rem);
  --text-fluid-lg: clamp(1.25rem, 1rem + 0.5vw, 1.5rem);
  --text-fluid-xl: clamp(1.5rem, 1.1rem + 1vw, 2.25rem);
  --text-fluid-2xl: clamp(2rem, 1.2rem + 2vw, 3.5rem);
}
```

---
