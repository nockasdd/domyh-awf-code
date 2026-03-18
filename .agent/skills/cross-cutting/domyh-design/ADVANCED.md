---
name: domyh-design
tier: 3
description: "Advanced UI/UX reference: /visualize integration, desktop stacks, design thinking, component mapping, platform guidelines"
---

# UI/UX Pro Max — Advanced Reference (T3)

> Detailed reference for complex UI/UX scenarios.
> For quick reference and workflow, see `SKILL.md`.

---

## `/visualize` Command Integration

> Map each `/visualize` sub-command to the correct skill data source

| `/visualize` Command          | Data Source                                               | Lookup Method            |
| ----------------------------- | --------------------------------------------------------- | ------------------------ |
| `/visualize system`           | Multi-domain (product+style+color+typography+landing)     | Read multiple YAML files |
| `/visualize web [page]`       | `data/stacks/html-tailwind.yaml`                          | Direct read              |
| `/visualize mobile` (Flutter) | `data/stacks/flutter.yaml`                                | Direct read              |
| `/visualize mobile` (SwiftUI) | `data/stacks/swiftui.yaml`                                | Direct read              |
| `/visualize mobile` (RN)      | `data/stacks/react-native.yaml`                           | Direct read              |
| `/visualize desktop`          | `data/stacks/desktop.yaml`                                | Direct read              |
| `/visualize component [name]` | `data/component-decision.yaml` + `component-mapping.yaml` | Direct read              |
| `/visualize a11y`             | `data/ux-guidelines.yaml`                                 | Direct read              |
| `/visualize animation`        | `data/ux-guidelines.yaml`                                 | Direct read              |
| `/visualize tokens`           | `data/design-tokens.yaml` (46 cross-platform tokens)      | Direct read              |
| `/visualize dark-mode`        | `data/ux-guidelines.yaml`                                 | Direct read              |
| `/visualize responsive`       | `data/ux-guidelines.yaml`                                 | Direct read              |

---

---

## Search Reference — Available Domains

| Domain       | Use For                              | Example Keywords                                         |
| ------------ | ------------------------------------ | -------------------------------------------------------- |
| `product`    | Product type recommendations         | SaaS, e-commerce, portfolio, healthcare, beauty, service |
| `style`      | UI styles, colors, effects           | glassmorphism, minimalism, dark mode, brutalism          |
| `typography` | Font pairings, Google Fonts          | elegant, playful, professional, modern                   |
| `color`      | Color palettes by product type       | saas, ecommerce, healthcare, beauty, fintech, service    |
| `landing`    | Page structure, CTA strategies       | hero, hero-centric, testimonial, pricing, social-proof   |
| `chart`      | Chart types, library recommendations | trend, comparison, timeline, funnel, pie                 |
| `ux`         | Best practices, anti-patterns        | animation, accessibility, z-index, loading               |
| `react`      | React/Next.js performance            | waterfall, bundle, suspense, memo, rerender, cache       |
| `web`        | Web interface guidelines             | aria, focus, keyboard, semantic, virtualize              |
| `prompt`     | AI prompts, CSS keywords             | (style name)                                             |

---

## Desktop Stacks

| Stack        | Category       | Language | Focus                                 |
| ------------ | -------------- | -------- | ------------------------------------- |
| `wpf`        | Windows        | C#/XAML  | MVVM, Fluent theme, easing animations |
| `winui3`     | Windows        | C#/XAML  | DirectX 12, Mica, Acrylic, Windows 11 |
| `webview2`   | Hybrid         | C++/C#   | Web+native, security patterns         |
| `qt-widgets` | Cross-Platform | C++      | Native widgets, C++17/20              |
| `qt-qml`     | Cross-Platform | C++/QML  | Material/Fluent styling               |
| `imgui`      | Game/Debug     | C++      | Immediate-mode, debug overlays        |
| `electron`   | Web-Desktop    | JS/TS    | Chromium, large ecosystem             |
| `tauri`      | Web-Desktop    | Rust+JS  | <10MB binary, native WebView          |
| `avalonia`   | .NET           | C#/XAML  | Skia rendering, cross-platform        |
| `pyqt`       | Python         | Python   | PyQt6/PySide6, professional           |

### Architecture Patterns

| Pattern | Best For                 | Data Binding |
| ------- | ------------------------ | ------------ |
| `mvvm`  | Complex apps (WPF/WinUI) | Auto two-way |
| `mvp`   | Testable desktop (Qt)    | Manual       |
| `mvc`   | Simple apps              | Manual       |

### Animation Domains

| Domain                 | Use For                           |
| ---------------------- | --------------------------------- |
| `desktop-animation`    | DirectX, WPF easing, Qt animation |
| `desktop-colors`       | Platform color palettes           |
| `desktop-architecture` | MVC/MVP/MVVM patterns             |

---

## Implementation Strategy

| Phase      | Component Priority                      | Approach           | Directory       |
| ---------- | --------------------------------------- | ------------------ | --------------- |
| MVP        | 20% most-used (Button/Input/Card/Modal) | Library + Headless | Simple          |
| Growth     | Extend + Complex components             | Headless + Custom  | Feature-Sliced  |
| Scale      | Design system + Variants                | Custom + Tokens    | Monorepo        |
| Enterprise | Multi-brand + Theming                   | Token-based        | Micro-frontends |

