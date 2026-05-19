---
library: tailwindcss
version: 4.x
latest: true
category: css
official_docs: https://tailwindcss.com/docs/
last_updated: 2026-03-20
last_checked: 2026-03-21
---

# Tailwind CSS v4

> A utility-first CSS framework for rapidly building custom user interfaces.
> Version: 4.x | License: MIT | Source: https://tailwindcss.com/docs/

## Installation

### Using Vite (Recommended)

The most seamless way to integrate Tailwind CSS with frameworks like Laravel, SvelteKit, React Router, Nuxt, and SolidJS.

```bash
# 1. Create project
npm create vite@latest my-project
cd my-project

# 2. Install Tailwind + Vite plugin
npm install tailwindcss @tailwindcss/vite

# 3. Configure vite.config.ts
```

```ts
import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [
    tailwindcss(),
  ],
})
```

```css
/* 4. In your main CSS file: */
@import "tailwindcss";
```

```html
<!-- 5. Start using utilities in HTML -->
<h1 class="text-3xl font-bold underline">Hello world!</h1>
```

### Using PostCSS

```bash
npm install tailwindcss @tailwindcss/postcss postcss
```

```js
// postcss.config.mjs
export default {
  plugins: {
    "@tailwindcss/postcss": {},
  },
};
```

### Using CLI

```bash
npx @tailwindcss/cli -i input.css -o output.css --watch
```

### Play CDN (Prototyping Only)

```html
<script src="https://cdn.tailwindcss.com"></script>
```

## Core Concepts: Utility-First

Style elements by combining single-purpose presentational classes directly in markup:

```html
<div class="mx-auto flex max-w-sm items-center gap-x-4 rounded-xl bg-white p-6 shadow-lg">
  <img class="size-12 shrink-0" src="/img/logo.svg" alt="Logo" />
  <div>
    <div class="text-xl font-medium text-black">ChitChat</div>
    <p class="text-gray-500">You have a new message!</p>
  </div>
</div>
```

### Key Utility Categories

| Category | Examples | CSS Property |
|:---------|:---------|:-------------|
| Display | `flex`, `block`, `grid`, `hidden` | display |
| Padding | `p-6`, `px-4`, `py-2`, `pt-8` | padding |
| Margin | `m-4`, `mx-auto`, `mt-2`, `-ml-1` | margin |
| Width | `w-16`, `w-full`, `w-1/2`, `w-screen` | width |
| Height | `h-12`, `h-full`, `h-screen` | height |
| Size | `size-12` (width + height) | width & height |
| Background | `bg-white`, `bg-sky-500`, `bg-black/50` | background-color |
| Text Color | `text-gray-900`, `text-white` | color |
| Font | `font-bold`, `font-medium`, `font-mono` | font-weight, font-family |
| Border | `rounded-xl`, `border`, `border-gray-200` | border-radius, border |
| Shadow | `shadow-lg`, `shadow-md`, `shadow-sm` | box-shadow |
| Gap | `gap-4`, `gap-x-4`, `gap-y-2` | gap |

### Arbitrary Values

Use brackets for one-off custom values:

```html
<div class="w-[200px] h-[calc(100vh-4rem)] bg-[#1da1f2] text-[14px]">
  Custom values
</div>
```

CSS variables shorthand:

```html
<div class="p-(--my-padding) text-(length:--my-font-size)">
  CSS variable shorthand
</div>
```

## Hover, Focus, and Other States

### Pseudo-Classes

Prefix any utility with a state variant:

```html
<!-- Hover -->
<button class="bg-sky-500 hover:bg-sky-700">Save changes</button>

<!-- Focus -->
<button class="bg-violet-500 focus:outline-2 focus:outline-offset-2 focus:outline-violet-500">
  Save changes
</button>

<!-- Active -->
<button class="bg-violet-500 active:bg-violet-700">Save changes</button>

<!-- Disabled -->
<button class="bg-sky-500 disabled:opacity-50 disabled:cursor-not-allowed">
  Submit
</button>

<!-- Stacking variants -->
<button class="bg-sky-500 disabled:hover:bg-sky-500">Save changes</button>
```

### First, Last, Odd, Even

