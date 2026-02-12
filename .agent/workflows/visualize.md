---
description: "🖼️ UI/UX Design: mockups, wireframes, component design, visual prototyping"
skills: { required: [domyh-design], contextual: [] }
---

# 🖼️ /visualize — Visualize Pro

> Component-First UI Design with Research-Backed Standards
> 📚 Multi-platform • Design Tokens (DTCG 2025.10) • A11y (WCAG 2.2) • VRT

---

## VISUALIZE FLOW

1. **DETECT** — Detect stack via HSA (`hsa_detect_stack`), load UI context (`hsa_get_context`), search existing components FIRST (70-90% token savings). Show: `[Step 1/8] Found 12 reusable components`
2. **PLAN** — Generate props/layout, not full code. Choose wireframe template, define a11y requirements. Show: `[Step 2/8] Designing Dashboard layout...`
3. **TOKENS** — Generate/load design tokens (W3C DTCG 2025.10 format). Apply platform-specific tokens (M3/HIG/Web). Show: `[Step 3/8] Loading design tokens...`
4. **PREVIEW** — Show wireframe/mockup → ⛔ **STOP — confirm before building**
5. **EXECUTE** — Build using mapped components + new ones, apply design system
6. **RESPONSIVE** — Container query verification + fluid typography check + breakpoint validation
7. **VERIFY** — A11y audit (axe-core) + contrast ratio + Lighthouse score + VRT baseline
8. **SYNC** — `hsa_check_changes` to update index, save design decisions to memory

---

## COMMANDS

| Command                        | Platform           | Output                  |
| ------------------------------ | ------------------ | ----------------------- |
| `/visualize web [page]`        | React/Vue/Svelte   | JSX + CSS               |
| `/visualize mobile [screen]`   | Flutter/RN/SwiftUI | Dart/JSX/Swift          |
| `/visualize desktop [window]`  | WPF/Qt/Electron    | XAML/QML/HTML           |
| `/visualize component [name]`  | Auto-detect        | Component code          |
| `/visualize system`            | All                | Design tokens + docs    |
| `/visualize dark-mode`         | All                | Dark tokens + toggle    |
| `/visualize responsive [page]` | Web                | Container query check   |
| `/visualize a11y [page]`       | All                | WCAG 2.2 audit report   |
| `/visualize animation [type]`  | Web/Mobile         | Micro-interaction code  |
| `/visualize tokens`            | All                | Export/import DTCG JSON |
| `/visualize migrate [from]`    | All                | Design token migration  |
| `/visualize compare`           | All                | VRT screenshot diff     |

---

## 🧩 COMPONENT MAPPING (KEY FEATURE)

### Priority: Map BEFORE Generate

1. **Index** — Scan `src/components`, `components`, `src/ui`
2. **Match** — Request → existing components (70-90% reuse)
3. **Gap** — Only generate missing components

---

## 🎨 DESIGN TOKENS (W3C DTCG 2025.10)

