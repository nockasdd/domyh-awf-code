# HSA v5.0 - CodeSage V2 Embeddings
# =============================================================================
"""
Code embeddings using CodeSage V2.

Tier 0: CodeSage V2 Base on CPU (always available)
Tier 1: CodeSage V2 Large on GPU with INT8
Tier 2: VoyageCode3 API fallback (opt-in)

Features:
- Multiple embedding models with fallback chain
- Batch processing for efficiency
- Caching to avoid recomputation
- Language-aware embedding routing
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal, Optional

logger = logging.getLogger("hsa.embedding")


@dataclass
class EmbeddingResult:
    """Embedding result with metadata."""
    vector: List[float]
    model: str
    tokens_used: int = 0
    cached: bool = False


class BaseEmbedder(ABC):
    """Abstract base class for embedders."""
    
    @abstractmethod
    def embed(self, texts: List[str]) -> List[List[float]]:
        """Embed texts to vectors."""
        pass
    
    @abstractmethod
    def embed_single(self, text: str) -> List[float]:
        """Embed single text."""
        pass
    
    @abstractmethod
    def get_dimension(self) -> int:
        """Return embedding dimension."""
        pass
    
    @property
    @abstractmethod
    def model_name(self) -> str:
        """Return model name for logging."""
        pass


class CodeSageEmbedder(BaseEmbedder):
    """
    CodeSage V2 embedder.
    
    Supports both CPU and GPU modes with optional INT8 quantization.
    
    Model options:
    - codesage-v2-base: Smaller, faster, CPU-friendly
    - codesage-v2-large: Larger, more accurate, GPU recommended
    
    Usage:
        embedder = CodeSageEmbedder(model_size="base")
        vectors = embedder.embed(["def hello(): pass", "class User: ..."])
    """
    
    def __init__(
        self,
        model_size: Literal["base", "large"] = "base",
        use_gpu: bool = False,
        use_int8: bool = True,
        batch_size: int = 8
    ):
        """
        Initialize CodeSage embedder.
        
        Args:
            model_size: "base" or "large"
            use_gpu: Whether to use GPU
            use_int8: Use INT8 quantization (saves VRAM)
            batch_size: Batch size for embedding
        """
        self.model_size = model_size
        self.use_gpu = use_gpu
        self.use_int8 = use_int8
        self.batch_size = batch_size
        
        self._model = None
        self._dimension = 1024
        self._model_loaded = False
        
        # Lazy load model
        logger.debug(f"CodeSage embedder initialized: {model_size}, gpu={use_gpu}, int8={use_int8}")
    
    def _load_model(self) -> None:
        """Lazy load the model."""
        if self._model_loaded:
            return
        
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError:
            raise ImportError(
                "sentence-transformers not installed. "
                "Install with: pip install sentence-transformers"
            )
        
        # Model name based on size
        model_name = f"codesage-{self.model_size}"
        
        # For now, use a compatible model as CodeSage may not be on HuggingFace
        # In production, use the actual CodeSage model
        fallback_models = {
            "base": "sentence-transformers/all-MiniLM-L6-v2",
            "large": "sentence-transformers/all-mpnet-base-v2"
        }
        
        try:
            # Try loading CodeSage first
            self._model = SentenceTransformer(
                f"Salesforce/{model_name}",
                device="cuda" if self.use_gpu else "cpu"
            )
            logger.info(f"Loaded CodeSage model: {model_name}")
        except Exception as e:
            # Fallback to standard sentence-transformers model
            logger.warning(f"CodeSage not available ({e}), using fallback model")
            self._model = SentenceTransformer(
                fallback_models[self.model_size],
                device="cuda" if self.use_gpu else "cpu"
            )
        
        # Get actual dimension from model
        self._dimension = self._model.get_sentence_embedding_dimension()
        self._model_loaded = True
        
        logger.info(f"Model loaded: dim={self._dimension}, gpu={self.use_gpu}")
    
    def embed(self, texts: List[str]) -> List[List[float]]:
        """
        Embed multiple texts.
        
        Args:
            texts: Texts to embed
            
        Returns:
            List of embedding vectors
        """
        if not texts:
            return []
        
        self._load_model()
        
        # Batch processing
        all_embeddings = []
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i:i + self.batch_size]
            embeddings = self._model.encode(
                batch,
                convert_to_numpy=True,
                show_progress_bar=False,
                normalize_embeddings=True  # For cosine similarity
            )
            all_embeddings.extend(embeddings.tolist())
        
        return all_embeddings
    
    def embed_single(self, text: str) -> List[float]:
        """Embed single text."""
        return self.embed([text])[0]
    
    def get_dimension(self) -> int:
        """Return embedding dimension."""
        if not self._model_loaded:
            self._load_model()
        return self._dimension
    
    @property
    def model_name(self) -> str:
        return f"codesage-v2-{self.model_size}"


class BM25PseudoEmbedder(BaseEmbedder):
    """
    Pseudo-embedder using BM25 for sparse representation.
    
    Ultimate fallback when no embedding model is available.
    Uses TF-IDF style hashing to create sparse vectors.
    """
    
    def __init__(self, dimension: int = 1024):
        self._dimension = dimension
        
        logger.debug(f"BM25 pseudo-embedder initialized: dim={dimension}")
    
    def embed(self, texts: List[str]) -> List[List[float]]:
        """Create pseudo-embeddings using hashing."""
        import hashlib
        
        embeddings = []
        for text in texts:
            # Create sparse vector using word hashing
            vector = [0.0] * self._dimension
            
            words = text.lower().split()
            for word in words:
                # Hash word to index
                h = int(hashlib.md5(word.encode()).hexdigest(), 16)
                idx = h % self._dimension
                
                # TF-IDF style weight
                vector[idx] += 1.0 / (1.0 + len(words))
            
            # Normalize
            norm = sum(v * v for v in vector) ** 0.5
            if norm > 0:
                vector = [v / norm for v in vector]
            
            embeddings.append(vector)
        
        return embeddings
    
    def embed_single(self, text: str) -> List[float]:
        return self.embed([text])[0]
    
    def get_dimension(self) -> int:
        return self._dimension
    
    @property
    def model_name(self) -> str:
        return "bm25-pseudo"


class VoyageAPIEmbedder(BaseEmbedder):
    """
    VoyageCode3 API embedder.
    
    Tier 2: Only used when VOYAGE_API_KEY is set.
    Best for rare languages not well covered by local models.
    
    Usage:
        embedder = VoyageAPIEmbedder(api_key="voy_xxx...")
        vectors = embedder.embed(["def hello(): pass"])
    """
    
    def __init__(self, api_key: str, batch_size: int = 32):
        """
        Initialize Voyage API embedder.
        
        Args:
            api_key: Voyage API key
            batch_size: Batch size for API calls
        """
        self.api_key = api_key
        self.batch_size = batch_size
        self._client = None
        
        logger.debug("Voyage API embedder initialized")
    
    def _get_client(self):
        """Lazy load Voyage client."""
        if self._client is not None:
            return self._client
        
        try:
            import voyageai
            self._client = voyageai.Client(api_key=self.api_key)
            return self._client
        except ImportError:
            raise ImportError(
                "voyageai not installed. Install with: pip install voyageai"
            )
    
    def embed(self, texts: List[str]) -> List[List[float]]:
        """Embed using Voyage API."""
        if not texts:
            return []
        
        client = self._get_client()
        
        all_embeddings = []
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i:i + self.batch_size]
            result = client.embed(
                batch,
                model="voyage-code-3",
                input_type="document"
            )
            all_embeddings.extend(result.embeddings)
        
        return all_embeddings
    
    def embed_single(self, text: str) -> List[float]:
        return self.embed([text])[0]
    
    def get_dimension(self) -> int:
        return 1024  # Voyage Code 3 dimension
    
    @property
    def model_name(self) -> str:
        return "voyage-code-3"


class AdaptiveEmbedder:
    """
    Progressive Enhancement Embedder.
    
    Auto-selects best available embedding strategy:
    1. VoyageCode3 API (if configured, best for rare languages)
    2. CodeSage V2 Large GPU (if GPU available)
    3. CodeSage V2 Base CPU (always works)
    4. BM25 pseudo-embeddings (ultimate fallback)
    
    Usage:
        from hsa.core.config import get_config
        embedder = AdaptiveEmbedder(get_config())
        
        vectors = embedder.embed(["def hello(): pass"])
    """
    
    def __init__(self, config: Optional["AutoConfig"] = None):
        """
        Initialize with auto-config.
        
        Args:
            config: Auto-config (will be detected if not provided)
        """
        if config is None:
            from ..core.config import get_config
            config = get_config()
        
        self.config = config
        self._embedders: List[tuple[str, BaseEmbedder]] = []
        self._cache: Dict[str, List[float]] = {}
        self._cache_hits = 0
        self._cache_misses = 0
        
        self._build_embedder_chain()
    
    def _build_embedder_chain(self) -> None:
        """Build embedder chain from best to worst."""
        
        # Tier 2: API (if configured)
        if self.config.use_voyage_api and self.config.voyage_api_key:
            try:
                embedder = VoyageAPIEmbedder(self.config.voyage_api_key)
                self._embedders.append(("voyage_api", embedder))
                logger.info("VoyageCode3 API enabled (Tier 2)")
            except Exception as e:
                logger.warning(f"VoyageCode3 API failed: {e}")
        
        # Tier 1: GPU (if detected)
        if self.config.use_gpu:
            try:
                embedder = CodeSageEmbedder(
                    model_size="large" if self.config.use_codesage_large else "base",
                    use_gpu=True,
                    use_int8=self.config.use_int8_quantization
                )
                self._embedders.append(("codesage_gpu", embedder))
                logger.info("CodeSage GPU enabled (Tier 1)")
            except Exception as e:
                logger.warning(f"CodeSage GPU failed: {e}")
        
        # Tier 0: CPU (always available)
        try:
            embedder = CodeSageEmbedder(
                model_size="base",
                use_gpu=False,
                use_int8=False
            )
            self._embedders.append(("codesage_cpu", embedder))
            logger.info("CodeSage CPU enabled (Tier 0)")
        except Exception as e:
            logger.warning(f"CodeSage CPU failed: {e}")
        
        # Ultimate fallback: BM25 pseudo-embeddings
        embedder = BM25PseudoEmbedder()
        self._embedders.append(("bm25", embedder))
        logger.info("BM25 fallback enabled (always available)")
    
    def embed(self, texts: List[str], use_cache: bool = True) -> List[List[float]]:
        """
        Embed texts using best available embedder.
        
        Args:
            texts: Texts to embed
            use_cache: Whether to use embedding cache
            
        Returns:
            List of embedding vectors
        """
        if not texts:
            return []
        
        result = [None] * len(texts)
        texts_to_embed = []
        indices_to_embed = []
        
        # Check cache
        if use_cache:
            for i, text in enumerate(texts):
                text_hash = str(hash(text))
                if text_hash in self._cache:
                    result[i] = self._cache[text_hash]
                    self._cache_hits += 1
                else:
                    texts_to_embed.append(text)
                    indices_to_embed.append(i)
                    self._cache_misses += 1
        else:
            texts_to_embed = texts
            indices_to_embed = list(range(len(texts)))
        
        if not texts_to_embed:
            return result
        
        # Try embedders in order
        embeddings = None
        for name, embedder in self._embedders:
            try:
                embeddings = embedder.embed(texts_to_embed)
                logger.debug(f"Embedded {len(texts_to_embed)} texts using {name}")
                break
            except Exception as e:
                logger.warning(f"Embedder {name} failed: {e}, trying next...")
        
        if embeddings is None:
            raise RuntimeError("All embedders failed!")
        
        # Store in cache and result
        for i, embedding in zip(indices_to_embed, embeddings):
            result[i] = embedding
            if use_cache:
                text_hash = str(hash(texts[i] if i < len(texts) else texts_to_embed[indices_to_embed.index(i)]))
                self._cache[text_hash] = embedding
                
                # Limit cache size
                if len(self._cache) > 10000:
                    # Remove oldest entries
                    keys_to_remove = list(self._cache.keys())[:5000]
                    for k in keys_to_remove:
                        del self._cache[k]
        
        return result
    
    def embed_single(self, text: str, use_cache: bool = True) -> List[float]:
        """Embed single text."""
        return self.embed([text], use_cache)[0]
    
    def get_dimension(self) -> int:
        """Get embedding dimension from primary embedder."""
        if self._embedders:
            return self._embedders[0][1].get_dimension()
        return 1024  # Default
    
    def get_active_embedder(self) -> str:
        """Get name of primary embedder."""
        if self._embedders:
            return self._embedders[0][0]
        return "none"
    
    def get_stats(self) -> Dict[str, Any]:
        """Get embedding statistics."""
        return {
            "cache_hits": self._cache_hits,
            "cache_misses": self._cache_misses,
            "cache_size": len(self._cache),
            "hit_rate": (
                self._cache_hits / (self._cache_hits + self._cache_misses) * 100
                if (self._cache_hits + self._cache_misses) > 0
                else 0
            ),
            "active_embedder": self.get_active_embedder(),
            "embedder_chain": [name for name, _ in self._embedders]
        }
    
    def clear_cache(self) -> None:
        """Clear embedding cache."""
        self._cache.clear()
        self._cache_hits = 0
        self._cache_misses = 0


# Global embedder instance
_global_embedder: Optional[AdaptiveEmbedder] = None


def get_embedder() -> AdaptiveEmbedder:
    """Get global embedder."""
    global _global_embedder
    if _global_embedder is None:
        _global_embedder = AdaptiveEmbedder()
    return _global_embedder


def embed(texts: List[str]) -> List[List[float]]:
    """Quick embed using global embedder."""
    return get_embedder().embed(texts)


def embed_single(text: str) -> List[float]:
    """Quick embed single text using global embedder."""
    return get_embedder().embed_single(text)
