# 🧠 HSA — Hierarchical Skills Architecture

> **Version**: 1.0.0 | **Python**: ≥3.10 | **Author**: NockDev

Unified context management engine for AI coding agents. Combines v4 orchestration with v5 progressive enhancement.

---

## 📦 Installation

```bash
# From project root
pip install -r .agent/scripts/hsa/requirements.txt
```

---

## 🚀 Quick Start

```python
from hsa import HSAEngine, get_context

# Quick API
context = get_context(query_files=["main.py"], max_tokens=8000)
print(f"Tier: {context.tier_name}")  # "baseline" | "gpu" | "distributed"
print(f"Tokens: {context.token_count}")

# Full engine
engine = HSAEngine.from_project("/path/to/project")
result = engine.get_context(
    query="handle user authentication",
    max_tokens=16000
)
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    HSAEngine (Facade)                       │
├─────────────────────────────────────────────────────────────┤
│  context/     │  detection/   │  merkle/      │  prefetch/  │
│  Token budget │  Stack detect │  Change track │  Prefetch   │
├───────────────┴───────────────┴───────────────┴─────────────┤
│  core/        │  tokenizer/   │  cache/       │  search/    │
│  Capabilities │  Tiktoken     │  LRU+Redis    │  BM25       │
├───────────────┴───────────────┴───────────────┴─────────────┤
│  index/       │  embedding/   │  ast/         │  retrieval/ │
│  FAISS/Qdrant │  CodeSage     │  Tree-sitter  │  HiRAG      │
├─────────────────────────────────────────────────────────────┤
│                      daemon/ (IPC)                          │
└─────────────────────────────────────────────────────────────┘
```

---

## 📚 Modules

| Module      | Purpose                     | Key Classes                        |
| ----------- | --------------------------- | ---------------------------------- |
| `core`      | System capabilities, config | `SystemCapabilities`, `AutoConfig` |
| `tokenizer` | Accurate token counting     | `AccurateTokenCounter`             |
| `cache`     | LRU + Redis caching         | `LRUCache`, `CacheStats`           |
| `search`    | BM25 keyword search         | `BM25Index`, `SearchResult`        |
| `index`     | Vector storage              | `FAISSStore`, `QdrantStore`        |
| `embedding` | Code embeddings             | `CodeSageEmbedder`, `VoyageAPI`    |
| `ast`       | Tree-sitter parsing         | `TreeSitterParser`, `ParseResult`  |
| `retrieval` | HiRAG retrieval             | `HiRAGRetriever`, `Entity`         |
| `context`   | Token budgeting             | `TokenBudgetManager`, `ContextGC`  |
| `detection` | Project detection           | `ScoringProjectDetector`           |
| `merkle`    | Change tracking             | `MerkleCodeTracker`                |
| `prefetch`  | Proactive loading           | `Prefetcher`, `TrajectoryModel`    |
| `engine`    | Main orchestrator           | `HSAEngine`, `ContextResult`       |
| `daemon`    | IPC server                  | `HSADaemon`, `DaemonClient`        |

---

## 🎯 Progressive Enhancement Tiers

| Tier | Name        | Requirements | Features                     |
| ---- | ----------- | ------------ | ---------------------------- |
| 0    | Baseline    | Any machine  | BM25, FAISS CPU, tiktoken    |
| 1    | GPU         | CUDA GPU     | INT8 embeddings, GPU FAISS   |
| 2    | Distributed | Qdrant/Redis | External vector DB, L2 cache |

```python
from hsa.core import get_capabilities

caps = get_capabilities()
print(f"Tier: {caps.tier}")  # 0, 1, or 2
print(f"GPU: {caps.has_gpu}")
print(f"Memory: {caps.available_memory_gb}GB")
```

---

## 🔧 Configuration

```python
from hsa import HSAEngine, EngineConfig

config = EngineConfig(
    max_tokens=16000,
    include_stack=True,
    use_cache=True,
    tier=None,  # Auto-detect
)

engine = HSAEngine(config)
```

### Environment Variables

| Variable         | Default | Description                |
| ---------------- | ------- | -------------------------- |
| `HSA_TIER`       | auto    | Force tier (0, 1, 2)       |
| `HSA_MAX_TOKENS` | 8000    | Default token budget       |
| `HSA_QDRANT_URL` | -       | Qdrant server URL (Tier 2) |
| `HSA_REDIS_URL`  | -       | Redis server URL (Tier 2)  |
| `VOYAGE_API_KEY` | -       | Voyage AI API key          |

---

## 🧪 Testing

```bash
# Run unit tests
pytest .agent/scripts/hsa/tests/ -v

# Test imports
python -c "from hsa import HSAEngine; print('OK')"
```

---

## ⚠️ Migration from v4/v5

```python
# Old (deprecated)
from hsa import HSAv4Engine

# New (recommended)
from hsa import HSAEngine
```

Both `hsa` and `hsa` are now shims that re-export from `hsa` with deprecation warnings.

---

_HSA v1.0.0 • DOMYH Awesome Code • NockDev_
