---
name: domyh-design
description: "UI/UX design intelligence. 50+ styles, 130+ palettes, 57 fonts, 9 stacks. React, Next.js, Vue, Svelte, SwiftUI, RN, Flutter, Tailwind, shadcn/ui."
---

# UI/UX Pro Max - Design Intelligence

> Design guide for web, desktop, and mobile. Searchable database with priority-based recommendations.
> For detailed reference, desktop stacks, /visualize integration, see `ADVANCED.md`.

## When to Apply

- Designing new UI components or pages
- Choosing color palettes and typography
- Reviewing code for UX issues
- Building landing pages or dashboards
- Implementing accessibility requirements

## Rule Categories by Priority

| Priority | Category            | Impact   | Domain                |
| -------- | ------------------- | -------- | --------------------- |
| 1        | Accessibility       | CRITICAL | `ux`                  |
| 2        | Touch & Interaction | CRITICAL | `ux`                  |
| 3        | Performance         | HIGH     | `ux`                  |
| 4        | Layout & Responsive | HIGH     | `ux`                  |
| 5        | Typography & Color  | MEDIUM   | `typography`, `color` |
| 6        | Animation           | MEDIUM   | `ux`                  |
| 7        | Style Selection     | MEDIUM   | `style`, `product`    |
| 8        | Charts & Data       | LOW      | `chart`               |

## Quick Reference

### 1. Accessibility (CRITICAL)

- `color-contrast` - Minimum 4.5:1 ratio for normal text
- `focus-states` - Visible focus rings on interactive elements
- `alt-text` - Descriptive alt text for meaningful images
- `aria-labels` - aria-label for icon-only buttons
- `keyboard-nav` - Tab order matches visual order
- `form-labels` - Use label with for attribute
- 🆕 `focus-not-obscured` - Focus not hidden by sticky/fixed elements (WCAG 2.2)
- 🆕 `dragging-alternative` - Single pointer alternative for drag ops (WCAG 2.2)
- 🆕 `accessible-auth` - No cognitive test for login (WCAG 2.2)

### 2. Touch & Interaction (CRITICAL)

- `touch-target-size` - Minimum 44x44px touch targets
- `hover-vs-tap` - Use click/tap for primary interactions
- `loading-buttons` - Disable button during async operations
- `error-feedback` - Clear error messages near problem
- `cursor-pointer` - Add cursor-pointer to clickable elements

### 3. Performance (HIGH)

- `image-optimization` - Use WebP, srcset, lazy loading
- `reduced-motion` - Check prefers-reduced-motion
- `content-jumping` - Reserve space for async content

### 4. Layout & Responsive (HIGH)

- `viewport-meta` - width=device-width initial-scale=1
- `readable-font-size` - Minimum 16px body text on mobile
- `horizontal-scroll` - Ensure content fits viewport width
- `z-index-management` - Define z-index scale (10, 20, 30, 50)

### 5-8. Typography, Animation, Style, Charts

- `line-height` - Use 1.5-1.75 for body text
- `duration-timing` - Use 150-300ms for micro-interactions
- `no-emoji-icons` - Use SVG icons, not emojis
- `chart-type` - Match chart type to data type

## How to Use

### Step 1: Analyze Requirements

Extract: **product type**, **style keywords**, **industry**, **stack** (default: html-tailwind)

### Step 2: Generate Design System (REQUIRED + VARIED)

Read data files directly for recommendations:

- **Product type** → `data/products.yaml` (96 product types with style/font/palette mappings)
  - ⚠️ Read `style_alternatives` — pick based on user mood keywords, NOT always `primary_style`
  - ⚠️ Read `color_palette_variants` — select specific hex palette, NEVER use generic descriptions
  - ⚠️ Read `anti_patterns` in metadata — follow these rules to avoid cookie-cutter designs
- **Color palette** → `data/colors.yaml` (130+ palettes by industry)
- **Typography** → `data/typography.yaml` (57 font pairings)
- **Style pattern** → `data/styles.yaml` (58 UI styles)