```html
<!-- Remove padding on first/last child -->
<li class="flex py-4 first:pt-0 last:pb-0">...</li>

<!-- Alternating row colors -->
<tr class="odd:bg-white even:bg-gray-50 dark:odd:bg-gray-900/50 dark:even:bg-gray-950">
  ...
</tr>

<!-- Nth child -->
<div class="nth-3:underline nth-last-5:underline">...</div>
```

### Group & Peer (Parent/Sibling State)

```html
<!-- Style children based on parent hover -->
<div class="group rounded-lg p-4 hover:bg-sky-500">
  <p class="text-gray-500 group-hover:text-white">Description</p>
</div>

<!-- Style sibling based on input state -->
<input class="peer" type="email" />
<p class="invisible peer-invalid:visible text-red-600">Invalid email</p>
```

### :has() and :not()

```html
<div class="has-[img]:grid has-[img]:grid-cols-2">
  Adapts layout when contains images
</div>

<div class="not-last:mb-4">
  Margin-bottom on all except last
</div>
```

### Pseudo-Elements

```html
<!-- Before/After -->
<blockquote class="before:content-['"'] before:text-3xl">
  Inspiration text
</blockquote>

<!-- Placeholder -->
<input class="placeholder:text-gray-400 placeholder:italic" placeholder="Search..." />

<!-- Selection highlight -->
<p class="selection:bg-fuchsia-300 selection:text-fuchsia-900">
  Try selecting this text
</p>

<!-- File input button -->
<input type="file" class="file:mr-4 file:rounded-full file:border-0 file:bg-violet-50 file:px-4 file:py-2 file:text-sm file:font-semibold file:text-violet-700 hover:file:bg-violet-100" />

<!-- List markers -->
<ul class="marker:text-sky-400 list-disc">
  <li>Item one</li>
</ul>
```

## Responsive Design

Mobile-first breakpoint system. Unprefixed = all sizes. Prefixed = that breakpoint and above.

### Default Breakpoints

| Prefix | Min width | CSS |
|:-------|:----------|:----|
| `sm:` | 40rem (640px) | `@media (width >= 40rem)` |
| `md:` | 48rem (768px) | `@media (width >= 48rem)` |
| `lg:` | 64rem (1024px) | `@media (width >= 64rem)` |
| `xl:` | 80rem (1280px) | `@media (width >= 80rem)` |
| `2xl:` | 96rem (1536px) | `@media (width >= 96rem)` |

### Usage Examples

```html
<!-- Responsive width -->
<img class="w-16 md:w-32 lg:w-48" src="..." />

<!-- Responsive layout -->
<div class="flex flex-col md:flex-row">
  <div class="md:w-1/3">Sidebar</div>
  <div class="md:w-2/3">Content</div>
</div>

<!-- Hide/show at breakpoints -->
<nav class="hidden lg:block">Desktop nav</nav>
<nav class="lg:hidden">Mobile nav</nav>

<!-- Responsive grid -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
  <div>Item</div>
</div>
```

### Breakpoint Ranges

```html
<!-- Only md to lg -->
<div class="md:max-lg:flex">Only flex between md and lg</div>

<!-- Custom breakpoints -->
<div class="min-[800px]:grid-cols-3">Custom breakpoint</div>
```

### Container Queries

```html
<!-- Define container -->
<div class="@container">
  <!-- Use container breakpoints -->
  <div class="@sm:grid-cols-2 @lg:grid-cols-3">
    Adapts to parent container width
  </div>
</div>

<!-- Named containers -->
<div class="@container/main">
  <div class="@lg/main:grid-cols-3">Named container query</div>
</div>
```

### Custom Breakpoints

```css
@import "tailwindcss";
@theme {
  --breakpoint-sm: 30rem;  /* Override default */
  --breakpoint-3xl: 120rem; /* Add new */
}
```

## Dark Mode

### Using prefers-color-scheme (Default)

```html
<div class="bg-white dark:bg-gray-800">
  <h3 class="text-gray-900 dark:text-white">Title</h3>
  <p class="text-gray-500 dark:text-gray-400">Description</p>
</div>
```

### Manual Toggle (Class-Based)

```css
@import "tailwindcss";
@custom-variant dark (&:where(.dark, .dark *));
```

```html
<html class="dark">
  <body>
    <div class="bg-white dark:bg-black">
      Controlled by .dark class
    </div>
  </body>
</html>
```

