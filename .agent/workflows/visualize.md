---
description: "🖼️ UI/UX Design: mockups, wireframes, component design, visual prototyping"
skills: { required: [domyh-design], contextual: [auto] }
success_criteria: "Design assets generated, WCAG compliance verified, tokens exported"
---

# 🖼️ /visualize — Visualize Pro

> Component-First UI Design with Research-Backed Standards
> 📚 Multi-platform • Design Tokens (DTCG 2025.10) • A11y (WCAG 2.2) • VRT

---

## ⛔ RULES (Always Apply)

| # | Rule | Category |
|:--|:-----|:---------|
| R1 | Search existing components FIRST — reuse before generate (70-90% savings) | Efficiency |
| R2 | Design tokens ONLY — no magic color/spacing/font values | Consistency |
| R3 | WCAG 2.2 AA minimum — verify via `hsa_design(health)` | Accessibility |
| R4 | ⛔ STOP after PREVIEW — user approves before framework conversion | Safety |

---

## FIDELITY DECISION (Auto-Select)

```yaml
fidelity:
  quick:  # Wireframe — early exploration, ~2min
    trigger: "brainstorm, sketch, wireframe, layout idea"
    output: "Gray-box wireframe (no colors, no tokens)"
    method: "HTML/CSS with placeholder content"
  full:   # Production-ready — validation/implementation, ~10min
    trigger: "component, page, screen, dashboard, build"
    output: "Full design system: tokens + a11y + responsive + dark mode"
    method: "Framework components via domyh-design skill"
  image:  # Concept art — stakeholder presentations
    trigger: "mockup, concept, generate, visualize idea"
    output: "PNG/WebP image via generate_image tool"
    method: "AI image generation (not code)"
```

---

## VISUALIZE FLOW (8 Steps)

1. **DETECT** — `hsa_detect`, `hsa_search` existing components, `hsa_design({action:'analyze'})` for Design DNA. Show: `[1/8] Found {n} reusable components, Health: {score}/100 Grade {grade}`
2. **PLAN** — Select fidelity (see decision above), generate props/layout plan, define a11y requirements. Use DNA insights for consistency.
   - **VARIATION CHECK**: Read `products.yaml` `style_alternatives` + `color_palette_variants`. Pick palette matching mood (NOT default).
   - Consider `/think tradeoff` for complex design decisions
3. **TOKENS** — `hsa_design({action:'tokens', format:'dtcg'})` to generate/load W3C DTCG 2025.10 tokens. Apply platform-specific tokens (M3/HIG/Web).
   > Data ref: `domyh-design/data/design-tokens.yaml` for complete token structure + OKLCH palettes.
4. **PREVIEW** — LiveCanvas iteration loop:
   - `hsa_canvas({action:"open"})` → start dev server (auto-detect)
   - `hsa_canvas({action:"capture"})` → screenshot + CDP diagnostics (health, AX tree, CLS)
   - Show Grade (A-F) + score (/100) to user
   - Iterate: `hsa_canvas({action:"update", css_edits})` → instant CSS (no reload)
   - Repeat capture→diff until approved
   - → ⛔ **STOP: "Preview ready. Approve to build with {framework}?"**
   - `hsa_canvas({action:"close"})` when done
   - **Fallback**: If Canvas unavailable → `browser_subagent` to open preview HTML
5. **EXECUTE** — Convert approved preview → framework components, apply design system
6. **RESPONSIVE** — Container query verification + fluid typography + breakpoint validation (375/768/1024/1280/1536px)
7. **VERIFY** — `hsa_design({action:'health', strict:true})` for WCAG + a11y audit:
   - `hsa_canvas({action:"capture", baseline:true})` → VRT baseline
   - `hsa_canvas({action:"inspect", selector:'...'})` → CSS cascade, AX role
   - `hsa_canvas({action:"diff", before:"baseline", after:"latest"})` → visual regression
   > Full WCAG 2.2 checklist: `domyh-design/data/ux-guidelines.yaml`
8. **SYNC** — `hsa_check_changes`, save design decisions to memory

---

## COMMANDS

