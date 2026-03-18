---
name: digital-marketing
description: "Digital marketing: GA4 analytics, GTM tracking, A/B testing, email marketing APIs, conversion optimization. For tracking, campaigns, or marketing integrations."
detect: ["gtag*", "*analytics*", "*gtm*", "dataLayer*", "*resend*", "*sendgrid*", "*postmark*"]
category: cross-cutting
tier: 1
---

# Digital Marketing Engineering

> 🎯 **Developer-facing marketing integration patterns**
> **Patterns**: 160+ | **Domains**: 6 | **Tools**: 15+

---

## Overview

| Domain | Tools | Data File |
| --- | --- | --- |
| **Analytics** | GA4, gtag.js, Measurement Protocol | `analytics-ga4.yaml` |
| **Tag Management** | GTM, dataLayer, Consent Mode v2 | `tag-management.yaml` |
| **A/B Testing** | PostHog, LaunchDarkly, Statsig | `ab-testing.yaml` |
| **Email Marketing** | Resend, React Email, SendGrid, Postmark | `email-marketing.yaml` |
| **Privacy Analytics** | Plausible, Umami, Fathom, Pirsch | `privacy-analytics.yaml` |
| **Conversion** | UTM, attribution, funnels, goals | `conversion-tracking.yaml` |

---

## 📊 GA4 Analytics

### Event Model (Event-Driven Architecture)

| Type | Description | Examples |
| --- | --- | --- |
| **Automatically collected** | Default, no code needed | `page_view`, `first_visit`, `session_start` |
| **Enhanced measurement** | Toggle in GA4 UI | `scroll`, `click`, `video_start`, `file_download` |
| **Recommended** | Google-defined names | `sign_up`, `login`, `purchase`, `add_to_cart` |
| **Custom** | Developer-defined | `feature_used`, `plan_upgraded`, `quiz_completed` |

### gtag.js Setup

```html
<!-- Google Tag (gtag.js) — place in <head> -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

### Custom Event Tracking

```javascript
// Track custom event
gtag('event', 'sign_up', {
  method: 'Google',
  value: 1
});

// E-commerce: purchase event (GA4 recommended)
gtag('event', 'purchase', {
  transaction_id: 'T_12345',
  value: 25.42,
  currency: 'USD',
  items: [{
    item_id: 'SKU_12345',
    item_name: 'Product Name',
    price: 25.42,
    quantity: 1
  }]
});
```

### Measurement Protocol (Server-Side)

```bash
# Send event via Measurement Protocol (server-to-server)
POST https://www.google-analytics.com/mp/collect?measurement_id=G-XXXX&api_secret=SECRET
{
  "client_id": "client_123",
  "events": [{
    "name": "purchase",
    "params": { "value": 99.99, "currency": "USD" }
  }]
}
```

---

## 🏷️ GTM & Tag Management

### dataLayer Best Practices

```javascript
// Initialize BEFORE GTM snippet
window.dataLayer = window.dataLayer || [];

// Always use push() — never overwrite
dataLayer.push({
  event: 'product_view',
  ecommerce: {
    items: [{
      item_id: 'SKU_001',
      item_name: 'Blue T-Shirt',
      price: 29.99,
      currency: 'USD'
    }]
  }
});

// Clear ecommerce before new push (prevent stale data)
dataLayer.push({ ecommerce: null });
dataLayer.push({ event: 'add_to_cart', ecommerce: { /* ... */ } });
```

### Consent Mode v2 (GDPR/CCPA)

```javascript
// Default consent state — fire BEFORE GTM loads
gtag('consent', 'default', {
  analytics_storage: 'denied',
  ad_storage: 'denied',
  ad_user_data: 'denied',        // New in v2
  ad_personalization: 'denied',   // New in v2
  wait_for_update: 500
});

// Update after user grants consent (CMP callback)
gtag('consent', 'update', {
  analytics_storage: 'granted',
  ad_storage: 'granted',
  ad_user_data: 'granted',
  ad_personalization: 'granted'
});
```

| Mode | Behavior | Data Loss |
| --- | --- | --- |
| **Basic** | Tags blocked until consent | Higher — no modeling |
| **Advanced** | Cookieless pings sent, modeled | Lower — Google models gaps |

### Server-Side Tagging

```
Browser → GTM Web Container → GTM Server Container → GA4/Ads/Meta
                                    ↓
                              First-party domain
                              (your-domain.com)
```

| Benefit | Description |
| --- | --- |
| Performance | Fewer client-side scripts |
| Privacy | Data stays first-party |
| Accuracy | Bypass ad blockers |
| Control | Transform/enrich data server-side |

---

## 🧪 A/B Testing & Feature Flags

### Tool Comparison

| Tool | Type | Open Source | Best For |
| --- | --- | --- | --- |
| **PostHog** | All-in-one | ✅ Yes | Startups, product teams |
| **LaunchDarkly** | Feature flags | ❌ No | Enterprise, CI/CD |
| **Statsig** | Experimentation | ❌ No | Statistical rigor |
| **Optimizely** | Full platform | ❌ No | Enterprise, multi-channel |

### PostHog Implementation

```javascript
// Initialize PostHog
import posthog from 'posthog-js';
posthog.init('phc_YOUR_KEY', {
  api_host: 'https://app.posthog.com'
});

// Feature flag check
if (posthog.isFeatureEnabled('new-checkout')) {
  renderNewCheckout();
} else {
  renderOldCheckout();
}

// Track experiment event
posthog.capture('checkout_completed', {
  variant: posthog.getFeatureFlag('new-checkout'),
  value: 49.99
});
```

### LaunchDarkly Implementation

```javascript
import * as ld from 'launchdarkly-js-client-sdk';