```js
// Toggle dark mode with JavaScript
document.documentElement.classList.toggle('dark');
localStorage.setItem('theme', 'dark');
```

### Data Attribute Method

```css
@custom-variant dark (&:where([data-theme=dark], [data-theme=dark] *));
```

```html
<html data-theme="dark">...</html>
```

## Layout: Display

```html
<!-- Block & Inline -->
<span class="inline">Inline element</span>
<span class="inline-block">Inline block</span>
<div class="block">Block element</div>

<!-- Flex -->
<div class="flex items-center gap-4">Flex container</div>
<span class="inline-flex items-baseline">Inline flex</span>

<!-- Grid -->
<div class="grid grid-cols-3 gap-4">Grid container</div>

<!-- Hidden / Screen Reader Only -->
<div class="hidden">Not rendered</div>
<span class="sr-only">Screen reader only</span>
<span class="not-sr-only">Undo sr-only</span>

<!-- Contents (remove wrapper) -->
<div class="contents">Children act as direct children of parent</div>

<!-- Flow Root (BFC) -->
<div class="flow-root">Creates Block Formatting Context</div>
```

### Position

```html
<div class="relative">
  <div class="absolute top-0 right-0">Top-right corner</div>
</div>
<div class="fixed bottom-4 right-4">Fixed FAB</div>
<div class="sticky top-0">Sticky header</div>
```

### Overflow

```html
<div class="overflow-auto">Scrollable when needed</div>
<div class="overflow-hidden">Clip overflow</div>
<div class="overflow-x-auto overflow-y-hidden">Horizontal scroll only</div>
```

### Z-Index

```html
<div class="z-10">z-index: 10</div>
<div class="z-50">z-index: 50</div>
<div class="-z-10">z-index: -10</div>
<div class="z-auto">z-index: auto</div>
```

## Flexbox

### Direction & Wrapping

```html
<div class="flex flex-row">Horizontal (default)</div>
<div class="flex flex-col">Vertical</div>
<div class="flex flex-row-reverse">Reversed horizontal</div>
<div class="flex flex-wrap">Allow wrapping</div>
<div class="flex flex-nowrap">No wrapping</div>
```

### Flex Items

```html
<div class="flex">
  <div class="flex-1">Grows and shrinks, ignores initial size</div>
  <div class="flex-auto">Grows and shrinks, considers initial size</div>
  <div class="flex-initial">Shrinks but doesn't grow</div>
  <div class="flex-none">Fixed size, no grow/shrink</div>
</div>

<!-- Custom flex -->
<div class="flex-[3_1_auto]">flex: 3 1 auto</div>
```

### Grow & Shrink

```html
<div class="grow">flex-grow: 1</div>
<div class="grow-0">flex-grow: 0</div>
<div class="shrink">flex-shrink: 1</div>
<div class="shrink-0">flex-shrink: 0</div>
```

### Alignment

```html
<!-- Justify (main axis) -->
<div class="flex justify-start">Left</div>
<div class="flex justify-center">Center</div>
<div class="flex justify-end">Right</div>
<div class="flex justify-between">Space between</div>
<div class="flex justify-around">Space around</div>
<div class="flex justify-evenly">Space evenly</div>

<!-- Align Items (cross axis) -->
<div class="flex items-start">Top</div>
<div class="flex items-center">Center</div>
<div class="flex items-end">Bottom</div>
<div class="flex items-stretch">Stretch (default)</div>
<div class="flex items-baseline">Baseline</div>

<!-- Self alignment -->
<div class="self-auto">auto</div>
<div class="self-start">start</div>
<div class="self-center">center</div>
<div class="self-end">end</div>
<div class="self-stretch">stretch</div>
```

### Order

```html
<div class="order-1">First visually</div>
<div class="order-2">Second visually</div>
<div class="order-first">order: -9999</div>
<div class="order-last">order: 9999</div>
```

## Grid

### Template Columns

```html
<!-- Equal columns -->
<div class="grid grid-cols-1">1 column</div>
<div class="grid grid-cols-2 gap-4">2 columns</div>
<div class="grid grid-cols-3 gap-4">3 columns</div>
<div class="grid grid-cols-4 gap-6">4 columns</div>
<div class="grid grid-cols-12 gap-4">12-column grid</div>

<!-- Custom columns -->
<div class="grid grid-cols-[200px_1fr_100px]">Custom column sizes</div>
<div class="grid grid-cols-[repeat(auto-fill,minmax(250px,1fr))]">Auto-fill</div>

<!-- Subgrid -->
<div class="grid grid-cols-4 gap-4">
  <div class="col-span-3 grid grid-cols-subgrid gap-4">
    <div class="col-start-2">Aligned to parent grid</div>
  </div>
</div>

<!-- Responsive -->
<div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
  Responsive grid columns
</div>
```