## Directory Structure Patterns

| Pattern         | Best For               | Structure                                  |
| --------------- | ---------------------- | ------------------------------------------ |
| `fsd`           | Large apps (50+ pages) | app/pages/widgets/features/entities/shared |
| `fsd-lite`      | Medium apps            | app/pages/features/shared                  |
| `atomic`        | Design systems         | atoms/molecules/organisms/templates/pages  |
| `simple`        | Small apps/MVPs        | components/pages/utils/hooks               |
| `colocation`    | Next.js App Router     | (feature)/page+components+hooks            |
| `domain-driven` | Business logic heavy   | domains/user/product/order + shared        |

## Component Decision Matrix

| Need       | → Use               | Examples                       |
| ---------- | ------------------- | ------------------------------ |
| Speed      | Library             | MUI, Ant Design, Chakra        |
| Brand      | Headless + Tailwind | Radix + shadcn                 |
| Control    | Custom              | Hand-built components          |
| A11y       | Headless            | Radix, React Aria, Headless UI |
| Data-heavy | Specialized         | TanStack Table, TipTap         |

## Platform Guidelines

| Platform   | Design System   | Touch Target | Spacing  |
| ---------- | --------------- | ------------ | -------- |
| Web        | Custom/shadcn   | 44x44px      | 4px base |
| Windows    | Fluent/WinUI3   | 32x32px      | 4px base |
| macOS      | Human Interface | 22x22px      | 8px base |
| iOS        | SwiftUI/UIKit   | 44x44pt      | 4px base |
| Android    | Material 3      | 48x48dp      | 4dp base |
| Desktop Qt | Qt Quick        | 32x32px      | 4px base |

## Component Mapping Strategy

```yaml
workflow: 1. Index existing components in project
  2. Match request to library (70-90% token savings)
  3. Generate props only, not full code
  4. Compose from primitives for gaps

decision_matrix:
  headless: 85-90% saved (Radix, React Aria)
  library: 70-85% saved (shadcn, MUI)
  custom: 50-60% saved (tokens + patterns)
```

---

## Example Workflow

**User request:** "Làm landing page cho dịch vụ chăm sóc da chuyên nghiệp"

### Step 1: Analyze Requirements

- Product type: Beauty/Spa service
- Style keywords: elegant, professional, soft
- Industry: Beauty/Wellness
- Stack: html-tailwind (default)

### Step 2: Generate Design System (REQUIRED)

Read data files directly:

- `data/products.yaml` → match "beauty spa wellness" → get style/font/palette recommendations
- `data/colors.yaml` → get industry-specific palette
- `data/typography.yaml` → get font pairing for "elegant" keyword

### Step 3: Supplement

Read additional domain files:

- `data/ux-guidelines.yaml` → animation + accessibility rules
- `data/typography.yaml` → search for "elegant luxury serif" pairings

### Step 4: Stack Guidelines

Read `data/stacks/html-tailwind.yaml` for layout, responsive, and form patterns.

---

## Common Rules for Professional UI

### Icons & Visual Elements

| Rule                       | Do                                              | Don't                                  |
| -------------------------- | ----------------------------------------------- | -------------------------------------- |
| **No emoji icons**         | Use SVG icons (Heroicons, Lucide, Simple Icons) | Use emojis like 🎨 🚀 ⚙️ as UI icons   |
| **Stable hover states**    | Use color/opacity transitions on hover          | Use scale transforms that shift layout |
| **Correct brand logos**    | Research official SVG from Simple Icons         | Guess or use incorrect logo paths      |
| **Consistent icon sizing** | Use fixed viewBox (24x24) with w-6 h-6          | Mix different icon sizes randomly      |

### Light/Dark Mode Contrast

| Rule                      | Do                                  | Don't                                   |
| ------------------------- | ----------------------------------- | --------------------------------------- |
| **Glass card light mode** | Use `bg-white/80` or higher opacity | Use `bg-white/10` (too transparent)     |
| **Text contrast light**   | Use `#0F172A` (slate-900) for text  | Use `#94A3B8` (slate-400) for body text |
| **Muted text light**      | Use `#475569` (slate-600) minimum   | Use gray-400 or lighter                 |
| **Border visibility**     | Use `border-gray-200` in light mode | Use `border-white/10` (invisible)       |

---

## 🎨 Design Thinking — Anthropic Guidelines

> **Philosophy**: Create DISTINCTIVE interfaces, not generic AI aesthetics

### Before Coding — BOLD Aesthetic Direction (REQUIRED)

| Question            | Why It Matters                                                            |
| ------------------- | ------------------------------------------------------------------------- |
| **Purpose**         | What problem does this interface solve?                                   |
| **Tone**            | Pick an EXTREME (brutally minimal, maximalist chaos, retro-futuristic...) |
| **Constraints**     | What CAN'T you do? (branding, technical, accessibility)                   |
| **Differentiation** | What makes this UNFORGETTABLE?                                            |

