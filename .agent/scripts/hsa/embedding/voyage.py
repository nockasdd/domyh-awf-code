# HSA v5.0 - VoyageAI Embedding Client
# =============================================================================
"""
VoyageAI API client for enterprise code embeddings.

Features:
- voyage-code-3 model support
- Rate limiting with backoff
- Budget tracking per request
- Rare language routing
- Batch processing optimization

Environment:
- VOYAGE_API_KEY: VoyageAI API key
- HSA_VOYAGE_MODEL: Model name (default: voyage-code-3)
- HSA_VOYAGE_BUDGET: Monthly budget in USD (default: 100)
"""

from __future__ import annotations

import asyncio
import logging
import os
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

logger = logging.getLogger("hsa.voyage")


@dataclass
class VoyageConfig:
    """Configuration for VoyageAI client."""
    api_key: str = ""
    model: str = "voyage-code-3"
    base_url: str = "https://api.voyageai.com/v1"
    max_batch_size: int = 128
    max_tokens_per_request: int = 120000
    rate_limit_rpm: int = 300
    monthly_budget_usd: float = 100.0
    timeout: float = 30.0
    
    @classmethod
    def from_env(cls) -> "VoyageConfig":
        """Create config from environment variables."""
        return cls(
            api_key=os.environ.get("VOYAGE_API_KEY", ""),
            model=os.environ.get("HSA_VOYAGE_MODEL", "voyage-code-3"),
            monthly_budget_usd=float(os.environ.get("HSA_VOYAGE_BUDGET", "100.0")),
        )


@dataclass
class UsageStats:
    """Track API usage and budget."""
    total_tokens: int = 0
    total_requests: int = 0
    total_cost_usd: float = 0.0
    month_start: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m"))
    
    # Pricing: $0.06 per 1M tokens for voyage-code-3
    COST_PER_1M_TOKENS = 0.06
    
    def add_usage(self, tokens: int) -> None:
        """Record usage."""
        current_month = datetime.now().strftime("%Y-%m")
        
        # Reset if new month
        if current_month != self.month_start:
            self.total_tokens = 0
            self.total_requests = 0
            self.total_cost_usd = 0.0
            self.month_start = current_month
        
        self.total_tokens += tokens
        self.total_requests += 1
        self.total_cost_usd = (self.total_tokens / 1_000_000) * self.COST_PER_1M_TOKENS
    
    def would_exceed_budget(self, estimated_tokens: int, budget: float) -> bool:
        """Check if request would exceed budget."""
        estimated_cost = ((self.total_tokens + estimated_tokens) / 1_000_000) * self.COST_PER_1M_TOKENS
        return estimated_cost > budget


class RateLimiter:
    """Token bucket rate limiter."""
    
    def __init__(self, requests_per_minute: int = 300):
        self.rpm = requests_per_minute
        self.tokens = requests_per_minute
        self.last_refill = time.time()
        self._lock = asyncio.Lock()
    
    async def acquire(self) -> None:
        """Acquire rate limit token."""
        async with self._lock:
            now = time.time()
            
            # Refill tokens
            elapsed = now - self.last_refill
            refill = elapsed * (self.rpm / 60.0)
            self.tokens = min(self.rpm, self.tokens + refill)
            self.last_refill = now
            
            # Wait if no tokens
            if self.tokens < 1:
                wait_time = (1 - self.tokens) * (60.0 / self.rpm)
                await asyncio.sleep(wait_time)
                self.tokens = 1
            
            self.tokens -= 1


