# HSA v5.0 - FAISS Vector Store
# =============================================================================
"""
FAISS vector store for semantic search.

Tier 0: FAISS flat index (100% recall, no training)
Tier 1: FAISS GPU acceleration (auto-detected)

Features:
- Flat index for small-medium codebases (100% recall)
- IVF index for large codebases (approximate but faster)
- GPU acceleration when available
- Persistence to disk
"""

from __future__ import annotations

import logging
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

logger = logging.getLogger("hsa.index")


@dataclass
class VectorSearchResult:
    """Search result with ID and score."""
    doc_id: str
    score: float
    metadata: Dict[str, Any] = field(default_factory=dict)


class BaseVectorStore(ABC):
    """Abstract base class for vector stores."""
    
    @abstractmethod
    def add(self, ids: List[str], vectors: List[List[float]]) -> None:
        """Add vectors to the store."""
        pass
    
    @abstractmethod
    def search(self, query: List[float], k: int = 10) -> List[VectorSearchResult]:
        """Search for similar vectors."""
        pass
    
    @abstractmethod
    def delete(self, ids: List[str]) -> int:
        """Delete vectors by ID."""
        pass
    
    @abstractmethod
    def clear(self) -> None:
        """Clear all vectors."""
        pass
    
    @property
    @abstractmethod
    def count(self) -> int:
        """Number of vectors in store."""
        pass


class FAISSStore(BaseVectorStore):
    """
    FAISS vector store implementation.
    
    Usage:
        store = FAISSStore(dimension=1024)
        
        # Add vectors
        store.add(["doc1", "doc2"], [[0.1, 0.2, ...], [0.3, 0.4, ...]])
        
        # Search
        results = store.search([0.1, 0.2, ...], k=10)
        for result in results:
            print(f"{result.doc_id}: {result.score}")
        
        # Persist
        store.save("index.faiss")
        store.load("index.faiss")
    """
    
    def __init__(
        self,
        dimension: int = 1024,
        use_gpu: bool = False,
        index_type: str = "flat",  # "flat" or "ivf"
        nlist: int = 100,  # IVF clusters
        max_memory_mb: int = 1024
    ):
        """
        Initialize FAISS store.
        
        Args:
            dimension: Vector dimension
            use_gpu: Whether to use GPU
            index_type: "flat" (100% recall) or "ivf" (faster but approximate)
            nlist: Number of clusters for IVF
            max_memory_mb: Maximum memory budget
        """
        self.dimension = dimension
        self.use_gpu = use_gpu
        self.index_type = index_type
        self.nlist = nlist
        self.max_memory_mb = max_memory_mb
        
        # ID mapping
        self._id_to_idx: Dict[str, int] = {}
        self._idx_to_id: Dict[int, str] = {}
        self._metadata: Dict[str, Dict[str, Any]] = {}
        self._next_idx = 0
        
        # FAISS index
        self._index = None
        self._gpu_resources = None
        
        self._init_index()
    
    def _init_index(self) -> None:
        """Initialize FAISS index."""
        try:
            import faiss
        except ImportError:
            raise ImportError(
                "faiss not installed. Install with: pip install faiss-cpu"
            )
        
        if self.index_type == "flat":
            # Flat index: 100% recall, slower for large datasets
            self._index = faiss.IndexFlatIP(self.dimension)
            logger.debug(f"Created FAISS flat index: dim={self.dimension}")
        else:
            # IVF index: approximate, faster for large datasets
            quantizer = faiss.IndexFlatIP(self.dimension)
            self._index = faiss.IndexIVFFlat(
                quantizer, 
                self.dimension, 
                self.nlist,
                faiss.METRIC_INNER_PRODUCT
            )
            logger.debug(f"Created FAISS IVF index: dim={self.dimension}, nlist={self.nlist}")
        
        # GPU acceleration
        if self.use_gpu:
            try:
                self._gpu_resources = faiss.StandardGpuResources()
                self._index = faiss.index_cpu_to_gpu(
                    self._gpu_resources, 0, self._index
                )
                logger.info("FAISS GPU acceleration enabled")
            except Exception as e:
                logger.warning(f"GPU acceleration failed, using CPU: {e}")
                self.use_gpu = False
    
    def add(
        self, 
        ids: List[str], 
        vectors: List[List[float]],
        metadata: Optional[List[Dict[str, Any]]] = None
    ) -> None:
        """
        Add vectors to the store.
        
        Args:
            ids: Document IDs
            vectors: Embedding vectors
            metadata: Optional metadata for each document
        """
        import faiss
        
        if len(ids) != len(vectors):
            raise ValueError("ids and vectors must have same length")
        
        if not vectors:
            return
        
        # Convert to numpy
        vectors_np = np.array(vectors, dtype=np.float32)
        
        # Normalize for cosine similarity
        faiss.normalize_L2(vectors_np)
        
        # Handle updates (remove existing then add)
        existing_ids = [id_ for id_ in ids if id_ in self._id_to_idx]
        if existing_ids:
            self.delete(existing_ids)
        
        # Add to index
        start_idx = self._next_idx
        
        if self.index_type == "ivf" and not self._index.is_trained:
            # Train IVF index on first batch
            self._index.train(vectors_np)
        
        self._index.add(vectors_np)
        
        # Update mappings
        for i, id_ in enumerate(ids):
            idx = start_idx + i
            self._id_to_idx[id_] = idx
            self._idx_to_id[idx] = id_
            
            if metadata and i < len(metadata):
                self._metadata[id_] = metadata[i]
        
        self._next_idx += len(ids)
        
        logger.debug(f"Added {len(ids)} vectors, total: {self.count}")
    
    def search(
        self, 
        query: List[float], 
        k: int = 10,
        min_score: float = 0.0
    ) -> List[VectorSearchResult]:
        """
        Search for similar vectors.
        
        Args:
            query: Query vector
            k: Number of results
            min_score: Minimum similarity score
            
        Returns:
            List of VectorSearchResult
        """
        import faiss
        
        if self._index.ntotal == 0:
            return []
        
        # Convert and normalize query
        query_np = np.array([query], dtype=np.float32)
        faiss.normalize_L2(query_np)
        
        # Search
        actual_k = min(k, self._index.ntotal)
        scores, indices = self._index.search(query_np, actual_k)
        
        # Build results
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0:
                continue
            
            if score < min_score:
                continue
            
            doc_id = self._idx_to_id.get(idx)
            if doc_id is None:
                continue
            
            results.append(VectorSearchResult(
                doc_id=doc_id,
                score=float(score),
                metadata=self._metadata.get(doc_id, {})
            ))
        
        return results
    
    def delete(self, ids: List[str]) -> int:
        """
        Delete vectors by ID.
        
        Note: FAISS doesn't support efficient deletion.
        For now, we mark as deleted and rebuild periodically.
        
        Args:
            ids: IDs to delete
            
        Returns:
            Number of deleted items
        """
        count = 0
        for id_ in ids:
            if id_ in self._id_to_idx:
                idx = self._id_to_idx[id_]
                del self._id_to_idx[id_]
                del self._idx_to_id[idx]
                self._metadata.pop(id_, None)
                count += 1
        
        # TODO: Implement periodic rebuild to reclaim space
        return count
    
    def clear(self) -> None:
        """Clear all vectors."""
        self._id_to_idx.clear()
        self._idx_to_id.clear()
        self._metadata.clear()
        self._next_idx = 0
        self._init_index()
    
    @property
    def count(self) -> int:
        """Number of vectors in store."""
        return len(self._id_to_idx)
    
    def save(self, path: str) -> None:
        """
        Save index to disk.
        
        Args:
            path: Path to save index
        """
        import faiss
        import pickle
        
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save FAISS index
        index_to_save = self._index
        if self.use_gpu:
            # Convert back to CPU for saving
            index_to_save = faiss.index_gpu_to_cpu(self._index)
        
        faiss.write_index(index_to_save, str(path))
        
        # Save mappings
        mappings_path = path.with_suffix(".pkl")
        with open(mappings_path, "wb") as f:
            pickle.dump({
                "id_to_idx": self._id_to_idx,
                "idx_to_id": self._idx_to_id,
                "metadata": self._metadata,
                "next_idx": self._next_idx,
                "dimension": self.dimension,
                "index_type": self.index_type
            }, f)
        
        logger.info(f"Saved FAISS index to {path}")
    
    def load(self, path: str) -> None:
        """
        Load index from disk.
        
        Args:
            path: Path to load index from
        """
        import faiss
        import pickle
        
        path = Path(path)
        
        if not path.exists():
            raise FileNotFoundError(f"Index not found: {path}")
        
        # Load FAISS index
        self._index = faiss.read_index(str(path))
        
        if self.use_gpu:
            try:
                self._gpu_resources = faiss.StandardGpuResources()
                self._index = faiss.index_cpu_to_gpu(
                    self._gpu_resources, 0, self._index
                )
            except:
                pass
        
        # Load mappings
        mappings_path = path.with_suffix(".pkl")
        if mappings_path.exists():
            with open(mappings_path, "rb") as f:
                data = pickle.load(f)
                self._id_to_idx = data["id_to_idx"]
                self._idx_to_id = data["idx_to_id"]
                self._metadata = data["metadata"]
                self._next_idx = data["next_idx"]
        
        logger.info(f"Loaded FAISS index from {path}: {self.count} vectors")
    
    def __len__(self) -> int:
        return self.count
    
    def __contains__(self, doc_id: str) -> bool:
        return doc_id in self._id_to_idx