### Frontend Aesthetics Rules

```yaml
typography:
  avoid: [Arial, Helvetica, system-default, Inter (overused)]
  choose: "Distinctive, characterful fonts that elevate design"

color:
  use_css_variables: true
  rule: "Dominant colors with SHARP accents outperform timid palettes"

motion:
  page_load: "Staggered reveals, choreographed entrance"
  micro: "Purposeful hover states, smooth transitions"

spatial_composition:
  rule: "Generous whitespace, asymmetry, overlapping planes"
  avoid: "Cramped layouts, center-everything defaults"

backgrounds:
  options: ["gradient meshes", "noise textures", "depth patterns"]
  avoid: "Plain white backgrounds"
```

### 🚫 Anti-Patterns

| Anti-Pattern             | Why It Fails           |
| ------------------------ | ---------------------- |
| System fonts everywhere  | Looks like a prototype |
| Generic purple gradients | "AI aesthetic" cliché  |
| Cookie-cutter layouts    | Forgettable            |
| No motion or personality | Dead interface         |
| White background only    | No atmosphere          |

---

### 🎯 AI Tells — Concrete Ban List

Patterns that reveal AI-generated code. MUST avoid:

**Visual & CSS:**
- ❌ `#000000` pure black → Use off-black (`#0a0a0a`, Zinc-950)
- ❌ Neon/outer glows → Use inner borders or tinted shadows
- ❌ Oversaturated accents (saturation >80%) → Desaturate to blend with neutrals
- ❌ Generic 3-card equal-column feature row → Use zig-zag, asymmetric grid, or masonry
- ❌ `box-shadow` with pure black → Tint shadows to match background hue
- ❌ `h-screen` for full-height → Use `min-h-[100dvh]` (iOS Safari viewport bug)
- ❌ Flexbox percentage math (`w-[calc(33%-1rem)]`) → Use CSS Grid

**Typography:**
- ❌ Inter for "premium" or "creative" projects → Use Geist, Outfit, Satoshi, Cabinet Grotesk
- ❌ Only Regular/Bold weights → Introduce Medium (500) / SemiBold (600)
- ❌ Missing letter-spacing on large headings → Use negative tracking (`tracking-tighter`)
- ❌ Orphaned words on last line → Use `text-wrap: balance` or `text-wrap: pretty`
- ❌ Serif fonts on dashboards/software UI → Sans-serif only for data interfaces

**Content (the "Jane Doe" effect):**
- ❌ "John Doe", "Jane Smith", "Acme Corp" → Diverse, realistic names
- ❌ Round numbers: `99.99%`, `50%`, `$100.00` → Organic data: `47.2%`, `$99.00`
- ❌ AI copywriting clichés: "Elevate", "Seamless", "Unleash", "Next-Gen" → Plain verbs
- ❌ Broken Unsplash links → Use `picsum.photos/seed/{name}/800/600`
- ❌ Lorem ipsum → Write real draft copy
- ❌ Exclamation marks in success messages → Be confident, not loud

**Component:**
- ❌ Default shadcn/ui without customization → Must customize radii, colors, shadows
- ❌ Sun/moon toggle for dark mode → Use dropdown or system preference detection
- ❌ Identical avatars for different users → Unique assets per person
- ❌ Accordion FAQ sections → Side-by-side list or progressive disclosure
- ❌ Standard centered hero when `DESIGN_VARIANCE > 4` → Split-screen or asymmetric

**Code Quality:**
- ❌ `<div>` soup → Semantic HTML: `<nav>`, `<main>`, `<article>`, `<section>`
- ❌ Commented-out dead code → Remove all debug artifacts
- ❌ Import hallucinations → Verify every import exists in `package.json`
- ❌ Missing `<title>`, `description`, `og:image` meta tags

---

## Redesign Audit Workflow

When upgrading an existing project, follow this priority sequence for maximum visual impact with minimum risk:

### Step 1: Scan
Read the codebase. Identify framework, styling method (Tailwind, vanilla CSS, styled-components), and current design patterns.

### Step 2: Diagnose
Run through the AI Tells Ban List above. List every generic pattern, weak point, and missing state.

### Step 3: Fix (Priority Order)

| Priority | Action | Impact | Risk |
|----------|--------|--------|------|
| 1 | **Font swap** | ⭐⭐⭐ Instant improvement | Low |
| 2 | **Color palette cleanup** | ⭐⭐⭐ Remove clashing colors | Low |
| 3 | **Hover + active states** | ⭐⭐ Interface feels alive | Low |
| 4 | **Layout + spacing** | ⭐⭐ Grid, max-width, padding | Medium |
| 5 | **Replace generic components** | ⭐⭐ Modern alternatives | Medium |
| 6 | **Add loading/empty/error states** | ⭐ Feels finished | Medium |
| 7 | **Polish typography scale** | ⭐ Premium final touch | Low |

### Rules
- Work with existing tech stack. Do not migrate frameworks
- Do not break existing functionality. Test after every change
- Before importing any new library, check `package.json` first
- Keep changes reviewable and focused. Small, targeted improvements over big rewrites

---
