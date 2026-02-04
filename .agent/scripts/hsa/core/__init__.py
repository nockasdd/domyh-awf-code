# HSA v5.0 Core Module
# =============================================================================
"""
Core functionality for HSA v5.0.

- Capability detection
- Auto configuration
- Progressive enhancement
- GPU memory management
- Resilience patterns (P3.4)
- SSE streaming (P3.5)
"""

from .capabilities import (
    SystemCapabilities,
    GPUInfo,
    get_capabilities,
    refresh_capabilities,
)

from .config import (
    AutoConfig,
    DeploymentTier,
    get_config,
    refresh_config,
)

from .gpu import (
    MemoryStats,
    MemoryBudget,
    GPUMemoryManager,
    FallbackChain,
    BatchProcessor,
    MemoryProfiler,
    get_memory_manager,
)

from .resilience import (
    CircuitState,
    CircuitBreakerConfig,
    CircuitStats,
    CircuitBreaker,
    CircuitOpenError,
    RetryConfig,
    RetryHandler,
    ResilientClient,
    with_circuit_breaker,
    with_retry,
    with_fallback,
)

from .streaming import (
    StreamEventType,
    StreamEvent,
    ProgressInfo,
    StreamController,
    ChunkedContextStream,
    sse_response,
)

__all__ = [
    # Capabilities
    "SystemCapabilities",
    "GPUInfo",
    "get_capabilities",
    "refresh_capabilities",
    # Config
    "AutoConfig",
    "DeploymentTier",
    "get_config",
    "refresh_config",
    # GPU
    "MemoryStats",
    "MemoryBudget",
    "GPUMemoryManager",
    "FallbackChain",
    "BatchProcessor",
    "MemoryProfiler",
    "get_memory_manager",
    # Resilience (P3.4)
    "CircuitState",
    "CircuitBreakerConfig",
    "CircuitStats",
    "CircuitBreaker",
    "CircuitOpenError",
    "RetryConfig",
    "RetryHandler",
    "ResilientClient",
    "with_circuit_breaker",
    "with_retry",
    "with_fallback",
    # Streaming (P3.5)
    "StreamEventType",
    "StreamEvent",
    "ProgressInfo",
    "StreamController",
    "ChunkedContextStream",
    "sse_response",
]


