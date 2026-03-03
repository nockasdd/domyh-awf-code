---
description: "🖼️ UI/UX Design: mockups, wireframes, component design, visual prototyping"
skills: { required: [domyh-design], contextual: [auto] }
success_criteria: "Design assets generated, WCAG compliance verified, tokens exported"
---

# 🖼️ /visualize — Visualize Pro

> Component-First UI Design with Research-Backed Standards
> 📚 Multi-platform • Design Tokens (DTCG 2025.10) • A11y (WCAG 2.2) • VRT

---

## VISUALIZE FLOW

1. **DETECT** — Detect stack via HSA (`hsa_detect`), load UI context (`hsa_search`), analyze existing design DNA (`hsa_design_analyze`), search existing components FIRST (70-90% token savings). Show: `[Step 1/8] Found 12 reusable components, Design Health: 72/100 Grade C`
2. **PLAN** — Generate props/layout, not full code. Choose wireframe template, define a11y requirements. Use DNA insights for consistency. Show: `[Step 2/8] Designing Dashboard layout...`
3. **TOKENS** — Generate/load design tokens via `hsa_design_tokens(format: "dtcg")` or from W3C DTCG 2025.10 data. Apply platform-specific tokens (M3/HIG/Web). Show: `[Step 3/8] Loading design tokens...`
   **VARIATION CHECK**: Read `products.yaml` `style_alternatives` + `color_palette_variants`. Select palette variant matching mood (NOT primary default). Avoid reusing same style+colors.
4. **PREVIEW** — LiveCanvas iteration loop (zero-config visual feedback):
   - `hsa_canvas({action:"open"})` → start dev server, auto-detect framework/port/entry
   - `hsa_canvas({action:"capture"})` → screenshot + CDP diagnostics (health score, AX tree, CLS, click reachability)
   - Show capture results to user with Grade (A-F) and score (/100)
   - **Iterate** with `hsa_canvas({action:"update",  css_edits: [{selector, property, value}] })` → live CSS tweaks (no reload)
   - `hsa_canvas({action:"capture"})` → re-capture after changes
   - `hsa_canvas({action:"diff",  before, after })` → 3-tier visual regression diff (pHash → LooksSame → pixelmatch)
   - Repeat iterate→capture→diff until approved
   - → ⛔ **STOP — "Preview ready. Approve to build with {framework}?"**
   - If user requests changes → iterate via `css_edits` (instant) or file writes (HMR reload)
   - `hsa_canvas({action:"close"})` → cleanup when done
   - **Fallback**: If Canvas unavailable, use `browser_subagent` to open preview HTML directly
5. **EXECUTE** — Convert approved preview → framework components, apply design system
6. **RESPONSIVE** — Container query verification + fluid typography check + breakpoint validation
7. **VERIFY** — Run `hsa_design_health(strict: true)` for WCAG + a11y audit + Lighthouse score + VRT:
   - `hsa_canvas({action:"capture",  baseline: true })` → save as VRT baseline
   - `hsa_canvas({action:"inspect", selector)` → verify CSS cascade, box model, AX role on critical elements
   - `hsa_canvas({action:"diff",  before: "baseline", after: "latest" })` → visual regression check
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

## 🧬 HSA DESIGN INTELLIGENCE TOOLS

> 3 design analysis tools + 6 canvas tools for AI-powered design workflow