### Template Rows

```html
<div class="grid grid-rows-3 grid-flow-col gap-4">3 rows, flow columns</div>
<div class="grid grid-rows-[auto_1fr_auto]">Header, content, footer</div>
```

### Column/Row Span

```html
<div class="col-span-2">Span 2 columns</div>
<div class="col-span-full">Span all columns</div>
<div class="col-start-2 col-end-4">Start at col 2, end at col 4</div>
<div class="row-span-2">Span 2 rows</div>
```

### Grid Flow

```html
<div class="grid grid-flow-row">Row flow (default)</div>
<div class="grid grid-flow-col">Column flow</div>
<div class="grid grid-flow-row-dense">Row dense</div>
```

### Place Items & Content

```html
<div class="grid place-items-center">Center all items</div>
<div class="grid place-content-center">Center content tracks</div>
<div class="place-self-center">Center individual item</div>
```

## Spacing

### Padding

```html
<!-- All sides -->
<div class="p-4">padding: 1rem</div>
<div class="p-8">padding: 2rem</div>

<!-- One side -->
<div class="pt-6">padding-top: 1.5rem</div>
<div class="pr-4">padding-right: 1rem</div>
<div class="pb-8">padding-bottom: 2rem</div>
<div class="pl-2">padding-left: 0.5rem</div>

<!-- Horizontal / Vertical -->
<div class="px-4">padding-left + right: 1rem</div>
<div class="py-2">padding-top + bottom: 0.5rem</div>

<!-- Logical properties (RTL-aware) -->
<div class="ps-4">padding-inline-start: 1rem</div>
<div class="pe-4">padding-inline-end: 1rem</div>

<!-- Custom -->
<div class="p-[5px]">padding: 5px</div>
<div class="p-(--my-padding)">CSS variable</div>
```

### Margin

```html
<!-- All sides -->
<div class="m-4">margin: 1rem</div>

<!-- One side -->
<div class="mt-4">margin-top: 1rem</div>
<div class="mr-2">margin-right: 0.5rem</div>
<div class="mb-6">margin-bottom: 1.5rem</div>
<div class="ml-auto">margin-left: auto</div>

<!-- Horizontal / Vertical -->
<div class="mx-auto">Center horizontally</div>
<div class="my-4">Vertical margin: 1rem</div>

<!-- Negative margin -->
<div class="-mt-4">margin-top: -1rem</div>

<!-- Logical properties -->
<div class="ms-4">margin-inline-start: 1rem</div>
<div class="me-4">margin-inline-end: 1rem</div>
```

### Space Between (Children Spacing)

```html
<!-- Horizontal space -->
<div class="flex space-x-4">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
</div>

<!-- Vertical space -->
<div class="flex flex-col space-y-4">
  <div>Item 1</div>
  <div>Item 2</div>
</div>

<!-- Reverse spacing -->
<div class="flex flex-row-reverse space-x-reverse space-x-4">
  <div>Item 1</div>
  <div>Item 2</div>
</div>
```

### Gap (for Flex & Grid)

```html
<div class="flex gap-4">Equal gaps</div>
<div class="grid gap-x-8 gap-y-4">Different x/y gaps</div>
```

## Sizing

### Width

```html
<!-- Fixed (spacing scale) -->
<div class="w-0">0px</div>
<div class="w-px">1px</div>
<div class="w-1">0.25rem (4px)</div>
<div class="w-4">1rem (16px)</div>
<div class="w-8">2rem (32px)</div>
<div class="w-16">4rem (64px)</div>
<div class="w-32">8rem (128px)</div>
<div class="w-64">16rem (256px)</div>
<div class="w-96">24rem (384px)</div>

<!-- Percentage -->
<div class="w-full">100%</div>
<div class="w-1/2">50%</div>
<div class="w-1/3">33.333%</div>
<div class="w-2/3">66.666%</div>
<div class="w-1/4">25%</div>
<div class="w-3/4">75%</div>

<!-- Container scale -->
<div class="w-xs">20rem</div>
<div class="w-sm">24rem</div>
<div class="w-md">28rem</div>
<div class="w-lg">32rem</div>
<div class="w-xl">36rem</div>

<!-- Viewport -->
<div class="w-screen">100vw</div>
<div class="w-dvw">100dvw (dynamic viewport)</div>

<!-- Auto / Min / Max / Fit -->
<div class="w-auto">auto</div>
<div class="w-min">min-content</div>
<div class="w-max">max-content</div>
<div class="w-fit">fit-content</div>
```

