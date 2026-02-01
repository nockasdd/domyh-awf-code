---
name: online-research
priority: 2
always_apply: true
category: intelligence
---

# 🔍 Online Research Decision Matrix

> 🌍 **Language / Ngôn ngữ**: English (default) | [Tiếng Việt](#tiếng-việt)
> 📚 **Based on**: AI Agent Best Practices 2024-2025

## Description

Rules for when agent should search online vs rely on internal knowledge.

---

## 🧠 DECISION MATRIX

### When to Search Online

| Scenario                  | Action    | Reason                     |
| ------------------------- | --------- | -------------------------- |
| API/Library documentation | ✅ Search | Versions change frequently |
| Security vulnerabilities  | ✅ Search | New CVEs daily             |
| Package compatibility     | ✅ Search | Dependency conflicts       |
| Latest framework features | ✅ Search | After knowledge cutoff     |
| Production error messages | ✅ Search | Specific solutions         |

### When to Use Internal Knowledge

| Scenario              | Action      | Reason                    |
| --------------------- | ----------- | ------------------------- |
| Core language syntax  | 🧠 Internal | Stable, well-known        |
| Design patterns       | 🧠 Internal | Timeless principles       |
| Common algorithms     | 🧠 Internal | Standard implementations  |
| Basic debugging       | 🧠 Internal | Fundamentals don't change |
| Code style/formatting | 🧠 Internal | Established conventions   |

### Hybrid Approach (Best Practice)

| Scenario                   | Primary                 | Fallback                  |
| -------------------------- | ----------------------- | ------------------------- |
| Complex debugging          | Internal analysis       | Search for specific error |
| New feature implementation | Internal patterns       | Search for examples       |
| Performance optimization   | Internal best practices | Search for benchmarks     |

---

## 🔎 SEARCH QUERY OPTIMIZATION

### Query Construction

```yaml
effective_queries:
  pattern: "[tech] [version] [specific problem] [year]"

  examples:
    good:
      - "Next.js 14 App Router middleware authentication 2025"
      - "Prisma 5 connection pooling serverless edge"
      - "React 19 useOptimistic form actions"

    bad:
      - "how to do auth" # Too vague
      - "nextjs problem" # No specifics
      - "error fix" # No context

token_limit:
  max_query_tokens: 50
  max_results_tokens: 2000
```

### Search Result Processing

```yaml
processing:
  filter:
    - Skip results older than 18 months (unless stable API)
    - Prioritize official documentation
    - Check source reliability

  extract:
    - Code snippets (verified working)
    - Configuration examples
    - Version-specific notes

  validate:
    - Cross-check with 2nd source for security
    - Verify package versions exist
    - Test code before suggesting
```

---

## 💾 CACHING STRATEGY

### Semantic Cache

```yaml
semantic_cache:
  enabled: true
  similarity_threshold: 0.85

  ttl_by_category:
    documentation: 7d
    tutorials: 3d
    security: 6h # Shorter for security
    common_queries: 6h

  invalidation:
    - On version mismatch
    - On user feedback (incorrect)
    - On explicit refresh request
```

### Context Cache

```yaml
context_cache:
  # Anthropic prompt caching
  enabled: true
  cost_reduction: "75%"

  cache_targets:
    - System prompts (static)
    - Common code patterns
    - Project structure info
```

---

## 📊 PROGRESSIVE LOADING (3-Tier)

### Tier 1: Minimal (Default)

```yaml
tier_1:
  tokens: 500
  content:
    - Query intent only
    - Top 1 result summary
  use_when: "Simple factual questions"
```

### Tier 2: Standard

```yaml
tier_2:
  tokens: 2000
  content:
    - Top 3 results
    - Code snippets
    - Key configuration
  use_when: "Implementation questions"
```

### Tier 3: Deep

```yaml
tier_3:
  tokens: 5000
  content:
    - Full documentation sections
    - Multiple examples
    - Version comparison
  use_when: "Complex debugging, security audit"
```

---

## ✅ VERIFICATION RULES

### Multi-Source Requirements

```yaml
verification:
  security_topics:
    sources_required: 2
    cross_check: mandatory
    prefer: ["official docs", "security advisories"]

  general_topics:
    sources_required: 1
    cross_check: recommended

  confidence_scoring:
    HIGH: "2+ sources agree, official docs"
    MEDIUM: "1 reliable source"
    LOW: "Single blog/forum post"
```

### Hallucination Prevention

```yaml
anti_hallucination:
  rules:
    - Never invent package names
    - Never fabricate version numbers
    - Never create fake API endpoints
    - Always verify code compiles

  targets:
    hallucination_rate: "<2%"
    faithfulness_score: ">0.9"

  actions_on_uncertainty:
    - State uncertainty explicitly
    - Suggest verification steps
    - Recommend official docs
```

---

## 📉 TOKEN OPTIMIZATION

### Budget Allocation

```yaml
token_budget:
  search_query: 50
  search_results: 2000 # Per search
  max_searches_per_task: 3
  total_search_budget: 6000

  priority_order:
    1: "Official documentation"
    2: "Verified examples"
    3: "Community solutions"
```

### Efficiency Rules

```yaml
efficiency:
  do:
    - Cache repeated queries
    - Summarize long results
    - Extract only relevant sections

  dont:
    - Search for basic syntax
    - Re-search same query
    - Include full page content
```

---

## 🛡️ SOURCE RELIABILITY

### Trusted Sources (Priority Order)

```yaml
source_priority:
  tier_1_official:
    - Official documentation sites
    - GitHub repositories (verified)
    - RFC/Spec documents

  tier_2_reliable:
    - Stack Overflow (high votes)
    - Major tech blogs (Vercel, Netlify, etc.)
    - Conference talks (recent)

  tier_3_community:
    - Medium articles (verify code)
    - Dev.to posts
    - Reddit (r/programming, etc.)

  avoid:
    - AI-generated SEO spam
    - Outdated tutorials (>2 years)
    - Unverified code snippets
```

---

## 📋 CHECKLIST

Before searching:

- [ ] Can internal knowledge answer this?
- [ ] Is query specific enough?
- [ ] Check cache for similar query?

After searching:

- [ ] Source reliable?
- [ ] Information current?
- [ ] Cross-verified (if security)?
- [ ] Code tested/verified?

---

# Tiếng Việt

> 🇻🇳 Phiên bản Tiếng Việt

## Mô Tả

Rules xác định khi nào agent nên search online vs dùng kiến thức nội bộ.

## 🧠 MA TRẬN QUYẾT ĐỊNH

### Khi Nào Search Online

| Tình huống             | Hành động | Lý do                |
| ---------------------- | --------- | -------------------- |
| Tài liệu API/Library   | ✅ Search | Versions thay đổi    |
| Lỗ hổng bảo mật        | ✅ Search | CVEs mới hàng ngày   |
| Package compatibility  | ✅ Search | Dependency conflicts |
| Features framework mới | ✅ Search | Sau knowledge cutoff |

### Khi Nào Dùng Internal Knowledge

| Tình huống              | Hành động   | Lý do                |
| ----------------------- | ----------- | -------------------- |
| Cú pháp ngôn ngữ cơ bản | 🧠 Internal | Ổn định              |
| Design patterns         | 🧠 Internal | Nguyên tắc không đổi |
| Thuật toán phổ biến     | 🧠 Internal | Standard             |

## 💾 CHIẾN LƯỢC CACHE

```yaml
semantic_cache:
  similarity_threshold: 0.85
  ttl:
    documentation: 7 ngày
    security: 6 giờ
```

## ✅ QUY TẮC XÁC MINH

```yaml
verification:
  security: "2+ nguồn bắt buộc"
  general: "1 nguồn đáng tin"

  confidence:
    HIGH: "2+ nguồn đồng ý"
    MEDIUM: "1 nguồn tin cậy"
    LOW: "Chỉ blog/forum"
```

## 📋 CHECKLIST

Trước khi search:

- [ ] Internal knowledge có thể trả lời?
- [ ] Query đủ cụ thể?
- [ ] Đã check cache?

Sau khi search:

- [ ] Nguồn đáng tin?
- [ ] Thông tin còn mới?
- [ ] Đã cross-verify (nếu security)?

---

_DOMYH Awesome Code v4.3 • Online Research Rules v1.0_
