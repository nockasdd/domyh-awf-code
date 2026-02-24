---
name: rag-patterns
version: "6.4.3"
category: ai-ml
---

# 🧠 RAG Patterns

> Retrieval-Augmented Generation architecture patterns
> 📚 Chunking • Embeddings • Vector DBs • Retrieval • Evaluation

---

## Quick Reference

| Component      | Options                            | Recommendation           |
| -------------- | ---------------------------------- | ------------------------ |
| **Chunking**   | Fixed, Semantic, Recursive         | Recursive for docs       |
| **Embeddings** | OpenAI, Cohere, Jina, local        | text-embedding-3-small   |
| **Vector DB**  | Pinecone, Qdrant, Chroma, pgvector | pgvector for existing PG |
| **Retrieval**  | Similarity, Hybrid, Reranking      | Hybrid + Reranking       |
| **Evaluation** | RAGAS, faithfulness, relevancy     | RAGAS framework          |

---

## RAG Pipeline

```
Documents → Chunking → Embedding → Vector Store
                                        ↓
Query → Embedding → Similarity Search → Retrieved Chunks
                                        ↓
                              LLM + Context → Answer
```

---

## Naive vs Advanced RAG

| Aspect        | Naive RAG               | Advanced RAG          |
| ------------- | ----------------------- | --------------------- |
| Chunking      | Fixed 512 tokens        | Semantic boundaries   |
| Retrieval     | Top-K similarity        | Hybrid + reranking    |
| Context       | All chunks concatenated | Filtered + compressed |
| Hallucination | Common                  | Reduced (citations)   |
| Latency       | Fast                    | Moderate              |

---

## Chunking Strategies

| Strategy           | Best For             | Overlap            |
| ------------------ | -------------------- | ------------------ |
| **Fixed-size**     | Simple docs, logs    | 10-20%             |
| **Recursive**      | Markdown, code, HTML | Respects structure |
| **Semantic**       | Mixed content        | By meaning change  |
| **Document-aware** | PDFs, tables         | Preserves layout   |

---

## Embedding Models (2026)

| Model                  | Dimensions | Context | Speed   | Quality |
| ---------------------- | ---------- | ------- | ------- | ------- |
| text-embedding-3-small | 1536       | 8K      | ⚡ Fast | Good    |
| text-embedding-3-large | 3072       | 8K      | Medium  | Great   |
| Cohere embed-v4        | 1024       | 512     | Fast    | Great   |
| Jina v3                | 1024       | 8K      | Fast    | Good    |
| BGE-M3 (local)         | 1024       | 8K      | Varies  | Good    |

---

## Vector Databases

| Database     | Type        | Best For                 |
| ------------ | ----------- | ------------------------ |
| **pgvector** | Extension   | Already using PostgreSQL |
| **Pinecone** | Managed     | Production, serverless   |
| **Qdrant**   | Self-hosted | Full control, filtering  |
| **Chroma**   | Embedded    | Prototyping, small scale |
| **Weaviate** | Self-hosted | Multi-modal, hybrid      |
| **Milvus**   | Self-hosted | Large scale, GPU         |

---

## HSA Integration

| Query                               | Data File                  |
| ----------------------------------- | -------------------------- |
| `chunking fixed semantic recursive` | `chunking-strategies.yaml` |
| `embedding model openai cohere`     | `embedding-models.yaml`    |
| `pinecone qdrant chroma pgvector`   | `vector-databases.yaml`    |
| `hybrid search reranking hyde`      | `retrieval-patterns.yaml`  |
| `ragas faithfulness evaluation`     | `evaluation.yaml`          |

---

_DOMYH Awesome Code • RAG Patterns_