| Tool | When | Input | Output |
|------|------|-------|--------|
| `hsa_design_analyze` | DETECT step | `{scope?, paths?}` | Design DNA: colors, spacing, typography, borders, animations, dark mode, framework |
| `hsa_design_health` | VERIFY step | `{strict?}` | Score 0-100, Grade A-F, 5 categories, WCAG contrast violations, improvements |
| `hsa_design_tokens` | TOKENS step | `{format: "dtcg"\|"css"}` | W3C DTCG 2025.10 JSON/CSS + migration plan |
| `hsa_canvas({action:"open"})` | PREVIEW step | `{port?, command?, viewport?}` | Start LiveCanvas session — auto-detect framework, entry file, project name |
| `hsa_canvas({action:"capture"})` | PREVIEW/VERIFY | `{analyze?, health?, baseline?}` | Screenshot + CDP diagnostics (health score, AX tree, CLS, click issues) |
| `hsa_canvas({action:"update"})` | PREVIEW step | `{files?, css_edits?}` | Write files + HMR reload, OR live CSS edits via CDP (instant, no reload) |
| `hsa_canvas({action:"diff"})` | VERIFY step | `{before, after}` | 3-tier visual regression: pHash → LooksSame → pixelmatch |
| `hsa_canvas({action:"inspect"})` | VERIFY step | `{selector}` | CSS cascade, box model, AX node, framework detection (React/Vue/Angular/Svelte) |
| `hsa_canvas({action:"extract"})` | TOKENS step | `{format?, categories?}` | Extract design tokens from live DOM (W3C DTCG, CSS vars, or Tailwind format) |

### Usage Flow

```
# Step 1: Analyze existing design patterns
hsa_design_analyze({scope: "full"})
→ DNA report: 15 colors, 4px grid, 2 fonts, 42% token adoption

# Step 3: Generate tokens from what exists
hsa_design_tokens({format: "css"})
→ CSS variables + migration plan for 23 hardcoded values

# Step 4: Preview with LiveCanvas
hsa_canvas({action:"open"}) → Session started, http://localhost:3000
hsa_canvas({action:"capture"}) → Score: 85/100 Grade B, CLS 0.000
hsa_canvas({action:"update",  css_edits: [{selector: "body", property: "background", value: "#1a1a2e"}] })
→ Applied 1/1 (instant, no reload)
hsa_canvas({action:"diff",  before: "cap_1", after: "cap_2" }) → 3.2% change, PASS

# Step 7: Verify + VRT baseline
hsa_design_health({strict: true})
→ Score: 85/100 Grade B, 2 contrast violations, 3 improvements
hsa_canvas({action:"inspect", selector: "h1"}) → CSS cascade, AX role=heading
hsa_canvas({action:"capture",  baseline: true }) → Saved as VRT baseline
```

---

## 🎨 DESIGN TOKENS (W3C DTCG 2025.10)

> Standard: [W3C Design Tokens Community Group 2025.10 Stable](https://w3.org/groups/cg/design-tokens/)

> **Data Reference**: Read `workflows/data/design-tokens.yaml` for complete W3C DTCG token structure, OKLCH color palettes, spacing, and fluid typography.

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

- ✅ Use off-black/off-white (e.g., `#1a1a2e` / `#f8f9fa`) — avoids eye strain
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

### HSA Canvas VRT (built-in — zero config)

```
hsa_canvas({action:"capture",  baseline: true })   # Save baseline
# ... make design changes ...
hsa_canvas({action:"capture"})                      # New capture
hsa_canvas({action:"diff",  before: "baseline_id", after: "latest" })
# Returns: 3-tier diff (pHash → LooksSame → pixelmatch)
# Threshold: 0.95 (configurable)
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
---

## REFLECTION CHECKPOINT

⛔ **MANDATORY** — Execute before completing this workflow (SESSION_005):

1. **VERIFY** — Does output meet success_criteria (see YAML frontmatter)?
2. **PERSIST** — Update session memory:
   - Append task summary to `memory/session.md` (per SESSION_005 format)
   - If key decision made → append to `memory/decisions.md`
3. **SNAPSHOT** — If this is the last task in session:
   - Update `memory/CONTEXT_SNAPSHOT.md` (Recent Changes, Status, Decisions)
4. **ANCHOR** (if HSA available):
   - `hsa_session(level: "action", label: "[workflow] completed", status: "completed")`
   - `hsa_session(content: "[SESSION] Done: [summary]. Files: [list].", category: "context")`