> Standard: [W3C Design Tokens Community Group 2025.10 Stable](https://w3.org/groups/cg/design-tokens/)

### Token Format

```json
{
  "$name": "color.primary",
  "$type": "color",
  "$value": "oklch(60% 0.15 250)",
  "$description": "Primary brand color",
  "$deprecated": false,
  "$extensions": {
    "com.domyh.platforms": ["web", "ios", "android", "flutter"]
  }
}
```

### Theming via `$extends` (DTCG 2025.10)

```json
// dark-theme.tokens.json
{
  "$extends": "./base.tokens.json",
  "color": {
    "primary": { "$value": "oklch(75% 0.12 250)" },
    "surface": { "$value": "oklch(15% 0.01 250)" }
  }
}
```

### Color System (Modern CSS)

| Token   | Web CSS (OKLCH)       | Tailwind      | Flutter (`fromSeed`)   | SwiftUI    |
| ------- | --------------------- | ------------- | ---------------------- | ---------- |
| primary | `oklch(60% 0.15 250)` | bg-blue-600   | `ColorScheme.fromSeed` | .blue      |
| surface | `oklch(98% 0.01 250)` | bg-gray-100   | `Colors.grey[100]`     | .secondary |
| error   | `oklch(55% 0.22 27)`  | bg-red-500    | `Colors.red`           | .red       |
| text    | `oklch(15% 0.01 250)` | text-gray-900 | —                      | .primary   |

### Spacing

| Token | Web  | Tailwind | Flutter | SwiftUI |
| ----- | ---- | -------- | ------- | ------- |
| xs    | 4px  | p-1      | 4       | 4       |
| sm    | 8px  | p-2      | 8       | 8       |
| md    | 16px | p-4      | 16      | 16      |
| lg    | 24px | p-6      | 24      | 24      |
| xl    | 32px | p-8      | 32      | 32      |

### Typography (Fluid via `clamp()`)

| Token    | Web CSS                         | Flutter |
| -------- | ------------------------------- | ------- |
| heading1 | `clamp(2rem, 4vw, 3.5rem)`      | 32sp    |
| heading2 | `clamp(1.5rem, 3vw, 2.5rem)`    | 24sp    |
| body     | `clamp(1rem, 1.5vw, 1.125rem)`  | 16sp    |
| caption  | `clamp(0.75rem, 1vw, 0.875rem)` | 12sp    |

---

## 🌗 DARK MODE STRATEGY

### Implementation

```css
/* CSS Custom Properties + prefers-color-scheme */
:root {
  --bg: oklch(98% 0.01 250); /* Light: off-white (NOT #fff) */
  --text: oklch(15% 0.01 250); /* Light: near-black (NOT #000) */
  --surface: oklch(95% 0.01 250);
}

@media (prefers-color-scheme: dark) {
  :root {
    --bg: oklch(15% 0.01 250); /* Dark: deep gray (NOT #000) */
    --text: oklch(90% 0.01 250); /* Dark: off-white */
    --surface: oklch(20% 0.01 250);
  }
}
```

### Rules

- ❌ Never pure black `#000` / pure white `#fff` — causes eye strain
- ✅ Use deep grays `oklch(15%)` and off-whites `oklch(90%)`
- ✅ Re-evaluate brand colors for dark backgrounds
- ✅ Provide user toggle + persist preference (localStorage)
- ✅ Prevent "white flash" — apply theme before body loads

---

## 📱 PLATFORM GUIDELINES

### Android — Material Design 3 Expressive

| Aspect       | Standard                                            |
| ------------ | --------------------------------------------------- |
| Color System | Dynamic Color via `ColorScheme.fromSeed(seedColor)` |
| Components   | NavigationBar, SegmentedButton, FilledButton        |
| Typography   | Material Type Scale (M3)                            |
| Navigation   | NavigationBar (bottom), NavigationDrawer (side)     |
| Flutter      | `useMaterial3: true` + `dynamic_color` package      |
| Shapes       | Rounded corners (M3 shape system)                   |

### iOS — Apple HIG + Liquid Glass (2025)

| Aspect          | Standard                                           |
| --------------- | -------------------------------------------------- |
| Principles      | Clarity, Consistency, Deference, Depth             |
| Design Language | Liquid Glass (translucency, depth, fluid response) |
| SwiftUI         | Preview-driven development                         |
| Navigation      | TabView, NavigationSplitView                       |
| Typography      | SF Pro (system), Dynamic Type sizes                |
| Touch Targets   | Minimum 44pt                                       |

---

## 📐 WIREFRAME TEMPLATES

| Pattern       | Layout                     | Use Case       |
| ------------- | -------------------------- | -------------- |
| Dashboard     | Header + Sidebar + Grid    | Admin panels   |
| Detail Page   | Header + Content + Actions | Entity view    |
| List + Filter | FilterBar + Table/Cards    | Data browsing  |
| Auth Flow     | Centered card              | Login/Register |
| Settings      | Sidebar nav + Form         | App settings   |
| Landing       | Hero + Features + CTA      | Marketing      |

---

## 📱 RESPONSIVE STRATEGY

### Container Queries (Component-Level)

```css
.card-container {
  container-type: inline-size;
  container-name: card;
}
@container card (min-width: 400px) {
  .card {
    flex-direction: row;
  }
}
```

### Breakpoints (Content-First)

| Breakpoint | Width   | Target           |
| ---------- | ------- | ---------------- |
| mobile     | < 640px | Phones           |
| tablet     | 768px   | Tablets          |
| desktop    | 1024px  | Laptops          |
| wide       | 1280px  | Full HD          |
| ultra      | 1536px  | Ultra-wide / 2K+ |

### Touch Targets

| Platform | Minimum Size | Standard        |
| -------- | ------------ | --------------- |
| Web      | 44×44px      | WCAG 2.2        |
| Android  | 48×48dp      | Material Design |
| iOS      | 44×44pt      | Apple HIG       |

---

## ♿ ACCESSIBILITY (WCAG 2.2)

### Automated Testing Tools

| Tool       | Command                                                | Use Case        |
| ---------- | ------------------------------------------------------ | --------------- |
| axe-core   | `npx @axe-core/cli <url>`                              | Single page     |
| Pa11y CI   | `npx pa11y-ci --config .pa11yci.json`                  | Batch pages     |
| Lighthouse | `npx lighthouse <url> --only-categories=accessibility` | Full audit      |
| Storybook  | Built-in axe-core addon (Storybook 9)                  | Component-level |

### Checklist (WCAG 2.2 — 9 new criteria highlighted)

**Core (WCAG 2.1 + 2.2 AA)**

- Color contrast ≥ 4.5:1 (AA) / ≥ 7:1 (AAA)
- Focus indicators visible (2px+ outline)
- Keyboard navigable (Tab order, Enter/Space activation)
- Touch targets ≥ platform minimum
- Screen reader labels (aria-label, role, alt text)
- Reduced motion support (`prefers-reduced-motion`)
- Semantic HTML (heading hierarchy, landmarks)

**NEW in WCAG 2.2 (Oct 2023)**

- 🆕 **Focus Not Obscured (Min)** (2.4.11 AA) — keyboard focus not hidden by sticky/fixed elements
- 🆕 **Focus Not Obscured (Enhanced)** (2.4.12 AAA) — focused element fully visible
- 🆕 **Focus Appearance** (2.4.13 AAA) — focus indicator ≥ 2px, sufficient contrast
- 🆕 **Dragging Movements** (2.5.7 AA) — alternative pointer action for any drag operation
- 🆕 **Target Size (Min)** (2.5.8 AA) — touch targets ≥ 24×24px (44×44px recommended)
- 🆕 **Consistent Help** (3.2.6 A) — help mechanism in same relative location across pages
- 🆕 **Redundant Entry** (3.3.7 A) — don't require re-entering previously provided info
- 🆕 **Accessible Auth (Min)** (3.3.8 AA) — no cognitive test for login (allow paste, passkeys)
- 🆕 **Accessible Auth (Enhanced)** (3.3.9 AAA) — stricter auth accessibility

---

## 🔍 VISUAL REGRESSION TESTING (VRT)

| Tool       | Type        | Engine     | Best For                    |
| ---------- | ----------- | ---------- | --------------------------- |
| Playwright | Built-in    | pixelmatch | Free, integrated with E2E   |
| Chromatic  | Cloud SaaS  | Storybook  | CDD teams (5k free/mo)      |
| Percy      | Cloud SaaS  | AI-powered | Cross-browser (5k free/mo)  |
| BackstopJS | Self-hosted | Puppeteer  | OSS, configurable scenarios |

### Playwright VRT (recommended — free)

```typescript
await expect(page).toHaveScreenshot("dashboard.png");
// On failure: generates actual, expected, diff images
```

---

## 🖼️ AI IMAGE GENERATION

| Command                      | Tool             | Formats                      |
| ---------------------------- | ---------------- | ---------------------------- |
| `/visualize generate [desc]` | `generate_image` | PNG, JPG, WebP               |
| `/visualize mockup [comp]`   | `generate_image` | 1920×1080, 1280×720, 375×812 |

---

## 🔌 SKILL INTEGRATION (domyh-design)

> Auto-loaded via `skills: { required: [domyh-design] }` in frontmatter

### Data Lookup Per Command

Read YAML data files directly from skill data directory:

```yaml
SKILL_DATA: ".agent/skills/cross-cutting/domyh-design/data"

# /visualize system — Generate complete design system
# Read: styles.yaml, colors.yaml, typography.yaml, design-tokens.yaml

# /visualize web — Stack-specific guidelines
# Read: stacks/html-tailwind.yaml, stacks/react.yaml, stacks/vue.yaml

# /visualize mobile — Mobile stack guidelines
# Read: stacks/flutter.yaml, stacks/swiftui.yaml, stacks/react-native.yaml

# /visualize desktop — Desktop stack guidelines
# Read: stacks/electron.yaml, stacks/qt.yaml, stacks/wpf.yaml

# /visualize component — Component decision + mapping
# Read: component-mapping.yaml, ux-guidelines.yaml

# /visualize a11y — Accessibility guidelines
# Read: ux-guidelines.yaml (accessibility section)

# /visualize animation — Animation patterns
# Read: ux-guidelines.yaml (animation/motion section)
```

### Direct Data Lookup (no script needed)

| Command                 | Data File                       | Format                    |
| ----------------------- | ------------------------------- | ------------------------- |
| `/visualize tokens`     | `data/design-tokens.yaml`       | 46 tokens × 8 platforms   |
| `/visualize responsive` | `data/platform-guidelines.yaml` | 12 platform breakpoints   |
| `/visualize component`  | `data/component-mapping.yaml`   | 30 components with scores |
| `/visualize dark-mode`  | `data/ux-guidelines.yaml`       | Dark mode contrast rules  |