**Variation Rules** (MANDATORY):
1. If user specified mood/keywords → match to `style_alternatives` mood tags
2. If no mood specified → randomly select from alternatives (NOT always primary)
3. ALWAYS use specific hex from `color_palette_variants` — never resolve "trust blue" generically
4. For same product type across projects, MUST use different palette variant each time

### Step 3: Supplement with Domain Data

| Domain     | Data File                 | Content                      |
| ---------- | ------------------------- | ---------------------------- |
| Product    | `data/products.yaml`      | Product type recommendations |
| Style      | `data/styles.yaml`        | UI styles, effects           |
| Typography | `data/typography.yaml`    | Font pairings                |
| Color      | `data/colors.yaml`        | Palettes by industry         |
| Landing    | `data/landing.yaml`       | Page structure, CTA          |
| Chart      | `data/charts.yaml`        | Chart types, libraries       |
| UX         | `data/ux-guidelines.yaml` | Best practices               |
| Icons      | `data/icons.yaml`         | Icon sets, guidelines        |

### Step 4: Stack Guidelines

Read stack-specific file from `data/stacks/` directory:

Stacks: `html-tailwind`, `react`, `nextjs`, `vue`, `svelte`, `swiftui`, `react-native`, `flutter`, `shadcn`

## Pre-Delivery Checklist

### Visual Quality

- [ ] No emojis as icons (use SVG: Heroicons/Lucide)
- [ ] Hover states don't cause layout shift
- [ ] Transitions smooth (150-300ms)

### Interaction

- [ ] All clickable elements have `cursor-pointer`
- [ ] Focus states visible for keyboard navigation

### Light/Dark Mode

- [ ] Light mode text contrast ≥ 4.5:1
- [ ] Glass elements visible in both modes
- [ ] Test both modes before delivery

### Layout

- [ ] Responsive at 375px, 768px, 1024px, 1440px
- [ ] No content hidden behind fixed navbars
- [ ] No horizontal scroll on mobile

### Accessibility (WCAG 2.2)

- [ ] All images have alt text
- [ ] Form inputs have labels
- [ ] Color not the only indicator
- [ ] `prefers-reduced-motion` respected
- [ ] Focus not obscured by sticky elements (2.4.11)
- [ ] Drag alternatives provided (2.5.7)
- [ ] Target size ≥ 44×44px (2.5.8)
- [ ] Accessible authentication (3.3.8)

### AI Image Generation (PRISM Framework)

> 📁 Data: `data/image-gen-prompts.yaml` • `data/image-gen-workflows.yaml` • `data/design-system-prompts.yaml`

**PRISM Prompt Structure**: Persona → Reference → Intent → Structure → Modifiers

**Quick Flow**:

1. Detect platform → select preset (desktop_dashboard, mobile_app, tablet_app, landing_page_hero, component_preview)
2. Pick component template (15 types: dashboard, landing, login, settings, mobile, nav, card, modal, table, form, pricing, profile, e-commerce, chat, onboarding)
3. Select design system fragment (Material 3, Apple HIG, Fluent 2, shadcn/ui, Ant Design, Chakra UI)
4. Assemble PRISM prompt from template + style variant
5. Append negative prompts (always_apply + component-specific)
6. Generate with `generate_image` tool

**Realism Boosters**: `screenshot` ⭐⭐⭐ | `UI design mockup` ⭐⭐⭐ | `high-fidelity` ⭐⭐ | `pixel-perfect` ⭐⭐

**Multi-Screen**: Same seed + color pinning (hex) + font pinning + reference image chaining

- [ ] Prompt follows PRISM framework
- [ ] Negative prompts appended (no device frames, no lorem ipsum)
- [ ] enhancePrompt=false for complex prompts (>30 words)
- [ ] Aspect ratio matches target platform
- [ ] Design system fragment included if applicable

---