class AdaptiveVectorStore(BaseVectorStore):
    """
    Adaptive vector store with progressive enhancement.
    
    Automatically selects:
    - FAISS (Tier 0/1)
    - Qdrant (Tier 2, if configured)
    """
    
    def __init__(self, config: Optional["AutoConfig"] = None):
        """
        Initialize with auto-config.
        
        Args:
            config: Auto-config (will be detected if not provided)
        """
        if config is None:
            from ..core.config import get_config
            config = self.config = get_config()
        else:
            self.config = config
        
        self._store: BaseVectorStore
        
        if config.use_qdrant:
            # Tier 2: Qdrant
            self._store = self._create_qdrant_store()
        else:
            # Tier 0/1: FAISS
            self._store = FAISSStore(
                dimension=1024,
                use_gpu=config.use_gpu,
                max_memory_mb=config.vector_index_mb
            )
    
    def _create_qdrant_store(self) -> BaseVectorStore:
        """Create Qdrant store (Tier 2)."""
        # TODO: Implement QdrantStore in Phase 4
        logger.warning("Qdrant not yet implemented, falling back to FAISS")
        return FAISSStore(dimension=1024)
    
    def add(self, ids: List[str], vectors: List[List[float]]) -> None:
        self._store.add(ids, vectors)
    
    def search(self, query: List[float], k: int = 10) -> List[VectorSearchResult]:
        return self._store.search(query, k)
    
    def delete(self, ids: List[str]) -> int:
        return self._store.delete(ids)
    
    def clear(self) -> None:
        self._store.clear()
    
    @property
    def count(self) -> int:
        return self._store.count


# Global store instance
_global_store: Optional[AdaptiveVectorStore] = None


def get_store() -> AdaptiveVectorStore:
    """Get global vector store."""
    global _global_store
    if _global_store is None:
        _global_store = AdaptiveVectorStore()
    return _global_store