### Height

```html
<div class="h-16">4rem</div>
<div class="h-full">100%</div>
<div class="h-screen">100vh</div>
<div class="h-dvh">100dvh (dynamic viewport height)</div>
<div class="h-svh">100svh (small viewport height)</div>
<div class="h-auto">auto</div>
```

### Size (Width + Height)

```html
<div class="size-12">width: 3rem; height: 3rem</div>
<div class="size-full">width: 100%; height: 100%</div>
```

### Min/Max Width & Height

```html
<div class="min-w-0">min-width: 0px</div>
<div class="min-w-full">min-width: 100%</div>
<div class="max-w-sm">max-width: 24rem</div>
<div class="max-w-md">max-width: 28rem</div>
<div class="max-w-lg">max-width: 32rem</div>
<div class="max-w-xl">max-width: 36rem</div>
<div class="max-w-2xl">max-width: 42rem</div>
<div class="max-w-7xl">max-width: 80rem</div>
<div class="max-w-full">max-width: 100%</div>
<div class="max-w-none">max-width: none</div>
<div class="max-w-prose">max-width: 65ch</div>

<div class="min-h-screen">min-height: 100vh</div>
<div class="max-h-64">max-height: 16rem</div>
```

## Typography

### Font Size

```html
<p class="text-xs">12px / 1rem</p>
<p class="text-sm">14px / 1.25rem</p>
<p class="text-base">16px / 1.5rem</p>
<p class="text-lg">18px / 1.75rem</p>
<p class="text-xl">20px / 1.75rem</p>
<p class="text-2xl">24px / 2rem</p>
<p class="text-3xl">30px / 2.25rem</p>
<p class="text-4xl">36px / 2.5rem</p>
<p class="text-5xl">48px</p>
<p class="text-6xl">60px</p>
<p class="text-7xl">72px</p>
<p class="text-8xl">96px</p>
<p class="text-9xl">128px</p>

<!-- With line-height shorthand -->
<p class="text-sm/6">14px font, 1.5rem line-height</p>
<p class="text-lg/7">18px font, 1.75rem line-height</p>
<p class="text-xl/8">20px font, 2rem line-height</p>

<!-- Custom -->
<p class="text-[14px]">Custom size</p>
<p class="text-(length:--my-size)">CSS variable</p>
```

### Font Weight

```html
<p class="font-thin">100</p>
<p class="font-extralight">200</p>
<p class="font-light">300</p>
<p class="font-normal">400</p>
<p class="font-medium">500</p>
<p class="font-semibold">600</p>
<p class="font-bold">700</p>
<p class="font-extrabold">800</p>
<p class="font-black">900</p>
```

### Font Family

```html
<p class="font-sans">System sans-serif stack</p>
<p class="font-serif">Georgia, serif stack</p>
<p class="font-mono">Monospace stack</p>

<!-- Custom font in theme -->
```

```css
@import "tailwindcss";
@theme {
  --font-display: "Inter", "sans-serif";
}
```

```html
<h1 class="font-display">Custom font family</h1>
```

### Text Color & Opacity

```html
<p class="text-black">Black</p>
<p class="text-gray-500">Gray 500</p>
<p class="text-blue-600">Blue 600</p>
<p class="text-red-500/75">Red 500 at 75% opacity</p>
<p class="text-inherit">Inherit color</p>
```

### Text Alignment & Decoration

```html
<p class="text-left">Left aligned</p>
<p class="text-center">Center aligned</p>
<p class="text-right">Right aligned</p>
<p class="text-justify">Justified</p>

<p class="underline">Underline</p>
<p class="overline">Overline</p>
<p class="line-through">Strikethrough</p>
<p class="no-underline">Remove underline</p>
<p class="underline decoration-sky-500 decoration-2 underline-offset-4">
  Styled underline
</p>
```

