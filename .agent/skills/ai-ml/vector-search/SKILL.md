---
name: vector-search
version: "6.3.9"
category: ai-ml
---

# Vector Search & Embeddings

> Vector databases • Semantic search • Hybrid retrieval  
> Pinecone • Weaviate • Qdrant • ChromaDB • pgvector

---

## Khi Nào Dùng

- Implement semantic search (tìm kiếm theo ý nghĩa)
- Build RAG (Retrieval-Augmented Generation) pipeline
- Chọn vector database phù hợp
- Optimize embedding & search performance

## Architecture

```
Documents → Chunking → Embedding Model → Vector DB
                                              │
Query → Embedding Model ──────────────────────┤
                                              ▼
                                     Similarity Search
                                              │
                                     Reranking (optional)
                                              │
                                     Top-K Results
```

## Vector DB Selection

| DB           | Type                 | Scale     | Best For                    |
| ------------ | -------------------- | --------- | --------------------------- |
| **Pinecone** | Managed cloud        | Billions  | Production SaaS, zero-ops   |
| **Weaviate** | Self-hosted/cloud    | Millions  | Hybrid search, multi-modal  |
| **Qdrant**   | Self-hosted/cloud    | Millions  | Performance, filtering      |
| **ChromaDB** | Embedded/self-hosted | Thousands | Dev/prototype, simple       |
| **Milvus**   | Self-hosted          | Billions  | Enterprise, GPU-accelerated |
| **pgvector** | PostgreSQL extension | Millions  | Already using PostgreSQL    |

## Core Patterns

### Embedding Generation

```typescript
// OpenAI embeddings
const response = await openai.embeddings.create({
  model: "text-embedding-3-small",
  input: "Search query or document text",
});
const embedding = response.data[0].embedding; // 1536 dimensions
```

### Chunking Strategy

| Strategy   | Chunk Size      | Overlap    | Best For        |
| ---------- | --------------- | ---------- | --------------- |
| Fixed-size | 500-1000 tokens | 50-100     | General purpose |
| Sentence   | 3-5 sentences   | 1 sentence | Q&A             |
| Semantic   | Variable        | Paragraph  | Long documents  |
| Code       | Function/class  | None       | Codebase search |

### Hybrid Search (Vector + BM25)

```typescript
// Weaviate hybrid search
const result = await client.graphql
  .get()
  .withClassName("Document")
  .withHybrid({ query: "machine learning", alpha: 0.5 }) // 0=BM25, 1=vector
  .withLimit(10)
  .do();
```

### pgvector Quick Start

```sql
CREATE EXTENSION vector;
CREATE TABLE documents (
  id SERIAL PRIMARY KEY,
  content TEXT,
  embedding vector(1536)
);
CREATE INDEX ON documents USING hnsw (embedding vector_cosine_ops);

-- Search
SELECT content, 1 - (embedding <=> query_embedding) AS similarity
FROM documents ORDER BY embedding <=> query_embedding LIMIT 10;
```

## Distance Metrics

| Metric             | Formula    | When to Use                         |
| ------------------ | ---------- | ----------------------------------- |
| **Cosine**         | 1 - cos(θ) | Normalized embeddings (most common) |
| **L2 (Euclidean)** | √Σ(a-b)²   | When magnitude matters              |
| **Dot Product**    | Σ(a×b)     | Already normalized, fastest         |

## Common Traps

| Trap                | Fix                                        |
| ------------------- | ------------------------------------------ |
| Wrong chunk size    | Test 256/512/1024 tokens, measure recall   |
| Slow search         | Use HNSW index, reduce dimensions          |
| Poor recall         | Hybrid search (vector + BM25)              |
| High embedding cost | Batch embeddings, cache, use smaller model |
| Stale data          | Implement incremental indexing pipeline    |

---

_DOMYH Awesome Code • Vector Search Skill v1.0.0_