class VoyageEmbedder:
    """
    VoyageAI embedding client.
    
    Enterprise-grade code embeddings with:
    - Superior quality for code understanding
    - 1024-dimensional vectors
    - 16K context window
    
    Usage:
        embedder = VoyageEmbedder()
        
        # Single text
        vector = await embedder.embed("def hello(): pass")
        
        # Batch
        vectors = await embedder.embed_batch(["code1", "code2"])
    """
    
    def __init__(self, config: Optional[VoyageConfig] = None):
        self.config = config or VoyageConfig.from_env()
        self._client = None
        self._rate_limiter = RateLimiter(self.config.rate_limit_rpm)
        self._usage = UsageStats()
    
    def _get_client(self):
        """Lazy load client."""
        if self._client is None:
            try:
                import voyageai
                self._client = voyageai.Client(api_key=self.config.api_key)
            except ImportError:
                raise RuntimeError(
                    "voyageai not installed. "
                    "Install with: pip install voyageai>=0.2"
                )
        return self._client
    
    def _estimate_tokens(self, texts: List[str]) -> int:
        """Estimate token count for texts."""
        # Rough estimate: 4 chars per token
        total_chars = sum(len(t) for t in texts)
        return total_chars // 4
    
    async def embed(self, text: str) -> List[float]:
        """Embed single text."""
        vectors = await self.embed_batch([text])
        return vectors[0] if vectors else []
    
    async def embed_batch(
        self,
        texts: List[str],
        input_type: str = "document"
    ) -> List[List[float]]:
        """
        Embed batch of texts.
        
        Args:
            texts: List of texts to embed
            input_type: "document" or "query"
            
        Returns:
            List of embedding vectors
        """
        if not texts:
            return []
        
        if not self.config.api_key:
            raise ValueError("VOYAGE_API_KEY not set")
        
        # Check budget
        estimated_tokens = self._estimate_tokens(texts)
        if self._usage.would_exceed_budget(estimated_tokens, self.config.monthly_budget_usd):
            raise RuntimeError(
                f"Would exceed monthly budget of ${self.config.monthly_budget_usd:.2f}. "
                f"Current usage: ${self._usage.total_cost_usd:.2f}"
            )
        
        client = self._get_client()
        all_vectors = []
        
        # Process in batches
        for i in range(0, len(texts), self.config.max_batch_size):
            batch = texts[i:i + self.config.max_batch_size]
            
            # Rate limit
            await self._rate_limiter.acquire()
            
            try:
                start = time.time()
                
                result = client.embed(
                    texts=batch,
                    model=self.config.model,
                    input_type=input_type,
                )
                
                elapsed_ms = (time.time() - start) * 1000
                
                # Extract vectors
                vectors = [e for e in result.embeddings]
                all_vectors.extend(vectors)
                
                # Track usage
                tokens_used = result.total_tokens
                self._usage.add_usage(tokens_used)
                
                logger.debug(
                    f"Voyage embed: {len(batch)} texts, {tokens_used} tokens, "
                    f"{elapsed_ms:.2f}ms, ${self._usage.total_cost_usd:.4f} MTD"
                )
                
            except Exception as e:
                logger.error(f"Voyage API error: {e}")
                
                # Retry with exponential backoff
                for retry in range(3):
                    wait = (2 ** retry) + (0.1 * retry)
                    await asyncio.sleep(wait)
                    
                    try:
                        result = client.embed(
                            texts=batch,
                            model=self.config.model,
                            input_type=input_type,
                        )
                        vectors = [e for e in result.embeddings]
                        all_vectors.extend(vectors)
                        self._usage.add_usage(result.total_tokens)
                        break
                    except Exception:
                        if retry == 2:
                            raise
        
        return all_vectors
    
    async def embed_query(self, query: str) -> List[float]:
        """Embed search query (optimized for retrieval)."""
        vectors = await self.embed_batch([query], input_type="query")
        return vectors[0] if vectors else []
    
    def get_usage(self) -> Dict[str, Any]:
        """Get usage statistics."""
        return {
            "total_tokens": self._usage.total_tokens,
            "total_requests": self._usage.total_requests,
            "total_cost_usd": self._usage.total_cost_usd,
            "month": self._usage.month_start,
            "budget_remaining": self.config.monthly_budget_usd - self._usage.total_cost_usd,
        }
    
    @property
    def dimension(self) -> int:
        """Vector dimension."""
        return 1024  # voyage-code-3 outputs 1024-dim vectors


# Language routing for Voyage
RARE_LANGUAGES = {
    "cobol", "fortran", "pascal", "ada", "lisp", "scheme",
    "prolog", "erlang", "haskell", "ocaml", "f#", "clojure",
    "racket", "julia", "r", "matlab", "sas", "stata",
    "verilog", "vhdl", "tcl", "awk", "sed", "perl6",
}


def should_use_voyage(file_path: str, content: str) -> bool:
    """
    Determine if VoyageAI should be used for this file.
    
    Uses Voyage for:
    - Rare languages that local models may struggle with
    - Very long files (better context window)
    - When local embedding quality is insufficient
    """
    # Check file extension
    ext = file_path.rsplit(".", 1)[-1].lower() if "." in file_path else ""
    
    # Rare language routing
    if ext in RARE_LANGUAGES:
        return True
    
    # Long file routing (>10K tokens estimated)
    if len(content) > 40000:  # ~10K tokens
        return True
    
    return False


def is_voyage_enabled() -> bool:
    """Check if VoyageAI is enabled via environment."""
    return bool(os.environ.get("VOYAGE_API_KEY"))


async def get_voyage_embedder() -> Optional[VoyageEmbedder]:
    """Get Voyage embedder if enabled."""
    if not is_voyage_enabled():
        return None
    
    return VoyageEmbedder()