### Text Transform & Wrapping

```html
<p class="uppercase">UPPERCASE</p>
<p class="lowercase">lowercase</p>
<p class="capitalize">Capitalize Each Word</p>
<p class="normal-case">Normal Case</p>

<p class="truncate">Truncated with ellipsis...</p>
<p class="text-ellipsis overflow-hidden">Ellipsis on overflow</p>
<p class="whitespace-nowrap">No wrapping</p>
<p class="text-wrap">Normal wrapping</p>
<p class="text-balance">Balanced wrapping</p>
```

### Letter & Line Spacing

```html
<p class="tracking-tighter">-0.05em</p>
<p class="tracking-tight">-0.025em</p>
<p class="tracking-normal">0em</p>
<p class="tracking-wide">0.025em</p>
<p class="tracking-wider">0.05em</p>
<p class="tracking-widest">0.1em</p>

<p class="leading-none">line-height: 1</p>
<p class="leading-tight">line-height: 1.25</p>
<p class="leading-normal">line-height: 1.5</p>
<p class="leading-relaxed">line-height: 1.625</p>
<p class="leading-loose">line-height: 2</p>
```

## Backgrounds

```html
<!-- Colors -->
<div class="bg-white">White</div>
<div class="bg-gray-100">Gray 100</div>
<div class="bg-blue-500">Blue 500</div>
<div class="bg-black/50">Black at 50% opacity</div>

<!-- Gradients -->
<div class="bg-gradient-to-r from-cyan-500 to-blue-500">Left to right</div>
<div class="bg-gradient-to-br from-purple-500 via-pink-500 to-red-500">Diagonal</div>

<!-- Stops -->
<div class="bg-gradient-to-r from-indigo-500 from-10% via-sky-500 via-30% to-emerald-500 to-90%">
  With percentage stops
</div>

<!-- Background Image -->
<div class="bg-cover bg-center bg-no-repeat" style="background-image: url(...)"></div>
<div class="bg-contain">Contain</div>
<div class="bg-fixed">Fixed attachment</div>
```

## Borders

```html
<!-- Width -->
<div class="border">1px all sides</div>
<div class="border-2">2px</div>
<div class="border-4">4px</div>
<div class="border-t">1px top only</div>
<div class="border-x-2">2px left + right</div>

<!-- Color -->
<div class="border-gray-200">Gray border</div>
<div class="border-blue-500">Blue border</div>
<div class="border-transparent">Transparent</div>

<!-- Radius -->
<div class="rounded">0.25rem</div>
<div class="rounded-md">0.375rem</div>
<div class="rounded-lg">0.5rem</div>
<div class="rounded-xl">0.75rem</div>
<div class="rounded-2xl">1rem</div>
<div class="rounded-full">9999px (circle)</div>
<div class="rounded-none">0px</div>
<div class="rounded-t-lg">Top corners only</div>

<!-- Divide (between children) -->
<div class="divide-y divide-gray-200">
  <div>Item 1</div>
  <div>Item 2</div>
</div>

<!-- Ring (outline) -->
<div class="ring-2 ring-blue-500">Focus ring</div>
<div class="ring-2 ring-offset-2 ring-blue-500">With offset</div>

<!-- Outline -->
<button class="outline-2 outline-offset-2 outline-blue-500">
  Outline style
</button>
```

## Effects

```html
<!-- Box Shadow -->
<div class="shadow-sm">Small shadow</div>
<div class="shadow">Default shadow</div>
<div class="shadow-md">Medium shadow</div>
<div class="shadow-lg">Large shadow</div>
<div class="shadow-xl">Extra large shadow</div>
<div class="shadow-2xl">2XL shadow</div>
<div class="shadow-inner">Inner shadow</div>
<div class="shadow-none">No shadow</div>

<!-- Shadow Color -->
<div class="shadow-lg shadow-blue-500/50">Blue shadow at 50%</div>

<!-- Opacity -->
<div class="opacity-100">Full opacity</div>
<div class="opacity-75">75%</div>
<div class="opacity-50">50%</div>
<div class="opacity-25">25%</div>
<div class="opacity-0">Invisible</div>
```

## Filters

