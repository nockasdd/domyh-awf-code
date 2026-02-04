# HSA v5.0 - Hybrid Search Engine
# =============================================================================
"""
Hybrid search combining vector similarity and BM25 keyword search.

Features:
- Weighted combination (default: 70% vector, 30% BM25)
- Score normalization (min-max)
- Reciprocal Rank Fusion (RRF)
- Configurable fusion strategies
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

logger = logging.getLogger("hsa.hybrid")


class FusionStrategy(Enum):
    """Score fusion strategies."""
    WEIGHTED_SUM = "weighted_sum"
    RRF = "rrf"  # Reciprocal Rank Fusion
    MAX_SCORE = "max_score"
    LINEAR_COMBINATION = "linear_combination"


@dataclass
class HybridResult:
    """Result from hybrid search."""
    doc_id: str
    combined_score: float
    vector_score: Optional[float] = None
    bm25_score: Optional[float] = None
    vector_rank: Optional[int] = None
    bm25_rank: Optional[int] = None
    content: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class HybridConfig:
    """Configuration for hybrid search."""
    vector_weight: float = 0.7
    bm25_weight: float = 0.3
    fusion_strategy: FusionStrategy = FusionStrategy.WEIGHTED_SUM
    rrf_k: int = 60  # RRF constant (typical values: 20-100)
    min_score: float = 0.0
    normalize_scores: bool = True
    deduplicate: bool = True


class ScoreNormalizer:
    """
    Normalize scores to [0, 1] range.
    
    Methods:
    - min_max: (x - min) / (max - min)
    - z_score: (x - mean) / std
    - sigmoid: 1 / (1 + exp(-x))
    """
    
    @staticmethod
    def min_max(scores: List[float]) -> List[float]:
        """Min-max normalization."""
        if not scores:
            return []
        
        min_score = min(scores)
        max_score = max(scores)
        
        if max_score == min_score:
            return [1.0] * len(scores)
        
        return [(s - min_score) / (max_score - min_score) for s in scores]
    
    @staticmethod
    def z_score(scores: List[float]) -> List[float]:
        """Z-score normalization."""
        if not scores:
            return []
        
        import statistics
        
        mean = statistics.mean(scores)
        try:
            std = statistics.stdev(scores)
        except:
            std = 1.0
        
        if std == 0:
            return [0.0] * len(scores)
        
        return [(s - mean) / std for s in scores]
    
    @staticmethod
    def sigmoid(scores: List[float], scale: float = 1.0) -> List[float]:
        """Sigmoid normalization."""
        import math
        
        return [1.0 / (1.0 + math.exp(-s * scale)) for s in scores]


class HybridSearchEngine:
    """
    Hybrid search engine combining vector and BM25 search.
    
    Usage:
        engine = HybridSearchEngine()
        
        results = engine.search(
            query="authentication",
            k=10,
            filters={"file_type": "py"}
        )
    """
    
    def __init__(self, config: Optional[HybridConfig] = None):
        self.config = config or HybridConfig()
        self._vector_search = None
        self._bm25_search = None
        self._normalizer = ScoreNormalizer()
    
    def set_vector_search(self, search_fn: Callable[[str, int], List[Tuple[str, float]]]) -> None:
        """
        Set vector search function.
        
        Args:
            search_fn: Function (query, k) -> [(doc_id, score), ...]
        """
        self._vector_search = search_fn
    
    def set_bm25_search(self, search_fn: Callable[[str, int], List[Tuple[str, float]]]) -> None:
        """
        Set BM25 search function.
        
        Args:
            search_fn: Function (query, k) -> [(doc_id, score), ...]
        """
        self._bm25_search = search_fn
    
    def search(
        self,
        query: str,
        k: int = 10,
        vector_k: Optional[int] = None,
        bm25_k: Optional[int] = None,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[HybridResult]:
        """
        Perform hybrid search.
        
        Args:
            query: Search query
            k: Number of results to return
            vector_k: Number of vector results to fetch (default: k * 2)
            bm25_k: Number of BM25 results to fetch (default: k * 2)
            filters: Optional filters to apply
            
        Returns:
            List of HybridResult sorted by combined score
        """
        vector_k = vector_k or k * 2
        bm25_k = bm25_k or k * 2
        
        # Get results from both systems
        vector_results = self._get_vector_results(query, vector_k)
        bm25_results = self._get_bm25_results(query, bm25_k)
        
        # Normalize scores
        if self.config.normalize_scores:
            vector_results = self._normalize_results(vector_results)
            bm25_results = self._normalize_results(bm25_results)
        
        # Fuse results
        fused = self._fuse_results(vector_results, bm25_results)
        
        # Apply filters
        if filters:
            fused = self._apply_filters(fused, filters)
        
        # Filter by minimum score
        fused = [r for r in fused if r.combined_score >= self.config.min_score]
        
        # Sort and limit
        fused.sort(key=lambda x: x.combined_score, reverse=True)
        
        return fused[:k]
    
    def _get_vector_results(
        self, 
        query: str, 
        k: int
    ) -> List[Tuple[str, float, int]]:
        """Get vector search results with ranks."""
        if self._vector_search is None:
            return []
        
        try:
            results = self._vector_search(query, k)
            # Add rank
            return [(doc_id, score, rank + 1) for rank, (doc_id, score) in enumerate(results)]
        except Exception as e:
            logger.warning(f"Vector search failed: {e}")
            return []
    
    def _get_bm25_results(
        self, 
        query: str, 
        k: int
    ) -> List[Tuple[str, float, int]]:
        """Get BM25 search results with ranks."""
        if self._bm25_search is None:
            return []
        
        try:
            results = self._bm25_search(query, k)
            # Add rank
            return [(doc_id, score, rank + 1) for rank, (doc_id, score) in enumerate(results)]
        except Exception as e:
            logger.warning(f"BM25 search failed: {e}")
            return []
    
    def _normalize_results(
        self, 
        results: List[Tuple[str, float, int]]
    ) -> List[Tuple[str, float, int]]:
        """Normalize scores."""
        if not results:
            return results
        
        scores = [score for _, score, _ in results]
        normalized = self._normalizer.min_max(scores)
        
        return [
            (doc_id, norm_score, rank)
            for (doc_id, _, rank), norm_score in zip(results, normalized)
        ]
    
    def _fuse_results(
        self,
        vector_results: List[Tuple[str, float, int]],
        bm25_results: List[Tuple[str, float, int]]
    ) -> List[HybridResult]:
        """Fuse results from both search methods."""
        
        if self.config.fusion_strategy == FusionStrategy.RRF:
            return self._rrf_fusion(vector_results, bm25_results)
        elif self.config.fusion_strategy == FusionStrategy.MAX_SCORE:
            return self._max_score_fusion(vector_results, bm25_results)
        else:
            return self._weighted_sum_fusion(vector_results, bm25_results)
    
    def _weighted_sum_fusion(
        self,
        vector_results: List[Tuple[str, float, int]],
        bm25_results: List[Tuple[str, float, int]]
    ) -> List[HybridResult]:
        """Weighted sum fusion."""
        combined: Dict[str, HybridResult] = {}
        
        # Add vector results
        for doc_id, score, rank in vector_results:
            if doc_id not in combined:
                combined[doc_id] = HybridResult(
                    doc_id=doc_id,
                    combined_score=0.0,
                    vector_score=score,
                    vector_rank=rank
                )
            combined[doc_id].combined_score += score * self.config.vector_weight
            combined[doc_id].vector_score = score
            combined[doc_id].vector_rank = rank
        
        # Add BM25 results
        for doc_id, score, rank in bm25_results:
            if doc_id not in combined:
                combined[doc_id] = HybridResult(
                    doc_id=doc_id,
                    combined_score=0.0,
                    bm25_score=score,
                    bm25_rank=rank
                )
            combined[doc_id].combined_score += score * self.config.bm25_weight
            combined[doc_id].bm25_score = score
            combined[doc_id].bm25_rank = rank
        
        return list(combined.values())
    
    def _rrf_fusion(
        self,
        vector_results: List[Tuple[str, float, int]],
        bm25_results: List[Tuple[str, float, int]]
    ) -> List[HybridResult]:
        """
        Reciprocal Rank Fusion.
        
        RRF(d) = Σ 1 / (k + rank(d))
        where k is a constant (default 60)
        """
        k = self.config.rrf_k
        combined: Dict[str, HybridResult] = {}
        
        # Add vector results with RRF score
        for doc_id, score, rank in vector_results:
            rrf_score = 1.0 / (k + rank)
            
            if doc_id not in combined:
                combined[doc_id] = HybridResult(
                    doc_id=doc_id,
                    combined_score=0.0,
                    vector_score=score,
                    vector_rank=rank
                )
            combined[doc_id].combined_score += rrf_score
            combined[doc_id].vector_score = score
            combined[doc_id].vector_rank = rank
        
        # Add BM25 results with RRF score
        for doc_id, score, rank in bm25_results:
            rrf_score = 1.0 / (k + rank)
            
            if doc_id not in combined:
                combined[doc_id] = HybridResult(
                    doc_id=doc_id,
                    combined_score=0.0,
                    bm25_score=score,
                    bm25_rank=rank
                )
            combined[doc_id].combined_score += rrf_score
            combined[doc_id].bm25_score = score
            combined[doc_id].bm25_rank = rank
        
        return list(combined.values())
    
    def _max_score_fusion(
        self,
        vector_results: List[Tuple[str, float, int]],
        bm25_results: List[Tuple[str, float, int]]
    ) -> List[HybridResult]:
        """Max score fusion - take the maximum score from either method."""
        combined: Dict[str, HybridResult] = {}
        
        for doc_id, score, rank in vector_results:
            if doc_id not in combined:
                combined[doc_id] = HybridResult(
                    doc_id=doc_id,
                    combined_score=score,
                    vector_score=score,
                    vector_rank=rank
                )
            else:
                combined[doc_id].combined_score = max(combined[doc_id].combined_score, score)
                combined[doc_id].vector_score = score
                combined[doc_id].vector_rank = rank
        
        for doc_id, score, rank in bm25_results:
            if doc_id not in combined:
                combined[doc_id] = HybridResult(
                    doc_id=doc_id,
                    combined_score=score,
                    bm25_score=score,
                    bm25_rank=rank
                )
            else:
                combined[doc_id].combined_score = max(combined[doc_id].combined_score, score)
                combined[doc_id].bm25_score = score
                combined[doc_id].bm25_rank = rank
        
        return list(combined.values())
    
    def _apply_filters(
        self, 
        results: List[HybridResult],
        filters: Dict[str, Any]
    ) -> List[HybridResult]:
        """Apply metadata filters."""
        filtered = []
        
        for result in results:
            match = True
            for key, value in filters.items():
                if key in result.metadata:
                    if result.metadata[key] != value:
                        match = False
                        break
            
            if match:
                filtered.append(result)
        
        return filtered


# Convenient factory
def create_hybrid_engine(
    vector_weight: float = 0.7,
    bm25_weight: float = 0.3,
    use_rrf: bool = False
) -> HybridSearchEngine:
    """Create configured hybrid search engine."""
    config = HybridConfig(
        vector_weight=vector_weight,
        bm25_weight=bm25_weight,
        fusion_strategy=FusionStrategy.RRF if use_rrf else FusionStrategy.WEIGHTED_SUM
    )
    return HybridSearchEngine(config)
