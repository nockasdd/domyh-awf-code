---
name: web-perf
detect: ["lighthouse.json", "web-vitals.*", ".lighthouserc.js"]
version: "6.2.5"
category: support
tier: 1
---

# Web Performance Audit — DOMYH Awesome Code

> **Source**: Cloudflare Web-Perf Best Practices
> **Focus**: Core Web Vitals, Network Optimization, Accessibility

---

## 🎯 When to Use This Skill

Use for: Performance audits, Lighthouse optimization, page speed improvement.
**NOT for**: Functional testing (→ testing), code quality (→ coding-rules).

---

## 📊 Core Web Vitals Thresholds

| Metric          | Good    | Needs Improvement | Poor    |
| --------------- | ------- | ----------------- | ------- |
| **TTFB**        | < 800ms | < 1.8s            | > 1.8s  |
| **FCP**         | < 1.8s  | < 3s              | > 3s    |
| **LCP**         | < 2.5s  | < 4s              | > 4s    |
| **INP**         | < 200ms | < 500ms           | > 500ms |
| **TBT**         | < 200ms | < 600ms           | > 600ms |
| **CLS**         | < 0.1   | < 0.25            | > 0.25  |
| **Speed Index** | < 3.4s  | < 5.8s            | > 5.8s  |

---

## 🔄 5-PHASE AUDIT WORKFLOW

```
Performance Audit:
- [ ] Phase 1: Performance trace (navigate + record)
- [ ] Phase 2: Core Web Vitals analysis (LCP, CLS, TBT)
- [ ] Phase 3: Network analysis (render-blocking, chains)
- [ ] Phase 4: Accessibility snapshot
- [ ] Phase 5: Codebase analysis (if applicable)
```

---

## 📋 Phase 1: Performance Trace

```bash
# Using Chrome DevTools MCP
navigate_page(url: "<target-url>")
performance_start_trace(autoStop: true, reload: true)
```

## 📋 Phase 2: Core Web Vitals

| Metric | Insight Name     | What to Look For                      |
| ------ | ---------------- | ------------------------------------- |
| LCP    | `LCPBreakdown`   | TTFB, resource load, render delay     |
| CLS    | `CLSCulprits`    | Images without dimensions, font swaps |
| TBT    | `RenderBlocking` | CSS/JS blocking first paint           |

## 📋 Phase 3: Network Analysis

**Look for:**

1. **Render-blocking resources** — JS/CSS without `async`/`defer`
2. **Network chains** — Resources discovered late
3. **Missing preloads** — Critical fonts, hero images
4. **Caching issues** — Missing `Cache-Control`
5. **Large payloads** — Uncompressed bundles

## 📋 Phase 4: Accessibility

```bash
take_snapshot(verbose: true)
```

**Flag:**

- Missing ARIA IDs
- Poor contrast ratios (< 4.5:1)
- Focus traps
- Interactive elements without names

## 📋 Phase 5: Codebase (if access)

| Framework | Config Files        |
| --------- | ------------------- |
| Next.js   | `next.config.js`    |
| Vite      | `vite.config.ts`    |
| Webpack   | `webpack.config.js` |

---

## ⚡ Quick Wins Checklist

```yaml
critical:
  - "Use <link rel=preload> for LCP image/font"
  - "Add async/defer to non-critical JS"
  - "Set explicit width/height on images"
  - "Enable gzip/brotli compression"

high:
  - "Lazy load below-fold images"
  - "Use next/image or WebP format"
  - "Reduce main thread blocking"
  - "Implement font-display: swap"

medium:
  - "Add Cache-Control headers"
  - "Use CDN for static assets"
  - "Preconnect to third-party origins"
```

---

## 📊 Output Format

```markdown
## Core Web Vitals Summary

| Metric | Value | Rating               |
| ------ | ----- | -------------------- |
| LCP    | 2.1s  | 🟢 Good              |
| CLS    | 0.05  | 🟢 Good              |
| TBT    | 450ms | 🟡 Needs Improvement |

## Top Issues

1. **Render-blocking CSS** (HIGH) — main.css blocks FCP
2. **Missing image dimensions** (MEDIUM) — hero.jpg causes CLS

## Recommendations

1. Add `media="print"` to non-critical CSS
2. Add `width` and `height` to all images
```

---

## 🔧 Commands

| Command         | Description            |
| --------------- | ---------------------- |
| `/perf [url]`   | Full performance audit |
| `/perf vitals`  | Core Web Vitals only   |
| `/perf network` | Network analysis       |
| `/perf bundle`  | Bundle size analysis   |

---

## 🔌 HSA Integration

Data powered by HSA BM25 search engine:

| Domain    | Query Examples                 |
| --------- | ------------------------------ |
| CWV       | "LCP optimization preload"     |
| Network   | "render blocking CSS defer"    |
| Framework | "Next.js image optimization"   |
| Audit     | "Lighthouse performance score" |

**Data domains**: `cwv`, `network`, `framework`, `audit`

---

_DOMYH Awesome Code • Web-Perf • Core Web Vitals • HSA-Powered_