```html
<!-- Blur -->
<div class="blur-sm">Small blur</div>
<div class="blur-md">Medium blur</div>
<div class="blur-none">No blur</div>

<!-- Brightness & Contrast -->
<div class="brightness-50">50% brightness</div>
<div class="brightness-150">150% brightness</div>
<div class="contrast-125">125% contrast</div>

<!-- Grayscale & Invert -->
<div class="grayscale">Full grayscale</div>
<div class="invert">Invert colors</div>
<div class="sepia">Sepia tone</div>

<!-- Saturate -->
<div class="saturate-50">50% saturation</div>
<div class="saturate-200">200% saturation</div>

<!-- Backdrop Blur (glass effect) -->
<div class="backdrop-blur-sm bg-white/30">Frosted glass</div>
<div class="backdrop-blur-md bg-black/20">Dark glass</div>
```

## Transitions & Animations

```html
<!-- Transitions -->
<button class="transition duration-300 ease-in-out hover:scale-105 hover:bg-blue-600">
  Smooth hover
</button>

<div class="transition-all duration-500">All properties</div>
<div class="transition-colors duration-200">Colors only</div>
<div class="transition-opacity duration-150">Opacity only</div>
<div class="transition-transform duration-300">Transform only</div>

<!-- Timing Functions -->
<div class="ease-linear">Linear</div>
<div class="ease-in">Ease in</div>
<div class="ease-out">Ease out</div>
<div class="ease-in-out">Ease in-out</div>

<!-- Delay -->
<div class="transition delay-150">150ms delay</div>
<div class="transition delay-300">300ms delay</div>

<!-- Animations -->
<div class="animate-spin">Spinning loader</div>
<div class="animate-ping">Ping effect</div>
<div class="animate-pulse">Pulsing</div>
<div class="animate-bounce">Bouncing</div>
```

## Transforms

```html
<!-- Scale -->
<div class="scale-75">75%</div>
<div class="scale-100">100%</div>
<div class="scale-150">150%</div>
<div class="hover:scale-105">Scale on hover</div>
<div class="scale-x-50">50% horizontal only</div>

<!-- Rotate -->
<div class="rotate-45">45 degrees</div>
<div class="rotate-90">90 degrees</div>
<div class="-rotate-12">-12 degrees</div>

<!-- Translate -->
<div class="translate-x-4">Move right 1rem</div>
<div class="translate-y-2">Move down 0.5rem</div>
<div class="-translate-x-1/2">Move left 50%</div>

<!-- Skew -->
<div class="skew-x-12">Skew horizontal</div>
<div class="skew-y-6">Skew vertical</div>

<!-- Transform Origin -->
<div class="origin-center">Center (default)</div>
<div class="origin-top-left">Top left</div>
```

## Interactivity

```html
<!-- Cursor -->
<div class="cursor-pointer">Pointer</div>
<div class="cursor-not-allowed">Not allowed</div>
<div class="cursor-grab">Grab</div>
<div class="cursor-text">Text select</div>

<!-- User Select -->
<div class="select-none">Cannot select text</div>
<div class="select-all">Select all on click</div>
<div class="select-text">Normal selection</div>

<!-- Pointer Events -->
<div class="pointer-events-none">Click through</div>
<div class="pointer-events-auto">Normal interaction</div>

<!-- Resize -->
<textarea class="resize">Both directions</textarea>
<textarea class="resize-y">Vertical only</textarea>
<textarea class="resize-none">No resize</textarea>

<!-- Scroll Behavior -->
<html class="scroll-smooth">Smooth page scrolling</html>
<div class="scroll-mt-16">Scroll margin top (for sticky headers)</div>
<div class="snap-start">Scroll snap start</div>
<div class="snap-x snap-mandatory">Horizontal snap</div>

<!-- Touch Action -->
<div class="touch-pan-x">Horizontal pan only</div>

<!-- Accent Color -->
<input type="checkbox" class="accent-pink-500" />

<!-- Caret Color -->
<input class="caret-blue-500" />

<!-- Appearance -->
<select class="appearance-none">Remove native styling</select>
```

## Theme Variables (v4 — CSS-First Config)

Tailwind v4 uses CSS `@theme` directive instead of `tailwind.config.js`.

### Extending the Default Theme

