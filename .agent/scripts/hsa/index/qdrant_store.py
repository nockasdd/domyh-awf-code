# HSA v5.0 - Qdrant Vector Store
# =============================================================================
"""
Qdrant cloud integration for enterprise-scale vector storage.

Features:
- Cloud-native vector database
- Collection management
- Connection pooling
- Automatic migration from FAISS
- Filtering and payload support

Environment:
- HSA_QDRANT_URL: Qdrant server URL
- HSA_QDRANT_API_KEY: API key for cloud
- HSA_QDRANT_COLLECTION: Collection name (default: hsa_code)
"""

from __future__ import annotations

import logging
import os
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from ..index import BaseVectorStore, VectorSearchResult

logger = logging.getLogger("hsa.qdrant")


@dataclass
class QdrantConfig:
    """Configuration for Qdrant connection."""
    url: str = "http://localhost:6333"
    api_key: Optional[str] = None
    collection_name: str = "hsa_code"
    vector_size: int = 1024  # CodeSage v2 dimension
    distance_metric: str = "Cosine"
    timeout: float = 30.0
    prefer_grpc: bool = True
    
    @classmethod
    def from_env(cls) -> "QdrantConfig":
        """Create config from environment variables."""
        return cls(
            url=os.environ.get("HSA_QDRANT_URL", "http://localhost:6333"),
            api_key=os.environ.get("HSA_QDRANT_API_KEY"),
            collection_name=os.environ.get("HSA_QDRANT_COLLECTION", "hsa_code"),
            vector_size=int(os.environ.get("HSA_VECTOR_SIZE", "1024")),
        )
    
    @property
    def is_cloud(self) -> bool:
        """Check if using Qdrant Cloud."""
        return self.api_key is not None or "cloud.qdrant.io" in self.url


