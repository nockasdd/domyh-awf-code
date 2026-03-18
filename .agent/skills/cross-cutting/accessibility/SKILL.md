---
name: accessibility
description: "Web accessibility patterns for WCAG compliance. Use when implementing ARIA, keyboard navigation, screen reader support."
category: cross-cutting
detect: ["aria-*", "a11y*", "*.a11y.*"]
tier: 1
---

# Accessibility (WCAG 2.2)

> ♿ **Build inclusive web experiences for all users**
> **Guidelines**: WCAG 2.2 AA/AAA | **Patterns**: 100+ | **Tools**: 5+

---

## Quick Reference

| What You Need                  | Data File              | Patterns |
| ------------------------------ | ---------------------- | -------- |
| WCAG 2.2 guidelines (POUR)     | `wcag-guidelines.yaml` | 45       |
| ARIA roles, states, properties | `aria-patterns.yaml`   | 35       |
| Testing tools and automation   | `testing-tools.yaml`   | 20       |

---

## POUR Principles

| Principle          | Meaning                    | Key Guidelines                  |
| ------------------ | -------------------------- | ------------------------------- |
| **P**erceivable    | Users can perceive content | Alt text, captions, contrast    |
| **O**perable       | Users can interact         | Keyboard, timing, seizures      |
| **U**nderstandable | Users can comprehend       | Readable, predictable, errors   |
| **R**obust         | Works with assistive tech  | Valid HTML, ARIA, compatibility |

---

## Essential Checklist

| Check                          | Requirement                  | Level |
| ------------------------------ | ---------------------------- | ----- |
| ✅ Alt text on images          | Descriptive, skip decorative | A     |
| ✅ Color contrast 4.5:1 (text) | Regular text                 | AA    |
| ✅ Color contrast 7:1 (text)   | Enhanced                     | AAA   |
| ✅ Color contrast 3:1 (UI)     | Borders, icons               | AA    |
| ✅ Keyboard navigation         | All interactive elements     | A     |
| ✅ Focus visible indicator     | 2px+ outline                 | AA    |
| ✅ Touch target 24x24px        | Minimum touch size           | AA    |
| ✅ Touch target 44x44px        | Recommended                  | AAA   |
| ✅ Skip navigation link        | Skip to main content         | A     |
| ✅ Heading hierarchy           | h1 → h2 → h3 (no skips)      | A     |
| ✅ Form labels                 | Every input has label        | A     |
| ✅ Error identification        | Clear error messages         | A     |
| ✅ Reduced motion              | `prefers-reduced-motion`     | AA    |
| ✅ Language attribute          | `<html lang="en">`           | A     |

---

## ARIA Quick Reference

| Widget    | Role                     | Required Properties                      |
| --------- | ------------------------ | ---------------------------------------- |
| Modal     | `dialog`                 | `aria-modal`, `aria-labelledby`          |
| Tab       | `tab, tablist, tabpanel` | `aria-selected`, `aria-controls`         |
| Accordion | `button` + region        | `aria-expanded`, `aria-controls`         |
| Menu      | `menu, menuitem`         | `aria-haspopup`, `aria-expanded`         |
| Toast     | `alert` or `status`      | `role="alert"` (assertive)               |
| Dropdown  | `combobox, listbox`      | `aria-expanded`, `aria-activedescendant` |

### ARIA Rules

1. **Don't use ARIA if native HTML works** — `<button>` not `<div role="button">`
2. **Don't change native semantics** — `<h2 role="tab">` is wrong
3. **All interactive ARIA must be keyboard accessible**
4. **Don't use `role="presentation"` on focusable elements**
5. **All ARIA states must be updated** — `aria-expanded`, `aria-pressed`

---

## Color Contrast

| Ratio     | Text Type                        | Level |
| --------- | -------------------------------- | ----- |
| **4.5:1** | Normal text (< 18pt)             | AA    |
| **3:1**   | Large text (≥ 18pt or 14pt bold) | AA    |
| **7:1**   | Normal text                      | AAA   |
| **4.5:1** | Large text                       | AAA   |
| **3:1**   | UI components, graphics          | AA    |

```css
/* High contrast focus styles */
:focus-visible {
  outline: 3px solid #005fcc;
  outline-offset: 2px;
}

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## Testing Tools

| Tool               | Type              | Usage                           |
| ------------------ | ----------------- | ------------------------------- |
| **axe-core**       | Automated         | `npm install @axe-core/cli`     |
| **Lighthouse**     | Automated         | Chrome DevTools → Accessibility |
| **WAVE**           | Browser extension | Visual overlay of issues        |
| **pa11y**          | CI/CD             | `npx pa11y https://example.com` |
| **NVDA/VoiceOver** | Manual            | Screen reader testing           |

---

## HSA Integration

Data powered by HSA BM25 search engine. Query YAML data via skill search:

| Domain  | Query Examples                     |
| ------- | ---------------------------------- |
| WCAG    | "contrast ratio text large font"   |
| ARIA    | "dialog modal focus trap keyboard" |
| Testing | "axe lighthouse automated CI"      |
