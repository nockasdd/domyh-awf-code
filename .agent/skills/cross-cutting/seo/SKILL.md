---
name: seo
version: "6.4.2"
category: cross-cutting
---

# SEO & Core Web Vitals

> 🔍 **Search engine optimization for modern web applications**
> **Patterns**: 90+ | **Metrics**: CWV + Technical + On-page

---

## Quick Reference

| What You Need                         | Data File              | Patterns |
| ------------------------------------- | ---------------------- | -------- |
| Core Web Vitals (LCP, INP, CLS)       | `core-web-vitals.yaml` | 30       |
| Structured data (JSON-LD, Schema.org) | `structured-data.yaml` | 30       |
| Technical SEO (sitemap, robots, meta) | `technical-seo.yaml`   | 30       |

---

## Core Web Vitals (2025)

| Metric                              | Measures         | Good    | Needs Work | Poor    |
| ----------------------------------- | ---------------- | ------- | ---------- | ------- |
| **LCP** (Largest Contentful Paint)  | Loading          | ≤ 2.5s  | ≤ 4.0s     | > 4.0s  |
| **INP** (Interaction to Next Paint) | Responsiveness   | ≤ 200ms | ≤ 500ms    | > 500ms |
| **CLS** (Cumulative Layout Shift)   | Visual stability | ≤ 0.1   | ≤ 0.25     | > 0.25  |

### Optimization Quick Wins

| Metric  | Fix                                                   | Impact |
| ------- | ----------------------------------------------------- | ------ |
| **LCP** | Preload hero image: `<link rel="preload" as="image">` | High   |
| **LCP** | Use `priority` on Next.js Image component             | High   |
| **INP** | Debounce event handlers                               | Medium |
| **INP** | Use `requestIdleCallback` for non-urgent work         | Medium |
| **CLS** | Set explicit `width`/`height` on images               | High   |
| **CLS** | Use `font-display: swap` for web fonts                | Medium |

---

## Essential Meta Tags

```html
<head>
  <title>Page Title — Brand (50-60 chars)</title>
  <meta name="description" content="Compelling description (150-160 chars)" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <link rel="canonical" href="https://example.com/page" />

  <!-- Open Graph -->
  <meta property="og:title" content="Page Title" />
  <meta property="og:description" content="Description" />
  <meta property="og:image" content="https://example.com/og.jpg" />
  <meta property="og:type" content="website" />

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="Page Title" />
</head>
```

---

## Structured Data (JSON-LD)

```html
<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "Article Title",
    "author": { "@type": "Person", "name": "Author" },
    "datePublished": "2025-01-01",
    "image": "https://example.com/image.jpg"
  }
</script>
```

| Schema Type        | Best For         |
| ------------------ | ---------------- |
| **Article**        | Blog posts, news |
| **Product**        | E-commerce       |
| **FAQ**            | FAQ pages        |
| **BreadcrumbList** | Navigation       |
| **Organization**   | Company info     |
| **LocalBusiness**  | Physical stores  |
| **HowTo**          | Tutorials        |

---

## Technical SEO Checklist

| Check                | Implementation                    |
| -------------------- | --------------------------------- |
| ✅ Sitemap           | `/sitemap.xml` with all URLs      |
| ✅ Robots.txt        | `/robots.txt` with crawl rules    |
| ✅ Canonical URLs    | `<link rel="canonical">`          |
| ✅ HTTPS             | Secure origin                     |
| ✅ Mobile responsive | Viewport meta + responsive design |
| ✅ 301 redirects     | Permanent URL changes             |
| ✅ hreflang          | Multi-language support            |
| ✅ Semantic HTML     | Proper heading hierarchy (h1→h6)  |
| ✅ Alt text          | Descriptive image alt attributes  |
| ✅ Internal linking  | Connect related pages             |

---

## HSA Integration

Data powered by HSA BM25 search engine. Query YAML data via skill search:

| Domain          | Query Examples                         |
| --------------- | -------------------------------------- |
| CWV             | "LCP largest contentful paint preload" |
| Structured Data | "JSON-LD schema.org product article"   |
| Technical       | "sitemap robots canonical hreflang"    |