| Command | Output | Fidelity |
|:--------|:-------|:---------|
| `/visualize web [page]` | JSX/Vue/Svelte + CSS | Full |
| `/visualize mobile [screen]` | Dart/JSX/Swift | Full |
| `/visualize desktop [window]` | XAML/QML/HTML | Full |
| `/visualize component [name]` | Component code (auto-detect) | Full |
| `/visualize system` | Design tokens + docs | Full |
| `/visualize dark-mode` | Dark tokens + toggle | Full |
| `/visualize generate [desc]` | PNG/WebP via `generate_image` | Image |
| `/visualize mockup [comp]` | Mockup at 1920/1280/375px | Image |
| `/visualize tokens` | Export/import DTCG JSON | — |
| `/visualize compare` | VRT screenshot diff | — |
| `/visualize a11y [page]` | WCAG 2.2 audit report | — |
| `/visualize migrate [from]` | Design token migration | — |

---

## COMPONENT MAPPING (Key Feature)

**Priority: Map BEFORE Generate**

1. **Index** — Scan `src/components`, `components`, `src/ui`
2. **Match** — Request → existing components (R1: 70-90% reuse)
3. **Gap** — Only generate what's missing

---

## WIREFRAME TEMPLATES

| Pattern | Layout | Use Case |
|:--------|:-------|:---------|
| Dashboard | Header + Sidebar + Grid | Admin panels |
| Detail Page | Header + Content + Actions | Entity view |
| List + Filter | FilterBar + Table/Cards | Data browsing |
| Auth Flow | Centered card | Login/Register |
| Settings | Sidebar nav + Form | App settings |
| Landing | Hero + Features + CTA | Marketing |

---

## AI IMAGE GENERATION

| Command | Tool | Resolutions |
|:--------|:-----|:------------|
| `/visualize generate [desc]` | `generate_image` | PNG, JPG, WebP |
| `/visualize mockup [comp]` | `generate_image` | 1920×1080, 1280×720, 375×812 |

---

## REFERENCE DATA (Lazy-Load from domyh-design skill)

> Full guidelines loaded via `skills: { required: [domyh-design] }`. Agent reads YAML data files on demand:

| Need | Data File | Content |
|:-----|:----------|:--------|
| Design tokens | `data/design-tokens.yaml` | W3C DTCG, OKLCH palettes, spacing, typography |
| WCAG 2.2 checklist | `data/ux-guidelines.yaml` | 9 new WCAG 2.2 criteria, contrast, focus, touch |
| Dark mode strategy | `data/ux-guidelines.yaml` | OKLCH off-black/off-white, prefers-color-scheme |
| Platform guidelines | `data/platform-guidelines.yaml` | M3 Expressive, Apple HIG Liquid Glass, breakpoints |
| Component mapping | `data/component-mapping.yaml` | 30 components with reuse scores |
| Stack-specific | `data/stacks/{framework}.yaml` | React/Vue/Flutter/SwiftUI/Electron patterns |

---

## CASCADE EVALUATION (Recommended — MCP)

⚠️ **Evaluate before EXECUTE** — see `delegation-intelligence` skill for scoring.

```
hsa_delegate({action:'cascade', cascade_text:'[prompt]', task_type:'browser'})
→ wait 5s → hsa_delegate({action:'cascade_read', cascade_id:'...'})
```
**Auto-cascade** (≥6.5): Multi-platform, design system migration
**Suggest cascade** (4.0-6.5): VRT >10 components, complex layout

---

## SYNERGY

| Workflow | When to use with /visualize |
|:---------|:----------------------------|
| `/code` (T3) | Routes design-only intent → `/visualize` |
| `/think` | `/think tradeoff` for design approach decisions |
| `/plan` | Design decisions flow from planning phase |
| `/scaffold` | After approval → generate component files |

---

## REFLECTION CHECKPOINT

⛔ **MANDATORY** — Execute before completing this workflow (SESSION_005):

1. **VERIFY** — Does output meet success_criteria (see YAML frontmatter)?
   - Design tokens used (no magic values)? Responsive verified? WCAG health ≥ B?
2. **PERSIST** (if HSA available — preferred, 1 tool call):
   - `hsa_session({action:'persist', task_summary:'[workflow] [summary]', files_touched:[...]})`
   - If key decision → `hsa_session({action:'anchor', content:'[decision]', category:'decision'})`
3. **PERSIST** (if HSA unavailable — manual fallback):
   - Append task summary to `memory/session.md`
   - If last task → Update `memory/CONTEXT_SNAPSHOT.md`