```css
@import "tailwindcss";
@theme {
  --font-script: Great Vibes, cursive;
  --color-brand: #3b82f6;
  --color-brand-dark: #1d4ed8;
}
```

Creates utility classes: `font-script`, `text-brand`, `bg-brand-dark`, etc.

### Overriding Default Values

```css
@import "tailwindcss";
@theme {
  --breakpoint-sm: 30rem;  /* Override sm breakpoint */
}
```

### Overriding Entire Namespace

Use `--namespace-*: initial` to clear all defaults in a namespace:

```css
@import "tailwindcss";
@theme {
  --color-*: initial;        /* Remove ALL default colors */
  --color-white: #fff;
  --color-purple: #3f3cbb;
  --color-midnight: #121063;
}
```

### Adding Custom Spacing

```css
@theme {
  --spacing-128: 32rem;
  --spacing-144: 36rem;
}
```

### Available Namespaces

| Namespace | Generates |
|:----------|:----------|
| `--color-*` | `text-*`, `bg-*`, `border-*`, etc. |
| `--font-*` | `font-*` |
| `--text-*` | `text-*` (font-size) |
| `--spacing-*` | `p-*`, `m-*`, `w-*`, `h-*`, `gap-*` |
| `--breakpoint-*` | `sm:`, `md:`, `lg:`, etc. |
| `--radius-*` | `rounded-*` |
| `--shadow-*` | `shadow-*` |
| `--animate-*` | `animate-*` |
| `--container-*` | `@container` sizes |

## Common Layout Patterns

### Flexbox Card

```html
<div class="flex items-center gap-4 rounded-lg bg-white p-4 shadow">
  <img class="h-12 w-12 rounded-full" src="avatar.jpg" />
  <div>
    <h3 class="font-semibold text-gray-900">John Doe</h3>
    <p class="text-sm text-gray-500">Developer</p>
  </div>
</div>
```

### Responsive Grid

```html
<div class="grid grid-cols-1 gap-6 p-6 sm:grid-cols-2 lg:grid-cols-3">
  <div class="rounded-xl bg-white p-6 shadow-md">Card 1</div>
  <div class="rounded-xl bg-white p-6 shadow-md">Card 2</div>
  <div class="rounded-xl bg-white p-6 shadow-md">Card 3</div>
</div>
```

### Centered Container

```html
<div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
  <!-- Centered content -->
</div>
```

### Sticky Header

```html
<header class="sticky top-0 z-50 bg-white/80 backdrop-blur-sm border-b">
  <nav class="mx-auto flex max-w-7xl items-center justify-between p-4">
    <a href="/" class="text-xl font-bold">Logo</a>
    <div class="hidden md:flex gap-6">
      <a href="#" class="text-gray-600 hover:text-gray-900">Home</a>
      <a href="#" class="text-gray-600 hover:text-gray-900">About</a>
    </div>
  </nav>
</header>
```

### Hero Section

```html
<section class="relative isolate overflow-hidden bg-gray-900 py-24 sm:py-32">
  <div class="mx-auto max-w-7xl px-6 lg:px-8">
    <h1 class="text-4xl font-bold tracking-tight text-white sm:text-6xl">
      Build amazing things
    </h1>
    <p class="mt-6 text-lg leading-8 text-gray-300">
      Start your next project with Tailwind CSS.
    </p>
    <div class="mt-10 flex gap-x-6">
      <a href="#" class="rounded-md bg-indigo-500 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-400">
        Get started
      </a>
    </div>
  </div>
</section>
```

### Modal / Dialog

```html
<div class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
  <div class="mx-4 w-full max-w-lg rounded-2xl bg-white p-6 shadow-2xl">
    <h2 class="text-lg font-semibold">Dialog Title</h2>
    <p class="mt-2 text-sm text-gray-500">Dialog content here.</p>
    <div class="mt-6 flex justify-end gap-3">
      <button class="rounded-md px-3 py-2 text-sm font-semibold text-gray-900 hover:bg-gray-100">
        Cancel
      </button>
      <button class="rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white hover:bg-indigo-500">
        Confirm
      </button>
    </div>
  </div>
</div>
```

## Useful Plugins

```css
@plugin "@tailwindcss/forms";        /* Form reset styles */
@plugin "@tailwindcss/typography";   /* Prose/article styles */
@plugin "@tailwindcss/container-queries"; /* Container queries (built-in v4) */
```