const client = ld.initialize('client-side-id', {
  key: 'user-123',
  email: 'user@example.com'
});

await client.waitForInitialization();
const showNewUI = client.variation('new-ui-experiment', false);
```

### Statistical Significance

| Metric | Minimum | Recommended |
| --- | --- | --- |
| Confidence level | 90% | 95% |
| Statistical power | 80% | 80% |
| MDE (Min Detectable Effect) | 5% | 2-5% |
| Sample size (per variant) | ~3,800 | Use calculator |

---

## 📧 Email Marketing APIs

### Provider Comparison

| Provider | Type | Best For | Pricing Model |
| --- | --- | --- | --- |
| **Resend** | Transactional | Modern React/Next.js apps | Per email |
| **React Email** | Templates | Component-based email design | Free (OSS) |
| **SendGrid** | Full platform | Scale, marketing campaigns | Tiered |
| **Postmark** | Transactional | Delivery speed, reliability | Per email |
| **Mailgun** | API-first | Developers, high volume | Per email |

### Resend + React Email

```typescript
// 1. Build template with React Email
import { Html, Head, Body, Text, Button } from '@react-email/components';

export function WelcomeEmail({ name }: { name: string }) {
  return (
    <Html>
      <Head />
      <Body style={{ fontFamily: 'Arial, sans-serif' }}>
        <Text>Welcome, {name}!</Text>
        <Button href="https://app.example.com" style={{
          backgroundColor: '#5F51E8', color: '#fff',
          padding: '12px 20px', borderRadius: '4px'
        }}>
          Get Started
        </Button>
      </Body>
    </Html>
  );
}

// 2. Send with Resend API
import { Resend } from 'resend';
const resend = new Resend('re_YOUR_API_KEY');

await resend.emails.send({
  from: 'hello@yourdomain.com',
  to: 'user@example.com',
  subject: 'Welcome!',
  react: WelcomeEmail({ name: 'Alice' })
});
```

### Email Authentication (Required)

| Protocol | Purpose | Record Type |
| --- | --- | --- |
| **SPF** | Authorize sending servers | TXT `v=spf1 include:_spf.google.com ~all` |
| **DKIM** | Sign emails cryptographically | TXT (public key from provider) |
| **DMARC** | Policy for SPF/DKIM failures | TXT `v=DMARC1; p=quarantine; rua=...` |

---

## 🔐 Privacy-First Analytics

### Tool Comparison

| Tool | Open Source | Self-Host | Cookie-Free | Script Size |
| --- | --- | --- | --- | --- |
| **Plausible** | ✅ CE | ✅ Docker | ✅ Yes | <1KB |
| **Umami** | ✅ Yes | ✅ Docker | ✅ Yes | <2KB |
| **Fathom** | ✅ Lite | ✅ Yes | ✅ Yes | ~1KB |
| **Pirsch** | ❌ No | ✅ Yes | ✅ Yes | ~1KB |
| **Matomo** | ✅ Yes | ✅ Yes | Optional | ~22KB |

### Plausible Integration

```html
<!-- Lightweight, cookie-free tracking -->
<script defer data-domain="yourdomain.com"
  src="https://plausible.io/js/script.js"></script>

<!-- Custom event tracking -->
<script>
  plausible('Signup', { props: { plan: 'pro', source: 'landing' } });
</script>
```

### Umami Self-Hosted Setup

```bash
# Docker deployment
docker run -d --name umami \
  -p 3000:3000 \
  -e DATABASE_URL=postgresql://user:pass@db:5432/umami \
  ghcr.io/umami-software/umami:postgresql-latest
```

---

## 📈 Conversion Tracking

### UTM Parameters

| Parameter | Purpose | Example |
| --- | --- | --- |
| `utm_source` | Traffic source | `google`, `newsletter` |
| `utm_medium` | Marketing medium | `cpc`, `email`, `social` |
| `utm_campaign` | Campaign name | `spring_sale_2025` |
| `utm_term` | Paid keywords | `running+shoes` |
| `utm_content` | A/B variant | `hero_v2`, `blue_cta` |

### Attribution Models

| Model | Logic | Best For |
| --- | --- | --- |
| **Last click** | 100% credit to last touchpoint | Simple, default GA4 |
| **First click** | 100% credit to first touchpoint | Brand awareness |
| **Linear** | Equal credit across all | Multi-channel |
| **Time decay** | More credit to recent | Long sales cycles |
| **Data-driven** | ML-based (GA4 default) | Sufficient data volume |

---

## ❌ Anti-Patterns

| Anti-Pattern | Risk | Fix |
| --- | --- | --- |
| Tracking without consent | GDPR fines | Implement Consent Mode v2 |
| DOM scraping for GTM data | Breaks on redesign | Use dataLayer.push() |
| Long-lived tracking cookies | Privacy violations | Cookieless or short-lived |
| No SPF/DKIM/DMARC | Emails go to spam | Configure all 3 DNS records |
| A/B test without sample size | False positives | Calculate MDE + sample first |
| Hardcoded Measurement IDs | Env mismatch | Use env variables |
| Sending from free email | Deliverability issues | Use custom domain |

---

## HSA Integration

Data powered by HSA BM25 search engine. Query YAML data via skill search:

| Domain | Query Examples |
| --- | --- |
| Analytics | "GA4 purchase event ecommerce gtag" |
| GTM | "dataLayer consent mode server-side" |
| A/B Testing | "PostHog feature flag experiment" |
| Email | "Resend React Email transactional" |
| Privacy | "Plausible Umami cookieless self-hosted" |
| Conversion | "UTM attribution funnel tracking" |

---
