# HSA v5.0 - Auto Configuration
# =============================================================================
"""
Progressive Enhancement Configuration.

All decisions are made automatically based on environment.
User can override via environment variables or config file.

Tiers:
- Tier 0 (Baseline): CPU only, zero dependencies
- Tier 1 (GPU): Auto-detected when GPU available
- Tier 2 (Distributed): Opt-in via environment variables
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger("hsa.config")


class DeploymentTier(Enum):
    """Deployment tier based on capabilities."""
    BASELINE = 0   # CPU only, zero dependencies
    GPU = 1        # GPU detected, enable acceleration
    DISTRIBUTED = 2  # Enterprise, full stack
    
    @property
    def emoji(self) -> str:
        return {
            DeploymentTier.BASELINE: "🟢",
            DeploymentTier.GPU: "🟡",
            DeploymentTier.DISTRIBUTED: "🔵"
        }[self]
    
    @property
    def description(self) -> str:
        return {
            DeploymentTier.BASELINE: "Baseline (CPU)",
            DeploymentTier.GPU: "GPU Accelerated",
            DeploymentTier.DISTRIBUTED: "Distributed (Enterprise)"
        }[self]


@dataclass
class AutoConfig:
    """
    Progressive Enhancement Configuration.
    
    All decisions are made automatically based on environment.
    User can override via environment variables.
    
    Usage:
        config = AutoConfig.detect()
        print(config.get_tier_name())  # "🟢 Baseline (CPU)"
        
        # Check features
        if config.use_gpu:
            # GPU-accelerated code path
            ...
    
    Environment variables (Tier 2 opt-in):
        HSA_QDRANT_URL: Enable Qdrant (e.g., "http://localhost:6333")
        HSA_REDIS_URL: Enable Redis (e.g., "redis://localhost:6379")
        VOYAGE_API_KEY: Enable VoyageCode3 API
        
    Override variables:
        HSA_FORCE_CPU: "1" to force CPU even if GPU available
        HSA_MAX_MEMORY_GB: Override memory detection
        HSA_LOG_LEVEL: "DEBUG|INFO|WARNING|ERROR"
    """
    
    # === Tier 0: Baseline (always available) ===
    use_tiktoken: bool = True  # ALWAYS - P0 fix
    use_bm25: bool = True      # ALWAYS - no dependencies
    use_treesitter: bool = True  # ALWAYS - fast AST
    use_lru_cache: bool = True  # ALWAYS - in-memory
    use_faiss_flat: bool = True  # ALWAYS - 100% recall
    
    # === Tier 1: GPU (auto-detected) ===
    use_gpu: bool = False       # Auto-detect CUDA/MPS
    use_codesage_large: bool = False  # Large model if GPU
    use_int8_quantization: bool = True  # Save VRAM
    
    # === Tier 2: Distributed (explicit opt-in) ===
    use_qdrant: bool = False    # Opt-in via HSA_QDRANT_URL
    use_redis: bool = False     # Opt-in via HSA_REDIS_URL
    use_voyage_api: bool = False  # Opt-in via VOYAGE_API_KEY
    
    # === Memory budgets (auto-adjusted) ===
    embedding_cache_mb: int = 512
    vector_index_mb: int = 1024
    max_concurrent_files: int = 100
    
    # === External service URLs ===
    qdrant_url: Optional[str] = None
    redis_url: Optional[str] = None
    voyage_api_key: Optional[str] = None
    
    # === Feature flags ===
    enable_hirag: bool = True
    enable_prefetch: bool = True
    enable_merkle: bool = True
    
    @classmethod
    def detect(cls) -> "AutoConfig":
        """
        Auto-detect capabilities and create optimal config.
        
        Returns:
            AutoConfig with optimal settings
        """
        config = cls()
        
        # === Check for force CPU override ===
        if os.getenv("HSA_FORCE_CPU", "").lower() in ("1", "true", "yes"):
            logger.info("HSA_FORCE_CPU set, forcing CPU mode")
            config.use_gpu = False
        else:
            # === TIER 1: GPU Detection ===
            config.use_gpu = cls._detect_gpu()
            
            if config.use_gpu:
                config.use_codesage_large = True
                config.use_int8_quantization = cls._should_use_int8()
                logger.info(f"GPU detected, INT8={config.use_int8_quantization}")
        
        # === TIER 2: External Services (Opt-in) ===
        
        # Qdrant
        qdrant_url = os.getenv("HSA_QDRANT_URL")
        if qdrant_url:
            config.use_qdrant = True
            config.qdrant_url = qdrant_url
            config.use_faiss_flat = False  # Switch to Qdrant
            logger.info(f"Qdrant enabled: {qdrant_url}")
        
        # Redis
        redis_url = os.getenv("HSA_REDIS_URL")
        if redis_url:
            config.use_redis = True
            config.redis_url = redis_url
            logger.info(f"Redis enabled: {redis_url}")
        
        # VoyageCode3 API
        voyage_key = os.getenv("VOYAGE_API_KEY")
        if voyage_key:
            config.use_voyage_api = True
            config.voyage_api_key = voyage_key
            logger.info("VoyageCode3 API enabled")
        
        # === Memory Budget (based on RAM) ===
        max_memory_override = os.getenv("HSA_MAX_MEMORY_GB")
        if max_memory_override:
            available_ram_gb = float(max_memory_override)
        else:
            available_ram_gb = cls._get_available_ram()
        
        if available_ram_gb >= 32:
            config.embedding_cache_mb = 2048
            config.vector_index_mb = 4096
            config.max_concurrent_files = 500
        elif available_ram_gb >= 16:
            config.embedding_cache_mb = 1024
            config.vector_index_mb = 2048
            config.max_concurrent_files = 200
        elif available_ram_gb >= 8:
            config.embedding_cache_mb = 512
            config.vector_index_mb = 1024
            config.max_concurrent_files = 100
        else:
            # Conservative for <8GB RAM
            config.embedding_cache_mb = 256
            config.vector_index_mb = 512
            config.max_concurrent_files = 50
        
        logger.info(
            f"Memory budget: cache={config.embedding_cache_mb}MB, "
            f"index={config.vector_index_mb}MB, "
            f"files={config.max_concurrent_files}"
        )
        
        return config
    
    @staticmethod
    def _detect_gpu() -> bool:
        """Detect GPU availability (CUDA or MPS)."""
        try:
            import torch
            if torch.cuda.is_available():
                return True
            if hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
                return True
        except ImportError:
            pass
        return False
    
    @staticmethod
    def _should_use_int8() -> bool:
        """Use INT8 if VRAM < 12GB."""
        try:
            import torch
            if torch.cuda.is_available():
                vram_gb = torch.cuda.get_device_properties(0).total_memory / 1e9
                return vram_gb < 12
        except:
            pass
        return True  # Default to INT8 (safer)
    
    @staticmethod
    def _get_available_ram() -> float:
        """Get available RAM in GB."""
        try:
            import psutil
            return psutil.virtual_memory().total / 1e9
        except ImportError:
            return 8  # Assume conservative default
    
    def get_tier(self) -> DeploymentTier:
        """Determine current deployment tier."""
        if self.use_qdrant or self.use_redis or self.use_voyage_api:
            return DeploymentTier.DISTRIBUTED
        elif self.use_gpu:
            return DeploymentTier.GPU
        else:
            return DeploymentTier.BASELINE
    
    def get_tier_name(self) -> str:
        """Human-readable tier name with emoji."""
        tier = self.get_tier()
        return f"{tier.emoji} {tier.description}"
    
    def get_embedding_model(self) -> str:
        """Get which embedding model to use."""
        if self.use_voyage_api:
            return "voyage-code-3"
        elif self.use_codesage_large and self.use_gpu:
            return "codesage-v2-large"
        else:
            return "codesage-v2-base"
    
    def get_vector_store(self) -> str:
        """Get which vector store to use."""
        if self.use_qdrant:
            return "qdrant"
        else:
            return "faiss"
    
    def get_cache_backend(self) -> str:
        """Get which cache backend to use."""
        if self.use_redis:
            return "redis"
        else:
            return "lru"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "tier": self.get_tier().name,
            "tier_name": self.get_tier_name(),
            "use_gpu": self.use_gpu,
            "use_qdrant": self.use_qdrant,
            "use_redis": self.use_redis,
            "use_voyage_api": self.use_voyage_api,
            "embedding_model": self.get_embedding_model(),
            "vector_store": self.get_vector_store(),
            "cache_backend": self.get_cache_backend(),
            "embedding_cache_mb": self.embedding_cache_mb,
            "vector_index_mb": self.vector_index_mb,
            "max_concurrent_files": self.max_concurrent_files,
        }
    
    def log_config(self) -> None:
        """Log configuration summary."""
        tier = self.get_tier()
        logger.info(f"HSA v5.0 Configuration: {self.get_tier_name()}")
        logger.info(f"  Embedding: {self.get_embedding_model()}")
        logger.info(f"  Vector Store: {self.get_vector_store()}")
        logger.info(f"  Cache: {self.get_cache_backend()}")
        
        if tier == DeploymentTier.BASELINE:
            logger.info("  Tip: GPU acceleration available if PyTorch+CUDA installed")
        elif tier == DeploymentTier.GPU:
            logger.info("  Tip: Set HSA_QDRANT_URL for persistent vector storage")


# Global cached config
_cached_config: Optional[AutoConfig] = None


def get_config() -> AutoConfig:
    """
    Get cached auto-config.
    
    Detects on first call, returns cached on subsequent calls.
    """
    global _cached_config
    if _cached_config is None:
        _cached_config = AutoConfig.detect()
    return _cached_config


def refresh_config() -> AutoConfig:
    """Force re-detection of config."""
    global _cached_config
    _cached_config = AutoConfig.detect()
    return _cached_config