class QdrantStore(BaseVectorStore):
    """
    Qdrant-backed vector store.
    
    Enterprise-grade vector database with:
    - Horizontal scaling
    - Filtering and payload
    - Cloud or self-hosted
    
    Usage:
        store = QdrantStore()
        await store.connect()
        
        # Add vectors
        await store.add(ids, vectors, payloads)
        
        # Search
        results = await store.search(query_vector, k=10)
    """
    
    def __init__(self, config: Optional[QdrantConfig] = None):
        super().__init__()
        self.config = config or QdrantConfig.from_env()
        self._client = None
        self._connected = False
    
    async def connect(self) -> None:
        """Connect to Qdrant server."""
        try:
            from qdrant_client import QdrantClient
            from qdrant_client.http import models
            
            if self.config.api_key:
                self._client = QdrantClient(
                    url=self.config.url,
                    api_key=self.config.api_key,
                    timeout=self.config.timeout,
                    prefer_grpc=self.config.prefer_grpc,
                )
            else:
                self._client = QdrantClient(
                    url=self.config.url,
                    timeout=self.config.timeout,
                    prefer_grpc=self.config.prefer_grpc,
                )
            
            # Ensure collection exists
            await self._ensure_collection()
            
            self._connected = True
            logger.info(f"Connected to Qdrant at {self.config.url}")
            
        except ImportError:
            raise RuntimeError(
                "qdrant-client not installed. "
                "Install with: pip install qdrant-client>=1.10"
            )
        except Exception as e:
            logger.error(f"Failed to connect to Qdrant: {e}")
            raise
    
    async def _ensure_collection(self) -> None:
        """Ensure collection exists with correct schema."""
        from qdrant_client.http import models
        
        collections = self._client.get_collections().collections
        exists = any(c.name == self.config.collection_name for c in collections)
        
        if not exists:
            self._client.create_collection(
                collection_name=self.config.collection_name,
                vectors_config=models.VectorParams(
                    size=self.config.vector_size,
                    distance=models.Distance.COSINE
                    if self.config.distance_metric == "Cosine"
                    else models.Distance.DOT,
                ),
            )
            logger.info(f"Created collection: {self.config.collection_name}")
    
    async def add(
        self,
        ids: List[str],
        vectors: List[List[float]],
        payloads: Optional[List[Dict[str, Any]]] = None
    ) -> None:
        """Add vectors to the store."""
        if not self._connected:
            await self.connect()
        
        from qdrant_client.http import models
        
        points = []
        for i, (doc_id, vector) in enumerate(zip(ids, vectors)):
            payload = payloads[i] if payloads else {}
            payload["doc_id"] = doc_id
            
            points.append(models.PointStruct(
                id=hash(doc_id) % (2**63),  # Convert to int ID
                vector=vector,
                payload=payload,
            ))
        
        # Batch upsert
        self._client.upsert(
            collection_name=self.config.collection_name,
            points=points,
        )
        
        logger.debug(f"Added {len(ids)} vectors to Qdrant")
    
    async def search(
        self,
        query_vector: List[float],
        k: int = 10,
        filter_dict: Optional[Dict[str, Any]] = None,
        score_threshold: float = 0.0
    ) -> List[VectorSearchResult]:
        """Search for similar vectors."""
        if not self._connected:
            await self.connect()
        
        from qdrant_client.http import models
        
        # Build filter if provided
        query_filter = None
        if filter_dict:
            conditions = []
            for key, value in filter_dict.items():
                conditions.append(
                    models.FieldCondition(
                        key=key,
                        match=models.MatchValue(value=value),
                    )
                )
            query_filter = models.Filter(must=conditions)
        
        start = time.time()
        
        results = self._client.search(
            collection_name=self.config.collection_name,
            query_vector=query_vector,
            limit=k,
            query_filter=query_filter,
            score_threshold=score_threshold,
        )
        
        elapsed_ms = (time.time() - start) * 1000
        
        search_results = []
        for result in results:
            doc_id = result.payload.get("doc_id", str(result.id))
            search_results.append(VectorSearchResult(
                doc_id=doc_id,
                score=result.score,
                metadata=result.payload,
            ))
        
        logger.debug(f"Qdrant search returned {len(results)} results in {elapsed_ms:.2f}ms")
        
        return search_results
    
    async def delete(self, ids: List[str]) -> None:
        """Delete vectors by ID."""
        if not self._connected:
            await self.connect()
        
        from qdrant_client.http import models
        
        # Convert to int IDs
        point_ids = [hash(doc_id) % (2**63) for doc_id in ids]
        
        self._client.delete(
            collection_name=self.config.collection_name,
            points_selector=models.PointIdsList(points=point_ids),
        )
        
        logger.debug(f"Deleted {len(ids)} vectors from Qdrant")
    
    async def count(self) -> int:
        """Get total vector count."""
        if not self._connected:
            await self.connect()
        
        info = self._client.get_collection(self.config.collection_name)
        return info.points_count
    
    async def close(self) -> None:
        """Close connection."""
        if self._client:
            self._client.close()
            self._connected = False
            logger.info("Qdrant connection closed")
    
    async def migrate_from_faiss(
        self,
        faiss_store: "FAISSStore",
        batch_size: int = 100
    ) -> int:
        """Migrate vectors from FAISS to Qdrant."""
        from ..index import FAISSStore
        
        if not isinstance(faiss_store, FAISSStore):
            raise TypeError("Expected FAISSStore instance")
        
        # Get all vectors from FAISS
        all_ids = list(faiss_store._id_to_idx.keys())
        total = len(all_ids)
        
        if total == 0:
            logger.info("No vectors to migrate")
            return 0
        
        migrated = 0
        
        for i in range(0, total, batch_size):
            batch_ids = all_ids[i:i + batch_size]
            batch_vectors = []
            batch_payloads = []
            
            for doc_id in batch_ids:
                idx = faiss_store._id_to_idx[doc_id]
                vector = faiss_store._index.reconstruct(idx).tolist()
                payload = faiss_store._metadata.get(doc_id, {})
                
                batch_vectors.append(vector)
                batch_payloads.append(payload)
            
            await self.add(batch_ids, batch_vectors, batch_payloads)
            migrated += len(batch_ids)
            
            logger.info(f"Migrated {migrated}/{total} vectors to Qdrant")
        
        return migrated


def is_qdrant_enabled() -> bool:
    """Check if Qdrant is enabled via environment."""
    return bool(os.environ.get("HSA_QDRANT_URL"))


async def get_qdrant_store() -> Optional[QdrantStore]:
    """Get Qdrant store if enabled."""
    if not is_qdrant_enabled():
        return None
    
    store = QdrantStore()
    await store.connect()
    return store
